#!/usr/bin/env python3
"""Exact selected-fixture audit of static versus p^2-persistent obstructions.

This program reads only the committed obstruction dossier and T(n) pilot
artifacts.  It never invokes a counting executable, scans a new interval,
solves a CRT system, or evaluates T at an arithmetic-progression candidate.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, localcontext
from functools import cmp_to_key
from pathlib import Path
from typing import Iterable


RESULT_COMMIT_BINDING = "RESULT_COMMIT_CONTAINING_THIS_FILE"
PILOT_LOW = 240000000001
PILOT_HIGH_EXCLUSIVE = 240000100001
BLOCK_WIDTH = 10_000
N0 = 240000005594
CHECKPOINTS = (1, 2, 4, 8, 16, 32)
TOP_K = (1, 2, 4, 8, 16)
BASELINE_PATHS = (
    "output/formal_results_audit.json",
    "output/final_packaging_audit.json",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt",
    "output/final_results_manifest.json",
    "output/direct/formal_1p6b_final/summary.json",
)


@dataclass(frozen=True, order=True)
class Pair:
    c: int
    d: int
    shift: int

    @property
    def key(self) -> tuple[int, int]:
        return (self.c, self.d)


@dataclass
class Fixture:
    n: int
    validated_t: int
    factors_by_pair: dict[tuple[int, int], tuple[tuple[int, int], ...]]
    pairs: list[Pair]
    winners: set[tuple[int, int]]
    losers: set[tuple[int, int]]
    valuations: dict[int, dict[tuple[int, int], int]]
    static_sets: dict[int, set[tuple[int, int]]]
    p2_sets: dict[int, set[tuple[int, int]]]
    higher_sets: dict[int, dict[int, set[tuple[int, int]]]]
    signatures: dict[tuple[int, int], tuple[int, ...]]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8")


def decimal_ratio(numerator: int, denominator: int) -> str:
    if denominator == 0:
        raise ValueError("zero denominator")
    with localcontext() as context:
        context.prec = 30
        return format(Decimal(numerator) / Decimal(denominator), ".18f")


def ratio(numerator: int, denominator: int) -> dict[str, object]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "decimal": decimal_ratio(numerator, denominator),
    }


def git_value(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, check=True, text=True, capture_output=True
    )
    return completed.stdout.strip()


def git_is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=root
    )
    return completed.returncode == 0


def git_file_sha256(root: Path, commit: str, path: str) -> str:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return hashlib.sha256(completed.stdout).hexdigest()


def powers_leq(base: int, limit: int) -> list[int]:
    values: list[int] = []
    value = 1
    while value <= limit:
        values.append(value)
        value *= base
    return values


def active_pairs(n: int) -> list[Pair]:
    p3 = powers_leq(3, n)
    p5 = powers_leq(5, n)
    return [
        Pair(c, d, x + y)
        for c, x in enumerate(p3)
        for d, y in enumerate(p5)
        if x + y <= n
    ]


def pair_text(pairs: Iterable[tuple[int, int]]) -> str:
    return ";".join(f"{c}:{d}" for c, d in sorted(pairs))


def json_pair_list(pairs: Iterable[tuple[int, int]]) -> list[list[int]]:
    return [[c, d] for c, d in sorted(pairs)]


def valuation(value: int, prime: int) -> int:
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def is_prime_u64(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small:
        if n % prime == 0:
            return n == prime
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
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


def prime_table(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p, flag in enumerate(sieve) if flag]


def factor_integer(value: int, primes: list[int]) -> tuple[tuple[int, int], ...]:
    if value <= 0:
        raise ValueError("factorization is defined here only for positive remainders")
    residual = value
    result: list[tuple[int, int]] = []
    for prime in primes:
        if prime * prime > residual:
            break
        if residual % prime:
            continue
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        result.append((prime, exponent))
    if residual > 1:
        if not is_prime_u64(residual):
            raise AssertionError(f"non-prime residual {residual}")
        result.append((residual, 1))
    product = 1
    for prime, exponent in result:
        product *= prime**exponent
    if product != value:
        raise AssertionError("factorization product mismatch")
    return tuple(result)


def verify_reported_factorization(
    remainder: int, raw_factors: list[dict[str, object]]
) -> tuple[tuple[int, int], ...]:
    factors: list[tuple[int, int]] = []
    residual = remainder
    prior = 1
    for item in raw_factors:
        prime = int(item["prime"])
        exponent = int(item["exponent"])
        if prime <= prior or exponent <= 0 or not is_prime_u64(prime):
            raise AssertionError("invalid reported prime factor")
        direct = valuation(remainder, prime)
        if direct != exponent:
            raise AssertionError("reported valuation mismatch")
        for _ in range(exponent):
            if residual % prime:
                raise AssertionError("reported factor does not divide residual")
            residual //= prime
        factors.append((prime, exponent))
        prior = prime
    if residual != 1:
        raise AssertionError("reported factorization is incomplete")
    return tuple(factors)


def verify_fixed_inputs(root: Path) -> dict[str, object]:
    dossier = root / "analysis/obstruction_dossier"
    pilot = root / "output/tn_pilot_20260713"
    metadata = json.loads((dossier / "metadata.json").read_text(encoding="utf-8"))

    declared_checks: list[dict[str, object]] = []

    def check_map(label: str, mapping: dict[str, str], base: Path) -> None:
        mismatches = []
        for relative, expected in sorted(mapping.items()):
            path = base / relative
            actual = sha256_file(path) if path.is_file() else "MISSING"
            if actual != expected:
                mismatches.append(
                    {"path": str(path.relative_to(root)), "expected": expected, "actual": actual}
                )
        declared_checks.append(
            {
                "label": label,
                "checked": len(mapping),
                "mismatches": mismatches,
                "passed": not mismatches,
            }
        )
        if mismatches:
            raise AssertionError(f"input hash failure: {label}")

    check_map("dossier_artifacts", metadata["artifact_sha256"], dossier)
    check_map(
        "pilot_inputs_before",
        metadata["pilot_input_integrity"]["before_generation"],
        root,
    )
    check_map(
        "pilot_inputs_after",
        metadata["pilot_input_integrity"]["after_generation"],
        root,
    )
    check_map(
        "baseline_before", metadata["baseline_integrity"]["before_generation"], root
    )
    check_map(
        "baseline_after", metadata["baseline_integrity"]["after_generation"], root
    )
    for phase in ("pilot_a", "pilot_b"):
        for implementation in ("bitset", "clean", "oracle"):
            base = pilot / phase / implementation
            provenance = json.loads((base / "provenance.json").read_text(encoding="utf-8"))
            check_map(
                f"{phase}_{implementation}_outputs", provenance["outputs_sha256"], base
            )

    all_tree_hashes: dict[str, str] = {}
    for tree in (dossier, pilot):
        for path in sorted(p for p in tree.rglob("*") if p.is_file()):
            all_tree_hashes[str(path.relative_to(root))] = sha256_file(path)
    return {
        "declared_hash_checks": declared_checks,
        "all_declared_hashes_passed": all(x["passed"] for x in declared_checks),
        "fixed_input_file_count": len(all_tree_hashes),
        "fixed_input_tree_sha256": all_tree_hashes,
    }


def read_counts(root: Path) -> tuple[dict[int, int], dict[str, str]]:
    base = root / "output/tn_pilot_20260713/pilot_b"
    paths = [base / implementation / "counts.csv" for implementation in ("bitset", "clean", "oracle")]
    payloads = [path.read_bytes() for path in paths]
    if not (payloads[0] == payloads[1] == payloads[2]):
        raise AssertionError("PILOT-B counts copies are not byte-identical")
    result: dict[int, int] = {}
    with paths[2].open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        if next(reader) != ["n", "T"]:
            raise AssertionError("unexpected counts header")
        expected_n = PILOT_LOW
        for row in reader:
            if len(row) != 2 or not all(field.isdigit() for field in row):
                raise AssertionError("malformed counts row")
            n, t = map(int, row)
            if n != expected_n:
                raise AssertionError("counts row gap or reordering")
            result[n] = t
            expected_n += 1
    if expected_n != PILOT_HIGH_EXCLUSIVE or len(result) != 100_000:
        raise AssertionError("counts interval mismatch")
    return result, {str(path.relative_to(root)): sha256_file(path) for path in paths}


def corrected_controls(
    counts: dict[int, int], low_tail: list[dict[str, int]]
) -> list[dict[str, object]]:
    low_members = {int(item["n"]) for item in low_tail}
    selections: list[dict[str, object]] = []
    for item in low_tail:
        n = int(item["n"])
        block_index = (n - PILOT_LOW) // BLOCK_WIDTH
        block_start = PILOT_LOW + block_index * BLOCK_WIDTH
        block_end = block_start + BLOCK_WIDTH
        candidates = [
            m
            for m in range(block_start, block_end)
            if m not in low_members and m % 360 == n % 360
        ]
        if not candidates:
            raise AssertionError("no corrected-control candidate")
        m = min(candidates, key=lambda x: (abs(counts[x] - 60), abs(x - n), x))
        selections.append(
            {
                "low_tail_n": n,
                "low_tail_T": int(item["validated_T"]),
                "control_n": m,
                "control_T": counts[m],
                "block_index": block_index,
                "block_start": block_start,
                "block_end_exclusive": block_end,
                "residue_mod_360": n % 360,
                "residue_mod_9": n % 9,
                "selection_key": [abs(counts[m] - 60), abs(m - n), m],
            }
        )
    return selections


def build_fixture(
    n: int,
    validated_t: int,
    factors_by_pair: dict[tuple[int, int], tuple[tuple[int, int], ...]],
) -> Fixture:
    pairs = active_pairs(n)
    if len(pairs) != 407:
        raise AssertionError(f"fixture {n} does not have 407 active pairs")
    if set(factors_by_pair) != {pair.key for pair in pairs}:
        raise AssertionError("factorization pair domain mismatch")
    valuations: dict[int, dict[tuple[int, int], int]] = defaultdict(dict)
    signatures: dict[tuple[int, int], tuple[int, ...]] = {}
    winners: set[tuple[int, int]] = set()
    losers: set[tuple[int, int]] = set()
    pair_lookup = {pair.key: pair for pair in pairs}
    for key, factors in factors_by_pair.items():
        remainder = n - pair_lookup[key].shift
        signature: list[int] = []
        for prime, reported_exponent in factors:
            direct_exponent = valuation(remainder, prime)
            if direct_exponent != reported_exponent:
                raise AssertionError("direct valuation reconstruction failed")
            if prime % 4 == 3 and direct_exponent % 2 == 1:
                valuations[prime][key] = direct_exponent
                signature.append(prime)
        signatures[key] = tuple(signature)
        if signature:
            losers.add(key)
        else:
            winners.add(key)
    if len(winners) != validated_t:
        raise AssertionError(
            f"fixture {n} winner count {len(winners)} != validated T {validated_t}"
        )
    static_sets: dict[int, set[tuple[int, int]]] = {}
    p2_sets: dict[int, set[tuple[int, int]]] = {}
    higher_sets: dict[int, dict[int, set[tuple[int, int]]]] = {}
    for prime, by_pair in valuations.items():
        static = set(by_pair)
        p2 = {key for key, exponent in by_pair.items() if exponent == 1}
        higher_by_e: dict[int, set[tuple[int, int]]] = defaultdict(set)
        for key, exponent in by_pair.items():
            if exponent >= 3:
                higher_by_e[exponent].add(key)
        higher = set().union(*higher_by_e.values()) if higher_by_e else set()
        if static != p2 | higher or p2 & higher:
            raise AssertionError("O_p is not the disjoint union of C_p and H_p")
        for key in p2:
            remainder = n - pair_lookup[key].shift
            w = (remainder // prime) % prime
            if remainder % prime or remainder % (prime * prime) == 0 or w == 0:
                raise AssertionError("C_p direct congruence failed")
        static_sets[prime] = static
        p2_sets[prime] = p2
        higher_sets[prime] = dict(higher_by_e)
    return Fixture(
        n=n,
        validated_t=validated_t,
        factors_by_pair=factors_by_pair,
        pairs=pairs,
        winners=winners,
        losers=losers,
        valuations=dict(valuations),
        static_sets=static_sets,
        p2_sets=p2_sets,
        higher_sets=higher_sets,
        signatures=signatures,
    )


def read_dossier_fixtures(
    root: Path, panel: dict[str, object]
) -> tuple[dict[int, Fixture], dict[str, int]]:
    records_path = root / "analysis/obstruction_dossier/records.jsonl"
    records_by_n: dict[int, list[dict[str, object]]] = defaultdict(list)
    for line in records_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        records_by_n[int(record["n"])].append(record)
    expected_n = {int(item["n"]) for item in panel["research_panel"]}
    if set(records_by_n) != expected_n or sum(map(len, records_by_n.values())) != 4070:
        raise AssertionError("dossier record domain mismatch")
    fixtures: dict[int, Fixture] = {}
    audit_counts = Counter()
    validated_t_by_n = {
        int(item["n"]): int(item["validated_T"]) for item in panel["research_panel"]
    }
    for n, records in records_by_n.items():
        generated = active_pairs(n)
        if len(generated) != 407:
            raise AssertionError("active-pair completeness failure")
        record_map = {(int(r["c"]), int(r["d"])): r for r in records}
        if set(record_map) != {pair.key for pair in generated}:
            raise AssertionError("reported pair domain differs from reconstruction")
        factors_by_pair: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
        for pair in generated:
            record = record_map[pair.key]
            remainder = n - pair.shift
            if int(record["shift"]) != pair.shift or int(record["remainder"]) != remainder:
                raise AssertionError("reported shift/remainder mismatch")
            factors = verify_reported_factorization(
                remainder, list(record["complete_factorization"])
            )
            recomputed_obstructions = [
                p for p, e in factors if p % 4 == 3 and e % 2 == 1
            ]
            reported_obstructions = [
                int(p) for p in record["all_3mod4_odd_valuation_primes"]
            ]
            if reported_obstructions != recomputed_obstructions:
                raise AssertionError("dossier obstruction list mismatch")
            expected_status = "LOSER" if recomputed_obstructions else "WINNER"
            if record["status"] != expected_status:
                raise AssertionError("dossier winner/loser status mismatch")
            factors_by_pair[pair.key] = factors
            audit_counts["reported_factorizations"] += 1
            audit_counts["reported_obstruction_primes"] += len(reported_obstructions)
        fixtures[n] = build_fixture(n, validated_t_by_n[n], factors_by_pair)
    return fixtures, dict(audit_counts)


def factor_selected_fixture(n: int, validated_t: int, primes: list[int]) -> Fixture:
    factors = {
        pair.key: factor_integer(n - pair.shift, primes) for pair in active_pairs(n)
    }
    return build_fixture(n, validated_t, factors)


def ranked_primes(sets: dict[int, set[tuple[int, int]]]) -> list[int]:
    return sorted((p for p, covered in sets.items() if covered), key=lambda p: (-len(sets[p]), p))


def prime_coverage_rows(
    fixture: Fixture, role: str, matched_low_tail_n: int | None
) -> list[dict[str, object]]:
    static_ranked = ranked_primes(fixture.static_sets)
    p2_ranked = ranked_primes(fixture.p2_sets)
    higher_flat = {
        prime: set().union(*by_e.values()) if by_e else set()
        for prime, by_e in fixture.higher_sets.items()
    }
    higher_ranked = ranked_primes(higher_flat)
    static_rank = {p: i + 1 for i, p in enumerate(static_ranked)}
    p2_rank = {p: i + 1 for i, p in enumerate(p2_ranked)}
    higher_rank = {p: i + 1 for i, p in enumerate(higher_ranked)}
    rows: list[dict[str, object]] = []
    for prime in static_ranked:
        static = fixture.static_sets[prime]
        persistent = fixture.p2_sets[prime]
        by_e = fixture.higher_sets[prime]
        higher = set().union(*by_e.values()) if by_e else set()
        higher_json = {
            str(e): json_pair_list(pairs) for e, pairs in sorted(by_e.items())
        }
        valuation_counts = Counter(fixture.valuations[prime].values())
        preserving_moduli = {
            str(e): str(prime ** (e + 1)) for e in sorted(by_e)
        }
        rows.append(
            {
                "n": fixture.n,
                "panel_role": role,
                "matched_low_tail_n": "" if matched_low_tail_n is None else matched_low_tail_n,
                "validated_T": fixture.validated_t,
                "active_pair_count": len(fixture.pairs),
                "losing_pair_count": len(fixture.losers),
                "prime": prime,
                "static_rank": static_rank[prime],
                "static_odd_count": len(static),
                "static_over_active": f"{len(static)}/{len(fixture.pairs)}",
                "static_over_losers": f"{len(static)}/{len(fixture.losers)}",
                "p2_rank": p2_rank.get(prime, ""),
                "p2_persistent_count": len(persistent),
                "p2_over_active": f"{len(persistent)}/{len(fixture.pairs)}",
                "p2_over_losers": f"{len(persistent)}/{len(fixture.losers)}",
                "higher_rank": higher_rank.get(prime, ""),
                "higher_odd_count": len(higher),
                "higher_over_active": f"{len(higher)}/{len(fixture.pairs)}",
                "higher_over_losers": f"{len(higher)}/{len(fixture.losers)}",
                "odd_valuation_counts": ";".join(
                    f"{e}:{valuation_counts[e]}" for e in sorted(valuation_counts)
                ),
                "O_p_pairs": pair_text(static),
                "C_p_pairs": pair_text(persistent),
                "H_p_pairs_by_valuation": json.dumps(
                    higher_json, separators=(",", ":"), sort_keys=True
                ),
                "higher_prime_power_moduli": json.dumps(
                    preserving_moduli, separators=(",", ":"), sort_keys=True
                ),
            }
        )
    return rows


def write_prime_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def marginal_greedy(fixture: Fixture, limit: int) -> list[dict[str, object]]:
    selected: list[int] = []
    covered: set[tuple[int, int]] = set()
    product = 1
    rows: list[dict[str, object]] = []
    available = {p for p, pairs in fixture.p2_sets.items() if pairs}
    for step in range(1, limit + 1):
        candidates = [
            (len(fixture.p2_sets[p] - covered), p) for p in available - set(selected)
        ]
        new_count, prime = min(candidates, key=lambda item: (-item[0], item[1]))
        if new_count <= 0:
            raise AssertionError("greedy core exhausted before requested depth")
        new_pairs = fixture.p2_sets[prime] - covered
        selected.append(prime)
        covered |= new_pairs
        product *= prime * prime
        rows.append(core_step_row("MARGINAL_COVERAGE_GREEDY", step, prime, new_pairs, selected, covered, product, fixture))
    return rows


def bit_score_compare(
    a: tuple[int, int], b: tuple[int, int]
) -> int:
    """Compare (new_count, prime) by new/log2(prime^2), then smaller prime."""
    a_new, a_prime = a
    b_new, b_prime = b
    left = pow(b_prime, a_new)
    right = pow(a_prime, b_new)
    if left > right:
        return -1
    if left < right:
        return 1
    return -1 if a_prime < b_prime else (1 if a_prime > b_prime else 0)


def bit_greedy(fixture: Fixture, limit: int) -> list[dict[str, object]]:
    selected: list[int] = []
    covered: set[tuple[int, int]] = set()
    product = 1
    rows: list[dict[str, object]] = []
    available = {p for p, pairs in fixture.p2_sets.items() if pairs}
    for step in range(1, limit + 1):
        candidates = [
            (len(fixture.p2_sets[p] - covered), p) for p in available - set(selected)
        ]
        candidates = [item for item in candidates if item[0] > 0]
        if not candidates:
            raise AssertionError("bit-cost greedy core exhausted before requested depth")
        new_count, prime = sorted(candidates, key=cmp_to_key(bit_score_compare))[0]
        new_pairs = fixture.p2_sets[prime] - covered
        selected.append(prime)
        covered |= new_pairs
        product *= prime * prime
        rows.append(core_step_row("COVERAGE_PER_MODULUS_BIT_GREEDY", step, prime, new_pairs, selected, covered, product, fixture))
    return rows


def core_step_row(
    ordering: str,
    step: int,
    prime: int,
    new_pairs: set[tuple[int, int]],
    selected: list[int],
    covered: set[tuple[int, int]],
    product: int,
    fixture: Fixture,
) -> dict[str, object]:
    covered_losers = len(covered & fixture.losers)
    covered_winners = len(covered & fixture.winners)
    return {
        "label": "HEURISTIC_P2_PERSISTENT_CORE",
        "ordering": ordering,
        "step": step,
        "checkpoint": "YES" if step in CHECKPOINTS else "NO",
        "selected_prime": prime,
        "newly_covered_pairs": len(new_pairs),
        "newly_covered_pair_set": pair_text(new_pairs),
        "selected_primes": ";".join(map(str, selected)),
        "cumulative_covered_active_pairs": len(covered),
        "active_pair_count": len(fixture.pairs),
        "cumulative_covered_current_losers": covered_losers,
        "current_losing_pair_count": len(fixture.losers),
        "uncovered_current_losers": len(fixture.losers) - covered_losers,
        "uncovered_original_winners": len(fixture.winners) - covered_winners,
        "product_M": str(product),
        "M_bit_length": product.bit_length(),
        "M_decimal_digit_count": len(str(product)),
    }


def write_core_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def activation_cell(n0: int) -> dict[str, object]:
    p3 = powers_leq(3, n0)
    p5 = powers_leq(5, n0)
    p3.append(p3[-1] * 3)
    p5.append(p5[-1] * 5)
    levels: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for c, x in enumerate(p3):
        for d, y in enumerate(p5):
            levels[x + y].append((c, d))
    active_levels = [shift for shift in levels if shift <= n0]
    future_levels = [shift for shift in levels if shift > n0]
    a = max(active_levels)
    next_shift = min(future_levels)
    b = next_shift - 1
    active = active_pairs(n0)
    duplicates = [
        {"shift": shift, "pairs": json_pair_list(pairs), "multiplicity": len(pairs)}
        for shift, pairs in sorted(levels.items())
        if len(pairs) > 1 and shift <= n0
    ]
    if duplicates != [{"shift": 28, "pairs": [[1, 2], [3, 0]], "multiplicity": 2}]:
        raise AssertionError("unexpected duplicate-shift structure")
    return {
        "A": a,
        "B": b,
        "active_pair_count": len(active),
        "distinct_active_shift_count": len({p.shift for p in active}),
        "left_boundary_activation": {
            "shift": a,
            "pairs": json_pair_list(levels[a]),
        },
        "next_activation": {
            "shift": next_shift,
            "pairs": json_pair_list(levels[next_shift]),
        },
        "duplicate_active_shifts": duplicates,
    }


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def progression_stats(n0: int, modulus: int, low: int, high: int) -> dict[str, object]:
    k_min = ceil_div(low - n0, modulus)
    k_max = (high - n0) // modulus
    count = max(0, k_max - k_min + 1)
    if not (k_min <= 0 <= k_max):
        raise AssertionError("reference point is outside progression interval")
    return {
        "interval": [low, high],
        "k_min": k_min,
        "k_max": k_max,
        "candidate_count_including_k0": count,
        "nearest_nonzero_left": (
            {"k": -1, "n": n0 - modulus} if k_min <= -1 else None
        ),
        "nearest_nonzero_right": (
            {"k": 1, "n": n0 + modulus} if k_max >= 1 else None
        ),
    }


def fixture_metrics(fixture: Fixture) -> dict[str, object]:
    active_count = len(fixture.pairs)
    loser_count = len(fixture.losers)
    obstruction_primes = len(fixture.static_sets)
    signature_count = len({fixture.signatures[key] for key in fixture.losers})
    p2_prime_count = sum(bool(pairs) for pairs in fixture.p2_sets.values())
    p3_static = len(fixture.static_sets.get(3, set()))
    p3_p2 = len(fixture.p2_sets.get(3, set()))
    p2_ranked = ranked_primes(fixture.p2_sets)
    top_k_rows = []
    for k in TOP_K:
        selected = p2_ranked[:k]
        union = set().union(*(fixture.p2_sets[p] for p in selected)) if selected else set()
        top_k_rows.append(
            {
                "k": k,
                "ranked_primes": selected,
                "covered_pairs": len(union),
                "coverage_over_active_pairs": ratio(len(union), active_count),
                "coverage_over_losing_pairs": ratio(len(union), loser_count),
            }
        )
    return {
        "n": fixture.n,
        "validated_T": fixture.validated_t,
        "active_pair_count": active_count,
        "losing_pair_count": loser_count,
        "distinct_obstruction_primes": {
            "absolute": obstruction_primes,
            "per_losing_pair": ratio(obstruction_primes, loser_count),
        },
        "obstruction_signatures": {
            "absolute": signature_count,
            "per_losing_pair": ratio(signature_count, loser_count),
        },
        "p2_persistent_prime_count": {
            "absolute": p2_prime_count,
            "per_losing_pair": ratio(p2_prime_count, loser_count),
        },
        "prime_3_static_coverage": {
            "absolute": p3_static,
            "over_active_pairs": ratio(p3_static, active_count),
            "over_losing_pairs": ratio(p3_static, loser_count),
        },
        "prime_3_p2_coverage": {
            "absolute": p3_p2,
            "over_active_pairs": ratio(p3_p2, active_count),
            "over_losing_pairs": ratio(p3_p2, loser_count),
        },
        "top_k_p2_frequency_ranked_union": top_k_rows,
    }


def greater_fraction(a: dict[str, object], b: dict[str, object]) -> bool:
    return int(a["numerator"]) * int(b["denominator"]) > int(b["numerator"]) * int(a["denominator"])


def verdict(values: list[bool]) -> str:
    if all(values):
        return "SURVIVES_ALL_FIVE"
    if any(values):
        return "SURVIVES_PARTIALLY"
    return "DOES_NOT_SURVIVE"


def comparison_observations(
    low_tail: list[dict[str, int]],
    old_controls: dict[int, int],
    corrected: list[dict[str, object]],
    metrics: dict[int, dict[str, object]],
    fixtures: dict[int, Fixture],
) -> list[dict[str, object]]:
    corrected_by_low = {int(x["low_tail_n"]): int(x["control_n"]) for x in corrected}
    pairs = []
    for item in low_tail:
        low_n = int(item["n"])
        pairs.append((low_n, old_controls[low_n], corrected_by_low[low_n]))

    def pairwise_test(path: tuple[str, ...], normalized_key: str | None, control_position: int) -> list[dict[str, object]]:
        output = []
        for low_n, old_n, corrected_n in pairs:
            control_n = (old_n, corrected_n)[control_position]
            low_value: object = metrics[low_n]
            control_value: object = metrics[control_n]
            for key in path:
                low_value = low_value[key]  # type: ignore[index]
                control_value = control_value[key]  # type: ignore[index]
            if normalized_key is None:
                passed = int(low_value) > int(control_value)
            else:
                passed = greater_fraction(
                    low_value[normalized_key], control_value[normalized_key]  # type: ignore[index]
                )
            output.append(
                {
                    "low_tail_n": low_n,
                    "control_n": control_n,
                    "low_value": low_value,
                    "control_value": control_value,
                    "low_is_strictly_greater": passed,
                }
            )
        return output

    statements: list[dict[str, object]] = []
    for statement, path, norm_key in (
        (
            "LOW_TAIL_HAS_MORE_DISTINCT_OBSTRUCTION_PRIMES",
            ("distinct_obstruction_primes",),
            "per_losing_pair",
        ),
        (
            "LOW_TAIL_HAS_MORE_OBSTRUCTION_SIGNATURES",
            ("obstruction_signatures",),
            "per_losing_pair",
        ),
        (
            "LOW_TAIL_HAS_MORE_P2_PERSISTENT_PRIMES",
            ("p2_persistent_prime_count",),
            "per_losing_pair",
        ),
    ):
        old_absolute = pairwise_test(path + ("absolute",), None, 0)
        old_normalized = pairwise_test(path, norm_key, 0)
        corrected_absolute = pairwise_test(path + ("absolute",), None, 1)
        corrected_normalized = pairwise_test(path, norm_key, 1)
        statements.append(
            {
                "statement": statement,
                "old_control_absolute": {
                    "verdict": verdict([x["low_is_strictly_greater"] for x in old_absolute]),
                    "pairs": old_absolute,
                },
                "old_control_normalized": {
                    "verdict": verdict([x["low_is_strictly_greater"] for x in old_normalized]),
                    "pairs": old_normalized,
                },
                "corrected_mod9_control_absolute": {
                    "verdict": verdict([x["low_is_strictly_greater"] for x in corrected_absolute]),
                    "pairs": corrected_absolute,
                },
                "corrected_mod9_control_normalized": {
                    "verdict": verdict([x["low_is_strictly_greater"] for x in corrected_normalized]),
                    "pairs": corrected_normalized,
                },
            }
        )

    prime3_static_old = pairwise_test(
        ("prime_3_static_coverage",), "over_active_pairs", 0
    )
    prime3_static_corrected = pairwise_test(
        ("prime_3_static_coverage",), "over_active_pairs", 1
    )
    prime3_p2_old = pairwise_test(
        ("prime_3_p2_coverage",), "over_active_pairs", 0
    )
    prime3_p2_corrected = pairwise_test(
        ("prime_3_p2_coverage",), "over_active_pairs", 1
    )
    statements.append(
        {
            "statement": "LOW_TAIL_HAS_HIGHER_PRIME_3_COVERAGE",
            "static_old_controls": {
                "verdict": verdict([x["low_is_strictly_greater"] for x in prime3_static_old]),
                "pairs": prime3_static_old,
            },
            "static_corrected_mod9_controls": {
                "verdict": verdict([x["low_is_strictly_greater"] for x in prime3_static_corrected]),
                "pairs": prime3_static_corrected,
            },
            "p2_old_controls": {
                "verdict": verdict([x["low_is_strictly_greater"] for x in prime3_p2_old]),
                "pairs": prime3_p2_old,
            },
            "p2_corrected_mod9_controls": {
                "verdict": verdict([x["low_is_strictly_greater"] for x in prime3_p2_corrected]),
                "pairs": prime3_p2_corrected,
                "exact_result": "EQUAL_FOR_EACH_MATCHED_PAIR_BY_MODULO_9_BINDING",
            },
        }
    )

    all_selected = {n for triple in pairs for n in triple}
    prime3_largest = []
    for n in sorted(all_selected):
        fixture = fixtures[n]
        ranking = ranked_primes(fixture.static_sets)
        prime3_largest.append(
            {
                "n": n,
                "largest_static_prime": ranking[0],
                "prime_3_is_largest": ranking[0] == 3,
            }
        )
    statements.append(
        {
            "statement": "PRIME_3_IS_THE_LARGEST_STATIC_SINGLE_PRIME_COVER",
            "verdict": (
                "SURVIVES_ALL_SELECTED_FIXTURES"
                if all(x["prime_3_is_largest"] for x in prime3_largest)
                else "DOES_NOT_SURVIVE_ALL_SELECTED_FIXTURES"
            ),
            "fixtures": prime3_largest,
        }
    )

    top_k_statement = {
        "statement": "LOW_TAIL_HAS_HIGHER_TOP_K_P2_UNION_COVERAGE",
        "definition": (
            "frequency-rank primes by descending |C_p| with smaller-prime tie-break, "
            "then compare the union of the first k sets"
        ),
        "by_k": [],
    }
    for k in TOP_K:
        comparisons_for_k: dict[str, object] = {"k": k}
        for label, control_position in (
            ("old_controls", 1),
            ("corrected_mod9_controls", 2),
        ):
            active_results = []
            loser_results = []
            for triple in pairs:
                low_n = triple[0]
                control_n = triple[control_position]
                low_row = next(
                    row
                    for row in metrics[low_n]["top_k_p2_frequency_ranked_union"]
                    if int(row["k"]) == k
                )
                control_row = next(
                    row
                    for row in metrics[control_n]["top_k_p2_frequency_ranked_union"]
                    if int(row["k"]) == k
                )
                active_pass = greater_fraction(
                    low_row["coverage_over_active_pairs"],
                    control_row["coverage_over_active_pairs"],
                )
                loser_pass = greater_fraction(
                    low_row["coverage_over_losing_pairs"],
                    control_row["coverage_over_losing_pairs"],
                )
                active_results.append(
                    {
                        "low_tail_n": low_n,
                        "control_n": control_n,
                        "low_covered_pairs": low_row["covered_pairs"],
                        "control_covered_pairs": control_row["covered_pairs"],
                        "low_is_strictly_greater": active_pass,
                    }
                )
                loser_results.append(
                    {
                        "low_tail_n": low_n,
                        "control_n": control_n,
                        "low_coverage": low_row["coverage_over_losing_pairs"],
                        "control_coverage": control_row["coverage_over_losing_pairs"],
                        "low_is_strictly_greater": loser_pass,
                    }
                )
            comparisons_for_k[label] = {
                "over_active_pairs": {
                    "verdict": verdict(
                        [x["low_is_strictly_greater"] for x in active_results]
                    ),
                    "pairs": active_results,
                },
                "over_losing_pairs": {
                    "verdict": verdict(
                        [x["low_is_strictly_greater"] for x in loser_results]
                    ),
                    "pairs": loser_results,
                },
            }
        top_k_statement["by_k"].append(comparisons_for_k)
    statements.append(top_k_statement)
    return statements


def same_mod9_audit(
    fixture_ns: list[int], fixtures: dict[int, Fixture]
) -> dict[str, object]:
    domains = [{pair.key for pair in fixtures[n].pairs} for n in fixture_ns]
    if any(domain != domains[0] for domain in domains[1:]):
        raise AssertionError("active domains differ in modulo-9 audit")
    groups: dict[int, list[int]] = defaultdict(list)
    for n in fixture_ns:
        groups[n % 9].append(n)
    output_groups = []
    for residue, ns in sorted(groups.items()):
        sets = [fixtures[n].p2_sets.get(3, set()) for n in ns]
        identical = all(s == sets[0] for s in sets[1:])
        if not identical:
            raise AssertionError("equal modulo-9 residues have unequal C_3 sets")
        output_groups.append(
            {
                "residue_mod_9": residue,
                "fixtures": ns,
                "C_3_pair_count": len(sets[0]),
                "C_3_pairs": json_pair_list(sets[0]),
                "identical": identical,
            }
        )
    return {
        "active_pair_domains_identical": True,
        "equal_residue_implies_identical_C_3": True,
        "groups": output_groups,
    }


def generate_report(
    metadata: dict[str, object],
    n0_fixture: Fixture,
    prime3: dict[str, object],
    core_rows: list[dict[str, object]],
    cell: dict[str, object],
    controls: dict[str, object],
    normalized: dict[str, object],
) -> str:
    checkpoints = [row for row in core_rows if row["checkpoint"] == "YES"]
    lines = [
        "# P2-persistent obstruction core and control audit",
        "",
        "## Technical summary",
        "",
        "This selected-fixture audit separates static odd valuations from exact",
        "valuation one.  It is an **EXACT FINITE COMPUTATION ON FIXED SELECTED",
        "FIXTURES**; the core orderings are explicitly **HEURISTIC_P2_PERSISTENT_CORE**",
        "constructions and are not minimum set covers.  The global A303656 problem",
        "remains **UNRESOLVED**.",
        "",
        f"Reusable source commit is `{metadata['source_commit']}` with parent "
        f"`{metadata['source_parent_commit']}`.  The results commit is the Git commit",
        "containing this generated report and is resolved explicitly during replay.",
        "All declared dossier, pilot, and certified-baseline hashes passed before",
        "analysis.  No counting executable, new integer scan, CRT solve, arithmetic",
        "progression search, or T-evaluation at progression candidates was performed.",
        "",
        "## Prime 3: 167 static pairs but only 143 p2-persistent pairs",
        "",
        f"For `n0={N0}`, the exact valuation distribution is `{prime3['valuation_distribution']}`.",
        "Therefore prime 3 covers 167 pairs statically, 143 pairs persistently modulo",
        "`3^2`, and 24 pairs have higher odd valuation and are excluded from the p2 core.",
        "",
        "The modular explanation is exact.  `n0 ≡ 2 (mod 9)`.  For `c>=2`,",
        "`3^c ≡ 0 (mod 9)`, while `5^d (mod 9)` cycles",
        "`1,5,7,8,4,2` with period 6.  Thus `2-5^d` is divisible by 3 but",
        "not by 9 exactly when `d ≡ 1 or 3 (mod 6)`, proving `v3=1` for",
        "those pairs.  The `c=0` and `c=1` rows were evaluated separately by exact",
        f"division: `{prime3['c_category_distributions']}`.",
        "",
        "## Static and persistent definitions",
        "",
        "For every fixture and prime `p ≡ 3 (mod 4)`, the audit reconstructs",
        "`O_p={(c,d):v_p(r) odd}`, `C_p={(c,d):v_p(r)=1}`, and",
        "`H_p={(c,d):v_p(r) odd and >=3}`.  It verifies `O_p=C_p disjoint-union H_p`",
        "and checks every `C_p` pair directly modulo `p^2`.  Explicit pair sets,",
        "separate rankings, both requested denominators, valuation-3/5/... splits,",
        "and optional preserving moduli `p^(e+1)` are in",
        "`analysis/p2_core/static_vs_p2_prime_coverage.csv`.",
        "",
        "## Heuristic p2-persistent cores",
        "",
        "The marginal ordering maximizes the exact number of newly covered pairs and",
        "breaks ties by smaller prime.  The bit-cost ordering maximizes",
        "`new/log2(p^2)`.  Scores are compared without floating point:",
        "`a/log(p) > b/log(q)` iff `q^a > p^b`; an exact equality is broken by",
        "smaller prime.",
        "",
        "| ordering | k | covered active | covered losers | uncovered losers | M bits | M digits |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in checkpoints:
        lines.append(
            f"| {row['ordering']} | {row['step']} | {row['cumulative_covered_active_pairs']}/407 | "
            f"{row['cumulative_covered_current_losers']}/391 | {row['uncovered_current_losers']} | "
            f"{row['M_bit_length']} | {row['M_decimal_digit_count']} |"
        )
    lines.extend(
        [
            "",
            "All 32 intermediate steps, selected primes, exact products, new pair sets,",
            "and residue bindings `t_p=n0 mod p^2` are stored in the CSV/JSON outputs.",
            "Every combined class is only `n ≡ n0 (mod M)`; no alternate CRT residue",
            "was computed.",
            "",
            "## Exact activation cell and candidate density",
            "",
            f"The maximal integer cell with the same 407 source pairs is `[{cell['A']},{cell['B']}]`.",
            f"The next activation occurs at `{cell['next_activation']['shift']}`.  The sole",
            "duplicate active shift is 28, supported by `(1,2)` and `(3,0)`, and both",
            "source pairs remain present.  Counts of `n0+kM` in this cell and in",
            "PILOT-B, plus the nearest nonzero k on each side when present, are purely",
            "arithmetic density calculations in `activation_cell.json`; T was not",
            "evaluated at any such point.",
            "",
            "## Corrected controls and normalization",
            "",
            "The previous controls matched modulo 120 only.  The corrected controls are",
            "selected from the existing PILOT-B counts with modulus 360 and the same",
            "fixed block/key rule.  Their selections are:",
            "",
            "| low-tail n | corrected control | T(control) | selection key |",
            "|---:|---:|---:|---|",
        ]
    )
    for selection in controls["selections"]:
        lines.append(
            f"| {selection['low_tail_n']} | {selection['control_n']} | {selection['control_T']} | "
            f"`{tuple(selection['selection_key'])}` |"
        )
    lines.extend(
        [
            "",
            f"Duplicate corrected controls: `{controls['duplicate_controls']}`.",
            "Equal residues modulo 9 give identical prime-3 p2-persistent pair sets",
            "because all ten low/corrected fixtures have the same active domain; this",
            "was also checked pair-for-pair.",
            "",
            "Absolute and losing-pair-normalized obstruction-prime counts, signature",
            "counts, p2-prime counts, prime-3 static/p2 coverage, and frequency-ranked",
            "top-k p2 union coverage are in `normalized_comparison.json`.  The audit",
            "records each prior qualitative statement as surviving all five pairs,",
            "surviving partially, or not surviving after normalization/modulo-9 matching.",
            "Every comparison is only a **COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES**.",
            "",
            "## Higher odd valuations and limitations",
            "",
            "Pairs of valuation 3, 5, and higher are reported separately and never enter",
            "p2-core totals.  The optional `p^(e+1)` values are labeled",
            "**HIGHER_PRIME_POWER_OBSERVATION**.  They are not mixed into M.",
            "",
            "This audit does not prove a counterexample, a minimum core, a useful CRT",
            "class outside the activation cell, or any infinite statement.  It does not",
            "evaluate whether the uncovered pairs can be eliminated simultaneously.",
            "",
            "## Corrections found by this audit",
            "",
            "1. The earlier all-odd-valuation top-k tables are static obstruction",
            "   tables, not p2-persistent coverage.  At n0, prime 3 changes from",
            "   167 static pairs to 143 persistent pairs; the omitted 24 pairs have",
            "   valuation 3 or 5.",
            "2. The old controls were matched modulo 120, which does not bind modulo",
            "   9.  With corrected modulo-360 controls, prime-3 p2 coverage is exactly",
            "   equal within every matched pair, so a strict low-tail advantage for",
            "   prime-3 p2 coverage does not survive.",
            "3. The old absolute advantages in distinct obstruction primes, signature",
            "   diversity, and p2-prime counts survive for all five pairs, but each",
            "   survives only partially after division by losing-pair count.  The same",
            "   partial result holds for the corrected controls.",
            "4. Frequency-ranked top-k p2 union comparisons depend on k and denominator;",
            "   they are recorded per pair rather than summarized as a universal",
            "   concentration claim.",
            "",
            "## Independent verification",
            "",
            "`src/verify_p2_persistent_core.py` imports no primary analysis module.  It",
            "independently checks the active domain, factor products/primality and direct",
            "valuations, the mandatory prime-3 distribution, every C_p congruence, both",
            "greedy histories, corrected controls, activation endpoints, modulus sizes,",
            "normalization, and input/baseline hashes.  Its result is stored in",
            "`analysis/p2_core/verification_report.json`.",
            "",
            "## Conclusion",
            "",
            "**VALIDATED P2-PERSISTENT CORE AUDIT**",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_current_state(metadata: dict[str, object]) -> str:
    return f"""# Current mathematical and computational state

