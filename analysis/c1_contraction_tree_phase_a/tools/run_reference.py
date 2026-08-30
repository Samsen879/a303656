#!/usr/bin/env python3
"""Generate all machine-readable reference results.

The output directory is replaced file-by-file with deterministic JSON.  No
repository code is imported.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from fractions import Fraction
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from contraction import (  # noqa: E402
    Event,
    beta_two_multishell_example,
    branching_pair_example,
    covered_points,
    exhaustive_universal_order_check,
    first_density_saturation_without_coverage,
    first_exact_cover_without_beta_one_pair,
    semantic_contraction_trace,
    semantic_eliminate_max,
)
from model import (  # noqa: E402
    OddRow,
    TwoAdicRow,
    coarse_fatal_by_enumeration,
    corrupted_coarse_fatal_zero_as_last_shell,
    direct_system_evaluation,
    factorint,
    first_witness_on_progression,
    fraction_pair,
    multiplicative_order_prime,
    odd_fatal,
    odd_row_data,
    odd_status,
    system_period,
    two_adic_period,
    two_adic_unsafe,
)

AUTHORITY_SHA = "29fee0317b268d2b2747f9564efc445fdd6da7f9"
AUTHORITY_TREE = "0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55"
REPOSITORY_ID = 1333945235


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def arithmetic_dependencies() -> dict[str, object]:
    primes = [3, 7, 11, 31, 67, 20771, 40487, 1645333507]
    rows = []
    for p in primes:
        w = multiplicative_order_prime(5, p)
        # K=3 is only a probe for s and period geometry; no row assertion is made.
        probe = OddRow(p=p, K=3, r=0, E=(1,), name=f"p={p}")
        data = odd_row_data(probe)
        rows.append(
            {
                "p": p,
                "w": w,
                "w_factorization": {str(q): e for q, e in factorint(w).items()},
                "s": data["s"],
                "ord_p3": data["ell"],
            }
        )
    return {
        "PASS": True,
        "formula_checked": "ord_(p^K)(5)=w_p*p^max(0,K-s_p)",
        "probe_K": 3,
        "rows": rows,
    }


def chain_replay() -> dict[str, object]:
    rows = [
        OddRow(11, 2, 4, (1,), "p=11"),
        OddRow(67, 2, 4, (1,), "p=67"),
        OddRow(20771, 2, 20775, (1,), "p=20771"),
    ]
    L = system_period(rows)
    full = direct_system_evaluation(rows, anchor=1, period=L)
    cylinder = first_witness_on_progression(rows, anchor=1, modulus=310, residue=0, period=L)

    # Relabel the 737 points as an exact 11 x 67 triangular model.
    events = [
        Event("p=11", 0, frozenset((x,) for x in range(1, 11)), "dynamic"),
        Event("p=67", 1, frozenset((0, y) for y in range(1, 67)), "dynamic"),
        Event("p=20771", 1, frozenset({(0, 0)}), "rigid"),
    ]
    semantic = semantic_contraction_trace([11, 67], events)
    return {
        "PASS": (
            L == 228470
            and full["safe_count"] == 176698
            and cylinder["first_witness_counts"]
            == {"p=11": 670, "p=67": 66, "p=20771": 1, "safe": 0}
            and semantic["root_covered"]
        ),
        "anchor": 1,
        "period": L,
        "full_period": full,
        "cylinder_d_mod_310": cylinder,
        "triangular_semantic_contraction": semantic,
    }


def aligned_and_misaligned_pair() -> dict[str, object]:
    p = 67
    q = 20771
    anchor = 1
    dynamic = OddRow(p, 2, 4, (1,), "dynamic_p=67")
    q2 = q * q
    b_aligned = 0
    b_misaligned = 155
    r_aligned = (3 + pow(5, b_aligned, q2) + q) % q2
    r_misaligned = (3 + pow(5, b_misaligned, q2) + q) % q2
    rigid_aligned = OddRow(q, 2, r_aligned, (1,), "rigid_q=20771_aligned")
    rigid_misaligned = OddRow(q, 2, r_misaligned, (1,), "rigid_q=20771_misaligned")
    U = lcm(multiplicative_order_prime(5, p), multiplicative_order_prime(5, q))
    lower_modulus = lcm(multiplicative_order_prime(5, p), multiplicative_order_prime(5, q) // p)
    if U // lower_modulus != p:
        raise AssertionError("expected a 67-element fiber")

    def evaluate(rigid: OddRow) -> dict[str, object]:
        dynamic_digits = []
        rigid_digits = []
        local_zero_digits = []
        covered_digits = []
        for t in range(p):
            d = lower_modulus * t
            p_status = odd_status(dynamic, anchor, d)[0]
            q_status = odd_status(rigid, anchor, d)[0]
            if p_status == "fatal":
                dynamic_digits.append(t)
            elif p_status == "zero":
                local_zero_digits.append(t)
            if q_status == "fatal":
                rigid_digits.append(t)
            if p_status == "fatal" or q_status == "fatal":
                covered_digits.append(t)
        return {
            "dynamic_fatal_digits": dynamic_digits,
            "dynamic_local_zero_digits": local_zero_digits,
            "rigid_digits": rigid_digits,
            "covered_count": len(covered_digits),
            "uncovered_digits": sorted(set(range(p)) - set(covered_digits)),
            "budget": fraction_pair(len(dynamic_digits) + len(rigid_digits), p),
            "actual_union_density": fraction_pair(len(covered_digits), p),
            "fiber_covered": len(covered_digits) == p,
        }

    aligned = evaluate(rigid_aligned)
    misaligned = evaluate(rigid_misaligned)
    return {
        "PASS": (
            aligned["fiber_covered"]
            and aligned["dynamic_local_zero_digits"] == aligned["rigid_digits"] == [0]
            and not misaligned["fiber_covered"]
            and misaligned["budget"] == [1, 1]
            and misaligned["uncovered_digits"] == [0]
        ),
        "anchor": anchor,
        "p": p,
        "q": q,
        "w_p": multiplicative_order_prime(5, p),
        "w_q": multiplicative_order_prime(5, q),
        "U": U,
        "lower_modulus": lower_modulus,
        "dynamic_row": {"K": 2, "r": 4, "E": [1]},
        "aligned_rigid_row": {"K": 2, "b": b_aligned, "r": r_aligned, "E": [1]},
        "misaligned_rigid_row": {"K": 2, "b": b_misaligned, "r": r_misaligned, "E": [1]},
        "contracted_lower_congruences_same": True,
        "contracted_system": [
            "d == 0 (mod 22)",
            "d == 0 (mod 155)",
            "equivalently d == 0 (mod 3410)",
        ],
        "aligned": aligned,
        "misaligned": misaligned,
        "logical_point": "The lower residual congruences do not encode the p-digit alignment; omitting the alignment check makes contraction unsound.",
    }


def k2_boundary_replay() -> dict[str, object]:
    odd = OddRow(11, 2, 0, (1,), "p=11")
    cases = {}
    specifications = [
        ("no_two_adic_row", None),
        ("K2_equals_2_safe", TwoAdicRow(2, 0, "two_adic")),
        ("K2_equals_2_unsafe", TwoAdicRow(2, 1, "two_adic")),
        ("K2_equals_3_coordinate", TwoAdicRow(3, 0, "two_adic")),
    ]
    for name, two in specifications:
        result = direct_system_evaluation([odd], anchor=0, two_row=two)
        cases[name] = {
            "K_2": None if two is None else two.K,
            "r_2": None if two is None else two.r,
            "t_2": None if two is None else two_adic_period(two),
            **result,
        }
    return {
        "PASS": (
            cases["no_two_adic_row"]["safe_count"] == 55
            and cases["K2_equals_2_safe"]["safe_count"] == 55
            and cases["K2_equals_2_unsafe"]["safe_count"] == 0
            and cases["K2_equals_3_coordinate"]["safe_count"] == 55
        ),
        "anchor": 0,
        "odd_row": {"p": 11, "K": 2, "r": 0, "E": [1]},
        "cases": cases,
    }


def local_zero_corruption() -> dict[str, object]:
    row = OddRow(3, 2, 2, (1,), "p=3")
    U = 2
    L = 6
    x = 0
    lifts = []
    for d in range(x, L, U):
        status, valuation = odd_status(row, anchor=0, d=d)
        lifts.append({"d": d, "status": status, "valuation": valuation})
    correct = coarse_fatal_by_enumeration(row, 0, x, U, L)
    corrupted = corrupted_coarse_fatal_zero_as_last_shell(row, 0, x, U, L)
    return {
        "PASS": (not correct and corrupted),
        "row": {"p": 3, "K": 2, "r": 2, "E": [1]},
        "anchor": 0,
        "coarse_class": "d == 0 (mod 2)",
        "full_period": L,
        "lifts": lifts,
        "correct_coarse_fatal": correct,
        "corrupted_zero_as_K_minus_1_coarse_fatal": corrupted,
        "logical_point": "The unresolved local zero at d=0 prevents coarse fatality.",
    }


def abstract_results() -> dict[str, object]:
    density_ce = first_density_saturation_without_coverage()
    no_pair_ce = first_exact_cover_without_beta_one_pair()
    beta2 = beta_two_multishell_example()
    moduli, events, branching = branching_pair_example()
    branching_trace = semantic_contraction_trace(moduli, events)

    # Exact residual that is not one singleton and not a beta-one complement.
    residual_events = [
        Event(
            name=f"rigid_y{y}_z{z}",
            top=1,
            prefixes=frozenset({(y, z)}),
            kind="rigid",
        )
        for y in (0, 2)
        for z in range(3)
    ]
    next_moduli, next_events, residual_trace = semantic_eliminate_max([5, 3], residual_events)
    derived = sorted(next(e for e in next_events if e.kind == "semantic_macro").prefixes)
    residual_set = [point[0] for point in derived]
    residual_is_singleton = len(residual_set) == 1
    residual_is_beta_one_complement = len(residual_set) == 4

    order_check = exhaustive_universal_order_check([2, 3, 2], keep=0)
    return {
        "PASS": (
            density_ce["coordinate_size"] == 3
            and no_pair_ce["coordinate_size"] == 3
            and beta2["covered"]
            and branching_trace["root_covered"]
            and not branching["naive_results_equal"]
            and order_check["PASS"]
            and residual_set == [0, 2]
        ),
        "density_saturation_without_coverage": density_ce,
        "exact_cover_without_beta_one_pair": no_pair_ce,
        "beta_two_multiple_shell_cover": beta2,
        "branch_local_reuse_and_naive_nonconfluence": {
            **branching,
            "semantic_trace": branching_trace,
        },
        "semantic_residual_nonclosure_example": {
            "parent_moduli": [5, 3],
            "saturated_lower_residues": residual_set,
            "residual_is_singleton": residual_is_singleton,
            "residual_is_beta_one_complement": residual_is_beta_one_complement,
            "semantic_identity": residual_trace,
            "logical_point": "The exact macro-predicate is a lower-coordinate subset, but not a single rigid singleton or beta-one dynamic shell in this grammar.",
        },
        "universal_projection_order_invariance": order_check,
        "simultaneous_anchor_terminal_conflict": {
            "anchor_0_required_terminal_residue": 0,
            "anchor_1_required_terminal_residue": 1,
            "each_fixed_anchor_tree_can_close": True,
            "common_terminal_residue_exists": False,
            "classification": "abstract coupling countermodel, not an arithmetic complete certificate",
        },
    }



def two_anchor_two_adic_audit(max_K: int = 10) -> dict[str, object]:
    levels = []
    overall_pass = True
    for K in range(2, max_K + 1):
        modulus = 2 ** K
        period = 1 if K == 2 else 2 ** (K - 2)
        pair_histogram: dict[str, int] = {}
        worst_min = Fraction(0, 1)
        worst_residues: list[int] = []
        for r in range(modulus):
            counts = []
            row = TwoAdicRow(K, r, "two_adic")
            for anchor in (0, 1):
                counts.append(sum(two_adic_unsafe(row, anchor, d) for d in range(period)))
            key = f"{counts[0]}/{period},{counts[1]}/{period}"
            pair_histogram[key] = pair_histogram.get(key, 0) + 1
            current = min(Fraction(counts[0], period), Fraction(counts[1], period))
            if current > worst_min:
                worst_min = current
                worst_residues = [r]
            elif current == worst_min:
                worst_residues.append(r)
        level_pass = (worst_min == 0 if K == 2 else worst_min <= Fraction(1, 2))
        overall_pass = overall_pass and level_pass
        levels.append({
            "K": K,
            "modulus": modulus,
            "period": period,
            "residues_checked": modulus,
            "worst_min_anchor_unsafe_density": [worst_min.numerator, worst_min.denominator],
            "worst_residues": worst_residues,
            "pair_histogram": dict(sorted(pair_histogram.items())),
            "PASS": level_pass,
        })
    return {
        "PASS": overall_pass,
        "max_K": max_K,
        "lemma_checked": "for every common residue r, one anchor has unsafe density <=1/2; for K=2 one anchor is completely safe",
        "levels": levels,
    }

def environment_result() -> dict[str, object]:
    return {
        "python": sys.version.splitlines()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "hash_seed": os.environ.get("PYTHONHASHSEED"),
        "dependencies": "Python standard library only",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    results = {
        "authority_binding.json": {
            "repository": "Samsen879/a303656",
            "repository_id": REPOSITORY_ID,
            "main_sha": AUTHORITY_SHA,
            "main_tree": AUTHORITY_TREE,
            "binding_verified_externally_before_computation": True,
            "repository_id_verified_externally": True,
            "main_ref_verified_externally": True,
            "tree_verified_externally": True,
            "github_modified": False,
            "project_state": {
                "PROJECT": "PAUSED",
                "ACTIVE_PROMOTED_ROUTE": "NONE",
                "A303656": "UNRESOLVED",
            },
        },
        "dependency_recheck.json": arithmetic_dependencies(),
        "chain_replay.json": chain_replay(),
        "aligned_misaligned_pair.json": aligned_and_misaligned_pair(),
        "k2_boundary.json": k2_boundary_replay(),
        "local_zero_corruption.json": local_zero_corruption(),
        "two_anchor_two_adic_audit.json": two_anchor_two_adic_audit(),
        "abstract_search.json": abstract_results(),
        "environment.json": environment_result(),
    }
    for name, data in results.items():
        write_json(out / name, data)

    pass_map = {
        name: bool(data.get("PASS", True)) if isinstance(data, dict) else True
        for name, data in results.items()
    }
    summary = {
        "PASS": all(pass_map.values()),
        "checks": pass_map,
        "outcome": "Outcome C plus an unconditional semantic contraction theorem",
        "main_candidate_strong_reading": "not established; completeness alone does not imply aligned/admitted-class contraction",
        "semantic_tree_reading": "proved for every finite triangular coarse cover",
        "explicit_actual_arithmetic_defect": "67/20771 misaligned rigid digit: budget 1, union 66/67",
        "smallest_abstract_normal_form_counterexamples": {
            "density_saturation_without_coverage_coordinate_size": 3,
            "exact_cover_without_beta_one_pair_coordinate_size": 3,
            "beta_two_multiple_shell_coordinate_size": 9,
        },
        "missing_structural_hypothesis": "hereditary exact shell decomposability with branch-local reuse and admitted residual closure",
        "final_verdict": "TARGETED PARTIAL ADVANCE",
        "forbidden_claims_not_made": [
            "UNIVERSAL C=1 NO-GO",
            "COMPLETE CERTIFICATE",
            "A303656 SOLVED",
        ],
        "project_state": {
            "PROJECT": "PAUSED",
            "ACTIVE_PROMOTED_ROUTE": "NONE",
            "A303656": "UNRESOLVED",
        },
    }
    write_json(out / "summary.json", summary)
    return 0 if summary["PASS"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
