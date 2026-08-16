from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("periodic_verifier", ROOT / "tools" / "periodic_verifier.py")
periodic = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(periodic)


def rejected(obj) -> bool:
    try:
        return not periodic.verify_certificate(obj)["PASS"]
    except (periodic.CertificateError, KeyError, TypeError, ValueError):
        return True


def cases():
    valid = {"C": 0, "two_adic": {"K": 2, "r": 1}, "primes": []}
    prime = {"C": 0, "primes": [{"p": 3, "K": 2, "r": 0, "odd_valuations": [1]}]}
    rows = []
    rows.append(("negative_C", {**valid, "C": -1}))
    rows.append(("unknown_top_field", {**valid, "note": "ignored?"}))
    x = copy.deepcopy(valid); x["two_adic"]["K"] = 1; rows.append(("two_adic_low_precision", x))
    x = copy.deepcopy(valid); x["two_adic"]["r"] = 0; rows.append(("destroy_complete_cover", x))
    x = copy.deepcopy(prime); x["primes"][0]["p"] = 9; rows.append(("composite_prime", x))
    x = copy.deepcopy(prime); x["primes"][0]["p"] = 13; rows.append(("wrong_prime_class", x))
    x = copy.deepcopy(prime); x["primes"][0]["p"] = 5; rows.append(("base_five_prime", x))
    x = copy.deepcopy(prime); x["primes"].append(copy.deepcopy(x["primes"][0])); rows.append(("duplicate_prime", x))
    x = copy.deepcopy(prime); x["primes"][0]["K"] = 1; rows.append(("odd_prime_low_precision", x))
    x = copy.deepcopy(prime); x["primes"][0]["odd_valuations"] = [2]; rows.append(("even_valuation", x))
    x = copy.deepcopy(prime); x["primes"][0]["odd_valuations"] = [3]; rows.append(("valuation_above_precision", x))
    x = copy.deepcopy(prime); x["primes"][0]["odd_valuations"] = [1, 1]; rows.append(("duplicate_valuation", x))
    x = copy.deepcopy(prime); x["primes"][0]["r"] = 2; rows.append(("zero_at_precision_unresolved", x))
    rows.append(("empty_certificate_incomplete", {"C": 0, "primes": []}))
    return valid, rows


class CorruptionTests(unittest.TestCase):
    def test_named_corruptions(self):
        valid, rows = cases()
        self.assertTrue(periodic.verify_certificate(valid)["PASS"])
        for name, obj in rows:
            with self.subTest(name=name):
                self.assertTrue(rejected(obj))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    valid, rows = cases()
    results = [{"name": name, "rejected": rejected(obj)} for name, obj in rows]
    report = {
        "schema": "a303656-one-sided-strip-corruption-tests-v1",
        "valid_control_passed": periodic.verify_certificate(valid)["PASS"],
        "test_count": len(results),
        "all_rejected": all(row["rejected"] for row in results),
        "tests": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["valid_control_passed"] and report["all_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
