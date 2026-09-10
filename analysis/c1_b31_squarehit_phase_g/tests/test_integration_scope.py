from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_b31_squarehit_phase_g/"


class IntegrationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "INTEGRATION.md").read_text(encoding="utf-8")
        cls.consolidation = json.loads((ROOT / "SOURCE_CONSOLIDATION.json").read_text(encoding="utf-8"))

    def test_authority_unchanged(self):
        status = (REPOSITORY / "STATUS.md").read_text(encoding="utf-8")
        for value in ("PROJECT: PAUSED", "ACTIVE PROMOTED ROUTE: NONE"):
            self.assertIn(value, status)
            self.assertIn(value, self.text)
        self.assertIn("A303656: UNRESOLVED", status)

    def test_consolidation_does_not_invent_independence(self):
        self.assertEqual(self.consolidation["independent_implementations_claimed"], 0)
        archives = {item["id"]: item for item in self.consolidation["archives"]}
        self.assertEqual(archives["E-v2"]["sha256"], archives["E-v2-duplicate"]["sha256"])
        self.assertEqual(archives["E-v2-duplicate"]["duplicate_of"], "E-v2")

    def test_mathematical_guards(self):
        normalized = " ".join(self.text.split())
        for value in (
            "does not manufacture an independent second Wieferich", "Polynomial irreducibility does not imply",
            "does not apply to these eight indices", "It does not say that no algebraic",
            "BOUNDED EXTERNAL COMPUTATIONAL GATE", "not asserted prime",
            "Phase F owns the exact eight-index three-vertex equivalence",
        ):
            self.assertIn(value, normalized)

    def test_exact_indices(self):
        for value in (878851, 2636553, 27244381, 81733143, 625552508473588471, 1876657525420765413, 19392127762681242601, 58176383288043727803):
            self.assertIn(str(value), self.text)

    def test_explicit_nonclaims(self):
        normalized = " ".join(self.text.split())
        for value in (
            "n=878851 CLOSED: NO", "FOUR-INDEX r=878851 FAMILY CLOSED: NO",
            "B31 THREE-VERTEX EMPTY: NO", "B31^odd EMPTY: NO",
            "ACTUAL B31^odd MEMBER: NONE", "EXACTLY-SEVEN: NOT KILLED",
            "N>=8: NOT PROVED", "A303656: UNRESOLVED",
        ):
            self.assertIn(value, normalized)

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
