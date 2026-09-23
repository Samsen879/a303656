#!/usr/bin/env python3
"""Offline full replay for the Thread 4 L5,3 falsification."""

from __future__ import annotations

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


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONOPTIMIZE", None)
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=180)
    require(result.returncode == 0, result.stdout)
    return result


def main() -> int:
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        require(sha256(ROOT / name.strip()) == expected, "integration custody: " + name)

    producer = ROOT / "source" / "producer_packet"
    producer_manifest = json.loads((producer / "SHA256.json").read_text(encoding="utf-8"))
    for name, expected in producer_manifest.items():
        require(sha256(producer / name) == expected, "producer custody: " + name)

    with tempfile.TemporaryDirectory(prefix="a303656_l53_replay_") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "support_scanner"
        support = tmp_path / "support_scan.json"
        criterion = tmp_path / "membership_details.json"
        certificate = tmp_path / "l53_falsification_certificate.json"
        producer_output = tmp_path / "producer_laboratory.json"

        run(["g++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
             str(ROOT / "tools" / "support_scanner.cpp"), "-o", str(binary)])
        run([str(binary), "7963079", "44922133", str(support)])
        require(support.read_bytes() == (ROOT / "results" / "support_scan.json").read_bytes(),
                "Engine A replay differs")

        run([sys.executable, "-B", str(ROOT / "tools" / "criterion_checker.py"),
             "--output", str(criterion)])
        require(criterion.read_bytes() == (ROOT / "results" / "membership_details.json").read_bytes(),
                "Engine B replay differs")

        run([sys.executable, "-B", str(ROOT / "tools" / "build_certificate.py"),
             "--support", str(support), "--criterion", str(criterion),
             "--output", str(certificate)])
        require(certificate.read_bytes() ==
                (ROOT / "results" / "l53_falsification_certificate.json").read_bytes(),
                "certificate replay differs")

        run([sys.executable, "-B", str(producer / "verify_thread4.py"),
             "--output", str(producer_output)])
        require(producer_output.read_bytes() == (producer / "laboratory.json").read_bytes(),
                "historical producer replay differs")

        run([sys.executable, "-B", "-m", "unittest", "discover", "-s",
             str(ROOT / "tests"), "-p", "test_*.py"])

    print(json.dumps({
        "a303656": "UNRESOLVED",
        "certificate": "L5,3 IS FALSE",
        "criterion_engine": "PASS",
        "direct_support_engine": "PASS",
        "first_failure": 7_963_079,
        "first_failure_exhaustive": True,
        "historical_packet_replay": "PASS",
        "regression_tests": "PASS",
        "verdict": "CERTIFIED FALSE",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
