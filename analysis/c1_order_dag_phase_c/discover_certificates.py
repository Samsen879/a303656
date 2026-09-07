"""Discovery only. The separate reference.py verifies every output exactly."""
from pathlib import Path
from math import prod
import sympy as sp
import json
ROOT=Path(__file__).resolve().parent
indices=[3,6,9,18,27,54,81,162,5,10,25,50,7,14,11,22,15,30,45,90]
x=sp.Symbol('x')
A=11419697846380955982026777206637491
B=2066067271380136212224701233463
hints={
 A:{2:1,3:4,5:1,159701:1,614267:1,143715885159696840787:1},
 B:{2:1,3:4,2029:1,10562011:1,158143499:1,3763131871:1},
 143715885159696840787:{2:1,3:1,41:1,584210915283320491:1},
 584210915283320491:{2:1,3:1,5:1,11:1,1770336106919153:1},
 1770336106919153:{2:4,126949:1,871578403:1},
 871578403:{2:1,3:1,79:1,1838773:1},
}
polys={}
for n in indices:
 value=int(sp.cyclotomic_poly(n,x).subs(x,5))
 fs={4861:1,A:1} if n==81 else {3:1,1783:1,5023:1,B:1} if n==162 else {int(p):int(e) for p,e in sp.factorint(value).items()}
 assert prod(p**e for p,e in fs.items())==value
 polys[str(n)]={'value':str(value),'factors':{str(p):e for p,e in fs.items()}}
 print('cyclotomic',n,flush=True)
# Build the exact absolute order-DAG for just the three authenticated source roots.
orders={}
def visit(q):
 if q in orders:return
 w=int(sp.n_order(5,q)); fs={int(p):int(e) for p,e in sp.factorint(w).items()}
 orders[q]={'order':w,'factors':fs}
 for p in fs:
  if p>3 and p%4==3:visit(p)
for q in [20771,40487,1645333507]:visit(q)
orders[3]={'order':2,'factors':{2:1}}
certs={}
def certify(n):
 if str(n) in certs:return
 if n==2:
  certs['2']={'base':1,'n_minus_1_factors':{}};return
 fs=hints.get(n) or {int(p):int(e) for p,e in sp.factorint(n-1).items()}
 assert prod(p**e for p,e in fs.items())==n-1
 for p in fs:certify(p)
 for a in range(2,1000):
  if pow(a,n-1,n)==1 and all(pow(a,(n-1)//p,n)!=1 for p in fs):break
 else:raise RuntimeError(('No Lucas generator found',n))
 certs[str(n)]={'base':a,'n_minus_1_factors':{str(p):e for p,e in fs.items()}}
for item in polys.values():
 for p in item['factors']:certify(int(p))
for q,row in orders.items():
 certify(q)
 for p in row['factors']:certify(p)
(ROOT/'arithmetic_inputs.json').write_text(json.dumps({'cyclotomics':polys,'order_dag':orders,'primality_certificates':certs},indent=2,sort_keys=True)+'\n')
print('DONE',len(certs),'prime certificates',len(orders),'DAG vertices')
