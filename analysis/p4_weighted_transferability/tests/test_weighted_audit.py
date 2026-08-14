#!/usr/bin/env python3
"""Positive contract checks and fail-closed corruption tests."""
from __future__ import annotations
import argparse,json,shutil,subprocess,tempfile
from pathlib import Path

def run(cmd:list[str])->int:return subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--artifact-dir",type=Path,required=True);p.add_argument("--certificate-a",type=Path,required=True);p.add_argument("--certificate-b",type=Path,required=True);p.add_argument("--verifier",type=Path,required=True);p.add_argument("--source-commit",required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    base=["python3",str(a.verifier),"--root",str(a.root),"--artifact-dir",str(a.artifact_dir),"--certificate-a",str(a.certificate_a),"--certificate-b",str(a.certificate_b),"--source-commit",a.source_commit,"--check-only"]
    if run(base)!=0:raise SystemExit("positive certificate check failed")
    tests=[]
    mutations=[
      ("enumerator_score_bitflip","cert_a","objective\tfull\todd\t2334\t","objective\tfull\todd\t2334\t9"),
      ("enumerator_mask_bitflip","cert_a","maskflip",None),
      ("ordered_digest_mismatch","cert_b","ordered_result_digest\t","ordered_result_digest\t0"),
      ("tuple_row_count_mismatch","cert_a","rows\t28227969","rows\t28227968"),
      ("target_rank_mismatch","cert_b","target\tCAL-216\t","target\tCAL-216\t0,"),
      ("weight_denominator_drift","weights",",2334,",",2335,"),
      ("weight_table_truncated","weights","truncate",None),
      ("pair_identity_corruption","weights",",0,0,2,",",0,1,2,"),
      ("payload_agreement_false","payload","\"normalized_payload_digests_match\": true","\"normalized_payload_digests_match\": false"),
      ("decoded_agreement_false","payload","\"decoded_digests_match\": true","\"decoded_digests_match\": false"),
      ("direct_T15_omitted","direct","\"contains_n_196653638594_T15\": true","\"contains_n_196653638594_T15\": false"),
      ("direct_count_corruption","direct","\"selected_point_count\": 457","\"selected_point_count\": 456"),
    ]
    with tempfile.TemporaryDirectory(prefix="a303656_weighted_mutations_") as td:
      td=Path(td)
      for name,kind,old,new in mutations:
        work=td/name;shutil.copytree(a.artifact_dir,work);ca=work/"a.tsv";cb=work/"b.tsv";shutil.copy2(a.certificate_a,ca);shutil.copy2(a.certificate_b,cb)
        target={"cert_a":ca,"cert_b":cb,"weights":work/"exact_weight_table.csv","payload":work/"payload_provenance.json","direct":work/"direct_oracle_selection_manifest.json"}[kind]
        text=target.read_text()
        if old=="truncate":text="\n".join(text.splitlines()[:-1])+"\n"
        elif old=="maskflip":
          lines=text.splitlines();index=next(i for i,line in enumerate(lines) if line.startswith("objective\t"));parts=lines[index].split("\t");parts[7]=("1" if parts[7][0]!="1" else "0")+parts[7][1:];lines[index]="\t".join(parts);text="\n".join(lines)+"\n"
        else:
          if old not in text:raise SystemExit(f"mutation anchor absent: {name}")
          text=text.replace(old,new,1)
        target.write_text(text)
        cmd=["python3",str(a.verifier),"--root",str(a.root),"--artifact-dir",str(work),"--certificate-a",str(ca),"--certificate-b",str(cb),"--source-commit",a.source_commit,"--check-only"]
        code=run(cmd);tests.append({"name":name,"return_code":code,"rejected":code!=0})
    report={"schema":"a303656-weighted-audit-corruption-tests-v1","required_count":len(tests),"all_rejected":all(x["rejected"] for x in tests),"tests":tests}
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    if not report["all_rejected"]:return 2
    print("WEIGHTED_AUDIT_CORRUPTION_TESTS_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
