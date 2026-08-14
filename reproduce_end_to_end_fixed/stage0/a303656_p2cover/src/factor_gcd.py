#!/usr/bin/env python3
"""Factor a hexadecimal G_B and emit the text certificate consumed by verify_pruning."""
from __future__ import annotations
import argparse
import math
from pathlib import Path
from sympy import factorint, isprime


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("B", type=int)
    ap.add_argument("g_hex", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    G = int(args.g_hex.read_text().strip(), 16)
    factors = factorint(G)
    assert all(isprime(p) for p in factors)
    assert math.prod(int(p) ** int(e) for p, e in factors.items()) == G
    with args.output.open("w") as out:
        out.write(f"B {args.B}\n")
        for p, e in sorted(factors.items()):
            out.write(f"{int(p)} {int(e)}\n")
    print(f"B={args.B} gcd_bits={G.bit_length()} distinct_factors={len(factors)} max_factor={max(factors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
