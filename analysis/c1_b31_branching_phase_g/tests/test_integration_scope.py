from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_b31_branching_phase_g/"


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

    def test_role_and_negative_scope(self):
        normalized = " ".join(self.text.split())
        self.assertIn("B31 FIXED-BASE NECESSITY / GENERAL ROUTE AUDIT", self.text)
        self.assertIn("not a B31 emptiness theorem", normalized)
        self.assertIn("does not rule out all reciprocity", normalized)
        self.assertIn("q-squared-sensitive arithmetic", normalized)

    def test_nonclaims(self):
        for value in (
            "B31^odd EMPTY: NOT PROVED", "ACTUAL B31^odd MEMBER: NONE",
            "GLOBAL FINITE CRITICAL FAMILY: NOT PROVED", "EXACTLY-SEVEN: NOT KILLED",
            "N>=8: NOT PROVED", "A303656: UNRESOLVED",
        ):
            self.assertIn(value, self.text)

    def test_required_mutation_mapping(self):
        for value in (
            "corrupt_exact_order", "terminal3_in_all_odd_rows", "drop_maximal_generator",
            "wrong_edge_sign", "fake_base5_member",
        ):
            self.assertIn(value, self.text)

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
