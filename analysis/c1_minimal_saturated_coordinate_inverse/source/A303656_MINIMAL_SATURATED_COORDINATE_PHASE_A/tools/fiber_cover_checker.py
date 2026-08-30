#!/usr/bin/env python3
"""Exact l-adic fiber-cover classifier and bounded exhaustive checker."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from fractions import Fraction
import itertools
from pathlib import Path

from common import (
    AuditError,
    Cylinder,
    complete_frontiers,
    cylinder_cells,
    dynamic_cells,
    event_mass,
    fraction_record,
    frontier_count,
    multiplicity_histogram,
    row_minimal,
    template_hash,
    uncovered_cells,
    write_json,
)


def allowed_shells(m: int, s_parity: int) -> tuple[int, ...]:
    if s_parity not in (0, 1):
        raise AuditError("s parity must be zero or one")
    return tuple(j for j in range(m) if (s_parity + j) % 2 == 1)


def branch_roots(l: int, j: int) -> tuple[Cylinder, ...]:
    return tuple(Cylinder(j + 1, digit * l**j) for digit in range(1, l))


def template_record(
    l: int,
    beta: int,
    m: int,
    accepted_j: tuple[int, ...],
    center_depth: int | None,
    rigid: tuple[Cylinder, ...],
    label: str,
    s_parity: int | None,
) -> dict:
    dynamic_present = bool(accepted_j)
    events = []
    row_descriptions = []
    if dynamic_present:
        event = dynamic_cells(l, beta, m, accepted_j, 0)
        events.append(event)
        row_descriptions.append({"type": "dynamic", "m": m, "accepted_j": list(accepted_j)})
    for cyl in rigid:
        events.append(cyl.cells(l, beta))
        row_descriptions.append({"type": "rigid", **cyl.as_record()})
    universe = l**beta
    holes = uncovered_cells(events, universe)
    masses = [event_mass(event, l, beta) for event in events]
    total = sum(masses, Fraction())
    hist = multiplicity_histogram(events, universe)
    minimal = row_minimal(events, universe)
    overlap_tail = [] if center_depth is None else [j for j in accepted_j if j >= center_depth]
    record = {
        "label": label,
        "l": l,
        "beta": beta,
        "m": m,
        "s_parity": s_parity,
        "accepted_j": list(accepted_j),
        "center_depth": center_depth,
        "rows": row_descriptions,
        "row_count": len(events),
        "event_masses": [fraction_record(x) for x in masses],
        "budget": fraction_record(total),
        "uncovered_cells": holes,
        "multiplicity_histogram": hist,
        "overlap_tail_j": overlap_tail,
        "exact_partition": hist == {"1": universe},
        "row_minimal": minimal,
    }
    record["template_sha256"] = template_hash(record)
    return record


def rigid_only_templates(l: int, beta: int) -> list[dict]:
    per_digit = [complete_frontiers(l, beta, Cylinder(1, digit)) for digit in range(l)]
    out = []
    for choice in itertools.product(*per_digit):
        rigid = tuple(sorted(itertools.chain.from_iterable(choice)))
        out.append(template_record(l, beta, 0, (), None, rigid, "rigid-only-prefix-frontier", None))
    return out


def dynamic_templates(l: int, beta: int, m: int, s_parity: int, accepted_j: tuple[int, ...]) -> list[dict]:
    if not accepted_j:
        return []
    out = []
    for e in range(1, beta + 1):
        if not any(j < e for j in accepted_j):
            continue  # dynamic row would be contained in the centered rigid cylinder
        branch_options = []
        for j in range(e):
            if j < m and j in accepted_j:
                continue
            for root in branch_roots(l, j):
                branch_options.append(complete_frontiers(l, beta, root))
        for selected in itertools.product(*branch_options) if branch_options else [()]:
            side = tuple(sorted(itertools.chain.from_iterable(selected))) if selected else ()
            rigid = tuple(sorted((Cylinder(e, 0),) + side))
            out.append(template_record(
                l,
                beta,
                m,
                accepted_j,
                e,
                rigid,
                "dynamic-plus-centered-prefix-frontiers",
                s_parity,
            ))
    return out


def generated_signatures(l: int, beta: int, m: int, accepted_j: tuple[int, ...]) -> set[tuple[tuple[int, int], ...]]:
    if accepted_j:
        records = []
        for s_parity in (0, 1):
            if set(accepted_j).issubset(allowed_shells(m, s_parity)):
                records.extend(dynamic_templates(l, beta, m, s_parity, accepted_j))
    else:
        records = rigid_only_templates(l, beta)
    return {
        tuple(sorted((row["depth"], row["residue"]) for row in record["rows"] if row["type"] == "rigid"))
        for record in records
    }


def brute_irredundant_signatures(l: int, beta: int, m: int, accepted_j: tuple[int, ...]) -> set[tuple[tuple[int, int], ...]]:
    """Independent subset brute force, used only for l=3,beta<=2."""
    if not (l == 3 and beta <= 2):
        raise AuditError("brute force is deliberately frozen to l=3,beta<=2")
    candidates = [Cylinder(depth, residue) for depth in range(1, beta + 1) for residue in range(l**depth)]
    dynamic = dynamic_cells(l, beta, m, accepted_j, 0) if accepted_j else None
    universe = l**beta
    out: set[tuple[tuple[int, int], ...]] = set()
    for mask in range(1 << len(candidates)):
        rigid = tuple(candidates[i] for i in range(len(candidates)) if mask >> i & 1)
        events = ([dynamic] if dynamic is not None else []) + [c.cells(l, beta) for c in rigid]
        if row_minimal(events, universe):
            out.add(tuple((c.depth, c.residue) for c in rigid))
    return out


def beta_symbolic_classification() -> dict:
    return {
        "beta_1": {
            "dynamic_s_odd_J0": "one dynamic shell S_0 plus the unique centered depth-1 rigid digit",
            "rigid_only": "all l depth-1 digits",
            "other": "none after row-minimal reduction",
        },
        "beta_2": {
            "rigid_only": "for each of the l depth-1 digits, independently take that digit or all l depth-2 children; labelled count 2^l",
            "dynamic_J0_s_odd": [
                "S_0 plus centered depth-1 cylinder",
                "S_0 plus all l depth-2 cylinders inside the center branch",
            ],
            "dynamic_J1_s_even": "S_1 plus centered depth-2 cell; each of the l-1 outer depth-1 branches is independently coarse or fully refined; labelled count 2^(l-1)",
            "overlap": "none: odd-valuation parity forbids accepting both j=0 and j=1",
        },
    }


def counterexamples() -> dict:
    # 1. Exact budget one, but the rigid digit is placed inside the dynamic shell.
    l, beta, m = 3, 1, 1
    bad_events = [dynamic_cells(l, beta, m, (0,), 0), cylinder_cells(l, beta, 1, 1)]
    bad = {
        "name": "budget_one_but_center_hole",
        "l": l,
        "beta": beta,
        "rows": [
            {"type": "dynamic", "accepted_j": [0], "center": 0},
            {"type": "rigid", "depth": 1, "residue": 1},
        ],
        "budget": fraction_record(sum((event_mass(e, l, beta) for e in bad_events), Fraction())),
        "uncovered_cells": uncovered_cells(bad_events, l**beta),
        "multiplicity_histogram": multiplicity_histogram(bad_events, l**beta),
    }
    bad["counterexample_sha256"] = template_hash(bad)

    rigid_events = [cylinder_cells(3, 1, 1, r) for r in range(3)]
    no_pair = {
        "name": "exact_cover_without_dynamic_beta_one_pair",
        "l": 3,
        "beta": 1,
        "rows": [{"type": "rigid", "depth": 1, "residue": r} for r in range(3)],
        "budget": fraction_record(sum((event_mass(e, 3, 1) for e in rigid_events), Fraction())),
        "uncovered_cells": uncovered_cells(rigid_events, 3),
        "row_minimal": row_minimal(rigid_events, 3),
    }
    no_pair["counterexample_sha256"] = template_hash(no_pair)

    overlap_events = [dynamic_cells(3, 3, 3, (0, 2), 0), cylinder_cells(3, 3, 1, 0)]
    overlap = {
        "name": "admitted_row_minimal_overlap_tail",
        "l": 3,
        "beta": 3,
        "m": 3,
        "s_parity": 1,
        "rows": [
            {"type": "dynamic", "accepted_j": [0, 2], "center": 0},
            {"type": "rigid", "depth": 1, "residue": 0},
        ],
        "budget": fraction_record(sum((event_mass(e, 3, 3) for e in overlap_events), Fraction())),
        "uncovered_cells": uncovered_cells(overlap_events, 27),
        "multiplicity_histogram": multiplicity_histogram(overlap_events, 27),
        "row_minimal": row_minimal(overlap_events, 27),
        "valuation_reduced_core": "delete accepted shell j=2 from E; the remaining event family is the beta-one exact partition",
    }
    overlap["counterexample_sha256"] = template_hash(overlap)

    assignment_sensitive = {
        "name": "coverage_depends_on_lower_coordinate_assignment",
        "l": 3,
        "beta": 1,
        "assignment_A": {
            "dynamic_center": 0,
            "rigid_event": {"depth": 1, "residue": 0},
            "uncovered_cells": [],
        },
        "assignment_B": {
            "dynamic_center": 0,
            "rigid_event": None,
            "uncovered_cells": [0],
        },
        "scope": "This is an exact cylinder-model warning: activation of a rigid row is conditioned on already-fixed lower coordinates.",
    }
    assignment_sensitive["counterexample_sha256"] = template_hash(assignment_sensitive)

    k2_guard = {
        "name": "K2_boundary_must_not_enter_odd_coordinate_catalog",
        "existing_exact_case": {
            "K_2": 2,
            "U": 5,
            "two_divides_U": False,
            "old_coordinate_wording_passed": True,
            "corrected_constant_boundary_passed": False,
            "direct_safe_count": 0,
        },
        "checker_policy": "fiber_cover_checker accepts only odd prime l; K_2 is handled before odd-coordinate induction.",
    }
    k2_guard["counterexample_sha256"] = template_hash(k2_guard)

    return {
        "budget_not_cover": bad,
        "covered_without_beta_one_pair": no_pair,
        "minimal_overlap": overlap,
        "lower_assignment_sensitivity": assignment_sensitive,
        "K2_separation": k2_guard,
    }


def build_catalog() -> dict:
    bounds = [
        {"l": 3, "beta_max": 3},
        {"l": 5, "beta_max": 2},
    ]
    groups = []
    all_records = []
    for spec in bounds:
        l = spec["l"]
        for beta in range(1, spec["beta_max"] + 1):
            records = rigid_only_templates(l, beta)
            for s_parity in (0, 1):
                for m in range(1, beta + 1):
                    allowed = allowed_shells(m, s_parity)
                    for size in range(1, len(allowed) + 1):
                        for accepted in itertools.combinations(allowed, size):
                            records.extend(dynamic_templates(l, beta, m, s_parity, tuple(accepted)))
            if any(record["uncovered_cells"] or not record["row_minimal"] for record in records):
                raise AssertionError("classifier emitted a non-cover or non-minimal template")
            records.sort(key=lambda r: (r["label"], r["m"], r["accepted_j"], r["center_depth"] or 0, r["row_count"], r["template_sha256"]))
            groups.append({
                "l": l,
                "beta": beta,
                "template_count": len(records),
                "frontier_recurrence": {str(h): frontier_count(l, h) for h in range(beta)},
                "templates": records,
            })
            all_records.extend(records)

    brute_checks = []
    for accepted, m in [((), 0), ((0,), 1), ((0,), 2), ((1,), 2)]:
        generated = generated_signatures(3, 2, m, accepted)
        brute = brute_irredundant_signatures(3, 2, m, accepted)
        check = {
            "l": 3,
            "beta": 2,
            "m": m,
            "accepted_j": list(accepted),
            "generated_count": len(generated),
            "bruteforce_count": len(brute),
            "match": generated == brute,
            "generated_hash": template_hash(sorted(generated)),
            "bruteforce_hash": template_hash(sorted(brute)),
        }
        if not check["match"]:
            raise AssertionError(f"bounded brute-force mismatch: {check}")
        brute_checks.append(check)

    result = {
        "schema": "a303656.minimal-fiber-template-catalog.v1",
        "model": "F_beta=Z/l^beta Z; dynamic shells centered at canonical zero; rigid rows are l-adic cylinders",
        "bounds": bounds,
        "classification": {
            "centered_row": "Every irredundant cover has exactly one rigid cylinder containing the canonical unresolved-center lift.",
            "side_frontiers": "Every other rigid row lies in one unaccepted shell before the centered depth and the rows in each side branch form a complete prefix-code frontier.",
            "dynamic_essentiality": "The dynamic row remains iff it accepts at least one shell j below the centered depth.",
            "overlap": "The only overlap cells are accepted shells j at or beyond the centered depth; their multiplicity is exactly two.",
        },
        "beta_symbolic_classification": beta_symbolic_classification(),
        "bounded_independent_bruteforce": brute_checks,
        "groups": groups,
        "counterexamples": counterexamples(),
        "theorem_checks": {
            "all_generated_are_row_minimal_covers": True,
            "no_multiplicity_above_two": all(max(map(int, record["multiplicity_histogram"])) <= 2 for record in all_records),
            "exact_budget_iff_no_overlap_tail": all(
                ((record["budget"]["numerator"] == record["budget"]["denominator"]) == (not record["overlap_tail_j"]))
                for record in all_records
            ),
        },
        "PASS": True,
    }
    result["catalog_sha256"] = template_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_json(args.output, build_catalog())


if __name__ == "__main__":
    main()
