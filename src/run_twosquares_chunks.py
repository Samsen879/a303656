#!/usr/bin/env python3
"""Gapless parallel chunk runner for direct two-square finite scanners."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanner", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--low", type=int, required=True)
    parser.add_argument("--high", type=int, required=True)
    parser.add_argument("--chunk-size", type=int, default=10_000_000)
    parser.add_argument("--jobs", type=int, default=5)
    parser.add_argument("--C", type=int, required=True)
    parser.add_argument("--D", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    scanner = args.scanner.resolve()
    if not scanner.is_file():
        raise SystemExit(f"missing scanner: {scanner}")
    if args.low < 2 or args.high < args.low or args.chunk_size < 1 or args.jobs < 1:
        raise SystemExit("invalid interval/chunk/jobs")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[tuple[int, int, int]] = []
    lo = args.low
    index = 0
    while lo <= args.high:
        hi = min(args.high, lo + args.chunk_size - 1)
        chunks.append((index, lo, hi))
        lo = hi + 1
        index += 1

    def run_one(item: tuple[int, int, int]) -> dict[str, object]:
        i, lo, hi = item
        stem = f"chunk_{i:04d}_{lo}_{hi}"
        jpath = args.out_dir / f"{stem}.json"
        cpath = args.out_dir / f"{stem}.candidates.txt"
        opath = args.out_dir / f"{stem}.stdout.log"
        epath = args.out_dir / f"{stem}.stderr.log"
        command = [
            str(scanner), "--low", str(lo), "--high", str(hi),
            "--C", str(args.C), "--D", str(args.D),
            "--json", str(jpath), "--candidates", str(cpath), "--quiet",
        ]
        started = perf_counter()
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elapsed = perf_counter() - started
        opath.write_text(completed.stdout, encoding="utf-8")
        epath.write_text(completed.stderr, encoding="utf-8")
        if completed.returncode not in (0, 1) or not jpath.is_file():
            return {
                "index": i, "low": str(lo), "high": str(hi),
                "returncode": completed.returncode, "elapsed_seconds": elapsed,
                "error": "scanner failed or omitted JSON",
            }
        data = json.loads(jpath.read_text(encoding="utf-8"))
        candidates = [str(v) for v in data["candidates"]]
        listed = cpath.read_text(encoding="utf-8").split()
        error = None
        if int(data["low"]) != lo or int(data["high"]) != hi:
            error = "JSON interval mismatch"
        elif int(data["candidate_count"]) != len(candidates) or listed != candidates:
            error = "candidate output mismatch"
        result: dict[str, object] = {
            "index": i, "low": str(lo), "high": str(hi),
            "returncode": completed.returncode, "elapsed_seconds": elapsed,
            "candidate_count": len(candidates), "candidates": candidates,
            "shifts_processed_before_termination": data["shifts_processed_before_termination"],
            "unordered_square_pairs_enumerated": data["unordered_square_pairs_enumerated"],
            "admissible_rectangle_pair_count_at_high": data["admissible_rectangle_pair_count_at_high"],
            "distinct_shift_count_at_high": data["distinct_shift_count_at_high"],
            "json": str(jpath), "json_sha256": sha256(jpath),
            "candidate_file": str(cpath), "candidate_file_sha256": sha256(cpath),
            "stdout": str(opath), "stdout_sha256": sha256(opath),
            "stderr": str(epath), "stderr_sha256": sha256(epath),
        }
        if error:
            result["error"] = error
        return result

    started = perf_counter()
    records: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run_one, chunk) for chunk in chunks]
        for future in as_completed(futures):
            row = future.result()
            records.append(row)
            print(
                f"chunk={row['index']} interval=[{row['low']},{row['high']}] "
                f"candidates={row.get('candidate_count', 'ERROR')} "
                f"elapsed={float(row['elapsed_seconds']):.6f}",
                flush=True,
            )
    wall = perf_counter() - started
    records.sort(key=lambda row: int(row["index"]))
    errors = [row for row in records if "error" in row]
    tested = sum(int(row["high"]) - int(row["low"]) + 1 for row in records if "error" not in row)
    complete = (
        not errors
        and len(records) == len(chunks)
        and int(records[0]["low"]) == args.low
        and int(records[-1]["high"]) == args.high
        and all(int(records[i]["high"]) + 1 == int(records[i + 1]["low"]) for i in range(len(records) - 1))
        and tested == args.high - args.low + 1
    )
    candidates = [value for row in records for value in row.get("candidates", [])]
    payload = {
        "schema": "a303656-direct-two-squares-chunked-v1",
        "scanner": str(scanner),
        "scanner_sha256": sha256(scanner),
        "source": str(args.source) if args.source else None,
        "source_sha256": sha256(args.source) if args.source else None,
        "low": str(args.low), "high": str(args.high),
        "chunk_size": args.chunk_size, "chunk_count": len(chunks), "jobs": args.jobs,
        "C": args.C, "D": args.D,
        "complete_gapless_coverage": complete,
        "integers_tested": tested,
        "candidate_count": len(candidates), "candidates": candidates,
        "error_count": len(errors), "errors": errors,
        "unordered_square_pairs_enumerated_total": sum(int(row.get("unordered_square_pairs_enumerated", 0)) for row in records),
        "wall_seconds": wall,
        "python": sys.version, "platform": platform.platform(), "cpu_count_reported": os.cpu_count(),
        "chunks": records,
        "classification": (
            "EXACT EXHAUSTIVE FINITE COMPUTATION: EVERY n IN INTERVAL HAS A REPRESENTATION"
            if complete and not candidates else
            "EXACT CANDIDATES REQUIRE INDEPENDENT CERTIFICATE VERIFICATION"
            if complete else "INCOMPLETE"
        ),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"complete_gapless_coverage={str(complete).lower()}")
    print(f"integers_tested={tested}")
    print(f"candidate_count={len(candidates)}")
    print(f"wall_seconds={wall:.6f}")
    return 0 if complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
