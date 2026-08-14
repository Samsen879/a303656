#!/usr/bin/env python3
"""Fail-closed verifier for the corrected frozen manifest, panel, and results."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from holdout_common import (
    MASK_BYTES, PAIR_COUNT, START_COMMIT, V2_REL, HoldoutError, atomic_json,
    canonical_pairs, construct_panel, demand, load_candidates, load_json,
    sha256_file, verify_protected,
)
from run_holdout import analyze, read_backend


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def normalize_panel(panel: dict) -> dict:
    value = json.loads(json.dumps(panel))
    value["source_commit"] = "SOURCE_COMMIT_M"
    value["integer_evaluation_performed"] = False
    value.pop("evaluated_point_count", None)
    return value


def verify_source_commit(root: Path, source_commit: str) -> dict:
    head = git(root, "rev-parse", "HEAD").stdout.decode().strip()
    demand(git(root, "cat-file", "-e", f"{source_commit}^{{commit}}").returncode == 0, "source commit unavailable")
    demand(git(root, "merge-base", "--is-ancestor", START_COMMIT, source_commit).returncode == 0, "starting commit is not ancestor of source commit")
    demand(git(root, "merge-base", "--is-ancestor", source_commit, head).returncode == 0, "source commit is not ancestor of HEAD")
    frozen = git(root, "show", f"{source_commit}:{V2_REL}")
    demand(frozen.returncode == 0, "v2 manifest absent from source commit")
    demand(hashlib.sha256(frozen.stdout).hexdigest() == sha256_file(root / V2_REL), "working v2 manifest differs from source-commit frozen authority")
    return {"starting_commit": START_COMMIT, "source_commit": source_commit, "head": head, "v2_manifest_frozen_in_source_commit": True}


def verify_pre(root: Path, panel_path: Path) -> dict:
    verify_protected(root)
    candidates = load_candidates(root)
    observed = load_json(panel_path)
    expected = construct_panel(root)
    demand(observed == expected, "panel differs from deterministic exhaustive reconstruction")
    demand(observed.get("r", 0) >= 3, "INSUFFICIENT FRESH CLASS MULTIPLICITY")
    demand(observed.get("candidate_inventory") and len(observed["candidate_inventory"]) == 13, "panel candidate inventory is not 13 masks")
    demand(observed.get("class_count") == 13 * observed["r"], "panel class count is not equal per mask")
    demand(observed.get("integer_evaluation_performed") is False, "pre-evaluation panel already claims integer evaluation")
    return {
        "schema": "a303656-holdout-pre-evaluation-verification-v1", "status": "PASS",
        "candidate_mask_count": len(candidates), "r": observed["r"], "class_count": observed["class_count"], "point_count": observed["point_count"],
        "original_12_preserved": True, "unique_added_mask_is_t3eq2_weighted_optimum": True,
        "complete_tuple_enumeration_reconstructed": True, "existing_class_exclusion_reconstructed": True,
        "deterministic_evenly_spaced_selection_reconstructed": True, "panel_disjoint_from_all_prior_T_panels": True,
        "all_activation_cell_members_of_selected_classes_present": True, "integer_evaluation_performed": False,
    }


def verify_direct(path: Path, rows: list[dict], masks: list[bytes], pairs: list[dict]) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        artifact = json.load(stream)
    points = artifact.get("points")
    demand(artifact.get("schema") == "a303656-holdout-all-point-direct-oracle-v1" and isinstance(points, list) and len(points) == len(rows), "all-point direct artifact schema/cardinality mismatch")
    pair_lookup = {pair["pair_index"]: pair for pair in pairs}
    witnesses = 0
    for ordinal, (row, mask, point) in enumerate(zip(rows, masks, points)):
        demand((point.get("point_ordinal"), point.get("mask_index"), point.get("class_index"), point.get("point_index"), point.get("n"), point.get("T"), point.get("winner_mask_hex")) == (ordinal, row["mask_index"], row["class_index"], row["point_index"], row["n"], row["T"], mask.hex()), f"direct point/mask mismatch at ordinal {ordinal}")
        winners = point.get("canonical_least_a_winners")
        demand(isinstance(winners, list) and len(winners) == row["T"], "direct winner cardinality mismatch")
        reconstructed = bytearray(MASK_BYTES)
        seen: set[int] = set()
        for winner in winners:
            index = winner.get("pair_index")
            pair = pair_lookup.get(index)
            demand(pair is not None and index not in seen, "direct winner pair invalid/duplicate")
            seen.add(index)
            remainder = row["n"] - pair["shift"]
            a, b = winner.get("a"), winner.get("b")
            demand((winner.get("c"), winner.get("d"), winner.get("shift"), winner.get("remainder")) == (pair["c"], pair["d"], pair["shift"], remainder), "direct winner identity mismatch")
            demand(isinstance(a, int) and isinstance(b, int) and 0 <= a <= b and a * a + b * b == remainder, "direct witness equation/canonical ordering mismatch")
            reconstructed[index // 8] |= 1 << (index % 8)
            witnesses += 1
        demand(bytes(reconstructed) == mask, "direct winners do not reconstruct complete mask")
    demand(artifact.get("point_count") == len(rows) and artifact.get("complete_mask_count") == len(rows) and artifact.get("canonical_witness_count") == witnesses, "direct artifact totals mismatch")
    if artifact.get("T_zero_points"):
        demand(artifact.get("T_zero_label") == "UNVERIFIED COUNTEREXAMPLE CANDIDATE", "T=0 point lacks permitted label")
    else:
        demand(artifact.get("T_zero_label") is None, "spurious T=0 label")
    return {"point_count": len(rows), "complete_mask_count": len(rows), "canonical_witness_count": witnesses, "T_zero_point_count": len(artifact.get("T_zero_points", []))}


def verify_final(root: Path, artifact_dir: Path, corruption_path: Path) -> dict:
    metadata = load_json(artifact_dir / "metadata.json")
    source_commit = metadata.get("source_commit")
    demand(isinstance(source_commit, str), "metadata source commit missing")
    provenance = verify_source_commit(root, source_commit)
    protected = verify_protected(root)
    panel = load_json(artifact_dir / "panel_manifest.json")
    expected_panel = construct_panel(root)
    demand(normalize_panel(panel) == expected_panel, "committed result panel differs from deterministic fresh reconstruction")
    demand(panel.get("integer_evaluation_performed") is True and panel.get("evaluated_point_count") == panel.get("point_count"), "result panel evaluation declaration mismatch")
    points = panel["points"]
    rows_a, masks_a = read_backend(artifact_dir / "backend_a_counts.csv", artifact_dir / "backend_a_masks.bin", points)
    rows_b, masks_b = read_backend(artifact_dir / "backend_b_counts.csv", artifact_dir / "backend_b_masks.bin", points)
    demand(rows_a == rows_b and masks_a == masks_b, "backend pointwise/bitwise agreement failure")
    candidates = load_candidates(root)
    persistent_winners = 0
    for row, mask in zip(rows_a, masks_a):
        covered = candidates[row["mask_index"]]["coverage_mask_int"].to_bytes(MASK_BYTES, "little")
        persistent_winners += sum((winner & persistent).bit_count() for winner, persistent in zip(mask, covered))
        demand(sum(byte.bit_count() for byte in mask) == row["T"], "popcount(mask) != T")
    demand(persistent_winners == 0, "persistent-covered winner count is nonzero")
    pairs = canonical_pairs(root)
    demand([(pair["c"], pair["d"]) for pair in pairs if pair["shift"] == 28] == [(1, 2), (3, 0)], "duplicate shift pair identities collapsed")
    direct = verify_direct(artifact_dir / "direct_oracle.json.gz", rows_a, masks_a, pairs)

    with (artifact_dir / "per_point_results.csv").open(newline="", encoding="utf-8") as stream:
        per_point = list(csv.DictReader(stream))
    demand(len(per_point) == len(rows_a), "per-point result cardinality mismatch")
    for raw, row in zip(per_point, rows_a):
        demand((int(raw["point_ordinal"]), int(raw["mask_index"]), raw["mask_id"], int(raw["class_index"]), raw["class_id"], int(raw["point_index"]), int(raw["n"]), int(raw["T"]), raw["winner_mask_hex"]) == (row["point_ordinal"], row["mask_index"], row["mask_id"], row["class_index"], row["class_id"], row["point_index"], row["n"], row["T"], row["winner_mask_hex"]), "per-point result differs from backend reconstruction")
    summaries, censoring, diagnostics, interpretation = analyze(root, panel, rows_a, masks_a)
    demand(load_json(artifact_dir / "summaries.json") == summaries, "exact summaries fail reconstruction")
    demand(load_json(artifact_dir / "structural_censoring.json") == censoring, "structural-censoring analysis fails reconstruction")
    demand(load_json(artifact_dir / "transfer_diagnostics.json") == diagnostics, "transfer diagnostics fail reconstruction")
    demand(len(summaries["per_mask"]) == 13, "not all 13 masks were reported")
    corruption = load_json(corruption_path)
    tests = corruption.get("tests")
    demand(corruption.get("all_rejected") is True and isinstance(tests, list) and len(tests) >= 12 and all(item.get("rejected") is True and item.get("return_code") != 0 for item in tests), "negative mutation report incomplete or contains an accepted corruption")
    commands = metadata.get("commands")
    demand(isinstance(commands, dict) and commands and all(record.get("return_code") == 0 for record in commands.values()), "raw command return codes missing or nonzero")
    for name, expected in metadata.get("artifact_sha256", {}).items():
        demand(sha256_file(artifact_dir / name) == expected, f"artifact hash mismatch: {name}")
    return {
        "schema": "a303656-weighted-fixed-p4-holdout-verification-report-v1", "status": "PASS",
        "validation_conclusion": "VALIDATED WEIGHTED FIXED-P4 OUT-OF-MASK HOLDOUT CENSUS",
        "interpretation_label": interpretation, "mathematical_status": "UNRESOLVED",
        "git_provenance": provenance, "candidate_mask_count": 13, "original_12_preserved": True,
        "unique_added_mask_is_certified_t3eq2_weighted_optimum": True, "r": panel["r"],
        "equal_fresh_class_count_per_mask": True, "class_count": panel["class_count"], "point_count": panel["point_count"],
        "prior_class_and_integer_overlap_count": 0, "adaptive_extension_count": 0, "outside_panel_integer_count": 0,
        "backend_pointwise_T_equal": True, "backend_pointwise_masks_equal": True,
        "direct_oracle": direct, "popcount_equals_T_all_points": True,
        "persistent_covered_winner_count": persistent_winners, "duplicate_shift_28_pair_identities_retained": [[1, 2], [3, 0]],
        "all_13_masks_reported": True, "exact_summaries_reconstructed": True,
        "structural_censoring_reconstructed": True, "negative_mutation_count": len(tests),
        "protected_hashes_unchanged": protected, "raw_return_codes_preserved": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pre", "final"), required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--panel", type=Path)
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument("--corruption-report", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.phase == "pre":
            demand(args.panel is not None, "pre phase requires --panel")
            result = verify_pre(root, args.panel.resolve())
        else:
            demand(args.artifact_dir is not None and args.corruption_report is not None, "final phase requires artifact and corruption report")
            result = verify_final(root, args.artifact_dir.resolve(), args.corruption_report.resolve())
        atomic_json(args.output, result)
        print(result.get("validation_conclusion", "PRE_EVALUATION_VERIFIED"))
        return 0
    except (HoldoutError, OSError, ValueError, UnicodeError, csv.Error, json.JSONDecodeError, gzip.BadGzipFile) as exc:
        print(f"holdout_verifier: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
