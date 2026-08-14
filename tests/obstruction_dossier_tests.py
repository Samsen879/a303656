#!/usr/bin/env python3
"""Small exact tests for both obstruction-dossier implementations."""
from __future__ import annotations

import importlib.util
import inspect
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


generator = load_module("obstruction_generator_under_test", "src/generate_obstruction_dossier.py")
verifier = load_module("obstruction_verifier_under_test", "src/verify_obstruction_dossier.py")


class ObstructionDossierTests(unittest.TestCase):
    def test_independent_verifier_does_not_import_generator(self) -> None:
        source = inspect.getsource(verifier)
        self.assertNotIn("import generate_obstruction_dossier", source)
        self.assertNotIn("from generate_obstruction_dossier", source)

    def test_active_domain_and_duplicate_shift(self) -> None:
        for n in (2, 3, 5, 25, 29, 240000005594):
            self.assertEqual(generator.active_pairs(n), verifier.independent_active_pairs(n))
        duplicate = [(c, d) for c, d, shift in generator.active_pairs(29) if shift == 28]
        self.assertEqual(duplicate, [(1, 2), (3, 0)])

    def test_complete_factorization_and_classification_examples(self) -> None:
        gp = generator.eratosthenes(1000)
        vp = verifier.odd_only_prime_table(1000)
        cases = {
            1: [],
            21: [(3, 1), (7, 1)],
            45: [(3, 2), (5, 1)],
            240: [(2, 4), (3, 1), (5, 1)],
            99991: [(99991, 1)],
        }
        for value, expected in cases.items():
            self.assertEqual(generator.complete_factorization(value, gp), expected)
            self.assertEqual(verifier.verifier_factor(value, vp), expected)
        self.assertEqual([p for p, e in cases[21] if p % 4 == 3 and e % 2], [3, 7])
        self.assertEqual([p for p, e in cases[45] if p % 4 == 3 and e % 2], [])

    def test_deterministic_primality_paths(self) -> None:
        values = (2, 3, 5, 97, 99991, 240000005593, 2305843009213693951)
        for value in values:
            if value < 341550071728321:
                self.assertEqual(generator.deterministic_prime_uint64(value), verifier.verifier_prime_test(value))
        for composite in (0, 1, 4, 21, 341550071728319):
            self.assertFalse(generator.deterministic_prime_uint64(composite))
            self.assertFalse(verifier.verifier_prime_test(composite))

    def test_canonical_witnesses(self) -> None:
        expected = {0: (0, 0), 1: (0, 1), 2: (1, 1), 25: (0, 5), 50: (1, 7), 65: (1, 8)}
        for remainder, witness in expected.items():
            self.assertEqual(generator.canonical_two_square_witness(remainder), witness)
            self.assertEqual(verifier.independent_canonical_witness(remainder), witness)
        self.assertIsNone(generator.canonical_two_square_witness(3))
        self.assertIsNone(verifier.independent_canonical_witness(3))

    def test_schema_regression_panel_is_separate_and_has_zero_paths(self) -> None:
        primes = generator.eratosthenes(math.isqrt(25))
        expected_active = {2: 1, 3: 1, 5: 2, 25: 6}
        for n in (2, 3, 5, 25):
            rows = generator.build_records_for_n(n, primes, "SCHEMA_REGRESSION_ONLY")
            self.assertEqual(len(rows), expected_active[n])
            self.assertEqual(sum(row["status"] == "WINNER" for row in rows), 1)
            self.assertTrue(all(row["purpose"] == "SCHEMA_REGRESSION_ONLY" for row in rows))
        zero_rows = [
            row
            for n in (2, 3, 5, 25)
            for row in generator.build_records_for_n(n, primes, "SCHEMA_REGRESSION_ONLY")
            if row["remainder"] == 0
        ]
        self.assertGreaterEqual(len(zero_rows), 1)
        self.assertTrue(all(row["status"] == "WINNER" and row["canonical_a"] == row["canonical_b"] == 0 for row in zero_rows))

    def test_fixed_control_selection(self) -> None:
        counts, _ = generator.load_validated_counts(ROOT / "output/tn_pilot_20260713")
        primary = generator.select_controls(counts)
        independent = verifier.independent_control_selection(counts)
        self.assertEqual(primary, independent)
        self.assertEqual(
            [(row["control_n"], row["control_T"]) for row in primary],
            [
                (240000002114, 50),
                (240000003122, 53),
                (240000048838, 55),
                (240000000728, 58),
                (240000003584, 53),
            ],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
