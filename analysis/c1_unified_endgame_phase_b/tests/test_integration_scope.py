from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_seven_prime_bound_and_authority(self):
        verdict = json.loads((ROOT / "results/verdict.json").read_text())
        authority = json.loads((ROOT / "results/source_binding.json").read_text())["status"]
        self.assertEqual(verdict["corollary"],
                         "At least seven distinct original nonregular primes are necessary.")
        self.assertFalse(verdict["a303656_solved"])
        self.assertEqual(authority,
                         {"PROJECT": "PAUSED", "ACTIVE PROMOTED ROUTE": "NONE",
                          "A303656": "UNRESOLVED"})

    def test_derived_macros_are_not_original_primes(self):
        scope = " ".join((ROOT / "INTEGRATION.md").read_text().split())
        self.assertIn("Derived provenance macros remain bookkeeping devices", scope)
        self.assertIn("not original actual primes", scope)
        self.assertIn("do not contribute to the seven-prime count", scope)


if __name__ == "__main__":
    unittest.main(verbosity=2)
