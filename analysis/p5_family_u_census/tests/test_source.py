#!/usr/bin/env python3
"""Evaluator-free unit tests required before SOURCE COMMIT S."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "analysis/p5_family_u_census/tools"))

from common import CensusError, deduplicate, exact_summary, parse_mask_hex, reconstruct_panel, validate_descriptions  # noqa: E402
from deduplicator import build as build_incidence  # noqa: E402


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = reconstruct_panel(ROOT)

    def test_exact_frozen_authority(self):
        self.assertEqual(self.panel["description_count"], 457)
        self.assertEqual(self.panel["distinct_integer_count"], 454)
        self.assertTrue(all(d["description_id"].startswith("U-") for d in self.panel["descriptions"]))

    def test_crt_and_masks(self):
        for row in self.panel["descriptions"]:
            self.assertEqual(row["activation_cell_member"] % row["modulus"], row["class_residue"])
            self.assertEqual(parse_mask_hex(row["resulting_union_mask_hex"]).bit_count(), row["G5"])
            self.assertTrue(row["prior_evaluation_excluded"])

    def test_collision_incidence(self):
        result = build_incidence(self.panel)
        self.assertEqual(result["distinct_integer_count"], 454)
        self.assertEqual(result["integers_generated_by_exactly_1_description"], 451)
        self.assertEqual(result["integers_generated_by_exactly_2_descriptions"], 3)
        self.assertEqual(result["maximum_description_multiplicity"], 2)

    def test_missing_and_family_injection_rejected(self):
        changed = copy.deepcopy(self.panel["descriptions"]); changed.pop()
        with self.assertRaises(CensusError): validate_descriptions(changed)
        changed = copy.deepcopy(self.panel["descriptions"]); changed[0]["description_id"] = "Q-INJECTED"
        with self.assertRaises(CensusError): validate_descriptions(changed)

    def test_no_evaluator_fields(self):
        self.assertFalse(self.panel["integer_evaluation_performed"])
        self.assertNotIn("T", self.panel["descriptions"][0])

    def test_even_sample_median_is_order_independent(self):
        summary = exact_summary([(10, 40), (11, 10), (12, 30), (13, 20)])
        self.assertEqual(summary["median"]["numerator"], 25)
        self.assertEqual(summary["median"]["denominator"], 1)


if __name__ == "__main__":
    unittest.main()
