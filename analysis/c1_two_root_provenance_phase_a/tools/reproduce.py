#!/usr/bin/env python3
"""Full replay into an explicit external output directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def unit_summary(output: Path) -> None:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "passed": result.wasSuccessful(),
    }
    (output / "unit_test_summary.json").write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    if not result.wasSuccessful():
        raise RuntimeError("unit test failure")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    root = ROOT.resolve()
    if output == root or root in output.parents:
        raise SystemExit("output directory must be outside the integration tree")
    output.mkdir(parents=True, exist_ok=False)
    results = output / "results"
    catalogs = output / "catalogs"
    results.mkdir()
    catalogs.mkdir()

    env = dict(
        os.environ,
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONHASHSEED="0",
        A303656_OUTPUT_DIR=str(results),
        A303656_CATALOG_DIR=str(catalogs),
    )
    for script in (
        "run_small_models.py",
        "run_arithmetic.py",
        "charge_filter.py",
        "rigid_blocker_audit.py",
    ):
        print(f"RUN {script}", flush=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / script)], env=env, check=True)
    unit_summary(results)

    committed = ROOT / "results"
    generated_names = sorted(path.name for path in results.glob("*.json"))
    for name in generated_names:
        expected = committed / name
        if not expected.is_file() or expected.read_bytes() != (results / name).read_bytes():
            raise RuntimeError(f"compact result mismatch: {name}")

    receipt = json.loads((committed / "generated_catalog_receipt.json").read_text())
    for item in receipt["catalogs"]:
        path = catalogs / item["filename"]
        if digest(path) != item["sha256"] or path.stat().st_size != item["size"]:
            raise RuntimeError(f"generated catalog mismatch: {item['filename']}")

    print(f"FULL REPOSITORY-NATIVE REPLAY PASS: {len(generated_names)} compact results")
    print(f"Generated catalogs retained only under: {catalogs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
