#!/usr/bin/env python3
"""Run the fixed K4 arithmetic-progression enrichment pilot.

This is an exact, bounded experiment.  The formal panel is hard-coded by the
task contract and is validated before either counting backend is invoked.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


N0 = 240000005594
H_VALUES = (-720, -360, 0, 360, 720)
K_LOW = -128
K_HIGH = 128
EXPECTED_ACTIVE = 407
EXPECTED_P4 = (3, 7, 11, 23)
EXPECTED_M4 = 28227969
EXPECTED_P4_COVERED = 216
EXPECTED_CELL = (183968950234, 246731069451)
FIXED_DIRECT_K = (-128, -96, -64, -32, -1, 0, 1, 32, 64, 96, 128)
RESULTS_COMMIT_SENTINEL = "RESULT_COMMIT_CONTAINING_THIS_FILE"


class PilotFailure(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def powers(base: int, limit: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    exponent = 0
    value = 1
    while value <= limit:
        result.append((exponent, value))
        if value > limit // base:
            break
        value *= base
        exponent += 1
    return result


def active_pairs(n: int) -> list[tuple[int, int, int]]:
    return [
        (c, d, p3 + p5)
        for c, p3 in powers(3, n)
        for d, p5 in powers(5, n)
        if p3 + p5 <= n
    ]


def strict_int(text: str, label: str, *, signed: bool = True) -> int:
    if not text or text.strip() != text:
        raise PilotFailure(f"malformed {label}: {text!r}")
    if text.startswith("+"):
        raise PilotFailure(f"malformed {label}: leading plus")
    digits = text[1:] if text.startswith("-") and signed else text
    if not digits or not digits.isascii() or not digits.isdigit():
        raise PilotFailure(f"malformed {label}: {text!r}")
    if len(digits) > 1 and digits.startswith("0"):
        raise PilotFailure(f"malformed {label}: leading zero")
    value = int(text)
    if not signed and value < 0:
        raise PilotFailure(f"negative {label}")
    return value


def read_greedy_rows(path: Path) -> dict[str, list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["ordering"], []).append(row)
    for rows_for_ordering in grouped.values():
        rows_for_ordering.sort(key=lambda row: strict_int(row["step"], "greedy step", signed=False))
    return grouped


def verify_committed_core(source_root: Path) -> dict[str, Any]:
    p2 = source_root / "analysis/p2_core"
    greedy = read_greedy_rows(p2 / "greedy_core_steps.csv")
    required = ("MARGINAL_COVERAGE_GREEDY", "COVERAGE_PER_MODULUS_BIT_GREEDY")
    if any(name not in greedy for name in required):
        raise PilotFailure("missing required P2 greedy ordering")
    first_four: dict[str, list[int]] = {}
    for name in required:
        if len(greedy[name]) < 4:
            raise PilotFailure(f"ordering {name} has fewer than four rows")
        first_four[name] = [strict_int(row["selected_prime"], "selected prime", signed=False) for row in greedy[name][:4]]
    if tuple(first_four[required[0]]) != tuple(first_four[required[1]]):
        raise PilotFailure("the two greedy orderings have different first four primes")
    p4 = tuple(first_four[required[0]])
    if p4 != EXPECTED_P4:
        raise PilotFailure(f"altered P4: {p4}")
    m4 = math.prod(p * p for p in p4)
    if m4 != EXPECTED_M4:
        raise PilotFailure(f"altered M4: {m4}")
    for name in required:
        row4 = greedy[name][3]
        if strict_int(row4["product_M"], "committed M4", signed=False) != m4:
            raise PilotFailure(f"committed M4 mismatch in {name}")
        if strict_int(row4["cumulative_covered_active_pairs"], "P4 coverage", signed=False) != EXPECTED_P4_COVERED:
            raise PilotFailure(f"committed P4 coverage mismatch in {name}")
        if strict_int(row4["active_pair_count"], "active pair count", signed=False) != EXPECTED_ACTIVE:
            raise PilotFailure(f"committed active-pair mismatch in {name}")
    activation = json.loads((p2 / "activation_cell.json").read_text(encoding="utf-8"))
    cell = activation.get("cell", {})
    observed_cell = (strict_int(str(cell.get("A")), "cell low"), strict_int(str(cell.get("B")), "cell high"))
    if observed_cell != EXPECTED_CELL or strict_int(str(cell.get("active_pair_count")), "cell active count") != EXPECTED_ACTIVE:
        raise PilotFailure("activation-cell artifact mismatch")
    n0_core = json.loads((p2 / "n0_p2_core.json").read_text(encoding="utf-8"))
    if strict_int(str(n0_core.get("n0")), "n0 core anchor", signed=False) != N0:
        raise PilotFailure("altered n0 in committed P2 core")
    bindings = n0_core.get("selected_prime_residue_bindings")
    if not isinstance(bindings, list):
        raise PilotFailure("missing selected-prime residue bindings")
    by_prime = {strict_int(str(item.get("prime")), "binding prime", signed=False): item for item in bindings}
    for p in p4:
        binding = by_prime.get(p)
        if binding is None:
            raise PilotFailure(f"missing residue binding for p={p}")
        if strict_int(str(binding.get("p_squared")), "binding p squared", signed=False) != p * p:
            raise PilotFailure(f"altered p-squared binding for p={p}")
        if strict_int(str(binding.get("t_p")), "binding residue", signed=False) != N0 % (p * p):
            raise PilotFailure(f"target residue binding mismatch for p={p}")
        if binding.get("direct_binding_verified") is not True:
            raise PilotFailure(f"unverified target residue binding for p={p}")
    if n0_core.get("combined_congruence") != "n == n0 (mod M)":
        raise PilotFailure("committed target congruence is not n == n0 (mod M)")
    return {
        "p4": list(p4),
        "m4": m4,
        "target_residue_mod_m4": N0 % m4,
        "four_prime_persistent_covered_active_pairs": EXPECTED_P4_COVERED,
        "active_pair_count": EXPECTED_ACTIVE,
        "activation_cell": list(EXPECTED_CELL),
        "greedy_first_four": first_four,
        "artifact_sha256": {
            str((p2 / name).relative_to(source_root)): sha256_file(p2 / name)
            for name in ("greedy_core_steps.csv", "activation_cell.json", "n0_p2_core.json", "metadata.json", "verification_report.json")
        },
    }


def construct_panel(core: dict[str, Any]) -> list[dict[str, int]]:
    m4 = int(core["m4"])
    panel = [
        {"h": h, "k": k, "n": N0 + h + k * m4, "active_pairs": EXPECTED_ACTIVE}
        for h in H_VALUES
        for k in range(K_LOW, K_HIGH + 1)
    ]
    if len(panel) != 1285 or any(sum(1 for row in panel if row["h"] == h) != 257 for h in H_VALUES):
        raise PilotFailure("fixed panel cardinality failure")
    integers = [row["n"] for row in panel]
    if len(set(integers)) != len(integers):
        raise PilotFailure("duplicated n in fixed panel")
    if not all(EXPECTED_CELL[0] <= n <= EXPECTED_CELL[1] for n in integers):
        raise PilotFailure("point outside activation cell")
    residues = {(N0 + h) % m4 for h in H_VALUES}
    if len(residues) != len(H_VALUES):
        raise PilotFailure("residue classes are not distinct modulo M4")
    if any((N0 + h - N0) % 360 != 0 for h in H_VALUES if h != 0):
        raise PilotFailure("control is not congruent to target modulo 360")
    endpoint_pairs = {n: active_pairs(n) for n in (min(integers), max(integers))}
    if any(len(pairs) != EXPECTED_ACTIVE for pairs in endpoint_pairs.values()):
        raise PilotFailure("incorrect endpoint active-pair count")
    if endpoint_pairs[min(integers)] != endpoint_pairs[max(integers)]:
        raise PilotFailure("active exponent-pair set changes inside panel")
    duplicates = Counter(shift for _, _, shift in endpoint_pairs[min(integers)])
    if {shift: count for shift, count in duplicates.items() if count > 1} != {28: 2}:
        raise PilotFailure("duplicate-shift invariant failed")
    return panel


def write_panel(path: Path, panel: Iterable[dict[str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["h", "k", "n", "active_pairs"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(panel)


def run_backend(
    executable: Path,
    panel_path: Path,
    output_path: Path,
    log_dir: Path,
    label: str,
    diagnostics_path: Path | None = None,
) -> dict[str, Any]:
    command = [str(executable), "--input", str(panel_path), "--output", str(output_path)]
    if diagnostics_path is not None:
        command += ["--diagnostics", str(diagnostics_path)]
    stdout_path = log_dir / f"{label}.stdout.log"
    stderr_path = log_dir / f"{label}.stderr.log"
    time_path = log_dir / f"{label}.time.txt"
    wrapped = command
    time_binary = Path("/usr/bin/time")
    if time_binary.exists():
        wrapped = [str(time_binary), "-v", "-o", str(time_path), *command]
    start = time.monotonic()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        completed = subprocess.run(wrapped, stdout=stdout, stderr=stderr, check=False)
    elapsed = time.monotonic() - start
    record = {
        "label": label,
        "command": command,
        "return_code": completed.returncode,
        "elapsed_seconds": format(elapsed, ".6f"),
        "stdout_log": stdout_path.name,
        "stderr_log": stderr_path.name,
        "time_log": time_path.name if time_path.exists() else None,
    }
    if completed.returncode != 0:
        raise PilotFailure(f"{label} failed with return code {completed.returncode}")
    return record


def read_counts(path: Path, panel: list[dict[str, int]]) -> list[dict[str, int]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["h", "k", "n", "T", "active_pairs"]:
            raise PilotFailure(f"malformed counts header in {path}")
        rows = []
        for row in reader:
            parsed = {
                "h": strict_int(row["h"], "h"),
                "k": strict_int(row["k"], "k"),
                "n": strict_int(row["n"], "n", signed=False),
                "T": strict_int(row["T"], "T", signed=False),
                "active_pairs": strict_int(row["active_pairs"], "active_pairs", signed=False),
            }
            if not 0 <= parsed["T"] <= EXPECTED_ACTIVE:
                raise PilotFailure("T outside exact active domain")
            rows.append(parsed)
    if len(rows) != len(panel):
        raise PilotFailure(f"omitted or extra point in {path}")
    for expected, observed in zip(panel, rows):
        if any(observed[key] != expected[key] for key in ("h", "k", "n", "active_pairs")):
            raise PilotFailure(f"altered panel row in {path}")
    if len({row["n"] for row in rows}) != len(rows):
        raise PilotFailure(f"duplicated n in {path}")
    return rows


def write_counts(path: Path, rows: list[dict[str, int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["h", "k", "n", "T", "active_pairs"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def decimal_fraction(value: Fraction, digits: int = 30) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def exact_number(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": decimal_fraction(value),
    }


def inverse_ecdf(values: list[int], numerator: int, denominator: int = 100) -> int:
    ordered = sorted(values)
    rank = (numerator * len(ordered) + denominator - 1) // denominator
    rank = max(1, rank)
    return ordered[rank - 1]


def summarize(rows: list[dict[str, int]]) -> dict[str, Any]:
    if not rows:
        raise PilotFailure("cannot summarize empty row set")
    values = [row["T"] for row in rows]
    count = len(values)
    minimum = min(values)
    maximum = max(values)
    mean = Fraction(sum(values), count)
    variance = sum((Fraction(value) - mean) ** 2 for value in values) / count
    with localcontext() as ctx:
        ctx.prec = 50
        std = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    ordered = sorted(values)
    median = Fraction(ordered[count // 2]) if count % 2 else Fraction(ordered[count // 2 - 1] + ordered[count // 2], 2)
    thresholds: dict[str, Any] = {}
    for threshold in (16, 18, 20, 25, 30):
        hits = sum(value <= threshold for value in values)
        thresholds[str(threshold)] = {"count": hits, "proportion": exact_number(Fraction(hits, count))}
    quantiles = {str(q): inverse_ecdf(values, q) for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)}
    return {
        "point_count": count,
        "minimum": minimum,
        "argmin": [{"h": row["h"], "k": row["k"], "n": row["n"]} for row in rows if row["T"] == minimum],
        "maximum": maximum,
        "mean": exact_number(mean),
        "population_standard_deviation": format(std, "f"),
        "population_variance": exact_number(variance),
        "median": exact_number(median),
        "inverse_empirical_cdf_quantiles_percent": quantiles,
        "thresholds": thresholds,
        "histogram": {str(value): occurrences for value, occurrences in sorted(Counter(values).items())},
    }


def format_half(value_twice: int) -> str:
    sign = "-" if value_twice < 0 else ""
    absolute = abs(value_twice)
    return f"{sign}{absolute // 2}" if absolute % 2 == 0 else f"{sign}{absolute // 2}.5"


def matched_k(rows: list[dict[str, int]], output_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_hk = {(row["h"], row["k"]): row for row in rows}
    output: list[dict[str, Any]] = []
    for k in range(K_LOW, K_HIGH + 1):
        target = by_hk[(0, k)]["T"]
        controls = [by_hk[(h, k)]["T"] for h in H_VALUES if h != 0]
        ordered_controls = sorted(controls)
        median_twice = ordered_controls[1] + ordered_controls[2]
        difference_twice = 2 * target - median_twice
        smaller = sum(value < target for value in [target, *controls])
        equal_controls = sum(value == target for value in controls)
        greater_controls = sum(value > target for value in controls)
        output.append({
            "k": k,
            "target_T": target,
            "control_h_-720_T": controls[0],
            "control_h_-360_T": controls[1],
            "control_h_360_T": controls[2],
            "control_h_720_T": controls[3],
            "control_median": format_half(median_twice),
            "control_minimum": min(controls),
            "control_maximum": max(controls),
            "target_minus_control_median": format_half(difference_twice),
            "target_rank_among_five": 1 + smaller,
            "target_unique_minimum": int(greater_controls == 4),
            "target_tied_minimum": int(equal_controls > 0 and smaller == 0),
            "target_below_all_four_controls": int(greater_controls == 4),
            "target_below_at_least_three_controls": int(greater_controls >= 3),
            "difference_twice": difference_twice,
        })
    fields = [key for key in output[0] if key != "difference_twice"]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)

    def aggregate(selected: list[dict[str, Any]]) -> dict[str, Any]:
        twice = [int(row["difference_twice"]) for row in selected]
        ordered = sorted(twice)
        median_twice = ordered[len(ordered) // 2] if len(ordered) % 2 else Fraction(ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2], 2)
        mean_difference = Fraction(sum(twice), 2 * len(twice))
        median_difference = Fraction(median_twice) / 2
        longest = 0
        run = 0
        for value in twice:
            run = run + 1 if value < 0 else 0
            longest = max(longest, run)
        return {
            "point_count": len(selected),
            "mean_target_minus_control_median": exact_number(mean_difference),
            "median_target_minus_control_median": exact_number(median_difference),
            "negative_differences": sum(value < 0 for value in twice),
            "zero_differences": sum(value == 0 for value in twice),
            "positive_differences": sum(value > 0 for value in twice),
            "unique_minimum_cases": sum(int(row["target_unique_minimum"]) for row in selected),
            "tied_minimum_cases": sum(int(row["target_tied_minimum"]) for row in selected),
            "below_all_four_controls_cases": sum(int(row["target_below_all_four_controls"]) for row in selected),
            "below_at_least_three_controls_cases": sum(int(row["target_below_at_least_three_controls"]) for row in selected),
            "longest_consecutive_negative_difference_run": longest,
        }

    return output, {
        "including_anchor_k0": aggregate(output),
        "leave_anchor_out": aggregate([row for row in output if row["k"] != 0]),
    }


def persistent_core(rows: list[dict[str, int]], core: dict[str, Any]) -> dict[str, Any]:
    by_hk = {(row["h"], row["k"]): row for row in rows}
    pairs = active_pairs(min(row["n"] for row in rows))
    if len(pairs) != EXPECTED_ACTIVE:
        raise PilotFailure("persistent-core active domain drift")
    result: dict[str, Any] = {
        "schema": "a303656-k4-persistent-core-by-class-v1",
        "classification": "EXACT FINITE COMPUTATION ON FIVE FIXED RESIDUE CLASSES",
        "p4": core["p4"],
        "m4": core["m4"],
        "classes": [],
    }
    for h in H_VALUES:
        base = N0 + h
        coverage: dict[int, set[tuple[int, int]]] = {}
        for p in EXPECTED_P4:
            p2 = p * p
            coverage[p] = {
                (c, d)
                for c, d, shift in pairs
                if (base - shift) % p == 0 and (base - shift) % p2 != 0
            }
            if any((N0 + h + k * EXPECTED_M4) % p2 != base % p2 for k in range(K_LOW, K_HIGH + 1)):
                raise PilotFailure("persistent set is not constant across k")
        union = set().union(*coverage.values())
        multiplicities = Counter(sum(pair in coverage[p] for p in EXPECTED_P4) for pair in union)
        pairwise = {
            f"{p}_{q}": len(coverage[p] & coverage[q])
            for index, p in enumerate(EXPECTED_P4)
            for q in EXPECTED_P4[index + 1 :]
        }
        t0 = by_hk[(h, 0)]["T"]
        result["classes"].append({
            "h": h,
            "base_n": base,
            "residue_mod_m4": base % EXPECTED_M4,
            "residue_mod_p_squared": {str(p): base % (p * p) for p in EXPECTED_P4},
            "persistent_covered_active_pair_count": len(union),
            "persistent_covered_active_pairs": [f"{c}:{d}" for c, d in sorted(union)],
            "current_loser_count_at_k0": EXPECTED_ACTIVE - t0,
            "persistent_covered_current_loser_count_at_k0": len(union),
            "uncovered_active_pair_count": EXPECTED_ACTIVE - len(union),
            "uncovered_active_pairs": [f"{c}:{d}" for c, d, _ in pairs if (c, d) not in union],
            "per_prime_covered_count": {str(p): len(coverage[p]) for p in EXPECTED_P4},
            "pairwise_duplicate_coverage_intersections": pairwise,
            "coverage_multiplicity_histogram": {str(k): v for k, v in sorted(multiplicities.items())},
            "multiply_covered_pairs": [
                {"pair": f"{c}:{d}", "primes": [p for p in EXPECTED_P4 if (c, d) in coverage[p]]}
                for c, d in sorted(union)
                if sum((c, d) in coverage[p] for p in EXPECTED_P4) > 1
            ],
            "guaranteed_pair_set_constant_for_all_257_k": True,
        })
    target = next(item for item in result["classes"] if item["h"] == 0)
    if target["persistent_covered_active_pair_count"] != EXPECTED_P4_COVERED:
        raise PilotFailure("target P4 persistent union does not reproduce committed coverage")
    return result


def direct_panel(rows: list[dict[str, int]]) -> tuple[list[dict[str, int]], dict[str, Any]]:
    selected_reasons: dict[int, set[str]] = {}
    for row in rows:
        if row["h"] == 0 and row["k"] == 0:
            selected_reasons.setdefault(row["n"], set()).add("anchor_n0")
        if row["k"] in FIXED_DIRECT_K:
            selected_reasons.setdefault(row["n"], set()).add("fixed_k")
        if row["T"] <= 25:
            selected_reasons.setdefault(row["n"], set()).add("T_le_25")
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        minimum = min(row["T"] for row in class_rows)
        for row in class_rows:
            if row["T"] == minimum:
                selected_reasons.setdefault(row["n"], set()).add("class_argmin")
    selected = [row for row in rows if row["n"] in selected_reasons]
    if len({row["n"] for row in selected}) != len(selected):
        raise PilotFailure("direct verification panel was not deduplicated")
    selection = {
        "point_count": len(selected),
        "fixed_k_values": list(FIXED_DIRECT_K),
        "points": [
            {"h": row["h"], "k": row["k"], "n": row["n"], "T": row["T"], "reasons": sorted(selected_reasons[row["n"]])}
            for row in selected
        ],
    }
    return selected, selection


def write_direct_panel(path: Path, rows: list[dict[str, int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["h", "k", "n", "active_pairs", "expected_T"],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "h": row["h"],
                    "k": row["k"],
                    "n": row["n"],
                    "active_pairs": row["active_pairs"],
                    "expected_T": row["T"],
                }
            )


def run_direct(executable: Path, panel_path: Path, output_path: Path, log_dir: Path) -> dict[str, Any]:
    command = [str(executable), "--input", str(panel_path), "--output", str(output_path)]
    stdout_path = log_dir / "direct_oracle.stdout.log"
    stderr_path = log_dir / "direct_oracle.stderr.log"
    time_path = log_dir / "direct_oracle.time.txt"
    wrapped = command
    if Path("/usr/bin/time").exists():
        wrapped = ["/usr/bin/time", "-v", "-o", str(time_path), *command]
    start = time.monotonic()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        completed = subprocess.run(wrapped, stdout=stdout, stderr=stderr, check=False)
    elapsed = time.monotonic() - start
    record = {
        "label": "direct_oracle",
        "command": command,
        "return_code": completed.returncode,
        "elapsed_seconds": format(elapsed, ".6f"),
        "stdout_log": stdout_path.name,
        "stderr_log": stderr_path.name,
        "time_log": time_path.name if time_path.exists() else None,
    }
    if completed.returncode != 0:
        raise PilotFailure(f"direct oracle failed with return code {completed.returncode}")
    return record


def verify_direct_json(path: Path, selected: list[dict[str, int]]) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    points = data.get("points")
    if not isinstance(points, list) or len(points) != len(selected):
        raise PilotFailure("direct oracle omitted or added points")
    by_n = {row["n"]: row for row in selected}
    if len(by_n) != len(selected):
        raise PilotFailure("direct selected panel duplicate")
    observed_n: set[int] = set()
    for point in points:
        n = strict_int(str(point.get("n")), "direct n", signed=False)
        if n not in by_n or n in observed_n:
            raise PilotFailure("unexpected or duplicated direct point")
        observed_n.add(n)
        expected = by_n[n]
        if strict_int(str(point.get("h")), "direct h") != expected["h"]:
            raise PilotFailure(f"direct h mismatch at n={n}")
        if strict_int(str(point.get("k")), "direct k") != expected["k"]:
            raise PilotFailure(f"direct k mismatch at n={n}")
        observed_t = strict_int(str(point.get("T")), "direct T", signed=False)
        active = strict_int(str(point.get("active_pair_count")), "direct active count", signed=False)
        if observed_t != expected["T"] or active != EXPECTED_ACTIVE:
            raise PilotFailure(f"direct T/domain mismatch at n={n}")
        winners = point.get("winning_exponent_pairs")
        if not isinstance(winners, list) or len(winners) != observed_t:
            raise PilotFailure(f"direct winner list mismatch at n={n}")
        seen_pairs: set[tuple[int, int]] = set()
        for winner in winners:
            c = strict_int(str(winner.get("c")), "winner c", signed=False)
            d = strict_int(str(winner.get("d")), "winner d", signed=False)
            shift = strict_int(str(winner.get("shift")), "winner shift", signed=False)
            remainder = strict_int(str(winner.get("remainder")), "winner remainder", signed=False)
            a = strict_int(str(winner.get("a")), "winner a", signed=False)
            b = strict_int(str(winner.get("b")), "winner b", signed=False)
            if (c, d) in seen_pairs or a > b:
                raise PilotFailure(f"noncanonical/duplicate direct witness at n={n}")
            seen_pairs.add((c, d))
            if shift != pow(3, c) + pow(5, d) or remainder != n - shift:
                raise PilotFailure(f"direct shift/remainder mismatch at n={n}")
            if a * a + b * b + pow(3, c) + pow(5, d) != n:
                raise PilotFailure(f"invalid direct witness at n={n}")
    data["runner_witness_validation"] = {
        "status": "PASS",
        "point_count": len(points),
        "all_exact_T_values_match": True,
        "all_complete_winner_lists_match_T": True,
        "all_witness_equations_and_a_le_b": True,
    }
    return data


def verify_protected_inputs(source_root: Path) -> dict[str, Any]:
    metadata = json.loads((source_root / "analysis/p2_core/metadata.json").read_text(encoding="utf-8"))
    expected = metadata.get("fixed_input_audit", {}).get("fixed_input_tree_sha256")
    if not isinstance(expected, dict) or not expected:
        raise PilotFailure("missing committed protected-input hash manifest")
    mismatches = []
    for relative, digest in sorted(expected.items()):
        path = source_root / relative
        actual = sha256_file(path) if path.is_file() else None
        if actual != digest:
            mismatches.append({"path": relative, "expected": digest, "actual": actual})
    if mismatches:
        raise PilotFailure(f"protected baseline/pilot hash mismatch: {mismatches[:3]}")
    canonical = "\n".join(f"{expected[path]}  {path}" for path in sorted(expected)) + "\n"
    return {
        "file_count": len(expected),
        "manifest_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "mismatch_count": 0,
        "all_byte_identical": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--backend-a", type=Path, required=True)
    parser.add_argument("--backend-b", type=Path, required=True)
    parser.add_argument("--direct-oracle", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-parent", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    work_dir = args.work_dir.resolve()
    artifact_dir = args.artifact_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    log_dir = work_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    protected_before = verify_protected_inputs(source_root)
    core = verify_committed_core(source_root)
    panel = construct_panel(core)
    panel_path = work_dir / "fixed_panel.csv"
    write_panel(panel_path, panel)

    raw_a = work_dir / "backend_a_counts.csv"
    raw_b = work_dir / "backend_b_counts.csv"
    commands = [
        run_backend(args.backend_a.resolve(), panel_path, raw_a, log_dir, "backend_a"),
        run_backend(args.backend_b.resolve(), panel_path, raw_b, log_dir, "backend_b"),
    ]
    rows_a = read_counts(raw_a, panel)
    rows_b = read_counts(raw_b, panel)
    mismatches = [
        {"backend_a": a, "backend_b": b}
        for a, b in zip(rows_a, rows_b)
        if a != b
    ]
    if mismatches:
        mismatch = mismatches[0]
        discrepancy_panel = work_dir / "discrepancy_panel.csv"
        write_panel(
            discrepancy_panel,
            [{key: mismatch["backend_a"][key] for key in ("h", "k", "n", "active_pairs")}],
        )
        failure = {
            "status": "FAIL",
            "reason": "backend pointwise disagreement",
            "exact_n": mismatch["backend_a"]["n"],
            "backend_a": mismatch["backend_a"],
            "backend_b": mismatch["backend_b"],
        }
        try:
            run_backend(args.backend_a.resolve(), discrepancy_panel, work_dir / "discrepancy_a_counts.csv", log_dir, "discrepancy_a", work_dir / "discrepancy_a_pairs.csv")
            run_backend(args.backend_b.resolve(), discrepancy_panel, work_dir / "discrepancy_b_counts.csv", log_dir, "discrepancy_b", work_dir / "discrepancy_b_pairs.csv")
        finally:
            atomic_json(work_dir / "discrepancy_failure.json", failure)
        raise PilotFailure("backend pointwise disagreement")

    out_a = artifact_dir / "backend_a_counts.csv"
    out_b = artifact_dir / "backend_b_counts.csv"
    write_counts(out_a, rows_a)
    write_counts(out_b, rows_b)
    comparison_path = artifact_dir / "pointwise_comparison.csv"
    with comparison_path.open("w", newline="", encoding="utf-8") as f:
        fields = ["h", "k", "n", "backend_a_T", "backend_b_T", "active_pairs", "pointwise_equal"]
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for a, b in zip(rows_a, rows_b):
            writer.writerow({
                "h": a["h"], "k": a["k"], "n": a["n"],
                "backend_a_T": a["T"], "backend_b_T": b["T"],
                "active_pairs": a["active_pairs"], "pointwise_equal": 1,
            })

    summaries: dict[str, Any] = {
        "schema": "a303656-k4-ap-class-summaries-v1",
        "classification": "EXACT FINITE DESCRIPTIVE COMPUTATION",
        "quantile_definition": "inverse empirical CDF: order statistic at rank ceil(q*N)",
        "classes": {},
    }
    for h in H_VALUES:
        class_rows = [row for row in rows_a if row["h"] == h]
        if h == 0:
            summaries["classes"][str(h)] = {
                "role": "TARGET",
                "including_anchor_k0": summarize(class_rows),
                "leave_anchor_out": summarize([row for row in class_rows if row["k"] != 0]),
            }
        else:
            summaries["classes"][str(h)] = {"role": "CONTROL", "all_points": summarize(class_rows)}
    _, matched_aggregate = matched_k(rows_a, artifact_dir / "matched_k_comparison.csv")
    summaries["matched_k_aggregate"] = matched_aggregate
    atomic_json(artifact_dir / "class_summaries.json", summaries)

    persistent = persistent_core(rows_a, core)
    atomic_json(artifact_dir / "persistent_core_by_class.json", persistent)

    selected, selection = direct_panel(rows_a)
    direct_panel_path = work_dir / "direct_panel.csv"
    write_direct_panel(direct_panel_path, selected)
    direct_raw = work_dir / "direct_verification_raw.json"
    commands.append(run_direct(args.direct_oracle.resolve(), direct_panel_path, direct_raw, log_dir))
    direct = verify_direct_json(direct_raw, selected)
    direct["selection"] = selection
    atomic_json(artifact_dir / "direct_verification.json", direct)

    protected_after = verify_protected_inputs(source_root)
    if protected_before != protected_after:
        raise PilotFailure("protected baseline/pilot inputs changed during run")

    binary_paths = {
        "backend_a": args.backend_a.resolve(),
        "backend_b": args.backend_b.resolve(),
        "direct_oracle": args.direct_oracle.resolve(),
    }
    source_paths = {
        "backend_a": source_root / "src/k4_ap_backend_a.cpp",
        "backend_b": source_root / "src/k4_ap_backend_b.cpp",
        "direct_oracle": source_root / "src/k4_ap_direct_oracle.cpp",
        "runner": source_root / "src/k4_ap_run.py",
        "verifier": source_root / "src/k4_ap_verify.py",
    }
    metadata = {
        "schema": "a303656-k4-ap-pilot-metadata-v1",
        "task": "K4 ARITHMETIC-PROGRESSION ENRICHMENT PILOT",
        "classification": "EXACT FINITE COMPUTATION; GLOBAL PROBLEM UNRESOLVED",
        "source_commit": args.source_commit,
        "source_parent_commit": args.source_parent,
        "results_commit": RESULTS_COMMIT_SENTINEL,
        "results_commit_resolution": "The verifier must bind this sentinel to the commit containing metadata.json.",
        "core": core,
        "panel": {
            "formula": "n(h,k)=240000005594+h+k*28227969",
            "h_values": list(H_VALUES),
            "k_interval": [K_LOW, K_HIGH],
            "points_per_class": 257,
            "point_count": len(panel),
            "unique_integer_count": len({row["n"] for row in panel}),
            "minimum_n": min(row["n"] for row in panel),
            "maximum_n": max(row["n"] for row in panel),
            "all_inside_activation_cell": True,
            "all_active_pair_count": EXPECTED_ACTIVE,
            "five_distinct_residues_mod_m4": True,
            "control_offsets_congruent_zero_mod_360": True,
            "duplicate_shift": {"shift": 28, "source_pairs": [[1, 2], [3, 0]]},
            "panel_csv_sha256": sha256_file(panel_path),
        },
        "backend_identities": {
            label: {
                "implementation_id": implementation_id,
                "algorithm": algorithm,
                "source_path": str(source_paths[label].relative_to(source_root)),
                "source_sha256": sha256_file(source_paths[label]),
                "binary_sha256": sha256_file(binary_paths[label]),
            }
            for label, implementation_id, algorithm in (
                ("backend_a", "k4_ap_backend_a_trial_division_v1", "independent generated prime table + deterministic uint64 trial division + Fermat two-square theorem"),
                ("backend_b", "k4_ap_backend_b_cpp17_mr7_brent_rho_v1", "deterministic uint64 Miller-Rabin + deterministic-seeded Pollard-Rho + independent Fermat classification"),
                ("direct_oracle", "k4_ap_direct_oracle_v1", "factorization-free direct two-square enumeration with canonical witnesses"),
            )
        },
        "tool_source_hashes": {
            str(path.relative_to(source_root)): sha256_file(path)
            for path in source_paths.values()
        },
        "pointwise_comparison": {"point_count": len(rows_a), "all_equal": True, "mismatch_count": 0},
        "direct_verification": {
            "selected_point_count": len(selected),
            "all_exact_T_values_match": True,
            "all_witnesses_valid": True,
            "selection_rule_complete": True,
        },
        "protected_prior_baseline_and_pilot_hashes_before": protected_before,
        "protected_prior_baseline_and_pilot_hashes_after": protected_after,
        "commands": commands,
        "raw_log_archive": {
            "policy": "Logs remain external under ~/code/a303656/archive; only archive name and SHA256 are committed.",
            "archive_name": "PENDING_EXTERNAL_ARCHIVE",
            "sha256": "PENDING_EXTERNAL_ARCHIVE_SHA256",
        },
        "scope_guards": {
            "formal_points_evaluated_by_each_full_backend": len(panel),
            "other_formal_points_evaluated": 0,
            "adaptive_points_added": 0,
            "CRT_system_solved": False,
            "neighboring_residue_classes_scanned": False,
            "complete_activation_cell_scanned": False,
        },
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    artifact_hashes = {}
    for path in sorted(artifact_dir.iterdir()):
        if path.is_file() and path.name not in ("metadata.json", "verification_report.json"):
            artifact_hashes[path.name] = sha256_file(path)
    metadata["artifact_sha256_before_metadata_and_verification_report"] = artifact_hashes
    atomic_json(artifact_dir / "metadata.json", metadata)
    print("K4_AP_PILOT_RUN_COMPLETE")
    print(f"formal_points={len(panel)}")
    print(f"direct_points={len(selected)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PilotFailure as exc:
        print(f"K4_AP_PILOT_RUN_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
