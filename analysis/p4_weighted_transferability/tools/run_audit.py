#!/usr/bin/env python3
"""Build, run, and verify the fixed-scope weighted audit with raw logs external."""
from __future__ import annotations
import argparse,json,os,subprocess,time
from pathlib import Path

def main()->int:
  p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--artifact-dir",type=Path,required=True);p.add_argument("--raw-dir",type=Path,required=True);p.add_argument("--source-commit",required=True);a=p.parse_args();root=a.root.resolve();art=a.artifact_dir.resolve();raw=a.raw_dir.resolve();art.mkdir(parents=True,exist_ok=True);raw.mkdir(parents=True,exist_ok=True)
  tools=root/"analysis/p4_weighted_transferability/tools";tests=root/"analysis/p4_weighted_transferability/tests/test_weighted_audit.py";commands=[]
  def run(name:str,cmd:list[str])->None:
    start=time.monotonic();out=raw/f"{name}.stdout.log";err=raw/f"{name}.stderr.log"
    with out.open("wb") as so,err.open("wb") as se:r=subprocess.run(cmd,cwd=root,stdout=so,stderr=se)
    commands.append({"name":name,"command":cmd,"return_code":r.returncode,"wall_seconds":format(time.monotonic()-start,".6f"),"stdout":out.name,"stderr":err.name})
    if r.returncode:raise SystemExit(f"{name} failed with return code {r.returncode}")
  py=os.environ.get("PYTHON","python3");cxx=os.environ.get("CXX","g++");bin_a=raw/"weighted_enumerator_a";bin_b=raw/"weighted_enumerator_b";cert_a=art/"enumerator_a_certificate.tsv";cert_b=art/"enumerator_b_certificate.tsv"
  run("prepare_inputs",[py,str(tools/"prepare_inputs.py"),"--root",str(root),"--output-dir",str(art),"--source-commit",a.source_commit])
  flags=[cxx,"-std=c++20","-O3","-DNDEBUG","-Wall","-Wextra","-Wpedantic","-Werror"]
  run("build_a",flags+[str(tools/"weighted_enumerator_a.cpp"),"-o",str(bin_a)]);run("build_b",flags+[str(tools/"weighted_enumerator_b.cpp"),"-o",str(bin_b)])
  run("enumerator_a",[str(bin_a),str(art/"exact_weight_table.csv"),str(cert_a)]);run("enumerator_b",[str(bin_b),str(art/"exact_weight_table.csv"),str(cert_b)])
  verifier=[py,str(tools/"verifier.py"),"--root",str(root),"--artifact-dir",str(art),"--certificate-a",str(cert_a),"--certificate-b",str(cert_b),"--source-commit",a.source_commit]
  run("certificate_check",verifier+["--check-only"])
  negative=art/"corruption_tests.json";run("corruption_tests",[py,str(tests),"--root",str(root),"--artifact-dir",str(art),"--certificate-a",str(cert_a),"--certificate-b",str(cert_b),"--verifier",str(tools/"verifier.py"),"--source-commit",a.source_commit,"--output",str(negative)])
  run("result_builder",verifier+["--negative-report",str(negative)])
  manifest=art/"command_manifest.json";manifest.write_text(json.dumps({"schema":"a303656-weighted-audit-command-manifest-v1","raw_log_directory":str(raw),"raw_logs_committed":False,"commands":commands},indent=2,sort_keys=True)+"\n")
  # Refresh metadata after command_manifest exists. The preceding result_builder return code is preserved above.
  run("artifact_verifier",verifier+["--negative-report",str(negative),"--command-manifest",str(manifest)])
  manifest.write_text(json.dumps({"schema":"a303656-weighted-audit-command-manifest-v1","raw_log_directory":str(raw),"raw_logs_committed":False,"commands":commands},indent=2,sort_keys=True)+"\n")
  print("WEIGHTED_AUDIT_RUN_PASS");return 0
if __name__=="__main__":raise SystemExit(main())
