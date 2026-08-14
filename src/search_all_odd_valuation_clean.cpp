// Independent clean-room exact finite scanner for all p == 3 (mod 4), with
// selectable valuation family: e=1; e in {1,3}; or every positive odd e.
//
// This implementation deliberately differs from the packed-bit scanner:
// it uses byte classifications and an explicit compacted vector of live offsets.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

enum class Mode { One, OneThree, Odd };

bool accepted(unsigned e, Mode m) {
    if (m == Mode::One) return e == 1;
    if (m == Mode::OneThree) return e == 1 || e == 3;
    return (e % 2U) == 1U;
}

const char* mode_text(Mode m) {
    if (m == Mode::One) return "exact-one";
    if (m == Mode::OneThree) return "one-or-three";
    return "any-odd";
}

uint64_t integer_root(uint64_t x) {
    uint64_t left = 0;
    uint64_t right = x < (uint64_t(1) << 32) ? x : (uint64_t(1) << 32);
    while (left < right) {
        uint64_t middle = left + (right - left + 1) / 2;
        if (middle != 0 && middle <= x / middle) left = middle;
        else right = middle - 1;
    }
    return left;
}

std::vector<uint32_t> primes_through(uint64_t bound64) {
    if (bound64 > std::numeric_limits<uint32_t>::max()) {
        throw std::runtime_error("prime bound exceeds uint32");
    }
    uint32_t bound = static_cast<uint32_t>(bound64);
    std::vector<uint8_t> crossed(static_cast<size_t>(bound) + 1U, 0);
    std::vector<uint32_t> result;
    for (uint32_t candidate = 2; candidate <= bound; ++candidate) {
        if (crossed[candidate]) continue;
        result.push_back(candidate);
        if (uint64_t(candidate) * candidate <= bound) {
            for (uint64_t multiple = uint64_t(candidate) * candidate;
                 multiple <= bound; multiple += candidate) {
                crossed[static_cast<size_t>(multiple)] = 1;
            }
        }
    }
    return result;
}

uint64_t exact_power(uint64_t base, int exponent) {
    uint64_t answer = 1;
    for (int i = 0; i < exponent; ++i) {
        if (answer > std::numeric_limits<uint64_t>::max() / base) {
            throw std::runtime_error("power overflow");
        }
        answer *= base;
    }
    return answer;
}

struct Stats {
    uint64_t progression_visits = 0;
    uint64_t divisions = 0;
    uint64_t small_marks = 0;
    uint64_t residual_marks = 0;
    uint64_t prefix_membership_tests = 0;
    uint64_t full_factor_tests = 0;
};

std::vector<uint8_t> classify_block(uint64_t low, uint64_t high,
                                    const std::vector<uint32_t>& primes,
                                    Mode mode, Stats& stats) {
    if (low > high) throw std::runtime_error("invalid block");
    uint64_t width64 = high - low + 1;
    if (width64 > std::numeric_limits<size_t>::max()) throw std::runtime_error("block too wide");
    size_t width = static_cast<size_t>(width64);
    std::vector<uint64_t> remaining(width);
    std::vector<uint8_t> good(width, 0);
    for (size_t i = 0; i < width; ++i) remaining[i] = low + static_cast<uint64_t>(i);
    if (low == 0) remaining[0] = 1; // r=0 is never accepted.

    uint64_t root = integer_root(high);
    for (uint32_t p32 : primes) {
        uint64_t p = p32;
        if (p > root) break;
        uint64_t k = low / p;
        if (low % p != 0) ++k;
        if (k == 0) k = 1; // skip the integer zero.
        if (k > high / p) continue;
        uint64_t value = k * p;
        for (;;) {
            ++stats.progression_visits;
            size_t index = static_cast<size_t>(value - low);
            if (!good[index]) {
                uint64_t reduced = remaining[index];
                unsigned exponent = 0;
                while (reduced % p == 0) {
                    reduced /= p;
                    ++exponent;
                }
                if ((p % 4U) == 3U && accepted(exponent, mode)) {
                    good[index] = 1;
                    ++stats.small_marks;
                } else {
                    remaining[index] = reduced;
                    stats.divisions += exponent;
                }
            }
            if (high - value < p) break;
            value += p;
        }
    }

    // After division by every prime <= sqrt(high), an unmarked residual >1 is
    // a single prime factor, necessarily with exponent one.
    for (size_t i = 0; i < width; ++i) {
        uint64_t q = remaining[i];
        if (!good[i] && q > 1 && q % 4U == 3U) {
            good[i] = 1;
            ++stats.residual_marks;
        }
    }
    return good;
}

uint64_t find_prime(uint64_t r, const std::vector<uint32_t>& primes, Mode mode) {
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
        if (p % 4U == 3U && accepted(exponent, mode)) return p;
    }
    // Standard trial-division invariant: x is 1 or a prime. Its exponent is 1.
    return (x > 1 && x % 4U == 3U) ? x : 0;
}

