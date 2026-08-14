#!/usr/bin/env python3
"""Packed winner-mask wrapper for the K4 trial-division backend.

The wrapped C++ executable remains the only two-square classifier.  This file
validates the fixed panel and canonical pair order, consumes backend A's
numeric diagnostic stream in order, and packs the resulting winner bits.
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
from collections import Counter
from pathlib import Path


IMPLEMENTATION_ID = "k4_survivor_backend_a_mask_wrapper_v1"
CORE_IMPLEMENTATION_ID = "k4_ap_backend_a_trial_division_v1"
N0 = 240000005594
M4 = 28227969
H_VALUES = (-720, -360, 0, 360, 720)
K_LOW = -128
K_HIGH = 128
PAIR_COUNT = 407
MASK_BYTES = 51
MAGIC = b"K4SMASK1"
VERSION = 1
HEADER = struct.Struct("<8sIIIIII32s")
ROW = struct.Struct("<QqqII")


class BackendFailure(RuntimeError):
    pass


def strict_int(text: str, label: str, *, signed: bool = True) -> int:
    if not text or text.strip() != text or text.startswith("+"):
        raise BackendFailure(f"malformed {label}: {text!r}")
    digits = text[1:] if signed and text.startswith("-") else text
    if not digits or not digits.isascii() or not digits.isdigit():
        raise BackendFailure(f"malformed {label}: {text!r}")
    if len(digits) > 1 and digits.startswith("0"):
        raise BackendFailure(f"leading zero in {label}: {text!r}")
    value = int(text)
    if not signed and value < 0:
        raise BackendFailure(f"negative {label}: {text!r}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def powers(base: int, limit: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    exponent = 0
    value = 1
    while value <= limit:
        result.append((exponent, value))
        if value > limit // base:
            break
        value *= base
        exponent += 1
    return result


def expected_pairs() -> list[dict[str, int | str]]:
    minimum_n = N0 + min(H_VALUES) + K_LOW * M4
    raw = [
        (c, d, p3 + p5)
        for c, p3 in powers(3, minimum_n)
        for d, p5 in powers(5, minimum_n)
        if p3 + p5 <= minimum_n
    ]
    if len(raw) != PAIR_COUNT or raw != sorted(raw):
        raise BackendFailure("internal canonical pair-domain failure")
    multiplicity = Counter(shift for _, _, shift in raw)
    if {shift: count for shift, count in multiplicity.items() if count > 1} != {28: 2}:
        raise BackendFailure("internal duplicate-shift invariant failure")
    return [
        {
            "pair_index": index,
            "c": c,
            "d": d,
            "shift": shift,
            "duplicate_shift_group": f"shift_{shift}" if multiplicity[shift] > 1 else "",
        }
        for index, (c, d, shift) in enumerate(raw)
    ]


def read_panel(path: Path) -> list[dict[str, int]]:
    try:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ["h", "k", "n", "active_pairs"]:
                raise BackendFailure("panel header mismatch")
            observed = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise BackendFailure(f"cannot read panel: {exc}") from exc
    expected = [
        {"h": h, "k": k, "n": N0 + h + k * M4, "active_pairs": PAIR_COUNT}
        for h in H_VALUES
        for k in range(K_LOW, K_HIGH + 1)
    ]
    if len(observed) != len(expected):
        raise BackendFailure(f"panel row count is {len(observed)}, expected {len(expected)}")
    parsed: list[dict[str, int]] = []
    for line_number, (row, wanted) in enumerate(zip(observed, expected), start=2):
        if set(row) != {"h", "k", "n", "active_pairs"} or None in row:
            raise BackendFailure(f"panel schema failure at line {line_number}")
        item = {
            "h": strict_int(row["h"], "h"),
            "k": strict_int(row["k"], "k"),
            "n": strict_int(row["n"], "n", signed=False),
            "active_pairs": strict_int(row["active_pairs"], "active_pairs", signed=False),
        }
        if item != wanted:
            raise BackendFailure(f"panel mismatch at line {line_number}: {item} != {wanted}")
        parsed.append(item)
    return parsed


def read_pair_order(path: Path, claimed_hash: str) -> list[dict[str, int | str]]:
    actual_hash = sha256_file(path)
    if claimed_hash != actual_hash:
        raise BackendFailure(f"pair-order hash mismatch: {claimed_hash} != {actual_hash}")
    try:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ["pair_index", "c", "d", "shift", "duplicate_shift_group"]:
                raise BackendFailure("pair-order header mismatch")
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise BackendFailure(f"cannot read pair order: {exc}") from exc
    parsed: list[dict[str, int | str]] = []
    for line_number, row in enumerate(rows, start=2):
        if set(row) != {"pair_index", "c", "d", "shift", "duplicate_shift_group"} or None in row:
            raise BackendFailure(f"pair-order schema failure at line {line_number}")
        parsed.append(
            {
                "pair_index": strict_int(row["pair_index"], "pair_index", signed=False),
                "c": strict_int(row["c"], "c", signed=False),
                "d": strict_int(row["d"], "d", signed=False),
                "shift": strict_int(row["shift"], "shift", signed=False),
                "duplicate_shift_group": row["duplicate_shift_group"],
            }
        )
    canonical = expected_pairs()
    if parsed != canonical:
        raise BackendFailure("pair-order table is not the exact canonical active domain")
    return parsed


def core_identity(path: Path) -> str:
    result = subprocess.run(
        [str(path), "--implementation-id"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0 or result.stderr or result.stdout.strip() != CORE_IMPLEMENTATION_ID:
        raise BackendFailure("backend A core identity mismatch")
    return result.stdout.strip()


def read_counts(path: Path, panel: list[dict[str, int]]) -> list[int]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["h", "k", "n", "T", "active_pairs"]:
            raise BackendFailure("backend A counts header mismatch")
        rows = list(reader)
    if len(rows) != len(panel):
        raise BackendFailure("backend A counts row count mismatch")
    result: list[int] = []
    for line_number, (row, point) in enumerate(zip(rows, panel), start=2):
        identity = (
            strict_int(row["h"], "count h"),
            strict_int(row["k"], "count k"),
            strict_int(row["n"], "count n", signed=False),
            strict_int(row["active_pairs"], "count active_pairs", signed=False),
        )
        if identity != (point["h"], point["k"], point["n"], PAIR_COUNT):
            raise BackendFailure(f"backend A counts identity mismatch at line {line_number}")
        result.append(strict_int(row["T"], "T", signed=False))
    return result


def pack_masks(
    diagnostics: Path,
    panel: list[dict[str, int]],
    pairs: list[dict[str, int | str]],
    counts: list[int],
) -> list[bytes]:
    masks: list[bytes] = []
    with diagnostics.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["h", "k", "n", "c", "d", "shift", "remainder", "winner"]:
            raise BackendFailure("backend A diagnostic header mismatch")
        for point_index, point in enumerate(panel):
            mask = bytearray(MASK_BYTES)
            popcount = 0
            for pair in pairs:
                try:
                    row = next(reader)
                except StopIteration as exc:
                    raise BackendFailure("backend A diagnostics truncated") from exc
                expected_identity = (
                    point["h"],
                    point["k"],
                    point["n"],
                    pair["c"],
                    pair["d"],
                    pair["shift"],
                    point["n"] - int(pair["shift"]),
                )
                observed_identity = (
                    strict_int(row["h"], "diagnostic h"),
                    strict_int(row["k"], "diagnostic k"),
                    strict_int(row["n"], "diagnostic n", signed=False),
                    strict_int(row["c"], "diagnostic c", signed=False),
                    strict_int(row["d"], "diagnostic d", signed=False),
                    strict_int(row["shift"], "diagnostic shift", signed=False),
                    strict_int(row["remainder"], "diagnostic remainder", signed=False),
                )
                if observed_identity != expected_identity:
                    raise BackendFailure(
                        f"backend A diagnostic identity/order mismatch at point {point_index}, "
                        f"pair {pair['pair_index']}"
                    )
                winner = strict_int(row["winner"], "diagnostic winner", signed=False)
                if winner not in (0, 1):
                    raise BackendFailure("backend A winner is not a bit")
                if winner:
                    index = int(pair["pair_index"])
                    mask[index // 8] |= 1 << (index % 8)
                    popcount += 1
            if popcount != counts[point_index]:
                raise BackendFailure(
                    f"backend A mask popcount {popcount} != T {counts[point_index]} at n={point['n']}"
                )
            masks.append(bytes(mask))
        try:
            extra = next(reader)
        except StopIteration:
            extra = None
        if extra is not None:
            raise BackendFailure("backend A diagnostics contain extra rows")
    return masks


def write_binary(
    path: Path,
    panel: list[dict[str, int]],
    counts: list[int],
    masks: list[bytes],
    pair_hash: str,
) -> None:
    try:
        pair_hash_bytes = bytes.fromhex(pair_hash)
    except ValueError as exc:
        raise BackendFailure("pair-order SHA256 is malformed") from exc
    if len(pair_hash_bytes) != 32:
        raise BackendFailure("pair-order SHA256 is not 32 bytes")
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with temporary.open("wb") as stream:
            stream.write(
                HEADER.pack(
                    MAGIC,
                    VERSION,
                    HEADER.size,
                    len(panel),
                    PAIR_COUNT,
                    MASK_BYTES,
                    ROW.size + MASK_BYTES,
                    pair_hash_bytes,
                )
            )
            for point, t_value, mask in zip(panel, counts, masks):
                stream.write(ROW.pack(point["n"], point["h"], point["k"], PAIR_COUNT, t_value))
                stream.write(mask)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--pair-order", type=Path, required=True)
    parser.add_argument("--pair-order-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
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
        panel = read_panel(args.input)
        pairs = read_pair_order(args.pair_order, args.pair_order_sha256)
        identity = core_identity(args.core)
        args.work_dir.mkdir(parents=True, exist_ok=True)
        counts_path = args.work_dir / "backend_a_counts.csv"
        diagnostics_path = args.work_dir / "backend_a_diagnostics.csv"
        command = [
            str(args.core),
            "--input",
            str(args.input),
            "--output",
            str(counts_path),
            "--diagnostics",
            str(diagnostics_path),
        ]
        core_started = time.monotonic()
        completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        core_elapsed = time.monotonic() - core_started
        if completed.returncode != 0:
            raise BackendFailure(
                f"backend A core failed with return code {completed.returncode}: "
                f"{completed.stderr.decode('utf-8', 'replace')[-2000:]}"
            )
        counts = read_counts(counts_path, panel)
        masks = pack_masks(diagnostics_path, panel, pairs, counts)
        write_binary(args.output, panel, counts, masks, args.pair_order_sha256)
        report = {
            "schema": "a303656-k4-survivor-backend-run-v1",
            "wrapper_implementation_id": IMPLEMENTATION_ID,
            "core_implementation_id": identity,
            "core_command": command,
            "core_return_code": completed.returncode,
            "core_elapsed_seconds": format(core_elapsed, ".6f"),
            "panel_rows": len(panel),
            "pair_count": len(pairs),
            "output_sha256": sha256_file(args.output),
            "elapsed_seconds": format(time.monotonic() - started, ".6f"),
        }
        atomic_json(args.run_report, report)
        sys.stderr.buffer.write(completed.stderr)
        return 0
    except (BackendFailure, OSError, csv.Error) as exc:
        print(f"{IMPLEMENTATION_ID}: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
