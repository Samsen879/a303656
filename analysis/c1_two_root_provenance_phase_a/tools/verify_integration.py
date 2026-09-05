#!/usr/bin/env python3
"""Fast integrity and scoped-invariant verification for the integration."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    failures = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or path.stat().st_size != item["size"] or digest(path) != item["sha256"]:
            failures.append(item["path"])
    if failures:
        raise SystemExit("integrity mismatch: " + ", ".join(failures))

    inventory = json.loads((ROOT / "results/rigid_blocker_inventory.json").read_text())
    assert [row["prime"] for row in inventory["nonregular_rows"]] == [20771, 40487]
    assert inventory["paired_blocker_assignment"] == {"20771": 5, "40487": 653}
    assert inventory["nonregular_rows"][0]["order"] == 10385
    assert inventory["nonregular_rows"][1]["order"] == 40486
    assert 5 % 4 != 3 and 653 % 4 != 3
    for load in inventory["loads"]:
        assert load["maximum_forbidden_digits"] < load["coordinate"]

    boundary = json.loads((ROOT / "results/blocker_boundary_resource.json").read_text())
    assert boundary["prime"] == 1645333507
    assert boundary["order"] == 1645333506
    assert boundary["order_factorization"] == {"2": 1, "3": 3, "30469139": 1}
    assert boundary["structurally_ineligible_odd_order_factors"] == []

    receipt = json.loads((ROOT / "results/generated_catalog_receipt.json").read_text())
    assert [item["prime"] for item in receipt["catalogs"]] == [67, 20771]
    assert not (ROOT / "catalogs").exists()
    print(f"PASS: {len(manifest['files'])} files and scoped blocker invariants verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
