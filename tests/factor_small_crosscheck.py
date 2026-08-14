#!/usr/bin/env python3
"""Exact small-domain cross-check for both all-prime factor-sieve implementations.

The reference implementation uses only Python integers and direct trial division.
It independently reconstructs the active-shift semantics, remainder-zero rule,
allowed odd valuations, and first-failure histogram.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path


def powers(base: int, limit: int) -> list[int]:
    out: list[int] = []
    value = 1
    while value <= limit:
        out.append(value)
        value *= base
    return out


def shift_data(high: int) -> tuple[list[int], int]:
    p3 = powers(3, high)
    p5 = powers(5, high)
    pairs = [(c, d, x + y) for c, x in enumerate(p3) for d, y in enumerate(p5) if x + y <= high]
    return sorted({s for _, _, s in pairs}), len(pairs)


def factorization(n: int) -> dict[int, int]:
    assert n > 0
    result: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def good_remainder(r: int, max_odd: int) -> bool:
    if r <= 0:
        return False
    for p, exponent in factorization(r).items():
        if p % 4 == 3 and exponent % 2 == 1 and (max_odd < 0 or exponent <= max_odd):
            return True
    return False


def reference(low: int, high: int, max_odd: int) -> dict[str, object]:
    shifts, pair_count = shift_data(high)
    alive = set(range(low, high + 1))
    histogram: list[dict[str, object]] = []
    shifts_processed = 0
    for shift in shifts:
        failures: list[int] = []
        for n in alive:
            # n < shift: inactive implication, hence no failure.
            # n == shift: remainder zero, hence no valuation obstruction.
            if n >= shift and not good_remainder(n - shift, max_odd):
                failures.append(n)
        if failures:
            for n in failures:
                alive.remove(n)
            histogram.append({"shift": str(shift), "count": len(failures)})
        shifts_processed += 1
        if not alive:
            break
    return {
        "pairs": pair_count,
        "shifts": len(shifts),
        "shifts_processed": shifts_processed,
        "candidates": sorted(alive),
        "histogram": histogram,
    }


def run(binary: Path, low: int, high: int, C: int, D: int, max_odd: int, directory: Path) -> dict:
    tag = f"{binary.name}_{max_odd}"
    output = directory / f"{tag}.json"
    candidates = directory / f"{tag}.txt"
    cp = subprocess.run(
        [
            str(binary), "--low", str(low), "--high", str(high),
            "--C", str(C), "--D", str(D), "--group-span", "1000",
            "--max-odd", str(max_odd), "--json", str(output),
            "--candidates", str(candidates), "--quiet",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if cp.returncode != 0:
        raise AssertionError(f"{binary} failed: rc={cp.returncode}\n{cp.stdout}\n{cp.stderr}")
    data = json.loads(output.read_text(encoding="utf-8"))
    listed = [int(x) for x in candidates.read_text(encoding="utf-8").split()]
    assert listed == [int(x) for x in data["candidates"]]
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--clean", type=Path, required=True)
    parser.add_argument("--low", type=int, default=2)
    parser.add_argument("--high", type=int, default=5000)
    parser.add_argument("--C", type=int, default=7)
    parser.add_argument("--D", type=int, default=5)
    args = parser.parse_args()
    assert args.high < 3 ** (args.C + 1) + 1
    assert args.high < 5 ** (args.D + 1) + 1

    with tempfile.TemporaryDirectory() as td:
        directory = Path(td)
        for max_odd in (1, 3, -1):
            expected = reference(args.low, args.high, max_odd)
            first = run(args.primary, args.low, args.high, args.C, args.D, max_odd, directory)
            second = run(args.clean, args.low, args.high, args.C, args.D, max_odd, directory)
            for actual in (first, second):
                assert actual["low"] == str(args.low)
                assert actual["high"] == str(args.high)
                assert actual["admissible_pair_count_at_high"] == expected["pairs"]
                assert actual["distinct_shift_count_at_high"] == expected["shifts"]
                assert actual["shifts_processed_before_termination"] == expected["shifts_processed"]
                assert [int(x) for x in actual["candidates"]] == expected["candidates"]
                assert actual["first_failure_histogram"] == expected["histogram"]
            mathematical_keys = (
                "low", "high", "C", "D", "finite_bound_3_rhs", "finite_bound_5_rhs",
                "max_odd", "admissible_pair_count_at_high", "distinct_shift_count_at_high",
                "integers_tested", "shifts_processed_before_termination", "candidate_count",
                "candidates", "first_failure_histogram",
            )
            assert all(first[key] == second[key] for key in mathematical_keys)
            print(
                f"mode={max_odd} candidates={len(expected['candidates'])} "
                f"shifts_processed={expected['shifts_processed']} PASS"
            )

    print("FACTOR_SMALL_CROSSCHECK_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
