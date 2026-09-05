#!/usr/bin/env python3
"""Create or verify repository-native integrity metadata for this directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXCLUDED = {"manifest.json", "SHA256SUMS.txt"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def payload(root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.relative_to(root).as_posix() not in EXCLUDED
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def expected_manifest(root: Path, source_zip_sha256: str) -> dict[str, object]:
    entries = [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": digest(path),
            "size": path.stat().st_size,
        }
        for path in payload(root)
    ]
    return {
        "schema": "a303656.repository-native-phase-integration.v1",
        "authority": {
            "repository": "Samsen879/a303656",
            "repository_id": 1333945235,
            "integration_base_sha": "1100eb5ba01d90e5b1001be0bdfa464860fdbb92",
            "integration_base_tree": "ad1269916bf420c564e34887a96c808033fe538b",
            "project": "PAUSED",
            "active_promoted_route": "NONE",
            "a303656": "UNRESOLVED",
        },
        "source": {
            "requested_filename": "A303656_PREFIX_FRONTIER_REALIZABILITY_PHASE_A(1).zip",
            "located_filename": "A303656_PREFIX_FRONTIER_REALIZABILITY_PHASE_A.zip",
            "outer_zip_sha256": source_zip_sha256,
            "safe_extraction": "PASS",
            "internal_sha256sums": "PASS",
            "standalone_replay": (
                "SOURCE_GENERATED_RESULTS_BYTE_IDENTICAL_BEFORE_REPAIR; "
                "SUMMARY_SCOPE_METADATA_INTENTIONALLY_REGENERATED_AFTER_QUANTIFIER_REPAIR"
            ),
        },
        "file_count": len(entries),
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    source_hash = "60780334b892445d966a0224e1e6eb8ca2acba6b4bad1bb67b8baf168f8d24ab"
    expected = expected_manifest(root, source_hash)
    sums = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in expected["files"]
    )
    if args.verify:
        actual = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        if actual != expected:
            raise SystemExit("manifest mismatch")
        if (root / "SHA256SUMS.txt").read_text(encoding="utf-8") != sums:
            raise SystemExit("SHA256SUMS mismatch")
        print(f"PASS: {len(expected['files'])} repository-native files verified")
        return 0
    (root / "manifest.json").write_text(
        json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (root / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    print(f"WROTE: {len(expected['files'])} repository-native file records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
