// Clean-room independent direct finite scanner for A303656.
//
// This implementation deliberately does not share the x-outer enumeration or
// integer-square-root code of search_twosquares_bitset.cpp.  It enumerates
// unordered square pairs with y as the outer variable, uses binary-search
// integer square root, and maintains the annulus x-boundaries in the opposite
// direction.  The candidate set is stored in a packed bit vector.
#include <chrono>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <system_error>
#include <utility>
#include <vector>

static constexpr const char* IMPLEMENTATION_ID = "search_twosquares_clean";

static uint64_t binary_isqrt(uint64_t n) {
    uint64_t lower = 0;
    uint64_t upper = uint64_t(1) << 32; // exclusive
    while (lower + 1 < upper) {
        const uint64_t middle = lower + (upper - lower) / 2;
        if (static_cast<__uint128_t>(middle) * middle <= n) lower = middle;
        else upper = middle;
    }
    return lower;
}

static uint64_t binary_ceil_sqrt(uint64_t n) {
    const uint64_t r = binary_isqrt(n);
    return static_cast<__uint128_t>(r) * r == n ? r : r + 1;
}

static uint64_t power_exact(uint64_t base, int exponent) {
    if (exponent < 0) throw std::runtime_error("negative exponent");
    __uint128_t value = 1;
    for (int k = 0; k < exponent; ++k) {
        value *= base;
        if (value > UINT64_MAX) throw std::runtime_error("power overflow");
    }
    return static_cast<uint64_t>(value);
}

static uint64_t decimal_u64(const std::string& text, const char* option) {
    if (text.empty()) throw std::runtime_error(std::string(option) + " requires a decimal value");
    uint64_t result = 0;
    const auto conversion = std::from_chars(text.data(), text.data() + text.size(), result, 10);
    if (conversion.ec == std::errc::result_out_of_range) {
        throw std::runtime_error(std::string(option) + " out of uint64 range");
    }
    if (conversion.ec != std::errc() || conversion.ptr != text.data() + text.size()) {
        throw std::runtime_error(std::string(option) + " must be unsigned decimal");
    }
    return result;
}

static int bounded_exponent(const std::string& text, const char* option, uint64_t maximum) {
    const uint64_t result = decimal_u64(text, option);
    if (result > maximum) {
        throw std::runtime_error(std::string(option) + " exceeds supported uint64 exponent range");
    }
    return static_cast<int>(result);
}

static uint64_t safe_sum(uint64_t left, uint64_t right, const char* label) {
    const __uint128_t result = static_cast<__uint128_t>(left) + right;
    if (result > UINT64_MAX) throw std::runtime_error(std::string(label) + " overflow");
    return static_cast<uint64_t>(result);
}

template <typename Visitor>
static uint64_t enumerate_annulus_y_outer(uint64_t lower_r, uint64_t upper_r, Visitor visit) {
    if (lower_r > upper_r) throw std::runtime_error("annulus lower bound exceeds upper bound");
    const uint64_t largest_y = binary_isqrt(upper_r);
    const uint64_t diagonal = binary_isqrt(upper_r / 2);
    uint64_t smallest_x = binary_ceil_sqrt(lower_r);
    uint64_t largest_x_after_diagonal = diagonal;
    uint64_t count = 0;
    for (uint64_t y = 0; y <= largest_y; ++y) {
        const __uint128_t y2 = static_cast<__uint128_t>(y) * y;
        while (smallest_x > 0 &&
               static_cast<__uint128_t>(smallest_x - 1) * (smallest_x - 1) + y2 >= lower_r) {
            --smallest_x;
        }
        uint64_t largest_x;
        if (y <= diagonal) {
            largest_x = y;
        } else {
            while (largest_x_after_diagonal > 0 &&
                   static_cast<__uint128_t>(largest_x_after_diagonal) * largest_x_after_diagonal + y2 > upper_r) {
                --largest_x_after_diagonal;
            }
            largest_x = largest_x_after_diagonal;
        }
        if (smallest_x > largest_x) continue;
        for (uint64_t x = smallest_x; x <= largest_x; ++x) {
            if (count == UINT64_MAX) throw std::runtime_error("annulus pair count overflow");
            visit(x, y);
            ++count;
        }
    }
    return count;
}

