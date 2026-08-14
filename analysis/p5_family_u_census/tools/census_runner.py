#!/usr/bin/env python3
"""Run the exact frozen Family-U census after the source commit gate."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

from common import (
    EXPECTED_R, MASK_BYTES, PAIR_COUNT, CensusError, atomic_json, canonical_digest,
    deduplicate, demand, exact_summary, load_json, load_pair_frequency_rows,
    mask_hex, parse_mask_hex, rational, reconstruct_panel, sha256_file, write_jsonl,
)
from deduplicator import build as build_incidence

TOOLS_REL = Path("analysis/p5_family_u_census/tools")


def git(root: Path, *args: str) -> str:
    process = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    demand(process.returncode == 0, f"git {' '.join(args)} failed: {process.stderr.decode(errors='replace')}")
    return process.stdout.decode().strip()


def source_gate(root: Path, source_commit: str) -> dict[str, Any]:
    head = git(root, "rev-parse", "HEAD")
    parent = git(root, "rev-parse", "HEAD^")
    demand(head == source_commit, "formal evaluation is not running at declared SOURCE COMMIT S")
    demand(parent == EXPECTED_R, "SOURCE COMMIT S is not a direct child of RESULTS COMMIT R")
    demand(git(root, "status", "--short", "--untracked-files=no") == "", "tracked worktree is not clean at source gate")
    return {"source_commit": source_commit, "head": head, "direct_parent": parent, "tracked_worktree_clean": True}


def run(command: list[str], cwd: Path, record: dict[str, Any], label: str, stdout_path: Path, stderr_path: Path) -> None:
    started = time.monotonic()
    process = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.write_bytes(process.stdout)
    stderr_path.write_bytes(process.stderr)
    record[label] = {
        "command": command, "return_code": process.returncode,
        "stdout": str(stdout_path), "stderr": str(stderr_path),
        "elapsed_seconds": format(time.monotonic() - started, ".6f"),
    }
    demand(process.returncode == 0, f"{label} returned {process.returncode}")


def evaluation_panel(panel: dict[str, Any], incidence: dict[str, Any]) -> dict[str, Any]:
    description_lookup = {d["description_id"]: d for d in panel["descriptions"]}
    points = []
    for ordinal, integer in enumerate(incidence["integers"]):
        points.append({
            # The existing factorization-free oracle's wire format reserves
            # class_index in [0,84).  This bijective mechanical identity map
            # carries no panel semantics and never changes n or its ordering.
            "point_ordinal": ordinal, "mask_index": ordinal, "class_index": ordinal % 84,
            "point_index": ordinal // 84, "n": integer["n"], "description_ids": integer["description_ids"],
            "description_multiplicity": integer["description_multiplicity"],
            "union_mask_hexes": [description_lookup[i]["resulting_union_mask_hex"] for i in integer["description_ids"]],
        })
    demand(len(points) == incidence["distinct_integer_count"] and len({p["n"] for p in points}) == len(points), "duplicate integer evaluation")
    return {
        **panel, "schema": "a303656-p5-family-u-evaluation-panel-v1",
        "point_count": len(points), "points": points,
        "incidence_digest": incidence["canonical_incidence_digest"],
    }


def read_counts(path: Path) -> list[dict[str, int]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    expected = ["point_ordinal", "mask_index", "class_index", "point_index", "n", "T", "mask_sha256"]
    demand(rows and list(rows[0]) == expected, "backend counts header mismatch")
    return [{k: int(row[k]) for k in expected[:-1]} | {"mask_sha256": row["mask_sha256"]} for row in rows]


def read_masks(path: Path, count: int) -> list[bytes]:
    data = path.read_bytes()
    demand(len(data) == count * MASK_BYTES, "truncated or extra mask bytes")
    masks = [data[i * MASK_BYTES:(i + 1) * MASK_BYTES] for i in range(count)]
    demand(all(not (mask[-1] & 0x80) for mask in masks), "mask tail outside pair domain")
    return masks


def load_direct(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def validate_point_outputs(panel: dict[str, Any], counts_a: list[dict[str, int]], counts_b: list[dict[str, int]], masks_a: list[bytes], masks_b: list[bytes], direct: dict[str, Any]) -> list[dict[str, Any]]:
    points = panel["points"]
    demand(len(counts_a) == len(counts_b) == len(masks_a) == len(masks_b) == len(points), "point output cardinality mismatch")
    demand(masks_a == masks_b, "Backend A/B bitwise mask disagreement")
    demand(direct.get("point_count") == len(points) and direct.get("complete_mask_count") == len(points), "direct oracle incomplete")
    direct_points = direct.get("points")
    demand(isinstance(direct_points, list) and len(direct_points) == len(points), "direct oracle point cardinality mismatch")
    rows = []
    for ordinal, (point, a, b, mask, observed) in enumerate(zip(points, counts_a, counts_b, masks_a, direct_points)):
        identity = (ordinal, ordinal, point["class_index"], point["point_index"], point["n"])
        demand(tuple(a[k] for k in ("point_ordinal", "mask_index", "class_index", "point_index", "n")) == identity, "Backend A outside/reordered panel")
        demand(tuple(b[k] for k in ("point_ordinal", "mask_index", "class_index", "point_index", "n")) == identity, "Backend B outside/reordered panel")
        demand(a["T"] == b["T"], "Backend A/B pointwise T disagreement")
        demand(hashlib.sha256(mask).hexdigest() == a["mask_sha256"] == b["mask_sha256"], "backend mask digest mismatch")
        demand(sum(byte.bit_count() for byte in mask) == a["T"], "popcount(mask) != T")
        demand(observed.get("point_ordinal") == ordinal and observed.get("class_index") == point["class_index"] and observed.get("point_index") == point["point_index"] and observed.get("n") == point["n"] and observed.get("T") == a["T"] and observed.get("winner_mask_hex") == mask.hex(), "direct complete mask mismatch")
        winners = observed.get("canonical_least_a_winners")
        demand(isinstance(winners, list) and len(winners) == a["T"], "direct witness cardinality mismatch")
        seen = set()
        for winner in winners:
            index = winner.get("pair_index")
            demand(isinstance(index, int) and 0 <= index < PAIR_COUNT and index not in seen and (mask[index // 8] >> (index % 8)) & 1, "direct winner identity/mask mismatch")
            seen.add(index)
            a_w, b_w, remainder = winner.get("a"), winner.get("b"), winner.get("remainder")
            demand(isinstance(a_w, int) and isinstance(b_w, int) and 0 <= a_w <= b_w and a_w * a_w + b_w * b_w == remainder, "direct-oracle witness corruption")
        mask_int = int.from_bytes(mask, "little")
        for union_hex in point["union_mask_hexes"]:
            demand(mask_int & parse_mask_hex(union_hex) == 0, "persistent-covered winner injection")
        rows.append({
            "point_ordinal": ordinal, "n": point["n"], "T": a["T"], "winner_mask_hex": mask.hex(),
            "description_ids": point["description_ids"], "description_multiplicity": point["description_multiplicity"],
        })
    return rows


def summarize_groups(descriptions: list[dict[str, Any]], t_by_n: dict[int, int], key: Callable[[dict[str, Any]], str]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for description in descriptions:
        groups[key(description)].append(description)
    result = []
    for label in sorted(groups):
        rows = groups[label]
        unique = sorted({row["activation_cell_member"] for row in rows})
        summary = exact_summary([(n, t_by_n[n]) for n in unique])
        result.append({"group": label, "descriptions": len(rows), "distinct_integers": len(unique), **summary})
    return result


def build_summaries(root: Path, panel: dict[str, Any], incidence: dict[str, Any], points: list[dict[str, Any]]) -> dict[str, Any]:
    t_by_n = {row["n"]: row["T"] for row in points}
    desc_by_id = {d["description_id"]: d for d in panel["descriptions"]}
    primary = exact_summary([(row["n"], row["T"]) for row in points])
    primary["label"] = "DISTINCT-INTEGER PRIMARY SUMMARY"
    secondary_items = [(d["activation_cell_member"], t_by_n[d["activation_cell_member"]]) for d in panel["descriptions"]]
    secondary = exact_summary(secondary_items)
    secondary["label"] = "DESCRIPTION-WEIGHTED SECONDARY SUMMARY"
    secondary["multiplicity_weighted"] = True

    all_occupied = [json.loads(line) for line in (root / "analysis/p5_sparse_panel_feasibility/results/occupied_fresh_class_manifest.jsonl").read_text().splitlines() if line]
    all_u_counts = Counter(row["entry_id"] for row in all_occupied if row["family"] == "U")
    shortlist = load_json(root / "analysis/fifth_prime_marginal_coverage/results/frozen_future_shortlist.json")["entries"]
    entry_summaries = []
    for index, entry in enumerate(shortlist, 1):
        entry_id = f"ENTRY-{index:03d}"
        descriptions = [d for d in panel["descriptions"] if d["entry_id"] == entry_id]
        unique = sorted({d["activation_cell_member"] for d in descriptions})
        multiplicity = Counter()
        for n in unique:
            multiplicity[sum(d["activation_cell_member"] == n for d in descriptions)] += 1
        base = {
            "entry_id": entry_id, "total_Family_U_descriptions": all_u_counts[entry_id],
            "fresh_descriptions": len(descriptions), "distinct_integers": len(unique),
            "G5": entry["G5"], "residual_size": entry["residual_size"], "q": entry["q"],
            "union_mask_digest": entry["resulting_union_mask_digest"],
            "integer_multiplicity_distribution": {str(k): multiplicity[k] for k in sorted(multiplicity)},
        }
        if unique:
            stats = exact_summary([(n, t_by_n[n]) for n in unique])
            base.update(stats)
            base["selected_low_tail_counts"] = {k: stats["low_tail_counts"][k] for k in ("T_le_15", "T_le_18", "T_le_20", "T_le_24")}
        else:
            base.update({"status": "NO FRESH OCCUPIED CLASS", "histogram": {}, "minimum": None, "argmins": [], "exact_mean": None, "median": None, "selected_low_tail_counts": {k: 0 for k in ("T_le_15", "T_le_18", "T_le_20", "T_le_24")}})
        entry_summaries.append(base)

    dimensions = {
        "resulting_union_mask": lambda d: d["resulting_union_mask_digest"],
        "fifth_prime_q": lambda d: str(d["q"]),
        "base_mask": lambda d: d["base_mask_digest"],
        "G5": lambda d: str(d["G5"]),
        "residual_size": lambda d: str(d["residual_size"]),
        "shortlist_selection_reason": lambda d: "+".join(d["selection_reason"]),
    }
    grouped = {name: summarize_groups(panel["descriptions"], t_by_n, function) for name, function in dimensions.items()}

    freq_rows = load_pair_frequency_rows(root)
    winner_frequency = [0] * PAIR_COUNT
    prevalence = [{"base_covered": 0, "union_covered": 0, "newly_covered": 0, "remaining_exposed": 0} for _ in range(PAIR_COUNT)]
    structural_descriptions = []
    for d in panel["descriptions"]:
        base_mask = parse_mask_hex(d["base_mask_hex"])
        union = parse_mask_hex(d["resulting_union_mask_hex"])
        winner = parse_mask_hex(next(row["winner_mask_hex"] for row in points if row["n"] == d["activation_cell_member"]))
        for i in range(PAIR_COUNT):
            prevalence[i]["base_covered"] += (base_mask >> i) & 1
            prevalence[i]["union_covered"] += (union >> i) & 1
            prevalence[i]["newly_covered"] += ((union & ~base_mask) >> i) & 1
            prevalence[i]["remaining_exposed"] += 1 - ((union >> i) & 1)
        structural_descriptions.append({
            "description_id": d["description_id"], "n": d["activation_cell_member"],
            "newly_covered_pair_count": len(d["newly_covered_pair_indices"]),
            "newly_covered_pairs_with_P4_annotations": [
                {"pair_index": i, "P4_winner_count": int(freq_rows[i]["winner_count"]), "P4_exposure_count": int(freq_rows[i]["exposure_count"])}
                for i in d["newly_covered_pair_indices"]
            ],
            "remaining_exposed_pair_count": len(d["remaining_exposed_pair_indices"]),
            "remaining_exposed_winner_count": winner.bit_count(),
            "sacrificed_pair_concept": "EMPTY FOR PURE P5 EXTENSION",
        })
    for row in points:
        winner = parse_mask_hex(row["winner_mask_hex"])
        for i in range(PAIR_COUNT):
            winner_frequency[i] += (winner >> i) & 1
    pair_rows = []
    for i, frequency in enumerate(winner_frequency):
        pair_rows.append({
            "pair_index": i, "distinct_integer_winner_count": frequency,
            "description_prevalence": prevalence[i],
            "P4_empirical_winner_count": int(freq_rows[i]["winner_count"]),
            "P4_empirical_exposure_count": int(freq_rows[i]["exposure_count"]),
        })
    highest = sorted(pair_rows, key=lambda row: (-row["distinct_integer_winner_count"], row["pair_index"]))[:20]
    never_rebound = [row for row in pair_rows if row["P4_empirical_winner_count"] == 0 and row["distinct_integer_winner_count"] > 0]
    total_wins = sum(winner_frequency)
    top_share = Fraction(sum(row["distinct_integer_winner_count"] for row in highest[:10]), total_wins) if total_wins else Fraction(0)
    structural = {
        "interpretation": "COMPUTATIONAL OBSERVATION; no causal effect is inferred",
        "descriptions": structural_descriptions, "pair_level": pair_rows,
        "highest_frequency_winner_pairs": highest,
        "NEVER_WIN_pairs_reappearing": never_rebound,
        "top_10_pair_winner_share": rational(top_share),
        "observed_T_concentrated_in_few_remaining_pairs": top_share >= Fraction(1, 2),
        "previously_high_frequency_pairs_still_dominate": [row["pair_index"] for row in highest[:10] if row["P4_empirical_winner_count"] > 0],
    }

    previous_histogram = {}
    with (root / "analysis/p4_maximizer_census/global_histogram.csv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            previous_histogram[row["T"]] = int(row["count"])
    comparisons = {
        "classification": "DESCRIPTIVE ONLY; unbalanced census; no causal or representative-population claim",
        "previous_exact_finite_record_T": 15,
        "current_distinct_integer_minimum": primary["minimum"],
        "strictly_lower_than_previous_record": primary["minimum"] < 15,
        "current_distinct_integer_sample_count": len(points),
        "description_count": 457,
        "multiplicity_distribution": dict(Counter(row["description_multiplicity"] for row in incidence["integers"])),
        "certified_fixed_P4_histogram": previous_histogram,
        "current_histogram": primary["histogram"],
        "allowed_group_comparisons": ["G5/residual_size", "q", "frozen shortlist selection reason"],
    }
    return {"primary": primary, "secondary": secondary, "entries": entry_summaries, "groups": grouped, "structural_rebound": structural, "comparisons": comparisons}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--jobs", type=int, default=max(1, min(32, os.cpu_count() or 1)))
    args = parser.parse_args()
    started = time.monotonic()
    return_codes: dict[str, Any] = {}
    try:
        root, output, archive = args.root.resolve(), args.output.resolve(), args.archive.resolve()
        gate = source_gate(root, args.source_commit)
        panel = reconstruct_panel(root)
        incidence = build_incidence(panel)
        eval_panel = evaluation_panel(panel, incidence)
        output.mkdir(parents=True, exist_ok=False)
        archive.mkdir(parents=True, exist_ok=False)
        atomic_json(output / "panel_reconstruction_manifest.json", eval_panel)
        atomic_json(output / "description_integer_incidence.json", incidence)

        bin_dir = archive / "bin"
        bin_dir.mkdir()
        compile_specs = {
            "compile_backend_a": ("src/k4_ap_backend_a.cpp", "backend_a"),
            "compile_backend_b": ("src/k4_ap_backend_b.cpp", "backend_b"),
            "compile_direct_oracle": ("src/p4_census_direct_oracle.cpp", "direct_oracle"),
        }
        for label, (source, binary) in compile_specs.items():
            run(["g++", "-std=c++17", "-O3", "-DNDEBUG", str(root / source), "-o", str(bin_dir / binary)], root, return_codes, label, archive / f"{label}.stdout.log", archive / f"{label}.stderr.log")

        adapters = {
            "backend_a": [sys.executable, str(root / TOOLS_REL / "backend_a_adapter.py"), "--root", str(root), "--core", str(bin_dir / "backend_a"), "--panel", str(output / "panel_reconstruction_manifest.json"), "--work-dir", str(archive / "backend_a"), "--counts", str(output / "backend_a_counts.csv"), "--masks", str(output / "backend_a_masks.bin"), "--run-report", str(output / "backend_a_run.json")],
            "backend_b": [sys.executable, str(root / TOOLS_REL / "backend_b_adapter.py"), "--root", str(root), "--core", str(bin_dir / "backend_b"), "--panel", str(output / "panel_reconstruction_manifest.json"), "--work-dir", str(archive / "backend_b"), "--counts", str(output / "backend_b_counts.csv"), "--masks", str(output / "backend_b_masks.bin"), "--run-report", str(output / "backend_b_run.json")],
        }
        for label, command in adapters.items():
            run(command, root, return_codes, label, archive / f"{label}.stdout.log", archive / f"{label}.stderr.log")
        direct_command = [sys.executable, str(root / TOOLS_REL / "direct_oracle_adapter.py"), "--root", str(root), "--oracle", str(bin_dir / "direct_oracle"), "--panel", str(output / "panel_reconstruction_manifest.json"), "--counts", str(output / "backend_a_counts.csv"), "--masks", str(output / "backend_a_masks.bin"), "--work-dir", str(archive / "direct_oracle"), "--artifact", str(output / "direct_oracle.json.gz"), "--run-report", str(output / "direct_oracle_run.json"), "--jobs", str(args.jobs)]
        run(direct_command, root, return_codes, "direct_oracle", archive / "direct_oracle.stdout.log", archive / "direct_oracle.stderr.log")

        counts_a = read_counts(output / "backend_a_counts.csv")
        counts_b = read_counts(output / "backend_b_counts.csv")
        masks_a = read_masks(output / "backend_a_masks.bin", len(eval_panel["points"]))
        masks_b = read_masks(output / "backend_b_masks.bin", len(eval_panel["points"]))
        direct = load_direct(output / "direct_oracle.json.gz")
        point_rows = validate_point_outputs(eval_panel, counts_a, counts_b, masks_a, masks_b, direct)
        write_jsonl(output / "per_integer_results.jsonl", point_rows)
        summaries = build_summaries(root, eval_panel, incidence, point_rows)
        atomic_json(output / "primary_distinct_integer_summary.json", summaries["primary"])
        atomic_json(output / "secondary_description_weighted_summary.json", summaries["secondary"])
        atomic_json(output / "all_entry_summaries.json", summaries["entries"])
        atomic_json(output / "group_summaries.json", summaries["groups"])
        atomic_json(output / "structural_rebound_analysis.json", summaries["structural_rebound"])
        atomic_json(output / "predeclared_comparisons.json", summaries["comparisons"])
        atomic_json(output / "return_codes.json", return_codes)
        zero = [row for row in point_rows if row["T"] == 0]
        metadata = {
            "schema": "a303656-p5-family-u-census-metadata-v1", "source_commit": args.source_commit,
            "source_gate": gate, "raw_description_count": 457, "distinct_integer_count": len(point_rows),
            "every_distinct_integer_evaluated_once_per_backend_and_oracle": True,
            "duplicate_shift_28_pairs_separate": True, "adaptive_extension": False,
            "outside_panel_integer_count": 0, "T_zero_points": [row["n"] for row in zero],
            "T_zero_label": "UNVERIFIED COUNTEREXAMPLE CANDIDATE" if zero else None,
            "protected_hashes_after": panel["authority"]["protected_hashes"],
            "external_archive": str(archive), "elapsed_seconds": format(time.monotonic() - started, ".6f"),
        }
        atomic_json(output / "metadata.json", metadata)
        if zero:
            print("UNVERIFIED COUNTEREXAMPLE CANDIDATE", file=sys.stderr)
            return 4
        print(f"P5_FAMILY_U_CENSUS_RUN_PASS descriptions=457 integers={len(point_rows)}")
        return 0
    except (CensusError, OSError, ValueError, csv.Error, json.JSONDecodeError) as exc:
        print(f"census_runner: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
