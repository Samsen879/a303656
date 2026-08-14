#!/usr/bin/env python3
"""Compare two completed all-prime factor-sieve runs, including chunk internals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MATHEMATICAL_KEYS = (
    "low", "high", "C", "D", "finite_bound_3_rhs", "finite_bound_5_rhs",
    "max_odd", "admissible_pair_count_at_high", "distinct_shift_count_at_high",
    "integers_tested", "shifts_processed_before_termination",
    "factor_groups_processed", "candidate_count", "candidates",
    "first_failure_histogram", "factor_groups",
)


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    first = read_json(args.first)
    second = read_json(args.second)

    summary_keys = (
        "low", "high", "max_odd", "complete_gapless_coverage",
        "integers_tested", "candidate_count", "candidates",
    )
    mismatches: list[str] = []
    for key in summary_keys:
        if first.get(key) != second.get(key):
            mismatches.append(f"summary:{key}")
    if not first.get("complete_gapless_coverage") or not second.get("complete_gapless_coverage"):
        mismatches.append("summary:not_complete_gapless")

    chunks_a = first.get("chunks", [])
    chunks_b = second.get("chunks", [])
    if len(chunks_a) != len(chunks_b):
        mismatches.append("summary:chunk_count")
    compared = 0
    details: list[dict[str, object]] = []
    for index, (a, b) in enumerate(zip(chunks_a, chunks_b)):
        row_mismatches: list[str] = []
        if (a.get("low"), a.get("high")) != (b.get("low"), b.get("high")):
            row_mismatches.append("interval")
        ja = read_json(resolve(root, str(a["json"])))
        jb = read_json(resolve(root, str(b["json"])))
        for key in MATHEMATICAL_KEYS:
            if ja.get(key) != jb.get(key):
                row_mismatches.append(key)
        if row_mismatches:
            mismatches.extend(f"chunk[{index}]:{name}" for name in row_mismatches)
        details.append({
            "index": index,
            "low": str(a.get("low")),
            "high": str(a.get("high")),
            "mismatches": row_mismatches,
            "candidate_count": ja.get("candidate_count"),
            "histogram_entries": len(ja.get("first_failure_histogram", [])),
        })
        compared += 1

    result = {
        "schema": "a303656-factor-run-comparison-v1",
        "first": str(args.first),
        "second": str(args.second),
        "summary_interval": [str(first.get("low")), str(first.get("high"))],
        "max_odd": first.get("max_odd"),
        "chunks_compared": compared,
        "candidate_count": first.get("candidate_count"),
        "mismatches": mismatches,
        "full_mathematical_output_match": not mismatches,
        "details": details,
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"chunks_compared={compared}")
    print(f"candidate_count={first.get('candidate_count')}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"full_mathematical_output_match={str(not mismatches).lower()}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
