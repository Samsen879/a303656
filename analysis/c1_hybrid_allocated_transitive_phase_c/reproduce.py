"""Reproduce the four mathematical result files outside the frozen bundle.
Usage: python3 -B reproduce.py --output /tmp/hybrid-replay
No repository, network, third-party package, or GitHub write is needed.
"""
from pathlib import Path
import argparse, hashlib, json, time
import actual_checks, geometry_checks, resource_checks, plan_checks

def main():
    if not __debug__:raise RuntimeError('Do not run with -O: assertions are part of this reference check.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();base=Path(__file__).resolve().parent
    target=args.output.resolve()
    if target==base:raise ValueError('Output must be outside the frozen bundle')
    target.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter();checks=[]
    for name,fn in [('actual_results.json',actual_checks.run),('geometry_results.json',geometry_checks.run),
                    ('resource_results.json',resource_checks.run),('plan_results.json',plan_checks.run)]:
        data=fn();text=json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
        raw=text.encode('utf-8');(target/name).write_bytes(raw)
        frozen=(base/name).read_bytes()
        if frozen!=raw:raise AssertionError(f'Exact replay mismatch: {name}')
        checks.append(dict(file=name,exact_bytes_equal=True,sha256=hashlib.sha256(raw).hexdigest()))
    result=dict(verdict='PASS',method='Fresh recomputation; exact comparison of all four mathematical JSON files',
                comparisons=checks,seconds=time.perf_counter()-started,
                github_writes='NONE',repository_native_replay=False,independent_authors=False)
    (target/'REPLAY.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
