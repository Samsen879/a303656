#!/usr/bin/env python3
"""Independent verifier for the fixed selected PILOT-B obstruction dossier.

This file imports no generator code.  It independently enumerates exponent
pairs, builds its own prime table, refactors every positive remainder, applies
Fermat's two-square criterion, and checks canonical witnesses by exhaustive
integer-square testing below the reported a.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any, Iterable


STARTING_COMMIT = "3a93ab744825780c14c58d177a5a8d97e887e1e2"
PILOT_LOW = 240000000001
PILOT_HIGH = 240000100001
COUNTS_DIGEST = "2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773"
FIXED_LOW = (
    (240000005594, 16),
    (240000004802, 18),
    (240000044158, 19),
    (240000000968, 20),
    (240000001544, 21),
)
SMALL_FIXTURES = (2, 3, 5, 25)
KS = (1, 2, 4, 8, 16)
BASELINES = (
    "output/formal_results_audit.json",
    "output/final_packaging_audit.json",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt",
    "output/final_results_manifest.json",
    "output/direct/formal_1p6b_final/summary.json",
)
PILOT_RELATIVE_FILES = tuple(
    f"{pilot}/{role}/{name}"
    for pilot in ("pilot_a", "pilot_b")
    for role in ("bitset", "clean", "oracle")
    for name in ("counts.csv", "low_t.jsonl")
)


def digest(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(131072)
            if not block:
                break
            state.update(block)
    return state.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ratio(part: int, whole: int) -> dict[str, Any]:
    if whole < 1:
        raise AssertionError("invalid exact-ratio denominator")
    with localcontext() as ctx:
        ctx.prec = 60
        rendered = format(Decimal(part) / Decimal(whole), ".15f")
    return {"numerator": part, "denominator": whole, "decimal": rendered}


def require_int(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise AssertionError(f"{label} is not an integer >= {minimum}: {value!r}")
    return value


def parse_decimal(cell: str, label: str) -> int:
    if not cell or not cell.isascii() or not cell.isdigit() or (len(cell) > 1 and cell[0] == "0"):
        raise AssertionError(f"noncanonical {label}: {cell!r}")
    return int(cell)


def independent_counts(input_root: Path) -> tuple[dict[int, int], dict[str, str]]:
    paths = [input_root / "pilot_b" / role / "counts.csv" for role in ("bitset", "clean", "oracle")]
    hashes = {str(path): digest(path) for path in paths}
    if set(hashes.values()) != {COUNTS_DIGEST}:
        raise AssertionError(f"PILOT-B counts hash disagreement: {hashes}")
    first = paths[0].read_bytes()
    if any(path.read_bytes() != first for path in paths[1:]):
        raise AssertionError("PILOT-B counts are not byte-identical")
    table: dict[int, int] = {}
    with paths[0].open(encoding="ascii", newline="") as stream:
        parser = csv.DictReader(stream)
        if parser.fieldnames != ["n", "T"]:
            raise AssertionError("counts header mismatch")
        cursor = PILOT_LOW
        for row in parser:
            n = parse_decimal(row["n"], "n")
            t = parse_decimal(row["T"], "T")
            if n != cursor:
                raise AssertionError(f"counts gap at {cursor}, observed {n}")
            table[n] = t
            cursor += 1
    if cursor != PILOT_HIGH or len(table) != 100000:
        raise AssertionError("counts interval mismatch")
    return table, hashes


def independent_control_selection(table: dict[int, int]) -> list[dict[str, Any]]:
    excluded = {n for n, _ in FIXED_LOW}
    selected = []
    for n, t in FIXED_LOW:
        if table[n] != t:
            raise AssertionError("fixed low-tail T mismatch")
        block = (n - PILOT_LOW) // 10000
        start = PILOT_LOW + block * 10000
        stop = start + 10000
        eligible: list[tuple[tuple[int, int, int], int]] = []
        residue = n % 120
        for m in range(start, stop):
            if m in excluded or m % 120 != residue:
                continue
            eligible.append(((abs(table[m] - 60), abs(m - n), m), table[m]))
        key, control_t = sorted(eligible, key=lambda item: item[0])[0]
        selected.append(
            {
                "low_tail_n": n, "low_tail_T": t,
                "block_index": block, "block_start": start, "block_end_exclusive": stop,
                "residue_mod_120": residue,
                "control_n": key[2], "control_T": control_t,
                "selection_key": list(key),
            }
        )
    return selected


def independent_active_pairs(n: int) -> list[tuple[int, int, int]]:
    result: list[tuple[int, int, int]] = []
    c = 0
    power3 = 1
    while power3 + 1 <= n:
        d = 0
        power5 = 1
        while power3 + power5 <= n:
            result.append((c, d, power3 + power5))
            d += 1
            power5 *= 5
        c += 1
        power3 *= 3
    return result


def odd_only_prime_table(limit: int) -> list[int]:
    """Independent odd-index sieve; no generator sieve code is used."""
    if limit < 2:
        return []
    composite = bytearray(limit // 2 + 1)
    root = math.isqrt(limit)
    index = 1
    while 2 * index + 1 <= root:
        candidate = 2 * index + 1
        if not composite[index]:
            first = (candidate * candidate) // 2
            for mark in range(first, len(composite), candidate):
                composite[mark] = 1
        index += 1
    answer = [2]
    for i in range(1, len(composite)):
        candidate = 2 * i + 1
        if candidate <= limit and not composite[i]:
            answer.append(candidate)
    return answer


def verifier_prime_test(n: int) -> bool:
    """Deterministic MR on this task's n < 341,550,071,728,321 bound."""
    if n < 2:
        return False
    for small in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % small == 0:
            return n == small
    if n >= 341550071728321:
        raise AssertionError("verifier primality input exceeds declared deterministic basis bound")
    odd = n - 1
    twos = 0
    while odd & 1 == 0:
        twos += 1
        odd >>= 1
    for base in (2, 3, 5, 7, 11, 13, 17):
        residue = pow(base, odd, n)
        if residue == 1 or residue == n - 1:
            continue
        passed = False
        for _ in range(twos - 1):
            residue = residue * residue % n
            if residue == n - 1:
                passed = True
                break
        if not passed:
            return False
    return True


