from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import sha256_file, write_json
from make_zip import create_deterministic_zip
from verify_package import build_manifest


class DeterministicZipTests(unittest.TestCase):
    def test_two_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "payload"
            root.mkdir()
            (root / "a.txt").write_text("alpha\n", encoding="utf-8")
            (root / "tool.py").write_text("print('exact')\n", encoding="utf-8")
            write_json(root / "manifest.json", build_manifest(root, {"test": True}))
            checksum_paths = sorted(p for p in root.rglob("*") if p.is_file())
            (root / "SHA256SUMS.txt").write_text(
                "".join(f"{sha256_file(p)}  {p.relative_to(root).as_posix()}\n" for p in checksum_paths),
                encoding="utf-8",
            )
            first = base / "first.zip"
            second = base / "second.zip"
            digest_one = create_deterministic_zip(root, first)
            digest_two = create_deterministic_zip(root, second)
            self.assertEqual(digest_one, digest_two)
            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
