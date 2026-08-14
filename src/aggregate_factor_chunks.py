#!/usr/bin/env python3
"""Audit and aggregate already-completed factor-sieve chunk JSON files."""
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from pathlib import Path

def digest(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main()->int:
    a=argparse.ArgumentParser()
    a.add_argument('--input-dir',required=True)
    a.add_argument('--low',required=True,type=int)
    a.add_argument('--high',required=True,type=int)
    a.add_argument('--max-odd',required=True,type=int)
    a.add_argument('--summary',required=True)
    a.add_argument('--implementation',required=True)
    ns=a.parse_args()
    d=Path(ns.input_dir)
    files=sorted(d.glob('chunk_*.json'))
    rec=[]
    for p in files:
        z=json.loads(p.read_text())
        if int(z['max_odd'])!=ns.max_odd: raise SystemExit(f'max_odd mismatch: {p}')
        c=[str(x) for x in z['candidates']]
        if int(z['candidate_count'])!=len(c): raise SystemExit(f'candidate count mismatch: {p}')
        rec.append({'low':str(z['low']),'high':str(z['high']),
                    'candidate_count':len(c),'candidates':c,
                    'admissible_pair_count_at_high':z['admissible_pair_count_at_high'],
                    'distinct_shift_count_at_high':z['distinct_shift_count_at_high'],
                    'shifts_processed_before_termination':z['shifts_processed_before_termination'],
                    'json':str(p),'json_sha256':digest(p)})
    rec.sort(key=lambda x:int(x['low']))
    complete=bool(rec) and int(rec[0]['low'])==ns.low and int(rec[-1]['high'])==ns.high and all(int(rec[i]['high'])+1==int(rec[i+1]['low']) for i in range(len(rec)-1))
    tested=sum(int(r['high'])-int(r['low'])+1 for r in rec)
    complete=complete and tested==ns.high-ns.low+1
    cand=[x for r in rec for x in r['candidates']]
    out={'schema':'a303656-factor-chunk-aggregate-v1','implementation':ns.implementation,
         'input_dir':str(d),'low':str(ns.low),'high':str(ns.high),'max_odd':ns.max_odd,
         'chunk_count':len(rec),'complete_gapless_coverage':complete,'integers_tested':tested,
         'candidate_count':len(cand),'candidates':cand,'chunks':rec,
         'python':sys.version,'platform':platform.platform(),
         'classification':('EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE STATED ALL-PRIME CERTIFICATE FAMILY' if complete and not cand else 'CANDIDATES REQUIRE INDEPENDENT VERIFICATION' if complete else 'INCOMPLETE')}
    Path(ns.summary).write_text(json.dumps(out,indent=2)+'\n')
    print(f'chunk_count={len(rec)}')
    print(f'complete_gapless_coverage={str(complete).lower()}')
    print(f'integers_tested={tested}')
    print(f'candidate_count={len(cand)}')
    return 0 if complete else 2
if __name__=='__main__': raise SystemExit(main())
