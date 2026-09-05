import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "phase2_reference", ROOT / "tools" / "reference_two_anchor.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TwoAnchorReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = MODULE.build_result()

    def test_frozen_exact_catalog(self):
        self.assertEqual(
            self.result["dynamic_common_residue_classification"]["pair_count_mod_67_squared"],
            603,
        )
        self.assertEqual(
            self.result["rigid_common_residue_classification"]["class_pair_count_mod_20771"],
            5192,
        )
        classification = self.result["exhaustive_fixed_pair_pointwise_classification"]
        self.assertEqual(classification["aligned_dynamic_rigid_class_combinations"], 693)
        self.assertEqual(classification["same_lower_assignment_combinations"], 0)

    def test_sharp_rigid_frontier_deficit(self):
        sharp = self.result["sharp_minimal_joint_counterexample"]
        self.assertEqual(
            sharp["all_lower_assignments"]["minimum_total_holes_over_common_lower_assignment"],
            66,
        )

    def test_scope_guard_is_recorded(self):
        boundary = self.result["logical_boundary"]
        self.assertIn("No universal incompatibility", boundary["not_proved"])
        self.assertIn("one lower assignment", boundary["missing_bridge"])

    def test_odd_row_anchor_exclusion_identity(self):
        for residue in range(19):
            for exponent_value in range(19):
                left = residue - 1 - exponent_value
                right = residue - 3 - exponent_value
                self.assertEqual(left - right, 2)
                self.assertFalse(left % 19 == 0 and right % 19 == 0)


if __name__ == "__main__":
    unittest.main()
