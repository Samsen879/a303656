#!/usr/bin/env python3
"""Run all deterministic reference checks to a separate, caller-selected path."""
from pathlib import Path
import argparse
from reference import run_all

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run_all(args.output_dir)
