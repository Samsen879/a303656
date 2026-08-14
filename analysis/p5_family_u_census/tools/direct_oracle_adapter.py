#!/usr/bin/env python3
"""Frozen source adapter for the factorization-free all-point direct oracle."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / "analysis/p4_holdout_census/tools"))
from direct_oracle_adapter import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())

