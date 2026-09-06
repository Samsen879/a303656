from fractions import Fraction
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_coordinate_three_depth_four(self):
        data = json.loads((ROOT / "results/cyclotomic_depth4.json").read_text())
        self.assertEqual(data["new_theorem"], "R_(3,4) is empty")
        self.assertEqual([x["m"] for x in data["factorizations"]], [81, 162])
        self.assertEqual(data["combined_with_source_depths_1_to_3"]["minimum_rigid_depth"], 5)

    def test_allocated_boundary_blocker(self):
        rows = json.loads((ROOT / "results/sparse_subclass.json").read_text())
        assigned = next(x for x in rows["assignments"] if x["q"] == 1645333507)
        load = Fraction(assigned["dynamic_load_supremum"]) + Fraction(assigned["worst_pair_load"])
        self.assertEqual(load, Fraction(89, 108))
        self.assertLess(load, 1)

    def test_demand_and_resource_scope(self):
        demand = json.loads((ROOT / "results/demand_audit.json").read_text())
        self.assertIn("EITHER -> EITHER", demand["transition_histogram"])
        self.assertIn("BOTH -> BOTH", demand["transition_histogram"])
        text = (ROOT / "INTEGRATION.md").read_text()
        self.assertIn("EITHER is not BOTH or TRUE", text)
        self.assertIn("Derived macros are not actual rigid", text)
        self.assertIn("A303656: UNRESOLVED", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
