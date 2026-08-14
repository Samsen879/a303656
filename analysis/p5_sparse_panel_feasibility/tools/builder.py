#!/usr/bin/env python3
"""Construct the exact P5 sparse cross-class feasibility artifacts.

No integer arithmetic property is evaluated: member integers are only CRT
solutions intersected with the frozen activation cell.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from common import (
    ANCHOR_ROLES, CELL_HIGH, CELL_LOW, CELL_WIDTH, GLOBALS, LANDSCAPES, L4,
    PROTECTED_HASHES, SHORTLIST, START_COMMIT, AuditError, atomic_json,
    build_class, build_prior_registry, canonical_digest, class_member, demand,
    enumerate_base_tuples, evenly_spaced_indices, load_bases, load_json,
    load_landscapes, load_pairs, load_shortlist, mask_digest, mask_int,
    registry_contains, sha256_file, verify_hashes, write_jsonl,
)


FAMILIES = ("R", "U", "Q")
THRESHOLDS = (1, 4, 8, 16, 32, 64)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    demand(result.returncode == 0, f"git {' '.join(args)} failed")
    return result.stdout.strip()


def verify_source(root: Path, source_commit: str) -> dict[str, Any]:
    head = git(root, "rev-parse", "HEAD")
    demand(git(root, "show", "-s", "--format=%P", START_COMMIT) == "ac161b0f6a60c6453c33b4b94435881a49dc62d0", "initial P/O direct-parent gate changed")
    demand(git(root, "show", "-s", "--format=%P", "ac161b0f6a60c6453c33b4b94435881a49dc62d0") == "02028314ab92d7aa089475f9a6bc96688526f731", "initial chain changed")
    result = subprocess.run(["git", "merge-base", "--is-ancestor", source_commit, head], cwd=root, check=False)
    demand(result.returncode == 0, "declared source commit is not an ancestor of HEAD")
    result = subprocess.run(["git", "merge-base", "--is-ancestor", START_COMMIT, source_commit], cwd=root, check=False)
    demand(result.returncode == 0, "required starting commit is not an ancestor of source commit")
    return {"starting_commit": START_COMMIT, "source_commit": source_commit, "head_at_generation": head, "source_is_ancestor": True}


def entry_records(root: Path, pairs: list[dict[str, int]], bases: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, str]]:
    shortlist = load_shortlist(root)
    landscapes = load_landscapes(root)
    base_by_id = {b["base_id"]: b for b in bases}
    records: list[dict[str, Any]] = []
    allowed: dict[str, list[dict[str, Any]]] = {family: [] for family in FAMILIES}
    for ordinal, frozen in enumerate(shortlist["entries"], 1):
        entry = dict(frozen)
        entry_id = f"ENTRY-{ordinal:03d}"
        entry["entry_id"] = entry_id
        base = base_by_id[entry["base_id"]]
        demand(base["base_mask_digest"] == entry["base_mask_digest"], "shortlist/base digest mismatch")
        q, q2 = entry["q"], entry["q2"]
        demand(q2 == q * q and q in landscapes, "unauthorized q")
        summary = next((x for x in landscapes[q]["base_summaries"] if x["base_id"] == entry["base_id"]), None)
        demand(summary is not None, "missing compressed base summary")
        base_mask = mask_int(base["coverage_mask_hex"])
        scored: list[dict[str, Any]] = []
        for t in range(q2):
            from common import coverage_for_prime
            fifth = coverage_for_prime(q, t, pairs)
            union = base_mask | fifth
            scored.append({"t": t, "delta": (fifth & ~base_mask).bit_count(), "union_mask_digest": mask_digest(union)})
        representative = [x for x in scored if x["t"] == entry["t"]]
        demand(len(representative) == 1 and representative[0]["union_mask_digest"] == entry["resulting_union_mask_digest"], "shortlist representative union mismatch")
        r_rows = representative
        u_rows = [x for x in scored if x["union_mask_digest"] == entry["resulting_union_mask_digest"]]
        q_rows = [x for x in scored if x["delta"] == summary["maximum_delta"]]
        demand(len(q_rows) == summary["argmax_count"], "Family Q multiplicity differs from compressed authority")
        demand(entry["t"] in {x["t"] for x in q_rows}, "shortlist t is not q-marginal-optimal")
        for family, rows in (("R", r_rows), ("U", u_rows), ("Q", q_rows)):
            allowed[family].append({"entry_id": entry_id, "residues": rows})
        entry["family_allowed_residue_counts"] = {"R": len(r_rows), "U": len(u_rows), "Q": len(q_rows)}
        records.append(entry)

    globals_value = load_json(root / GLOBALS)
    global_by_base = {b["base_id"]: b for b in globals_value["bases"]}
    anchor_map: dict[str, str] = {}
    for role in ANCHOR_ROLES:
        matches = [b for b in bases if role in b["roles"]]
        demand(len(matches) == 1, f"anchor base role is not unique: {role}")
        base = matches[0]
        authority = global_by_base[base["base_id"]]
        q, t = authority["lexicographically_first_global_maximizer"]
        entries = [e for e in records if e["base_id"] == base["base_id"] and e["q"] == q and e["t"] == t]
        demand(len(entries) == 1, f"anchor global optimum absent/nonunique in shortlist: {role}")
        anchor_map[role] = entries[0]["entry_id"]
    demand(len(set(anchor_map.values())) == 6, "six anchor entries are not distinct")
    return records, allowed, anchor_map


def fraction(value: Fraction) -> dict[str, int | str]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": format(value.numerator / value.denominator, ".18f")}


def build_classes(
    entries: list[dict[str, Any]], allowed: dict[str, list[dict[str, Any]]],
    tuples: dict[str, list[tuple[int, int, int, int]]], registry: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    entry_by_id = {e["entry_id"]: e for e in entries}
    class_rows: list[dict[str, Any]] = []
    metrics: list[dict[str, Any]] = []
    entry_class_rows: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for family in FAMILIES:
        for allowed_record in allowed[family]:
            entry_id = allowed_record["entry_id"]
            entry = entry_by_id[entry_id]
            fixed = tuples[entry["base_id"]]
            raw_count = len(fixed) * len(allowed_record["residues"])
            grouped: dict[tuple[int, int], dict[str, Any]] = {}
            for tuple4 in fixed:
                for residue_record in allowed_record["residues"]:
                    t = residue_record["t"]
                    residue, modulus = build_class(tuple4, entry["q"], t)
                    key = (modulus, residue)
                    description = {
                        "fixed_P4_tuple": list(tuple4), "t": t,
                        "resulting_union_mask_digest": residue_record["union_mask_digest"],
                        "delta": residue_record["delta"],
                    }
                    if key not in grouped:
                        grouped[key] = {"descriptions": []}
                    grouped[key]["descriptions"].append(description)
            rows: list[dict[str, Any]] = []
            for (modulus, residue), grouped_value in sorted(grouped.items()):
                descriptions = sorted(grouped_value["descriptions"], key=lambda x: (x["fixed_P4_tuple"], x["t"], x["resulting_union_mask_digest"]))
                members = class_member(residue, modulus)
                member = members[0] if members else None
                old = member is not None and registry_contains(registry, member)
                row = {
                    "class_id": f"{family}-{entry_id}-{modulus}-{residue}",
                    "family": family, "entry_id": entry_id, "base_id": entry["base_id"],
                    "q": entry["q"], "q2": entry["q2"], "modulus": modulus, "class_residue": residue,
                    "description_count": len(descriptions), "descriptions": descriptions,
                    "member_count": len(members), "member": member,
                    "previously_evaluated": bool(old), "fresh": bool(member is not None and not old),
                    "cell_position_numerator": None if member is None else member - CELL_LOW,
                    "cell_position_denominator": CELL_HIGH - CELL_LOW,
                }
                rows.append(row)
                class_rows.append(row)
            entry_class_rows[(family, entry_id)] = rows
            occupied_members = [r["member"] for r in rows if r["member"] is not None]
            fresh_members = [r["member"] for r in rows if r["fresh"]]
            distinct_occupied = len(set(occupied_members))
            occupied = len(occupied_members)
            modulus = L4 * entry["q2"]
            actual = Fraction(occupied, len(rows)) if rows else Fraction()
            theoretical = Fraction(CELL_WIDTH, modulus)
            boundary_count = sum(
                r["member"] is not None and (
                    r["member"] - CELL_LOW <= (CELL_HIGH - CELL_LOW) // 20 or
                    CELL_HIGH - r["member"] <= (CELL_HIGH - CELL_LOW) // 20
                ) for r in rows
            )
            metrics.append({
                "family": family, "entry_id": entry_id, "base_id": entry["base_id"], "q": entry["q"],
                "L5": modulus, "cell_width_over_L5": fraction(theoretical),
                "generating_fixed_P4_tuple_count": len(fixed),
                "allowed_t_residue_count": len(allowed_record["residues"]),
                "raw_cartesian_class_count": raw_count,
                "distinct_CRT_class_count": len(rows),
                "duplicate_class_description_count": raw_count - len(rows),
                "occupied_class_count": occupied,
                "zero_member_class_count": len(rows) - occupied,
                "previously_evaluated_member_count": sum(r["previously_evaluated"] for r in rows),
                "fresh_occupied_class_count": sum(r["fresh"] for r in rows),
                "duplicate_integer_collision_count": occupied - distinct_occupied,
                "exact_member_list_digest": canonical_digest(occupied_members),
                "exact_fresh_member_list_digest": canonical_digest(fresh_members),
                "distinct_resulting_union_mask_count": len({d["resulting_union_mask_digest"] for r in rows for d in r["descriptions"]}),
                "theoretical_occupancy_fraction": fraction(theoretical),
                "actual_occupied_fraction": fraction(actual),
                "occupancy_discrepancy": fraction(actual - theoretical),
                "class_residue_alignment": {
                    "cell_low_mod_L5": CELL_LOW % modulus,
                    "cell_high_mod_L5": CELL_HIGH % modulus,
                    "occupied_residues_digest": canonical_digest([r["class_residue"] for r in rows if r["member"] is not None]),
                    "member_positions_digest": canonical_digest([r["cell_position_numerator"] for r in rows if r["member"] is not None]),
                },
                "boundary_5pct_member_count": boundary_count,
                "boundary_5pct_fraction": fraction(Fraction(boundary_count, occupied) if occupied else Fraction()),
            })

    integer_groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in class_rows:
        if row["member"] is not None:
            integer_groups[row["member"]].append({
                "class_id": row["class_id"], "family": row["family"], "entry_id": row["entry_id"],
                "q": row["q"], "modulus": row["modulus"], "class_residue": row["class_residue"],
            })
    integers = [{
        "n": n, "fresh": not registry_contains(registry, n), "previously_evaluated": registry_contains(registry, n),
        "description_count": len(descriptions), "descriptions": sorted(descriptions, key=lambda x: (x["family"], x["entry_id"], x["modulus"], x["class_residue"])),
    } for n, descriptions in sorted(integer_groups.items())]
    dedup = {
        "class_description_count": sum(r["description_count"] for r in class_rows),
        "distinct_family_entry_class_count": len(class_rows),
        "duplicate_class_description_count": sum(r["description_count"] - 1 for r in class_rows),
        "occupied_family_entry_class_count": sum(r["member_count"] for r in class_rows),
        "distinct_integer_count": len(integers),
        "duplicate_integer_description_count": sum(max(0, r["description_count"] - 1) for r in integers),
        "distinct_resulting_union_mask_count": len({d["resulting_union_mask_digest"] for r in class_rows for d in r["descriptions"]}),
        "distinct_shortlist_provenance_count": len(entries),
        "integer_manifest_digest": canonical_digest(integers),
    }
    return class_rows, integers, {"metrics": metrics, "deduplication": dedup, "entry_class_rows": entry_class_rows}


def designs(entries: list[dict[str, Any]], anchor_map: dict[str, str], entry_rows: dict[tuple[str, str], list[dict[str, Any]]], metrics: list[dict[str, Any]]) -> tuple[dict, dict, dict, dict]:
    metric = {(m["family"], m["entry_id"]): m for m in metrics}
    anchor_ids = list(anchor_map.values())
    feasibility: dict[str, Any] = {"families": {}, "thresholds": list(THRESHOLDS)}
    for family in FAMILIES:
        all_counts = [metric[(family, e["entry_id"])]["fresh_occupied_class_count"] for e in entries]
        anchor_counts = [metric[(family, entry_id)]["fresh_occupied_class_count"] for entry_id in anchor_ids]
        feasibility["families"][family] = {
            "s_all": min(all_counts), "s_anchor": min(anchor_counts),
            "entries_meeting_threshold": {str(t): sum(n >= t for n in all_counts) for t in THRESHOLDS},
            "anchors_meeting_threshold": {str(t): sum(n >= t for n in anchor_counts) for t in THRESHOLDS},
        }

    def select(family: str, entry_id: str, count: int) -> dict[str, Any]:
        rows = [r for r in entry_rows[(family, entry_id)] if r["fresh"]]
        rows.sort(key=lambda r: (r["modulus"], r["class_residue"], r["class_id"]))
        indices = evenly_spaced_indices(len(rows), count)
        selected = [rows[i] for i in indices]
        return {"entry_id": entry_id, "selection_count": count, "ordered_fresh_class_count": len(rows), "selection_indices": indices,
                "classes": [{"class_id": r["class_id"], "n": r["member"], "modulus": r["modulus"], "class_residue": r["class_residue"]} for r in selected],
                "member_digest": canonical_digest([r["member"] for r in selected])}

    design_a: dict[str, Any] = {"schema": "a303656-p5-provisional-design-A-v1", "name": "all-entry balanced", "families": {}}
    design_b: dict[str, Any] = {"schema": "a303656-p5-provisional-design-B-v1", "name": "anchor-balanced", "anchor_map": anchor_map, "families": {}}
    for family in FAMILIES:
        s_all = feasibility["families"][family]["s_all"]
        if s_all >= 8:
            count = min(32, s_all)
            design_a["families"][family] = {"feasible": True, "per_entry_count": count, "entries": [select(family, e["entry_id"], count) for e in entries]}
        else:
            design_a["families"][family] = {"feasible": False, "reason": "s_all < 8", "entries": []}
        s_anchor = feasibility["families"][family]["s_anchor"]
        if s_anchor >= 8:
            count = min(64, s_anchor)
            design_b["families"][family] = {"feasible": True, "per_anchor_count": count, "entries": [select(family, entry_id, count) for entry_id in anchor_ids]}
        else:
            design_b["families"][family] = {"feasible": False, "reason": "s_anchor < 8", "entries": []}

    u_counts = {e["entry_id"]: metric[("U", e["entry_id"])]["fresh_occupied_class_count"] for e in entries}
    u_refs = []
    for entry in entries:
        rows = sorted((r for r in entry_rows[("U", entry["entry_id"])] if r["fresh"]), key=lambda r: (r["modulus"], r["class_residue"]))
        u_refs.extend({"entry_id": entry["entry_id"], "class_id": r["class_id"], "n": r["member"], "modulus": r["modulus"], "class_residue": r["class_residue"]} for r in rows)
    design_c = {
        "schema": "a303656-p5-provisional-design-C-v1", "name": "full sparse census", "family": "U",
        "fresh_class_description_count": len(u_refs), "classes": u_refs,
        "per_entry_counts": u_counts, "minimum_per_entry": min(u_counts.values()), "maximum_per_entry": max(u_counts.values()),
        "imbalance_ratio": None if min(u_counts.values()) == 0 else fraction(Fraction(max(u_counts.values()), min(u_counts.values()))),
        "severe_sample_imbalance_reported": max(u_counts.values()) != min(u_counts.values()),
        "selection_uses_T_or_arithmetic_properties": False,
    }
    if max(v["s_all"] for v in feasibility["families"].values()) >= 8:
        interpretation = "BALANCED P5 SPARSE HOLDOUT IS FEASIBLE"
    elif max(v["s_anchor"] for v in feasibility["families"].values()) >= 8:
        interpretation = "ANCHOR-ONLY P5 SPARSE HOLDOUT IS FEASIBLE"
    elif len(u_refs) > 0:
        interpretation = "ONLY AN UNBALANCED FULL SPARSE CENSUS IS FEASIBLE"
    elif all(metric[(f, e["entry_id"])]["fresh_occupied_class_count"] == 0 for f in FAMILIES for e in entries):
        interpretation = "P5 SPARSE PANEL MULTIPLICITY IS INSUFFICIENT"
    else:
        interpretation = "MIXED / INCONCLUSIVE GEOMETRIC RESULT"
    feasibility["interpretation_label"] = interpretation
    return feasibility, design_a, design_b, design_c


def build(root: Path, output: Path, source_commit: str) -> dict[str, Any]:
    provenance = verify_source(root, source_commit)
    protected_before = verify_hashes(root, PROTECTED_HASHES)
    registry = build_prior_registry(root)
    demand(registry["completeness"]["status"] == "CERTIFIED COMPLETE", "prior registry incomplete")
    pairs = load_pairs(root)
    bases = load_bases(root)
    tuples = enumerate_base_tuples(bases, pairs)
    entries, allowed, anchor_map = entry_records(root, pairs, bases)
    class_rows, integers, built = build_classes(entries, allowed, tuples, registry)
    feasibility, design_a, design_b, design_c = designs(entries, anchor_map, built["entry_class_rows"], built["metrics"])

    output.mkdir(parents=True, exist_ok=True)
    atomic_json(output / "prior_evaluation_registry.json", registry)
    atomic_json(output / "per_entry_multiplicity.json", {
        "schema": "a303656-p5-family-entry-multiplicity-v1", "entry_count": len(entries), "entries": entries,
        "anchor_entries": anchor_map, "metrics": built["metrics"], "deduplication": built["deduplication"],
    })
    occupied_manifest_rows = [row for row in class_rows if row["member"] is not None]
    write_jsonl(output / "occupied_fresh_class_manifest.jsonl", occupied_manifest_rows)
    write_jsonl(output / "integer_deduplication_manifest.jsonl", integers)
    atomic_json(output / "design_A_all_entry_balanced.json", design_a)
    atomic_json(output / "design_B_anchor_balanced.json", design_b)
    atomic_json(output / "design_C_full_sparse_census.json", design_c)
    geometry = {
        "schema": "a303656-p5-sparse-geometry-v1", "activation_cell": [CELL_LOW, CELL_HIGH], "cell_width": CELL_WIDTH,
        "entries": [{k: m[k] for k in (
            "family", "entry_id", "q", "L5", "cell_width_over_L5", "theoretical_occupancy_fraction",
            "actual_occupied_fraction", "occupancy_discrepancy", "class_residue_alignment",
            "boundary_5pct_member_count", "boundary_5pct_fraction",
        )} for m in built["metrics"]],
        "diagnostic_rule": "boundary alignment is flagged per entry when more than half of occupied members lie in the first or last 5 percent of the activation cell",
        "boundary_alignment_driven_entries": [f"{m['family']}/{m['entry_id']}" for m in built["metrics"] if m["boundary_5pct_fraction"]["numerator"] * 2 > m["boundary_5pct_fraction"]["denominator"]],
        "random_sampling_claim_made": False, "CRT_class_independence_claim_made": False,
    }
    atomic_json(output / "geometry_diagnostics.json", geometry)
    report = {
        "schema": "a303656-exact-p5-sparse-feasibility-report-v1", "source_provenance": provenance,
        "prior_registry_complete": True, "shortlist_sha256": sha256_file(root / SHORTLIST),
        "shortlist_entry_count": len(entries), "all_shortlist_entries_processed": True, "anchor_entries": anchor_map,
        "family_definitions": {
            "R": "only the frozen representative t",
            "U": "all t modulo q^2 with B union C(q,t) equal to the frozen union mask",
            "Q": "all t modulo q^2 attaining that base/q maximum marginal coverage; union masks retained separately",
        },
        "Family_Q_future_integer_census_requires_new_web_review_and_freeze": True,
        "feasibility": feasibility, "deduplication": built["deduplication"],
        "forbidden_activity": {"T_evaluator_called": False, "winner_mask_evaluated": False, "two_square_test_called": False, "factorization_called": False, "direct_oracle_called": False},
        "mathematical_status": "UNRESOLVED",
    }
    atomic_json(output / "feasibility_report.json", report)
    protected_after = verify_hashes(root, PROTECTED_HASHES)
    demand(protected_after == protected_before, "protected authorities changed during build")
    artifact_names = sorted(p.name for p in output.iterdir() if p.is_file() and p.name not in {"metadata.json", "verification_report.json", "corruption_tests.json", "return_codes.json"})
    metadata = {
        "schema": "a303656-p5-sparse-feasibility-metadata-v1", "source_provenance": provenance,
        "protected_hashes_before_and_after": protected_after, "artifact_sha256": {name: sha256_file(output / name) for name in artifact_names},
        "new_integer_T_evaluations": 0, "integer_values_recorded_from_CRT_only": True,
        "T_backends_called": False, "direct_oracle_called": False, "factorization_called": False, "two_square_test_called": False,
    }
    atomic_json(output / "metadata.json", metadata)
    return {"entry_count": len(entries), "all_class_count": len(class_rows), "occupied_manifest_row_count": len(occupied_manifest_rows), "integer_count": len(integers), "interpretation": feasibility["interpretation_label"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        result = build(args.root.resolve(), args.output.resolve(), args.source_commit)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (AuditError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"p5_sparse_builder: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
