from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from arithmetic_realizability_checker import (
    actual_beta_one_67_20771,
    common_residue_audit,
    k2_constant_boundary_replay,
    nonregular_record,
    scan_nonregular,
    separate_anchor_beta_one_class_zero,
)


class ArithmeticTests(unittest.TestCase):
    def test_known_nonregular_orders(self) -> None:
        expected = {
            20771: (10385, 2, 67, 1),
            40487: (40486, 2, 653, 1),
            1645333507: (1645333506, 2, 30469139, 1),
        }
        for q, target in expected.items():
            row = nonregular_record(q)
            self.assertEqual(
                (row["w_q"], row["s_q"], row["largest_order_prime"], row["largest_order_prime_exponent"]),
                target,
            )

    def test_frozen_small_scan(self) -> None:
        searched, found = scan_nonregular(100_000)
        self.assertEqual(len(searched), 4808)
        self.assertEqual([row["q"] for row in found], [20771, 40487])

    def test_actual_beta_one_partition(self) -> None:
        record = actual_beta_one_67_20771()
        self.assertEqual(record["dynamic_fatal_count"], 66)
        self.assertEqual(record["rigid_fatal_count"], 1)
        self.assertTrue(record["exact_partition"])
        self.assertTrue(record["local_zero_fail_closed"])

    def test_common_residue_compatibility(self) -> None:
        audit = common_residue_audit()
        compatibility = audit["compatibility"]
        self.assertTrue(compatibility["known_pair_6528_2_present"])
        self.assertFalse(compatibility["pair_0_0_present"])
        self.assertEqual(audit["verified_common_residue_sample"]["classes"], {"0": [6528], "1": [2]})

    def test_k2_constant_boundary_is_separate(self) -> None:
        replay = k2_constant_boundary_replay()
        self.assertTrue(replay["old_odd_coordinate_hypothesis_passes"])
        self.assertFalse(replay["corrected_constant_boundary_passes"])
        self.assertEqual(replay["direct_safe_count"], 0)
        self.assertFalse(replay["two_divides_U"])
        self.assertTrue(replay["kept_outside_odd_coordinate_catalog"])

    def test_separate_anchor_beta_one_templates_do_not_share_residues(self) -> None:
        record = separate_anchor_beta_one_class_zero()
        self.assertTrue(record["anchors"]["0"]["exact_partition"])
        self.assertTrue(record["anchors"]["1"]["exact_partition"])
        self.assertFalse(record["one_common_dynamic_residue_possible"])
        self.assertFalse(record["one_common_rigid_residue_possible"])


if __name__ == "__main__":
    unittest.main()
