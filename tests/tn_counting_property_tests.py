#!/usr/bin/env python3
"""Focused T(n) semantics checks across both backends and the GMP oracle."""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path


def run_backend(binary: Path, out_dir: Path) -> None:
    out_dir.mkdir()
    completed = subprocess.run(
        [
            str(binary),
            "--low", "2",
            "--high", "100",
            "--interval-id", "FIXTURE-TN-SEMANTICS",
            "--out-dir", str(out_dir),
            "--emit-all-records",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"fixture backend failed rc={completed.returncode}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )


def records(directory: Path) -> dict[int, dict]:
    result = {}
    for line in (directory / "low_t.jsonl").read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        result[int(record["n"])] = record
    return result


def canonical(remainder: int) -> tuple[int, int] | None:
    for a in range(math.isqrt(remainder // 2) + 1):
        b = math.isqrt(remainder - a * a)
        if a <= b and a * a + b * b == remainder:
            return a, b
    return None


def winners_by_key(record: dict) -> dict[tuple[int, int], dict]:
    return {
        (int(row["c"]), int(row["d"])): row
        for row in record["winning_exponent_pairs"]
    }


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bitset", type=Path, required=True)
    parser.add_argument("--clean", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    args.work_dir.mkdir(parents=True, exist_ok=False)
    directories = {
        "bitset": args.work_dir / "bitset",
        "clean": args.work_dir / "clean",
        "oracle": args.work_dir / "oracle",
    }
    for role, binary in (("bitset", args.bitset), ("clean", args.clean), ("oracle", args.oracle)):
        run_backend(binary, directories[role])
    count_bytes = {(directory / "counts.csv").read_bytes() for directory in directories.values()}
    assert len(count_bytes) == 1
    all_records = {role: records(directory) for role, directory in directories.items()}
    assert all(set(value) == set(range(2, 100)) for value in all_records.values())

    reference = all_records["oracle"]
    for n, record in reference.items():
        winners = record["winning_exponent_pairs"]
        assert len(winners) == int(record["T"])
        keys = [(int(row["c"]), int(row["d"])) for row in winners]
        assert len(keys) == len(set(keys))
        for row in winners:
            c, d = int(row["c"]), int(row["d"])
            shift = int(row["shift"])
            remainder = int(row["remainder"])
            a, b = int(row["a"]), int(row["b"])
            assert shift == 3**c + 5**d
            assert remainder == n - shift
            assert 0 <= a <= b and a * a + b * b == remainder
            assert canonical(remainder) == (a, b)

    # Remainder zero contributes exactly once for its source pair.
    n2 = winners_by_key(reference[2])
    assert n2[(0, 0)]["remainder"] == "0"
    assert (n2[(0, 0)]["a"], n2[(0, 0)]["b"]) == ("0", "0")

    # Real collision: (1,2) and (3,0) both have shift 28 and both contribute.
    n28 = winners_by_key(reference[28])
    assert int(n28[(1, 2)]["shift"]) == int(n28[(3, 0)]["shift"]) == 28
    assert int(n28[(1, 2)]["remainder"]) == int(n28[(3, 0)]["remainder"]) == 0

    # 25 has two unordered representations, but source pair (0,0) contributes once.
    representations_25 = [
        (a, math.isqrt(25 - a * a))
        for a in range(math.isqrt(25 // 2) + 1)
        if math.isqrt(25 - a * a) ** 2 == 25 - a * a
    ]
    assert representations_25 == [(0, 5), (3, 4)]
    n27_rows = [
        row for row in reference[27]["winning_exponent_pairs"]
        if (int(row["c"]), int(row["d"])) == (0, 0)
    ]
    assert len(n27_rows) == 1
    assert (n27_rows[0]["a"], n27_rows[0]["b"]) == ("0", "5")

    # Activation is exact at s-1/s/s+1, including remainder 0 and 1.
    for c, d in ((0, 0), (1, 0), (0, 1), (2, 1)):
        shift = 3**c + 5**d
        key = (c, d)
        if shift - 1 >= 2:
            assert key not in winners_by_key(reference[shift - 1])
        at_shift = winners_by_key(reference[shift])[key]
        after_shift = winners_by_key(reference[shift + 1])[key]
        assert (at_shift["remainder"], at_shift["a"], at_shift["b"]) == ("0", "0", "0")
        assert (after_shift["remainder"], after_shift["a"], after_shift["b"]) == ("1", "0", "1")

    # A count above four demonstrates absence of first-hit or saturated counting.
    rich_n = next(n for n, record in reference.items() if int(record["T"]) >= 4)
    rich_count = int(reference[rich_n]["T"])
    assert rich_count == len(reference[rich_n]["winning_exponent_pairs"])
    assert rich_count >= 4

    for role in ("bitset", "clean"):
        normalized = []
        oracle_normalized = []
        for n in range(2, 100):
            left = dict(all_records[role][n])
            right = dict(reference[n])
            left.pop("implementation_id", None)
            right.pop("implementation_id", None)
            normalized.append(left)
            oracle_normalized.append(right)
        assert normalized == oracle_normalized

    print("TN_COUNTING_PROPERTY_TESTS_PASS")
    print(f"duplicate_shift_n=28 multiple_rep_remainder=25 no_early_termination_n={rich_n} T={rich_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
