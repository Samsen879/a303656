#!/usr/bin/env python3
"""Build the deterministic compact result manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

CORE = [
    "REPORT.md",
    "c0_mod4_control.json",
    "corruption_tests.json",
    "finite_replay.json",
    "regular_lift_theorem_audit.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def valid_hex(value: str, length: int) -> bool:
    return len(value) == length and all(c in "0123456789abcdef" for c in value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--base-tree", required=True)
    args = parser.parse_args()
    if not all(valid_hex(value, 40) for value in (args.source_commit, args.base_sha, args.base_tree)):
        raise SystemExit("invalid provenance identifier")
    files = []
    for name in CORE:
        path = args.results / name
        if not path.is_file():
            raise SystemExit(f"missing core result: {name}")
        files.append({"path": name, "sha256": sha256(path), "size_bytes": path.stat().st_size})
    manifest = {
        "schema": "a303656-one-sided-strip-audit-manifest-v1",
        "authority": {
            "repository": "Samsen879/a303656",
            "repository_id": 1333945235,
            "base_sha": args.base_sha,
            "base_tree": args.base_tree,
            "source_commit": args.source_commit,
            "project": "PAUSED",
            "active_promoted_route": "NONE",
            "A303656": "UNRESOLVED",
        },
        "files": files,
        "scope_guards": {
            "domain": [2, 100000000],
            "interval_extension": "NOT EXECUTED",
            "prime_pool_expansion": "NOT EXECUTED",
            "wieferich_full_cover_research": "NOT EXECUTED",
            "raw_arrays_committed": False,
            "authority_modified": False,
        },
        "verdict": "PASS_NARROW_REPOSITORY_NATIVE_AUDIT",
    }
    output = args.results / "manifest.json"
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(output), "files": len(files)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
