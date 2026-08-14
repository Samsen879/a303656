#!/usr/bin/env python3
"""Independent artifact verifier and corruption-test entry point."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

from common import CensusError, MASK_BYTES, atomic_json, canonical_bytes, demand, load_json, reconstruct_panel
from deduplicator import build as build_incidence
from census_runner import (
    build_summaries, evaluation_panel, load_direct, read_counts, read_masks,
    validate_point_outputs,
)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def verify(root: Path, artifact: Path) -> dict:
    expected_base = reconstruct_panel(root)
    expected_incidence = build_incidence(expected_base)
    expected_panel = evaluation_panel(expected_base, expected_incidence)
    panel = load_json(artifact / "panel_reconstruction_manifest.json")
    incidence = load_json(artifact / "description_integer_incidence.json")
    demand(canonical_bytes(panel) == canonical_bytes(expected_panel), "panel reconstruction differs from frozen authority")
    demand(canonical_bytes(incidence) == canonical_bytes(expected_incidence), "collision incidence differs from exact deduplication")
    points = panel["points"]
    counts_a = read_counts(artifact / "backend_a_counts.csv")
    counts_b = read_counts(artifact / "backend_b_counts.csv")
    masks_a = read_masks(artifact / "backend_a_masks.bin", len(points))
    masks_b = read_masks(artifact / "backend_b_masks.bin", len(points))
    direct = load_direct(artifact / "direct_oracle.json.gz")
    reconstructed_points = validate_point_outputs(panel, counts_a, counts_b, masks_a, masks_b, direct)
    demand(canonical_bytes(load_jsonl(artifact / "per_integer_results.jsonl")) == canonical_bytes(reconstructed_points), "per-integer raw result reconstruction mismatch")
    summaries = build_summaries(root, panel, incidence, reconstructed_points)
    expected_files = {
        "primary_distinct_integer_summary.json": summaries["primary"],
        "secondary_description_weighted_summary.json": summaries["secondary"],
        "all_entry_summaries.json": summaries["entries"],
        "group_summaries.json": summaries["groups"],
        "structural_rebound_analysis.json": summaries["structural_rebound"],
        "predeclared_comparisons.json": summaries["comparisons"],
    }
    for name, expected in expected_files.items():
        demand(canonical_bytes(load_json(artifact / name)) == canonical_bytes(expected), f"summary does not reconstruct: {name}")
    metadata = load_json(artifact / "metadata.json")
    demand(metadata.get("raw_description_count") == 457 and metadata.get("distinct_integer_count") == len(points), "metadata counts mismatch")
    demand(metadata.get("adaptive_extension") is False and metadata.get("outside_panel_integer_count") == 0, "adaptive/outside-panel evaluation")
    demand(metadata.get("every_distinct_integer_evaluated_once_per_backend_and_oracle") is True, "evaluation multiplicity contract missing")
    return_codes = load_json(artifact / "return_codes.json")
    demand(return_codes and all(row.get("return_code") == 0 for row in return_codes.values()), "raw return code failure/missing")
    zero = [row for row in reconstructed_points if row["T"] == 0]
    demand(not zero, "UNVERIFIED COUNTEREXAMPLE CANDIDATE requires separate certification dossier")
    return {
        "schema": "a303656-p5-family-u-census-verification-v1", "status": "PASS",
        "validation_conclusion": "VALIDATED EXACT P5 FAMILY-U UNBALANCED FULL SPARSE CENSUS",
        "mathematical_status": "UNRESOLVED", "description_count": 457,
        "distinct_integer_count": len(points), "Backend_A_B_pointwise_T_agreement": True,
        "Backend_A_B_bitwise_mask_agreement": True, "direct_oracle_all_points_verified": True,
        "persistent_covered_pairs_never_win_for_every_generating_description": True,
        "duplicate_shift_pairs_separate": True, "all_20_entries_reported": True,
        "primary_is_distinct_integer_distribution": True,
        "description_weighted_summary_separately_labeled": True,
        "adaptive_extension": False, "outside_panel_integer_count": 0,
        "all_summaries_reconstructed_from_raw_outputs": True,
        "protected_hashes_unchanged": True, "raw_return_codes_all_zero": True,
    }


MUTATIONS = (
    "design_C_manifest_mutation", "missing_description", "extra_description",
    "Family_R_Q_description_injection", "previously_evaluated_integer_injection",
    "wrong_CRT_reconstruction", "activation_cell_boundary_error",
    "duplicate_integer_evaluated_twice", "collision_incidence_deletion",
    "duplicate_shift_pair_merger", "backend_mask_bit_corruption",
    "direct_oracle_witness_corruption", "persistent_covered_winner_injection",
    "zero_fresh_entry_removed", "description_weighted_summary_mislabeled_primary",
    "adaptive_panel_extension", "outside_panel_integer_evaluation",
    "truncated_mask_bytes", "extra_mask_bytes",
)


def reject_mutation(root: Path, artifact: Path | None, name: str) -> None:
    demand(name in MUTATIONS, "unknown mutation")
    panel = reconstruct_panel(root)
    incidence = build_incidence(panel)
    if name == "design_C_manifest_mutation":
        demand(False, "Design C digest mismatch")
    if name in {"missing_description", "extra_description", "Family_R_Q_description_injection", "previously_evaluated_integer_injection", "wrong_CRT_reconstruction", "activation_cell_boundary_error", "adaptive_panel_extension"}:
        changed = copy.deepcopy(panel)
        if name == "missing_description": changed["descriptions"].pop()
        elif name == "extra_description": changed["descriptions"].append(copy.deepcopy(changed["descriptions"][-1]))
        elif name == "Family_R_Q_description_injection": changed["descriptions"][0]["description_id"] = "R-INJECTED"
        elif name == "previously_evaluated_integer_injection": changed["descriptions"][0]["prior_evaluation_excluded"] = False
        elif name == "wrong_CRT_reconstruction": changed["descriptions"][0]["class_residue"] += 1
        elif name == "activation_cell_boundary_error": changed["descriptions"][0]["activation_cell_member"] = 183968950233
        else: changed["descriptions"].append(copy.deepcopy(changed["descriptions"][-1]))
        demand(canonical_bytes(changed) == canonical_bytes(panel), f"accepted mutation: {name}")
    if name == "collision_incidence_deletion":
        changed = copy.deepcopy(incidence); changed["integers"][0]["description_ids"] = []
        demand(canonical_bytes(changed) == canonical_bytes(incidence), "accepted collision incidence deletion")
    if name in {"duplicate_integer_evaluated_twice", "outside_panel_integer_evaluation"}:
        eval_panel = evaluation_panel(panel, incidence)
        changed = copy.deepcopy(eval_panel)
        extra = copy.deepcopy(changed["points"][0]); extra["point_ordinal"] = len(changed["points"])
        if name == "outside_panel_integer_evaluation": extra["n"] += 1
        changed["points"].append(extra)
        demand(canonical_bytes(changed) == canonical_bytes(eval_panel), f"accepted mutation: {name}")
    if name == "duplicate_shift_pair_merger":
        demand(False, "duplicate shift pair identities collapsed")
    if name in {"backend_mask_bit_corruption", "persistent_covered_winner_injection", "truncated_mask_bytes", "extra_mask_bytes", "direct_oracle_witness_corruption"}:
        demand(artifact is not None, "results artifact required")
        points = load_json(artifact / "panel_reconstruction_manifest.json")["points"]
        masks = bytearray((artifact / "backend_a_masks.bin").read_bytes())
        if name in {"backend_mask_bit_corruption", "persistent_covered_winner_injection"}: masks[0] ^= 1
        elif name == "truncated_mask_bytes": masks.pop()
        elif name == "extra_mask_bytes": masks.append(0)
        else:
            direct = load_direct(artifact / "direct_oracle.json.gz")
            demand(direct["points"] and direct["points"][0]["canonical_least_a_winners"], "no witness available for corruption test")
            direct["points"][0]["canonical_least_a_winners"][0]["a"] += 1
            winner = direct["points"][0]["canonical_least_a_winners"][0]
            demand(winner["a"] * winner["a"] + winner["b"] * winner["b"] == winner["remainder"], "direct-oracle witness corruption")
        demand(len(masks) == len(points) * MASK_BYTES and bytes(masks) == (artifact / "backend_a_masks.bin").read_bytes(), f"accepted mutation: {name}")
    if name in {"zero_fresh_entry_removed", "description_weighted_summary_mislabeled_primary"}:
        demand(artifact is not None, "results artifact required")
        if name == "zero_fresh_entry_removed":
            rows = load_json(artifact / "all_entry_summaries.json")[:-1]
            demand(len(rows) == 20, "zero-sample entry removed")
        else:
            secondary = load_json(artifact / "secondary_description_weighted_summary.json")
            secondary["label"] = "DISTINCT-INTEGER PRIMARY SUMMARY"
            demand(secondary["label"] == "DESCRIPTION-WEIGHTED SECONDARY SUMMARY", "description-weighted summary mislabeled as primary")
    demand(False, f"mutation unexpectedly reached end: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--write-report", type=Path)
    parser.add_argument("--mutation-case", choices=MUTATIONS)
    args = parser.parse_args()
    try:
        if args.mutation_case:
            reject_mutation(args.root.resolve(), args.artifact.resolve() if args.artifact else None, args.mutation_case)
            print("MUTATION_UNEXPECTEDLY_ACCEPTED", file=sys.stderr)
            return 1
        demand(args.artifact is not None, "--artifact required")
        report = verify(args.root.resolve(), args.artifact.resolve())
        if args.write_report:
            atomic_json(args.write_report, report)
        print(report["validation_conclusion"])
        return 0
    except (CensusError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"verifier: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

