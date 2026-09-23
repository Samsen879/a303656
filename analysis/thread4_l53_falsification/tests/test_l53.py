#!/usr/bin/env python3
"""Regression tests for the L5,3 falsification certificate."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("criterion_checker", ROOT / "tools" / "criterion_checker.py")
CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECKER)


class L53Regression(unittest.TestCase):
    def test_sum_two_squares_criterion(self):
        self.assertTrue(CHECKER.sum2_criterion(0)[0])
        self.assertTrue(CHECKER.sum2_criterion(65)[0])
        self.assertFalse(CHECKER.sum2_criterion(3)[0])
        self.assertFalse(CHECKER.sum2_criterion(21)[0])

    def test_first_failure_supports(self):
        source = CHECKER.d_table(7_963_079)["D"]
        target = CHECKER.d_table(39_815_398)["D"]
        self.assertEqual(source, [0, 1, 2, 4, 6, 7, 8, 9])
        self.assertEqual(target, [0, 4, 6])
        self.assertFalse(set(d + 1 for d in source) & set(target))

    def test_second_failure_supports(self):
        source = CHECKER.d_table(8_984_426)["D"]
        target = CHECKER.d_table(44_922_133)["D"]
        self.assertEqual(source, [1, 4, 5, 7, 9])
        self.assertEqual(target, [0, 1, 3, 7, 9])
        self.assertFalse(set(d + 1 for d in source) & set(target))

    def test_committed_certificate(self):
        certificate = json.loads((ROOT / "results" / "l53_falsification_certificate.json").read_text())
        self.assertEqual(certificate["status"], "FALSE")
        self.assertEqual(certificate["first_failure"]["m"], 7_963_079)
        self.assertTrue(certificate["independent_checker_pass"])


if __name__ == "__main__":
    unittest.main()
