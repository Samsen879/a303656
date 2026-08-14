#!/usr/bin/env python3
"""Build correction, prospective gate, and human reports from frozen authorities."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import digest, write_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    root, out = args.root.resolve(), args.output.resolve()
    registry = json.loads((out / "historical_exposure_registry.json").read_text())
    designs = {k: json.loads((out / f"candidate_design_{k}.json").read_text()) for k in "ABC"}
    correction = {
        "schema": "a303656-p4-mod8-promotion-semantics-correction-v1",
        "accepted_core_result_unchanged": {"D8": 107, "A8": 300, "H8_min": 32, "H8_max": 201, "argmax_tuple_count": 468, "lex_first_argmax": [2, 13, 50, 5], "distinct_maximizing_full_masks": 21, "distinct_maximizing_live_projections": 5},
        "source_commit_U": "ee5bef63b02277786fe9c01ae9ff44233d889883",
        "results_commit_V": "6efcf58e18714b100fa86c0646e1b9657e03c908",
        "old_promotion_gate": "FAIL",
        "corrections": {
            "468_fresh_classes": "468 design-novel classes relative to the frozen designed-class ledger",
            "21_new_masks": "21 design-novel full masks relative to the frozen/design mask ledger",
            "25345_fresh_integers": "integer count absent only from the registry version used by RESULTS V; not certified unseen under registry v2",
            "strict_historical_class_freshness": 0,
            "strict_historically_new_maximizing_masks": 0,
            "strict_historically_new_live_projections": 0,
        },
        "proof": {"inclusive_interval": [240000000001, 241600000000], "length": 1600000000, "L4": 1129118760, "covers_every_residue_class_mod_L4": True},
        "deprecated_terms": {"fresh_class": "forbidden unless explicit scope is supplied", "new_mask": "forbidden unless design ledger is named", "fresh_integer": "forbidden unless registry version and exposure predicate are named"},
        "audit_trail_policy": "RESULTS V is retained; this artifact supersedes only its promotion interpretation.",
    }
    correction["canonical_digest"] = digest(correction)
    write_json(out / "promotion_semantics_correction.json", correction)

    gates = {
        "V2.1_CORE_EXACT_RESULT": {"status": "PASS", "evidence": "H8_max=201 and accepted independent reproduction"},
        "V2.2_REGISTRY_INTEGRITY": {"status": "NOT_ESTABLISHED", "evidence": registry["unresolved_components"]},
        "V2.3_EXACT_INTEGER_NON_REUSE": {"status": "NOT_ESTABLISHED", "evidence": "candidate integers are absent from reconstructed registry, but any-recorded-evaluation completeness is NOT_ESTABLISHED"},
        "V2.4_T_BLIND_SELECTION": {"status": "PASS", "evidence": "selection source static forbidden-field audit and deterministic construction"},
        "V2.5_HIERARCHICAL_BALANCE": {"status": "PASS", "evidence": "all candidates encode H8→projection→mask→class→integer assignments"},
        "V2.6_CONTROLLED_COMPARISON": {"status": "PASS", "evidence": "A/B/C cover H8 in {199,200,201}; A/B raw G=227 and t3=2"},
        "V2.7_IMMUTABLE_PREREGISTRATION": {"status": "NOT_ESTABLISHED", "evidence": "candidate designs only; no final design selected or frozen for execution"},
        "V2.8_INDEPENDENT_AUDIT": {"status": "NOT_ESTABLISHED", "evidence": "pending web GPT-5.6 Pro audit"},
    }
    gate = {
        "schema": "a303656-p4-live-top-band-prospective-gate-v2",
        "gate_name": "P4_LIVE_TOP_BAND_PROSPECTIVE_GATE_V2",
        "overall_status": "NOT_ESTABLISHED",
        "old_promotion_gate": "FAIL",
        "gates": gates,
        "registry_digest": registry["canonical_digest"],
        "candidate_manifest_digests": {k: v["canonical_digest"] for k, v in designs.items()},
        "authorization": "NO_T_EVALUATION_AUTHORIZED",
        "global_problem_status": "UNRESOLVED",
    }
    gate["canonical_digest"] = digest(gate)
    write_json(out / "prospective_gate_v2.json", gate)

    lines = ["# Candidate design comparison", "", "All candidates are T-blind preregistration candidates only; none is authorized for evaluation.", "", "| Design | Integers | Per-band projections | Per-band masks | raw G | Main limitation |", "|---|---:|---|---|---|---|"]
    for k, d in designs.items():
        projs = "/".join(str(d["hierarchy"][str(h)]["live_projection_count"]) for h in (199,200,201))
        masks = "/".join(str(d["hierarchy"][str(h)]["full_mask_count"]) for h in (199,200,201))
        raw = "/".join(",".join(map(str,d["hierarchy"][str(h)]["raw_G_values"])) for h in (199,200,201))
        limit = "strict 384-point blueprint" if k == "A" else ("more raw-G-matched projection diversity; 288 points" if k == "B" else "all five H8=201 projections; residual raw-G/projection confounding")
        lines.append(f"| {k} | {d['distinct_integer_count']} | {projs} | {masks} | {raw} | {limit} |")
    lines += ["", "Design A follows the proposed 3×2×2×4×8 hierarchy exactly. Design B uses three projections per band, one mask per projection, four classes per mask, and eight integers per class. Design C uses five projections per band to include all five accepted H8=201 projections; it therefore cannot retain exact raw-G matching.", ""]
    (out / "candidate_design_comparison.md").write_text("\n".join(lines))

    report = f"""# Historical exposure registry repair and prospective gate v2

## Outcome

The accepted exact modular landscape is unchanged: `H8_max=201`, 468 maximizing tuples, 21 maximizing full masks, and five maximizing live projections. RESULTS V remains part of the audit trail.

The old promotion gate remains **FAIL**. Its 468 classes are design-novel relative to a designed-class ledger, not historically fresh. The inclusive 1.6B interval is longer than `L4`, so every fixed-P4 CRT class is historically exposed.

The version-2 historical registry is **PARTIAL** because interrupted-run touched-integer exposure cannot be reconstructed. Candidate integers are absent from the reconstructed registry, but both `integer_unseen_any_recorded_evaluation` and `integer_unseen_exact_T` remain **NOT ESTABLISHED** under the fail-closed completeness rule.

`P4_LIVE_TOP_BAND_PROSPECTIVE_GATE_V2`: **NOT ESTABLISHED**. Designs A, B, and C are technically deterministic candidate manifests, not an execution authorization. No new T values were inspected or computed.

Global A303656 status: **UNRESOLVED**.
"""
    (out / "REPORT.md").write_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
