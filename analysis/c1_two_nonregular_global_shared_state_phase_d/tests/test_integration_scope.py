from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_two_nonregular_global_shared_state_phase_d/"


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
            "`C9_R(q1) OR C9_R(q2)`", "two-root\nwhole odd pooled cover exists",
            "exists ONE lower\nstate vector `tau`", "existential\nlower-state quantifier",
            "not an order-signature-only complete\nclassification", "EITHER != BOTH",
            "Whole odd pooled cover != complete C=1 certificate",
            "not a new universal\nno-go", "no A303656 solution",
        ):
            self.assertIn(statement, self.text)

    def test_custody_policy(self):
        self.assertEqual(len(self.manifest["source_payload"]), 17)
        self.assertFalse(self.manifest["source_archive"]["committed"])
        self.assertFalse(self.manifest["transport_archives_committed"])
        self.assertFalse(self.manifest["generated_binaries_committed"])

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
