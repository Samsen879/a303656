from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = 'analysis/c1_b7_branching_phase_e/'
REQUIRED = ['GENERAL B7 CLOSED-STATE AUTHORITY', 'finite branching is not finite depth', 'B7 empty: NOT PROVED', 'minimal B7 member three-vertex: NOT PROVED', 'SQD: NOT PROVED', 'N>=8: NOT PROVED']

class IntegrationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.integration = (ROOT / "INTEGRATION.md").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "INTEGRATION_MANIFEST.json").read_text(encoding="utf-8"))

    def test_authority_is_unchanged(self):
        status = (REPOSITORY / "STATUS.md").read_text(encoding="utf-8")
        for statement in ("PROJECT: PAUSED", "ACTIVE PROMOTED ROUTE: NONE", "A303656: UNRESOLVED"):
            self.assertIn(statement, status)
            self.assertIn(statement, self.integration)

    def test_package_scope_guards(self):
        for statement in REQUIRED:
            self.assertIn(statement, self.integration)

    def test_transport_and_binary_policy(self):
        self.assertFalse(self.manifest["source_archive"]["committed"])
        self.assertFalse(self.manifest["transport_archives_committed"])
        self.assertFalse(self.manifest["generated_binaries_committed"])

    def test_diff_is_confined_to_this_directory(self):
        receipt = (ROOT / "INTEGRATION.md").relative_to(REPOSITORY).as_posix()
        introductions = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", receipt], cwd=REPOSITORY, check=True, capture_output=True, text=True).stdout.splitlines()
        self.assertTrue(introductions)
        changed = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", introductions[0]], cwd=REPOSITORY, check=True, capture_output=True, text=True).stdout.splitlines()
        self.assertTrue(changed)
        self.assertTrue(all(path.startswith(DESTINATION) for path in changed if path), changed)

if __name__ == "__main__":
    unittest.main(verbosity=2)
