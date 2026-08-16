#!/usr/bin/env python3
"""Build both exact implementations, compare raw arrays, and emit compact evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("NumPy is required; install the repository requirements.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
INF = 255


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout, file=sys.stderr)
        raise SystemExit(f"command failed with {result.returncode}: {command[0]}")
    return {"command": command, "return_code": result.returncode, "stdout": result.stdout}


def normalize_command(command: list[str], scratch: Path) -> list[str]:
    repo_root = ROOT.parents[1]
    normalized = []
    for token in command:
        if token == sys.executable:
            normalized.append("<python>")
        else:
            normalized.append(token.replace(str(repo_root), "<repo>").replace(str(scratch), "<scratch>"))
    return normalized


def records(array: np.ndarray) -> list[list[int]]:
    values = array[2:]
    if np.any(values == INF):
        raise AssertionError("uncovered value in fixed domain")
    prefix = np.maximum.accumulate(values)
    change = np.empty(prefix.size, dtype=bool)
    change[0] = True
    change[1:] = prefix[1:] > prefix[:-1]
    return [[int(index) + 2, int(array[int(index) + 2])] for index in np.flatnonzero(change)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.N < 2 or len(args.source_commit) != 40 or any(c not in "0123456789abcdef" for c in args.source_commit):
        raise SystemExit("invalid N or source commit")
    args.scratch.mkdir(parents=True, exist_ok=True)
    binary = args.scratch / "method_b"
    commands = [
        run(["g++", "-O3", "-std=c++20", "-Wall", "-Wextra", "-pedantic", str(TOOLS / "method_b.cpp"), "-o", str(binary)]),
        run([sys.executable, str(TOOLS / "method_a.py"), "--N", str(args.N), "--outdir", str(args.scratch)]),
        run([str(binary), str(args.N), str(args.scratch)]),
    ]
    for record in commands:
        record["command"] = normalize_command(record["command"], args.scratch)
    pairs = {}
    arrays = {}
    for name in ("S2", "C3", "C5"):
        a = args.scratch / f"method_a_{name}.uint8"
        b = args.scratch / f"method_b_{name}.uint8"
        if a.stat().st_size != args.N + 1 or b.stat().st_size != args.N + 1:
            raise AssertionError((name, "raw array size"))
        hash_a, hash_b = sha256(a), sha256(b)
        if hash_a != hash_b:
            raise AssertionError((name, "hash mismatch"))
        array_a = np.memmap(a, dtype=np.uint8, mode="r", shape=(args.N + 1,))
        array_b = np.memmap(b, dtype=np.uint8, mode="r", shape=(args.N + 1,))
        if not np.array_equal(array_a, array_b):
            raise AssertionError((name, "byte mismatch"))
        pairs[name] = {"method_a": hash_a, "method_b": hash_b, "byte_for_byte_equal": True}
        arrays[name] = array_a

    c3_records, c5_records = records(arrays["C3"]), records(arrays["C5"])
    claimed_n, claimed_c = 47_708_696, 13
    claimed_point = {"n": claimed_n, "status": "OUTSIDE_REPLAY_DOMAIN"}
    if args.N >= claimed_n:
        powers5, value = [], 1
        while value <= claimed_n:
            powers5.append(value)
            value *= 5
        smaller_pairs = 0
        for c in range(claimed_c):
            for p5 in powers5:
                shift = 3**c + p5
                if shift > claimed_n:
                    break
                smaller_pairs += 1
                if arrays["S2"][claimed_n - shift]:
                    raise AssertionError((claimed_n, c, p5, "smaller-c hit"))
        witness = {"a": 2988, "b": 6098, "c": 13, "d": 4}
        if witness["a"]**2 + witness["b"]**2 + 3**witness["c"] + 5**witness["d"] != claimed_n:
            raise AssertionError("claimed witness")
        claimed_point = {
            "n": claimed_n, "C3": claimed_c, "smaller_c_pairs_checked": smaller_pairs,
            "status": "VERIFIED", "witness": witness,
        }

    result = {
        "schema": "a303656-one-sided-strip-finite-replay-v1",
        "source_commit": args.source_commit,
        "N": args.N,
        "n_domain": [2, args.N],
        "arrays": pairs,
        "raw_arrays_committed": False,
        "s2_count": int(np.count_nonzero(arrays["S2"])),
        "max_C3": int(arrays["C3"][2:].max()),
        "max_C5": int(arrays["C5"][2:].max()),
        "uncovered_C3": int(np.count_nonzero(arrays["C3"][2:] == INF)),
        "uncovered_C5": int(np.count_nonzero(arrays["C5"][2:] == INF)),
        "C3_records": c3_records,
        "C5_records": c5_records,
        "claimed_point": claimed_point,
        "commands": commands,
        "verdict": "PASS_EXACT_FINITE_DOMAIN_ONLY",
    }
    if args.expected:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        checks = {
            "N": result["N"] == expected["N"],
            "S2_hash": pairs["S2"]["method_a"] == expected["hashes"]["S2"],
            "C3_hash": pairs["C3"]["method_a"] == expected["hashes"]["C3"],
            "C5_hash": pairs["C5"]["method_a"] == expected["hashes"]["C5"],
            "s2_count": result["s2_count"] == expected["s2_count"],
            "max_C3": result["max_C3"] == expected["max_C3"],
            "max_C5": result["max_C5"] == expected["max_C5"],
            "uncovered_C3": result["uncovered_C3"] == expected["uncovered_C3"],
            "uncovered_C5": result["uncovered_C5"] == expected["uncovered_C5"],
            "C3_records": result["C3_records"] == expected["C3_records"],
            "C5_records": result["C5_records"] == expected["C5_records"],
        }
        if not all(checks.values()):
            raise AssertionError(checks)
        result["expected_crosscheck"] = checks
        result["external_packet_sha256"] = expected["external_packet_sha256"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "verdict": result["verdict"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