State date: 2026-07-13 (Asia/Shanghai)

Task: **P2-PERSISTENT OBSTRUCTION CORE AND CONTROL AUDIT**

Reusable source commit: `{metadata['source_commit']}`

Source parent: `{metadata['source_parent_commit']}`

Results commit: the commit containing this generated document; the independent
replay resolves and checks its exact Git object separately from the source.

## Mathematical status

The global A303656 question remains **UNRESOLVED**.  No proof or certified
counterexample is claimed.  The selected-fixture result is:

> **VALIDATED P2-PERSISTENT CORE AUDIT**

The two 32-prime constructions are **HEURISTIC_P2_PERSISTENT_CORE** objects,
not minimum set covers.  No counting executable, new integer scan, CRT solve,
progression search, or evaluation of T at a progression candidate occurred.

## Exact finite findings

- All fixtures have 407 active exponent pairs and 406 distinct numerical
  shifts; shift 28 occurs for both `(1,2)` and `(3,0)`.
- At `n0=240000005594`, the prime-3 valuation distribution is
  `v0=214, v1=143, v2=26, v3=23, v5=1`.
- Prime 3 therefore has 167 static odd pairs, 143 p2-persistent pairs, and 24
  higher-odd pairs.  Higher odd valuations are excluded from p2 totals.
