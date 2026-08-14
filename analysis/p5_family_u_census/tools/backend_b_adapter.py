#!/usr/bin/env python3
"""Frozen source adapter selecting independent exact Backend B."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / "analysis/p4_holdout_census/tools"))
from backend_adapter import main  # noqa: E402

if __name__ == "__main__":
    sys.argv[1:1] = ["--backend", "B"]
    raise SystemExit(main())

