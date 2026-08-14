#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BIN=Path(os.environ.get('A303656_BIN', ROOT/'bin'))
sys.path.insert(0,str(ROOT/'src'))
from common import enumerate_pairs, exact_one_obstructs, valuation

# Exact domain enumeration and p=3 edge.
p3,p5,pairs=enumerate_pairs(5)
assert p3==[1,3]
assert p5==[1,5]
assert [(x.c,x.d,x.shift) for x in pairs]==[(0,0,2),(1,0,4)]
assert exact_one_obstructs(3,3) and valuation(3,3)==1
assert not exact_one_obstructs(9,3)
assert not exact_one_obstructs(0,3)
print('synthetic_restricted_instance: n=5, sole shift=2, p=3, v=1: PASS')

# The theorem verifier must reject the same n because the full domain also has shift 4.
py=[sys.executable,str(ROOT/'src/verifier.py'),'--n','5','--primes','3','--quiet-pairs']
assert subprocess.run(py,capture_output=True,text=True).returncode==1
cpp=[str(BIN/'verifier_gmp'),'--n','5','--primes','3','--quiet-pairs']
assert subprocess.run(cpp,capture_output=True,text=True).returncode==1

# Remainder zero must be rejected independently.
assert subprocess.run([sys.executable,str(ROOT/'src/verifier.py'),'--n','2','--primes','3','--quiet-pairs'],capture_output=True).returncode==1
assert subprocess.run([str(BIN/'verifier_gmp'),'--n','2','--primes','3','--quiet-pairs'],capture_output=True).returncode==1

# Deliberately incomplete assignment must be rejected.
with tempfile.TemporaryDirectory() as td:
    f=Path(td)/'bad.csv';f.write_text('c,d,prime\n0,0,3\n')
    cp=subprocess.run([sys.executable,str(ROOT/'src/verifier.py'),'--n','5','--primes','3','--assignment',str(f),'--quiet-pairs'],capture_output=True,text=True)
    assert cp.returncode==1 and 'assignment missing 1 admissible pairs' in cp.stdout

# The completed toy method records agree on no candidate in [2,50].
a=json.loads((ROOT/'output/toy_small_method_a.json').read_text())
b=json.loads((ROOT/'output/toy_small_method_b.json').read_text())
c=json.loads((ROOT/'output/toy_small_method_c.json').read_text())
assert a['records'][0]['result']=='unsat'
assert b['termination']=='solver_unsat_without_proof_object'
assert c['candidate_count']==0 and c['integers_tested']==49
print('toy_method_A_B_C_agreement_on_[2,50]: PASS')
print('ALL_TOY_TESTS_PASS')
