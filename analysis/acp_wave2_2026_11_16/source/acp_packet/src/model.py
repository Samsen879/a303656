#!/usr/bin/env python3
"""Definition-level reference engine for the eventual-power model (A303656).

  beta_{p^k}(y) = #{(u,v) mod p^k : u^2+v^2 = y} / p^k            (mean 1)
  T_b(alpha)_p  = b^alpha (p != b),  0 (p == b)                    (eventual powers)
  F_q(a)        = E_{(alpha,beta)} prod_{p^k || q} beta_{p^k}(a - T_b1(alpha) - T_b2(beta)),
  f_q(a)        = pi * F_q(a).

Everything is exact (Fractions) and brute force; it is used only to validate
the reductions of Phase 1 on small moduli.
"""
from fractions import Fraction
from math import gcd
from functools import lru_cache
from arith import factorint


def lcm(a, b):
    return a // gcd(a, b) * b


@lru_cache(maxsize=None)
def beta_table(pk):
    """List of beta_{pk}(y), y = 0..pk-1, as integer counts (divide by pk)."""
    sq = [0] * pk
    for u in range(pk):
        sq[u * u % pk] += 1
    out = [0] * pk
    nz = [(t, c) for t, c in enumerate(sq) if c]
    for t1, c1 in nz:
        for t2, c2 in nz:
            out[(t1 + t2) % pk] += c1 * c2
    return out


def beta_zero_rule(p, k, y):
    """Closed-form zero rule (checked against beta_table in validate.py)."""
    y %= p ** k
    if y == 0:
        return False
    v = 0
    while y % p == 0:
        y //= p; v += 1
    if p == 2:
        return y % 4 == 3 and v + 2 <= k
    if p % 4 == 3:
        return v % 2 == 1 and v < k
    return False


def order_mod(b, m):
    assert gcd(b, m) == 1
    x, k = b % m, 1
    while x != 1:
        x = x * b % m; k += 1
    return k


def exponent_moduli(q, b1=3, b2=5):
    """Periods N1, N2 of the eventual sequences T_b1, T_b2 modulo q."""
    N1 = N2 = 1
    for p, k in factorint(q).items():
        pk = p ** k
        if p != b1 and gcd(b1, p) == 1:
            N1 = lcm(N1, order_mod(b1, pk))
        if p != b2 and gcd(b2, p) == 1:
            N2 = lcm(N2, order_mod(b2, pk))
    return N1, N2


def s_residues(q, b1=3, b2=5):
    """Dict pk -> (list over alpha of T_b1 mod pk, list over beta of T_b2 mod pk)."""
    N1, N2 = exponent_moduli(q, b1, b2)
    out = {}
    for p, k in factorint(q).items():
        pk = p ** k
        t1 = [0] * N1 if b1 % p == 0 else [pow(b1, al, pk) for al in range(N1)]
        t2 = [0] * N2 if b2 % p == 0 else [pow(b2, be, pk) for be in range(N2)]
        out[pk] = (t1, t2)
    return N1, N2, out


def F_q(q, a, b1=3, b2=5):
    """Exact F_q(a) = f_q(a)/pi as a Fraction."""
    N1, N2, res = s_residues(q, b1, b2)
    tabs = {pk: beta_table(pk) for pk in res}
    tot = 0
    den = 1
    for pk in res:
        den *= pk
    for al in range(N1):
        for be in range(N2):
            prod = 1
            for pk, (t1, t2) in res.items():
                prod *= tabs[pk][(a - t1[al] - t2[be]) % pk]
                if prod == 0:
                    break
            tot += prod
    return Fraction(tot, den * N1 * N2)


def class_zero_pattern(q, a, b1=3, b2=5):
    """Set of exponent classes (alpha mod N1, beta mod N2) on which the integrand vanishes."""
    N1, N2, res = s_residues(q, b1, b2)
    tabs = {pk: beta_table(pk) for pk in res}
    bad = set()
    for al in range(N1):
        for be in range(N2):
            if any(tabs[pk][(a - t1[al] - t2[be]) % pk] == 0 for pk, (t1, t2) in res.items()):
                bad.add((al, be))
    return N1, N2, bad
