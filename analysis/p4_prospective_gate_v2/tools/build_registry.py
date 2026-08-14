#!/usr/bin/env python3
"""Build the versioned historical-exposure registry without running evaluators."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path

from common import LEVELS, canonical_bytes, digest, normalize_intervals, sha256_file, write_json


def git_commit(root: Path, path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    p = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel], cwd=root, text=True, capture_output=True)
    return p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else "NOT_ESTABLISHED"


def component(root: Path, component_id: str, path_text: str, status: str, levels: list[str],
              extent: dict, exact_t: bool | str, downstream: bool | str, note: str) -> dict:
    path = root / path_text
    return {
        "component_id": component_id,
        "source_path": path_text,
        "source_commit": git_commit(root, path) if path.exists() else "NOT_ESTABLISHED",
        "sha256": sha256_file(path) if path.is_file() else "NOT_ESTABLISHED",
        "status": status,
        "exposure_levels": levels,
        "extent": extent,
        "endpoint_convention": "inclusive" if "interval" in extent or "intervals" in extent else "not_applicable",
        "exact_T_computed": exact_t,
        "outcome_used_in_downstream_selection": downstream,
        "note": note,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    root, out = args.root.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)

    prior_path = root / "analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json"
    prior = json.loads(prior_path.read_text())
    intervals = normalize_intervals([list(x) for x in prior["interval_union"]])
    sparse_levels: dict[int, set[str]] = defaultdict(set)
    sparse_sources: dict[int, set[str]] = defaultdict(set)
    for n in prior["sparse_points"]:
        sparse_levels[int(n)].add("E1_BINARY_REPRESENTABILITY_CHECK")
        sparse_sources[int(n)].add("LEGACY_COMPLETE_PRIOR_REGISTRY_V1")

    def add_csv_points(path_text: str, levels: tuple[str, ...], source: str) -> None:
        with (root / path_text).open() as handle:
            for row in csv.DictReader(handle):
                n = int(row["n"])
                sparse_levels[n].update(levels)
                sparse_sources[n].add(source)

    def add_json_points(path_text: str, levels: tuple[str, ...], source: str) -> None:
        data = json.loads((root / path_text).read_text())
        for row in data["points"]:
            n = int(row["n"])
            sparse_levels[n].update(levels)
            sparse_sources[n].add(source)

    add_csv_points("analysis/k4_ap_pilot/backend_a_counts.csv", ("E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK"), "K4_PROGRESSION_PANEL")
    add_csv_points("analysis/p4_maximizer_census/backend_a_counts.csv", ("E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK"), "P4_CALIBRATION_AND_G231")
    add_json_points("analysis/k4_ap_pilot/direct_verification.json", ("E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED",), "K4_DIRECT_VERIFICATION")
    add_json_points("analysis/p4_maximizer_census/direct_verification.json", ("E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED",), "P4_DIRECT_VERIFICATION")

    # Family U is after the v1 registry. Its checked-in census certifies exact count,
    # complete winner mask, and direct-oracle verification for the same 454 integers.
    u_path = root / "analysis/p5_family_u_census/results/panel_reconstruction_manifest.json"
    u = json.loads(u_path.read_text())
    for point in u["points"]:
        n = int(point["n"])
        sparse_levels[n].update(("E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK", "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"))
        sparse_sources[n].add("P5_FAMILY_U_CENSUS")

    components = [
        component(root, "FORMAL_CONTINUOUS_1P6B", "output/formal_results_audit.json", "COMPLETE",
                  ["E1_BINARY_REPRESENTABILITY_CHECK"], {"interval": [240000000001, 241600000000], "integer_count": 1600000000},
                  False, False, "Continuous direct representability interval; length exceeds L4."),
        component(root, "FORMAL_OTHER_DUAL_INTERVALS", "output/formal_results_audit.json", "COMPLETE",
                  ["E1_BINARY_REPRESENTABILITY_CHECK"], {"interval_union_count": len(intervals)-1, "normalized_intervals": intervals},
                  False, False, "Remaining formal dual-implementation intervals imported through the legacy registry."),
        component(root, "LEGACY_COMPLETE_PRIOR_REGISTRY_V1", prior_path.relative_to(root).as_posix(), "COMPLETE",
                  ["E1_BINARY_REPRESENTABILITY_CHECK", "E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK", "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"],
                  {"interval_union_count": len(intervals), "sparse_integer_count": len(prior["sparse_points"])},
                  "MIXED_BY_SUBCOMPONENT", "MIXED_BY_SUBCOMPONENT", "Provenance snapshot for pilots, dossier, K4, and fixed-P4 census."),
        component(root, "P4_CALIBRATION_AND_G231", "analysis/p4_maximizer_census/verification_report.json", "COMPLETE",
                  ["E0_DESIGN_ONLY", "E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK", "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"],
                  {"integer_source": "analysis/p4_maximizer_census/class_panel.csv"}, True, True,
                  "Calibration panels and G=231 census; integers already represented by legacy registry points."),
        component(root, "P4_WEIGHTED_FIXED_RUNS", "analysis/p4_weighted_transferability/results/metadata.json", "COMPLETE",
                  ["E0_DESIGN_ONLY", "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"], {"new_integer_count": 0}, False, True,
                  "Weighted work reused the census and its oracle-selection subset."),
        component(root, "FIFTH_PRIME_MARGINAL", "analysis/fifth_prime_marginal_coverage/results/metadata.json", "COMPLETE",
                  ["E0_DESIGN_ONLY"], {"new_integer_count": 0}, False, True, "Modular-only work; no integer evaluation."),
        component(root, "P5_FAMILY_U_CENSUS", u_path.relative_to(root).as_posix(), "COMPLETE",
                  ["E0_DESIGN_ONLY", "E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK", "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"],
                  {"distinct_integer_count": len({int(x["n"]) for x in u["points"]}), "description_count": u["description_count"]},
                  True, True, "Post-v1 census; collisions preserve one integer with multiple descriptions."),
        component(root, "P5_FAMILY_R", "analysis/p5_sparse_panel_feasibility/results/design_A_all_entry_balanced.json", "COMPLETE",
                  ["E0_DESIGN_ONLY"], {"new_integer_count": 0}, False, False, "Family R descriptions were design-only in this authority chain."),
        component(root, "P5_FAMILY_Q", "analysis/p5_sparse_panel_feasibility/results/design_B_anchor_balanced.json", "COMPLETE",
                  ["E0_DESIGN_ONLY"], {"new_integer_count": 0}, False, False, "Family Q descriptions were design-only in this authority chain."),
        component(root, "SPARSE_FEASIBILITY_RUNS", "analysis/p5_sparse_panel_feasibility/results/verification_report.json", "COMPLETE",
                  ["E0_DESIGN_ONLY"], {"new_integer_count": 0}, False, False, "Sparse feasibility did not execute candidate integers."),
        component(root, "LOW_T_RECORDS", "output/tn_pilot_20260713/pilot_a/bitset/counts.csv", "COMPLETE",
                  ["E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK"], {"covered_by": "LEGACY_COMPLETE_PRIOR_REGISTRY_V1"}, True, True,
                  "PILOT-A/B are imported through the legacy registry; labels are never read by candidate selection."),
        component(root, "INTERRUPTED_PARTIAL_ABANDONED", "logs/INTERRUPTED_RUNS.txt", "PARTIAL",
                  ["E1_BINARY_REPRESENTABILITY_CHECK"], {"integer_count": "NOT_ESTABLISHED"}, "NOT_ESTABLISHED", "NOT_ESTABLISHED",
                  "Some processes ended before complete chunk JSON/return-code pairs; actual touched integers are not reconstructable."),
        component(root, "REPLAY_AND_COLLISION_RECORDS", "analysis/p5_family_u_census/results/description_integer_incidence.json", "COMPLETE",
                  ["E0_DESIGN_ONLY"], {"new_integer_count": 0, "reused_integer_count": 3}, False, False,
                  "Replays and description collisions reuse registered integers; they are not new exposure."),
    ]
    unresolved = [c["component_id"] for c in components if c["status"] != "COMPLETE"]

    rows = [{
        "n": n,
        "exposure_levels": sorted(sparse_levels[n], key=LEVELS.index),
        "component_ids": sorted(sparse_sources[n]),
    } for n in sorted(sparse_levels)]
    registry = {
        "schema": "a303656-historical-exposure-registry-v2",
        "version": 2,
        "status": "PARTIAL" if unresolved else "COMPLETE",
        "completeness_for_any_recorded_evaluation": "NOT_ESTABLISHED" if unresolved else "COMPLETE",
        "completeness_for_exact_T": "NOT_ESTABLISHED" if unresolved else "COMPLETE",
        "levels": list(LEVELS),
        "inclusive_interval_exposures": ([{"low": a, "high": b, "levels": ["E1_BINARY_REPRESENTABILITY_CHECK"]} for a, b in intervals]
            + [{"low": 2, "high": 200001, "levels": ["E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK"]},
               {"low": 240000000001, "high": 240000100000, "levels": ["E2_EXACT_T_COUNT", "E3_COMPLETE_WINNER_MASK"]}]),
        "sparse_integer_exposures": rows,
        "historically_exposed_fixed_P4_classes": {
            "value": True,
            "all_classes_modulus": 1129118760,
            "proof_interval": [240000000001, 241600000000],
            "proof_interval_length": 1600000000,
            "reason": "inclusive interval length is at least the modulus, hence every residue class occurs",
        },
        "unresolved_components": unresolved,
    }
    registry["canonical_digest"] = digest({k: v for k, v in registry.items() if k != "canonical_digest"})
    write_json(out / "historical_exposure_registry.json", registry)

    with (out / "historical_exposure_registry.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("record_type", "low_or_n", "high", "exposure_levels", "component_ids"))
        writer.writeheader()
        for rec in registry["inclusive_interval_exposures"]:
            writer.writerow({"record_type": "inclusive_interval", "low_or_n": rec["low"], "high": rec["high"], "exposure_levels": ";".join(rec["levels"]), "component_ids": "FORMAL_REGISTRY"})
        for rec in rows:
            writer.writerow({"record_type": "sparse_integer", "low_or_n": rec["n"], "high": rec["n"], "exposure_levels": ";".join(rec["exposure_levels"]), "component_ids": ";".join(rec["component_ids"])})

    comp_doc = {"schema": "a303656-historical-exposure-components-v2", "components": components}
    comp_doc["canonical_digest"] = digest(comp_doc)
    write_json(out / "historical_exposure_components.json", comp_doc)
    limitations = """# Historical exposure registry limitations

