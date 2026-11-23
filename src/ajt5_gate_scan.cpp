// R2 independent postprocessing of R1's canonical, shared exact D table.
// Counts establish sufficient gates without accepting by D & P.
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Counts = std::array<uint64_t, 5>;
static int pc(uint32_t x) { return __builtin_popcount(x); }
// Second arithmetic route walks individual exponents; no popcount, bitwise
// predecessor union, parity masks, or shared gate formula with the fast route.
static std::array<int, 9> literal(uint32_t m, uint32_t L, uint32_t d, uint32_t e) {
    int ds = 0, es = 0, runs = 0, ps = 0, outside = 0;
    int dc[2]{}, ec[2]{}, universe[2]{}, excluded[2]{};
    bool previous = false;
    uint32_t five = 1;
    for (uint32_t i = 0; i <= L; ++i, five *= 5) {
        bool present = (d >> i) & 1;
        bool pred = ((e >> i) & 1) || ((e >> (i + 1)) & 1);
        ++universe[i % 2];
        if (present) { ++ds; ++dc[i % 2]; if (!previous) ++runs; }
        previous = present;
        if (pred) { ++ps; ++ec[i % 2]; }
        if ((m - five) % 36 == 24 && !pred) { ++outside; ++excluded[i % 2]; }
    }
    for (uint32_t i = 0; i <= L + 1; ++i) if ((e >> i) & 1) ++es;
    int k0 = dc[0] + ec[0] - universe[0], k1 = dc[1] + ec[1] - universe[1];
    int q0 = k0 + excluded[0], q1 = k1 + excluded[1];
    return {ds + runs + es - int(L) - 2, ds + ps - int(L) - 1,
            k0, k1, std::max(k0, k1), ds + ps + outside - int(L) - 1,
            q0, q1, std::max(q0, q1)};
}
static void array(std::ostream& out, const Counts& a) {
    out << '[';
    for (int r = 0; r < 5; ++r) out << (r ? "," : "") << a[r];
    out << ']';
}
int main(int argc, char** argv) try {
    if (argc != 4) throw std::runtime_error("usage: ajt5_gate_scan MAX_M MASKS.u16le OUT_DIR");
    std::string arg(argv[1]);
    if (arg.empty() || arg.find_first_not_of("0123456789") != std::string::npos)
        throw std::runtime_error("invalid bound");
    auto bound = std::stoull(arg);
    if (bound < 2 || bound > 10000000) throw std::runtime_error("campaign bound");
    uint32_t max_m = bound, max_n = 5 * max_m + 4;
    std::ifstream in(argv[2], std::ios::binary);
    std::vector<uint16_t> masks(max_n + 1);
    uint32_t max_d = 0;
    for (uint32_t p = 1; p <= max_n / 5; p *= 5) ++max_d;
    for (auto& d : masks) {
        int lo = in.get(), hi = in.get();
        if (lo < 0 || hi < 0) throw std::runtime_error("truncated masks");
        d = uint32_t(lo) | (uint32_t(hi) << 8);
        if (d >> (max_d + 1)) throw std::runtime_error("mask high bits");
    }
    if (in.get() != std::char_traits<char>::eof()) throw std::runtime_error("trailing masks");
    std::filesystem::path out(argv[3]); std::filesystem::create_directories(out);
    std::ofstream critical(out / "critical.csv"), nearest(out / "nearest36.csv"), failure(out / "failures.csv");
    const char* header = "m,r,L,D,E,gF,gB,k0,k1,PB2,delta36,q0,q1,PB36\n";
    critical << header; nearest << header; failure << header;
    std::array<std::array<Counts, 33>, 4> hist{};
    const std::array<std::string, 4> names{"PB2", "delta36", "PB36", "K"};
    Counts vacuous{}, nonvacuous{};
    uint32_t L = 0, next5 = 5;
    for (uint32_t m = 2; m <= max_m; ++m) {
        if (m == next5) { ++L; next5 *= 5; }
        uint32_t u = (1U << (L + 1)) - 1, d = masks[m], f = 0;
        for (uint32_t j = 0, five = 1; j <= L; ++j, five *= 5)
            if ((m - five) % 36 == 24) f |= 1U << j;
        if (d & ~u) throw std::runtime_error("parent exponent domain");
        if (d & f) throw std::runtime_error("mod36 exclusion contradicts exact input");
        for (int r = 0; r < 5; ++r) {
            uint32_t e = masks[5 * m + r];
            if (e >> (L + 2)) throw std::runtime_error("child exponent domain");
            if (!d) { ++vacuous[r]; continue; }
            ++nonvacuous[r];
            uint32_t p = (e | (e >> 1)) & u;
            int gf = pc(d) + pc(d & ~(d << 1)) + pc(e) - int(L + 2);
            int gb = pc(d) + pc(p) - int(L + 1);
            int k[2], q[2];
            for (int b = 0; b < 2; ++b) {
                uint32_t parity = u & (b ? 0xaaaaU : 0x5555U);
                k[b] = pc(d & parity) + pc(p & parity) - pc(parity);
                q[b] = k[b] + pc(f & ~p & parity);
            }
            int pb = std::max(k[0], k[1]), delta = gb + pc(f & ~p), pb36 = std::max(q[0], q[1]);
            if (literal(m, L, d, e) != std::array<int, 9>{gf, gb, k[0], k[1], pb, delta, q[0], q[1], pb36})
                throw std::runtime_error("R2 arithmetic mismatch at " + std::to_string(m) + "," + std::to_string(r));
            const std::array<int, 4> values{pb, delta, pb36, std::max(gf, pb)};
            for (int i = 0; i < 4; ++i) {
                if (values[i] < -16 || values[i] > 16) throw std::runtime_error("histogram range");
                ++hist[i][values[i] + 16][r];
            }
            auto row = [&](std::ostream& s) {
                s << m << ',' << r << ',' << L << ',' << d << ',' << e << ',' << gf << ',' << gb << ','
                  << k[0] << ',' << k[1] << ',' << pb << ',' << delta << ',' << q[0] << ',' << q[1] << ',' << pb36 << '\n';
            };
            if (pb <= 1) row(critical);
            if (pb36 <= 1) row(nearest);
            if (pb <= 0) row(failure);
        }
    }
    std::ofstream s(out / "summary.json");
    s << "{\"max_m\":" << max_m << ",\"max_n\":" << max_n << ",\"nonvacuous\":"; array(s, nonvacuous);
    s << ",\"vacuous\":"; array(s, vacuous);
    for (int i = 0; i < 4; ++i) {
        s << ",\"" << names[i] << "\":{"; bool first = true;
        for (int bin = 0; bin < 33; ++bin) {
            const auto& counts = hist[i][bin];
            if (counts == Counts{}) continue;
            const int value = bin - 16;
            s << (first ? "" : ",") << '"' << value << "\":"; array(s, counts); first = false;
        }
        s << '}';
    }
    s << "}\n";
    if (!s || !critical || !nearest || !failure) throw std::runtime_error("write error");
    std::cout << "postprocessed " << uint64_t(max_m - 1) * 5 << " shared-input pairs\n";
    return 0;
} catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
