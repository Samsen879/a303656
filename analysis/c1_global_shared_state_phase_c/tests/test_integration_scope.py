from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_global_shared_state_phase_c/"


class IntegrationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.integration = (ROOT / "INTEGRATION.md").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "INTEGRATION_MANIFEST.json").read_text(encoding="utf-8"))

    def test_authority_is_unchanged(self):
        status = (REPOSITORY / "STATUS.md").read_text(encoding="utf-8")
        for statement in (
            "PROJECT: PAUSED", "ACTIVE PROMOTED ROUTE: NONE", "A303656: UNRESOLVED"
        ):
            self.assertIn(statement, status)
            self.assertIn(statement, self.integration)

    def test_global_state_quantifiers_and_scope(self):
        self.assertIn("`EITHER` is not `BOTH`, and `BOTH` is not `TRUE`", self.integration)
        self.assertIn("existence of one global state vector", self.integration)
        self.assertIn("not permission to choose a new state\n  independently for each fiber", self.integration)
        self.assertIn("odd pooled cover is not a complete simultaneous", self.integration)
        self.assertIn("does **not** prove universal pooled-branch elimination", self.integration)
        self.assertIn("does not\nsolve A303656", self.integration)
        self.assertIn("derived macro is not an original prime", self.integration)

    def test_transport_archive_is_absent(self):
        self.assertFalse(self.manifest["source_archive"]["committed"])
        self.assertFalse(self.manifest["transport_archives_committed"])
        self.assertFalse(any(path.suffix.lower() == ".zip" for path in ROOT.rglob("*") if path.is_file()))

    def test_diff_is_confined_to_this_directory(self):
        base = self.manifest["integration_base"]["sha"]
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            cwd=REPOSITORY, check=True, capture_output=True, text=True,
        )
        changed = [line for line in result.stdout.splitlines() if line]
        self.assertTrue(changed)
        self.assertTrue(all(path.startswith(DESTINATION) for path in changed), changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
