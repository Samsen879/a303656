#pragma once

#include <cstdint>
#include <map>
#include <optional>
#include <stdexcept>
#include <vector>

namespace a303656 {

struct ExponentPairSource {
    uint32_t c;
    uint32_t d;
    uint64_t shift;
};

struct TwoSquareWitness {
    uint64_t a;
    uint64_t b;
};

struct SuccessfulExponentPair {
    uint32_t c;
    uint32_t d;
    uint64_t shift;
    uint64_t remainder;
    TwoSquareWitness witness;
};

struct MultiplicityAccounting {
    uint64_t distinct_shift_evaluations = 0;
    std::vector<SuccessfulExponentPair> successes;
};

template <typename RemainderEvaluator>
MultiplicityAccounting account_exponent_pair_multiplicity(
    uint64_t n,
    const std::vector<ExponentPairSource>& sources,
    RemainderEvaluator evaluate_remainder
) {
    MultiplicityAccounting result;
    std::map<uint64_t, std::optional<TwoSquareWitness>> status_by_shift;
    for (const ExponentPairSource& source : sources) {
        if (source.shift > n) continue;
        auto found = status_by_shift.find(source.shift);
        if (found == status_by_shift.end()) {
            if (result.distinct_shift_evaluations == UINT64_MAX) {
                throw std::runtime_error("distinct shift evaluation count overflow");
            }
            const uint64_t remainder = n - source.shift;
            found = status_by_shift.emplace(source.shift, evaluate_remainder(remainder)).first;
            ++result.distinct_shift_evaluations;
        }
        if (found->second.has_value()) {
            result.successes.push_back(SuccessfulExponentPair{
                source.c,
                source.d,
                source.shift,
                n - source.shift,
                *found->second,
            });
        }
    }
    return result;
}

}  // namespace a303656
