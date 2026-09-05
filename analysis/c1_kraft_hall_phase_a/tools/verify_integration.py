#!/usr/bin/env python3
"""Fast repository-native integrity and theorem-scope verification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for item in manifest["files"]:
        path = ROOT / item["path"]
        assert path.is_file() and path.stat().st_size == item["size"] and digest(path) == item["sha256"]
    proof = json.loads((ROOT / "results/theorem_verification.json").read_text())
    arithmetic = proof["arithmetic"]
    combinatorics = proof["combinatorics"]
    assert proof["status"] == "PASS"
    assert arithmetic["coordinate3_min_rigid_depth"] == 4
    assert arithmetic["rigid_only_minimum_rows"] == 81
    assert arithmetic["dynamic_allowed_minimum_rows"] == 21
    assert arithmetic["coordinate5_beta1_Y0_joint_rows"] == 10
    assert arithmetic["coordinate7_beta1_Y0_joint_rows"] == 8
    assert combinatorics["all_cylinder_subsets"] == 4096
    assert combinatorics["corrected_branch_inequalities_checked"] == 8748
    authority = json.loads((ROOT / "results/source_authority.json").read_text())
    assert authority["project"] == "PAUSED"
    assert authority["active_promoted_route"] == "NONE"
    assert authority["a303656"] == "UNRESOLVED"
    print(f"PASS: {len(manifest['files'])} files and scoped Kraft-Hall invariants verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
