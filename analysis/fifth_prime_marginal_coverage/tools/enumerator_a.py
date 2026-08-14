#!/usr/bin/env python3
"""Enumerator A: direct q^2 event accumulation with compressed default lifts."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from common import canonical_digest, indices, mask_hex


def enumerate_compressed(q: int, pairs: list[dict[str, int]]) -> dict[str, Any]:
    q2 = q * q
    event_masks: dict[int, int] = {}
    for row in pairs:
        t = row["shift"] % q2
        event_masks[t] = event_masks.get(t, 0) | (1 << row["pair_index"])
    by_residue: dict[int, list[int]] = defaultdict(list)
    for t in event_masks:
        by_residue[t % q].append(t)
    buckets = []
    for residue in sorted(by_residue):
        exception_ts = sorted(by_residue[residue])
        full = 0
        exclusions = []
        for t in exception_ts:
            excluded = event_masks[t]
            full |= excluded
            exclusions.append([t, indices(excluded)])
        excluded_set = set(exception_ts)
        first_full = next((residue + k * q for k in range(q) if residue + k * q not in excluded_set), None)
        buckets.append({"residue_mod_q": residue, "full_lift_count": q - len(exception_ts), "first_full_t": first_full, "exclusions": exclusions})
    compression = {
        "q": q,
        "q2_residue_count": q2,
        "empty_residue_class_count_mod_q": q - len(buckets),
        "empty_lift_count": q * (q - len(buckets)),
        "first_empty_t": next((r for r in range(q) if r not in by_residue), None),
        "buckets": buckets,
    }
    compression["ordered_compressed_digest"] = canonical_digest(compression)
    return compression


def score(compression: dict[str, Any], base_mask: int, base_digest: str) -> dict[str, Any]:
    histogram: Counter[int] = Counter()
    maximum = -1
    argmax_count = 0
    first_argmax = None
    maximum_unions: set[int] = set()

    def consume(coverage: int, multiplicity: int, first_t: int | None) -> None:
        nonlocal maximum, argmax_count, first_argmax, maximum_unions
        if not multiplicity:
            return
        delta = (coverage & ~base_mask).bit_count()
        histogram[delta] += multiplicity
        union = coverage | base_mask
        if delta > maximum:
            maximum, argmax_count, first_argmax, maximum_unions = delta, multiplicity, first_t, {union}
        elif delta == maximum:
            argmax_count += multiplicity
            if first_t is not None and (first_argmax is None or first_t < first_argmax):
                first_argmax = first_t
            maximum_unions.add(union)

    consume(0, compression["empty_lift_count"], compression["first_empty_t"])
    for bucket in compression["buckets"]:
        full = 0
        for _t, excluded_indices in bucket["exclusions"]:
            for index in excluded_indices:
                full |= 1 << index
        consume(full, bucket["full_lift_count"], bucket["first_full_t"])
        for t, excluded_indices in bucket["exclusions"]:
            excluded = sum(1 << index for index in excluded_indices)
            consume(full & ~excluded, 1, t)
    result = {
        "histogram": [[delta, histogram[delta]] for delta in sorted(histogram)],
        "maximum_delta": maximum,
        "maximum_G5": base_mask.bit_count() + maximum,
        "minimum_residual_size": 407 - base_mask.bit_count() - maximum,
        "argmax_count": argmax_count,
        "first_argmax_t": first_argmax,
        "maximum_union_masks_hex": sorted(mask_hex(x) for x in maximum_unions),
        "distinct_maximum_union_mask_count": len(maximum_unions),
        "counts_below_maximum": {str(k): histogram.get(maximum - k, 0) if maximum >= k else 0 for k in (1, 2, 3)},
    }
    result["canonical_scored_digest"] = canonical_digest({"q": compression["q"], "base": base_digest, **result})
    return result
