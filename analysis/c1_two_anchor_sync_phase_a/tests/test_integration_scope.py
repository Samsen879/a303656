from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntegrationScopeTests(unittest.TestCase):
    def test_open_bridges_remain_open(self):
        data = json.loads((ROOT / "results/summary.json").read_text())
        self.assertEqual(data["actual_H1"], "OPEN AFTER TARGETED SEARCH")
        self.assertEqual(data["actual_H2"], "OPEN AFTER TARGETED SEARCH")
        self.assertEqual(data["A303656"], "UNRESOLVED")

    def test_exact_audits_have_no_mismatch(self):
        data = json.loads((ROOT / "results/summary.json").read_text())
        self.assertEqual(data["truth"]["mismatches"], 0)
        self.assertEqual(data["contraction"]["mismatches"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
