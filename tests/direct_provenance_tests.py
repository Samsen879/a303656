#!/usr/bin/env python3
"""Positive and mandatory negative tests for direct-scanner provenance."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


X_ID = "search_twosquares_bitset"
Y_ID = "search_twosquares_clean"


def invoke(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def checked(command: list[str]) -> subprocess.CompletedProcess[str]:
    completed = invoke(command)
    if completed.returncode != 0:
        raise AssertionError(
            f"command failed rc={completed.returncode}: {command!r}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return completed


def write_result(directory: Path, name: str, result: subprocess.CompletedProcess[str]) -> None:
    (directory / f"{name}.stdout.log").write_text(result.stdout, encoding="utf-8")
    (directory / f"{name}.stderr.log").write_text(result.stderr, encoding="utf-8")
    (directory / f"{name}.return_code.txt").write_text(f"{result.returncode}\n", encoding="utf-8")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--auditor", type=Path, required=True)
    parser.add_argument("--bin-dir", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--compiler", required=True)
    parser.add_argument("--gmp-version", required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    args.work_dir.mkdir(parents=True, exist_ok=False)
    x_dir = args.work_dir / "x"
    y_dir = args.work_dir / "y"

    def generate(identity: str, out_dir: Path) -> subprocess.CompletedProcess[str]:
        return checked(
            [
                args.python,
                str(args.auditor),
                "run",
                "--implementation-id", identity,
                "--executable", str(args.bin_dir / identity),
                "--source", str(args.source_dir / f"{identity}.cpp"),
                "--source-commit", args.source_commit,
                "--compiler", args.compiler,
                "--gmp-version", args.gmp_version,
                "--low", "1",
                "--high", "65",
                "--C", "3",
                "--D", "2",
                "--out-dir", str(out_dir),
            ]
        )

    write_result(args.work_dir, "generate_x", generate(X_ID, x_dir))
    write_result(args.work_dir, "generate_y", generate(Y_ID, y_dir))
    audit_base = [
        args.python,
        str(args.auditor),
        "audit-pair",
        "--expected-source-commit", args.source_commit,
    ]
    positive = checked(
        [
            *audit_base,
            "--x-manifest", str(x_dir / "manifest.json"),
            "--y-manifest", str(y_dir / "manifest.json"),
        ]
    )
    write_result(args.work_dir, "positive_audit", positive)

    swapped = invoke(
        [
            *audit_base,
            "--x-manifest", str(y_dir / "manifest.json"),
            "--y-manifest", str(x_dir / "manifest.json"),
        ]
    )
    write_result(args.work_dir, "swapped_identity_rejection", swapped)
    if swapped.returncode == 0:
        raise AssertionError("swapped x/y provenance was unexpectedly accepted")
    if "implementation identity/provenance mismatch" not in swapped.stderr:
        raise AssertionError(f"swapped rejection lacked identity diagnosis: {swapped.stderr}")

    x_output = x_dir / "output.json"
    original = x_output.read_bytes()
    x_output.write_bytes(original + b"\n")
    tampered = invoke(
        [
            *audit_base,
            "--x-manifest", str(x_dir / "manifest.json"),
            "--y-manifest", str(y_dir / "manifest.json"),
        ]
    )
    write_result(args.work_dir, "tampered_output_rejection", tampered)
    x_output.write_bytes(original)
    if tampered.returncode == 0:
        raise AssertionError("tampered output was unexpectedly accepted")
    if "output SHA256/provenance mismatch" not in tampered.stderr:
        raise AssertionError(f"tamper rejection lacked hash diagnosis: {tampered.stderr}")

    restored = checked(
        [
            *audit_base,
            "--x-manifest", str(x_dir / "manifest.json"),
            "--y-manifest", str(y_dir / "manifest.json"),
        ]
    )
    write_result(args.work_dir, "restored_positive_audit", restored)
    print("DIRECT_PROVENANCE_TESTS_PASS")
    print(f"swapped_rc={swapped.returncode} swapped_error={swapped.stderr.strip()}")
    print(f"tampered_rc={tampered.returncode} tampered_error={tampered.stderr.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
