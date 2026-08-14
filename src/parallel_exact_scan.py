#!/usr/bin/env python3
"""Parallel exact interval orchestrator with explicit gap/overlap validation.

The mathematical work is performed by the selected exact scanner binary.  This
wrapper partitions one inclusive interval into deterministic inclusive shards,
runs each shard, validates every machine-readable result, and emits an aggregate
manifest.  Exit codes: 0 if candidates are present, 1 if all shards are exactly
empty, 2 on any incomplete/error/invalid shard.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
from pathlib import Path
from time import perf_counter


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()


def partition(low:int,high:int,count:int)->list[tuple[int,int]]:
    total=high-low+1
    if count<1 or count>total: raise ValueError('invalid shard count')
    ans=[]
    for i in range(count):
        a=low+(total*i)//count
        b=low+(total*(i+1))//count-1
        ans.append((a,b))
    assert ans[0][0]==low and ans[-1][1]==high
    assert all(ans[i][1]+1==ans[i+1][0] for i in range(len(ans)-1))
    return ans


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--binary',required=True)
    ap.add_argument('--low',type=int,required=True);ap.add_argument('--high',type=int,required=True)
    ap.add_argument('--C',type=int,required=True);ap.add_argument('--D',type=int,required=True)
    ap.add_argument('--prefix-shifts',type=int,default=100);ap.add_argument('--window',type=int,default=5_000_000)
    ap.add_argument('--workers',type=int,default=16);ap.add_argument('--shards',type=int,default=32)
    ap.add_argument('--out-dir',required=True);ap.add_argument('--summary',required=True)
    args=ap.parse_args()
    if args.low>args.high: raise SystemExit('low>high')
    binary=Path(args.binary).resolve()
    if not binary.is_file(): raise SystemExit(f'missing binary {binary}')
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    pieces=partition(args.low,args.high,args.shards)
    started=perf_counter()

    def run_one(item:tuple[int,tuple[int,int]]):
        i,(a,b)=item
        stem=f'shard_{i:04d}_{a}_{b}'
        jpath=out/(stem+'.json'); lpath=out/(stem+'.log')
        cmd=[str(binary),'--low',str(a),'--high',str(b),'--C',str(args.C),'--D',str(args.D),
             '--window',str(args.window),'--prefix-shifts',str(args.prefix_shifts),
             '--json',str(jpath),'--quiet']
        t0=perf_counter()
        cp=subprocess.run(cmd,text=True,capture_output=True)
        sec=perf_counter()-t0
        lpath.write_text(cp.stdout+cp.stderr,encoding='utf-8')
        return {'index':i,'low':a,'high':b,'returncode':cp.returncode,'wall_seconds':sec,
                'json_path':str(jpath),'log_path':str(lpath),'command':cmd}

    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures=[ex.submit(run_one,x) for x in enumerate(pieces)]
        for fut in concurrent.futures.as_completed(futures):
            r=fut.result();results.append(r)
            print(json.dumps({k:r[k] for k in ('index','low','high','returncode','wall_seconds')}),flush=True)
    results.sort(key=lambda x:x['index'])

    errors=[];candidates=[];tested=0;sum_scanner_seconds=0.0;sum_prefix_survivors=0
    for expected,r in zip(pieces,results,strict=True):
        a,b=expected
        if (r['low'],r['high'])!=(a,b): errors.append(f'partition mismatch shard {r["index"]}')
        if r['returncode'] not in (0,1): errors.append(f'shard {r["index"]} returncode {r["returncode"]}')
        p=Path(r['json_path'])
        if not p.is_file(): errors.append(f'missing JSON shard {r["index"]}');continue
        try:d=json.loads(p.read_text())
        except Exception as e:errors.append(f'invalid JSON shard {r["index"]}: {e}');continue
        if int(d['low'])!=a or int(d['high'])!=b:errors.append(f'JSON bounds mismatch shard {r["index"]}')
        width=b-a+1
        if int(d['integers_tested'])!=width:errors.append(f'integer count mismatch shard {r["index"]}')
        dc=[int(x) for x in d.get('candidates',[])]
        if int(d['candidate_count'])!=len(dc):errors.append(f'candidate count mismatch shard {r["index"]}')
        if any(x<a or x>b for x in dc):errors.append(f'candidate out of shard {r["index"]}')
        if (r['returncode']==0)!=(len(dc)>0):errors.append(f'exit/candidate mismatch shard {r["index"]}')
        candidates.extend(dc);tested+=width
        sum_scanner_seconds+=float(d.get('elapsed_seconds',0.0))
        sum_prefix_survivors+=int(d.get('survivors_after_prefix_total',0))
        r['result_sha256']=sha256(p);r['candidate_count']=len(dc);r['scanner_seconds']=d.get('elapsed_seconds')
        r['prefix_survivors']=d.get('survivors_after_prefix_total')
    if tested!=args.high-args.low+1: errors.append('aggregate tested count mismatch')
    if len(set(candidates))!=len(candidates): errors.append('duplicate candidate across shards')
    elapsed=perf_counter()-started
    payload={
      'schema':'a303656-parallel-exact-scan-v1','binary':str(binary),'binary_sha256':sha256(binary),
      'low':str(args.low),'high':str(args.high),'C':args.C,'D':args.D,
      'prefix_shifts':args.prefix_shifts,'window':args.window,'workers':args.workers,'shard_count':args.shards,
      'partition_rule':'[low+floor(total*i/shards), low+floor(total*(i+1)/shards)-1], inclusive',
      'coverage_contiguous_no_gaps_no_overlaps':not errors,
      'integers_tested':tested,'expected_integers':args.high-args.low+1,
      'sum_prefix_survivors':sum_prefix_survivors,'candidate_count':len(candidates),
      'candidates':[str(x) for x in sorted(candidates)],'errors':errors,
      'aggregate_wall_seconds':elapsed,'sum_scanner_seconds':sum_scanner_seconds,
      'environment':{'python':sys.version,'platform':platform.platform(),'cpu_count':os.cpu_count(),
                     'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
      'shards':results,
      'classification':('INVALID_OR_INCOMPLETE' if errors else
                        'CANDIDATES_REQUIRE_INDEPENDENT_VERIFIERS' if candidates else
                        'EXACT EXHAUSTIVE FINITE COMPUTATION; ALL SHARDS EMPTY')
    }
    summary=Path(args.summary);summary.parent.mkdir(parents=True,exist_ok=True)
    summary.write_text(json.dumps(payload,indent=2)+'\n')
    print(f'integers_tested={tested}')
    print(f'candidate_count={len(candidates)}')
    print(f'errors={len(errors)}')
    print(f'aggregate_wall_seconds={elapsed:.6f}')
    if errors:
        for e in errors: print('ERROR '+e,file=sys.stderr)
        return 2
    return 0 if candidates else 1

if __name__=='__main__': raise SystemExit(main())
