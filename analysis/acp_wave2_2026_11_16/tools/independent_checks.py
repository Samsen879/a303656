#!/usr/bin/env python3
"""Independent, standard-library-only checks of selected ACP wave-2 claims.

This script was written separately from the producer packet and shares no code
with it.  It checks finite statements only:

  1. every line of source/acp_packet/SHA256SUMS;
  2. the explicit 18-prime beta-line covering of Z/315 (REPORT.md section 3.5);
  3. the Proposition H horizon: the reciprocal sum over inert primes
     7 <= p <= 473899 is >= 1, and is < 1 without the last prime
     (directed-rounding decimal bounds, 50 digits);
  4. Lemma L4 by brute force for M in {3,5,7,11,13} and primes p < 3000,
     p = 1 mod M, all coset pairs and all z (asserting the stated bounds);
  5. class (0,0) has no z = 0 fibre point: 9^a + 25^b != 0 mod p for inert
     p < 400 (the general reason: -1 is a non-square mod p).

None of this verifies an analytic argument, Theorem A, or Theorem R.
"""
from __future__ import annotations

import decimal
import hashlib
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
PACKET = PACKAGE / "source" / "acp_packet"
WITNESS = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for q in WITNESS:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in WITNESS:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> set[int]:
    out, q = set(), 2
    while q * q <= n:
        while n % q == 0:
            out.add(q)
            n //= q
        q += 1
    if n > 1:
        out.add(n)
    return out


def order(b: int, p: int) -> int:
    o = p - 1
    for q in prime_factors(p - 1):
        while o % q == 0 and pow(b, o // q, p) == 1:
            o //= q
    return o


def oddpart(n: int) -> int:
    while n % 2 == 0:
        n //= 2
    return n


def check_sums() -> None:
    lines = (PACKET / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    bad = []
    for line in lines:
        digest, name = line.split(maxsplit=1)
        name = name.strip().lstrip("*")
        if hashlib.sha256((PACKET / name).read_bytes()).hexdigest() != digest:
            bad.append(name)
    assert not bad, f"hash mismatches: {bad}"
    print(f"[PASS] packet SHA256SUMS: {len(lines)} entries")


BETA_LINE = [
    (7, 3, 0), (11, 5, 3), (19, 9, 7), (31, 3, 2), (43, 21, 7), (71, 5, 1),
    (127, 21, 4), (211, 35, 22), (379, 21, 19), (631, 35, 15), (883, 63, 31),
    (1171, 45, 34), (5167, 9, 1), (7603, 21, 16), (19531, 7, 6),
    (23311, 315, 274), (34651, 315, 314), (169831, 45, 20),
]


def check_beta_line() -> None:
    assert len({p for p, _, _ in BETA_LINE}) == len(BETA_LINE)
    for p, h, _ in BETA_LINE:
        assert is_prime(p) and p % 4 == 3, p
        assert oddpart(order(5, p)) == h, (p, h)
    assert all(any(b % h == r for _, h, r in BETA_LINE) for b in range(315))
    print("[PASS] 18 inert primes, h5 values exact, residues cover Z/315")


def check_horizon() -> None:
    primes = [p for p in range(7, 473900) if p % 4 == 3 and is_prime(p)]

    def total(rounding, seq):
        ctx = decimal.Context(prec=50, rounding=rounding)
        acc = decimal.Decimal(0)
        for p in seq:
            acc = ctx.add(acc, ctx.divide(decimal.Decimal(1), decimal.Decimal(p)))
        return acc

    lower_full = total(decimal.ROUND_FLOOR, primes)
    upper_without_last = total(decimal.ROUND_CEILING, primes[:-1])
    assert primes[-1] == 473899 and len(primes) == 19789
    assert lower_full >= 1 and upper_without_last < 1
    print(f"[PASS] Proposition H horizon: {len(primes)} inert primes up to 473899; "
          "sum >= 1, and < 1 without the last prime")


def check_l4(p_max: int = 3000) -> None:
    observed: dict[tuple[int, str], int] = {}
    for m in (3, 5, 7, 11, 13):
        for p in range(m + 1, p_max):
            if p % m != 1 or not is_prime(p):
                continue
            fs = prime_factors(p - 1)
            g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fs))
            mu = [pow(g, (p - 1) // m * k, p) for k in range(m)]
            cosets, seen = [], set()
            for u in range(1, p):
                key = min(u * x % p for x in mu)
                if key not in seen:
                    seen.add(key)
                    cosets.append(sorted(u * x % p for x in mu))
            for i, a in enumerate(cosets):
                for b in cosets[i:]:
                    counts: dict[int, int] = {}
                    for x in a:
                        for y in b:
                            z = (x + y) % p
                            counts[z] = counts.get(z, 0) + 1
                    same = a == b
                    for z, c in counts.items():
                        if z == 0:
                            assert c in (0, m), (m, p, c)
                            continue
                        limit = (m - 2 if m >= 5 else m - 1) if same else (m - 1) // 2
                        assert c <= limit, (m, p, z, c)
                        key = (m, "same" if same else "diff")
                        observed[key] = max(observed.get(key, 0), c)
    print(f"[PASS] Lemma L4 bounds by brute force (p < {p_max}); observed maxima:",
          {f"M={m} {k}": v for (m, k), v in sorted(observed.items())})


def check_class00() -> None:
    for p in range(7, 400):
        if p % 4 == 3 and is_prime(p):
            assert all((pow(9, a, p) + pow(25, b, p)) % p for a in range(40) for b in range(40)), p
    print("[PASS] class (0,0): no z = 0 fibre point for inert p < 400")


def main() -> int:
    check_sums()
    check_beta_line()
    check_horizon()
    check_l4()
    check_class00()
    print("ACP_INDEPENDENT_CHECKS_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
