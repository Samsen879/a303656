#!/usr/bin/env python3
"""Generate exact obstruction dossiers for the fixed selected PILOT-B panel.

This program reads the already validated PILOT-B counts.  It does not invoke a
counter, scan a new interval, perform CRT work, or search for a new fixture.
All arithmetic is integer arithmetic.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "a303656-selected-obstruction-dossier-v1"
STARTING_COMMIT = "3a93ab744825780c14c58d177a5a8d97e887e1e2"
PILOT_B_LOW = 240000000001
PILOT_B_HIGH_EXCLUSIVE = 240000100001
PILOT_B_COUNTS_SHA256 = "2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773"
LOW_TAIL_PANEL = (
    (240000005594, 16),
    (240000004802, 18),
    (240000044158, 19),
    (240000000968, 20),
    (240000001544, 21),
)
REGRESSION_PANEL = (2, 3, 5, 25)
TOP_K_VALUES = (1, 2, 4, 8, 16)
BASELINE_PATHS = (
    "output/formal_results_audit.json",
    "output/final_packaging_audit.json",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt",
    "output/final_results_manifest.json",
    "output/direct/formal_1p6b_final/summary.json",
)
PILOT_INPUT_GLOBS = (
    "pilot_a/bitset/counts.csv", "pilot_a/bitset/low_t.jsonl",
    "pilot_a/clean/counts.csv", "pilot_a/clean/low_t.jsonl",
    "pilot_a/oracle/counts.csv", "pilot_a/oracle/low_t.jsonl",
    "pilot_b/bitset/counts.csv", "pilot_b/bitset/low_t.jsonl",
    "pilot_b/clean/counts.csv", "pilot_b/clean/low_t.jsonl",
    "pilot_b/oracle/counts.csv", "pilot_b/oracle/low_t.jsonl",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_ratio(numerator: int, denominator: int) -> dict[str, Any]:
    if denominator <= 0:
        raise ValueError("ratio denominator must be positive")
    with localcontext() as context:
        context.prec = 60
        decimal = format(Decimal(numerator) / Decimal(denominator), ".15f")
    return {"numerator": numerator, "denominator": denominator, "decimal": decimal}


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def strict_unsigned(text: str, field: str) -> int:
    if not text or not text.isascii() or not text.isdigit():
        raise ValueError(f"{field} is not an unsigned decimal integer: {text!r}")
    if len(text) > 1 and text[0] == "0":
        raise ValueError(f"{field} is not canonical decimal: {text!r}")
    return int(text)


def load_validated_counts(input_root: Path) -> tuple[dict[int, int], dict[str, str]]:
    role_paths = {
        role: input_root / "pilot_b" / role / "counts.csv"
        for role in ("bitset", "clean", "oracle")
    }
    payloads = {role: path.read_bytes() for role, path in role_paths.items()}
    if not (payloads["bitset"] == payloads["clean"] == payloads["oracle"]):
        raise ValueError("validated PILOT-B count arrays are not byte-identical")
    hashes = {role: hashlib.sha256(data).hexdigest() for role, data in payloads.items()}
    if any(value != PILOT_B_COUNTS_SHA256 for value in hashes.values()):
        raise ValueError(f"unexpected PILOT-B counts SHA256: {hashes}")

    rows: dict[int, int] = {}
    with role_paths["bitset"].open(newline="", encoding="ascii") as handle:
        reader = csv.reader(handle)
        if next(reader, None) != ["n", "T"]:
            raise ValueError("PILOT-B counts header mismatch")
        expected_n = PILOT_B_LOW
        for line_number, row in enumerate(reader, start=2):
            if len(row) != 2:
                raise ValueError(f"bad counts row {line_number}")
            n = strict_unsigned(row[0], "n")
            value = strict_unsigned(row[1], "T")
            if n != expected_n:
                raise ValueError(f"noncontiguous counts at row {line_number}: {n} != {expected_n}")
            rows[n] = value
            expected_n += 1
    if expected_n != PILOT_B_HIGH_EXCLUSIVE or len(rows) != 100_000:
        raise ValueError("PILOT-B counts interval or row count mismatch")
    return rows, {str(path.relative_to(input_root.parent.parent)): hashes[role] for role, path in role_paths.items()}


def select_controls(counts: dict[int, int]) -> list[dict[str, Any]]:
    low_values = {n for n, _ in LOW_TAIL_PANEL}
    selections: list[dict[str, Any]] = []
    for n, expected_t in LOW_TAIL_PANEL:
        if counts.get(n) != expected_t:
            raise ValueError(f"validated T mismatch for low-tail n={n}")
        block_index = (n - PILOT_B_LOW) // 10_000
        block_start = PILOT_B_LOW + block_index * 10_000
        block_end = block_start + 10_000
        candidates = (
            (abs(value - 60), abs(m - n), m, value)
            for m, value in counts.items()
            if block_start <= m < block_end and m % 120 == n % 120 and m not in low_values
        )
        distance_from_60, distance_from_n, control, control_t = min(candidates)
        selections.append(
            {
                "low_tail_n": n,
                "low_tail_T": expected_t,
                "block_index": block_index,
                "block_start": block_start,
                "block_end_exclusive": block_end,
                "residue_mod_120": n % 120,
                "control_n": control,
                "control_T": control_t,
                "selection_key": [distance_from_60, distance_from_n, control],
            }
        )
    return selections


def active_pairs(n: int) -> list[tuple[int, int, int]]:
    powers3: list[int] = []
    value = 1
    while value <= n:
        powers3.append(value)
        value *= 3
    powers5: list[int] = []
    value = 1
    while value <= n:
        powers5.append(value)
        value *= 5
    return [
        (c, d, power3 + power5)
        for c, power3 in enumerate(powers3)
        for d, power5 in enumerate(powers5)
        if power3 + power5 <= n
    ]


def eratosthenes(limit: int) -> list[int]:
    if limit < 2:
        return []
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            start = p * p
            flags[start:limit + 1:p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def deterministic_prime_uint64(n: int) -> bool:
    """Deterministic Miller--Rabin for every unsigned 64-bit integer."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # Jim Sinclair / deterministic 64-bit basis set.
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def complete_factorization(value: int, primes: Iterable[int]) -> list[tuple[int, int]]:
    if value <= 0:
        raise ValueError("factorization is defined here only for positive integers")
    residual = value
    factors: list[tuple[int, int]] = []
    for prime in primes:
        if prime * prime > residual:
            break
        if residual % prime:
            continue
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        factors.append((prime, exponent))
    if residual > 1:
        factors.append((residual, 1))
    product = 1
    previous = 1
    for prime, exponent in factors:
        if prime <= previous or exponent <= 0 or not deterministic_prime_uint64(prime):
            raise AssertionError("internal factorization verification failed")
        product *= prime ** exponent
        previous = prime
    if product != value:
        raise AssertionError("factor product does not reconstruct input")
    return factors


