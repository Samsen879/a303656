#!/usr/bin/env python3
"""Run the exact predeclared 87-class fixed-P4 census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import resource
import statistics
import struct
import subprocess
import sys
import time
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from p4_census_common import (
    A, B, CLASS_COUNT, CONSTRAINED_ARGMAX_DIGEST, CONSTRAINED_G,
    COUNT_FIELDS, L, MASK_BYTES, MAXIMIZER_COUNT, M4, N0, P4,
    PAIR_COUNT, PANEL_FIELDS, START_COMMIT, TASK, CensusError, ClassSpec,
    Pair, canonical_json, class_points, construct_panel, coverage_set,
    mask_popcount, panel_digest, sha256_file, verify_protected, write_panel,
)


RESULTS_COMMIT_SENTINEL = "RESULT_COMMIT_CONTAINING_THIS_FILE"
ARTIFACT_NAMES = [
    "metadata.json", "class_panel.csv", "backend_a_counts.csv",
    "backend_b_counts.csv", "backend_a_masks.bin", "backend_b_masks.bin",
    "class_summaries.json", "global_histogram.csv", "coverage_response.json",
    "common_uncovered.json", "pair_frequencies.csv", "direct_verification.json",
]
MASK_HEADER = struct.Struct("<8sIIIIII32s32s32s")


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def exact_fraction(value: Fraction, digits: int = 18) -> dict[str, Any]:
    with localcontext() as context:
        context.prec = max(50, digits + 20)
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": format(decimal, f".{digits}f"),
    }


def exact_median(values: list[int]) -> dict[str, Any]:
    ordered = sorted(values)
    size = len(ordered)
    if size % 2:
        value = Fraction(ordered[size // 2], 1)
    else:
        value = Fraction(ordered[size // 2 - 1] + ordered[size // 2], 2)
    return exact_fraction(value)


def inverse_ecdf(values: list[int], percent: int) -> int:
    if not values or not 0 < percent <= 100:
        raise CensusError("invalid inverse-ECDF request")
    ordered = sorted(values)
    rank = (percent * len(ordered) + 99) // 100
    return ordered[rank - 1]


def population_stddev(values: list[int]) -> dict[str, Any]:
    count = len(values)
    total = sum(values)
    square_total = sum(value * value for value in values)
    variance = Fraction(square_total, count) - Fraction(total * total, count * count)
    with localcontext() as context:
        context.prec = 60
        decimal = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    return {
        "variance_numerator": variance.numerator,
        "variance_denominator": variance.denominator,
        "decimal": format(decimal, ".18f"),
    }


def summary(values: list[int], ns: list[int], coverage: int) -> dict[str, Any]:
    if not values or len(values) != len(ns):
        raise CensusError("invalid summary population")
    minimum = min(values)
    maximum = max(values)
    total = sum(values)
    thresholds = [5, 10, 12, 14, 16, 18, 20, 25]
    return {
        "point_count": len(values),
        "minimum_T": minimum,
        "argmin_n": [n for n, value in zip(ns, values) if value == minimum],
        "maximum_T": maximum,
        "mean_T": exact_fraction(Fraction(total, len(values))),
        "population_standard_deviation_T": population_stddev(values),
        "median_T": exact_median(values),
        "inverse_empirical_cdf": {str(percent): inverse_ecdf(values, percent) for percent in (10, 25, 50, 75, 90)},
        "counts": {"T=0": values.count(0), **{f"T<={threshold}": sum(value <= threshold for value in values) for threshold in thresholds}},
        "total_winner_incidences": total,
        "residual_survival_rate": exact_fraction(Fraction(total, len(values) * (PAIR_COUNT - coverage))),
    }


def parse_counts(path: Path, panel: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != COUNT_FIELDS:
            raise CensusError(f"counts header mismatch: {path}")
        raw = list(reader)
    if len(raw) != len(panel):
        raise CensusError(f"counts row count mismatch: {path}")
    parsed: list[dict[str, int | str]] = []
    numeric = [field for field in COUNT_FIELDS if field not in ("class_id", "mask_sha256")]
    for ordinal, (row, expected) in enumerate(zip(raw, panel)):
        item: dict[str, int | str] = {"class_id": row["class_id"], "mask_sha256": row["mask_sha256"]}
        for field in numeric:
            item[field] = int(row[field])
        if {field: item[field] for field in PANEL_FIELDS} != expected:
            raise CensusError(f"counts panel identity mismatch at row {ordinal}: {path}")
        if not 0 <= int(item["T"]) <= PAIR_COUNT:
            raise CensusError("counts T outside domain")
        parsed.append(item)
    return parsed


def parse_masks(
    path: Path,
    expected_backend: int,
    panel_path: Path,
    root: Path,
    expected_core: str,
    rows: list[dict[str, int | str]],
) -> tuple[list[bytes], dict[str, Any]]:
    data = path.read_bytes()
    if len(data) < MASK_HEADER.size:
        raise CensusError("packed mask file truncated before header")
    unpacked = MASK_HEADER.unpack(data[:MASK_HEADER.size])
    magic, version, backend, header_size, point_count, pair_count, mask_bytes, panel_hash, pair_hash, core_hash = unpacked
    if magic != b"P4CMASK1" or version != 1 or backend != expected_backend or header_size != MASK_HEADER.size:
        raise CensusError("packed mask identity/header mismatch")
    if point_count != len(rows) or pair_count != PAIR_COUNT or mask_bytes != MASK_BYTES:
        raise CensusError("packed mask dimensions mismatch")
    if panel_hash.hex() != panel_digest(panel_path):
        raise CensusError("packed mask panel digest mismatch")
    committed_pair_hash = sha256_file(root / "analysis/k4_survivor_incidence/pair_order.csv")
    if pair_hash.hex() != committed_pair_hash:
        raise CensusError("packed mask pair-order digest mismatch")
    if core_hash != hashlib.sha256(expected_core.encode()).digest():
        raise CensusError("packed mask backend core identity mismatch")
    expected_size = MASK_HEADER.size + len(rows) * MASK_BYTES
    if len(data) != expected_size:
        raise CensusError("packed mask file has truncated or extra bytes")
    masks = [data[MASK_HEADER.size + index * MASK_BYTES:MASK_HEADER.size + (index + 1) * MASK_BYTES] for index in range(len(rows))]
    for ordinal, (row, mask) in enumerate(zip(rows, masks)):
        if int(row["mask_offset"]) != MASK_HEADER.size + ordinal * MASK_BYTES:
            raise CensusError("counts mask offset mismatch")
        if str(row["mask_sha256"]) != hashlib.sha256(mask).hexdigest():
            raise CensusError("counts mask digest mismatch")
        if mask_popcount(mask) != int(row["T"]):
            raise CensusError("packed mask popcount/T mismatch")
    return masks, {
        "sha256": sha256_file(path), "size_bytes": len(data), "header_bytes": MASK_HEADER.size,
        "point_count": point_count, "pair_count": pair_count, "mask_bytes_per_point": mask_bytes,
        "backend_slot": backend, "core_identity": expected_core,
    }


def run_logged(command: list[str], stdout_path: Path, stderr_path: Path) -> dict[str, Any]:
    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    elapsed = time.monotonic() - started
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    record = {
        "command": command, "return_code": completed.returncode,
        "wall_seconds": format(elapsed, ".6f"),
        "children_user_seconds_delta": format(after.ru_utime - before.ru_utime, ".6f"),
        "children_system_seconds_delta": format(after.ru_stime - before.ru_stime, ".6f"),
        "children_max_rss_kib_after": after.ru_maxrss,
        "stdout": stdout_path.name, "stderr": stderr_path.name,
    }
    if completed.returncode != 0:
        raise CensusError(f"command failed with return code {completed.returncode}: {' '.join(command)}")
    return record


def coverage_mask(spec: ClassSpec) -> bytes:
    mask = bytearray(MASK_BYTES)
    for index in spec.covered:
        mask[index // 8] |= 1 << (index % 8)
    return bytes(mask)


def validate_persistent(masks: list[bytes], panel: list[dict[str, int | str]], specs: list[ClassSpec]) -> None:
    for mask, point in zip(masks, panel):
        spec = specs[int(point["class_index"])]
        for pair_index in spec.covered:
            if mask[pair_index // 8] & (1 << (pair_index % 8)):
                raise CensusError(f"persistent-covered pair appears as winner at n={point['n']}, pair={pair_index}")


def selected_direct_points(
    rows: list[dict[str, int | str]],
) -> tuple[list[dict[str, int | str]], dict[tuple[int, int], list[str]]]:
    grouped: dict[int, list[dict[str, int | str]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["class_index"])].append(row)
    reasons: dict[tuple[int, int], set[str]] = defaultdict(set)
    for class_index in range(CLASS_COUNT):
        group = grouped[class_index]
        minimum = min(int(row["T"]) for row in group)
        for row in group:
            key = (class_index, int(row["point_index"]))
            if int(row["T"]) == minimum:
                reasons[key].add("class_minimum")
            if int(row["T"]) <= 20:
                reasons[key].add("T<=20")
            if int(row["T"]) <= 16:
                reasons[key].add("T<=previous_known_16")
        for label, index in (("class_first", 0), ("class_median_lower", (len(group) - 1) // 2), ("class_last", len(group) - 1)):
            reasons[(class_index, int(group[index]["point_index"]))].add(label)
        nearest = min(group, key=lambda row: (abs(int(row["n"]) - N0), int(row["n"])))
        reasons[(class_index, int(nearest["point_index"]))].add(
            "calibration_nearest_n0" if class_index < 3 else "maximizer_class_nearest_n0"
        )
    lookup = {(int(row["class_index"]), int(row["point_index"])): row for row in rows}
    keys = sorted(reasons, key=lambda key: rows.index(lookup[key]))
    selected = [lookup[key] for key in keys]
    normalized = {key: sorted(values) for key, values in reasons.items()}
    if len({int(row["n"]) for row in selected}) != len(selected):
        raise CensusError("direct panel deduplication failure")
    return selected, normalized


def write_direct_panel(path: Path, selected: list[dict[str, int | str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["class_index", "point_index", "n", "active_pairs", "expected_T"])
        for row in selected:
            writer.writerow([row["class_index"], row["point_index"], row["n"], PAIR_COUNT, row["T"]])


def verify_direct_raw(
    raw_path: Path,
    selected: list[dict[str, int | str]],
    reasons: dict[tuple[int, int], list[str]],
    masks_by_key: dict[tuple[int, int], bytes],
    pairs: list[Pair],
) -> dict[str, Any]:
    with raw_path.open(encoding="utf-8") as stream:
        raw = json.load(stream)
    if raw.get("implementation_id") != "p4_census_direct_oracle_adapter_v1" or raw.get("method") != "factorization-free exact monotone boundary enumeration; canonical least-a witness":
        raise CensusError("direct-oracle identity/method mismatch")
    points = raw.get("points")
    if not isinstance(points, list) or len(points) != len(selected):
        raise CensusError("direct-oracle point count mismatch")
    pair_lookup = {(pair.c, pair.d): pair for pair in pairs}
    output_points: list[dict[str, Any]] = []
    witness_count = 0
    for expected, point in zip(selected, points):
        key = (int(expected["class_index"]), int(expected["point_index"]))
        if (point.get("class_index"), point.get("point_index"), point.get("n"), point.get("active_pair_count"), point.get("T")) != (
            key[0], key[1], expected["n"], PAIR_COUNT, expected["T"],
        ):
            raise CensusError("direct-oracle point identity/T mismatch")
        winner_mask = bytearray(MASK_BYTES)
        winners = point.get("winners")
        if not isinstance(winners, list) or len(winners) != int(expected["T"]):
            raise CensusError("direct-oracle winner cardinality mismatch")
        compact_winners: list[dict[str, int]] = []
        seen_pairs: set[tuple[int, int]] = set()
        for winner in winners:
            identity = (winner.get("c"), winner.get("d"))
            pair = pair_lookup.get(identity)
            if pair is None or identity in seen_pairs:
                raise CensusError("direct-oracle duplicate/unknown winner pair")
            seen_pairs.add(identity)
            remainder = int(expected["n"]) - pair.shift
            a, b = winner.get("a"), winner.get("b")
            if winner.get("shift") != pair.shift or winner.get("remainder") != remainder or not isinstance(a, int) or not isinstance(b, int):
                raise CensusError("direct-oracle winner shift/witness schema mismatch")
            if not 0 <= a <= b or a * a + b * b != remainder:
                raise CensusError("direct-oracle witness arithmetic failure")
            winner_mask[pair.index // 8] |= 1 << (pair.index % 8)
            compact_winners.append({"c": pair.c, "d": pair.d, "shift": pair.shift, "remainder": remainder, "a": a, "b": b})
            witness_count += 1
        packed = bytes(winner_mask)
        if packed != masks_by_key[key]:
            raise CensusError("direct-oracle complete winner mask differs from full backends")
        output_points.append({
            "class_index": key[0], "class_id": expected["class_id"], "point_index": key[1],
            "n": expected["n"], "T": expected["T"], "selection_reasons": reasons[key],
            "winner_mask_hex": packed.hex(), "canonical_winners": compact_winners,
        })
    return {
        "schema": "a303656-p4-census-direct-verification-v1",
        "oracle_implementation_id": raw["implementation_id"], "oracle_method": raw["method"],
        "selection_policy": {
            "class_minimum": "all points attaining each class minimum",
            "thresholds": ["T<=20", "T<=previous_known_16"],
            "positional": ["first", "lower median by ordered point index", "last"],
            "nearest_n0": "one nearest member per class, ties resolved by smaller n",
            "deduplicated": True,
        },
        "selected_point_count": len(output_points), "verified_complete_mask_count": len(output_points),
        "verified_canonical_witness_count": witness_count,
        "T_zero_points": [point["n"] for point in output_points if point["T"] == 0],
        "T_zero_label": "UNVERIFIED COUNTEREXAMPLE CANDIDATE" if any(point["T"] == 0 for point in output_points) else None,
        "points": output_points,
    }


def build_class_and_aggregate(
    rows: list[dict[str, int | str]], masks: list[bytes], specs: list[ClassSpec]
) -> tuple[dict[str, Any], dict[str, Any]]:
    grouped: dict[int, list[tuple[dict[str, int | str], bytes]]] = defaultdict(list)
    for row, mask in zip(rows, masks):
        grouped[int(row["class_index"])].append((row, mask))
    class_items: list[dict[str, Any]] = []
    for spec in specs:
        group = grouped[spec.index]
        values = [int(row["T"]) for row, _ in group]
        ns = [int(row["n"]) for row, _ in group]
        item = {
            "class_index": spec.index, "class_id": spec.class_id, "residue_tuple": list(spec.tuple4),
            "G": spec.coverage, "uncovered_pair_count": PAIR_COUNT - spec.coverage,
            "crt_residue_mod_L": spec.residue, "activation_cell_member_count": len(group),
            "persistent_covered_mask_sha256": hashlib.sha256(coverage_mask(spec)).hexdigest(),
        }
        item.update(summary(values, ns, spec.coverage))
        class_items.append(item)

    max_rows = [(row, mask) for row, mask in zip(rows, masks) if int(row["class_index"]) >= 3]
    max_values = [int(row["T"]) for row, _ in max_rows]
    global_min = min(max_values)
    class_minima = [item["minimum_T"] for item in class_items[3:]]
    class_means = [item["mean_T"] for item in class_items[3:]]
    mask_groups: dict[str, list[str]] = defaultdict(list)
    for spec in specs[3:]:
        mask_groups[hashlib.sha256(coverage_mask(spec)).hexdigest()].append(spec.class_id)
    survival = sorted(
        ((Decimal(item["residual_survival_rate"]["decimal"]), item["class_id"], item["residual_survival_rate"]) for item in class_items[3:]),
        key=lambda entry: (entry[0], entry[1]),
    )
    aggregate = {
        "maximizing_class_count": MAXIMIZER_COUNT,
        "total_points": len(max_rows),
        "global_minimum_T": global_min,
        "global_argmins": [
            {"class_id": row["class_id"], "residue_tuple": [row["t3"], row["t7"], row["t11"], row["t23"]], "point_index": row["point_index"], "n": row["n"]}
            for row, _ in max_rows if int(row["T"]) == global_min
        ],
        "T_histogram": {str(value): count for value, count in sorted(Counter(max_values).items())},
        "class_minima_distribution": {str(value): count for value, count in sorted(Counter(class_minima).items())},
        "class_means_distribution": sorted(
            ({"class_id": item["class_id"], "mean_T": item["mean_T"]} for item in class_items[3:]),
            key=lambda item: (Fraction(item["mean_T"]["numerator"], item["mean_T"]["denominator"]), item["class_id"]),
        ),
        "class_minimum_threshold_counts": {f"minimum_T<={threshold}": sum(value <= threshold for value in class_minima) for threshold in (10, 12, 14, 16, 18, 20)},
        "classes_with_point_below_known_T16": sum(value < 16 for value in class_minima),
        "distinct_persistent_covered_masks": len(mask_groups),
        "classes_per_persistent_covered_mask": [
            {"mask_sha256": digest, "class_count": len(class_ids), "class_ids": class_ids}
            for digest, class_ids in sorted(mask_groups.items())
        ],
        "best_residual_survival_rate": {"class_id": survival[0][1], "rate": survival[0][2]},
        "worst_residual_survival_rate": {"class_id": survival[-1][1], "rate": survival[-1][2]},
    }
    return {"schema": "a303656-p4-census-class-summaries-v1", "classes": class_items, "aggregate_G231": aggregate}, aggregate


def write_histogram(path: Path, histogram: dict[str, int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["T", "count"])
        for value, count in sorted(((int(key), count) for key, count in histogram.items())):
            writer.writerow([value, count])


def aggregate_summary(rows: list[dict[str, int | str]], coverage: int) -> dict[str, Any]:
    return summary([int(row["T"]) for row in rows], [int(row["n"]) for row in rows], coverage)


def coverage_response(rows: list[dict[str, int | str]], class_summaries: dict[str, Any]) -> dict[str, Any]:
    classes = class_summaries["classes"]
    max_rows = [row for row in rows if int(row["class_index"]) >= 3]
    aggregate = aggregate_summary(max_rows, 231)
    levels = {
        "G216_CAL-216": classes[0], "G227_CAL-227": classes[1], "G230_CAL-230": classes[2],
        "G231_all_84": {"G": 231, "uncovered_pair_count": 176, **aggregate},
        "G231_lexicographically_first": classes[3],
    }
    baseline_mean = Fraction(classes[0]["mean_T"]["numerator"], classes[0]["mean_T"]["denominator"])
    reductions: dict[str, Any] = {}
    for label, item in levels.items():
        g = int(item["G"])
        mean = Fraction(item["mean_T"]["numerator"], item["mean_T"]["denominator"])
        reductions[label] = None if g == 216 else exact_fraction((baseline_mean - mean) / (g - 216))
    adjacent: list[dict[str, Any]] = []
    ordered = [(216, classes[0]), (227, classes[1]), (230, classes[2]), (231, aggregate)]
    for (g0, left), (g1, right) in zip(ordered, ordered[1:]):
        left_mean = Fraction(left["mean_T"]["numerator"], left["mean_T"]["denominator"])
        right_mean = Fraction(right["mean_T"]["numerator"], right["mean_T"]["denominator"])
        adjacent.append({"from_G": g0, "to_G": g1, "mean_T_reduction_per_newly_covered_pair": exact_fraction((left_mean - right_mean) / (g1 - g0))})
    max_class_means = [item["mean_T"] for item in classes[3:]]
    max_class_mins = [item["minimum_T"] for item in classes[3:]]
    max_class_medians = [item["median_T"] for item in classes[3:]]
    return {
        "schema": "a303656-p4-census-coverage-response-v1", "levels": levels,
        "G231_class_level_distribution": {"means": max_class_means, "minima": max_class_mins, "medians": max_class_medians},
        "mean_T_reduction_per_newly_covered_pair_from_CAL216": reductions,
        "adjacent_level_mean_T_reduction_per_newly_covered_pair": adjacent,
        "causality_caveat": "Four fixed finite coverage levels do not identify a causal coverage response.",
    }


def common_and_frequencies(
    rows: list[dict[str, int | str]], masks: list[bytes], specs: list[ClassSpec], pairs: list[Pair]
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    max_specs = specs[3:]
    cover_counts = [sum(pair.index in spec.covered for spec in max_specs) for pair in pairs]
    common = {pair.index for pair, count in zip(pairs, cover_counts) if count == 0}
    union = {pair.index for pair, count in zip(pairs, cover_counts) if count > 0}
    all_covered = {pair.index for pair, count in zip(pairs, cover_counts) if count == MAXIMIZER_COUNT}
    max_entries = [(row, mask) for row, mask in zip(rows, masks) if int(row["class_index"]) >= 3]
    common_values: list[int] = []
    common_by_class: dict[int, list[tuple[int, int]]] = defaultdict(list)
    max_by_class: dict[int, list[tuple[dict[str, int | str], bytes]]] = defaultdict(list)
    for row, mask in max_entries:
        max_by_class[int(row["class_index"])].append((row, mask))
        value = sum(bool(mask[index // 8] & (1 << (index % 8))) for index in common)
        common_values.append(value)
        common_by_class[int(row["class_index"])].append((int(row["n"]), value))
    common_classes = []
    for spec in max_specs:
        class_values = common_by_class[spec.index]
        common_classes.append({"class_id": spec.class_id, **summary([value for _, value in class_values], [n for n, _ in class_values], PAIR_COUNT - len(common))})

    frequency_rows: list[dict[str, Any]] = []
    highlights = {"never_winning_exposed_pairs": [], "frequency_at_least_10_percent": [], "frequency_at_least_25_percent": [], "frequency_at_least_50_percent": []}
    for pair, covered_class_count in zip(pairs, cover_counts):
        exposure = winner_count = 0
        classes_with_win = 0
        max_within = Fraction(0, 1)
        for spec in max_specs:
            class_rows = max_by_class[spec.index]
            if pair.index in spec.covered:
                continue
            wins = sum(bool(mask[pair.index // 8] & (1 << (pair.index % 8))) for _, mask in class_rows)
            exposure += len(class_rows)
            winner_count += wins
            if wins:
                classes_with_win += 1
            max_within = max(max_within, Fraction(wins, len(class_rows)))
        frequency = Fraction(winner_count, exposure) if exposure else Fraction(0, 1)
        record = {
            "pair_index": pair.index, "c": pair.c, "d": pair.d, "shift": pair.shift,
            "exposure_count": exposure, "winner_count": winner_count,
            "winner_frequency": exact_fraction(frequency),
            "persistently_covered_class_count": covered_class_count,
            "classes_with_at_least_one_win": classes_with_win,
            "maximum_within_class_winner_frequency": exact_fraction(max_within),
        }
        frequency_rows.append(record)
        identity = {"pair_index": pair.index, "c": pair.c, "d": pair.d, "shift": pair.shift}
        if exposure and winner_count == 0:
            highlights["never_winning_exposed_pairs"].append(identity)
        for threshold, key in ((Fraction(1, 10), "frequency_at_least_10_percent"), (Fraction(1, 4), "frequency_at_least_25_percent"), (Fraction(1, 2), "frequency_at_least_50_percent")):
            if exposure and frequency >= threshold:
                highlights[key].append(identity)
    ranked = sorted(frequency_rows, key=lambda row: (-Fraction(row["winner_frequency"]["numerator"], row["winner_frequency"]["denominator"]), row["pair_index"]))
    highlights["highest_frequency_residual_pairs"] = ranked[:20]
    common_artifact = {
        "schema": "a303656-p4-census-common-uncovered-v1",
        "I_84_size": len(common), "covered_by_at_least_one_maximizer_count": len(union),
        "covered_by_all_84_count": len(all_covered),
        "pairs": [
            {"pair_index": pair.index, "c": pair.c, "d": pair.d, "shift": pair.shift, "maximizing_classes_covering_pair": count}
            for pair, count in zip(pairs, cover_counts)
        ],
        "pairs_uncovered_by_all_84": [pair.index for pair in pairs if pair.index in common],
        "pairs_covered_by_all_84": [pair.index for pair in pairs if pair.index in all_covered],
        "T_common_histogram": {str(value): count for value, count in sorted(Counter(common_values).items())},
        "T_common_class_summaries": common_classes,
    }
    return common_artifact, frequency_rows, highlights


def write_pair_frequencies(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "pair_index", "c", "d", "shift", "exposure_count", "winner_count",
        "winner_frequency_numerator", "winner_frequency_denominator", "winner_frequency_decimal",
        "persistently_covered_class_count", "classes_with_at_least_one_win",
        "maximum_within_class_frequency_numerator", "maximum_within_class_frequency_denominator",
        "maximum_within_class_frequency_decimal",
    ]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            winner = row["winner_frequency"]
            maximum = row["maximum_within_class_winner_frequency"]
            writer.writerow({
                "pair_index": row["pair_index"], "c": row["c"], "d": row["d"], "shift": row["shift"],
                "exposure_count": row["exposure_count"], "winner_count": row["winner_count"],
                "winner_frequency_numerator": winner["numerator"], "winner_frequency_denominator": winner["denominator"], "winner_frequency_decimal": winner["decimal"],
                "persistently_covered_class_count": row["persistently_covered_class_count"], "classes_with_at_least_one_win": row["classes_with_at_least_one_win"],
                "maximum_within_class_frequency_numerator": maximum["numerator"], "maximum_within_class_frequency_denominator": maximum["denominator"], "maximum_within_class_frequency_decimal": maximum["decimal"],
            })


def interpretation(coverage: dict[str, Any], aggregate: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    cal = coverage["levels"]["G216_CAL-216"]
    g231 = coverage["levels"]["G231_all_84"]
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
    reduction = cal_mean - g_mean
    per_obstruction = reduction / 15
    return label, {
        "any_G231_T_below_16": aggregate["global_minimum_T"] < 16,
        "any_G231_T_zero": aggregate["global_minimum_T"] == 0,
        "aggregate_mean_improvement_over_CAL216": exact_fraction(reduction),
        "mean_improvement_per_15_additional_guaranteed_obstructions": exact_fraction(per_obstruction),
        "approximately_explained_by_15_additional_obstructions": "finite comparison only; inspect observed per-covered-pair response, no causal claim",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--backend-a-core", type=Path, required=True)
    parser.add_argument("--backend-b-core", type=Path, required=True)
    parser.add_argument("--direct-oracle", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-parent", required=True)
    parser.add_argument("--direct-jobs", type=int, default=max(1, min(32, os.cpu_count() or 1)))
    parser.add_argument("--archive-name", default="PENDING_EXTERNAL_ARCHIVE")
    parser.add_argument("--archive-sha256", default="PENDING_EXTERNAL_ARCHIVE_SHA256")
    parser.add_argument("--archive-size-bytes", type=int, default=0)
    parser.add_argument("--archive-file-count", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        root = args.root.resolve()
        if args.source_commit == START_COMMIT:
            raise CensusError("source commit must be the child source commit I, not the starting results commit")
        protected = verify_protected(root)
        artifact_dir = args.artifact_dir.resolve()
        work_dir = args.work_dir.resolve()
        log_dir = args.log_dir.resolve()
        artifact_dir.mkdir(parents=True, exist_ok=True)
        work_dir.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)
        panel, specs, pairs = construct_panel(root)
        panel_path = artifact_dir / "class_panel.csv"
        write_panel(panel_path, panel)

        commands: dict[str, Any] = {}
        adapter_a = root / "src/p4_census_backend_a.py"
        adapter_b = root / "src/p4_census_backend_b.py"
        a_command = [sys.executable, str(adapter_a), "--root", str(root), "--core", str(args.backend_a_core.resolve()), "--panel", str(panel_path), "--counts", str(artifact_dir / "backend_a_counts.csv"), "--masks", str(artifact_dir / "backend_a_masks.bin"), "--work-dir", str(work_dir / "backend_a"), "--run-report", str(work_dir / "backend_a_run.json")]
        b_command = [sys.executable, str(adapter_b), "--root", str(root), "--core", str(args.backend_b_core.resolve()), "--panel", str(panel_path), "--counts", str(artifact_dir / "backend_b_counts.csv"), "--masks", str(artifact_dir / "backend_b_masks.bin"), "--work-dir", str(work_dir / "backend_b"), "--run-report", str(work_dir / "backend_b_run.json")]
        commands["backend_a"] = run_logged(a_command, log_dir / "backend_a.stdout.log", log_dir / "backend_a.stderr.log")
        commands["backend_b"] = run_logged(b_command, log_dir / "backend_b.stdout.log", log_dir / "backend_b.stderr.log")

        rows_a = parse_counts(artifact_dir / "backend_a_counts.csv", panel)
        rows_b = parse_counts(artifact_dir / "backend_b_counts.csv", panel)
        masks_a, manifest_a = parse_masks(artifact_dir / "backend_a_masks.bin", 1, panel_path, root, "k4_ap_backend_a_trial_division_v1", rows_a)
        masks_b, manifest_b = parse_masks(artifact_dir / "backend_b_masks.bin", 2, panel_path, root, "k4_ap_backend_b_cpp17_mr7_brent_rho_v1", rows_b)
        if [int(row["T"]) for row in rows_a] != [int(row["T"]) for row in rows_b]:
            raise CensusError("backend pointwise T disagreement")
        if masks_a != masks_b:
            raise CensusError("backend pointwise winner-mask disagreement")
        validate_persistent(masks_a, panel, specs)

        selected, reasons = selected_direct_points(rows_a)
        direct_panel = work_dir / "direct_panel.csv"
        direct_raw = work_dir / "direct_oracle_raw.json"
        write_direct_panel(direct_panel, selected)
        direct_command = [str(args.direct_oracle.resolve()), "--input", str(direct_panel), "--output", str(direct_raw), "--jobs", str(args.direct_jobs)]
        commands["direct_oracle"] = run_logged(direct_command, log_dir / "direct_oracle.stdout.log", log_dir / "direct_oracle.stderr.log")
        mask_lookup = {(int(row["class_index"]), int(row["point_index"])): mask for row, mask in zip(rows_a, masks_a)}
        direct = verify_direct_raw(direct_raw, selected, reasons, mask_lookup, pairs)
        atomic_json(artifact_dir / "direct_verification.json", direct)

        class_summaries, aggregate = build_class_and_aggregate(rows_a, masks_a, specs)
        atomic_json(artifact_dir / "class_summaries.json", class_summaries)
        write_histogram(artifact_dir / "global_histogram.csv", aggregate["T_histogram"])
        response = coverage_response(rows_a, class_summaries)
        atomic_json(artifact_dir / "coverage_response.json", response)
        common, frequency_rows, frequency_highlights = common_and_frequencies(rows_a, masks_a, specs, pairs)
        atomic_json(artifact_dir / "common_uncovered.json", common)
        write_pair_frequencies(artifact_dir / "pair_frequencies.csv", frequency_rows)
        label, stopping = interpretation(response, aggregate)

        artifact_hashes = {
            name: sha256_file(artifact_dir / name)
            for name in ARTIFACT_NAMES if name != "metadata.json"
        }
        class_counts = Counter(len(class_points(spec)) for spec in specs)
        metadata = {
            "schema": "a303656-p4-maximizer-class-census-metadata-v1",
            "task": TASK, "classification": "EXACT FINITE COMPUTATION; GLOBAL A303656 PROBLEM UNRESOLVED",
            "mathematical_status": "UNRESOLVED", "validation_conclusion": "VALIDATED T3=2 FIXED-P4 MAXIMIZER-CLASS CENSUS",
            "source_parent_commit": args.source_parent, "source_commit": args.source_commit,
            "results_commit": RESULTS_COMMIT_SENTINEL,
            "fixed_domain": {"P4": list(P4), "M4": M4, "L": L, "activation_cell": [A, B], "n0": N0, "common_modulo_40_residue": N0 % 40, "active_pair_count": PAIR_COUNT, "constrained_G": CONSTRAINED_G, "constrained_argmax_count": MAXIMIZER_COUNT, "constrained_argmax_digest": CONSTRAINED_ARGMAX_DIGEST},
            "panel": {"class_count": CLASS_COUNT, "maximizing_class_count": MAXIMIZER_COUNT, "calibration_class_count": 3, "point_count": len(panel), "unique_point_count": len({row["n"] for row in panel}), "class_member_count_distribution": {str(key): value for key, value in sorted(class_counts.items())}, "class_panel_sha256": panel_digest(panel_path), "minimum_n": min(int(row["n"]) for row in panel), "maximum_n": max(int(row["n"]) for row in panel)},
            "backend_identities": {"A": {"adapter": "p4_census_backend_a_stream_adapter_v1", "core": "k4_ap_backend_a_trial_division_v1", **manifest_a}, "B": {"adapter": "p4_census_backend_b_keyed_adapter_v1", "core": "k4_ap_backend_b_cpp17_mr7_brent_rho_v1", **manifest_b}, "direct_oracle": {"implementation_id": "p4_census_direct_oracle_adapter_v1", "method": direct["oracle_method"]}},
            "agreement": {"pointwise_T_equal": True, "pointwise_masks_equal": True, "point_count": len(panel), "mask_bit_count_per_point": PAIR_COUNT, "popcount_equals_T_all_points": True, "persistent_covered_winner_count": 0},
            "direct_oracle": {"selected_point_count": direct["selected_point_count"], "verified_complete_mask_count": direct["verified_complete_mask_count"], "verified_canonical_witness_count": direct["verified_canonical_witness_count"]},
            "aggregate_G231": aggregate,
            "common_uncovered_summary": {"I_84_size": common["I_84_size"], "covered_by_at_least_one_maximizer_count": common["covered_by_at_least_one_maximizer_count"], "covered_by_all_84_count": common["covered_by_all_84_count"]},
            "winner_frequency_highlights": frequency_highlights,
            "predeclared_stopping_answers": stopping,
            "interpretation_label": label,
            "scope_guards": {"formal_integers_evaluated": len(panel), "integers_outside_panel_evaluated": 0, "new_primes": 0, "optimized_residue_tuples": 0, "adaptive_extensions": 0, "formal_class_count": CLASS_COUNT},
            "protected_baseline_and_landscape_sha256": protected,
            "raw_log_archive": {"directory_policy": "external under ~/code/a303656/archive", "archive_name": args.archive_name, "sha256": args.archive_sha256, "size_bytes": args.archive_size_bytes, "file_count": args.archive_file_count},
            "resource_use": {"runner_wall_seconds": format(time.monotonic() - started, ".6f"), "commands": commands, "formal_backend_diagnostic_rows_each": len(panel) * PAIR_COUNT, "direct_oracle_point_count": len(selected)},
            "artifact_sha256_excluding_metadata_and_verification_report": artifact_hashes,
            "caveats": ["This is a fixed finite panel, not a proof about all integers.", "Coverage-response comparisons across four fixed levels are observational and noncausal.", "Any T=0 point is only an UNVERIFIED COUNTEREXAMPLE CANDIDATE until a separate theorem verifier runs."],
        }
        atomic_json(artifact_dir / "metadata.json", metadata)
        print(f"formal_classes={CLASS_COUNT}")
        print(f"formal_points={len(panel)}")
        print(f"direct_points={len(selected)}")
        print(f"global_G231_minimum_T={aggregate['global_minimum_T']}")
        print(f"interpretation_label={label}")
        return 0
    except (CensusError, OSError, ValueError, KeyError, json.JSONDecodeError, csv.Error) as exc:
        print(f"p4_census_run: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
