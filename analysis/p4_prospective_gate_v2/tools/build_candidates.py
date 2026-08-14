#!/usr/bin/env python3
"""Construct deterministic, T-blind prospective panel candidates; execute none."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from common import (MODS, class_members, digest, fixed_p4_class,
                    live_authority, pair_domain, prime_masks,
                    project_live, sha256_file, write_json)

INTEGER_INDICES = (0, 7, 14, 21, 28, 35, 42, 49)


def enumerate_universe() -> dict[int, dict[str, dict[str, dict]]]:
    pairs = pair_domain()
    live_indices, live_mask = live_authority()
    masks = [prime_masks(pairs, p) for p in (3, 7, 11, 23)]
    universe = {h: defaultdict(dict) for h in (199, 200, 201)}
    for t7 in range(MODS[1]):
        for t11 in range(MODS[2]):
            base = masks[0][2] | masks[1][t7] | masks[2][t11]
            for t23 in range(MODS[3]):
                full = base | masks[3][t23]
                h8 = (full & live_mask).bit_count()
                if h8 not in universe:
                    continue
                full_bytes = full.to_bytes(51, "little")
                full_digest = hashlib.sha256(full_bytes).hexdigest()
                live = project_live(full, live_indices)
                projection_digest = hashlib.sha256(live.to_bytes(38, "little")).hexdigest()
                row = universe[h8][projection_digest].setdefault(full_digest, {
                    "H8": h8,
                    "raw_G": full.bit_count(),
                    "covered_dead": (full & ~live_mask).bit_count(),
                    "full_mask_digest": full_digest,
                    "full_mask_hex": full_bytes.hex(),
                    "live_projection_digest": projection_digest,
                    "live_projection_hex": live.to_bytes(38, "little").hex(),
                    "tuples": [],
                })
                row["tuples"].append([2, t7, t11, t23])
    return universe


def known_exposure(registry: dict, n: int) -> tuple[bool, list[str]]:
    levels = set()
    for rec in registry["inclusive_interval_exposures"]:
        if rec["low"] <= n <= rec["high"]:
            levels.update(rec["levels"])
    # Sparse list is small enough for a prebuilt map at the caller, but retain a
    # literal implementation for transparent verification.
    for rec in registry["sparse_integer_exposures"]:
        if rec["n"] == n:
            levels.update(rec["exposure_levels"])
    return bool(levels), sorted(levels)


def eligible_masks(projections: dict, raw_g: int | None) -> list[tuple[str, str, dict]]:
    rows = []
    for pd, masks in projections.items():
        for fd, row in masks.items():
            if len(row["tuples"]) >= 4 and (raw_g is None or row["raw_G"] == raw_g):
                rows.append((pd, fd, row))
    return sorted(rows)


def choose_a(universe: dict) -> dict[int, list[tuple[str, str, dict]]]:
    chosen = {}
    for h in (199, 200, 201):
        by_projection = defaultdict(list)
        for pd, fd, row in eligible_masks(universe[h], 227):
            by_projection[pd].append((pd, fd, row))
        usable = [(pd, rows) for pd, rows in sorted(by_projection.items()) if len(rows) >= 2]
        if len(usable) < 2:
            raise ValueError(f"DESIGN_A_CAPACITY_H{h}")
        chosen[h] = usable[0][1][:2] + usable[1][1][:2]
    return chosen


def choose_b(universe: dict) -> dict[int, list[tuple[str, str, dict]]]:
    chosen = {}
    for h in (199, 200, 201):
        by_projection = defaultdict(list)
        for pd, fd, row in eligible_masks(universe[h], 227):
            by_projection[pd].append((pd, fd, row))
        usable = [(pd, rows[0]) for pd, rows in sorted(by_projection.items()) if rows]
        if len(usable) < 3:
            raise ValueError(f"DESIGN_B_CAPACITY_H{h}")
        chosen[h] = [row for _, row in usable[:3]]
    return chosen


def choose_c(universe: dict) -> dict[int, list[tuple[str, str, dict]]]:
    chosen = {}
    for h in (199, 200, 201):
        candidates = eligible_masks(universe[h], None)
        by_projection = defaultdict(list)
        for row in candidates:
            by_projection[row[0]].append(row)
        if len(by_projection) < 5:
            raise ValueError(f"DESIGN_C_PROJECTION_CAPACITY_H{h}")
        selected = []
        for pd, rows in sorted(by_projection.items())[:5]:
            # Preserve raw G=227 when available; otherwise choose the closest,
            # then the digest. This is fixed before any integer outcome exists.
            rows.sort(key=lambda x: (abs(x[2]["raw_G"] - 227), x[2]["raw_G"], x[1]))
            selected.append(rows[0])
        chosen[h] = selected
    return chosen


def materialize(name: str, selected: dict, registry: dict, designed_classes: set[tuple[int, ...]],
                frozen_masks: set[str], known_projections: set[str]) -> dict:
    rows = []
    selected_integers = set()
    exact_complete = registry["completeness_for_exact_T"] == "COMPLETE"
    any_complete = registry["completeness_for_any_recorded_evaluation"] == "COMPLETE"
    for h in (199, 200, 201):
        for pd, fd, mask in selected[h]:
            for tup_list in sorted(mask["tuples"])[:4]:
                tup = tuple(tup_list)
                residue = fixed_p4_class(tup)
                available = []
                excluded = []
                for n in class_members(residue):
                    exposed, levels = known_exposure(registry, n)
                    (excluded if exposed else available).append((n, levels))
                if len(available) <= INTEGER_INDICES[-1]:
                    raise ValueError(f"INSUFFICIENT_RECONSTRUCTED_UNSEEN_MEMBERS:{tup}")
                integers = []
                for index in INTEGER_INDICES:
                    n, levels = available[index]
                    if n in selected_integers:
                        raise ValueError(f"DUPLICATE_INTEGER:{n}")
                    selected_integers.add(n)
                    integers.append({
                        "n": n,
                        "selection_index": index,
                        "absent_from_reconstructed_registry": True,
                        "known_exposure_levels": levels,
                        "integer_unseen_any_recorded_evaluation": True if any_complete else "NOT_ESTABLISHED",
                        "integer_unseen_exact_T": True if exact_complete else "NOT_ESTABLISHED",
                    })
                rows.append({
                    "H8": h,
                    "raw_G": mask["raw_G"],
                    "covered_dead": mask["covered_dead"],
                    "live_projection_digest": pd,
                    "full_mask_digest": fd,
                    "tuple": list(tup),
                    "class_residue_mod_L4": residue,
                    "design_novel_class": tup not in designed_classes,
                    "historically_exposed_class": True,
                    "design_novel_full_mask": fd not in frozen_masks,
                    "design_novel_live_projection": pd not in known_projections,
                    "activation_cell_member_count": len(class_members(residue)),
                    "known_exposure_exclusion_count": len(excluded),
                    "selected_integers": integers,
                })
    hierarchy = {}
    for h in (199, 200, 201):
        subset = [r for r in rows if r["H8"] == h]
        hierarchy[str(h)] = {
            "live_projection_count": len({r["live_projection_digest"] for r in subset}),
            "full_mask_count": len({r["full_mask_digest"] for r in subset}),
            "CRT_class_count": len(subset),
            "integer_count": sum(len(r["selected_integers"]) for r in subset),
            "raw_G_values": sorted({r["raw_G"] for r in subset}),
        }
    all_n = sorted(selected_integers)
    doc = {
        "schema": "a303656-p4-live-prospective-candidate-v2",
        "design_id": name,
        "status": "CANDIDATE_ONLY_NOT_AUTHORIZED_FOR_T_EVALUATION",
        "selection_T_blind": True,
        "selection_order": ["H8", "live_projection_digest", "full_mask_digest", "lexicographic_tuple", "ascending_absent_integer"],
        "integer_indices": list(INTEGER_INDICES),
        "registry_digest": registry["canonical_digest"],
        "hierarchy": hierarchy,
        "class_rows": rows,
        "distinct_integer_count": len(all_n),
        "collision_report": {"duplicate_integer_count": sum(len(r["selected_integers"]) for r in rows) - len(all_n), "status": "PASS"},
        "minimum_integer": min(all_n),
        "maximum_integer": max(all_n),
        "exposure_level_exclusions": "all reconstructed E1-E4 interval/sparse exposures excluded before indexed selection",
        "limitations": [
            "integer_unseen_any_recorded_evaluation is NOT_ESTABLISHED while interrupted-run exposure remains unreconstructed",
            "historically_exposed_class is true for every fixed-P4 class because of the continuous 1.6B E1 interval",
        ],
    }
    if name == "DESIGN_C":
        doc["limitations"].append("all five H8=201 projections require raw-G relaxation; raw G is not identical across bands")
    doc["canonical_digest"] = digest({k: v for k, v in doc.items() if k != "canonical_digest"})
    return doc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--registry", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    root, out = args.root.resolve(), args.output.resolve()
    registry = json.loads(args.registry.read_text())
    out.mkdir(parents=True, exist_ok=True)
    universe = enumerate_universe()

    designed_classes = set()
    panel = root / "analysis/p4_maximizer_census/class_panel.csv"
    if panel.exists():
        import csv
        for row in csv.DictReader(panel.open()):
            keys = next((ks for ks in (("t3", "t7", "t11", "t23"), ("r3", "r7", "r11", "r23")) if all(k in row for k in ks)), None)
            if keys:
                designed_classes.add(tuple(int(row[k]) for k in keys))
    frozen = json.loads((root / "analysis/fifth_prime_marginal_coverage/results/frozen_base_masks.json").read_text())
    frozen_masks = {row.get("mask_digest", row.get("base_mask_digest")) for row in frozen.get("bases", frozen.get("masks", []))}
    accepted = json.loads((root / "analysis/p4_mod8_live_landscape/results/top_band_masks.json").read_text())
    known_projections = set()
    for row in accepted["masks"]:
        if row["H8"] == 201:
            full = int.from_bytes(bytes.fromhex(row["mask_hex"]), "little")
            li, _ = live_authority()
            lp = project_live(full, li)
            known_projections.add(hashlib.sha256(lp.to_bytes(38, "little")).hexdigest())

    designs = {
        "A": materialize("DESIGN_A", choose_a(universe), registry, designed_classes, frozen_masks, known_projections),
        "B": materialize("DESIGN_B", choose_b(universe), registry, designed_classes, frozen_masks, known_projections),
        "C": materialize("DESIGN_C", choose_c(universe), registry, designed_classes, frozen_masks, known_projections),
    }
    for key, doc in designs.items():
        write_json(out / f"candidate_design_{key}.json", doc)
    summary = {
        "schema": "a303656-p4-live-candidate-comparison-v2",
        "designs": {k: {"digest": v["canonical_digest"], "hierarchy": v["hierarchy"], "distinct_integer_count": v["distinct_integer_count"], "minimum_integer": v["minimum_integer"], "maximum_integer": v["maximum_integer"]} for k, v in designs.items()},
        "selection_code_sha256": sha256_file(Path(__file__)),
    }
    write_json(out / "candidate_design_comparison.json", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
