#!/usr/bin/env python3
"""Audit and aggregate two independent direct two-square chunk directories."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_chunks(directory: Path) -> list[dict[str, object]]:
    files = sorted(directory.glob("chunk_*.json"))
    rows: list[dict[str, object]] = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        candidates = [str(value) for value in data["candidates"]]
        if int(data["candidate_count"]) != len(candidates):
            raise ValueError(f"candidate_count mismatch: {path}")
        candidate_path = path.with_suffix(".candidates")
        if not candidate_path.exists():
            candidate_path = path.with_suffix(".candidates.txt")
        if candidate_path.exists() and candidate_path.read_text(encoding="utf-8").split() != candidates:
            raise ValueError(f"candidate file mismatch: {candidate_path}")
        rows.append({
            "path": str(path),
            "sha256": sha256(path),
            "method": data["method"],
            "low": str(data["low"]),
            "high": str(data["high"]),
            "C": int(data["C"]),
            "D": int(data["D"]),
            "three_power_next_plus_one": str(data["three_power_next_plus_one"]),
            "five_power_next_plus_one": str(data["five_power_next_plus_one"]),
            "strict_domain_inequalities_checked": bool(data["strict_domain_inequalities_checked"]),
            "admissible_rectangle_pair_count_at_high": int(data["admissible_rectangle_pair_count_at_high"]),
            "distinct_shift_count_at_high": int(data["distinct_shift_count_at_high"]),
            "duplicate_pair_count": int(data["duplicate_pair_count"]),
            "integers_tested": int(data["integers_tested"]),
            "shifts_processed_before_termination": int(data["shifts_processed_before_termination"]),
            "unordered_square_pairs_enumerated": int(data["unordered_square_pairs_enumerated"]),
            "candidate_count": len(candidates),
            "candidates": candidates,
            "elapsed_seconds": float(data["elapsed_seconds"]),
        })
    rows.sort(key=lambda row: int(row["low"]))
    return rows


def gapless(rows: list[dict[str, object]], low: int, high: int) -> bool:
    return (
        bool(rows)
        and int(rows[0]["low"]) == low
        and int(rows[-1]["high"]) == high
        and all(int(rows[i]["high"]) + 1 == int(rows[i + 1]["low"]) for i in range(len(rows) - 1))
        and sum(int(row["integers_tested"]) for row in rows) == high - low + 1
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-dir", type=Path, required=True)
    parser.add_argument("--y-dir", type=Path, required=True)
    parser.add_argument("--low", type=int, required=True)
    parser.add_argument("--high", type=int, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    xrows = read_chunks(args.x_dir)
    yrows = read_chunks(args.y_dir)
    mismatches: list[str] = []
    if not gapless(xrows, args.low, args.high):
        mismatches.append("x_not_gapless")
    if not gapless(yrows, args.low, args.high):
        mismatches.append("y_not_gapless")
    if len(xrows) != len(yrows):
        mismatches.append("chunk_count")

    compare_keys = (
        "low", "high", "C", "D", "three_power_next_plus_one",
        "five_power_next_plus_one", "strict_domain_inequalities_checked",
        "admissible_rectangle_pair_count_at_high", "distinct_shift_count_at_high",
        "duplicate_pair_count", "integers_tested", "shifts_processed_before_termination",
        "unordered_square_pairs_enumerated", "candidate_count", "candidates",
    )
    chunk_checks: list[dict[str, object]] = []
    for index, (xrow, yrow) in enumerate(zip(xrows, yrows)):
        differences = [key for key in compare_keys if xrow[key] != yrow[key]]
        if differences:
            mismatches.extend(f"chunk[{index}]:{key}" for key in differences)
        chunk_checks.append({
            "index": index,
            "low": xrow["low"],
            "high": xrow["high"],
            "mismatches": differences,
            "candidate_count": xrow["candidate_count"],
            "unordered_square_pairs_enumerated": xrow["unordered_square_pairs_enumerated"],
            "x_json": xrow["path"],
            "x_sha256": xrow["sha256"],
            "y_json": yrow["path"],
            "y_sha256": yrow["sha256"],
        })

    candidates_x = [value for row in xrows for value in row["candidates"]]
    candidates_y = [value for row in yrows for value in row["candidates"]]
    if candidates_x != candidates_y:
        mismatches.append("aggregate_candidates")
    complete = not mismatches
    payload = {
        "schema": "a303656-direct-two-squares-dual-aggregate-v1",
        "low": str(args.low),
        "high": str(args.high),
        "chunk_count_x": len(xrows),
        "chunk_count_y": len(yrows),
        "integers_tested_x": sum(int(row["integers_tested"]) for row in xrows),
        "integers_tested_y": sum(int(row["integers_tested"]) for row in yrows),
        "candidate_count_x": len(candidates_x),
        "candidate_count_y": len(candidates_y),
        "candidates_x": candidates_x,
        "candidates_y": candidates_y,
        "unordered_square_pairs_enumerated_x": sum(int(row["unordered_square_pairs_enumerated"]) for row in xrows),
        "unordered_square_pairs_enumerated_y": sum(int(row["unordered_square_pairs_enumerated"]) for row in yrows),
        "elapsed_seconds_sum_x": sum(float(row["elapsed_seconds"]) for row in xrows),
        "elapsed_seconds_sum_y": sum(float(row["elapsed_seconds"]) for row in yrows),
        "complete_gapless_independent_crosscheck": complete,
        "mismatches": mismatches,
        "chunks": chunk_checks,
        "classification": (
            "INDEPENDENTLY REPRODUCIBLE EXACT EXHAUSTIVE FINITE COMPUTATION: EVERY n IN INTERVAL HAS A REPRESENTATION"
            if complete and not candidates_x else
            "EXACT CANDIDATES REQUIRE INDEPENDENT CERTIFICATE VERIFICATION"
            if complete else "INCOMPLETE OR MISMATCHED"
        ),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"chunk_count_x={len(xrows)}")
    print(f"chunk_count_y={len(yrows)}")
    print(f"complete_gapless_independent_crosscheck={str(complete).lower()}")
    print(f"candidate_count_x={len(candidates_x)}")
    print(f"candidate_count_y={len(candidates_y)}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"unordered_square_pairs_x={payload['unordered_square_pairs_enumerated_x']}")
    print(f"unordered_square_pairs_y={payload['unordered_square_pairs_enumerated_y']}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