def verifier_factor(value: int, primes: Iterable[int]) -> list[tuple[int, int]]:
    if value < 1:
        raise AssertionError("independent factorizer received nonpositive input")
    remaining = value
    output: list[tuple[int, int]] = []
    for divisor in primes:
        if divisor > remaining // divisor:
            break
        count = 0
        while remaining % divisor == 0:
            remaining //= divisor
            count += 1
        if count:
            output.append((divisor, count))
    if remaining != 1:
        output.append((remaining, 1))
    if math.prod(prime ** exponent for prime, exponent in output) != value:
        raise AssertionError("independent factor product mismatch")
    if any(not verifier_prime_test(prime) for prime, _ in output):
        raise AssertionError("independent factorizer produced nonprime")
    return output


def independent_canonical_witness(remainder: int) -> tuple[int, int] | None:
    if remainder < 0:
        return None
    ceiling = math.isqrt(remainder)
    a = 0
    while a <= ceiling and a * a <= remainder - a * a:
        complement = remainder - a * a
        b = math.isqrt(complement)
        if b >= a and b * b == complement:
            return a, b
        a += 1
    return None


def expected_factor_json(factors: list[tuple[int, int]]) -> list[dict[str, Any]]:
    return [
        {
            "prime": prime,
            "exponent": exponent,
            "primality_verification_status": "DETERMINISTIC_MILLER_RABIN_UINT64_PASS",
        }
        for prime, exponent in factors
    ]


