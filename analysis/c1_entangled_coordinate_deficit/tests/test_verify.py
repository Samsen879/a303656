from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from verify import (  # noqa: E402
    clipped_valuation,
    order_mod_5,
    verify_chain,
    verify_coordinate_examples,
    verify_k2_boundary,
    verify_two_adic,
)


class EntangledCoordinateAuditTests(unittest.TestCase):
    def test_local_zero_is_unresolved(self):
        self.assertIsNone(clipped_valuation(0, 11, 2))

    def test_chain_orders(self):
        self.assertEqual(
            [order_mod_5(p) for p in (11, 67, 20771)],
            [5, 22, 10385],
        )

    def test_chain_direct_enumeration(self):
        result = verify_chain()
        self.assertTrue(result["PASS"])
        self.assertEqual(result["assignment_counts"], [670, 66, 1])
        self.assertEqual(result["safe_counts"]["1"], 176698)

    def test_chain_is_not_a_certificate(self):
        result = verify_chain()
        self.assertGreater(result["safe_counts"]["0"], 0)
        self.assertGreater(result["safe_counts"]["1"], 0)

    def test_coordinate_incomparability(self):
        result = verify_coordinate_examples()
        self.assertTrue(result["PASS"])
        first = result["coordinate_succeeds_global_fails"]["global_mass"]
        second = result["global_succeeds_coordinate_fails"]["global_mass"]
        self.assertGreater(Fraction(*first), 1)
        self.assertLess(Fraction(*second), 1)

    def test_common_residue_two_anchors(self):
        sample = verify_coordinate_examples()["dual_anchor_common_residue"]
        self.assertEqual(sample["r"], 96315155)
        self.assertEqual(sample["fatal_classes"], {"0": [6528], "1": [2]})

    def test_two_adic_direct_square_residues(self):
        result = verify_two_adic()
        self.assertTrue(result["PASS"])
        self.assertEqual(result["direct_membership_checks"], 699048)

    def test_k2_equals_2_old_wording_counterexample(self):
        case = verify_k2_boundary()["k2_equals_2_unsafe"]
        self.assertEqual(
            (case["w_11"], case["s_11"], case["a_11"], case["t_2"]),
            (5, 1, 1, 1),
        )
        self.assertEqual((case["U"], case["L"], case["beta_11"]), (5, 55, 0))
        self.assertFalse(case["two_divides_U"])
        self.assertTrue(case["old_wording_hypothesis"])
        self.assertEqual(case["odd_coordinate_hazards"], {"5": [0, 1]})
        self.assertEqual(case["odd_fatal_count"], 0)
        self.assertEqual(case["Theta_c"], [1, 1])
        self.assertFalse(case["constant_two_adic_safe"])
        self.assertFalse(case["corrected_criterion_hypothesis"])
        self.assertEqual(case["direct_safe_count"], 0)

    def test_k2_equals_2_safe_anchor(self):
        case = verify_k2_boundary()["k2_equals_2_safe"]
        self.assertTrue(case["constant_two_adic_safe"])
        self.assertEqual(case["Theta_c"], [0, 1])
        self.assertTrue(case["corrected_criterion_hypothesis"])
        self.assertEqual(case["direct_safe_count"], case["L"])

    def test_k2_at_least_3_uses_genuine_coordinate_two(self):
        case = verify_k2_boundary()["k2_equals_3_coordinate"]
        self.assertTrue(case["two_divides_U"])
        self.assertEqual((case["U"], case["L"]), (10, 110))
        self.assertEqual(case["coordinate_hazards"]["2"], [1, 2])
        self.assertTrue(case["corrected_criterion_hypothesis"])
        self.assertEqual(case["direct_safe_count"], 55)

    def test_no_two_adic_row_has_no_constant_requirement(self):
        case = verify_k2_boundary()["no_two_adic_row"]
        self.assertIsNone(case["constant_two_adic_safe"])
        self.assertNotIn("2", case["coordinate_hazards"])
        self.assertTrue(case["corrected_criterion_hypothesis"])
        self.assertEqual(case["direct_safe_count"], case["L"])


if __name__ == "__main__":
    unittest.main()
