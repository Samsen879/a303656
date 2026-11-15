from math import gcd,lcm,prod,isqrt
from fractions import Fraction as F
from collections import Counter
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
primes=[3,5,7,11,13,17,19]
def smooth(n):
 for p in primes:
  while n%p==0:n//=p
 return n==1
hs=[n for n in range(1,512,2) if smooth(n)]
P3=prod(3**(2*h)-1 for h in hs);P5=prod(5**(2*h)-1 for h in hs)
g=gcd(P3,P5)
def factor(n):
 out={};d=2
 while d*d<=n:
  if n%d==0:
   e=0
   while n%d==0:n//=d;e+=1
   out[d]=e
  d=3 if d==2 else d+2
 if n>1:out[n]=1
 return out
fac=factor(g)
assert prod(p**e for p,e in fac.items())==g
assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in fac)
def order(b,p):
 x=b%p;k=1
 while x!=1:x=x*b%p;k+=1
 return k
rows=[]
for p in fac:
 if p<=3 or p%4!=3:continue
 a,b=order(3,p),order(5,p)
 h3=a//gcd(a,2);h5=b//gcd(b,2);H=max(h3,h5)
 maxorderprime=max(factor(lcm(a,b)))
 w=F(1,H)
 if p in [11,71,271]:
  maxima=[]
  for e in range(2):
   for f in range(2):
    c=Counter((pow(3,e+2*i,p)+pow(5,f+2*j,p))%p for i in range(h3) for j in range(h5))
    maxima.append(max(c.values()))
  w=F(max(maxima),h3*h5)
 rows.append({'p':p,'o3':a,'o5':b,'H':H,'M':maxorderprime,'w':w})
assert len(hs)==80 and len(str(g))==613 and len(fac)==60 and len(rows)==46
assert [(r['p'],r['w']) for r in rows if r['p'] in [11,71,271]]==[(11,F(3,25)),(71,F(4,175)),(271,F(1,81))]
K=22;tau=F(1,512)
def top(weights,k):return sum(sorted(weights+[tau]*k,reverse=True)[:k],F(0))
base=F(1,3)+top([r['w'] for r in rows if r['p']>7 and r['M']<=7],K)
budgets=[{'M':7,'t':'base','budget':base}]
for M in [11,13,17,19]:
 core=sum((r['w'] for r in rows if 7<=r['p']<=M),F(0))-F(1,25)
 active=[r['w'] for r in rows if r['p']>M and r['M']==M]
 inactive=[r['w'] for r in rows if r['p']>M and r['M']<M]
 for t in range(M,K+1):
  B=core+top(active,t)+top(inactive,K-t)
  budgets.append({'M':M,'t':t,'budget':B})
assert len(budgets)==33 and all(x['budget']<1 for x in budgets)
maximum=max(budgets,key=lambda x:x['budget'])
print('catalog:',len(hs),'smooth exponents,',len(fac),'prime factors,',len(rows),'inert rows')
print('budgets:',len(budgets),'all strictly <1')
print('base:',base)
print('maximum:',maximum,'slack',1-maximum['budget'])
assert base==F(155932663,190512000)
assert maximum['M']==11 and maximum['t']==11 and maximum['budget']==F(4238011529,4390848000)
assert 1-maximum['budget']==F(152836471,4390848000)
# Check independence directly on the four possible parity cylinders.
for e in range(2):
 for f in range(2):
  counts7=Counter((pow(3,e+2*i,7)+pow(5,f+2*j,7))%7 for i in range(3) for j in range(3))
  counts11=Counter((pow(3,e+2*i,11)+pow(5,f+2*j,11))%11 for i in range(5) for j in range(5))
  both=Counter(((pow(3,e+2*i,7)+pow(5,f+2*j,7))%7,(pow(3,e+2*i,11)+pow(5,f+2*j,11))%11) for i in range(15) for j in range(15))
  assert all(both[(a,b)]==counts7[a]*counts11[b] for a in range(7) for b in range(11))
  assert max(F(counts7[a],9)+F(counts11[b],25)-F(both[(a,b)],225) for a in range(7) for b in range(11))<=F(31,75)
print('direct 225-cell joint independence checks: four parity pairs PASS')
obj={'status':'PASS','target_budget':22,'catalog_counts':{'h':len(hs),'gcd_digits':len(str(g)),'factors':len(fac),'inert':len(rows)},'core_union_bound':'31/75','old_core_bound':'34/75','maximum':{**maximum,'budget':str(maximum['budget']),'slack':str(1-maximum['budget'])},'budgets':[{**r,'budget':str(r['budget']),'slack':str(1-r['budget'])} for r in budgets],'catalog':[{**r,'w':str(r['w'])} for r in rows]}
(OUT/'c22_independent_budget.json').write_text(json.dumps(obj,indent=2)+'\n')
