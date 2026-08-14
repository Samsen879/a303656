#!/usr/bin/env python3
"""Strict adapters for the two independent existing exact factorization cores."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from holdout_common import MASK_BYTES, PAIR_COUNT, HoldoutError, atomic_json, canonical_pairs, demand, load_json, sha256_file


CORE_IDS = {
    "A": "k4_ap_backend_a_trial_division_v1",
    "B": "k4_ap_backend_b_cpp17_mr7_brent_rho_v1",
}


def identify(core: Path, backend: str) -> str:
    result = subprocess.run([str(core), "--implementation-id"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    identity = result.stdout.decode("ascii", "strict").strip()
    demand(result.returncode == 0 and result.stderr == b"" and identity == CORE_IDS[backend], f"backend {backend} core identity mismatch")
    return identity


def write_core_panel(path: Path, points: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["h", "k", "n", "active_pairs"])
        for point in points:
            writer.writerow([point["class_index"], point["point_index"], point["n"], PAIR_COUNT])


def parse_counts(path: Path, points: list[dict]) -> list[int]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        demand(reader.fieldnames == ["h", "k", "n", "T", "active_pairs"], "core counts header mismatch")
        rows = list(reader)
    demand(len(rows) == len(points), "core counts point cardinality mismatch")
    values: list[int] = []
    for ordinal, (row, point) in enumerate(zip(rows, points)):
        observed = (int(row["h"]), int(row["k"]), int(row["n"]), int(row["active_pairs"]))
        expected = (point["class_index"], point["point_index"], point["n"], PAIR_COUNT)
        demand(observed == expected, f"core counts point identity mismatch at ordinal {ordinal}")
        value = int(row["T"])
        demand(0 <= value <= PAIR_COUNT, "core T outside active domain")
        values.append(value)
    return values


def parse_diagnostics(path: Path, backend: str, points: list[dict], pairs: list[dict], counts: list[int]) -> list[bytes]:
    expected_headers = {
        "A": ["h", "k", "n", "c", "d", "shift", "remainder", "winner"],
        "B": ["h", "k", "n", "c", "d", "shift", "remainder", "classification", "prime_factorization"],
    }
    point_lookup = {(point["class_index"], point["point_index"]): ordinal for ordinal, point in enumerate(points)}
    pair_lookup = {(pair["c"], pair["d"]): pair for pair in pairs}
    per_point: list[dict[int, bool]] = [dict() for _ in points]
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        demand(reader.fieldnames == expected_headers[backend], f"backend {backend} diagnostic header mismatch")
        row_count = 0
        for row in reader:
            row_count += 1
            key = (int(row["h"]), int(row["k"]))
            ordinal = point_lookup.get(key)
            demand(ordinal is not None, f"backend {backend} diagnostic outside panel")
            point = points[ordinal]
            demand(int(row["n"]) == point["n"], f"backend {backend} diagnostic n mismatch")
            pair = pair_lookup.get((int(row["c"]), int(row["d"])))
            demand(pair is not None, f"backend {backend} diagnostic pair outside domain")
            index = pair["pair_index"]
            demand(index not in per_point[ordinal], f"backend {backend} diagnostic pair duplicated")
            demand(int(row["shift"]) == pair["shift"] and int(row["remainder"]) == point["n"] - pair["shift"], f"backend {backend} shift/remainder mismatch")
            if backend == "A":
                demand(row["winner"] in ("0", "1"), "backend A winner is not a bit")
                winner = row["winner"] == "1"
            else:
                demand(row["classification"] in ("WINNER", "LOSER"), "backend B classification invalid")
                winner = row["classification"] == "WINNER"
            per_point[ordinal][index] = winner
    demand(row_count == len(points) * PAIR_COUNT, f"backend {backend} evaluated missing or extra diagnostic rows")
    masks: list[bytes] = []
    for ordinal, mapping in enumerate(per_point):
        demand(set(mapping) == set(range(PAIR_COUNT)), f"backend {backend} incomplete pair mask at point {ordinal}")
        mask = bytearray(MASK_BYTES)
        for index, winner in mapping.items():
            if winner:
                mask[index // 8] |= 1 << (index % 8)
        packed = bytes(mask)
        demand(sum(byte.bit_count() for byte in packed) == counts[ordinal], f"backend {backend} popcount/T mismatch")
        masks.append(packed)
    return masks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("A", "B"), required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--counts", type=Path, required=True)
    parser.add_argument("--masks", type=Path, required=True)
    parser.add_argument("--run-report", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        root = args.root.resolve()
        panel = load_json(args.panel)
        demand(panel.get("status") == "FROZEN PANEL READY FOR EVALUATION" and panel.get("integer_evaluation_performed") is False, "backend refused non-frozen or already-evaluated panel")
        points = panel.get("points")
        demand(isinstance(points, list) and len(points) == panel.get("point_count"), "panel points malformed")
        identity = identify(args.core.resolve(), args.backend)
        work = args.work_dir.resolve()
        work.mkdir(parents=True, exist_ok=True)
        core_panel = work / "core_panel.csv"
        raw_counts = work / "raw_counts.csv"
        diagnostics = work / "raw_diagnostics.csv"
        write_core_panel(core_panel, points)
        command = [str(args.core.resolve()), "--input", str(core_panel), "--output", str(raw_counts), "--diagnostics", str(diagnostics)]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        (work / "core.stdout.log").write_bytes(process.stdout)
        (work / "core.stderr.log").write_bytes(process.stderr)
        demand(process.returncode == 0, f"backend {args.backend} core return code {process.returncode}")
        counts = parse_counts(raw_counts, points)
        masks = parse_diagnostics(diagnostics, args.backend, points, canonical_pairs(root), counts)
        args.counts.parent.mkdir(parents=True, exist_ok=True)
        with args.counts.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["point_ordinal", "mask_index", "class_index", "point_index", "n", "T", "mask_sha256"])
            for point, value, mask in zip(points, counts, masks):
                writer.writerow([point["point_ordinal"], point["mask_index"], point["class_index"], point["point_index"], point["n"], value, hashlib.sha256(mask).hexdigest()])
        args.masks.write_bytes(b"".join(masks))
        atomic_json(args.run_report, {
            "schema": "a303656-holdout-backend-run-v1", "backend": args.backend, "core_implementation_id": identity,
            "command": command, "return_code": process.returncode, "point_count": len(points), "diagnostic_row_count": len(points) * PAIR_COUNT,
            "counts_sha256": sha256_file(args.counts), "masks_sha256": sha256_file(args.masks), "elapsed_seconds": format(time.monotonic() - started, ".6f"),
            "stdout": str(work / "core.stdout.log"), "stderr": str(work / "core.stderr.log"),
        })
        print(f"BACKEND_{args.backend}_PASS point_count={len(points)}")
        return 0
    except (HoldoutError, OSError, ValueError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        print(f"backend_adapter: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