int main(int argc, char** argv) {
    try {
        uint64_t low = 0, high = 0;
        int C = -1, D = -1;
        std::string json_path, candidates_path;
        bool quiet = false;
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
            const std::string arg = argv[i];
            auto next = [&]() -> std::string {
                if (++i >= argc) throw std::runtime_error("missing option value");
                return argv[i];
            };
            if (arg == "--low") low = decimal_u64(next(), "--low");
            else if (arg == "--high") high = decimal_u64(next(), "--high");
            else if (arg == "--C") C = bounded_exponent(next(), "--C", 39);
            else if (arg == "--D") D = bounded_exponent(next(), "--D", 26);
            else if (arg == "--json") json_path = next();
            else if (arg == "--candidates") candidates_path = next();
            else if (arg == "--test-isqrt") {
                test_isqrt = decimal_u64(next(), "--test-isqrt");
                test_isqrt_set = true;
            } else if (arg == "--test-annulus-low") {
                annulus_low = decimal_u64(next(), "--test-annulus-low");
                annulus_low_set = true;
            } else if (arg == "--test-annulus-high") {
                annulus_high = decimal_u64(next(), "--test-annulus-high");
                annulus_high_set = true;
            } else if (arg == "--test-activation-c") {
                activation_c = bounded_exponent(next(), "--test-activation-c", 40);
                activation_c_set = true;
            } else if (arg == "--test-activation-d") {
                activation_d = bounded_exponent(next(), "--test-activation-d", 27);
                activation_d_set = true;
            } else if (arg == "--test-activation-n") {
                activation_n = decimal_u64(next(), "--test-activation-n");
                activation_n_set = true;
            } else if (arg == "--test-arithmetic-a") {
                arithmetic_a = decimal_u64(next(), "--test-arithmetic-a");
                arithmetic_a_set = true;
            } else if (arg == "--test-arithmetic-b") {
                arithmetic_b = decimal_u64(next(), "--test-arithmetic-b");
                arithmetic_b_set = true;
            } else if (arg == "--test-arithmetic-shift") {
                arithmetic_shift = decimal_u64(next(), "--test-arithmetic-shift");
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
                      << "\",\"floor_sqrt\":\"" << binary_isqrt(test_isqrt) << "\"}\n";
            return 0;
        }
        if (annulus_mode) {
            if (!annulus_low_set || !annulus_high_set) throw std::runtime_error("both annulus bounds are required");
            std::vector<std::pair<uint64_t, uint64_t>> pairs;
            const uint64_t pair_count = enumerate_annulus_y_outer(
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
            const uint64_t shift = safe_sum(
                power_exact(3, activation_c), power_exact(5, activation_d), "activation shift"
            );
            const bool active = activation_n >= shift;
            uint64_t remainder = 0;
            std::vector<std::pair<uint64_t, uint64_t>> witnesses;
            if (active) {
                remainder = activation_n - shift;
                enumerate_annulus_y_outer(
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
            const uint64_t represented = safe_sum(
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
        if (!low || !high || low > high || C < 0 || D < 0 || json_path.empty()) {
            throw std::runtime_error("missing required arguments");
        }
        const uint64_t next3 = power_exact(3, C + 1) + 1;
        const uint64_t next5 = power_exact(5, D + 1) + 1;
        if (high >= next3 || high >= next5) throw std::runtime_error("finite exponent-domain check failed");
        const uint64_t count64 = high - low + 1;
        if (count64 > SIZE_MAX) throw std::runtime_error("interval too large");
        const size_t count = static_cast<size_t>(count64);
        if (count > SIZE_MAX - 63) throw std::runtime_error("packed interval word count overflow");

        std::vector<uint64_t> powers3(C + 1), powers5(D + 1);
        for (int c = 0; c <= C; ++c) powers3[c] = power_exact(3, c);
        for (int d = 0; d <= D; ++d) powers5[d] = power_exact(5, d);
        std::set<uint64_t> shift_set;
        size_t pair_count = 0;
        for (uint64_t a : powers3) {
            for (uint64_t b : powers5) {
                const __uint128_t s = static_cast<__uint128_t>(a) + b;
                if (s <= high) {
                    shift_set.insert(static_cast<uint64_t>(s));
                    ++pair_count;
                }
            }
        }

        std::vector<uint64_t> remaining((count + 63) / 64, ~uint64_t(0));
        if (count % 64) remaining.back() = (uint64_t(1) << (count % 64)) - 1;
        size_t survivors = count;
        size_t shifts_used = 0;
        uint64_t lattice_pairs = 0;
        const auto start_time = std::chrono::steady_clock::now();

        for (uint64_t shift : shift_set) {
            if (shift > high) break;
            const uint64_t lower_r = low > shift ? low - shift : 0;
            const uint64_t upper_r = high - shift;
            size_t cleared_here = 0;
            const uint64_t pairs_this_shift = enumerate_annulus_y_outer(
                lower_r, upper_r,
                [&](uint64_t x, uint64_t y) {
                    const __uint128_t square_sum = static_cast<__uint128_t>(x) * x + static_cast<__uint128_t>(y) * y;
                    if (square_sum > UINT64_MAX) throw std::runtime_error("enumerated square sum overflow");
                    const uint64_t n = safe_sum(static_cast<uint64_t>(square_sum), shift, "represented n");
                    const size_t index = static_cast<size_t>(n - low);
                    uint64_t& word = remaining[index / 64];
                    const uint64_t mask = uint64_t(1) << (index % 64);
                    word &= ~mask;
                }
            );
            lattice_pairs = safe_sum(lattice_pairs, pairs_this_shift, "total unordered square-pair count");
            ++shifts_used;
            const size_t previous_survivors = survivors;
            survivors = 0;
            for (uint64_t word : remaining) survivors += __builtin_popcountll(word);
            cleared_here = previous_survivors - survivors;
            if (!quiet && (shifts_used <= 20 || shifts_used % 10 == 0 || survivors == 0)) {
                const double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - start_time).count();
                std::cout << "STEP shift=" << shift << " used=" << shifts_used
                          << " cleared=" << cleared_here << " survivors=" << survivors
                          << " elapsed_seconds=" << seconds << '\n' << std::flush;
            }
            if (survivors == 0) break;
        }

        std::vector<uint64_t> candidates;
        for (size_t word_index = 0; word_index < remaining.size(); ++word_index) {
            uint64_t word = remaining[word_index];
            while (word) {
                const unsigned bit = __builtin_ctzll(word);
                const size_t index = word_index * 64 + bit;
                if (index < count) candidates.push_back(low + index);
                word &= word - 1;
            }
        }
        if (candidates.size() != survivors) throw std::runtime_error("survivor mismatch");
        if (!candidates_path.empty()) {
            std::ofstream cfile(candidates_path);
            if (!cfile) throw std::runtime_error("cannot write candidate file");
            for (uint64_t n : candidates) cfile << n << '\n';
        }

        const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start_time).count();
        std::ofstream json(json_path);
        if (!json) throw std::runtime_error("cannot write JSON");
        json << "{\n"
             << "  \"method\": \"clean_room_direct_two_squares_y_outer\",\n"
             << "  \"implementation_id\": \"" << IMPLEMENTATION_ID << "\",\n"
             << "  \"arithmetic\": \"exact uint64/__uint128; binary-search integer square root; no floating point\",\n"
             << "  \"low\": \"" << low << "\",\n"
             << "  \"high\": \"" << high << "\",\n"
             << "  \"C\": " << C << ",\n"
             << "  \"D\": " << D << ",\n"
             << "  \"three_power_next_plus_one\": \"" << next3 << "\",\n"
             << "  \"five_power_next_plus_one\": \"" << next5 << "\",\n"
             << "  \"strict_domain_inequalities_checked\": true,\n"
             << "  \"admissible_rectangle_pair_count_at_high\": " << pair_count << ",\n"
             << "  \"distinct_shift_count_at_high\": " << shift_set.size() << ",\n"
             << "  \"duplicate_pair_count\": " << pair_count - shift_set.size() << ",\n"
             << "  \"integers_tested\": " << count64 << ",\n"
             << "  \"shifts_processed_before_termination\": " << shifts_used << ",\n"
             << "  \"unordered_square_pairs_enumerated\": " << lattice_pairs << ",\n"
             << "  \"candidate_count\": " << candidates.size() << ",\n"
             << "  \"candidates\": [";
        for (size_t i = 0; i < candidates.size(); ++i) {
            if (i) json << ',';
            json << '"' << candidates[i] << '"';
        }
        json << "],\n"
             << "  \"elapsed_seconds\": " << elapsed << ",\n"
             << "  \"classification\": \""
             << (candidates.empty()
                   ? "EXACT EXHAUSTIVE FINITE COMPUTATION: EVERY n IN INTERVAL HAS A REPRESENTATION"
                   : "EXACT CANDIDATES REQUIRE INDEPENDENT CERTIFICATE VERIFICATION")
             << "\"\n}\n";

        std::cout << "integers_tested=" << count64 << '\n'
                  << "admissible_pair_count_at_high=" << pair_count << '\n'
                  << "distinct_shift_count_at_high=" << shift_set.size() << '\n'
                  << "shifts_processed=" << shifts_used << '\n'
                  << "candidate_count=" << candidates.size() << '\n'
                  << "elapsed_seconds=" << elapsed << '\n'
                  << (candidates.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return candidates.empty() ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR " << e.what() << '\n';
        return 2;
    }
}
