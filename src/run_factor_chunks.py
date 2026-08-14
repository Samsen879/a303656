#!/usr/bin/env python3
"""Exact, auditable chunk orchestrator for the all-prime factor-sieve scanners."""
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
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scanner", required=True)
    ap.add_argument("--low", required=True, type=int)
    ap.add_argument("--high", required=True, type=int)
    ap.add_argument("--chunk-size", type=int, default=10_000_000)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--C", required=True, type=int)
    ap.add_argument("--D", required=True, type=int)
    ap.add_argument("--group-span", type=int, default=5_000_000)
    ap.add_argument("--max-odd", type=int, default=1)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--summary", required=True)
    args = ap.parse_args()

    scanner = Path(args.scanner).resolve()
    if not scanner.is_file():
        raise SystemExit(f"scanner not found: {scanner}")
    if args.low < 2 or args.high < args.low or args.chunk_size <= 0 or args.jobs <= 0:
        raise SystemExit("invalid interval/chunk/jobs")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[tuple[int, int, int]] = []
    x = args.low
    idx = 0
    while x <= args.high:
        y = min(args.high, x + args.chunk_size - 1)
        chunks.append((idx, x, y))
        idx += 1
        x = y + 1
    assert chunks[0][1] == args.low and chunks[-1][2] == args.high
    assert all(chunks[i][2] + 1 == chunks[i + 1][1] for i in range(len(chunks) - 1))

    def run_one(item: tuple[int, int, int]) -> dict[str, object]:
        i, lo, hi = item
        stem = f"chunk_{i:04d}_{lo}_{hi}"
        jpath = out_dir / f"{stem}.json"
        lpath = out_dir / f"{stem}.stdout.log"
        epath = out_dir / f"{stem}.stderr.log"
        cmd = [
            str(scanner), "--low", str(lo), "--high", str(hi),
            "--C", str(args.C), "--D", str(args.D),
            "--group-span", str(args.group_span),
            "--max-odd", str(args.max_odd),
            "--json", str(jpath),
        ]
        # The primary implementation supports --quiet; the clean implementation
        # already emits only its summary.  Detect by binary name, avoiding a
        # failed run from an unsupported option.
        if scanner.name == "search_factor_sieve":
            cmd.append("--quiet")
        t0 = perf_counter()
        cp = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elapsed = perf_counter() - t0
        lpath.write_text(cp.stdout, encoding="utf-8")
        epath.write_text(cp.stderr, encoding="utf-8")
        if cp.returncode not in (0, 1):
            return {
                "index": i, "low": str(lo), "high": str(hi), "returncode": cp.returncode,
                "elapsed_seconds": elapsed, "error": "scanner execution failed",
                "json": str(jpath), "stdout": str(lpath), "stderr": str(epath),
            }
        if not jpath.is_file():
            return {
                "index": i, "low": str(lo), "high": str(hi), "returncode": cp.returncode,
                "elapsed_seconds": elapsed, "error": "scanner did not produce JSON",
                "json": str(jpath), "stdout": str(lpath), "stderr": str(epath),
            }
        try:
            data = json.loads(jpath.read_text(encoding="utf-8"))
            if int(data["low"]) != lo or int(data["high"]) != hi:
                raise ValueError("JSON interval mismatch")
            candidates = [int(v) for v in data["candidates"]]
            if int(data["candidate_count"]) != len(candidates):
                raise ValueError("candidate_count mismatch")
            # Scanner binaries may use either convention: always-zero on a
            # completed exact scan, or one for an exact-empty scan.  The JSON
            # candidate list is authoritative; return code 2 is reserved for
            # execution/input failure.
            return {
                "index": i, "low": str(lo), "high": str(hi), "returncode": cp.returncode,
                "elapsed_seconds": elapsed, "candidate_count": len(candidates),
                "candidates": [str(v) for v in candidates],
                "admissible_pair_count_at_high": data["admissible_pair_count_at_high"],
                "distinct_shift_count_at_high": data["distinct_shift_count_at_high"],
                "shifts_processed_before_termination": data["shifts_processed_before_termination"],
                "json": str(jpath), "json_sha256": sha256(jpath),
                "stdout": str(lpath), "stdout_sha256": sha256(lpath),
                "stderr": str(epath), "stderr_sha256": sha256(epath),
            }
        except Exception as exc:  # exact audit failure
            return {
                "index": i, "low": str(lo), "high": str(hi), "returncode": cp.returncode,
                "elapsed_seconds": elapsed, "error": f"invalid scanner JSON: {exc}",
                "json": str(jpath), "stdout": str(lpath), "stderr": str(epath),
            }

    started = perf_counter()
    records: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(run_one, item): item for item in chunks}
        for fut in as_completed(futures):
            rec = fut.result()
            records.append(rec)
            print(
                f"chunk={rec['index']} interval=[{rec['low']},{rec['high']}] "
                f"rc={rec['returncode']} candidates={rec.get('candidate_count','ERROR')} "
                f"elapsed={float(rec['elapsed_seconds']):.6f}",
                flush=True,
            )
    wall = perf_counter() - started
    records.sort(key=lambda r: int(r["index"]))
    errors = [r for r in records if "error" in r]
    all_candidates = [v for r in records for v in r.get("candidates", [])]
    tested = sum(int(r["high"]) - int(r["low"]) + 1 for r in records if "error" not in r)
    complete = (
        not errors
        and len(records) == len(chunks)
        and int(records[0]["low"]) == args.low
        and int(records[-1]["high"]) == args.high
        and all(int(records[i]["high"]) + 1 == int(records[i + 1]["low"]) for i in range(len(records) - 1))
        and tested == args.high - args.low + 1
    )
    payload = {
        "schema": "a303656-all-prime-chunked-search-v1",
        "scanner": str(scanner),
        "scanner_sha256": sha256(scanner),
        "low": str(args.low),
        "high": str(args.high),
        "chunk_size": args.chunk_size,
        "chunk_count": len(chunks),
        "jobs": args.jobs,
        "C": args.C,
        "D": args.D,
        "group_span": args.group_span,
        "max_odd": args.max_odd,
        "complete_gapless_coverage": complete,
        "integers_tested": tested,
        "candidate_count": len(all_candidates),
        "candidates": all_candidates,
        "error_count": len(errors),
        "errors": errors,
        "wall_seconds": wall,
        "python": sys.version,
        "platform": platform.platform(),
        "cpu_count_reported": os.cpu_count(),
        "chunks": records,
        "classification": (
            "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE STATED ALL-PRIME CERTIFICATE FAMILY"
            if complete and not all_candidates else
            "CANDIDATES REQUIRE INDEPENDENT VERIFICATION"
            if complete else "INCOMPLETE"
        ),
    }
    summary = Path(args.summary)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"complete_gapless_coverage={str(complete).lower()}")
    print(f"integers_tested={tested}")
    print(f"candidate_count={len(all_candidates)}")
    print(f"wall_seconds={wall:.6f}")
    print(f"summary={summary}")
    if errors or not complete:
        return 2
    return 0 if all_candidates else 1


if __name__ == "__main__":
    raise SystemExit(main())
