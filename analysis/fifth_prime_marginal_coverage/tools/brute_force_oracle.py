#!/usr/bin/env python3
"""Literal small-prime valuation oracle; deliberately loops through every t mod q^2."""

from __future__ import annotations

from collections import Counter
from typing import Any

from common import canonical_digest, mask_hex

SMALL_PRIMES = (19, 31, 43)


def literal_score(q: int, pairs: list[dict[str, int]], base_mask: int, base_digest: str) -> dict[str, Any]:
    q2 = q * q
    histogram: Counter[int] = Counter()
    maximum = -1
    argmax_count = 0
    first = None
    unions: set[int] = set()
    for t in range(q2):
        coverage = 0
        for row in pairs:
            value = t - row["shift"]
            valuation = 0
            while value and value % q == 0:
                valuation += 1
                value //= q
            if valuation == 1:
                coverage |= 1 << row["pair_index"]
        delta = (coverage & ~base_mask).bit_count()
        histogram[delta] += 1
        if delta > maximum:
            maximum, argmax_count, first, unions = delta, 1, t, {coverage | base_mask}
        elif delta == maximum:
            argmax_count += 1
            unions.add(coverage | base_mask)
    result = {
        "histogram": [[d, histogram[d]] for d in sorted(histogram)],
        "maximum_delta": maximum,
        "maximum_G5": base_mask.bit_count() + maximum,
        "minimum_residual_size": 407 - base_mask.bit_count() - maximum,
        "argmax_count": argmax_count,
        "first_argmax_t": first,
        "maximum_union_masks_hex": sorted(mask_hex(x) for x in unions),
        "distinct_maximum_union_mask_count": len(unions),
        "counts_below_maximum": {str(k): histogram.get(maximum - k, 0) if maximum >= k else 0 for k in (1, 2, 3)},
    }
    result["canonical_scored_digest"] = canonical_digest({"q": q, "base": base_digest, **result})
    return result