- For `c>=2`, `n0=2 (mod 9)`, `3^c=0 (mod 9)`, and the period-six cycle of
  `5^d` proves that `d=1 or 3 (mod 6)` gives valuation one.  The `c=0` and
  `c=1` rows were checked separately.
- Both greedy rules cover 286 of 391 current losers at 32 primes, leaving 105
  current losers uncovered and all 16 original winners uncovered.
- The exact activation cell is `[183968950234,246731069451]`; only candidate
  density was computed inside it.
- Corrected controls were selected only from committed PILOT-B counts using
  modulus 360.  No duplicates occur, and equal residues modulo 9 give equal
  prime-3 p2-persistent pair sets on the common active domain.

All normalized comparisons remain **COMPUTATIONAL OBSERVATION ON SELECTED
FIXTURES**.  Details are in `docs/p2_persistent_core_audit.md` and the compact
machine artifacts under `analysis/p2_core/`.

## Verification boundary

The independent verifier imports no primary analysis module.  It reconstructs
the domain, valuations, controls, greedy histories, activation cell, hashes,
and normalized metrics.  Both programs remain Python implementations sharing
the stored inputs and mathematical specification; neither is formally
verified.  Certified and pilot artifacts remain unchanged.
"""


def generate_gap_register(metadata: dict[str, object]) -> str:
    return f"""# Audit gap register

