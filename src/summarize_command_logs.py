#!/usr/bin/env python3
"""Collapse run_logged_command.sh records into one concise JSON manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def elapsed_seconds(time_text: str) -> str | None:
    match = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*([^\n]+)", time_text)
    return None if match is None else match.group(1).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError(f"refusing to overwrite manifest: {args.output}")
    records = []
    for directory in sorted(path for path in args.log_root.iterdir() if path.is_dir()):
        required = {
            name: directory / name
            for name in ("command.txt", "stdout.log", "stderr.log", "return_code.txt", "time.txt")
        }
        missing = [name for name, path in required.items() if not path.is_file()]
        if missing:
            raise ValueError(f"incomplete command record {directory.name}: {missing}")
        command_lines = required["command.txt"].read_text(encoding="utf-8").splitlines()
        command = next((line.removeprefix("command=") for line in command_lines if line.startswith("command=")), None)
        if command is None:
            raise ValueError(f"command missing from {directory}")
        rc_text = required["return_code.txt"].read_text(encoding="utf-8").strip()
        records.append(
            {
                "tag": directory.name,
                "command_shell_escaped": command,
                "return_code": int(rc_text),
                "elapsed_wall_clock": elapsed_seconds(required["time.txt"].read_text(encoding="utf-8")),
                "stdout_bytes": required["stdout.log"].stat().st_size,
                "stdout_sha256": sha256(required["stdout.log"]),
                "stderr_bytes": required["stderr.log"].stat().st_size,
                "stderr_sha256": sha256(required["stderr.log"]),
            }
        )
    value = {
        "schema": "a303656-concise-command-manifest-v1",
        "raw_log_root": str(args.log_root),
        "record_count": len(records),
        "nonzero_return_codes": [
            {"tag": row["tag"], "return_code": row["return_code"]}
            for row in records
            if row["return_code"] != 0
        ],
        "records": records,
    }
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"COMMAND_MANIFEST_PASS records={len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
