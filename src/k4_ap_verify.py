#!/usr/bin/env python3
"""Independent fail-closed verifier for the bounded K4 AP pilot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


N0 = 240000005594
H_VALUES = (-720, -360, 0, 360, 720)
K_LOW, K_HIGH = -128, 128
ACTIVE = 407
P4 = (3, 7, 11, 23)
M4 = 28227969
P4_COVERED = 216
CELL = (183968950234, 246731069451)
SOURCE_PARENT = "2f87e5fa431eb96166eed57809013dee84b492d2"
RESULT_SENTINEL = "RESULT_COMMIT_CONTAINING_THIS_FILE"
FIXED_DIRECT_K = (-128, -96, -64, -32, -1, 0, 1, 32, 64, 96, 128)
COUNT_FIELDS = ["h", "k", "n", "T", "active_pairs"]
COMPARISON_FIELDS = [
    "h", "k", "n", "backend_a_T", "backend_b_T", "active_pairs", "pointwise_equal"
]
MATCHED_FIELDS = [
    "k", "target_T", "control_h_-720_T", "control_h_-360_T",
    "control_h_360_T", "control_h_720_T", "control_median",
    "control_minimum", "control_maximum", "target_minus_control_median",
    "target_rank_among_five", "target_unique_minimum", "target_tied_minimum",
    "target_below_all_four_controls", "target_below_at_least_three_controls",
]
REQUIRED_ARTIFACTS = {
    "backend_a_counts.csv", "backend_b_counts.csv", "pointwise_comparison.csv",
    "class_summaries.json", "matched_k_comparison.csv",
    "persistent_core_by_class.json", "direct_verification.json", "metadata.json",
}
IMPLEMENTATIONS = {
    "backend_a": (
        "k4_ap_backend_a_trial_division_v1", "src/k4_ap_backend_a.cpp"
    ),
    "backend_b": (
        "k4_ap_backend_b_cpp17_mr7_brent_rho_v1", "src/k4_ap_backend_b.cpp"
    ),
    "direct_oracle": ("k4_ap_direct_oracle_v1", "src/k4_ap_direct_oracle.cpp"),
}
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1 << 20), b""):
                digest.update(block)
    except OSError as exc:
        raise VerificationFailure(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def reject_constant(value: str) -> None:
    raise VerificationFailure(f"non-finite JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationFailure(f"malformed JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def jint(value: Any, label: str, *, nonnegative: bool = False) -> int:
    require(type(value) is int, f"integer required for {label}")
    if nonnegative:
        require(value >= 0, f"negative {label}")
    return value


def cint(value: str, label: str, *, nonnegative: bool = False) -> int:
    require(value != "" and value.strip() == value, f"malformed {label}")
    require(not value.startswith("+"), f"malformed {label}: leading plus")
    digits = value[1:] if value.startswith("-") else value
    require(digits.isascii() and digits.isdigit(), f"malformed {label}")
    require(len(digits) == 1 or not digits.startswith("0"), f"malformed {label}: leading zero")
    parsed = int(value)
    if nonnegative:
        require(parsed >= 0, f"negative {label}")
    return parsed


def exact_keys(value: dict[str, Any], keys: Iterable[str], label: str) -> None:
    expected = set(keys)
    require(set(value) == expected, f"{label} key set mismatch")


def git(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", *arguments], cwd=root, check=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationFailure(f"git invocation failed: {exc}") from exc
    if check and result.returncode != 0:
        diagnostic = result.stderr.decode("utf-8", "replace").strip()
        raise VerificationFailure(f"git {' '.join(arguments)} failed: {diagnostic}")
    return result


def git_text(root: Path, *arguments: str) -> str:
    return git(root, *arguments).stdout.decode("ascii").strip()


def validate_commit_chain(
    root: Path, source_commit: str, results_commit: str, metadata: dict[str, Any]
) -> dict[str, Any]:
    require(COMMIT_RE.fullmatch(source_commit) is not None, "source commit is not a full SHA")
    git(root, "cat-file", "-e", f"{source_commit}^{{commit}}")
    source_parents = git_text(root, "rev-list", "--parents", "-n", "1", source_commit).split()
    require(source_parents == [source_commit, SOURCE_PARENT], "source commit parent mismatch")
    require(metadata.get("source_commit") == source_commit, "source-commit mismatch")
    require(metadata.get("source_parent_commit") == SOURCE_PARENT, "metadata source parent mismatch")
    require(metadata.get("results_commit") == RESULT_SENTINEL, "results-commit sentinel mismatch")
    if results_commit == RESULT_SENTINEL:
        require(git_text(root, "rev-parse", "HEAD") == source_commit,
                "deferred results sentinel is allowed only at source commit HEAD")
        return {
            "source_commit": source_commit,
            "source_parent_commit": SOURCE_PARENT,
            "results_commit": RESULT_SENTINEL,
            "resolution": "DEFERRED_UNTIL_RESULTS_COMMIT_REPLAY",
            "parent_chain_verified": True,
        }
    require(COMMIT_RE.fullmatch(results_commit) is not None, "results commit is not a full SHA")
    git(root, "cat-file", "-e", f"{results_commit}^{{commit}}")
    require(git_text(root, "rev-parse", "HEAD") == results_commit,
            "fresh replay HEAD does not equal results commit")
    result_parents = git_text(root, "rev-list", "--parents", "-n", "1", results_commit).split()
    require(result_parents == [results_commit, source_commit], "results commit is not the child of source commit")
    require(git(root, "merge-base", "--is-ancestor", source_commit, results_commit, check=False).returncode == 0,
            "source commit is not an ancestor of results commit")
    committed = git(root, "show", f"{results_commit}:analysis/k4_ap_pilot/metadata.json").stdout
    require(sha256_bytes(committed) == sha256_file(Path(metadata["_path"])),
            "metadata does not match results-commit blob")
    return {
        "source_commit": source_commit,
        "source_parent_commit": SOURCE_PARENT,
        "results_commit": results_commit,
        "metadata_sentinel": RESULT_SENTINEL,
        "resolution": "RESOLVED_TO_COMMIT_CONTAINING_METADATA",
        "parent_chain_verified": True,
    }


def powers(base: int, limit: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    exponent, value = 0, 1
    while value <= limit:
        result.append((exponent, value))
        if value > limit // base:
            break
        exponent += 1
        value *= base
    return result


def active_pairs(n: int) -> list[tuple[int, int, int]]:
    return [
        (c, d, p3 + p5)
        for c, p3 in powers(3, n)
        for d, p5 in powers(5, n)
        if p3 + p5 <= n
    ]


def panel() -> list[dict[str, int]]:
    rows = [
        {"h": h, "k": k, "n": N0 + h + k * M4, "active_pairs": ACTIVE}
        for h in H_VALUES for k in range(K_LOW, K_HIGH + 1)
    ]
    require(len(rows) == 1285 and len({row["n"] for row in rows}) == 1285,
            "independent panel cardinality/uniqueness failure")
    require(all(CELL[0] <= row["n"] <= CELL[1] for row in rows), "panel outside activation cell")
    require(len({(N0 + h) % M4 for h in H_VALUES}) == 5, "residue classes are not distinct")
    require(all(h % 360 == 0 for h in H_VALUES), "control congruence failure")
    domains = [active_pairs(min(row["n"] for row in rows)), active_pairs(max(row["n"] for row in rows))]
    require(domains[0] == domains[1] and len(domains[0]) == ACTIVE,
            "active exponent-pair domain changes in panel")
    duplicates = Counter(shift for _, _, shift in domains[0])
    require({shift: count for shift, count in duplicates.items() if count > 1} == {28: 2},
            "duplicate shift 28 invariant failed")
    return rows


def read_counts(path: Path, expected: list[dict[str, int]]) -> list[dict[str, int]]:
    try:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == COUNT_FIELDS, f"counts header mismatch: {path.name}")
            result = []
            for line, raw in enumerate(reader, 2):
                require(None not in raw and all(value is not None for value in raw.values()),
                        f"malformed counts row {path.name}:{line}")
                result.append({
                    "h": cint(raw["h"], "h"), "k": cint(raw["k"], "k"),
                    "n": cint(raw["n"], "n", nonnegative=True),
                    "T": cint(raw["T"], "T", nonnegative=True),
                    "active_pairs": cint(raw["active_pairs"], "active_pairs", nonnegative=True),
                })
    except (OSError, UnicodeError, csv.Error) as exc:
        raise VerificationFailure(f"cannot parse counts {path}: {exc}") from exc
    require(len(result) == 1285, f"omitted or extra point in {path.name}")
    require(len({row["n"] for row in result}) == 1285, f"duplicated n in {path.name}")
    for wanted, observed in zip(expected, result):
        require(all(observed[key] == wanted[key] for key in ("h", "k", "n", "active_pairs")),
                f"altered h/k/n/active count in {path.name}")
        require(0 <= observed["T"] <= ACTIVE, f"T outside active domain in {path.name}")
    return result


def verify_pointwise(path: Path, a_rows: list[dict[str, int]], b_rows: list[dict[str, int]]) -> None:
    require(a_rows == b_rows, "backend A/B full T arrays disagree point-by-point")
    try:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == COMPARISON_FIELDS, "pointwise comparison header mismatch")
            raw_rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise VerificationFailure(f"cannot parse pointwise comparison: {exc}") from exc
    require(len(raw_rows) == 1285, "pointwise comparison completeness mismatch")
    for raw, a, b in zip(raw_rows, a_rows, b_rows):
        observed = [
            cint(raw["h"], "comparison h"), cint(raw["k"], "comparison k"),
            cint(raw["n"], "comparison n", nonnegative=True),
            cint(raw["backend_a_T"], "comparison backend A T", nonnegative=True),
            cint(raw["backend_b_T"], "comparison backend B T", nonnegative=True),
            cint(raw["active_pairs"], "comparison active", nonnegative=True),
            cint(raw["pointwise_equal"], "comparison equality", nonnegative=True),
        ]
        require(observed == [a["h"], a["k"], a["n"], a["T"], b["T"], ACTIVE, 1],
                "pointwise comparison row mismatch")


def decimal_fraction(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 30
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def exact_number(value: Fraction) -> dict[str, Any]:
    return {"numerator": value.numerator, "denominator": value.denominator,
            "decimal": decimal_fraction(value)}


def inverse_ecdf(values: list[int], percent: int) -> int:
    ordered = sorted(values)
    rank = max(1, (percent * len(ordered) + 99) // 100)
    return ordered[rank - 1]


def summary(rows: list[dict[str, int]]) -> dict[str, Any]:
    require(bool(rows), "empty summary row set")
    values = [row["T"] for row in rows]
    count = len(values)
    minimum = min(values)
    mean = Fraction(sum(values), count)
    variance = sum((Fraction(value) - mean) ** 2 for value in values) / count
    with localcontext() as context:
        context.prec = 50
        std = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    ordered = sorted(values)
    median = (Fraction(ordered[count // 2]) if count % 2 else
              Fraction(ordered[count // 2 - 1] + ordered[count // 2], 2))
    thresholds = {}
    for threshold in (16, 18, 20, 25, 30):
        hits = sum(value <= threshold for value in values)
        thresholds[str(threshold)] = {"count": hits, "proportion": exact_number(Fraction(hits, count))}
    return {
        "point_count": count,
        "minimum": minimum,
        "argmin": [{"h": row["h"], "k": row["k"], "n": row["n"]}
                   for row in rows if row["T"] == minimum],
        "maximum": max(values), "mean": exact_number(mean),
        "population_standard_deviation": format(std, "f"),
        "population_variance": exact_number(variance), "median": exact_number(median),
        "inverse_empirical_cdf_quantiles_percent": {
            str(q): inverse_ecdf(values, q) for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)
        },
        "thresholds": thresholds,
        "histogram": {str(key): value for key, value in sorted(Counter(values).items())},
    }


def half_string(twice: int) -> str:
    sign, absolute = ("-", -twice) if twice < 0 else ("", twice)
    return f"{sign}{absolute // 2}" if absolute % 2 == 0 else f"{sign}{absolute // 2}.5"


def expected_matched(rows: list[dict[str, int]]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    by_hk = {(row["h"], row["k"]): row["T"] for row in rows}
    full: list[dict[str, Any]] = []
    for k in range(K_LOW, K_HIGH + 1):
        target = by_hk[(0, k)]
        controls = [by_hk[(h, k)] for h in H_VALUES if h]
        ordered = sorted(controls)
        median_twice = ordered[1] + ordered[2]
        difference_twice = 2 * target - median_twice
        equal_controls = sum(value == target for value in controls)
        greater_controls = sum(value > target for value in controls)
        full.append({
            "k": k, "target_T": target,
            "control_h_-720_T": controls[0], "control_h_-360_T": controls[1],
            "control_h_360_T": controls[2], "control_h_720_T": controls[3],
            "control_median": half_string(median_twice), "control_minimum": min(controls),
            "control_maximum": max(controls),
            "target_minus_control_median": half_string(difference_twice),
            "target_rank_among_five": 1 + sum(value < target for value in controls),
            "target_unique_minimum": int(greater_controls == 4),
            "target_tied_minimum": int(equal_controls > 0 and not any(value < target for value in controls)),
            "target_below_all_four_controls": int(greater_controls == 4),
            "target_below_at_least_three_controls": int(greater_controls >= 3),
            "_twice": difference_twice,
        })

    def aggregate(selected: list[dict[str, Any]]) -> dict[str, Any]:
        twice = [row["_twice"] for row in selected]
        ordered = sorted(twice)
        middle = (Fraction(ordered[len(ordered) // 2]) if len(ordered) % 2 else
                  Fraction(ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2], 2))
        longest = current = 0
        for value in twice:
            current = current + 1 if value < 0 else 0
            longest = max(longest, current)
        return {
            "point_count": len(selected),
            "mean_target_minus_control_median": exact_number(Fraction(sum(twice), 2 * len(twice))),
            "median_target_minus_control_median": exact_number(middle / 2),
            "negative_differences": sum(value < 0 for value in twice),
            "zero_differences": sum(value == 0 for value in twice),
            "positive_differences": sum(value > 0 for value in twice),
            "unique_minimum_cases": sum(row["target_unique_minimum"] for row in selected),
            "tied_minimum_cases": sum(row["target_tied_minimum"] for row in selected),
            "below_all_four_controls_cases": sum(row["target_below_all_four_controls"] for row in selected),
            "below_at_least_three_controls_cases": sum(row["target_below_at_least_three_controls"] for row in selected),
            "longest_consecutive_negative_difference_run": longest,
        }

    csv_rows = [{key: str(row[key]) for key in MATCHED_FIELDS} for row in full]
    return csv_rows, {
        "including_anchor_k0": aggregate(full),
        "leave_anchor_out": aggregate([row for row in full if row["k"] != 0]),
    }


def verify_summaries(artifact_dir: Path, rows: list[dict[str, int]]) -> dict[str, Any]:
    expected: dict[str, Any] = {
        "schema": "a303656-k4-ap-class-summaries-v1",
        "classification": "EXACT FINITE DESCRIPTIVE COMPUTATION",
        "quantile_definition": "inverse empirical CDF: order statistic at rank ceil(q*N)",
        "classes": {},
    }
    for h in H_VALUES:
        selected = [row for row in rows if row["h"] == h]
        expected["classes"][str(h)] = (
            {"role": "TARGET", "including_anchor_k0": summary(selected),
             "leave_anchor_out": summary([row for row in selected if row["k"] != 0])}
            if h == 0 else {"role": "CONTROL", "all_points": summary(selected)}
        )
    expected_csv, aggregate = expected_matched(rows)
    expected["matched_k_aggregate"] = aggregate
    require(load_json(artifact_dir / "class_summaries.json") == expected,
            "class summaries or target/control labels mismatch")
    try:
        with (artifact_dir / "matched_k_comparison.csv").open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == MATCHED_FIELDS, "matched-k header mismatch")
            observed = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise VerificationFailure(f"cannot parse matched-k comparison: {exc}") from exc
    require(observed == expected_csv, "matched-k comparison is incomplete or incorrect")
    return aggregate


def verify_core(source_root: Path, metadata_core: Any) -> dict[str, Any]:
    require(isinstance(metadata_core, dict), "metadata core object missing")
    p2 = source_root / "analysis/p2_core"
    try:
        with (p2 / "greedy_core_steps.csv").open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise VerificationFailure(f"cannot read P2 greedy artifact: {exc}") from exc
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get("ordering", ""), []).append(row)
    orderings = ("MARGINAL_COVERAGE_GREEDY", "COVERAGE_PER_MODULUS_BIT_GREEDY")
    first_four = {}
    for ordering in orderings:
        require(ordering in grouped, f"missing greedy ordering {ordering}")
        grouped[ordering].sort(key=lambda row: cint(row["step"], "greedy step", nonnegative=True))
        require(len(grouped[ordering]) >= 4, f"short greedy ordering {ordering}")
        first_four[ordering] = [cint(row["selected_prime"], "selected prime", nonnegative=True)
                                for row in grouped[ordering][:4]]
        fourth = grouped[ordering][3]
        require(cint(fourth["product_M"], "committed M4", nonnegative=True) == M4,
                "committed M4 mismatch")
        require(cint(fourth["cumulative_covered_active_pairs"], "P4 coverage", nonnegative=True) == P4_COVERED,
                "committed P4 coverage mismatch")
        require(cint(fourth["active_pair_count"], "active pair count", nonnegative=True) == ACTIVE,
                "committed active-pair mismatch")
    require(first_four[orderings[0]] == first_four[orderings[1]] == list(P4),
            "both greedy orderings do not reproduce P4")
    activation = load_json(p2 / "activation_cell.json").get("cell")
    require(isinstance(activation, dict), "activation cell object missing")
    require((jint(activation.get("A"), "cell A"), jint(activation.get("B"), "cell B")) == CELL,
            "activation cell bounds mismatch")
    require(jint(activation.get("active_pair_count"), "cell active count") == ACTIVE,
            "activation cell active count mismatch")
    n0_core = load_json(p2 / "n0_p2_core.json")
    require(jint(n0_core.get("n0"), "P2 n0") == N0, "P2 n0 mismatch")
    bindings = n0_core.get("selected_prime_residue_bindings")
    require(isinstance(bindings, list), "P2 residue bindings missing")
    by_prime = {jint(item.get("prime"), "binding prime"): item for item in bindings
                if isinstance(item, dict)}
    for prime in P4:
        binding = by_prime.get(prime)
        require(binding is not None, f"missing binding for p={prime}")
        require(jint(binding.get("p_squared"), "p squared") == prime * prime,
                f"p-squared mismatch for p={prime}")
        require(jint(binding.get("t_p"), "binding residue") == N0 % (prime * prime),
                f"target residue mismatch for p={prime}")
        require(binding.get("direct_binding_verified") is True, f"unverified binding for p={prime}")
    require(n0_core.get("combined_congruence") == "n == n0 (mod M)", "combined congruence mismatch")
    files = ("greedy_core_steps.csv", "activation_cell.json", "n0_p2_core.json",
             "metadata.json", "verification_report.json")
    rebuilt = {
        "p4": list(P4), "m4": M4, "target_residue_mod_m4": N0 % M4,
        "four_prime_persistent_covered_active_pairs": P4_COVERED,
        "active_pair_count": ACTIVE, "activation_cell": list(CELL),
        "greedy_first_four": first_four,
        "artifact_sha256": {f"analysis/p2_core/{name}": sha256_file(p2 / name) for name in files},
    }
    require(metadata_core == rebuilt, "metadata P4/M4/core reproduction mismatch")
    return rebuilt


def expected_persistent(rows: list[dict[str, int]], core: dict[str, Any]) -> dict[str, Any]:
    domain = active_pairs(min(row["n"] for row in rows))
    by_hk = {(row["h"], row["k"]): row for row in rows}
    result: dict[str, Any] = {
        "schema": "a303656-k4-persistent-core-by-class-v1",
        "classification": "EXACT FINITE COMPUTATION ON FIVE FIXED RESIDUE CLASSES",
        "p4": core["p4"], "m4": core["m4"], "classes": [],
    }
    for h in H_VALUES:
        base = N0 + h
        coverage = {
            prime: {(c, d) for c, d, shift in domain
                    if (base - shift) % prime == 0 and (base - shift) % (prime * prime) != 0}
            for prime in P4
        }
        for prime in P4:
            require(all((N0 + h + k * M4) % (prime * prime) == base % (prime * prime)
                        for k in range(K_LOW, K_HIGH + 1)), "persistent set changed across k")
        union = set().union(*coverage.values())
        multiplicities = Counter(sum(pair in coverage[p] for p in P4) for pair in union)
        result["classes"].append({
            "h": h, "base_n": base, "residue_mod_m4": base % M4,
            "residue_mod_p_squared": {str(p): base % (p * p) for p in P4},
            "persistent_covered_active_pair_count": len(union),
            "persistent_covered_active_pairs": [f"{c}:{d}" for c, d in sorted(union)],
            "current_loser_count_at_k0": ACTIVE - by_hk[(h, 0)]["T"],
            "persistent_covered_current_loser_count_at_k0": len(union),
            "uncovered_active_pair_count": ACTIVE - len(union),
            "uncovered_active_pairs": [f"{c}:{d}" for c, d, _ in domain if (c, d) not in union],
            "per_prime_covered_count": {str(p): len(coverage[p]) for p in P4},
            "pairwise_duplicate_coverage_intersections": {
                f"{p}_{q}": len(coverage[p] & coverage[q])
                for index, p in enumerate(P4) for q in P4[index + 1:]
            },
            "coverage_multiplicity_histogram": {str(k): v for k, v in sorted(multiplicities.items())},
            "multiply_covered_pairs": [
                {"pair": f"{c}:{d}", "primes": [p for p in P4 if (c, d) in coverage[p]]}
                for c, d in sorted(union) if sum((c, d) in coverage[p] for p in P4) > 1
            ],
            "guaranteed_pair_set_constant_for_all_257_k": True,
        })
    require(next(item for item in result["classes"] if item["h"] == 0)
            ["persistent_covered_active_pair_count"] == P4_COVERED,
            "target persistent coverage does not equal committed 216")
    return result


def direct_selection(rows: list[dict[str, int]]) -> tuple[list[dict[str, int]], dict[str, Any]]:
    reasons: dict[int, set[str]] = {}
    for row in rows:
        if row["h"] == 0 and row["k"] == 0:
            reasons.setdefault(row["n"], set()).add("anchor_n0")
        if row["k"] in FIXED_DIRECT_K:
            reasons.setdefault(row["n"], set()).add("fixed_k")
        if row["T"] <= 25:
            reasons.setdefault(row["n"], set()).add("T_le_25")
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        minimum = min(row["T"] for row in class_rows)
        for row in class_rows:
            if row["T"] == minimum:
                reasons.setdefault(row["n"], set()).add("class_argmin")
    selected = [row for row in rows if row["n"] in reasons]
    selection = {
        "point_count": len(selected), "fixed_k_values": list(FIXED_DIRECT_K),
        "points": [{"h": row["h"], "k": row["k"], "n": row["n"], "T": row["T"],
                    "reasons": sorted(reasons[row["n"]])} for row in selected],
    }
    return selected, selection


def verify_direct(path: Path, rows: list[dict[str, int]]) -> int:
    data = load_json(path)
    selected, selection = direct_selection(rows)
    require(data.get("schema") == "a303656-k4-ap-direct-verification-v1", "direct schema mismatch")
    require(data.get("implementation_id") == IMPLEMENTATIONS["direct_oracle"][0], "direct identity mismatch")
    require(data.get("method") == "factorization-free exact monotone boundary enumeration; canonical least-a witness",
            "direct method mismatch")
    require(jint(data.get("n0"), "direct n0") == N0 and jint(data.get("M4"), "direct M4") == M4,
            "direct n0/M4 mismatch")
    require(jint(data.get("expected_active_pair_count"), "direct active") == ACTIVE,
            "direct active count mismatch")
    require(jint(data.get("point_count"), "direct point count") == len(selected),
            "direct point count mismatch")
    require(data.get("all_points_processed") is True and data.get("expected_T_agreement") is True,
            "direct oracle did not report complete agreement")
    require(data.get("selection") == selection, "direct selection rule is incomplete")
    require(data.get("runner_witness_validation") == {
        "status": "PASS", "point_count": len(selected), "all_exact_T_values_match": True,
        "all_complete_winner_lists_match_T": True,
        "all_witness_equations_and_a_le_b": True,
    }, "runner direct validation record mismatch")
    points = data.get("points")
    require(isinstance(points, list) and len(points) == len(selected), "direct points omitted or added")
    domain = {(c, d): shift for c, d, shift in active_pairs(min(row["n"] for row in rows))}
    for point, expected in zip(points, selected):
        require(isinstance(point, dict), "direct point is not an object")
        require(jint(point.get("h"), "direct h") == expected["h"] and
                jint(point.get("k"), "direct k") == expected["k"] and
                jint(point.get("n"), "direct n") == expected["n"], "direct point identity mismatch")
        t_value = jint(point.get("T"), "direct T", nonnegative=True)
        require(t_value == expected["T"] == jint(point.get("expected_T"), "direct expected T"),
                "direct T mismatch")
        require(jint(point.get("active_pair_count"), "direct active count") == ACTIVE,
                "direct point active count mismatch")
        require(point.get("expected_T_match") is True, "direct point expected-T flag mismatch")
        elapsed = point.get("elapsed_seconds")
        require(type(elapsed) in (int, float) and not isinstance(elapsed, bool) and math.isfinite(elapsed) and elapsed >= 0,
                "invalid direct elapsed time")
        winners = point.get("winning_exponent_pairs")
        require(isinstance(winners, list) and len(winners) == t_value, "direct winner-list/T mismatch")
        seen: set[tuple[int, int]] = set()
        last = (-1, -1)
        for winner in winners:
            require(isinstance(winner, dict), "direct winner is not an object")
            c = jint(winner.get("c"), "winner c", nonnegative=True)
            d = jint(winner.get("d"), "winner d", nonnegative=True)
            shift = jint(winner.get("shift"), "winner shift", nonnegative=True)
            remainder = jint(winner.get("remainder"), "winner remainder", nonnegative=True)
            a = jint(winner.get("a"), "winner a", nonnegative=True)
            b = jint(winner.get("b"), "winner b", nonnegative=True)
            require((c, d) in domain and domain[(c, d)] == shift, "direct winner source identity mismatch")
            require((c, d) not in seen and (c, d) > last, "duplicate/unsorted direct winner")
            seen.add((c, d)); last = (c, d)
            require(remainder == expected["n"] - shift and a <= b, "direct remainder/canonical order mismatch")
            require(a * a + b * b + pow(3, c) + pow(5, d) == expected["n"],
                    "direct witness equation mismatch")
    return len(selected)


def reconstructed_panel_hash(expected: list[dict[str, int]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=["h", "k", "n", "active_pairs"], lineterminator="\n")
    writer.writeheader(); writer.writerows(expected)
    return sha256_bytes(stream.getvalue().encode("utf-8"))


def binary_identity(path: Path) -> str:
    require(path.is_file(), f"missing executable: {path}")
    try:
        result = subprocess.run([str(path), "--implementation-id"], check=False, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationFailure(f"cannot query binary identity {path}: {exc}") from exc
    require(result.returncode == 0, f"binary identity query failed: {path}")
    require(result.stderr == "", f"binary identity query wrote stderr: {path}")
    return result.stdout.strip()


def verify_provenance(
    source_root: Path, artifact_dir: Path, metadata: dict[str, Any],
    source_commit: str, binaries: dict[str, Path], chain: dict[str, Any],
) -> dict[str, str]:
    require(metadata.get("schema") == "a303656-k4-ap-pilot-metadata-v1", "metadata schema mismatch")
    require(metadata.get("task") == "K4 ARITHMETIC-PROGRESSION ENRICHMENT PILOT", "metadata task mismatch")
    require(metadata.get("classification") == "EXACT FINITE COMPUTATION; GLOBAL PROBLEM UNRESOLVED",
            "metadata classification mismatch")
    identities = metadata.get("backend_identities")
    require(isinstance(identities, dict) and set(identities) == set(IMPLEMENTATIONS),
            "backend identity slots mismatch")
    observed_hashes: dict[str, str] = {}
    for label, (implementation_id, source_relative) in IMPLEMENTATIONS.items():
        record = identities[label]
        require(isinstance(record, dict), f"identity record missing for {label}")
        require(record.get("implementation_id") == implementation_id, f"{label} implementation relabel")
        require(record.get("source_path") == source_relative, f"{label} source path mismatch")
        source_path = source_root / source_relative
        source_hash = sha256_file(source_path)
        require(record.get("source_sha256") == source_hash, f"{label} source hash mismatch")
        committed_source = git(source_root, "show", f"{source_commit}:{source_relative}").stdout
        require(sha256_bytes(committed_source) == source_hash, f"{label} source differs from source commit")
        binary_hash = sha256_file(binaries[label])
        require(record.get("binary_sha256") == binary_hash, f"{label} binary replacement/hash mismatch")
        require(binary_identity(binaries[label]) == implementation_id, f"{label} binary slot identity mismatch")
        observed_hashes[label] = binary_hash
    tool_hashes = metadata.get("tool_source_hashes")
    expected_tool_paths = {
        "src/k4_ap_backend_a.cpp", "src/k4_ap_backend_b.cpp", "src/k4_ap_direct_oracle.cpp",
        "src/k4_ap_run.py", "src/k4_ap_verify.py",
    }
    require(isinstance(tool_hashes, dict) and set(tool_hashes) == expected_tool_paths,
            "tool source hash manifest mismatch")
    for relative, expected_hash in tool_hashes.items():
        current = sha256_file(source_root / relative)
        require(expected_hash == current, f"tool source hash mismatch: {relative}")
        require(sha256_bytes(git(source_root, "show", f"{source_commit}:{relative}").stdout) == current,
                f"tool source not bound to source commit: {relative}")
    artifact_hashes = metadata.get("artifact_sha256_before_metadata_and_verification_report")
    expected_names = REQUIRED_ARTIFACTS - {"metadata.json"}
    require(isinstance(artifact_hashes, dict) and set(artifact_hashes) == expected_names,
            "artifact hash manifest key mismatch")
    for name, digest in artifact_hashes.items():
        require(SHA_RE.fullmatch(str(digest)) is not None and sha256_file(artifact_dir / name) == digest,
                f"artifact tamper/hash mismatch: {name}")
    if chain["resolution"] == "RESOLVED_TO_COMMIT_CONTAINING_METADATA":
        results_commit = chain["results_commit"]
        for name in sorted(REQUIRED_ARTIFACTS):
            require(sha256_bytes(git(source_root, "show", f"{results_commit}:analysis/k4_ap_pilot/{name}").stdout)
                    == sha256_file(artifact_dir / name), f"artifact differs from results commit: {name}")
    return observed_hashes


def verify_protected(source_root: Path, metadata: dict[str, Any]) -> None:
    p2_metadata = load_json(source_root / "analysis/p2_core/metadata.json")
    manifest = p2_metadata.get("fixed_input_audit", {}).get("fixed_input_tree_sha256")
    require(isinstance(manifest, dict) and bool(manifest), "protected-input manifest missing")
    for relative, digest in manifest.items():
        require(SHA_RE.fullmatch(str(digest)) is not None and sha256_file(source_root / relative) == digest,
                f"protected baseline/pilot changed: {relative}")
    canonical = "".join(f"{manifest[path]}  {path}\n" for path in sorted(manifest))
    expected = {"file_count": len(manifest), "manifest_sha256": sha256_bytes(canonical.encode()),
                "mismatch_count": 0, "all_byte_identical": True}
    require(metadata.get("protected_prior_baseline_and_pilot_hashes_before") == expected,
            "protected-input before record mismatch")
    require(metadata.get("protected_prior_baseline_and_pilot_hashes_after") == expected,
            "protected-input after record mismatch")


def verify_metadata_claims(
    metadata: dict[str, Any], expected_panel: list[dict[str, int]], direct_count: int
) -> None:
    expected_panel_record = {
        "formula": "n(h,k)=240000005594+h+k*28227969", "h_values": list(H_VALUES),
        "k_interval": [K_LOW, K_HIGH], "points_per_class": 257, "point_count": 1285,
        "unique_integer_count": 1285, "minimum_n": min(row["n"] for row in expected_panel),
        "maximum_n": max(row["n"] for row in expected_panel), "all_inside_activation_cell": True,
        "all_active_pair_count": ACTIVE, "five_distinct_residues_mod_m4": True,
        "control_offsets_congruent_zero_mod_360": True,
        "duplicate_shift": {"shift": 28, "source_pairs": [[1, 2], [3, 0]]},
        "panel_csv_sha256": reconstructed_panel_hash(expected_panel),
    }
    require(metadata.get("panel") == expected_panel_record, "metadata exact panel claim mismatch")
    require(metadata.get("pointwise_comparison") == {"point_count": 1285, "all_equal": True, "mismatch_count": 0},
            "metadata pointwise claim mismatch")
    require(metadata.get("direct_verification") == {
        "selected_point_count": direct_count, "all_exact_T_values_match": True,
        "all_witnesses_valid": True, "selection_rule_complete": True,
    }, "metadata direct-verification claim mismatch")
    commands = metadata.get("commands")
    require(isinstance(commands, list) and len(commands) == 3, "metadata command record count mismatch")
    require([item.get("label") for item in commands if isinstance(item, dict)] ==
            ["backend_a", "backend_b", "direct_oracle"], "metadata command labels mismatch")
    require(all(type(item.get("return_code")) is int and item["return_code"] == 0 for item in commands),
            "metadata records a nonzero/malformed command return code")
    archive = metadata.get("raw_log_archive")
    require(isinstance(archive, dict), "raw-log archive metadata missing")
    require(archive.get("policy") ==
            "Logs remain external under ~/code/a303656/archive; only archive name and SHA256 are committed.",
            "raw-log archive policy mismatch")
    require(isinstance(archive.get("archive_name"), str) and archive["archive_name"] not in
            ("", "PENDING_EXTERNAL_ARCHIVE"), "raw-log archive name unresolved")
    require(SHA_RE.fullmatch(str(archive.get("sha256"))) is not None,
            "raw-log archive SHA256 unresolved/malformed")
    require(metadata.get("scope_guards") == {
        "formal_points_evaluated_by_each_full_backend": 1285,
        "other_formal_points_evaluated": 0, "adaptive_points_added": 0,
        "CRT_system_solved": False, "neighboring_residue_classes_scanned": False,
        "complete_activation_cell_scanned": False,
    }, "scope-guard metadata mismatch")
    require(isinstance(metadata.get("generated_utc"), str) and metadata["generated_utc"].endswith("Z"),
            "generated UTC timestamp malformed")


def atomic_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    except OSError as exc:
        raise VerificationFailure(f"cannot write verification report: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--results-commit", required=True)
    parser.add_argument("--backend-a", type=Path, required=True)
    parser.add_argument("--backend-b", type=Path, required=True)
    parser.add_argument("--direct-oracle", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    artifact_dir, source_root = args.artifact_dir.resolve(), args.source_root.resolve()
    require(artifact_dir.is_dir() and source_root.is_dir(), "artifact/source directory missing")
    missing = sorted(name for name in REQUIRED_ARTIFACTS if not (artifact_dir / name).is_file())
    require(not missing, f"required artifacts missing: {missing}")
    metadata = load_json(artifact_dir / "metadata.json")
    metadata["_path"] = str(artifact_dir / "metadata.json")
    core = verify_core(source_root, metadata.get("core"))
    expected_panel = panel()
    a_rows = read_counts(artifact_dir / "backend_a_counts.csv", expected_panel)
    b_rows = read_counts(artifact_dir / "backend_b_counts.csv", expected_panel)
    verify_pointwise(artifact_dir / "pointwise_comparison.csv", a_rows, b_rows)
    matched = verify_summaries(artifact_dir, a_rows)
    require(load_json(artifact_dir / "persistent_core_by_class.json") == expected_persistent(a_rows, core),
            "persistent-core records mismatch")
    direct_count = verify_direct(artifact_dir / "direct_verification.json", a_rows)
    verify_metadata_claims(metadata, expected_panel, direct_count)
    verify_protected(source_root, metadata)
    chain = validate_commit_chain(source_root, args.source_commit, args.results_commit, metadata)
    metadata.pop("_path")
    binaries = {"backend_a": args.backend_a.resolve(), "backend_b": args.backend_b.resolve(),
                "direct_oracle": args.direct_oracle.resolve()}
    binary_hashes = verify_provenance(source_root, artifact_dir, metadata, args.source_commit, binaries, chain)
    report = {
        "schema": "a303656-k4-ap-pilot-verification-report-v1", "status": "PASS",
        "classification": "INDEPENDENTLY VERIFIED EXACT FINITE COMPUTATION; GLOBAL PROBLEM UNRESOLVED",
        "conclusion": "VALIDATED K4 ARITHMETIC-PROGRESSION ENRICHMENT PILOT",
        "commit_chain": chain, "p4": list(P4), "m4": M4,
        "panel": {"point_count": 1285, "unique_integer_count": 1285,
                  "h_values": list(H_VALUES), "k_interval": [K_LOW, K_HIGH],
                  "active_pair_count": ACTIVE, "activation_cell": list(CELL)},
        "backend_pointwise_equality": {"status": "PASS", "point_count": 1285,
                                       "mismatch_count": 0},
        "direct_verification": {"status": "PASS", "selected_point_count": direct_count,
                                "selection_complete": True, "all_witnesses_valid": True},
        "matched_k": {"status": "PASS", "point_count": 257,
                      "leave_anchor_out_point_count": 256,
                      "aggregate": matched},
        "persistent_core": {"status": "PASS", "class_count": 5,
                            "target_covered_active_pairs": P4_COVERED},
        "binary_sha256": binary_hashes,
        "checks": {
            "exact_panel": True, "class_summaries": True, "matched_k_complete": True,
            "persistent_sets_reconstructed": True, "direct_selection_complete": True,
            "direct_winner_identities_and_equations": True, "artifact_hashes": True,
            "source_hashes": True, "binary_identities_and_hashes": True,
            "protected_prior_artifacts_byte_identical": True,
        },
    }
    if args.report is not None:
        atomic_report(args.report.resolve(), report)
    print("K4_AP_PILOT_VERIFICATION_PASS")
    print("formal_points=1285")
    print(f"direct_points={direct_count}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationFailure as exc:
        print(f"K4_AP_PILOT_VERIFICATION_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
