#!/usr/bin/env python3
"""Fail-closed mutation tests for the standalone arithmetic verifier."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parent
cases={
 'invalid_Lucas_witness':lambda d:d['prime_certificates']['268987578643643042531'].__setitem__('a',1),
 'wrong_exact_order':lambda d:d['nodes']['3326871479'].__setitem__('order','19530'),
 'nonadmitted_promoted':lambda d:d['nodes']['38678701'].__setitem__('admitted',True),
 'wrong_CRT_head_residue':lambda d:d['conditional_fixture']['rows'][1].__setitem__('r_mod_h2',34),
 'overstated_lower_bound_scope':lambda d:d['terminal_lower_bounds']['7'].__setitem__('scope','all exactly-seven systems'),
 'invented_complete_certificate':lambda d:d['conditional_fixture'].__setitem__('full_actual_certificate',True),
}
results=[]
for name,mutate in cases.items():
 with tempfile.TemporaryDirectory(prefix='chain_mutation_') as td:
  t=Path(td)
  for folder in ['search','replay_search','cofactors']:shutil.copytree(R/folder,t/folder)
  for fn in ['verify.py','large31_independent_replay.json']:shutil.copy(R/fn,t/fn)
  d=json.loads((R/'evidence.json').read_text());mutate(d);(t/'evidence.json').write_text(json.dumps(d))
  p=subprocess.run([sys.executable,str(t/'verify.py')],capture_output=True,text=True)
  if p.returncode==0:raise RuntimeError('mutation escaped: '+name)
  results.append({'case':name,'status':'REJECTED_AS_REQUIRED','last_error':p.stderr.strip().splitlines()[-1]})
print(json.dumps({'mutation_tests':results,'passed':len(results)},indent=2))
