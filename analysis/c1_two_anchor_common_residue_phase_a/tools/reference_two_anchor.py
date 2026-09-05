#!/usr/bin/env python3
"""Exact reference computation for A303656 C=1 two-anchor uniformization.

This program is intentionally standalone and uses only Python's standard
library.  It does not import repository code.  It performs two differently
organized exact classifications:

  Method A: solve common-residue equations in exponent/logarithm space and
            propagate CRT/alignment constraints symbolically;
  Method B: enumerate residue classes directly and, for selected systems,
            enumerate every lower assignment and every 67-adic fiber digit.

The computation is scoped to the beta-one pair (p,q)=(67,20771), K=2,
E={1}; universal theorem statements are proved in REPORT.md and are not
inferred from this finite enumeration.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

AUTHORITY = {
    "repository": "Samsen879/a303656",
    "repository_id": 1333945235,
    "main_sha": "1100eb5ba01d90e5b1001be0bdfa464860fdbb92",
    "main_tree": "ad1269916bf420c564e34887a96c808033fe538b",
    "state": {
        "PROJECT": "PAUSED",
        "ACTIVE_PROMOTED_ROUTE": "NONE",
        "A303656": "UNRESOLVED",
    },
}

P = 67
Q = 20771
P2 = P * P
Q2 = Q * Q
W_P = 22
ORD_P2 = W_P * P
W_Q = 10385  # 155 * 67; s_Q=2, so this is also ord_{Q^2}(5).
LOWER_Q = W_Q // P  # 155
LOWER_MODULUS = 3410  # lcm(22,155)
FULL_PERIOD = 228470  # LOWER_MODULUS * 67


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_record(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def powers(base: int, modulus: int, order: int) -> list[int]:
    values: list[int] = []
    x = 1
    for _ in range(order):
        values.append(x)
        x = (x * base) % modulus
    if x != 1:
        raise AssertionError(f"claimed order {order} does not close modulo {modulus}")
    if len(set(values)) != order:
        raise AssertionError(f"claimed order {order} is not exact modulo {modulus}")
    return values


def crt_coprime(a: int, m: int, b: int, n: int) -> int:
    """Return the unique x modulo mn with x=a (mod m), x=b (mod n)."""
    if __import__("math").gcd(m, n) != 1:
        raise ValueError("moduli must be coprime")
    return (a + (((b - a) * pow(m, -1, n)) % n) * m) % (m * n)


def fatal_k2_h1(
    prime: int,
    residue: int,
    anchor: int,
    exponent: int,
    order: int,
    power_table: list[int],
) -> bool:
    """Exact fail-closed test v_prime(residue-3^c-5^d)=1 at precision prime^2."""
    modulus = prime * prime
    value = (residue - 3**anchor - power_table[exponent % order]) % modulus
    return value % prime == 0 and value != 0


def method_a_dynamic_pairs(pow_p2: list[int]) -> list[dict[str, int]]:
    """Solve 5^a0-5^a1=2 mod 67^2 in logarithm space."""
    lookup = {value: exponent for exponent, value in enumerate(pow_p2)}
    records: list[dict[str, int]] = []
    for a0, value0 in enumerate(pow_p2):
        a1 = lookup.get((value0 - 2) % P2)
        if a1 is not None:
            records.append({"a0": a0, "a1": a1, "r_p": (1 + value0) % P2})
    return records


def method_b_dynamic_pairs(pow_p2: list[int]) -> list[dict[str, int]]:
    """Enumerate all r_p mod 67^2 and recover both exact center logarithms."""
    lookup = {value: exponent for exponent, value in enumerate(pow_p2)}
    records: list[dict[str, int]] = []
    for residue in range(P2):
        a0 = lookup.get((residue - 1) % P2)
        a1 = lookup.get((residue - 3) % P2)
        if a0 is not None and a1 is not None:
            records.append({"a0": a0, "a1": a1, "r_p": residue})
    return records


def method_a_rigid_pairs(pow_q: list[int]) -> list[dict[str, int]]:
    """Solve 5^b0-5^b1=2 mod q in logarithm space."""
    lookup = {value: exponent for exponent, value in enumerate(pow_q)}
    records: list[dict[str, int]] = []
    for b0, value0 in enumerate(pow_q):
        b1 = lookup.get((value0 - 2) % Q)
        if b1 is not None:
            records.append({"b0": b0, "b1": b1, "r_q_mod_q": (1 + value0) % Q})
    return records


def method_b_rigid_pairs(pow_q: list[int]) -> list[dict[str, int]]:
    """Enumerate every r_q mod q and recover both rigid logarithms."""
    lookup = {value: exponent for exponent, value in enumerate(pow_q)}
    records: list[dict[str, int]] = []
    for residue in range(Q):
        b0 = lookup.get((residue - 1) % Q)
        b1 = lookup.get((residue - 3) % Q)
        if b0 is not None and b1 is not None:
            records.append({"b0": b0, "b1": b1, "r_q_mod_q": residue})
    return records


def normalized_records(records: Iterable[dict[str, int]], keys: tuple[str, ...]) -> list[tuple[int, ...]]:
    return sorted(tuple(record[key] for key in keys) for record in records)


def q2_valid_lift_count(record: dict[str, int], pow_q2: list[int]) -> tuple[int, list[int]]:
    """Count r_q=rbar+kq for which neither anchor is a fail-closed local zero."""
    rbar = record["r_q_mod_q"]
    excluded: set[int] = set()
    for anchor, key in ((0, "b0"), (1, "b1")):
        exact_zero_residue = (3**anchor + pow_q2[record[key]]) % Q2
        if exact_zero_residue % Q != rbar:
            raise AssertionError("mod-q compatibility and q^2 lift disagree")
        excluded.add(((exact_zero_residue - rbar) // Q) % Q)
    return Q - len(excluded), sorted(excluded)


def pointwise_join(
    dynamic_pairs: list[dict[str, int]],
    rigid_pairs: list[dict[str, int]],
    pow_q2: list[int],
) -> tuple[list[dict[str, Any]], int]:
    """Join exact center-alignment constraints at both anchors.

    Alignment is a_c == b_c (mod 67).  The lower assignment at anchor c is
    then the CRT solution of a_c mod 22 and b_c mod 155.
    """
    rigid_by_signature: dict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for rigid in rigid_pairs:
        rigid_by_signature[(rigid["b0"] % P, rigid["b1"] % P)].append(rigid)

    joined: list[dict[str, Any]] = []
    total_full_residue_systems = 0
    for dynamic in dynamic_pairs:
        signature = (dynamic["a0"] % P, dynamic["a1"] % P)
        for rigid in rigid_by_signature.get(signature, []):
            y0 = crt_coprime(dynamic["a0"] % W_P, W_P, rigid["b0"] % LOWER_Q, LOWER_Q)
            y1 = crt_coprime(dynamic["a1"] % W_P, W_P, rigid["b1"] % LOWER_Q, LOWER_Q)
            valid_lifts, excluded_lifts = q2_valid_lift_count(rigid, pow_q2)
            total_full_residue_systems += valid_lifts
            joined.append(
                {
                    "r_p_mod_p2": dynamic["r_p"],
                    "r_q_mod_q": rigid["r_q_mod_q"],
                    "a0": dynamic["a0"],
                    "a1": dynamic["a1"],
                    "b0": rigid["b0"],
                    "b1": rigid["b1"],
                    "lower_y0_mod_3410": y0,
                    "lower_y1_mod_3410": y1,
                    "same_lower_assignment": y0 == y1,
                    "valid_r_q_lifts_mod_q2": valid_lifts,
                    "excluded_local_zero_lifts": excluded_lifts,
                }
            )
    return joined, total_full_residue_systems


def independent_nested_join_count(
    dynamic_pairs: list[dict[str, int]], rigid_pairs: list[dict[str, int]]
) -> tuple[int, int]:
    """A direct nested check, independent of the signature hash-join."""
    aligned = 0
    common_lower = 0
    for dynamic in dynamic_pairs:
        for rigid in rigid_pairs:
            if dynamic["a0"] % P != rigid["b0"] % P:
                continue
            if dynamic["a1"] % P != rigid["b1"] % P:
                continue
            aligned += 1
            y0 = crt_coprime(dynamic["a0"] % W_P, W_P, rigid["b0"] % LOWER_Q, LOWER_Q)
            y1 = crt_coprime(dynamic["a1"] % W_P, W_P, rigid["b1"] % LOWER_Q, LOWER_Q)
            if y0 == y1:
                common_lower += 1
    return aligned, common_lower


def fiber_stats(
    r_p: int,
    r_q: int,
    lower_assignment: int,
    anchor: int,
    pow_p2: list[int],
    pow_q2: list[int],
) -> dict[str, Any]:
    dynamic: list[bool] = []
    rigid: list[bool] = []
    exponents: list[int] = []
    for digit in range(P):
        exponent = (lower_assignment + LOWER_MODULUS * digit) % FULL_PERIOD
        exponents.append(exponent)
        dynamic.append(fatal_k2_h1(P, r_p, anchor, exponent, ORD_P2, pow_p2))
        rigid.append(fatal_k2_h1(Q, r_q, anchor, exponent, W_Q, pow_q2))

    holes = [i for i, (d_flag, r_flag) in enumerate(zip(dynamic, rigid)) if not (d_flag or r_flag)]
    overlaps = [i for i, (d_flag, r_flag) in enumerate(zip(dynamic, rigid)) if d_flag and r_flag]
    dynamic_nonfatal = [i for i, flag in enumerate(dynamic) if not flag]
    rigid_digits = [i for i, flag in enumerate(rigid) if flag]

    local_zero_fail_closed = False
    if len(dynamic_nonfatal) == 1:
        center = dynamic_nonfatal[0]
        exponent = exponents[center]
        local_value = (r_p - 3**anchor - pow_p2[exponent % ORD_P2]) % P2
        local_zero_fail_closed = local_value == 0 and not dynamic[center]

    return {
        "anchor": anchor,
        "lower_assignment_mod_3410": lower_assignment,
        "dynamic_fatal_count": sum(dynamic),
        "rigid_fatal_count": sum(rigid),
        "hole_count": len(holes),
        "overlap_count": len(overlaps),
        "hole_indices": holes,
        "overlap_indices": overlaps,
        "dynamic_nonfatal_indices": dynamic_nonfatal,
        "rigid_indices": rigid_digits,
        "local_zero_fail_closed": local_zero_fail_closed,
        "exact_66_plus_1_partition": (
            sum(dynamic) == P - 1
            and sum(rigid) == 1
            and not holes
            and not overlaps
            and local_zero_fail_closed
        ),
    }


def scan_all_lower_assignments(
    r_p: int,
    r_q: int,
    pow_p2: list[int],
    pow_q2: list[int],
) -> dict[str, Any]:
    saturation = {0: [], 1: []}
    joint_hole_histogram: Counter[tuple[int, int]] = Counter()
    minimum_total_holes = 2 * P
    minimizers: list[dict[str, Any]] = []

    for lower_assignment in range(LOWER_MODULUS):
        stats0 = fiber_stats(r_p, r_q, lower_assignment, 0, pow_p2, pow_q2)
        stats1 = fiber_stats(r_p, r_q, lower_assignment, 1, pow_p2, pow_q2)
        holes = (stats0["hole_count"], stats1["hole_count"])
        joint_hole_histogram[holes] += 1
        if holes[0] == 0:
            saturation[0].append(lower_assignment)
        if holes[1] == 0:
            saturation[1].append(lower_assignment)
        total = holes[0] + holes[1]
        if total < minimum_total_holes:
            minimum_total_holes = total
            minimizers = [
                {
                    "lower_assignment_mod_3410": lower_assignment,
                    "anchor_0_holes": holes[0],
                    "anchor_1_holes": holes[1],
                }
            ]
        elif total == minimum_total_holes:
            minimizers.append(
                {
                    "lower_assignment_mod_3410": lower_assignment,
                    "anchor_0_holes": holes[0],
                    "anchor_1_holes": holes[1],
                }
            )

    histogram_records = [
        {"anchor_0_holes": h0, "anchor_1_holes": h1, "lower_assignment_count": count}
        for (h0, h1), count in sorted(joint_hole_histogram.items())
    ]
    return {
        "saturated_lower_assignments": {
            "anchor_0": saturation[0],
            "anchor_1": saturation[1],
            "intersection": sorted(set(saturation[0]) & set(saturation[1])),
        },
        "minimum_total_holes_over_common_lower_assignment": minimum_total_holes,
        "minimizers": minimizers,
        "joint_hole_histogram": histogram_records,
        "joint_hole_histogram_sha256": sha256_record(histogram_records),
    }


def full_period_stats(
    r_p: int,
    r_q: int,
    pow_p2: list[int],
    pow_q2: list[int],
) -> dict[str, Any]:
    per_anchor: dict[str, dict[str, int]] = {}
    flags_by_anchor: dict[int, list[bool]] = {}
    for anchor in (0, 1):
        covered_flags: list[bool] = []
        dynamic_count = rigid_count = overlap_count = 0
        for exponent in range(FULL_PERIOD):
            dynamic = fatal_k2_h1(P, r_p, anchor, exponent, ORD_P2, pow_p2)
            rigid = fatal_k2_h1(Q, r_q, anchor, exponent, W_Q, pow_q2)
            dynamic_count += int(dynamic)
            rigid_count += int(rigid)
            overlap_count += int(dynamic and rigid)
            covered_flags.append(dynamic or rigid)
        flags_by_anchor[anchor] = covered_flags
        covered_count = sum(covered_flags)
        per_anchor[str(anchor)] = {
            "dynamic_fatal_count": dynamic_count,
            "rigid_fatal_count": rigid_count,
            "overlap_count": overlap_count,
            "covered_count": covered_count,
            "safe_count": FULL_PERIOD - covered_count,
        }
    both = sum(a and b for a, b in zip(flags_by_anchor[0], flags_by_anchor[1]))
    return {
        "per_anchor": per_anchor,
        "both_anchors_covered_at_same_exponent_count": both,
        "exponents_not_jointly_covered_count": FULL_PERIOD - both,
        "is_complete_two_anchor_certificate": both == FULL_PERIOD,
    }


def direct_system_record(
    name: str,
    r_p: int,
    r_q: int,
    expected_y0: int,
    expected_y1: int,
    pow_p2: list[int],
    pow_q2: list[int],
) -> dict[str, Any]:
    scan = scan_all_lower_assignments(r_p, r_q, pow_p2, pow_q2)
    sats = scan["saturated_lower_assignments"]
    if sats["anchor_0"] != [expected_y0] or sats["anchor_1"] != [expected_y1]:
        raise AssertionError(f"unexpected saturation sets for {name}: {sats}")
    if sats["intersection"]:
        raise AssertionError(f"common lower saturation unexpectedly found for {name}")

    witness0 = fiber_stats(r_p, r_q, expected_y0, 0, pow_p2, pow_q2)
    witness1 = fiber_stats(r_p, r_q, expected_y1, 1, pow_p2, pow_q2)
    if not witness0["exact_66_plus_1_partition"] or not witness1["exact_66_plus_1_partition"]:
        raise AssertionError(f"pointwise witness failed for {name}")

    record = {
        "name": name,
        "r_67_mod_67_squared": r_p,
        "r_20771_mod_20771_squared": r_q,
        "pointwise_witness_anchor_0": witness0,
        "pointwise_witness_anchor_1": witness1,
        "all_lower_assignments": scan,
        "full_period": full_period_stats(r_p, r_q, pow_p2, pow_q2),
        "level_classification": {
            "pointwise_exact_fiber_at_each_anchor": True,
            "same_lower_assignment_full_fiber": False,
            "lower_uniform_saturation": False,
            "anchor_uniform_joint_contraction": False,
            "complete_two_anchor_certificate": False,
        },
    }
    record["record_sha256"] = sha256_record(record)
    return record


def build_result() -> dict[str, Any]:
    if (P2, Q2, ORD_P2, W_Q, LOWER_MODULUS, FULL_PERIOD) != (
        4489,
        431434441,
        1474,
        10385,
        3410,
        228470,
    ):
        raise AssertionError("frozen arithmetic constants changed")

    pow_p2 = powers(5, P2, ORD_P2)
    pow_p = powers(5, P, W_P)
    pow_q = powers(5, Q, W_Q)
    pow_q2 = powers(5, Q2, W_Q)

    method_a_dynamic = method_a_dynamic_pairs(pow_p2)
    method_b_dynamic = method_b_dynamic_pairs(pow_p2)
    dyn_keys = ("a0", "a1", "r_p")
    if normalized_records(method_a_dynamic, dyn_keys) != normalized_records(method_b_dynamic, dyn_keys):
        raise AssertionError("dynamic equation and direct residue enumerations disagree")

    method_a_rigid = method_a_rigid_pairs(pow_q)
    method_b_rigid = method_b_rigid_pairs(pow_q)
    rigid_keys = ("b0", "b1", "r_q_mod_q")
    if normalized_records(method_a_rigid, rigid_keys) != normalized_records(method_b_rigid, rigid_keys):
        raise AssertionError("rigid equation and direct residue enumerations disagree")

    # Universal rowwise exclusion appears here as an exact finite check:
    # no shared dynamic residue has the same lower class modulo ord_67(5)=22.
    same_dynamic_lower = [
        record for record in method_a_dynamic if record["a0"] % W_P == record["a1"] % W_P
    ]

    rigid_same_lower = [
        record for record in method_a_rigid if record["b0"] % LOWER_Q == record["b1"] % LOWER_Q
    ]

    q2_counts = Counter()
    q2_exact_difference_count = 0
    for record in method_a_rigid:
        valid_count, excluded = q2_valid_lift_count(record, pow_q2)
        q2_counts[(valid_count, len(excluded))] += 1
        if (pow_q2[record["b0"]] - pow_q2[record["b1"]] - 2) % Q2 == 0:
            q2_exact_difference_count += 1

    joined, total_full_systems = pointwise_join(method_a_dynamic, method_a_rigid, pow_q2)
    independent_aligned, independent_common = independent_nested_join_count(
        method_a_dynamic, method_a_rigid
    )
    if independent_aligned != len(joined) or independent_common != sum(
        record["same_lower_assignment"] for record in joined
    ):
        raise AssertionError("hash-join and direct nested pointwise checks disagree")

    lower_pairs = [
        [record["lower_y0_mod_3410"], record["lower_y1_mod_3410"]] for record in joined
    ]

    # Repository positive pointwise example.
    repository_example = direct_system_record(
        "repository shared-residue pointwise example",
        r_p=2,
        r_q=13471,
        expected_y0=2728,
        expected_y1=1639,
        pow_p2=pow_p2,
        pow_q2=pow_q2,
    )
    if repository_example["all_lower_assignments"]["minimum_total_holes_over_common_lower_assignment"] != 67:
        raise AssertionError("repository example joint-hole minimum changed")

    # A sharper diagnostic: the rigid row has one common lower condition at
    # both anchors, so the remaining failure is isolated to dynamic-anchor
    # exclusion rather than an accidental rigid CRT mismatch.
    sharp_example = direct_system_record(
        "sharp two-row joint counterexample with common rigid lower condition",
        r_p=0,
        r_q=4494,
        expected_y0=2431,
        expected_y1=106,
        pow_p2=pow_p2,
        pow_q2=pow_q2,
    )
    if sharp_example["all_lower_assignments"]["minimum_total_holes_over_common_lower_assignment"] != 66:
        raise AssertionError("sharp p-1 joint deficit changed")

    # Verify and expose its logarithm/CRT core.
    dyn_lookup = {value: exponent for exponent, value in enumerate(pow_p2)}
    rigid_lookup = {value: exponent for exponent, value in enumerate(pow_q)}
    sharp_logs = {
        "dynamic_center_logs": {
            "anchor_0_mod_1474": dyn_lookup[(0 - 1) % P2],
            "anchor_1_mod_1474": dyn_lookup[(0 - 3) % P2],
        },
        "rigid_logs": {
            "anchor_0_mod_10385": rigid_lookup[(4494 - 1) % Q],
            "anchor_1_mod_10385": rigid_lookup[(4494 - 3) % Q],
        },
    }
    sharp_logs["dynamic_lower_classes_mod_22"] = {
        "anchor_0": sharp_logs["dynamic_center_logs"]["anchor_0_mod_1474"] % W_P,
        "anchor_1": sharp_logs["dynamic_center_logs"]["anchor_1_mod_1474"] % W_P,
    }
    sharp_logs["rigid_lower_classes_mod_155"] = {
        "anchor_0": sharp_logs["rigid_logs"]["anchor_0_mod_10385"] % LOWER_Q,
        "anchor_1": sharp_logs["rigid_logs"]["anchor_1_mod_10385"] % LOWER_Q,
    }
    sharp_logs["alignment_digits_mod_67"] = {
        "anchor_0": {
            "dynamic": sharp_logs["dynamic_center_logs"]["anchor_0_mod_1474"] % P,
            "rigid": sharp_logs["rigid_logs"]["anchor_0_mod_10385"] % P,
        },
        "anchor_1": {
            "dynamic": sharp_logs["dynamic_center_logs"]["anchor_1_mod_1474"] % P,
            "rigid": sharp_logs["rigid_logs"]["anchor_1_mod_10385"] % P,
        },
    }
    expected_sharp_logs = {
        "dynamic_center_logs": {"anchor_0_mod_1474": 737, "anchor_1_mod_1474": 788},
        "rigid_logs": {"anchor_0_mod_10385": 7236, "anchor_1_mod_10385": 9096},
        "dynamic_lower_classes_mod_22": {"anchor_0": 11, "anchor_1": 18},
        "rigid_lower_classes_mod_155": {"anchor_0": 106, "anchor_1": 106},
        "alignment_digits_mod_67": {
            "anchor_0": {"dynamic": 0, "rigid": 0},
            "anchor_1": {"dynamic": 51, "rigid": 51},
        },
    }
    if sharp_logs != expected_sharp_logs:
        raise AssertionError(f"sharp logarithm core changed: {sharp_logs}")
    sharp_example["logarithm_and_crt_core"] = sharp_logs
    sharp_example["record_sha256"] = sha256_record(
        {k: v for k, v in sharp_example.items() if k != "record_sha256"}
    )

    mod_p_compatibility = []
    lookup_p = {value: exponent for exponent, value in enumerate(pow_p)}
    for a0, value0 in enumerate(pow_p):
        a1 = lookup_p.get((value0 - 2) % P)
        if a1 is not None:
            mod_p_compatibility.append(
                {"r_p_mod_p": (1 + value0) % P, "anchor_0_log_mod_22": a0, "anchor_1_log_mod_22": a1}
            )
    mod_p_compatibility.sort(key=lambda record: record["r_p_mod_p"])

    joined_digest_payload = [
        [
            record["r_p_mod_p2"],
            record["r_q_mod_q"],
            record["a0"],
            record["a1"],
            record["b0"],
            record["b1"],
            record["lower_y0_mod_3410"],
            record["lower_y1_mod_3410"],
            record["valid_r_q_lifts_mod_q2"],
        ]
        for record in joined
    ]

    result: dict[str, Any] = {
        "schema": "a303656.c1-two-anchor-common-residue-phase-a.v1",
        "authority": AUTHORITY,
        "scope": {
            "universal_results": [
                "odd-row anchor exclusion",
                "joint common-fiber dynamic/rigid dichotomy",
                "rigid-frontier tax: at least p active rigid rows on the dynamic-inactive anchor",
                "Hall-type anchor-capacity deficit is a necessary condition",
            ],
            "finite_exact_domain": {
                "dynamic_prime": P,
                "rigid_prime": Q,
                "K_dynamic": 2,
                "K_rigid": 2,
                "accepted_valuations": [1],
                "lower_assignment_count": LOWER_MODULUS,
                "fiber_digit_count": P,
                "full_period": FULL_PERIOD,
            },
        },
        "method_agreement": {
            "dynamic_equation_vs_direct_residue": True,
            "rigid_equation_vs_direct_residue": True,
            "signature_join_vs_direct_nested_join": True,
        },
        "dynamic_common_residue_classification": {
            "pair_count_mod_67_squared": len(method_a_dynamic),
            "distinct_shared_r_67_count": len({record["r_p"] for record in method_a_dynamic}),
            "same_lower_class_mod_22_count": len(same_dynamic_lower),
            "mod_67_compatibility_classes": mod_p_compatibility,
            "records_sha256": sha256_record(normalized_records(method_a_dynamic, dyn_keys)),
        },
        "rigid_common_residue_classification": {
            "class_pair_count_mod_20771": len(method_a_rigid),
            "same_lower_class_mod_155_count": len(rigid_same_lower),
            "q2_exact_difference_pair_count": q2_exact_difference_count,
            "q2_valid_lift_distribution": [
                {
                    "valid_r_q_lifts": valid,
                    "excluded_local_zero_lifts": excluded,
                    "class_pair_count": count,
                }
                for (valid, excluded), count in sorted(q2_counts.items())
            ],
            "records_sha256": sha256_record(normalized_records(method_a_rigid, rigid_keys)),
        },
        "exhaustive_fixed_pair_pointwise_classification": {
            "aligned_dynamic_rigid_class_combinations": len(joined),
            "independent_nested_count": independent_aligned,
            "unique_ordered_lower_assignment_pairs": len({tuple(pair) for pair in lower_pairs}),
            "same_lower_assignment_combinations": sum(record["same_lower_assignment"] for record in joined),
            "independent_nested_same_lower_count": independent_common,
            "full_shared_residue_system_count_mod_p2_times_q2": total_full_systems,
            "joined_records_sha256": sha256_record(joined_digest_payload),
            "first_20_joined_records": joined[:20],
            "interpretation": (
                "Every counted system has an exact beta-one 66+1 fiber at each anchor on possibly different "
                "lower assignments. None has one common lower assignment."
            ),
        },
        "direct_repository_example": repository_example,
        "sharp_minimal_joint_counterexample": sharp_example,
        "theorem_checks": {
            "odd_row_anchor_exclusion_identity": "(r-1-5^d)-(r-3-5^d)=2; an odd p cannot divide both",
            "dynamic_both_active_same_lower_assignment_impossible": len(same_dynamic_lower) == 0,
            "rigid_frontier_tax_for_p_67": 67,
            "one_rigid_row_sharp_first_branch_deficit": 66,
            "sharp_example_attains_p_minus_1_deficit": (
                sharp_example["all_lower_assignments"]["minimum_total_holes_over_common_lower_assignment"]
                == P - 1
            ),
        },
        "logical_boundary": {
            "proved_global_principle": (
                "Direct same-lower dynamic gluing is universally impossible for odd rows with one shared residue; "
                "a common saturated p-fiber therefore forces a rigid-only frontier at at least one anchor."
            ),
            "not_proved": (
                "No universal incompatibility of arbitrary complete simultaneous certificates: separate lower branches, "
                "p or more rigid rows, other coordinates, and derived lower events remain possible."
            ),
            "missing_bridge": (
                "A theorem forcing every complete simultaneous certificate to expose one odd coordinate and one lower "
                "assignment whose two anchor fibers must be saturated simultaneously, together with an arithmetic "
                "bound excluding p compatible active rigid rows there."
            ),
        },
        "PASS": True,
    }

    # Frozen expected values: any change is a fail-closed regression.
    expected = {
        "dynamic_pairs": 603,
        "rigid_pairs": 5192,
        "rigid_same_lower": 33,
        "joined": 693,
        "unique_lower_pairs": 692,
        "same_lower": 0,
        "full_systems": 14_392_917,
    }
    observed = {
        "dynamic_pairs": result["dynamic_common_residue_classification"]["pair_count_mod_67_squared"],
        "rigid_pairs": result["rigid_common_residue_classification"]["class_pair_count_mod_20771"],
        "rigid_same_lower": result["rigid_common_residue_classification"]["same_lower_class_mod_155_count"],
        "joined": result["exhaustive_fixed_pair_pointwise_classification"]["aligned_dynamic_rigid_class_combinations"],
        "unique_lower_pairs": result["exhaustive_fixed_pair_pointwise_classification"]["unique_ordered_lower_assignment_pairs"],
        "same_lower": result["exhaustive_fixed_pair_pointwise_classification"]["same_lower_assignment_combinations"],
        "full_systems": result["exhaustive_fixed_pair_pointwise_classification"]["full_shared_residue_system_count_mod_p2_times_q2"],
    }
    if observed != expected:
        raise AssertionError(f"frozen exact classification changed: {observed} != {expected}")

    result["result_sha256"] = sha256_record(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    args = parser.parse_args()
    result = build_result()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "PASS": result["PASS"],
        "result_sha256": result["result_sha256"],
        "output": str(args.output),
        "dynamic_pairs": result["dynamic_common_residue_classification"]["pair_count_mod_67_squared"],
        "rigid_pairs": result["rigid_common_residue_classification"]["class_pair_count_mod_20771"],
        "pointwise_combinations": result["exhaustive_fixed_pair_pointwise_classification"]["aligned_dynamic_rigid_class_combinations"],
        "same_lower_combinations": result["exhaustive_fixed_pair_pointwise_classification"]["same_lower_assignment_combinations"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
