#!/usr/bin/env python3
"""Exact common utilities for the A303656 bounded search.

All arithmetic in this module is Python integer arithmetic.  No floating-point
operations are used to determine exponent domains or modular conditions.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence
import csv


@dataclass(frozen=True, order=True)
class PairShift:
    c: int
    d: int
    shift: int


def exact_powers(base: int, limit: int) -> list[int]:
    if base < 2:
        raise ValueError("base must be at least 2")
    if limit < 1:
        return []
    out: list[int] = []
    x = 1
    while x <= limit:
        out.append(x)
        x *= base
    return out


def enumerate_pairs(n: int) -> tuple[list[int], list[int], list[PairShift]]:
    """Enumerate all and only (c,d) with 3**c + 5**d <= n."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    p3 = exact_powers(3, n)
    p5 = exact_powers(5, n)
    pairs: list[PairShift] = []
    for c, x in enumerate(p3):
        for d, y in enumerate(p5):
            s = x + y
            if s > n:
                break
            pairs.append(PairShift(c, d, s))
    return p3, p5, pairs


def enumerate_rectangle(C: int, D: int) -> tuple[list[int], list[int], list[PairShift]]:
    if C < 0 or D < 0:
        raise ValueError("C,D must be nonnegative")
    p3 = [1]
    for _ in range(C):
        p3.append(p3[-1] * 3)
    p5 = [1]
    for _ in range(D):
        p5.append(p5[-1] * 5)
    pairs = [PairShift(c, d, x + y) for c, x in enumerate(p3) for d, y in enumerate(p5)]
    return p3, p5, pairs


def check_domain_bounds(C: int, D: int, n_high: int) -> None:
    """Check the strict finite-domain inequalities required by the brief."""
    if C < 0 or D < 0:
        raise ValueError("C,D must be nonnegative")
    if n_high >= pow(3, C + 1) + 1:
        raise ValueError(
            f"invalid C={C}: N_high={n_high} is not < 3^(C+1)+1={pow(3,C+1)+1}"
        )
    if n_high >= pow(5, D + 1) + 1:
        raise ValueError(
            f"invalid D={D}: N_high={n_high} is not < 5^(D+1)+1={pow(5,D+1)+1}"
        )


def is_prime_trial(n: int) -> bool:
    """Exact primality test for verifier prime pools.

    For n < 2**64 this uses the deterministic seven-base Miller--Rabin test.
    Larger Python integers fall back to exact trial division.  Thus verifier
    correctness never depends on a probable-prime answer.
    """
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    if n < 1 << 64:
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
            if a % n == 0:
                continue
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True
    f = 41
    while f <= n // f:
        if n % f == 0:
            return False
        f += 2
    return True


def validate_prime_pool(primes: Sequence[int]) -> list[int]:
    if not primes:
        raise ValueError("prime pool is empty")
    unique = sorted(set(int(p) for p in primes))
    if len(unique) != len(primes):
        raise ValueError("prime pool contains duplicates")
    for p in unique:
        if not is_prime_trial(p):
            raise ValueError(f"not prime: {p}")
        if p % 4 != 3:
            raise ValueError(f"prime is not 3 mod 4: {p}")
    return unique


def primes_3mod4(count: int) -> list[int]:
    if count <= 0:
        return []
    out: list[int] = []
    n = 3
    while len(out) < count:
        if n % 4 == 3 and is_prime_trial(n):
            out.append(n)
        n += 4
    return out


def parse_primes(text: str) -> list[int]:
    path = Path(text)
    try:
        is_file = path.is_file()
    except OSError:
        # A long comma-separated prime list is data, not a filesystem path.
        is_file = False
    if is_file:
        raw = path.read_text(encoding="utf-8")
    else:
        raw = text
    fields = raw.replace("\n", ",").replace(" ", ",").split(",")
    vals = [int(x) for x in fields if x.strip()]
    return validate_prime_pool(vals)


def valuation(n: int, p: int) -> int | None:
    """Return v_p(n) for n>0; return None for n=0 (not a finite valuation)."""
    if n < 0:
        raise ValueError("valuation called on negative integer")
    if n == 0:
        return None
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def exact_one_obstructs(remainder: int, p: int) -> bool:
    return remainder > 0 and remainder % p == 0 and remainder % (p * p) != 0


def active_pairs_from_rectangle(rect_pairs: Sequence[PairShift], n: int) -> list[PairShift]:
    return [ps for ps in rect_pairs if ps.shift <= n]


def load_assignment_csv(path: str | Path) -> dict[tuple[int, int], int]:
    ans: dict[tuple[int, int], int] = {}
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"c", "d", "prime"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"assignment CSV must contain columns {sorted(required)}")
        for row in reader:
            key = (int(row["c"]), int(row["d"]))
            if key in ans:
                raise ValueError(f"duplicate assignment row for {key}")
            ans[key] = int(row["prime"])
    return ans
