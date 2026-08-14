#!/usr/bin/env python3
"""Independent semantic verifier for recovered exposure and Design A."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent / "tools"
sys.path.insert(0, str(TOOLS))
from common import L4, MODS, class_members, fixed_p4_class, live_authority, pair_domain, prime_masks, project_live  # noqa:E402
from common_v2 import GATES, LEVELS, digest, normalize, sha256_file  # noqa:E402


class SemanticError(ValueError):
    def __init__(self, code: str, category: str):
        super().__init__(code)
        self.code, self.category = code, category


def fail(code: str, category: str) -> None:
    raise SemanticError(code, category)


def require(ok: bool, code: str, category: str) -> None:
    if not ok:
        fail(code, category)


def closed(doc: dict, code: str = "CANONICAL_DIGEST_MISMATCH") -> None:
    require(doc.get("canonical_digest") == digest({k: v for k, v in doc.items() if k != "canonical_digest"}), code, "hash_closure")


def levels_for(n: int, registry: dict, include_possible: bool = False) -> set[str]:
    levels: set[str] = set()
    for row in registry["interval_records"]:
        if row["certainty"] == "CONFIRMED" and row["normalized_low"] <= n <= row["normalized_high"]:
            levels.update(row["exposure_levels"])
        if include_possible and row["certainty"] in ("CONSERVATIVE_SUPERSET", "UNKNOWN"):
            low, high = row.get("normalized_low"), row.get("normalized_high")
            if low is None or (low <= n <= high):
                levels.update(row["exposure_levels"])
    for row in registry["integer_records"]:
        if int(row["n"]) == n and (row["certainty"] == "CONFIRMED" or include_possible):
            levels.update(row["exposure_levels"])
    return levels


def verify_registry(registry: dict, components: dict, manifest: dict) -> None:
    closed(registry, "REGISTRY_DIGEST_MISMATCH")
    closed(components, "COMPONENT_DIGEST_MISMATCH")
    closed(manifest, "REGISTRY_MANIFEST_DIGEST_MISMATCH")
    require(registry.get("status") == "PARTIAL", "REGISTRY_MUST_REMAIN_PARTIAL", "provenance_completeness")
    rows = registry.get("interval_records", [])
    require(len([r for r in rows if r["certainty"] == "CONFIRMED"]) == 28, "INTERVAL_COUNT_28_REQUIRED", "interval_semantics")
    for row in rows:
        require(row.get("boundary_convention") in ("closed", "unknown"), "ENDPOINT_CONVENTION_MISSING", "interval_semantics")
        if row["boundary_convention"] == "closed":
            require(row["inclusive_length"] == row["normalized_high"] - row["normalized_low"] + 1, "INCLUSIVE_LENGTH_MISMATCH", "interval_semantics")
    confirmed = [(r["normalized_low"], r["normalized_high"]) for r in rows if r["certainty"] == "CONFIRMED"]
    require(normalize(confirmed) == confirmed, "INTERVAL_UNION_NOT_NORMALIZED", "interval_semantics")
    require(registry["reconciliation_27_28"]["correct_count"] == 28, "RECONCILIATION_27_28_MISSING", "registry_consistency")
    require(registry["reconciliation_253m_533p2m"]["direct_other_metric"] == 253_000_000, "DIRECT_253M_DEFINITION_MISSING", "registry_consistency")
    require(registry["reconciliation_253m_533p2m"]["registry_other_union_metric"] == 533_200_000, "REGISTRY_533P2M_DEFINITION_MISSING", "registry_consistency")
    ids = {x["source_id"] for x in components["components"]}
    require({"K4_PROGRESSION_PANEL", "K4_DIRECT_VERIFICATION", "P4_DIRECT_VERIFICATION"} <= ids, "ORPHAN_SOURCE_UNRESOLVED", "source_provenance")
    for row in components["components"]:
        require(row["status"] in ("COMPLETE", "PARTIAL", "MISSING", "NOT_APPLICABLE", "NOT_ESTABLISHED"), "INVALID_COMPONENT_STATUS", "schema")
        require(row.get("boundary_convention") != "not_applicable", "ENDPOINT_NOT_APPLICABLE_FORBIDDEN", "interval_semantics")
        if row["status"] == "COMPLETE" and row.get("path"):
            require(row.get("sha256") not in (None, "", "NOT_ESTABLISHED"), "COMPLETE_SOURCE_HASH_MISSING", "source_provenance")
    required = manifest.get("expected_hashes", {})
    for name in ("builder_source", "registry", "candidate_universe", "authorities", "final_manifest", "analysis_plan"):
        require(isinstance(required.get(name), str) and len(required[name]) == 64, "EXPECTED_SOURCE_HASH_MISSING", "hash_closure")


SENSITIVE = {"t", "low_t", "winner_mask", "winner_masks", "candidate_outcome", "empirical_winner", "outcome", "outcomes"}


class BlindnessVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.constants: dict[str, str] = {}
        self.tainted: set[str] = set()
        self.violations: list[dict] = []

    def bad(self, node: ast.AST, reason: str) -> None:
        self.violations.append({"line": getattr(node, "lineno", 0), "reason": reason})

    def key(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name):
            return self.constants.get(node.id)
        return None

    def visit_Assign(self, node: ast.Assign) -> None:
        value = self.key(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name) and value is not None:
                self.constants[target.id] = value
                if value.lower() in SENSITIVE:
                    self.tainted.add(target.id)
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Name) and node.value.id in self.tainted:
                self.tainted.add(target.id)
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        key = self.key(node.slice)
        if key and key.lower() in SENSITIVE:
            self.bad(node, f"sensitive subscript {key}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute) and node.func.attr == "get" and node.args:
            key = self.key(node.args[0])
            if key and key.lower() in SENSITIVE:
                self.bad(node, f"sensitive get {key}")
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and any(s in arg.value.lower() for s in ("low_t", "winner_mask", "outcome")):
                self.bad(node, "outcome-conditioned imported data")
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        for key, value in zip(node.keys, node.values):
            if key is None and isinstance(value, ast.Name) and value.id in self.tainted:
                self.bad(node, "tainted dictionary unpack")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load) and node.id.lower() in SENSITIVE:
            self.bad(node, f"sensitive identifier {node.id}")


def audit_selection_source(path: Path, expected_sha: str | None) -> dict:
    require(isinstance(expected_sha, str) and len(expected_sha) == 64, "EXPECTED_SOURCE_HASH_MISSING", "hash_closure")
    require(sha256_file(path) == expected_sha, "SELECTION_SOURCE_HASH_MISMATCH", "hash_closure")
    visitor = BlindnessVisitor()
    try:
        visitor.visit(ast.parse(path.read_text()))
    except SyntaxError:
        fail("SELECTION_SOURCE_AST_INVALID", "selection_blindness")
    require(not visitor.violations, "FORBIDDEN_OUTCOME_DATAFLOW", "selection_blindness")
    return {"status": "PASS", "check_id": "SEM-STATIC-OUTCOME-001", "source_sha256": expected_sha, "violations": []}


@lru_cache(maxsize=1)
def mask_authority() -> tuple[list[list[int]], list[int], int]:
    pairs = pair_domain()
    masks = [prime_masks(pairs, p) for p in (3, 7, 11, 23)]
    live_indices, live_mask = live_authority()
    return masks, live_indices, live_mask


def reconstruct_mask(row: dict) -> tuple[int, str, str, int, int]:
    masks, live_indices, live_mask = mask_authority()
    tup = tuple(int(x) for x in row["tuple"])
    require(all(0 <= tup[i] < MODS[i] for i in range(4)), "CRT_TUPLE_NOT_NORMALIZED", "arithmetic")
    full = masks[0][tup[0]] | masks[1][tup[1]] | masks[2][tup[2]] | masks[3][tup[3]]
    full_digest = hashlib.sha256(full.to_bytes(51, "little")).hexdigest()
    live = project_live(full, live_indices)
    live_digest = hashlib.sha256(live.to_bytes(38, "little")).hexdigest()
    return full, full_digest, live_digest, (full & live_mask).bit_count(), full.bit_count()


def verify_candidate(candidate: dict, registry: dict, expected_prior_sha: str) -> dict:
    require(candidate.get("prior_design_A_file_sha256") == expected_prior_sha, "PRIOR_DESIGN_HASH_MISMATCH", "hash_closure")
    require(candidate.get("authorization") is False and candidate.get("preregistration_level") == 1, "UNAUTHORIZED_CANDIDATE", "authorization")
    require(candidate.get("selection_T_blind") is True, "SELECTION_BLINDNESS_DECLARATION_MISSING", "selection_blindness")
    selected: list[int] = []
    rebuilt: dict[str, dict] = {}
    for row in candidate["class_rows"]:
        full, fd, pd, h8, raw_g = reconstruct_mask(row)
        require(fd == row["full_mask_digest"], "FULL_MASK_DIGEST_MISMATCH", "arithmetic")
        require(pd == row["live_projection_digest"], "LIVE_PROJECTION_DIGEST_MISMATCH", "arithmetic")
        require(h8 == row["H8"], "H8_MISMATCH", "arithmetic")
        require(raw_g == row["raw_G"], "RAW_G_MISMATCH", "arithmetic")
        require(fixed_p4_class(tuple(row["tuple"])) == row["class_residue_mod_L4"], "CRT_CLASS_MISMATCH", "arithmetic")
        members = class_members(row["class_residue_mod_L4"])
        eligible = [n for n in members if not levels_for(n, registry)]
        require(row["activation_cell_member_count"] == len(members), "CLASS_MULTIPLICITY_MISMATCH", "arithmetic")
        for item in row["selected_integers"]:
            idx, n = int(item["selection_index"]), int(item["n"])
            require(not levels_for(n, registry), "AUTHORITATIVE_EXPOSURE_MEMBERSHIP", "exposure")
            require(0 <= idx < len(eligible), "SELECTION_INDEX_RANGE", "selection")
            require(eligible[idx] == n, "SELECTION_INDEX_IDENTITY", "selection")
            require(item.get("known_exposure_levels") == [], "SELF_REPORTED_EXPOSURE_NOT_AUTHORITY", "exposure")
            selected.append(n)
        key = str(row["H8"])
        entry = rebuilt.setdefault(key, {"projections": set(), "masks": set(), "classes": 0, "integers": 0, "raw_G_values": set()})
        entry["projections"].add(pd); entry["masks"].add(fd); entry["classes"] += 1
        entry["integers"] += len(row["selected_integers"]); entry["raw_G_values"].add(raw_g)
    require(len(selected) == len(set(selected)), "DUPLICATE_INTEGER", "collision")
    require(candidate["distinct_integer_count"] == len(set(selected)), "DISTINCT_INTEGER_COUNT_MISMATCH", "collision")
    require(candidate["minimum_integer"] == min(selected) and candidate["maximum_integer"] == max(selected), "MIN_MAX_RECONSTRUCTION_MISMATCH", "selection")
    for h in (199, 200, 201):
        x, declared = rebuilt[str(h)], candidate["hierarchy"][str(h)]
        actual = {"live_projection_count": len(x["projections"]), "full_mask_count": len(x["masks"]), "CRT_class_count": x["classes"], "integer_count": x["integers"], "raw_G_values": sorted(x["raw_G_values"])}
        require(actual == declared, "HIERARCHY_RECONSTRUCTION_MISMATCH", "hierarchy")
        require(actual["live_projection_count"] == 2 and actual["full_mask_count"] == 4 and actual["CRT_class_count"] == 16 and actual["integer_count"] == 128, "DESIGN_A_BALANCE_MISMATCH", "hierarchy")
    closed(candidate, "CANDIDATE_CANONICAL_DIGEST_MISMATCH")
    return {"status": "PASS", "integer_count": len(selected), "duplicate_integer_count": 0}


def verify_gate(gate: dict) -> None:
    require(list(gate["items"]) == list(GATES), "NINE_GATE_ORDER_MISMATCH", "gate_schema")
    statuses = [gate["items"][name]["status"] for name in GATES]
    require(all(x in ("PASS", "FAIL", "NOT_ESTABLISHED") for x in statuses), "INVALID_GATE_STATUS", "gate_schema")
    expected = "FAIL" if "FAIL" in statuses else "NOT_ESTABLISHED" if "NOT_ESTABLISHED" in statuses else "PASS"
    require(gate["overall_status"] == expected, "OVERALL_GATE_RULE_MISMATCH", "gate_schema")
    require(gate["items"]["V2.9_INDEPENDENT_AUTHORIZATION"]["status"] == "NOT_ESTABLISHED", "V2_9_MUST_REMAIN_NOT_ESTABLISHED", "authorization")
    closed(gate, "GATE_DIGEST_MISMATCH")


def verify_all(root: Path, out: Path) -> dict:
    registry = json.loads((out / "historical_exposure_registry_v2.json").read_text())
    components = json.loads((out / "historical_exposure_components_v2.json").read_text())
    manifest = json.loads((out / "historical_exposure_manifest_v2.json").read_text())
    candidate = json.loads((out / "design_A_preregistration_candidate_v2.json").read_text())
    gate = json.loads((out / "prospective_gate_v2_nine_item.json").read_text())
    verify_registry(registry, components, manifest)
    selection = audit_selection_source(root / manifest["selection_source_path"], manifest["expected_hashes"]["builder_source"])
    verify_candidate(candidate, registry, manifest["prior_design_A_file_sha256"])
    verify_gate(gate)
    return {"status": "PASS", "checks": ["registry", "hash_closure", "selection_AST", "candidate_arithmetic", "hierarchy", "gate_schema"], "selection_audit": selection}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); ap.add_argument("--results", type=Path, required=True)
    args = ap.parse_args()
    try:
        report = verify_all(args.root.resolve(), args.results.resolve())
    except SemanticError as exc:
        print(json.dumps({"status": "FAIL", "code": exc.code, "category": exc.category}))
        raise SystemExit(1)
    print(json.dumps(report, sort_keys=True))
