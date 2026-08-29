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


if __name__ == "__main__":
    unittest.main()
