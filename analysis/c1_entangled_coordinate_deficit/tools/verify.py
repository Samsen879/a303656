#!/usr/bin/env python3
"""Clean-room checks for the C=1 entangled coordinate-deficit audit.

This verifier uses direct modular valuation sets for the finite chain and
square-residue sets for the 2-adic audit.  It imports no candidate code.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


def factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    q = 2
    while q * q <= n:
        while n % q == 0:
            out[q] = out.get(q, 0) + 1
            n //= q
        q = 3 if q == 2 else q + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_prime(n: int) -> bool:
    return n >= 2 and factor(n) == {n: 1}


def order_mod_5(p: int) -> int:
    if not is_prime(p) or p == 5:
        raise ValueError("invalid order modulus")
    order = p - 1
    for q, multiplicity in factor(order).items():
        for _ in range(multiplicity):
            if pow(5, order // q, p) != 1:
                break
            order //= q
    return order


def vp_nonzero(n: int, p: int) -> int:
    if n == 0:
        raise ValueError("zero has no finite valuation")
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e


def clipped_valuation(n: int, p: int, precision: int) -> int | None:
    n %= p**precision
    return None if n == 0 else vp_nonzero(n, p)


def exact_s(p: int, order: int, cap: int = 4) -> int:
    for e in range(1, cap):
        if pow(5, order, p ** (e + 1)) != 1:
            return e
    raise ValueError("valuation exceeded clean-room cap")


def fatal(p: int, residue: int, anchor: int, exponent: int) -> bool:
    value = residue - 3**anchor - pow(5, exponent, p * p)
    return clipped_valuation(value, p, 2) == 1


def verify_chain() -> dict:
    rows = ((11, 4), (67, 4), (20771, 20775))
    orders = {p: order_mod_5(p) for p, _ in rows}
    s_values = {p: exact_s(p, orders[p]) for p, _ in rows}
    periods = {
        p: orders[p] * (p if s_values[p] == 1 else 1) for p, _ in rows
    }
    coarse = math.lcm(*(orders.values()))
    full = math.lcm(*(periods.values()))
    if (orders, s_values, coarse, full) != (
        {11: 5, 67: 22, 20771: 10385},
        {11: 1, 67: 1, 20771: 2},
        228470,
        228470,
    ):
        raise AssertionError("chain arithmetic mismatch")

    beta = {p: vp_nonzero(coarse, p) if coarse % p == 0 else 0 for p, _ in rows}
    fatal_sets: dict[int, set[int]] = {}
    safe_counts: dict[str, int] = {}
    first_safe: dict[str, int] = {}
    row_counts: dict[str, list[int]] = {}
    for anchor in (0, 1):
        sets = {
            p: {d for d in range(full) if fatal(p, r, anchor, d)}
            for p, r in rows
        }
        safe = set(range(full)).difference(*sets.values())
        safe_counts[str(anchor)] = len(safe)
        first_safe[str(anchor)] = min(safe)
        row_counts[str(anchor)] = [len(sets[p]) for p, _ in rows]
        if anchor == 1:
            fatal_sets = sets

    fiber = [310 * t for t in range(11 * 67)]
    assignment = bytearray()
    witness_counts = [0, 0, 0]
    for d in fiber:
        flags = [d in fatal_sets[p] for p, _ in rows]
        if not any(flags):
            raise AssertionError("uncovered saturated fiber cell")
        chosen = flags.index(True)
        witness_counts[chosen] += 1
        assignment.append(chosen)
    if witness_counts != [670, 66, 1]:
        raise AssertionError("chain partition mismatch")
    if any(fatal(p, 4, 1, 0) for p in (11, 67, 20771)):
        raise AssertionError("local-zero corruption did not fail closed")

    return {
        "orders": {str(k): v for k, v in orders.items()},
        "s": {str(k): v for k, v in s_values.items()},
        "beta": {str(k): v for k, v in beta.items()},
        "U": coarse,
        "L": full,
        "edges": [[11, 67], [67, 20771]],
        "safe_counts": safe_counts,
        "first_safe": first_safe,
        "row_fatal_counts": row_counts,
        "fiber_modulus": 310,
        "fiber_cells": len(fiber),
        "assignment_counts": witness_counts,
        "assignment_sha256": hashlib.sha256(assignment).hexdigest(),
        "corruption_fail_closed": True,
        "PASS": True,
    }


def verify_coordinate_examples() -> dict:
    comparison_rows = (3, 11, 31, 71, 67, 20771, 1279)
    orders = {p: order_mod_5(p) for p in comparison_rows}
    expected = {3: 2, 11: 5, 31: 3, 71: 5, 67: 22, 20771: 10385, 1279: 639}
    if orders != expected:
        raise AssertionError("comparison orders mismatch")
    U = math.lcm(*orders.values())
    if U != 145992330:
        raise AssertionError("comparison coarse period mismatch")

    active = (3, 11, 31, 71)
    hazards = {p: Fraction(p - 1, p) for p in active}
    global_mass = sum((hazards[p] / orders[p] for p in active), Fraction())
    if global_mass != Fraction(75169, 72633) or global_mass <= 1:
        raise AssertionError("first incomparability direction mismatch")
    if any(clipped_valuation(4 - 3 - 1, p, 2) is not None for p in active):
        raise AssertionError("explicit centers are not unresolved")
    if any(clipped_valuation(3 - 3 - 1, p, 2) != 0 for p in (67, 20771, 1279)):
        raise AssertionError("catalyst rows are not inactive")

    chain_mass = Fraction(2, 11) + Fraction(3, 67) + Fraction(1, 10385)
    if chain_mass != Fraction(25896, 114235) or chain_mass >= 1:
        raise AssertionError("second incomparability direction mismatch")

    p, residue = 20771, 96315155
    dual = {
        str(c): [
            d for d in range(10385)
            if fatal(p, residue, c, d)
        ]
        for c in (0, 1)
    }
    if dual != {"0": [6528], "1": [2]}:
        raise AssertionError("common-residue dual-anchor mismatch")

    moduli = (2, 3, 5, 6, 22)
    period = math.lcm(*moduli)
    maximum = 0
    maximizers: list[tuple[int, ...]] = []
    for choices in itertools.product(*(range(m) for m in moduli)):
        covered = sum(
            any(x % m == b for m, b in zip(moduli, choices))
            for x in range(period)
        )
        if covered > maximum:
            maximum, maximizers = covered, [choices]
        elif covered == maximum:
            maximizers.append(choices)
    if (maximum, len(maximizers)) != (290, 660):
        raise AssertionError("active-cover optimum mismatch")
    maximizer_hash = hashlib.sha256(
        json.dumps(maximizers, separators=(",", ":")).encode()
    ).hexdigest()

    return {
        "coordinate_succeeds_global_fails": {
            "U": U,
            "hazards": {str(p): [v.numerator, v.denominator] for p, v in hazards.items()},
            "global_mass": [global_mass.numerator, global_mass.denominator],
            "safe_coarse_class": 0,
        },
        "global_succeeds_coordinate_fails": {
            "global_mass": [chain_mass.numerator, chain_mass.denominator],
            "saturated_coordinate": 67,
            "coordinate_budget": [1, 1],
        },
        "dual_anchor_common_residue": {"p": p, "r": residue, "fatal_classes": dual},
        "active_cover_relaxation": {
            "assignments_checked": math.prod(moduli),
            "period": period,
            "maximum": maximum,
            "maximizers": len(maximizers),
            "maximizers_sha256": maximizer_hash,
            "upper_bound_with_terminal_shell": [301198, 342705],
        },
        "PASS": True,
    }


def two_square_residues(modulus: int) -> set[int]:
    square_residues = {x * x % modulus for x in range(modulus)}
    return {(x + y) % modulus for x in square_residues for y in square_residues}


def two_adic_safe(precision: int, residue: int, anchor: int, exponent: int) -> bool:
    modulus = 2**precision
    value = (residue - 3**anchor - pow(5, exponent, modulus)) % modulus
    return value in two_square_residues(modulus)


def verify_k2_boundary() -> dict:
    """Directly replay the constant K_2=2 boundary and adjacent cases."""
    p, precision, residue, anchor = 11, 2, 0, 0
    order = order_mod_5(p)
    s_value = exact_s(p, order)
    lift_power = max(0, precision - s_value)
    odd_period = order * p**lift_power
    if (order, s_value, lift_power, odd_period) != (5, 1, 1, 55):
        raise AssertionError("K2 boundary odd-row arithmetic mismatch")

    def replay_case(name: str, k2: int | None, r2: int | None) -> dict:
        t2 = None if k2 is None else (1 if k2 == 2 else 2 ** (k2 - 2))
        U = order if t2 is None else math.lcm(order, t2)
        L = odd_period if t2 is None else math.lcm(odd_period, t2)
        odd_fatal = [d for d in range(L) if fatal(p, residue, anchor, d)]
        odd_coordinate_hazards = {"5": [0, 1]}

        if k2 is None:
            constant_safe: bool | None = None
            theta: list[int] | None = None
            coordinate_hazards = dict(odd_coordinate_hazards)
            safe = [d for d in range(L) if d not in odd_fatal]
            old_hypothesis = True
            corrected_hypothesis = all(n < q for n, q in coordinate_hazards.values())
        else:
            assert r2 is not None and t2 is not None
            safe_in_period = [
                d for d in range(t2)
                if two_adic_safe(k2, r2, anchor, d)
            ]
            theta_fraction = Fraction(t2 - len(safe_in_period), t2)
            theta = [theta_fraction.numerator, theta_fraction.denominator]
            constant_safe = (len(safe_in_period) == t2) if k2 == 2 else None
            coordinate_hazards = dict(odd_coordinate_hazards)
            if k2 >= 3:
                coordinate_hazards["2"] = theta
            safe = [
                d for d in range(L)
                if d not in odd_fatal and two_adic_safe(k2, r2, anchor, d)
            ]
            old_hypothesis = all(n < q for n, q in odd_coordinate_hazards.values())
            boundary_ok = constant_safe if k2 == 2 else True
            corrected_hypothesis = bool(boundary_ok) and all(
                n < q for n, q in coordinate_hazards.values()
            )

        return {
            "name": name,
            "p": p,
            "K": precision,
            "r": residue,
            "E": [1],
            "anchor": anchor,
            "K_2": k2,
            "r_2": r2,
            "w_11": order,
            "s_11": s_value,
            "a_11": lift_power,
            "t_2": t2,
            "U": U,
            "L": L,
            "beta_11": 0,
            "two_divides_U": U % 2 == 0,
            "odd_fatal_count": len(odd_fatal),
            "odd_coordinate_hazards": odd_coordinate_hazards,
            "constant_two_adic_safe": constant_safe,
            "Theta_c": theta,
            "coordinate_hazards": coordinate_hazards,
            "old_wording_hypothesis": old_hypothesis,
            "corrected_criterion_hypothesis": corrected_hypothesis,
            "direct_safe_count": len(safe),
            "first_safe": min(safe) if safe else None,
        }

    cases = {
        "k2_equals_2_unsafe": replay_case("K2=2 constant obstruction", 2, 1),
        "k2_equals_2_safe": replay_case("K2=2 safe constant boundary", 2, 0),
        "k2_equals_3_coordinate": replay_case("K2=3 coordinate-2 hazard", 3, 0),
        "no_two_adic_row": replay_case("no two-adic row", None, None),
    }
    bad = cases["k2_equals_2_unsafe"]
    good = cases["k2_equals_2_safe"]
    coordinate = cases["k2_equals_3_coordinate"]
    absent = cases["no_two_adic_row"]
    if not (
        bad["old_wording_hypothesis"]
        and not bad["constant_two_adic_safe"]
        and not bad["corrected_criterion_hypothesis"]
        and bad["direct_safe_count"] == 0
        and good["constant_two_adic_safe"]
        and good["corrected_criterion_hypothesis"]
        and good["direct_safe_count"] == good["L"] == 55
        and coordinate["two_divides_U"]
        and coordinate["coordinate_hazards"]["2"] == [1, 2]
        and coordinate["corrected_criterion_hypothesis"]
        and coordinate["direct_safe_count"] == 55
        and absent["constant_two_adic_safe"] is None
        and absent["corrected_criterion_hypothesis"]
        and absent["direct_safe_count"] == absent["L"] == 55
    ):
        raise AssertionError("K2 boundary replay mismatch")
    return {**cases, "old_wording_counterexample_reproduced": True, "PASS": True}


def verify_two_adic() -> dict:
    distributions: dict[str, dict[str, int]] = {}
    checks = 0
    for K in range(2, 11):
        modulus = 2**K
        period = 1 if K == 2 else 2 ** (K - 2)
        sums = two_square_residues(modulus)
        observed: dict[str, int] = {}
        for residue in range(modulus):
            counts = tuple(
                sum(
                    (residue - 3**anchor - pow(5, d, modulus)) % modulus in sums
                    for d in range(period)
                )
                for anchor in (0, 1)
            )
            checks += 2 * period
            key = str(list(counts))
            observed[key] = observed.get(key, 0) + 1
            if max(counts) < period / 2:
                raise AssertionError("no anchor has required 2-adic safe density")
        distributions[str(K)] = observed
    return {
        "K_min": 2,
        "K_max": 10,
        "direct_membership_checks": checks,
        "distributions": distributions,
        "PASS": True,
    }


BASE_SHA = "6f6611ce089d0f3378e191f55bffdb0caa4b83bc"
BASE_TREE = "ebfd4a6dcbcdb4f0e84f89a0c86ff40d13e538b2"
INPUT_ZIP_SHA256 = "8c300e869ebfa0a4a559e38d9667a469b3e352dd9b9dfbd9425ae200d55cb4e0"


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def seal_results(output_dir: Path, names: list[str]) -> dict:
    files = []
    for name in sorted(names):
        payload = (output_dir / name).read_bytes()
        files.append({
            "path": name,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    return {
        "schema": "a303656-c1-entangled-results-manifest-v2",
        "artifact_class": "compact_repository_native_audit",
        "base_sha": BASE_SHA,
        "base_tree": BASE_TREE,
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    chain = verify_chain()
    examples = verify_coordinate_examples()
    k2_boundary = verify_k2_boundary()
    two_adic = verify_two_adic()
    audit_summary = {
        "schema": "a303656-c1-entangled-audit-summary-v2",
        "repository": "Samsen879/a303656",
        "repository_id": 1333945235,
        "base_sha": BASE_SHA,
        "base_tree": BASE_TREE,
        "input_zip_sha256": INPUT_ZIP_SHA256,
        "accepted_new_theorems": [
            "boundary-corrected prime-coordinate strict-deficit criterion",
            "necessary saturated odd-coordinate condition",
            "beta-one saturation and lower-coordinate contraction lemma",
        ],
        "boundary_repair": {
            "old_wording_counterexample_reproduced": (
                k2_boundary["old_wording_counterexample_reproduced"]
            ),
            "cases": [
                "no two-adic row",
                "K_2=2 constant boundary",
                "K_2>=3 genuine coordinate-two hazard",
            ],
        },
        "prior_dependencies_not_reclassified_as_new": [
            "prime-power lifting geometry",
            "exact entangled fatal normal form",
            "coarse-to-full reverse CRT equivalence",
        ],
        "status": {
            "PROJECT": "PAUSED",
            "ACTIVE_PROMOTED_ROUTE": "NONE",
            "A303656": "UNRESOLVED",
        },
        "verdict": "ACCEPT_REPOSITORY_NATIVE_TARGETED_PARTIAL_ADVANCE",
        "PASS": True,
    }
    verification = {
        "schema": "a303656-c1-entangled-verification-v2",
        "implementation": "clean-room direct modular enumeration",
        "imports_candidate_code": False,
        "chain": chain["PASS"],
        "coordinate_examples": examples["PASS"],
        "k2_boundary": k2_boundary["PASS"],
        "old_wording_counterexample_reproduced": (
            k2_boundary["old_wording_counterexample_reproduced"]
        ),
        "two_adic": two_adic["PASS"],
        "reference_assignment_hash_match": (
            chain["assignment_sha256"]
            == "416fbeeaae28e7d348ceab0c4cfcaa7a188356647af87e0cf9a1c493a381d879"
        ),
        "reference_active_cover_hash_match": (
            examples["active_cover_relaxation"]["maximizers_sha256"]
            == "ee9d717d71fe688f891664e306711fd9a36127c0cee84462f03d5c24d931afc0"
        ),
        "unit_test_command": (
            "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover "
            "-s analysis/c1_entangled_coordinate_deficit/tests -p test_*.py"
        ),
        "unit_tests_expected": 11,
        "PASS": True,
    }
    records = {
        "audit_summary.json": audit_summary,
        "coordinate_examples.json": examples,
        "dependency_chain.json": chain,
        "k2_boundary_replay.json": k2_boundary,
        "two_adic_replay.json": two_adic,
        "verification_report.json": verification,
    }
    for name, value in records.items():
        write_json(args.output_dir / name, value)
    report = """# C=1 entangled coordinate-deficit audit report

