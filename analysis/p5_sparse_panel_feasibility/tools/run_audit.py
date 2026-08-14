#!/usr/bin/env python3
"""Source/results replay runner with preserved return codes."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run(command: list[str], root: Path) -> dict:
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return {"command": command, "return_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    tools = Path(__file__).resolve().parent
    tests = tools.parent / "tests"
    output.mkdir(parents=True, exist_ok=True)
    commands = {
        "unit_tests": [sys.executable, str(tests / "test_exact.py")],
        "builder": [sys.executable, str(tools / "builder.py"), "--root", str(root), "--output", str(output), "--source-commit", args.source_commit],
        "verifier_pre_corruption": [sys.executable, str(tools / "verifier.py"), "--root", str(root), "--results", str(output), "--output", str(output / "verification_report.json")],
        "corruption_tests": [sys.executable, str(tests / "corruption_tests.py"), "--root", str(root), "--results", str(output), "--output", str(output / "corruption_tests.json")],
    }
    records = {}
    for name in ("unit_tests", "builder", "verifier_pre_corruption", "corruption_tests"):
        records[name] = run(commands[name], root)
        if records[name]["return_code"] != 0:
            break
    compact = {name: {"command": record["command"], "return_code": record["return_code"], "stdout_sha256": __import__("hashlib").sha256(record["stdout"].encode()).hexdigest(), "stderr_sha256": __import__("hashlib").sha256(record["stderr"].encode()).hexdigest()} for name, record in records.items()}
    (output / "return_codes.json").write_text(json.dumps({"schema": "a303656-p5-sparse-return-codes-v1", "commands": compact}, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if all(record["return_code"] == 0 for record in records.values()) and len(records) == len(commands):
        final = run([sys.executable, str(tools / "verifier.py"), "--root", str(root), "--results", str(output), "--output", str(output / "verification_report.json")], root)
        print(final["stdout"], end="")
        if final["stderr"]:
            print(final["stderr"], file=sys.stderr, end="")
        return final["return_code"]
    for name, record in records.items():
        if record["return_code"] != 0:
            print(f"{name} failed rc={record['return_code']}", file=sys.stderr)
            print(record["stderr"], file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
