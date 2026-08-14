#include "../src/tn_pilot_output.hpp"

#include <gmpxx.h>

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <optional>
#include <stdexcept>
#include <vector>

using a303656_tn::Config;
using a303656_tn::SourcePair;
using a303656_tn::Winner;

static constexpr const char* IMPLEMENTATION_ID = "tn_gmp_uv_oracle_v1";

static uint64_t gmp_floor_sqrt(const mpz_class& value) {
    mpz_class root;
    mpz_sqrt(root.get_mpz_t(), value.get_mpz_t());
    if (!mpz_fits_ulong_p(root.get_mpz_t())) throw std::runtime_error("GMP root exceeds uint64");
    return root.get_ui();
}

static uint64_t gmp_ceil_sqrt(const mpz_class& value) {
    const uint64_t root = gmp_floor_sqrt(value);
    const mpz_class square = mpz_class(root) * root;
    return square == value ? root : root + 1;
}

static std::vector<SourcePair> reference_sources(uint64_t high_exclusive) {
    std::vector<SourcePair> result;
    for (uint32_t c = 0;; ++c) {
        mpz_class power3;
        mpz_ui_pow_ui(power3.get_mpz_t(), 3, c);
        if (power3 >= high_exclusive) break;
        for (uint32_t d = 0;; ++d) {
            mpz_class power5;
            mpz_ui_pow_ui(power5.get_mpz_t(), 5, d);
            if (power5 >= high_exclusive) break;
            const mpz_class shift = power3 + power5;
            if (shift < high_exclusive) {
                result.push_back(SourcePair{c, d, power3.get_ui(), power5.get_ui(), shift.get_ui()});
            }
        }
    }
    return result;
}

template <typename Visitor>
static void enumerate_uv_reference(uint64_t lower, uint64_t upper, Visitor visit) {
    const mpz_class twice_lower = mpz_class(lower) * 2;
    const mpz_class twice_upper = mpz_class(upper) * 2;
    const uint64_t u_max = gmp_floor_sqrt(mpz_class(upper));
    uint64_t v_high = gmp_floor_sqrt(twice_upper);
    uint64_t v_low = gmp_ceil_sqrt(twice_lower);
    for (uint64_t u = 0; u <= u_max; ++u) {
        const mpz_class u2 = mpz_class(u) * u;
        while (v_high >= u && u2 + mpz_class(v_high) * v_high > twice_upper) --v_high;
        while (v_low > u && u2 + mpz_class(v_low - 1) * (v_low - 1) >= twice_lower) --v_low;
        uint64_t v = std::max(u, v_low);
        if ((v & 1) != (u & 1)) ++v;
        for (; v <= v_high; v += 2) {
            const mpz_class doubled_sum = u2 + mpz_class(v) * v;
            if (!mpz_even_p(doubled_sum.get_mpz_t())) throw std::runtime_error("u/v parity invariant failed");
            const mpz_class sum = doubled_sum / 2;
            const uint64_t a = (v - u) / 2;
            const uint64_t b = (v + u) / 2;
            visit(a, b, sum.get_ui());
            if (v > UINT64_MAX - 2) break;
        }
    }
}

static std::optional<std::pair<uint64_t, uint64_t>> canonical_reference(uint64_t remainder) {
    const mpz_class target = remainder;
    for (uint64_t a = 0;; ++a) {
        const mpz_class a2 = mpz_class(a) * a;
        if (a2 + a2 > target) break;
        const mpz_class b2 = target - a2;
        mpz_class b;
        mpz_sqrt(b.get_mpz_t(), b2.get_mpz_t());
        if (b * b == b2 && b >= a) return std::make_pair(a, b.get_ui());
    }
    return std::nullopt;
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--implementation-id") {
            std::cout << IMPLEMENTATION_ID << '\n';
            return 0;
        }
        if (argc == 2 && std::string(argv[1]) == "--gmp-version") {
            std::cout << gmp_version << '\n';
            return 0;
        }
        const Config config = a303656_tn::parse_config(argc, argv);
        const size_t width = static_cast<size_t>(config.high - config.low);
        const std::vector<SourcePair> sources = reference_sources(config.high);
        std::vector<uint32_t> counts(width, 0);
        std::vector<uint32_t> active(width, 0);
        std::vector<uint8_t> represented(width, 0);

        for (const SourcePair& source : sources) {
            const uint64_t first_n = std::max(config.low, source.shift);
            if (first_n >= config.high) continue;
            for (uint64_t n = first_n; n < config.high; ++n) ++active[static_cast<size_t>(n - config.low)];
            std::fill(represented.begin(), represented.end(), uint8_t(0));
            enumerate_uv_reference(first_n - source.shift, config.high - 1 - source.shift,
                [&](uint64_t a, uint64_t b, uint64_t remainder) {
                    if (a > b) throw std::runtime_error("u/v map violated a <= b");
                    const uint64_t n = source.shift + remainder;
                    const size_t index = static_cast<size_t>(n - config.low);
                    if (!represented[index]) {
                        represented[index] = 1;
                        ++counts[index];
                    }
                }
            );
        }

        auto winners = [&](uint64_t n) {
            std::vector<Winner> result;
            for (const SourcePair& source : sources) {
                if (source.shift > n) continue;
                const uint64_t remainder = n - source.shift;
                const auto pair = canonical_reference(remainder);
                if (pair.has_value()) result.push_back(Winner{source, remainder, pair->first, pair->second});
            }
            return result;
        };
        a303656_tn::write_outputs(
            config, IMPLEMENTATION_ID,
            "independent GMP reference using u=b-a, v=b+a annuli and byte per-pair dedup flags",
            sources, counts, active, winners
        );
        std::cout << "TN_ORACLE_PASS implementation_id=" << IMPLEMENTATION_ID
                  << " gmp_version=" << gmp_version
                  << " interval=[" << config.low << ',' << config.high << ")"
                  << " integers=" << width << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR " << error.what() << '\n';
        return 2;
    }
}
