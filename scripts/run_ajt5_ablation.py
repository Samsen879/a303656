#!/usr/bin/env python3
"""Fresh deterministic R3 generation; preserve any mismatch and stop (exit 2)."""
import argparse
import csv
import json
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verify_ajt5_ablation import (BASE, SOURCES, compare, compute, controls, digest,  # noqa: E402
                                  frozen_inputs, verify_directory)
from verify_ajt5_reports import require  # noqa: E402


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--emit-states", action="store_true", help="write canonical states.jsonl in work directory, outside committed evidence")
    args = parser.parse_args()
    work = args.work_dir.resolve()
    require(not work.exists(), "choose a fresh work directory")
    evidence = work / "evidence"
    evidence.mkdir(parents=True)
    start = time.monotonic()
    selected, certs, bindings = frozen_inputs()
    try:
        if args.emit_states:
            with (work / "states.jsonl").open("wb") as f:
                report, keys = compute(selected, f)
        else:
            report, keys = compute(selected)
    except ValueError as error:
        write_json(evidence / "discrepancy.json", {"base": BASE, "error": str(error), "input_sha256": bindings})
        raise
    write_json(evidence / "report.json", report)
    with (evidence / "keys.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(keys[0]))
        writer.writeheader(); writer.writerows(keys)
    write_json(evidence / "controls.json", controls(certs))
    write_json(evidence / "receipt.json", {"schema": 1, "base": BASE, "input_sha256": bindings,
               "sources_sha256": {name: digest(ROOT / name) for name in SOURCES},
               "command": ["python3", "scripts/run_ajt5_ablation.py", "--work-dir", str(args.work_dir)]
                          + (["--emit-states"] if args.emit_states else []),
               "python": platform.python_version(), "single_thread": True,
               "generation_seconds": round(time.monotonic() - start, 6),
               "a303656": "UNRESOLVED", "scope": "fixed 534 R2 PB2 keys plus explicitly named small controls; no scan enlargement"})
    comparison = compare(report)
    write_json(evidence / "comparison.json", comparison)
    write_json(evidence / "manifest.json", {p.name: digest(p) for p in sorted(evidence.iterdir())})
    if comparison["status"] != "MATCH":
        print("MISMATCH preserved at " + str(evidence), file=sys.stderr)
        return 2
    print(json.dumps(verify_directory(evidence), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
