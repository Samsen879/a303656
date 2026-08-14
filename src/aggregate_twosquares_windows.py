#!/usr/bin/env python3
"""Audit paired direct-two-square scans on an explicit list of disjoint windows."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--windows", type=Path, required=True)
    parser.add_argument("--x-dir", type=Path, required=True)
    parser.add_argument("--y-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    expected: list[tuple[str, int, int]] = []
    for line in args.windows.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        tag, low, high = line.split()
        expected.append((tag, int(low), int(high)))

    compare_keys = (
        "low", "high", "C", "D", "three_power_next_plus_one",
        "five_power_next_plus_one", "strict_domain_inequalities_checked",
        "admissible_rectangle_pair_count_at_high", "distinct_shift_count_at_high",
        "duplicate_pair_count", "integers_tested", "shifts_processed_before_termination",
        "unordered_square_pairs_enumerated", "candidate_count", "candidates",
    )
    records: list[dict[str, object]] = []
    mismatches: list[str] = []
    total_tested = 0
    total_candidates = 0
    for tag, low, high in expected:
        xp = args.x_dir / f"window_{tag}.json"
        yp = args.y_dir / f"window_{tag}.json"
        if not xp.is_file() or not yp.is_file():
            mismatches.append(f"window_{tag}:missing_file")
            continue
        x = json.loads(xp.read_text(encoding="utf-8"))
        y = json.loads(yp.read_text(encoding="utf-8"))
        differences = [key for key in compare_keys if x.get(key) != y.get(key)]
        if int(x["low"]) != low or int(x["high"]) != high:
            differences.append("x_interval_vs_manifest")
        if int(y["low"]) != low or int(y["high"]) != high:
            differences.append("y_interval_vs_manifest")
        xc = xp.with_suffix(".candidates")
        yc = yp.with_suffix(".candidates")
        if xc.is_file() and xc.read_text(encoding="utf-8").split() != [str(v) for v in x["candidates"]]:
            differences.append("x_candidate_file")
        if yc.is_file() and yc.read_text(encoding="utf-8").split() != [str(v) for v in y["candidates"]]:
            differences.append("y_candidate_file")
        if differences:
            mismatches.extend(f"window_{tag}:{name}" for name in differences)
        total_tested += high - low + 1
        total_candidates += int(x["candidate_count"])
        records.append({
            "tag": tag, "low": str(low), "high": str(high),
            "candidate_count": int(x["candidate_count"]),
            "unordered_square_pairs_enumerated": int(x["unordered_square_pairs_enumerated"]),
            "shifts_processed_before_termination": int(x["shifts_processed_before_termination"]),
            "mismatches": differences,
            "x_json": str(xp), "x_sha256": digest(xp),
            "y_json": str(yp), "y_sha256": digest(yp),
        })

    complete = len(records) == len(expected) and not mismatches
    payload = {
        "schema": "a303656-direct-two-squares-disjoint-windows-v1",
        "window_manifest": str(args.windows),
        "window_count_expected": len(expected),
        "window_count_compared": len(records),
        "integers_tested": total_tested,
        "candidate_count": total_candidates,
        "complete_independent_crosscheck": complete,
        "mismatches": mismatches,
        "windows": records,
        "classification": (
            "INDEPENDENTLY REPRODUCIBLE EXACT EXHAUSTIVE FINITE COMPUTATION ON THE EXPLICIT DISJOINT WINDOWS"
            if complete and total_candidates == 0 else
            "EXACT CANDIDATES REQUIRE INDEPENDENT CERTIFICATE VERIFICATION"
            if complete else "INCOMPLETE OR MISMATCHED"
        ),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"window_count_expected={len(expected)}")
    print(f"window_count_compared={len(records)}")
    print(f"integers_tested={total_tested}")
    print(f"candidate_count={total_candidates}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"complete_independent_crosscheck={str(complete).lower()}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
