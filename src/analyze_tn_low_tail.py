#!/usr/bin/env python3
"""Deterministic read-only analysis of the validated A303656 T(n) pilot."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import sys
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable


INTERVALS = {
    "PILOT-A": {
        "directory": "pilot_a",
        "low": 2,
        "high": 200002,
        "counts_sha256": "cf53f054c6a3055083470e45e2bafa9d2f5bc3a1d62b5c912bf255e87910bd2d",
    },
    "PILOT-B": {
        "directory": "pilot_b",
        "low": 240000000001,
        "high": 240000100001,
        "counts_sha256": "2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773",
    },
}
ROLES = ("bitset", "clean", "oracle")
QUANTILES = (
    ("0.1%", Fraction(1, 1000)),
    ("1%", Fraction(1, 100)),
    ("5%", Fraction(5, 100)),
    ("10%", Fraction(10, 100)),
    ("25%", Fraction(25, 100)),
    ("50%", Fraction(50, 100)),
    ("75%", Fraction(75, 100)),
    ("90%", Fraction(90, 100)),
    ("95%", Fraction(95, 100)),
    ("99%", Fraction(99, 100)),
    ("99.9%", Fraction(999, 1000)),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot load JSON object {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def write_object(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, header: list[str], rows: Iterable[list[object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def decimal_fraction(value: Fraction, places: int = 15) -> str:
    with localcontext() as context:
        context.prec = 60
        result = Decimal(value.numerator) / Decimal(value.denominator)
        quantum = Decimal(1).scaleb(-places)
        return format(result.quantize(quantum), "f")


def fraction_record(value: Fraction) -> dict:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": decimal_fraction(value),
    }


def parse_unsigned(text: str, label: str) -> int:
    if not text or not text.isascii() or not text.isdigit():
        raise ValueError(f"{label} must be canonical unsigned decimal")
    value = int(text)
    if str(value) != text:
        raise ValueError(f"{label} must not contain leading zeroes")
    return value


def read_counts(path: Path, low: int, high: int) -> list[int]:
    try:
        stream = path.open("r", encoding="utf-8", newline="")
    except OSError as error:
        raise ValueError(f"cannot open counts file {path}: {error}") from error
    values: list[int] = []
    with stream:
        reader = csv.reader(stream)
        try:
            header = next(reader)
        except StopIteration as error:
            raise ValueError(f"empty counts file: {path}") from error
        if header != ["n", "T"]:
            raise ValueError(f"counts header mismatch: {path}")
        for row_number, row in enumerate(reader, start=2):
            if len(row) != 2:
                raise ValueError(f"malformed row {row_number}: {path}")
            n = parse_unsigned(row[0], f"n at row {row_number}")
            count = parse_unsigned(row[1], f"T at row {row_number}")
            expected_n = low + len(values)
            if n != expected_n:
                raise ValueError(
                    f"missing, duplicate, out-of-order, or out-of-range n at row {row_number}: "
                    f"expected {expected_n}, got {n}"
                )
            if n >= high:
                raise ValueError(f"out-of-range n at row {row_number}: {n}")
            values.append(count)
    if len(values) != high - low:
        raise ValueError(f"row count mismatch: expected {high-low}, got {len(values)}")
    return values


def read_jsonl(path: Path) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValueError(f"cannot read JSONL {path}: {error}") from error
    records: list[dict] = []
    for line_number, line in enumerate(lines, start=1):
        if not line:
            raise ValueError(f"blank JSONL row {line_number}: {path}")
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"malformed JSONL row {line_number}: {path}: {error}") from error
        if not isinstance(value, dict):
            raise ValueError(f"object required at JSONL row {line_number}: {path}")
        records.append(value)
    return records


def normalized_records(records: list[dict]) -> list[dict]:
    result = []
    for source in records:
        row = dict(source)
        row.pop("implementation_id", None)
        result.append(row)
    return result


def verify_inputs(root: Path) -> tuple[dict[str, list[int]], dict[str, list[dict]], dict]:
    counts_by_interval: dict[str, list[int]] = {}
    low_by_interval: dict[str, list[dict]] = {}
    input_manifest: dict = {"intervals": {}}
    for interval_id, spec in INTERVALS.items():
        directory = root / spec["directory"]
        role_bytes: dict[str, bytes] = {}
        role_records: dict[str, list[dict]] = {}
        role_manifest: dict = {}
        for role in ROLES:
            role_dir = directory / role
            counts_path = role_dir / "counts.csv"
            low_path = role_dir / "low_t.jsonl"
            summary_path = role_dir / "summary.json"
            report_path = role_dir / "verifier_report.json"
            for path in (counts_path, low_path, summary_path, report_path):
                if not path.is_file():
                    raise ValueError(f"missing required input: {path}")
            role_bytes[role] = counts_path.read_bytes()
            counts_hash = sha256(counts_path)
            low_hash = sha256(low_path)
            if counts_hash != spec["counts_sha256"]:
                raise ValueError(f"{interval_id}/{role} counts hash differs from validated report")
            summary = load_object(summary_path)
            report = load_object(report_path)
            if summary.get("counts_csv_sha256") != counts_hash:
                raise ValueError(f"{interval_id}/{role} summary counts hash mismatch")
            if summary.get("low_t_jsonl_sha256") != low_hash:
                raise ValueError(f"{interval_id}/{role} summary low-T hash mismatch")
            if report.get("counts_csv_sha256") != counts_hash or report.get("status") != "PASS":
                raise ValueError(f"{interval_id}/{role} verifier report mismatch")
            role_records[role] = read_jsonl(low_path)
            role_manifest[role] = {
                "counts_path": str(counts_path),
                "counts_sha256": counts_hash,
                "low_t_path": str(low_path),
                "low_t_sha256": low_hash,
                "summary_sha256": sha256(summary_path),
                "verifier_report_sha256": sha256(report_path),
            }
        if not (role_bytes["bitset"] == role_bytes["clean"] == role_bytes["oracle"]):
            raise ValueError(f"{interval_id} three-way counts are not byte-identical")
        normalized = {role: normalized_records(records) for role, records in role_records.items()}
        if not (normalized["bitset"] == normalized["clean"] == normalized["oracle"]):
            raise ValueError(f"{interval_id} three-way low records differ mathematically")
        values = read_counts(
            directory / "bitset/counts.csv", int(spec["low"]), int(spec["high"])
        )
        counts_by_interval[interval_id] = values
        low_by_interval[interval_id] = role_records["bitset"]
        input_manifest["intervals"][interval_id] = {
            "canonical_counts_role": "bitset",
            "three_way_counts_byte_identical": True,
            "three_way_low_records_mathematically_identical": True,
            "roles": role_manifest,
        }
    return counts_by_interval, low_by_interval, input_manifest


def nearest_rank(sorted_values: list[int], probability: Fraction) -> int:
    if not sorted_values or probability <= 0 or probability > 1:
        raise ValueError("nearest-rank probability must be in (0,1]")
    numerator = probability.numerator * len(sorted_values)
    rank = (numerator + probability.denominator - 1) // probability.denominator
    return sorted_values[rank - 1]


def statistics(values: list[int], low: int, high: int) -> tuple[dict, Counter[int]]:
    if len(values) != high - low:
        raise ValueError("statistics width mismatch")
    ordered = sorted(values)
    total = sum(values)
    total_squares = sum(value * value for value in values)
    size = len(values)
    mean = Fraction(total, size)
    variance = Fraction(total_squares * size - total * total, size * size)
    with localcontext() as context:
        context.prec = 60
        standard_deviation = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    histogram = Counter(values)
    minimum = ordered[0]
    maximum = ordered[-1]
    argmin = [low + index for index, value in enumerate(values) if value == minimum]
    result = {
        "interval": {"low": str(low), "high_exclusive": str(high)},
        "row_count": size,
        "minimum": minimum,
        "maximum": maximum,
        "argmin_count": len(argmin),
        "argmin_n": [str(n) for n in argmin],
        "mean": fraction_record(mean),
        "population_variance": fraction_record(variance),
        "population_standard_deviation": format(standard_deviation, ".15f"),
        "median": nearest_rank(ordered, Fraction(1, 2)),
        "quantiles": {
            label: nearest_rank(ordered, probability) for label, probability in QUANTILES
        },
        "histogram_total": sum(histogram.values()),
        "distinct_T_count": len(histogram),
    }
    return result, histogram


def block_minima(values: list[int], low: int, width: int) -> list[dict]:
    if len(values) % width != 0:
        raise ValueError(f"interval width is not divisible by block width {width}")
    result = []
    for block_index, offset in enumerate(range(0, len(values), width)):
        block = values[offset : offset + width]
        minimum = min(block)
        argmin = [low + offset + index for index, value in enumerate(block) if value == minimum]
        result.append(
            {
                "block_index": block_index,
                "start": low + offset,
                "end_exclusive": low + offset + width,
                "minimum_T": minimum,
                "argmin_n": argmin,
            }
        )
    return result


def record_lows(interval_id: str, values: list[int], low: int) -> list[list[object]]:
    rows: list[list[object]] = []
    best: int | None = None
    sequence = 0
    for index, value in enumerate(values):
        if best is None or value < best:
            rows.append([interval_id, "left_to_right", sequence, low + index, value, "" if best is None else best])
            best = value
            sequence += 1
    best = None
    sequence = 0
    for index in range(len(values) - 1, -1, -1):
        value = values[index]
        if best is None or value < best:
            rows.append([interval_id, "right_to_left", sequence, low + index, value, "" if best is None else best])
            best = value
            sequence += 1
    return rows


def local_minima(interval_id: str, values: list[int], low: int) -> tuple[list[list[object]], dict]:
    rows: list[list[object]] = []
    strict_count = 0
    weak_count = 0
    for index, value in enumerate(values):
        left = values[index - 1] if index > 0 else None
        right = values[index + 1] if index + 1 < len(values) else None
        strict = (left is None or value < left) and (right is None or value < right)
        weak = (left is None or value <= left) and (right is None or value <= right)
        position = "interior"
        if index == 0:
            position = "left_endpoint"
        elif index + 1 == len(values):
            position = "right_endpoint"
        if strict:
            rows.append([interval_id, "strict", low + index, low + index, 1, value, position, "" if left is None else left, "" if right is None else right])
            strict_count += 1
        if weak:
            rows.append([interval_id, "weak", low + index, low + index, 1, value, position, "" if left is None else left, "" if right is None else right])
            weak_count += 1

    plateau_count = 0
    index = 0
    while index < len(values):
        end = index + 1
        while end < len(values) and values[end] == values[index]:
            end += 1
        if end - index >= 2:
            left = values[index - 1] if index > 0 else None
            right = values[end] if end < len(values) else None
            if (left is None or values[index] < left) and (right is None or values[index] < right):
                position = "interior"
                if index == 0:
                    position = "left_endpoint"
                elif end == len(values):
                    position = "right_endpoint"
                rows.append([
                    interval_id,
                    "plateau",
                    low + index,
                    low + end - 1,
                    end - index,
                    values[index],
                    position,
                    "" if left is None else left,
                    "" if right is None else right,
                ])
                plateau_count += 1
        index = end
    return rows, {
        "strict_local_minimum_count": strict_count,
        "weak_local_minimum_count": weak_count,
        "plateau_minimum_count": plateau_count,
    }


def neighborhood(values: list[int], low: int, n0: int, radius: int) -> tuple[list[list[object]], dict]:
    center_index = n0 - low
    if center_index - radius < 0 or center_index + radius >= len(values):
        raise ValueError("neighborhood would read outside the validated interval")
    center = values[center_index]
    rows = []
    window_values = []
    for n in range(n0 - radius, n0 + radius + 1):
        value = values[n - low]
        rows.append([n, value, n - n0, value - center])
        window_values.append(value)

    same_left = next(
        (n for n in range(n0 - 1, low - 1, -1) if values[n - low] == center), None
    )
    same_right = next(
        (low + index for index in range(center_index + 1, len(values)) if values[index] == center), None
    )

    plateau_start = center_index
    while plateau_start > 0 and values[plateau_start - 1] == center:
        plateau_start -= 1
    plateau_end = center_index
    while plateau_end + 1 < len(values) and values[plateau_end + 1] == center:
        plateau_end += 1

    def side_profile(sequence: list[int]) -> dict:
        upward = sum(right > left for left, right in zip(sequence, sequence[1:]))
        equal = sum(right == left for left, right in zip(sequence, sequence[1:]))
        downward = sum(right < left for left, right in zip(sequence, sequence[1:]))
        monotone_steps = 0
        previous = center
        for value in sequence:
            if value > previous:
                monotone_steps += 1
                previous = value
            else:
                break
        mean = Fraction(sum(sequence), len(sequence))
        return {
            "minimum": min(sequence),
            "maximum": max(sequence),
            "mean": fraction_record(mean),
            "first_step_delta_from_argmin": sequence[0] - center,
            "strictly_increasing_steps_away_from_argmin": monotone_steps,
            "adjacent_movements_away_from_argmin": {
                "up": upward,
                "equal": equal,
                "down": downward,
            },
        }

    left_away = list(reversed(window_values[:radius]))
    right_away = window_values[radius + 1 :]
    window_mean = Fraction(sum(window_values), len(window_values))
    result = {
        "n0": str(n0),
        "T_n0": center,
        "window": {"low_inclusive": str(n0 - radius), "high_inclusive": str(n0 + radius), "row_count": 2 * radius + 1},
        "strict_local_minimum": values[center_index - 1] > center and values[center_index + 1] > center,
        "nearest_same_value": {
            "left_n": None if same_left is None else str(same_left),
            "left_distance": None if same_left is None else n0 - same_left,
            "right_n": None if same_right is None else str(same_right),
            "right_distance": None if same_right is None else same_right - n0,
        },
        "left_side_away_from_argmin": side_profile(left_away),
        "right_side_away_from_argmin": side_profile(right_away),
        "window_distinct_T_values": sorted(set(window_values)),
        "window_mean": fraction_record(window_mean),
        "window_mean_minus_argmin": fraction_record(window_mean - center),
        "equal_value_plateau_containing_argmin": {
            "start_n": str(low + plateau_start),
            "end_n": str(low + plateau_end),
            "width": plateau_end - plateau_start + 1,
            "wide_plateau": plateau_end > plateau_start,
        },
    }
    return rows, result


def validate_winner_records(
    counts: dict[str, list[int]], low_records: dict[str, list[dict]]
) -> tuple[dict, list[list[object]], list[list[object]]]:
    details: list[dict] = []
    pair_counters: dict[str, dict[str, Counter]] = {}
    shift_counters: dict[str, Counter] = {}
    shift_pairs: dict[str, dict[int, set[tuple[int, int]]]] = {}
    occurrence_ns: dict[tuple[str, str, object], list[int]] = defaultdict(list)

    for interval_id in INTERVALS:
        pair_counters[interval_id] = {
            "c": Counter(),
            "d": Counter(),
            "exponent_pair": Counter(),
            "remainder": Counter(),
        }
        shift_counters[interval_id] = Counter()
        shift_pairs[interval_id] = defaultdict(set)
        low = int(INTERVALS[interval_id]["low"])
        high = int(INTERVALS[interval_id]["high"])
        seen_n: set[int] = set()
        for record in low_records[interval_id]:
            n = parse_unsigned(str(record.get("n", "")), "low-record n")
            if n in seen_n or not low <= n < high:
                raise ValueError(f"duplicate or out-of-range low record n={n}")
            seen_n.add(n)
            count = int(record.get("T", -1))
            if count != counts[interval_id][n - low]:
                raise ValueError(f"low-record T mismatch at n={n}")
            active = int(record.get("active_exponent_pair_count", -1))
            if active <= 0 or count > active:
                raise ValueError(f"invalid active exponent-pair count at n={n}")
            winners = record.get("winning_exponent_pairs")
            if not isinstance(winners, list) or len(winners) != count:
                raise ValueError(f"winner-list length mismatch at n={n}")
            keys: set[tuple[int, int]] = set()
            shift_map: dict[int, list[dict]] = defaultdict(list)
            copied_winners = []
            for winner in winners:
                c = int(winner["c"])
                d = int(winner["d"])
                key = (c, d)
                if key in keys:
                    raise ValueError(f"duplicate source exponent pair at n={n}: {key}")
                keys.add(key)
                shift = parse_unsigned(str(winner["shift"]), "winner shift")
                remainder = parse_unsigned(str(winner["remainder"]), "winner remainder")
                a = parse_unsigned(str(winner["a"]), "winner a")
                b = parse_unsigned(str(winner["b"]), "winner b")
                if shift != 3**c + 5**d or remainder != n - shift or a > b:
                    raise ValueError(f"winner source/remainder/order mismatch at n={n}")
                if a * a + b * b != remainder:
                    raise ValueError(f"winner equation mismatch at n={n}")
                pair_counters[interval_id]["c"][c] += 1
                pair_counters[interval_id]["d"][d] += 1
                pair_counters[interval_id]["exponent_pair"][key] += 1
                pair_counters[interval_id]["remainder"][remainder] += 1
                shift_counters[interval_id][shift] += 1
                shift_pairs[interval_id][shift].add(key)
                for dimension, value in (("c", c), ("d", d), ("exponent_pair", key), ("remainder", remainder)):
                    occurrence_ns[(interval_id, dimension, value)].append(n)
                occurrence_ns[(interval_id, "shift", shift)].append(n)
                copied = {
                    "c": c,
                    "d": d,
                    "shift": str(shift),
                    "remainder": str(remainder),
                    "canonical_witness": {"a": str(a), "b": str(b)},
                }
                copied_winners.append(copied)
                shift_map[shift].append(copied)
            duplicate_shifts = [
                {
                    "shift": str(shift),
                    "source_exponent_pairs": [
                        {"c": row["c"], "d": row["d"]} for row in rows
                    ],
                }
                for shift, rows in sorted(shift_map.items())
                if len(rows) > 1
            ]
            details.append(
                {
                    "interval_id": interval_id,
                    "n": str(n),
                    "T": count,
                    "active_exponent_pair_count": active,
                    "T_over_active": fraction_record(Fraction(count, active)),
                    "winning_exponent_pairs": copied_winners,
                    "duplicate_numerical_shifts": duplicate_shifts,
                    "sole_winner": copied_winners[0] if count == 1 else None,
                }
            )

    for interval_id in INTERVALS:
        pair_counters[interval_id]["winner_total"] = Counter({"total": sum(shift_counters[interval_id].values())})

    combined_pair: dict[str, Counter] = {
        dimension: pair_counters["PILOT-A"][dimension] + pair_counters["PILOT-B"][dimension]
        for dimension in ("c", "d", "exponent_pair", "remainder")
    }
    combined_shift = shift_counters["PILOT-A"] + shift_counters["PILOT-B"]
    combined_shift_pairs: dict[int, set[tuple[int, int]]] = defaultdict(set)
    for interval_id in INTERVALS:
        for shift, pairs in shift_pairs[interval_id].items():
            combined_shift_pairs[shift].update(pairs)

    pair_rows: list[list[object]] = []
    dimension_order = ("c", "d", "exponent_pair", "remainder")
    for interval_id in (*INTERVALS.keys(), "COMBINED"):
        counters = pair_counters[interval_id] if interval_id != "COMBINED" else combined_pair
        for dimension in dimension_order:
            for value, frequency in sorted(counters[dimension].items(), key=lambda item: item[0]):
                c: object = ""
                d: object = ""
                display: object = value
                if dimension == "exponent_pair":
                    c, d = value
                    display = f"{c},{d}"
                elif dimension == "c":
                    c = value
                elif dimension == "d":
                    d = value
                ns = []
                if interval_id == "COMBINED":
                    for source_interval in INTERVALS:
                        ns.extend(occurrence_ns[(source_interval, dimension, value)])
                else:
                    ns = occurrence_ns[(interval_id, dimension, value)]
                pair_rows.append([
                    interval_id,
                    dimension,
                    c,
                    d,
                    display,
                    frequency,
                    min(ns),
                    max(ns),
                ])

    shift_rows: list[list[object]] = []
    for interval_id in (*INTERVALS.keys(), "COMBINED"):
        counter = shift_counters[interval_id] if interval_id != "COMBINED" else combined_shift
        pair_map = shift_pairs[interval_id] if interval_id != "COMBINED" else combined_shift_pairs
        for shift, frequency in sorted(counter.items()):
            pairs = sorted(pair_map[shift])
            ns = []
            if interval_id == "COMBINED":
                for source_interval in INTERVALS:
                    ns.extend(occurrence_ns[(source_interval, "shift", shift)])
            else:
                ns = occurrence_ns[(interval_id, "shift", shift)]
            shift_rows.append([
                interval_id,
                shift,
                frequency,
                len(pairs),
                ";".join(f"{c}:{d}" for c, d in pairs),
                min(ns),
                max(ns),
            ])

    detail_object = {
        "schema": "a303656-tn-low-record-details-v1",
        "classification": "FINITE COMPUTATIONAL OBSERVATION FROM VALIDATED PILOT OUTPUTS",
        "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
        "record_count": len(details),
        "winner_totals": {
            interval_id: sum(shift_counters[interval_id].values()) for interval_id in INTERVALS
        },
        "records": sorted(details, key=lambda row: (row["interval_id"], int(row["n"]))),
        "T_equals_1_sole_winners": [
            {"n": row["n"], "winner": row["sole_winner"]}
            for row in details
            if row["T"] == 1
        ],
    }
    return detail_object, pair_rows, shift_rows


def recommended_panel(
    stats: dict[str, dict],
    values_b: list[int],
    low_b: int,
    low_levels: list[dict],
    blocks_10k: list[dict],
) -> dict:
    selected: dict[tuple[str, int], dict] = {}

    def add(interval_id: str, n: int, rule: str) -> None:
        key = (interval_id, n)
        if key not in selected:
            selected[key] = {
                "interval_id": interval_id,
                "n": str(n),
                "T": stats[interval_id]["minimum"] if interval_id == "PILOT-A" else values_b[n - low_b],
                "mechanical_selection_rules": [],
            }
        selected[key]["mechanical_selection_rules"].append(rule)

    for n_text in stats["PILOT-A"]["argmin_n"]:
        add("PILOT-A", int(n_text), "all PILOT-A global argmin rows (the four T=1 integers)")
    for level_index, level in enumerate(low_levels):
        n = int(level["first_25_n"][0])
        add(
            "PILOT-B",
            n,
            f"smallest n at PILOT-B distinct low-T level rank {level_index + 1} (T={level['T']})",
        )

    covered_blocks: set[int] = set()
    for block in blocks_10k:
        candidates = set(block["argmin_n"])
        for (interval_id, n), row in selected.items():
            if interval_id == "PILOT-B" and n in candidates:
                row["mechanical_selection_rules"].append(
                    f"argmin of 10,000-wide PILOT-B block {block['block_index']}"
                )
                covered_blocks.add(block["block_index"])
    for block in blocks_10k:
        if len(covered_blocks) >= 2:
            break
        if block["block_index"] in covered_blocks:
            continue
        n = block["argmin_n"][0]
        add(
            "PILOT-B",
            n,
            f"smallest argmin of earliest not-yet-covered 10,000-wide block {block['block_index']}",
        )
        covered_blocks.add(block["block_index"])

    panel = sorted(selected.values(), key=lambda row: (row["interval_id"], int(row["n"])))
    if len(panel) > 12 or len(covered_blocks) < 2:
        raise ValueError("recommended obstruction panel constraints were not met")
    return {
        "schema": "a303656-recommended-obstruction-panel-v1",
        "classification": "DETERMINISTIC FUTURE FIXTURE PROPOSAL; NO FACTORIZATION RUN",
        "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
        "maximum_panel_size": 12,
        "panel_size": len(panel),
        "covered_pilot_b_10k_block_indices": sorted(covered_blocks),
        "selection_order": [
            "all PILOT-A global argmin rows",
            "smallest n at each of the five lowest distinct PILOT-B T levels",
            "earliest 10,000-wide PILOT-B block minima until at least two blocks are covered",
        ],
        "panel": panel,
    }


def analyze(input_root: Path, output_dir: Path) -> None:
    input_root = input_root.resolve(strict=True)
    if output_dir.exists():
        raise ValueError(f"refusing to overwrite output directory: {output_dir}")
    output_dir.mkdir(parents=True)
    try:
        counts, low_records, input_manifest = verify_inputs(input_root)
        summary: dict = {
            "schema": "a303656-tn-low-tail-summary-statistics-v1",
            "classification": "FINITE COMPUTATIONAL OBSERVATION FROM 300000 VALIDATED PILOT ROWS",
            "quantile_definition": (
                "Empirical inverse-CDF nearest rank: for 0<p<=1 and N sorted values, "
                "Q(p)=x[ceil(p*N)-1]. Median is Q(0.5). No interpolation is used."
            ),
            "population_variance_definition": "N^{-1} sum_i (T_i - mean)^2",
            "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
            "intervals": {},
        }
        histograms: dict[str, Counter[int]] = {}
        histogram_rows: list[list[object]] = []
        cdf_rows: list[list[object]] = []
        record_rows: list[list[object]] = []
        local_rows: list[list[object]] = []
        for interval_id, spec in INTERVALS.items():
            values = counts[interval_id]
            interval_stats, histogram = statistics(values, int(spec["low"]), int(spec["high"]))
            local_for_interval, local_counts = local_minima(interval_id, values, int(spec["low"]))
            interval_stats["local_minimum_profile"] = local_counts
            summary["intervals"][interval_id] = interval_stats
            histograms[interval_id] = histogram
            cumulative = 0
            for value, frequency in sorted(histogram.items()):
                cumulative += frequency
                histogram_rows.append([
                    interval_id,
                    value,
                    frequency,
                    f"{frequency}/{len(values)}",
                    decimal_fraction(Fraction(frequency, len(values))),
                ])
                cdf_rows.append([
                    interval_id,
                    value,
                    frequency,
                    cumulative,
                    f"{cumulative}/{len(values)}",
                    decimal_fraction(Fraction(cumulative, len(values))),
                ])
            record_rows.extend(record_lows(interval_id, values, int(spec["low"])))
            local_rows.extend(local_for_interval)

        values_b = counts["PILOT-B"]
        low_b = int(INTERVALS["PILOT-B"]["low"])
        lowest_levels = sorted(histograms["PILOT-B"])[:5]
        low_levels = []
        for level in lowest_levels:
            ns = [low_b + index for index, value in enumerate(values_b) if value == level]
            low_levels.append({"T": level, "count": len(ns), "first_25_n": [str(n) for n in ns[:25]]})
        low_level_object = {
            "schema": "a303656-pilot-b-low-levels-v1",
            "selection_rule": "global minimum and the next four smallest distinct T levels",
            "levels": low_levels,
        }
        blocks_1k = block_minima(values_b, low_b, 1000)
        blocks_10k = block_minima(values_b, low_b, 10000)
        neighborhood_rows, neighborhood_object = neighborhood(
            values_b, low_b, 240000005594, 100
        )
        details, pair_rows, shift_rows = validate_winner_records(counts, low_records)
        panel = recommended_panel(summary["intervals"], values_b, low_b, low_levels, blocks_10k)

        metadata = {
            "schema": "a303656-tn-read-only-low-tail-analysis-metadata-v1",
            "classification": "READ-ONLY FINITE COMPUTATIONAL ANALYSIS; NOT A THEOREM",
            "input_scope": "only output/tn_pilot_20260713 PILOT-A and PILOT-B committed artifacts",
            "canonical_counts_source": {
                "PILOT-A": "pilot_a/bitset/counts.csv",
                "PILOT-B": "pilot_b/bitset/counts.csv",
            },
            "canonical_source_selected_only_after_three_way_byte_equality": True,
            "new_integer_intervals_scanned": False,
            "counting_executables_invoked": False,
            "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
            "input_manifest": input_manifest,
        }

        write_object(output_dir / "metadata.json", metadata)
        write_object(output_dir / "summary_statistics.json", summary)
        write_csv(
            output_dir / "histogram.csv",
            ["interval_id", "T", "count", "probability_exact", "probability_decimal"],
            histogram_rows,
        )
        write_csv(
            output_dir / "lower_tail_cdf.csv",
            ["interval_id", "T", "count_at_T", "cumulative_count", "cumulative_fraction_exact", "cumulative_fraction_decimal"],
            cdf_rows,
        )
        write_object(output_dir / "pilot_b_low_levels.json", low_level_object)
        for filename, blocks in (
            ("pilot_b_local_minima_1k.csv", blocks_1k),
            ("pilot_b_local_minima_10k.csv", blocks_10k),
        ):
            write_csv(
                output_dir / filename,
                ["block_index", "start_n", "end_exclusive", "minimum_T", "argmin_count", "argmin_n"],
                [
                    [
                        block["block_index"],
                        block["start"],
                        block["end_exclusive"],
                        block["minimum_T"],
                        len(block["argmin_n"]),
                        ";".join(str(n) for n in block["argmin_n"]),
                    ]
                    for block in blocks
                ],
            )
        write_csv(
            output_dir / "pilot_b_argmin_neighborhood.csv",
            ["n", "T", "n_minus_n0", "T_minus_T_n0"],
            neighborhood_rows,
        )
        write_object(output_dir / "pilot_b_argmin_neighborhood.json", neighborhood_object)
        write_csv(
            output_dir / "record_lows.csv",
            ["interval_id", "direction", "sequence_index", "n", "T", "previous_record_T"],
            record_rows,
        )
        write_csv(
            output_dir / "local_minima.csv",
            ["interval_id", "minimum_type", "start_n", "end_n", "width", "T", "position", "left_neighbor_T", "right_neighbor_T"],
            local_rows,
        )
        write_csv(
            output_dir / "winner_pair_frequency.csv",
            ["interval_id", "dimension", "c", "d", "value", "frequency", "first_n", "last_n"],
            pair_rows,
        )
        write_csv(
            output_dir / "winner_shift_frequency.csv",
            ["interval_id", "shift", "frequency", "distinct_exponent_pair_count", "exponent_pairs", "first_n", "last_n"],
            shift_rows,
        )
        write_object(output_dir / "low_record_details.json", details)
        write_object(output_dir / "recommended_obstruction_panel.json", panel)

        output_hashes = {
            path.name: sha256(path)
            for path in sorted(output_dir.iterdir())
            if path.is_file()
        }
        write_object(
            output_dir / "artifact_manifest.json",
            {
                "schema": "a303656-tn-low-tail-artifact-manifest-v1",
                "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
                "outputs_sha256": output_hashes,
            },
        )
    except Exception:
        shutil.rmtree(output_dir)
        raise


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--input-root", type=Path, required=True)
    run_parser.add_argument("--output-dir", type=Path, required=True)
    validate_parser = subparsers.add_parser("validate-counts")
    validate_parser.add_argument("--counts", type=Path, required=True)
    validate_parser.add_argument("--low", type=int, required=True)
    validate_parser.add_argument("--high", type=int, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    if args.command == "validate-counts":
        values = read_counts(args.counts, args.low, args.high)
        print(f"COUNTS_VALID rows={len(values)} minimum={min(values)} maximum={max(values)}")
        return 0
    analyze(args.input_root, args.output_dir)
    print("READ_ONLY_TN_LOW_TAIL_ANALYSIS_PASS")
    print(f"output_directory={args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, csv.Error) as error:
        print(f"LOW_TAIL_ANALYSIS_ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
