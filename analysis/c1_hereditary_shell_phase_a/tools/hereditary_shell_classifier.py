#!/usr/bin/env python3
"""Independent exact reference classifier for A303656 hereditary shell contraction.

Standard-library only.  It does not import code from the A303656 repository.
All coverage tests are finite set/bitset identities; all mass calculations use
integers or Fraction.  No floating-point decision is used.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import gcd, isqrt, lcm
from pathlib import Path
import argparse
import json
import random
import sys
from typing import Iterable, Sequence

sys.set_int_max_str_digits(1_000_000)

AUTHORITY = {
    "repository": "Samsen879/a303656",
    "repository_id": 1333945235,
    "main_sha": "1100eb5ba01d90e5b1001be0bdfa464860fdbb92",
    "main_tree": "ad1269916bf420c564e34887a96c808033fe538b",
    "project": "PAUSED",
    "active_promoted_route": "NONE",
    "a303656": "UNRESOLVED",
}


def factorint(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorint requires n>=1")
    out: dict[int, int] = {}
    while n % 2 == 0:
        out[2] = out.get(2, 0) + 1
        n //= 2
    d = 3
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def sieve(n: int) -> list[int]:
    flags = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        flags[0] = 0
    if n >= 1:
        flags[1] = 0
    for p in range(2, isqrt(n) + 1):
        if flags[p]:
            start = p * p
            flags[start : n + 1 : p] = b"\x00" * (((n - start) // p) + 1)
    return [i for i, b in enumerate(flags) if b]


def order_mod_prime(a: int, p: int) -> int:
    if gcd(a, p) != 1:
        raise ValueError("a and p must be coprime")
    order = p - 1
    for q in factorint(order):
        while order % q == 0 and pow(a, order // q, p) == 1:
            order //= q
    return order


def lifting_depth(a: int, order: int, p: int, cap: int = 12) -> int:
    if pow(a, order, p) != 1:
        raise ValueError("order is invalid")
    s = 1
    while s < cap and pow(a, order, p ** (s + 1)) == 1:
        s += 1
    if s == cap and pow(a, order, p ** (cap + 1)) == 1:
        raise RuntimeError("lifting depth exceeded cap")
    return s


def valuation_nonzero(n: int, p: int) -> int:
    if n == 0:
        raise ValueError("v_p(0) is intentionally undefined")
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def fatal(p: int, K: int, r: int, E: set[int], c: int, d: int) -> bool:
    mod = p**K
    value = (r - pow(3, c, mod) - pow(5, d, mod)) % mod
    if value == 0:
        return False  # fail closed: local zero is unresolved
    return valuation_nonzero(value, p) in E


def vp_residue(x: int, ell: int, beta: int) -> int | None:
    modulus = ell**beta
    x %= modulus
    if x == 0:
        return None
    v = 0
    while x % ell == 0:
        x //= ell
        v += 1
    return v


def shell_set(ell: int, beta: int, j: int, center: int = 0) -> frozenset[int]:
    modulus = ell**beta
    return frozenset(
        x for x in range(modulus) if vp_residue(x - center, ell, beta) == j
    )


def cylinder_set(ell: int, beta: int, depth: int, residue: int) -> frozenset[int]:
    modulus = ell**beta
    submodulus = ell**depth
    residue %= submodulus
    return frozenset(x for x in range(modulus) if x % submodulus == residue)


def dynamic_set(ell: int, beta: int, J: Iterable[int], center: int = 0) -> frozenset[int]:
    out: set[int] = set()
    for j in J:
        out.update(shell_set(ell, beta, j, center))
    return frozenset(out)


def all_rigid_cylinders(ell: int, beta: int) -> list[tuple[int, int, frozenset[int]]]:
    return [
        (depth, residue, cylinder_set(ell, beta, depth, residue))
        for depth in range(1, beta + 1)
        for residue in range(ell**depth)
    ]


def bitmask(points: Iterable[int]) -> int:
    out = 0
    for x in points:
        out |= 1 << x
    return out


def is_row_minimal_cover(
    size: int,
    dynamic: frozenset[int],
    rigid: Sequence[tuple[int, int, frozenset[int]]],
) -> bool:
    sets: list[frozenset[int]] = []
    if dynamic:
        sets.append(dynamic)
    sets.extend(item[2] for item in rigid)
    if not sets or len(set().union(*sets)) != size:
        return False
    for i in range(len(sets)):
        union: set[int] = set()
        for j, event in enumerate(sets):
            if i != j:
                union.update(event)
        if len(union) == size:
            return False
    return True


def check_prefix_frontier(
    ell: int,
    beta: int,
    J: set[int],
    rigid: Sequence[tuple[int, int, frozenset[int]]],
) -> bool:
    size = ell**beta
    dynamic = dynamic_set(ell, beta, J)
    if not is_row_minimal_cover(size, dynamic, rigid):
        return False
    centered = [row for row in rigid if 0 in row[2]]
    if len(centered) != 1:
        return False
    centered_row = centered[0]
    e = centered_row[0]
    centered_set = centered_row[2]
    for row in rigid:
        if row == centered_row:
            continue
        if row[2] & centered_set:
            return False
        shell_indices = {vp_residue(x, ell, beta) for x in row[2]}
        if len(shell_indices) != 1:
            return False
        j = next(iter(shell_indices))
        if j is None or j >= e or j in J:
            return False
    if dynamic and not any(j < e for j in J):
        return False
    return True


def brute_row_minimal_counts(
    ell: int, beta: int, J: set[int], max_rigid: int
) -> dict[int, int]:
    size = ell**beta
    full = (1 << size) - 1
    cylinders = all_rigid_cylinders(ell, beta)
    masks = [bitmask(row[2]) for row in cylinders]
    dynamic_mask = bitmask(dynamic_set(ell, beta, J))
    result: Counter[int] = Counter()
    for r in range(1, min(max_rigid, len(cylinders)) + 1):
        for indices in combinations(range(len(cylinders)), r):
            union = dynamic_mask
            for i in indices:
                union |= masks[i]
            if union != full:
                continue
            if dynamic_mask:
                rigid_union = 0
                for i in indices:
                    rigid_union |= masks[i]
                if rigid_union == full:
                    continue
            minimal = True
            for i in indices:
                test = dynamic_mask
                for j in indices:
                    if j != i:
                        test |= masks[j]
                if test == full:
                    minimal = False
                    break
            if not minimal:
                continue
            rows = [cylinders[i] for i in indices]
            if not check_prefix_frontier(ell, beta, J, rows):
                raise AssertionError("prefix-frontier classifier mismatch")
            result[r + bool(dynamic_mask)] += 1
    return dict(sorted(result.items()))


def brute_all_cover_statistics(ell: int, beta: int, J: set[int]) -> dict[str, object]:
    """Enumerate every rigid-cylinder subset for a genuinely small fiber."""
    size = ell**beta
    cylinders = all_rigid_cylinders(ell, beta)
    if len(cylinders) > 20:
        raise ValueError("full subset enumeration is restricted to at most 20 cylinders")
    dynamic = dynamic_set(ell, beta, J)
    full = set(range(size))
    cover_count = 0
    partition_count = 0
    overlap_count = 0
    row_minimal_count = 0
    minimum_rows: int | None = None
    by_rows: Counter[int] = Counter()
    for mask in range(1 << len(cylinders)):
        selected = [cylinders[i] for i in range(len(cylinders)) if (mask >> i) & 1]
        event_sets: list[frozenset[int]] = ([dynamic] if dynamic else []) + [
            row[2] for row in selected
        ]
        if not event_sets:
            continue
        union: set[int] = set()
        for event in event_sets:
            union.update(event)
        if union != full:
            continue
        cover_count += 1
        rows = len(event_sets)
        by_rows[rows] += 1
        minimum_rows = rows if minimum_rows is None else min(minimum_rows, rows)
        multiplicities = [sum(x in event for event in event_sets) for x in range(size)]
        if all(m == 1 for m in multiplicities):
            partition_count += 1
        else:
            overlap_count += 1
        if is_row_minimal_cover(size, dynamic, selected):
            if not check_prefix_frontier(ell, beta, J, selected):
                raise AssertionError("full enumeration found a non-frontier minimal cover")
            row_minimal_count += 1
    return {
        "rigid_cylinders": len(cylinders),
        "subsets_checked": 1 << len(cylinders),
        "exact_covers": cover_count,
        "exact_partitions": partition_count,
        "covers_with_overlap": overlap_count,
        "row_minimal_covers": row_minimal_count,
        "minimum_total_rows": minimum_rows,
        "exact_covers_by_total_rows": {str(k): v for k, v in sorted(by_rows.items())},
    }


# Polynomial counts by number of rigid rows in a complete prefix frontier.
def poly_add(a: dict[int, int], b: dict[int, int], cap: int) -> dict[int, int]:
    out: defaultdict[int, int] = defaultdict(int)
    for source in (a, b):
        for degree, coefficient in source.items():
            if degree <= cap:
                out[degree] += coefficient
    return dict(out)


def poly_mul(a: dict[int, int], b: dict[int, int], cap: int) -> dict[int, int]:
    out: defaultdict[int, int] = defaultdict(int)
    for i, ai in a.items():
        for j, bj in b.items():
            if i + j <= cap:
                out[i + j] += ai * bj
    return dict(out)


def poly_pow(a: dict[int, int], exponent: int, cap: int) -> dict[int, int]:
    out = {0: 1}
    base = a
    e = exponent
    while e:
        if e & 1:
            out = poly_mul(out, base, cap)
        e //= 2
        if e:
            base = poly_mul(base, base, cap)
    return out


@lru_cache(maxsize=None)
def frontier_count(ell: int, height: int) -> int:
    return 1 if height == 0 else 1 + frontier_count(ell, height - 1) ** ell


@lru_cache(maxsize=None)
def frontier_poly_cached(ell: int, height: int, cap: int) -> tuple[tuple[int, int], ...]:
    if height == 0:
        return ((1, 1),)
    previous = dict(frontier_poly_cached(ell, height - 1, cap))
    refined = poly_pow(previous, ell, cap)
    return tuple(sorted(poly_add({1: 1}, refined, cap).items()))


def frontier_poly(ell: int, height: int, cap: int) -> dict[int, int]:
    return dict(frontier_poly_cached(ell, height, cap))


def total_parameter_labelled_templates(ell: int, beta: int) -> int:
    total = frontier_count(ell, beta - 1) ** ell  # rigid-only
    for m in range(1, beta + 1):
        for parity in (0, 1):
            allowed = [j for j in range(m) if j % 2 == parity]
            for mask in range(1, 1 << len(allowed)):
                J = {allowed[k] for k in range(len(allowed)) if (mask >> k) & 1}
                for centered_depth in range(1, beta + 1):
                    if not any(j < centered_depth for j in J):
                        continue
                    count = 1
                    for j in range(centered_depth):
                        if j not in J:
                            count *= frontier_count(ell, beta - j - 1) ** (ell - 1)
                    total += count
    return total


def template_row_distribution(ell: int, beta: int, cap: int) -> dict[int, int]:
    total: defaultdict[int, int] = defaultdict(int)
    rigid_only = poly_pow(frontier_poly(ell, beta - 1, cap), ell, cap)
    for degree, coefficient in rigid_only.items():
        total[degree] += coefficient
    for m in range(1, beta + 1):
        for parity in (0, 1):
            allowed = [j for j in range(m) if j % 2 == parity]
            for mask in range(1, 1 << len(allowed)):
                J = {allowed[k] for k in range(len(allowed)) if (mask >> k) & 1}
                for centered_depth in range(1, beta + 1):
                    if not any(j < centered_depth for j in J):
                        continue
                    polynomial = {2: 1}  # one dynamic row plus one centered rigid row
                    for j in range(centered_depth):
                        if j not in J:
                            branches = poly_pow(
                                frontier_poly(ell, beta - j - 1, cap), ell - 1, cap
                            )
                            polynomial = poly_mul(polynomial, branches, cap)
                    for degree, coefficient in polynomial.items():
                        total[degree] += coefficient
    return dict(sorted(total.items()))


@dataclass(frozen=True, order=True)
class Guard:
    modulus: int
    residue: int

    def normalized(self) -> "Guard":
        return Guard(self.modulus, self.residue % self.modulus)

    def points(self, ambient: int) -> frozenset[int]:
        if ambient % self.modulus:
            raise ValueError("guard modulus must divide ambient modulus")
        r = self.residue % self.modulus
        return frozenset(x for x in range(ambient) if x % self.modulus == r)


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def intersect_two_guards(a: Guard, b: Guard) -> Guard | None:
    a = a.normalized()
    b = b.normalized()
    g = gcd(a.modulus, b.modulus)
    if (b.residue - a.residue) % g:
        return None
    m1 = a.modulus // g
    m2 = b.modulus // g
    _, inv, _ = egcd(m1, m2)
    k = ((b.residue - a.residue) // g * inv) % m2
    modulus = lcm(a.modulus, b.modulus)
    residue = (a.residue + a.modulus * k) % modulus
    return Guard(modulus, residue)


def intersect_guards(guards: Sequence[Guard]) -> Guard | None:
    current = Guard(1, 0)
    for guard in guards:
        current = intersect_two_guards(current, guard)
        if current is None:
            return None
    return current


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def all_guards(ambient: int) -> list[Guard]:
    return [Guard(m, r) for m in divisors(ambient) for r in range(m)]


def minimal_cover_subsets(slices: Sequence[frozenset[int]], fiber_size: int) -> list[tuple[int, ...]]:
    full = set(range(fiber_size))
    covers: list[tuple[int, ...]] = []
    for size in range(1, len(slices) + 1):
        for indices in combinations(range(len(slices)), size):
            union: set[int] = set()
            for i in indices:
                union.update(slices[i])
            if union != full:
                continue
            if any(set(previous).issubset(indices) for previous in covers):
                continue
            covers.append(indices)
    return covers


def canonical_residual_guards(
    slices: Sequence[frozenset[int]], guards: Sequence[Guard], fiber_size: int
) -> tuple[list[tuple[int, ...]], list[Guard]]:
    covers = minimal_cover_subsets(slices, fiber_size)
    clauses: set[Guard] = set()
    for cover in covers:
        clause = intersect_guards([guards[i] for i in cover])
        if clause is not None:
            clauses.add(clause.normalized())
    # Delete clauses contained in another clause: C(M,a) subset C(m,b) iff m|M and a=b mod m.
    kept: list[Guard] = []
    for clause in sorted(clauses):
        absorbed = False
        for other in clauses:
            if other == clause:
                continue
            if clause.modulus % other.modulus == 0 and clause.residue % other.modulus == other.residue:
                absorbed = True
                break
        if not absorbed:
            kept.append(clause)
    return covers, kept


def direct_saturation_points(
    slices: Sequence[frozenset[int]], guards: Sequence[Guard], fiber_size: int, ambient: int
) -> frozenset[int]:
    out: set[int] = set()
    full = set(range(fiber_size))
    guard_points = [guard.points(ambient) for guard in guards]
    for y in range(ambient):
        union: set[int] = set()
        for event_slice, active_points in zip(slices, guard_points):
            if y in active_points:
                union.update(event_slice)
        if union == full:
            out.add(y)
    return frozenset(out)


def residual_points(clauses: Sequence[Guard], ambient: int) -> frozenset[int]:
    out: set[int] = set()
    for clause in clauses:
        out.update(clause.points(ambient))
    return frozenset(out)


def row_union_representable(target: frozenset[int], guards: Sequence[Guard], ambient: int) -> bool:
    guard_points = [guard.points(ambient) for guard in guards]
    for mask in range(1 << len(guards)):
        union: set[int] = set()
        for i, points in enumerate(guard_points):
            if (mask >> i) & 1:
                union.update(points)
        if frozenset(union) == target:
            return True
    return False


def exact_guarded_slice_audit() -> dict[str, object]:
    # Complete pair on a 3-cell fiber: dynamic shell {1,2}, centered rigid {0}.
    slices_pair = [frozenset({1, 2}), frozenset({0})]
    ambient = 30
    guards = all_guards(ambient)
    pair_cases = 0
    pair_nonempty = 0
    pair_row_only_failures = 0
    for g0 in guards:
        for g1 in guards:
            pair_cases += 1
            direct = direct_saturation_points(slices_pair, [g0, g1], 3, ambient)
            covers, clauses = canonical_residual_guards(slices_pair, [g0, g1], 3)
            if covers != [(0, 1)]:
                raise AssertionError("unexpected pair cover hypergraph")
            reconstructed = residual_points(clauses, ambient)
            if reconstructed != direct:
                raise AssertionError("canonical cover-clause identity failed")
            if direct:
                pair_nonempty += 1
                if not row_union_representable(direct, [g0, g1], ambient):
                    pair_row_only_failures += 1

    # Rigid-only 3-digit partition; all guard assignments on Z/6Z.
    slices_triple = [frozenset({0}), frozenset({1}), frozenset({2})]
    ambient3 = 6
    guards3 = all_guards(ambient3)
    triple_cases = 0
    for assignment in product(guards3, repeat=3):
        triple_cases += 1
        direct = direct_saturation_points(slices_triple, assignment, 3, ambient3)
        _, clauses = canonical_residual_guards(slices_triple, assignment, 3)
        if residual_points(clauses, ambient3) != direct:
            raise AssertionError("triple cover-clause identity failed")

    # Branch-local reuse: D pairs with either R0 or R1.
    slices_reuse = [frozenset({1, 2}), frozenset({0}), frozenset({0})]
    reuse_cover_hypergraph = minimal_cover_subsets(slices_reuse, 3)
    if reuse_cover_hypergraph != [(0, 1), (0, 2)]:
        raise AssertionError("branch-reuse cover hypergraph mismatch")
    reuse_cases = 0
    for assignment in product(guards3, repeat=3):
        reuse_cases += 1
        direct = direct_saturation_points(slices_reuse, assignment, 3, ambient3)
        _, clauses = canonical_residual_guards(slices_reuse, assignment, 3)
        if residual_points(clauses, ambient3) != direct:
            raise AssertionError("branch-reuse identity failed")

    # Deterministic randomized prefix-frontier systems, all checked exactly.
    rng = random.Random(303656)
    random_cases = 0
    for _ in range(10_000):
        ell = rng.choice([3, 5, 7])
        beta = rng.choice([1, 2, 3])
        fiber_size = ell**beta
        center = 0
        # Use a guaranteed exact dynamic+centered cover; optional same-parity tail.
        J = {0}
        if beta >= 3 and rng.randrange(2):
            J.add(2)
        event_slices = [dynamic_set(ell, beta, J, center), cylinder_set(ell, beta, 1, 0)]
        # Sometimes duplicate the center slice to force branch-local alternatives.
        if rng.randrange(3) == 0:
            event_slices.append(cylinder_set(ell, beta, 1, 0))
        assignment = [rng.choice(guards) for _ in event_slices]
        direct = direct_saturation_points(event_slices, assignment, fiber_size, ambient)
        _, clauses = canonical_residual_guards(event_slices, assignment, fiber_size)
        if residual_points(clauses, ambient) != direct:
            raise AssertionError("random exact cover-clause identity failed")
        random_cases += 1

    return {
        "pair_guard_cases": pair_cases,
        "pair_nonempty_residual_cases": pair_nonempty,
        "pair_row_only_grammar_failures": pair_row_only_failures,
        "triple_guard_cases": triple_cases,
        "branch_reuse_guard_cases": reuse_cases,
        "branch_reuse_minimal_covers": [list(x) for x in reuse_cover_hypergraph],
        "deterministic_random_cases": random_cases,
        "provenance_dnf_failures": 0,
    }


@dataclass(frozen=True)
class RectEvent:
    """Triangular product event on a small CRT-coordinate product."""

    factors: tuple[frozenset[int], ...]
    provenance: tuple[str, ...]


def direct_rect_cover(sizes: Sequence[int], events: Sequence[RectEvent]) -> bool:
    for point in product(*(range(size) for size in sizes)):
        if not any(
            all(point[i] in event.factors[i] for i in range(len(sizes)))
            for event in events
        ):
            return False
    return True


def eliminate_rect_max(
    sizes: Sequence[int], events: Sequence[RectEvent]
) -> tuple[tuple[int, ...], list[RectEvent], int]:
    if not sizes:
        return tuple(), list(events), 0
    n = len(sizes)
    top_full = frozenset(range(sizes[-1]))
    lower: list[RectEvent] = []
    top: list[RectEvent] = []
    for event in events:
        if len(event.factors) != n:
            raise ValueError("rectangular event dimension mismatch")
        if event.factors[-1] == top_full:
            lower.append(RectEvent(event.factors[:-1], event.provenance))
        else:
            top.append(event)
    slices = [event.factors[-1] for event in top]
    covers = minimal_cover_subsets(slices, sizes[-1]) if top else []
    derived: list[RectEvent] = []
    for cover in covers:
        factors: list[frozenset[int]] = []
        valid = True
        for coordinate in range(n - 1):
            intersection = frozenset.intersection(
                *(top[i].factors[coordinate] for i in cover)
            )
            if not intersection:
                valid = False
                break
            factors.append(intersection)
        if valid:
            provenance = ("cover",) + tuple(
                token for i in cover for token in top[i].provenance
            )
            derived.append(RectEvent(tuple(factors), provenance))
    # Set/provenance equality is enough for this audit; retain one witness per
    # identical cylinder because multiplicity has no semantic effect.
    unique: dict[tuple[frozenset[int], ...], RectEvent] = {}
    for event in lower + derived:
        unique.setdefault(event.factors, event)
    return tuple(sizes[:-1]), list(unique.values()), len(derived)


def recursive_rect_root_cover(
    sizes: Sequence[int], events: Sequence[RectEvent]
) -> tuple[bool, list[int]]:
    current_sizes = tuple(sizes)
    current_events = list(events)
    derived_counts: list[int] = []
    while current_sizes:
        current_sizes, current_events, count = eliminate_rect_max(
            current_sizes, current_events
        )
        derived_counts.append(count)
    return bool(current_events), derived_counts


def recursive_provenance_audit(cases: int = 5000) -> dict[str, object]:
    rng = random.Random(30365667)
    sizes = (3, 5, 7)
    full_factors = tuple(frozenset(range(size)) for size in sizes)
    direct_complete_count = 0
    maximum_derived_in_one_level = 0
    total_derived_clauses = 0
    for case in range(cases):
        events: list[RectEvent] = []
        for rank, size in enumerate(sizes):
            lower_factors: list[frozenset[int]] = []
            for lower_size in sizes[:rank]:
                if rng.randrange(2):
                    lower_factors.append(frozenset(range(lower_size)))
                else:
                    lower_factors.append(frozenset({rng.randrange(lower_size)}))
            # At most one dynamic beta-one shell at this coordinate.
            if rng.randrange(4) != 0:
                center = rng.randrange(size)
                factors = list(lower_factors)
                factors.append(frozenset(x for x in range(size) if x != center))
                factors.extend(full_factors[rank + 1 :])
                events.append(RectEvent(tuple(factors), (f"D{case}:{rank}",)))
            # Zero to three rigid singleton slices, independently guarded.
            for rigid_index in range(rng.randrange(4)):
                rigid_lower: list[frozenset[int]] = []
                for lower_size in sizes[:rank]:
                    if rng.randrange(2):
                        rigid_lower.append(frozenset(range(lower_size)))
                    else:
                        rigid_lower.append(frozenset({rng.randrange(lower_size)}))
                factors = rigid_lower + [frozenset({rng.randrange(size)})]
                factors.extend(full_factors[rank + 1 :])
                events.append(
                    RectEvent(tuple(factors), (f"R{case}:{rank}:{rigid_index}",))
                )
        direct = direct_rect_cover(sizes, events)
        recursive, derived_counts = recursive_rect_root_cover(sizes, events)
        if direct != recursive:
            raise AssertionError("multi-level provenance contraction mismatch")
        direct_complete_count += int(direct)
        if derived_counts:
            maximum_derived_in_one_level = max(
                maximum_derived_in_one_level, max(derived_counts)
            )
        total_derived_clauses += sum(derived_counts)
    return {
        "coordinate_sizes": list(sizes),
        "cases": cases,
        "direct_complete_cases": direct_complete_count,
        "recursive_mismatches": 0,
        "total_derived_clauses": total_derived_clauses,
        "maximum_derived_clauses_in_one_level": maximum_derived_in_one_level,
    }


def arithmetic_prime_search(limit: int = 500_000) -> dict[str, object]:
    candidates = []
    searched_primes: list[int] = []
    for q in sieve(limit):
        if q < 3 or q == 5 or q % 4 != 3:
            continue
        searched_primes.append(q)
        w = order_mod_prime(5, q)
        if pow(5, w, q * q) == 1:
            s = lifting_depth(5, w, q)
            factors = factorint(w)
            largest = max(factors) if factors else 1
            candidates.append(
                {
                    "q": q,
                    "w": w,
                    "s": s,
                    "largest_order_prime": largest,
                    "largest_order_depth": factors.get(largest, 0),
                }
            )
    resources = {
        str(ell): [item for item in candidates if item["largest_order_prime"] == ell]
        for ell in (3, 5, 7)
    }
    searched_payload = "".join(f"{q}\n" for q in searched_primes).encode()
    return {
        "limit": limit,
        "searched_primes_q_eq_3_mod_4_q_ne_5": len(searched_primes),
        "searched_primes_sha256": sha256(searched_payload).hexdigest(),
        "first_searched_prime": searched_primes[0],
        "last_searched_prime": searched_primes[-1],
        "nonregular_hits": candidates,
        "small_coordinate_resources": resources,
    }


def square_sum_residues_power_two(K: int) -> frozenset[int]:
    mod = 2**K
    squares = {x * x % mod for x in range(mod)}
    return frozenset((a + b) % mod for a in squares for b in squares)


def two_adic_unsafe(K: int, r: int, c: int, d: int) -> bool:
    mod = 2**K
    remainder = (r - pow(3, c, mod) - pow(5, d, mod)) % mod
    return remainder not in square_sum_residues_power_two(K)


def actual_67_20771_audit() -> dict[str, object]:
    p = 67
    q = 20771
    wp = order_mod_prime(5, p)
    wq = order_mod_prime(5, q)
    sp = lifting_depth(5, wp, p)
    sq = lifting_depth(5, wq, q)
    U = lcm(wp * p, wq)
    lower_modulus = U // p
    if (wp, sp, wq, sq, U, lower_modulus) != (22, 1, 10385, 2, 228470, 3410):
        raise AssertionError("unexpected arithmetic data")

    def saturated_lower(rp: int, rq: int, c: int) -> tuple[list[int], dict[int, dict[str, object]]]:
        saturated: list[int] = []
        detail: dict[int, dict[str, object]] = {}
        sat_bits = bytearray(lower_modulus)
        for y in range(lower_modulus):
            dyn: list[int] = []
            rig: list[int] = []
            covered: list[int] = []
            for t in range(p):
                d = y + lower_modulus * t
                fd = fatal(p, 2, rp, {1}, c, d)
                fr = fatal(q, 2, rq, {1}, c, d)
                if fd:
                    dyn.append(t)
                if fr:
                    rig.append(t)
                if fd or fr:
                    covered.append(t)
            if len(covered) == p:
                saturated.append(y)
                sat_bits[y] = 1
                detail[y] = {
                    "dynamic_count": len(dyn),
                    "rigid_count": len(rig),
                    "dynamic_hole": next(t for t in range(p) if t not in dyn),
                    "rigid_digits": rig,
                    "overlap": len(set(dyn) & set(rig)),
                }
        return saturated, {
            "fibers": detail,
            "saturation_indicator_sha256": sha256(bytes(sat_bits)).hexdigest(),
        }

    aligned, aligned_detail = saturated_lower(4, q + 4, 1)
    if aligned != [0]:
        raise AssertionError("aligned pair residual mismatch")

    # Verify the guarded-slice product normal form on every coarse exponent.
    # In the global CRT coordinate x_p=d mod p, the dynamic shell is all
    # nonzero digits over guard d=0 mod w_p; the rigid slice is digit zero
    # over guard d=0 mod (w_q/p).
    dynamic_factorization_checks = 0
    rigid_factorization_checks = 0
    factorization_codes = bytearray(U)
    for d in range(U):
        fd = fatal(p, 2, 4, {1}, 1, d)
        expected_fd = (d % wp == 0 and d % p != 0)
        if fd != expected_fd:
            raise AssertionError("67-row guarded-slice factorization mismatch")
        fr = fatal(q, 2, q + 4, {1}, 1, d)
        expected_fr = (d % wq == 0)
        if fr != expected_fr:
            raise AssertionError("20771-row guarded-slice factorization mismatch")
        dynamic_factorization_checks += 1
        rigid_factorization_checks += 1
        factorization_codes[d] = int(fd) | (int(fr) << 1)

    # Exact stripped guards.
    dynamic_guard = Guard(wp, 0)
    rigid_guard = Guard(wq // p, 0)
    residual = intersect_guards([dynamic_guard, rigid_guard])
    if residual != Guard(3410, 0):
        raise AssertionError("stripped residual mismatch")
    direct_sat = frozenset(aligned)
    if residual.points(lower_modulus) != direct_sat:
        raise AssertionError("actual pair canonical residual mismatch")
    row_only = row_union_representable(direct_sat, [dynamic_guard, rigid_guard], lower_modulus)

    common: dict[str, object] = {}
    for c in (0, 1):
        sat, detail = saturated_lower(2, 13471, c)
        expected = [2728] if c == 0 else [1639]
        if sat != expected:
            raise AssertionError("common-residue anchor replay mismatch")
        common[str(c)] = {"saturated_lower_residues": sat, **detail}

    # Universal finite truth-table check for commuting a lower two-adic event
    # with projection over an odd coordinate.  B is independent of the odd
    # coordinate, so all(B or T_z) == B or all(T_z).
    commute_cases = 0
    universal_top_size = 7
    for B in (False, True):
        for mask in range(1 << universal_top_size):
            top = [bool((mask >> z) & 1) for z in range(universal_top_size)]
            if all(B or value for value in top) != (B or all(top)):
                raise AssertionError("two-adic commutation truth-table failure")
            commute_cases += 1

    # Verify from actual periods that a two-adic event is independent of the
    # 67-coordinate once the lower modulus retains the full two-adic period.
    period_independence_cases = 0
    for K2 in (2, 3, 4, 5):
        period = 1 if K2 == 2 else 2 ** (K2 - 2)
        refined = lcm(lower_modulus, period)
        for r2 in range(2**K2):
            for c2 in (0, 1):
                for y2 in range(refined):
                    base = two_adic_unsafe(K2, r2, c2, y2)
                    # One step by refined is enough because refined is a
                    # multiple of the exact two-adic exponent period.
                    if two_adic_unsafe(K2, r2, c2, y2 + refined) != base:
                        raise AssertionError("two-adic period independence failure")
                    period_independence_cases += 1

    return {
        "p": p,
        "q": q,
        "w_p": wp,
        "s_p": sp,
        "w_q": wq,
        "s_q": sq,
        "U": U,
        "lower_modulus_after_67": lower_modulus,
        "aligned_anchor_1": {
            "row_residues": {"r_67": 4, "r_20771": q + 4},
            "saturated_lower_residues": aligned,
            "canonical_cover_clause": ["G_67", "G_20771"],
            "stripped_guards": [
                {"modulus": dynamic_guard.modulus, "residue": dynamic_guard.residue},
                {"modulus": rigid_guard.modulus, "residue": rigid_guard.residue},
            ],
            "residual": {"modulus": residual.modulus, "residue": residual.residue},
            "row_only_union_representable": row_only,
            "guarded_slice_factorization": {
                "dynamic_checks": dynamic_factorization_checks,
                "rigid_checks": rigid_factorization_checks,
                "status_sha256": sha256(bytes(factorization_codes)).hexdigest(),
                "dynamic_formula": "d mod 22 = 0 and d mod 67 != 0",
                "rigid_formula": "d mod 10385 = 0",
            },
            **aligned_detail,
        },
        "common_residue_system": {
            "r_67": 2,
            "r_20771": 13471,
            "anchors": common,
            "same_untagged_residual": common["0"]["saturated_lower_residues"]
            == common["1"]["saturated_lower_residues"],
        },
        "two_adic_commutation_cases": commute_cases,
        "two_adic_period_independence_cases": period_independence_cases,
        "two_adic_commutation_failures": 0,
    }


def build_catalog() -> dict[str, object]:
    catalog: dict[str, object] = {}
    for ell in (3, 5, 7):
        for beta in range(1, 6):
            key = f"l={ell},beta={beta}"
            distribution = template_row_distribution(ell, beta, 12)
            catalog[key] = {
                "parameter_labelled_template_count": str(
                    total_parameter_labelled_templates(ell, beta)
                ),
                "row_count_distribution_through_12": {
                    str(k): str(v) for k, v in distribution.items()
                },
                "templates_with_at_most_12_rows": str(sum(distribution.values())),
                "rigid_only_template_count": str(frontier_count(ell, beta - 1) ** ell),
            }
    return catalog


def run() -> dict[str, object]:
    brute = {
        "l=3,beta=2": {
            "J=[]": brute_row_minimal_counts(3, 2, set(), 12),
            "J=[0]": brute_row_minimal_counts(3, 2, {0}, 12),
            "J=[1]": brute_row_minimal_counts(3, 2, {1}, 12),
            "complete_subsets_checked": str(2 ** len(all_rigid_cylinders(3, 2))),
        },
        "l=3,beta=3,rigid_rows<=6": {
            "J=[]": brute_row_minimal_counts(3, 3, set(), 6),
            "J=[0]": brute_row_minimal_counts(3, 3, {0}, 6),
            "J=[1]": brute_row_minimal_counts(3, 3, {1}, 6),
            "J=[2]": brute_row_minimal_counts(3, 3, {2}, 6),
            "J=[0,2]": brute_row_minimal_counts(3, 3, {0, 2}, 6),
        },
        "l=5,beta=2,rigid_rows<=6": {
            "J=[]": brute_row_minimal_counts(5, 2, set(), 6),
            "J=[0]": brute_row_minimal_counts(5, 2, {0}, 6),
            "J=[1]": brute_row_minimal_counts(5, 2, {1}, 6),
        },
    }
    abstract_exact = {
        "l=3,beta=1,J=[]": brute_all_cover_statistics(3, 1, set()),
        "l=3,beta=1,J=[0]": brute_all_cover_statistics(3, 1, {0}),
        "l=3,beta=2,J=[]": brute_all_cover_statistics(3, 2, set()),
        "l=3,beta=2,J=[0]": brute_all_cover_statistics(3, 2, {0}),
        "l=3,beta=2,J=[1]": brute_all_cover_statistics(3, 2, {1}),
        "l=5,beta=1,J=[]": brute_all_cover_statistics(5, 1, set()),
        "l=5,beta=1,J=[0]": brute_all_cover_statistics(5, 1, {0}),
        "l=7,beta=1,J=[]": brute_all_cover_statistics(7, 1, set()),
        "l=7,beta=1,J=[0]": brute_all_cover_statistics(7, 1, {0}),
    }
    prime_search = arithmetic_prime_search()
    hits_by_top: defaultdict[int, list[dict[str, int]]] = defaultdict(list)
    for hit in prime_search["nonregular_hits"]:
        hits_by_top[int(hit["largest_order_prime"])].append(hit)
    admitted_label_audit = {
        str(ell): {
            "dynamic_row_allowed": ell % 4 == 3 and ell != 5,
            "bounded_rigid_resources": hits_by_top.get(ell, []),
            "bounded_resource_count": len(hits_by_top.get(ell, [])),
            "bounded_beta_one_dynamic_pair_available": (
                ell % 4 == 3 and ell != 5 and any(
                    int(hit["largest_order_depth"]) == 1
                    for hit in hits_by_top.get(ell, [])
                )
            ),
        }
        for ell in (3, 5, 7, 67, 653)
    }
    result = {
        "authority": AUTHORITY,
        "formal_outcome": {
            "canonical_residual_formula": "Sat_p = OR_{I minimal exact slice cover} AND_{i in I} G_i",
            "provenance_cylinder_grammar": "PASS: closed under exact maximal-coordinate contraction",
            "row_only_grammar": "FAIL in general: conjunction of stripped guards is required",
            "hereditary_counterexamples_in_provenance_grammar": 0,
        },
        "abstract_exact_cover_enumeration": abstract_exact,
        "prefix_frontier_catalog": build_catalog(),
        "independent_bruteforce": brute,
        "guarded_slice_audit": exact_guarded_slice_audit(),
        "recursive_provenance_audit": recursive_provenance_audit(),
        "arithmetic_prime_search": prime_search,
        "admitted_row_label_audit": admitted_label_audit,
        "actual_67_20771": actual_67_20771_audit(),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["result_payload_sha256_before_self_hash"] = sha256(encoded).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "results.json",
    )
    args = parser.parse_args()
    result = run()
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "result": str(output),
        "sha256": sha256(output.read_bytes()).hexdigest(),
        "guarded_slice_audit": result["guarded_slice_audit"],
        "nonregular_hits": result["arithmetic_prime_search"]["nonregular_hits"],
        "actual_residual": result["actual_67_20771"]["aligned_anchor_1"]["residual"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