struct Options {
    uint64_t low = 0;
    uint64_t high = 0;
    uint64_t window = 10000000;
    int C = -1;
    int D = -1;
    size_t prefix = 100;
    Mode mode = Mode::One;
    std::string json_path;
    std::string candidate_path;
    bool quiet = false;
};

Options read_options(int argc, char** argv) {
    Options o;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        auto next = [&]() -> std::string {
            if (++i >= argc) throw std::runtime_error("missing command-line value");
            return argv[i];
        };
        if (key == "--low") o.low = std::stoull(next());
        else if (key == "--high") o.high = std::stoull(next());
        else if (key == "--C") o.C = std::stoi(next());
        else if (key == "--D") o.D = std::stoi(next());
        else if (key == "--window") o.window = std::stoull(next());
        else if (key == "--prefix-shifts") o.prefix = static_cast<size_t>(std::stoull(next()));
        else if (key == "--json") o.json_path = next();
        else if (key == "--candidates") o.candidate_path = next();
        else if (key == "--valuation-mode") {
            std::string value = next();
            if (value == "exact-one") o.mode = Mode::One;
            else if (value == "one-or-three") o.mode = Mode::OneThree;
            else if (value == "any-odd") o.mode = Mode::Odd;
            else throw std::runtime_error("bad valuation mode");
        }
        else if (key == "--quiet") o.quiet = true;
        else throw std::runtime_error("unknown option: " + key);
    }
    if (!o.low || !o.high || o.low > o.high || o.C < 0 || o.D < 0 ||
        !o.window || !o.prefix || o.json_path.empty()) {
        throw std::runtime_error("missing/invalid required options");
    }
    return o;
}

} // namespace

