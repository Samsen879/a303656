from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import AuditError, write_json
from verify_package import build_manifest, verify_manifest, verify_text_hygiene


class CorruptionTests(unittest.TestCase):
    def test_manifest_fails_closed_after_byte_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "payload.txt").write_text("exact\n", encoding="utf-8")
            manifest = build_manifest(root)
            verify_manifest(root, manifest)
            (root / "payload.txt").write_text("corrupt\n", encoding="utf-8")
            with self.assertRaises(AuditError):
                verify_manifest(root, manifest)

    def test_manifest_fails_closed_on_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "payload.txt").write_text("exact\n", encoding="utf-8")
            manifest = build_manifest(root)
            (root / "extra.txt").write_text("unexpected\n", encoding="utf-8")
            with self.assertRaises(AuditError):
                verify_manifest(root, manifest)

    def test_hidden_control_character_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "report.md").write_bytes(b"clean\nmalformed\x1econtrol\n")
            with self.assertRaises(AuditError):
                verify_text_hygiene(root)


if __name__ == "__main__":
    unittest.main()
