from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_r43_squarepart_phase_f/"
REQUIRED = ["903 CLOSED: NO", "1806 CLOSED: NO", "r=43 family empty: NO", "squarefree: NOT PROVED", "Negative ECM or randomized misses are not squarefree proof"]


class IntegrationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.integration = (ROOT / "INTEGRATION.md").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "INTEGRATION_MANIFEST.json").read_text(encoding="utf-8"))
        cls.binding = json.loads((ROOT / "DEPENDENCY_BINDING.json").read_text(encoding="utf-8"))

    def test_authority_is_unchanged(self):
        status = (REPOSITORY / "STATUS.md").read_text(encoding="utf-8")
        for statement in ("PROJECT: PAUSED", "ACTIVE PROMOTED ROUTE: NONE", "A303656: UNRESOLVED"):
            self.assertIn(statement, status)
            self.assertIn(statement, self.integration)

    def test_package_scope_and_hard_objects(self):
        for statement in REQUIRED:
            self.assertIn(statement, self.integration)
        receipts = self.binding["reconciliation_receipts"]
        self.assertEqual(receipts["C903_BYTE_IDENTITY"], "PASS")
        self.assertEqual(receipts["C1806_BYTE_IDENTITY"], "PASS")
        self.assertEqual(receipts["C903"]["sha256"], "07dff3e4b33a6e893c24f83f07dbac243b48c25b3f48b334c821035064804e7b")
        self.assertEqual(receipts["C1806"]["sha256"], "39cbbcdb3b186c1672471af958ec63bd5f91967b8bd7d7c37857a11f79a4eb44")

    def test_dependency_is_fail_closed(self):
        self.assertTrue(self.binding["producer_source_gap"]["preserved"])
        self.assertEqual(self.binding["repository_dependency_status"], "PENDING_MERGE")
        self.assertTrue(self.binding["merge_blocked"])

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
