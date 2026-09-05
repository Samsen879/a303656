from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_catalogs_are_reproducible_not_committed(self):
        self.assertFalse((ROOT / "catalogs").exists())
        receipt = json.loads((ROOT / "results/generated_catalog_receipt.json").read_text())
        self.assertEqual([item["exact_states"] for item in receipt["catalogs"]], [2346, 25963])

    def test_finite_inventory_and_capacity(self):
        data = json.loads((ROOT / "results/rigid_blocker_inventory.json").read_text())
        self.assertEqual([row["prime"] for row in data["nonregular_rows"]], [20771, 40487])
        self.assertEqual(data["paired_blocker_assignment"], {"20771": 5, "40487": 653})
        self.assertTrue(all(row["maximum_forbidden_digits"] < row["coordinate"] for row in data["loads"]))

    def test_boundary_does_not_get_universalized(self):
        data = json.loads((ROOT / "results/blocker_boundary_resource.json").read_text())
        self.assertEqual(data["prime"], 1645333507)
        self.assertEqual(data["structurally_ineligible_odd_order_factors"], [])
        self.assertTrue(data["not_a_complete_certificate"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