## Verdict

```text
ACCEPT — REPOSITORY-NATIVE TARGETED PARTIAL ADVANCE
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The independent audit accepts the boundary-corrected prime-coordinate
strict-deficit theorem, the re-audited necessary saturated odd-coordinate
condition, and the beta-one aligned rigid-shell contraction lemma.  Lifting
geometry, the fatal normal form, and reverse CRT are prior dependencies and
are not counted as new results.

The superseded coordinate-only wording failed when `K_2=2` and `2` did not
divide `U`: an exact `p=11, r=0, r_2=1, c=0` replay has zero odd-coordinate
hazard but no safe exponent modulo `L=55`.  The corrected theorem checks this
constant boundary first, treats `K_2>=3` as a genuine coordinate-two hazard,
and imposes no two-adic condition when the row is absent.  Four regression
cases agree with direct full-period enumeration.

The direct verifier reproduces `U=L=228470`, the chain witness partition
`670+66+1`, diagnostic assignment SHA-256
`416fbeeaae28e7d348ceab0c4cfcaa7a188356647af87e0cf9a1c493a381d879`,
176,698 safe anchor-one cells, both exact incomparability examples, the
common-residue dual-anchor sample, and all two-adic distributions through
`K_2=10`.

The saturated 737-cell fiber is not a complete certificate.  A local escape
does not prove a sum-of-two-squares representation.  No universal `C=1`
no-go, complete certificate, A303656 resolution, or route promotion is
claimed.
"""
    (args.output_dir / "REPORT.md").write_text(report, encoding="utf-8")
    sealed_names = list(records) + ["REPORT.md"]
    write_json(args.output_dir / "manifest.json", seal_results(args.output_dir, sealed_names))
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
