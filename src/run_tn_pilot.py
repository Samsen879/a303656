#!/usr/bin/env python3
"""Run one bounded T(n) implementation with automatically derived provenance."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


IDENTITIES = {
    "tn_bitset_annulus_v1": "src/tn_count_bitset.cpp",
    "tn_clean_annulus_v1": "src/tn_count_clean.cpp",
    "tn_gmp_uv_oracle_v1": "tests/tn_gmp_oracle.cpp",
}
FORMAL_INTERVALS = {
    "PILOT-A": (2, 200002),
    "PILOT-B": (240000000001, 240000100001),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def command_output(command: list[str], cwd: Path | None = None) -> str:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def write_object(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--source-tree", type=Path, required=True)
    parser.add_argument("--low", type=int, required=True)
    parser.add_argument("--high", type=int, required=True)
    parser.add_argument("--interval-id", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--compiler", default="g++")
    parser.add_argument("--timeout-seconds", type=int, required=True)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--emit-all-records", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.low <= 1 or args.high <= args.low:
        raise ValueError("invalid half-open interval")
    if args.high - args.low > 200000:
        raise ValueError("bounded runner refuses width above 200000")
    if args.timeout_seconds <= 0:
        raise ValueError("timeout must be positive")
    if args.interval_id in FORMAL_INTERVALS and (args.low, args.high) != FORMAL_INTERVALS[args.interval_id]:
        raise ValueError("formal interval id/bounds mismatch")
    if args.interval_id not in FORMAL_INTERVALS and not args.interval_id.startswith("FIXTURE-"):
        raise ValueError("interval id must be PILOT-A, PILOT-B, or FIXTURE-*")

    binary = args.binary.resolve(strict=True)
    source_tree = Path(command_output(["git", "-C", str(args.source_tree), "rev-parse", "--show-toplevel"]))
    source_commit = command_output(["git", "-C", str(source_tree), "rev-parse", "HEAD"])
    dirty_text = command_output(["git", "-C", str(source_tree), "status", "--porcelain"])
    dirty = bool(dirty_text)
    if dirty and not args.allow_dirty:
        raise ValueError("formal pilot requires a clean source tree")

    identity = command_output([str(binary), "--implementation-id"])
    if identity not in IDENTITIES:
        raise ValueError(f"binary reported unsupported implementation_id: {identity}")
    source_path = (source_tree / IDENTITIES[identity]).resolve(strict=True)
    schema_header = (source_tree / "src/tn_pilot_output.hpp").resolve(strict=True)
    runner_path = Path(__file__).resolve(strict=True)

    formal = args.interval_id in FORMAL_INTERVALS and not args.emit_all_records
    acceptance_eligible = formal and not dirty
    if args.out_dir.exists():
        raise ValueError(f"refusing to overwrite output directory: {args.out_dir}")
    args.out_dir.mkdir(parents=True)
    out_dir = args.out_dir.resolve()
    backend_command = [
        str(binary),
        "--low", str(args.low),
        "--high", str(args.high),
        "--interval-id", args.interval_id,
        "--out-dir", str(out_dir),
    ]
    if args.emit_all_records:
        backend_command.append("--emit-all-records")

    started = perf_counter()
    timed_out = False
    try:
        completed = subprocess.run(
            backend_command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout_seconds,
        )
        return_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        return_code = 124
        stdout = error.stdout if isinstance(error.stdout, str) else ""
        stderr = error.stderr if isinstance(error.stderr, str) else ""
        stderr += f"\nRUNNER_ERROR timeout after {args.timeout_seconds} seconds\n"
    elapsed = perf_counter() - started

    stdout_path = out_dir / "backend_stdout.log"
    stderr_path = out_dir / "backend_stderr.log"
    return_code_path = out_dir / "backend_return_code.txt"
    elapsed_path = out_dir / "backend_elapsed_seconds.txt"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return_code_path.write_text(f"{return_code}\n", encoding="utf-8")
    elapsed_path.write_text(f"{elapsed:.9f}\n", encoding="utf-8")
    if timed_out or return_code != 0:
        raise ValueError(f"backend failed rc={return_code}; raw output retained in {out_dir}")

    required = ["metadata.json", "counts.csv", "low_t.jsonl", "summary.json"]
    for filename in required:
        if not (out_dir / filename).is_file():
            raise ValueError(f"backend omitted {filename}")
    metadata = load_object(out_dir / "metadata.json")
    summary = load_object(out_dir / "summary.json")
    if metadata.get("implementation_id") != identity or summary.get("implementation_id") != identity:
        raise ValueError("backend output identity mismatch")
    interval = metadata.get("interval", {})
    if (int(interval.get("low", -1)), int(interval.get("high_exclusive", -1))) != (args.low, args.high):
        raise ValueError("backend metadata interval mismatch")

    counts_hash = sha256(out_dir / "counts.csv")
    low_hash = sha256(out_dir / "low_t.jsonl")
    summary["counts_csv_sha256"] = counts_hash
    summary["low_t_jsonl_sha256"] = low_hash
    write_object(out_dir / "summary.json", summary)
    metadata.update(
        {
            "generation_timestamp_utc": utc_now(),
            "source_commit": source_commit,
            "source_tree_dirty": dirty,
            "formal_acceptance_eligible": acceptance_eligible,
            "runner_timeout_seconds": args.timeout_seconds,
        }
    )
    write_object(out_dir / "metadata.json", metadata)

    compiler_version = command_output([args.compiler, "--version"])
    gmp_version = (
        command_output([str(binary), "--gmp-version"])
        if identity == "tn_gmp_uv_oracle_v1"
        else "NOT_LINKED_BY_THIS_BACKEND"
    )
    output_names = [
        "metadata.json",
        "counts.csv",
        "low_t.jsonl",
        "summary.json",
        "backend_stdout.log",
        "backend_stderr.log",
        "backend_return_code.txt",
        "backend_elapsed_seconds.txt",
    ]
    provenance = {
        "schema": "a303656-tn-pilot-provenance-v1",
        "generation_timestamp_utc": utc_now(),
        "implementation_id": identity,
        "source_commit": source_commit,
        "source_tree": str(source_tree),
        "source_tree_dirty": dirty,
        "formal_acceptance_eligible": acceptance_eligible,
        "executable": {
            "path": str(binary),
            "filename": binary.name,
            "sha256": sha256(binary),
        },
        "source_files": {
            str(source_path.relative_to(source_tree)): sha256(source_path),
            str(schema_header.relative_to(source_tree)): sha256(schema_header),
            str(runner_path.relative_to(source_tree)): sha256(runner_path),
        },
        "compiler": {"command": args.compiler, "version": compiler_version},
        "gmp_version": gmp_version,
        "exact_runner_cli": sys.argv,
        "exact_backend_cli": backend_command,
        "interval": {
            "id": args.interval_id,
            "low": str(args.low),
            "high_exclusive": str(args.high),
            "number_of_n": args.high - args.low,
        },
        "timeout_seconds": args.timeout_seconds,
        "backend_return_code": return_code,
        "elapsed_seconds": elapsed,
        "outputs_sha256": {name: sha256(out_dir / name) for name in output_names},
        "verifier_report_status": "PENDING_THREE_WAY_VERIFICATION",
    }
    write_object(out_dir / "provenance.json", provenance)
    print(
        f"TN_RUN_PASS implementation_id={identity} interval_id={args.interval_id} "
        f"source_commit={source_commit} dirty={str(dirty).lower()} elapsed_seconds={elapsed:.6f}"
    )
    print(f"output_directory={out_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"RUNNER_ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
