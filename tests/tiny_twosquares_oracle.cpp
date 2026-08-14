// Independent, deliberately simple small-range oracle for direct scanner tests.
//
// This file includes no production headers.  Representations and annuli are
// generated with explicit GMP-integer nested loops; production square-root,
// annulus, and packed-bit code is not called or copied.
#include <gmpxx.h>

#include <cstdint>
#include <iostream>
#include <optional>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

struct Pair {
    uint64_t a;
    uint64_t b;
};

struct SourcePair {
    unsigned c;
    unsigned d;
    uint64_t shift;
};

static mpz_class natural(const std::string& text, const char* name) {
    mpz_class value;
    if (text.empty() || mpz_set_str(value.get_mpz_t(), text.c_str(), 10) != 0 || value < 0) {
        throw std::runtime_error(std::string(name) + " must be a nonnegative decimal integer");
    }
    return value;
}

static uint64_t tiny_u64(const std::string& text, const char* name) {
    const mpz_class value = natural(text, name);
    if (!mpz_fits_ulong_p(value.get_mpz_t())) {
        throw std::runtime_error(std::string(name) + " does not fit uint64");
    }
    const uint64_t result = value.get_ui();
    if (result > 1000000) {
        throw std::runtime_error(std::string(name) + " exceeds the tiny-oracle limit");
    }
    return result;
}

static unsigned tiny_exponent(const std::string& text, const char* name) {
    const uint64_t value = tiny_u64(text, name);
    if (value > 20) throw std::runtime_error(std::string(name) + " exceeds 20");
    return static_cast<unsigned>(value);
}

static std::vector<Pair> brute_exact_remainder(uint64_t remainder) {
    const mpz_class target = remainder;
    std::vector<Pair> pairs;
    for (uint64_t a = 0;; ++a) {
        const mpz_class a2 = mpz_class(a) * a;
        if (a2 > target) break;
        for (uint64_t b = a;; ++b) {
            const mpz_class sum = a2 + mpz_class(b) * b;
            if (sum > target) break;
            if (sum == target) pairs.push_back(Pair{a, b});
        }
    }
    return pairs;
}

static std::vector<Pair> brute_annulus(uint64_t lower, uint64_t upper) {
    if (lower > upper) throw std::runtime_error("annulus lower exceeds upper");
    const mpz_class lo = lower;
    const mpz_class hi = upper;
    std::vector<Pair> pairs;
    for (uint64_t a = 0;; ++a) {
        const mpz_class a2 = mpz_class(a) * a;
        if (a2 + a2 > hi) break;
        for (uint64_t b = a;; ++b) {
            const mpz_class sum = a2 + mpz_class(b) * b;
            if (sum > hi) break;
            if (sum >= lo) pairs.push_back(Pair{a, b});
        }
    }
    return pairs;
}

static void print_pairs(const std::vector<Pair>& pairs) {
    std::cout << '[';
    for (size_t i = 0; i < pairs.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << "[\"" << pairs[i].a << "\",\"" << pairs[i].b << "\"]";
    }
    std::cout << ']';
}

static std::vector<SourcePair> source_pairs(uint64_t high, unsigned C, unsigned D) {
    std::vector<SourcePair> result;
    for (unsigned c = 0; c <= C; ++c) {
        mpz_class p3;
        mpz_ui_pow_ui(p3.get_mpz_t(), 3, c);
        for (unsigned d = 0; d <= D; ++d) {
            mpz_class p5;
            mpz_ui_pow_ui(p5.get_mpz_t(), 5, d);
            const mpz_class shift = p3 + p5;
            if (shift <= high) result.push_back(SourcePair{c, d, shift.get_ui()});
        }
    }
    return result;
}

