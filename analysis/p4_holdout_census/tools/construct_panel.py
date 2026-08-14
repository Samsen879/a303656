#!/usr/bin/env python3
"""Construct the deterministic fresh-class panel without evaluating T(n)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from holdout_common import HoldoutError, atomic_json, construct_panel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        panel = construct_panel(args.root.resolve())
        atomic_json(args.output, panel)
        print(panel["status"])
        print(f"r={panel['r']}")
        print(f"class_count={panel.get('class_count', 0)}")
        print(f"point_count={panel.get('point_count', 0)}")
        return 0 if panel["r"] >= 3 else 3
    except (HoldoutError, OSError, ValueError) as exc:
        print(f"construct_panel: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
