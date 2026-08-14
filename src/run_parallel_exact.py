#!/usr/bin/env python3
"""Run an exact interval scanner over gap-free chunks and aggregate completed JSON outputs."""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, os, subprocess, time
from pathlib import Path


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--binary',required=True);ap.add_argument('--low',type=int,required=True);ap.add_argument('--high',type=int,required=True)
    ap.add_argument('--C',type=int,required=True);ap.add_argument('--D',type=int,required=True);ap.add_argument('--primes',required=True)
    ap.add_argument('--chunks',type=int,default=32);ap.add_argument('--workers',type=int,default=32);ap.add_argument('--window',type=int,default=100_000_000)
    ap.add_argument('--prefix-shifts',type=int,default=64);ap.add_argument('--out-dir',required=True);ap.add_argument('--summary',required=True)
    a=ap.parse_args()
    if a.low>a.high or a.chunks<=0 or a.workers<=0:raise SystemExit('invalid range/chunks/workers')
    binary=Path(a.binary).resolve();prime_file=Path(a.primes).resolve();out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    total=a.high-a.low+1;base=total//a.chunks;extra=total%a.chunks
    ranges=[];cur=a.low
    for i in range(a.chunks):
        size=base+(1 if i<extra else 0);lo=cur;hi=cur+size-1;ranges.append((i,lo,hi));cur=hi+1
    assert cur==a.high+1
    started=time.perf_counter()
    def run(job):
        i,lo,hi=job
        jp=out/f'chunk_{i:04d}.json';lp=out/f'chunk_{i:04d}.log'
        cmd=[str(binary),'--low',str(lo),'--high',str(hi),'--C',str(a.C),'--D',str(a.D),'--primes',str(prime_file),
             '--window',str(a.window),'--prefix-shifts',str(a.prefix_shifts),'--json',str(jp),'--quiet']
        t=time.perf_counter();cp=subprocess.run(cmd,text=True,capture_output=True);sec=time.perf_counter()-t
        lp.write_text(cp.stdout+cp.stderr,encoding='utf-8')
        data=None;err=None
        try:data=json.loads(jp.read_text())
        except Exception as e:err=f'{type(e).__name__}: {e}'
        return {'index':i,'low':str(lo),'high':str(hi),'returncode':cp.returncode,'wall_seconds':sec,
                'json':str(jp.relative_to(out.parent)),'log':str(lp.relative_to(out.parent)),
                'candidate_count':None if data is None else data.get('candidate_count'),
                'integers_tested':None if data is None else data.get('integers_tested'),
                'json_sha256':sha256(jp) if jp.exists() else None,'parse_error':err}
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for r in concurrent.futures.as_completed([ex.submit(run,j) for j in ranges]):
            results.append(r);print(json.dumps(r,sort_keys=True),flush=True)
    results.sort(key=lambda r:r['index'])
    elapsed=time.perf_counter()-started
    complete=True;reason=[];expected=a.low;candidate_total=0;tested_total=0
    for r in results:
        if int(r['low'])!=expected:complete=False;reason.append(f'gap_or_overlap_before_chunk_{r["index"]}')
        expected=int(r['high'])+1
        if r['returncode'] not in (0,1):complete=False;reason.append(f'bad_rc_chunk_{r["index"]}')
        if r['candidate_count'] is None or r['integers_tested'] is None:complete=False;reason.append(f'missing_json_chunk_{r["index"]}')
        else:
            candidate_total+=int(r['candidate_count']);tested_total+=int(r['integers_tested'])
            if int(r['integers_tested'])!=int(r['high'])-int(r['low'])+1:complete=False;reason.append(f'wrong_test_count_chunk_{r["index"]}')
            if (int(r['candidate_count'])==0) != (r['returncode']==1):complete=False;reason.append(f'rc_count_mismatch_chunk_{r["index"]}')
    if expected!=a.high+1:complete=False;reason.append('final_endpoint_mismatch')
    if tested_total!=total:complete=False;reason.append('aggregate_test_count_mismatch')
    payload={'method':'parallel_gap_free_exact_chunk_orchestration','binary':str(binary),'binary_sha256':sha256(binary),
             'prime_file':str(prime_file),'prime_file_sha256':sha256(prime_file),'low':str(a.low),'high':str(a.high),
             'C':a.C,'D':a.D,'chunks':a.chunks,'workers':a.workers,'window':a.window,'prefix_shifts':a.prefix_shifts,
             'integers_expected':total,'integers_tested':tested_total,'candidate_count':candidate_total,
             'all_chunks_complete':complete,'validation_errors':reason,'wall_seconds':elapsed,'chunks_detail':results,
             'classification':('EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL' if complete and candidate_total==0 else
                               'CANDIDATES REQUIRE INDEPENDENT VERIFICATION' if complete else 'UNKNOWN_INCOMPLETE')}
    Path(a.summary).write_text(json.dumps(payload,indent=2)+'\n')
    print(f'all_chunks_complete={complete}');print(f'integers_tested={tested_total}');print(f'candidate_count={candidate_total}');print(f'wall_seconds={elapsed:.6f}')
    return 1 if complete and candidate_total==0 else (0 if complete else 2)
if __name__=='__main__':raise SystemExit(main())
