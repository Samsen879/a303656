#!/usr/bin/env python3
"""Enumerator B: independent mod-q buckets with mod-q^2 exclusion buckets."""

from __future__ import annotations

from typing import Any

from common import canonical_digest, indices, mask_hex


def enumerate_compressed(q: int, pairs: list[dict[str, int]]) -> dict[str, Any]:
    q2 = q ** 2
    mod_q: dict[int, list[int]] = {}
    mod_q2: dict[tuple[int, int], list[int]] = {}
    for row in pairs:
        residue = row["shift"] % q
        lift = row["shift"] % q2
        mod_q.setdefault(residue, []).append(row["pair_index"])
        mod_q2.setdefault((residue, lift), []).append(row["pair_index"])
    buckets = []
    for residue in sorted(mod_q):
        exclusions = [[lift, mod_q2[(residue, lift)]] for lift in sorted(t for r, t in mod_q2 if r == residue)]
        exceptional = {lift for lift, _ in exclusions}
        ordinary = [residue + k * q for k in range(q) if residue + k * q not in exceptional]
        buckets.append({"residue_mod_q": residue, "full_lift_count": len(ordinary), "first_full_t": ordinary[0] if ordinary else None, "exclusions": exclusions})
    inactive = sorted(set(range(q)) - set(mod_q))
    compression = {
        "q": q,
        "q2_residue_count": q2,
        "empty_residue_class_count_mod_q": len(inactive),
        "empty_lift_count": len(inactive) * q,
        "first_empty_t": inactive[0] if inactive else None,
        "buckets": buckets,
    }
    compression["ordered_compressed_digest"] = canonical_digest(compression)
    return compression


def score(compression: dict[str, Any], base_mask: int, base_digest: str) -> dict[str, Any]:
    counts: dict[int, int] = {}
    winners: list[tuple[int, int, int]] = []
    for bucket in compression["buckets"]:
        full_indices = sorted({i for _lift, group in bucket["exclusions"] for i in group})
        full_mask = sum(1 << i for i in full_indices)
        if bucket["full_lift_count"]:
            delta = (full_mask | base_mask).bit_count() - base_mask.bit_count()
            counts[delta] = counts.get(delta, 0) + bucket["full_lift_count"]
            winners.append((delta, bucket["first_full_t"], full_mask | base_mask))
        for lift, group in bucket["exclusions"]:
            covered = full_mask ^ sum(1 << i for i in group)
            delta = (covered | base_mask).bit_count() - base_mask.bit_count()
            counts[delta] = counts.get(delta, 0) + 1
            winners.append((delta, lift, covered | base_mask))
    if compression["empty_lift_count"]:
        counts[0] = counts.get(0, 0) + compression["empty_lift_count"]
        winners.append((0, compression["first_empty_t"], base_mask))
    maximum = max(counts)
    first = min(t for delta, t, _union in winners if delta == maximum)
    unions = sorted({mask_hex(union) for delta, _t, union in winners if delta == maximum})
    result = {
        "histogram": [[delta, counts[delta]] for delta in sorted(counts)],
        "maximum_delta": maximum,
        "maximum_G5": base_mask.bit_count() + maximum,
        "minimum_residual_size": 407 - base_mask.bit_count() - maximum,
        "argmax_count": counts[maximum],
        "first_argmax_t": first,
        "maximum_union_masks_hex": unions,
        "distinct_maximum_union_mask_count": len(unions),
        "counts_below_maximum": {str(k): counts.get(maximum - k, 0) if maximum >= k else 0 for k in (1, 2, 3)},
    }
    result["canonical_scored_digest"] = canonical_digest({"q": compression["q"], "base": base_digest, **result})
    return result