def canonical_two_square_witness(remainder: int) -> tuple[int, int] | None:
    if remainder < 0:
        return None
    if remainder == 0:
        return (0, 0)
    for a in range(math.isqrt(remainder // 2) + 1):
        b_squared = remainder - a * a
        b = math.isqrt(b_squared)
        if b * b == b_squared and a <= b:
            return (a, b)
    return None


def factor_json(factors: list[tuple[int, int]]) -> list[dict[str, Any]]:
    return [
        {
            "prime": prime,
            "exponent": exponent,
            "primality_verification_status": "DETERMINISTIC_MILLER_RABIN_UINT64_PASS",
        }
        for prime, exponent in factors
    ]


def build_records_for_n(n: int, primes: list[int], purpose: str) -> list[dict[str, Any]]:
    pairs = active_pairs(n)
    multiplicity = Counter(shift for _, _, shift in pairs)
    records: list[dict[str, Any]] = []
    for c, d, shift in pairs:
        remainder = n - shift
        if remainder == 0:
            factors: list[tuple[int, int]] = []
            obstruction_primes: list[int] = []
            witness = (0, 0)
            factor_status = "ZERO_REMAINDER_NOT_APPLICABLE"
            theorem_status = "ZERO_REMAINDER_WINNER_VERIFIED"
        else:
            factors = complete_factorization(remainder, primes)
            obstruction_primes = [p for p, e in factors if p % 4 == 3 and e % 2 == 1]
            witness = canonical_two_square_witness(remainder) if not obstruction_primes else None
            factor_status = "COMPLETE_FACTORIZATION_VERIFIED"
            theorem_status = (
                "FERMAT_TWO_SQUARE_WINNER_VERIFIED"
                if not obstruction_primes
                else "FERMAT_TWO_SQUARE_OBSTRUCTION_VERIFIED"
            )
        status = "WINNER" if not obstruction_primes else "LOSER"
        if status == "WINNER" and witness is None:
            raise AssertionError(f"Fermat winner lacks witness for n={n}, c={c}, d={d}")
        record: dict[str, Any] = {
            "schema": "a303656-obstruction-pair-record-v1",
            "purpose": purpose,
            "n": n,
            "c": c,
            "d": d,
            "shift": shift,
            "duplicate_shift_multiplicity": multiplicity[shift],
            "remainder": remainder,
            "status": status,
            "complete_factorization": factor_json(factors),
            "factorization_verification_status": factor_status,
            "two_square_theorem_status": theorem_status,
            "all_3mod4_odd_valuation_primes": obstruction_primes,
        }
        if status == "WINNER":
            assert witness is not None
            record.update(
                {
                    "canonical_a": witness[0],
                    "canonical_b": witness[1],
                    "witness_verified": True,
                }
            )
        else:
            record.update(
                {
                    "canonical_obstruction_prime": obstruction_primes[0],
                    "obstruction_verified": True,
                }
            )
        records.append(record)
    return records


def duplicate_groups(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_shift: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_shift[record["shift"]].append(record)
    groups = []
    for shift, rows in sorted(by_shift.items()):
        if len(rows) < 2:
            continue
        reference = rows[0]
        consistency_fields = (
            "remainder", "status", "complete_factorization",
            "all_3mod4_odd_valuation_primes",
        )
        consistent = all(
            all(row[field] == reference[field] for field in consistency_fields)
            for row in rows[1:]
        )
        groups.append(
            {
                "shift": shift,
                "multiplicity": len(rows),
                "exponent_pairs": [[row["c"], row["d"]] for row in rows],
                "obstruction_consistent": consistent,
                "status": reference["status"],
                "obstruction_signature": reference["all_3mod4_odd_valuation_primes"],
            }
        )
    return groups


def summarize_n(n: int, expected_t: int, role: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    winners = [row for row in records if row["status"] == "WINNER"]
    losers = [row for row in records if row["status"] == "LOSER"]
    if len(winners) != expected_t:
        raise ValueError(f"correctness failure: n={n} winners={len(winners)} validated_T={expected_t}")
    all_frequency: Counter[int] = Counter()
    canonical_frequency: Counter[int] = Counter()
    signature_frequency: Counter[tuple[int, ...]] = Counter()
    obstruction_count_frequency: Counter[int] = Counter()
    for row in losers:
        signature = tuple(row["all_3mod4_odd_valuation_primes"])
        all_frequency.update(signature)
        canonical_frequency[row["canonical_obstruction_prime"]] += 1
        signature_frequency[signature] += 1
        obstruction_count_frequency[len(signature)] += 1
    ranked_primes = sorted(all_frequency, key=lambda prime: (-all_frequency[prime], prime))
    top_coverage = []
    for k in TOP_K_VALUES:
        selected = ranked_primes[:k]
        selected_set = set(selected)
        covered = sum(
            1 for row in losers
            if selected_set.intersection(row["all_3mod4_odd_valuation_primes"])
        )
        top_coverage.append(
            {
                "k": k,
                "ranked_primes": selected,
                "covered_losing_pairs": covered,
                "coverage": exact_ratio(covered, len(losers)),
            }
        )
    pairs = active_pairs(n)
    duplicates = duplicate_groups(records)
    if not all(group["obstruction_consistent"] for group in duplicates):
        raise AssertionError("duplicate numerical shift has inconsistent obstruction data")
    winner_c = Counter(row["c"] for row in winners)
    winner_d = Counter(row["d"] for row in winners)
    winner_shift = Counter(row["shift"] for row in winners)
    return {
        "schema": "a303656-obstruction-per-n-summary-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "n": n,
        "panel_role": role,
        "validated_T": expected_t,
        "winner_count": len(winners),
        "losing_exponent_pair_count": len(losers),
        "active_pair_count": len(records),
        "T_over_active_pair_count": exact_ratio(len(winners), len(records)),
        "distinct_shift_count": len({row["shift"] for row in records}),
        "duplicate_shift_groups": duplicates,
        "maximum_c": max(c for c, _, _ in pairs),
        "maximum_d": max(d for _, d, _ in pairs),
        "distinct_obstruction_prime_count": len(all_frequency),
        "canonical_obstruction_prime_frequency": [
            {"prime": p, "frequency": canonical_frequency[p]}
            for p in sorted(canonical_frequency)
        ],
        "all_obstruction_prime_frequency": [
            {"prime": p, "frequency": all_frequency[p]}
            for p in ranked_primes
        ],
        "obstruction_prime_ranking_rule": "descending all-obstruction frequency, then ascending prime",
        "top_k_coverage": top_coverage,
        "largest_single_prime_coverage": {
            "prime": ranked_primes[0],
            "covered_losing_pairs": all_frequency[ranked_primes[0]],
            "coverage": exact_ratio(all_frequency[ranked_primes[0]], len(losers)),
        },
        "obstruction_prime_count_per_pair_frequency": [
            {"obstruction_prime_count": count, "losing_pair_frequency": obstruction_count_frequency[count]}
            for count in sorted(obstruction_count_frequency)
        ],
        "obstruction_signature_frequency": [
            {"signature": list(signature), "frequency": frequency}
            for signature, frequency in sorted(signature_frequency.items(), key=lambda item: (item[0], item[1]))
        ],
        "obstruction_signature_diversity": len(signature_frequency),
        "winner_c_distribution": [
            {"c": c, "frequency": winner_c[c]} for c in sorted(winner_c)
        ],
        "winner_d_distribution": [
            {"d": d, "frequency": winner_d[d]} for d in sorted(winner_d)
        ],
        "winner_shift_distribution": [
            {"shift": shift, "frequency": winner_shift[shift]} for shift in sorted(winner_shift)
        ],
    }


def metric_snapshot(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": summary["n"],
        "T": summary["validated_T"],
        "active_pair_count": summary["active_pair_count"],
        "T_over_active_pair_count": summary["T_over_active_pair_count"],
        "distinct_obstruction_prime_count": summary["distinct_obstruction_prime_count"],
        "top_k_coverage": summary["top_k_coverage"],
        "largest_single_prime_coverage": summary["largest_single_prime_coverage"],
        "obstruction_signature_diversity": summary["obstruction_signature_diversity"],
        "winner_c_distribution": summary["winner_c_distribution"],
        "winner_d_distribution": summary["winner_d_distribution"],
        "winner_shift_distribution": summary["winner_shift_distribution"],
    }


def file_hashes(repo_root: Path, paths: Iterable[str]) -> dict[str, str]:
    return {path: sha256_file(repo_root / path) for path in paths}


def pilot_input_hashes(input_root: Path) -> dict[str, str]:
    return {str(Path("output/tn_pilot_20260713") / rel): sha256_file(input_root / rel) for rel in PILOT_INPUT_GLOBS}


def self_test() -> int:
    primes = eratosthenes(1000)
    assert complete_factorization(1, primes) == []
    assert complete_factorization(240, primes) == [(2, 4), (3, 1), (5, 1)]
    assert deterministic_prime_uint64(99991)
    assert not deterministic_prime_uint64(99999)
    assert canonical_two_square_witness(0) == (0, 0)
    assert canonical_two_square_witness(25) == (0, 5)
    assert {(c, d) for c, d, shift in active_pairs(29) if shift == 28} == {(1, 2), (3, 0)}
    expected = {2: 1, 3: 1, 5: 1, 25: 1}
    for n in REGRESSION_PANEL:
        rows = build_records_for_n(n, primes, "SCHEMA_REGRESSION_ONLY")
        assert sum(row["status"] == "WINNER" for row in rows) == expected[n]
        assert all(row["purpose"] == "SCHEMA_REGRESSION_ONLY" for row in rows)
    print("GENERATOR_SELF_TEST_PASS")
    return 0


def generate(args: argparse.Namespace) -> int:
    repo_root = args.repo_root.resolve()
    input_root = (repo_root / args.input_root).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite output directory: {output_dir}")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True).strip()
    if head != STARTING_COMMIT:
        raise ValueError(f"starting commit mismatch: {head} != {STARTING_COMMIT}")
    baseline_before = file_hashes(repo_root, BASELINE_PATHS)
    pilot_before = pilot_input_hashes(input_root)
    counts, count_hashes = load_validated_counts(input_root)
    selections = select_controls(counts)
    controls = [row["control_n"] for row in selections]
    duplicate_controls = [n for n, count in Counter(controls).items() if count > 1]
    panel_order = [n for n, _ in LOW_TAIL_PANEL]
    for control in controls:
        if control not in panel_order:
            panel_order.append(control)
    if len(panel_order) > 10:
        raise AssertionError("distinct panel exceeds ten integers")
    role_by_n = {n: "LOW_TAIL" for n, _ in LOW_TAIL_PANEL}
    for control in controls:
        role_by_n.setdefault(control, "MATCHED_CONTROL")
    expected_t = {n: counts[n] for n in panel_order}
    primes = eratosthenes(math.isqrt(max(panel_order)))
    all_records: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for n in panel_order:
        rows = build_records_for_n(n, primes, "PILOT_B_SELECTED_FIXTURE")
        all_records.extend(rows)
        summaries.append(summarize_n(n, expected_t[n], role_by_n[n], rows))
    summary_by_n = {row["n"]: row for row in summaries}

    regression = []
    regression_primes = eratosthenes(math.isqrt(max(REGRESSION_PANEL)))
    for n in REGRESSION_PANEL:
        rows = build_records_for_n(n, regression_primes, "SCHEMA_REGRESSION_ONLY")
        regression.append(
            {
                "n": n,
                "purpose": "SCHEMA_REGRESSION_ONLY",
                "active_pair_count": len(rows),
                "winner_count": sum(row["status"] == "WINNER" for row in rows),
                "contains_remainder_zero": any(row["remainder"] == 0 for row in rows),
                "records": rows,
            }
        )

    panel_entries = []
    for n in panel_order:
        matched_for = [row["low_tail_n"] for row in selections if row["control_n"] == n]
        panel_entries.append(
            {
                "n": n,
                "validated_T": expected_t[n],
                "panel_role": role_by_n[n],
                "matched_for_low_tail_n": matched_for,
            }
        )
    panel_json = {
        "schema": "a303656-selected-obstruction-panel-v1",
        "task": "SELECTED PILOT-B OBSTRUCTION DOSSIER",
        "classification": "EXACT FINITE COMPUTATION ON FIXED SELECTED FIXTURES",
        "pilot_b_interval": {"low": PILOT_B_LOW, "high_exclusive": PILOT_B_HIGH_EXCLUSIVE},
        "low_tail_panel": [{"n": n, "validated_T": value} for n, value in LOW_TAIL_PANEL],
        "control_selection_rule": {
            "block_anchor": PILOT_B_LOW,
            "block_width": 10_000,
            "same_residue_modulus": 120,
            "lexicographic_key": ["abs(T(m)-60)", "abs(m-n)", "m"],
            "exclude_all_low_tail_members": True,
            "source": "existing validated PILOT-B counts.csv only",
        },
        "matched_control_selections": selections,
        "duplicate_control_selection": bool(duplicate_controls),
        "duplicate_controls": duplicate_controls,
        "distinct_research_panel_size": len(panel_order),
        "research_panel": panel_entries,
        "regression_fixtures": regression,
    }
    per_n_json = {
        "schema": "a303656-selected-obstruction-per-n-collection-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "summaries": summaries,
    }
    low_vs_control = {
        "schema": "a303656-low-vs-control-comparison-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "global_statistical_significance_claimed": False,
        "comparisons": [
            {
                "low_tail_n": selection["low_tail_n"],
                "control_n": selection["control_n"],
                "selection_key": selection["selection_key"],
                "low_tail": metric_snapshot(summary_by_n[selection["low_tail_n"]]),
                "matched_control": metric_snapshot(summary_by_n[selection["control_n"]]),
                "scalar_differences_control_minus_low": {
                    "T": summary_by_n[selection["control_n"]]["validated_T"] - summary_by_n[selection["low_tail_n"]]["validated_T"],
                    "active_pair_count": summary_by_n[selection["control_n"]]["active_pair_count"] - summary_by_n[selection["low_tail_n"]]["active_pair_count"],
                    "distinct_obstruction_prime_count": summary_by_n[selection["control_n"]]["distinct_obstruction_prime_count"] - summary_by_n[selection["low_tail_n"]]["distinct_obstruction_prime_count"],
                    "obstruction_signature_diversity": summary_by_n[selection["control_n"]]["obstruction_signature_diversity"] - summary_by_n[selection["low_tail_n"]]["obstruction_signature_diversity"],
                },
            }
            for selection in selections
        ],
    }

    n0 = LOW_TAIL_PANEL[0][0]
    n0_rows = [row for row in all_records if row["n"] == n0]
    n0_losers = [row for row in n0_rows if row["status"] == "LOSER"]
    n0_frequency: Counter[int] = Counter()
    for row in n0_losers:
        n0_frequency.update(row["all_3mod4_odd_valuation_primes"])
    high_coverage = [
        prime for prime in sorted(n0_frequency)
        if n0_frequency[prime] * 100 >= len(n0_losers) * 5
    ]
    n0_winners = []
    for row in n0_rows:
        if row["status"] != "WINNER":
            continue
        n0_winners.append(
            {
                "c": row["c"], "d": row["d"], "shift": row["shift"],
                "remainder": row["remainder"],
                "complete_factorization": row["complete_factorization"],
                "canonical_a": row["canonical_a"], "canonical_b": row["canonical_b"],
                "remainder_residues_mod_high_coverage_primes": [
                    {"prime": prime, "residue": row["remainder"] % prime}
                    for prime in high_coverage
                ],
            }
        )
    n0_json = {
        "schema": "a303656-n0-surviving-pairs-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "n0": n0,
        "validated_T": 16,
        "winner_pair_count": len(n0_winners),
        "high_coverage_definition": "prime covers at least 5 percent of n0 losing exponent pairs",
        "losing_pair_count": len(n0_losers),
        "high_coverage_primes": [
            {
                "prime": prime,
                "covered_losing_pairs": n0_frequency[prime],
                "coverage": exact_ratio(n0_frequency[prime], len(n0_losers)),
            }
            for prime in high_coverage
        ],
        "residue_table_only": True,
        "CRT_search_performed": False,
        "simultaneous_winner_elimination_claimed": False,
        "surviving_winner_pairs": n0_winners,
    }
    if len(n0_winners) != 16:
        raise ValueError("n0 winner count is not 16")

    output_dir.mkdir(parents=True)
    write_json(output_dir / "panel.json", panel_json)
    with (output_dir / "records.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in all_records:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    write_json(output_dir / "per_n_summary.json", per_n_json)
    with (output_dir / "prime_frequency.csv").open("w", encoding="ascii", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("n", "panel_role", "rank", "prime", "all_obstruction_frequency", "canonical_obstruction_frequency", "losing_pair_count", "coverage_numerator", "coverage_denominator", "coverage_decimal"))
        for summary in summaries:
            canonical = {row["prime"]: row["frequency"] for row in summary["canonical_obstruction_prime_frequency"]}
            for rank, row in enumerate(summary["all_obstruction_prime_frequency"], start=1):
                ratio = exact_ratio(row["frequency"], summary["losing_exponent_pair_count"])
                writer.writerow((summary["n"], summary["panel_role"], rank, row["prime"], row["frequency"], canonical.get(row["prime"], 0), summary["losing_exponent_pair_count"], ratio["numerator"], ratio["denominator"], ratio["decimal"]))
    with (output_dir / "top_k_coverage.csv").open("w", encoding="ascii", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("n", "panel_role", "k", "ranked_primes", "covered_losing_pairs", "losing_pair_count", "coverage_numerator", "coverage_denominator", "coverage_decimal"))
        for summary in summaries:
            for row in summary["top_k_coverage"]:
                ratio = row["coverage"]
                writer.writerow((summary["n"], summary["panel_role"], row["k"], ";".join(map(str, row["ranked_primes"])), row["covered_losing_pairs"], summary["losing_exponent_pair_count"], ratio["numerator"], ratio["denominator"], ratio["decimal"]))
    write_json(output_dir / "low_vs_control.json", low_vs_control)
    write_json(output_dir / "n0_surviving_pairs.json", n0_json)

    baseline_after = file_hashes(repo_root, BASELINE_PATHS)
    pilot_after = pilot_input_hashes(input_root)
    if baseline_before != baseline_after or pilot_before != pilot_after:
        raise ValueError("baseline or validated pilot input changed during generation")
    generated_artifacts = (
        "panel.json", "records.jsonl", "per_n_summary.json", "prime_frequency.csv",
        "top_k_coverage.csv", "low_vs_control.json", "n0_surviving_pairs.json",
    )
    metadata = {
        "schema": "a303656-selected-obstruction-metadata-v1",
        "task": "SELECTED PILOT-B OBSTRUCTION DOSSIER",
        "classification": "EXACT FINITE COMPUTATION ON FIXED SELECTED FIXTURES",
        "mathematical_problem_status": "UNRESOLVED",
        "starting_commit": head,
        "generated_utc": args.generated_utc,
        "generator": {
            "path": "src/generate_obstruction_dossier.py",
            "sha256": sha256_file(Path(__file__)),
            "implementation_id": "selected_obstruction_generator_trial_division_v1",
        },
        "independent_verifier": {
            "path": "src/verify_obstruction_dossier.py",
            "sha256": sha256_file(repo_root / "src/verify_obstruction_dossier.py"),
            "implementation_id": "selected_obstruction_independent_verifier_v1",
            "shares_correctness_critical_factorization_or_two_square_helper": False,
        },
        "primality_contract": {
            "input_bound": "all positive remainders are less than 2^64",
            "factorization_method": "complete trial division by an exact Eratosthenes prime table through integer sqrt of the residual",
            "reported_factor_check": "deterministic Miller-Rabin bases 2,325,9375,28178,450775,9780504,1795265022, valid for uint64",
            "assurance": "DETERMINISTIC_FOR_UINT64_NOT_PROBABLE_PRIME_ONLY",
        },
        "scope_guards": {
            "new_interval_scanned": False,
            "counting_executable_invoked": False,
            "broad_mining_performed": False,
            "CRT_search_performed": False,
            "existing_pilot_outputs_modified": False,
            "certified_baseline_modified": False,
        },
        "panel_distinct_n_count": len(panel_order),
        "record_count": len(all_records),
        "counts_source_sha256": count_hashes,
        "artifact_sha256": {name: sha256_file(output_dir / name) for name in generated_artifacts},
        "baseline_integrity": {
            "before_generation": baseline_before,
            "after_generation": baseline_after,
            "byte_identical": baseline_before == baseline_after,
        },
        "pilot_input_integrity": {
            "before_generation": pilot_before,
            "after_generation": pilot_after,
            "byte_identical": pilot_before == pilot_after,
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
            "pid": os.getpid(),
        },
        "final_conclusion_pending_independent_verifier": True,
    }
    write_json(output_dir / "metadata.json", metadata)
    print(f"DOSSIER_GENERATION_PASS panel={len(panel_order)} records={len(all_records)}")
    print("winner_counts=" + ",".join(f"{row['n']}:{row['winner_count']}" for row in summaries))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test")
    run = subparsers.add_parser("run")
    run.add_argument("--repo-root", type=Path, default=Path("."))
    run.add_argument("--input-root", type=Path, default=Path("output/tn_pilot_20260713"))
    run.add_argument("--output-dir", type=Path, default=Path("analysis/obstruction_dossier"))
    run.add_argument("--generated-utc", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "self-test":
        return self_test()
    return generate(args)


if __name__ == "__main__":
    raise SystemExit(main())
