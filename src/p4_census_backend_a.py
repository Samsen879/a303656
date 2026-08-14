#!/usr/bin/env python3
"""Census adapter for the deterministic trial-division/Fermat K4 core."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import struct
import subprocess
import sys
import time
from pathlib import Path

from p4_census_common import (
    COUNT_FIELDS, MASK_BYTES, PAIR_COUNT, PANEL_FIELDS, CensusError,
    canonical_pairs, mask_popcount, panel_digest, read_panel, sha256_file,
)


IMPLEMENTATION_ID = "p4_census_backend_a_stream_adapter_v1"
CORE_ID = "k4_ap_backend_a_trial_division_v1"
MAGIC = b"P4CMASK1"
VERSION = 1
BACKEND_CODE = 1
HEADER = struct.Struct("<8sIIIIII32s32s32s")


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def core_identity(core: Path) -> str:
    result = subprocess.run([str(core), "--implementation-id"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0 or result.stderr or result.stdout.decode().strip() != CORE_ID:
        raise CensusError("backend A core identity mismatch")
    return result.stdout.decode().strip()


def write_core_panel(path: Path, panel: list[dict[str, int | str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["h", "k", "n", "active_pairs"])
        for row in panel:
            writer.writerow([row["class_index"], row["point_index"], row["n"], PAIR_COUNT])


def parse_counts(path: Path, panel: list[dict[str, int | str]]) -> list[int]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["h", "k", "n", "T", "active_pairs"]:
            raise CensusError("backend A core counts header mismatch")
        rows = list(reader)
    if len(rows) != len(panel):
        raise CensusError("backend A core counts truncated or extended")
    result: list[int] = []
    for index, (row, point) in enumerate(zip(rows, panel)):
        observed = (int(row["h"]), int(row["k"]), int(row["n"]), int(row["active_pairs"]))
        expected = (point["class_index"], point["point_index"], point["n"], PAIR_COUNT)
        if observed != expected:
            raise CensusError(f"backend A core counts identity mismatch at row {index}")
        value = int(row["T"])
        if not 0 <= value <= PAIR_COUNT:
            raise CensusError("backend A emitted out-of-domain T")
        result.append(value)
    return result


def pack_stream(
    path: Path,
    panel: list[dict[str, int | str]],
    root: Path,
    counts: list[int],
) -> list[bytes]:
    pairs = canonical_pairs(root)
    masks: list[bytes] = []
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        expected_header = ["h", "k", "n", "c", "d", "shift", "remainder", "winner"]
        if reader.fieldnames != expected_header:
            raise CensusError("backend A diagnostic header mismatch")
        for point_index, point in enumerate(panel):
            mask = bytearray(MASK_BYTES)
            for pair in pairs:
                row = next(reader, None)
                if row is None:
                    raise CensusError("backend A diagnostics truncated")
                observed = (
                    int(row["h"]), int(row["k"]), int(row["n"]), int(row["c"]),
                    int(row["d"]), int(row["shift"]), int(row["remainder"]),
                )
                expected = (
                    point["class_index"], point["point_index"], point["n"],
                    pair.c, pair.d, pair.shift, int(point["n"]) - pair.shift,
                )
                if observed != expected:
                    raise CensusError(f"backend A diagnostic order mismatch at point {point_index}, pair {pair.index}")
                if row["winner"] not in ("0", "1"):
                    raise CensusError("backend A winner is not a bit")
                if row["winner"] == "1":
                    mask[pair.index // 8] |= 1 << (pair.index % 8)
            packed = bytes(mask)
            if mask_popcount(packed) != counts[point_index]:
                raise CensusError(f"backend A popcount/T mismatch at point {point_index}")
            masks.append(packed)
        if next(reader, None) is not None:
            raise CensusError("backend A diagnostics contain extra rows")
    return masks


def write_outputs(
    counts_path: Path,
    masks_path: Path,
    panel_path: Path,
    panel: list[dict[str, int | str]],
    counts: list[int],
    masks: list[bytes],
    core_id: str,
    root: Path,
) -> None:
    panel_hash = bytes.fromhex(panel_digest(panel_path))
    pair_hash = bytes.fromhex(sha256_file(root / "analysis/k4_survivor_incidence/pair_order.csv"))
    core_hash = hashlib.sha256(core_id.encode()).digest()
    masks_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = masks_path.with_name(masks_path.name + f".tmp.{os.getpid()}")
    with temporary.open("wb") as stream:
        stream.write(HEADER.pack(MAGIC, VERSION, BACKEND_CODE, HEADER.size, len(panel), PAIR_COUNT, MASK_BYTES, panel_hash, pair_hash, core_hash))
        for mask in masks:
            stream.write(mask)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, masks_path)
    temporary_csv = counts_path.with_name(counts_path.name + f".tmp.{os.getpid()}")
    with temporary_csv.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=COUNT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for index, (point, t_value, mask) in enumerate(zip(panel, counts, masks)):
            row = {field: point[field] for field in PANEL_FIELDS}
            row.update({"T": t_value, "mask_offset": HEADER.size + index * MASK_BYTES, "mask_sha256": hashlib.sha256(mask).hexdigest()})
            writer.writerow(row)
    os.replace(temporary_csv, counts_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--counts", type=Path, required=True)
    parser.add_argument("--masks", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--run-report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--implementation-id":
        print(IMPLEMENTATION_ID)
        return 0
    args = parse_args()
    started = time.monotonic()
    try:
        root = args.root.resolve()
        panel = read_panel(args.panel.resolve(), root)
        identity = core_identity(args.core.resolve())
        args.work_dir.mkdir(parents=True, exist_ok=True)
        core_panel = args.work_dir / "backend_a_core_panel.csv"
        raw_counts = args.work_dir / "backend_a_core_counts.csv"
        diagnostics = args.work_dir / "backend_a_diagnostics.csv"
        write_core_panel(core_panel, panel)
        command = [str(args.core.resolve()), "--input", str(core_panel), "--output", str(raw_counts), "--diagnostics", str(diagnostics)]
        core_started = time.monotonic()
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        core_elapsed = time.monotonic() - core_started
        if completed.returncode != 0:
            raise CensusError(f"backend A core return code {completed.returncode}: {completed.stderr.decode('utf-8', 'replace')[-2000:]}")
        values = parse_counts(raw_counts, panel)
        masks = pack_stream(diagnostics, panel, root, values)
        write_outputs(args.counts, args.masks, args.panel, panel, values, masks, identity, root)
        atomic_json(args.run_report, {
            "schema": "a303656-p4-census-backend-run-v1", "adapter": IMPLEMENTATION_ID,
            "core": identity, "core_command": command, "core_return_code": completed.returncode,
            "core_elapsed_seconds": format(core_elapsed, ".6f"), "point_count": len(panel),
            "diagnostic_rows": len(panel) * PAIR_COUNT, "counts_sha256": sha256_file(args.counts),
            "masks_sha256": sha256_file(args.masks), "elapsed_seconds": format(time.monotonic() - started, ".6f"),
        })
        sys.stdout.buffer.write(completed.stdout)
        sys.stderr.buffer.write(completed.stderr)
        return 0
    except (CensusError, OSError, ValueError, csv.Error) as exc:
        print(f"{IMPLEMENTATION_ID}: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
