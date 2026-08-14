#!/usr/bin/env python3
"""Census adapter for the deterministic MR7/Brent-Rho/Fermat K4 core.

Unlike adapter A's positional stream packer, this adapter first builds a
per-point map keyed by (c,d), then projects that map onto the canonical domain.
"""

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


IMPLEMENTATION_ID = "p4_census_backend_b_keyed_adapter_v1"
CORE_ID = "k4_ap_backend_b_cpp17_mr7_brent_rho_v1"
FILE_MAGIC = b"P4CMASK1"
FORMAT_VERSION = 1
BACKEND_SLOT = 2
FILE_HEADER = struct.Struct("<8sIIIIII32s32s32s")


def write_json_atomically(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary, path)


def identify_core(path: Path) -> str:
    process = subprocess.run([str(path), "--implementation-id"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = process.stdout.decode("utf-8", "strict").strip()
    if process.returncode != 0 or process.stderr != b"" or stdout != CORE_ID:
        raise CensusError("backend B executable identity check failed")
    return stdout


def emit_compatibility_panel(path: Path, points: list[dict[str, int | str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        output = csv.writer(handle, lineterminator="\n")
        output.writerow(("h", "k", "n", "active_pairs"))
        output.writerows((point["class_index"], point["point_index"], point["n"], PAIR_COUNT) for point in points)


def load_core_counts(path: Path, points: list[dict[str, int | str]]) -> list[int]:
    with path.open(newline="", encoding="utf-8") as handle:
        records = csv.reader(handle)
        if next(records, None) != ["h", "k", "n", "T", "active_pairs"]:
            raise CensusError("backend B counts header differs")
        actual = list(records)
    if len(actual) != len(points):
        raise CensusError("backend B counts point cardinality differs")
    values: list[int] = []
    for position, (fields, point) in enumerate(zip(actual, points)):
        if len(fields) != 5:
            raise CensusError("backend B counts row width differs")
        identity = tuple(int(value) for value in (fields[0], fields[1], fields[2], fields[4]))
        wanted = (point["class_index"], point["point_index"], point["n"], PAIR_COUNT)
        if identity != wanted:
            raise CensusError(f"backend B counts identity differs at position {position}")
        t_value = int(fields[3])
        if t_value < 0 or t_value > PAIR_COUNT:
            raise CensusError("backend B T is outside the active domain")
        values.append(t_value)
    return values


def map_and_pack(
    diagnostics_path: Path,
    points: list[dict[str, int | str]],
    root: Path,
    t_values: list[int],
) -> list[bytes]:
    domain = canonical_pairs(root)
    by_identity = {(pair.c, pair.d): pair for pair in domain}
    point_lookup = {
        (int(point["class_index"]), int(point["point_index"])): ordinal
        for ordinal, point in enumerate(points)
    }
    if len(point_lookup) != len(points):
        raise CensusError("formal panel class/point identity is not unique")
    per_point: list[dict[tuple[int, int], bool]] = [dict() for _ in points]
    with diagnostics_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        wanted_header = ["h", "k", "n", "c", "d", "shift", "remainder", "classification", "prime_factorization"]
        if reader.fieldnames != wanted_header:
            raise CensusError("backend B diagnostics header differs")
        row_count = 0
        for row in reader:
            row_count += 1
            class_index, point_index = int(row["h"]), int(row["k"])
            if not 0 <= class_index < 87:
                raise CensusError("backend B diagnostic class index outside panel")
            # The ordered panel is not rectangular; locate by exact triple.
            ordinal = point_lookup.get((class_index, point_index))
            if ordinal is None:
                raise CensusError("backend B diagnostic point identity not unique")
            point = points[ordinal]
            if int(row["n"]) != point["n"]:
                raise CensusError("backend B diagnostic n differs from panel")
            c, d = int(row["c"]), int(row["d"])
            pair = by_identity.get((c, d))
            if pair is None:
                raise CensusError("backend B diagnostic exponent pair outside canonical domain")
            if int(row["shift"]) != pair.shift or int(row["remainder"]) != int(point["n"]) - pair.shift:
                raise CensusError("backend B diagnostic shift/remainder mismatch")
            if (c, d) in per_point[ordinal]:
                raise CensusError("backend B duplicated a diagnostic exponent pair")
            classification = row["classification"]
            if classification not in ("WINNER", "LOSER"):
                raise CensusError("backend B classification is invalid")
            per_point[ordinal][(c, d)] = classification == "WINNER"
    if row_count != len(points) * PAIR_COUNT:
        raise CensusError("backend B diagnostics missing or extra rows")

    packed_masks: list[bytes] = []
    for ordinal, mapping in enumerate(per_point):
        if set(mapping) != set(by_identity):
            raise CensusError(f"backend B diagnostic pair set differs at point {ordinal}")
        packed = bytearray(MASK_BYTES)
        for pair in domain:
            if mapping[(pair.c, pair.d)]:
                packed[pair.index >> 3] |= 1 << (pair.index & 7)
        result = bytes(packed)
        if mask_popcount(result) != t_values[ordinal]:
            raise CensusError(f"backend B packed popcount/T differs at point {ordinal}")
        packed_masks.append(result)
    return packed_masks


def serialize_results(
    csv_path: Path,
    binary_path: Path,
    panel_path: Path,
    points: list[dict[str, int | str]],
    t_values: list[int],
    masks: list[bytes],
    identity: str,
    root: Path,
) -> None:
    panel_hash = bytes.fromhex(panel_digest(panel_path))
    pair_hash = bytes.fromhex(sha256_file(root / "analysis/k4_survivor_incidence/pair_order.csv"))
    identity_hash = hashlib.sha256(identity.encode("ascii")).digest()
    binary_path.parent.mkdir(parents=True, exist_ok=True)
    binary_temporary = binary_path.with_name(binary_path.name + f".tmp.{os.getpid()}")
    with binary_temporary.open("wb") as handle:
        handle.write(FILE_HEADER.pack(FILE_MAGIC, FORMAT_VERSION, BACKEND_SLOT, FILE_HEADER.size, len(points), PAIR_COUNT, MASK_BYTES, panel_hash, pair_hash, identity_hash))
        for packed in masks:
            handle.write(packed)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(binary_temporary, binary_path)
    csv_temporary = csv_path.with_name(csv_path.name + f".tmp.{os.getpid()}")
    with csv_temporary.open("w", newline="", encoding="utf-8") as handle:
        output = csv.DictWriter(handle, fieldnames=COUNT_FIELDS, lineterminator="\n")
        output.writeheader()
        for ordinal, (point, t_value, packed) in enumerate(zip(points, t_values, masks)):
            record = {field: point[field] for field in PANEL_FIELDS}
            record["T"] = t_value
            record["mask_offset"] = FILE_HEADER.size + ordinal * MASK_BYTES
            record["mask_sha256"] = hashlib.sha256(packed).hexdigest()
            output.writerow(record)
    os.replace(csv_temporary, csv_path)


def options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--core", required=True, type=Path)
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--counts", required=True, type=Path)
    parser.add_argument("--masks", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--run-report", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--implementation-id":
        print(IMPLEMENTATION_ID)
        return 0
    args = options()
    beginning = time.monotonic()
    try:
        root = args.root.resolve()
        points = read_panel(args.panel.resolve(), root)
        identity = identify_core(args.core.resolve())
        args.work_dir.mkdir(parents=True, exist_ok=True)
        compatibility = args.work_dir / "backend_b_core_panel.csv"
        raw_counts = args.work_dir / "backend_b_core_counts.csv"
        diagnostics = args.work_dir / "backend_b_diagnostics.csv"
        emit_compatibility_panel(compatibility, points)
        command = [str(args.core.resolve()), "--input", str(compatibility), "--output", str(raw_counts), "--diagnostics", str(diagnostics)]
        core_start = time.monotonic()
        process = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        core_seconds = time.monotonic() - core_start
        if process.returncode != 0:
            raise CensusError(f"backend B core return code {process.returncode}: {process.stderr.decode('utf-8', 'replace')[-2000:]}")
        t_values = load_core_counts(raw_counts, points)
        masks = map_and_pack(diagnostics, points, root, t_values)
        serialize_results(args.counts, args.masks, args.panel, points, t_values, masks, identity, root)
        write_json_atomically(args.run_report, {
            "schema": "a303656-p4-census-backend-run-v1", "adapter": IMPLEMENTATION_ID,
            "core": identity, "core_command": command, "core_return_code": process.returncode,
            "core_elapsed_seconds": format(core_seconds, ".6f"), "point_count": len(points),
            "diagnostic_rows": len(points) * PAIR_COUNT, "counts_sha256": sha256_file(args.counts),
            "masks_sha256": sha256_file(args.masks), "elapsed_seconds": format(time.monotonic() - beginning, ".6f"),
        })
        sys.stdout.buffer.write(process.stdout)
        sys.stderr.buffer.write(process.stderr)
        return 0
    except (CensusError, OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"{IMPLEMENTATION_ID}: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
