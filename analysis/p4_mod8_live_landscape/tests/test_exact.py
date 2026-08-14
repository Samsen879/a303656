#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 s=importlib.util.spec_from_file_location(name,ROOT/'tools'/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=load('enumerator_a');B=load('enumerator_b')
pa=A.domain();pb=B.make_pairs()
assert pa==pb and len(pa)==407 and pa[-1][:2]==(23,15)
assert [(c,d) for c,d,s in pa if s==28]==[(1,2),(3,0)]
dead=[x for x in pa if x[0]%2 and x[1]%2==0];live=[x for x in pa if x not in dead]
assert len(dead)==107 and len(live)==300
assert 12*9-1==107
squares={(a*a+b*b)%8 for a in range(8) for b in range(8)}
assert 6 not in squares
for c,d,s in dead:assert (2-pow(3,c,8)-pow(5,d,8))%8==6
for p in A.PRIMES:
 am=A.prime_masks(pa,p);lm=B.build(live,p);dm=B.build(dead,p)
 assert len(am)==p*p and len(lm)==p*p and len(dm)==p*p
print('exact unit tests: PASS')
