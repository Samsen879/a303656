#!/usr/bin/env python3
"""Fail-closed CSV parser tests for the read-only T(n) analysis."""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def invoke(python: str, analyzer: Path, path: Path, low: int, high: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            python,
            str(analyzer),
            "validate-counts",
            "--counts",
            str(path),
            "--low",
            str(low),
            "--high",
            str(high),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--analyzer", type=Path, required=True)
    args = parser.parse_args()

    fixtures = {
        "valid": ("n,T\n2,1\n3,1\n4,2\n", True),
        "missing": ("n,T\n2,1\n4,2\n", False),
        "duplicate": ("n,T\n2,1\n2,1\n4,2\n", False),
        "out_of_order": ("n,T\n3,1\n2,1\n4,2\n", False),
        "out_of_range": ("n,T\n2,1\n3,1\n4,2\n5,3\n", False),
        "malformed": ("n,T\n2,1,extra\n3,1\n4,2\n", False),
        "bad_header": ("T,n\n1,2\n1,3\n2,4\n", False),
        "leading_zero": ("n,T\n02,1\n3,1\n4,2\n", False),
        "signed": ("n,T\n2,1\n3,-1\n4,2\n", False),
    }
    with tempfile.TemporaryDirectory(prefix="a303656-tn-low-tail-parser-") as text:
        root = Path(text)
        observed_rejections = []
        for name, (contents, should_pass) in fixtures.items():
            path = root / f"{name}.csv"
            path.write_text(contents, encoding="utf-8")
            completed = invoke(args.python, args.analyzer, path, 2, 5)
            if should_pass:
                if completed.returncode != 0 or "COUNTS_VALID rows=3" not in completed.stdout:
                    raise AssertionError(f"valid fixture failed: {completed.stderr}")
            else:
                if completed.returncode == 0 or "LOW_TAIL_ANALYSIS_ERROR" not in completed.stderr:
                    raise AssertionError(f"{name} fixture did not fail closed")
                observed_rejections.append(name)
    print("TN_LOW_TAIL_FAIL_CLOSED_TESTS_PASS")
    print("expected_rejections=" + ",".join(observed_rejections))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