Status: **PARTIAL**. The checked-in complete interval and sparse ledgers are reconstructed, including the post-v1 Family U census. However, `logs/INTERRUPTED_RUNS.txt` records interrupted or abandoned processes for which the set of integers actually touched before termination cannot be reconstructed from complete result/return-code pairs.

Consequently, absence from this registry proves only `absent_from_reconstructed_registry`. It does **not** establish either `integer_unseen_any_recorded_evaluation` or `integer_unseen_exact_T` under this fail-closed registry version. The checked-in exact-T result families inventoried here are represented, but global completeness remains `NOT ESTABLISHED` until interrupted and otherwise unresolved exposure is reconstructed or proved empty.

The continuous inclusive interval `[240000000001,241600000000]` has length 1,600,000,000, greater than `L4=1,129,118,760`; therefore every fixed-P4 CRT class is historically exposed at E1. Design novelty is not historical freshness.
"""
    (out / "historical_exposure_limitations.md").write_text(limitations)
    manifest = {
        "schema": "a303656-historical-exposure-manifest-v2",
        "registry_digest": registry["canonical_digest"],
        "component_digest": comp_doc["canonical_digest"],
        "files": {p.name: sha256_file(p) for p in sorted(out.glob("historical_exposure_*")) if p.name != "historical_exposure_manifest.json"},
        "unresolved_components": unresolved,
    }
    manifest["canonical_digest"] = digest(manifest)
    write_json(out / "historical_exposure_manifest.json", manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
