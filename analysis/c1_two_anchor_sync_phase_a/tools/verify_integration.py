#!/usr/bin/env python3
"""Verify repository-native integrity, replay bytes, and scope-critical results."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = {
    "actual_arithmetic_replay.json", "actual_first_split.json", "counterexamples.json",
    "frozen_U15_nonrealizability.json", "random_contraction_audit.json", "summary.json",
    "template_search.json", "truth_table_audit.json", "two_adic_audit.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-results", type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for item in manifest["files"]:
        path = ROOT / item["path"]
        assert path.is_file() and path.stat().st_size == item["size"] and digest(path) == item["sha256"]
    summary = json.loads((ROOT / "results/summary.json").read_text())
    assert summary["actual_H1"] == "OPEN AFTER TARGETED SEARCH"
    assert summary["actual_H2"] == "OPEN AFTER TARGETED SEARCH"
    assert summary["A303656"] == "UNRESOLVED"
    assert summary["truth"]["mismatches"] == 0
    assert summary["contraction"]["mismatches"] == 0
    if args.replay_results:
        actual = args.replay_results.resolve()
        assert {p.name for p in actual.glob("*.json")} == GENERATED
        for name in GENERATED:
            assert (ROOT / "results" / name).read_bytes() == (actual / name).read_bytes(), name
    print(f"PASS: {len(manifest['files'])} files; scoped invariants; replay={bool(args.replay_results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