def verify_one_record(
    record: dict[str, Any], n: int, expected_pair: tuple[int, int, int],
    shift_count: Counter[int], primes: list[int], purpose: str,
) -> None:
    c, d, shift = expected_pair
    require_int(record.get("n"), "n")
    if record.get("schema") != "a303656-obstruction-pair-record-v1" or record.get("purpose") != purpose:
        raise AssertionError("record schema or purpose mismatch")
    if (record["n"], record.get("c"), record.get("d"), record.get("shift")) != (n, c, d, shift):
        raise AssertionError("record exponent-pair identity mismatch")
    remainder = n - pow(3, c) - pow(5, d)
    if remainder != record.get("remainder") or shift != pow(3, c) + pow(5, d):
        raise AssertionError("record shift/remainder mismatch")
    if record.get("duplicate_shift_multiplicity") != shift_count[shift]:
        raise AssertionError("duplicate shift multiplicity mismatch")
    if remainder == 0:
        factors: list[tuple[int, int]] = []
        obstruction: list[int] = []
        factor_status = "ZERO_REMAINDER_NOT_APPLICABLE"
        theorem_status = "ZERO_REMAINDER_WINNER_VERIFIED"
    else:
        factors = verifier_factor(remainder, primes)
        factor_status = "COMPLETE_FACTORIZATION_VERIFIED"
        obstruction = [prime for prime, exponent in factors if prime % 4 == 3 and exponent % 2]
        theorem_status = "FERMAT_TWO_SQUARE_WINNER_VERIFIED" if not obstruction else "FERMAT_TWO_SQUARE_OBSTRUCTION_VERIFIED"
    if record.get("complete_factorization") != expected_factor_json(factors):
        raise AssertionError("reported factorization differs from independent complete factorization")
    if record.get("factorization_verification_status") != factor_status:
        raise AssertionError("factorization status mismatch")
    if record.get("two_square_theorem_status") != theorem_status:
        raise AssertionError("two-square theorem status mismatch")
    if record.get("all_3mod4_odd_valuation_primes") != obstruction:
        raise AssertionError("odd-valuation obstruction-prime list mismatch")
    product = math.prod(
        require_int(item.get("prime"), "factor prime", 2) ** require_int(item.get("exponent"), "factor exponent", 1)
        for item in record.get("complete_factorization", [])
    )
    if remainder > 0 and product != remainder:
        raise AssertionError("reported factor product does not reconstruct remainder")
    for item in record.get("complete_factorization", []):
        prime = item["prime"]
        if item.get("primality_verification_status") != "DETERMINISTIC_MILLER_RABIN_UINT64_PASS" or not verifier_prime_test(prime):
            raise AssertionError("reported factor fails deterministic primality verification")
    expected_status = "LOSER" if obstruction else "WINNER"
    if record.get("status") != expected_status:
        raise AssertionError("classification mismatch")
    if expected_status == "LOSER":
        if not obstruction or record.get("canonical_obstruction_prime") != min(obstruction) or record.get("obstruction_verified") is not True:
            raise AssertionError("loser obstruction fields invalid")
        if any(key in record for key in ("canonical_a", "canonical_b", "witness_verified")):
            raise AssertionError("loser carries winner-only fields")
    else:
        witness = independent_canonical_witness(remainder)
        if witness is None:
            raise AssertionError("Fermat winner has no independent witness")
        if (record.get("canonical_a"), record.get("canonical_b")) != witness:
            raise AssertionError("witness is not canonical")
        a, b = witness
        if not (0 <= a <= b and a * a + b * b == remainder and record.get("witness_verified") is True):
            raise AssertionError("winner equation invalid")
        if any(key in record for key in ("canonical_obstruction_prime", "obstruction_verified")):
            raise AssertionError("winner carries loser-only fields")


