#!/usr/bin/env python3
"""Run specified negative mutations and record the exact rejected error."""
from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path

from common import digest, write_json
from verifier import AuditError, verify_candidate, verify_registry, verify_selection_source


def expected(label, code, fn, rows):
    try:
        fn()
    except AuditError as exc:
        actual = str(exc)
        rows.append({"test": label, "expected_error": code, "actual_error": actual, "return_code": 1, "status": "PASS" if actual == code else "FAIL"})
        return
    rows.append({"test": label, "expected_error": code, "actual_error": None, "return_code": 0, "status": "FAIL"})


def redigest(doc):
    doc["canonical_digest"] = digest({k: v for k, v in doc.items() if k != "canonical_digest"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    registry = json.loads((a.results / "historical_exposure_registry.json").read_text())
    components = json.loads((a.results / "historical_exposure_components.json").read_text())
    candidate = json.loads((a.results / "candidate_design_A.json").read_text())
    rows = []

    r = copy.deepcopy(registry); r["fresh_class"] = 1; redigest(r)
    expected("design_novel_class_mislabeled_fresh_class", "UNSCOPED_FRESH_CLASS_TERM", lambda: verify_registry(r, components), rows)
    c = copy.deepcopy(components); c["components"].pop()
    expected("registry_component_missing", "REGISTRY_COMPONENT_SET_MISMATCH", lambda: verify_registry(registry, c), rows)
    r = copy.deepcopy(registry); r["historically_exposed_fixed_P4_classes"]["proof_interval"][1] -= 1; redigest(r)
    expected("interval_endpoint_off_by_one", "CONTINUOUS_INTERVAL_ENDPOINT_MISMATCH", lambda: verify_registry(r, components), rows)

    d = copy.deepcopy(candidate); d["class_rows"][0]["selected_integers"][1]["n"] = d["class_rows"][0]["selected_integers"][0]["n"]; redigest(d)
    expected("duplicate_integer", "DUPLICATE_INTEGER", lambda: verify_candidate(d, registry), rows)
    d = copy.deepcopy(candidate); d["class_rows"][0]["selected_integers"][0]["known_exposure_levels"] = ["E1_BINARY_REPRESENTABILITY_CHECK"]; redigest(d)
    expected("selected_integer_already_E1", "SELECTED_INTEGER_ALREADY_E1", lambda: verify_candidate(d, registry), rows)
    d = copy.deepcopy(candidate); d["class_rows"][0]["selected_integers"][0]["known_exposure_levels"] = ["E2_EXACT_T_COUNT"]; redigest(d)
    expected("selected_integer_already_E2", "SELECTED_INTEGER_ALREADY_E2", lambda: verify_candidate(d, registry), rows)
    for field, code, label in (("live_projection_count", "PROJECTION_BALANCE_MISMATCH", "projection_imbalance"), ("full_mask_count", "MASK_BALANCE_MISMATCH", "mask_imbalance"), ("CRT_class_count", "CLASS_BALANCE_MISMATCH", "class_imbalance")):
        d = copy.deepcopy(candidate); d["hierarchy"]["199"][field] += 1; redigest(d)
        expected(label, code, lambda d=d: verify_candidate(d, registry), rows)
    d = copy.deepcopy(candidate); d["minimum_integer"] -= 1
    expected("manifest_changed_after_freeze", "FROZEN_MANIFEST_CHANGED", lambda: verify_candidate(d, registry), rows)

    source = a.root / "analysis/p4_prospective_gate_v2/tools/build_candidates.py"
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "selection.py"; bad.write_text(source.read_text() + "\nvalue = row[\"T\"]\n")
        expected("selection_reads_forbidden_T_field", "FORBIDDEN_T_FIELD_READ", lambda: verify_selection_source(bad), rows)
        expected("selection_code_hash_changed", "SELECTION_CODE_HASH_CHANGED", lambda: verify_selection_source(source, "0" * 64), rows)
    d = copy.deepcopy(candidate); d["registry_digest"] = "0" * 64; redigest(d)
    expected("stale_registry_hash", "STALE_REGISTRY_HASH", lambda: verify_candidate(d, registry), rows)
    d = copy.deepcopy(candidate); d["collision_report"]["duplicate_integer_count"] = 1; redigest(d)
    expected("collision_deduplication_error", "COLLISION_DEDUPLICATION_MISMATCH", lambda: verify_candidate(d, registry), rows)
    d = copy.deepcopy(candidate); d["class_rows"][0]["tuple"][0] = 1; redigest(d)
    expected("non_deterministic_selection", "NONDETERMINISTIC_SELECTION", lambda: verify_candidate(d, registry), rows)

    result = {"schema": "a303656-p4-gate-v2-corruption-tests-v1", "test_count": len(rows), "all_passed": all(x["status"] == "PASS" and x["return_code"] != 0 for x in rows), "tests": rows}
    write_json(a.output, result)
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
