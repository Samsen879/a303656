#!/usr/bin/env python3
"""Exact small-range cross-checks for the two direct two-square scanners.

The reference implementation is intentionally simple Python bigint brute force.
It enumerates the finite exponent rectangle and tests square sums directly.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path


def powers(base: int, exponent_max: int) -> list[int]:
    out = [1]
    for _ in range(exponent_max):
        out.append(out[-1] * base)
    return out


def brute_candidates(low: int, high: int, C: int, D: int) -> list[int]:
    shifts = sorted({
        x + y
        for x in powers(3, C)
        for y in powers(5, D)
        if x + y <= high
    })
    candidates: list[int] = []
    for n in range(low, high + 1):
        represented = False
        for shift in shifts:
            if shift > n:
                break
            remainder = n - shift
            a = 0
            while a * a <= remainder:
                b2 = remainder - a * a
                b = math.isqrt(b2)
                if b * b == b2:
                    represented = True
                    break
                a += 1
            if represented:
                break
        if not represented:
            candidates.append(n)
    return candidates


def run(binary: Path, low: int, high: int, C: int, D: int, stem: Path) -> dict:
    jpath = stem.with_suffix(".json")
    cpath = stem.with_suffix(".candidates")
    completed = subprocess.run(
        [
            str(binary), "--low", str(low), "--high", str(high),
            "--C", str(C), "--D", str(D),
            "--json", str(jpath), "--candidates", str(cpath), "--quiet",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode not in (0, 1):
        raise AssertionError(
            f"scanner failed rc={completed.returncode}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )
    data = json.loads(jpath.read_text(encoding="utf-8"))
    listed = [int(x) for x in cpath.read_text(encoding="utf-8").split()]
    declared = [int(x) for x in data["candidates"]]
    assert listed == declared
    assert completed.returncode == (1 if not declared else 0)
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", type=Path, required=True)
    parser.add_argument("--y", type=Path, required=True)
    parser.add_argument("--work", type=Path)
    args = parser.parse_args()

    cases = [
        # A deliberately surviving point proves the programs can emit candidates.
        (1, 1, 2, 1),
        # Complete low ranges and boundaries where new shifts become active.
        (2, 50, 4, 3),
        (2, 500, 6, 4),
        (17, 350, 6, 4),
        (240, 760, 6, 4),
    ]

    manager = tempfile.TemporaryDirectory() if args.work is None else None
    work = Path(manager.name) if manager is not None else args.work
    work.mkdir(parents=True, exist_ok=True)

    for index, (low, high, C, D) in enumerate(cases):
        assert high < 3 ** (C + 1) + 1
        assert high < 5 ** (D + 1) + 1
        expected = brute_candidates(low, high, C, D)
        x = run(args.x, low, high, C, D, work / f"case_{index}_x")
        y = run(args.y, low, high, C, D, work / f"case_{index}_y")
        cx = [int(v) for v in x["candidates"]]
        cy = [int(v) for v in y["candidates"]]
        assert cx == expected, (index, cx, expected)
        assert cy == expected, (index, cy, expected)
        for key in (
            "low", "high", "C", "D", "three_power_next_plus_one",
            "five_power_next_plus_one", "admissible_rectangle_pair_count_at_high",
            "distinct_shift_count_at_high", "duplicate_pair_count", "integers_tested",
            "shifts_processed_before_termination", "unordered_square_pairs_enumerated",
            "candidate_count", "candidates",
        ):
            assert x[key] == y[key], (index, key, x[key], y[key])
        print(
            f"case={index} interval=[{low},{high}] candidates={len(expected)} "
            f"lattice_pairs={x['unordered_square_pairs_enumerated']} PASS"
        )

    assert brute_candidates(1, 1, 2, 1) == [1]
    assert brute_candidates(2, 2, 2, 1) == []  # 2 = 0^2+0^2+1+1.
    print("candidate_emission_boundary: PASS")
    print("remainder_zero_representation_boundary: PASS")
    print("ALL_TWO_SQUARE_TESTS_PASS")
    if manager is not None:
        manager.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
