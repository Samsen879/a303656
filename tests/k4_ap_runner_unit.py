#!/usr/bin/env python3
"""Narrow regression tests for the bounded K4 pilot runner."""

from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "src"))

import k4_ap_run  # noqa: E402


def main() -> int:
    row = {"h": 0, "k": 0, "n": 240000005594, "T": 16, "active_pairs": 407}
    with tempfile.TemporaryDirectory(prefix="k4_ap_runner_unit_") as directory:
        path = Path(directory) / "direct_panel.csv"
        k4_ap_run.write_direct_panel(path, [row])
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            assert reader.fieldnames == ["h", "k", "n", "active_pairs", "expected_T"]
            assert list(reader) == [
                {
                    "h": "0",
                    "k": "0",
                    "n": "240000005594",
                    "active_pairs": "407",
                    "expected_T": "16",
                }
            ]
    print("K4_AP_RUNNER_UNIT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
