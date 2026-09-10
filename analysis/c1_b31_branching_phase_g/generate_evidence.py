#!/usr/bin/env python3
"""Optional evidence regeneration (requires SymPy), not the trusted verifier.

Run in a scratch output directory:
  python generate_evidence.py --output-dir /tmp/b31g-regenerated
  python verify.py --evidence /tmp/b31g-regenerated/evidence.json

Only complete Lucas certificates accepted by verify.py establish primality.
This script builds the five fixtures; it is not a base-5 emptiness search.
"""
from pathlib import Path
import argparse
import json, math, itertools, time
import sympy as sp

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, required=True)
args=parser.parse_args()
ROOT=args.output_dir
ROOT.mkdir(parents=True, exist_ok=True)
A=878851; B=625552508473588471
certs={}
def factors(n):return {int(p):int(e) for p,e in sp.factorint(n).items()}
def certify(p):
 p=int(p)
 if str(p) in certs:return
 if p==2:certs['2']={'p':'2','factors':{},'witness':None};return
 fac=factors(p-1)
 for r in fac:certify(r)
 for g in range(2,10000):
  if pow(g,p-1,p)==1 and all(math.gcd(pow(g,(p-1)//r,p)-1,p)==1 for r in fac):break
 else:raise RuntimeError('no Lucas witness')
 certs[str(p)]={'p':str(p),'factors':{str(r):e for r,e in fac.items()},'witness':g}

def row(base,p,n):
 certify(p)
 fac=factors(n)
 for l in fac:certify(l)
 if pow(base,n,p)!=1 or any(pow(base,n//l,p)==1 for l in fac):raise RuntimeError('bad order')
 s=1
 while pow(base,n,p**(s+1))==1:s+=1
 return {'p':str(p),'order':str(n),'order_factors':{str(l):e for l,e in fac.items()},'valuation':s,
         'first_nonzero_lift':str((pow(base,n,p**(s+1))-1)//p**s),
         'residue_mod_p':str(base%p),'residue_mod_p2':str(base%(p*p))}

def leg(a,p):
 z=pow(a,(p-1)//2,p)
 return -1 if z==p-1 else z

def closure_record(name,base,ps,orders,base_prime=False,extra=None):
 if base_prime:certify(base)
 rows=[row(base,p,n) for p,n in zip(ps,orders)]
 root=ps[-1]; edges=[]
 for p,n in zip(ps,orders):
  for t in factors(n):
   if t!=3:
    edges.append({'upper':str(p),'lower':str(t),'lower_over_upper':leg(t,p),'upper_over_lower':leg(p,t)})
 R=set(ps[:-1]);targets={int(e['lower']) for e in edges if int(e['upper']) in R}
 maxima=sorted(R-targets)
 return {'name':name,'base':str(base),'base_is_certified_prime':base_prime,'is_base5_member':False,
         'root':str(root),'proper_state':[str(p) for p in ps[:-1]],'maximal_generators':[str(p) for p in maxima],
         'maximal_symbol_product':math.prod(leg(a,root) for a in maxima),
         'rows':rows,'terminal3':row(base,3,2),'edges_excluding_terminal3':edges,
         'extra':extra or {}}

# Actual base-5 reference rows, not claimed new.
actual_ps=[31,A,B,490398859,48486209671,268987578643643042531]
actual_ns=[3,93,31,81733143,2636553,B]
actual_rows=[row(5,p,n) for p,n in zip(actual_ps,actual_ns)]

# Model 1: certified prime base; all residues modulo every vertex prime equal 5.
base1=171647557511869913
M1=4*9*31**2; q=A;n=93
K=(pow(5,n,q*q)-1)//q
h=(-K*pow(M1*n*pow(5,-1,q),-1,q))%q
b0=5+M1*q*h;period=M1*q*q
models=[closure_record('odd_antichain_prime_base_same_first_order_as_5',base1,[31,A],[3,93],True,
 {'preserved_modulus':str(M1),'original_base':'5','q_order_at_base5':93,'q_valuation_at_base5':1,
  'base5_first_lift':K,'hensel_digit_in_Mq_parameter':h,'least_lifted_base':str(b0),
  'progression_modulus':str(period),'progression_step':6})]

# A strengthened odd-antichain fixture also preserves the base-5 residue modulo 8.
base1strong=679350864025912037
models.append(closure_record('odd_antichain_prime_base_also_preserves_mod8',base1strong,[31,A],[3,93],True,
 {'preserved_modulus':str(8*9*31**2),'original_base':'5','q_order_at_base5':93,'q_valuation_at_base5':1,
  'root_first_order_equals_base5':True,'progression_modulus':str(period),'progression_step':25,
  'least_lifted_base':str(b0)}))

# Model 2: actual base-5 proper fork retained modulo p^2; newly chosen prime terminal.
n=A*B
for k in range(1,100000,2):
 q=1+2*k*n
 if q%20 in (11,19) and sp.isprime(q):break
else:raise RuntimeError('no terminal prime found')
certify(q);qf=factors(q-1)
for g in range(2,1000):
 if all(pow(g,(q-1)//l,q)!=1 for l in qf):break
u=pow(g,(q-1)//n,q)
omega=pow(u,q,q*q)
M2=8*9*(31*A*B)**2
base2=5+M2*((omega-5)*pow(M2,-1,q*q)%(q*q))
if pow(base2,n,q**3)==1:base2+=M2*q*q
model2=closure_record('even_antichain_preserves_actual_base5_proper_fork',base2,[31,A,B,q],[3,93,31,n],False,
 {'preserved_modulus':str(M2),'k':k,'primitive_generator_mod_q':g,'u_mod_q':str(u),
  'teichmuller_mod_q2':str(omega),'regular_comparator_base':str(base2+M2*q),
  'root_base5_full_order_residue':str(pow(5,n,q)),
  'terminal_first_order_equals_base5':u==5%q})
models.append(model2)

# Model 3: a true three-generator fork in a variable base; small actual prime labels.
relays=[311,2791,3659]
n=math.prod(relays)
for k in range(1,100000,2):
 q=1+2*k*n
 if q%20 in (11,19) and sp.isprime(q):break
ps=[31]+relays+[q];orders=[3]+[31]*3+[n]
congruences=[(5,8*9),(5,31**2)]
for p in relays:
 fac=factors(p-1)
 for g in range(2,p):
  if all(pow(g,(p-1)//l,p)!=1 for l in fac):break
 u=pow(g,(p-1)//31,p)
 if pow(u,31,p*p)==1:u+=p
 congruences.append((u,p*p))
fac=factors(q-1)
for g in range(2,1000):
 if all(pow(g,(q-1)//l,q)!=1 for l in fac):break
u=pow(g,(q-1)//n,q);omega=pow(u,q,q*q)
congruences.append((omega,q*q))
b=0;mod=1
for residue,m in congruences:
 b+=mod*((residue-b)*pow(mod,-1,m)%m);mod*=m
if pow(b,n,q**3)==1:b+=mod
models.append(closure_record('three_generator_fork_variable_base',b,ps,orders,False,
 {'crt_congruences':[[str(a),str(m)] for a,m in congruences],'period':str(mod),'k':k}))

# Model 4: first-order base-5 serial/transitive edges retained at every prime.
ps=[31,A,490398859];orders=[3,93,81733143];q=ps[-1];n=orders[-1]
M=8*9*(31*A)**2
K=(pow(5,n,q*q)-1)//q
h=(-K*pow(M*n*pow(5,-1,q),-1,q))%q
b=5+M*q*h
if pow(b,n,q**3)==1:b+=M*q*q
models.append(closure_record('transitive_edge_same_first_order_as_5',b,ps,orders,False,
 {'preserved_modulus':str(M),'base5_first_lift':str(K),'hensel_digit_in_Mq_parameter':str(h)}))

payload={'schema':'a303656-b31-phase-g-evidence-v1','actual_base5_rows_inherited_then_recertified':actual_rows,
         'countermodels':models,'lucas_certificates':certs}
(ROOT/'evidence.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')

print('certificates',len(certs))
for m in models:
 print(m['name'],'BASE',m['base'],'Q',m['root'],'A',m['maximal_generators'],'s',[r['valuation'] for r in m['rows']],'prod',m['maximal_symbol_product'])
print('actualrows',len(actual_rows))
