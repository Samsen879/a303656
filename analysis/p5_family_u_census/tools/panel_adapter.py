#!/usr/bin/env python3
"""CLI for frozen Design C reconstruction; never evaluates T."""
import argparse
import sys
from pathlib import Path

from common import CensusError, atomic_json, reconstruct_panel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        panel = reconstruct_panel(args.root)
        atomic_json(args.output, panel)
        print(f"FROZEN_FAMILY_U_PANEL_PASS descriptions={panel['description_count']} integers={panel['distinct_integer_count']}")
        return 0
    except (CensusError, OSError, ValueError) as exc:
        print(f"panel_adapter: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

