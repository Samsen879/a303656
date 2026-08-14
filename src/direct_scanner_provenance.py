#!/usr/bin/env python3
"""Generate and audit fail-closed provenance for direct-scanner test outputs."""
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
    "search_twosquares_bitset": {
        "method": "direct_two_squares_bitset_x_outer",
        "executable": "search_twosquares_bitset",
        "source": "search_twosquares_bitset.cpp",
    },
    "search_twosquares_clean": {
        "method": "clean_room_direct_two_squares_y_outer",
        "executable": "search_twosquares_clean",
        "source": "search_twosquares_clean.cpp",
    },
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def require_file(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_file():
        raise ValueError(f"missing {label}: {resolved}")
    return resolved


def run_command(args: argparse.Namespace) -> int:
    identity = IDENTITIES[args.implementation_id]
    executable = require_file(args.executable, "executable")
    source = require_file(args.source, "source")
    if executable.name != identity["executable"]:
        raise ValueError("executable filename does not match implementation identity")
    if source.name != identity["source"]:
        raise ValueError("source filename does not match implementation identity")

    args.out_dir.mkdir(parents=True, exist_ok=False)
    output = (args.out_dir / "output.json").resolve()
    candidates = (args.out_dir / "candidates.txt").resolve()
    stdout_path = (args.out_dir / "stdout.log").resolve()
    stderr_path = (args.out_dir / "stderr.log").resolve()
    manifest_path = (args.out_dir / "manifest.json").resolve()
    command = [
        str(executable),
        "--low", str(args.low),
        "--high", str(args.high),
        "--C", str(args.C),
        "--D", str(args.D),
        "--json", str(output),
        "--candidates", str(candidates),
        "--quiet",
    ]
    started = perf_counter()
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = perf_counter() - started
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    if completed.returncode not in (0, 1):
        raise ValueError(f"scanner returned unexpected code {completed.returncode}")
    if not output.is_file() or not candidates.is_file():
        raise ValueError("scanner omitted output or candidate sidecar")
    data = load_object(output)
    if data.get("implementation_id") != args.implementation_id:
        raise ValueError("scanner output implementation identity mismatch")
    if data.get("method") != identity["method"]:
        raise ValueError("scanner output method mismatch")
    if (int(data["low"]), int(data["high"]), int(data["C"]), int(data["D"])) != (
        args.low,
        args.high,
        args.C,
        args.D,
    ):
        raise ValueError("scanner output parameters differ from exact CLI arguments")
    listed = candidates.read_text(encoding="utf-8").split()
    declared = [str(value) for value in data["candidates"]]
    if listed != declared or int(data["candidate_count"]) != len(declared):
        raise ValueError("candidate output mismatch")
    if completed.returncode != (0 if declared else 1):
        raise ValueError("scanner return code does not match candidate status")

    compiler_version = subprocess.run(
        [args.compiler, "--version"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()
    payload = {
        "schema": "a303656-direct-scanner-provenance-v1",
        "generation_timestamp_utc": utc_now(),
        "implementation_id": args.implementation_id,
        "method": identity["method"],
        "executable": {
            "path": str(executable),
            "filename": executable.name,
            "sha256": digest(executable),
        },
        "source": {
            "path": str(source),
            "filename": source.name,
            "sha256": digest(source),
            "commit": args.source_commit,
        },
        "compiler": {
            "command": args.compiler,
            "version": compiler_version,
        },
        "gmp_version": args.gmp_version,
        "exact_cli_arguments": command,
        "interval": {
            "low": str(args.low),
            "high": str(args.high),
            "C": args.C,
            "D": args.D,
        },
        "scanner_return_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "output": {"path": str(output), "sha256": digest(output)},
        "candidates": {"path": str(candidates), "sha256": digest(candidates)},
        "stdout": {"path": str(stdout_path), "sha256": digest(stdout_path)},
        "stderr": {"path": str(stderr_path), "sha256": digest(stderr_path)},
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"PROVENANCE_RUN_PASS implementation_id={args.implementation_id}")
    print(f"manifest={manifest_path}")
    return 0


def required(mapping: dict, key: str, context: str):
    if key not in mapping:
        raise ValueError(f"{context} missing {key}")
    return mapping[key]


def audit_slot(path: Path, expected_id: str, expected_commit: str) -> dict:
    manifest = load_object(path)
    if manifest.get("schema") != "a303656-direct-scanner-provenance-v1":
        raise ValueError(f"{expected_id} provenance schema mismatch")
    actual_id = manifest.get("implementation_id")
    if actual_id != expected_id:
        raise ValueError(
            f"{expected_id} slot implementation identity/provenance mismatch: got {actual_id}"
        )
    identity = IDENTITIES[expected_id]
    if manifest.get("method") != identity["method"]:
        raise ValueError(f"{expected_id} method provenance mismatch")
    if not manifest.get("generation_timestamp_utc"):
        raise ValueError(f"{expected_id} generation timestamp missing")
    if not manifest.get("gmp_version"):
        raise ValueError(f"{expected_id} GMP version missing")
    compiler = required(manifest, "compiler", expected_id)
    if not compiler.get("command") or not compiler.get("version"):
        raise ValueError(f"{expected_id} compiler provenance missing")

    executable_row = required(manifest, "executable", expected_id)
    source_row = required(manifest, "source", expected_id)
    if executable_row.get("filename") != identity["executable"]:
        raise ValueError(f"{expected_id} executable identity mismatch")
    if source_row.get("filename") != identity["source"]:
        raise ValueError(f"{expected_id} source identity mismatch")
    if source_row.get("commit") != expected_commit:
        raise ValueError(f"{expected_id} source commit mismatch")

    for label in ("executable", "source", "output", "candidates", "stdout", "stderr"):
        row = required(manifest, label, expected_id)
        artifact = require_file(Path(required(row, "path", label)), label)
        actual_hash = digest(artifact)
        if actual_hash != row.get("sha256"):
            raise ValueError(f"{expected_id} {label} SHA256/provenance mismatch")

    output_path = Path(manifest["output"]["path"])
    candidate_path = Path(manifest["candidates"]["path"])
    output = load_object(output_path)
    if output.get("implementation_id") != expected_id or output.get("method") != identity["method"]:
        raise ValueError(f"{expected_id} output identity mismatch")
    interval = required(manifest, "interval", expected_id)
    expected_values = (
        int(interval["low"]),
        int(interval["high"]),
        int(interval["C"]),
        int(interval["D"]),
    )
    output_values = (int(output["low"]), int(output["high"]), int(output["C"]), int(output["D"]))
    if output_values != expected_values:
        raise ValueError(f"{expected_id} output interval differs from manifest")

    cli = required(manifest, "exact_cli_arguments", expected_id)
    if not isinstance(cli, list) or not cli or str(Path(cli[0]).resolve()) != manifest["executable"]["path"]:
        raise ValueError(f"{expected_id} exact CLI executable mismatch")
    expected_cli = [
        manifest["executable"]["path"],
        "--low", str(expected_values[0]),
        "--high", str(expected_values[1]),
        "--C", str(expected_values[2]),
        "--D", str(expected_values[3]),
        "--json", manifest["output"]["path"],
        "--candidates", manifest["candidates"]["path"],
        "--quiet",
    ]
    if cli != expected_cli:
        raise ValueError(f"{expected_id} exact CLI arguments mismatch")
    declared = [str(value) for value in output["candidates"]]
    if candidate_path.read_text(encoding="utf-8").split() != declared:
        raise ValueError(f"{expected_id} candidate sidecar mismatch")
    if int(output["candidate_count"]) != len(declared):
        raise ValueError(f"{expected_id} candidate count mismatch")
    expected_return_code = 0 if declared else 1
    if int(manifest.get("scanner_return_code", -1)) != expected_return_code:
        raise ValueError(f"{expected_id} scanner return-code provenance mismatch")
    if float(manifest.get("elapsed_seconds", -1)) < 0:
        raise ValueError(f"{expected_id} elapsed-time provenance mismatch")
    return manifest


def audit_pair_command(args: argparse.Namespace) -> int:
    x = audit_slot(args.x_manifest.resolve(), "search_twosquares_bitset", args.expected_source_commit)
    y = audit_slot(args.y_manifest.resolve(), "search_twosquares_clean", args.expected_source_commit)
    if x["source"]["sha256"] == y["source"]["sha256"]:
        raise ValueError("x/y source hashes are unexpectedly identical")
    if x["executable"]["sha256"] == y["executable"]["sha256"]:
        raise ValueError("x/y executable hashes are unexpectedly identical")
    if x["interval"] != y["interval"]:
        raise ValueError("x/y interval provenance mismatch")
    x_output = load_object(Path(x["output"]["path"]))
    y_output = load_object(Path(y["output"]["path"]))
    for key in (
        "low",
        "high",
        "C",
        "D",
        "admissible_rectangle_pair_count_at_high",
        "distinct_shift_count_at_high",
        "duplicate_pair_count",
        "integers_tested",
        "shifts_processed_before_termination",
        "unordered_square_pairs_enumerated",
        "candidate_count",
        "candidates",
    ):
        if x_output.get(key) != y_output.get(key):
            raise ValueError(f"x/y mathematical output mismatch in {key}")
    print("PROVENANCE_AUDIT_PASS")
    print(f"x_executable_sha256={x['executable']['sha256']}")
    print(f"y_executable_sha256={y['executable']['sha256']}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    subparsers = root.add_subparsers(dest="action", required=True)
    run = subparsers.add_parser("run")
    run.add_argument("--implementation-id", choices=sorted(IDENTITIES), required=True)
    run.add_argument("--executable", type=Path, required=True)
    run.add_argument("--source", type=Path, required=True)
    run.add_argument("--source-commit", required=True)
    run.add_argument("--compiler", required=True)
    run.add_argument("--gmp-version", required=True)
    run.add_argument("--low", type=int, required=True)
    run.add_argument("--high", type=int, required=True)
    run.add_argument("--C", type=int, required=True)
    run.add_argument("--D", type=int, required=True)
    run.add_argument("--out-dir", type=Path, required=True)
    run.set_defaults(function=run_command)

    audit_pair = subparsers.add_parser("audit-pair")
    audit_pair.add_argument("--x-manifest", type=Path, required=True)
    audit_pair.add_argument("--y-manifest", type=Path, required=True)
    audit_pair.add_argument("--expected-source-commit", required=True)
    audit_pair.set_defaults(function=audit_pair_command)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        return args.function(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"PROVENANCE_ERROR {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
