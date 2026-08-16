#!/usr/bin/env python3
"""Independent exact checks supporting the regular-lift no-go proof audit."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def order(a: int, modulus: int) -> int:
    value = 1
    for exponent in range(1, modulus + 1):
        value = value * a % modulus
        if value == 1:
            return exponent
    raise AssertionError((a, modulus))


def vp_below(delta: int, p: int, K: int) -> int | None:
    delta %= p**K
    if delta == 0:
        return None
    exponent = 0
    while delta % p == 0:
        exponent += 1
        delta //= p
    return exponent


def s2_residues(modulus: int) -> set[int]:
    squares = {x * x % modulus for x in range(modulus)}
    return {(a + b) % modulus for a in squares for b in squares}


def lemma_checks() -> list[dict[str, int]]:
    rows = []
    for p in (3, 7, 11, 19, 31, 43):
        w = order(5, p)
        regular = order(5, p * p) == w * p
        if not regular:
            raise AssertionError((p, "unexpected nonregular test prime"))
        K = 3
        full_order = order(5, p**K)
        assert full_order == w * p ** (K - 1)
        subgroup = {pow(5, e, p**K) for e in range(full_order)}
        coarse = {pow(5, e, p) for e in range(w)}
        inverse_image = {x for x in range(1, p**K) if x % p in coarse and math.gcd(x, p) == 1}
        assert subgroup == inverse_image
        for q in range(1, p * p):
            valuation = vp_below(1 - pow(5, w * q, p**K), p, K)
            expected = 1
            copy = q
            while copy % p == 0:
                expected += 1
                copy //= p
            if expected >= K:
                assert valuation is None
            else:
                assert valuation == expected
        rows.append({"p": p, "w": w, "ord_p3": full_order, "subgroup_size": len(subgroup)})
    return rows


def exhaustive_small_model() -> dict[str, int | str]:
    K2 = 3
    odd_rows = [(3, 3), (7, 2)]
    period = math.lcm(order(5, 2**K2), *(order(5, p**K) for p, K in odd_rows))
    local_s2 = s2_residues(2**K2)
    tested = 0
    minimum_uncovered = 10**9
    maximum_covered = -1
    for r2 in range(2**K2):
        for r3 in range(3**3):
            for r7 in range(7**2):
                tested += 1
                covered = 0
                for c in (0, 1):
                    for d in range(period):
                        rem2 = (r2 - pow(3, c, 2**K2) - pow(5, d, 2**K2)) % (2**K2)
                        obstructed = rem2 not in local_s2
                        e3 = vp_below(r3 - pow(3, c, 3**3) - pow(5, d, 3**3), 3, 3)
                        e7 = vp_below(r7 - pow(3, c, 7**2) - pow(5, d, 7**2), 7, 2)
                        if obstructed or e3 == 1 or e7 == 1:
                            covered += 1
                cells = 2 * period
                uncovered = cells - covered
                assert uncovered > 0
                minimum_uncovered = min(minimum_uncovered, uncovered)
                maximum_covered = max(maximum_covered, covered)
    return {
        "cells_per_tuple": 2 * period,
        "maximum_covered": maximum_covered,
        "minimum_uncovered": minimum_uncovered,
        "period": period,
        "residue_tuples": tested,
        "status": "PASS_NO_COMPLETE_COVER",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schema": "a303656-regular-lift-theorem-audit-v1",
        "classification": "PROVED_NEGATIVE_STRUCTURAL_THEOREM_PENDING_AUTHORITY_REVIEW",
        "lemma_checks": lemma_checks(),
        "small_complete_model": exhaustive_small_model(),
        "scope": {
            "anchors_used": [0, 1],
            "arbitrary_finite_regular_bad_prime_set": True,
            "base5_nonregular_primes": "NOT COVERED",
            "global_nonlocal_mechanisms": "NOT COVERED",
            "universal_strip_target": "UNRESOLVED",
        },
        "verdict": "PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
