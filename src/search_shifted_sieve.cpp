// Exact shifted segmented sieve for the bounded A303656 valuation-one search.
//
// For a fixed prime pool P define good(r)=1 iff some p in P has v_p(r)=1.
// For a window [L,U] and a shift s, the bounded certificate condition is
// exactly good(n-s)=1 (with n-s>0).  We sieve good once on the union of the
// translated remainder intervals for a prefix of active shifts, then intersect
// shifted packed-bit slices.  Any survivors are checked against every active
// shift and every prime directly.  Thus an empty result is an exact exhaustive
// result for the supplied interval and prime pool, not a heuristic.
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

namespace {

bool is_prime_trial(uint64_t n) {
    if (n < 2) return false;
    if ((n & 1U) == 0) return n == 2;
    for (uint64_t f = 3; f <= n / f; f += 2) {
        if (n % f == 0) return false;
    }
    return true;
}

std::vector<uint64_t> parse_primes(std::string raw) {
    std::ifstream in(raw);
    if (in) {
        std::ostringstream ss;
        ss << in.rdbuf();
        raw = ss.str();
    }
    for (char& ch : raw) {
        if (ch == '\n' || ch == '\r' || ch == ' ' || ch == '\t') ch = ',';
    }
    std::stringstream ss(raw);
    std::string item;
    std::vector<uint64_t> out;
    std::set<uint64_t> seen;
    while (std::getline(ss, item, ',')) {
        if (item.empty()) continue;
        uint64_t p = std::stoull(item);
        if (!seen.insert(p).second) throw std::runtime_error("duplicate prime");
        if (!is_prime_trial(p) || p % 4 != 3) {
            throw std::runtime_error("invalid obstruction prime: " + std::to_string(p));
        }
        if (p > 0xffffffffULL) throw std::runtime_error("prime exceeds 2^32-1");
        if (static_cast<__uint128_t>(p) * p > std::numeric_limits<uint64_t>::max()) {
            throw std::runtime_error("p^2 overflows uint64");
        }
        out.push_back(p);
    }
    if (out.empty()) throw std::runtime_error("empty prime pool");
    return out;
}

uint64_t ipow(uint64_t base, int exponent) {
    __uint128_t x = 1;
    for (int i = 0; i < exponent; ++i) {
        x *= base;
        if (x > std::numeric_limits<uint64_t>::max()) {
            throw std::runtime_error("power overflow");
        }
    }
    return static_cast<uint64_t>(x);
}

inline void set_bit(std::vector<uint64_t>& bits, uint64_t i) {
    bits[static_cast<size_t>(i >> 6)] |= uint64_t(1) << (i & 63U);
}

inline bool get_bit(const std::vector<uint64_t>& bits, uint64_t i) {
    return (bits[static_cast<size_t>(i >> 6)] >> (i & 63U)) & 1U;
}

uint64_t popcount_bits(const std::vector<uint64_t>& bits) {
    uint64_t total = 0;
    for (uint64_t w : bits) total += static_cast<uint64_t>(__builtin_popcountll(w));
    return total;
}

bool any_bits(const std::vector<uint64_t>& bits) {
    for (uint64_t w : bits) if (w != 0) return true;
    return false;
}

uint64_t slice_word(const std::vector<uint64_t>& source, uint64_t bit_start) {
    const size_t wi = static_cast<size_t>(bit_start >> 6);
    const unsigned off = static_cast<unsigned>(bit_start & 63U);
    uint64_t lo = wi < source.size() ? source[wi] : 0;
    if (off == 0) return lo;
    uint64_t hi = wi + 1 < source.size() ? source[wi + 1] : 0;
    return (lo >> off) | (hi << (64U - off));
}

bool exact_one(uint64_t n, uint64_t shift, uint64_t p) {
    if (n <= shift) return false;
    uint64_t r = n - shift;
    if (r % p != 0) return false;
    uint64_t p2 = p * p;
    return r % p2 != 0;
}

struct Args {
    uint64_t low = 0;
    uint64_t high = 0;
    uint64_t window = 10000000;
    int C = -1;
    int D = -1;
    size_t prefix_shifts = 64;
    std::string prime_arg;
    std::string json_path;
    std::string candidates_path;
    bool quiet = false;
};

Args parse_args(int argc, char** argv) {
    Args a;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        auto need = [&](const char* name) -> std::string {
            if (i + 1 >= argc) throw std::runtime_error(std::string("missing value for ") + name);
            return argv[++i];
        };
        if (key == "--low") a.low = std::stoull(need("--low"));
        else if (key == "--high") a.high = std::stoull(need("--high"));
        else if (key == "--C") a.C = std::stoi(need("--C"));
        else if (key == "--D") a.D = std::stoi(need("--D"));
        else if (key == "--primes") a.prime_arg = need("--primes");
        else if (key == "--window") a.window = std::stoull(need("--window"));
        else if (key == "--prefix-shifts") a.prefix_shifts = static_cast<size_t>(std::stoull(need("--prefix-shifts")));
        else if (key == "--json") a.json_path = need("--json");
        else if (key == "--candidates") a.candidates_path = need("--candidates");
        else if (key == "--quiet") a.quiet = true;
        else throw std::runtime_error("unknown argument: " + key);
    }
    if (a.low == 0 || a.high == 0 || a.low > a.high || a.C < 0 || a.D < 0 ||
        a.prime_arg.empty() || a.json_path.empty() || a.window == 0 || a.prefix_shifts == 0) {
        throw std::runtime_error("required: --low --high --C --D --primes --json; positive --window and --prefix-shifts");
    }
    return a;
}

