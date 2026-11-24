// Independently structured bounded end-to-end replay using prime valuations.
// Does not include the producer, use its functions, or read expected answers.
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) try {
    if (argc != 4) throw std::runtime_error("usage: ajt5_valuation_replay MAX_M PRODUCER_DIR OUTPUT_DIR");
    const std::string arg = argv[1];
    if (arg.empty() || arg.find_first_not_of("0123456789") != std::string::npos) throw std::runtime_error("invalid MAX_M");
    const auto limit = std::stoull(arg);
    if (limit < 2 || limit > 10000000) throw std::runtime_error("MAX_M outside bounded campaign");
    const uint32_t end = 5 * limit + 4;
    const std::filesystem::path input = argv[2], output = argv[3];
    std::filesystem::create_directories(output);
    // Boolean prime sieve; eliminate exactly the odd-valuation multiples of
    // every 3 mod 4 prime. Zero remains a sum of two zero squares.
    std::vector<bool> prime(end + 1, true), norm(end + 1, true), ternary(end + 1, false);
    prime[0] = prime[1] = false;
    for (uint64_t p = 2; p <= end; ++p) {
        if (!prime[p]) continue;
        if (p <= end / p)
            for (uint64_t j = p * p; j <= end; j += p) prime[j] = false;
        if (p % 4 != 3) continue;
        uint64_t odd_power = p;
        for (;;) {
            for (uint64_t k = 1; k <= end / odd_power; ++k)
                if (k % p) norm[odd_power * k] = false;
            if (p > end / p || odd_power > end / (p * p)) break;
            odd_power *= p * p;
        }
    }
    // Test each x directly, rather than shifting a bitset.
    std::vector<uint32_t> threes, fives;
    for (uint64_t q = 1;;) {
        threes.push_back(q);
        if (q > end / 3) break;
        q *= 3;
    }
    for (uint64_t q = 1;;) {
        fives.push_back(q);
        if (q > end / 5) break;
        q *= 5;
    }
    for (uint32_t x = 1; x <= end; ++x)
        for (uint32_t q : threes) {
            if (q > x) break;
            if (norm[x - q]) { ternary[x] = true; break; }
        }
    auto compare_bits = [&](const char* file, const std::vector<bool>& values) {
        std::ifstream f(input / file, std::ios::binary);
        if (!f) throw std::runtime_error(std::string("missing ") + file);
        for (uint32_t start = 0; start <= end; start += 8) {
            unsigned char expected = 0;
            for (unsigned b = 0; b < 8 && start + b <= end; ++b)
                if (values[start + b]) expected |= 1u << b;
            const int actual = f.get();
            if (actual != expected) throw std::runtime_error(std::string(file) + " mismatch at byte " + std::to_string(start / 8));
        }
        if (f.get() != EOF) throw std::runtime_error("trailing bitset bytes");
    };
    compare_bits("s2.bits", norm); compare_bits("t.bits", ternary);
    std::ifstream masks(input / "masks.u16le", std::ios::binary);
    if (!masks) throw std::runtime_error("missing masks");
    std::vector<uint16_t> d(end + 1);
    for (uint32_t n = 0; n <= end; ++n) {
        uint16_t value = 0;
        for (unsigned i = 0; i < fives.size() && fives[i] < n; ++i)
            if (ternary[n - fives[i]]) value += uint16_t(1u << i);
        d[n] = value;
        int lo = masks.get(), hi = masks.get();
        if (lo < 0 || hi < 0 || (lo + 256 * hi) != value)
            throw std::runtime_error("D mismatch at n=" + std::to_string(n));
    }
    if (masks.get() != EOF) throw std::runtime_error("trailing mask bytes");
    using C = std::array<uint64_t, 5>;
    C vacuous{}, same_fail{}, plus_fail{}, combined{}, first_same{}, first_plus{}, gate1{}, gate2{}, unique{};
    std::map<int, C> h1, h2, hb;
    std::ofstream hard(output / "hard_cases.csv"), minima(output / "minima.csv"), failures(output / "failures.csv");
    const std::string header = "m,r,n,L,parent_mask,child_mask,runs,defect1,defect2,same_sources,plus_sources,bridge_edges,gate2_hard\n";
    hard << header; minima << "branch," << header; failures << header;
    // Count runs, predecessors and edges by walking individual exponents.
    for (uint32_t m = 2; m <= limit; ++m) {
        int L = 0;
        for (uint32_t q = m; q >= 5; q /= 5) ++L;
        for (int r = 0; r <= 4; ++r) {
            const uint32_t n = 5 * m + r;
            int dc = 0, ec = 0, runs = 0, pc = 0, edges = 0;
            unsigned same = 0, plus = 0;
            for (int j = 0; j <= L + 1; ++j) {
                bool parent = d[m] & (1u << j), child = d[n] & (1u << j);
                dc += parent; ec += child;
                if (parent && (j == 0 || !(d[m] & (1u << (j - 1))))) ++runs;
                if (j <= L && (child || (d[n] & (1u << (j + 1))))) ++pc;
                if (parent && child) { same += 1u << j; ++edges; }
                if (parent && (d[n] & (1u << (j + 1)))) { plus += 1u << j; ++edges; }
            }
            const int defect1 = dc + runs + ec - (L + 2), defect2 = dc + pc - (L + 1);
            ++h1[defect1][r]; ++h2[defect2][r]; ++hb[edges][r];
            if (edges == 1) ++unique[r];
            auto row = [&](std::ostream& f) {
                f << m << ',' << r << ',' << n << ',' << L << ',' << d[m] << ',' << d[n] << ','
                  << runs << ',' << defect1 << ',' << defect2 << ',' << same << ',' << plus << ',' << edges << ',' << (defect2 <= 0) << '\n';
            };
            if (dc == 0) { ++vacuous[r]; continue; }
            if (same == 0) { ++same_fail[r]; if (!first_same[r]) { first_same[r] = m; minima << "same,"; row(minima); } }
            if (plus == 0) { ++plus_fail[r]; if (!first_plus[r]) { first_plus[r] = m; minima << "plus,"; row(minima); } }
            if (edges == 0) { ++combined[r]; row(failures); }
            if (defect1 <= 0) { ++gate1[r]; row(hard); if (defect2 <= 0) ++gate2[r]; }
        }
    }
    std::ofstream f(output / "summary.json");
    f << "{\n\"schema\":1,\"engine\":\"odd-prime-valuation-direct-membership\",\"max_m\":" << limit
      << ",\"max_n\":" << end << ",\"cases\":" << (limit - 1) * 5;
    auto array = [&](const C& c) { f << '['; for (int r = 0; r < 5; ++r) f << (r ? "," : "") << c[r]; f << ']'; };
    auto field = [&](const char* name, const C& c) { f << ",\n\"" << name << "\":"; array(c); };
    field("vacuous", vacuous); field("same_failures", same_fail); field("plus_failures", plus_fail);
    field("combined_failures", combined); field("same_minima", first_same); field("plus_minima", first_plus);
    field("gate1_hard", gate1); field("gate2_hard", gate2); field("unique_bridge_cases", unique);
    auto hist = [&](const char* name, const std::map<int, C>& h) {
        f << ",\n\"" << name << "\":{"; bool first = true;
        for (const auto& [k, c] : h) { f << (first ? "" : ",") << '"' << k << "\":"; array(c); first = false; }
        f << '}';
    };
    hist("defect1_histogram", h1); hist("defect2_histogram", h2); hist("bridge_edge_histogram", hb);
    f << "\n}\n";
    if (!f || !hard || !minima || !failures) throw std::runtime_error("write output");
    std::cout << "independent valuation replay matched all " << end + 1 << " S2, T, and D entries; " << (limit - 1) * 5 << " cases recounted\n";
    return 0;
} catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
