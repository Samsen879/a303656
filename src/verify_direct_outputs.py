#!/usr/bin/env python3
"""Audit every stored direct two-square exact finite-search result.

This checker does not trust aggregate prose.  It reopens both independently
written scanner outputs, checks the exact exponent-domain inequalities,
interval coverage, candidate files, and all mathematical accounting fields
needed to compare the x-outer and y-outer implementations.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
COMPARE_KEYS = (
    "low", "high", "C", "D", "three_power_next_plus_one",
    "five_power_next_plus_one", "strict_domain_inequalities_checked",
    "admissible_rectangle_pair_count_at_high", "distinct_shift_count_at_high",
    "duplicate_pair_count", "integers_tested",
    "shifts_processed_before_termination", "unordered_square_pairs_enumerated",
    "candidate_count", "candidates",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_path(json_path: Path) -> Path:
    choices = (
        json_path.with_suffix(".candidates.txt"),
        json_path.with_suffix(".candidates"),
    )
    for path in choices:
        if path.is_file():
            return path
    raise AssertionError(f"missing candidate file for {json_path}")


def check_pair(x_path: Path, y_path: Path, low: int, high: int) -> tuple[int, int]:
    x = load(x_path)
    y = load(y_path)
    for key in COMPARE_KEYS:
        if x.get(key) != y.get(key):
            raise AssertionError(f"{x_path.name}: implementation mismatch in {key}")
    if (int(x["low"]), int(x["high"])) != (low, high):
        raise AssertionError(f"stored interval mismatch: {x_path}")
    if int(x["integers_tested"]) != high - low + 1:
        raise AssertionError(f"integer count mismatch: {x_path}")
    if not bool(x["strict_domain_inequalities_checked"]):
        raise AssertionError(f"domain check flag false: {x_path}")
    if not high < int(x["three_power_next_plus_one"]):
        raise AssertionError(f"C-domain inequality false: {x_path}")
    if not high < int(x["five_power_next_plus_one"]):
        raise AssertionError(f"D-domain inequality false: {x_path}")
    if int(x["candidate_count"]) != 0 or x["candidates"] != []:
        raise AssertionError(f"nonempty candidate result: {x_path}")
    for path, data in ((x_path, x), (y_path, y)):
        listed = candidate_path(path).read_text(encoding="utf-8").split()
        if listed != [str(v) for v in data["candidates"]]:
            raise AssertionError(f"candidate file mismatch: {path}")
    return int(x["integers_tested"]), int(x["unordered_square_pairs_enumerated"])


def json_rows(directory: Path) -> list[tuple[int, int, Path]]:
    rows: list[tuple[int, int, Path]] = []
    for path in directory.glob("*.json"):
        data = load(path)
        if "low" in data and "high" in data and "method" in data:
            rows.append((int(data["low"]), int(data["high"]), path))
    rows.sort()
    return rows


def audit_gapless(x_dir: Path, y_dir: Path, low: int, high: int, expected_chunks: int) -> tuple[int, int]:
    xrows = json_rows(x_dir)
    yrows = json_rows(y_dir)
    if len(xrows) != expected_chunks or len(yrows) != expected_chunks:
        raise AssertionError(f"wrong chunk count: {x_dir} / {y_dir}")
    if [(a, b) for a, b, _ in xrows] != [(a, b) for a, b, _ in yrows]:
        raise AssertionError("x/y interval manifests differ")
    intervals = [(a, b) for a, b, _ in xrows]
    if intervals[0][0] != low or intervals[-1][1] != high:
        raise AssertionError("gapless interval endpoints differ")
    if any(intervals[i][1] + 1 != intervals[i + 1][0] for i in range(len(intervals) - 1)):
        raise AssertionError("gap or overlap in direct chunks")
    tested = pairs = 0
    for (lo, hi, xp), (_, _, yp) in zip(xrows, yrows):
        n, q = check_pair(xp, yp, lo, hi)
        tested += n
        pairs += q
    if tested != high - low + 1:
        raise AssertionError("aggregate tested count mismatch")
    return tested, pairs


def audit_explicit_windows(manifest: Path, x_dir: Path, y_dir: Path) -> tuple[list[tuple[int, int]], int, int]:
    intervals: list[tuple[int, int]] = []
    tested = pairs = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        tag, low_text, high_text = line.split()
        low, high = int(low_text), int(high_text)
        n, q = check_pair(x_dir / f"window_{tag}.json", y_dir / f"window_{tag}.json", low, high)
        intervals.append((low, high))
        tested += n
        pairs += q
    return intervals, tested, pairs


def audit_named_windows(names: Iterable[str], x_dir: Path, y_dir: Path) -> tuple[list[tuple[int, int]], int, int]:
    intervals: list[tuple[int, int]] = []
    tested = pairs = 0
    for name in names:
        xp = x_dir / f"{name}.json"
        yp = y_dir / f"{name}.json"
        x = load(xp)
        low, high = int(x["low"]), int(x["high"])
        n, q = check_pair(xp, yp, low, high)
        intervals.append((low, high))
        tested += n
        pairs += q
    return intervals, tested, pairs


def assert_disjoint(intervals: list[tuple[int, int]]) -> None:
    ordered = sorted(intervals)
    for (_, previous_high), (next_low, _) in zip(ordered, ordered[1:]):
        if previous_high >= next_low:
            raise AssertionError(f"claimed distinct intervals overlap at {next_low}")


def main() -> int:
    intervals: list[tuple[int, int]] = []
    total_tested = 0
    total_pairs = 0

    # Continuous 1.6 billion integers after the previously known 240B bound.
    low, high = 240_000_000_001, 241_600_000_000
    tested, pairs = audit_gapless(
        ROOT / "output/direct/formal_1p6b_final/x",
        ROOT / "output/direct/formal_1p6b_final/y",
        low, high, 160,
    )
    intervals.append((low, high)); total_tested += tested; total_pairs += pairs

    # Twenty-one adaptive/far 10M windows.
    far_intervals, tested, pairs = audit_explicit_windows(
        ROOT / "output/direct/far_windows/windows.tsv",
        ROOT / "output/direct/far_windows/x",
        ROOT / "output/direct/far_windows/y",
    )
    intervals.extend(far_intervals); total_tested += tested; total_pairs += pairs

    # Three logarithmic 1M windows.
    log_intervals, tested, pairs = audit_named_windows(
        ("w1e12", "w1e13", "w1e14"),
        ROOT / "output/direct/log_windows/x",
        ROOT / "output/direct/log_windows/y",
    )
    intervals.extend(log_intervals); total_tested += tested; total_pairs += pairs

    # Windows crossing the exact points where C and D must increase.
    for name, low, high in (
        ("cross_C24_boundary", 282_420_000_001, 282_440_000_000),
        ("cross_D17_boundary", 762_930_000_001, 762_950_000_000),
    ):
        tested, pairs = audit_gapless(
            ROOT / f"output/direct/{name}/x",
            ROOT / f"output/direct/{name}/y",
            low, high, 2,
        )
        intervals.append((low, high)); total_tested += tested; total_pairs += pairs

    assert_disjoint(intervals)
    expected = 1_600_000_000 + 210_000_000 + 3_000_000 + 20_000_000 + 20_000_000
    if total_tested != expected:
        raise AssertionError(f"total distinct integer count {total_tested} != {expected}")

    print("DIRECT_OUTPUT_AUDIT_PASS")
    print("continuous_integer_count=1600000000")
    print("far_window_integer_count=210000000")
    print("logarithmic_window_integer_count=3000000")
    print("C_boundary_integer_count=20000000")
    print("D_boundary_integer_count=20000000")
    print(f"total_distinct_integer_count={total_tested}")
    print(f"matched_unordered_square_pairs={total_pairs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