void write_json_string_array(std::ostream& out, const std::vector<uint64_t>& values) {
    out << '[';
    for (size_t i = 0; i < values.size(); ++i) {
        if (i) out << ',';
        out << '"' << values[i] << '"';
    }
    out << ']';
}

} // namespace

int main(int argc, char** argv) {
    try {
        const Args args = parse_args(argc, argv);
        const uint64_t bound3 = ipow(3, args.C + 1);
        const uint64_t bound5 = ipow(5, args.D + 1);
        if (args.high >= bound3 + 1) throw std::runtime_error("N_high < 3^(C+1)+1 fails");
        if (args.high >= bound5 + 1) throw std::runtime_error("N_high < 5^(D+1)+1 fails");

        const std::vector<uint64_t> primes = parse_primes(args.prime_arg);
        std::vector<uint64_t> p3(static_cast<size_t>(args.C + 1));
        std::vector<uint64_t> p5(static_cast<size_t>(args.D + 1));
        p3[0] = p5[0] = 1;
        for (int i = 1; i <= args.C; ++i) p3[static_cast<size_t>(i)] = p3[static_cast<size_t>(i - 1)] * 3;
        for (int i = 1; i <= args.D; ++i) p5[static_cast<size_t>(i)] = p5[static_cast<size_t>(i - 1)] * 5;

        std::map<uint64_t, std::vector<std::pair<int,int>>> shift_pairs;
        for (int c = 0; c <= args.C; ++c) {
            for (int d = 0; d <= args.D; ++d) {
                __uint128_t sum = static_cast<__uint128_t>(p3[static_cast<size_t>(c)]) + p5[static_cast<size_t>(d)];
                if (sum <= args.high) shift_pairs[static_cast<uint64_t>(sum)].push_back({c,d});
            }
        }
        std::vector<uint64_t> shifts;
        shifts.reserve(shift_pairs.size());
        size_t pair_count = 0;
        for (const auto& kv : shift_pairs) {
            shifts.push_back(kv.first);
            pair_count += kv.second.size();
        }

        std::ofstream candidate_file;
        if (!args.candidates_path.empty()) {
            candidate_file.open(args.candidates_path);
            if (!candidate_file) throw std::runtime_error("cannot write candidates file");
        }

        uint64_t tested = 0;
        uint64_t windows = 0;
        uint64_t activation_splits = 0;
        uint64_t marked_multiples = 0;
        uint64_t prefix_word_ands = 0;
        uint64_t survivors_after_prefix_total = 0;
        uint64_t full_shift_checks = 0;
        uint64_t full_prime_checks = 0;
        size_t maximum_prefix_used = 0;
        std::vector<uint64_t> found;
        const auto started = std::chrono::steady_clock::now();

        uint64_t cur = args.low;
        while (cur <= args.high) {
            uint64_t end = args.high;
            if (args.window - 1 <= args.high - cur) end = std::min(end, cur + args.window - 1);

            // Split immediately before the next newly active shift, so the active set is constant.
            auto next_it = std::upper_bound(shifts.begin(), shifts.end(), cur);
            if (next_it != shifts.end() && *next_it <= end) {
                end = *next_it - 1;
                ++activation_splits;
            }
            const size_t active_count = static_cast<size_t>(
                std::upper_bound(shifts.begin(), shifts.end(), cur) - shifts.begin());
            const size_t prefix_count = std::min(args.prefix_shifts, active_count);
            maximum_prefix_used = std::max(maximum_prefix_used, prefix_count);
            const uint64_t len = end - cur + 1;
            tested += len;
            ++windows;

            std::vector<uint64_t> candidate((static_cast<size_t>(len) + 63U) / 64U, ~uint64_t(0));
            if (len & 63U) candidate.back() = (uint64_t(1) << (len & 63U)) - 1U;

            if (prefix_count == 0) {
                // This only occurs in tiny toy ranges before shift 2 activates.
            } else {
                const uint64_t s_min = shifts[0];
                const uint64_t s_max = shifts[prefix_count - 1];
                if (cur < s_max) throw std::runtime_error("internal activation error");
                const uint64_t rem_low = cur - s_max;
                const uint64_t rem_high = end - s_min;
                const uint64_t rem_len = rem_high - rem_low + 1;
                std::vector<uint64_t> good((static_cast<size_t>(rem_len) + 63U) / 64U, 0);

                for (uint64_t p : primes) {
                    uint64_t q = rem_low / p;
                    if (rem_low % p != 0) ++q;
                    if (q > rem_high / p) continue;
                    uint64_t m = q * p;
                    for (;;) {
                        // m is divisible by p^2 exactly when q is divisible by p.
                        if (q % p != 0) {
                            set_bit(good, m - rem_low);
                            ++marked_multiples;
                        }
                        if (rem_high - m < p) break;
                        m += p;
                        ++q;
                    }
                }

                for (size_t si = 0; si < prefix_count && any_bits(candidate); ++si) {
                    const uint64_t offset = s_max - shifts[si];
                    for (size_t wi = 0; wi < candidate.size(); ++wi) {
                        candidate[wi] &= slice_word(good, offset + static_cast<uint64_t>(wi) * 64U);
                        ++prefix_word_ands;
                    }
                    if (len & 63U) candidate.back() &= (uint64_t(1) << (len & 63U)) - 1U;
                }
            }

            uint64_t prefix_survivors = popcount_bits(candidate);
            survivors_after_prefix_total += prefix_survivors;

            // Full direct verification of every prefix survivor against all active shifts.
            for (size_t wi = 0; wi < candidate.size(); ++wi) {
                uint64_t word = candidate[wi];
                while (word) {
                    unsigned bit = static_cast<unsigned>(__builtin_ctzll(word));
                    uint64_t index = static_cast<uint64_t>(wi) * 64U + bit;
                    if (index < len) {
                        uint64_t n = cur + index;
                        bool all = true;
                        const size_t n_active = static_cast<size_t>(
                            std::upper_bound(shifts.begin(), shifts.end(), n) - shifts.begin());
                        for (size_t si = 0; si < n_active; ++si) {
                            ++full_shift_checks;
                            bool covered = false;
                            for (uint64_t p : primes) {
                                ++full_prime_checks;
                                if (exact_one(n, shifts[si], p)) {
                                    covered = true;
                                    break;
                                }
                            }
                            if (!covered) {
                                all = false;
                                break;
                            }
                        }
                        if (all) {
                            found.push_back(n);
                            if (candidate_file) candidate_file << n << '\n';
                        }
                    }
                    word &= word - 1;
                }
            }

            if (!args.quiet) {
                std::cout << "WINDOW low=" << cur << " high=" << end
                          << " active_distinct_shifts=" << active_count
                          << " prefix_shifts=" << prefix_count
                          << " prefix_survivors=" << prefix_survivors
                          << " verified_candidates=" << found.size() << '\n';
            }
            if (end == std::numeric_limits<uint64_t>::max()) break;
            cur = end + 1;
        }

        const double seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        std::ofstream js(args.json_path);
        if (!js) throw std::runtime_error("cannot write JSON");
        js << "{\n"
           << "  \"method\": \"exact_shifted_segmented_sieve\",\n"
           << "  \"low\": \"" << args.low << "\",\n"
           << "  \"high\": \"" << args.high << "\",\n"
           << "  \"C\": " << args.C << ",\n"
           << "  \"D\": " << args.D << ",\n"
           << "  \"bound_3_next\": \"" << bound3 + 1 << "\",\n"
           << "  \"bound_5_next\": \"" << bound5 + 1 << "\",\n"
           << "  \"prime_count\": " << primes.size() << ",\n"
           << "  \"primes\": [";
        for (size_t i = 0; i < primes.size(); ++i) {
            if (i) js << ',';
            js << primes[i];
        }
        js << "],\n"
           << "  \"admissible_pair_count_at_high\": " << pair_count << ",\n"
           << "  \"distinct_shift_count_at_high\": " << shifts.size() << ",\n"
           << "  \"requested_prefix_shifts\": " << args.prefix_shifts << ",\n"
           << "  \"maximum_prefix_shifts_used\": " << maximum_prefix_used << ",\n"
           << "  \"window_size\": " << args.window << ",\n"
           << "  \"windows\": " << windows << ",\n"
           << "  \"activation_splits\": " << activation_splits << ",\n"
           << "  \"integers_tested\": " << tested << ",\n"
           << "  \"marked_exact_one_multiples\": " << marked_multiples << ",\n"
           << "  \"prefix_word_ands\": " << prefix_word_ands << ",\n"
           << "  \"survivors_after_prefix_total\": " << survivors_after_prefix_total << ",\n"
           << "  \"full_shift_checks\": " << full_shift_checks << ",\n"
           << "  \"full_prime_checks\": " << full_prime_checks << ",\n"
           << "  \"candidate_count\": " << found.size() << ",\n"
           << "  \"candidates\": ";
        write_json_string_array(js, found);
        js << ",\n"
           << "  \"elapsed_seconds\": " << seconds << ",\n"
           << "  \"classification\": \""
           << (found.empty() ? "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL"
                             : "CANDIDATES REQUIRE INDEPENDENT VERIFIERS")
           << "\"\n}\n";

        std::cout << "integers_tested=" << tested << '\n'
                  << "survivors_after_prefix_total=" << survivors_after_prefix_total << '\n'
                  << "candidate_count=" << found.size() << '\n'
                  << "elapsed_seconds=" << seconds << '\n'
                  << (found.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return found.empty() ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR " << e.what() << '\n';
        return 2;
    }
}