def independent_duplicate_groups(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[row["shift"]].append(row)
    result = []
    for shift in sorted(grouped):
        rows = grouped[shift]
        if len(rows) == 1:
            continue
        base = rows[0]
        consistent = all(
            row["remainder"] == base["remainder"]
            and row["status"] == base["status"]
            and row["complete_factorization"] == base["complete_factorization"]
            and row["all_3mod4_odd_valuation_primes"] == base["all_3mod4_odd_valuation_primes"]
            for row in rows[1:]
        )
        result.append(
            {
                "shift": shift,
                "multiplicity": len(rows),
                "exponent_pairs": [[row["c"], row["d"]] for row in rows],
                "obstruction_consistent": consistent,
                "status": base["status"],
                "obstruction_signature": base["all_3mod4_odd_valuation_primes"],
            }
        )
    return result


def independent_summary(n: int, t: int, role: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    winning = [row for row in records if row["status"] == "WINNER"]
    losing = [row for row in records if row["status"] == "LOSER"]
    if len(winning) != t:
        raise AssertionError(f"winner count {len(winning)} != validated T={t} for n={n}")
    all_frequency: Counter[int] = Counter()
    canonical: Counter[int] = Counter()
    signatures: Counter[tuple[int, ...]] = Counter()
    signature_sizes: Counter[int] = Counter()
    for row in losing:
        sig = tuple(row["all_3mod4_odd_valuation_primes"])
        all_frequency.update(sig)
        canonical[row["canonical_obstruction_prime"]] += 1
        signatures[sig] += 1
        signature_sizes[len(sig)] += 1
    ranking = sorted(all_frequency, key=lambda p: (-all_frequency[p], p))
    top = []
    for k in KS:
        chosen = ranking[:k]
        covered = sum(bool(set(chosen) & set(row["all_3mod4_odd_valuation_primes"])) for row in losing)
        top.append({"k": k, "ranked_primes": chosen, "covered_losing_pairs": covered, "coverage": ratio(covered, len(losing))})
    pairs = independent_active_pairs(n)
    duplicate_data = independent_duplicate_groups(records)
    if any(not row["obstruction_consistent"] for row in duplicate_data):
        raise AssertionError("duplicate-shift obstruction inconsistency")
    c_counts = Counter(row["c"] for row in winning)
    d_counts = Counter(row["d"] for row in winning)
    shift_counts = Counter(row["shift"] for row in winning)
    return {
        "schema": "a303656-obstruction-per-n-summary-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "n": n, "panel_role": role, "validated_T": t, "winner_count": len(winning),
        "losing_exponent_pair_count": len(losing), "active_pair_count": len(records),
        "T_over_active_pair_count": ratio(len(winning), len(records)),
        "distinct_shift_count": len({row["shift"] for row in records}),
        "duplicate_shift_groups": duplicate_data,
        "maximum_c": max(c for c, _, _ in pairs), "maximum_d": max(d for _, d, _ in pairs),
        "distinct_obstruction_prime_count": len(all_frequency),
        "canonical_obstruction_prime_frequency": [{"prime": p, "frequency": canonical[p]} for p in sorted(canonical)],
        "all_obstruction_prime_frequency": [{"prime": p, "frequency": all_frequency[p]} for p in ranking],
        "obstruction_prime_ranking_rule": "descending all-obstruction frequency, then ascending prime",
        "top_k_coverage": top,
        "largest_single_prime_coverage": {"prime": ranking[0], "covered_losing_pairs": all_frequency[ranking[0]], "coverage": ratio(all_frequency[ranking[0]], len(losing))},
        "obstruction_prime_count_per_pair_frequency": [{"obstruction_prime_count": size, "losing_pair_frequency": signature_sizes[size]} for size in sorted(signature_sizes)],
        "obstruction_signature_frequency": [{"signature": list(sig), "frequency": count} for sig, count in sorted(signatures.items(), key=lambda item: (item[0], item[1]))],
        "obstruction_signature_diversity": len(signatures),
        "winner_c_distribution": [{"c": c, "frequency": c_counts[c]} for c in sorted(c_counts)],
        "winner_d_distribution": [{"d": d, "frequency": d_counts[d]} for d in sorted(d_counts)],
        "winner_shift_distribution": [{"shift": shift, "frequency": shift_counts[shift]} for shift in sorted(shift_counts)],
    }


def snapshot(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": summary["n"], "T": summary["validated_T"],
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


def csv_prime_frequency(summaries: list[dict[str, Any]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("n", "panel_role", "rank", "prime", "all_obstruction_frequency", "canonical_obstruction_frequency", "losing_pair_count", "coverage_numerator", "coverage_denominator", "coverage_decimal"))
    for summary in summaries:
        canonical = {row["prime"]: row["frequency"] for row in summary["canonical_obstruction_prime_frequency"]}
        for rank, item in enumerate(summary["all_obstruction_prime_frequency"], 1):
            exact = ratio(item["frequency"], summary["losing_exponent_pair_count"])
            writer.writerow((summary["n"], summary["panel_role"], rank, item["prime"], item["frequency"], canonical.get(item["prime"], 0), summary["losing_exponent_pair_count"], exact["numerator"], exact["denominator"], exact["decimal"]))
    return stream.getvalue()


def csv_top_k(summaries: list[dict[str, Any]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("n", "panel_role", "k", "ranked_primes", "covered_losing_pairs", "losing_pair_count", "coverage_numerator", "coverage_denominator", "coverage_decimal"))
    for summary in summaries:
        for item in summary["top_k_coverage"]:
            exact = item["coverage"]
            writer.writerow((summary["n"], summary["panel_role"], item["k"], ";".join(map(str, item["ranked_primes"])), item["covered_losing_pairs"], summary["losing_exponent_pair_count"], exact["numerator"], exact["denominator"], exact["decimal"]))
    return stream.getvalue()


def current_hashes(repo_root: Path, relative: Iterable[str]) -> dict[str, str]:
    return {name: digest(repo_root / name) for name in relative}


def self_test() -> int:
    primes = odd_only_prime_table(1000)
    assert verifier_factor(1, primes) == []
    assert verifier_factor(240, primes) == [(2, 4), (3, 1), (5, 1)]
    assert verifier_prime_test(99991)
    assert not verifier_prime_test(341550071728319)
    assert independent_canonical_witness(0) == (0, 0)
    assert independent_canonical_witness(25) == (0, 5)
    assert {(c, d) for c, d, shift in independent_active_pairs(29) if shift == 28} == {(1, 2), (3, 0)}
    print("INDEPENDENT_VERIFIER_SELF_TEST_PASS")
    return 0


def verify(args: argparse.Namespace) -> int:
    repo = args.repo_root.resolve()
    input_root = (repo / args.input_root).resolve()
    dossier = (repo / args.dossier_dir).resolve()
    report_path = (repo / args.report).resolve()
    if report_path.exists() and not args.overwrite_report:
        raise AssertionError(f"refusing to overwrite verification report: {report_path}")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", STARTING_COMMIT, head],
        cwd=repo,
        check=False,
    )
    if ancestry.returncode != 0:
        raise AssertionError(f"required starting commit is not an ancestor of verifier HEAD: {head}")
    table, _ = independent_counts(input_root)
    selections = independent_control_selection(table)
    panel = load_json(dossier / "panel.json")
    if panel.get("matched_control_selections") != selections:
        raise AssertionError("panel controls do not match independent mechanical selection")
    expected_duplicates = sorted(n for n, count in Counter(row["control_n"] for row in selections).items() if count > 1)
    if panel.get("duplicate_controls") != expected_duplicates or panel.get("duplicate_control_selection") != bool(expected_duplicates):
        raise AssertionError("duplicate-control reporting mismatch")
    order = [n for n, _ in FIXED_LOW]
    for item in selections:
        if item["control_n"] not in order:
            order.append(item["control_n"])
    expected_roles = {n: "LOW_TAIL" for n, _ in FIXED_LOW}
    for item in selections:
        expected_roles.setdefault(item["control_n"], "MATCHED_CONTROL")
    if [row["n"] for row in panel.get("research_panel", [])] != order or len(order) > 10:
        raise AssertionError("research panel identity/order mismatch")

    records: list[dict[str, Any]] = []
    with (dossier / "records.jsonl").open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.endswith("\n") or not line.strip():
                raise AssertionError(f"malformed JSONL line {line_number}")
            records.append(json.loads(line))
    expected_record_count = sum(len(independent_active_pairs(n)) for n in order)
    if len(records) != expected_record_count:
        raise AssertionError("records.jsonl count mismatch")
    primes = odd_only_prime_table(math.isqrt(max(order)))
    cursor = 0
    verified_by_n: dict[int, list[dict[str, Any]]] = {}
    summaries: list[dict[str, Any]] = []
    for n in order:
        pairs = independent_active_pairs(n)
        rows = records[cursor:cursor + len(pairs)]
        cursor += len(pairs)
        multiplicity = Counter(shift for _, _, shift in pairs)
        for record, pair in zip(rows, pairs, strict=True):
            verify_one_record(record, n, pair, multiplicity, primes, "PILOT_B_SELECTED_FIXTURE")
        verified_by_n[n] = rows
        summaries.append(independent_summary(n, table[n], expected_roles[n], rows))
    expected_summary_document = {
        "schema": "a303656-selected-obstruction-per-n-collection-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "summaries": summaries,
    }
    if load_json(dossier / "per_n_summary.json") != expected_summary_document:
        raise AssertionError("per_n_summary differs from independent reconstruction")
    if (dossier / "prime_frequency.csv").read_text(encoding="ascii") != csv_prime_frequency(summaries):
        raise AssertionError("prime_frequency.csv differs from independent reconstruction")
    if (dossier / "top_k_coverage.csv").read_text(encoding="ascii") != csv_top_k(summaries):
        raise AssertionError("top_k_coverage.csv differs from independent reconstruction")

    summary_by_n = {row["n"]: row for row in summaries}
    expected_comparisons = []
    for item in selections:
        low = summary_by_n[item["low_tail_n"]]
        control = summary_by_n[item["control_n"]]
        expected_comparisons.append(
            {
                "low_tail_n": item["low_tail_n"], "control_n": item["control_n"],
                "selection_key": item["selection_key"],
                "low_tail": snapshot(low), "matched_control": snapshot(control),
                "scalar_differences_control_minus_low": {
                    "T": control["validated_T"] - low["validated_T"],
                    "active_pair_count": control["active_pair_count"] - low["active_pair_count"],
                    "distinct_obstruction_prime_count": control["distinct_obstruction_prime_count"] - low["distinct_obstruction_prime_count"],
                    "obstruction_signature_diversity": control["obstruction_signature_diversity"] - low["obstruction_signature_diversity"],
                },
            }
        )
    expected_low_control = {
        "schema": "a303656-low-vs-control-comparison-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "global_statistical_significance_claimed": False,
        "comparisons": expected_comparisons,
    }
    if load_json(dossier / "low_vs_control.json") != expected_low_control:
        raise AssertionError("low_vs_control differs from independent reconstruction")

    n0 = FIXED_LOW[0][0]
    losers = [row for row in verified_by_n[n0] if row["status"] == "LOSER"]
    frequency: Counter[int] = Counter()
    for row in losers:
        frequency.update(row["all_3mod4_odd_valuation_primes"])
    high = [p for p in sorted(frequency) if frequency[p] * 100 >= len(losers) * 5]
    survivors = []
    for row in verified_by_n[n0]:
        if row["status"] != "WINNER":
            continue
        survivors.append(
            {
                "c": row["c"], "d": row["d"], "shift": row["shift"], "remainder": row["remainder"],
                "complete_factorization": row["complete_factorization"],
                "canonical_a": row["canonical_a"], "canonical_b": row["canonical_b"],
                "remainder_residues_mod_high_coverage_primes": [{"prime": p, "residue": row["remainder"] % p} for p in high],
            }
        )
    expected_n0 = {
        "schema": "a303656-n0-surviving-pairs-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "n0": n0, "validated_T": 16, "winner_pair_count": len(survivors),
        "high_coverage_definition": "prime covers at least 5 percent of n0 losing exponent pairs",
        "losing_pair_count": len(losers),
        "high_coverage_primes": [{"prime": p, "covered_losing_pairs": frequency[p], "coverage": ratio(frequency[p], len(losers))} for p in high],
        "residue_table_only": True, "CRT_search_performed": False,
        "simultaneous_winner_elimination_claimed": False,
        "surviving_winner_pairs": survivors,
    }
    if len(survivors) != 16 or load_json(dossier / "n0_surviving_pairs.json") != expected_n0:
        raise AssertionError("n0 surviving-pair dossier mismatch")

    regression_report = []
    regression_entries = panel.get("regression_fixtures")
    if not isinstance(regression_entries, list) or [row.get("n") for row in regression_entries] != list(SMALL_FIXTURES):
        raise AssertionError("regression fixture panel mismatch")
    small_primes = odd_only_prime_table(math.isqrt(max(SMALL_FIXTURES)))
    for fixture in regression_entries:
        n = fixture["n"]
        pairs = independent_active_pairs(n)
        rows = fixture.get("records")
        if fixture.get("purpose") != "SCHEMA_REGRESSION_ONLY" or not isinstance(rows, list) or len(rows) != len(pairs):
            raise AssertionError("regression fixture purpose or record count mismatch")
        multiplicity = Counter(shift for _, _, shift in pairs)
        for record, pair in zip(rows, pairs, strict=True):
            verify_one_record(record, n, pair, multiplicity, small_primes, "SCHEMA_REGRESSION_ONLY")
        winners = sum(row["status"] == "WINNER" for row in rows)
        zero_count = sum(row["remainder"] == 0 for row in rows)
        if winners != 1 or fixture.get("winner_count") != winners or fixture.get("contains_remainder_zero") != bool(zero_count):
            raise AssertionError("regression winner/zero result mismatch")
        regression_report.append({"n": n, "purpose": "SCHEMA_REGRESSION_ONLY", "active_pair_count": len(rows), "winner_count": winners, "remainder_zero_record_count": zero_count, "status": "PASS"})

    metadata = load_json(dossier / "metadata.json")
    artifact_names = ("panel.json", "records.jsonl", "per_n_summary.json", "prime_frequency.csv", "top_k_coverage.csv", "low_vs_control.json", "n0_surviving_pairs.json")
    actual_artifact_hashes = {name: digest(dossier / name) for name in artifact_names}
    if metadata.get("artifact_sha256") != actual_artifact_hashes:
        raise AssertionError("metadata artifact hashes mismatch")
    if (
        metadata.get("starting_commit") != STARTING_COMMIT
        or metadata.get("generator", {}).get("sha256") != digest(repo / "src/generate_obstruction_dossier.py")
        or metadata.get("independent_verifier", {}).get("sha256") != digest(Path(__file__))
    ):
        raise AssertionError("metadata source provenance mismatch")
    baseline_now = current_hashes(repo, BASELINES)
    pilot_now = {str(Path("output/tn_pilot_20260713") / rel): digest(input_root / rel) for rel in PILOT_RELATIVE_FILES}
    if metadata.get("baseline_integrity", {}).get("before_generation") != baseline_now or metadata.get("baseline_integrity", {}).get("after_generation") != baseline_now:
        raise AssertionError("baseline hash drift")
    if metadata.get("pilot_input_integrity", {}).get("before_generation") != pilot_now or metadata.get("pilot_input_integrity", {}).get("after_generation") != pilot_now:
        raise AssertionError("pilot input hash drift")

    losing_total = sum(row["losing_exponent_pair_count"] for row in summaries)
    winner_total = sum(row["winner_count"] for row in summaries)
    factor_count = sum(len(row["complete_factorization"]) for row in records)
    report = {
        "schema": "a303656-selected-obstruction-verification-report-v1",
        "status": "PASS",
        "verified_utc": args.verified_utc,
        "classification": "INDEPENDENTLY VERIFIED EXACT FINITE COMPUTATION ON FIXED SELECTED FIXTURES",
        "final_conclusion": "VALIDATED SELECTED OBSTRUCTION DOSSIER",
        "starting_commit": STARTING_COMMIT,
        "verifier": {
            "path": "src/verify_obstruction_dossier.py",
            "sha256": digest(Path(__file__)),
            "implementation_id": "selected_obstruction_independent_verifier_v1",
            "imports_generator": False,
            "factorization_method": "independent odd-index sieve plus complete trial division",
            "primality_method": "deterministic Miller-Rabin bases 2,3,5,7,11,13,17 below 341550071728321",
        },
        "checked_research_n_count": len(order),
        "checked_record_count": len(records),
        "checked_winner_count": winner_total,
        "checked_loser_count": losing_total,
        "checked_reported_prime_factor_count": factor_count,
        "checks": {
            "fixed_low_tail_panel": True,
            "mechanical_control_selection": True,
            "control_duplicate_reporting": True,
            "active_exponent_pair_completeness": True,
            "each_active_pair_exactly_once": True,
            "shift_and_remainder": True,
            "complete_factor_product": True,
            "deterministic_factor_primality": True,
            "obstruction_prime_modulo_4": True,
            "obstruction_valuation_parity": True,
            "independent_fermat_classification": True,
            "winner_equation": True,
            "canonical_witness": True,
            "winner_count_equals_validated_T": True,
            "duplicate_shift_multiplicity_and_consistency": True,
            "concentration_summaries": True,
            "low_vs_control_comparisons": True,
            "n0_residue_table": True,
            "baseline_byte_integrity": True,
            "pilot_input_byte_integrity": True,
            "no_CRT_or_broad_search_claim": True,
        },
        "regression_fixtures": regression_report,
        "artifact_sha256_at_verification": actual_artifact_hashes,
        "baseline_sha256_at_verification": baseline_now,
        "pilot_input_sha256_at_verification": pilot_now,
        "unresolved_risks": [
            "The observations concern only ten fixed PILOT-B fixtures and have no global statistical significance.",
            "The global A303656 mathematical problem remains UNRESOLVED.",
        ],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"INDEPENDENT_DOSSIER_VERIFICATION_PASS panel={len(order)} records={len(records)} winners={winner_total} losers={losing_total}")
    print("VALIDATED SELECTED OBSTRUCTION DOSSIER")
    return 0


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("self-test")
    run = commands.add_parser("run")
    run.add_argument("--repo-root", type=Path, default=Path("."))
    run.add_argument("--input-root", type=Path, default=Path("output/tn_pilot_20260713"))
    run.add_argument("--dossier-dir", type=Path, default=Path("analysis/obstruction_dossier"))
    run.add_argument("--report", type=Path, default=Path("analysis/obstruction_dossier/verification_report.json"))
    run.add_argument("--verified-utc", required=True)
    run.add_argument("--overwrite-report", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = arguments()
    return self_test() if args.command == "self-test" else verify(args)


if __name__ == "__main__":
    raise SystemExit(main())
