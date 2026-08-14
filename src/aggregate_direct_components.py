#!/usr/bin/env python3
"""Aggregate already-audited gapless direct two-square component summaries."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--summary',type=Path,required=True)
    ap.add_argument('--low',type=int,required=True)
    ap.add_argument('--high',type=int,required=True)
    ap.add_argument('components',nargs='+',type=Path)
    a=ap.parse_args()
    rows=[]
    for p in a.components:
        z=json.loads(p.read_text(encoding='utf-8'))
        row={
          'path':str(p),'sha256':sha256(p),'low':str(z['low']),'high':str(z['high']),
          'integers_tested_x':int(z['integers_tested_x']),'integers_tested_y':int(z['integers_tested_y']),
          'candidate_count_x':int(z['candidate_count_x']),'candidate_count_y':int(z['candidate_count_y']),
          'complete_gapless_independent_crosscheck':bool(z['complete_gapless_independent_crosscheck']),
          'mismatches':list(z['mismatches']),
          'unordered_square_pairs_enumerated_x':int(z['unordered_square_pairs_enumerated_x']),
          'unordered_square_pairs_enumerated_y':int(z['unordered_square_pairs_enumerated_y']),
          'chunk_count_x':int(z['chunk_count_x']),'chunk_count_y':int(z['chunk_count_y']),
        }
        rows.append(row)
    rows.sort(key=lambda r:int(r['low']))
    errors=[]
    if not rows or int(rows[0]['low'])!=a.low or int(rows[-1]['high'])!=a.high: errors.append('endpoint_mismatch')
    for i,r in enumerate(rows):
        expected=int(r['high'])-int(r['low'])+1
        if r['integers_tested_x']!=expected or r['integers_tested_y']!=expected: errors.append(f'component[{i}]:tested_count')
        if not r['complete_gapless_independent_crosscheck'] or r['mismatches']: errors.append(f'component[{i}]:not_complete')
        if r['candidate_count_x']!=0 or r['candidate_count_y']!=0: errors.append(f'component[{i}]:nonzero_candidates')
        if r['unordered_square_pairs_enumerated_x']!=r['unordered_square_pairs_enumerated_y']: errors.append(f'component[{i}]:lattice_pair_mismatch')
        if r['chunk_count_x']!=r['chunk_count_y']: errors.append(f'component[{i}]:chunk_count_mismatch')
        if i and int(rows[i-1]['high'])+1!=int(r['low']): errors.append(f'gap_or_overlap_before_component[{i}]')
    total=a.high-a.low+1
    tx=sum(r['integers_tested_x'] for r in rows); ty=sum(r['integers_tested_y'] for r in rows)
    if tx!=total or ty!=total: errors.append('aggregate_tested_count')
    payload={
      'schema':'a303656-direct-two-squares-component-aggregate-v1',
      'low':str(a.low),'high':str(a.high),'component_count':len(rows),
      'chunk_count_x':sum(r['chunk_count_x'] for r in rows),
      'chunk_count_y':sum(r['chunk_count_y'] for r in rows),
      'integers_tested_x':tx,'integers_tested_y':ty,
      'candidate_count_x':sum(r['candidate_count_x'] for r in rows),
      'candidate_count_y':sum(r['candidate_count_y'] for r in rows),
      'unordered_square_pairs_enumerated_x':sum(r['unordered_square_pairs_enumerated_x'] for r in rows),
      'unordered_square_pairs_enumerated_y':sum(r['unordered_square_pairs_enumerated_y'] for r in rows),
      'complete_gapless_independent_crosscheck':not errors,'validation_errors':errors,
      'components':rows,
      'classification':('INDEPENDENTLY REPRODUCIBLE EXACT EXHAUSTIVE FINITE COMPUTATION: EVERY n IN INTERVAL HAS A REPRESENTATION' if not errors else 'INCOMPLETE OR MISMATCHED'),
    }
    a.summary.parent.mkdir(parents=True,exist_ok=True)
    a.summary.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(f"component_count={len(rows)}")
    print(f"chunk_count_x={payload['chunk_count_x']}")
    print(f"chunk_count_y={payload['chunk_count_y']}")
    print(f"integers_tested_x={tx}")
    print(f"integers_tested_y={ty}")
    print(f"candidate_count_x={payload['candidate_count_x']}")
    print(f"candidate_count_y={payload['candidate_count_y']}")
    print(f"complete_gapless_independent_crosscheck={str(not errors).lower()}")
    if errors: print('validation_errors='+','.join(errors))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
