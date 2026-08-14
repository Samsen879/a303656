#!/usr/bin/env python3
"""Fail-closed verifier for the exact P5 sparse feasibility artifacts."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from common import (
    ANCHOR_ROLES, CELL_HIGH, CELL_LOW, CELL_WIDTH, GLOBALS, L4, P4,
    P4_SQUARES, PROTECTED_HASHES, SHORTLIST, START_COMMIT, AuditError,
    atomic_json, build_prior_registry, canonical_digest, coverage_for_prime,
    demand, enumerate_base_tuples, evenly_spaced_indices, load_bases,
    load_json, load_pairs, load_shortlist, mask_digest, mask_int,
    registry_contains, sha256_file, verify_hashes,
)


CONCLUSION = "VALIDATED EXACT P5 SPARSE CROSS-CLASS PANEL FEASIBILITY AUDIT"
ALLOWED_INTERPRETATIONS = {
    "BALANCED P5 SPARSE HOLDOUT IS FEASIBLE",
    "ANCHOR-ONLY P5 SPARSE HOLDOUT IS FEASIBLE",
    "ONLY AN UNBALANCED FULL SPARSE CENSUS IS FEASIBLE",
    "P5 SPARSE PANEL MULTIPLICITY IS INSUFFICIENT",
    "MIXED / INCONCLUSIVE GEOMETRIC RESULT",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def alternate_member(residue: int, modulus: int) -> list[int]:
    low_k = (CELL_LOW - residue + modulus - 1) // modulus
    high_k = (CELL_HIGH - residue) // modulus
    if low_k > high_k:
        return []
    return [residue + k * modulus for k in range(low_k, high_k + 1)]


def p4_mask(tuple4: list[int], pairs: list[dict[str, int]]) -> int:
    value = 0
    for prime, modulus, residue in zip(P4, P4_SQUARES, tuple4):
        demand(0 <= residue < modulus, "fixed tuple residue outside modulus")
        for pair in pairs:
            delta = residue - pair["shift"]
            if delta % prime == 0 and delta % modulus != 0:
                value |= 1 << pair["pair_index"]
    return value


def fraction(value: Fraction) -> dict[str, int | str]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": format(value.numerator / value.denominator, ".18f")}


def source_provenance(root: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    source = metadata["source_provenance"]["source_commit"]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, stdout=subprocess.PIPE, check=True).stdout.strip()
    demand(subprocess.run(["git", "merge-base", "--is-ancestor", START_COMMIT, source], cwd=root).returncode == 0, "start not ancestor of source")
    demand(subprocess.run(["git", "merge-base", "--is-ancestor", source, head], cwd=root).returncode == 0, "source not ancestor of verifier HEAD")
    return {"starting_commit": START_COMMIT, "source_commit": source, "verification_head": head, "ancestry_verified": True}


def verify(root: Path, results: Path) -> dict[str, Any]:
    protected = verify_hashes(root, PROTECTED_HASHES)
    metadata = load_json(results / "metadata.json")
    provenance = source_provenance(root, metadata)
    demand(metadata["protected_hashes_before_and_after"] == protected, "protected hash record mismatch")
    demand(all(sha256_file(results / name) == digest for name, digest in metadata["artifact_sha256"].items()), "artifact hash manifest mismatch")
    demand(metadata["new_integer_T_evaluations"] == 0 and metadata["integer_values_recorded_from_CRT_only"], "integer-evaluation scope violation")
    demand(not any(metadata[k] for k in ("T_backends_called", "direct_oracle_called", "factorization_called", "two_square_test_called")), "forbidden evaluator invocation recorded")

    registry = load_json(results / "prior_evaluation_registry.json")
    expected_registry = build_prior_registry(root)
    demand(registry == expected_registry, "prior registry is incomplete, mutated, or non-normalized")
    demand(registry["completeness"]["status"] == "CERTIFIED COMPLETE", "prior registry not complete")

    multiplicity = load_json(results / "per_entry_multiplicity.json")
    shortlist = load_shortlist(root)
    entries = multiplicity["entries"]
    demand(len(entries) == 20 and [e["entry_id"] for e in entries] == [f"ENTRY-{i:03d}" for i in range(1, 21)], "adaptive shortlist entry deletion/reorder")
    for stored, frozen in zip(entries, shortlist["entries"]):
        for key, value in frozen.items():
            demand(stored.get(key) == value, f"shortlist mutation: {stored['entry_id']}/{key}")
    pairs = load_pairs(root)
    bases = load_bases(root)
    base_by_id = {b["base_id"]: b for b in bases}
    tuples = enumerate_base_tuples(bases, pairs)

    globals_value = load_json(root / GLOBALS)
    globals_by_base = {b["base_id"]: b for b in globals_value["bases"]}
    expected_anchors = {}
    for role in ANCHOR_ROLES:
        base_matches = [b for b in bases if role in b["roles"]]
        demand(len(base_matches) == 1, "anchor role ambiguity")
        base = base_matches[0]
        q, t = globals_by_base[base["base_id"]]["lexicographically_first_global_maximizer"]
        matches = [e["entry_id"] for e in entries if e["base_id"] == base["base_id"] and e["q"] == q and e["t"] == t]
        demand(len(matches) == 1, "mandatory anchor missing")
        expected_anchors[role] = matches[0]
    demand(multiplicity["anchor_entries"] == expected_anchors and len(set(expected_anchors.values())) == 6, "anchor map corruption")

    allowed: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for entry in entries:
        base = base_by_id[entry["base_id"]]
        base_mask = mask_int(base["coverage_mask_hex"])
        scored = []
        for t in range(entry["q2"]):
            fifth = coverage_for_prime(entry["q"], t, pairs)
            union = base_mask | fifth
            scored.append({"t": t, "delta": (fifth & ~base_mask).bit_count(), "union_mask_digest": mask_digest(union)})
        maximum = max(x["delta"] for x in scored)
        definitions = {
            "R": [x for x in scored if x["t"] == entry["t"]],
            "U": [x for x in scored if x["union_mask_digest"] == entry["resulting_union_mask_digest"]],
            "Q": [x for x in scored if x["delta"] == maximum],
        }
        for family, values in definitions.items():
            demand(values and all(0 <= x["t"] < entry["q2"] for x in values), "unauthorized q/t residue")
            allowed[(family, entry["entry_id"])] = values
            demand(entry["family_allowed_residue_counts"][family] == len(values), "allowed residue multiplicity mismatch")

    classes = read_jsonl(results / "occupied_fresh_class_manifest.jsonl")
    demand(classes and all(r["member_count"] == 1 and r["member"] is not None for r in classes), "occupied manifest contains zero/multi-member class")
    class_keys = [(r["family"], r["entry_id"], r["modulus"], r["class_residue"]) for r in classes]
    demand(len(class_keys) == len(set(class_keys)), "duplicate class was not deduplicated")
    by_entry: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    expected_occupied_keys: set[tuple[str, str, int, int]] = set()
    expected_descriptions: dict[tuple[str, str, int, int], dict[str, Any]] = {}
    for family in ("R", "U", "Q"):
        for entry in entries:
            for tuple4 in tuples[entry["base_id"]]:
                for residue_record in allowed[(family, entry["entry_id"])]:
                    q2 = entry["q2"]
                    modulus = L4 * q2
                    residues = (*tuple4, residue_record["t"], 34)
                    moduli = (*P4_SQUARES, q2, 40)
                    # Independent reconstruction by a direct CRT sum.
                    crt_value = sum(r * (modulus // m) * pow(modulus // m, -1, m) for r, m in zip(residues, moduli)) % modulus
                    members = alternate_member(crt_value, modulus)
                    demand(len(members) <= 1, "independent verifier found >1 activation-cell member")
                    if members:
                        key = (family, entry["entry_id"], modulus, crt_value)
                        expected_occupied_keys.add(key)
                        expected_descriptions[key] = {
                            "fixed_P4_tuple": list(tuple4), "t": residue_record["t"],
                            "resulting_union_mask_digest": residue_record["union_mask_digest"], "delta": residue_record["delta"],
                        }
    demand(set(class_keys) == expected_occupied_keys, "occupied CRT class manifest missing or contains extra class")

    for row in classes:
        key = (row["family"], row["entry_id"], row["modulus"], row["class_residue"])
        entry = next(e for e in entries if e["entry_id"] == row["entry_id"])
        demand(row["q"] == entry["q"] and row["q2"] == entry["q2"] and row["modulus"] == L4 * entry["q2"], "unauthorized q/modulus")
        demand(len(row["descriptions"]) == row["description_count"] == 1, "class description not exactly deduplicated")
        demand(row["descriptions"][0] == expected_descriptions[key], "wrong base/union/t class description")
        description = row["descriptions"][0]
        base = base_by_id[entry["base_id"]]
        demand(mask_digest(p4_mask(description["fixed_P4_tuple"], pairs)) == base["base_mask_digest"], "wrong base mask")
        for residue, modulus in zip((*description["fixed_P4_tuple"], description["t"], 34), (*P4_SQUARES, entry["q2"], 40)):
            demand(row["class_residue"] % modulus == residue, "CRT congruence corruption")
        members = alternate_member(row["class_residue"], row["modulus"])
        demand(members == [row["member"]] and CELL_LOW <= row["member"] <= CELL_HIGH, "activation-cell boundary/member corruption")
        old = registry_contains(registry, row["member"])
        demand(row["previously_evaluated"] == old and row["fresh"] == (not old), "previously evaluated integer marked fresh")
        demand(row["cell_position_numerator"] == row["member"] - CELL_LOW and row["cell_position_denominator"] == CELL_HIGH - CELL_LOW, "member position corruption")
        by_entry[(row["family"], row["entry_id"])].append(row)

    stored_metrics = multiplicity["metrics"]
    demand(len(stored_metrics) == 60, "adaptive entry/family deletion")
    for metric in stored_metrics:
        key = (metric["family"], metric["entry_id"])
        entry = next(e for e in entries if e["entry_id"] == metric["entry_id"])
        rows = sorted(by_entry[key], key=lambda r: (r["modulus"], r["class_residue"]))
        raw = len(tuples[entry["base_id"]]) * len(allowed[key])
        members = [r["member"] for r in rows]
        fresh = [r["member"] for r in rows if r["fresh"]]
        theoretical = Fraction(CELL_WIDTH, L4 * entry["q2"])
        actual = Fraction(len(rows), raw)
        boundary = sum(r["member"] - CELL_LOW <= (CELL_HIGH-CELL_LOW)//20 or CELL_HIGH-r["member"] <= (CELL_HIGH-CELL_LOW)//20 for r in rows)
        checks = {
            "generating_fixed_P4_tuple_count": len(tuples[entry["base_id"]]),
            "allowed_t_residue_count": len(allowed[key]), "raw_cartesian_class_count": raw,
            "distinct_CRT_class_count": raw, "duplicate_class_description_count": 0,
            "occupied_class_count": len(rows), "zero_member_class_count": raw-len(rows),
            "previously_evaluated_member_count": sum(r["previously_evaluated"] for r in rows),
            "fresh_occupied_class_count": sum(r["fresh"] for r in rows),
            "duplicate_integer_collision_count": len(members)-len(set(members)),
            "exact_member_list_digest": canonical_digest(members), "exact_fresh_member_list_digest": canonical_digest(fresh),
            "distinct_resulting_union_mask_count": len({x["union_mask_digest"] for x in allowed[key]}),
            "theoretical_occupancy_fraction": fraction(theoretical), "actual_occupied_fraction": fraction(actual),
            "occupancy_discrepancy": fraction(actual-theoretical), "boundary_5pct_member_count": boundary,
            "boundary_5pct_fraction": fraction(Fraction(boundary, len(rows)) if rows else Fraction()),
        }
        for field, expected in checks.items():
            demand(metric[field] == expected, f"metric reconstruction mismatch: {key}/{field}")
        demand(metric["class_residue_alignment"]["occupied_residues_digest"] == canonical_digest([r["class_residue"] for r in rows]), "class alignment digest mismatch")
        demand(metric["class_residue_alignment"]["member_positions_digest"] == canonical_digest([r["cell_position_numerator"] for r in rows]), "member-position digest mismatch")

    integers = read_jsonl(results / "integer_deduplication_manifest.jsonl")
    demand([r["n"] for r in integers] == sorted({r["member"] for r in classes}), "integer manifest duplicate/missing integer")
    descriptions_by_n: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in classes:
        descriptions_by_n[row["member"]].append({"class_id": row["class_id"], "family": row["family"], "entry_id": row["entry_id"], "q": row["q"], "modulus": row["modulus"], "class_residue": row["class_residue"]})
    for row in integers:
        expected = sorted(descriptions_by_n[row["n"]], key=lambda x: (x["family"], x["entry_id"], x["modulus"], x["class_residue"]))
        demand(row["descriptions"] == expected and row["description_count"] == len(expected), "duplicate integer provenance not deduplicated")
        old = registry_contains(registry, row["n"])
        demand(row["previously_evaluated"] == old and row["fresh"] == (not old), "integer freshness mismatch")

    feasibility_report = load_json(results / "feasibility_report.json")
    forbidden = feasibility_report["forbidden_activity"]
    demand(not any(forbidden.values()), "accidental forbidden evaluator invocation")
    demand(feasibility_report["shortlist_sha256"] == sha256_file(root / SHORTLIST) and feasibility_report["all_shortlist_entries_processed"], "shortlist mutation/deletion")
    feasibility = feasibility_report["feasibility"]
    metric_by_key = {(m["family"], m["entry_id"]): m for m in stored_metrics}
    anchor_ids = list(expected_anchors.values())
    for family in ("R", "U", "Q"):
        counts = [metric_by_key[(family, e["entry_id"])]["fresh_occupied_class_count"] for e in entries]
        anchor_counts = [metric_by_key[(family, e)]["fresh_occupied_class_count"] for e in anchor_ids]
        stored = feasibility["families"][family]
        demand(stored["s_all"] == min(counts) and stored["s_anchor"] == min(anchor_counts), "balanced feasibility minimum mismatch")
        for threshold in (1,4,8,16,32,64):
            demand(stored["entries_meeting_threshold"][str(threshold)] == sum(x >= threshold for x in counts), "threshold entry count mismatch")
            demand(stored["anchors_meeting_threshold"][str(threshold)] == sum(x >= threshold for x in anchor_counts), "threshold anchor count mismatch")
    demand(feasibility["interpretation_label"] in ALLOWED_INTERPRETATIONS, "forbidden interpretation label")

    # Deterministic design verification, including ordering even when A/B are infeasible.
    design_a = load_json(results / "design_A_all_entry_balanced.json")
    design_b = load_json(results / "design_B_anchor_balanced.json")
    design_c = load_json(results / "design_C_full_sparse_census.json")
    for family in ("R", "U", "Q"):
        for design, ids, limit, field in ((design_a, [e["entry_id"] for e in entries], 32, "s_all"), (design_b, anchor_ids, 64, "s_anchor")):
            score = feasibility["families"][family][field]
            stored = design["families"][family]
            demand(stored["feasible"] == (score >= 8), "design feasibility mismatch")
            if score >= 8:
                count = min(limit, score)
                demand(len(stored["entries"]) == len(ids), "balanced design entry deletion")
                for selected, entry_id in zip(stored["entries"], ids):
                    rows = sorted((r for r in by_entry[(family, entry_id)] if r["fresh"]), key=lambda r: (r["modulus"], r["class_residue"], r["class_id"]))
                    indices = evenly_spaced_indices(len(rows), count)
                    demand(selected["selection_indices"] == indices and [x["class_id"] for x in selected["classes"]] == [rows[i]["class_id"] for i in indices], "non-deterministic balanced panel selection")
    expected_u = []
    for entry in entries:
        for row in sorted((r for r in by_entry[("U", entry["entry_id"])] if r["fresh"]), key=lambda r: (r["modulus"], r["class_residue"])):
            expected_u.append({"entry_id": entry["entry_id"], "class_id": row["class_id"], "n": row["member"], "modulus": row["modulus"], "class_residue": row["class_residue"]})
    demand(design_c["classes"] == expected_u and design_c["fresh_class_description_count"] == len(expected_u), "non-deterministic/full-census selection corruption")

    geometry = load_json(results / "geometry_diagnostics.json")
    demand(geometry["activation_cell"] == [CELL_LOW, CELL_HIGH] and geometry["cell_width"] == CELL_WIDTH, "activation-cell boundary corruption")
    demand(not geometry["random_sampling_claim_made"] and not geometry["CRT_class_independence_claim_made"], "prohibited random/independence language flag")
    demand(verify_hashes(root, PROTECTED_HASHES) == protected, "protected hashes changed during verification")
    return {
        "schema": "a303656-p5-sparse-feasibility-verification-v1", "status": "PASS",
        "validation_conclusion": CONCLUSION, "interpretation_label": feasibility["interpretation_label"],
        "mathematical_status": "UNRESOLVED", "git_provenance": provenance,
        "prior_registry_complete": True, "shortlist_unchanged": True, "shortlist_entry_count": 20,
        "anchor_entry_count": 6, "family_definitions_verified": ["R", "U", "Q"],
        "CRT_congruences_independently_verified": True, "maximum_activation_cell_member_count": 1,
        "previously_evaluated_integers_excluded_from_fresh": True, "class_and_integer_deduplication_exact": True,
        "feasibility_metrics_reconstructed": True, "provisional_selections_reconstructed": True,
        "T_backend_called": False, "direct_oracle_called": False, "factorization_called": False, "two_square_test_called": False,
        "protected_hashes_unchanged": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = verify(args.root.resolve(), args.results.resolve())
        if args.output:
            atomic_json(args.output.resolve(), report)
        print(CONCLUSION)
        print(report["interpretation_label"])
        return 0
    except (AuditError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"p5_sparse_verifier: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
