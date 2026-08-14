#include "tn_pilot_output.hpp"

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <optional>
#include <stdexcept>
#include <vector>

using a303656_tn::Config;
using a303656_tn::SourcePair;
using a303656_tn::Winner;

static constexpr const char* IMPLEMENTATION_ID = "tn_bitset_annulus_v1";

static uint64_t bitwise_isqrt(uint64_t input) {
    uint64_t remainder = input;
    uint64_t root = 0;
    uint64_t bit = uint64_t(1) << 62;
    while (bit > remainder) bit >>= 2;
    while (bit) {
        if (remainder >= root + bit) {
            remainder -= root + bit;
            root = (root >> 1) + bit;
        } else {
            root >>= 1;
        }
        bit >>= 2;
    }
    return root;
}

static uint64_t bitwise_ceil_sqrt(uint64_t input) {
    const uint64_t root = bitwise_isqrt(input);
    return static_cast<__uint128_t>(root) * root == input ? root : root + 1;
}

static std::vector<SourcePair> make_sources(uint64_t high_exclusive) {
    std::vector<SourcePair> result;
    uint64_t power3 = 1;
    for (uint32_t c = 0;; ++c) {
        uint64_t power5 = 1;
        for (uint32_t d = 0;; ++d) {
            const __uint128_t shift = static_cast<__uint128_t>(power3) + power5;
            if (shift < high_exclusive) {
                result.push_back(SourcePair{c, d, power3, power5, static_cast<uint64_t>(shift)});
            }
            if (power5 > (high_exclusive - 1) / 5) break;
            power5 *= 5;
        }
        if (power3 > (high_exclusive - 1) / 3) break;
        power3 *= 3;
    }
    return result;
}

template <typename Visitor>
static void enumerate_a_outer(uint64_t lower, uint64_t upper, Visitor visit) {
    const uint64_t a_max = bitwise_isqrt(upper / 2);
    uint64_t b_high = bitwise_isqrt(upper);
    uint64_t b_low = bitwise_ceil_sqrt(lower);
    for (uint64_t a = 0; a <= a_max; ++a) {
        const __uint128_t a2 = static_cast<__uint128_t>(a) * a;
        while (b_high >= a && a2 + static_cast<__uint128_t>(b_high) * b_high > upper) --b_high;
        while (b_low > a && a2 + static_cast<__uint128_t>(b_low - 1) * (b_low - 1) >= lower) --b_low;
        const uint64_t first_b = std::max(a, b_low);
        for (uint64_t b = first_b; b <= b_high; ++b) visit(a, b);
    }
}

static std::optional<std::pair<uint64_t, uint64_t>> canonical_pair(uint64_t remainder) {
    const uint64_t a_max = bitwise_isqrt(remainder / 2);
    for (uint64_t a = 0; a <= a_max; ++a) {
        const uint64_t a2 = a * a;
        const uint64_t b2 = remainder - a2;
        const uint64_t b = bitwise_isqrt(b2);
        if (b >= a && b * b == b2) return std::make_pair(a, b);
    }
    return std::nullopt;
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--implementation-id") {
            std::cout << IMPLEMENTATION_ID << '\n';
            return 0;
        }
        const Config config = a303656_tn::parse_config(argc, argv);
        const size_t width = static_cast<size_t>(config.high - config.low);
        const std::vector<SourcePair> sources = make_sources(config.high);
        std::vector<uint32_t> counts(width, 0);
        std::vector<uint32_t> active(width, 0);
        std::vector<uint64_t> represented((width + 63) / 64, 0);

        for (const SourcePair& source : sources) {
            const uint64_t first_n = std::max(config.low, source.shift);
            if (first_n >= config.high) continue;
            for (uint64_t n = first_n; n < config.high; ++n) ++active[static_cast<size_t>(n - config.low)];
            std::fill(represented.begin(), represented.end(), 0);
            enumerate_a_outer(first_n - source.shift, config.high - 1 - source.shift,
                [&](uint64_t a, uint64_t b) {
                    const uint64_t sum = static_cast<uint64_t>(
                        static_cast<__uint128_t>(a) * a + static_cast<__uint128_t>(b) * b
                    );
                    const uint64_t n = source.shift + sum;
                    const size_t index = static_cast<size_t>(n - config.low);
                    uint64_t& word = represented[index >> 6];
                    const uint64_t mask = uint64_t(1) << (index & 63);
                    if ((word & mask) == 0) {
                        word |= mask;
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
                const auto pair = canonical_pair(remainder);
                if (pair.has_value()) {
                    result.push_back(Winner{source, remainder, pair->first, pair->second});
                }
            }
            return result;
        };
        a303656_tn::write_outputs(
            config, IMPLEMENTATION_ID,
            "source-pair counting with a-outer annuli, packed per-pair dedup bits, and bitwise isqrt",
            sources, counts, active, winners
        );
        std::cout << "TN_BACKEND_PASS implementation_id=" << IMPLEMENTATION_ID
                  << " interval=[" << config.low << ',' << config.high << ")"
                  << " integers=" << width << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR " << error.what() << '\n';
        return 2;
    }
}
