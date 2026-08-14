#!/usr/bin/env python3
"""Execute only builders/verifiers/tests; evaluator invocation is absent by construction."""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
from common_v2 import sha256_file, write_json

def run(cmd, root, log):
    p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}); log.parent.mkdir(parents=True,exist_ok=True); log.write_text(p.stdout or "<no stdout; return code recorded>\n"); return p.returncode

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--root",type=Path,required=True);ap.add_argument("--output",type=Path,required=True);ap.add_argument("--inventory-dir",type=Path,required=True);a=ap.parse_args();root=a.root.resolve();out=a.output.resolve();here=Path(__file__).resolve().parent;logs=out/"execution_logs"
    steps=[("build",[sys.executable,str(here/"build_recovery_v2.py"),"--root",str(root),"--output",str(out),"--inventory-dir",str(a.inventory_dir)]),("verify",[sys.executable,str(here/"semantic_verifier_v2.py"),"--root",str(root),"--results",str(out)]),("tests",[sys.executable,str(here/"run_semantic_tests_v2.py"),"--root",str(root),"--results",str(out),"--output",str(out/"semantic_test_matrix.json"),"--logs",str(out/"semantic_test_logs")])]
    codes={}
    for name,cmd in steps:
        codes[name]=run(cmd,root,logs/f"{name}.log")
        if codes[name]: write_json(out/"return_codes.json",codes); return codes[name]
    audit=json.loads((logs/"verify.log").read_text()); sel=out/"selection_blindness_audit.json"; write_json(sel,{"schema":"a303656-selection-blindness-audit-v2",**audit["selection_audit"]})
    write_json(out/"return_codes.json",codes); return 0
if __name__=="__main__": raise SystemExit(main())