static void interval_mode(uint64_t low, uint64_t high, unsigned C, unsigned D) {
    if (low == 0 || low > high) throw std::runtime_error("invalid tiny interval");
    const auto sources = source_pairs(high, C, D);
    std::set<uint64_t> distinct_shifts;
    for (const auto& source : sources) distinct_shifts.insert(source.shift);

    uint64_t scanner_pair_visits = 0;
    for (uint64_t shift : distinct_shifts) {
        const uint64_t lower_r = low > shift ? low - shift : 0;
        const uint64_t upper_r = high - shift;
        const auto pairs = brute_annulus(lower_r, upper_r);
        scanner_pair_visits += pairs.size();
    }

    std::cout << "{\"schema\":\"a303656-independent-gmp-tiny-oracle-v1\""
              << ",\"gmp_version\":\"" << gmp_version << "\""
              << ",\"low\":\"" << low << "\",\"high\":\"" << high
              << "\",\"C\":" << C << ",\"D\":" << D
              << ",\"source_pair_count\":" << sources.size()
              << ",\"distinct_shift_count\":" << distinct_shifts.size()
              << ",\"scanner_unordered_pair_visits\":" << scanner_pair_visits
              << ",\"marked\":[";
    bool first_marked = true;
    std::vector<std::string> rows;
    for (uint64_t n = low; n <= high; ++n) {
        uint64_t success_count = 0;
        std::optional<std::tuple<unsigned, unsigned, uint64_t, uint64_t, Pair>> witness;
        for (const auto& source : sources) {
            if (source.shift > n) continue;
            const uint64_t remainder = n - source.shift;
            const auto pairs = brute_exact_remainder(remainder);
            if (!pairs.empty()) {
                ++success_count;
                if (!witness.has_value()) {
                    witness = std::make_tuple(source.c, source.d, source.shift, remainder, pairs.front());
                }
            }
        }
        if (success_count) {
            if (!first_marked) std::cout << ',';
            std::cout << '"' << n << '"';
            first_marked = false;
        }
        std::string row = "{\"n\":\"" + std::to_string(n) + "\",\"representable\":"
                        + (success_count ? "true" : "false")
                        + ",\"exponent_pair_success_count\":" + std::to_string(success_count)
                        + ",\"witness\":";
        if (!witness.has_value()) {
            row += "null}";
        } else {
            const auto [c, d, shift, remainder, pair] = *witness;
            row += "{\"c\":" + std::to_string(c)
                 + ",\"d\":" + std::to_string(d)
                 + ",\"shift\":\"" + std::to_string(shift)
                 + "\",\"remainder\":\"" + std::to_string(remainder)
                 + "\",\"a\":\"" + std::to_string(pair.a)
                 + "\",\"b\":\"" + std::to_string(pair.b) + "\"}}";
        }
        rows.push_back(row);
        if (n == UINT64_MAX) break;
    }
    std::cout << "],\"rows\":[";
    for (size_t i = 0; i < rows.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << rows[i];
    }
    std::cout << "]}\n";
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--gmp-version") {
            std::cout << gmp_version << '\n';
            return 0;
        }
        if (argc == 3 && std::string(argv[1]) == "--isqrt") {
            const mpz_class input = natural(argv[2], "isqrt input");
            mpz_class root;
            mpz_sqrt(root.get_mpz_t(), input.get_mpz_t());
            std::cout << "{\"input\":\"" << input << "\",\"floor_sqrt\":\"" << root
                      << "\",\"gmp_version\":\"" << gmp_version << "\"}\n";
            return 0;
        }
        if (argc == 4 && std::string(argv[1]) == "--annulus") {
            const uint64_t lower = tiny_u64(argv[2], "annulus lower");
            const uint64_t upper = tiny_u64(argv[3], "annulus upper");
            const auto pairs = brute_annulus(lower, upper);
            std::cout << "{\"lower\":\"" << lower << "\",\"upper\":\"" << upper
                      << "\",\"pair_count\":" << pairs.size() << ",\"pairs\":";
            print_pairs(pairs);
            std::cout << "}\n";
            return 0;
        }
        if (argc == 6 && std::string(argv[1]) == "--interval") {
            interval_mode(
                tiny_u64(argv[2], "low"),
                tiny_u64(argv[3], "high"),
                tiny_exponent(argv[4], "C"),
                tiny_exponent(argv[5], "D")
            );
            return 0;
        }
        std::cerr << "usage: tiny_twosquares_oracle --gmp-version | --isqrt N | "
                     "--annulus LOW HIGH | --interval LOW HIGH C D\n";
        return 2;
    } catch (const std::exception& error) {
        std::cerr << "ERROR " << error.what() << '\n';
        return 2;
    }
}
