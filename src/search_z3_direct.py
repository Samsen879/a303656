#!/usr/bin/env python3
"""Method A: direct exact Z3 integer encoding, with interval splitting."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

import z3
from common import check_domain_bounds, enumerate_rectangle, parse_primes


def clause(n: z3.ArithRef, s: int, primes: list[int]) -> z3.BoolRef:
    return z3.Or(*[
        z3.And(n % p == s % p, n % (p*p) != s % (p*p))
        for p in primes
    ])


def solve_interval(low: int, high: int, C: int, D: int, primes: list[int], timeout_ms: int, seed: int):
    check_domain_bounds(C,D,high)
    _,_,rect=enumerate_rectangle(C,D)
    relevant=[ps for ps in rect if ps.shift<=high]
    n=z3.Int("n")
    solver=z3.Solver()
    solver.set(timeout=timeout_ms, random_seed=seed)
    solver.add(n>=low,n<=high)
    constraint_count=0
    for ps in relevant:
        cl=clause(n,ps.shift,primes)
        if ps.shift<=low:
            solver.add(cl)
        else:
            solver.add(z3.Implies(ps.shift<=n,cl))
        constraint_count+=1
    t0=perf_counter(); result=solver.check(); elapsed=perf_counter()-t0
    candidate=None
    if result==z3.sat:
        candidate=solver.model().eval(n,model_completion=True).as_long()
    return {
        "low":str(low),"high":str(high),"result":str(result),"candidate":str(candidate) if candidate is not None else None,
        "constraint_count":constraint_count,"solver_seconds":elapsed,"statistics":str(solver.statistics()),
        "reason_unknown":solver.reason_unknown() if result==z3.unknown else None,
    }


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--low",type=int,required=True); ap.add_argument("--high",type=int,required=True)
    ap.add_argument("--C",type=int,required=True); ap.add_argument("--D",type=int,required=True)
    ap.add_argument("--primes",required=True)
    ap.add_argument("--timeout-ms",type=int,default=60000)
    ap.add_argument("--split-size",type=int,default=0)
    ap.add_argument("--seed",type=int,default=1)
    ap.add_argument("--json",required=True)
    ap.add_argument("--verifier",default=str(Path(__file__).with_name("verifier.py")))
    ap.add_argument("--cert-dir")
    args=ap.parse_args()
    if args.low>args.high: raise SystemExit("low>high")
    check_domain_bounds(args.C,args.D,args.high)
    primes=parse_primes(args.primes)
    split=args.split_size if args.split_size>0 else args.high-args.low+1
    records=[]; candidate=None; verifier_rc=None
    a=args.low
    while a<=args.high:
        b=min(args.high,a+split-1)
        rec=solve_interval(a,b,args.C,args.D,primes,args.timeout_ms,args.seed+len(records))
        records.append(rec)
        print(json.dumps(rec,sort_keys=True),flush=True)
        if rec["result"]=="sat":
            candidate=int(rec["candidate"]); break
        a=b+1
    cert_paths={}
    if candidate is not None:
        cert_dir=Path(args.cert_dir or Path(args.json).with_suffix(""))
        cert_dir.mkdir(parents=True,exist_ok=True)
        cert_json=cert_dir/"counterexample.json"; cert_csv=cert_dir/"obstructions.csv"; vlog=cert_dir/"python_verifier.log"
        cmd=[sys.executable,args.verifier,"--n",str(candidate),"--primes",",".join(map(str,primes)),
             "--interval-low",str(args.low),"--interval-high",str(args.high),"--C",str(args.C),"--D",str(args.D),
             "--cert-json",str(cert_json),"--obstructions-csv",str(cert_csv),"--quiet-pairs"]
        cp=subprocess.run(cmd,text=True,capture_output=True)
        vlog.write_text(cp.stdout+cp.stderr,encoding="utf-8")
        verifier_rc=cp.returncode
        cert_paths={"json":str(cert_json),"csv":str(cert_csv),"log":str(vlog)}
        print(cp.stdout,end="")
    payload={
        "method":"A_direct_Z3_Int","z3_version":z3.get_version_string(),
        "low":str(args.low),"high":str(args.high),"C":args.C,"D":args.D,"primes":primes,
        "timeout_ms_per_split":args.timeout_ms,"split_size":split,"records":records,
        "candidate":str(candidate) if candidate is not None else None,
        "independent_python_verifier_returncode":verifier_rc,"certificate_paths":cert_paths,
        "classification":("CERTIFIED BY INDEPENDENT VERIFIER" if candidate is not None and verifier_rc==0 else
                          "COMPUTATIONAL OBSERVATION" if candidate is not None else
                          "UNKNOWN" if any(r["result"]=="unknown" for r in records) else
                          "SMT_UNSAT_WITHOUT_PROOF_OBJECT"),
    }
    Path(args.json).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json).write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    return 0 if candidate is not None and verifier_rc==0 else (2 if any(r["result"]=="unknown" for r in records) else 1)
if __name__=="__main__": raise SystemExit(main())
