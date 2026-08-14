#!/usr/bin/env python3
"""Packed winner-mask wrapper for the independent MR/Pollard-Rho backend.

Unlike backend A's streaming positional packer, this wrapper reconstructs a
per-point map keyed by exponent identity and then projects that map onto the
canonical pair table.  No factorization, valuation, classification, parser,
or mask-construction code is imported from backend A.
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


IMPLEMENTATION_ID = "k4_survivor_backend_b_mask_wrapper_v1"
CORE_IMPLEMENTATION_ID = "k4_ap_backend_b_cpp17_mr7_brent_rho_v1"
ANCHOR = 240000005594
MODULUS = 28227969
CLASSES = (-720, -360, 0, 360, 720)
LOW_K = -128
HIGH_K = 128
DOMAIN_SIZE = 407
PACKED_BYTES = 51
FILE_MAGIC = b"K4SMASK1"
FORMAT_VERSION = 1
FILE_HEADER = struct.Struct("<8sIIIIII32s")
POINT_PREFIX = struct.Struct("<QqqII")


class MaskConstructionError(RuntimeError):
    pass


def parse_decimal(text: str, context: str, allow_negative: bool = True) -> int:
    if text == "" or text != text.strip() or text.startswith("+"):
        raise MaskConstructionError(f"invalid decimal for {context}: {text!r}")
    body = text[1:] if allow_negative and text.startswith("-") else text
    if body == "" or not body.isascii() or any(character < "0" or character > "9" for character in body):
        raise MaskConstructionError(f"invalid decimal for {context}: {text!r}")
    if len(body) != 1 and body[0] == "0":
        raise MaskConstructionError(f"noncanonical decimal for {context}: {text!r}")
    number = int(text, 10)
    if number < 0 and not allow_negative:
        raise MaskConstructionError(f"negative decimal for {context}: {text!r}")
    return number


def file_digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if chunk == b"":
                break
            state.update(chunk)
    return state.hexdigest()


def integer_powers(base: int, ceiling: int) -> list[tuple[int, int]]:
    entries: list[tuple[int, int]] = []
    exponent, value = 0, 1
    while value <= ceiling:
        entries.append((exponent, value))
        if value > ceiling // base:
            return entries
        exponent += 1
        value *= base
    return entries


def canonical_domain() -> list[tuple[int, int, int, str]]:
    lower_endpoint = ANCHOR + CLASSES[0] + LOW_K * MODULUS
    triples: list[tuple[int, int, int]] = []
    for c, power3 in integer_powers(3, lower_endpoint):
        for d, power5 in integer_powers(5, lower_endpoint):
            shift = power3 + power5
            if shift <= lower_endpoint:
                triples.append((c, d, shift))
    if len(triples) != DOMAIN_SIZE:
        raise MaskConstructionError("canonical domain size is not 407")
    shift_counts = Counter(item[2] for item in triples)
    repeated = {shift: count for shift, count in shift_counts.items() if count != 1}
    if repeated != {28: 2}:
        raise MaskConstructionError(f"unexpected repeated shifts: {repeated}")
    return [
        (c, d, shift, f"shift_{shift}" if shift_counts[shift] > 1 else "")
        for c, d, shift in triples
    ]


def load_fixed_panel(path: Path) -> list[tuple[int, int, int, int]]:
    expected = [
        (h, k, ANCHOR + h + k * MODULUS, DOMAIN_SIZE)
        for h in CLASSES
        for k in range(LOW_K, HIGH_K + 1)
    ]
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            parser = csv.reader(handle)
            header = next(parser, None)
            if header != ["h", "k", "n", "active_pairs"]:
                raise MaskConstructionError("fixed-panel header is invalid")
            actual: list[tuple[int, int, int, int]] = []
            for line, fields in enumerate(parser, start=2):
                if len(fields) != 4:
                    raise MaskConstructionError(f"fixed-panel width failure on line {line}")
                actual.append(
                    (
                        parse_decimal(fields[0], f"h line {line}"),
                        parse_decimal(fields[1], f"k line {line}"),
                        parse_decimal(fields[2], f"n line {line}", False),
                        parse_decimal(fields[3], f"active_pairs line {line}", False),
                    )
                )
    except (OSError, UnicodeError, csv.Error) as exc:
        raise MaskConstructionError(f"fixed-panel read failed: {exc}") from exc
    if actual != expected:
        for index, (found, wanted) in enumerate(zip(actual, expected)):
            if found != wanted:
                raise MaskConstructionError(f"fixed panel differs at row {index}: {found} != {wanted}")
        raise MaskConstructionError(f"fixed-panel row count {len(actual)} != {len(expected)}")
    return actual


def load_pair_table(path: Path, claimed_digest: str) -> list[tuple[int, int, int, str]]:
    observed_digest = file_digest(path)
    if observed_digest != claimed_digest:
        raise MaskConstructionError("pair-table digest does not match the supplied SHA256")
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            parser = csv.reader(handle)
            if next(parser, None) != ["pair_index", "c", "d", "shift", "duplicate_shift_group"]:
                raise MaskConstructionError("pair-table header is invalid")
            observed: list[tuple[int, int, int, str]] = []
            for expected_index, fields in enumerate(parser):
                line = expected_index + 2
                if len(fields) != 5:
                    raise MaskConstructionError(f"pair-table width failure on line {line}")
                pair_index = parse_decimal(fields[0], f"pair index line {line}", False)
                if pair_index != expected_index:
                    raise MaskConstructionError(f"pair index discontinuity on line {line}")
                observed.append(
                    (
                        parse_decimal(fields[1], f"c line {line}", False),
                        parse_decimal(fields[2], f"d line {line}", False),
                        parse_decimal(fields[3], f"shift line {line}", False),
                        fields[4],
                    )
                )
    except (OSError, UnicodeError, csv.Error) as exc:
        raise MaskConstructionError(f"pair-table read failed: {exc}") from exc
    regenerated = canonical_domain()
    if observed != regenerated:
        raise MaskConstructionError("pair table is not the independently regenerated canonical domain")
    return observed


def verify_core(path: Path) -> None:
    probe = subprocess.run(
        [str(path), "--implementation-id"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if (
        probe.returncode != 0
        or probe.stderr != b""
        or probe.stdout.decode("ascii", "strict").strip() != CORE_IMPLEMENTATION_ID
    ):
        raise MaskConstructionError("backend B core implementation identity is wrong")


def load_count_vector(path: Path, points: list[tuple[int, int, int, int]]) -> list[int]:
    values: list[int] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = csv.reader(handle)
        if next(rows, None) != ["h", "k", "n", "T", "active_pairs"]:
            raise MaskConstructionError("backend B count header is invalid")
        for index, fields in enumerate(rows):
            if index >= len(points) or len(fields) != 5:
                raise MaskConstructionError("backend B count shape is invalid")
            h, k, n, active = points[index]
            identity = (
                parse_decimal(fields[0], "backend B count h"),
                parse_decimal(fields[1], "backend B count k"),
                parse_decimal(fields[2], "backend B count n", False),
                parse_decimal(fields[4], "backend B count active", False),
            )
            if identity != (h, k, n, active):
                raise MaskConstructionError(f"backend B count identity differs at row {index}")
            values.append(parse_decimal(fields[3], "backend B T", False))
    if len(values) != len(points):
        raise MaskConstructionError("backend B count file is truncated")
    return values


def construct_masks(
    diagnostic_path: Path,
    points: list[tuple[int, int, int, int]],
    domain: list[tuple[int, int, int, str]],
    t_values: list[int],
) -> list[bytes]:
    result: list[bytes] = []
    with diagnostic_path.open("r", newline="", encoding="utf-8") as handle:
        rows = csv.reader(handle)
        expected_header = [
            "h",
            "k",
            "n",
            "c",
            "d",
            "shift",
            "remainder",
            "classification",
            "prime_factorization",
        ]
        if next(rows, None) != expected_header:
            raise MaskConstructionError("backend B diagnostic header is invalid")
        for point_index, (h, k, n, _) in enumerate(points):
            outcomes: dict[tuple[int, int], tuple[int, bool]] = {}
            for _ in range(DOMAIN_SIZE):
                fields = next(rows, None)
                if fields is None:
                    raise MaskConstructionError("backend B diagnostic stream is truncated")
                if len(fields) != 9:
                    raise MaskConstructionError("backend B diagnostic row width is invalid")
                row_h = parse_decimal(fields[0], "backend B diagnostic h")
                row_k = parse_decimal(fields[1], "backend B diagnostic k")
                row_n = parse_decimal(fields[2], "backend B diagnostic n", False)
                if (row_h, row_k, row_n) != (h, k, n):
                    raise MaskConstructionError(
                        f"backend B diagnostic point identity mismatch at point {point_index}"
                    )
                c = parse_decimal(fields[3], "backend B diagnostic c", False)
                d = parse_decimal(fields[4], "backend B diagnostic d", False)
                shift = parse_decimal(fields[5], "backend B diagnostic shift", False)
                remainder = parse_decimal(fields[6], "backend B diagnostic remainder", False)
                if remainder != n - shift:
                    raise MaskConstructionError("backend B remainder identity mismatch")
                if fields[7] == "WINNER":
                    winner = True
                elif fields[7] == "LOSER":
                    winner = False
                else:
                    raise MaskConstructionError("backend B classification is not WINNER/LOSER")
                key = (c, d)
                if key in outcomes:
                    raise MaskConstructionError("backend B repeated an exponent pair")
                outcomes[key] = (shift, winner)

            packed = bytearray(PACKED_BYTES)
            winner_count = 0
            for pair_index, (c, d, shift, _) in enumerate(domain):
                observed = outcomes.pop((c, d), None)
                if observed is None or observed[0] != shift:
                    raise MaskConstructionError(
                        f"backend B omitted or altered pair {(c, d)} at point {point_index}"
                    )
                if observed[1]:
                    packed[pair_index >> 3] |= 1 << (pair_index & 7)
                    winner_count += 1
            if outcomes:
                raise MaskConstructionError("backend B added exponent pairs outside the canonical domain")
            if winner_count != t_values[point_index]:
                raise MaskConstructionError(
                    f"backend B mask popcount {winner_count} != T {t_values[point_index]} at n={n}"
                )
            result.append(bytes(packed))
        if next(rows, None) is not None:
            raise MaskConstructionError("backend B diagnostic stream has extra rows")
    return result


def install_binary(
    destination: Path,
    points: list[tuple[int, int, int, int]],
    t_values: list[int],
    masks: list[bytes],
    pair_digest: str,
) -> None:
    try:
        digest_bytes = bytes.fromhex(pair_digest)
    except ValueError as exc:
        raise MaskConstructionError("pair-table SHA256 is not hexadecimal") from exc
    if len(digest_bytes) != 32:
        raise MaskConstructionError("pair-table SHA256 has the wrong width")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    try:
        with staging.open("wb") as handle:
            handle.write(
                FILE_HEADER.pack(
                    FILE_MAGIC,
                    FORMAT_VERSION,
                    FILE_HEADER.size,
                    len(points),
                    DOMAIN_SIZE,
                    PACKED_BYTES,
                    POINT_PREFIX.size + PACKED_BYTES,
                    digest_bytes,
                )
            )
            for (h, k, n, active), t_value, packed in zip(points, t_values, masks):
                handle.write(POINT_PREFIX.pack(n, h, k, active, t_value))
                handle.write(packed)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staging, destination)
    finally:
        if staging.exists():
            staging.unlink()


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with staging.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(staging, path)


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--pair-order", required=True, type=Path)
    parser.add_argument("--pair-order-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--run-report", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    if sys.argv[1:] == ["--implementation-id"]:
        print(IMPLEMENTATION_ID)
        return 0
    args = arguments()
    total_started = time.monotonic()
    try:
        points = load_fixed_panel(args.input)
        domain = load_pair_table(args.pair_order, args.pair_order_sha256)
        verify_core(args.core)
        args.work_dir.mkdir(parents=True, exist_ok=True)
        counts = args.work_dir / "backend_b_counts.csv"
        diagnostics = args.work_dir / "backend_b_diagnostics.csv"
        command = [
            str(args.core),
            "--input",
            str(args.input),
            "--output",
            str(counts),
            "--diagnostics",
            str(diagnostics),
        ]
        core_started = time.monotonic()
        completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        core_elapsed = time.monotonic() - core_started
        if completed.returncode != 0:
            tail = completed.stderr.decode("utf-8", "replace")[-2000:]
            raise MaskConstructionError(f"backend B core return code {completed.returncode}: {tail}")
        t_values = load_count_vector(counts, points)
        masks = construct_masks(diagnostics, points, domain, t_values)
        install_binary(args.output, points, t_values, masks, args.pair_order_sha256)
        save_json(
            args.run_report,
            {
                "schema": "a303656-k4-survivor-backend-run-v1",
                "wrapper_implementation_id": IMPLEMENTATION_ID,
                "core_implementation_id": CORE_IMPLEMENTATION_ID,
                "core_command": command,
                "core_return_code": completed.returncode,
                "core_elapsed_seconds": format(core_elapsed, ".6f"),
                "panel_rows": len(points),
                "pair_count": len(domain),
                "output_sha256": file_digest(args.output),
                "elapsed_seconds": format(time.monotonic() - total_started, ".6f"),
            },
        )
        sys.stderr.buffer.write(completed.stderr)
        return 0
    except (MaskConstructionError, OSError, UnicodeError, csv.Error, StopIteration) as exc:
        print(f"{IMPLEMENTATION_ID}: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
