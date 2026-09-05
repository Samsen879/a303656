#!/usr/bin/env python3
"""Run every standalone calculation in a temporary directory and compare exact
mathematical outputs against the sealed reference JSON. Timings are excluded
explicitly; integer data, lists, Fractions as strings, and scope metadata are not.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys, tempfile, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if not __debug__:
    raise RuntimeError('Run without -O.')

def math_data(x):
    if isinstance(x,dict):return {k:math_data(v) for k,v in x.items() if k!='seconds'}
    if isinstance(x,list):return [math_data(v) for v in x]
    return x

def run(output: Path) -> None:
    start=time.perf_counter();matched={}
    with tempfile.TemporaryDirectory(prefix='a303656-kraft-hall-') as td:
        temp=Path(td)
        commands=[
            ['panel.py','--bound','100000','--output',temp/'benchmark_panel.json'],
            ['generate_certificates.py','--output-dir',temp],
            ['panel.py','--bound','10000000','--output',temp/'panel_10000000.json'],
            ['paired.py','--output',temp/'paired_positions.json'],
            ['replay.py','--output',temp/'existing_pair_replay.json'],
            ['counterexamples.py','--output',temp/'counterexamples.json'],
            ['verify_theorems.py','--input-dir',temp,'--output',temp/'theorem_verification.json'],
        ]
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'}
        for cmd in commands:
            proc=subprocess.run([sys.executable,str(ROOT/'tools'/cmd[0]),*[str(a) for a in cmd[1:]]],env=env,text=True,capture_output=True,timeout=45)
            if proc.returncode:
                raise RuntimeError(f'{cmd[0]} failed:\n{proc.stdout}\n{proc.stderr}')
            print(cmd[0]+': PASS')
        for generated in sorted(temp.glob('*.json')):
            reference=ROOT/'results'/generated.name
            if not reference.exists():raise RuntimeError(f'Missing reference {reference.name}')
            a=math_data(json.loads(reference.read_text()));b=math_data(json.loads(generated.read_text()))
            if a!=b:raise RuntimeError(f'Exact mathematical mismatch: {generated.name}')
            payload=json.dumps(a,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
            matched[generated.name]=hashlib.sha256(payload).hexdigest()
        result={'status':'PASS','matched_result_files':len(matched),'comparison':'All JSON content except fields named seconds; no numeric tolerance','mathematical_sha256':matched,'seconds':time.perf_counter()-start}
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();run(args.output)
