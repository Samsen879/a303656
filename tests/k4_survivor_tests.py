#!/usr/bin/env python3
"""Required expected-rejection harness for the K4 survivor audit."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path
from typing import Callable


HEADER_SIZE = 64
ROW_PREFIX_SIZE = 32
MASK_SIZE = 51
ROW_SIZE = ROW_PREFIX_SIZE + MASK_SIZE
POINT_PREFIX = struct.Struct("<QqqII")
TEST_NAMES = [
    "changed_pair_ordering",
    "changed_pair_order_hash",
    "one_flipped_winner_bit",
    "mask_row_deletion",
    "duplicated_row",
    "extra_bytes",
    "truncated_mask",
    "incorrect_popcount_T",
    "class_relabeling",
    "point_reordering",
    "persistent_covered_pair_marked_winner",
    "swapped_backend_identity",
    "source_commit_mismatch",
    "baseline_hash_mismatch",
]


class TestFailure(RuntimeError):
    pass


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TestFailure(f"JSON root is not an object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary, path)


def base_command(args: argparse.Namespace, fixture: Path, *, swapped: bool = False) -> list[str]:
    return [
        sys.executable,
        str(args.source_root / "src/k4_survivor_verify.py"),
        "--source-root",
        str(args.source_root),
        "--artifact-dir",
        str(fixture),
        "--source-commit",
        args.source_commit,
        "--backend-a-core",
        str(args.backend_b_core if swapped else args.backend_a_core),
        "--backend-b-core",
        str(args.backend_a_core if swapped else args.backend_b_core),
        "--direct-oracle",
        str(args.direct_oracle),
        "--direct-json",
        str(args.direct_json),
        "--negative-tests",
        str(args.bootstrap_negative_report),
        "--report",
        str(args.work_dir / "should_not_exist_verification_report.json"),
    ]


def copy_fixture(args: argparse.Namespace, name: str) -> Path:
    destination = args.work_dir / "fixtures" / name
    shutil.copytree(args.artifact_dir, destination)
    return destination


def mutate_binary(path: Path, operation: Callable[[bytearray], None]) -> None:
    data = bytearray(path.read_bytes())
    operation(data)
    path.write_bytes(data)


def pair_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def persistent_index(pair_order: Path, h: int) -> int:
    for row in pair_rows(pair_order):
        shift = int(row["shift"])
        base = 240000005594 + h
        if any((base - shift) % p == 0 and (base - shift) % (p * p) != 0 for p in (3, 7, 11, 23)):
            return int(row["pair_index"])
    raise TestFailure("cannot find persistent-covered pair for mutation")


def mutate_pair_order(fixture: Path) -> None:
    path = fixture / "pair_order.csv"
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[1], lines[2] = lines[2], lines[1]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def mutate_pair_hash(fixture: Path) -> None:
    manifest = read_json(fixture / "mask_manifest.json")
    manifest["pair_order_sha256"] = "00" * 32
    write_json(fixture / "mask_manifest.json", manifest)


def flip_one_bit(fixture: Path) -> None:
    mutate_binary(fixture / "backend_a_masks.bin", lambda data: data.__setitem__(HEADER_SIZE + ROW_PREFIX_SIZE, data[HEADER_SIZE + ROW_PREFIX_SIZE] ^ 1))


def delete_row(fixture: Path) -> None:
    path = fixture / "backend_a_masks.bin"
    data = path.read_bytes()
    path.write_bytes(data[:HEADER_SIZE] + data[HEADER_SIZE + ROW_SIZE:])


def duplicate_row(fixture: Path) -> None:
    path = fixture / "backend_a_masks.bin"
    data = bytearray(path.read_bytes())
    data[HEADER_SIZE + ROW_SIZE:HEADER_SIZE + 2 * ROW_SIZE] = data[HEADER_SIZE:HEADER_SIZE + ROW_SIZE]
    path.write_bytes(data)


def append_extra(fixture: Path) -> None:
    path = fixture / "backend_a_masks.bin"
    path.write_bytes(path.read_bytes() + b"EXTRA")


def truncate_mask(fixture: Path) -> None:
    path = fixture / "backend_a_masks.bin"
    path.write_bytes(path.read_bytes()[:-1])


def wrong_t(fixture: Path) -> None:
    def operation(data: bytearray) -> None:
        offset = HEADER_SIZE
        n, h, k, active, t_value = POINT_PREFIX.unpack_from(data, offset)
        POINT_PREFIX.pack_into(data, offset, n, h, k, active, t_value + 1)
    mutate_binary(fixture / "backend_a_masks.bin", operation)


def relabel_class(fixture: Path) -> None:
    def operation(data: bytearray) -> None:
        n, h, k, active, t_value = POINT_PREFIX.unpack_from(data, HEADER_SIZE)
        POINT_PREFIX.pack_into(data, HEADER_SIZE, n, h + 360, k, active, t_value)
    mutate_binary(fixture / "backend_a_masks.bin", operation)


def reorder_points(fixture: Path) -> None:
    path = fixture / "backend_a_masks.bin"
    data = bytearray(path.read_bytes())
    first = bytes(data[HEADER_SIZE:HEADER_SIZE + ROW_SIZE])
    second = bytes(data[HEADER_SIZE + ROW_SIZE:HEADER_SIZE + 2 * ROW_SIZE])
    data[HEADER_SIZE:HEADER_SIZE + ROW_SIZE] = second
    data[HEADER_SIZE + ROW_SIZE:HEADER_SIZE + 2 * ROW_SIZE] = first
    path.write_bytes(data)


def mark_persistent_winner(fixture: Path) -> None:
    index = persistent_index(fixture / "pair_order.csv", -720)
    for name in ("backend_a_masks.bin", "backend_b_masks.bin"):
        path = fixture / name
        data = bytearray(path.read_bytes())
        prefix = HEADER_SIZE
        n, h, k, active, t_value = POINT_PREFIX.unpack_from(data, prefix)
        byte_offset = prefix + ROW_PREFIX_SIZE + index // 8
        bit_value = 1 << (index % 8)
        if data[byte_offset] & bit_value:
            raise TestFailure("chosen persistent pair is unexpectedly already marked winner")
        data[byte_offset] |= bit_value
        POINT_PREFIX.pack_into(data, prefix, n, h, k, active, t_value + 1)
        path.write_bytes(data)


def mismatch_source(fixture: Path) -> None:
    metadata = read_json(fixture / "metadata.json")
    metadata["source_commit"] = "406677c3b095d2125a4a439c76b3a8d6788cb1da"
    write_json(fixture / "metadata.json", metadata)


def mismatch_baseline(fixture: Path) -> None:
    metadata = read_json(fixture / "metadata.json")
    metadata["protected_baseline_and_prior_pilot_hashes_before"]["baseline_manifest_sha256"] = "ff" * 32
    write_json(fixture / "metadata.json", metadata)


MUTATIONS: dict[str, Callable[[Path], None] | None] = {
    "changed_pair_ordering": mutate_pair_order,
    "changed_pair_order_hash": mutate_pair_hash,
    "one_flipped_winner_bit": flip_one_bit,
    "mask_row_deletion": delete_row,
    "duplicated_row": duplicate_row,
    "extra_bytes": append_extra,
    "truncated_mask": truncate_mask,
    "incorrect_popcount_T": wrong_t,
    "class_relabeling": relabel_class,
    "point_reordering": reorder_points,
    "persistent_covered_pair_marked_winner": mark_persistent_winner,
    "swapped_backend_identity": None,
    "source_commit_mismatch": mismatch_source,
    "baseline_hash_mismatch": mismatch_baseline,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--backend-a-core", type=Path, required=True)
    parser.add_argument("--backend-b-core", type=Path, required=True)
    parser.add_argument("--direct-oracle", type=Path, required=True)
    parser.add_argument("--direct-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        args.source_root = args.source_root.resolve()
        args.artifact_dir = args.artifact_dir.resolve()
        args.work_dir = args.work_dir.resolve()
        args.work_dir.mkdir(parents=True, exist_ok=True)
        args.bootstrap_negative_report = args.work_dir / "bootstrap_negative_tests.json"
        write_json(
            args.bootstrap_negative_report,
            {
                "schema": "a303656-k4-survivor-negative-tests-v1",
                "tests": [{"name": name, "rejected": True, "return_code": 2} for name in TEST_NAMES],
            },
        )

        tests: list[dict[str, object]] = []
        for name in TEST_NAMES:
            fixture = copy_fixture(args, name)
            mutation = MUTATIONS[name]
            if mutation is not None:
                mutation(fixture)
            command = base_command(args, fixture, swapped=name == "swapped_backend_identity")
            result = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            rejected = result.returncode != 0
            tests.append(
                {
                    "name": name,
                    "rejected": rejected,
                    "return_code": result.returncode,
                    "stderr_last_line": result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "",
                }
            )
            if not rejected:
                raise TestFailure(f"negative test unexpectedly accepted: {name}")
        report = {"schema": "a303656-k4-survivor-negative-tests-v1", "tests": tests}
        write_json(args.output, report)
        print("K4_SURVIVOR_NEGATIVE_TESTS_PASS")
        return 0
    except (TestFailure, OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        print(f"K4_SURVIVOR_NEGATIVE_TESTS_FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
