from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_coordinate_three_bounds(self):
        data = json.loads((ROOT / "results/theorem_verification.json").read_text())["arithmetic"]
        self.assertEqual(data["coordinate3_min_rigid_depth"], 4)
        self.assertEqual(data["rigid_only_minimum_rows"], 81)
        self.assertEqual(data["dynamic_allowed_minimum_rows"], 21)

    def test_zero_lower_joint_bounds(self):
        data = json.loads((ROOT / "results/theorem_verification.json").read_text())["arithmetic"]
        self.assertEqual(data["coordinate5_beta1_Y0_joint_rows"], 10)
        self.assertEqual(data["coordinate7_beta1_Y0_joint_rows"], 8)

    def test_authority_scope_unchanged(self):
        data = json.loads((ROOT / "results/source_authority.json").read_text())
        self.assertEqual((data["project"], data["active_promoted_route"], data["a303656"]),
                         ("PAUSED", "NONE", "UNRESOLVED"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
