#!/usr/bin/env python3
"""Expected-rejection tests for the bounded K4 AP pilot.

The artifact tests operate only on copies of an already validated result set.
The executable tests use malformed or uint64-overflow parser fixtures, so they
cannot cause any backend to evaluate T(n) for an off-panel integer.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable


CSV_FIELDS = ["h", "k", "n", "T", "active_pairs"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--results-commit", required=True)
    parser.add_argument("--backend-a", type=Path, required=True)
    parser.add_argument("--backend-b", type=Path, required=True)
    parser.add_argument("--direct-oracle", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    return parser.parse_args()


def verifier_command(
    args: argparse.Namespace,
    artifact_dir: Path,
    *,
    backend_a: Path | None = None,
    backend_b: Path | None = None,
    direct_oracle: Path | None = None,
) -> list[str]:
    return [
        args.python,
        str(args.verifier.resolve()),
        "--artifact-dir",
        str(artifact_dir.resolve()),
        "--source-root",
        str(args.source_root.resolve()),
        "--source-commit",
        args.source_commit,
        "--results-commit",
        args.results_commit,
        "--backend-a",
        str((backend_a or args.backend_a).resolve()),
        "--backend-b",
        str((backend_b or args.backend_b).resolve()),
        "--direct-oracle",
        str((direct_oracle or args.direct_oracle).resolve()),
    ]


def invoke(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )


def preserve(work_dir: Path, name: str, result: subprocess.CompletedProcess[str]) -> None:
    (work_dir / f"{name}.stdout.log").write_text(result.stdout, encoding="utf-8")
    (work_dir / f"{name}.stderr.log").write_text(result.stderr, encoding="utf-8")
    (work_dir / f"{name}.return_code.txt").write_text(
        f"{result.returncode}\n", encoding="utf-8"
    )


def require_acceptance(
    work_dir: Path, name: str, command: list[str]
) -> subprocess.CompletedProcess[str]:
    result = invoke(command)
    preserve(work_dir, name, result)
    if result.returncode != 0:
        raise AssertionError(
            f"{name} rejected the unmodified valid artifacts with rc={result.returncode}: "
            f"{result.stderr}"
        )
    return result


def require_rejection(
    work_dir: Path, name: str, command: list[str]
) -> subprocess.CompletedProcess[str]:
    result = invoke(command)
    preserve(work_dir, name, result)
    if result.returncode == 0:
        raise AssertionError(f"{name} unexpectedly returned zero")
    return result


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object in {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_counts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != CSV_FIELDS:
            raise AssertionError(f"unexpected counts schema in valid fixture: {path}")
        return list(reader)


def write_counts(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mutate_counts(
    directory: Path, mutation: Callable[[list[dict[str, str]]], None]
) -> None:
    path = directory / "backend_a_counts.csv"
    rows = read_counts(path)
    mutation(rows)
    write_counts(path, rows)


def duplicate_n(rows: list[dict[str, str]]) -> None:
    rows.append(dict(rows[0]))


def omit_point(rows: list[dict[str, str]]) -> None:
    rows.pop()


def alter_h(rows: list[dict[str, str]]) -> None:
    rows[0]["h"] = "-719"


def alter_k(rows: list[dict[str, str]]) -> None:
    rows[0]["k"] = "-127"


def outside_cell(rows: list[dict[str, str]]) -> None:
    rows[0]["n"] = "183968950233"


def incorrect_active_count(rows: list[dict[str, str]]) -> None:
    rows[0]["active_pairs"] = "406"


def tamper_t(rows: list[dict[str, str]]) -> None:
    value = int(rows[0]["T"])
    rows[0]["T"] = str(value + 1 if value < 407 else value - 1)


def alter_p4(directory: Path) -> None:
    path = directory / "metadata.json"
    value = load_json(path)
    value["core"]["p4"][3] = 19
    write_json(path, value)


def alter_m4(directory: Path) -> None:
    path = directory / "metadata.json"
    value = load_json(path)
    value["core"]["m4"] = int(value["core"]["m4"]) + 1
    write_json(path, value)


def relabel_target_control(directory: Path) -> None:
    path = directory / "class_summaries.json"
    value = load_json(path)
    value["classes"]["0"]["role"] = "CONTROL"
    value["classes"]["-720"]["role"] = "TARGET"
    write_json(path, value)


def mismatch_source_commit(directory: Path) -> None:
    path = directory / "metadata.json"
    value = load_json(path)
    value["source_commit"] = "0" * 40
    write_json(path, value)


def copied_fixture(args: argparse.Namespace, name: str) -> Path:
    destination = args.work_dir / "fixtures" / name
    shutil.copytree(args.artifact_dir.resolve(), destination)
    return destination


def parser_fixture_command(
    executable: Path,
    fixture: Path,
    output: Path,
) -> list[str]:
    return [str(executable.resolve()), "--input", str(fixture), "--output", str(output)]


def parser_rejection(
    args: argparse.Namespace,
    return_codes: dict[str, int],
    name: str,
    executable: Path,
    header: str,
    row: str,
) -> None:
    fixture = args.work_dir / "parser_fixtures" / f"{name}.csv"
    output = args.work_dir / "parser_fixtures" / f"{name}.out"
    fixture.write_text(f"{header}\n{row}\n", encoding="ascii")
    result = require_rejection(
        args.work_dir, name, parser_fixture_command(executable, fixture, output)
    )
    if output.exists():
        raise AssertionError(
            f"{name} created an output despite malformed/overflow input; "
            "the fixture must be rejected before counting"
        )
    return_codes[name] = result.returncode


def main() -> int:
    args = parse_args()
    if args.work_dir.exists():
        raise AssertionError(f"work directory already exists: {args.work_dir}")
    args.work_dir.mkdir(parents=True)
    (args.work_dir / "fixtures").mkdir()
    (args.work_dir / "parser_fixtures").mkdir()

    return_codes: dict[str, int] = {}
    baseline = require_acceptance(
        args.work_dir,
        "valid_baseline",
        verifier_command(args, args.artifact_dir),
    )
    return_codes["valid_baseline"] = baseline.returncode

    count_mutations: tuple[
        tuple[str, Callable[[list[dict[str, str]]], None]], ...
    ] = (
        ("duplicated_n", duplicate_n),
        ("omitted_point", omit_point),
        ("altered_h", alter_h),
        ("altered_k", alter_k),
        ("point_outside_activation_cell", outside_cell),
        ("incorrect_active_pair_count", incorrect_active_count),
        ("tampered_T_row", tamper_t),
    )
    for name, mutation in count_mutations:
        fixture = copied_fixture(args, name)
        mutate_counts(fixture, mutation)
        result = require_rejection(
            args.work_dir, name, verifier_command(args, fixture)
        )
        return_codes[name] = result.returncode

    json_mutations: tuple[tuple[str, Callable[[Path], None]], ...] = (
        ("altered_P4_prime_list", alter_p4),
        ("altered_M4", alter_m4),
        ("target_control_relabel", relabel_target_control),
        ("source_commit_mismatch", mismatch_source_commit),
    )
    for name, mutation in json_mutations:
        fixture = copied_fixture(args, name)
        mutation(fixture)
        result = require_rejection(
            args.work_dir, name, verifier_command(args, fixture)
        )
        return_codes[name] = result.returncode

    result = require_rejection(
        args.work_dir,
        "swapped_backend_identity",
        verifier_command(
            args,
            args.artifact_dir,
            backend_a=args.backend_b,
            backend_b=args.backend_a,
        ),
    )
    return_codes["swapped_backend_identity"] = result.returncode

    replacement = args.work_dir / "binary_replacement_backend_a"
    shutil.copy2(args.backend_a, replacement)
    replacement.write_bytes(replacement.read_bytes() + b"\nK4_NEGATIVE_REPLACEMENT\n")
    replacement.chmod(args.backend_a.stat().st_mode)
    result = require_rejection(
        args.work_dir,
        "binary_replacement",
        verifier_command(args, args.artifact_dir, backend_a=replacement),
    )
    return_codes["binary_replacement"] = result.returncode

    counts_header = "h,k,n,active_pairs"
    direct_header = "h,k,n,active_pairs,expected_T"
    overflow = "18446744073709551616"
    parser_rejection(
        args,
        return_codes,
        "backend_a_malformed_integer",
        args.backend_a,
        counts_header,
        "0,0,12x,407",
    )
    parser_rejection(
        args,
        return_codes,
        "backend_a_uint64_overflow",
        args.backend_a,
        counts_header,
        f"0,0,{overflow},407",
    )
    parser_rejection(
        args,
        return_codes,
        "backend_b_malformed_integer",
        args.backend_b,
        counts_header,
        "0,0,12x,407",
    )
    parser_rejection(
        args,
        return_codes,
        "backend_b_uint64_overflow",
        args.backend_b,
        counts_header,
        f"0,0,{overflow},407",
    )
    parser_rejection(
        args,
        return_codes,
        "direct_oracle_malformed_integer",
        args.direct_oracle,
        direct_header,
        "0,0,12x,407,0",
    )
    parser_rejection(
        args,
        return_codes,
        "direct_oracle_uint64_overflow",
        args.direct_oracle,
        direct_header,
        f"0,0,{overflow},407,0",
    )

    rejected = {name: rc for name, rc in return_codes.items() if name != "valid_baseline"}
    if len(rejected) != 19 or any(rc == 0 for rc in rejected.values()):
        raise AssertionError("negative-test cardinality/nonzero-return invariant failed")
    summary = {
        "schema": "a303656-k4-ap-negative-tests-v1",
        "status": "PASS",
        "valid_baseline_return_code": return_codes["valid_baseline"],
        "expected_nonzero_return_codes": rejected,
        "formal_non_panel_T_evaluations": 0,
        "parser_fixtures_rejected_before_output": True,
    }
    write_json(args.work_dir / "summary.json", summary)
    print("K4_AP_PILOT_NEGATIVE_TESTS_PASS")
    print(f"expected_rejections={len(rejected)}")
    print(json.dumps(return_codes, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