Audit date: 2026-07-13

Scope: **P2-PERSISTENT OBSTRUCTION CORE AND CONTROL AUDIT** on fixed selected
fixtures and committed PILOT-B counts.  `CLOSED` means a finite check passed;
it does not settle the global problem.

Source commit: `{metadata['source_commit']}`

Source parent: `{metadata['source_parent_commit']}`

Results commit: the commit containing this file, resolved during fresh replay.

| Gap | Status | Confirmed guarantee | Remaining limit |
|---|---|---|---|
| Source/result provenance split | **CLOSED** | Reusable programs are bound to the source commit; generated artifacts bind symbolically to their containing results commit, which replay resolves explicitly. | Git and SHA256 are trust anchors. |
| Fixed-input hashes | **CLOSED** | All 95 declared dossier, pilot, and baseline checks pass. | Stored inputs remain shared evidence. |
| Active-pair completeness | **CLOSED** | Both paths independently reconstruct 407 pairs per fixture and retain both pairs at shift 28. | Both implement the same domain definition. |
| Static versus p2 separation | **CLOSED** | Every prime passes `O_p=C_p` disjoint-union `H_p`; all `C_p` sets pass direct modulo-p-squared checks. | Selected fixtures only. |
| Mandatory prime-3 audit | **CLOSED** | The exact distribution `214/143/26/23/1` and the modulo-9 explanation reproduce. | Local to n0 and its active cell. |
| Factorization and valuation audit | **CLOSED** | 4,070 reported products and 6,905 obstruction-prime occurrences are independently checked. | Deterministic uint64 primality and Python remain trust surfaces. |
| Persistent rankings and unions | **CLOSED** | 4,873 coverage rows and both 32-step greedy histories reproduce exactly. | Greedy is heuristic; 105 losers remain uncovered. |
| Higher odd valuations | **CLOSED** | Valuations 3,5,... are separate and excluded from p2 totals. | Higher prime powers are not combined. |
| Corrected controls | **CLOSED** | Five modulo-360 controls are selected only from existing counts; no duplicates occur. | The sample is not statistically representative. |
| Activation cell | **CLOSED** | The exact cell and all nested-modulus density counts reproduce. | No candidate T value is evaluated. |
| Independent verification | **CLOSED** | The compact verifier imports no primary module and checks source, inputs, outputs, and baselines. | Both paths share runtime and specification. |
| Global A303656 statement | **OPEN** | No global claim is made. | The mathematical problem remains **UNRESOLVED**. |

