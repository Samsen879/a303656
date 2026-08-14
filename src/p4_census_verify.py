#!/usr/bin/env python3
"""Fail-closed independent verifier for the fixed-P4 census artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import struct
import subprocess
import sys
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from p4_census_common import (
    A, B, CLASS_COUNT, CONSTRAINED_ARGMAX_DIGEST, COUNT_FIELDS, L,
    MASK_BYTES, MAXIMIZER_COUNT, M4, N0, P4, PAIR_COUNT, PANEL_FIELDS,
    START_COMMIT, CensusError, ClassSpec, Pair, construct_panel,
    coverage_set, mask_popcount, panel_digest, read_panel, sha256_file,
    verify_protected,
)


IMPLEMENTATION_ID = "p4_census_independent_verifier_v1"
RESULTS_SENTINEL = "RESULT_COMMIT_CONTAINING_THIS_FILE"
CORE_ARTIFACTS = {
    "metadata.json", "class_panel.csv", "backend_a_counts.csv", "backend_b_counts.csv",
    "backend_a_masks.bin", "backend_b_masks.bin", "class_summaries.json",
    "global_histogram.csv", "coverage_response.json", "common_uncovered.json",
    "pair_frequencies.csv", "direct_verification.json",
}
HEADER = struct.Struct("<8sIIIIII32s32s32s")
EXPECTED_NEGATIVE_TESTS = {
    "missing_maximizing_class", "extra_class", "changed_constrained_tuple", "incorrect_G",
    "altered_CRT_residue", "missing_point", "duplicated_point", "point_outside_activation_cell",
    "point_not_congruent_to_class", "changed_class_ordering", "flipped_mask_bit",
    "popcount_T_mismatch", "persistent_covered_winner", "backend_identity_swap",
    "source_commit_mismatch", "baseline_or_landscape_hash_mismatch",
    "truncated_mask_bytes", "extra_mask_bytes",
}


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise CensusError(message)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def fraction_record(value: Fraction) -> dict[str, Any]:
    with localcontext() as context:
        context.prec = 70
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": format(decimal, ".18f")}


def stddev_record(values: list[int]) -> dict[str, Any]:
    n = len(values)
    variance = Fraction(sum(value * value for value in values), n) - Fraction(sum(values) ** 2, n * n)
    with localcontext() as context:
        context.prec = 70
        decimal = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    return {"variance_numerator": variance.numerator, "variance_denominator": variance.denominator, "decimal": format(decimal, ".18f")}


def median_record(values: list[int]) -> dict[str, Any]:
    ordered = sorted(values)
    n = len(ordered)
    value = Fraction(ordered[n // 2], 1) if n % 2 else Fraction(ordered[n // 2 - 1] + ordered[n // 2], 2)
    return fraction_record(value)


def quantile(values: list[int], percent: int) -> int:
    ordered = sorted(values)
    return ordered[(percent * len(ordered) + 99) // 100 - 1]


def expected_summary(values: list[int], ns: list[int], coverage: int) -> dict[str, Any]:
    minimum = min(values)
    thresholds = (5, 10, 12, 14, 16, 18, 20, 25)
    return {
        "point_count": len(values), "minimum_T": minimum,
        "argmin_n": [n for n, value in zip(ns, values) if value == minimum],
        "maximum_T": max(values), "mean_T": fraction_record(Fraction(sum(values), len(values))),
        "population_standard_deviation_T": stddev_record(values), "median_T": median_record(values),
        "inverse_empirical_cdf": {str(percent): quantile(values, percent) for percent in (10, 25, 50, 75, 90)},
        "counts": {"T=0": values.count(0), **{f"T<={threshold}": sum(value <= threshold for value in values) for threshold in thresholds}},
        "total_winner_incidences": sum(values),
        "residual_survival_rate": fraction_record(Fraction(sum(values), len(values) * (PAIR_COUNT - coverage))),
    }


def verify_git(root: Path, source_commit: str, source_parent: str) -> dict[str, str]:
    demand(len(source_commit) == 40 and all(ch in "0123456789abcdef" for ch in source_commit), "source commit is not a full SHA")
    demand(source_parent == START_COMMIT, "source parent is not the required starting commit")
    for commit in (START_COMMIT, source_commit):
        result = subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        demand(result.returncode == 0, f"commit unavailable: {commit}")
    ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", START_COMMIT, source_commit], cwd=root, check=False)
    demand(ancestor.returncode == 0, "required starting commit is not an ancestor of source commit")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    demand(subprocess.run(["git", "merge-base", "--is-ancestor", source_commit, head], cwd=root, check=False).returncode == 0, "source commit is not an ancestor of HEAD")
    return {"starting_commit": START_COMMIT, "source_commit": source_commit, "head": head}


def read_counts(path: Path, panel: list[dict[str, int | str]]) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        demand(reader.fieldnames == COUNT_FIELDS, f"counts header mismatch: {path.name}")
        raw = list(reader)
    demand(len(raw) == len(panel), f"counts row count mismatch: {path.name}")
    rows: list[dict[str, Any]] = []
    for ordinal, (record, expected) in enumerate(zip(raw, panel)):
        parsed = {"class_id": record["class_id"], "mask_sha256": record["mask_sha256"]}
        for field in COUNT_FIELDS:
            if field not in ("class_id", "mask_sha256"):
                parsed[field] = int(record[field])
        demand({field: parsed[field] for field in PANEL_FIELDS} == expected, f"counts panel mismatch at row {ordinal}")
        demand(0 <= parsed["T"] <= PAIR_COUNT, "T outside active domain")
        rows.append(parsed)
    return rows


def read_masks(
    path: Path, slot: int, core_identity: str, panel_path: Path, pair_hash: str,
    rows: list[dict[str, Any]],
) -> list[bytes]:
    data = path.read_bytes()
    demand(len(data) >= HEADER.size, f"{path.name} truncated header")
    magic, version, backend, header_size, point_count, pair_count, mask_bytes, panel_hash, observed_pair_hash, core_hash = HEADER.unpack(data[:HEADER.size])
    demand((magic, version, backend, header_size) == (b"P4CMASK1", 1, slot, HEADER.size), f"{path.name} backend identity/header mismatch")
    demand((point_count, pair_count, mask_bytes) == (len(rows), PAIR_COUNT, MASK_BYTES), f"{path.name} dimensions mismatch")
    demand(panel_hash.hex() == panel_digest(panel_path), f"{path.name} panel digest mismatch")
    demand(observed_pair_hash.hex() == pair_hash, f"{path.name} pair-order digest mismatch")
    demand(core_hash == hashlib.sha256(core_identity.encode()).digest(), f"{path.name} core identity mismatch")
    demand(len(data) == HEADER.size + len(rows) * MASK_BYTES, f"{path.name} truncated or extra mask bytes")
    masks: list[bytes] = []
    for ordinal, row in enumerate(rows):
        begin = HEADER.size + ordinal * MASK_BYTES
        mask = data[begin:begin + MASK_BYTES]
        demand(row["mask_offset"] == begin, "counts mask offset mismatch")
        demand(row["mask_sha256"] == hashlib.sha256(mask).hexdigest(), "counts mask digest mismatch")
        demand(mask_popcount(mask) == row["T"], "popcount/T mismatch")
        masks.append(mask)
    return masks


def covered_mask(spec: ClassSpec) -> bytes:
    result = bytearray(MASK_BYTES)
    for index in spec.covered:
        result[index // 8] |= 1 << (index % 8)
    return bytes(result)


def verify_class_summaries(
    artifact: dict[str, Any], rows: list[dict[str, Any]], masks: list[bytes], specs: list[ClassSpec]
) -> dict[str, Any]:
    demand(artifact.get("schema") == "a303656-p4-census-class-summaries-v1", "class summaries schema mismatch")
    classes = artifact.get("classes")
    demand(isinstance(classes, list) and len(classes) == CLASS_COUNT, "class summary count mismatch")
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["class_index"]].append(row)
    for spec, item in zip(specs, classes):
        group = grouped[spec.index]
        identity = {
            "class_index": spec.index, "class_id": spec.class_id, "residue_tuple": list(spec.tuple4),
            "G": spec.coverage, "uncovered_pair_count": PAIR_COUNT - spec.coverage,
            "crt_residue_mod_L": spec.residue, "activation_cell_member_count": len(group),
            "persistent_covered_mask_sha256": hashlib.sha256(covered_mask(spec)).hexdigest(),
        }
        for key, value in identity.items():
            demand(item.get(key) == value, f"class summary identity mismatch for {spec.class_id}: {key}")
        expected = expected_summary([row["T"] for row in group], [row["n"] for row in group], spec.coverage)
        for key, value in expected.items():
            demand(item.get(key) == value, f"class summary reconstruction mismatch for {spec.class_id}: {key}")

    maximum_rows = [row for row in rows if row["class_index"] >= 3]
    values = [row["T"] for row in maximum_rows]
    aggregate = artifact.get("aggregate_G231")
    demand(isinstance(aggregate, dict), "aggregate G231 summary missing")
    minimum = min(values)
    demand(aggregate.get("maximizing_class_count") == MAXIMIZER_COUNT and aggregate.get("total_points") == len(maximum_rows), "aggregate G231 cardinality mismatch")
    demand(aggregate.get("global_minimum_T") == minimum, "aggregate global minimum mismatch")
    expected_argmins = [
        {"class_id": row["class_id"], "residue_tuple": [row["t3"], row["t7"], row["t11"], row["t23"]], "point_index": row["point_index"], "n": row["n"]}
        for row in maximum_rows if row["T"] == minimum
    ]
    demand(aggregate.get("global_argmins") == expected_argmins, "aggregate global argmins mismatch")
    histogram = {str(value): count for value, count in sorted(Counter(values).items())}
    demand(aggregate.get("T_histogram") == histogram, "aggregate T histogram mismatch")
    minima = [item["minimum_T"] for item in classes[3:]]
    demand(aggregate.get("class_minima_distribution") == {str(value): count for value, count in sorted(Counter(minima).items())}, "class minima distribution mismatch")
    demand(aggregate.get("class_minimum_threshold_counts") == {f"minimum_T<={threshold}": sum(value <= threshold for value in minima) for threshold in (10, 12, 14, 16, 18, 20)}, "class minimum thresholds mismatch")
    demand(aggregate.get("classes_with_point_below_known_T16") == sum(value < 16 for value in minima), "below-known-T class count mismatch")
    expected_means = sorted(
        ({"class_id": item["class_id"], "mean_T": item["mean_T"]} for item in classes[3:]),
        key=lambda item: (Fraction(item["mean_T"]["numerator"], item["mean_T"]["denominator"]), item["class_id"]),
    )
    demand(aggregate.get("class_means_distribution") == expected_means, "class means distribution mismatch")
    mask_class_ids: dict[str, list[str]] = defaultdict(list)
    for spec in specs[3:]:
        mask_class_ids[hashlib.sha256(covered_mask(spec)).hexdigest()].append(spec.class_id)
    mask_groups = Counter({digest: len(class_ids) for digest, class_ids in mask_class_ids.items()})
    demand(aggregate.get("distinct_persistent_covered_masks") == len(mask_groups), "distinct covered-mask count mismatch")
    expected_mask_groups = [
        {"mask_sha256": digest, "class_count": len(class_ids), "class_ids": class_ids}
        for digest, class_ids in sorted(mask_class_ids.items())
    ]
    demand(aggregate.get("classes_per_persistent_covered_mask") == expected_mask_groups, "covered-mask class grouping mismatch")
    survival = sorted(
        ((Fraction(item["residual_survival_rate"]["numerator"], item["residual_survival_rate"]["denominator"]), item["class_id"], item["residual_survival_rate"]) for item in classes[3:]),
        key=lambda entry: (entry[0], entry[1]),
    )
    demand(aggregate.get("best_residual_survival_rate") == {"class_id": survival[0][1], "rate": survival[0][2]}, "best residual survival rate mismatch")
    demand(aggregate.get("worst_residual_survival_rate") == {"class_id": survival[-1][1], "rate": survival[-1][2]}, "worst residual survival rate mismatch")
    return aggregate


def verify_global_histogram(path: Path, expected: dict[str, int]) -> None:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.reader(stream))
    demand(rows and rows[0] == ["T", "count"], "global histogram header mismatch")
    observed = {row[0]: int(row[1]) for row in rows[1:]}
    demand(observed == expected and len(rows) == len(expected) + 1, "global histogram reconstruction mismatch")


def direct_selection(rows: list[dict[str, Any]]) -> dict[tuple[int, int], list[str]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["class_index"]].append(row)
    reasons: dict[tuple[int, int], set[str]] = defaultdict(set)
    for class_index in range(CLASS_COUNT):
        group = grouped[class_index]
        minimum = min(row["T"] for row in group)
        for row in group:
            key = (class_index, row["point_index"])
            if row["T"] == minimum: reasons[key].add("class_minimum")
            if row["T"] <= 20: reasons[key].add("T<=20")
            if row["T"] <= 16: reasons[key].add("T<=previous_known_16")
        for label, index in (("class_first", 0), ("class_median_lower", (len(group) - 1) // 2), ("class_last", len(group) - 1)):
            reasons[(class_index, group[index]["point_index"])].add(label)
        nearest = min(group, key=lambda row: (abs(row["n"] - N0), row["n"]))
        reasons[(class_index, nearest["point_index"])].add("calibration_nearest_n0" if class_index < 3 else "maximizer_class_nearest_n0")
    return {key: sorted(value) for key, value in reasons.items()}


def verify_direct(path: Path, rows: list[dict[str, Any]], masks: list[bytes], pairs: list[Pair]) -> dict[str, int]:
    direct = load_json(path)
    demand(direct.get("schema") == "a303656-p4-census-direct-verification-v1", "direct artifact schema mismatch")
    demand(direct.get("oracle_implementation_id") == "p4_census_direct_oracle_adapter_v1", "direct oracle identity mismatch")
    reasons = direct_selection(rows)
    points = direct.get("points")
    demand(isinstance(points, list) and len(points) == len(reasons), "direct selected-point cardinality mismatch")
    row_lookup = {(row["class_index"], row["point_index"]): (row, mask) for row, mask in zip(rows, masks)}
    pair_lookup = {(pair.c, pair.d): pair for pair in pairs}
    observed_keys: set[tuple[int, int]] = set()
    witnesses = 0
    for point in points:
        key = (point.get("class_index"), point.get("point_index"))
        demand(key in reasons and key not in observed_keys, "direct point extra/duplicate")
        observed_keys.add(key)
        row, mask = row_lookup[key]
        demand((point.get("class_id"), point.get("n"), point.get("T"), point.get("selection_reasons")) == (row["class_id"], row["n"], row["T"], reasons[key]), "direct point identity/reason mismatch")
        demand(point.get("winner_mask_hex") == mask.hex(), "direct complete mask mismatch")
        winners = point.get("canonical_winners")
        demand(isinstance(winners, list) and len(winners) == row["T"], "direct winner count mismatch")
        seen: set[tuple[int, int]] = set()
        reconstructed = bytearray(MASK_BYTES)
        for winner in winners:
            identity = (winner.get("c"), winner.get("d"))
            pair = pair_lookup.get(identity)
            demand(pair is not None and identity not in seen, "direct winner pair invalid/duplicate")
            seen.add(identity)
            remainder = row["n"] - pair.shift
            a, b = winner.get("a"), winner.get("b")
            demand((winner.get("shift"), winner.get("remainder")) == (pair.shift, remainder), "direct shift/remainder mismatch")
            demand(isinstance(a, int) and isinstance(b, int) and 0 <= a <= b and a * a + b * b == remainder, "direct witness arithmetic mismatch")
            reconstructed[pair.index // 8] |= 1 << (pair.index % 8)
            witnesses += 1
        demand(bytes(reconstructed) == mask, "direct winners do not reconstruct complete mask")
    demand(observed_keys == set(reasons), "direct selection missing points")
    demand(direct.get("selected_point_count") == len(points) and direct.get("verified_complete_mask_count") == len(points) and direct.get("verified_canonical_witness_count") == witnesses, "direct summary counts mismatch")
    zero = [point["n"] for point in points if point["T"] == 0]
    demand(direct.get("T_zero_points") == zero, "direct T=0 list mismatch")
    demand(direct.get("T_zero_label") == ("UNVERIFIED COUNTEREXAMPLE CANDIDATE" if zero else None), "direct T=0 label mismatch")
    return {"selected_point_count": len(points), "witness_count": witnesses}


def verify_common_and_frequencies(
    common_path: Path, frequency_path: Path, rows: list[dict[str, Any]], masks: list[bytes],
    specs: list[ClassSpec], pairs: list[Pair],
) -> dict[str, int]:
    max_specs = specs[3:]
    cover_counts = [sum(pair.index in spec.covered for spec in max_specs) for pair in pairs]
    common_set = {pair.index for pair, count in zip(pairs, cover_counts) if count == 0}
    union = {pair.index for pair, count in zip(pairs, cover_counts) if count > 0}
    all_set = {pair.index for pair, count in zip(pairs, cover_counts) if count == MAXIMIZER_COUNT}
    common = load_json(common_path)
    demand(common.get("I_84_size") == len(common_set), "I_84 size mismatch")
    demand(common.get("covered_by_at_least_one_maximizer_count") == len(union), "maximizer covered-union size mismatch")
    demand(common.get("covered_by_all_84_count") == len(all_set), "all-84 covered size mismatch")
    expected_pairs = [{"pair_index": pair.index, "c": pair.c, "d": pair.d, "shift": pair.shift, "maximizing_classes_covering_pair": count} for pair, count in zip(pairs, cover_counts)]
    demand(common.get("pairs") == expected_pairs, "per-pair maximizing coverage counts mismatch")
    demand(common.get("pairs_uncovered_by_all_84") == sorted(common_set), "pairs-uncovered-by-all list mismatch")
    demand(common.get("pairs_covered_by_all_84") == sorted(all_set), "pairs-covered-by-all list mismatch")
    max_entries = [(row, mask) for row, mask in zip(rows, masks) if row["class_index"] >= 3]
    common_values = [sum(bool(mask[index // 8] & (1 << (index % 8))) for index in common_set) for _, mask in max_entries]
    demand(common.get("T_common_histogram") == {str(value): count for value, count in sorted(Counter(common_values).items())}, "T_common histogram mismatch")

    grouped = defaultdict(list)
    for row, mask in max_entries:
        grouped[row["class_index"]].append((row, mask))
    common_class_summaries = common.get("T_common_class_summaries")
    demand(isinstance(common_class_summaries, list) and len(common_class_summaries) == MAXIMIZER_COUNT, "T_common class summary count mismatch")
    for spec, item in zip(max_specs, common_class_summaries):
        group = grouped[spec.index]
        values = [sum(bool(mask[index // 8] & (1 << (index % 8))) for index in common_set) for _, mask in group]
        ns = [row["n"] for row, _ in group]
        expected = {"class_id": spec.class_id, **expected_summary(values, ns, PAIR_COUNT - len(common_set))}
        demand(item == expected, f"T_common class summary mismatch for {spec.class_id}")
    with frequency_path.open(newline="", encoding="utf-8") as stream:
        frequency_rows = list(csv.DictReader(stream))
    demand(len(frequency_rows) == PAIR_COUNT, "pair frequency row count mismatch")
    normalized_frequency_rows: list[dict[str, Any]] = []
    highlights: dict[str, list[Any]] = {
        "never_winning_exposed_pairs": [], "frequency_at_least_10_percent": [],
        "frequency_at_least_25_percent": [], "frequency_at_least_50_percent": [],
    }
    for pair, covered_count, record in zip(pairs, cover_counts, frequency_rows):
        exposure = wins = classes_with_win = 0
        maximum = Fraction(0, 1)
        for spec in max_specs:
            if pair.index in spec.covered:
                continue
            group = grouped[spec.index]
            within = sum(bool(mask[pair.index // 8] & (1 << (pair.index % 8))) for _, mask in group)
            exposure += len(group)
            wins += within
            classes_with_win += bool(within)
            maximum = max(maximum, Fraction(within, len(group)))
        frequency = Fraction(wins, exposure) if exposure else Fraction(0, 1)
        expected = {
            "pair_index": str(pair.index), "c": str(pair.c), "d": str(pair.d), "shift": str(pair.shift),
            "exposure_count": str(exposure), "winner_count": str(wins),
            "winner_frequency_numerator": str(frequency.numerator), "winner_frequency_denominator": str(frequency.denominator),
            "winner_frequency_decimal": fraction_record(frequency)["decimal"],
            "persistently_covered_class_count": str(covered_count), "classes_with_at_least_one_win": str(classes_with_win),
            "maximum_within_class_frequency_numerator": str(maximum.numerator), "maximum_within_class_frequency_denominator": str(maximum.denominator),
            "maximum_within_class_frequency_decimal": fraction_record(maximum)["decimal"],
        }
        demand(record == expected, f"pair frequency reconstruction mismatch at pair {pair.index}")
        normalized = {
            "pair_index": pair.index, "c": pair.c, "d": pair.d, "shift": pair.shift,
            "exposure_count": exposure, "winner_count": wins,
            "winner_frequency": fraction_record(frequency),
            "persistently_covered_class_count": covered_count,
            "classes_with_at_least_one_win": classes_with_win,
            "maximum_within_class_winner_frequency": fraction_record(maximum),
        }
        normalized_frequency_rows.append(normalized)
        identity = {"pair_index": pair.index, "c": pair.c, "d": pair.d, "shift": pair.shift}
        if exposure and wins == 0:
            highlights["never_winning_exposed_pairs"].append(identity)
        for threshold, key in ((Fraction(1, 10), "frequency_at_least_10_percent"), (Fraction(1, 4), "frequency_at_least_25_percent"), (Fraction(1, 2), "frequency_at_least_50_percent")):
            if exposure and frequency >= threshold:
                highlights[key].append(identity)
    highlights["highest_frequency_residual_pairs"] = sorted(
        normalized_frequency_rows,
        key=lambda row: (-Fraction(row["winner_frequency"]["numerator"], row["winner_frequency"]["denominator"]), row["pair_index"]),
    )[:20]
    return {"I_84_size": len(common_set), "covered_union_size": len(union), "winner_frequency_highlights": highlights}


def verify_coverage_response(path: Path, class_artifact: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    response = load_json(path)
    demand(response.get("schema") == "a303656-p4-census-coverage-response-v1", "coverage response schema mismatch")
    classes = class_artifact["classes"]
    levels = response.get("levels", {})
    demand(levels.get("G216_CAL-216") == classes[0] and levels.get("G227_CAL-227") == classes[1] and levels.get("G230_CAL-230") == classes[2] and levels.get("G231_lexicographically_first") == classes[3], "coverage calibration levels mismatch")
    max_rows = [row for row in rows if row["class_index"] >= 3]
    expected_aggregate = {"G": 231, "uncovered_pair_count": 176, **expected_summary([row["T"] for row in max_rows], [row["n"] for row in max_rows], 231)}
    demand(levels.get("G231_all_84") == expected_aggregate, "aggregate G231 coverage response mismatch")
    demand(response.get("G231_class_level_distribution") == {
        "means": [item["mean_T"] for item in classes[3:]],
        "minima": [item["minimum_T"] for item in classes[3:]],
        "medians": [item["median_T"] for item in classes[3:]],
    }, "G231 class-level coverage distribution mismatch")
    baseline = Fraction(classes[0]["mean_T"]["numerator"], classes[0]["mean_T"]["denominator"])
    expected_reductions: dict[str, Any] = {}
    for label, item in levels.items():
        g = item["G"]
        mean = Fraction(item["mean_T"]["numerator"], item["mean_T"]["denominator"])
        expected_reductions[label] = None if g == 216 else fraction_record((baseline - mean) / (g - 216))
    demand(response.get("mean_T_reduction_per_newly_covered_pair_from_CAL216") == expected_reductions, "coverage reductions from CAL216 mismatch")
    ordered = [(216, classes[0]), (227, classes[1]), (230, classes[2]), (231, expected_aggregate)]
    adjacent = []
    for (g0, left), (g1, right) in zip(ordered, ordered[1:]):
        left_mean = Fraction(left["mean_T"]["numerator"], left["mean_T"]["denominator"])
        right_mean = Fraction(right["mean_T"]["numerator"], right["mean_T"]["denominator"])
        adjacent.append({"from_G": g0, "to_G": g1, "mean_T_reduction_per_newly_covered_pair": fraction_record((left_mean - right_mean) / (g1 - g0))})
    demand(response.get("adjacent_level_mean_T_reduction_per_newly_covered_pair") == adjacent, "adjacent coverage reductions mismatch")
    demand(response.get("causality_caveat") == "Four fixed finite coverage levels do not identify a causal coverage response.", "coverage response causality caveat missing")


def verify_metadata(
    metadata: dict[str, Any], root: Path, artifact: Path, protected: dict[str, str],
    panel: list[dict[str, int | str]], source_commit: str, source_parent: str,
    rows: list[dict[str, Any]], masks: list[bytes], aggregate: dict[str, Any], direct: dict[str, int], common: dict[str, int],
) -> None:
    demand(metadata.get("schema") == "a303656-p4-maximizer-class-census-metadata-v1", "metadata schema mismatch")
    demand(metadata.get("source_commit") == source_commit and metadata.get("source_parent_commit") == source_parent, "metadata source commit mismatch")
    demand(metadata.get("results_commit") == RESULTS_SENTINEL, "metadata results commit sentinel mismatch")
    demand(metadata.get("mathematical_status") == "UNRESOLVED", "metadata global status mismatch")
    demand(metadata.get("validation_conclusion") == "VALIDATED T3=2 FIXED-P4 MAXIMIZER-CLASS CENSUS", "metadata conclusion mismatch")
    fixed = metadata.get("fixed_domain", {})
    demand((fixed.get("P4"), fixed.get("M4"), fixed.get("L"), fixed.get("activation_cell"), fixed.get("n0"), fixed.get("active_pair_count"), fixed.get("constrained_argmax_count"), fixed.get("constrained_argmax_digest")) == (list(P4), M4, L, [A, B], N0, PAIR_COUNT, MAXIMIZER_COUNT, CONSTRAINED_ARGMAX_DIGEST), "metadata fixed-domain mismatch")
    panel_meta = metadata.get("panel", {})
    demand((panel_meta.get("class_count"), panel_meta.get("maximizing_class_count"), panel_meta.get("calibration_class_count"), panel_meta.get("point_count"), panel_meta.get("unique_point_count"), panel_meta.get("class_panel_sha256")) == (CLASS_COUNT, MAXIMIZER_COUNT, 3, len(panel), len(panel), panel_digest(artifact / "class_panel.csv")), "metadata panel mismatch")
    agreement = metadata.get("agreement", {})
    demand(agreement.get("pointwise_T_equal") is True and agreement.get("pointwise_masks_equal") is True and agreement.get("popcount_equals_T_all_points") is True and agreement.get("persistent_covered_winner_count") == 0, "metadata agreement claim mismatch")
    demand(metadata.get("protected_baseline_and_landscape_sha256") == protected, "metadata protected hashes mismatch")
    demand(metadata.get("aggregate_G231") == aggregate, "metadata aggregate mismatch")
    demand(metadata.get("direct_oracle", {}).get("selected_point_count") == direct["selected_point_count"] and metadata.get("direct_oracle", {}).get("verified_canonical_witness_count") == direct["witness_count"], "metadata direct summary mismatch")
    demand(metadata.get("common_uncovered_summary", {}).get("I_84_size") == common["I_84_size"], "metadata common-uncovered summary mismatch")
    demand(metadata.get("winner_frequency_highlights") == common["winner_frequency_highlights"], "metadata winner-frequency highlights mismatch")
    response = load_json(artifact / "coverage_response.json")
    cal = response["levels"]["G216_CAL-216"]
    g231 = response["levels"]["G231_all_84"]
    cal_mean = Fraction(cal["mean_T"]["numerator"], cal["mean_T"]["denominator"])
    g_mean = Fraction(g231["mean_T"]["numerator"], g231["mean_T"]["denominator"])
    cal_median = Fraction(cal["median_T"]["numerator"], cal["median_T"]["denominator"])
    g_median = Fraction(g231["median_T"]["numerator"], g231["median_T"]["denominator"])
    if aggregate["global_minimum_T"] < 16:
        label = "FIXED-P4 MAXIMIZATION PRODUCES A STRICTLY LOWER FINITE T MINIMUM"
    elif g_mean < cal_mean and g_median < cal_median:
        label = "FIXED-P4 MAXIMIZATION LOWERS THE DISTRIBUTION BUT NOT THE KNOWN MINIMUM"
    elif g_mean >= cal_mean and g_median >= cal_median:
        label = "FIXED-P4 MAXIMIZATION SHOWS NO MATERIAL FINITE IMPROVEMENT"
    else:
        label = "MIXED / INCONCLUSIVE FINITE RESULT"
    demand(metadata.get("interpretation_label") == label, "metadata interpretation label mismatch")
    reduction = cal_mean - g_mean
    expected_stopping = {
        "any_G231_T_below_16": aggregate["global_minimum_T"] < 16,
        "any_G231_T_zero": aggregate["global_minimum_T"] == 0,
        "aggregate_mean_improvement_over_CAL216": fraction_record(reduction),
        "mean_improvement_per_15_additional_guaranteed_obstructions": fraction_record(reduction / 15),
        "approximately_explained_by_15_additional_obstructions": "finite comparison only; inspect observed per-covered-pair response, no causal claim",
    }
    demand(metadata.get("predeclared_stopping_answers") == expected_stopping, "metadata stopping answers mismatch")
    scope = metadata.get("scope_guards", {})
    demand(scope == {"formal_integers_evaluated": len(panel), "integers_outside_panel_evaluated": 0, "new_primes": 0, "optimized_residue_tuples": 0, "adaptive_extensions": 0, "formal_class_count": CLASS_COUNT}, "metadata scope guards mismatch")
    declared_hashes = metadata.get("artifact_sha256_excluding_metadata_and_verification_report")
    expected_hashes = {name: sha256_file(artifact / name) for name in sorted(CORE_ARTIFACTS - {"metadata.json"})}
    demand(declared_hashes == expected_hashes, "metadata artifact hash manifest mismatch")


def verify_negative_report(path: Path) -> dict[str, int]:
    report = load_json(path)
    tests = report.get("tests")
    demand(isinstance(tests, list), "negative-test report malformed")
    observed = {test.get("name") for test in tests}
    demand(observed == EXPECTED_NEGATIVE_TESTS and len(tests) == len(EXPECTED_NEGATIVE_TESTS), "negative-test set mismatch")
    codes: dict[str, int] = {}
    for test in tests:
        code = test.get("return_code")
        demand(isinstance(code, int) and code != 0 and test.get("rejected") is True, f"negative test did not reject: {test.get('name')}")
        codes[test["name"]] = code
    return codes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-parent", required=True)
    parser.add_argument("--negative-report", type=Path)
    parser.add_argument("--negative-test-mode", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = args.root.resolve()
        artifact = args.artifact_dir.resolve()
        actual_names = {path.name for path in artifact.iterdir() if path.is_file()}
        allowed = CORE_ARTIFACTS | {"verification_report.json"}
        demand(CORE_ARTIFACTS <= actual_names and actual_names <= allowed, f"artifact file set mismatch: {sorted(actual_names)}")
        git = verify_git(root, args.source_commit, args.source_parent)
        protected = verify_protected(root)
        panel, specs, pairs = construct_panel(root)
        read_panel(artifact / "class_panel.csv", root)
        rows_a = read_counts(artifact / "backend_a_counts.csv", panel)
        rows_b = read_counts(artifact / "backend_b_counts.csv", panel)
        pair_hash = sha256_file(root / "analysis/k4_survivor_incidence/pair_order.csv")
        masks_a = read_masks(artifact / "backend_a_masks.bin", 1, "k4_ap_backend_a_trial_division_v1", artifact / "class_panel.csv", pair_hash, rows_a)
        masks_b = read_masks(artifact / "backend_b_masks.bin", 2, "k4_ap_backend_b_cpp17_mr7_brent_rho_v1", artifact / "class_panel.csv", pair_hash, rows_b)
        demand([row["T"] for row in rows_a] == [row["T"] for row in rows_b], "backend pointwise T mismatch")
        demand(masks_a == masks_b, "backend pointwise mask mismatch")
        for row, mask in zip(rows_a, masks_a):
            spec = specs[row["class_index"]]
            independently_covered = coverage_set(spec.tuple4, pairs)
            demand(independently_covered == spec.covered and len(independently_covered) == spec.coverage, "persistent coverage regeneration mismatch")
            for pair_index in independently_covered:
                demand(not mask[pair_index // 8] & (1 << (pair_index % 8)), "persistent-covered pair appears as winner")

        class_artifact = load_json(artifact / "class_summaries.json")
        aggregate = verify_class_summaries(class_artifact, rows_a, masks_a, specs)
        verify_global_histogram(artifact / "global_histogram.csv", aggregate["T_histogram"])
        verify_coverage_response(artifact / "coverage_response.json", class_artifact, rows_a)
        common = verify_common_and_frequencies(artifact / "common_uncovered.json", artifact / "pair_frequencies.csv", rows_a, masks_a, specs, pairs)
        direct = verify_direct(artifact / "direct_verification.json", rows_a, masks_a, pairs)
        metadata = load_json(artifact / "metadata.json")
        verify_metadata(metadata, root, artifact, protected, panel, args.source_commit, args.source_parent, rows_a, masks_a, aggregate, direct, common)
        demand(args.negative_report is not None or args.negative_test_mode, "authoritative verification requires the negative-test report")
        negative_codes = verify_negative_report(args.negative_report.resolve()) if args.negative_report else {}
        report = {
            "schema": "a303656-p4-census-verification-report-v1", "verifier_implementation_id": IMPLEMENTATION_ID,
            "status": "PASS", "git_provenance": git, "formal_class_count": CLASS_COUNT,
            "formal_point_count": len(panel), "backend_pointwise_T_equal": True,
            "backend_pointwise_masks_equal": True, "popcount_equals_T_all_points": True,
            "persistent_covered_winner_count": 0, "direct_oracle": direct,
            "class_and_aggregate_summaries_reconstructed": True,
            "common_uncovered_and_pair_frequencies_reconstructed": True,
            "protected_baseline_and_landscape_hashes_match": True,
            "negative_tests": {"required_count": len(EXPECTED_NEGATIVE_TESTS), "all_rejected": bool(negative_codes), "return_codes": negative_codes},
            "mathematical_status": "UNRESOLVED",
            "conclusion": "VALIDATED T3=2 FIXED-P4 MAXIMIZER-CLASS CENSUS",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_name(args.output.name + f".tmp.{os.getpid()}")
        with temporary.open("w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, args.output)
        print("P4_CENSUS_VERIFICATION_PASS")
        print(f"formal_classes={CLASS_COUNT}")
        print(f"formal_points={len(panel)}")
        return 0
    except (CensusError, OSError, ValueError, KeyError, json.JSONDecodeError, csv.Error, subprocess.CalledProcessError) as exc:
        print(f"{IMPLEMENTATION_ID}: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
