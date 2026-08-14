#!/usr/bin/env python3
"""Small-range exact cross-checks for both all-prime factor-sieve implementations."""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path


def powers(base: int, limit: int) -> list[int]:
    out: list[int] = []
    x = 1
    while x <= limit:
        out.append(x)
        x *= base
    return out


def factor(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError(n)
    ans: dict[int, int] = {}
    q = 2
    while q * q <= n:
        while n % q == 0:
            ans[q] = ans.get(q, 0) + 1
            n //= q
        q = 3 if q == 2 else q + 2
    if n > 1:
        ans[n] = ans.get(n, 0) + 1
    return ans


def remainder_is_obstructed(r: int, max_odd: int) -> bool:
    if r <= 0:
        return False
    for p, e in factor(r).items():
        if p % 4 == 3 and e % 2 == 1 and (max_odd < 0 or e <= max_odd):
            return True
    return False


def brute_candidates(low: int, high: int, max_odd: int) -> list[int]:
    p3 = powers(3, high)
    p5 = powers(5, high)
    shifts = sorted({x + y for x in p3 for y in p5 if x + y <= high})
    result: list[int] = []
    for n in range(low, high + 1):
        if all(s > n or remainder_is_obstructed(n - s, max_odd) for s in shifts):
            result.append(n)
    return result


def run(binary: Path, low: int, high: int, C: int, D: int, max_odd: int, stem: Path) -> dict:
    json_path = stem.with_suffix('.json')
    candidates_path = stem.with_suffix('.txt')
    subprocess.run(
        [
            str(binary), '--low', str(low), '--high', str(high), '--C', str(C), '--D', str(D),
            '--group-span', '200', '--max-odd', str(max_odd), '--json', str(json_path),
            '--candidates', str(candidates_path), '--quiet',
        ],
        check=True,
    )
    data = json.loads(json_path.read_text())
    listed = [int(x) for x in candidates_path.read_text().split()]
    assert listed == [int(x) for x in data['candidates']]
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--v1', type=Path, required=True)
    parser.add_argument('--v2', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    low, high, C, D = 2, 10_000, 8, 5
    for max_odd in (1, 3, -1):
        expected = brute_candidates(low, high, max_odd)
        a = run(args.v1, low, high, C, D, max_odd, args.work / f'v1_m{max_odd}')
        b = run(args.v2, low, high, C, D, max_odd, args.work / f'v2_m{max_odd}')
        ca = [int(x) for x in a['candidates']]
        cb = [int(x) for x in b['candidates']]
        assert ca == expected, (max_odd, ca[:10], expected[:10])
        assert cb == expected, (max_odd, cb[:10], expected[:10])
        assert a['candidate_count'] == b['candidate_count'] == len(expected)
        assert a['admissible_pair_count_at_high'] == b['admissible_pair_count_at_high']
        assert a['distinct_shift_count_at_high'] == b['distinct_shift_count_at_high']
        assert a['first_failure_histogram'] == b['first_failure_histogram']
        print(f'max_odd={max_odd}: candidates={len(expected)} exact cross-check PASS')

    # Boundary test: n=s=2 must fail because remainder zero has no valuation.
    assert 2 not in brute_candidates(2, 2, -1)
    print('remainder_zero_boundary: PASS')
    print('ALL_FACTOR_SIEVE_TESTS_PASS')


if __name__ == '__main__':
    main()
