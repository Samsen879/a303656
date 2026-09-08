from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_private_provider_charging_phase_d/"


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
            "center/provider ancestry", "root-basin support confinement",
            "single-frontier\nfrozen-shadow capacity", "capacity-saturated",
            "`N>=8` is **NOT proved**", "no global N-only capacity theorem",
            "derived macro is not an original\nprime",
            "conditional chain fixture is not an actual complete certificate",
            "no A303656 solution",
        ):
            self.assertIn(statement, self.text)

    def test_custody_policy(self):
        self.assertEqual(len(self.manifest["source_payload"]), 12)
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
        introduction = commits[-1]
        changed = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", introduction],
            cwd=REPOSITORY, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        self.assertTrue(changed)
        self.assertTrue(all(path.startswith(DESTINATION) for path in changed), changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
