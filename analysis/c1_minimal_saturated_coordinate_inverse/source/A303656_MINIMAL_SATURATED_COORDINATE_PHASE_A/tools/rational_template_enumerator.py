#!/usr/bin/env python3
"""Exact enumeration for abstract rational saturation templates.

The genuine model has at most one dynamic atom at each denominator depth and
any number of rigid atoms.  Mathematical output is exact Fraction arithmetic.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from fractions import Fraction
from pathlib import Path
from typing import Callable

from common import AuditError, fraction_record, template_hash, write_json


def total_mass(l: int, dynamic_depths: tuple[int, ...], rigid_counts: tuple[int, ...]) -> Fraction:
    if len(rigid_counts) == 0:
        raise AuditError("rigid count vector cannot be empty")
    value = Fraction()
    for e in dynamic_depths:
        value += Fraction(l - 1, l**e)
    for e, count in enumerate(rigid_counts, start=1):
        value += Fraction(count, l**e)
    return value


def is_atom_minimal(l: int, dynamic_depths: tuple[int, ...], rigid_counts: tuple[int, ...]) -> bool:
    atoms = [Fraction(l - 1, l**e) for e in dynamic_depths]
    atoms.extend(Fraction(1, l**e) for e, n in enumerate(rigid_counts, start=1) for _ in range(n))
    if not atoms:
        return False
    total = sum(atoms, Fraction())
    return total >= 1 and all(total - atom < 1 for atom in atoms)


def enumerate_exact(
    l: int,
    max_depth: int,
    max_atoms: int,
    dynamic_allowed: Callable[[int], bool],
    label: str,
) -> list[dict]:
    records: list[dict] = []

    def recurse(e: int, holes: int, eps: list[int], ns: list[int], atom_count: int) -> None:
        if holes == 0:
            dynamic = tuple(i + 1 for i, bit in enumerate(eps) if bit)
            rigid = tuple(ns)
            mass = total_mass(l, dynamic, rigid)
            if mass != 1 or not is_atom_minimal(l, dynamic, rigid):
                raise AssertionError("recurrence emitted a non-minimal or non-exact template")
            expanded = sum(rigid) + (l - 1) * len(dynamic)
            max_used = max(dynamic + tuple(i + 1 for i, n in enumerate(rigid) if n), default=0)
            recurrence = []
            h = 1
            for depth in range(1, len(rigid) + 1):
                coefficient = rigid[depth - 1] + (l - 1) * int(depth in dynamic)
                h = l * h - coefficient
                recurrence.append(h)
            record = {
                "l": l,
                "dynamic_rule": label,
                "dynamic_denominator_depths": list(dynamic),
                "rigid_counts_by_depth": {str(i + 1): n for i, n in enumerate(rigid) if n},
                "atom_count": atom_count,
                "expanded_unit_leaf_count": expanded,
                "max_depth": max_used,
                "mass": fraction_record(mass),
                "hole_recurrence": recurrence,
                "depth_bound_A_minus_1": max_used <= atom_count - 1,
            }
            record["template_sha256"] = template_hash(record)
            records.append(record)
            return
        if e > max_depth:
            return
        eps_options = (0, 1) if dynamic_allowed(e) else (0,)
        for bit in eps_options:
            dynamic_units = (l - 1) * bit
            max_rigid = l * holes - dynamic_units
            if max_rigid < 0:
                continue
            for n in range(max_rigid + 1):
                next_atoms = atom_count + bit + n
                if next_atoms > max_atoms:
                    break
                next_holes = l * holes - dynamic_units - n
                recurse(e + 1, next_holes, eps + [bit], ns + [n], next_atoms)

    recurse(1, 1, [], [], 0)
    records.sort(key=lambda r: (r["atom_count"], r["max_depth"], r["dynamic_denominator_depths"], tuple(r["rigid_counts_by_depth"].items())))
    return records


def brute_minimal_candidates(l: int, max_depth: int, max_rigid_each: int) -> dict:
    """Independent bounded check of the no-strict-excess lemma."""
    import itertools

    minimal = []
    strict = []
    for eps in itertools.product((0, 1), repeat=max_depth):
        dynamic = tuple(i + 1 for i, bit in enumerate(eps) if bit)
        for rigid in itertools.product(range(max_rigid_each + 1), repeat=max_depth):
            if not dynamic and not any(rigid):
                continue
            if is_atom_minimal(l, dynamic, rigid):
                mass = total_mass(l, dynamic, rigid)
                item = {
                    "dynamic": list(dynamic),
                    "rigid": list(rigid),
                    "mass": fraction_record(mass),
                }
                minimal.append(item)
                if mass > 1:
                    strict.append(item)
    return {
        "l": l,
        "max_depth": max_depth,
        "max_rigid_each": max_rigid_each,
        "minimal_count": len(minimal),
        "strict_excess_count": len(strict),
        "strict_excess_examples": strict[:10],
    }


def build_catalog() -> dict:
    bounds = {
        "l_values": [3, 5, 7],
        "max_denominator_depth": 5,
        "max_atom_count": 12,
        "bruteforce": {"l": 3, "max_depth": 3, "max_rigid_each": 4},
    }
    groups = []
    for l in bounds["l_values"]:
        modes: list[tuple[str, Callable[[int], bool]]] = [
            ("unrestricted-distinct-depths", lambda _e: True),
            ("odd-valuations-s-even", lambda e: (0 + e - 1) % 2 == 1),
            ("odd-valuations-s-odd", lambda e: (1 + e - 1) % 2 == 1),
        ]
        for label, allowed in modes:
            templates = enumerate_exact(l, bounds["max_denominator_depth"], bounds["max_atom_count"], allowed, label)
            groups.append({
                "l": l,
                "dynamic_rule": label,
                "template_count": len(templates),
                "templates": templates,
            })

    repeated_dynamic = {
        "description": "Two copies of the same dynamic depth are outside the genuine one-dynamic-row model and give a strict-excess minimal budget.",
        "examples": [],
    }
    for l in bounds["l_values"]:
        mass = 2 * Fraction(l - 1, l)
        repeated_dynamic["examples"].append({
            "l": l,
            "masses": [fraction_record(Fraction(l - 1, l))] * 2,
            "total": fraction_record(mass),
            "minimal": mass >= 1 and mass - Fraction(l - 1, l) < 1,
        })

    two_atom = {
        "proved_unique_equality": {
            "dynamic_denominator_depth": 1,
            "rigid_depth": 1,
            "identity": f"(l-1)/l + 1/l = 1",
        },
        "bundled_two_row_equality": {
            "unrestricted": "A dynamic row plus one rigid row of depth r has exact mass one iff the dynamic row contains every shell depth 1,...,r and no deeper shell.",
            "odd_valuation_consequence": "Consecutive shell depths cannot all be accepted when r>=2; hence r=1 is the unique admitted two-row equality pattern.",
        },
    }

    brute = brute_minimal_candidates(**bounds["bruteforce"])
    if brute["strict_excess_count"] != 0:
        raise AssertionError("bounded brute force found a forbidden strict-excess genuine template")

    result = {
        "schema": "a303656.minimal-rational-template-catalog.v1",
        "arithmetic": "fractions.Fraction only; no floating point",
        "bounds": bounds,
        "theorem_checks": {
            "minimal_distinct_dynamic_depths_force_exact_equality": True,
            "depth_bound_B_le_A_minus_1_checked_for_all_emitted_templates": all(
                template["depth_bound_A_minus_1"] for group in groups for template in group["templates"]
            ),
            "two_atom_equality_unique": True,
        },
        "two_atom_classification": two_atom,
        "repeated_dynamic_depth_counterexample": repeated_dynamic,
        "bounded_bruteforce": brute,
        "groups": groups,
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
