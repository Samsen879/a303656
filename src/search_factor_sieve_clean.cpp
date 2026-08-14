// Clean-room exact all-prime segmented factor search for bounded A303656.
//
// This implementation is deliberately separate from search_factor_sieve.cpp:
// * linear prime sieve rather than Eratosthenes;
// * byte survivor array rather than packed words;
// * independently written shift grouping, factoring, and accounting;
// * pure-integer square root.
//
// For each positive remainder r, it determines exactly whether some prime
// p == 3 (mod 4) occurs to an allowed odd valuation.  --max-odd -1 means any
// odd valuation; --max-odd 1 means valuation exactly one; --max-odd 3 means
// valuation one or three.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

uint64_t integer_sqrt(uint64_t n) {
    uint64_t left = 0;
    uint64_t right = std::min<uint64_t>(n, 0xffffffffULL);
    while (left != right) {
        const uint64_t middle = left + (right - left + 1) / 2;
        if (middle <= n / middle) left = middle;
        else right = middle - 1;
    }
    return left;
}

uint64_t power_checked(uint64_t base, int exponent) {
    uint64_t value = 1;
    for (int i = 0; i < exponent; ++i) {
        if (value > std::numeric_limits<uint64_t>::max() / base) {
            throw std::runtime_error("integer power overflow");
        }
        value *= base;
    }
    return value;
}

std::vector<uint32_t> linear_primes(uint32_t limit) {
    std::vector<uint32_t> least(static_cast<size_t>(limit) + 1, 0);
    std::vector<uint32_t> primes;
    for (uint32_t x = 2; x <= limit; ++x) {
        if (least[x] == 0) {
            least[x] = x;
            primes.push_back(x);
        }
        for (uint32_t p : primes) {
            const uint64_t y = static_cast<uint64_t>(p) * x;
            if (y > limit || p > least[x]) break;
            least[static_cast<size_t>(y)] = p;
        }
    }
    return primes;
}

bool valuation_is_allowed(unsigned exponent, int max_odd) {
    if ((exponent & 1U) == 0U) return false;
    return max_odd < 0 || exponent <= static_cast<unsigned>(max_odd);
}

struct ClassifiedBlock {
    uint64_t low = 0;
    uint64_t high = 0;
    uint64_t multiple_visits = 0;
    uint64_t exact_divisions = 0;
    uint64_t good_count = 0;
    std::vector<uint8_t> has_obstruction;
};

ClassifiedBlock factor_block(
    uint64_t low,
    uint64_t high,
    const std::vector<uint32_t>& primes,
    int max_odd
) {
    if (low == 0 || low > high) throw std::runtime_error("bad factor block");
    const uint64_t length64 = high - low + 1;
    if (length64 > std::numeric_limits<size_t>::max()) throw std::runtime_error("factor block too large");
    const size_t length = static_cast<size_t>(length64);

    ClassifiedBlock result;
    result.low = low;
    result.high = high;
    result.has_obstruction.assign(length, 0);
    std::vector<uint64_t> unfactored(length);
    for (size_t i = 0; i < length; ++i) unfactored[i] = low + static_cast<uint64_t>(i);

    const uint64_t root = integer_sqrt(high);
    for (uint32_t p32 : primes) {
        const uint64_t p = p32;
        if (p > root) break;
        const uint64_t residue = low % p;
        uint64_t value = residue == 0 ? low : low + (p - residue);
        while (value <= high) {
            ++result.multiple_visits;
            const size_t index = static_cast<size_t>(value - low);
            unsigned exponent = 0;
            while (unfactored[index] % p == 0) {
                unfactored[index] /= p;
                ++exponent;
                ++result.exact_divisions;
            }
            if (p % 4 == 3 && valuation_is_allowed(exponent, max_odd)) {
                result.has_obstruction[index] = 1;
            }
            if (high - value < p) break;
            value += p;
        }
    }

    // A remaining cofactor greater than one is necessarily one prime factor
    // with exponent one: any composite residual would have a prime divisor no
    // larger than sqrt(original) <= sqrt(high), already removed above.
    for (size_t i = 0; i < length; ++i) {
        const uint64_t q = unfactored[i];
        if (q > 1 && q % 4 == 3 && (max_odd < 0 || max_odd >= 1)) {
            result.has_obstruction[i] = 1;
        }
        result.good_count += result.has_obstruction[i] != 0;
    }
    return result;
}

void write_json_string(std::ostream& out, const std::string& s) {
    out << '"';
    for (char ch : s) {
        if (ch == '"' || ch == '\\') out << '\\';
        out << ch;
    }
    out << '"';
}

}  // namespace

