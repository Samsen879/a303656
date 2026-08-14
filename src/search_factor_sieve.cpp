// Exact all-prime segmented factor-sieve search for bounded A303656 certificates.
//
// For each positive remainder r in a contiguous range, this program factors r
// exactly by segmented trial division with every prime <= sqrt(max_r).  It marks
// r iff some prime p == 3 (mod 4) occurs with an allowed odd valuation.  Thus
// --max-odd 1 searches the unrestricted valuation-one certificate family; no
// finite prime pool truncation is involved.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct PairShift { int c; int d; uint64_t s; };

static uint64_t checked_pow(uint64_t b, int e) {
    __uint128_t x = 1;
    for (int i = 0; i < e; ++i) {
        x *= b;
        if (x > std::numeric_limits<uint64_t>::max()) throw std::runtime_error("power overflow");
    }
    return static_cast<uint64_t>(x);
}

static uint64_t isqrt_u64(uint64_t n) {
    // Pure-integer binary search.  No floating-point sqrt is used.
    uint64_t lo = 0;
    uint64_t hi = std::min<uint64_t>(n, 0xffffffffULL);
    while (lo < hi) {
        uint64_t mid = lo + (hi - lo + 1) / 2;
        if (mid <= n / mid) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}

static std::vector<uint32_t> primes_up_to(uint64_t limit64) {
    if (limit64 > std::numeric_limits<uint32_t>::max()) throw std::runtime_error("prime sieve limit too large");
    uint32_t limit = static_cast<uint32_t>(limit64);
    std::vector<uint8_t> composite(static_cast<size_t>(limit) + 1, 0);
    std::vector<uint32_t> primes;
    for (uint32_t x = 2; x <= limit; ++x) {
        if (!composite[x]) {
            primes.push_back(x);
            if (static_cast<uint64_t>(x) * x <= limit) {
                for (uint64_t y = static_cast<uint64_t>(x) * x; y <= limit; y += x) composite[static_cast<size_t>(y)] = 1;
            }
        }
    }
    return primes;
}

static bool allowed_valuation(unsigned e, int max_odd) {
    return (e & 1U) && (max_odd < 0 || static_cast<int>(e) <= max_odd);
}

struct FactorStats {
    uint64_t range_low = 0;
    uint64_t range_high = 0;
    uint64_t values = 0;
    uint64_t prime_multiple_visits = 0;
    uint64_t division_steps = 0;
    uint64_t marked = 0;
};

static std::vector<uint8_t> classify_range(
    uint64_t lo,
    uint64_t hi,
    const std::vector<uint32_t>& primes,
    int max_odd,
    FactorStats& stats
) {
    if (lo < 1 || lo > hi) throw std::runtime_error("invalid positive factor range");
    uint64_t len64 = hi - lo + 1;
    if (len64 > static_cast<uint64_t>(std::numeric_limits<size_t>::max())) throw std::runtime_error("range too large for memory");
    size_t len = static_cast<size_t>(len64);
    std::vector<uint64_t> residual(len);
    std::vector<uint8_t> good(len, 0);
    for (size_t i = 0; i < len; ++i) residual[i] = lo + static_cast<uint64_t>(i);

    uint64_t root = isqrt_u64(hi);
    for (uint32_t p32 : primes) {
        uint64_t p = p32;
        if (p > root) break;
        uint64_t rem = lo % p;
        uint64_t first = rem == 0 ? lo : lo + (p - rem);
        for (uint64_t m = first; m <= hi; ) {
            size_t idx = static_cast<size_t>(m - lo);
            ++stats.prime_multiple_visits;
            unsigned e = 0;
            while (residual[idx] % p == 0) {
                residual[idx] /= p;
                ++e;
                ++stats.division_steps;
            }
            if ((p & 3U) == 3U && allowed_valuation(e, max_odd)) good[idx] = 1;
            if (hi - m < p) break;
            m += p;
        }
    }
    // After removing every prime <= sqrt(hi), any residual > 1 is prime and
    // occurs to exponent exactly one.
    if (max_odd < 0 || max_odd >= 1) {
        for (size_t i = 0; i < len; ++i) {
            uint64_t q = residual[i];
            if (q > 1 && (q & 3U) == 3U) good[i] = 1;
        }
    }
    stats.range_low = lo;
    stats.range_high = hi;
    stats.values = len64;
    for (uint8_t x : good) stats.marked += x != 0;
    return good;
}

static uint64_t popcount_bits(const std::vector<uint64_t>& bits) {
    uint64_t z = 0;
    for (uint64_t w : bits) z += static_cast<uint64_t>(__builtin_popcountll(w));
    return z;
}

int main(int argc, char** argv) {
    try {
        uint64_t low = 0, high = 0, group_span = 1000000;
        int C = -1, D = -1, max_odd = 1;
        std::string json_path, candidates_path;
        bool quiet = false;
        for (int i = 1; i < argc; ++i) {
            std::string a = argv[i];
            auto need = [&]() -> std::string {
                if (++i >= argc) throw std::runtime_error("missing argument value");
                return argv[i];
            };
            if (a == "--low") low = std::stoull(need());
            else if (a == "--high") high = std::stoull(need());
            else if (a == "--C") C = std::stoi(need());
            else if (a == "--D") D = std::stoi(need());
            else if (a == "--group-span") group_span = std::stoull(need());
            else if (a == "--max-odd") max_odd = std::stoi(need());
            else if (a == "--json") json_path = need();
            else if (a == "--candidates") candidates_path = need();
            else if (a == "--quiet") quiet = true;
            else throw std::runtime_error("unknown argument: " + a);
        }
        if (low < 2 || high < low || C < 0 || D < 0 || group_span == 0 || json_path.empty()) {
            throw std::runtime_error("required: --low --high --C --D --json; low >= 2");
        }
        if (!(max_odd == -1 || (max_odd >= 1 && (max_odd & 1)))) {
            throw std::runtime_error("--max-odd must be -1 (all odd) or a positive odd integer");
        }
        uint64_t cap3 = checked_pow(3, C + 1);
        uint64_t cap5 = checked_pow(5, D + 1);
        if (high >= cap3 + 1) throw std::runtime_error("N_high < 3^(C+1)+1 check failed");
        if (high >= cap5 + 1) throw std::runtime_error("N_high < 5^(D+1)+1 check failed");

        std::vector<uint64_t> p3(C + 1), p5(D + 1);
        p3[0] = p5[0] = 1;
        for (int c = 1; c <= C; ++c) p3[c] = p3[c - 1] * 3;
        for (int d = 1; d <= D; ++d) p5[d] = p5[d - 1] * 5;
        std::map<uint64_t, std::vector<std::pair<int,int>>> by_shift;
        for (int c = 0; c <= C; ++c) {
            for (int d = 0; d <= D; ++d) {
                __uint128_t z = static_cast<__uint128_t>(p3[c]) + p5[d];
                if (z <= high) by_shift[static_cast<uint64_t>(z)].push_back({c,d});
            }
        }
        std::vector<uint64_t> shifts;
        shifts.reserve(by_shift.size());
        uint64_t pair_count = 0;
        for (auto const& kv : by_shift) { shifts.push_back(kv.first); pair_count += kv.second.size(); }

        auto primes = primes_up_to(isqrt_u64(high - shifts.front()));
        uint64_t ncount = high - low + 1;
        size_t words = static_cast<size_t>((ncount + 63) / 64);
        std::vector<uint64_t> alive(words, ~uint64_t(0));
        if (ncount % 64) alive.back() = (uint64_t(1) << (ncount % 64)) - 1;
        std::vector<uint64_t> first_failure(shifts.size(), 0);
        std::vector<FactorStats> group_stats;
        uint64_t shifts_processed = 0;
        auto t0 = std::chrono::steady_clock::now();

        size_t gi = 0;
        while (gi < shifts.size() && popcount_bits(alive) != 0) {
            uint64_t min_s = shifts[gi];
            size_t gj = gi;
            while (gj + 1 < shifts.size() && shifts[gj + 1] - min_s <= group_span) ++gj;
            uint64_t max_s = shifts[gj];
            uint64_t rlo = low > max_s ? low - max_s : 1;
            uint64_t rhi = high - min_s;
            FactorStats fs;
            auto good = classify_range(rlo, rhi, primes, max_odd, fs);
            group_stats.push_back(fs);

            for (size_t si = gi; si <= gj && popcount_bits(alive) != 0; ++si) {
                uint64_t s = shifts[si];
                for (size_t wi = 0; wi < alive.size(); ++wi) {
                    uint64_t w = alive[wi];
                    while (w) {
                        unsigned bit = static_cast<unsigned>(__builtin_ctzll(w));
                        uint64_t idxn = static_cast<uint64_t>(wi) * 64 + bit;
                        if (idxn >= ncount) break;
                        uint64_t n = low + idxn;
                        bool ok = true;
                        if (n >= s) {
                            if (n == s) ok = false;
                            else {
                                uint64_t r = n - s;
                                if (r < rlo || r > rhi) throw std::runtime_error("internal factor-range indexing error");
                                ok = good[static_cast<size_t>(r - rlo)] != 0;
                            }
                        }
                        if (!ok) {
                            alive[wi] &= ~(uint64_t(1) << bit);
                            ++first_failure[si];
                        }
                        w &= w - 1;
                    }
                }
                ++shifts_processed;
                if (!quiet) {
                    std::cout << "SHIFT s=" << s << " survivors=" << popcount_bits(alive) << "\n";
                }
            }
            gi = gj + 1;
        }

        std::vector<uint64_t> candidates;
        for (size_t wi = 0; wi < alive.size(); ++wi) {
            uint64_t w = alive[wi];
            while (w) {
                unsigned bit = static_cast<unsigned>(__builtin_ctzll(w));
                uint64_t idx = static_cast<uint64_t>(wi) * 64 + bit;
                if (idx < ncount) candidates.push_back(low + idx);
                w &= w - 1;
            }
        }
        double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();

        if (!candidates_path.empty()) {
            std::ofstream cf(candidates_path);
            if (!cf) throw std::runtime_error("cannot write candidates file");
            for (uint64_t n : candidates) cf << n << '\n';
        }
        std::ofstream js(json_path);
        if (!js) throw std::runtime_error("cannot write JSON");
        js << "{\n";
        js << "  \"method\": \"exact_all_prime_segmented_factor_sieve\",\n";
        js << "  \"low\": \"" << low << "\",\n  \"high\": \"" << high << "\",\n";
        js << "  \"C\": " << C << ",\n  \"D\": " << D << ",\n";
        js << "  \"finite_bound_3_rhs\": \"" << cap3 + 1 << "\",\n";
        js << "  \"finite_bound_5_rhs\": \"" << cap5 + 1 << "\",\n";
        js << "  \"max_odd\": " << max_odd << ",\n";
        js << "  \"certificate_family\": \"" << (max_odd == 1 ? "all primes p=3 mod 4 with v_p=1" : (max_odd < 0 ? "all primes p=3 mod 4 with arbitrary odd v_p" : "all primes p=3 mod 4 with odd v_p <= max_odd")) << "\",\n";
        js << "  \"admissible_pair_count_at_high\": " << pair_count << ",\n";
        js << "  \"distinct_shift_count_at_high\": " << shifts.size() << ",\n";
        js << "  \"integers_tested\": " << ncount << ",\n";
        js << "  \"shifts_processed_before_termination\": " << shifts_processed << ",\n";
        js << "  \"factor_groups_processed\": " << group_stats.size() << ",\n";
        js << "  \"candidate_count\": " << candidates.size() << ",\n  \"candidates\": [";
        for (size_t i = 0; i < candidates.size(); ++i) { if (i) js << ','; js << '"' << candidates[i] << '"'; }
        js << "],\n  \"first_failure_histogram\": [";
        bool first = true;
        for (size_t i = 0; i < shifts.size(); ++i) if (first_failure[i]) {
            if (!first) js << ',';
            first = false;
            js << "{\"shift\":\"" << shifts[i] << "\",\"count\":" << first_failure[i] << "}";
        }
        js << "],\n  \"factor_groups\": [";
        for (size_t i = 0; i < group_stats.size(); ++i) {
            if (i) js << ',';
            auto const& f = group_stats[i];
            js << "{\"low\":\"" << f.range_low << "\",\"high\":\"" << f.range_high
               << "\",\"values\":" << f.values << ",\"prime_multiple_visits\":" << f.prime_multiple_visits
               << ",\"division_steps\":" << f.division_steps << ",\"marked\":" << f.marked << "}";
        }
        js << "],\n  \"elapsed_seconds\": " << elapsed << ",\n";
        js << "  \"classification\": \"" << (candidates.empty() ? "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE STATED ALL-PRIME CERTIFICATE FAMILY" : "CANDIDATES REQUIRE INDEPENDENT VERIFICATION") << "\"\n}\n";

        std::cout << "integers_tested=" << ncount << "\n";
        std::cout << "admissible_pair_count_at_high=" << pair_count << "\n";
        std::cout << "distinct_shift_count_at_high=" << shifts.size() << "\n";
        std::cout << "shifts_processed_before_termination=" << shifts_processed << "\n";
        std::cout << "candidate_count=" << candidates.size() << "\n";
        std::cout << "elapsed_seconds=" << elapsed << "\n";
        std::cout << (candidates.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << "\n";
        return 0;
    } catch (std::exception const& e) {
        std::cerr << "ERROR " << e.what() << "\n";
        return 2;
    }
}
