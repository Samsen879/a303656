from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
DESTINATION = "analysis/c1_order_dag_phase_c/"


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

    def test_extremal_and_conditional_scope(self):
        self.assertIn("total original nonregular lower bound remains seven", self.integration)
        self.assertIn("at least seven original nonregular primes above `2e9`", self.integration)
        self.assertIn("Theorem 12.1 is conditional", self.integration)
        self.assertIn("roots have not been instantiated", self.integration)
        self.assertIn("no certified\ncounterexample exists", self.integration)
        self.assertIn("B7 emptiness is not proved", self.integration)
        self.assertIn("does not solve A303656", self.integration)
        self.assertIn("derived macro is not an\noriginal prime", self.integration)

    def test_cross_package_interface_is_not_duplicated(self):
        self.assertIn("general Phase C hybrid\nallocated-transitive theorem is the primary authority", self.integration)
        self.assertIn("restricted interface/corollary", self.integration)
        self.assertIn("not\npromoted as a second distinct theorem identity", self.integration)

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