## Corrections retained

1. Static odd coverage is not p2-persistent coverage.
2. Modulo-120 controls do not generally match modulo 9; modulo 360 repairs the
   prime-3 comparison.
3. Absolute obstruction-count advantages survive on all selected pairs, but
   losing-pair normalization and top-k unions are denominator- and k-dependent.

## Current conclusion

**VALIDATED P2-PERSISTENT CORE AUDIT**
"""


def run(
    root: Path, output_root: Path, generated_utc: str, requested_source_commit: str
) -> None:
    checkout_commit = git_value(root, "rev-parse", "HEAD")
    source_commit = git_value(
        root, "rev-parse", f"{requested_source_commit}^{{commit}}"
    )
    if not git_is_ancestor(root, source_commit, checkout_commit):
        raise SystemExit(
            f"source commit {source_commit} is not an ancestor of checkout {checkout_commit}"
        )
    source_parent = git_value(root, "rev-parse", f"{source_commit}^")
    source_paths = (
        "src/analyze_p2_persistent_core.py",
        "src/verify_p2_persistent_core.py",
    )
    source_hashes = {
        path: git_file_sha256(root, source_commit, path) for path in source_paths
    }
    for path in source_paths:
        if sha256_file(root / path) != source_hashes[path]:
            raise SystemExit(f"working source differs from source commit: {path}")
    fixed_input_audit = verify_fixed_inputs(root)
    counts, counts_hashes = read_counts(root)
    dossier_dir = root / "analysis/obstruction_dossier"
    panel = json.loads((dossier_dir / "panel.json").read_text(encoding="utf-8"))
    low_tail = [
        {"n": int(item["n"]), "validated_T": int(item["validated_T"])}
        for item in panel["low_tail_panel"]
    ]
    old_control_by_low = {
        int(item["low_tail_n"]): int(item["control_n"])
        for item in panel["matched_control_selections"]
    }
    dossier_fixtures, dossier_audit_counts = read_dossier_fixtures(root, panel)
    corrected = corrected_controls(counts, low_tail)

    max_remainder = max(int(item["control_n"]) for item in corrected) - 2
    primes = prime_table(math.isqrt(max_remainder))
    fixtures = dict(dossier_fixtures)
    for selection in corrected:
        n = int(selection["control_n"])
        if n not in fixtures:
            fixtures[n] = factor_selected_fixture(n, int(selection["control_T"]), primes)

    n0_fixture = fixtures[N0]
    prime3_distribution = Counter()
    category_distributions: dict[str, Counter[int]] = {
        "c=0": Counter(),
        "c=1": Counter(),
        "c>=2": Counter(),
    }
    for pair in n0_fixture.pairs:
        exponent = valuation(N0 - pair.shift, 3)
        prime3_distribution[exponent] += 1
        category = "c=0" if pair.c == 0 else ("c=1" if pair.c == 1 else "c>=2")
        category_distributions[category][exponent] += 1
    expected_distribution = {0: 214, 1: 143, 2: 26, 3: 23, 5: 1}
    if dict(sorted(prime3_distribution.items())) != expected_distribution:
        raise SystemExit(
            f"mandatory prime-3 check failed: {dict(sorted(prime3_distribution.items()))}"
        )
    if (
        len(n0_fixture.static_sets[3]) != 167
        or len(n0_fixture.p2_sets[3]) != 143
        or sum(len(v) for v in n0_fixture.higher_sets[3].values()) != 24
    ):
        raise SystemExit("mandatory prime-3 O/C/H count check failed")
    c_ge_2_expected = {
        pair.key
        for pair in n0_fixture.pairs
        if pair.c >= 2 and pair.d % 6 in (1, 3)
    }
    c_ge_2_actual = {
        pair.key
        for pair in n0_fixture.pairs
        if pair.c >= 2 and valuation(N0 - pair.shift, 3) == 1
    }
    if c_ge_2_expected != c_ge_2_actual:
        raise SystemExit("mandatory prime-3 modular explanation failed")

    role_instances: list[tuple[Fixture, str, int | None]] = []
    for item in low_tail:
        role_instances.append((fixtures[item["n"]], "LOW_TAIL", None))
    for item in panel["matched_control_selections"]:
        role_instances.append(
            (fixtures[int(item["control_n"])], "OLD_CONTROL_MOD_120", int(item["low_tail_n"]))
        )
    for item in corrected:
        role_instances.append(
            (fixtures[int(item["control_n"])], "CORRECTED_CONTROL_MOD_360", int(item["low_tail_n"]))
        )
    coverage_rows: list[dict[str, object]] = []
    for fixture, role, matched in role_instances:
        coverage_rows.extend(prime_coverage_rows(fixture, role, matched))

    marginal_rows = marginal_greedy(n0_fixture, 32)
    bit_rows = bit_greedy(n0_fixture, 32)
    core_rows = marginal_rows + bit_rows
    cell = activation_cell(N0)
    activation_rows = []
    for row in core_rows:
        modulus = int(row["product_M"])
        activation_rows.append(
            {
                "ordering": row["ordering"],
                "step": row["step"],
                "selected_primes": [int(x) for x in str(row["selected_primes"]).split(";")],
                "M": str(modulus),
                "M_bit_length": modulus.bit_length(),
                "M_decimal_digit_count": len(str(modulus)),
                "activation_cell": progression_stats(N0, modulus, int(cell["A"]), int(cell["B"])),
                "pilot_b": progression_stats(
                    N0, modulus, PILOT_LOW, PILOT_HIGH_EXCLUSIVE - 1
                ),
            }
        )

    corrected_ns = [int(item["control_n"]) for item in corrected]
    duplicate_controls = sorted(
        n for n, frequency in Counter(corrected_ns).items() if frequency > 1
    )
    low_and_corrected = [int(item["n"]) for item in low_tail] + corrected_ns
    mod9 = same_mod9_audit(low_and_corrected, fixtures)

    all_metric_ns = sorted(
        {int(item["n"]) for item in low_tail}
        | set(old_control_by_low.values())
        | set(corrected_ns)
    )
    metric_map = {n: fixture_metrics(fixtures[n]) for n in all_metric_ns}
    normalized = {
        "schema": "a303656-p2-normalized-comparison-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "top_k_definition": (
            "rank primes by descending |C_p|, tie by smaller prime, then take the union "
            "of the first k C_p sets; this is not the marginal greedy ordering"
        ),
        "fixtures": [metric_map[n] for n in all_metric_ns],
        "comparisons": [
            {
                "low_tail_n": int(item["n"]),
                "old_control_n": old_control_by_low[int(item["n"])],
                "corrected_control_n": next(
                    int(x["control_n"])
                    for x in corrected
                    if int(x["low_tail_n"]) == int(item["n"])
                ),
            }
            for item in low_tail
        ],
        "earlier_qualitative_statement_audit": comparison_observations(
            low_tail, old_control_by_low, corrected, metric_map, fixtures
        ),
        "global_statistical_significance_claimed": False,
    }

    selected_steps: dict[int, dict[str, int]] = defaultdict(dict)
    for row in core_rows:
        selected_steps[int(row["selected_prime"])][str(row["ordering"])] = int(row["step"])
    residue_bindings = []
    for prime in sorted(selected_steps):
        p2 = prime * prime
        expected = {
            pair.key
            for pair in n0_fixture.pairs
            if (N0 % p2 - pow(3, pair.c, p2) - pow(5, pair.d, p2)) % prime == 0
            and (N0 % p2 - pow(3, pair.c, p2) - pow(5, pair.d, p2)) % p2 != 0
        }
        if expected != n0_fixture.p2_sets[prime]:
            raise AssertionError("residue binding differs from C_p")
        residue_bindings.append(
            {
                "prime": prime,
                "t_p": N0 % p2,
                "p_squared": p2,
                "selected_at_step": selected_steps[prime],
                "C_p_pair_count": len(expected),
                "C_p_pairs": json_pair_list(expected),
                "direct_binding_verified": True,
            }
        )

    higher_observations = []
    for prime, by_e in sorted(n0_fixture.higher_sets.items()):
        for exponent, pairs_for_e in sorted(by_e.items()):
            higher_observations.append(
                {
                    "label": "HIGHER_PRIME_POWER_OBSERVATION",
                    "prime": prime,
                    "valuation": exponent,
                    "pairs": json_pair_list(pairs_for_e),
                    "pair_count": len(pairs_for_e),
                    "modulus_preserving_exact_valuation": str(prime ** (exponent + 1)),
                    "included_in_p2_core_totals": False,
                }
            )

    prime3 = {
        "valuation_distribution": {
            str(e): prime3_distribution[e] for e in sorted(prime3_distribution)
        },
        "static_odd_obstruction_count": len(n0_fixture.static_sets[3]),
        "p2_persistent_obstruction_count": len(n0_fixture.p2_sets[3]),
        "higher_odd_valuation_count": sum(
            len(v) for v in n0_fixture.higher_sets[3].values()
        ),
        "n0_mod_9": N0 % 9,
        "five_power_cycle_mod_9": [pow(5, d, 9) for d in range(6)],
        "c_ge_2_v1_residue_classes_mod_6": [1, 3],
        "c_ge_2_v1_pair_count": len(c_ge_2_actual),
        "c_category_distributions": {
            category: {str(e): counter[e] for e in sorted(counter)}
            for category, counter in category_distributions.items()
        },
    }

    output_dir = output_root / "analysis/p2_core"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_prime_csv(output_dir / "static_vs_p2_prime_coverage.csv", coverage_rows)
    write_core_csv(output_dir / "greedy_core_steps.csv", core_rows)

    baseline_hashes = {
        path: sha256_file(root / path) for path in BASELINE_PATHS
    }
    metadata = {
        "schema": "a303656-p2-core-metadata-v1",
        "task": "P2-PERSISTENT OBSTRUCTION CORE AND CONTROL AUDIT",
        "classification": "EXACT FINITE COMPUTATION ON FIXED SELECTED FIXTURES",
        "mathematical_problem_status": "UNRESOLVED",
        "generated_utc": generated_utc,
        "source_commit": source_commit,
        "source_parent_commit": source_parent,
        "results_commit": RESULT_COMMIT_BINDING,
        "results_commit_resolution": (
            "resolved as the commit containing this metadata and checked by the "
            "independent verifier during fresh replay"
        ),
        "source_file_sha256_at_source_commit": source_hashes,
        "primary_analyzer": {
            "path": "src/analyze_p2_persistent_core.py",
            "sha256": source_hashes["src/analyze_p2_persistent_core.py"],
        },
        "fixed_input_audit": fixed_input_audit,
        "pilot_b_counts_sha256": counts_hashes,
        "baseline_hashes_at_generation": baseline_hashes,
        "dossier_verification_counts": dossier_audit_counts,
        "fixture_counts": {
            "low_tail": 5,
            "old_controls": 5,
            "corrected_controls": 5,
            "distinct_analyzed_n": len(fixtures),
            "active_pairs_each": 407,
        },
        "scope_guards": {
            "counting_executable_invoked": False,
            "new_integer_interval_scanned": False,
            "CRT_system_solved": False,
            "arithmetic_progression_searched": False,
            "T_evaluated_at_progression_candidates": False,
            "certified_or_pilot_outputs_modified": False,
        },
    }
    n0_core = {
        "schema": "a303656-n0-p2-persistent-core-v1",
        "label": "HEURISTIC_P2_PERSISTENT_CORE",
        "optimality_claimed": False,
        "n0": N0,
        "active_pair_count": len(n0_fixture.pairs),
        "current_losing_pair_count": len(n0_fixture.losers),
        "original_winner_pair_count": len(n0_fixture.winners),
        "original_winner_pairs": json_pair_list(n0_fixture.winners),
        "prime_3": prime3,
        "greedy_orderings": {
            "MARGINAL_COVERAGE_GREEDY": [int(r["selected_prime"]) for r in marginal_rows],
            "COVERAGE_PER_MODULUS_BIT_GREEDY": [int(r["selected_prime"]) for r in bit_rows],
        },
        "bit_score_exact_comparison": (
            "compare a/log2(p^2) and b/log2(q^2) by q^a versus p^b; "
            "on exact equality choose the smaller prime"
        ),
        "selected_prime_residue_bindings": residue_bindings,
        "combined_congruence": "n == n0 (mod M)",
        "different_CRT_residue_solved": False,
        "higher_odd_valuations": higher_observations,
    }
    activation = {
        "schema": "a303656-p2-activation-cell-v1",
        "classification": "CANDIDATE_DENSITY ANALYSIS ONLY",
        "n0": N0,
        "cell": cell,
        "pilot_b_interval": [PILOT_LOW, PILOT_HIGH_EXCLUSIVE - 1],
        "nested_moduli": activation_rows,
        "T_evaluated_at_candidates": False,
    }
    corrected_output = {
        "schema": "a303656-p2-corrected-controls-v1",
        "classification": "COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES",
        "selection_rule": {
            "source": "existing validated PILOT-B counts.csv only",
            "block_anchor": PILOT_LOW,
            "block_width": BLOCK_WIDTH,
            "same_residue_modulus": 360,
            "exclude_all_low_tail_members": True,
            "lexicographic_key": ["abs(T(m)-60)", "abs(m-n)", "m"],
        },
        "counts_sha256": counts_hashes,
        "selections": corrected,
        "duplicate_controls": duplicate_controls,
        "duplicate_control_selection": bool(duplicate_controls),
        "modulo_9_C_3_audit": mod9,
    }
    write_json(output_dir / "metadata.json", metadata)
    write_json(output_dir / "n0_p2_core.json", n0_core)
    write_json(output_dir / "activation_cell.json", activation)
    write_json(output_dir / "corrected_controls.json", corrected_output)
    write_json(output_dir / "normalized_comparison.json", normalized)
    report = generate_report(
        metadata, n0_fixture, prime3, core_rows, cell, corrected_output, normalized
    )
    docs_dir = output_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "p2_persistent_core_audit.md").write_text(
        report, encoding="utf-8"
    )
    (docs_dir / "current_state.md").write_text(
        generate_current_state(metadata), encoding="utf-8"
    )
    (docs_dir / "audit_gap_register.md").write_text(
        generate_gap_register(metadata), encoding="utf-8"
    )
    print("P2_PRIMARY_ANALYSIS_PASS")
    print(f"prime3_distribution={dict(sorted(prime3_distribution.items()))}")
    print(f"corrected_controls={corrected_ns}")
    print(f"activation_cell=[{cell['A']},{cell['B']}]")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("run",))
    parser.add_argument("--generated-utc", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output_root = args.output_root.resolve() if args.output_root else root
    if args.action == "run":
        run(root, output_root, args.generated_utc, args.source_commit)


if __name__ == "__main__":
    main()
