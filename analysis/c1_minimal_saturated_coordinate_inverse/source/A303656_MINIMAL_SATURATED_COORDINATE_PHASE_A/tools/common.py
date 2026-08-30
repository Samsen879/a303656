#!/usr/bin/env python3
"""Shared exact utilities for the minimal saturated coordinate audit.

Standard-library only.  No floating-point arithmetic is used in mathematical
claims or generated catalogs.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
from functools import lru_cache
import json
import math
from pathlib import Path
from typing import Iterable, Iterator, Sequence


class AuditError(ValueError):
    """Fail-closed error for malformed inputs or violated invariants."""


def canonical_json_bytes(obj: object) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(obj))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def factor(n: int) -> dict[int, int]:
    if n < 1:
        raise AuditError("factor requires a positive integer")
    out: dict[int, int] = {}
    while n % 2 == 0:
        out[2] = out.get(2, 0) + 1
        n //= 2
    p = 3
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for unsigned 64-bit integers."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
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
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primes_up_to(bound: int) -> Iterator[int]:
    if bound < 2:
        return
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(bound) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : bound + 1 : p] = b"\x00" * (((bound - start) // p) + 1)
    for p, flag in enumerate(sieve):
        if flag:
            yield p


def order_mod_prime(base: int, p: int) -> int:
    if not is_prime(p) or math.gcd(base, p) != 1:
        raise AuditError("multiplicative order requires a prime modulus and a unit")
    order = p - 1
    for q, multiplicity in factor(order).items():
        for _ in range(multiplicity):
            if pow(base, order // q, p) != 1:
                break
            order //= q
    return order


def exact_lifting_depth(base: int, p: int, order: int, cap: int = 8) -> int:
    """Return v_p(base**order-1), using only modular powers.

    The supplied cap is a fail-closed computational guard, not a theorem bound.
    """
    if pow(base, order, p) != 1:
        raise AuditError("order does not return to one modulo p")
    for s in range(1, cap):
        if pow(base, order, p ** (s + 1)) != 1:
            return s
    raise AuditError(f"lifting depth reached computational cap {cap}")


def vp_nonzero(n: int, p: int) -> int:
    if n == 0:
        raise AuditError("zero has no finite p-adic valuation")
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e


def clipped_valuation(value: int, p: int, precision: int) -> int | None:
    value %= p**precision
    if value == 0:
        return None
    return vp_nonzero(value, p)


def cylinder_cells(l: int, beta: int, depth: int, residue: int) -> frozenset[int]:
    if not (is_prime(l) and l % 2 == 1 and 1 <= depth <= beta):
        raise AuditError("invalid odd-prime cylinder")
    modulus = l**depth
    residue %= modulus
    return frozenset(range(residue, l**beta, modulus))


def shell_cells(l: int, beta: int, j: int, center: int = 0) -> frozenset[int]:
    if not (0 <= j < beta):
        raise AuditError("shell depth outside the fiber")
    center %= l**beta
    cells = []
    for x in range(l**beta):
        diff = (x - center) % (l**beta)
        if diff == 0:
            continue
        if vp_nonzero(diff, l) == j:
            cells.append(x)
    return frozenset(cells)


def dynamic_cells(l: int, beta: int, m: int, accepted_j: Iterable[int], center: int = 0) -> frozenset[int]:
    accepted = sorted(set(accepted_j))
    if not (0 <= m <= beta) or any(j < 0 or j >= m for j in accepted):
        raise AuditError("invalid dynamic shell set")
    out: set[int] = set()
    for j in accepted:
        out.update(shell_cells(l, beta, j, center))
    return frozenset(out)


def event_mass(cells: Iterable[int], l: int, beta: int) -> Fraction:
    return Fraction(len(set(cells)), l**beta)


def multiplicity_histogram(events: Sequence[frozenset[int]], universe_size: int) -> dict[str, int]:
    counts = [0] * universe_size
    for event in events:
        for x in event:
            counts[x] += 1
    hist: dict[str, int] = {}
    for value in counts:
        hist[str(value)] = hist.get(str(value), 0) + 1
    return dict(sorted(hist.items(), key=lambda item: int(item[0])))


def uncovered_cells(events: Sequence[frozenset[int]], universe_size: int) -> list[int]:
    covered: set[int] = set()
    for event in events:
        covered.update(event)
    return [x for x in range(universe_size) if x not in covered]


def row_minimal(events: Sequence[frozenset[int]], universe_size: int) -> bool:
    if uncovered_cells(events, universe_size):
        return False
    for i in range(len(events)):
        if not uncovered_cells(events[:i] + events[i + 1 :], universe_size):
            return False
    return True


@dataclass(frozen=True, order=True)
class Cylinder:
    depth: int
    residue: int

    def cells(self, l: int, beta: int) -> frozenset[int]:
        return cylinder_cells(l, beta, self.depth, self.residue)

    def as_record(self) -> dict[str, int]:
        return {"depth": self.depth, "residue": self.residue}


@lru_cache(maxsize=None)
def complete_frontiers(l: int, beta: int, root: Cylinder) -> tuple[tuple[Cylinder, ...], ...]:
    """All complete prefix-code frontiers inside one rooted cylinder.

    The root itself may be selected.  Otherwise every child subtree must be
    covered by an independently selected complete frontier.
    """
    if not (1 <= root.depth <= beta):
        raise AuditError("frontier root depth outside fiber")
    if root.depth == beta:
        return ((root,),)
    options: list[tuple[Cylinder, ...]] = [(root,)]
    modulus = l**root.depth
    children = [Cylinder(root.depth + 1, root.residue + digit * modulus) for digit in range(l)]
    child_frontiers = [complete_frontiers(l, beta, child) for child in children]
    for choice in itertools.product(*child_frontiers):
        merged = tuple(sorted(itertools.chain.from_iterable(choice)))
        options.append(merged)
    return tuple(options)


def frontier_count(l: int, height: int) -> int:
    if height < 0:
        raise AuditError("negative tree height")
    value = 1
    for _ in range(height):
        value = 1 + value**l
    return value


def template_hash(record: object) -> str:
    return sha256_bytes(canonical_json_bytes(record))
