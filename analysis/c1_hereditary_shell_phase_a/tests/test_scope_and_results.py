import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HereditaryShellIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = json.loads((ROOT / "results" / "results.json").read_text(encoding="utf-8"))
        cls.report = (ROOT / "REPORT.md").read_text(encoding="utf-8")

    def test_provenance_formula_and_recursive_audit(self):
        outcome = self.result["formal_outcome"]
        self.assertIn("OR_{I minimal exact slice cover}", outcome["canonical_residual_formula"])
        self.assertIn("PASS", outcome["provenance_cylinder_grammar"])
        self.assertEqual(outcome["hereditary_counterexamples_in_provenance_grammar"], 0)
        self.assertEqual(self.result["recursive_provenance_audit"]["recursive_mismatches"], 0)

    def test_literal_row_only_obstruction(self):
        outcome = self.result["formal_outcome"]
        self.assertIn("FAIL", outcome["row_only_grammar"])
        self.assertEqual(self.result["guarded_slice_audit"]["pair_row_only_grammar_failures"], 422)

    def test_actual_prime_boundary_is_explicit(self):
        self.assertIn("does **not** make that macro a new actual arithmetic", self.report)
        self.assertIn("UNQUALIFIED ADMITTED-ROW CLOSURE: NOT CLAIMED", self.report)

    def test_authority_state_unchanged(self):
        authority = self.result["authority"]
        self.assertEqual(authority["project"], "PAUSED")
        self.assertEqual(authority["active_promoted_route"], "NONE")
        self.assertEqual(authority["a303656"], "UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
