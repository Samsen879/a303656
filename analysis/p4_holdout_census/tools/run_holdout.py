#!/usr/bin/env python3
"""Evaluate only the frozen holdout panel and build exact result artifacts."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from holdout_common import (
    MASK_BYTES, PAIR_COUNT, START_COMMIT, THRESHOLDS, HoldoutError, atomic_json,
    canonical_pairs, demand, exact_summary, fraction_record, load_candidates,
    load_json, sha256_file, verify_protected,
)


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def run_logged(command: list[str], cwd: Path, log_dir: Path, label: str) -> dict[str, Any]:
    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    process = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    stdout = log_dir / f"{label}.stdout.log"
    stderr = log_dir / f"{label}.stderr.log"
    stdout.write_bytes(process.stdout)
    stderr.write_bytes(process.stderr)
    record = {
        "command": command, "cwd": str(cwd), "return_code": process.returncode,
        "wall_seconds": format(time.monotonic() - started, ".6f"),
        "children_user_seconds_delta": format(after.ru_utime - before.ru_utime, ".6f"),
        "children_system_seconds_delta": format(after.ru_stime - before.ru_stime, ".6f"),
        "children_max_rss_kib_after": after.ru_maxrss, "stdout": str(stdout), "stderr": str(stderr),
    }
    demand(process.returncode == 0, f"{label} failed with return code {process.returncode}")
    return record


def build_binaries(root: Path, work: Path, logs: Path) -> tuple[dict[str, Path], dict[str, Any]]:
    bindir = work / "bin"
    bindir.mkdir(parents=True, exist_ok=True)
    sources = {
        "backend_a": root / "src/k4_ap_backend_a.cpp",
        "backend_b": root / "src/k4_ap_backend_b.cpp",
        "direct_oracle": root / "src/p4_census_direct_oracle.cpp",
    }
    commands: dict[str, Any] = {}
    binaries: dict[str, Path] = {}
    for label, source in sources.items():
        binary = bindir / label
        command = ["g++", "-std=c++20", "-O3", "-DNDEBUG", "-Wall", "-Wextra", "-Wpedantic", "-Werror", str(source), "-o", str(binary)]
        commands[f"build_{label}"] = run_logged(command, root, logs, f"build_{label}")
        binaries[label] = binary
    return binaries, commands


def read_backend(counts: Path, masks: Path, points: list[dict]) -> tuple[list[dict], list[bytes]]:
    with counts.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    demand(len(rows) == len(points), "backend count cardinality mismatch")
    data = masks.read_bytes()
    demand(len(data) == len(points) * MASK_BYTES, "backend mask cardinality mismatch")
    parsed: list[dict] = []
    packed: list[bytes] = []
    for ordinal, (row, point) in enumerate(zip(rows, points)):
        mask = data[ordinal * MASK_BYTES:(ordinal + 1) * MASK_BYTES]
        demand((int(row["point_ordinal"]), int(row["mask_index"]), int(row["class_index"]), int(row["point_index"]), int(row["n"])) == (ordinal, point["mask_index"], point["class_index"], point["point_index"], point["n"]), "backend point identity mismatch")
        demand(hashlib.sha256(mask).hexdigest() == row["mask_sha256"], "backend per-mask digest mismatch")
        value = int(row["T"])
        demand(sum(byte.bit_count() for byte in mask) == value, "backend popcount/T mismatch")
        parsed.append({**point, "T": value, "winner_mask_hex": mask.hex()})
        packed.append(mask)
    return parsed, packed


def load_training_weights(root: Path) -> list[dict[str, int]]:
    path = root / "analysis/p4_weighted_transferability/results/exact_weight_table.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    demand(len(rows) == PAIR_COUNT, "training weight table row count mismatch")
    result: list[dict[str, int]] = []
    for index, row in enumerate(rows):
        demand(int(row["pair_index"]) == index, "training weight table pair order mismatch")
        result.append({key: int(value) for key, value in row.items()})
    return result


def rank_records(records: list[dict], value_key: str, descending: bool) -> list[dict]:
    ordered = sorted(records, key=lambda row: ((-row[value_key] if descending else row[value_key]), row["mask_index"]))
    previous = None
    rank = 0
    for position, row in enumerate(ordered, 1):
        value = row[value_key]
        if previous is None or value != previous:
            rank = position
            previous = value
        row["rank"] = rank
    return ordered


def variance(values: list[Fraction]) -> Fraction:
    mean = sum(values, Fraction()) / len(values)
    return sum(((value - mean) ** 2 for value in values), Fraction()) / len(values)


def analyze(root: Path, panel: dict, rows: list[dict], masks: list[bytes]) -> tuple[dict, dict, dict, str]:
    candidates = load_candidates(root)
    pairs = canonical_pairs(root)
    weights = load_training_weights(root)
    by_mask: dict[int, list[tuple[dict, bytes]]] = defaultdict(list)
    by_class: dict[int, list[dict]] = defaultdict(list)
    for row, mask in zip(rows, masks):
        by_mask[row["mask_index"]].append((row, mask))
        by_class[row["class_index"]].append(row)

    summaries: list[dict] = []
    for candidate in candidates:
        group = by_mask[candidate["mask_index"]]
        values = [row["T"] for row, _ in group]
        ns = [row["n"] for row, _ in group]
        class_values = [[row["T"] for row in by_class[spec["class_index"]]] for spec in panel["masks"][candidate["mask_index"]]["classes"]]
        summary = exact_summary(values, ns, class_values, candidate["G"])
        summary.update({"mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "roles": candidate["roles"], "class_count": panel["r"], "coverage_mask_hex": candidate["coverage_mask_hex"]})
        summaries.append(summary)
    aggregate_values = [row["T"] for row in rows]
    aggregate_ns = [row["n"] for row in rows]
    aggregate_classes = [[row["T"] for row in by_class[index]] for index in sorted(by_class)]
    aggregate = exact_summary(aggregate_values, aggregate_ns, aggregate_classes, 0)
    aggregate.pop("survival_ratio_T_over_407_minus_G")
    aggregate.update({"mask_count": 13, "class_count": len(by_class), "point_count": len(rows), "G": "MIXED"})
    summary_artifact = {"schema": "a303656-holdout-summaries-v1", "per_mask": summaries, "aggregate_13_masks": aggregate}

    control = next(candidate for candidate in candidates if "G231-COMMON" in candidate["roles"])
    control_summary = summaries[control["mask_index"]]
    control_mask = control["coverage_mask_int"]
    censoring_items: list[dict] = []
    for candidate, summary in zip(candidates, summaries):
        candidate_mask = candidate["coverage_mask_int"]
        newly = [index for index in range(PAIR_COUNT) if not (control_mask >> index) & 1 and (candidate_mask >> index) & 1]
        sacrificed = [index for index in range(PAIR_COUNT) if (control_mask >> index) & 1 and not (candidate_mask >> index) & 1]
        group = by_mask[candidate["mask_index"]]
        sacrificed_rows: list[dict] = []
        total_rebound = 0
        active_sacrificed = 0
        for index in sacrificed:
            wins = sum(bool(mask[index // 8] & (1 << (index % 8))) for _, mask in group)
            total_rebound += wins
            active_sacrificed += wins > 0
            pair = pairs[index]
            sacrificed_rows.append({**pair, "holdout_win_count": wins})
        newly_rows: list[dict] = []
        estimated = Fraction()
        for index in newly:
            row = weights[index]
            weight = Fraction(row["pool_winner_numerator"], row["pool_denominator"])
            estimated += weight
            newly_rows.append({**pairs[index], "training_weight": fraction_record(weight)})
        candidate_mean = Fraction(summary["point_weighted_mean_T"]["numerator"], summary["point_weighted_mean_T"]["denominator"])
        control_mean = Fraction(control_summary["point_weighted_mean_T"]["numerator"], control_summary["point_weighted_mean_T"]["denominator"])
        candidate_class_mean = Fraction(summary["class_equal_weighted_mean_T"]["numerator"], summary["class_equal_weighted_mean_T"]["denominator"])
        control_class_mean = Fraction(control_summary["class_equal_weighted_mean_T"]["numerator"], control_summary["class_equal_weighted_mean_T"]["denominator"])
        censoring_items.append({
            "mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "roles": candidate["roles"], "G": candidate["G"],
            "newly_covered_pairs": newly_rows, "sacrificed_pairs": sacrificed_rows,
            "newly_covered_pair_count": len(newly), "sacrificed_pair_count": len(sacrificed),
            "sacrificed_pairs_with_at_least_one_win": active_sacrificed, "sacrificed_pair_total_winner_count": total_rebound,
            "newly_covered_estimated_benefit": fraction_record(estimated),
            "sacrificed_pair_realized_rebound_per_point": fraction_record(Fraction(total_rebound, len(group))),
            "realized_net_T_difference_point_weighted_candidate_minus_control": fraction_record(candidate_mean - control_mean),
            "realized_net_T_difference_class_equal_candidate_minus_control": fraction_record(candidate_class_mean - control_class_mean),
        })
    censoring = {"schema": "a303656-holdout-structural-censoring-v1", "control_mask_id": control["mask_id"], "control_definition": "existing G=231 common mask", "noncausal_caveat": "Training weights are pre-holdout estimates and are not interpreted as causal effects.", "candidates": censoring_items}

    diagnostic_rows: list[dict] = []
    for candidate, summary in zip(candidates, summaries):
        scores = {}
        for lane, numerator_key, denominator_key in (("pool", "pool_winner_numerator", "pool_denominator"), ("odd", "odd_winner_numerator", "odd_denominator"), ("even", "even_winner_numerator", "even_denominator")):
            numerator = sum(weights[index][numerator_key] for index in range(PAIR_COUNT) if (candidate["coverage_mask_int"] >> index) & 1)
            denominator = weights[0][denominator_key]
            scores[lane] = Fraction(numerator, denominator)
        holdout_mean = Fraction(summary["class_equal_weighted_mean_T"]["numerator"], summary["class_equal_weighted_mean_T"]["denominator"])
        diagnostic_rows.append({"mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "roles": candidate["roles"], "pool_score": scores["pool"], "odd_score": scores["odd"], "even_score": scores["even"], "holdout_mean": holdout_mean})
    orderings: dict[str, list[dict]] = {}
    for lane in ("pool", "odd", "even"):
        ranked = rank_records([dict(row) for row in diagnostic_rows], f"{lane}_score", True)
        orderings[f"{lane}_score"] = [{"rank": row["rank"], "mask_id": row["mask_id"], "mask_index": row["mask_index"], "roles": row["roles"], "score": fraction_record(row[f"{lane}_score"])} for row in ranked]
    holdout_ranked = rank_records([dict(row) for row in diagnostic_rows], "holdout_mean", False)
    orderings["holdout_class_equal_mean_T"] = [{"rank": row["rank"], "mask_id": row["mask_id"], "mask_index": row["mask_index"], "roles": row["roles"], "mean_T": fraction_record(row["holdout_mean"])} for row in holdout_ranked]

    calibration_roles = ("CAL-216", "CAL-227", "CAL-230", "G231-COMMON")
    opts = [candidate for candidate in candidates if any(role in candidate["roles"] for role in ("POOLED-GLOBAL-WEIGHTED-OPT", "T3EQ2-CONSTRAINED-WEIGHTED-OPT"))]
    comparisons: list[dict] = []
    for optimum in opts:
        opt_mean = diagnostic_rows[optimum["mask_index"]]["holdout_mean"]
        item = {"optimum_mask_id": optimum["mask_id"], "optimum_roles": optimum["roles"], "comparisons": []}
        for role in calibration_roles:
            other = next(candidate for candidate in candidates if role in candidate["roles"])
            other_mean = diagnostic_rows[other["mask_index"]]["holdout_mean"]
            item["comparisons"].append({"against": role, "other_mask_id": other["mask_id"], "optimum_better_lower_class_equal_mean_T": opt_mean < other_mean, "difference_optimum_minus_other": fraction_record(opt_mean - other_mean)})
        item["better_than_all_three_calibrations_and_control"] = all(row["optimum_better_lower_class_equal_mean_T"] for row in item["comparisons"])
        comparisons.append(item)

    tuple_orderings: list[dict] = []
    per_mask_class_means: dict[int, list[Fraction]] = {}
    for candidate in candidates:
        means = []
        for spec in panel["masks"][candidate["mask_index"]]["classes"]:
            group = by_class[spec["class_index"]]
            means.append(Fraction(sum(row["T"] for row in group), len(group)))
        per_mask_class_means[candidate["mask_index"]] = means
    for slot in range(panel["r"]):
        slot_rows = [{"mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "value": per_mask_class_means[candidate["mask_index"]][slot]} for candidate in candidates]
        ranked = rank_records(slot_rows, "value", False)
        tuple_orderings.append({"selected_tuple_slot": slot, "ordering": [{"rank": row["rank"], "mask_id": row["mask_id"], "class_mean_T": fraction_record(row["value"])} for row in ranked]})
    stable = all([row["mask_id"] for row in item["ordering"]] == [row["mask_id"] for row in tuple_orderings[0]["ordering"]] for item in tuple_orderings[1:])
    mask_means = [row["holdout_mean"] for row in diagnostic_rows]
    within_variances = []
    for candidate in candidates:
        values = [Fraction(row["T"]) for row, _ in by_mask[candidate["mask_index"]]]
        within_variances.append({"mask_id": candidate["mask_id"], "variance": fraction_record(variance(values))})

    leave_one_out: list[dict] = []
    control_class_means = per_mask_class_means[control["mask_index"]]
    for optimum in opts:
        gaps = [left - right for left, right in zip(per_mask_class_means[optimum["mask_index"]], control_class_means)]
        full_gap = sum(gaps, Fraction()) / len(gaps)
        omitted = []
        for slot in range(panel["r"]):
            gap = sum((value for index, value in enumerate(gaps) if index != slot), Fraction()) / (len(gaps) - 1)
            omitted.append({"omitted_tuple_slot": slot, "mean_gap_optimum_minus_control": fraction_record(gap), "sign_reversal_from_full_gap": (gap < 0) != (full_gap < 0) if gap != 0 and full_gap != 0 else gap != full_gap})
        leave_one_out.append({"optimum_mask_id": optimum["mask_id"], "full_class_slot_equal_gap": fraction_record(full_gap), "leave_one_tuple_out": omitted, "single_tuple_drives_sign": any(row["sign_reversal_from_full_gap"] for row in omitted)})

    low_tail_checks: list[dict] = []
    for optimum in opts:
        opt_summary = summaries[optimum["mask_index"]]
        low_improved = any(Fraction(opt_summary["threshold_counts"][f"T<={threshold}"], opt_summary["point_count"]) > Fraction(control_summary["threshold_counts"][f"T<={threshold}"], control_summary["point_count"]) for threshold in THRESHOLDS)
        opt_mean = Fraction(opt_summary["point_weighted_mean_T"]["numerator"], opt_summary["point_weighted_mean_T"]["denominator"])
        ctl_mean = Fraction(control_summary["point_weighted_mean_T"]["numerator"], control_summary["point_weighted_mean_T"]["denominator"])
        opt_median = Fraction(opt_summary["median_T"]["numerator"], opt_summary["median_T"]["denominator"])
        ctl_median = Fraction(control_summary["median_T"]["numerator"], control_summary["median_T"]["denominator"])
        low_tail_checks.append({"optimum_mask_id": optimum["mask_id"], "low_tail_rate_improves_at_any_predeclared_threshold": low_improved, "mean_deteriorates": opt_mean > ctl_mean, "median_deteriorates": opt_median > ctl_median, "low_tail_improvement_with_mean_or_median_deterioration": low_improved and (opt_mean > ctl_mean or opt_median > ctl_median)})

    censor_by_id = {item["mask_id"]: item for item in censoring_items}
    reversed_flags = []
    for optimum in opts:
        item = censor_by_id[optimum["mask_id"]]
        rebound = Fraction(item["sacrificed_pair_realized_rebound_per_point"]["numerator"], item["sacrificed_pair_realized_rebound_per_point"]["denominator"])
        benefit = Fraction(item["newly_covered_estimated_benefit"]["numerator"], item["newly_covered_estimated_benefit"]["denominator"])
        net = Fraction(item["realized_net_T_difference_class_equal_candidate_minus_control"]["numerator"], item["realized_net_T_difference_class_equal_candidate_minus_control"]["denominator"])
        reversed_flags.append(rebound >= benefit and net >= 0)
    all_better = all(item["better_than_all_three_calibrations_and_control"] for item in comparisons)
    any_low_only = any(item["low_tail_improvement_with_mean_or_median_deterioration"] for item in low_tail_checks)
    any_material = any(Fraction(summaries[opt["mask_index"]]["class_equal_weighted_mean_T"]["numerator"], summaries[opt["mask_index"]]["class_equal_weighted_mean_T"]["denominator"]) < Fraction(control_summary["class_equal_weighted_mean_T"]["numerator"], control_summary["class_equal_weighted_mean_T"]["denominator"]) for opt in opts)
    if all(reversed_flags):
        interpretation = "STRUCTURAL CENSORING REVERSES THE APPARENT WEIGHTED BENEFIT"
    elif all_better:
        interpretation = "WEIGHTED COVERAGE COMPOSITION TRANSFERS TO FRESH FIXED-P4 CLASSES"
    elif any_low_only:
        interpretation = "WEIGHTED COVERAGE COMPOSITION LOWERS THE FINITE LOW TAIL BUT NOT THE FULL DISTRIBUTION"
    elif not any_material:
        interpretation = "WEIGHTED COVERAGE COMPOSITION SHOWS NO MATERIAL HOLDOUT IMPROVEMENT"
    else:
        interpretation = "MIXED / INCONCLUSIVE FINITE RESULT"
    diagnostics = {
        "schema": "a303656-holdout-transfer-diagnostics-v1", "exact_rank_orderings": orderings,
        "weighted_optima_vs_calibrations_and_control": comparisons,
        "selected_tuple_rankings": tuple_orderings, "candidate_ranking_identical_across_selected_tuples": stable,
        "within_mask_variance": within_variances, "between_mask_variance_of_class_equal_means": fraction_record(variance(mask_means)),
        "single_tuple_driver_test": leave_one_out, "low_tail_vs_distribution_checks": low_tail_checks,
        "deterministic_panel_caveat": "No random-sampling p-value is used; this panel is deterministic and finite.", "interpretation_label": interpretation,
    }
    return summary_artifact, censoring, diagnostics, interpretation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--direct-jobs", type=int, default=max(1, min(32, os.cpu_count() or 1)))
    args = parser.parse_args()
    started = time.monotonic()
    try:
        root = args.root.resolve()
        panel_path = args.panel.resolve()
        panel = load_json(panel_path)
        demand(panel.get("status") == "FROZEN PANEL READY FOR EVALUATION" and panel.get("integer_evaluation_performed") is False, "runner refused non-frozen panel")
        head = git(root, "rev-parse", "HEAD").stdout.decode().strip()
        demand(git(root, "cat-file", "-e", f"{args.source_commit}^{{commit}}").returncode == 0, "source commit unavailable")
        demand(git(root, "merge-base", "--is-ancestor", START_COMMIT, args.source_commit).returncode == 0, "starting commit is not an ancestor of source commit")
        demand(git(root, "merge-base", "--is-ancestor", args.source_commit, head).returncode == 0, "source commit is not an ancestor of HEAD")
        protected = verify_protected(root)
        artifacts = args.artifact_dir.resolve()
        work = args.work_dir.resolve()
        logs = args.log_dir.resolve()
        demand(not artifacts.exists() or not any(artifacts.iterdir()), "artifact directory must be absent or empty")
        artifacts.mkdir(parents=True, exist_ok=True)
        work.mkdir(parents=True, exist_ok=True)
        logs.mkdir(parents=True, exist_ok=True)
        binaries, commands = build_binaries(root, work, logs)
        tools = root / "analysis/p4_holdout_census/tools"
        for backend, wrapper, core in (("A", tools / "backend_a_adapter.py", binaries["backend_a"]), ("B", tools / "backend_b_adapter.py", binaries["backend_b"])):
            command = [sys.executable, str(wrapper), "--root", str(root), "--core", str(core), "--panel", str(panel_path), "--work-dir", str(work / f"backend_{backend.lower()}"), "--counts", str(artifacts / f"backend_{backend.lower()}_counts.csv"), "--masks", str(artifacts / f"backend_{backend.lower()}_masks.bin"), "--run-report", str(work / f"backend_{backend.lower()}_run.json")]
            commands[f"backend_{backend.lower()}"] = run_logged(command, root, logs, f"backend_{backend.lower()}")
        points = panel["points"]
        rows_a, masks_a = read_backend(artifacts / "backend_a_counts.csv", artifacts / "backend_a_masks.bin", points)
        rows_b, masks_b = read_backend(artifacts / "backend_b_counts.csv", artifacts / "backend_b_masks.bin", points)
        demand(rows_a == rows_b and masks_a == masks_b, "backend A/B pointwise or bitwise disagreement")
        candidates = load_candidates(root)
        for row, mask in zip(rows_a, masks_a):
            covered = candidates[row["mask_index"]]["coverage_mask_int"].to_bytes(MASK_BYTES, "little")
            demand(all((winner & persistent) == 0 for winner, persistent in zip(mask, covered)), f"persistent-covered pair won at n={row['n']}")
        direct_command = [sys.executable, str(tools / "direct_oracle_adapter.py"), "--root", str(root), "--oracle", str(binaries["direct_oracle"]), "--panel", str(panel_path), "--counts", str(artifacts / "backend_a_counts.csv"), "--masks", str(artifacts / "backend_a_masks.bin"), "--work-dir", str(work / "direct_oracle"), "--artifact", str(artifacts / "direct_oracle.json.gz"), "--run-report", str(work / "direct_run.json"), "--jobs", str(args.direct_jobs)]
        commands["direct_oracle"] = run_logged(direct_command, root, logs, "direct_oracle")
        with (artifacts / "per_point_results.csv").open("w", newline="", encoding="utf-8") as stream:
            fields = ["point_ordinal", "mask_index", "mask_id", "class_index", "class_id", "point_index", "n", "T", "winner_mask_hex"]
            writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows({key: row[key] for key in fields} for row in rows_a)
        summaries, censoring, diagnostics, interpretation = analyze(root, panel, rows_a, masks_a)
        atomic_json(artifacts / "summaries.json", summaries)
        atomic_json(artifacts / "structural_censoring.json", censoring)
        atomic_json(artifacts / "transfer_diagnostics.json", diagnostics)
        final_panel = dict(panel)
        final_panel["source_commit"] = args.source_commit
        final_panel["integer_evaluation_performed"] = True
        final_panel["evaluated_point_count"] = len(points)
        atomic_json(artifacts / "panel_manifest.json", final_panel)
        run_reports = {name: load_json(path) for name, path in (("backend_a", work / "backend_a_run.json"), ("backend_b", work / "backend_b_run.json"), ("direct_oracle", work / "direct_run.json"))}
        metadata = {
            "schema": "a303656-weighted-fixed-p4-holdout-metadata-v1", "source_commit": args.source_commit, "starting_commit": START_COMMIT,
            "head_at_generation": head, "classification": "EXACT FINITE COMPUTATION; GLOBAL A303656 PROBLEM UNRESOLVED",
            "validation_conclusion": "PENDING INDEPENDENT VERIFIER", "interpretation_label": interpretation,
            "scope_guards": {"candidate_mask_count": 13, "r": panel["r"], "class_count": panel["class_count"], "point_count": panel["point_count"], "adaptive_extensions": 0, "outside_panel_integers_evaluated": 0, "new_primes": 0, "activation_cell_changes": 0},
            "protected_hashes": protected, "commands": commands, "run_reports": run_reports,
            "artifact_sha256": {name: sha256_file(artifacts / name) for name in ("panel_manifest.json", "backend_a_counts.csv", "backend_b_counts.csv", "backend_a_masks.bin", "backend_b_masks.bin", "per_point_results.csv", "direct_oracle.json.gz", "summaries.json", "structural_censoring.json", "transfer_diagnostics.json")},
            "runner_wall_seconds": format(time.monotonic() - started, ".6f"),
        }
        atomic_json(artifacts / "metadata.json", metadata)
        print("HOLDOUT_EVALUATION_COMPLETE")
        print(f"point_count={len(points)}")
        print(f"interpretation_label={interpretation}")
        return 0
    except (HoldoutError, OSError, ValueError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        print(f"run_holdout: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
