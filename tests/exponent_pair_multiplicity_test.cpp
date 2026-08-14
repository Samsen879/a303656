#include <cstdint>
#include <iostream>
#include <optional>
#include <stdexcept>
#include <vector>

#include "../src/exponent_pair_multiplicity.hpp"

int main() {
    try {
        using a303656::ExponentPairSource;
        using a303656::TwoSquareWitness;
        const uint64_t n = 33;
        const std::vector<ExponentPairSource> sources = {
            {1, 2, 28},
            {3, 0, 28},
        };
        uint64_t evaluator_calls = 0;
        const auto result = a303656::account_exponent_pair_multiplicity(
            n,
            sources,
            [&](uint64_t remainder) -> std::optional<TwoSquareWitness> {
                ++evaluator_calls;
                if (remainder == 5) return TwoSquareWitness{1, 2};
                return std::nullopt;
            }
        );
        if (evaluator_calls != 1 || result.distinct_shift_evaluations != 1) {
            throw std::runtime_error("duplicate numerical shift was not reused exactly once");
        }
        if (result.successes.size() != 2) {
            throw std::runtime_error("exponent-pair multiplicity was collapsed or early-terminated");
        }
        if (result.successes[0].c != 1 || result.successes[0].d != 2 ||
            result.successes[1].c != 3 || result.successes[1].d != 0) {
            throw std::runtime_error("source exponent-pair records were not preserved in order");
        }
        for (const auto& success : result.successes) {
            if (success.shift != 28 || success.remainder != 5 ||
                success.witness.a != 1 || success.witness.b != 2) {
                throw std::runtime_error("machine-readable success record is inconsistent");
            }
        }
        std::cout << "{\"schema\":\"a303656-exponent-pair-multiplicity-test-v1\""
                  << ",\"n\":\"33\",\"distinct_shift_evaluations\":1"
                  << ",\"T\":2,\"successes\":[";
        for (size_t i = 0; i < result.successes.size(); ++i) {
            if (i) std::cout << ',';
            const auto& row = result.successes[i];
            std::cout << "{\"c\":" << row.c << ",\"d\":" << row.d
                      << ",\"shift\":\"" << row.shift
                      << "\",\"remainder\":\"" << row.remainder
                      << "\",\"witness\":[\"" << row.witness.a
                      << "\",\"" << row.witness.b << "\"]}";
        }
        std::cout << "]}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR " << error.what() << '\n';
        return 1;
    }
}
