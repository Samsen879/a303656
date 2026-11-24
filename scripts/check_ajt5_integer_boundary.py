#!/usr/bin/env python3
"""Rebuild integer D tables with exact exponent cutoffs, independently of the checker."""
import hashlib
import json
import sys
from array import array
from functools import lru_cache
from math import isqrt


def square_table(limit):
    table = bytearray(2 * (limit + 1))
    for a in range(isqrt(limit) + 1):
        aa = a*a
        for b in range(a, isqrt(limit-aa) + 1):
            table[2*(aa+b*b)] = 1
    return int.from_bytes(table, "little")


def mask_table(limit, squares, max_c):
    # Each 16-bit lane holds the mask for one integer. Byte order is explicit.
    ceiling = (1 << (16*(limit+1))) - 1
    triples = 0
    for c in range(max_c+1):
        if 3**c > limit:
            break
        triples |= (squares << (16*3**c)) & ceiling
    result = 0
    d = 0
    while 5**d < limit:
        if d >= 16:
            raise ValueError("mask width")
        result |= (triples << (16 * 5**d + d)) & ceiling
        d += 1
    return result.to_bytes(2*(limit+1), "little")


def native(raw):
    values = array("H")
    if values.itemsize != 2:
        raise RuntimeError("16-bit array storage required")
    values.frombytes(raw)
    if sys.byteorder != "little":
        values.byteswap()
    return values


def odd_inert_factors(n):
    if n <= 0:
        raise ValueError("only positive residuals can be blocked")
    factors = set()
    p = 2
    while p*p <= n:
        v = 0
        while n % p == 0:
            n //= p
            v += 1
        if p % 4 == 3 and v % 2:
            factors.add(p)
        p = 3 if p == 2 else p + 2
    if n % 4 == 3:
        factors.add(n)
    return frozenset(factors)


def cover_number(rows):
    # A covering set must choose at least one element of any uncovered row.
    if any(not row for row in rows):
        raise ValueError("unblockable residual")
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return 0
        row = min(remaining, key=lambda s: (len(s), sorted(s)))
        return 1 + min(solve(frozenset(r for r in remaining if p not in r)) for p in row)
    return solve(frozenset(rows))


def exception_budget(parent):
    m, r = 513014, 4
    edges = {e for d in range(7) if parent[m] >> d & 1 for e in (d, d+1)}
    rows = [odd_inert_factors(5*m+r-5**e-3**c) for e in sorted(edges)
            for c in range(15) if 5**e+3**c <= 5*m+r]
    return len(rows), cover_number(rows)


def require(value, expected):
    if value != expected:
        raise ValueError(f"endpoint discrepancy: {value!r} != {expected!r}")


def main():
    boundary = 547066
    extended = 956598
    limit = 5*extended+4
    squares = square_table(limit)
    full_raw = mask_table(limit, squares, 14)  # 3^15 exceeds the largest child.
    digest = hashlib.sha256(full_raw[:2*(5*boundary+5)]).hexdigest()
    require(digest, "4ddb8029360990b2bfb2fd551ca010d896c78f927e1b45786ef85333a445be24")
    full = native(full_raw)
    del full_raw
    c12 = native(mask_table(5*boundary+4, squares, 12))
    c13 = native(mask_table(5*boundary+4, squares, 13))
    counts = dict(pairs=0, empty_parent=0, no_bridge=0, d7_c13_misses=0)
    low_long_misses = []
    low_short_misses = []
    for m in range(2, extended+1):
        p = full[m]  # m < 3^13, hence parent c <= 12 automatically.
        for r in range(5):
            n = 5*m+r
            actual = p & (full[n] | (full[n] >> 1))
            if not actual & 127:
                low_long_misses.append((m, r))
            if m <= boundary:
                counts["pairs"] += 1
                counts["empty_parent"] += p == 0
                counts["no_bridge"] += actual == 0
                counts["d7_c13_misses"] += (p & 255 & (c13[n] | (c13[n] >> 1))) == 0
                if not p & 127 & (c12[n] | (c12[n] >> 1)):
                    low_short_misses.append((m, r))
    require(counts, dict(pairs=2735325, empty_parent=0, no_bridge=0, d7_c13_misses=0))
    require(low_long_misses, [(513014, 4)])
    require(low_short_misses, low_long_misses)
    rows, cost = exception_budget(full)
    require((rows, cost), (112, 44))
    # At the sole exception this child residual survives every palette omitting 3.
    require(513014, 147**2 + 701**2 + 3 + 1)
    require(5*513014+4-5-3**4, 3*(140**2+914**2))
    print(json.dumps(dict(boundary=boundary, D_sha256=digest, **counts,
                          extended=extended, extended_pairs=5*(extended-1),
                          low_parent_misses=low_long_misses, exception_rows=rows,
                          minimum_child_prime_cover=cost), sort_keys=True))


if __name__ == "__main__":
    main()
