// Exact direct search for A303656 counterexamples on a finite interval.
//
// For every distinct shift s = 3^c + 5^d <= U, clear every n in [L,U]
// for which n-s = x^2+y^2 with 0 <= x <= y.  Remaining bits are exactly
// the integers with no representation a^2+b^2+3^c+5^d.
//
// This implementation uses an x-outer annulus enumeration and exact bitwise
// integer square root.  It does not use floating point or factorization.
#include <algorithm>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <system_error>
#include <utility>
#include <vector>

static constexpr const char* IMPLEMENTATION_ID = "search_twosquares_bitset";

static uint64_t isqrt_u64(uint64_t n) {
    uint64_t result = 0;
    uint64_t bit = uint64_t(1) << 62;
    while (bit > n) bit >>= 2;
    while (bit != 0) {
        if (n >= result + bit) {
            n -= result + bit;
            result = (result >> 1) + bit;
        } else {
            result >>= 1;
        }
        bit >>= 2;
    }
    return result;
}

static uint64_t ceil_sqrt_u64(uint64_t n) {
    uint64_t r = isqrt_u64(n);
    return static_cast<__uint128_t>(r) * r == n ? r : r + 1;
}

static uint64_t checked_pow(uint64_t base, int exponent) {
    if (exponent < 0) throw std::runtime_error("negative exponent");
    __uint128_t value = 1;
    for (int i = 0; i < exponent; ++i) {
        value *= base;
        if (value > UINT64_MAX) throw std::runtime_error("power overflow");
    }
    return static_cast<uint64_t>(value);
}

static uint64_t parse_u64_decimal(const std::string& text, const char* option) {
    if (text.empty()) throw std::runtime_error(std::string(option) + " requires a decimal value");
    uint64_t value = 0;
    const char* begin = text.data();
    const char* end = begin + text.size();
    const auto parsed = std::from_chars(begin, end, value, 10);
    if (parsed.ec == std::errc::result_out_of_range) {
        throw std::runtime_error(std::string(option) + " out of uint64 range");
    }
    if (parsed.ec != std::errc() || parsed.ptr != end) {
        throw std::runtime_error(std::string(option) + " must be unsigned decimal");
    }
    return value;
}

static int parse_bounded_exponent(const std::string& text, const char* option, uint64_t maximum) {
    const uint64_t value = parse_u64_decimal(text, option);
    if (value > maximum) {
        throw std::runtime_error(std::string(option) + " exceeds supported uint64 exponent range");
    }
    return static_cast<int>(value);
}

static uint64_t checked_add_u64(uint64_t left, uint64_t right, const char* what) {
    const __uint128_t sum = static_cast<__uint128_t>(left) + right;
    if (sum > UINT64_MAX) throw std::runtime_error(std::string(what) + " overflow");
    return static_cast<uint64_t>(sum);
}

template <typename Visitor>
static uint64_t enumerate_annulus_x_outer(uint64_t remainder_low, uint64_t remainder_high, Visitor visit) {
    if (remainder_low > remainder_high) throw std::runtime_error("annulus lower bound exceeds upper bound");
    const uint64_t x_max = isqrt_u64(remainder_high / 2);
    uint64_t y_high = isqrt_u64(remainder_high);
    uint64_t y_low = ceil_sqrt_u64(remainder_low);
    uint64_t count = 0;
    for (uint64_t x = 0; x <= x_max; ++x) {
        const __uint128_t x2 = static_cast<__uint128_t>(x) * x;
        while (y_high >= x && x2 + static_cast<__uint128_t>(y_high) * y_high > remainder_high) {
            --y_high;
        }
        while (y_low > x && x2 + static_cast<__uint128_t>(y_low - 1) * (y_low - 1) >= remainder_low) {
            --y_low;
        }
        const uint64_t begin_y = std::max(x, y_low);
        if (begin_y > y_high) continue;
        for (uint64_t y = begin_y; y <= y_high; ++y) {
            if (count == UINT64_MAX) throw std::runtime_error("annulus pair count overflow");
            visit(x, y);
            ++count;
        }
    }
    return count;
}

