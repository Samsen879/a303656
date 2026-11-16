#!/usr/bin/env python3
"""Exact arithmetic helpers for the ACP package (A303656).

Everything here is deterministic.  Primality is certified either by complete
trial division (n < TD_LIMIT) or by a recursive Pratt (Lucas) certificate, so no
unproved pseudoprime test is ever relied on.
"""
from math import isqrt, gcd
import random

try:
    import gmpy2
    HAVE_GMP = True
except ImportError:  # pure-python fallback
    gmpy2 = None
    HAVE_GMP = False

TD_LIMIT = 10 ** 13  # below this we certify primality by complete trial division


def sieve(n):
    """List of primes <= n."""
    if n < 2:
        return []
    bs = bytearray([1]) * (n + 1)
    bs[0] = bs[1] = 0
    for i in range(2, isqrt(n) + 1):
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
    return [i for i in range(n + 1) if bs[i]]


_SMALL = sieve(4 * 10 ** 6)  # enough for complete trial division up to 1.6e13
_SMALL_SET = set(_SMALL)


def is_prime_td(n):
    """Deterministic primality by complete trial division (n < TD_LIMIT)."""
    if n < 2:
        return False
    if n <= _SMALL[-1]:
        return n in _SMALL_SET
    assert n < TD_LIMIT, "trial division limit exceeded"
    r = isqrt(n)
    for p in _SMALL:
        if p > r:
            return True
        if n % p == 0:
            return False
    return True


def _mr(n, a):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def probable_prime(n):
    """Fast filter only (never used as a proof)."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    return all(_mr(n, a) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37))


def pollard_rho(n, seed=1):
    if n % 2 == 0:
        return 2
    rng = random.Random(seed)
    while True:
        c = rng.randrange(1, n)
        y = rng.randrange(0, n)
        m, g, r, q = 128, 1, 1, 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def factorint(n):
    """Complete factorisation {prime: exponent}; primes are probable primes for
    n >= TD_LIMIT (callers that need proofs use certify_prime)."""
    out = {}
    if n <= 1:
        return out
    for p in _SMALL:
        if p * p > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out[p] = e
    if n == 1:
        return out
    if n < _SMALL[-1] ** 2:
        out[n] = out.get(n, 0) + 1
        return out
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if probable_prime(m):
            out[m] = out.get(m, 0) + 1
            continue
        d = pollard_rho(m, seed=len(stack) + m % 1000 + 1)
        stack.append(d)
        stack.append(m // d)
    return out


def pratt_certificate(n):
    """Recursive Lucas/Pratt certificate.  Leaves below TD_LIMIT are certified
    by trial division at verification time."""
    if n < TD_LIMIT:
        assert is_prime_td(n), n
        return {"n": n, "method": "trial-division"}
    fac = factorint(n - 1)
    for a in range(2, 10 ** 4):
        if pow(a, n - 1, n) != 1:
            raise AssertionError(("composite", n))
        if all(pow(a, (n - 1) // q, n) != 1 for q in fac):
            return {"n": n, "method": "pratt", "witness": a,
                    "factors": {str(q): [e, pratt_certificate(q)] for q, e in fac.items()}}
    raise AssertionError(("no witness", n))


def verify_pratt(cert):
    n = cert["n"]
    if cert["method"] == "trial-division":
        return is_prime_td(n)
    a = cert["witness"]
    prod = 1
    for qs, (e, sub) in cert["factors"].items():
        q = int(qs)
        if sub["n"] != q or not verify_pratt(sub):
            return False
        prod *= q ** e
        if pow(a, (n - 1) // q, n) == 1:
            return False
    return prod == n - 1 and pow(a, n - 1, n) == 1


def certify_prime(n):
    """Return a certificate object (and raise if n is composite)."""
    return pratt_certificate(n)


def mult_order(b, p, fac_pm1=None):
    """Exact multiplicative order of b modulo the prime p."""
    if fac_pm1 is None:
        fac_pm1 = factorint(p - 1)
    o = p - 1
    for q in fac_pm1:
        while o % q == 0 and pow(b, o // q, p) == 1:
            o //= q
    return o


def order_by_iteration(b, p):
    """Independent first-return order (used by verifiers for p of modest size)."""
    x, k = b % p, 1
    while x != 1:
        x = x * b % p
        k += 1
    return k


def odd_part(n):
    while n % 2 == 0:
        n //= 2
    return n


def prime_factors(n):
    return sorted(factorint(n))
