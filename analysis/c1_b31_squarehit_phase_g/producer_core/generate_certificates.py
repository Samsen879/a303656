"""One-time small certificate construction; not a target-prime scan."""
from pathlib import Path
from math import gcd
import json, sympy as sp
OUT=Path(__file__).parent
certs={}
def certify(n):
    n=int(n)
    if str(n) in certs:return
    if n==2:
        certs['2']={'n':2,'factors':{},'witness':None};return
    fs={int(p):int(e) for p,e in sp.factorint(n-1).items()}
    for p in fs:certify(p)
    a=2
    while not(pow(a,n-1,n)==1 and all(gcd(pow(a,(n-1)//p,n)-1,n)==1 for p in fs)):
        a+=1
        if a>10000:raise RuntimeError('No Lucas witness within construction budget')
    certs[str(n)]={'n':n,'factors':{str(p):e for p,e in sorted(fs.items())},'witness':a}
nums=[2,3,5,7,11,13,17,19,23,29,31,93,878851,625552508473588471,490398859,20771,40487,53471161,1645333507,6692367337,188748146801,1861,148429,172974812463239310024750410929]
# The composite index 93 is not a requested primality claim.
for n in nums:
    if n!=93: certify(n)
orders=[10385,40486,13367790,1645333506,6692367336,11796759175]
for n in orders:
    for p in sp.factorint(n):certify(p)
obj={'schema':'recursive-full-n-minus-one-Lucas-v1','construction':'SymPy factorint used only to propose factors; all claims replay with Python standard library and Lucas theorem. No prime candidate scan.','certificates':certs,'known_orders':{str(q):{'order':int(sp.n_order(5,q)),'order_factors':{str(p):int(e) for p,e in sp.factorint(int(sp.n_order(5,q))).items()}} for q in [20771,40487,53471161,1645333507,6692367337,188748146801]}}
(OUT/'certificates.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print('certificates',len(certs))
