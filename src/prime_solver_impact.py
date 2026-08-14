#!/usr/bin/env python3
"""Cumulative per-prime Z3 branching-impact pilot (observational, not proof)."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from time import perf_counter
import z3
from common import check_domain_bounds,enumerate_rectangle,parse_primes

def getstat(st,key):
    try:return st.get_key_value(key)
    except Exception:return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--low',type=int,required=True);ap.add_argument('--high',type=int,required=True)
    ap.add_argument('--C',type=int,required=True);ap.add_argument('--D',type=int,required=True);ap.add_argument('--primes',required=True)
    ap.add_argument('--timeout-ms',type=int,default=3000);ap.add_argument('--csv',required=True);ap.add_argument('--json',required=True)
    a=ap.parse_args();check_domain_bounds(a.C,a.D,a.high);P=parse_primes(a.primes);_,_,rect=enumerate_rectangle(a.C,a.D);rel=[x for x in rect if x.shift<=a.high]
    rows=[]
    for k in range(1,len(P)+1):
        pool=P[:k];n=z3.Int(f'n_{k}');s=z3.Solver();s.set(timeout=a.timeout_ms,random_seed=1);s.add(n>=a.low,n<=a.high)
        for ps in rel:
            cl=z3.Or(*[z3.And(n%p==ps.shift%p,n%(p*p)!=ps.shift%(p*p)) for p in pool])
            s.add(cl if ps.shift<=a.low else z3.Implies(ps.shift<=n,cl))
        t=perf_counter();r=s.check();sec=perf_counter()-t;st=s.statistics()
        row={'rank':k,'added_prime':P[k-1],'pool_size':k,'result':str(r),'seconds':sec,'reason_unknown':s.reason_unknown() if r==z3.unknown else '',
             'decisions':getstat(st,'decisions'),'conflicts':getstat(st,'conflicts'),'propagations':getstat(st,'propagations'),'rlimit_count':getstat(st,'rlimit count'),'max_memory_mb':getstat(st,'max memory')}
        rows.append(row);print(json.dumps(row),flush=True)
    fields=list(rows[0]);Path(a.csv).parent.mkdir(parents=True,exist_ok=True)
    with Path(a.csv).open('w',newline='') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
    Path(a.json).write_text(json.dumps({'classification':'COMPUTATIONAL OBSERVATION','pilot_interval':[str(a.low),str(a.high)],'rows':rows},indent=2)+'\n')
if __name__=='__main__':main()
