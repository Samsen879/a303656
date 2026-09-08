from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_seven_head_chain_realizability_phase_d/"


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

    def test_mathematical_and_cross_package_scope(self):
        for statement in (
            "ALL SEVEN CHAINS EXIST: OPEN",
            "TERMINAL NONREGULAR ROOTS: NOT INSTANTIATED",
            "ACTUAL COMPLETE C=1 CERTIFICATE: NONE",
            "EXACTLY-SEVEN IMPOSSIBILITY: NOT PROVED",
            "not a necessary general B7 basin representation",
            "B7 Phase D package is the more general arithmetic authority",
            "Literal-chain failure is not B7 emptiness",
            "exactly-seven is not killed",
        ):
            self.assertIn(statement, self.text)

    def test_full_replay_and_custody(self):
        self.assertEqual(len(self.manifest["source_payload"]), 103)
        flattened = [item for command in self.manifest["source_replay"]["commands"] for item in command]
        self.assertIn("--replay-search", flattened)
        self.assertEqual(self.manifest["source_replay"]["result"], "PASS")
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
