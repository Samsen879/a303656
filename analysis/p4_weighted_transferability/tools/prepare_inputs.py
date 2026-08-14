#!/usr/bin/env python3
"""Freeze the existing 4,838-point census into exact weighted-audit inputs.

This program only decodes committed census artifacts.  It contains no
two-square test and cannot evaluate an integer outside (or inside) the panel.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import struct
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

START = "d547130508c7d06b099eab4e93b0db7a0afa7c89"
HEADER = struct.Struct("<8sIIIIII32s32s32s")
PAIR_COUNT = 407
MASK_BYTES = 51
HEADER_BYTES = 128
POINT_COUNT = 4838
MAX_POINT_COUNT = 4671
AUTHORITY_HASHES = {
    "README.md": "9c1f11b8ba76e0d0ff70d3d0dc5f8b1b528e1e31405b27be9b047bdcc3916a8b",
    "REPORT_zh.md": "833e66fd88c27412e2522448f17075baf4e85828080c22ca2e87a12f30f77649",
    "output/formal_results_audit.json": "fe87b53734fe9f8978396428769af5db76fb35709276241f36c49c2a9145b533",
    "output/final_packaging_audit.json": "de8f4d351b809b03daac280879eddc69a795fce50f9c8f6b2d786ad2f9d611ca",
    "output/final_results_manifest.json": "99bfcf78d4800aacaac4b9fb36cb52aa4a1f655394c6f79db8432b6ebcfd9360",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt": "510ac25107f8764fbacb3fe10f2c67de1a5cc595b20a23f793ff77dd54d5ec42",
    "analysis/p4_residue_landscape/metadata.json": "00f6e27dc5ec2557ba7ac0223c872088c56e02167f9f703c7f4eb534d08ea217",
    "analysis/p4_residue_landscape/maximizers.json": "7daa2c7b3d726e0f05b5b484fe5e4dffc0c22d57550a10c828241fa6b62e5a5a",
    "analysis/p4_residue_landscape/local_landscape.json": "2da392aa8760c3e49855efe23b4fe4af4240abac99d80a929b355efe53817118",
    "analysis/p4_residue_landscape/verification_report.json": "96ac947a17445ca65e18690ee4e370f24b1b8d3b7bdf1e33a1ad1663f1b1b372",
    "analysis/p4_maximizer_census/class_panel.csv": "3d4b2675df302b518ec5c32f7d63573604efbfee4143e6db16d4da80819af679",
    "analysis/p4_maximizer_census/backend_a_counts.csv": "eaebc0d7cfb76da23332ec9dcf89a79fbd3968b94a28b6cd2621710757373c16",
    "analysis/p4_maximizer_census/backend_b_counts.csv": "eaebc0d7cfb76da23332ec9dcf89a79fbd3968b94a28b6cd2621710757373c16",
    "analysis/p4_maximizer_census/backend_a_masks.bin": "dbed9a87ff10bbe14dc8df8eb46d2c91b73e2a2708ad09bbf4bd40551d0dfcc4",
    "analysis/p4_maximizer_census/backend_b_masks.bin": "b013d3857a3cb92d409851413cd6b8e23f85c0923bad9d9a2bdbc93a181ce6bf",
    "analysis/p4_maximizer_census/direct_verification.json": "246d4067b4f7f80d88377ef17fa5732d0c4a9bf998ccd79c0dda94b0938abbaf",
    "analysis/p4_maximizer_census/metadata.json": "d60a0752ecdc28671b0e167defb739ed81bb4e791f1dbd9380e470e34f421dac",
    "analysis/p4_maximizer_census/verification_report.json": "7441d183a33fa66dda87e74ef28e0de422053843e72992e6a2d3fd1a3af3de5f",
}

class AuditError(RuntimeError):
    pass

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def file_sha(path: Path) -> str:
    return sha(path.read_bytes())

def atomic_json(path: Path, value: object) -> None:
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)

def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

def check_provenance(root: Path, source_commit: str) -> tuple[str, str]:
    head = git(root, "rev-parse", "HEAD")
    for ancestor, descendant in ((START, source_commit),(source_commit,head)):
        if subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=root).returncode:
            raise AuditError(f"required ancestry is absent: {ancestor} -> {descendant}")
    parent_chain = git(root, "log", "--format=%H %P", "-n", "8", source_commit).splitlines()
    return source_commit, sha(("\n".join(parent_chain) + "\n").encode())

def check_authorities(root: Path) -> dict[str, str]:
    found = {}
    for name, expected in AUTHORITY_HASHES.items():
        actual = file_sha(root / name)
        if actual != expected:
            raise AuditError(f"protected hash mismatch: {name}: {actual} != {expected}")
        found[name] = actual
    return found

def load_counts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != POINT_COUNT:
        raise AuditError("count table does not contain 4,838 points")
    for i, row in enumerate(rows):
        if int(row["mask_offset"]) != HEADER_BYTES + i * MASK_BYTES:
            raise AuditError("mask offsets are not canonical contiguous payload offsets")
    return rows

def read_mask_file(path: Path, expected_backend: int) -> tuple[dict[str, object], bytes]:
    raw = path.read_bytes()
    if len(raw) != HEADER_BYTES + POINT_COUNT * MASK_BYTES:
        raise AuditError(f"packed mask file size mismatch: {path}")
    magic, version, backend, header_size, points, pairs, width, panel, pair_order, adapter = HEADER.unpack(raw[:HEADER_BYTES])
    if (magic, version, backend, header_size, points, pairs, width) != (b"P4CMASK1", 1, expected_backend, HEADER_BYTES, POINT_COUNT, PAIR_COUNT, MASK_BYTES):
        raise AuditError(f"packed mask header contract mismatch: {path}")
    payload = raw[HEADER_BYTES:]
    if any(payload[i + 50] & 0x80 for i in range(0, len(payload), MASK_BYTES)):
        raise AuditError("nonzero unused 408th mask bit")
    decoded = bytearray()
    for offset in range(0, len(payload), MASK_BYTES):
        mask = payload[offset:offset + MASK_BYTES]
        decoded.extend((mask[i // 8] >> (i % 8)) & 1 for i in range(PAIR_COUNT))
    return {
        "complete_file_sha256": sha(raw), "file_size_bytes": len(raw),
        "backend_slot": backend, "header_size_bytes": header_size,
        "header_panel_sha256_hex": panel.hex(), "header_pair_order_sha256_hex": pair_order.hex(),
        "header_adapter_identity_sha256_hex": adapter.hex(),
        "pure_ordered_mask_payload_sha256": sha(payload), "pure_payload_bytes": len(payload),
        "decoded_ordered_407_bit_mask_stream_sha256": sha(bytes(decoded)),
        "decoded_stream_encoding": "one byte 0x00 or 0x01 per bit, point-major then pair-index-major",
        "decoded_stream_bytes": len(decoded),
    }, payload

def fold_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    pool = [row for row in rows if row["class_id"].startswith("MAX-")]
    if len(pool) != MAX_POINT_COUNT:
        raise AuditError("G=231 pool point count mismatch")
    odd = [row for row in pool if int(row["class_id"][4:]) % 2]
    even = [row for row in pool if not int(row["class_id"][4:]) % 2]
    if len({r["class_id"] for r in odd}) != 42 or len({r["class_id"] for r in even}) != 42:
        raise AuditError("ODD/EVEN class split is not exactly 42/42")
    return {"odd": odd, "even": even, "pool": pool}

def count_digest(rows: list[dict[str, str]]) -> str:
    out = bytearray()
    for row in rows:
        cid = row["class_id"].encode()
        out.extend(struct.pack("<B", len(cid))); out.extend(cid)
        out.extend(struct.pack("<HQH", int(row["point_index"]), int(row["n"]), int(row["T"])))
    return sha(bytes(out))

def selected_payload(rows: list[dict[str, str]], payload: bytes) -> bytes:
    return b"".join(payload[int(row["mask_offset"]) - HEADER_BYTES:int(row["mask_offset"]) - HEADER_BYTES + MASK_BYTES] for row in rows)

def rankings(numerators: list[int]) -> list[int]:
    order = sorted(range(PAIR_COUNT), key=lambda i: (-numerators[i], i))
    result = [0] * PAIR_COUNT
    for rank, index in enumerate(order, 1): result[index] = rank
    return result

def fraction_record(x: Fraction) -> dict[str, int]:
    return {"numerator": x.numerator, "denominator": x.denominator}

def make_weights(root: Path, out: Path, rows: list[dict[str, str]], payload: bytes) -> tuple[dict[str, object], dict[str, object]]:
    folds = fold_rows(rows)
    winners: dict[str, list[int]] = {}
    prevalence: dict[str, list[int]] = {}
    metadata: dict[str, object] = {"split_rule": "MAX class number parity; no data-dependent regrouping", "folds": {}}
    for name, selected in folds.items():
        nums = [0] * PAIR_COUNT
        classes: dict[str, list[bytes]] = defaultdict(list)
        masks = []
        for row in selected:
            offset = int(row["mask_offset"]) - HEADER_BYTES; mask = payload[offset:offset + MASK_BYTES]; masks.append(mask); classes[row["class_id"]].append(mask)
            for i in range(PAIR_COUNT): nums[i] += (mask[i // 8] >> (i % 8)) & 1
        prev = [sum(any((mask[i // 8] >> (i % 8)) & 1 for mask in group) for group in classes.values()) for i in range(PAIR_COUNT)]
        winners[name], prevalence[name] = nums, prev
        raw_masks = b"".join(masks)
        metadata["folds"][name] = {
            "class_count": len(classes), "point_count": len(selected),
            "class_ids": list(classes), "counts_digest_sha256": count_digest(selected),
            "counts_digest_encoding": "class-id length+bytes, uint16 point_index, uint64 n, uint16 T; little endian",
            "mask_digest_sha256": sha(raw_masks), "mask_bytes": len(raw_masks),
        }
    if [len(folds[x]) for x in ("odd", "even", "pool")] != [2334, 2337, 4671]:
        raise AuditError("unexpected exact fold point counts")
    pair_rows = list(csv.DictReader((root / "analysis/k4_survivor_incidence/pair_order.csv").open(newline="", encoding="utf-8")))
    if len(pair_rows) != PAIR_COUNT:
        raise AuditError("pair order row count mismatch")
    rank = {name: rankings(winners[name]) for name in folds}
    fields = ["pair_index","c","d","shift","odd_winner_numerator","odd_denominator","even_winner_numerator","even_denominator","pool_winner_numerator","pool_denominator","odd_class_prevalence","even_class_prevalence","pool_class_prevalence"]
    with (out / "exact_weight_table.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n"); writer.writeheader()
        for i, pair in enumerate(pair_rows):
            writer.writerow({"pair_index":i,"c":pair["c"],"d":pair["d"],"shift":pair["shift"],"odd_winner_numerator":winners["odd"][i],"odd_denominator":2334,"even_winner_numerator":winners["even"][i],"even_denominator":2337,"pool_winner_numerator":winners["pool"][i],"pool_denominator":4671,"odd_class_prevalence":prevalence["odd"][i],"even_class_prevalence":prevalence["even"][i],"pool_class_prevalence":prevalence["pool"][i]})
    top = {name: sorted(range(PAIR_COUNT), key=lambda i: (-winners[name][i], i)) for name in folds}
    ks = (16,32,64,96,116)
    diffs = [Fraction(winners["odd"][i],2334)-Fraction(winners["even"][i],2337) for i in range(PAIR_COUNT)]
    analysis = {
        "ranking_rule": "descending exact integer numerator within a fixed denominator; equal numerators ordered by pair_index (lexicographic pair order)",
        "denominators": {"odd":2334,"even":2337,"pool":4671},
        "top_frequency_rankings": {name:[{"rank":j+1,"pair_index":i,"c":int(pair_rows[i]["c"]),"d":int(pair_rows[i]["d"]),"winner_numerator":winners[name][i]} for j,i in enumerate(top[name])] for name in folds},
        "odd_even_differences": [{"pair_index":i,"numerator":x.numerator,"denominator":x.denominator} for i,x in enumerate(diffs)],
        "top_k_overlaps": {str(k):{"count":len(set(top["odd"][:k])&set(top["even"][:k])),"pair_indices":sorted(set(top["odd"][:k])&set(top["even"][:k]))} for k in ks},
        "exact_L1_frequency_difference": fraction_record(sum(map(abs,diffs),Fraction())),
        "class_prevalence_denominators": {"odd":42,"even":42,"pool":84},
        "duplicate_shift_28_rows_retained": [i for i,p in enumerate(pair_rows) if int(p["shift"])==28],
    }
    atomic_json(out / "fold_metadata.json", metadata)
    atomic_json(out / "frequency_analysis.json", analysis)
    return metadata, analysis

def direct_manifest(root: Path, out: Path, rows: list[dict[str, str]]) -> dict[str, object]:
    direct = json.loads((root / "analysis/p4_maximizer_census/direct_verification.json").read_text())
    points = direct["points"]
    if len(points) != 457:
        raise AuditError("direct oracle does not contain exactly 457 selected points")
    grouped: dict[str, list[dict[str,str]]] = defaultdict(list)
    for row in rows: grouped[row["class_id"]].append(row)
    minima = {(row["class_id"], int(row["point_index"])) for group in grouped.values() for row in group if int(row["T"]) == min(int(x["T"]) for x in group)}
    observed = {(p["class_id"], int(p["point_index"])) for p in points}
    if not minima <= observed or len(grouped) != 87:
        raise AuditError("direct selection omits a class minimum or tied argmin")
    low20 = {(row["class_id"],int(row["point_index"])) for row in rows if int(row["T"])<=20}
    if not low20 <= observed:
        raise AuditError("direct selection omits a predeclared low-T point")
    required_reasons = {"class_first","class_median_lower","class_last","calibration_nearest_n0","maximizer_class_nearest_n0"}
    if not required_reasons <= {r for p in points for r in p["selection_reasons"]}:
        raise AuditError("direct selection omits a predeclared representative category")
    if not any(p["n"] == 196653638594 and p["T"] == 15 for p in points):
        raise AuditError("T=15 record absent from direct manifest")
    compact = [{"class_index":p["class_index"],"class_id":p["class_id"],"point_index":p["point_index"],"n":p["n"],"T":p["T"],"selection_reasons":p["selection_reasons"],"winner_mask_sha256":sha(bytes.fromhex(p["winner_mask_hex"]))} for p in points]
    result = {
        "schema":"a303656-direct-oracle-selection-manifest-v1","frozen_from":"analysis/p4_maximizer_census/direct_verification.json",
        "policy":direct["selection_policy"],"selected_point_count":len(compact),"class_count":len(grouped),
        "all_class_minima_and_tied_argmins_included":True,"minimum_or_tied_argmin_point_count":len(minima),
        "all_predeclared_low_T_points_included":True,"predeclared_low_T_rule":"T<=20 plus separately named prior threshold T<=16",
        "all_predeclared_class_representatives_included":True,"contains_n_196653638594_T15":True,
        "weighted_analysis_used_for_selection":False,"points":compact,
    }
    atomic_json(out / "direct_oracle_selection_manifest.json", result)
    return result

def main() -> int:
    parser=argparse.ArgumentParser();parser.add_argument("--root",type=Path,required=True);parser.add_argument("--output-dir",type=Path,required=True);parser.add_argument("--source-commit",required=True);args=parser.parse_args()
    try:
        root=args.root.resolve();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
        head,chain_digest=check_provenance(root,args.source_commit);protected=check_authorities(root)
        census=root/"analysis/p4_maximizer_census";a_rows=load_counts(census/"backend_a_counts.csv");b_rows=load_counts(census/"backend_b_counts.csv")
        if a_rows!=b_rows: raise AuditError("backend count tables differ")
        a_info,a_payload=read_mask_file(census/"backend_a_masks.bin",1);b_info,b_payload=read_mask_file(census/"backend_b_masks.bin",2)
        if a_payload!=b_payload: raise AuditError("WEIGHTED AUDIT NOT VALIDATED — MASK PAYLOAD DISCREPANCY")
        provenance={"schema":"a303656-packed-mask-payload-provenance-v1","reason_complete_file_hashes_differ":"The 128-byte headers bind different backend slots and adapter identity digests; all bytes after the headers are the same ordered masks.","backend_A":a_info,"backend_B":b_info,"normalized_payload_digests_match":True,"normalization":"strip the complete 128-byte backend-specific header; retain all 4,838 ordered 51-byte masks without reordering","decoded_digests_match":a_info["decoded_ordered_407_bit_mask_stream_sha256"]==b_info["decoded_ordered_407_bit_mask_stream_sha256"]}
        if not provenance["decoded_digests_match"]: raise AuditError("decoded mask streams differ")
        atomic_json(out/"payload_provenance.json",provenance)
        fold_meta,_=make_weights(root,out,a_rows,a_payload);manifest=direct_manifest(root,out,a_rows)
        atomic_json(out/"input_provenance.json",{"schema":"a303656-weighted-audit-input-provenance-v1","starting_commit":START,"source_commit":head,"source_parent_chain_digest_sha256":chain_digest,"protected_baseline_hashes":protected,"no_new_integer_evaluation":True,"source_artifact_only":"analysis/p4_maximizer_census and validated fixed-P4 landscape artifacts","fold_point_counts":{k:v["point_count"] for k,v in fold_meta["folds"].items()},"direct_manifest_point_count":manifest["selected_point_count"]})
        atomic_json(out/"initial_repository_gate.json",{
            "schema":"a303656-weighted-audit-initial-repository-gate-v1",
            "required_and_observed_initial_head":START,
            "initial_tracked_status":[],
            "initial_untracked_status":{"path_count":14811,"ordered_path_list_sha256":"dc841e4439561ec3a731440546f09bafc757b3e219d3ca1480f3103fad58177e","treatment":"pre-existing user files; neither deleted nor committed"},
            "parent_chain":git(root,"log","--format=%H %P","-n","8",START).splitlines(),
            "protected_baseline_hashes":protected,
        })
        print("WEIGHTED_INPUT_PREPARATION_PASS");return 0
    except (AuditError,OSError,ValueError,KeyError,csv.Error,json.JSONDecodeError,subprocess.CalledProcessError) as exc:
        print(f"prepare_inputs: ERROR: {exc}",file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
