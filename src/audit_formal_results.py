#!/usr/bin/env python3
"""Independent audit of every finite result claimed in the final report.

This script does not rerun the expensive searches.  It reopens the raw chunk
outputs, recomputes exact exponent-domain counts with Python integers, checks
all interval and candidate accounting, verifies the stored chunk SHA256 values,
and compares the mathematical output of the independent implementations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"JSON object required: {path}")
    return value


def resolve(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def exact_domain(high: int, C: int, D: int) -> dict[str, int]:
    rhs3 = pow(3, C + 1) + 1
    rhs5 = pow(5, D + 1) + 1
    if not high < rhs3:
        raise AssertionError(f"false C-domain inequality: {high} !< {rhs3}")
    if not high < rhs5:
        raise AssertionError(f"false D-domain inequality: {high} !< {rhs5}")
    powers3 = [pow(3, c) for c in range(C + 1)]
    powers5 = [pow(5, d) for d in range(D + 1)]
    pairs = [(c, d, x + y) for c, x in enumerate(powers3)
             for d, y in enumerate(powers5) if x + y <= high]
    shifts = {s for _, _, s in pairs}
    return {
        "rhs3": rhs3,
        "rhs5": rhs5,
        "pairs": len(pairs),
        "shifts": len(shifts),
        "duplicates": len(pairs) - len(shifts),
    }


def candidate_file(path: Path) -> Path:
    for suffix in (".candidates.txt", ".candidates"):
        candidate = path.with_suffix(suffix)
        if candidate.is_file():
            return candidate
    raise AssertionError(f"missing candidate sidecar for {path}")


DIRECT_KEYS = (
    "low", "high", "C", "D", "three_power_next_plus_one",
    "five_power_next_plus_one", "strict_domain_inequalities_checked",
    "admissible_rectangle_pair_count_at_high", "distinct_shift_count_at_high",
    "duplicate_pair_count", "integers_tested",
    "shifts_processed_before_termination", "unordered_square_pairs_enumerated",
    "candidate_count", "candidates",
)


def read_direct_rows(directory: Path) -> list[tuple[int, int, Path, dict]]:
    rows: list[tuple[int, int, Path, dict]] = []
    for path in directory.glob("*.json"):
        data = load(path)
        if "method" not in data or "low" not in data or "high" not in data:
            continue
        rows.append((int(data["low"]), int(data["high"]), path, data))
    rows.sort(key=lambda row: (row[0], row[1], row[2].name))
    return rows


def check_direct_pair(x_path: Path, y_path: Path, low: int, high: int) -> dict[str, object]:
    x, y = load(x_path), load(y_path)
    differences = [key for key in DIRECT_KEYS if x.get(key) != y.get(key)]
    if differences:
        raise AssertionError(f"direct implementation mismatch {x_path}: {differences}")
    if (int(x["low"]), int(x["high"])) != (low, high):
        raise AssertionError(f"direct interval mismatch: {x_path}")
    if int(x["integers_tested"]) != high - low + 1:
        raise AssertionError(f"direct tested count mismatch: {x_path}")
    if not x["strict_domain_inequalities_checked"]:
        raise AssertionError(f"direct strict-domain flag false: {x_path}")
    domain = exact_domain(high, int(x["C"]), int(x["D"]))
    expected = {
        "three_power_next_plus_one": str(domain["rhs3"]),
        "five_power_next_plus_one": str(domain["rhs5"]),
        "admissible_rectangle_pair_count_at_high": domain["pairs"],
        "distinct_shift_count_at_high": domain["shifts"],
        "duplicate_pair_count": domain["duplicates"],
    }
    for key, value in expected.items():
        if x.get(key) != value:
            raise AssertionError(f"direct exact-domain mismatch in {key}: {x_path}")
    if int(x["candidate_count"]) != len(x["candidates"]):
        raise AssertionError(f"direct candidate count mismatch: {x_path}")
    if x["candidates"] or int(x["candidate_count"]) != 0:
        raise AssertionError(f"direct result is not empty: {x_path}")
    for path, data in ((x_path, x), (y_path, y)):
        sidecar = candidate_file(path)
        if sidecar.read_text(encoding="utf-8").split() != [str(v) for v in data["candidates"]]:
            raise AssertionError(f"direct candidate sidecar mismatch: {sidecar}")
    return {
        "low": str(low),
        "high": str(high),
        "C": int(x["C"]),
        "D": int(x["D"]),
        "integers": high - low + 1,
        "pairs": domain["pairs"],
        "distinct_shifts": domain["shifts"],
        "duplicate_pairs": domain["duplicates"],
        "shifts_processed": int(x["shifts_processed_before_termination"]),
        "unordered_square_pairs": int(x["unordered_square_pairs_enumerated"]),
        "x_sha256": sha256(x_path),
        "y_sha256": sha256(y_path),
    }


def check_gapless_intervals(intervals: list[tuple[int, int]], low: int, high: int) -> None:
    if not intervals or intervals[0][0] != low or intervals[-1][1] != high:
        raise AssertionError("gapless endpoints mismatch")
    if any(a_high + 1 != b_low for (_, a_high), (b_low, _) in zip(intervals, intervals[1:])):
        raise AssertionError("gap or overlap in purported continuous interval")


def audit_direct_gapless(label: str, x_dir: Path, y_dir: Path,
                         low: int, high: int, expected_chunks: int,
                         aggregate: Path | None = None) -> dict[str, object]:
    xrows, yrows = read_direct_rows(x_dir), read_direct_rows(y_dir)
    if len(xrows) != expected_chunks or len(yrows) != expected_chunks:
        raise AssertionError(f"{label}: unexpected chunk count")
    xi = [(a, b) for a, b, _, _ in xrows]
    yi = [(a, b) for a, b, _, _ in yrows]
    if xi != yi:
        raise AssertionError(f"{label}: x/y interval manifests differ")
    check_gapless_intervals(xi, low, high)
    chunks = [check_direct_pair(xp, yp, lo, hi)
              for (lo, hi, xp, _), (_, _, yp, _) in zip(xrows, yrows)]
    tested = sum(int(row["integers"]) for row in chunks)
    lattice = sum(int(row["unordered_square_pairs"]) for row in chunks)
    if tested != high - low + 1:
        raise AssertionError(f"{label}: aggregate tested count mismatch")
    if aggregate:
        data = load(aggregate)
        required = {
            "low": str(low), "high": str(high),
            "chunk_count_x": expected_chunks, "chunk_count_y": expected_chunks,
            "integers_tested_x": tested, "integers_tested_y": tested,
            "candidate_count_x": 0, "candidate_count_y": 0,
            "candidates_x": [], "candidates_y": [],
            "unordered_square_pairs_enumerated_x": lattice,
            "unordered_square_pairs_enumerated_y": lattice,
            "complete_gapless_independent_crosscheck": True,
            "mismatches": [],
        }
        for key, value in required.items():
            if data.get(key) != value:
                raise AssertionError(f"{label}: aggregate mismatch in {key}")
        manifest_rows = data.get("chunks", [])
        if len(manifest_rows) != expected_chunks:
            raise AssertionError(f"{label}: aggregate chunk manifest length")
        for index, (manifest, chunk, xrow, yrow) in enumerate(zip(manifest_rows, chunks, xrows, yrows)):
            x_path, y_path = xrow[2], yrow[2]
            manifest_required = {
                "index": index,
                "low": chunk["low"],
                "high": chunk["high"],
                "mismatches": [],
                "candidate_count": 0,
                "unordered_square_pairs_enumerated": chunk["unordered_square_pairs"],
                "x_json": str(x_path.relative_to(ROOT)),
                "x_sha256": chunk["x_sha256"],
                "y_json": str(y_path.relative_to(ROOT)),
                "y_sha256": chunk["y_sha256"],
            }
            for key, value in manifest_required.items():
                if manifest.get(key) != value:
                    raise AssertionError(f"{label}: aggregate chunk {index} mismatch in {key}")
    return {
        "label": label,
        "low": str(low), "high": str(high),
        "integers": tested, "chunk_count": expected_chunks,
        "candidate_count": 0,
        "matched_unordered_square_pairs": lattice,
        "aggregate": str(aggregate.relative_to(ROOT)) if aggregate else None,
        "aggregate_sha256": sha256(aggregate) if aggregate else None,
        "chunks": chunks,
    }


def audit_direct_named_windows(label: str, names: Iterable[str], x_dir: Path, y_dir: Path,
                               summary: Path | None = None) -> dict[str, object]:
    windows = []
    for name in names:
        xp, yp = x_dir / f"{name}.json", y_dir / f"{name}.json"
        x = load(xp)
        windows.append(check_direct_pair(xp, yp, int(x["low"]), int(x["high"])))
    if summary:
        data = load(summary)
        if label == "logarithmic_windows":
            if int(data.get("total_integers_tested_per_implementation", -1)) != sum(int(w["integers"]) for w in windows):
                raise AssertionError("log-window summary integer count mismatch")
            if any(int(row.get("candidate_count", -1)) != 0 for row in data.get("windows", [])):
                raise AssertionError("log-window summary candidate mismatch")
        elif label == "far_windows":
            if int(data.get("window_count_compared", -1)) != len(windows):
                raise AssertionError("far-window count mismatch")
            if int(data.get("integers_tested", -1)) != sum(int(w["integers"]) for w in windows):
                raise AssertionError("far-window integer count mismatch")
            if data.get("candidate_count") != 0 or not data.get("complete_independent_crosscheck"):
                raise AssertionError("far-window summary not complete/empty")
    return {
        "label": label,
        "window_count": len(windows),
        "integers": sum(int(w["integers"]) for w in windows),
        "candidate_count": 0,
        "matched_unordered_square_pairs": sum(int(w["unordered_square_pairs"]) for w in windows),
        "summary": str(summary.relative_to(ROOT)) if summary else None,
        "summary_sha256": sha256(summary) if summary else None,
        "windows": windows,
    }


FACTOR_KEYS = (
    "low", "high", "C", "D", "finite_bound_3_rhs", "finite_bound_5_rhs",
    "max_odd", "certificate_family", "admissible_pair_count_at_high",
    "distinct_shift_count_at_high", "integers_tested",
    "shifts_processed_before_termination", "factor_groups_processed",
    "candidate_count", "candidates", "first_failure_histogram", "factor_groups",
)


def validate_factor_chunk(path: Path, expected_mode: int) -> dict:
    data = load(path)
    low, high = int(data["low"]), int(data["high"])
    if int(data["max_odd"]) != expected_mode:
        raise AssertionError(f"factor mode mismatch: {path}")
    if int(data["integers_tested"]) != high - low + 1:
        raise AssertionError(f"factor tested count mismatch: {path}")
    domain = exact_domain(high, int(data["C"]), int(data["D"]))
    required = {
        "finite_bound_3_rhs": str(domain["rhs3"]),
        "finite_bound_5_rhs": str(domain["rhs5"]),
        "admissible_pair_count_at_high": domain["pairs"],
        "distinct_shift_count_at_high": domain["shifts"],
    }
    for key, value in required.items():
        if data.get(key) != value:
            raise AssertionError(f"factor domain mismatch in {key}: {path}")
    candidates = [str(v) for v in data["candidates"]]
    if int(data["candidate_count"]) != len(candidates):
        raise AssertionError(f"factor candidate count mismatch: {path}")
    if candidates:
        raise AssertionError(f"factor result is not empty: {path}")
    hist_total = sum(int(row["count"]) for row in data["first_failure_histogram"])
    if hist_total != int(data["integers_tested"]):
        raise AssertionError(f"factor first-failure total mismatch: {path}")
    if int(data["factor_groups_processed"]) != len(data["factor_groups"]):
        raise AssertionError(f"factor-group count mismatch: {path}")
    return data


def audit_factor_summary(path: Path, expected_low: int, expected_high: int,
                         expected_mode: int, expected_chunks: int) -> tuple[dict, list[dict]]:
    summary = load(path)
    required = {
        "low": str(expected_low), "high": str(expected_high),
        "max_odd": expected_mode, "chunk_count": expected_chunks,
        "complete_gapless_coverage": True,
        "integers_tested": expected_high - expected_low + 1,
        "candidate_count": 0, "candidates": [],
    }
    for key, value in required.items():
        if summary.get(key) != value:
            raise AssertionError(f"factor summary {path}: mismatch in {key}")
    rows = summary.get("chunks", [])
    if len(rows) != expected_chunks:
        raise AssertionError(f"factor summary {path}: chunk list length")
    intervals: list[tuple[int, int]] = []
    chunks: list[dict] = []
    for row in rows:
        chunk_path = resolve(row["json"])
        if not chunk_path.is_file():
            raise AssertionError(f"missing factor chunk: {chunk_path}")
        if "json_sha256" in row and sha256(chunk_path) != row["json_sha256"]:
            raise AssertionError(f"factor chunk hash mismatch: {chunk_path}")
        data = validate_factor_chunk(chunk_path, expected_mode)
        low, high = int(data["low"]), int(data["high"])
        if (str(low), str(high)) != (str(row["low"]), str(row["high"])):
            raise AssertionError(f"factor row interval mismatch: {chunk_path}")
        intervals.append((low, high)); chunks.append(data)
    check_gapless_intervals(intervals, expected_low, expected_high)
    return summary, chunks


def audit_factor_pair(label: str, first_path: Path, second_path: Path,
                      low: int, high: int, mode: int, chunks: int) -> dict[str, object]:
    first, achunks = audit_factor_summary(first_path, low, high, mode, chunks)
    second, bchunks = audit_factor_summary(second_path, low, high, mode, chunks)
    for index, (a, b) in enumerate(zip(achunks, bchunks)):
        differences = [key for key in FACTOR_KEYS if a.get(key) != b.get(key)]
        if differences:
            raise AssertionError(f"{label}: chunk {index} differs in {differences}")
    return {
        "label": label,
        "low": str(low), "high": str(high), "integers": high - low + 1,
        "max_odd": mode, "chunk_count": chunks, "candidate_count": 0,
        "full_mathematical_output_match": True,
        "first_summary": str(first_path.relative_to(ROOT)),
        "second_summary": str(second_path.relative_to(ROOT)),
        "first_summary_sha256": sha256(first_path),
        "second_summary_sha256": sha256(second_path),
    }


def audit_factor_single(label: str, path: Path, low: int, high: int,
                        mode: int, chunks: int) -> dict[str, object]:
    audit_factor_summary(path, low, high, mode, chunks)
    return {
        "label": label,
        "low": str(low), "high": str(high), "integers": high - low + 1,
        "max_odd": mode, "chunk_count": chunks, "candidate_count": 0,
        "summary": str(path.relative_to(ROOT)), "summary_sha256": sha256(path),
    }


def audit_fixed_pool() -> dict[str, object]:
    first_path = ROOT / "output/formal_ranked_256_10m_bitset_finalsource.json"
    second_path = ROOT / "output/formal_ranked_256_10m_clean_cpp.json"
    pool_path = ROOT / "output/primes_ranked_256.txt"
    first_log = ROOT / "logs/formal_ranked_256_10m_bitset_finalsource.time"
    second_log = ROOT / "logs/formal_ranked_256_10m_clean_cpp.time"
    a, b = load(first_path), load(second_path)
    # The clean-room scanner's older JSON schema deliberately omitted the
    # literal prime list.  We therefore compare every common mathematical
    # field and audit the raw /usr/bin/time command lines, both of which name
    # the same retained prime-pool file.
    keys = (
        "low", "high", "C", "D", "prime_count",
        "distinct_shift_count_relevant_to_high", "integers_tested",
        "candidate_count", "candidates",
    )
    differences = [key for key in keys if a.get(key) != b.get(key)]
    if differences:
        raise AssertionError(f"fixed-pool implementations differ: {differences}")
    low, high = int(a["low"]), int(a["high"])
    domain = exact_domain(high, int(a["C"]), int(a["D"]))
    if a["rectangle_pair_count_relevant_to_high"] != domain["pairs"] or a["distinct_shift_count_relevant_to_high"] != domain["shifts"]:
        raise AssertionError("fixed-pool exact-domain count mismatch")
    primes = [int(line) for line in pool_path.read_text(encoding="utf-8").split()]
    if a.get("primes") != primes:
        raise AssertionError("fixed-pool embedded list differs from retained pool file")
    if int(a["prime_count"]) != 256 or len(primes) != 256 or primes[0] != 3:
        raise AssertionError("fixed-pool prime list mismatch")
    for log in (first_log, second_log):
        text = log.read_text(encoding="utf-8")
        if "output/primes_ranked_256.txt" not in text and str(pool_path) not in text:
            raise AssertionError(f"fixed-pool raw command does not name retained pool: {log}")
    if int(a["candidate_count"]) != 0 or a["candidates"]:
        raise AssertionError("fixed-pool candidates nonempty")
    return {
        "low": str(low), "high": str(high), "integers": high - low + 1,
        "prime_count": 256, "candidate_count": 0,
        "common_mathematical_output_match": True,
        "prime_pool": str(pool_path.relative_to(ROOT)),
        "prime_pool_sha256": sha256(pool_path),
        "first": str(first_path.relative_to(ROOT)), "second": str(second_path.relative_to(ROOT)),
        "first_sha256": sha256(first_path), "second_sha256": sha256(second_path),
        "raw_command_logs": [str(first_log.relative_to(ROOT)), str(second_log.relative_to(ROOT))],
    }


def assert_disjoint(intervals: list[tuple[int, int]]) -> None:
    ordered = sorted(intervals)
    for (_, previous_high), (next_low, _) in zip(ordered, ordered[1:]):
        if previous_high >= next_low:
            raise AssertionError(f"claimed disjoint direct intervals overlap at {next_low}")


def source_hashes() -> dict[str, str]:
    names = (
        "src/common.py", "src/verifier.py", "src/verifier_gmp.cpp",
        "src/search_z3_direct.py", "src/search_z3_cegis.py",
        "src/search_bitset.cpp", "src/search_exhaustive_clean.cpp",
        "src/search_factor_sieve.cpp", "src/search_factor_sieve_clean.cpp",
        "src/search_twosquares_bitset.cpp", "src/search_twosquares_clean.cpp",
        "src/audit_formal_results.py", "src/verify_direct_outputs.py",
        "tests/toy_tests.py", "tests/direct_small_crosscheck.py",
        "tests/factor_small_crosscheck.py",
    )
    return {name: sha256(ROOT / name) for name in names}


def main(output: Path | None = None) -> int:
    direct: list[dict[str, object]] = []
    direct.append(audit_direct_gapless(
        "continuous_next_1p6_billion",
        ROOT / "output/direct/formal_1p6b_final/x", ROOT / "output/direct/formal_1p6b_final/y",
        240_000_000_001, 241_600_000_000, 160,
        ROOT / "output/direct/formal_1p6b_final/summary.json"))

    manifest = ROOT / "output/direct/far_windows/windows.tsv"
    far_names: list[str] = []
    far_intervals: list[tuple[int, int]] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        name, low_text, high_text = line.split()
        far_names.append(f"window_{name}")
        far_intervals.append((int(low_text), int(high_text)))
    direct.append(audit_direct_named_windows(
        "far_windows", far_names,
        ROOT / "output/direct/far_windows/x", ROOT / "output/direct/far_windows/y",
        ROOT / "output/direct/far_windows/summary.json"))

    log_intervals = [
        (1_000_000_000_001, 1_000_001_000_000),
        (10_000_000_000_001, 10_000_001_000_000),
        (100_000_000_000_001, 100_000_001_000_000),
    ]
    direct.append(audit_direct_named_windows(
        "logarithmic_windows", ("w1e12", "w1e13", "w1e14"),
        ROOT / "output/direct/log_windows/x", ROOT / "output/direct/log_windows/y",
        ROOT / "output/direct/log_windows/summary.json"))

    direct.append(audit_direct_gapless(
        "cross_C24_activation",
        ROOT / "output/direct/cross_C24_boundary/x", ROOT / "output/direct/cross_C24_boundary/y",
        282_420_000_001, 282_440_000_000, 2,
        ROOT / "output/direct/cross_C24_boundary/summary.json"))
    direct.append(audit_direct_gapless(
        "cross_D17_activation",
        ROOT / "output/direct/cross_D17_boundary/x", ROOT / "output/direct/cross_D17_boundary/y",
        762_930_000_001, 762_950_000_000, 2,
        ROOT / "output/direct/cross_D17_boundary/summary.json"))

    all_direct_intervals = [(240_000_000_001, 241_600_000_000), *far_intervals, *log_intervals,
                            (282_420_000_001, 282_440_000_000),
                            (762_930_000_001, 762_950_000_000)]
    assert_disjoint(all_direct_intervals)
    direct_total = sum(int(row["integers"]) for row in direct)
    if direct_total != 1_853_000_000:
        raise AssertionError(f"direct total mismatch: {direct_total}")

    factor_dual = [
        audit_factor_pair(
            "all_prime_exact_valuation_one_first_100m",
            ROOT / "output/formal_allprime_exact1_primary_b00_summary.json",
            ROOT / "output/formal_allprime_exact1_clean_b00_summary.json",
            240_000_000_001, 240_100_000_000, 1, 10),
        audit_factor_pair(
            "all_prime_valuation_1_or_3_first_100m",
            ROOT / "output/formal_allprime_odd13_primary_b00_summary.json",
            ROOT / "output/formal_allprime_odd13_clean_b00_summary.json",
            240_000_000_001, 240_100_000_000, 3, 10),
        audit_factor_pair(
            "all_prime_arbitrary_odd_first_100m",
            ROOT / "output/formal_allprime_allodd_primary_100m_summary.json",
            ROOT / "output/formal_allprime_allodd_clean_100m_summary.json",
            240_000_000_001, 240_100_000_000, -1, 10),
        audit_factor_pair(
            "all_prime_exact_valuation_one_band_282_3B",
            ROOT / "output/formal_allprime_exact1_primary_band282_summary.json",
            ROOT / "output/formal_allprime_exact1_clean_band282_summary.json",
            282_300_000_001, 282_400_000_000, 1, 10),
    ]
    factor_single = [
        audit_factor_single(
            "primary_all_prime_exact_one_next_billion",
            ROOT / "output/formal_allprime_exact1_primary_1b_summary.json",
            240_000_000_001, 241_000_000_000, 1, 100),
        audit_factor_single(
            "primary_all_prime_exact_one_band_250B",
            ROOT / "output/formal_allprime_exact1_primary_band250_summary.json",
            250_000_000_001, 250_100_000_000, 1, 10),
        audit_factor_single(
            "primary_all_prime_exact_one_band_270B",
            ROOT / "output/formal_allprime_exact1_primary_band270_summary.json",
            270_000_000_001, 270_100_000_000, 1, 10),
    ]

    methods = {}
    for name, path in {
        "A_K16": ROOT / "output/formal_method_a_K16_100.json",
        "A_K32": ROOT / "output/formal_method_a_K32_100.json",
        "B_K16": ROOT / "output/formal_method_b_K16_100.json",
        "B_K32": ROOT / "output/formal_method_b_K32_100.json",
    }.items():
        data = load(path)
        if data.get("candidate") is not None:
            raise AssertionError(f"unexpected stored solver candidate: {path}")
        methods[name] = {
            "classification": data.get("classification"),
            "candidate": None,
            "sha256": sha256(path),
            "path": str(path.relative_to(ROOT)),
        }

    payload = {
        "schema": "a303656-formal-results-audit-v1",
        "audit_status": "PASS",
        "certified_counterexample_found": False,
        "direct_original_representation_search": {
            "classification": "INDEPENDENTLY REPRODUCIBLE EXACT EXHAUSTIVE FINITE COMPUTATION ON EXPLICIT INTERVALS",
            "total_distinct_integers": direct_total,
            "candidate_count": 0,
            "datasets": direct,
        },
        "all_prime_factor_certificate_search": {
            "dual_implementation_results": factor_dual,
            "single_implementation_results": factor_single,
        },
        "fixed_pool_method_C": audit_fixed_pool(),
        "SMT_CEGIS_pilots": methods,
        "source_sha256": source_hashes(),
    }
    out = output or (ROOT / "output/formal_results_audit.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("FORMAL_RESULTS_AUDIT_PASS")
    print(f"direct_distinct_integer_count={direct_total}")
    print("direct_candidate_count=0")
    print(f"factor_dual_dataset_count={len(factor_dual)}")
    print(f"factor_single_dataset_count={len(factor_single)}")
    print(f"output={out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="write the regenerated audit to this path; defaults to the historical in-tree location",
    )
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.output))
