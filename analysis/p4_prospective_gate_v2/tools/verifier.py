#!/usr/bin/env python3
"""Fail-closed verifier with stable error identifiers for gate-v2 artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import digest, sha256_file

REQUIRED_COMPONENTS = {
    "FORMAL_CONTINUOUS_1P6B", "FORMAL_OTHER_DUAL_INTERVALS", "LEGACY_COMPLETE_PRIOR_REGISTRY_V1",
    "P4_CALIBRATION_AND_G231", "P4_WEIGHTED_FIXED_RUNS", "FIFTH_PRIME_MARGINAL",
    "P5_FAMILY_U_CENSUS", "P5_FAMILY_R", "P5_FAMILY_Q", "SPARSE_FEASIBILITY_RUNS", "LOW_T_RECORDS",
    "INTERRUPTED_PARTIAL_ABANDONED", "REPLAY_AND_COLLISION_RECORDS",
}
FORBIDDEN_SELECTION_PATTERNS = ('["T"]', "['T']", 'low_T', 'winner_mask', 'candidate_outcome', 'empirical_winner')


class AuditError(ValueError):
    pass


def fail(code: str) -> None:
    raise AuditError(code)


def verify_registry(registry: dict, components: dict) -> None:
    if any("fresh_class" in str(k) for k in registry):
        fail("UNSCOPED_FRESH_CLASS_TERM")
    ids = {x["component_id"] for x in components["components"]}
    if ids != REQUIRED_COMPONENTS:
        fail("REGISTRY_COMPONENT_SET_MISMATCH")
    proof = registry["historically_exposed_fixed_P4_classes"]
    if proof["proof_interval"] != [240000000001, 241600000000] or proof["proof_interval_length"] != 1600000000:
        fail("CONTINUOUS_INTERVAL_ENDPOINT_MISMATCH")
    body = {k: v for k, v in registry.items() if k != "canonical_digest"}
    if registry["canonical_digest"] != digest(body):
        fail("REGISTRY_DIGEST_MISMATCH")


def verify_candidate(doc: dict, registry: dict) -> None:
    if doc["registry_digest"] != registry["canonical_digest"]:
        fail("STALE_REGISTRY_HASH")
    if doc.get("selection_T_blind") is not True:
        fail("SELECTION_NOT_T_BLIND")
    selected = []
    for row in doc["class_rows"]:
        for item in row["selected_integers"]:
            if "E1_BINARY_REPRESENTABILITY_CHECK" in item["known_exposure_levels"]:
                fail("SELECTED_INTEGER_ALREADY_E1")
            if "E2_EXACT_T_COUNT" in item["known_exposure_levels"]:
                fail("SELECTED_INTEGER_ALREADY_E2")
            selected.append(item["n"])
    if len(selected) != len(set(selected)):
        fail("DUPLICATE_INTEGER")
    if doc["collision_report"]["duplicate_integer_count"] != 0 or doc["distinct_integer_count"] != len(set(selected)):
        fail("COLLISION_DEDUPLICATION_MISMATCH")
    for h in (199, 200, 201):
        rows = [r for r in doc["class_rows"] if r["H8"] == h]
        got = doc["hierarchy"][str(h)]
        if got["live_projection_count"] != len({r["live_projection_digest"] for r in rows}):
            fail("PROJECTION_BALANCE_MISMATCH")
        if got["full_mask_count"] != len({r["full_mask_digest"] for r in rows}):
            fail("MASK_BALANCE_MISMATCH")
        if got["CRT_class_count"] != len(rows) or got["integer_count"] != sum(len(r["selected_integers"]) for r in rows):
            fail("CLASS_BALANCE_MISMATCH")
    tuples = [tuple(r["tuple"]) for r in doc["class_rows"]]
    if any(t[0] != 2 for t in tuples):
        fail("NONDETERMINISTIC_SELECTION")
    body = {k: v for k, v in doc.items() if k != "canonical_digest"}
    if doc["canonical_digest"] != digest(body):
        fail("FROZEN_MANIFEST_CHANGED")


def verify_selection_source(path: Path, expected_sha: str | None = None) -> None:
    text = path.read_text()
    if any(pattern in text for pattern in FORBIDDEN_SELECTION_PATTERNS):
        fail("FORBIDDEN_T_FIELD_READ")
    if expected_sha is not None and sha256_file(path) != expected_sha:
        fail("SELECTION_CODE_HASH_CHANGED")


def verify_results(root: Path, result_dir: Path) -> None:
    registry = json.loads((result_dir / "historical_exposure_registry.json").read_text())
    components = json.loads((result_dir / "historical_exposure_components.json").read_text())
    verify_registry(registry, components)
    for key in "ABC":
        verify_candidate(json.loads((result_dir / f"candidate_design_{key}.json").read_text()), registry)
    verify_selection_source(root / "analysis/p4_prospective_gate_v2/tools/build_candidates.py")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--results", type=Path, required=True)
    args = ap.parse_args()
    try:
        verify_results(args.root.resolve(), args.results.resolve())
    except AuditError as exc:
        print(str(exc))
        return 1
    print("VERIFIED_P4_LIVE_TOP_BAND_PROSPECTIVE_GATE_V2_ARTIFACTS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
