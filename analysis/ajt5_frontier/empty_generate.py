#!/usr/bin/env python3
"""Generate a fresh EMPTY_D integer proof with the R4 LP search (requires SciPy)."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from generate_ajt5_palette_proofs import catalogue, maximal3, solve


def generate():
    roots = sorted({5**d + 3**c for d in range(8) for c in range(13) if (d, c) != (7, 12)})
    groups = catalogue(roots)
    active = set(range(len(roots)))
    proofs = []
    for mask in maximal3(roots):
        key = hex(sum(1 << i for i in mask))
        proofs.append([key, solve(active - mask, groups, 15)])
    return {"no3": solve(active, groups, 16), "with3": proofs}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(generate(), separators=(",", ":")) + "\n", encoding="ascii")
