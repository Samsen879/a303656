#!/usr/bin/env python3
"""Offline custody and independent replay for the Thread 3 audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONOPTIMIZE", None)
    result = subprocess.run(command, cwd=ROOT, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=180)
    require(result.returncode == 0, result.stdout)
    return result


def without_environment(value: dict) -> dict:
    result = dict(value)
    result.pop("environment", None)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-producer", action="store_true")
    parser.add_argument("--producer-python", default=sys.executable)
    args = parser.parse_args()

    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        name = name.strip()
        require(sha256(ROOT / name) == expected, "integration custody: " + name)

    producer = ROOT / "source" / "producer_packet"
    for line in (producer / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        name = name.strip()
        require(sha256(producer / name) == expected, "producer custody: " + name)

    with tempfile.TemporaryDirectory(prefix="a303656_thread3_audit_") as tmp:
        tmp_path = Path(tmp)
        independent_output = tmp_path / "reference_audit.json"
        run([sys.executable, "-B", str(ROOT / "tools" / "reference_audit.py"),
             "--limit", "5000", "--output", str(independent_output)])
        expected_independent = ROOT / "results" / "reference_audit.json"
        require(independent_output.read_bytes() == expected_independent.read_bytes(),
                "independent replay differs from committed result")

        producer_status = "NOT_REQUESTED"
        if args.with_producer:
            producer_output = tmp_path / "producer_certificate.json"
            run([args.producer_python, "-B", str(producer / "verify_thread3.py"),
                 "--N", "20000", "--output", str(producer_output)])
            expected = json.loads((producer / "certificate.json").read_text(encoding="utf-8"))
            actual = json.loads(producer_output.read_text(encoding="utf-8"))
            require(without_environment(actual) == without_environment(expected),
                    "producer mathematical payload differs")
            producer_status = "PASS"

    print(json.dumps({
        "a303656": "UNRESOLVED",
        "independent_replay": "PASS",
        "producer_custody": "PASS",
        "producer_replay": producer_status,
        "scope": "finite checks and custody; infinite theorems stand on PROOF_AUDIT.md",
        "verdict": "PASS",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
