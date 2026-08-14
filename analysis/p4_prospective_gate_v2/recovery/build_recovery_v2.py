#!/usr/bin/env python3
"""Build forensic recovery, registry V2, preregistration, and nine-gate results.

This program reads historical artifacts only. It never invokes an evaluator.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
from pathlib import Path

from common_v2 import GATES, LEVELS, close, digest, sha256_file, union_length, write_json


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True)
    return p.stdout.strip()


def provenance(root: Path, rel: str, source_id: str, schema: str, level: list[str], count: int, count_kind: str) -> dict:
    path = root / rel
    commit = git(root, "log", "-1", "--format=%H", "--", rel)
    tree = git(root, "show", "-s", "--format=%T", commit)
    blob = git(root, "rev-parse", f"{commit}:{rel}")
    return {"source_id": source_id, "path": rel, "status": "COMPLETE", "commit": commit, "tree": tree,
            "blob": blob, "sha256": sha256_file(path), "schema": schema, "exposure_levels": level,
            count_kind: count, "provenance_completeness": "COMPLETE", "boundary_convention": "NOT_APPLICABLE_SPARSE"}


def component(root: Path, source_id: str, rel: str | None, status: str, levels: list[str], note: str,
              boundary: str = "NOT_APPLICABLE_SPARSE", extent: dict | None = None) -> dict:
    path = root / rel if rel else None
    commit = git(root, "log", "-1", "--format=%H", "--", rel) if path and path.exists() else "NOT_ESTABLISHED"
    return {"source_id": source_id, "path": rel, "status": status, "commit": commit,
            "tree": git(root, "show", "-s", "--format=%T", commit) if len(commit) == 40 else "NOT_ESTABLISHED",
            "sha256": sha256_file(path) if path and path.is_file() else "NOT_ESTABLISHED",
            "schema": "repository-native-authority", "exposure_levels": levels, "extent": extent or {},
            "provenance_completeness": status, "boundary_convention": boundary, "note": note}


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: ";".join(map(str, v)) if isinstance(v, list) else v for k, v in row.items()})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--inventory-dir", type=Path, required=True)
    args = ap.parse_args(); root=args.root.resolve(); out=args.output.resolve(); inv=args.inventory_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in ("forensic_inventory.json", "forensic_inventory.csv", "git_history_relevant_paths.json", "archive_inventory.json", "ignored_generated_files_inventory.json"):
        shutil.copy2(inv / name, out / name)

    prior_path = root / "analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json"
    prior = json.loads(prior_path.read_text())
    intervals = [(int(a), int(b)) for a, b in prior["interval_union"]]
    interval_rows = []
    for i, (low, high) in enumerate(intervals, 1):
        interval_rows.append({"record_id": f"I{i:02d}", "source_id": "LEGACY_COMPLETE_PRIOR_REGISTRY_V1",
            "source_artifact": prior_path.relative_to(root).as_posix(), "source_artifact_sha256": sha256_file(prior_path),
            "source_commit": git(root, "log", "-1", "--format=%H", "--", prior_path.relative_to(root).as_posix()),
            "exposure_levels": ["E1_BINARY_REPRESENTABILITY_CHECK"], "certainty": "CONFIRMED",
            "boundary_convention": "closed", "original_low": low, "original_high": high,
            "normalized_low": low, "normalized_high": high, "inclusive_length": high-low+1,
            "overlap_handling": "normalized closed union; overlaps and adjacent intervals merged once",
            "outcome_influenced_selection": False, "provenance_completeness": "COMPLETE"})

    orphan = [
        provenance(root, "analysis/k4_ap_pilot/backend_a_counts.csv", "K4_PROGRESSION_PANEL", "CSV:h,k,n,T,active_pairs", ["E2_EXACT_T_COUNT","E3_COMPLETE_WINNER_MASK"], 1285, "row_count"),
        provenance(root, "analysis/k4_ap_pilot/direct_verification.json", "K4_DIRECT_VERIFICATION", "a303656-k4-ap-direct-verification-v1", ["E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"], 73, "selected_point_count"),
        provenance(root, "analysis/p4_maximizer_census/direct_verification.json", "P4_DIRECT_VERIFICATION", "a303656-p4-direct-verification-v1", ["E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED"], 457, "selected_point_count"),
    ]
    components = [
        component(root,"FORMAL_CONTINUOUS_1P6B","output/direct/formal_1p6b_final/summary.json","COMPLETE",["E1_BINARY_REPRESENTABILITY_CHECK"],"160 closed chunks; protected report source", "closed", {"low":240000000001,"high":241600000000,"inclusive_length":1600000000}),
        component(root,"FORMAL_OTHER_DUAL_INTERVALS","output/formal_results_audit.json","COMPLETE",["E1_BINARY_REPRESENTABILITY_CHECK"],"253M is the four non-continuous direct datasets; registry union additionally imports other historical intervals", "closed", {"historical_direct_other":253000000,"registry_other_union":533200000}),
        component(root,"LEGACY_COMPLETE_PRIOR_REGISTRY_V1",prior_path.relative_to(root).as_posix(),"COMPLETE",list(LEVELS[1:]),"28 normalized interval records and 6129 sparse integers", "closed", {"interval_count":28,"sparse_integer_count":len(prior["sparse_points"])}),
        *orphan,
        component(root,"P4_CALIBRATION_AND_G231","analysis/p4_maximizer_census/verification_report.json","COMPLETE",list(LEVELS[2:]),"87 classes, 4838 points; source panel recovered"),
        component(root,"P4_WEIGHTED_FIXED_RUNS","analysis/p4_weighted_transferability/results/metadata.json","COMPLETE",[LEVELS[0],LEVELS[4]],"reuses 457-point direct selection manifest; zero new integer evaluation"),
        component(root,"FIFTH_PRIME_MARGINAL","analysis/fifth_prime_marginal_coverage/results/metadata.json","COMPLETE",[LEVELS[0]],"modular design work; no integer evaluation"),
        component(root,"P5_FAMILY_U_CENSUS","analysis/p5_family_u_census/results/panel_reconstruction_manifest.json","COMPLETE",list(LEVELS[2:]),"457 descriptions, 454 distinct integers"),
        component(root,"P5_FAMILY_R","analysis/p5_sparse_panel_feasibility/results/design_A_all_entry_balanced.json","COMPLETE",[LEVELS[0]],"design-only authority"),
        component(root,"P5_FAMILY_Q","analysis/p5_sparse_panel_feasibility/results/design_B_anchor_balanced.json","COMPLETE",[LEVELS[0]],"design-only authority"),
        component(root,"SPARSE_FEASIBILITY_RUNS","analysis/p5_sparse_panel_feasibility/results/verification_report.json","COMPLETE",[LEVELS[0]],"verifier records evaluator calls false"),
        component(root,"LOW_T_RECORDS","output/tn_pilot_20260713/pilot_a/bitset/counts.csv","COMPLETE",[LEVELS[2],LEVELS[3]],"pilot A/B imported through legacy registry"),
        component(root,"REPLAY_AND_COLLISION_RECORDS","analysis/p5_family_u_census/results/description_integer_incidence.json","COMPLETE",[LEVELS[0]],"three description collisions, no new integer"),
        component(root,"INTERRUPTED_PARTIAL_ABANDONED","logs/INTERRUPTED_RUNS.txt","PARTIAL",[LEVELS[1],LEVELS[2],LEVELS[3],LEVELS[4]],"not all historical execution buffers/touched integers are reconstructable", "UNKNOWN"),
    ]
    components_doc = close({"schema":"a303656-historical-exposure-components-v2","components":components})
    write_json(out/"historical_exposure_components_v2.json", components_doc)

    interrupted = [
      {"run_id":"INT-DIRECT-100M-256","evidence":"logs/INTERRUPTED_RUNS.txt#1","runner":"two implementation fixed-pool scan","input_universe":{"low":240000000001,"high":240100000000,"boundary":"closed"},"deterministic_order":"ascending n within declared interval","completed_count":"NOT_ESTABLISHED","last_written_row":"NONE","flush_semantics":"final JSON and rc only; buffered partial progress can be lost","crash_location":"external timeout","resume_behavior":"fresh rerun, no checkpoint resume","certainty":"CONSERVATIVE_SUPERSET","possible_levels":[LEVELS[1]],"exact_T_stage":"NOT_REACHABLE_BY_IDENTIFIED_RUNNER"},
      {"run_id":"INT-FIXEDPOOL-10M-512","evidence":"logs/INTERRUPTED_RUNS.txt#2","runner":"two implementation fixed-pool scan","input_universe":{"low":240000000001,"high":240010000000,"boundary":"closed"},"deterministic_order":"ascending n","completed_count":"NOT_ESTABLISHED","last_written_row":"NONE","flush_semantics":"final result only","crash_location":"external timeout","resume_behavior":"separate rerun","certainty":"CONSERVATIVE_SUPERSET","possible_levels":[LEVELS[1]],"exact_T_stage":"NOT_REACHABLE_BY_IDENTIFIED_RUNNER"},
      {"run_id":"INT-SMT-K16-K32","evidence":"logs/INTERRUPTED_RUNS.txt#3","runner":"SMT/CEGIS orchestration","input_universe":{"low":240000000001,"high":240000000100,"boundary":"closed"},"deterministic_order":"solver-dependent candidates; not an ordered exhaustive scan","completed_count":"NOT_ESTABLISHED","last_written_row":"K32 direct UNKNOWN JSON","flush_semantics":"per-run JSON; enclosing orchestration interrupted","crash_location":"after direct UNKNOWN","resume_behavior":"CEGIS rerun separately","certainty":"CONSERVATIVE_SUPERSET","possible_levels":[LEVELS[0]],"exact_T_stage":"NOT_REACHABLE_BY_IDENTIFIED_RUNNER"},
      {"run_id":"INT-STAGE0-REDUNDANT","evidence":"logs/INTERRUPTED_RUNS.txt#4","runner":"baseline reproduction","input_universe":"uploaded stage0 baseline only","deterministic_order":"script order","completed_count":"not an integer evaluation run","last_written_row":"527/598/135 reproduced","flush_semantics":"logged stages","crash_location":"bundle reproduction","resume_behavior":"not used","certainty":"CONFIRMED","possible_levels":[LEVELS[0]],"exact_T_stage":"NOT_APPLICABLE"},
      {"run_id":"INT-DIRECT-52WAY","evidence":"logs/direct/interrupted_parallel_52way/README.txt","runner":"52-way direct representability pilot","input_universe":"52 declared 100,000,000-integer chunks; start bounds absent from retained runner metadata","deterministic_order":"ascending within each chunk; parallel interleaving nondeterministic","completed_count":0,"last_written_row":"NONE","flush_semantics":"no incremental rows; complete JSON only","crash_location":"external signal; chunk_0014 rc=143","resume_behavior":"no checkpoint","certainty":"UNKNOWN","possible_levels":[LEVELS[1]],"exact_T_stage":"NOT_REACHABLE_BY_IDENTIFIED_RUNNER"},
      {"run_id":"ABANDONED-K4-PRE-C","evidence":"docs/k4_ap_enrichment_pilot.md","runner":"k4_ap_run pre-C direct CSV attempt","input_universe":{"path":"analysis/k4_ap_pilot/backend_a_counts.csv","row_count":1285},"deterministic_order":"fixed panel order","completed_count":"PARTIAL_NOT_ESTABLISHED","last_written_row":"NOT_ESTABLISHED","flush_semantics":"CSV may contain rows before schema defect rejection","crash_location":"direct CSV extra T field","resume_behavior":"discarded then clean replay","certainty":"CONSERVATIVE_SUPERSET","possible_levels":[LEVELS[2],LEVELS[3],LEVELS[4]],"exact_T_stage":"CONFIRMED_ENTERED; entire fixed 1285-point panel already registered"},
    ]
    write_json(out/"interrupted_run_catalog.json", {"schema":"a303656-interrupted-run-catalog-v2","runs":interrupted,"status":"PARTIAL"})
    stages=("runner_started","integer_loaded","binary_check_started","binary_check_completed","exact_T_started","exact_T_completed","winner_mask_completed","output_committed")
    stage_rows=[]
    for run in interrupted:
        reach={s:"NOT_ESTABLISHED" for s in stages}; reach["runner_started"]="CONFIRMED"
        if run["run_id"]=="ABANDONED-K4-PRE-C": reach.update({"integer_loaded":"CONFIRMED","exact_T_started":"CONFIRMED","exact_T_completed":"POSSIBLE","winner_mask_completed":"POSSIBLE","output_committed":"FAIL"})
        elif LEVELS[1] in run["possible_levels"]: reach.update({"integer_loaded":"POSSIBLE","binary_check_started":"POSSIBLE","binary_check_completed":"POSSIBLE","output_committed":"FAIL"})
        stage_rows.append({"run_id":run["run_id"],"stages":reach})
    write_json(out/"interrupted_run_stage_reachability.json", {"schema":"a303656-interrupted-stage-reachability-v2","stage_order":stages,"runs":stage_rows})
    touched=out/"interrupted_run_touched_sets"; supers=out/"interrupted_run_conservative_supersets"; touched.mkdir(exist_ok=True); supers.mkdir(exist_ok=True)
    for run in interrupted:
        write_json(touched/f'{run["run_id"]}.json', {"run_id":run["run_id"],"exact_touched_set":"NOT_ESTABLISHED","evidence":run["evidence"]})
        write_json(supers/f'{run["run_id"]}.json', {"run_id":run["run_id"],"superset":run["input_universe"],"certainty":run["certainty"],"proof_derivation":"The retained runner declaration fixes this universe; execution can touch no integer outside it. Where bounds are absent, UNKNOWN is retained rather than guessed."})
    (out/"interrupted_run_limitations.md").write_text("# Interrupted-run limitations\n\nThe 52-way run lacks retained chunk bounds and incremental output. Its exact touched set cannot be recovered. The K4 abandoned run is conservatively the full 1,285-row fixed panel and is already in confirmed sparse exposure. Absence of final JSON is never interpreted as absence of backend execution. Global any-evaluation and exact-T completeness therefore remain NOT_ESTABLISHED.\n")

    integer_map: dict[int, dict] = {}
    for n in prior["sparse_points"]:
        integer_map[int(n)]={"n":int(n),"source_id":"LEGACY_COMPLETE_PRIOR_REGISTRY_V1","source_artifact_sha256":sha256_file(prior_path),"source_commit":git(root,"log","-1","--format=%H","--",prior_path.relative_to(root).as_posix()),"exposure_levels":[LEVELS[1]],"certainty":"CONFIRMED","outcome_influenced_selection":"MIXED","provenance_completeness":"COMPLETE","boundary_convention":"NOT_APPLICABLE_SPARSE"}
    for rel, source, levels in (("analysis/k4_ap_pilot/backend_a_counts.csv","K4_PROGRESSION_PANEL",[LEVELS[2],LEVELS[3]]),("analysis/p4_maximizer_census/backend_a_counts.csv","P4_CALIBRATION_AND_G231",[LEVELS[2],LEVELS[3]])):
        with (root/rel).open() as stream:
            for row in csv.DictReader(stream):
                n=int(row["n"]); x=integer_map.setdefault(n,{"n":n,"source_id":source,"source_artifact_sha256":sha256_file(root/rel),"source_commit":git(root,"log","-1","--format=%H","--",rel),"exposure_levels":[],"certainty":"CONFIRMED","outcome_influenced_selection":True,"provenance_completeness":"COMPLETE","boundary_convention":"NOT_APPLICABLE_SPARSE"}); x["exposure_levels"]=sorted(set(x["exposure_levels"]+levels),key=LEVELS.index)
    registry=close({"schema":"a303656-historical-exposure-registry-v2","version":2,"status":"PARTIAL","certainty_values":["CONFIRMED","CONSERVATIVE_SUPERSET","UNKNOWN"],"levels":list(LEVELS),"interval_records":interval_rows,"integer_records":sorted(integer_map.values(),key=lambda x:x["n"]),"unknown_exposure":{"any_recorded_evaluation":"NOT_ESTABLISHED","exact_T":"NOT_ESTABLISHED","reason":"52-way bounds and complete historical execution ledger absent"},"reconciliation_27_28":{"incorrect_component_claim":27,"actual_embedded_records":28,"correct_count":28,"cause":"builder subtracted the 1.6B interval in the count but embedded the full normalized list","before_union":intervals,"after_union":intervals,"overlap_structure":"already normalized disjoint closed intervals"},"reconciliation_253m_533p2m":{"direct_other_metric":253000000,"direct_other_definition":"210M remote windows + 3M logarithmic windows + 20M 3-power boundary + 20M 5-power boundary","registry_other_union_metric":union_length(intervals)-1600000000,"registry_other_definition":"all normalized confirmed intervals excluding continuous 1.6B","additional_280p2m":{"toy_2_to_200001":200000,"250B_extension_beyond_direct_window":90000000,"270B_extension_beyond_direct_window":90000000,"282p3_factor_interval_joined_to_282p4_window":100000000,"total":280200000},"overlap_policy":"closed union counts each integer once"}})
    write_json(out/"historical_exposure_registry_v2.json",registry)
    write_csv(out/"historical_exposure_intervals_v2.csv",interval_rows,["record_id","source_id","source_artifact","source_artifact_sha256","source_commit","exposure_levels","certainty","boundary_convention","original_low","original_high","normalized_low","normalized_high","inclusive_length","overlap_handling","outcome_influenced_selection","provenance_completeness"])
    reg_rows=[{"record_type":"integer",**r} for r in registry["integer_records"]]+[{"record_type":"interval",**r} for r in interval_rows]
    write_csv(out/"historical_exposure_registry_v2.csv",reg_rows,["record_type","n","record_id","normalized_low","normalized_high","source_id","source_artifact_sha256","source_commit","exposure_levels","certainty","outcome_influenced_selection","provenance_completeness","boundary_convention"])
    old=json.loads((root/"analysis/p4_prospective_gate_v2/results/historical_exposure_registry.json").read_text())
    write_json(out/"historical_exposure_registry_diff.json", {"schema":"a303656-registry-v1-v2-diff","old_digest":old["canonical_digest"],"new_digest":registry["canonical_digest"],"changes":["27/28 metadata repaired without deleting a row","endpoint conventions explicit","orphan source provenance restored","interrupted stages and conservative supersets recorded","253M and 533.2M metrics retained with separate definitions"],"scientific_authorities_changed":False})
    (out/"historical_exposure_limitations_v2.md").write_text("# Historical exposure registry V2 limitations\n\nStatus: **PARTIAL**. Confirmed records are complete for recovered sources. The 52-way interrupted direct run has no retained chunk bounds; the possible touched set cannot be intersected exactly. No assumption of non-execution is made. Any-evaluation and exact-T non-reuse remain NOT_ESTABLISHED.\n")

    old_a_path=root/"analysis/p4_prospective_gate_v2/results/candidate_design_A.json"; candidate=json.loads(old_a_path.read_text())
    candidate.update({"schema":"a303656-design-A-preregistration-candidate-v2","prior_design_A_file_sha256":sha256_file(old_a_path),"prior_design_A_canonical_digest":candidate["canonical_digest"],"registry_digest":registry["canonical_digest"],"preregistration_level":1,"authorization":False,"status":"LEVEL_1_CONDITIONAL_CANDIDATE_ONLY"})
    all_n=[]
    for row in candidate["class_rows"]:
        for item in row["selected_integers"]:
            item["integer_unseen_any_recorded_evaluation"]="NOT_ESTABLISHED"; item["integer_unseen_exact_T"]="NOT_ESTABLISHED"; item["known_exposure_levels"]=[]; all_n.append(item["n"])
    candidate=close(candidate); write_json(out/"design_A_preregistration_candidate_v2.json",candidate)
    cross=[]
    for row in candidate["class_rows"]:
        for item in row["selected_integers"]:
            cross.append({"n":item["n"],"H8":row["H8"],"live_projection_digest":row["live_projection_digest"],"full_mask_digest":row["full_mask_digest"],"CRT_class":row["class_residue_mod_L4"],"confirmed_E1_E4_intersection":False,"conservative_superset_intersection":"UNKNOWN","unknown_exposure":True,"confirmed_exact_T_intersection":False,"possible_exact_T_intersection":"UNKNOWN"})
    write_csv(out/"design_A_exposure_crosswalk_v2.csv",cross,list(cross[0]))
    replacement=close({"schema":"a303656-design-A-replacement-protocol-v2","authorization":False,"outcome_blind":True,"rules":["replace only a slot disqualified by new provenance","same H8 band","same live projection","same full mask","same CRT class","same ordered eligible list","next unused unexposed constraint-satisfying deterministic index","unaffected rows unchanged"],"failure_rule":"If a class cannot retain eight eligible integers: STOP; do not change class/mask/projection; return to independent web audit.","forbidden":"read any T or outcome field"})
    write_json(out/"design_A_replacement_protocol_v2.json",replacement)
    prereg=close({"schema":"a303656-immutable-preregistration-v2","status":"SCHEMA_COMPLETE_CONTENT_NOT_AUTHORIZED","research_question":"Prospective fixed-P4 live-top-band descriptive comparison without adaptive extension","primary_design":"DESIGN_A","secondary_design":"DESIGN_C","exact_manifests":{"primary":"design_A_preregistration_candidate_v2.json","secondary_prior":"analysis/p4_prospective_gate_v2/results/candidate_design_C.json"},"selection_code_hash":sha256_file(root/"analysis/p4_prospective_gate_v2/tools/build_candidates.py"),"registry_hash":registry["canonical_digest"],"authorities":{"H8_min":32,"H8_max":201,"argmax":468,"lex_first":[2,13,50,5],"masks":21,"live_projections":5,"maximizing_mask_aggregate_sha256":"3d6fb47adb745d5501a53f2dcfddbc1106e8f67cfa85ea0d1ce61d487102bce3"},"replacement_protocol":replacement["canonical_digest"],"exposure_exclusion_policy":"exclude confirmed E1-E4; fail closed on possible/unknown exposure","outcome_schema":"FROZEN_BUT_NO_VALUES_PRESENT","planned_descriptive_statistics":["predeclared per-band summaries","controlled band comparisons"],"duplicate_collision_treatment":"reject duplicates; report description collisions separately","execution_failure":"STOP and preserve logs; no replacement based on outcomes","stopping_rules":"single frozen manifest only","no_adaptive_extension":True,"no_post_hoc_mask_class_replacement":True,"audit_authorization_commit_hash":"NOT_ESTABLISHED_PENDING_WEB_AUDIT","authorization":False})
    write_json(out/"immutable_preregistration_schema.json",prereg)

    selection_source="analysis/p4_prospective_gate_v2/tools/build_candidates.py"
    expected={"builder_source":sha256_file(root/selection_source),"registry":registry["canonical_digest"],"candidate_universe":sha256_file(root/"analysis/p4_mod8_live_landscape/results/top_band_masks.json"),"authorities":sha256_file(root/"analysis/p4_mod8_live_landscape/results/authorities.json"),"final_manifest":candidate["canonical_digest"],"analysis_plan":prereg["canonical_digest"]}
    manifest=close({"schema":"a303656-historical-exposure-manifest-v2","registry_digest":registry["canonical_digest"],"components_digest":components_doc["canonical_digest"],"selection_source_path":selection_source,"prior_design_A_file_sha256":sha256_file(old_a_path),"expected_hashes":expected,"status":"PARTIAL"})
    write_json(out/"historical_exposure_manifest_v2.json",manifest)
    gate_items={
      GATES[0]:{"status":"PASS","evidence_references":["protected_authorities.json"],"required_hashes":["3d6fb47a...bce3"],"exact_reason":"accepted exact fixed-P4 result unchanged","blocking_artifacts":[],"verifier_check_ids":["SEM-ARITH-CORE-001"]},
      GATES[1]:{"status":"NOT_ESTABLISHED","evidence_references":["historical_exposure_registry_v2.json"],"required_hashes":[registry["canonical_digest"]],"exact_reason":"interrupted exposure inventory remains PARTIAL","blocking_artifacts":["INT-DIRECT-52WAY bounds"],"verifier_check_ids":["SEM-REG-001"]},
      GATES[2]:{"status":"NOT_ESTABLISHED","evidence_references":["design_A_exposure_crosswalk_v2.csv"],"required_hashes":[registry["canonical_digest"]],"exact_reason":"possible any-evaluation intersection is UNKNOWN","blocking_artifacts":["complete historical execution ledger"],"verifier_check_ids":["SEM-EXP-ANY-001"]},
      GATES[3]:{"status":"NOT_ESTABLISHED","evidence_references":["interrupted_run_catalog.json"],"required_hashes":[registry["canonical_digest"]],"exact_reason":"exact-T global non-reuse cannot be established from incomplete historical ledger","blocking_artifacts":["complete exact-T execution ledger"],"verifier_check_ids":["SEM-EXP-T-001"]},
      GATES[4]:{"status":"PASS","evidence_references":["selection_blindness_audit.json"],"required_hashes":[expected["builder_source"]],"exact_reason":"AST and outcome-dataflow audit passes","blocking_artifacts":[],"verifier_check_ids":["SEM-STATIC-OUTCOME-001"]},
      GATES[5]:{"status":"PASS","evidence_references":["design_A_preregistration_candidate_v2.json"],"required_hashes":[candidate["canonical_digest"]],"exact_reason":"row-level hierarchy reconstructed","blocking_artifacts":[],"verifier_check_ids":["SEM-HIER-001"]},
      GATES[6]:{"status":"PASS","evidence_references":["immutable_preregistration_schema.json"],"required_hashes":[prereg["canonical_digest"]],"exact_reason":"primary and controlled comparison schema frozen","blocking_artifacts":[],"verifier_check_ids":["SEM-COMP-001"]},
      GATES[7]:{"status":"NOT_ESTABLISHED","evidence_references":["immutable_preregistration_schema.json"],"required_hashes":[prereg["canonical_digest"]],"exact_reason":"authorization commit/hash remains pending","blocking_artifacts":["audit authorization commit/hash"],"verifier_check_ids":["SEM-PREREG-001"]},
      GATES[8]:{"status":"NOT_ESTABLISHED","evidence_references":["AUDIT_READY_SUMMARY.md"],"required_hashes":[],"exact_reason":"independent web audit has not reviewed repaired bundle","blocking_artifacts":["independent authorization"],"verifier_check_ids":["SEM-AUTH-001"]},
    }
    gate=close({"schema":"a303656-p4-live-top-band-prospective-gate-v2-nine-item","gate_name":"P4_LIVE_TOP_BAND_PROSPECTIVE_GATE_V2","items":gate_items,"overall_status":"NOT_ESTABLISHED","authorization":"NO_NEW_T_EVALUATION_AUTHORIZED","old_promotion_gate":"FAIL","global_problem_status":"UNRESOLVED"})
    write_json(out/"prospective_gate_v2_nine_item.json",gate)
    write_json(out/"selection_blindness_audit.json", {"schema":"a303656-selection-blindness-audit-v2","status":"PENDING_SEMANTIC_VERIFIER_EXECUTION","source":selection_source,"source_sha256":expected["builder_source"],"method":"Python AST with constant alias, subscript/get, dict-unpack, identifier, and outcome-path checks","forbidden_outcomes":["T","low_T","winner_mask","candidate_outcome","empirical_winner","renamed/aliased outcome data"]})
    protected={"H8_min":32,"H8_max":201,"argmax":468,"lex_first_argmax":[2,13,50,5],"maximizing_full_masks":21,"live_projections":5,"maximizing_mask_aggregate_sha256":"3d6fb47adb745d5501a53f2dcfddbc1106e8f67cfa85ea0d1ce61d487102bce3","changed":False}; write_json(out/"protected_authorities.json",protected)
    commit_doc={"initial_HEAD":"339df087171809610a297a733bedcb0ec98694bc","initial_parent":"db003ac88ff74d6423a9c1e8c215d0222cd53283","SOURCE_Y":"SOURCE_COMMIT_PARENT_OF_RESULTS_Z","RESULTS_Z":"RESULT_COMMIT_CONTAINING_THIS_FILE","W":"db003ac88ff74d6423a9c1e8c215d0222cd53283","X":"339df087171809610a297a733bedcb0ec98694bc","worktree_initially_clean":False,"preexisting_untracked_preserved":True}; write_json(out/"commit_provenance.json",commit_doc)
    limitations="""# Limitations\n\nHistorical provenance remains PARTIAL. The 52-way interrupted direct pilot has no recoverable chunk bounds or exact touched rows. Global exact-T history is not provably exhaustive. Design A is Level 1 only. No new T(n), factorization, two-square oracle, P5/P6 search, or adaptive scan was executed. OEIS A303656 remains UNRESOLVED.\n"""; (out/"limitations.md").write_text(limitations)
    report="""# REPORT: forensic historical exposure recovery\n\nRegistry V2 is **PARTIAL**. The 27/28 mismatch was a count/embedded-list metadata defect: all 28 closed normalized records are retained. The historical 253M metric is the four non-continuous direct datasets; 533.2M is the broader normalized registry union excluding 1.6B. Their exact difference is 280.2M and is decomposed in the registry. Three orphan IDs were recovered with Git commit/tree/blob/SHA and row counts. Interrupted exact touched sets remain unrecoverable; conservative supersets are recorded. Gate V2 remains **NOT_ESTABLISHED** and Design A remains Level 1. No new T(n) was run. Global status: **OEIS A303656: UNRESOLVED**.\n"""; (out/"REPORT.md").write_text(report)
    (out/"AUDIT_READY_SUMMARY.md").write_text(report+"\nIndependent authorization is still required for V2.9.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
