#!/usr/bin/env python3
"""Finite triangular-cover and contraction reference model."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Iterable, Sequence


Point = tuple[int, ...]


@dataclass(frozen=True)
class Event:
    name: str
    top: int
    prefixes: frozenset[Point]
    kind: str = "generic"

    def covers(self, point: Point) -> bool:
        if self.top < 0:
            return () in self.prefixes
        return point[: self.top + 1] in self.prefixes


def all_points(moduli: Sequence[int]) -> list[Point]:
    return list(product(*(range(n) for n in moduli))) if moduli else [()]


def covered_points(moduli: Sequence[int], events: Sequence[Event]) -> frozenset[Point]:
    return frozenset(point for point in all_points(moduli) if any(e.covers(point) for e in events))


def semantic_eliminate_max(moduli: Sequence[int], events: Sequence[Event]) -> tuple[list[int], list[Event], dict[str, object]]:
    """Eliminate the largest coordinate by exact full-fiber saturation.

    The resulting macro-event is an arbitrary lower predicate.  Therefore this
    is semantically exact but does not claim closure in the admitted row grammar.
    """
    if not moduli:
        return [], list(events), {"root_covered": any(e.covers(()) for e in events)}
    k = len(moduli) - 1
    lower_moduli = list(moduli[:-1])
    top_size = moduli[-1]
    lower_events = [e for e in events if e.top < k]
    top_events = [e for e in events if e.top == k]
    saturated: set[Point] = set()
    already_lower: set[Point] = set()
    for y in all_points(lower_moduli):
        probe = y + (0,)
        if any(e.covers(probe) for e in lower_events):
            already_lower.add(y)
        if all(any(e.covers(y + (z,)) for e in top_events) for z in range(top_size)):
            saturated.add(y)
    next_events = list(lower_events)
    if saturated:
        next_events.append(
            Event(
                name=f"SAT_COORD_{k}",
                top=k - 1,
                prefixes=frozenset(saturated),
                kind="semantic_macro",
            )
        )
    original_full_fibers = {
        y
        for y in all_points(lower_moduli)
        if all(any(e.covers(y + (z,)) for e in events) for z in range(top_size))
    }
    contracted_covered = covered_points(lower_moduli, next_events)
    if original_full_fibers != contracted_covered:
        raise AssertionError("semantic contraction identity failed")
    trace = {
        "coordinate_index": k,
        "coordinate_size": top_size,
        "lower_point_count": len(all_points(lower_moduli)),
        "already_lower_covered": len(already_lower),
        "saturated_fiber_count": len(saturated),
        "full_fiber_projection_count": len(original_full_fibers),
        "identity_verified": True,
    }
    return lower_moduli, next_events, trace


def semantic_contraction_trace(moduli: Sequence[int], events: Sequence[Event]) -> dict[str, object]:
    cur_moduli = list(moduli)
    cur_events = list(events)
    levels: list[dict[str, object]] = []
    initial_covered = covered_points(cur_moduli, cur_events)
    initial_complete = len(initial_covered) == len(all_points(cur_moduli))
    while cur_moduli:
        cur_moduli, cur_events, level = semantic_eliminate_max(cur_moduli, cur_events)
        levels.append(level)
    root_covered = any(e.covers(()) for e in cur_events)
    return {
        "initial_complete": initial_complete,
        "root_covered": root_covered,
        "depth": len(levels),
        "levels": levels,
        "sound_and_complete": initial_complete == root_covered,
    }


def eliminate_coordinate_from_set(
    points: frozenset[Point], moduli: Sequence[int], coordinate: int
) -> tuple[frozenset[Point], list[int]]:
    if not (0 <= coordinate < len(moduli)):
        raise IndexError("coordinate out of range")
    remaining_moduli = list(moduli[:coordinate]) + list(moduli[coordinate + 1 :])
    projected: set[Point] = set()
    for y in all_points(remaining_moduli):
        ok = True
        for z in range(moduli[coordinate]):
            point = y[:coordinate] + (z,) + y[coordinate:]
            if point not in points:
                ok = False
                break
        if ok:
            projected.add(y)
    return frozenset(projected), remaining_moduli


def universal_projection(
    points: frozenset[Point], moduli: Sequence[int], elimination_order: Sequence[int]
) -> tuple[frozenset[Point], list[int]]:
    active_labels = list(range(len(moduli)))
    cur_points = points
    cur_moduli = list(moduli)
    for original_label in elimination_order:
        idx = active_labels.index(original_label)
        cur_points, cur_moduli = eliminate_coordinate_from_set(cur_points, cur_moduli, idx)
        active_labels.pop(idx)
    return cur_points, cur_moduli


def exhaustive_universal_order_check(moduli: Sequence[int], keep: int) -> dict[str, object]:
    universe = all_points(moduli)
    eliminate = [i for i in range(len(moduli)) if i != keep]
    if len(eliminate) != 2:
        raise ValueError("reference check currently expects exactly two eliminated coordinates")
    checked = 0
    for mask in range(1 << len(universe)):
        pts = frozenset(universe[i] for i in range(len(universe)) if (mask >> i) & 1)
        left, left_moduli = universal_projection(pts, moduli, eliminate)
        right, right_moduli = universal_projection(pts, moduli, list(reversed(eliminate)))
        if left != right or left_moduli != right_moduli:
            return {
                "PASS": False,
                "checked_before_failure": checked,
                "mask": mask,
                "left": sorted(left),
                "right": sorted(right),
            }
        checked += 1
    return {
        "PASS": True,
        "moduli": list(moduli),
        "kept_coordinate": keep,
        "subsets_checked": checked,
        "orders": [eliminate, list(reversed(eliminate))],
    }


def first_density_saturation_without_coverage(max_odd_size: int = 11) -> dict[str, object]:
    for n in range(3, max_odd_size + 1, 2):
        for center in range(n):
            dynamic = set(range(n)) - {center}
            for rigid_digit in range(n):
                rigid = {rigid_digit}
                budget = Fraction(len(dynamic), n) + Fraction(1, n)
                union = dynamic | rigid
                if budget >= 1 and len(union) < n:
                    return {
                        "coordinate_size": n,
                        "dynamic_center": center,
                        "dynamic_fatal_digits": sorted(dynamic),
                        "rigid_digit": rigid_digit,
                        "budget": [budget.numerator, budget.denominator],
                        "covered_digits": sorted(union),
                        "uncovered_digits": sorted(set(range(n)) - union),
                        "minimal_in_search_grammar": True,
                    }
    raise RuntimeError("no counterexample found")


def first_exact_cover_without_beta_one_pair(max_odd_size: int = 9) -> dict[str, object]:
    """Search grammar: at most one complement-of-singleton dynamic event and distinct rigid singletons."""
    best = None
    for n in range(3, max_odd_size + 1, 2):
        digits = range(n)
        dynamic_options: list[int | None] = [None] + list(digits)
        for center in dynamic_options:
            dynamic = set() if center is None else set(digits) - {center}
            for rcount in range(n + 1):
                for rigid_digits in combinations(digits, rcount):
                    union = dynamic | set(rigid_digits)
                    aligned = center is not None and center in rigid_digits
                    event_count = (0 if center is None else 1) + rcount
                    if len(union) == n and not aligned:
                        candidate = {
                            "coordinate_size": n,
                            "dynamic_center": center,
                            "rigid_digits": list(rigid_digits),
                            "event_count": event_count,
                            "minimal_in_search_grammar": True,
                        }
                        if best is None or (n, event_count) < (best[0], best[1]):
                            best = (n, event_count, candidate)
                if best is not None and best[0] == n:
                    break
        if best is not None and best[0] == n:
            return best[2]
    raise RuntimeError("no counterexample found")


def beta_two_multishell_example() -> dict[str, object]:
    p = 3
    beta = 2
    n = p ** beta
    center_residue = 0
    dynamic = {x for x in range(n) if x % p != center_residue}
    center_cylinder = sorted(set(range(n)) - dynamic)
    rigid_singletons = center_cylinder.copy()
    union = dynamic | set(rigid_singletons)
    return {
        "p": p,
        "beta": beta,
        "coordinate_size": n,
        "dynamic_shell": sorted(dynamic),
        "unresolved_center_cylinder": center_cylinder,
        "rigid_singletons_required": rigid_singletons,
        "rigid_count": len(rigid_singletons),
        "covered": len(union) == n,
        "single_rigid_closes_center": any({r} >= set(center_cylinder) for r in rigid_singletons),
    }


def branching_pair_example() -> tuple[list[int], list[Event], dict[str, object]]:
    """A complete 2x3 cover where a dynamic event must be reused branch-locally."""
    moduli = [2, 3]
    dynamic_prefixes = frozenset((y, z) for y in range(2) for z in (0, 1))
    r0 = frozenset({(0, 2)})
    r1 = frozenset({(1, 2)})
    events = [
        Event("D", 1, dynamic_prefixes, "beta_one_dynamic"),
        Event("R0", 1, r0, "rigid"),
        Event("R1", 1, r1, "rigid"),
    ]
    original_complete = len(covered_points(moduli, events)) == 6
    branch_local_residual = {0, 1}
    naive_order_r0_first = {0}
    naive_order_r1_first = {1}
    return moduli, events, {
        "original_complete": original_complete,
        "branch_local_residual": sorted(branch_local_residual),
        "naive_global_consume_R0_then_R1": sorted(naive_order_r0_first),
        "naive_global_consume_R1_then_R0": sorted(naive_order_r1_first),
        "naive_results_equal": naive_order_r0_first == naive_order_r1_first,
        "both_naive_results_incomplete": len(naive_order_r0_first) < 2 and len(naive_order_r1_first) < 2,
    }
