#!/usr/bin/env python3
"""Independent verification of read-only T(n) low-tail analysis artifacts.

This file intentionally does not import src/analyze_tn_low_tail.py.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


INTERVALS = {
    "PILOT-A": ("pilot_a", 2, 200002, "cf53f054c6a3055083470e45e2bafa9d2f5bc3a1d62b5c912bf255e87910bd2d"),
    "PILOT-B": ("pilot_b", 240000000001, 240000100001, "2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773"),
}
ROLES = ("bitset", "clean", "oracle")
PROBABILITIES = (
    ("0.1%", 1, 1000),
    ("1%", 1, 100),
    ("5%", 5, 100),
    ("10%", 10, 100),
    ("25%", 25, 100),
    ("50%", 50, 100),
    ("75%", 75, 100),
    ("90%", 90, 100),
    ("95%", 95, 100),
    ("99%", 99, 100),
    ("99.9%", 999, 1000),
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1048576)
            if not block:
                return digest.hexdigest()
            digest.update(block)


def obj(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"object required: {path}")
    return value


def rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.reader(stream))


def counts(path: Path, low: int, high: int) -> list[int]:
    data = rows(path)
    if not data or data[0] != ["n", "T"] or len(data) != high - low + 1:
        raise ValueError(f"counts shape failure: {path}")
    result = []
    for offset, row in enumerate(data[1:]):
        if len(row) != 2 or not all(field.isascii() and field.isdigit() for field in row):
            raise ValueError(f"malformed counts row: {path}:{offset+2}")
        n = int(row[0])
        value = int(row[1])
        if str(n) != row[0] or str(value) != row[1] or n != low + offset:
            raise ValueError(f"noncanonical or out-of-order counts row: {path}:{offset+2}")
        result.append(value)
    return result


def decimal_fraction(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 60
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
        return format(decimal.quantize(Decimal("0.000000000000001")), "f")


def fraction_obj(value: Fraction) -> dict:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": decimal_fraction(value),
    }


def quantile(ordered: list[int], numerator: int, denominator: int) -> int:
    product = numerator * len(ordered)
    rank = (product + denominator - 1) // denominator
    return ordered[rank - 1]


def computed_statistics(values: list[int], low: int, high: int) -> tuple[dict, Counter[int]]:
    ordered = sorted(values)
    size = len(values)
    total = sum(values)
    squares = sum(value * value for value in values)
    mean = Fraction(total, size)
    variance = Fraction(squares * size - total * total, size * size)
    with localcontext() as context:
        context.prec = 60
        deviation = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    minimum = ordered[0]
    argmin = [low + index for index, value in enumerate(values) if value == minimum]
    histogram = Counter(values)
    return {
        "interval": {"low": str(low), "high_exclusive": str(high)},
        "row_count": size,
        "minimum": minimum,
        "maximum": ordered[-1],
        "argmin_count": len(argmin),
        "argmin_n": [str(n) for n in argmin],
        "mean": fraction_obj(mean),
        "population_variance": fraction_obj(variance),
        "population_standard_deviation": format(deviation, ".15f"),
        "median": quantile(ordered, 1, 2),
        "quantiles": {
            label: quantile(ordered, numerator, denominator)
            for label, numerator, denominator in PROBABILITIES
        },
        "histogram_total": sum(histogram.values()),
        "distinct_T_count": len(histogram),
    }, histogram


def expected_block_rows(values: list[int], low: int, width: int) -> list[list[str]]:
    result = [["block_index", "start_n", "end_exclusive", "minimum_T", "argmin_count", "argmin_n"]]
    for block_index, offset in enumerate(range(0, len(values), width)):
        block = values[offset : offset + width]
        minimum = min(block)
        argmin = [str(low + offset + index) for index, value in enumerate(block) if value == minimum]
        result.append([
            str(block_index),
            str(low + offset),
            str(low + offset + width),
            str(minimum),
            str(len(argmin)),
            ";".join(argmin),
        ])
    return result


def expected_record_rows(interval_id: str, values: list[int], low: int) -> list[list[str]]:
    result: list[list[str]] = []
    current = None
    sequence = 0
    for index, value in enumerate(values):
        if current is None or value < current:
            result.append([interval_id, "left_to_right", str(sequence), str(low + index), str(value), "" if current is None else str(current)])
            current = value
            sequence += 1
    current = None
    sequence = 0
    for index in range(len(values) - 1, -1, -1):
        value = values[index]
        if current is None or value < current:
            result.append([interval_id, "right_to_left", str(sequence), str(low + index), str(value), "" if current is None else str(current)])
            current = value
            sequence += 1
    return result


def expected_local_rows(interval_id: str, values: list[int], low: int) -> tuple[list[list[str]], dict]:
    result: list[list[str]] = []
    strict_count = 0
    weak_count = 0
    for index, value in enumerate(values):
        left = values[index - 1] if index else None
        right = values[index + 1] if index + 1 < len(values) else None
        position = "left_endpoint" if index == 0 else "right_endpoint" if index + 1 == len(values) else "interior"
        base = [str(low + index), str(low + index), "1", str(value), position, "" if left is None else str(left), "" if right is None else str(right)]
        if (left is None or value < left) and (right is None or value < right):
            result.append([interval_id, "strict", *base])
            strict_count += 1
        if (left is None or value <= left) and (right is None or value <= right):
            result.append([interval_id, "weak", *base])
            weak_count += 1
    plateau_count = 0
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[end] == values[start]:
            end += 1
        left = values[start - 1] if start else None
        right = values[end] if end < len(values) else None
        if end - start >= 2 and (left is None or values[start] < left) and (right is None or values[start] < right):
            position = "left_endpoint" if start == 0 else "right_endpoint" if end == len(values) else "interior"
            result.append([
                interval_id,
                "plateau",
                str(low + start),
                str(low + end - 1),
                str(end - start),
                str(values[start]),
                position,
                "" if left is None else str(left),
                "" if right is None else str(right),
            ])
            plateau_count += 1
        start = end
    return result, {
        "strict_local_minimum_count": strict_count,
        "weak_local_minimum_count": weak_count,
        "plateau_minimum_count": plateau_count,
    }


def parse_jsonl(path: Path) -> list[dict]:
    result = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line:
            raise ValueError(f"blank JSONL row: {path}:{line_number}")
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"object required: {path}:{line_number}")
        result.append(value)
    return result


def expected_frequencies(input_root: Path) -> tuple[dict, dict, dict]:
    dimension_counters: dict[str, dict[str, Counter]] = {}
    shift_counters: dict[str, Counter] = {}
    winner_totals: dict[str, int] = {}
    for interval_id, (directory, _, _, _) in INTERVALS.items():
        dimension_counters[interval_id] = {
            "c": Counter(),
            "d": Counter(),
            "exponent_pair": Counter(),
            "remainder": Counter(),
        }
        shift_counters[interval_id] = Counter()
        total = 0
        for record in parse_jsonl(input_root / directory / "bitset/low_t.jsonl"):
            winners = record["winning_exponent_pairs"]
            if len(winners) != int(record["T"]):
                raise ValueError("input winner total mismatch")
            for winner in winners:
                c = int(winner["c"])
                d = int(winner["d"])
                remainder = int(winner["remainder"])
                shift = int(winner["shift"])
                dimension_counters[interval_id]["c"][c] += 1
                dimension_counters[interval_id]["d"][d] += 1
                dimension_counters[interval_id]["exponent_pair"][(c, d)] += 1
                dimension_counters[interval_id]["remainder"][remainder] += 1
                shift_counters[interval_id][shift] += 1
                total += 1
        winner_totals[interval_id] = total
    return dimension_counters, shift_counters, winner_totals


def verify_frequency_files(input_root: Path, analysis_dir: Path) -> dict:
    dimensions, shifts, totals = expected_frequencies(input_root)
    pair_data = rows(analysis_dir / "winner_pair_frequency.csv")
    shift_data = rows(analysis_dir / "winner_shift_frequency.csv")
    if pair_data[0] != ["interval_id", "dimension", "c", "d", "value", "frequency", "first_n", "last_n"]:
        raise ValueError("winner pair frequency header mismatch")
    if shift_data[0] != ["interval_id", "shift", "frequency", "distinct_exponent_pair_count", "exponent_pairs", "first_n", "last_n"]:
        raise ValueError("winner shift frequency header mismatch")
    observed_dimensions: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for row in pair_data[1:]:
        if len(row) != 8:
            raise ValueError("malformed winner pair frequency row")
        interval_id, dimension, c_text, d_text, value_text, frequency_text, _, _ = row
        if interval_id == "COMBINED":
            continue
        if dimension == "exponent_pair":
            key: object = (int(c_text), int(d_text))
        else:
            key = int(value_text)
        observed_dimensions[(interval_id, dimension)][key] = int(frequency_text)
    for interval_id in INTERVALS:
        for dimension in ("c", "d", "exponent_pair", "remainder"):
            if observed_dimensions[(interval_id, dimension)] != dimensions[interval_id][dimension]:
                raise ValueError(f"winner frequency mismatch: {interval_id}/{dimension}")
    observed_shifts: dict[str, Counter] = defaultdict(Counter)
    for row in shift_data[1:]:
        if len(row) != 7:
            raise ValueError("malformed winner shift frequency row")
        if row[0] != "COMBINED":
            observed_shifts[row[0]][int(row[1])] = int(row[2])
    for interval_id in INTERVALS:
        if observed_shifts[interval_id] != shifts[interval_id]:
            raise ValueError(f"winner shift frequency mismatch: {interval_id}")
    details = obj(analysis_dir / "low_record_details.json")
    if details.get("winner_totals") != totals:
        raise ValueError("low-record winner totals mismatch")
    if int(details.get("record_count", -1)) != 57:
        raise ValueError("low-record detail count mismatch")
    return {"record_count": 57, "winner_totals": totals}


def verify(input_root: Path, analysis_dir: Path) -> dict:
    input_root = input_root.resolve(strict=True)
    analysis_dir = analysis_dir.resolve(strict=True)
    metadata = obj(analysis_dir / "metadata.json")
    if metadata.get("counting_executables_invoked") is not False or metadata.get("new_integer_intervals_scanned") is not False:
        raise ValueError("read-only metadata discipline failure")
    if metadata.get("obstruction_data_status") != "SCHEMA_ONLY_NOT_COLLECTED":
        raise ValueError("obstruction status mismatch")

    values_by_interval: dict[str, list[int]] = {}
    histograms: dict[str, Counter[int]] = {}
    expected_statistics: dict[str, dict] = {}
    expected_record_data = [["interval_id", "direction", "sequence_index", "n", "T", "previous_record_T"]]
    expected_local_data = [["interval_id", "minimum_type", "start_n", "end_n", "width", "T", "position", "left_neighbor_T", "right_neighbor_T"]]
    for interval_id, (directory, low, high, expected_hash) in INTERVALS.items():
        count_paths = [input_root / directory / role / "counts.csv" for role in ROLES]
        payloads = [path.read_bytes() for path in count_paths]
        if not (payloads[0] == payloads[1] == payloads[2]):
            raise ValueError(f"{interval_id} three-way input mismatch")
        if any(sha(path) != expected_hash for path in count_paths):
            raise ValueError(f"{interval_id} validated input hash mismatch")
        values = counts(count_paths[0], low, high)
        values_by_interval[interval_id] = values
        stats, histogram = computed_statistics(values, low, high)
        local_rows, local_profile = expected_local_rows(interval_id, values, low)
        stats["local_minimum_profile"] = local_profile
        expected_statistics[interval_id] = stats
        histograms[interval_id] = histogram
        expected_record_data.extend(expected_record_rows(interval_id, values, low))
        expected_local_data.extend(local_rows)

    summary = obj(analysis_dir / "summary_statistics.json")
    if summary.get("intervals") != expected_statistics:
        raise ValueError("independent summary/quantile reconstruction mismatch")
    if summary.get("obstruction_data_status") != "SCHEMA_ONLY_NOT_COLLECTED":
        raise ValueError("summary obstruction status mismatch")

    expected_histogram = [["interval_id", "T", "count", "probability_exact", "probability_decimal"]]
    expected_cdf = [["interval_id", "T", "count_at_T", "cumulative_count", "cumulative_fraction_exact", "cumulative_fraction_decimal"]]
    for interval_id in INTERVALS:
        size = len(values_by_interval[interval_id])
        cumulative = 0
        for value, frequency in sorted(histograms[interval_id].items()):
            cumulative += frequency
            expected_histogram.append([interval_id, str(value), str(frequency), f"{frequency}/{size}", decimal_fraction(Fraction(frequency, size))])
            expected_cdf.append([interval_id, str(value), str(frequency), str(cumulative), f"{cumulative}/{size}", decimal_fraction(Fraction(cumulative, size))])
    if rows(analysis_dir / "histogram.csv") != expected_histogram:
        raise ValueError("histogram reconstruction mismatch")
    if rows(analysis_dir / "lower_tail_cdf.csv") != expected_cdf:
        raise ValueError("lower-tail CDF reconstruction mismatch")
    if rows(analysis_dir / "record_lows.csv") != expected_record_data:
        raise ValueError("record-low reconstruction mismatch")
    if rows(analysis_dir / "local_minima.csv") != expected_local_data:
        raise ValueError("local-minimum reconstruction mismatch")

    b_values = values_by_interval["PILOT-B"]
    b_low = INTERVALS["PILOT-B"][1]
    if rows(analysis_dir / "pilot_b_local_minima_1k.csv") != expected_block_rows(b_values, b_low, 1000):
        raise ValueError("1k block-minimum reconstruction mismatch")
    if rows(analysis_dir / "pilot_b_local_minima_10k.csv") != expected_block_rows(b_values, b_low, 10000):
        raise ValueError("10k block-minimum reconstruction mismatch")
    levels = obj(analysis_dir / "pilot_b_low_levels.json")["levels"]
    expected_levels = []
    for level in sorted(histograms["PILOT-B"])[:5]:
        ns = [b_low + index for index, value in enumerate(b_values) if value == level]
        expected_levels.append({"T": level, "count": len(ns), "first_25_n": [str(n) for n in ns[:25]]})
    if levels != expected_levels:
        raise ValueError("PILOT-B low-level selection mismatch")

    frequency_report = verify_frequency_files(input_root, analysis_dir)
    artifact_manifest = obj(analysis_dir / "artifact_manifest.json")
    for filename, expected_hash in artifact_manifest.get("outputs_sha256", {}).items():
        path = analysis_dir / filename
        if not path.is_file() or sha(path) != expected_hash:
            raise ValueError(f"analysis artifact hash mismatch: {filename}")
    return {
        "schema": "a303656-independent-tn-low-tail-verifier-report-v1",
        "status": "PASS",
        "classification": "INDEPENDENT RECOMPUTATION OF FINITE PILOT STATISTICS",
        "three_way_input_counts_equal": True,
        "histogram_totals": {interval_id: sum(histogram.values()) for interval_id, histogram in histograms.items()},
        "minimum_and_argmin_verified": True,
        "quantiles_verified": True,
        "record_lows_verified": True,
        "local_minima_verified": True,
        "winner_frequencies_verified": True,
        "winner_frequency_totals": frequency_report,
        "obstruction_data_status": "SCHEMA_ONLY_NOT_COLLECTED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--analysis-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise ValueError(f"refusing to overwrite verifier report: {args.report}")
    report = verify(args.input_root, args.analysis_dir)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("INDEPENDENT_TN_LOW_TAIL_VERIFICATION_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, csv.Error, json.JSONDecodeError) as error:
        print(f"LOW_TAIL_VERIFY_ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
