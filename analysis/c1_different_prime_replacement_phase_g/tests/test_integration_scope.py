from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_different_prime_replacement_phase_g/"


class IntegrationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "INTEGRATION.md").read_text(encoding="utf-8")
        cls.results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))

    def test_authority_unchanged(self):
        status = (REPOSITORY / "STATUS.md").read_text(encoding="utf-8")
        for value in ("PROJECT: PAUSED", "ACTIVE PROMOTED ROUTE: NONE", "A303656: UNRESOLVED"):
            self.assertIn(value, status)
            self.assertIn(value, self.text)

    def test_abstract_arithmetic_boundary(self):
        self.assertIn("ABSTRACT MODEL != ACTUAL ARITHMETIC CERTIFICATE", self.text)
        self.assertEqual(self.results["ABSTRACT_COUNTERMODEL"], "FOUND")
        self.assertEqual(self.results["ACTUAL_ARITHMETIC_COUNTEREXAMPLE"], "NOT FOUND")
        self.assertEqual(self.results["actual_endpoint_prime_checks"], 0)

    def test_route_scope_and_nonclaims(self):
        for value in (
            "DEAD AT CURRENT STRUCTURAL AUTHORITY", "B7 EMPTY: NOT PROVED",
            "EXACTLY-SEVEN: NOT KILLED", "N>=8: NOT PROVED", "A303656: UNRESOLVED",
        ):
            self.assertIn(value, self.text)
        normalized = " ".join(self.text.split())
        self.assertIn("not a claim that the route is mathematically impossible in fixed base 5", normalized)

    def test_branch_diff_is_isolated_after_commit(self):
        receipt = (ROOT / "INTEGRATION.md").relative_to(REPOSITORY).as_posix()
        commits = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%H", "--", receipt],
            cwd=REPOSITORY, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        if not commits:
            self.skipTest("package introduction commit not created yet")
        changed = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commits[0]],
            cwd=REPOSITORY, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        self.assertTrue(changed)
        self.assertTrue(all(path.startswith(DESTINATION) for path in changed if path), changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
