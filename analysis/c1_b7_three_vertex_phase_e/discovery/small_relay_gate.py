"""Exact bounded relay inventory, not a global Wieferich scan."""
from pathlib import Path
from math import isqrt
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from exact_arithmetic import factor_small
B=2287;eligible=set();rows=[]
for p in range(7,B+1,4):
 if any(p%d==0 for d in range(2,isqrt(p)+1)):continue
 w=p-1
 for ell in factor_small(p-1):
  while w%ell==0 and pow(5,w//ell,p)==1:w//=ell
 s=1
 while pow(5,w,p**(s+1))==1:s+=1
 f=factor_small(w);odd={q for q in f if q>2}
 regular=s==1;squarefree=all(e==1 for e in f.values())
 good=regular and squarefree and (p==7 or (bool(odd-{3}) and odd<={3}|eligible))
 if good:eligible.add(p)
 rows.append({'p':p,'w':w,'s':s,'order_factors':f,'regular_B7_compatible_basin':good})
assert eligible=={7,43,127,379,2287}
(Path(__file__).resolve().parent/'small_relay_inventory_rebuilt.json').write_text(json.dumps({'bound_inclusive':B,'prime_count':len(rows),'eligible':sorted(eligible),'rows':rows},indent=2))
print('PASS',len(rows),'admitted primes; eligible',sorted(eligible))
print('2287 lifting', (pow(5,254,2287**2)-1)//2287)
