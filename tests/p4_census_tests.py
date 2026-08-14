#!/usr/bin/env python3
"""Unit and required negative tests for the fixed-P4 census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from p4_census_common import (  # noqa: E402
    A, B, CLASS_COUNT, COUNT_FIELDS, L, MASK_BYTES, M4, N0, PAIR_COUNT,
    PANEL_FIELDS, START_COMMIT, CensusError, construct_panel, coverage_set,
    mask_popcount, tuple_residue_mod_l,
)


HEADER = struct.Struct("<8sIIIIII32s32s32s")


def unit_tests() -> None:
    assert M4 == 9 * 49 * 121 * 529
    assert L == 40 * M4
    panel, specs, pairs = construct_panel(ROOT)
    assert len(specs) == CLASS_COUNT == 87
    assert len(pairs) == PAIR_COUNT == 407
    assert len(panel) == 4838
    assert Counter(len([row for row in panel if row["class_index"] == spec.index]) for spec in specs) == {55: 34, 56: 53}
    assert len({row["n"] for row in panel}) == len(panel)
    assert all(A <= row["n"] <= B and row["n"] % 40 == N0 % 40 for row in panel)
    assert [spec.class_id for spec in specs[:3]] == ["CAL-216", "CAL-227", "CAL-230"]
    assert [spec.coverage for spec in specs[:3]] == [216, 227, 230]
    assert all(spec.tuple4[0] == 2 and spec.coverage == 231 for spec in specs[3:])
    assert all(tuple_residue_mod_l(spec.tuple4) == spec.residue for spec in specs)
    assert len({spec.residue for spec in specs}) == 87
    assert [(pair.c, pair.d) for pair in pairs if pair.shift == 28] == [(1, 2), (3, 0)]
    valid_tail = bytes(MASK_BYTES - 1) + b"\x40"
    assert mask_popcount(valid_tail) == 1
    try:
        mask_popcount(bytes(MASK_BYTES - 1) + b"\x80")
    except CensusError:
        pass
    else:
        raise AssertionError("unused bit 407 was not rejected")
    # Exact-one semantics must exclude a p^2 congruence, not treat it as covered.
    found_square_divisible = False
    for spec in specs:
        for p, residue in zip((3, 7, 11, 23), spec.tuple4):
            for pair in pairs:
                if (residue - pair.shift) % (p * p) == 0:
                    assert pair.index not in coverage_set(spec.tuple4, pairs) or any(
                        (other_residue - pair.shift) % other_p == 0 and (other_residue - pair.shift) % (other_p * other_p) != 0
                        for other_p, other_residue in zip((3, 7, 11, 23), spec.tuple4)
                    )
                    found_square_divisible = True
                    break
            if found_square_divisible:
                break
        if found_square_divisible:
            break
    assert found_square_divisible


def edit_csv(path: Path, mutator: Callable[[list[str], list[list[str]]], None]) -> None:
    with path.open(newline="", encoding="utf-8") as stream:
        all_rows = list(csv.reader(stream))
    header, rows = all_rows[0], all_rows[1:]
    mutator(header, rows)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def replace_metadata(path: Path, mutator: Callable[[dict], None]) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutator(value)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def change_field(header: list[str], rows: list[list[str]], row_index: int, field: str, value: str) -> None:
    rows[row_index][header.index(field)] = value


def flip_mask(path: Path, ordinal: int, pair_index: int) -> bytes:
    data = bytearray(path.read_bytes())
    offset = HEADER.size + ordinal * MASK_BYTES + pair_index // 8
    data[offset] ^= 1 << (pair_index % 8)
    path.write_bytes(data)
    return bytes(data[HEADER.size + ordinal * MASK_BYTES:HEADER.size + (ordinal + 1) * MASK_BYTES])


def negative_tests(artifact: Path, source_commit: str, output: Path) -> None:
    panel, specs, _ = construct_panel(ROOT)

    def missing_maximizer(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: r.__setitem__(slice(None), [row for row in r if row[h.index("class_index")] != "86"]))

    def extra_class(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: r.append(list(r[-1])))

    def changed_tuple(copy: Path) -> None:
        def mutate(header: list[str], rows: list[list[str]]) -> None:
            index = next(i for i, row in enumerate(rows) if row[header.index("class_index")] == "3")
            change_field(header, rows, index, "t7", "8")
        edit_csv(copy / "class_panel.csv", mutate)

    def incorrect_g(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: change_field(h, r, 0, "G", "215"))

    def altered_crt(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: change_field(h, r, 0, "crt_residue", str(int(r[0][h.index("crt_residue")]) + 1)))

    def missing_point(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: r.pop(0))

    def duplicated_point(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: change_field(h, r, 1, "n", r[0][h.index("n")]))

    def outside(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: change_field(h, r, 0, "n", str(A - 1)))

    def incongruent(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: change_field(h, r, 0, "n", str(int(r[0][h.index("n")]) + 40)))

    def reorder(copy: Path) -> None:
        edit_csv(copy / "class_panel.csv", lambda h, r: r.__setitem__(slice(0, 2), [r[1], r[0]]))

    def flipped(copy: Path) -> None:
        flip_mask(copy / "backend_a_masks.bin", 0, 0)

    def popcount(copy: Path) -> None:
        edit_csv(copy / "backend_a_counts.csv", lambda h, r: change_field(h, r, 0, "T", str(int(r[0][h.index("T")]) + 1)))

    def persistent(copy: Path) -> None:
        pair_index = min(specs[0].covered)
        mask_a = flip_mask(copy / "backend_a_masks.bin", 0, pair_index)
        mask_b = flip_mask(copy / "backend_b_masks.bin", 0, pair_index)
        assert mask_a == mask_b
        for name in ("backend_a_counts.csv", "backend_b_counts.csv"):
            def mutate(header: list[str], rows: list[list[str]]) -> None:
                change_field(header, rows, 0, "T", str(int(rows[0][header.index("T")]) + 1))
                change_field(header, rows, 0, "mask_sha256", hashlib.sha256(mask_a).hexdigest())
            edit_csv(copy / name, mutate)

    def identity_swap(copy: Path) -> None:
        a = (copy / "backend_a_masks.bin").read_bytes()
        b = (copy / "backend_b_masks.bin").read_bytes()
        (copy / "backend_a_masks.bin").write_bytes(b)
        (copy / "backend_b_masks.bin").write_bytes(a)

    def source_mismatch(copy: Path) -> None:
        replace_metadata(copy / "metadata.json", lambda value: value.__setitem__("source_commit", START_COMMIT))

    def baseline_mismatch(copy: Path) -> None:
        def mutate(value: dict) -> None:
            key = "analysis/p4_residue_landscape/maximizers.json"
            value["protected_baseline_and_landscape_sha256"][key] = "0" * 64
        replace_metadata(copy / "metadata.json", mutate)

    def truncated(copy: Path) -> None:
        path = copy / "backend_a_masks.bin"
        path.write_bytes(path.read_bytes()[:-1])

    def extra_bytes(copy: Path) -> None:
        path = copy / "backend_a_masks.bin"
        path.write_bytes(path.read_bytes() + b"\x00")

    mutations: list[tuple[str, Callable[[Path], None]]] = [
        ("missing_maximizing_class", missing_maximizer), ("extra_class", extra_class),
        ("changed_constrained_tuple", changed_tuple), ("incorrect_G", incorrect_g),
        ("altered_CRT_residue", altered_crt), ("missing_point", missing_point),
        ("duplicated_point", duplicated_point), ("point_outside_activation_cell", outside),
        ("point_not_congruent_to_class", incongruent), ("changed_class_ordering", reorder),
        ("flipped_mask_bit", flipped), ("popcount_T_mismatch", popcount),
        ("persistent_covered_winner", persistent), ("backend_identity_swap", identity_swap),
        ("source_commit_mismatch", source_mismatch),
        ("baseline_or_landscape_hash_mismatch", baseline_mismatch),
        ("truncated_mask_bytes", truncated), ("extra_mask_bytes", extra_bytes),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="p4_census_negative_") as temporary:
        base = Path(temporary)
        for index, (name, mutation) in enumerate(mutations):
            case = base / f"case_{index:02d}"
            shutil.copytree(artifact, case)
            mutation(case)
            report = base / f"report_{index:02d}.json"
            command = [
                sys.executable, str(ROOT / "src/p4_census_verify.py"),
                "--root", str(ROOT), "--artifact-dir", str(case),
                "--source-commit", source_commit, "--source-parent", START_COMMIT,
                "--negative-test-mode",
                "--output", str(report),
            ]
            completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed.returncode == 0:
                raise AssertionError(f"negative test unexpectedly accepted: {name}")
            results.append({
                "name": name, "return_code": completed.returncode, "rejected": True,
                "stderr_tail": completed.stderr.decode("utf-8", "replace")[-500:],
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"schema": "a303656-p4-census-negative-tests-v1", "tests": results}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-only", action="store_true")
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    unit_tests()
    if args.unit_only:
        print("P4_CENSUS_UNIT_TESTS_PASS")
        return 0
    if args.artifact_dir is None or args.source_commit is None or args.output is None:
        raise SystemExit("--artifact-dir, --source-commit, and --output are required for negative tests")
    negative_tests(args.artifact_dir.resolve(), args.source_commit, args.output.resolve())
    print("P4_CENSUS_NEGATIVE_TESTS_PASS count=18")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
