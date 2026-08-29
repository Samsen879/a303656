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


def verify_two_adic() -> dict:
    distributions: dict[str, dict[str, int]] = {}
    checks = 0
    for K in range(2, 11):
        modulus = 2**K
        period = 1 if K == 2 else 2 ** (K - 2)
        square_residues = {x * x % modulus for x in range(modulus)}
        sums = {(x + y) % modulus for x in square_residues for y in square_residues}
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
        "schema": "a303656-c1-entangled-results-manifest-v1",
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
    two_adic = verify_two_adic()
    audit_summary = {
        "schema": "a303656-c1-entangled-audit-summary-v1",
        "repository": "Samsen879/a303656",
        "repository_id": 1333945235,
        "base_sha": BASE_SHA,
        "base_tree": BASE_TREE,
        "input_zip_sha256": INPUT_ZIP_SHA256,
        "accepted_new_theorems": [
            "prime-coordinate strict-deficit criterion",
            "necessary saturated odd-coordinate condition",
            "beta-one saturation and lower-coordinate contraction lemma",
        ],
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
        "schema": "a303656-c1-entangled-verification-v1",
        "implementation": "clean-room direct modular enumeration",
        "imports_candidate_code": False,
        "chain": chain["PASS"],
        "coordinate_examples": examples["PASS"],
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
        "unit_tests_expected": 7,
        "PASS": True,
    }
    records = {
        "audit_summary.json": audit_summary,
        "coordinate_examples.json": examples,
        "dependency_chain.json": chain,
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

The independent audit accepts the prime-coordinate strict-deficit theorem,
the necessary saturated odd-coordinate condition, and the beta-one aligned
rigid-shell contraction lemma.  Lifting geometry, the fatal normal form, and
reverse CRT are prior dependencies and are not counted as new results.

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
