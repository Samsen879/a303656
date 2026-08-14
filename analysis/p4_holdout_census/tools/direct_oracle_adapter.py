#!/usr/bin/env python3
"""Run the factorization-free oracle on every frozen holdout point."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from holdout_common import MASK_BYTES, PAIR_COUNT, HoldoutError, atomic_json, canonical_pairs, demand, load_json, sha256_file


ORACLE_ID = "p4_census_direct_oracle_adapter_v1"
ORACLE_METHOD = "factorization-free exact monotone boundary enumeration; canonical least-a witness"


def load_backend(counts_path: Path, masks_path: Path, points: list[dict]) -> tuple[list[int], list[bytes]]:
    with counts_path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        demand(reader.fieldnames == ["point_ordinal", "mask_index", "class_index", "point_index", "n", "T", "mask_sha256"], "backend counts schema mismatch for direct adapter")
        rows = list(reader)
    demand(len(rows) == len(points), "backend count cardinality mismatch for direct adapter")
    data = masks_path.read_bytes()
    demand(len(data) == len(points) * MASK_BYTES, "backend mask byte count mismatch for direct adapter")
    values: list[int] = []
    masks: list[bytes] = []
    for ordinal, (row, point) in enumerate(zip(rows, points)):
        demand((int(row["point_ordinal"]), int(row["mask_index"]), int(row["class_index"]), int(row["point_index"]), int(row["n"])) == (ordinal, point["mask_index"], point["class_index"], point["point_index"], point["n"]), "backend point identity mismatch for direct adapter")
        mask = data[ordinal * MASK_BYTES:(ordinal + 1) * MASK_BYTES]
        demand(hashlib.sha256(mask).hexdigest() == row["mask_sha256"], "backend mask row digest mismatch for direct adapter")
        values.append(int(row["T"]))
        masks.append(mask)
    return values, masks


def write_input(path: Path, points: list[dict], values: list[int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["class_index", "point_index", "n", "active_pairs", "expected_T"])
        for point, value in zip(points, values):
            writer.writerow([point["class_index"], point["point_index"], point["n"], PAIR_COUNT, value])


def write_gzip_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    payload = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as stream:
            stream.write(payload)
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--counts", type=Path, required=True)
    parser.add_argument("--masks", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--run-report", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=max(1, min(32, os.cpu_count() or 1)))
    args = parser.parse_args()
    started = time.monotonic()
    try:
        root = args.root.resolve()
        panel = load_json(args.panel)
        points = panel.get("points")
        demand(panel.get("status") == "FROZEN PANEL READY FOR EVALUATION" and isinstance(points, list), "direct adapter refused malformed panel")
        values, masks = load_backend(args.counts, args.masks, points)
        identity = subprocess.run([str(args.oracle.resolve()), "--implementation-id"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        demand(identity.returncode == 0 and identity.stderr == b"" and identity.stdout.decode().strip() == ORACLE_ID, "direct oracle identity mismatch")
        work = args.work_dir.resolve()
        work.mkdir(parents=True, exist_ok=True)
        input_path = work / "all_point_panel.csv"
        raw_path = work / "direct_raw.json"
        write_input(input_path, points, values)
        command = [str(args.oracle.resolve()), "--input", str(input_path), "--output", str(raw_path), "--jobs", str(args.jobs)]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        (work / "oracle.stdout.log").write_bytes(process.stdout)
        (work / "oracle.stderr.log").write_bytes(process.stderr)
        demand(process.returncode == 0, f"direct oracle return code {process.returncode}")
        raw = load_json(raw_path)
        demand(raw.get("implementation_id") == ORACLE_ID and raw.get("method") == ORACLE_METHOD, "direct oracle raw identity/method mismatch")
        raw_points = raw.get("points")
        demand(isinstance(raw_points, list) and len(raw_points) == len(points), "direct oracle did not return every panel point")
        pair_lookup = {(pair["c"], pair["d"]): pair for pair in canonical_pairs(root)}
        compact_points: list[dict] = []
        witness_count = 0
        zero_points: list[int] = []
        for ordinal, (expected, t_value, backend_mask, observed) in enumerate(zip(points, values, masks, raw_points)):
            demand((observed.get("class_index"), observed.get("point_index"), observed.get("n"), observed.get("active_pair_count"), observed.get("T")) == (expected["class_index"], expected["point_index"], expected["n"], PAIR_COUNT, t_value), f"direct oracle point identity/T mismatch at {ordinal}")
            winners = observed.get("winners")
            demand(isinstance(winners, list) and len(winners) == t_value, "direct oracle winner cardinality mismatch")
            reconstructed = bytearray(MASK_BYTES)
            normalized: list[dict] = []
            seen: set[int] = set()
            for winner in winners:
                pair = pair_lookup.get((winner.get("c"), winner.get("d")))
                demand(pair is not None and pair["pair_index"] not in seen, "direct oracle winner pair invalid or duplicated")
                seen.add(pair["pair_index"])
                remainder = expected["n"] - pair["shift"]
                a, b = winner.get("a"), winner.get("b")
                demand(winner.get("shift") == pair["shift"] and winner.get("remainder") == remainder, "direct oracle shift/remainder mismatch")
                demand(isinstance(a, int) and isinstance(b, int) and 0 <= a <= b and a * a + b * b == remainder, "direct oracle canonical witness equation mismatch")
                reconstructed[pair["pair_index"] // 8] |= 1 << (pair["pair_index"] % 8)
                normalized.append({"pair_index": pair["pair_index"], "c": pair["c"], "d": pair["d"], "shift": pair["shift"], "remainder": remainder, "a": a, "b": b})
                witness_count += 1
            demand(bytes(reconstructed) == backend_mask, "direct oracle complete mask differs from backend mask")
            if t_value == 0:
                zero_points.append(expected["n"])
            compact_points.append({"point_ordinal": ordinal, "mask_index": expected["mask_index"], "class_index": expected["class_index"], "point_index": expected["point_index"], "n": expected["n"], "T": t_value, "winner_mask_hex": backend_mask.hex(), "canonical_least_a_winners": normalized})
        artifact = {
            "schema": "a303656-holdout-all-point-direct-oracle-v1", "implementation_id": ORACLE_ID, "method": ORACLE_METHOD,
            "panel_sha256": sha256_file(args.panel), "point_count": len(points), "complete_mask_count": len(points), "canonical_witness_count": witness_count,
            "T_zero_points": zero_points, "T_zero_label": "UNVERIFIED COUNTEREXAMPLE CANDIDATE" if zero_points else None, "points": compact_points,
        }
        write_gzip_json(args.artifact, artifact)
        atomic_json(args.run_report, {"schema": "a303656-holdout-direct-run-v1", "command": command, "return_code": process.returncode, "point_count": len(points), "canonical_witness_count": witness_count, "artifact_sha256": sha256_file(args.artifact), "elapsed_seconds": format(time.monotonic() - started, ".6f"), "stdout": str(work / "oracle.stdout.log"), "stderr": str(work / "oracle.stderr.log")})
        print(f"DIRECT_ORACLE_ALL_POINTS_PASS point_count={len(points)} witness_count={witness_count}")
        if zero_points:
            print("UNVERIFIED COUNTEREXAMPLE CANDIDATE", file=sys.stderr)
            return 4
        return 0
    except (HoldoutError, OSError, ValueError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        print(f"direct_oracle_adapter: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
