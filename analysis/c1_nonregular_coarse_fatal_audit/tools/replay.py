#!/usr/bin/env python3
"""Generate deterministic compact evidence for issue #4."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from model import (  # noqa: E402
    LocalSystem, factor, is_prime, order_mod_prime, two_square_mod_2k,
    valuation_below,
)

BASE_SHA = "9ae583fcaa7b0a46ed638d7ab25423b55e1a8f8d"
BASE_TREE = "86f5b202972981ab2d028c6613fa74f7f07eaa68"
EXPECTED_ENTANGLED_HASH = "bf6d55c505b3ba4b388b2407149e68caf6e07eda17263fdf4e96406124dc0906"
KNOWN = (
    (20771, 10385, 5192, 2176, 179336818),
    (40487, 40486, 40485, 33704, 972740666),
    (1645333507, 1645333506, 1645333505, 85648253, 596221528337137121),
)


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def boundary_replay() -> dict:
    rows = []
    orders = []
    for p, expected_w, expected_count, b0, residue in KNOWN:
        if not is_prime(p):
            raise AssertionError(f"composite boundary prime {p}")
        factors = factor(p - 1)
        if any(not is_prime(q) for q in factors):
            raise AssertionError("factorization contains a composite factor")
        w = order_mod_prime(5, p)
        if w != expected_w:
            raise AssertionError((p, w, expected_w))
        if pow(5, w, p * p) != 1 or pow(5, w, p * p * p) == 1:
            raise AssertionError(f"s is not exactly two for {p}")
        if any(pow(5, w // q, p) == 1 for q in factor(w)):
            raise AssertionError("order prime-divisor certificate failed")
        modulus = p * p
        if valuation_below(residue - 1 - pow(5, b0, modulus), p, 2) != 1:
            raise AssertionError("c=0 anchor sample failed")
        if valuation_below(residue - 3 - 1, p, 2) != 1:
            raise AssertionError("c=1 anchor sample failed")
        if w == p - 1:
            compatible_count = p - 2
        else:
            subgroup = {pow(5, exponent, p) for exponent in range(w)}
            compatible_count = sum(1 for y in subgroup if (y + 2) % p in subgroup)
        if compatible_count != expected_count:
            raise AssertionError("anchor compatibility count failed")
        rows.append({
            "p": p,
            "p_minus_1_factorization": factors,
            "w": w,
            "s": 2,
            "ord_p2": w,
            "ord_p3": w * p,
            "anchor_pair_count": compatible_count,
            "anchor_sample": {"b_c0": b0, "b_c1": 0, "r_mod_p2": residue},
        })
        orders.append(w)
    U = math.lcm(*orders)
    mass = sum((Fraction(1, order) for order in orders), Fraction())
    if U != 11157672864255930:
        raise AssertionError("known-panel U changed")
    if mass != Fraction(675001461539, 5578836432127965):
        raise AssertionError("known-panel shell mass changed")
    if any(math.gcd(p, U) != 1 for p, *_ in KNOWN) or mass >= Fraction(1, 2):
        raise AssertionError("known panel is not order-decoupled shell-sparse")
    return {
        "schema": "a303656-c1-boundary-replay-v2",
        "rows": rows,
        "coarse_period_U": U,
        "gcds": {str(p): math.gcd(p, U) for p, *_ in KNOWN},
        "shell_mass": [mass.numerator, mass.denominator],
        "PASS": True,
    }


def entangled_replay() -> dict:
    rng = random.Random(30365619)
    records = []
    total_checks = 0
    for _ in range(120):
        e3 = list(rng.choice(((1,), (3,), (1, 3))))
        obj = {
            "C": 1,
            "two_adic": {"K": 3, "r": rng.randrange(8)},
            "primes": [
                {"p": 3, "K": 4, "r": rng.randrange(81), "odd_valuations": e3},
                {"p": 7, "K": 2, "r": rng.randrange(49), "odd_valuations": [1]},
                {"p": 19, "K": 2, "r": rng.randrange(361), "odd_valuations": [1]},
            ],
        }
        audit = LocalSystem.build(obj).audit()
        if (audit["U"], audit["L"]) != (18, 7182):
            raise AssertionError("entangled test period changed")
        total_checks += audit["closed_formula_checks"]
        records.append([
            obj["two_adic"]["r"],
            obj["primes"][0]["r"], obj["primes"][1]["r"], obj["primes"][2]["r"],
            e3, audit["full_safe_count"], audit["projected_safe_count"],
            audit["complete_certificate"],
        ])
    digest = hashlib.sha256(
        json.dumps(records, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if digest != EXPECTED_ENTANGLED_HASH:
        raise AssertionError("entangled replay record hash changed")
    return {
        "schema": "a303656-c1-entangled-replay-v1",
        "systems": len(records),
        "U": 18,
        "L": 7182,
        "beta_3": 2,
        "a_3": 3,
        "closed_formula_checks": total_checks,
        "records_sha256": digest,
        "expected_records_sha256": EXPECTED_ENTANGLED_HASH,
        "complete_certificate_count": sum(1 for row in records if row[-1]),
        "PASS": True,
    }


def two_adic_replay() -> dict:
    checked = 0
    for K in range(2, 13):
        modulus = 2**K
        squares = {x * x % modulus for x in range(modulus)}
        direct = {(x + y) % modulus for x in squares for y in squares}
        formula = {x for x in range(modulus) if two_square_mod_2k(x, K)}
        if direct != formula:
            raise AssertionError(f"two-adic characterization failed at K={K}")
        checked += modulus
    return {
        "schema": "a303656-c1-two-adic-replay-v1",
        "K_min": 2,
        "K_max": 12,
        "residues_checked": checked,
        "PASS": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    boundary = boundary_replay()
    entangled = entangled_replay()
    two_adic = two_adic_replay()
    write_json(args.output_dir / "boundary_replay.json", boundary)
    write_json(args.output_dir / "entangled_replay.json", entangled)
    write_json(args.output_dir / "two_adic_replay.json", two_adic)
    summary = {
        "schema": "a303656-c1-coarse-fatal-audit-summary-v1",
        "repository": "Samsen879/a303656",
        "repository_id": 1333945235,
        "base_sha": BASE_SHA,
        "base_tree": BASE_TREE,
        "source_commit": args.source_commit,
        "checks": {
            "boundary_replay": boundary["PASS"],
            "entangled_closed_formula": entangled["PASS"],
            "two_adic_characterization": two_adic["PASS"],
        },
        "custody": {
            "external_directory_internal_sha256s": "PASS_AT_INTAKE",
            "external_sha256s_file":
                "90abe6a18b28c27f124d0e16fd0d057b87aa9f95b0fedcb6dc80867ed5c0cb73",
            "outer_zip_sha256": "NOT_VERIFIED_NOT_SUPPLIED",
        },
        "status": {
            "PROJECT": "PAUSED",
            "ACTIVE_PROMOTED_ROUTE": "NONE",
            "A303656": "UNRESOLVED",
        },
        "verdict": "PASS_BOUNDED_NEGATIVE_STRUCTURAL_THEOREM_AUDIT",
    }
    write_json(args.output_dir / "audit_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
