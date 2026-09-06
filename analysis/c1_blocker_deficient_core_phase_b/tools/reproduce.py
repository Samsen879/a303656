#!/usr/bin/env python3
"""Replay all frozen computations to a separate directory; compare exact JSON."""
import argparse
import json
import sys
import tempfile
from pathlib import Path
import arithmetic, audits, paired_digits, boundary, primed_three, six_rows

ROOT=Path(__file__).resolve().parents[1]

def tasks():
    return [('arithmetic_closure',arithmetic.run),
            ('hall_audit',audits.hall_audit),('route_audit',audits.route_audit),
            ('terminal_signatures',audits.signatures),
            ('paired_digits',paired_digits.run),('boundary_escape',boundary.run),
            ('primed_three',primed_three.audit),
            ('primed_terminal_signatures',primed_three.signatures),
            ('six_row_obstruction',six_rows.run)]

def replay(out, compare=True):
    out=Path(out).resolve()
    if out==ROOT/'results':
        raise ValueError('Replay must not overwrite the sealed reference results')
    out.mkdir(parents=True,exist_ok=True)
    checked=[]
    for name,fn in tasks():
        result=fn()
        text=json.dumps(result,sort_keys=True,indent=2)+'\n'
        (out/(name+'.json')).write_text(text,encoding='utf-8')
        if compare:
            expected=(ROOT/'results'/(name+'.json')).read_text(encoding='utf-8')
            if text!=expected:raise AssertionError(f'exact replay mismatch: {name}')
        checked.append(name)
        print(name,'PASS',flush=True)
    return dict(exact_json_outputs=len(checked),outputs=checked,
                comparison='byte-for-byte deterministic JSON',mismatches=0)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path)
    a=p.parse_args()
    if a.output_dir:
        print(json.dumps(replay(a.output_dir),indent=2))
    else:
        with tempfile.TemporaryDirectory(prefix='a303656-phase-b-') as d:
            print(json.dumps(replay(d),indent=2))
