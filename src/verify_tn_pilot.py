#!/usr/bin/env python3
"""Independent row, summary, witness, and provenance checks for a T(n) trio."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


EXPECTED = {
    "bitset": "tn_bitset_annulus_v1",
    "clean": "tn_clean_annulus_v1",
    "oracle": "tn_gmp_uv_oracle_v1",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"object required: {path}")
    return value


def write_object(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def identity(binary: Path) -> str:
    return subprocess.run(
        [str(binary), "--implementation-id"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()


def audit_provenance(
    directory: Path,
    expected_id: str,
    low: int,
    high: int,
    interval_id: str,
    require_report: bool,
) -> dict:
    provenance = load_object(directory / "provenance.json")
    if provenance.get("schema") != "a303656-tn-pilot-provenance-v1":
        raise ValueError(f"{expected_id} provenance schema mismatch")
    if provenance.get("implementation_id") != expected_id:
        raise ValueError(f"{expected_id} implementation manifest relabel/slot mismatch")
    executable = Path(provenance["executable"]["path"])
    if not executable.is_file() or sha256(executable) != provenance["executable"].get("sha256"):
        raise ValueError(f"{expected_id} executable SHA256/binary replacement mismatch")
    if identity(executable) != expected_id:
        raise ValueError(f"{expected_id} binary-reported identity mismatch")
    source_tree = Path(provenance["source_tree"])
    actual_commit = subprocess.run(
        ["git", "-C", str(source_tree), "rev-parse", "HEAD"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()
    if actual_commit != provenance.get("source_commit"):
        raise ValueError(f"{expected_id} automatically derived source commit mismatch")
    dirty = bool(
        subprocess.run(
            ["git", "-C", str(source_tree), "status", "--porcelain"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
    )
    if dirty != bool(provenance.get("source_tree_dirty")):
        raise ValueError(f"{expected_id} source dirty-state mismatch")
    if provenance.get("formal_acceptance_eligible") and dirty:
        raise ValueError(f"{expected_id} dirty run incorrectly marked acceptance eligible")
    for relative, expected_hash in provenance.get("source_files", {}).items():
        source = source_tree / relative
        if not source.is_file() or sha256(source) != expected_hash:
            raise ValueError(f"{expected_id} source hash mismatch: {relative}")
    interval = provenance.get("interval", {})
    if (
        interval.get("id") != interval_id
        or (int(interval.get("low", -1)), int(interval.get("high_exclusive", -1))) != (low, high)
        or int(interval.get("number_of_n", -1)) != high - low
    ):
        raise ValueError(f"{expected_id} provenance interval mismatch")
    if interval_id in ("PILOT-A", "PILOT-B") and provenance.get("formal_acceptance_eligible") is not True:
        raise ValueError(f"{expected_id} formal run is not acceptance eligible")
    runner_cli = provenance.get("exact_runner_cli")
    backend_cli = provenance.get("exact_backend_cli")
    if not isinstance(runner_cli, list) or "--source-commit" in runner_cli or "--implementation-id" in runner_cli:
        raise ValueError(f"{expected_id} caller-declared identity/commit found in runner CLI")
    expected_backend_cli = [
        str(executable),
        "--low", str(low),
        "--high", str(high),
        "--interval-id", interval_id,
        "--out-dir", str(directory),
    ]
    metadata = load_object(directory / "metadata.json")
    if metadata.get("emit_all_records_fixture_mode") is True:
        expected_backend_cli.append("--emit-all-records")
    if backend_cli != expected_backend_cli:
        raise ValueError(f"{expected_id} exact backend CLI mismatch")
    for filename, expected_hash in provenance.get("outputs_sha256", {}).items():
        artifact = directory / filename
        if not artifact.is_file() or sha256(artifact) != expected_hash:
            raise ValueError(f"{expected_id} output tamper/hash mismatch: {filename}")
    if require_report:
        if "verifier_report.json" not in provenance.get("outputs_sha256", {}):
            raise ValueError(f"{expected_id} verifier report provenance missing")
        verifier = provenance.get("verifier")
        expected_verifier = (source_tree / "src/verify_tn_pilot.py").resolve()
        if not isinstance(verifier, dict) or Path(verifier.get("path", "")).resolve() != expected_verifier:
            raise ValueError(f"{expected_id} verifier source provenance mismatch")
        if not expected_verifier.is_file() or sha256(expected_verifier) != verifier.get("sha256"):
            raise ValueError(f"{expected_id} verifier source SHA256 mismatch")
        if provenance.get("verifier_report_status") != "PASS":
            raise ValueError(f"{expected_id} verifier report status mismatch")
    return provenance


def read_counts(path: Path, low: int, high: int) -> list[int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "n,T":
        raise ValueError(f"counts header mismatch: {path}")
    if len(lines) != high - low + 1:
        raise ValueError(f"counts row completeness mismatch: {path}")
    result: list[int] = []
    for index, line in enumerate(lines[1:]):
        fields = line.split(",")
        if len(fields) != 2:
            raise ValueError(f"counts row shape mismatch: {path}:{index + 2}")
        n, count = map(int, fields)
        if n != low + index or count < 0:
            raise ValueError(f"counts row missing/duplicate/out-of-range: {path}:{index + 2}")
        result.append(count)
    return result


def source_pairs(high: int) -> list[tuple[int, int, int]]:
    threes: list[int] = []
    value = 1
    while value < high:
        threes.append(value)
        value *= 3
    fives: list[int] = []
    value = 1
    while value < high:
        fives.append(value)
        value *= 5
    return [
        (c, d, p3 + p5)
        for c, p3 in enumerate(threes)
        for d, p5 in enumerate(fives)
        if p3 + p5 < high
    ]


def canonical_pair(remainder: int) -> tuple[int, int] | None:
    for a in range(math.isqrt(remainder // 2) + 1):
        b2 = remainder - a * a
        b = math.isqrt(b2)
        if a <= b and b * b == b2:
            return a, b
    return None


def expected_summary(counts: list[int], low: int, high: int, pairs: list[tuple[int, int, int]]) -> dict:
    minimum = min(counts)
    argmin = [low + index for index, value in enumerate(counts) if value == minimum]
    histogram = Counter(counts)
    for value in range(4):
        histogram.setdefault(value, 0)
    active = [sum(shift <= n for _, _, shift in pairs) for n in range(low, high)]
    return {
        "minimum_T": minimum,
        "argmin_count": len(argmin),
        "first_argmin_n": str(argmin[0]),
        "last_argmin_n": str(argmin[-1]),
        "count_T0": histogram[0],
        "count_T1": histogram[1],
        "count_T2": histogram[2],
        "count_T3": histogram[3],
        "exact_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "active_pair_range": {"minimum": min(active), "maximum": max(active)},
    }


def verify_directory(
    directory: Path,
    expected_id: str,
    low: int,
    high: int,
    counts: list[int],
    pairs: list[tuple[int, int, int]],
    canonical_cache: dict[int, tuple[int, int] | None],
) -> tuple[dict, list[dict]]:
    metadata = load_object(directory / "metadata.json")
    summary = load_object(directory / "summary.json")
    if metadata.get("implementation_id") != expected_id or summary.get("implementation_id") != expected_id:
        raise ValueError(f"{expected_id} metadata/summary identity mismatch")
    if metadata.get("obstruction_data_status") != "NOT_COLLECTED_IN_TN_PILOT":
        raise ValueError(f"{expected_id} obstruction status mismatch")
    if metadata.get("early_termination") is not False or metadata.get("all_active_pairs_processed") is not True:
        raise ValueError(f"{expected_id} early-termination declaration mismatch")
    reconstructed = expected_summary(counts, low, high, pairs)
    interval = summary.get("interval", {})
    if (
        interval.get("id") != metadata.get("interval", {}).get("id")
        or int(interval.get("low", -1)) != low
        or int(interval.get("high_exclusive", -1)) != high
        or int(interval.get("number_of_n", -1)) != high - low
    ):
        raise ValueError(f"{expected_id} summary interval mismatch")
    for key, value in reconstructed.items():
        if summary.get(key) != value:
            raise ValueError(f"{expected_id} summary reconstruction mismatch: {key}")
    if summary.get("counts_csv_sha256") != sha256(directory / "counts.csv"):
        raise ValueError(f"{expected_id} summary counts hash mismatch")
    if summary.get("low_t_jsonl_sha256") != sha256(directory / "low_t.jsonl"):
        raise ValueError(f"{expected_id} summary low-T hash mismatch")

    records = [json.loads(line) for line in (directory / "low_t.jsonl").read_text().splitlines() if line]
    selected = (
        set(range(low, high))
        if metadata.get("emit_all_records_fixture_mode") is True
        else {
            low + index
            for index, count in enumerate(counts)
            if count <= 3 or count == reconstructed["minimum_T"]
        }
    )
    record_ns = [int(record["n"]) for record in records]
    if len(record_ns) != len(set(record_ns)) or set(record_ns) != selected:
        raise ValueError(f"{expected_id} low-T row selection/completeness mismatch")
    if int(summary.get("low_t_record_count", -1)) != len(records):
        raise ValueError(f"{expected_id} low-T summary count mismatch")
    pair_map = {(c, d): shift for c, d, shift in pairs}
    for record in records:
        n = int(record["n"])
        count = int(record["T"])
        if count != counts[n - low]:
            raise ValueError(f"{expected_id} low-T count mismatch at n={n}")
        expected_active = sum(shift <= n for shift in pair_map.values())
        if int(record["active_exponent_pair_count"]) != expected_active:
            raise ValueError(f"{expected_id} active-pair count mismatch at n={n}")
        winners = record["winning_exponent_pairs"]
        if len(winners) != count:
            raise ValueError(f"{expected_id} winning source-pair list length mismatch at n={n}")
        keys: set[tuple[int, int]] = set()
        for winner in winners:
            key = (int(winner["c"]), int(winner["d"]))
            if key in keys or key not in pair_map:
                raise ValueError(f"{expected_id} duplicate/invalid source pair at n={n}")
            keys.add(key)
            shift = int(winner["shift"])
            remainder = int(winner["remainder"])
            a = int(winner["a"])
            b = int(winner["b"])
            if shift != pair_map[key] or shift > n or remainder != n - shift:
                raise ValueError(f"{expected_id} shift/remainder mismatch at n={n}")
            if not (0 <= a <= b) or a * a + b * b + 3 ** key[0] + 5 ** key[1] != n:
                raise ValueError(f"{expected_id} witness equation mismatch at n={n}")
            if remainder not in canonical_cache:
                canonical_cache[remainder] = canonical_pair(remainder)
            if canonical_cache[remainder] != (a, b):
                raise ValueError(f"{expected_id} noncanonical witness at n={n}, pair={key}")
            equation = winner.get("witness_equation", {})
            if (
                equation.get("verified") is not True
                or int(equation.get("a_squared", -1)) != a * a
                or int(equation.get("b_squared", -1)) != b * b
                or int(equation.get("three_power", -1)) != 3 ** key[0]
                or int(equation.get("five_power", -1)) != 5 ** key[1]
                or int(equation.get("lhs", -1)) != n
            ):
                raise ValueError(f"{expected_id} equation verification fields mismatch at n={n}")
    return reconstructed, records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bitset-dir", type=Path, required=True)
    parser.add_argument("--clean-dir", type=Path, required=True)
    parser.add_argument("--oracle-dir", type=Path, required=True)
    parser.add_argument("--low", type=int, required=True)
    parser.add_argument("--high", type=int, required=True)
    parser.add_argument("--interval-id", required=True)
    parser.add_argument("--audit-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    verifier_path = Path(__file__).resolve(strict=True)
    directories = {
        "bitset": args.bitset_dir.resolve(),
        "clean": args.clean_dir.resolve(),
        "oracle": args.oracle_dir.resolve(),
    }
    require_report = args.audit_only
    for role, directory in directories.items():
        audit_provenance(
            directory, EXPECTED[role], args.low, args.high, args.interval_id, require_report
        )
    if args.audit_only:
        print("TN_PROVENANCE_AUDIT_PASS")
        return 0

    raw_counts = {role: (directory / "counts.csv").read_bytes() for role, directory in directories.items()}
    if len(set(raw_counts.values())) != 1:
        raise ValueError("three-way per-n counts.csv byte mismatch")
    counts = read_counts(directories["bitset"] / "counts.csv", args.low, args.high)
    for role in ("clean", "oracle"):
        if read_counts(directories[role] / "counts.csv", args.low, args.high) != counts:
            raise ValueError(f"{role} per-n T array mismatch")
    pairs = source_pairs(args.high)
    canonical_cache: dict[int, tuple[int, int] | None] = {}
    summaries: dict[str, dict] = {}
    normalized_records: dict[str, list[dict]] = {}
    for role, directory in directories.items():
        summary, records = verify_directory(
            directory, EXPECTED[role], args.low, args.high, counts, pairs, canonical_cache
        )
        summaries[role] = summary
        normalized = []
        for record in records:
            record = dict(record)
            record.pop("implementation_id", None)
            normalized.append(record)
        normalized_records[role] = normalized
    if not (summaries["bitset"] == summaries["clean"] == summaries["oracle"]):
        raise ValueError("three-way reconstructed summary mismatch")
    if not (normalized_records["bitset"] == normalized_records["clean"] == normalized_records["oracle"]):
        raise ValueError("three-way low-T record mismatch")

    summary = summaries["bitset"]
    status = "PASS"
    bounded_candidate_status = (
        "CERTIFIED BOUNDED CANDIDATE PENDING SEPARATE THEOREM VERIFICATION"
        if summary["minimum_T"] == 0
        else "NO T(n)=0 IN THIS BOUNDED PILOT INTERVAL"
    )
    report_base = {
        "schema": "a303656-tn-three-way-verifier-report-v1",
        "status": status,
        "classification": "EXACT THREE-WAY BOUNDED PILOT VERIFICATION; NOT A GLOBAL PROOF",
        "interval": {
            "id": args.interval_id,
            "low": str(args.low),
            "high_exclusive": str(args.high),
            "number_of_n": args.high - args.low,
        },
        "per_n_counts_equal": True,
        "counts_csv_sha256": sha256(directories["bitset"] / "counts.csv"),
        "all_low_t_witnesses_verified": True,
        "summary_reconstructed": True,
        "row_completeness_verified": True,
        "minimum_T": summary["minimum_T"],
        "bounded_candidate_status": bounded_candidate_status,
        "verifier_source_sha256": sha256(verifier_path),
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    for role, directory in directories.items():
        report = dict(report_base)
        report["implementation_id"] = EXPECTED[role]
        write_object(directory / "verifier_report.json", report)
        provenance = load_object(directory / "provenance.json")
        expected_verifier = (Path(provenance["source_tree"]) / "src/verify_tn_pilot.py").resolve()
        if verifier_path != expected_verifier:
            raise ValueError(
                f"{EXPECTED[role]} verifier must come from the recorded source tree: {expected_verifier}"
            )
        provenance["outputs_sha256"]["verifier_report.json"] = sha256(directory / "verifier_report.json")
        provenance["verifier"] = {
            "path": str(verifier_path),
            "sha256": sha256(verifier_path),
            "exact_cli": sys.argv,
        }
        provenance["verifier_report_status"] = "PASS"
        write_object(directory / "provenance.json", provenance)

    print("TN_THREE_WAY_VERIFICATION_PASS")
    print(f"interval_id={args.interval_id} rows={len(counts)} minimum_T={summary['minimum_T']}")
    print(f"counts_csv_sha256={report_base['counts_csv_sha256']}")
    print(f"bounded_candidate_status={bounded_candidate_status}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"TN_VERIFY_ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
