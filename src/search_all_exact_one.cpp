// Exact exhaustive search for the valuation-one certificate using ALL possible
// obstruction primes p == 3 (mod 4), not a preselected finite pool.
//
// For each remainder interval [A,B] this program factors every integer by a
// segmented sieve using all primes <= floor(sqrt(B)).  It marks r precisely
// when at least one p == 3 (mod 4) occurs with exponent exactly one.  Any
// residual factor after the sieve is a prime > sqrt(B), hence has exponent one.
// Shifted packed-bit intersections then test a prefix of active shifts; every
// survivor is independently factored against every active shift.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

uint64_t isqrt_u64(uint64_t n) {
    uint64_t lo = 0;
    uint64_t hi = std::min<uint64_t>(n, uint64_t(1) << 32);
    while (lo < hi) {
        uint64_t mid = lo + (hi - lo + 1) / 2;
        if (mid <= n / mid) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}

std::vector<uint32_t> prime_sieve(uint64_t limit64) {
    if (limit64 > std::numeric_limits<uint32_t>::max()) {
        throw std::runtime_error("prime-sieve limit exceeds uint32");
    }
    uint32_t limit = static_cast<uint32_t>(limit64);
    std::vector<bool> composite(static_cast<size_t>(limit) + 1, false);
    std::vector<uint32_t> primes;
    for (uint32_t i = 2; i <= limit; ++i) {
        if (!composite[i]) {
            primes.push_back(i);
            if (uint64_t(i) * i <= limit) {
                for (uint64_t j = uint64_t(i) * i; j <= limit; j += i) {
                    composite[static_cast<size_t>(j)] = true;
                }
            }
        }
    }
    return primes;
}

uint64_t ipow(uint64_t base, int exponent) {
    __uint128_t x = 1;
    for (int i = 0; i < exponent; ++i) {
        x *= base;
        if (x > std::numeric_limits<uint64_t>::max()) throw std::runtime_error("power overflow");
    }
    return static_cast<uint64_t>(x);
}

inline void set_bit(std::vector<uint64_t>& bits, uint64_t i) {
    bits[static_cast<size_t>(i >> 6)] |= uint64_t(1) << (i & 63U);
}

inline bool get_bit(const std::vector<uint64_t>& bits, uint64_t i) {
    return ((bits[static_cast<size_t>(i >> 6)] >> (i & 63U)) & 1U) != 0;
}

uint64_t slice_word(const std::vector<uint64_t>& bits, uint64_t start) {
    size_t wi = static_cast<size_t>(start >> 6);
    unsigned off = static_cast<unsigned>(start & 63U);
    uint64_t lo = wi < bits.size() ? bits[wi] : 0;
    if (off == 0) return lo;
    uint64_t hi = wi + 1 < bits.size() ? bits[wi + 1] : 0;
    return (lo >> off) | (hi << (64U - off));
}

bool any_bits(const std::vector<uint64_t>& bits) {
    for (uint64_t w : bits) if (w) return true;
    return false;
}

uint64_t popcount_bits(const std::vector<uint64_t>& bits) {
    uint64_t total = 0;
    for (uint64_t w : bits) total += static_cast<uint64_t>(__builtin_popcountll(w));
    return total;
}

struct FactorStats {
    uint64_t division_attempts = 0;
    uint64_t successful_divisions = 0;
    uint64_t exact_one_marks = 0;
    uint64_t large_residual_marks = 0;
};

std::vector<uint64_t> classify_interval(uint64_t A, uint64_t B,
                                        const std::vector<uint32_t>& primes,
                                        FactorStats& stats) {
    if (A < 1 || A > B) throw std::runtime_error("invalid positive factor interval");
    const uint64_t len64 = B - A + 1;
    if (len64 > std::numeric_limits<size_t>::max()) throw std::runtime_error("interval too large");
    const size_t len = static_cast<size_t>(len64);
    std::vector<uint64_t> residual(len);
    for (size_t i = 0; i < len; ++i) residual[i] = A + static_cast<uint64_t>(i);
    std::vector<uint64_t> good((len + 63U) / 64U, 0);

    const uint64_t root = isqrt_u64(B);
    for (uint32_t p32 : primes) {
        uint64_t p = p32;
        if (p > root) break;
        uint64_t first = A / p;
        if (A % p) ++first;
        if (first > B / p) continue;
        uint64_t m = first * p;
        for (;;) {
            const size_t idx = static_cast<size_t>(m - A);
            if (!get_bit(good, static_cast<uint64_t>(idx))) {
                // The original integer m has v_p(m)=1 exactly when (m/p) is
                // not divisible by p.  In that case a 3 mod 4 prime already
                // certifies this remainder, so no further factorization of
                // this element is needed.
                if ((p & 3U) == 3U && (m / p) % p != 0) {
                    set_bit(good, static_cast<uint64_t>(idx));
                    ++stats.exact_one_marks;
                } else {
                    // For still-unclassified elements, remove the full p-part.
                    // One division is guaranteed because m is a multiple of p
                    // and no earlier distinct prime can remove that factor.
                    residual[idx] /= p;
                    ++stats.successful_divisions;
                    while (true) {
                        ++stats.division_attempts;
                        if (residual[idx] % p != 0) break;
                        residual[idx] /= p;
                        ++stats.successful_divisions;
                    }
                }
            }
            if (B - m < p) break;
            m += p;
        }
    }
    for (size_t i = 0; i < len; ++i) {
        uint64_t q = residual[i];
        if (!get_bit(good, static_cast<uint64_t>(i)) && q > 1 && (q & 3U) == 3U) {
            set_bit(good, static_cast<uint64_t>(i));
            ++stats.large_residual_marks;
        }
    }
    return good;
}

uint64_t find_exact_one_factor(uint64_t r, const std::vector<uint32_t>& primes) {
    if (r == 0) return 0;
    uint64_t x = r;
    for (uint32_t p32 : primes) {
        uint64_t p = p32;
        if (p > x / p) break;
        if (x % p != 0) continue;
        unsigned exponent = 0;
        do {
            x /= p;
            ++exponent;
        } while (x % p == 0);
        if ((p & 3U) == 3U && exponent == 1) return p;
    }
    if (x > 1 && (x & 3U) == 3U) return x;
    return 0;
}

struct Args {
    uint64_t low = 0, high = 0, window = 10000000;
    int C = -1, D = -1;
    size_t prefix_shifts = 64;
    std::string json_path, candidates_path;
    bool quiet = false;
};

Args parse_args(int argc, char** argv) {
    Args a;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        auto need = [&](const char* name) {
            if (i + 1 >= argc) throw std::runtime_error(std::string("missing value for ") + name);
            return std::string(argv[++i]);
        };
        if (key == "--low") a.low = std::stoull(need("--low"));
        else if (key == "--high") a.high = std::stoull(need("--high"));
        else if (key == "--C") a.C = std::stoi(need("--C"));
        else if (key == "--D") a.D = std::stoi(need("--D"));
        else if (key == "--window") a.window = std::stoull(need("--window"));
        else if (key == "--prefix-shifts") a.prefix_shifts = static_cast<size_t>(std::stoull(need("--prefix-shifts")));
        else if (key == "--json") a.json_path = need("--json");
        else if (key == "--candidates") a.candidates_path = need("--candidates");
        else if (key == "--quiet") a.quiet = true;
        else throw std::runtime_error("unknown argument: " + key);
    }
    if (!a.low || !a.high || a.low > a.high || a.C < 0 || a.D < 0 || !a.window ||
        !a.prefix_shifts || a.json_path.empty()) {
        throw std::runtime_error("required: --low --high --C --D --json; positive window/prefix");
    }
    return a;
}

} // namespace

