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

static constexpr const char* IMPLEMENTATION_ID = "tn_clean_annulus_v1";

static uint64_t binary_isqrt(uint64_t input) {
    uint64_t low = 0;
    uint64_t high = uint64_t(1) << 32;
    while (low + 1 < high) {
        const uint64_t middle = low + (high - low) / 2;
        if (static_cast<__uint128_t>(middle) * middle <= input) low = middle;
        else high = middle;
    }
    return low;
}

static uint64_t binary_ceil_sqrt(uint64_t input) {
    const uint64_t root = binary_isqrt(input);
    return static_cast<__uint128_t>(root) * root == input ? root : root + 1;
}

static std::vector<SourcePair> enumerate_source_rectangle(uint64_t high_exclusive) {
    std::vector<uint64_t> threes{1};
    std::vector<uint64_t> fives{1};
    while (threes.back() <= (high_exclusive - 1) / 3) threes.push_back(threes.back() * 3);
    while (fives.back() <= (high_exclusive - 1) / 5) fives.push_back(fives.back() * 5);
    std::vector<SourcePair> result;
    for (size_t c = 0; c < threes.size(); ++c) {
        for (size_t d = 0; d < fives.size(); ++d) {
            const __uint128_t shift = static_cast<__uint128_t>(threes[c]) + fives[d];
            if (shift < high_exclusive) {
                result.push_back(SourcePair{
                    static_cast<uint32_t>(c), static_cast<uint32_t>(d), threes[c], fives[d],
                    static_cast<uint64_t>(shift)
                });
            }
        }
    }
    return result;
}

template <typename Visitor>
static void enumerate_b_outer(uint64_t lower, uint64_t upper, Visitor visit) {
    const uint64_t largest_b = binary_isqrt(upper);
    const uint64_t diagonal = binary_isqrt(upper / 2);
    uint64_t smallest_a = binary_ceil_sqrt(lower);
    uint64_t largest_a_after_diagonal = diagonal;
    for (uint64_t b = 0; b <= largest_b; ++b) {
        const __uint128_t b2 = static_cast<__uint128_t>(b) * b;
        while (smallest_a > 0 &&
               static_cast<__uint128_t>(smallest_a - 1) * (smallest_a - 1) + b2 >= lower) {
            --smallest_a;
        }
        uint64_t largest_a = b <= diagonal ? b : largest_a_after_diagonal;
        if (b > diagonal) {
            while (largest_a > 0 && static_cast<__uint128_t>(largest_a) * largest_a + b2 > upper) {
                --largest_a;
            }
            largest_a_after_diagonal = largest_a;
        }
        if (smallest_a > largest_a) continue;
        for (uint64_t a = smallest_a; a <= largest_a; ++a) visit(a, b);
    }
}

static std::optional<std::pair<uint64_t, uint64_t>> canonical_pair(uint64_t remainder) {
    std::optional<std::pair<uint64_t, uint64_t>> best;
    const uint64_t b_max = binary_isqrt(remainder);
    for (uint64_t b = 0; b <= b_max; ++b) {
        const uint64_t b2 = b * b;
        const uint64_t a2 = remainder - b2;
        const uint64_t a = binary_isqrt(a2);
        if (a <= b && a * a == a2) {
            const std::pair<uint64_t, uint64_t> candidate{a, b};
            if (!best.has_value() || candidate < *best) best = candidate;
        }
    }
    return best;
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--implementation-id") {
            std::cout << IMPLEMENTATION_ID << '\n';
            return 0;
        }
        const Config config = a303656_tn::parse_config(argc, argv);
        const size_t width = static_cast<size_t>(config.high - config.low);
        const std::vector<SourcePair> sources = enumerate_source_rectangle(config.high);
        std::vector<uint32_t> counts(width, 0);
        std::vector<uint32_t> active(width, 0);
        std::vector<uint8_t> represented(width, 0);

        for (const SourcePair& source : sources) {
            const uint64_t start = source.shift > config.low ? source.shift : config.low;
            if (start >= config.high) continue;
            for (size_t index = static_cast<size_t>(start - config.low); index < width; ++index) ++active[index];
            std::fill(represented.begin(), represented.end(), uint8_t(0));
            enumerate_b_outer(start - source.shift, config.high - source.shift - 1,
                [&](uint64_t a, uint64_t b) {
                    const __uint128_t remainder = static_cast<__uint128_t>(a) * a
                                                  + static_cast<__uint128_t>(b) * b;
                    const uint64_t n = source.shift + static_cast<uint64_t>(remainder);
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
                const auto pair = canonical_pair(remainder);
                if (pair.has_value()) result.push_back(Winner{source, remainder, pair->first, pair->second});
            }
            return result;
        };
        a303656_tn::write_outputs(
            config, IMPLEMENTATION_ID,
            "source-pair counting with b-outer annuli, byte per-pair dedup flags, and binary-search isqrt",
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
