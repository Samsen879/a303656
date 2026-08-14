#!/usr/bin/env python3
"""Small exact cross-check of both C++ direct scanners against Python brute force."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = Path(os.environ.get("A303656_BIN", ROOT / "bin"))


def powers(base: int, limit: int) -> list[int]:
    out: list[int] = []
    x = 1
    while x <= limit:
        out.append(x)
        x *= base
    return out


def brute_candidates(low: int, high: int) -> list[int]:
    shifts = sorted({x + y for x in powers(3, high) for y in powers(5, high) if x + y <= high})
    square_sums: set[int] = set()
    a = 0
    while a * a <= high:
        b = a
        while a * a + b * b <= high:
            square_sums.add(a * a + b * b)
            b += 1
        a += 1
    return [
        n for n in range(low, high + 1)
        if not any(s <= n and n - s in square_sums for s in shifts)
    ]


def run(binary: str, low: int, high: int, C: int, D: int, directory: Path) -> tuple[int, list[int], dict]:
    js = directory / f"{binary}.json"
    cand = directory / f"{binary}.txt"
    cp = subprocess.run([
        str(BIN / binary), "--low", str(low), "--high", str(high),
        "--C", str(C), "--D", str(D), "--json", str(js),
        "--candidates", str(cand), "--quiet",
    ], text=True, capture_output=True)
    values = [int(x) for x in cand.read_text().split()] if cand.exists() else []
    return cp.returncode, values, json.loads(js.read_text())


with tempfile.TemporaryDirectory() as td_text:
    td = Path(td_text)
    cases = [(1, 1, 0, 0), (2, 500, 5, 3), (97, 2000, 6, 4)]
    for low, high, C, D in cases:
        expected = brute_candidates(low, high)
        xrc, xvals, xjson = run("search_twosquares_bitset", low, high, C, D, td)
        yrc, yvals, yjson = run("search_twosquares_clean", low, high, C, D, td)
        expected_rc = 0 if expected else 1
        assert xrc == yrc == expected_rc
        assert xvals == yvals == expected
        assert xjson["unordered_square_pairs_enumerated"] == yjson["unordered_square_pairs_enumerated"]
        assert xjson["candidate_count"] == yjson["candidate_count"] == len(expected)

print("DIRECT_SMALL_CROSSCHECK_PASS")
