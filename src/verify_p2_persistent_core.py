#!/usr/bin/env python3
"""Independent verifier for the selected-fixture p^2-persistent core audit.

This file intentionally imports no primary analysis module.  It reconstructs
the active domain, valuations, control selection, greedy histories, activation
cell, normalized metrics, hashes, and output tables using separately coded
helpers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path
from typing import Iterable


RESULT_COMMIT_BINDING = "RESULT_COMMIT_CONTAINING_THIS_FILE"
N0 = 240000005594
PILOT_LOW = 240000000001
PILOT_HIGH_EXCLUSIVE = 240000100001
BLOCK = 10_000
TOP_K = (1, 2, 4, 8, 16)
EXPECTED_V3 = {0: 214, 1: 143, 2: 26, 3: 23, 5: 1}
BASELINES = (
    "output/formal_results_audit.json",
    "output/final_packaging_audit.json",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt",
    "output/final_results_manifest.json",
    "output/direct/formal_1p6b_final/summary.json",
)


@dataclass
class RebuiltFixture:
    n: int
    validated_t: int
    domain: list[tuple[int, int, int]]
    winners: set[tuple[int, int]]
    losers: set[tuple[int, int]]
    odd: dict[int, set[tuple[int, int]]]
    exact_one: dict[int, set[tuple[int, int]]]
    higher: dict[int, dict[int, set[tuple[int, int]]]]
    signatures: dict[tuple[int, int], tuple[int, ...]]


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(262_144)
            if not block:
                return h.hexdigest()
            h.update(block)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: object) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def git(root: Path, argument: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", argument],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def git_is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=root
        ).returncode
        == 0
    )


def git_file_hash(root: Path, commit: str, path: str) -> str:
    content = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(content).hexdigest()


def pair_domain(n: int) -> list[tuple[int, int, int]]:
    threes: list[int] = []
    value = 1
    while value <= n:
        threes.append(value)
        value = value * 3
    fives: list[int] = []
    value = 1
    while value <= n:
        fives.append(value)
        value = value * 5
    result: list[tuple[int, int, int]] = []
    for c in range(len(threes)):
        for d in range(len(fives)):
            shift = threes[c] + fives[d]
            if shift <= n:
                result.append((c, d, shift))
    return result


def vp(x: int, p: int) -> int:
    count = 0
    quotient, remainder = divmod(x, p)
    while remainder == 0:
        count += 1
        x = quotient
        quotient, remainder = divmod(x, p)
    return count


def deterministic_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    odd = n - 1
    twos = 0
    while odd & 1 == 0:
        odd >>= 1
        twos += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        y = pow(a, odd, n)
        if y == 1 or y == n - 1:
            continue
        passed = False
        for _ in range(twos - 1):
            y = y * y % n
            if y == n - 1:
                passed = True
                break
        if not passed:
            return False
    return True


def odd_prime_sieve(limit: int) -> list[int]:
    if limit < 2:
        return []
    flags = bytearray(b"\x01") * ((limit // 2) + 1)
    flags[0] = 0
    stop = math.isqrt(limit)
    for i in range(1, stop // 2 + 1):
        if not flags[i]:
            continue
        p = 2 * i + 1
        start = (p * p) // 2
        for j in range(start, len(flags), p):
            flags[j] = 0
    return [2] + [2 * i + 1 for i in range(1, len(flags)) if flags[i] and 2 * i + 1 <= limit]


def independent_factor(n: int, primes: list[int]) -> tuple[tuple[int, int], ...]:
    remaining = n
    answer: list[tuple[int, int]] = []
    for p in primes:
        if p > remaining // p:
            break
        if remaining % p != 0:
            continue
        exponent = 0
        while remaining % p == 0:
            remaining //= p
            exponent += 1
        answer.append((p, exponent))
    if remaining != 1:
        if not deterministic_prime(remaining):
            raise AssertionError("independent factor residual is composite")
        answer.append((remaining, 1))
    return tuple(answer)


def reported_factors(
    remainder: int, raw: list[dict[str, object]]
) -> tuple[tuple[int, int], ...]:
    factors: list[tuple[int, int]] = []
    product = 1
    last = 0
    for entry in raw:
        p = int(entry["prime"])
        e = int(entry["exponent"])
        if p <= last or e <= 0 or not deterministic_prime(p):
            raise AssertionError("bad reported prime factor")
        if vp(remainder, p) != e:
            raise AssertionError("direct valuation differs from reported exponent")
        product *= p**e
        factors.append((p, e))
        last = p
    if product != remainder:
        raise AssertionError("reported factorization product does not reconstruct remainder")
    return tuple(factors)


def rebuild_fixture(
    n: int,
    validated_t: int,
    factors: dict[tuple[int, int], tuple[tuple[int, int], ...]],
) -> RebuiltFixture:
    domain = pair_domain(n)
    if len(domain) != 407 or set(factors) != {(c, d) for c, d, _ in domain}:
        raise AssertionError("active-pair reconstruction failure")
    shifts = {(c, d): shift for c, d, shift in domain}
    odd: dict[int, set[tuple[int, int]]] = defaultdict(set)
    exact_one: dict[int, set[tuple[int, int]]] = defaultdict(set)
    higher: dict[int, dict[int, set[tuple[int, int]]]] = defaultdict(lambda: defaultdict(set))
    signatures: dict[tuple[int, int], tuple[int, ...]] = {}
    winners: set[tuple[int, int]] = set()
    losers: set[tuple[int, int]] = set()
    for key, factorization in factors.items():
        remainder = n - shifts[key]
        signature: list[int] = []
        for p, reported_e in factorization:
            e = vp(remainder, p)
            if e != reported_e:
                raise AssertionError("valuation reconstruction failure")
            if p % 4 == 3 and e % 2 == 1:
                signature.append(p)
                odd[p].add(key)
                if e == 1:
                    exact_one[p].add(key)
                    if remainder % p or remainder % (p * p) == 0:
                        raise AssertionError("C_p modulo-p-squared definition failure")
                    w = (remainder // p) % p
                    if w == 0:
                        raise AssertionError("C_p quotient is zero modulo p")
                elif e >= 3:
                    higher[p][e].add(key)
        signatures[key] = tuple(signature)
        (losers if signature else winners).add(key)
    if len(winners) != validated_t:
        raise AssertionError("winner count does not reproduce stored T")
    for p in odd:
        high_union = set().union(*higher[p].values()) if higher[p] else set()
        if odd[p] != exact_one[p] | high_union or exact_one[p] & high_union:
            raise AssertionError("O_p disjoint-union identity failed")
    return RebuiltFixture(
        n, validated_t, domain, winners, losers, dict(odd), dict(exact_one),
        {p: dict(by_e) for p, by_e in higher.items()}, signatures
    )


def strict_counts(root: Path) -> tuple[dict[int, int], dict[str, str]]:
    base = root / "output/tn_pilot_20260713/pilot_b"
    files = [base / x / "counts.csv" for x in ("bitset", "clean", "oracle")]
    contents = [p.read_bytes() for p in files]
    if contents.count(contents[0]) != 3:
        raise AssertionError("counts copies differ")
    values: dict[int, int] = {}
    with files[0].open(newline="", encoding="ascii") as handle:
        rows = csv.reader(handle)
        if next(rows, None) != ["n", "T"]:
            raise AssertionError("bad counts header")
        expected = PILOT_LOW
        for row in rows:
            if len(row) != 2 or not row[0].isdigit() or not row[1].isdigit():
                raise AssertionError("bad counts row")
            n, t = int(row[0]), int(row[1])
            if n != expected:
                raise AssertionError("counts rows not contiguous")
            values[n] = t
            expected += 1
    if expected != PILOT_HIGH_EXCLUSIVE:
        raise AssertionError("counts endpoint mismatch")
    return values, {str(p.relative_to(root)): file_hash(p) for p in files}


def select_controls(
    counts: dict[int, int], low_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    forbidden = {int(row["n"]) for row in low_rows}
    result = []
    for row in low_rows:
        n = int(row["n"])
        index = (n - PILOT_LOW) // BLOCK
        start = PILOT_LOW + index * BLOCK
        stop = start + BLOCK
        same_residue = (
            m for m in range(start, stop) if m not in forbidden and (m - n) % 360 == 0
        )
        m = min(same_residue, key=lambda q: (abs(counts[q] - 60), abs(q - n), q))
        result.append(
            {
                "low_tail_n": n,
                "low_tail_T": int(row["validated_T"]),
                "control_n": m,
                "control_T": counts[m],
                "block_index": index,
                "block_start": start,
                "block_end_exclusive": stop,
                "residue_mod_360": n % 360,
                "residue_mod_9": n % 9,
                "selection_key": [abs(counts[m] - 60), abs(m - n), m],
            }
        )
    return result


def verify_declared_hashes(root: Path) -> tuple[int, dict[str, str]]:
    dossier = root / "analysis/obstruction_dossier"
    pilot = root / "output/tn_pilot_20260713"
    metadata = read_json(dossier / "metadata.json")
    checked = 0

    def validate(mapping: dict[str, str], base: Path) -> None:
        nonlocal checked
        for relative, expected in mapping.items():
            actual = file_hash(base / relative)
            checked += 1
            if actual != expected:
                raise AssertionError(f"hash mismatch for {base / relative}")

    validate(metadata["artifact_sha256"], dossier)
    validate(metadata["pilot_input_integrity"]["before_generation"], root)
    validate(metadata["pilot_input_integrity"]["after_generation"], root)
    validate(metadata["baseline_integrity"]["before_generation"], root)
    validate(metadata["baseline_integrity"]["after_generation"], root)
    for phase in ("pilot_a", "pilot_b"):
        for implementation in ("bitset", "clean", "oracle"):
            base = pilot / phase / implementation
            provenance = read_json(base / "provenance.json")
            validate(provenance["outputs_sha256"], base)
    baselines = {path: file_hash(root / path) for path in BASELINES}
    for path, actual in baselines.items():
        expected = metadata["baseline_integrity"]["after_generation"][path]
        if actual != expected:
            raise AssertionError("certified baseline hash changed")
    return checked, baselines


def ranked(mapping: dict[int, set[tuple[int, int]]]) -> list[int]:
    return sorted((p for p in mapping if mapping[p]), key=lambda p: (-len(mapping[p]), p))


def parse_pair_text(text: str) -> set[tuple[int, int]]:
    if not text:
        return set()
    return {tuple(map(int, item.split(":"))) for item in text.split(";")}


def verify_coverage_csv(
    root: Path,
    fixtures: dict[int, RebuiltFixture],
    instances: list[tuple[int, str, int | None]],
) -> int:
    path = root / "analysis/p2_core/static_vs_p2_prime_coverage.csv"
    groups: dict[tuple[int, str, int | None], list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (
                int(row["n"]),
                row["panel_role"],
                int(row["matched_low_tail_n"]) if row["matched_low_tail_n"] else None,
            )
            groups[key].append(row)
    if set(groups) != set(instances):
        raise AssertionError("coverage CSV fixture-role domain mismatch")
    row_count = 0
    for instance in instances:
        fixture = fixtures[instance[0]]
        rows = groups[instance]
        by_prime = {int(row["prime"]): row for row in rows}
        if set(by_prime) != set(fixture.odd):
            raise AssertionError("coverage CSV prime domain mismatch")
        odd_rank = {p: i + 1 for i, p in enumerate(ranked(fixture.odd))}
        one_rank = {p: i + 1 for i, p in enumerate(ranked(fixture.exact_one))}
        high_flat = {
            p: set().union(*fixture.higher.get(p, {}).values())
            if fixture.higher.get(p)
            else set()
            for p in fixture.odd
        }
        high_rank = {p: i + 1 for i, p in enumerate(ranked(high_flat))}
        for p, row in by_prime.items():
            odd_set = fixture.odd[p]
            one_set = fixture.exact_one.get(p, set())
            by_e = fixture.higher.get(p, {})
            high_set = set().union(*by_e.values()) if by_e else set()
            expected_scalars = {
                "validated_T": fixture.validated_t,
                "active_pair_count": 407,
                "losing_pair_count": len(fixture.losers),
                "static_rank": odd_rank[p],
                "static_odd_count": len(odd_set),
                "p2_persistent_count": len(one_set),
                "higher_odd_count": len(high_set),
            }
            for field, expected in expected_scalars.items():
                if int(row[field]) != expected:
                    raise AssertionError(f"coverage scalar mismatch: {field}")
            if row["p2_rank"] != (str(one_rank[p]) if p in one_rank else ""):
                raise AssertionError("p2 rank mismatch")
            if row["higher_rank"] != (str(high_rank[p]) if p in high_rank else ""):
                raise AssertionError("higher rank mismatch")
            if parse_pair_text(row["O_p_pairs"]) != odd_set:
                raise AssertionError("O_p explicit set mismatch")
            if parse_pair_text(row["C_p_pairs"]) != one_set:
                raise AssertionError("C_p explicit set mismatch")
            raw_h = json.loads(row["H_p_pairs_by_valuation"])
            parsed_h = {
                int(e): {tuple(pair) for pair in pairs} for e, pairs in raw_h.items()
            }
            if parsed_h != by_e:
                raise AssertionError("H_p explicit split mismatch")
            expected_moduli = {str(e): str(p ** (e + 1)) for e in by_e}
            if json.loads(row["higher_prime_power_moduli"]) != expected_moduli:
                raise AssertionError("higher-prime-power modulus mismatch")
            row_count += 1
    return row_count


def bit_order(a: tuple[int, int], b: tuple[int, int]) -> int:
    a_new, a_p = a
    b_new, b_p = b
    compare_left = pow(b_p, a_new)
    compare_right = pow(a_p, b_new)
    if compare_left != compare_right:
        return -1 if compare_left > compare_right else 1
    return (a_p > b_p) - (a_p < b_p)


def rebuild_greedy(fixture: RebuiltFixture, mode: str) -> list[dict[str, object]]:
    used: set[int] = set()
    union: set[tuple[int, int]] = set()
    product = 1
    output = []
    for step in range(1, 33):
        options = [
            (len(fixture.exact_one[p] - union), p)
            for p in fixture.exact_one
            if fixture.exact_one[p] and p not in used
        ]
        options = [item for item in options if item[0]]
        if mode == "MARGINAL_COVERAGE_GREEDY":
            new_count, p = min(options, key=lambda x: (-x[0], x[1]))
        else:
            new_count, p = sorted(options, key=cmp_to_key(bit_order))[0]
        new_pairs = fixture.exact_one[p] - union
        used.add(p)
        union |= new_pairs
        product *= p * p
        output.append(
            {
                "step": step,
                "selected_prime": p,
                "newly_covered_pairs": new_count,
                "newly_covered_pair_set": new_pairs,
                "covered": len(union),
                "covered_losers": len(union & fixture.losers),
                "uncovered_losers": len(fixture.losers - union),
                "uncovered_winners": len(fixture.winners - union),
                "product": product,
                "bits": product.bit_length(),
                "digits": len(str(product)),
                "selected": list(output[-1]["selected"] if output else []) + [p],
            }
        )
    return output


def verify_greedy(root: Path, fixture: RebuiltFixture) -> tuple[list[dict[str, object]], int]:
    path = root / "analysis/p2_core/greedy_core_steps.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 64:
        raise AssertionError("greedy CSV must have 64 rows")
    expected_all = []
    for mode in ("MARGINAL_COVERAGE_GREEDY", "COVERAGE_PER_MODULUS_BIT_GREEDY"):
        expected = rebuild_greedy(fixture, mode)
        actual = [row for row in rows if row["ordering"] == mode]
        if len(actual) != 32:
            raise AssertionError("greedy ordering row count mismatch")
        for wanted, row in zip(expected, actual, strict=True):
            scalars = {
                "step": wanted["step"],
                "selected_prime": wanted["selected_prime"],
                "newly_covered_pairs": wanted["newly_covered_pairs"],
                "cumulative_covered_active_pairs": wanted["covered"],
                "cumulative_covered_current_losers": wanted["covered_losers"],
                "uncovered_current_losers": wanted["uncovered_losers"],
                "uncovered_original_winners": wanted["uncovered_winners"],
                "M_bit_length": wanted["bits"],
                "M_decimal_digit_count": wanted["digits"],
            }
            for field, value in scalars.items():
                if int(row[field]) != value:
                    raise AssertionError(f"greedy mismatch {mode} {field}")
            if int(row["product_M"]) != wanted["product"]:
                raise AssertionError("greedy modulus product mismatch")
            if parse_pair_text(row["newly_covered_pair_set"]) != wanted["newly_covered_pair_set"]:
                raise AssertionError("greedy newly covered set mismatch")
            if [int(x) for x in row["selected_primes"].split(";")] != wanted["selected"]:
                raise AssertionError("greedy selected prefix mismatch")
        expected_all.extend({"ordering": mode, **item} for item in expected)
    return expected_all, len(rows)


def independent_cell(n: int) -> tuple[int, int, int, dict[int, list[tuple[int, int]]]]:
    threes = [1]
    while threes[-1] <= n:
        threes.append(threes[-1] * 3)
    fives = [1]
    while fives[-1] <= n:
        fives.append(fives[-1] * 5)
    levels: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for c, x in enumerate(threes):
        for d, y in enumerate(fives):
            levels[x + y].append((c, d))
    before = max(x for x in levels if x <= n)
    next_level = min(x for x in levels if x > n)
    return before, next_level - 1, next_level, levels


def ceiling_division(x: int, y: int) -> int:
    q, r = divmod(x, y)
    return q if r == 0 else q + 1


def candidate_count(n0: int, modulus: int, low: int, high: int) -> tuple[int, int, int]:
    lo = ceiling_division(low - n0, modulus)
    hi = (high - n0) // modulus
    return lo, hi, hi - lo + 1


def verify_activation(
    root: Path, greedy: list[dict[str, object]]
) -> tuple[int, int, int]:
    artifact = read_json(root / "analysis/p2_core/activation_cell.json")
    a, b, next_level, levels = independent_cell(N0)
    cell = artifact["cell"]
    if (int(cell["A"]), int(cell["B"]), int(cell["next_activation"]["shift"])) != (a, b, next_level):
        raise AssertionError("activation-cell endpoints mismatch")
    duplicates = {shift: pairs for shift, pairs in levels.items() if len(pairs) > 1 and shift <= N0}
    if duplicates != {28: [(1, 2), (3, 0)]}:
        raise AssertionError("duplicate shift 28 audit failed")
    actual_rows = {
        (row["ordering"], int(row["step"])): row for row in artifact["nested_moduli"]
    }
    if len(actual_rows) != 64:
        raise AssertionError("activation modulus row count mismatch")
    for expected in greedy:
        row = actual_rows[(expected["ordering"], int(expected["step"]))]
        modulus = int(expected["product"])
        if int(row["M"]) != modulus or int(row["M_bit_length"]) != modulus.bit_length() or int(row["M_decimal_digit_count"]) != len(str(modulus)):
            raise AssertionError("activation modulus size mismatch")
        for key, low, high in (
            ("activation_cell", a, b),
            ("pilot_b", PILOT_LOW, PILOT_HIGH_EXCLUSIVE - 1),
        ):
            lo, hi, count = candidate_count(N0, modulus, low, high)
            saved = row[key]
            if (int(saved["k_min"]), int(saved["k_max"]), int(saved["candidate_count_including_k0"])) != (lo, hi, count):
                raise AssertionError("candidate-density arithmetic mismatch")
            expected_left = {"k": -1, "n": N0 - modulus} if lo <= -1 else None
            expected_right = {"k": 1, "n": N0 + modulus} if hi >= 1 else None
            if saved["nearest_nonzero_left"] != expected_left or saved["nearest_nonzero_right"] != expected_right:
                raise AssertionError("nearest candidate mismatch")
    return a, b, next_level


def exact_ratio(obj: dict[str, object], numerator: int, denominator: int) -> None:
    if int(obj["numerator"]) != numerator or int(obj["denominator"]) != denominator:
        raise AssertionError("normalized ratio numerator/denominator mismatch")


def fixture_summary(fixture: RebuiltFixture) -> dict[str, object]:
    losers = len(fixture.losers)
    signatures = len({fixture.signatures[x] for x in fixture.losers})
    p2_count = sum(bool(x) for x in fixture.exact_one.values())
    p2_ranked = ranked(fixture.exact_one)
    top = {}
    for k in TOP_K:
        union = set().union(*(fixture.exact_one[p] for p in p2_ranked[:k]))
        top[k] = (p2_ranked[:k], len(union))
    return {
        "losers": losers,
        "primes": len(fixture.odd),
        "signatures": signatures,
        "p2_primes": p2_count,
        "p3_static": len(fixture.odd.get(3, set())),
        "p3_p2": len(fixture.exact_one.get(3, set())),
        "top": top,
    }


def verify_normalized(root: Path, fixtures: dict[int, RebuiltFixture]) -> int:
    artifact = read_json(root / "analysis/p2_core/normalized_comparison.json")
    rows = artifact["fixtures"]
    if {int(row["n"]) for row in rows} != set(fixtures):
        raise AssertionError("normalized fixture domain mismatch")
    summaries: dict[int, dict[str, object]] = {}
    for row in rows:
        n = int(row["n"])
        fixture = fixtures[n]
        expected = fixture_summary(fixture)
        summaries[n] = expected
        if int(row["validated_T"]) != fixture.validated_t or int(row["active_pair_count"]) != 407 or int(row["losing_pair_count"]) != expected["losers"]:
            raise AssertionError("normalized fixture header mismatch")
        for field, key in (
            ("distinct_obstruction_primes", "primes"),
            ("obstruction_signatures", "signatures"),
            ("p2_persistent_prime_count", "p2_primes"),
        ):
            if int(row[field]["absolute"]) != expected[key]:
                raise AssertionError("normalized absolute metric mismatch")
            exact_ratio(row[field]["per_losing_pair"], expected[key], expected["losers"])
        for field, key in (
            ("prime_3_static_coverage", "p3_static"),
            ("prime_3_p2_coverage", "p3_p2"),
        ):
            if int(row[field]["absolute"]) != expected[key]:
                raise AssertionError("prime-3 metric mismatch")
            exact_ratio(row[field]["over_active_pairs"], expected[key], 407)
            exact_ratio(row[field]["over_losing_pairs"], expected[key], expected["losers"])
        top_rows = {int(item["k"]): item for item in row["top_k_p2_frequency_ranked_union"]}
        for k, (primes, covered) in expected["top"].items():
            saved = top_rows[k]
            if saved["ranked_primes"] != primes or int(saved["covered_pairs"]) != covered:
                raise AssertionError("top-k p2 union mismatch")
            exact_ratio(saved["coverage_over_active_pairs"], covered, 407)
            exact_ratio(saved["coverage_over_losing_pairs"], covered, expected["losers"])

    triples = [
        (
            int(row["low_tail_n"]),
            int(row["old_control_n"]),
            int(row["corrected_control_n"]),
        )
        for row in artifact["comparisons"]
    ]
    if len(triples) != 5:
        raise AssertionError("normalized comparison pair count mismatch")

    def classify(values: list[bool]) -> str:
        if all(values):
            return "SURVIVES_ALL_FIVE"
        if any(values):
            return "SURVIVES_PARTIALLY"
        return "DOES_NOT_SURVIVE"

    def normalized_greater(low: int, control: int, field: str) -> bool:
        return int(summaries[low][field]) * int(summaries[control]["losers"]) > int(
            summaries[control][field]
        ) * int(summaries[low]["losers"])

    statements = {
        row["statement"]: row for row in artifact["earlier_qualitative_statement_audit"]
    }
    for statement_name, field in (
        ("LOW_TAIL_HAS_MORE_DISTINCT_OBSTRUCTION_PRIMES", "primes"),
        ("LOW_TAIL_HAS_MORE_OBSTRUCTION_SIGNATURES", "signatures"),
        ("LOW_TAIL_HAS_MORE_P2_PERSISTENT_PRIMES", "p2_primes"),
    ):
        saved = statements[statement_name]
        for label, position in (("old_control", 1), ("corrected_mod9_control", 2)):
            absolute = [
                int(summaries[t[0]][field]) > int(summaries[t[position]][field])
                for t in triples
            ]
            normalized = [normalized_greater(t[0], t[position], field) for t in triples]
            if saved[f"{label}_absolute"]["verdict"] != classify(absolute):
                raise AssertionError("qualitative absolute verdict mismatch")
            if saved[f"{label}_normalized"]["verdict"] != classify(normalized):
                raise AssertionError("qualitative normalized verdict mismatch")

    prime3_saved = statements["LOW_TAIL_HAS_HIGHER_PRIME_3_COVERAGE"]
    for label, position in (("old", 1), ("corrected_mod9", 2)):
        for kind, field in (("static", "p3_static"), ("p2", "p3_p2")):
            comparisons = [
                int(summaries[t[0]][field]) > int(summaries[t[position]][field])
                for t in triples
            ]
            if prime3_saved[f"{kind}_{label}_controls"]["verdict"] != classify(comparisons):
                raise AssertionError("prime-3 qualitative verdict mismatch")

    largest_saved = statements["PRIME_3_IS_THE_LARGEST_STATIC_SINGLE_PRIME_COVER"]
    all_largest = all(ranked(fixtures[n].odd)[0] == 3 for n in fixtures)
    expected_largest_verdict = (
        "SURVIVES_ALL_SELECTED_FIXTURES"
        if all_largest
        else "DOES_NOT_SURVIVE_ALL_SELECTED_FIXTURES"
    )
    if largest_saved["verdict"] != expected_largest_verdict:
        raise AssertionError("prime-3 largest-cover verdict mismatch")

    top_saved = statements["LOW_TAIL_HAS_HIGHER_TOP_K_P2_UNION_COVERAGE"]
    saved_by_k = {int(row["k"]): row for row in top_saved["by_k"]}
    for k in TOP_K:
        for label, position in (("old_controls", 1), ("corrected_mod9_controls", 2)):
            active_values = []
            loser_values = []
            for triple in triples:
                low_n, control_n = triple[0], triple[position]
                low_covered = int(summaries[low_n]["top"][k][1])
                control_covered = int(summaries[control_n]["top"][k][1])
                active_values.append(low_covered > control_covered)
                loser_values.append(
                    low_covered * int(summaries[control_n]["losers"])
                    > control_covered * int(summaries[low_n]["losers"])
                )
            saved = saved_by_k[k][label]
            if saved["over_active_pairs"]["verdict"] != classify(active_values):
                raise AssertionError("top-k active-denominator verdict mismatch")
            if saved["over_losing_pairs"]["verdict"] != classify(loser_values):
                raise AssertionError("top-k loser-denominator verdict mismatch")
    return len(rows)


def verify_residue_bindings(root: Path, fixture: RebuiltFixture) -> int:
    artifact = read_json(root / "analysis/p2_core/n0_p2_core.json")
    bindings = artifact["selected_prime_residue_bindings"]
    domain = fixture.domain
    for binding in bindings:
        p = int(binding["prime"])
        square = p * p
        t = N0 % square
        if int(binding["t_p"]) != t or int(binding["p_squared"]) != square:
            raise AssertionError("saved residue binding scalar mismatch")
        direct = set()
        for c, d, _ in domain:
            difference = (t - pow(3, c, square) - pow(5, d, square)) % square
            if difference % p == 0 and difference != 0:
                direct.add((c, d))
        if direct != fixture.exact_one[p] or {tuple(pair) for pair in binding["C_p_pairs"]} != direct:
            raise AssertionError("saved residue binding C_p mismatch")
    return len(bindings)


def run(
    root: Path,
    output_root: Path,
    verified_utc: str,
    requested_source_commit: str,
    requested_results_commit: str | None,
) -> None:
    checkout_commit = git(root, "HEAD")
    source_commit = git(root, f"{requested_source_commit}^{{commit}}")
    if not git_is_ancestor(root, source_commit, checkout_commit):
        raise SystemExit(
            f"source commit {source_commit} is not an ancestor of checkout {checkout_commit}"
        )
    source_parent = git(root, f"{source_commit}^")
    source_paths = (
        "src/analyze_p2_persistent_core.py",
        "src/verify_p2_persistent_core.py",
    )
    source_hashes = {
        path: git_file_hash(root, source_commit, path) for path in source_paths
    }
    for path in source_paths:
        if file_hash(root / path) != source_hashes[path]:
            raise SystemExit(f"working source differs from source commit: {path}")
    if requested_results_commit is None:
        results_commit = RESULT_COMMIT_BINDING
        results_commit_resolved = False
    else:
        results_commit = git(root, f"{requested_results_commit}^{{commit}}")
        results_commit_resolved = True
        if checkout_commit != results_commit:
            raise SystemExit(
                f"results checkout mismatch: expected {results_commit}, got {checkout_commit}"
            )
        if not git_is_ancestor(root, source_commit, results_commit):
            raise SystemExit("source commit is not an ancestor of results commit")
    checks: dict[str, bool] = {}
    checks["source_commit_ancestry_and_source_hashes"] = True
    declared_hash_count, baseline_hashes = verify_declared_hashes(root)
    checks["input_and_baseline_hashes"] = True
    counts, counts_hashes = strict_counts(root)
    checks["pilot_b_counts_three_way_identity_and_domain"] = True

    panel = read_json(root / "analysis/obstruction_dossier/panel.json")
    low_rows = panel["low_tail_panel"]
    old_selections = panel["matched_control_selections"]
    old_control_by_low = {
        int(row["low_tail_n"]): int(row["control_n"]) for row in old_selections
    }
    selected_controls = select_controls(counts, low_rows)
    controls_artifact = read_json(root / "analysis/p2_core/corrected_controls.json")
    if controls_artifact["selections"] != selected_controls:
        raise AssertionError("corrected control selections differ")
    duplicates = sorted(
        n for n, count in Counter(int(x["control_n"]) for x in selected_controls).items() if count > 1
    )
    if controls_artifact["duplicate_controls"] != duplicates:
        raise AssertionError("duplicate-control report mismatch")
    checks["corrected_control_selection_from_existing_counts"] = True

    records_by_n: dict[int, list[dict[str, object]]] = defaultdict(list)
    records_path = root / "analysis/obstruction_dossier/records.jsonl"
    for raw_line in records_path.read_text(encoding="utf-8").splitlines():
        row = json.loads(raw_line)
        records_by_n[int(row["n"])].append(row)
    expected_old_ns = {int(row["n"]) for row in panel["research_panel"]}
    if set(records_by_n) != expected_old_ns or sum(map(len, records_by_n.values())) != 4070:
        raise AssertionError("dossier row domain mismatch")
    validated_t = {int(row["n"]): int(row["validated_T"]) for row in panel["research_panel"]}
    fixtures: dict[int, RebuiltFixture] = {}
    factorization_count = 0
    obstruction_count = 0
    for n, rows in records_by_n.items():
        domain = pair_domain(n)
        by_key = {(int(row["c"]), int(row["d"])): row for row in rows}
        factors = {}
        for c, d, shift in domain:
            row = by_key[(c, d)]
            remainder = n - shift
            if int(row["shift"]) != shift or int(row["remainder"]) != remainder:
                raise AssertionError("dossier shift/remainder mismatch")
            factorization = reported_factors(remainder, row["complete_factorization"])
            recomputed = [p for p, e in factorization if p % 4 == 3 and e % 2 == 1]
            if recomputed != [int(p) for p in row["all_3mod4_odd_valuation_primes"]]:
                raise AssertionError("dossier obstruction list mismatch")
            factors[(c, d)] = factorization
            factorization_count += 1
            obstruction_count += len(recomputed)
        fixtures[n] = rebuild_fixture(n, validated_t[n], factors)
    checks["active_pair_completeness_and_reported_factorizations"] = True
    checks["independent_direct_valuations_and_obstruction_lists"] = True

    corrected_ns = [int(row["control_n"]) for row in selected_controls]
    prime_list = odd_prime_sieve(math.isqrt(max(corrected_ns) - 2))
    for row in selected_controls:
        n = int(row["control_n"])
        if n in fixtures:
            continue
        factor_map = {
            (c, d): independent_factor(n - shift, prime_list)
            for c, d, shift in pair_domain(n)
        }
        fixtures[n] = rebuild_fixture(n, int(row["control_T"]), factor_map)
    checks["corrected_control_factorizations_and_T_reproduction"] = True

    n0 = fixtures[N0]
    distribution = Counter(vp(N0 - shift, 3) for _, _, shift in n0.domain)
    if dict(sorted(distribution.items())) != EXPECTED_V3:
        raise AssertionError("mandatory prime-3 distribution mismatch")
    if len(n0.odd[3]) != 167 or len(n0.exact_one[3]) != 143 or sum(len(x) for x in n0.higher[3].values()) != 24:
        raise AssertionError("mandatory prime-3 O/C/H mismatch")
    modular_expected = {
        (c, d) for c, d, shift in n0.domain if c >= 2 and d % 6 in (1, 3)
    }
    modular_actual = {
        (c, d) for c, d, shift in n0.domain if c >= 2 and vp(N0 - shift, 3) == 1
    }
    if modular_expected != modular_actual:
        raise AssertionError("prime-3 modular explanation mismatch")
    checks["mandatory_prime_3_distribution_and_modular_explanation"] = True
    checks["O_equals_disjoint_C_union_H_and_C_congruence"] = True

    instances: list[tuple[int, str, int | None]] = []
    for row in low_rows:
        instances.append((int(row["n"]), "LOW_TAIL", None))
    for row in old_selections:
        instances.append((int(row["control_n"]), "OLD_CONTROL_MOD_120", int(row["low_tail_n"])))
    for row in selected_controls:
        instances.append((int(row["control_n"]), "CORRECTED_CONTROL_MOD_360", int(row["low_tail_n"])))
    coverage_rows = verify_coverage_csv(root, fixtures, instances)
    checks["static_vs_p2_rankings_and_explicit_pair_sets"] = True

    greedy, greedy_rows = verify_greedy(root, n0)
    checks["both_greedy_histories_and_exact_modulus_sizes"] = True
    a, b, next_level = verify_activation(root, greedy)
    checks["activation_cell_and_candidate_density"] = True
    binding_count = verify_residue_bindings(root, n0)
    checks["selected_prime_residue_bindings"] = True

    low_corrected_ns = [int(row["n"]) for row in low_rows] + corrected_ns
    domains = [{(c, d) for c, d, _ in fixtures[n].domain} for n in low_corrected_ns]
    if any(domain != domains[0] for domain in domains):
        raise AssertionError("low/corrected active domains differ")
    for i, n in enumerate(low_corrected_ns):
        for m in low_corrected_ns[i + 1 :]:
            if n % 9 == m % 9 and fixtures[n].exact_one[3] != fixtures[m].exact_one[3]:
                raise AssertionError("equal mod-9 residues have different C_3")
    checks["modulo_9_prime_3_set_identity"] = True

    normalized_fixture_count = verify_normalized(root, fixtures)
    checks["absolute_and_normalized_comparison_metrics"] = True

    primary_metadata = read_json(root / "analysis/p2_core/metadata.json")
    if (
        primary_metadata["source_commit"] != source_commit
        or primary_metadata["source_parent_commit"] != source_parent
        or primary_metadata["results_commit"] != RESULT_COMMIT_BINDING
        or primary_metadata["source_file_sha256_at_source_commit"] != source_hashes
    ):
        raise AssertionError("primary metadata commit binding mismatch")
    if primary_metadata["baseline_hashes_at_generation"] != baseline_hashes:
        raise AssertionError("primary baseline hashes differ")
    if primary_metadata["pilot_b_counts_sha256"] != counts_hashes:
        raise AssertionError("primary counts hashes differ")
    if file_hash(root / primary_metadata["primary_analyzer"]["path"]) != primary_metadata["primary_analyzer"]["sha256"]:
        raise AssertionError("primary analyzer source hash mismatch")
    checks["primary_metadata_bindings"] = True

    output_paths = (
        "analysis/p2_core/metadata.json",
        "analysis/p2_core/static_vs_p2_prime_coverage.csv",
        "analysis/p2_core/n0_p2_core.json",
        "analysis/p2_core/greedy_core_steps.csv",
        "analysis/p2_core/activation_cell.json",
        "analysis/p2_core/corrected_controls.json",
        "analysis/p2_core/normalized_comparison.json",
        "docs/p2_persistent_core_audit.md",
    )
    output_hashes = {path: file_hash(root / path) for path in output_paths}
    report = {
        "schema": "a303656-p2-core-independent-verification-v1",
        "status": "PASS",
        "final_conclusion": "VALIDATED P2-PERSISTENT CORE AUDIT",
        "verified_utc": verified_utc,
        "source_commit": source_commit,
        "source_parent_commit": source_parent,
        "results_commit": results_commit,
        "results_commit_resolved": results_commit_resolved,
        "verification_checkout_commit": checkout_commit,
        "source_commit_is_ancestor_of_results_commit": (
            True if results_commit_resolved else None
        ),
        "source_file_sha256_at_source_commit": source_hashes,
        "independent_verifier": {
            "path": "src/verify_p2_persistent_core.py",
            "sha256": source_hashes["src/verify_p2_persistent_core.py"],
            "imports_primary_analysis_module": False,
        },
        "checks": checks,
        "counts": {
            "declared_input_hashes_checked": declared_hash_count,
            "reported_factorizations_checked": factorization_count,
            "reported_obstruction_primes_checked": obstruction_count,
            "active_pairs_per_fixture": 407,
            "distinct_analyzed_n": len(fixtures),
            "coverage_csv_rows_checked": coverage_rows,
            "greedy_rows_checked": greedy_rows,
            "residue_bindings_checked": binding_count,
            "normalized_fixtures_checked": normalized_fixture_count,
        },
        "prime_3_valuation_distribution": {
            str(e): distribution[e] for e in sorted(distribution)
        },
        "activation_cell": {"A": a, "B": b, "next_activation": next_level},
        "corrected_controls": selected_controls,
        "duplicate_controls": duplicates,
        "baseline_hashes": baseline_hashes,
        "output_sha256": output_hashes,
        "scope_confirmation": {
            "counting_executable_invoked_by_verifier": False,
            "new_integer_interval_scanned": False,
            "CRT_system_solved": False,
            "arithmetic_progression_searched": False,
            "T_evaluated_at_progression_candidates": False,
        },
    }
    report_path = output_root / "analysis/p2_core/verification_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    dump_json(report_path, report)
    print("P2_INDEPENDENT_VERIFICATION_PASS")
    print(f"checks={len(checks)}")
    print(f"coverage_rows={coverage_rows}")
    print("final_conclusion=VALIDATED P2-PERSISTENT CORE AUDIT")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("run",))
    parser.add_argument("--verified-utc", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--results-commit")
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output_root = args.output_root.resolve() if args.output_root else root
    run(
        root,
        output_root,
        args.verified_utc,
        args.source_commit,
        args.results_commit,
    )


if __name__ == "__main__":
    main()
