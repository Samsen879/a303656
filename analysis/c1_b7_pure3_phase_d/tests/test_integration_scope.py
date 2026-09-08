from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_b7_pure3_phase_d/"


class IntegrationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "INTEGRATION.md").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "INTEGRATION_MANIFEST.json").read_text(encoding="utf-8"))

    def test_authority_unchanged(self):
        status = (REPOSITORY / "STATUS.md").read_text(encoding="utf-8")
        for statement in ("PROJECT: PAUSED", "ACTIVE PROMOTED ROUTE: NONE", "A303656: UNRESOLVED"):
            self.assertIn(statement, status)
            self.assertIn(statement, self.text)

    def test_mathematical_scope(self):
        for statement in (
            "`{43,127,379,7603,19531,519499}`", "48 initial order indices",
            "`43,86,127,129,258`", "`{301,602,903,1806}`",
            "B7 EMPTY: NOT PROVED", "ACTUAL B7 MEMBER: NOT FOUND",
            "TOTAL NONREGULAR LOWER BOUND: REMAINS 7", "N>=8: NOT PROVED",
            "Literal\nprime-order chains are not necessary",
            "discovery-only and not promoted theorem\nevidence",
        ):
            self.assertIn(statement, self.text)

    def test_custody_and_result_guards(self):
        self.assertEqual(len(self.manifest["source_payload"]), 11)
        results = json.loads((ROOT / "verification_results.json").read_text(encoding="utf-8"))
        self.assertFalse(results["B7_member_found"])
        self.assertFalse(results["B7_empty_proved"])
        self.assertFalse(results["total_lower_bound_raised_to_eight"])
        self.assertFalse(self.manifest["source_archive"]["committed"])

    def test_introduction_commit_is_confined(self):
        receipt = (ROOT / "INTEGRATION.md").relative_to(REPOSITORY).as_posix()
        commits = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%H", "--", receipt],
            cwd=REPOSITORY, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        self.assertTrue(commits)
        changed = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commits[-1]],
            cwd=REPOSITORY, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        self.assertTrue(changed)
        self.assertTrue(all(path.startswith(DESTINATION) for path in changed), changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