int main(int argc, char** argv) {
    try {
        Options o = read_options(argc, argv);
        uint64_t next3 = exact_power(3, o.C + 1) + 1;
        uint64_t next5 = exact_power(5, o.D + 1) + 1;
        if (o.high >= next3 || o.high >= next5) throw std::runtime_error("finite exponent bound fails");

        std::vector<uint64_t> power3(static_cast<size_t>(o.C + 1), 1);
        std::vector<uint64_t> power5(static_cast<size_t>(o.D + 1), 1);
        for (int c = 1; c <= o.C; ++c) power3[static_cast<size_t>(c)] = 3 * power3[static_cast<size_t>(c - 1)];
        for (int d = 1; d <= o.D; ++d) power5[static_cast<size_t>(d)] = 5 * power5[static_cast<size_t>(d - 1)];

        std::map<uint64_t, unsigned> multiplicity;
        for (uint64_t a : power3) {
            for (uint64_t b : power5) {
                if (a <= o.high && b <= o.high - a) ++multiplicity[a + b];
            }
        }
        std::vector<uint64_t> shifts;
        size_t pair_count = 0;
        for (const auto& item : multiplicity) {
            shifts.push_back(item.first);
            pair_count += item.second;
        }
        if (shifts.empty()) throw std::runtime_error("empty shift family");
        uint64_t sieve_limit = integer_root(o.high - shifts.front());
        std::vector<uint32_t> primes = primes_through(sieve_limit);

        std::ofstream candidate_file;
        if (!o.candidate_path.empty()) {
            candidate_file.open(o.candidate_path);
            if (!candidate_file) throw std::runtime_error("cannot write candidate file");
        }

        Stats stats;
        uint64_t integers = 0;
        uint64_t windows = 0;
        uint64_t activation_splits = 0;
        uint64_t total_prefix_survivors = 0;
        size_t maximum_prefix = 0;
        std::vector<uint64_t> candidates;
        auto start = std::chrono::steady_clock::now();

        uint64_t left = o.low;
        while (left <= o.high) {
            uint64_t right = o.high;
            if (o.window - 1 <= o.high - left) right = std::min(right, left + o.window - 1);
            auto next_shift = std::upper_bound(shifts.begin(), shifts.end(), left);
            if (next_shift != shifts.end() && *next_shift <= right) {
                right = *next_shift - 1;
                ++activation_splits;
            }
            size_t active = static_cast<size_t>(std::upper_bound(shifts.begin(), shifts.end(), left) - shifts.begin());
            size_t use = std::min(o.prefix, active);
            maximum_prefix = std::max(maximum_prefix, use);
            uint64_t width64 = right - left + 1;
            if (width64 > std::numeric_limits<uint32_t>::max()) {
                throw std::runtime_error("window too wide for clean-room live-offset representation");
            }
            size_t width = static_cast<size_t>(width64);
            integers += width64;
            ++windows;

            std::vector<uint32_t> live(width);
            for (size_t i = 0; i < width; ++i) live[i] = static_cast<uint32_t>(i);
            if (use > 0) {
                uint64_t largest = shifts[use - 1];
                if (left < largest) throw std::runtime_error("activation invariant failure");
                uint64_t A = left - largest;
                uint64_t B = right - shifts.front();
                std::vector<uint8_t> good = classify_block(A, B, primes, o.mode, stats);
                for (size_t si = 0; si < use && !live.empty(); ++si) {
                    size_t write = 0;
                    uint64_t shift = shifts[si];
                    for (uint32_t offset : live) {
                        ++stats.prefix_membership_tests;
                        uint64_t r = (left + offset) - shift;
                        if (good[static_cast<size_t>(r - A)]) live[write++] = offset;
                    }
                    live.resize(write);
                }
            }

            total_prefix_survivors += live.size();
            for (uint32_t offset : live) {
                uint64_t n = left + offset;
                size_t nactive = static_cast<size_t>(std::upper_bound(shifts.begin(), shifts.end(), n) - shifts.begin());
                bool all = true;
                for (size_t si = 0; si < nactive; ++si) {
                    ++stats.full_factor_tests;
                    if (find_prime(n - shifts[si], primes, o.mode) == 0) {
                        all = false;
                        break;
                    }
                }
                if (all) {
                    candidates.push_back(n);
                    if (candidate_file) candidate_file << n << '\n';
                }
            }

            if (!o.quiet) {
                std::cout << "BLOCK low=" << left << " high=" << right
                          << " active=" << active << " prefix=" << use
                          << " prefix_survivors=" << live.size()
                          << " candidates_so_far=" << candidates.size() << '\n';
            }
            if (right == std::numeric_limits<uint64_t>::max()) break;
            left = right + 1;
        }

        double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
        std::ofstream json(o.json_path);
        if (!json) throw std::runtime_error("cannot write JSON");
        json << "{\n"
             << "  \"method\": \"independent_clean_byte_all_primes_odd_valuation_scanner\",\n"
             << "  \"low\": \"" << o.low << "\",\n"
             << "  \"high\": \"" << o.high << "\",\n"
             << "  \"C\": " << o.C << ",\n"
             << "  \"D\": " << o.D << ",\n"
             << "  \"next_power_bound_3\": \"" << next3 << "\",\n"
             << "  \"next_power_bound_5\": \"" << next5 << "\",\n"
             << "  \"prime_sieve_limit\": " << sieve_limit << ",\n"
             << "  \"prime_sieve_count\": " << primes.size() << ",\n"
             << "  \"obstruction_prime_family\": \"all primes p == 3 mod 4 (large residual prime handled exactly)\",\n"
             << "  \"valuation_mode\": \"" << mode_text(o.mode) << "\",\n"
             << "  \"admissible_pair_count_at_high\": " << pair_count << ",\n"
             << "  \"distinct_shift_count_at_high\": " << shifts.size() << ",\n"
             << "  \"requested_prefix_shifts\": " << o.prefix << ",\n"
             << "  \"maximum_prefix_shifts_used\": " << maximum_prefix << ",\n"
             << "  \"window_size\": " << o.window << ",\n"
             << "  \"windows\": " << windows << ",\n"
             << "  \"activation_splits\": " << activation_splits << ",\n"
             << "  \"integers_tested\": " << integers << ",\n"
             << "  \"progression_visits\": " << stats.progression_visits << ",\n"
             << "  \"residual_divisions\": " << stats.divisions << ",\n"
             << "  \"small_allowed_marks\": " << stats.small_marks << ",\n"
             << "  \"large_residual_marks\": " << stats.residual_marks << ",\n"
             << "  \"prefix_membership_tests\": " << stats.prefix_membership_tests << ",\n"
             << "  \"full_shift_factor_tests\": " << stats.full_factor_tests << ",\n"
             << "  \"survivors_after_prefix_total\": " << total_prefix_survivors << ",\n"
             << "  \"candidate_count\": " << candidates.size() << ",\n"
             << "  \"candidates\": [";
        for (size_t i = 0; i < candidates.size(); ++i) {
            if (i) json << ',';
            json << '"' << candidates[i] << '"';
        }
        json << "],\n"
             << "  \"elapsed_seconds\": " << elapsed << ",\n"
             << "  \"classification\": \""
             << (candidates.empty() ? "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE DECLARED ODD-VALUATION FAMILY"
                                    : "CANDIDATES REQUIRE INDEPENDENT VERIFIERS")
             << "\"\n}\n";

        std::cout << "integers_tested=" << integers << '\n'
                  << "survivors_after_prefix_total=" << total_prefix_survivors << '\n'
                  << "candidate_count=" << candidates.size() << '\n'
                  << "elapsed_seconds=" << elapsed << '\n'
                  << (candidates.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return candidates.empty() ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR " << e.what() << '\n';
        return 2;
    }
}
