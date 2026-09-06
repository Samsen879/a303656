from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_six_row_obstruction_is_seven_prime_lower_bound(self):
        data = json.loads((ROOT / "results/six_row_obstruction.json").read_text())
        self.assertEqual(data["claim_scope"],
                         "no complete admitted C=1 certificate with at most six original nonregular rows")
        self.assertEqual(data["allocation_cases"], 84)
        self.assertEqual(data["mismatches"], 0)

    def test_transitive_release_preserves_original_identity(self):
        data = json.loads((ROOT / "results/boundary_escape.json").read_text())
        self.assertEqual(data["dependency_released_route"], [1645333507, 30469139, 1429])
        self.assertEqual(data["original_direct_core"], [1645333507])
        self.assertNotEqual(data["dependency_released_route"], data["original_direct_core"])

    def test_terminal_exception_and_no_synthetic_prime(self):
        text = (ROOT / "INTEGRATION.md").read_text()
        self.assertIn("terminal Hall exceptional class remains", text)
        self.assertIn("do not synthesize new original primes", text)
        self.assertIn("A303656: UNRESOLVED", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
