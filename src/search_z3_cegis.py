#!/usr/bin/env python3
"""Method B: exact CEGIS with full-domain adversarial enumeration every round."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

import z3
from common import check_domain_bounds, enumerate_pairs, enumerate_rectangle, exact_one_obstructs, parse_primes


def z3_clause(n: z3.ArithRef,s:int,primes:list[int])->z3.BoolRef:
    return z3.Or(*[z3.And(n%p==s%p,n%(p*p)!=s%(p*p)) for p in primes])


def first_uncovered(nval:int,primes:list[int]):
    t0=perf_counter(); _,_,pairs=enumerate_pairs(nval)
    for ps in pairs:
        r=nval-ps.shift
        if not any(exact_one_obstructs(r,p) for p in primes):
            return ps,len(pairs),perf_counter()-t0
    return None,len(pairs),perf_counter()-t0


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--low",type=int,required=True); ap.add_argument("--high",type=int,required=True)
    ap.add_argument("--C",type=int,required=True); ap.add_argument("--D",type=int,required=True)
    ap.add_argument("--primes",required=True); ap.add_argument("--timeout-ms",type=int,default=60000)
    ap.add_argument("--max-iterations",type=int,default=1000); ap.add_argument("--seed",type=int,default=1)
    ap.add_argument("--initial-pairs",type=int,default=1)
    ap.add_argument("--json",required=True); ap.add_argument("--jsonl",required=True)
    ap.add_argument("--verifier",default=str(Path(__file__).with_name("verifier.py"))); ap.add_argument("--cert-dir")
    args=ap.parse_args()
    if args.low>args.high: raise SystemExit("low>high")
    check_domain_bounds(args.C,args.D,args.high)
    primes=parse_primes(args.primes)
    _,_,rect=enumerate_rectangle(args.C,args.D)
    relevant=sorted([ps for ps in rect if ps.shift<=args.high],key=lambda x:(x.shift,x.c,x.d))
    n=z3.Int("n")
    solver=z3.Solver(); solver.set(timeout=args.timeout_ms,random_seed=args.seed)
    solver.add(n>=args.low,n<=args.high)
    constrained:set[tuple[int,int]]=set()
    for ps in relevant[:max(0,args.initial_pairs)]:
        solver.add(z3.Implies(ps.shift<=n,z3_clause(n,ps.shift,primes)))
        constrained.add((ps.c,ps.d))
    Path(args.jsonl).parent.mkdir(parents=True,exist_ok=True)
    jf=Path(args.jsonl).open("w",encoding="utf-8")
    records=[]; candidate=None; verifier_rc=None; termination="iteration_limit"
    for it in range(1,args.max_iterations+1):
        t0=perf_counter(); res=solver.check(); st=perf_counter()-t0
        if res!=z3.sat:
            termination="solver_unknown" if res==z3.unknown else "solver_unsat_without_proof_object"
            rec={"iteration":it,"solver_result":str(res),"solver_seconds":st,"reason_unknown":solver.reason_unknown() if res==z3.unknown else None,
                 "current_constraint_count":len(constrained),"prime_count":len(primes),"termination":termination}
            records.append(rec); jf.write(json.dumps(rec)+"\n"); jf.flush(); print(json.dumps(rec),flush=True); break
        nval=solver.model().eval(n,model_completion=True).as_long()
        witness,active_count,vt=first_uncovered(nval,primes)
        rec={"iteration":it,"candidate_n":str(nval),"active_pair_count":active_count,
             "new_counterexample_pair":None if witness is None else {"c":witness.c,"d":witness.d,"shift":str(witness.shift)},
             "current_constraint_count":len(constrained),"prime_count":len(primes),"solver_seconds":st,"verifier_seconds":vt}
        if witness is None:
            candidate=nval; termination="full_exact_adversary_pass"; rec["termination"]=termination
            records.append(rec); jf.write(json.dumps(rec)+"\n"); jf.flush(); print(json.dumps(rec),flush=True); break
        key=(witness.c,witness.d)
        if key in constrained:
            termination="internal_error_repeated_constrained_witness"; rec["termination"]=termination
            records.append(rec); jf.write(json.dumps(rec)+"\n"); jf.flush(); print(json.dumps(rec),flush=True); break
        solver.add(z3.Implies(witness.shift<=n,z3_clause(n,witness.shift,primes)))
        constrained.add(key); rec["termination"]="continue"
        records.append(rec); jf.write(json.dumps(rec)+"\n"); jf.flush(); print(json.dumps(rec),flush=True)
    jf.close()
    cert_paths={}
    if candidate is not None:
        cert_dir=Path(args.cert_dir or Path(args.json).with_suffix("")); cert_dir.mkdir(parents=True,exist_ok=True)
        cert_json=cert_dir/"counterexample.json"; cert_csv=cert_dir/"obstructions.csv"; vlog=cert_dir/"python_verifier.log"
        cmd=[sys.executable,args.verifier,"--n",str(candidate),"--primes",",".join(map(str,primes)),
             "--interval-low",str(args.low),"--interval-high",str(args.high),"--C",str(args.C),"--D",str(args.D),
             "--cert-json",str(cert_json),"--obstructions-csv",str(cert_csv),"--quiet-pairs"]
        cp=subprocess.run(cmd,text=True,capture_output=True); vlog.write_text(cp.stdout+cp.stderr,encoding="utf-8")
        verifier_rc=cp.returncode; cert_paths={"json":str(cert_json),"csv":str(cert_csv),"log":str(vlog)}; print(cp.stdout,end="")
    payload={"method":"B_CEGIS_Z3_Int","z3_version":z3.get_version_string(),"low":str(args.low),"high":str(args.high),
             "C":args.C,"D":args.D,"primes":primes,"max_iterations":args.max_iterations,"records":records,
             "candidate":str(candidate) if candidate is not None else None,"termination":termination,
             "independent_python_verifier_returncode":verifier_rc,"certificate_paths":cert_paths,
             "classification":("CERTIFIED BY INDEPENDENT VERIFIER" if candidate is not None and verifier_rc==0 else
                               "COMPUTATIONAL OBSERVATION" if candidate is not None else
                               "UNKNOWN" if "unknown" in termination or termination=="iteration_limit" else
                               "SMT_UNSAT_WITHOUT_PROOF_OBJECT")}
    Path(args.json).write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    return 0 if candidate is not None and verifier_rc==0 else (2 if payload["classification"]=="UNKNOWN" else 1)
if __name__=="__main__": raise SystemExit(main())
