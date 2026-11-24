// Bounded AJT5 replay. No reference answers are inputs to this program.
// C++17; exact integer arithmetic, including at zero and power boundaries.
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using U = uint32_t;
using Bits = std::vector<uint64_t>;
using Counts = std::array<uint64_t, 5>;

static std::vector<U> powers(U base, U limit) {
    std::vector<U> v;
    for (U p = 1; p <= limit;) {
        v.push_back(p);
        if (p > limit / base) break;
        p *= base;
    }
    return v;
}
static bool bit(const Bits& v, U n) { return (v[n / 64] >> (n % 64)) & 1; }
static int count(U n) { return __builtin_popcount(n); }
static void write_bits(const std::filesystem::path& p, const Bits& v, U last) {
    std::ofstream f(p, std::ios::binary);
    // Canonical bytes, independent of machine endianness; unused tail bits zero.
    for (U i = 0; i <= last / 8; ++i) {
        auto b = static_cast<unsigned char>(v[i / 8] >> (8 * (i % 8)));
        f.put(static_cast<char>(b));
    }
    if (!f) throw std::runtime_error("write bits");
}
static void array_json(std::ostream& f, const Counts& v) {
    f << '[';
    for (int r = 0; r < 5; ++r) f << (r ? "," : "") << v[r];
    f << ']';
}
static void hist_json(std::ostream& f, const std::map<int, Counts>& h) {
    f << '{'; bool first = true;
    for (const auto& [k, v] : h) {
        f << (first ? "" : ",") << '"' << k << "\":";
        array_json(f, v); first = false;
    }
    f << '}';
}

int main(int argc, char** argv) try {
    if (argc != 3) throw std::runtime_error("usage: ajt5_scan MAX_M OUTPUT_DIR (2..10000000)");
    const std::string arg = argv[1];
    if (arg.empty() || arg.find_first_not_of("0123456789") != std::string::npos)
        throw std::runtime_error("invalid MAX_M");
    const auto parsed = std::stoull(arg);
    if (parsed < 2 || parsed > 10000000) throw std::runtime_error("MAX_M outside bounded campaign");
    const U max_m = static_cast<U>(parsed), max_n = 5 * max_m + 4;
    const std::filesystem::path out = argv[2];
    std::filesystem::create_directories(out);
    const auto p3 = powers(3, max_n), p5 = powers(5, max_n);
    Bits s2(max_n / 64 + 1), t(s2.size());
    // All unordered nonnegative square pairs, including (0,0).
    for (U a = 0; uint64_t(a) * a <= max_n; ++a) {
        const U aa = a * a;
        for (U b = a; uint64_t(b) * b <= max_n - aa; ++b) {
            const U n = aa + b * b;
            s2[n / 64] |= uint64_t(1) << (n % 64);
        }
    }
    // T(x) iff x = a^2+b^2+3^c; source s2 is immutable.
    for (U p : p3) {
        const U words = p / 64, shift = p % 64;
        for (size_t i = 0; i + words < t.size(); ++i) {
            t[i + words] |= s2[i] << shift;
            if (shift && i + words + 1 < t.size())
                t[i + words + 1] |= s2[i] >> (64 - shift);
        }
    }
    const U tail = (max_n + 1) % 64;
    if (tail) t.back() &= (uint64_t(1) << tail) - 1;
    std::vector<uint16_t> masks(max_n + 1);
    // Deliberately materialize all masks, so the distinct replay can compare
    // every n rather than just a hash or selected successes.
    for (U d = 0; d < p5.size(); ++d)
        for (U n = p5[d]; n <= max_n; ++n)
            if (bit(t, n - p5[d])) masks[n] |= U(1) << d;
    write_bits(out / "s2.bits", s2, max_n);
    write_bits(out / "t.bits", t, max_n);
    {
        std::ofstream f(out / "masks.u16le", std::ios::binary);
        for (auto mask : masks) { f.put(char(mask & 255)); f.put(char(mask >> 8)); }
        if (!f) throw std::runtime_error("write masks");
    }
    std::ofstream hard(out / "hard_cases.csv"), minima(out / "minima.csv"), failures(out / "failures.csv");
    const std::string header = "m,r,n,L,parent_mask,child_mask,runs,defect1,defect2,same_sources,plus_sources,bridge_edges,gate2_hard\n";
    hard << header; minima << "branch," << header; failures << header;
    Counts same_fail{}, plus_fail{}, combined_fail{}, vacuous{}, gate1{}, gate2{}, unique{};
    Counts same_min{}, plus_min{};
    std::map<int, Counts> defect1_hist, defect2_hist, bridge_hist;
    U level = 0;
    for (U m = 2; m <= max_m; ++m) {
        while (level + 1 < p5.size() && p5[level + 1] <= m) ++level;
        const U d = masks[m];
        const int runs = count(d & ~(d << 1));
        for (U r = 0; r < 5; ++r) {
            const U n = 5 * m + r, e = masks[n];
            const U same = d & e, plus = d & (e >> 1);
            const int b = count(same) + count(plus);
            const int g1 = count(d) + runs + count(e) - int(level + 2);
            const U pred = (e | (e >> 1)) & ((U(1) << (level + 1)) - 1);
            const int g2 = count(d) + count(pred) - int(level + 1);
            auto row = [&](std::ostream& f) {
                f << m << ',' << r << ',' << n << ',' << level << ',' << d << ',' << e << ','
                  << runs << ',' << g1 << ',' << g2 << ',' << same << ',' << plus << ',' << b << ',' << (g2 <= 0) << '\n';
            };
            // Histograms include vacuous cases; scoped failure counts do not.
            ++defect1_hist[g1][r]; ++defect2_hist[g2][r]; ++bridge_hist[b][r];
            if (b == 1) ++unique[r];
            if (!d) { ++vacuous[r]; continue; }
            if (!same) {
                ++same_fail[r];
                if (!same_min[r]) { same_min[r] = m; minima << "same,"; row(minima); }
            }
            if (!plus) {
                ++plus_fail[r];
                if (!plus_min[r]) { plus_min[r] = m; minima << "plus,"; row(minima); }
            }
            if (!b) { ++combined_fail[r]; row(failures); }
            if (g1 <= 0) {
                ++gate1[r]; row(hard);
                if (g2 <= 0) ++gate2[r];
            }
        }
    }
    if (!hard || !minima || !failures) throw std::runtime_error("write CSV");
    std::ofstream f(out / "summary.json");
    f << "{\n\"schema\":1,\"engine\":\"square-enumeration-shift-union\",\"max_m\":" << max_m
      << ",\"max_n\":" << max_n << ",\"cases\":" << uint64_t(max_m - 1) * 5;
    auto field = [&](const char* name, const Counts& value) { f << ",\n\"" << name << "\":"; array_json(f, value); };
    field("vacuous", vacuous); field("same_failures", same_fail); field("plus_failures", plus_fail);
    field("combined_failures", combined_fail); field("same_minima", same_min); field("plus_minima", plus_min);
    field("gate1_hard", gate1); field("gate2_hard", gate2); field("unique_bridge_cases", unique);
    f << ",\n\"defect1_histogram\":"; hist_json(f, defect1_hist);
    f << ",\n\"defect2_histogram\":"; hist_json(f, defect2_hist);
    f << ",\n\"bridge_edge_histogram\":"; hist_json(f, bridge_hist);
    f << "\n}\n";
    if (!f) throw std::runtime_error("write summary");
    std::cout << "completed " << uint64_t(max_m - 1) * 5 << " cases; max_n=" << max_n << '\n';
    return 0;
} catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
