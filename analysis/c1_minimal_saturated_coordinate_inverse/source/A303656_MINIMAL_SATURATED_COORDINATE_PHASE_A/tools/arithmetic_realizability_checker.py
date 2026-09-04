#!/usr/bin/env python3
"""Bounded exact audit of arithmetic realizability resources.

The bounded search is evidence only.  Universal statements in the report are
proved separately from the finite scan.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from common import (
    AuditError,
    clipped_valuation,
    exact_lifting_depth,
    factor,
    fraction_record,
    is_prime,
    order_mod_prime,
    primes_up_to,
    template_hash,
    write_json,
)


def nonregular_record(q: int) -> dict:
    if not is_prime(q) or q % 4 != 3 or q == 5:
        raise AuditError("q is not an admitted odd row prime")
    w = order_mod_prime(5, q)
    s = exact_lifting_depth(5, q, w)
    fac = factor(w)
    largest = max(fac)
    return {
        "q": q,
        "q_mod_4": q % 4,
        "w_q": w,
        "order_factorization": {str(p): e for p, e in sorted(fac.items())},
        "s_q": s,
        "largest_order_prime": largest,
        "largest_order_prime_exponent": fac[largest],
        "rigid_positive_odd_depth_available": s >= 2,
    }


def scan_nonregular(bound: int) -> tuple[list[int], list[dict]]:
    searched = [q for q in primes_up_to(bound) if q % 4 == 3 and q != 5]
    found = []
    for q in searched:
        w = order_mod_prime(5, q)
        if pow(5, w, q * q) == 1:
            found.append(nonregular_record(q))
    return searched, found


def fatal_at_precision_two(p: int, residue: int, anchor: int, exponent: int) -> bool:
    value = residue - 3**anchor - pow(5, exponent, p * p)
    return clipped_valuation(value, p, 2) == 1


def two_square_mod_four(value: int) -> bool:
    """Exact sum-of-two-squares test modulo four."""
    return value % 4 in {0, 1, 2}


def k2_constant_boundary_replay() -> dict:
    """Independently replay the frozen K_2=2 constant obstruction.

    This deliberately remains outside the odd-coordinate fiber classifier.
    """
    p, precision, residue, anchor = 11, 2, 0, 0
    k2, r2 = 2, 1
    w = order_mod_prime(5, p)
    s = exact_lifting_depth(5, p, w)
    full_period = w * p ** max(0, precision - s)
    odd_fatal = [
        d for d in range(full_period)
        if fatal_at_precision_two(p, residue, anchor, d)
    ]
    two_safe = [
        d for d in range(full_period)
        if two_square_mod_four(r2 - 3**anchor - pow(5, d, 4))
    ]
    direct_safe = [d for d in two_safe if d not in odd_fatal]
    record = {
        "name": "K2=2 constant obstruction, independent replay",
        "p": p,
        "K": precision,
        "r": residue,
        "anchor": anchor,
        "K_2": k2,
        "r_2": r2,
        "w_p": w,
        "s_p": s,
        "U": w,
        "L": full_period,
        "two_divides_U": w % 2 == 0,
        "odd_fatal_count": len(odd_fatal),
        "two_adic_safe_count": len(two_safe),
        "direct_safe_count": len(direct_safe),
        "old_odd_coordinate_hypothesis_passes": len(odd_fatal) == 0,
        "corrected_constant_boundary_passes": len(two_safe) == full_period,
        "kept_outside_odd_coordinate_catalog": True,
    }
    expected = {
        "w_p": 5,
        "s_p": 1,
        "U": 5,
        "L": 55,
        "two_divides_U": False,
        "odd_fatal_count": 0,
        "two_adic_safe_count": 0,
        "direct_safe_count": 0,
        "old_odd_coordinate_hypothesis_passes": True,
        "corrected_constant_boundary_passes": False,
    }
    for key, value in expected.items():
        if record[key] != value:
            raise AssertionError(f"K2 boundary mismatch at {key}: {record[key]} != {value}")
    record["record_sha256"] = template_hash(record)
    return record


def actual_beta_one_67_20771() -> dict:
    l, q, anchor = 67, 20771, 1
    r_l, r_q = 4, 20775
    exponents = [3410 * t for t in range(l)]
    dynamic = [fatal_at_precision_two(l, r_l, anchor, d) for d in exponents]
    rigid = [fatal_at_precision_two(q, r_q, anchor, d) for d in exponents]
    assignment = bytearray()
    overlaps = 0
    holes = []
    for index, (a, b) in enumerate(zip(dynamic, rigid)):
        if not (a or b):
            holes.append(index)
        if a and b:
            overlaps += 1
        assignment.append(0 if a else (1 if b else 2))
    center_local_zero = clipped_valuation(r_l - 3**anchor - pow(5, 0, l * l), l, 2)
    record = {
        "dynamic_prime_l": l,
        "rigid_prime_q": q,
        "anchor": anchor,
        "lower_assignment": "d == 0 (mod 3410), after the coordinate-11 center has been fixed inside the d==0 (mod 310) chain fiber",
        "fiber_exponents": exponents,
        "dynamic_fatal_count": sum(dynamic),
        "rigid_fatal_count": sum(rigid),
        "overlap_count": overlaps,
        "uncovered_indices": holes,
        "assignment_sha256": hashlib.sha256(assignment).hexdigest(),
        "dynamic_order": order_mod_prime(5, l),
        "rigid_order": order_mod_prime(5, q),
        "v_67_rigid_order": factor(order_mod_prime(5, q)).get(67, 0),
        "s_dynamic": exact_lifting_depth(5, l, order_mod_prime(5, l)),
        "s_rigid": exact_lifting_depth(5, q, order_mod_prime(5, q)),
        "center_local_zero_clipped_valuation": center_local_zero,
        "local_zero_fail_closed": center_local_zero is None and not dynamic[0] and rigid[0],
        "exact_partition": not holes and overlaps == 0 and sum(dynamic) + sum(rigid) == l,
    }
    if not record["exact_partition"] or not record["local_zero_fail_closed"]:
        raise AssertionError("actual beta-one realization failed")
    record["record_sha256"] = template_hash(record)
    return record


def actual_dual_anchor_beta_one_67_20771() -> dict:
    """Replay one common-residue system on one fiber at each anchor.

    The two fibers use different lower-coordinate assignments.  This is a
    positive compatibility example, not uniform lower-class saturation and
    not a complete certificate.
    """
    l, q = 67, 20771
    r_l, r_q = 2, 13471
    lower_modulus = 3410
    full_period = 228470
    lower_assignments = {0: 2728, 1: 1639}
    expected_active_logs = {
        0: {"dynamic": 0, "rigid": 8308},
        1: {"dynamic": 11, "rigid": 7839},
    }

    def active_log(p: int, residue: int, anchor: int) -> int | None:
        order = order_mod_prime(5, p)
        target = (residue - 3**anchor) % p
        for exponent in range(order):
            if pow(5, exponent, p) == target:
                return exponent
        return None

    anchors: dict[str, dict] = {}
    assignment = bytearray()
    for anchor in (0, 1):
        dynamic_log = active_log(l, r_l, anchor)
        rigid_log = active_log(q, r_q, anchor)
        expected = expected_active_logs[anchor]
        if dynamic_log != expected["dynamic"] or rigid_log != expected["rigid"]:
            raise AssertionError("dual-anchor active-log mismatch")

        lower = lower_assignments[anchor]
        if lower % order_mod_prime(5, l) != dynamic_log:
            raise AssertionError("dynamic lower-coordinate assignment mismatch")
        if lower % (order_mod_prime(5, q) // l) != rigid_log % (order_mod_prime(5, q) // l):
            raise AssertionError("rigid lower-coordinate assignment mismatch")

        exponents = [(lower + lower_modulus * t) % full_period for t in range(l)]
        dynamic = [fatal_at_precision_two(l, r_l, anchor, d) for d in exponents]
        rigid = [fatal_at_precision_two(q, r_q, anchor, d) for d in exponents]
        holes = [i for i, flags in enumerate(zip(dynamic, rigid)) if not any(flags)]
        overlaps = [i for i, flags in enumerate(zip(dynamic, rigid)) if all(flags)]
        center_indices = [i for i, flag in enumerate(dynamic) if not flag]
        local_zero_fail_closed = (
            len(center_indices) == 1
            and rigid[center_indices[0]]
            and clipped_valuation(
                r_l - 3**anchor - pow(5, exponents[center_indices[0]], l * l),
                l,
                2,
            ) is None
        )
        if holes or overlaps or sum(dynamic) != 66 or sum(rigid) != 1 or not local_zero_fail_closed:
            raise AssertionError("dual-anchor fiber is not an exact fail-closed 66+1 partition")
        assignment.extend(0 if a else 1 if b else 2 for a, b in zip(dynamic, rigid))
        anchors[str(anchor)] = {
            "lower_assignment_mod_3410": lower,
            "dynamic_active_log": dynamic_log,
            "rigid_active_log": rigid_log,
            "dynamic_fatal_count": sum(dynamic),
            "rigid_fatal_count": sum(rigid),
            "uncovered_indices": holes,
            "overlap_indices": overlaps,
            "local_zero_fail_closed": local_zero_fail_closed,
        }

    record = {
        "name": "one common-residue system with one exact beta-one fiber at each anchor",
        "l": l,
        "q": q,
        "dynamic_residue": r_l,
        "rigid_residue": r_q,
        "lower_modulus": lower_modulus,
        "full_period": full_period,
        "anchors": anchors,
        "assignment_sha256": hashlib.sha256(assignment).hexdigest(),
        "scope": "Positive pointwise compatibility only: the anchor-dependent fibers do not establish uniform lower-coordinate saturation or a complete certificate.",
    }
    record["record_sha256"] = template_hash(record)
    return record


def unrealizable_q7_rigid_label() -> dict:
    q = 7
    w = order_mod_prime(5, q)
    s = exact_lifting_depth(5, q, w)
    record = {
        "name": "q=7 cannot supply a positive odd rigid valuation",
        "abstract_request": {"coordinate_l": 3, "depth": 1, "rigid_prime_q": q},
        "w_q": w,
        "s_q": s,
        "order_factorization": {str(p): e for p, e in sorted(factor(w).items())},
        "positive_odd_h_below_s_exists": any(h % 2 == 1 for h in range(1, s)),
        "realizable": False,
        "reason": "Although 3 divides ord_7(5)=6, s_7=1 leaves no positive odd h<s_7.",
    }
    if (w, s, record["positive_odd_h_below_s_exists"]) != (6, 1, False):
        raise AssertionError("q=7 rigid-label boundary changed")
    record["record_sha256"] = template_hash(record)
    return record


def separate_anchor_beta_one_class_zero() -> dict:
    """Two exact one-anchor beta-one fibers with prescribed class zero.

    Each anchor is realizable after choosing its row residues separately.  The
    two prescribed templates cannot be implemented by one common-residue
    system because both row residues disagree already modulo their primes.
    """
    l, q = 67, 20771
    exponents = [3410 * t for t in range(l)]
    anchors: dict[str, dict] = {}
    for c in (0, 1):
        r_l = 3**c + 1
        r_q = q + 3**c + 1
        dynamic = [fatal_at_precision_two(l, r_l, c, d) for d in exponents]
        rigid = [fatal_at_precision_two(q, r_q, c, d) for d in exponents]
        holes = [i for i, flags in enumerate(zip(dynamic, rigid)) if not any(flags)]
        overlaps = [i for i, flags in enumerate(zip(dynamic, rigid)) if all(flags)]
        record = {
            "anchor": c,
            "r_dynamic": r_l,
            "r_rigid": r_q,
            "prescribed_full_exponent_class": 0,
            "dynamic_fatal_count": sum(dynamic),
            "rigid_fatal_count": sum(rigid),
            "uncovered_indices": holes,
            "overlap_indices": overlaps,
            "exact_partition": not holes and not overlaps and sum(dynamic) + sum(rigid) == l,
        }
        if not record["exact_partition"]:
            raise AssertionError(f"separate anchor beta-one template failed at c={c}")
        anchors[str(c)] = record
    combined = {
        "name": "separately realizable prescribed beta-one class-zero fibers, not one common-residue system",
        "l": l,
        "q": q,
        "lower_assignment": "d == 0 (mod 3410)",
        "anchors": anchors,
        "one_common_dynamic_residue_possible": anchors["0"]["r_dynamic"] % l == anchors["1"]["r_dynamic"] % l,
        "one_common_rigid_residue_possible": anchors["0"]["r_rigid"] % q == anchors["1"]["r_rigid"] % q,
        "scope": "This excludes the prescribed class-zero pair. It does not exclude other class choices or larger systems.",
    }
    if combined["one_common_dynamic_residue_possible"] or combined["one_common_rigid_residue_possible"]:
        raise AssertionError("prescribed separate-anchor incompatibility disappeared")
    combined["record_sha256"] = template_hash(combined)
    return combined


def compatible_class_pairs_k2_h1(q: int) -> dict:
    """Full class-pair compatibility at K=2 and fixed valuation h=1.

    At the mod-q level a common residue requires 5^b0 - 5^b1 == 2.
    For q>3 this condition is also sufficient to choose nonzero first-lift
    coefficients on both anchors.
    """
    w = order_mod_prime(5, q)
    lookup: dict[int, int] = {}
    value = 1
    for b in range(w):
        lookup[value] = b
        value = value * 5 % q
    pairs = []
    value = 1
    for b0 in range(w):
        b1 = lookup.get((value - 2) % q)
        if b1 is not None:
            pairs.append([b0, b1])
        value = value * 5 % q
    digest = hashlib.sha256(json.dumps(pairs, separators=(",", ":")).encode()).hexdigest()
    return {
        "q": q,
        "w_q": w,
        "pair_count": len(pairs),
        "pairs_sha256": digest,
        "first_pairs": pairs[:20],
        "known_pair_6528_2_present": [6528, 2] in pairs,
        "pair_0_0_present": [0, 0] in pairs,
        "criterion": "5^b0 - 5^b1 == 2 (mod q)",
    }


def fatal_classes(q: int, residue: int, anchor: int) -> list[int]:
    w = order_mod_prime(5, q)
    modulus = q * q
    return [
        b
        for b in range(w)
        if clipped_valuation(residue - 3**anchor - pow(5, b, modulus), q, 2) == 1
    ]


def common_residue_audit() -> dict:
    q = 20771
    compatibility = compatible_class_pairs_k2_h1(q)
    sample_r = 96315155
    sample = {
        "q": q,
        "r": sample_r,
        "classes": {"0": fatal_classes(q, sample_r, 0), "1": fatal_classes(q, sample_r, 1)},
    }
    if sample["classes"] != {"0": [6528], "1": [2]}:
        raise AssertionError("dual-anchor common-residue sample mismatch")

    independent = {
        "anchor_0": {"desired_b": 0, "residue": q + 2},
        "anchor_1": {"desired_b": 0, "residue": q + 4},
    }
    if fatal_classes(q, q + 2, 0) != [0] or fatal_classes(q, q + 4, 1) != [0]:
        raise AssertionError("separate-anchor class-zero construction failed")
    return {
        "compatibility": compatibility,
        "verified_common_residue_sample": sample,
        "separately_realizable_but_not_common": {
            "desired_full_classes": {"anchor_0": 0, "anchor_1": 0},
            "separate_residues": independent,
            "common_residue_possible": compatibility["pair_0_0_present"],
            "reason": "mod q, anchor 0 requires r==2 while anchor 1 requires r==4",
            "scope": "This blocks the prescribed use of one fixed rigid row; it does not rule out a larger system with additional rows.",
        },
    }


def feasibility_summary(found: list[dict], known: list[dict], bound: int) -> dict:
    bounded_signatures: dict[str, int] = {}
    for row in found:
        if row["s_q"] >= 2:
            key = f"l={row['largest_order_prime']},e={row['largest_order_prime_exponent']}"
            bounded_signatures[key] = bounded_signatures.get(key, 0) + 1
    depth_ge_2 = [row for row in found if row["largest_order_prime_exponent"] >= 2]
    partners = []
    for row in known:
        l = row["largest_order_prime"]
        partner = {
            "q": row["q"],
            "l": l,
            "e": row["largest_order_prime_exponent"],
            "l_is_prime": is_prime(l),
            "l_mod_4": l % 4,
            "dynamic_l_admitted": is_prime(l) and l % 4 == 3 and l != 5,
        }
        if partner["dynamic_l_admitted"]:
            w_l = order_mod_prime(5, l)
            partner["w_l"] = w_l
            partner["s_l"] = exact_lifting_depth(5, l, w_l)
            partner["one_anchor_beta_one_resource_signature"] = row["s_q"] >= 2 and row["largest_order_prime_exponent"] == 1
        partners.append(partner)
    return {
        "universal_impossibility_example": {
            "abstract_template": "dynamic beta-one shell at coordinate l=5 plus one centered rigid digit",
            "realizable": False,
            "reason": "the formal class admits dynamic rows only at primes p == 3 (mod 4), p != 5",
        },
        "bounded_signature_counts": bounded_signatures,
        "bounded_depth_ge_2_rigid_resources": depth_ge_2,
        "bounded_absence_warning": f"No qualifying largest-coordinate depth e>=2 was found for q<={bound}; this is finite evidence only.",
        "known_nonregular_partner_audit": partners,
        "resource_lemma": {
            "rigid": "N_e active rigid cylinders at coordinate l and depth e require N_e distinct primes q with q==3 mod4, s_q>=2, P+(ord_q(5))=l, and v_l(ord_q(5))=e.",
            "ambient_beta": "If no covering row has l-order depth beta, an additional admitted support row with v_l(ord_q(5))>=beta is required to create the ambient coordinate.",
            "dynamic": "A dynamic l-row requires l==3 mod4, l!=5, K_l>=s_l+m, and accepted shell indices j only where s_l+j is positive odd.",
        },
    }


def build_result(bound: int, searched_primes_output: Path) -> dict:
    searched, found = scan_nonregular(bound)
    searched_primes_output.parent.mkdir(parents=True, exist_ok=True)
    searched_primes_output.write_text("".join(f"{q}\n" for q in searched), encoding="ascii")

    known_qs = [20771, 40487, 1645333507]
    known = [nonregular_record(q) for q in known_qs]
    if [r["q"] for r in found] != [20771, 40487]:
        raise AssertionError("bounded nonregular search result changed")

    result = {
        "schema": "a303656.arithmetic-realizability-audit.v1",
        "search": {
            "domain": {
                "q_min": 3,
                "q_max_inclusive": bound,
                "predicate": "q prime, q == 3 (mod 4), q != 5",
                "searched_prime_count": len(searched),
                "searched_primes_file": searched_primes_output.name,
                "searched_primes_sha256": hashlib.sha256(searched_primes_output.read_bytes()).hexdigest(),
            },
            "complexity_estimate": {
                "candidate_count": len(searched),
                "method": "sieve to bound; factor q-1; exact order reduction; one modular exponentiation modulo q^2 for nonregularity",
                "asymptotic_description": "O(B log log B) sieve plus trial-division factor/order work over the frozen candidate set",
            },
            "nonregular_found": found,
            "found_count": len(found),
            "no_universal_inference_from_absence": True,
        },
        "known_panel": known,
        "actual_beta_one_realization": actual_beta_one_67_20771(),
        "actual_dual_anchor_beta_one_realization": actual_dual_anchor_beta_one_67_20771(),
        "separate_anchor_beta_one_class_zero": separate_anchor_beta_one_class_zero(),
        "common_residue": common_residue_audit(),
        "k2_constant_boundary_replay": k2_constant_boundary_replay(),
        "feasibility": feasibility_summary(found, known, bound),
        "unrealizable_q7_rigid_label": unrealizable_q7_rigid_label(),
        "local_zero_policy": "A value zero modulo p^K has clipped valuation None and is never accepted; the actual 67/20771 fiber test checks the dynamic center is covered only by the rigid row.",
        "both_anchor_policy": "Anchorwise cylinder choices are not independent: every row must pass the exact common-residue congruence before a two-anchor template is called realizable.",
        "PASS": True,
    }
    result["result_sha256"] = template_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=500_000)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--searched-primes-output", type=Path, required=True)
    args = parser.parse_args()
    if args.bound != 500_000:
        raise AuditError("the audited Phase A bound is frozen at 500000")
    write_json(args.output, build_result(args.bound, args.searched_primes_output))


if __name__ == "__main__":
    main()