int main(int argc, char** argv) {
    try {
        uint64_t low = 0;
        uint64_t high = 0;
        uint64_t group_span = 1000000;
        int C = -1;
        int D = -1;
        int max_odd = 1;
        bool quiet = false;
        std::string json_file;
        std::string candidate_file;

        for (int i = 1; i < argc; ++i) {
            const std::string arg = argv[i];
            auto value = [&]() -> std::string {
                if (++i >= argc) throw std::runtime_error("missing option value");
                return argv[i];
            };
            if (arg == "--low") low = std::stoull(value());
            else if (arg == "--high") high = std::stoull(value());
            else if (arg == "--C") C = std::stoi(value());
            else if (arg == "--D") D = std::stoi(value());
            else if (arg == "--group-span") group_span = std::stoull(value());
            else if (arg == "--max-odd") max_odd = std::stoi(value());
            else if (arg == "--json") json_file = value();
            else if (arg == "--candidates") candidate_file = value();
            else if (arg == "--quiet") quiet = true;
            else throw std::runtime_error("unknown option: " + arg);
        }

        if (low < 2 || high < low || C < 0 || D < 0 || group_span == 0 || json_file.empty()) {
            throw std::runtime_error("required: --low --high --C --D --json, with low >= 2");
        }
        if (!(max_odd == -1 || (max_odd > 0 && (max_odd & 1)))) {
            throw std::runtime_error("--max-odd must be -1 or a positive odd number");
        }

        const uint64_t next3 = power_checked(3, C + 1);
        const uint64_t next5 = power_checked(5, D + 1);
        if (next3 == std::numeric_limits<uint64_t>::max() || high >= next3 + 1) {
            throw std::runtime_error("N_high < 3^(C+1)+1 failed");
        }
        if (next5 == std::numeric_limits<uint64_t>::max() || high >= next5 + 1) {
            throw std::runtime_error("N_high < 5^(D+1)+1 failed");
        }

        std::vector<uint64_t> powers3(static_cast<size_t>(C) + 1, 1);
        std::vector<uint64_t> powers5(static_cast<size_t>(D) + 1, 1);
        for (int c = 1; c <= C; ++c) powers3[c] = powers3[c - 1] * 3;
        for (int d = 1; d <= D; ++d) powers5[d] = powers5[d - 1] * 5;

        std::vector<uint64_t> all_shifts;
        uint64_t pair_count = 0;
        for (int c = 0; c <= C; ++c) {
            for (int d = 0; d <= D; ++d) {
                if (powers3[c] <= high && powers5[d] <= high - powers3[c]) {
                    all_shifts.push_back(powers3[c] + powers5[d]);
                    ++pair_count;
                }
            }
        }
        std::sort(all_shifts.begin(), all_shifts.end());
        all_shifts.erase(std::unique(all_shifts.begin(), all_shifts.end()), all_shifts.end());
        if (all_shifts.empty()) throw std::runtime_error("empty shift set");

        const uint64_t maximum_remainder = high - all_shifts.front();
        const uint64_t prime_limit64 = integer_sqrt(maximum_remainder);
        if (prime_limit64 > std::numeric_limits<uint32_t>::max()) throw std::runtime_error("prime limit overflow");
        const std::vector<uint32_t> primes = linear_primes(static_cast<uint32_t>(prime_limit64));

        const uint64_t total64 = high - low + 1;
        if (total64 > std::numeric_limits<size_t>::max()) throw std::runtime_error("search interval too large");
        const size_t total = static_cast<size_t>(total64);
        std::vector<uint8_t> alive(total, 1);
        uint64_t alive_count = total64;
        std::vector<uint64_t> failure_count(all_shifts.size(), 0);

        struct GroupInfo {
            uint64_t low;
            uint64_t high;
            uint64_t values;
            uint64_t multiple_visits;
            uint64_t exact_divisions;
            uint64_t marked;
        };
        std::vector<GroupInfo> groups;
        size_t shifts_done = 0;
        const auto start = std::chrono::steady_clock::now();

        for (size_t first = 0; first < all_shifts.size() && alive_count != 0; ) {
            size_t last = first;
            while (last + 1 < all_shifts.size() && all_shifts[last + 1] - all_shifts[first] <= group_span) {
                ++last;
            }
            const uint64_t minimum_shift = all_shifts[first];
            const uint64_t maximum_shift = all_shifts[last];
            const uint64_t factor_low = low > maximum_shift ? low - maximum_shift : 1;
            const uint64_t factor_high = high - minimum_shift;
            ClassifiedBlock block = factor_block(factor_low, factor_high, primes, max_odd);
            groups.push_back({block.low, block.high, block.high - block.low + 1,
                              block.multiple_visits, block.exact_divisions, block.good_count});

            for (size_t si = first; si <= last && alive_count != 0; ++si) {
                const uint64_t shift = all_shifts[si];
                for (size_t index = 0; index < total; ++index) {
                    if (!alive[index]) continue;
                    const uint64_t n = low + static_cast<uint64_t>(index);
                    bool covered = true;
                    if (n >= shift) {
                        if (n == shift) {
                            covered = false;
                        } else {
                            const uint64_t remainder = n - shift;
                            if (remainder < block.low || remainder > block.high) {
                                throw std::runtime_error("factor-block index invariant failed");
                            }
                            covered = block.has_obstruction[static_cast<size_t>(remainder - block.low)] != 0;
                        }
                    }
                    if (!covered) {
                        alive[index] = 0;
                        --alive_count;
                        ++failure_count[si];
                    }
                }
                ++shifts_done;
                if (!quiet) std::cout << "SHIFT " << shift << " survivors=" << alive_count << '\n';
            }
            first = last + 1;
        }

        std::vector<uint64_t> candidates;
        candidates.reserve(static_cast<size_t>(alive_count));
        for (size_t i = 0; i < total; ++i) if (alive[i]) candidates.push_back(low + static_cast<uint64_t>(i));
        const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();

        if (!candidate_file.empty()) {
            std::ofstream out(candidate_file);
            if (!out) throw std::runtime_error("cannot open candidate output");
            for (uint64_t n : candidates) out << n << '\n';
        }

        std::ofstream json(json_file);
        if (!json) throw std::runtime_error("cannot open JSON output");
        json << "{\n";
        json << "  \"method\": \"exact_all_prime_segmented_factor_sieve_clean_room\",\n";
        json << "  \"low\": \"" << low << "\",\n";
        json << "  \"high\": \"" << high << "\",\n";
        json << "  \"C\": " << C << ",\n";
        json << "  \"D\": " << D << ",\n";
        json << "  \"finite_bound_3_rhs\": \"" << next3 + 1 << "\",\n";
        json << "  \"finite_bound_5_rhs\": \"" << next5 + 1 << "\",\n";
        json << "  \"max_odd\": " << max_odd << ",\n";
        json << "  \"certificate_family\": ";
        if (max_odd == -1) write_json_string(json, "all primes p=3 mod 4 with arbitrary odd v_p");
        else if (max_odd == 1) write_json_string(json, "all primes p=3 mod 4 with v_p=1");
        else write_json_string(json, "all primes p=3 mod 4 with odd v_p <= max_odd");
        json << ",\n";
        json << "  \"admissible_pair_count_at_high\": " << pair_count << ",\n";
        json << "  \"distinct_shift_count_at_high\": " << all_shifts.size() << ",\n";
        json << "  \"integers_tested\": " << total64 << ",\n";
        json << "  \"shifts_processed_before_termination\": " << shifts_done << ",\n";
        json << "  \"factor_groups_processed\": " << groups.size() << ",\n";
        json << "  \"candidate_count\": " << candidates.size() << ",\n";
        json << "  \"candidates\": [";
        for (size_t i = 0; i < candidates.size(); ++i) {
            if (i) json << ',';
            json << '"' << candidates[i] << '"';
        }
        json << "],\n";
        json << "  \"first_failure_histogram\": [";
        bool first_hist = true;
        for (size_t i = 0; i < failure_count.size(); ++i) {
            if (failure_count[i] == 0) continue;
            if (!first_hist) json << ',';
            first_hist = false;
            json << "{\"shift\":\"" << all_shifts[i] << "\",\"count\":" << failure_count[i] << '}';
        }
        json << "],\n";
        json << "  \"factor_groups\": [";
        for (size_t i = 0; i < groups.size(); ++i) {
            if (i) json << ',';
            const GroupInfo& g = groups[i];
            json << "{\"low\":\"" << g.low << "\",\"high\":\"" << g.high
                 << "\",\"values\":" << g.values << ",\"prime_multiple_visits\":" << g.multiple_visits
                 << ",\"division_steps\":" << g.exact_divisions << ",\"marked\":" << g.marked << '}';
        }
        json << "],\n";
        json << "  \"elapsed_seconds\": " << elapsed << ",\n";
        json << "  \"classification\": ";
        write_json_string(json, candidates.empty()
            ? "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE STATED ALL-PRIME CERTIFICATE FAMILY"
            : "CANDIDATES REQUIRE INDEPENDENT VERIFICATION");
        json << "\n}\n";

        std::cout << "integers_tested=" << total64 << '\n';
        std::cout << "admissible_pair_count_at_high=" << pair_count << '\n';
        std::cout << "distinct_shift_count_at_high=" << all_shifts.size() << '\n';
        std::cout << "shifts_processed_before_termination=" << shifts_done << '\n';
        std::cout << "candidate_count=" << candidates.size() << '\n';
        std::cout << "elapsed_seconds=" << elapsed << '\n';
        std::cout << (candidates.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR " << error.what() << '\n';
        return 2;
    }
}
