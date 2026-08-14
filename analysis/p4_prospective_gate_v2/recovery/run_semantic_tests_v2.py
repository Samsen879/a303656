#!/usr/bin/env python3
"""Corruption, bypass-regression, and metamorphic tests with semantic matching."""
from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path

from common_v2 import close, write_json
from semantic_verifier_v2 import (SemanticError, audit_selection_source, levels_for,
                                  verify_candidate, verify_gate, verify_registry)


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,required=True); ap.add_argument("--results",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--logs",type=Path,required=True)
    a=ap.parse_args(); root=a.root.resolve(); out=a.results.resolve(); a.logs.mkdir(parents=True,exist_ok=True)
    reg=json.loads((out/"historical_exposure_registry_v2.json").read_text()); comps=json.loads((out/"historical_exposure_components_v2.json").read_text()); man=json.loads((out/"historical_exposure_manifest_v2.json").read_text()); cand=json.loads((out/"design_A_preregistration_candidate_v2.json").read_text()); gate=json.loads((out/"prospective_gate_v2_nine_item.json").read_text())
    tests=[]
    def run(name, mutation, expected_code, category, fn):
        try: fn(); code="ACCEPTED"; actual="none"; rc=0
        except SemanticError as e: code=e.code; actual=e.category; rc=1
        status="PASS" if code==expected_code and actual==category else "FAIL"
        row={"test":name,"mutation":mutation,"expected_error_code":expected_code,"expected_semantic_category":category,"actual_code":code,"actual_category":actual,"return_code":rc,"stderr_excerpt":f"{code}:{actual}","status":status}; tests.append(row); (a.logs/f"{len(tests):02d}_{name}.log").write_text(json.dumps(row,sort_keys=True)+"\n")
    def redoc(x):
        x.pop("canonical_digest", None)
        return close(x)

    # Retained 15 corruption classes.
    x=copy.deepcopy(reg); x["status"]="COMPLETE"; redoc(x); run("registry_false_complete","registry status COMPLETE","REGISTRY_MUST_REMAIN_PARTIAL","provenance_completeness",lambda:verify_registry(x,comps,man))
    x=copy.deepcopy(reg); x["interval_records"].pop(); redoc(x); run("interval_missing","delete interval","INTERVAL_COUNT_28_REQUIRED","interval_semantics",lambda:verify_registry(x,comps,man))
    x=copy.deepcopy(reg); x["interval_records"][0]["inclusive_length"]+=1; redoc(x); run("endpoint_off_by_one","inclusive length +1","INCLUSIVE_LENGTH_MISMATCH","interval_semantics",lambda:verify_registry(x,comps,man))
    x=copy.deepcopy(comps); x["components"]=[q for q in x["components"] if q["source_id"]!="K4_PROGRESSION_PANEL"]; redoc(x); run("orphan_removed","delete orphan source","ORPHAN_SOURCE_UNRESOLVED","source_provenance",lambda:verify_registry(reg,x,man))
    x=copy.deepcopy(cand); x["class_rows"][0]["selected_integers"][1]["n"]=x["class_rows"][0]["selected_integers"][0]["n"]; redoc(x); run("duplicate_integer","duplicate n","SELECTION_INDEX_IDENTITY","selection",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["full_mask_digest"]="0"*64; redoc(x); run("full_mask_corrupt","same-length digest mutation","FULL_MASK_DIGEST_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["live_projection_digest"]="0"*64; redoc(x); run("projection_corrupt","projection digest mutation","LIVE_PROJECTION_DIGEST_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["H8"]-=1; redoc(x); run("H8_corrupt","H8 -1","H8_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["raw_G"]-=1; redoc(x); run("raw_G_corrupt","raw G -1","RAW_G_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["class_residue_mod_L4"]+=1; redoc(x); run("CRT_corrupt","CRT +1","CRT_CLASS_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["hierarchy"]["199"]["integer_count"]+=1; redoc(x); run("hierarchy_corrupt","summary +1","HIERARCHY_RECONSTRUCTION_MISMATCH","hierarchy",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["minimum_integer"]-=1; redoc(x); run("minimum_corrupt","minimum -1","MIN_MAX_RECONSTRUCTION_MISMATCH","selection",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["authorization"]=True; redoc(x); run("authorization_corrupt","authorization true","UNAUTHORIZED_CANDIDATE","authorization",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(gate); x["overall_status"]="PASS"; redoc(x); run("gate_overall_corrupt","overall PASS","OVERALL_GATE_RULE_MISMATCH","gate_schema",lambda:verify_gate(x))
    x=copy.deepcopy(gate); x["items"]["V2.9_INDEPENDENT_AUTHORIZATION"]["status"]="PASS"; x["overall_status"]="NOT_ESTABLISHED"; redoc(x); run("independent_auth_corrupt","V2.9 PASS","V2_9_MUST_REMAIN_NOT_ESTABLISHED","authorization",lambda:verify_gate(x))

    # Seven named bypass regressions.
    x=copy.deepcopy(cand); n=x["class_rows"][0]["selected_integers"][0]["n"]; x["class_rows"][0]["selected_integers"][0]["known_exposure_levels"]=[]; r=copy.deepcopy(reg); r["interval_records"].append({"certainty":"CONFIRMED","normalized_low":n,"normalized_high":n,"boundary_convention":"closed","inclusive_length":1,"exposure_levels":["E1_BINARY_REPRESENTABILITY_CHECK"]}); redoc(r); redoc(x); run("bypass1_forged_exposures","self-report empty, authority exposed","AUTHORITATIVE_EXPOSURE_MEMBERSHIP","exposure",lambda:verify_candidate(x,r,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["class_residue_mod_L4"]+=1; redoc(x); run("bypass2_wrong_CRT","wrong CRT class","CRT_CLASS_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["selected_integers"][0]["selection_index"]=-1; redoc(x); run("bypass3_invalid_index","negative index","SELECTION_INDEX_RANGE","selection",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["minimum_integer"]-=1; redoc(x); run("bypass4_false_minimum_redigest","false minimum with redigest","MIN_MAX_RECONSTRUCTION_MISMATCH","selection",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["hierarchy"]["199"]["CRT_class_count"]+=1; redoc(x); run("bypass5_self_consistent_hierarchy","wrong summary with redigest","HIERARCHY_RECONSTRUCTION_MISMATCH","hierarchy",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"bad.py"; p.write_text('key="T"\nvalue=row.get(key)\n'); import hashlib; h=hashlib.sha256(p.read_bytes()).hexdigest(); run("bypass6_row_get_alias","row.get aliased T","FORBIDDEN_OUTCOME_DATAFLOW","selection_blindness",lambda:audit_selection_source(p,h))
    x=copy.deepcopy(man); x["expected_hashes"]["builder_source"]=None; redoc(x); run("bypass7_missing_expected_hash","null expected builder hash","EXPECTED_SOURCE_HASH_MISSING","hash_closure",lambda:verify_registry(reg,comps,x))

    # Ten property/metamorphic checks, each forced through a semantic rejection or invariant.
    x=copy.deepcopy(cand); x["class_rows"]=list(reversed(x["class_rows"])); redoc(x); run("property_row_order_permutation","reverse rows but canonical semantics require frozen order","CANDIDATE_CANONICAL_DIGEST_MISMATCH","hash_closure",lambda:verify_candidate({**x,"canonical_digest":cand["canonical_digest"]},reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["hierarchy"]["200"]["full_mask_count"]+=1; redoc(x); run("property_summary_reconstruction","summary corrupt","HIERARCHY_RECONSTRUCTION_MISMATCH","hierarchy",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); d=x["class_rows"][0]["full_mask_digest"]; x["class_rows"][0]["full_mask_digest"]=("1" if d[0]!="1" else "0")+d[1:]; redoc(x); run("property_same_length_bitflip","digest nibble flip","FULL_MASK_DIGEST_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(reg); a0=x["interval_records"].pop(0); mid=(a0["normalized_low"]+a0["normalized_high"])//2; p1=copy.deepcopy(a0);p2=copy.deepcopy(a0);p1["normalized_high"]=mid;p1["inclusive_length"]=mid-p1["normalized_low"]+1;p2["normalized_low"]=mid+1;p2["inclusive_length"]=p2["normalized_high"]-mid; x["interval_records"]=[p1,p2]+x["interval_records"]; redoc(x); run("property_interval_split_merge","split one normalized record","INTERVAL_COUNT_28_REQUIRED","interval_semantics",lambda:verify_registry(x,comps,man))
    x=copy.deepcopy(reg); x["interval_records"].append(copy.deepcopy(x["interval_records"][0])); redoc(x); run("property_duplicate_interval","duplicate interval","INTERVAL_COUNT_28_REQUIRED","interval_semantics",lambda:verify_registry(x,comps,man))
    x=copy.deepcopy(cand); x["class_rows"][0]["tuple"][1]+=49; redoc(x); run("property_class_plus_L4_component","non-normalized tuple representative","CRT_TUPLE_NOT_NORMALIZED","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["raw_G"]+=2; redoc(x); run("property_redigest_arithmetic","redigest after arithmetic corruption","RAW_G_MISMATCH","arithmetic",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    x=copy.deepcopy(cand); x["class_rows"][0]["selected_integers"].pop(); x["hierarchy"]["199"]["integer_count"]-=1; x["distinct_integer_count"]-=1; redoc(x); run("property_delete_row_sync_summary","delete candidate and sync summary","DESIGN_A_BALANCE_MISMATCH","hierarchy",lambda:verify_candidate(x,reg,man["prior_design_A_file_sha256"]))
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"bad.py"; p.write_text('outcome_key="winner_mask"\nx=data.get(outcome_key)\n'); import hashlib; h=hashlib.sha256(p.read_bytes()).hexdigest(); run("property_outcome_rename_alias","renamed winner mask alias","FORBIDDEN_OUTCOME_DATAFLOW","selection_blindness",lambda:audit_selection_source(p,h))
    x=copy.deepcopy(man); del x["expected_hashes"]["analysis_plan"]; redoc(x); run("property_expected_hash_absent","delete analysis plan hash","EXPECTED_SOURCE_HASH_MISSING","hash_closure",lambda:verify_registry(reg,comps,x))
    result={"schema":"a303656-semantic-test-matrix-v2","test_count":len(tests),"retained_corruption_tests":15,"bypass_regression_tests":7,"property_metamorphic_tests":10,"all_passed":all(x["status"]=="PASS" for x in tests),"tests":tests}; write_json(a.output,result); return 0 if result["all_passed"] else 1


if __name__=="__main__": raise SystemExit(main())
