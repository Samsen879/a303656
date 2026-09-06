from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_exact_bounded_scan(self):
        scan = json.loads((ROOT / "results/scan_summary.json").read_text())
        replay = json.loads((ROOT / "results/repository_replay_environment.json").read_text())
        self.assertEqual(scan["limit"], 2_000_000_000)
        self.assertEqual(scan["hits"], [20771, 40487, 1645333507])
        self.assertEqual(scan["candidate_count"], 49_112_626)
        self.assertEqual(scan["full_block_comparison"], "PASS")
        self.assertEqual(replay["scan_bound"], scan["limit"])
        self.assertEqual(replay["candidate_count"], scan["candidate_count"])
        self.assertEqual(replay["nonregular_hits"], scan["hits"])
        self.assertEqual([x["order"] for x in replay["hit_certificates"]],
                         [10385, 40486, 1645333506])
        self.assertEqual([x["s_q"] for x in replay["hit_certificates"]], [2, 2, 2])
        self.assertEqual(replay["two_implementation_jsonl_comparison"], "BYTE_IDENTICAL_PASS")

    def test_structural_theorem_is_not_the_bounded_scan(self):
        text = " ".join((ROOT / "INTEGRATION.md").read_text().split())
        self.assertIn("unbounded structural theorem", text)
        self.assertIn("bounded exact computation", text)
        self.assertIn("A303656: UNRESOLVED", text)

    def test_nested_transport_and_macro_guards(self):
        receipt = json.loads((ROOT / "evidence/nested_source_receipt.json").read_text())
        self.assertFalse(receipt["committed"])
        self.assertEqual(receipt["byte_identity_with_package_a"], "PASS")
        self.assertIn("not original actual primes", (ROOT / "INTEGRATION.md").read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
