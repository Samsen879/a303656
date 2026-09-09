"""Fixed 48-index, k<=10000 exact-order divisor discovery; NOT a general prime scan."""
import json,time
from pathlib import Path
import sympy as S
P=Path(__file__).resolve().parent;rs=[43,127,379,7603,19531,519499];ts=[1,2,3,6,7,14,21,42]
rows=[];start=time.monotonic()
for r in rs:
 for t in ts:
  n=r*t;counts=0;hits=[];ps=list(S.factorint(n))
  for k in range(1,10001):
   q=k*n+1
   if q%2==0 or q%5==0:continue
   counts+=1
   if pow(5,n,q)!=1:continue
   if not S.isprime(q):continue
   if any(pow(5,n//int(p),q)==1 for p in ps):continue
   s=1
   while pow(5,n,q**(s+1))==1:s+=1
   hits.append({'q':str(q),'k':k,'q_mod_4':q%4,'exact_order':n,'s':s})
  rows.append({'r':r,'n':n,'k_max':10000,'tested_odd_not5_candidates':counts,'prime_hits':hits})
  print(r,n,'hits',[(h['q'],h['s']) for h in hits],flush=True)
(P/'all48_probe.json').write_text(json.dumps(rows,indent=2))
print('elapsed',time.monotonic()-start)
