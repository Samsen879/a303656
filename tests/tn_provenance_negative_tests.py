#!/usr/bin/env python3
"""Mandatory expected-rejection tests for T(n) pilot provenance."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def invoke(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def preserve(work: Path, name: str, result: subprocess.CompletedProcess[str]) -> None:
    (work / f"{name}.stdout.log").write_text(result.stdout, encoding="utf-8")
    (work / f"{name}.stderr.log").write_text(result.stderr, encoding="utf-8")
    (work / f"{name}.return_code.txt").write_text(f"{result.returncode}\n", encoding="utf-8")


def require_rejection(work: Path, name: str, command: list[str], fragment: str) -> None:
    result = invoke(command)
    preserve(work, name, result)
    if result.returncode == 0:
        raise AssertionError(f"{name} unexpectedly accepted")
    if fragment not in result.stderr:
        raise AssertionError(f"{name} lacked diagnostic {fragment!r}: {result.stderr}")


def audit_command(args: argparse.Namespace, bitset: Path, clean: Path, oracle: Path) -> list[str]:
    return [
        args.python,
        str(args.verifier),
        "--audit-only",
        "--bitset-dir", str(bitset),
        "--clean-dir", str(clean),
        "--oracle-dir", str(oracle),
        "--low", str(args.low),
        "--high", str(args.high),
        "--interval-id", args.interval_id,
    ]


def copy_trio(args: argparse.Namespace, name: str) -> tuple[Path, Path, Path]:
    root = args.work_dir / name
    shutil.copytree(args.bitset_dir, root / "bitset")
    shutil.copytree(args.clean_dir, root / "clean")
    shutil.copytree(args.oracle_dir, root / "oracle")
    for directory in (root / "bitset", root / "clean", root / "oracle"):
        path = directory / "provenance.json"
        provenance = json.loads(path.read_text())
        position = provenance["exact_backend_cli"].index("--out-dir") + 1
        provenance["exact_backend_cli"][position] = str(directory.resolve())
        path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    return root / "bitset", root / "clean", root / "oracle"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--bitset-dir", type=Path, required=True)
    parser.add_argument("--clean-dir", type=Path, required=True)
    parser.add_argument("--oracle-dir", type=Path, required=True)
    parser.add_argument("--clean-binary", type=Path, required=True)
    parser.add_argument("--source-tree", type=Path, required=True)
    parser.add_argument("--low", type=int, required=True)
    parser.add_argument("--high", type=int, required=True)
    parser.add_argument("--interval-id", required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    args.work_dir.mkdir(parents=True, exist_ok=False)

    wrong_commit = [
        args.python,
        str(args.runner),
        "--source-commit", "deadbeef",
        "--binary", str(args.clean_binary),
        "--source-tree", str(args.source_tree),
        "--low", "2", "--high", "3",
        "--interval-id", "FIXTURE-WRONG-COMMIT",
        "--out-dir", str(args.work_dir / "wrong-commit-output"),
        "--timeout-seconds", "10",
    ]
    require_rejection(args.work_dir, "wrong_commit_cli", wrong_commit, "unrecognized arguments: --source-commit")

    require_rejection(
        args.work_dir,
        "swapped_slots",
        audit_command(args, args.clean_dir, args.bitset_dir, args.oracle_dir),
        "implementation manifest relabel/slot mismatch",
    )

    bitset, clean, oracle = copy_trio(args, "relabel")
    provenance_path = bitset / "provenance.json"
    provenance = json.loads(provenance_path.read_text())
    provenance["implementation_id"] = "tn_clean_annulus_v1"
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    require_rejection(
        args.work_dir,
        "manifest_relabel",
        audit_command(args, bitset, clean, oracle),
        "implementation manifest relabel/slot mismatch",
    )

    bitset, clean, oracle = copy_trio(args, "tamper")
    with (bitset / "counts.csv").open("a", encoding="utf-8") as stream:
        stream.write("999999999999,0\n")
    require_rejection(
        args.work_dir,
        "output_tamper",
        audit_command(args, bitset, clean, oracle),
        "output tamper/hash mismatch: counts.csv",
    )

    bitset, clean, oracle = copy_trio(args, "binary-replacement")
    provenance_path = bitset / "provenance.json"
    provenance = json.loads(provenance_path.read_text())
    replacement = args.work_dir / "binary-replacement" / "bitset-binary"
    shutil.copy2(provenance["executable"]["path"], replacement)
    provenance["executable"]["path"] = str(replacement)
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    shutil.copy2(args.clean_binary, replacement)
    require_rejection(
        args.work_dir,
        "binary_replacement",
        audit_command(args, bitset, clean, oracle),
        "executable SHA256/binary replacement mismatch",
    )

    print("TN_PROVENANCE_NEGATIVE_TESTS_PASS")
    print("expected_rejections=wrong_commit,swapped_slots,manifest_relabel,output_tamper,binary_replacement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
