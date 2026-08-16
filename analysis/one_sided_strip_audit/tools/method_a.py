#!/usr/bin/env python3
"""Direct square-pair oracle followed by exact shifted integer bitsets."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    import numpy as np
except ModuleNotFoundError as exc:  # fail before allocating large objects
    raise SystemExit("NumPy is required; install the repository requirements.txt") from exc

INF = np.uint8(255)


def powers_le(base: int, limit: int) -> list[int]:
    out, value = [], 1
    while value <= limit:
        out.append(value)
        value *= base
    return out


def direct_s2(N: int) -> tuple[np.ndarray, int]:
    roots = np.arange(math.isqrt(N) + 1, dtype=np.int64)
    squares = roots * roots
    s2 = np.zeros(N + 1, dtype=np.bool_)
    for a2 in squares:
        count = int(np.searchsorted(squares, N - int(a2), side="right"))
        s2[int(a2) + squares[:count]] = True
    packed = np.packbits(s2, bitorder="little")
    return s2, int.from_bytes(packed.tobytes(), "little")


def minimum_outer(N: int, s2_bits: int, outer: list[int], inner: list[int]) -> np.ndarray:
    bit_count = N + 1
    byte_count = (bit_count + 7) // 8
    universe = (1 << bit_count) - 1
    assigned = 0
    answer = np.full(bit_count, INF, dtype=np.uint8)
    for exponent, outer_power in enumerate(outer):
        level = 0
        for inner_power in inner:
            shift = outer_power + inner_power
            if shift > N:
                break
            level |= s2_bits << shift
        new = (level & universe) & (universe ^ assigned)
        if new:
            raw = new.to_bytes(byte_count, "little")
            mask = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="little")[:bit_count]
            answer[mask.astype(bool, copy=False)] = exponent
            assigned |= new
    return answer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    if args.N < 2:
        raise SystemExit("N must be at least 2")
    args.outdir.mkdir(parents=True, exist_ok=True)
    p3 = powers_le(3, args.N - 1)
    p5 = powers_le(5, args.N - 1)
    s2, s2_bits = direct_s2(args.N)
    c3 = minimum_outer(args.N, s2_bits, p3, p5)
    c5 = minimum_outer(args.N, s2_bits, p5, p3)
    s2.astype(np.uint8, copy=False).tofile(args.outdir / "method_a_S2.uint8")
    c3.tofile(args.outdir / "method_a_C3.uint8")
    c5.tofile(args.outdir / "method_a_C5.uint8")
    summary = {
        "N": args.N,
        "method": "direct_square_pairs_then_integer_bitset_shifts",
        "s2_count": int(s2.sum()),
        "uncovered_C3": int(np.count_nonzero(c3[2:] == INF)),
        "uncovered_C5": int(np.count_nonzero(c5[2:] == INF)),
        "max_C3": int(c3[2:].max()),
        "max_C5": int(c5[2:].max()),
    }
    (args.outdir / "method_a_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
