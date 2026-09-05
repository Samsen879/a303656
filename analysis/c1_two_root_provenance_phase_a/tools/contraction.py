"""Independent guarded-slice/provenance laboratory; Python standard library only.

Geometry is a product of coordinate subsets (bit masks). A provenance monomial
is a set of original row labels, not a multiset of consumable resources.
No repository implementation is imported.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

Shape = tuple[int, ...]

@dataclass(frozen=True)
class Clause:
    shape: Shape
    provenance: frozenset[int]


def antichain(items: Iterable[frozenset]) -> frozenset[frozenset]:
    result: list[frozenset] = []
    for term in sorted(set(items), key=lambda s: (len(s), tuple(sorted(s)))):
        if not any(old <= term for old in result):
            result.append(term)
    return frozenset(result)


def minimal_slice_covers(slices: list[int], full: int) -> list[tuple[int, ...]]:
    """Enumerate inclusion-minimal covers, with distinct clause identities."""
    covers: list[tuple[int, ...]] = []
    covered_sets: list[frozenset[int]] = []
    for size in range(1, len(slices) + 1):
        for choice in combinations(range(len(slices)), size):
            fs = frozenset(choice)
            if any(previous <= fs for previous in covered_sets):
                continue
            union = 0
            for i in choice:
                union |= slices[i]
            if union == full:
                covers.append(choice)
                covered_sets.append(fs)
    return covers


def clean_clauses(clauses: Iterable[Clause]) -> list[Clause]:
    """Only identical-geometry provenance absorption is used."""
    by_shape: dict[Shape, list[frozenset[int]]] = {}
    for item in clauses:
        if any(v == 0 for v in item.shape):
            continue
        by_shape.setdefault(item.shape, []).append(item.provenance)
    result = [Clause(shape, p) for shape, prov in by_shape.items()
              for p in antichain(prov)]
    return sorted(result, key=lambda i: (i.shape, len(i.provenance), tuple(sorted(i.provenance))))


def contract_provenance(dims: tuple[int, ...], shapes: list[Shape | None],
                        trace: bool = False) -> dict:
    if any(n < 2 for n in dims):
        raise ValueError('Every coordinate must have at least two values.')
    fulls = tuple((1 << n) - 1 for n in dims)
    for shape in shapes:
        if shape is not None and (len(shape) != len(dims) or
            any(s < 1 or s & ~f for s, f in zip(shape, fulls))):
            raise ValueError('Invalid nonempty product event.')
    clauses = clean_clauses(Clause(s, frozenset([i]))
                            for i, s in enumerate(shapes) if s is not None)
    stages = []
    total_created = 0
    for level in range(len(dims) - 1, -1, -1):
        full = fulls[level]
        top = [c for c in clauses if c.shape[-1] != full]
        lower = [Clause(c.shape[:-1], c.provenance)
                 for c in clauses if c.shape[-1] == full]
        created = []
        records = []
        for cover in minimal_slice_covers([c.shape[-1] for c in top], full):
            guard = list(fulls[:level])
            prov: frozenset[int] = frozenset()
            for j in cover:
                clause = top[j]
                guard = [x & y for x, y in zip(guard, clause.shape[:-1])]
                prov = prov | clause.provenance
            if any(g == 0 for g in guard):
                continue
            macro = Clause(tuple(guard), prov)
            created.append(macro)
            if trace:
                records.append({'guard': guard, 'provenance': sorted(prov),
                                'parent_provenances': [sorted(top[j].provenance) for j in cover],
                                'parent_slices': [top[j].shape[-1] for j in cover],
                                'resource_kind': 'DERIVED MACRO'})
        total_created += len(created)
        clauses = clean_clauses(lower + created)
        if trace:
            stages.append({'coordinate_index': level, 'size': dims[level],
                           'top_clause_count': len(top), 'new_macros': records,
                           'output_clause_count': len(clauses)})
    supports = antichain(c.provenance for c in clauses)
    return {'covered': bool(supports), 'minimal_supports': supports,
            'derived_clause_count_before_absorption': total_created, 'stages': stages}


def contract_geometry(dims: tuple[int, ...], shapes: list[Shape | None]) -> bool:
    """Geometry-only, but with the original row states FROZEN.

Exact geometry and provenance MUST agree about truth in this use case.
"""
    current = set(s for s in shapes if s is not None)
    for level in range(len(dims) - 1, -1, -1):
        full = (1 << dims[level]) - 1
        top = sorted(s for s in current if s[-1] != full)
        output = set(s[:-1] for s in current if s[-1] == full)
        for choice in minimal_slice_covers([s[-1] for s in top], full):
            guard = [(1 << n) - 1 for n in dims[:level]]
            for i in choice:
                guard = [a & b for a, b in zip(guard, top[i][:-1])]
            if all(guard):
                output.add(tuple(guard))
        current = output
    return () in current


# State-sensitive provenance. Tokens (row, state) designate ONE original
# paired-mask state, shared across all points, branches, and both anchors.
Token = tuple[int, int]
Term = frozenset[Token]
Polynomial = frozenset[Term]
ZERO: Polynomial = frozenset()
ONE: Polynomial = frozenset([frozenset()])


def add(a: Polynomial, b: Polynomial) -> Polynomial:
    return antichain(a | b)


def multiply(a: Polynomial, b: Polynomial) -> Polynomial:
    products = []
    for x in a:
        for y in b:
            term = x | y
            assignments: dict[int, int] = {}
            valid = True
            for row, state in term:
                if row in assignments and assignments[row] != state:
                    valid = False
                    break
                assignments[row] = state
            if valid:
                products.append(term)
    return antichain(products)


def symbolic_roots(dims: tuple[int, ...], state_masks: list[list[tuple[int, int]]]) -> dict:
    """Build original-demand positive clauses; eliminate coordinates exactly.

Mask bit order is lexicographic product order. This routine manipulates
state-literal antichains; it does not enumerate assignments to all rows.
"""
    n = 1
    for size in dims:
        n *= size
    roots = []
    stage_sizes = []
    for c in (0, 1):
        predicates = []
        for x in range(n):
            terms = [frozenset([(p, s)]) for p, states in enumerate(state_masks)
                     for s, pair in enumerate(states) if pair[c] >> x & 1]
            predicates.append(antichain(terms))
        local_sizes = []
        for size in reversed(dims):
            contracted = []
            for start in range(0, len(predicates), size):
                value = ONE
                for f in predicates[start:start + size]:
                    value = multiply(value, f)
                contracted.append(value)
            predicates = contracted
            local_sizes.append(sum(len(p) for p in predicates))
        roots.append(predicates[0])
        stage_sizes.append(local_sizes)
    return {'anchor_roots': roots, 'joint': multiply(*roots),
            'stage_term_counts': stage_sizes}


def evaluate_polynomial(poly: Polynomial, assignment: tuple[int, ...]) -> bool:
    return any(all(assignment[r] == s for r, s in term) for term in poly)