static std::string json_array_u64(const std::vector<uint64_t>& values) {
    std::string out = "[";
    for (size_t i = 0; i < values.size(); ++i) {
        if (i) out += ',';
        out += '"' + std::to_string(values[i]) + '"';
    }
    out += ']';
    return out;
}

int main(int argc, char** argv) {
    try {
        uint64_t low = 0, high = 0;
        int C = -1, D = -1;
        std::string json_path, candidates_path;
        bool quiet = false;
        uint64_t progress_every = 0;
        bool test_isqrt_set = false;
        uint64_t test_isqrt = 0;
        bool annulus_low_set = false, annulus_high_set = false;
        uint64_t annulus_low = 0, annulus_high = 0;
        bool activation_c_set = false, activation_d_set = false, activation_n_set = false;
        int activation_c = 0, activation_d = 0;
        uint64_t activation_n = 0;
        bool arithmetic_a_set = false, arithmetic_b_set = false, arithmetic_shift_set = false;
        uint64_t arithmetic_a = 0, arithmetic_b = 0, arithmetic_shift = 0;

        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            auto value = [&](const char* name) -> std::string {
                if (i + 1 >= argc) throw std::runtime_error(std::string("missing value for ") + name);
                return argv[++i];
            };
            if (arg == "--low") low = parse_u64_decimal(value("--low"), "--low");
            else if (arg == "--high") high = parse_u64_decimal(value("--high"), "--high");
            else if (arg == "--C") C = parse_bounded_exponent(value("--C"), "--C", 39);
            else if (arg == "--D") D = parse_bounded_exponent(value("--D"), "--D", 26);
            else if (arg == "--json") json_path = value("--json");
            else if (arg == "--candidates") candidates_path = value("--candidates");
            else if (arg == "--progress-every") progress_every = parse_u64_decimal(value("--progress-every"), "--progress-every");
            else if (arg == "--test-isqrt") {
                test_isqrt = parse_u64_decimal(value("--test-isqrt"), "--test-isqrt");
                test_isqrt_set = true;
            } else if (arg == "--test-annulus-low") {
                annulus_low = parse_u64_decimal(value("--test-annulus-low"), "--test-annulus-low");
                annulus_low_set = true;
            } else if (arg == "--test-annulus-high") {
                annulus_high = parse_u64_decimal(value("--test-annulus-high"), "--test-annulus-high");
                annulus_high_set = true;
            } else if (arg == "--test-activation-c") {
                activation_c = parse_bounded_exponent(value("--test-activation-c"), "--test-activation-c", 40);
                activation_c_set = true;
            } else if (arg == "--test-activation-d") {
                activation_d = parse_bounded_exponent(value("--test-activation-d"), "--test-activation-d", 27);
                activation_d_set = true;
            } else if (arg == "--test-activation-n") {
                activation_n = parse_u64_decimal(value("--test-activation-n"), "--test-activation-n");
                activation_n_set = true;
            } else if (arg == "--test-arithmetic-a") {
                arithmetic_a = parse_u64_decimal(value("--test-arithmetic-a"), "--test-arithmetic-a");
                arithmetic_a_set = true;
            } else if (arg == "--test-arithmetic-b") {
                arithmetic_b = parse_u64_decimal(value("--test-arithmetic-b"), "--test-arithmetic-b");
                arithmetic_b_set = true;
            } else if (arg == "--test-arithmetic-shift") {
                arithmetic_shift = parse_u64_decimal(value("--test-arithmetic-shift"), "--test-arithmetic-shift");
                arithmetic_shift_set = true;
            }
            else if (arg == "--quiet") quiet = true;
            else throw std::runtime_error("unknown argument: " + arg);
        }

        const bool annulus_mode = annulus_low_set || annulus_high_set;
        const bool activation_mode = activation_c_set || activation_d_set || activation_n_set;
        const bool arithmetic_mode = arithmetic_a_set || arithmetic_b_set || arithmetic_shift_set;
        const int test_mode_count = static_cast<int>(test_isqrt_set) + static_cast<int>(annulus_mode)
                                  + static_cast<int>(activation_mode) + static_cast<int>(arithmetic_mode);
        if (test_mode_count > 1) throw std::runtime_error("test modes are mutually exclusive");
        if (test_isqrt_set) {
            std::cout << "{\"implementation_id\":\"" << IMPLEMENTATION_ID
                      << "\",\"input\":\"" << test_isqrt
                      << "\",\"floor_sqrt\":\"" << isqrt_u64(test_isqrt) << "\"}\n";
            return 0;
        }
        if (annulus_mode) {
            if (!annulus_low_set || !annulus_high_set) throw std::runtime_error("both annulus bounds are required");
            std::vector<std::pair<uint64_t, uint64_t>> pairs;
            const uint64_t pair_count = enumerate_annulus_x_outer(
                annulus_low, annulus_high,
                [&](uint64_t x, uint64_t y) { pairs.push_back({x, y}); }
            );
            std::cout << "{\"implementation_id\":\"" << IMPLEMENTATION_ID
                      << "\",\"remainder_low\":\"" << annulus_low
                      << "\",\"remainder_high\":\"" << annulus_high
                      << "\",\"pair_count\":" << pair_count << ",\"pairs\":[";
            for (size_t i = 0; i < pairs.size(); ++i) {
                if (i) std::cout << ',';
                std::cout << "[\"" << pairs[i].first << "\",\"" << pairs[i].second << "\"]";
            }
            std::cout << "]}\n";
            return 0;
        }
        if (activation_mode) {
            if (!activation_c_set || !activation_d_set || !activation_n_set) {
                throw std::runtime_error("activation test requires c, d, and n");
            }
            const uint64_t shift = checked_add_u64(
                checked_pow(3, activation_c), checked_pow(5, activation_d), "activation shift"
            );
            const bool active = activation_n >= shift;
            uint64_t remainder = 0;
            std::vector<std::pair<uint64_t, uint64_t>> witnesses;
            if (active) {
                remainder = activation_n - shift;
                enumerate_annulus_x_outer(
                    remainder, remainder,
                    [&](uint64_t x, uint64_t y) { witnesses.push_back({x, y}); }
                );
            }
            std::cout << "{\"implementation_id\":\"" << IMPLEMENTATION_ID
                      << "\",\"c\":" << activation_c << ",\"d\":" << activation_d
                      << ",\"n\":\"" << activation_n << "\",\"shift\":\"" << shift
                      << "\",\"active\":" << (active ? "true" : "false")
                      << ",\"remainder\":" << (active ? "\"" + std::to_string(remainder) + "\"" : "null")
                      << ",\"two_square_remainder\":" << (!witnesses.empty() ? "true" : "false")
                      << ",\"witness\":";
            if (witnesses.empty()) std::cout << "null";
            else std::cout << "[\"" << witnesses[0].first << "\",\"" << witnesses[0].second << "\"]";
            std::cout << "}\n";
            return 0;
        }
        if (arithmetic_mode) {
            if (!arithmetic_a_set || !arithmetic_b_set || !arithmetic_shift_set) {
                throw std::runtime_error("arithmetic test requires a, b, and shift");
            }
            if (arithmetic_a > arithmetic_b) throw std::runtime_error("arithmetic test requires a <= b");
            if (arithmetic_b > UINT32_MAX) {
                throw std::runtime_error("square coordinate exceeds uint64-remainder contract");
            }
            const __uint128_t a2 = static_cast<__uint128_t>(arithmetic_a) * arithmetic_a;
            const __uint128_t b2 = static_cast<__uint128_t>(arithmetic_b) * arithmetic_b;
            const __uint128_t square_sum = a2 + b2;
            if (square_sum > UINT64_MAX) {
                throw std::runtime_error("square sum exceeds uint64 remainder contract");
            }
            const uint64_t represented = checked_add_u64(
                static_cast<uint64_t>(square_sum), arithmetic_shift, "represented n"
            );
            std::cout << "{\"implementation_id\":\"" << IMPLEMENTATION_ID
                      << "\",\"a\":\"" << arithmetic_a << "\",\"b\":\"" << arithmetic_b
                      << "\",\"a_squared\":\"" << static_cast<uint64_t>(a2)
                      << "\",\"b_squared\":\"" << static_cast<uint64_t>(b2)
                      << "\",\"square_sum\":\"" << static_cast<uint64_t>(square_sum)
                      << "\",\"shift\":\"" << arithmetic_shift
                      << "\",\"represented_n\":\"" << represented << "\"}\n";
            return 0;
        }

        if (low == 0 || high == 0 || low > high || C < 0 || D < 0 || json_path.empty()) {
            throw std::runtime_error(
                "required: --low L --high U --C C --D D --json FILE [--candidates FILE]"
            );
        }
        const uint64_t cap3 = checked_pow(3, C + 1);
        const uint64_t cap5 = checked_pow(5, D + 1);
        if (high >= cap3 + 1) throw std::runtime_error("strict C-domain inequality fails");
        if (high >= cap5 + 1) throw std::runtime_error("strict D-domain inequality fails");
        const uint64_t length64 = high - low + 1;
        if (length64 > static_cast<uint64_t>(SIZE_MAX)) throw std::runtime_error("interval too large for address space");
        const size_t length = static_cast<size_t>(length64);
        if (length > SIZE_MAX - 63) throw std::runtime_error("packed interval word count overflow");

        std::vector<uint64_t> p3(C + 1), p5(D + 1);
        for (int c = 0; c <= C; ++c) p3[c] = checked_pow(3, c);
        for (int d = 0; d <= D; ++d) p5[d] = checked_pow(5, d);

        std::map<uint64_t, std::vector<std::pair<int, int>>> by_shift;
        size_t admissible_rectangle_pairs = 0;
        for (int c = 0; c <= C; ++c) {
            for (int d = 0; d <= D; ++d) {
                __uint128_t sum = static_cast<__uint128_t>(p3[c]) + p5[d];
                if (sum <= high) {
                    by_shift[static_cast<uint64_t>(sum)].push_back({c, d});
                    ++admissible_rectangle_pairs;
                }
            }
        }
        std::vector<uint64_t> shifts;
        shifts.reserve(by_shift.size());
        for (const auto& entry : by_shift) shifts.push_back(entry.first);

        const size_t words = (length + 63) / 64;
        std::vector<uint64_t> alive(words, ~uint64_t(0));
        if (length % 64) alive.back() = (uint64_t(1) << (length % 64)) - 1;

        size_t survivors = length;
        uint64_t representation_pairs_enumerated = 0;
        size_t shifts_processed = 0;
        auto started = std::chrono::steady_clock::now();

        for (uint64_t shift : shifts) {
            if (shift > high) break;
            const uint64_t first_n = std::max(low, shift);
            if (first_n > high) continue;
            const uint64_t remainder_low = first_n - shift;
            const uint64_t remainder_high = high - shift;

            size_t newly_cleared = 0;
            const uint64_t pairs_this_shift = enumerate_annulus_x_outer(
                remainder_low, remainder_high,
                [&](uint64_t x, uint64_t y) {
                    const __uint128_t square_sum = static_cast<__uint128_t>(x) * x + static_cast<__uint128_t>(y) * y;
                    if (square_sum > UINT64_MAX) throw std::runtime_error("enumerated square sum overflow");
                    const uint64_t n = checked_add_u64(static_cast<uint64_t>(square_sum), shift, "represented n");
                    const size_t index = static_cast<size_t>(n - low);
                    uint64_t& word = alive[index >> 6];
                    const uint64_t mask = uint64_t(1) << (index & 63);
                    word &= ~mask;
                }
            );
            representation_pairs_enumerated = checked_add_u64(
                representation_pairs_enumerated, pairs_this_shift, "total unordered square-pair count"
            );
            ++shifts_processed;
            const size_t previous_survivors = survivors;
            survivors = 0;
            for (uint64_t word : alive) survivors += __builtin_popcountll(word);
            newly_cleared = previous_survivors - survivors;
            if (!quiet && (progress_every == 0 || shifts_processed <= 20 || shifts_processed % progress_every == 0 || survivors == 0)) {
                const double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
                std::cout << "SHIFT shift=" << shift
                          << " processed=" << shifts_processed
                          << " newly_cleared=" << newly_cleared
                          << " survivors=" << survivors
                          << " elapsed_seconds=" << seconds << '\n' << std::flush;
            }
            if (survivors == 0) break;
        }

        std::vector<uint64_t> candidates;
        candidates.reserve(survivors);
        for (size_t wi = 0; wi < alive.size(); ++wi) {
            uint64_t word = alive[wi];
            while (word) {
                const unsigned bit = __builtin_ctzll(word);
                const size_t index = wi * 64 + bit;
                if (index < length) candidates.push_back(low + index);
                word &= word - 1;
            }
        }
        if (candidates.size() != survivors) throw std::runtime_error("internal survivor count mismatch");

        if (!candidates_path.empty()) {
            std::ofstream out(candidates_path);
            if (!out) throw std::runtime_error("cannot write candidates file");
            for (uint64_t n : candidates) out << n << '\n';
        }

        const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
        std::ofstream js(json_path);
        if (!js) throw std::runtime_error("cannot write JSON output");
        js << "{\n"
           << "  \"method\": \"direct_two_squares_bitset_x_outer\",\n"
           << "  \"implementation_id\": \"" << IMPLEMENTATION_ID << "\",\n"
           << "  \"arithmetic\": \"exact uint64/__uint128; bitwise integer square root; no floating point\",\n"
           << "  \"low\": \"" << low << "\",\n"
           << "  \"high\": \"" << high << "\",\n"
           << "  \"C\": " << C << ",\n"
           << "  \"D\": " << D << ",\n"
           << "  \"three_power_next_plus_one\": \"" << cap3 + 1 << "\",\n"
           << "  \"five_power_next_plus_one\": \"" << cap5 + 1 << "\",\n"
           << "  \"strict_domain_inequalities_checked\": true,\n"
           << "  \"admissible_rectangle_pair_count_at_high\": " << admissible_rectangle_pairs << ",\n"
           << "  \"distinct_shift_count_at_high\": " << shifts.size() << ",\n"
           << "  \"duplicate_pair_count\": " << admissible_rectangle_pairs - shifts.size() << ",\n"
           << "  \"integers_tested\": " << length64 << ",\n"
           << "  \"shifts_processed_before_termination\": " << shifts_processed << ",\n"
           << "  \"unordered_square_pairs_enumerated\": " << representation_pairs_enumerated << ",\n"
           << "  \"candidate_count\": " << candidates.size() << ",\n"
           << "  \"candidates\": " << json_array_u64(candidates) << ",\n"
           << "  \"elapsed_seconds\": " << elapsed << ",\n"
           << "  \"classification\": \""
           << (candidates.empty()
                 ? "EXACT EXHAUSTIVE FINITE COMPUTATION: EVERY n IN INTERVAL HAS A REPRESENTATION"
                 : "EXACT CANDIDATES REQUIRE INDEPENDENT CERTIFICATE VERIFICATION")
           << "\"\n}\n";

        std::cout << "integers_tested=" << length64 << '\n'
                  << "admissible_pair_count_at_high=" << admissible_rectangle_pairs << '\n'
                  << "distinct_shift_count_at_high=" << shifts.size() << '\n'
                  << "shifts_processed=" << shifts_processed << '\n'
                  << "candidate_count=" << candidates.size() << '\n'
                  << "elapsed_seconds=" << elapsed << '\n'
                  << (candidates.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return candidates.empty() ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR " << e.what() << '\n';
        return 2;
    }
}