int main(int argc, char** argv) {
    try {
        Args args = parse_args(argc, argv);
        uint64_t next3 = ipow(3, args.C + 1) + 1;
        uint64_t next5 = ipow(5, args.D + 1) + 1;
        if (args.high >= next3) throw std::runtime_error("N_high < 3^(C+1)+1 fails");
        if (args.high >= next5) throw std::runtime_error("N_high < 5^(D+1)+1 fails");

        std::vector<uint64_t> p3(static_cast<size_t>(args.C + 1), 1);
        std::vector<uint64_t> p5(static_cast<size_t>(args.D + 1), 1);
        for (int i = 1; i <= args.C; ++i) p3[static_cast<size_t>(i)] = 3 * p3[static_cast<size_t>(i - 1)];
        for (int i = 1; i <= args.D; ++i) p5[static_cast<size_t>(i)] = 5 * p5[static_cast<size_t>(i - 1)];
        std::map<uint64_t, std::vector<std::pair<int,int>>> by_shift;
        for (int c = 0; c <= args.C; ++c) for (int d = 0; d <= args.D; ++d) {
            __uint128_t s = static_cast<__uint128_t>(p3[static_cast<size_t>(c)]) + p5[static_cast<size_t>(d)];
            if (s <= args.high) by_shift[static_cast<uint64_t>(s)].push_back({c,d});
        }
        std::vector<uint64_t> shifts;
        size_t pair_count = 0;
        for (const auto& kv : by_shift) {
            shifts.push_back(kv.first);
            pair_count += kv.second.size();
        }

        const uint64_t global_root = isqrt_u64(args.high - shifts.front());
        const std::vector<uint32_t> primes = prime_sieve(global_root);
        std::ofstream candidates;
        if (!args.candidates_path.empty()) {
            candidates.open(args.candidates_path);
            if (!candidates) throw std::runtime_error("cannot write candidates file");
        }

        uint64_t tested = 0, windows = 0, activation_splits = 0;
        uint64_t prefix_survivors_total = 0, full_shift_checks = 0, full_factor_calls = 0;
        size_t maximum_prefix_used = 0;
        FactorStats factor_stats;
        std::vector<uint64_t> found;
        auto start = std::chrono::steady_clock::now();

        uint64_t cur = args.low;
        while (cur <= args.high) {
            uint64_t end = args.high;
            if (args.window - 1 <= args.high - cur) end = std::min(end, cur + args.window - 1);
            auto next_shift = std::upper_bound(shifts.begin(), shifts.end(), cur);
            if (next_shift != shifts.end() && *next_shift <= end) {
                end = *next_shift - 1;
                ++activation_splits;
            }
            size_t active = static_cast<size_t>(std::upper_bound(shifts.begin(), shifts.end(), cur) - shifts.begin());
            size_t prefix = std::min(args.prefix_shifts, active);
            maximum_prefix_used = std::max(maximum_prefix_used, prefix);
            uint64_t len = end - cur + 1;
            tested += len;
            ++windows;

            std::vector<uint64_t> candidate((static_cast<size_t>(len) + 63U) / 64U, ~uint64_t(0));
            if (len & 63U) candidate.back() = (uint64_t(1) << (len & 63U)) - 1U;
            if (prefix > 0) {
                uint64_t s_min = shifts.front();
                uint64_t s_max = shifts[prefix - 1];
                if (cur < s_max) throw std::runtime_error("activation invariant failure");
                uint64_t A = cur - s_max;
                uint64_t B = end - s_min;
                if (A == 0) A = 1; // remainder zero must stay unmarked; tiny-range boundary only
                std::vector<uint64_t> good = classify_interval(A, B, primes, factor_stats);
                for (size_t si = 0; si < prefix && any_bits(candidate); ++si) {
                    // If A was raised from 0 to 1, the only omitted bit corresponds to r=0 and is correctly false.
                    uint64_t natural_A = cur - s_max;
                    uint64_t base_adjust = A - natural_A;
                    uint64_t offset = (s_max - shifts[si]);
                    for (size_t wi = 0; wi < candidate.size(); ++wi) {
                        uint64_t start_bit = offset + static_cast<uint64_t>(wi) * 64U;
                        uint64_t word = 0;
                        if (start_bit >= base_adjust) word = slice_word(good, start_bit - base_adjust);
                        else {
                            // Only possible for one leading r=0 bit in toy ranges.
                            unsigned missing = static_cast<unsigned>(base_adjust - start_bit);
                            if (missing < 64U) word = slice_word(good, 0) << missing;
                        }
                        candidate[wi] &= word;
                    }
                    if (len & 63U) candidate.back() &= (uint64_t(1) << (len & 63U)) - 1U;
                }
            }

            uint64_t prefix_survivors = popcount_bits(candidate);
            prefix_survivors_total += prefix_survivors;
            for (size_t wi = 0; wi < candidate.size(); ++wi) {
                uint64_t word = candidate[wi];
                while (word) {
                    unsigned b = static_cast<unsigned>(__builtin_ctzll(word));
                    uint64_t idx = static_cast<uint64_t>(wi) * 64U + b;
                    if (idx < len) {
                        uint64_t n = cur + idx;
                        size_t n_active = static_cast<size_t>(std::upper_bound(shifts.begin(), shifts.end(), n) - shifts.begin());
                        bool all = true;
                        for (size_t si = 0; si < n_active; ++si) {
                            ++full_shift_checks;
                            ++full_factor_calls;
                            if (find_exact_one_factor(n - shifts[si], primes) == 0) {
                                all = false;
                                break;
                            }
                        }
                        if (all) {
                            found.push_back(n);
                            if (candidates) candidates << n << '\n';
                        }
                    }
                    word &= word - 1;
                }
            }
            if (!args.quiet) {
                std::cout << "WINDOW low=" << cur << " high=" << end
                          << " active=" << active << " prefix=" << prefix
                          << " prefix_survivors=" << prefix_survivors
                          << " candidates_so_far=" << found.size() << '\n';
            }
            if (end == std::numeric_limits<uint64_t>::max()) break;
            cur = end + 1;
        }

        double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
        std::ofstream js(args.json_path);
        if (!js) throw std::runtime_error("cannot write JSON");
        js << "{\n"
           << "  \"method\": \"exact_all_primes_segmented_factor_shifted_sieve\",\n"
           << "  \"low\": \"" << args.low << "\",\n"
           << "  \"high\": \"" << args.high << "\",\n"
           << "  \"C\": " << args.C << ",\n"
           << "  \"D\": " << args.D << ",\n"
           << "  \"next_power_bound_3\": \"" << next3 << "\",\n"
           << "  \"next_power_bound_5\": \"" << next5 << "\",\n"
           << "  \"prime_sieve_limit\": " << global_root << ",\n"
           << "  \"prime_sieve_count\": " << primes.size() << ",\n"
           << "  \"obstruction_prime_family\": \"all primes p == 3 mod 4 (large residual prime handled exactly)\",\n"
           << "  \"admissible_pair_count_at_high\": " << pair_count << ",\n"
           << "  \"distinct_shift_count_at_high\": " << shifts.size() << ",\n"
           << "  \"requested_prefix_shifts\": " << args.prefix_shifts << ",\n"
           << "  \"maximum_prefix_shifts_used\": " << maximum_prefix_used << ",\n"
           << "  \"window_size\": " << args.window << ",\n"
           << "  \"windows\": " << windows << ",\n"
           << "  \"activation_splits\": " << activation_splits << ",\n"
           << "  \"integers_tested\": " << tested << ",\n"
           << "  \"factor_division_attempts\": " << factor_stats.division_attempts << ",\n"
           << "  \"factor_successful_divisions\": " << factor_stats.successful_divisions << ",\n"
           << "  \"small_exact_one_marks\": " << factor_stats.exact_one_marks << ",\n"
           << "  \"large_residual_marks\": " << factor_stats.large_residual_marks << ",\n"
           << "  \"survivors_after_prefix_total\": " << prefix_survivors_total << ",\n"
           << "  \"full_shift_checks\": " << full_shift_checks << ",\n"
           << "  \"full_factor_calls\": " << full_factor_calls << ",\n"
           << "  \"candidate_count\": " << found.size() << ",\n"
           << "  \"candidates\": [";
        for (size_t i = 0; i < found.size(); ++i) {
            if (i) js << ',';
            js << '"' << found[i] << '"';
        }
        js << "],\n"
           << "  \"elapsed_seconds\": " << seconds << ",\n"
           << "  \"classification\": \""
           << (found.empty() ? "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE UNRESTRICTED VALUATION-ONE PRIME FAMILY"
                             : "CANDIDATES REQUIRE INDEPENDENT VERIFIERS")
           << "\"\n}\n";

        std::cout << "integers_tested=" << tested << '\n'
                  << "survivors_after_prefix_total=" << prefix_survivors_total << '\n'
                  << "candidate_count=" << found.size() << '\n'
                  << "elapsed_seconds=" << seconds << '\n'
                  << (found.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return found.empty() ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR " << e.what() << '\n';
        return 2;
    }
}
