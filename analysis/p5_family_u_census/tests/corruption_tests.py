#!/usr/bin/env python3
"""Run every declared mutation as a subprocess and require nonzero status."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "analysis/p5_family_u_census/tools"))
from common import atomic_json  # noqa: E402
from verifier import MUTATIONS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for name in MUTATIONS:
        command = [sys.executable, str(ROOT / "analysis/p5_family_u_census/tools/verifier.py"), "--root", str(args.root), "--mutation-case", name]
        if args.artifact:
            command += ["--artifact", str(args.artifact)]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        rows.append({"mutation": name, "return_code": process.returncode, "rejected": process.returncode != 0, "stderr": process.stderr.decode(errors="replace").strip()})
    atomic_json(args.output, {"schema": "a303656-p5-family-u-corruption-tests-v1", "all_rejected": all(r["rejected"] for r in rows), "tests": rows})
    if not all(r["rejected"] for r in rows):
        print("corruption_tests: one or more mutations were accepted", file=sys.stderr)
        return 1
    print(f"CORRUPTION_TESTS_PASS count={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
