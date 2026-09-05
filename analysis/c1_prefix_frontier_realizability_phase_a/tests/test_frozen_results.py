import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


class FrozenPhaseThreeResults(unittest.TestCase):
    def test_bounded_resource_inventory(self):
        result = load("resource_scan_B10000000.json")
        self.assertEqual(result["domain"]["bound_inclusive"], 10_000_000)
        self.assertEqual(result["domain"]["admitted_prime_count"], 332_398)
        self.assertEqual([row["q"] for row in result["all_nonregular_rows"]], [20771, 40487])
        depth = result["targets"]["67"]["depths"]
        self.assertEqual(depth["1"]["order_signature"]["count"], 645)
        self.assertEqual(depth["1"]["active_nonregular"]["count"], 1)
        self.assertEqual(depth["2"]["order_signature"]["count"], 35)
        self.assertEqual(depth["2"]["active_nonregular"]["count"], 0)
        self.assertEqual(depth["3"]["order_signature"]["count"], 1)
        self.assertEqual(depth["3"]["active_nonregular"]["count"], 0)

    def test_literal_and_compressed_catalogs(self):
        literal = load("l3_beta_le_3_literal_catalog.json")
        self.assertEqual(literal["candidate_total"], 1431)
        compressed = load("l67_beta_le_3_compressed_catalog.json")
        realized = [group["status_counts"].get("ARITHMETICALLY_REALIZABLE", "0") for group in compressed["groups"]]
        self.assertEqual(realized, ["1", "2", "4"])

    def test_actual_embeddings_are_local_and_exact(self):
        result = load("actual_67_beta_1_2_3_embeddings.json")
        self.assertEqual(len(result["cases"]), 14)
        self.assertTrue(all(case["hole_count"] == 0 for case in result["cases"]))
        self.assertIn("different lower assignments", result["scope"])
        self.assertIn("not a complete certificate", result["scope"])

    def test_common_residue_audit(self):
        result = load("common_residue_audit.json")
        self.assertEqual(result["q20771_k2_h1"]["pair_count"], 5192)
        self.assertTrue(result["q20771_k2_h1"]["contains_6528_2"])

    def test_ambient_quantifier_scope_is_explicit(self):
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("First choose distinct rigid-resource rows", report)
        self.assertIn("determine the final coarse period", report)
        self.assertIn("previously prescribed partial lower point", report)
        self.assertIn("the theorem does not", report)
        self.assertIn("promise to add arbitrary resources", report)


if __name__ == "__main__":
    unittest.main()
