from math import prod,gcd,isqrt,lcm
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json,sys,time,hashlib
sys.set_int_max_str_digits(100000)
start=time.monotonic()
small=(3,5,7,11,13,17,19)
def smooth_odd(h):
    u=h
    for p in small:
        while u%p==0:u//=p
    return u==1
hs=[h for h in range(1,512,2) if smooth_odd(h)]
assert len(hs)==80
p3=prod(3**(2*h)-1 for h in hs)
p5=prod(5**(2*h)-1 for h in hs)
g=gcd(p3,p5)
# Determine prime factors by an ordinary sieve and exact division, without
# trusting the report's 60-factor list or any probabilistic primality result.
cap=120000
prime=bytearray(b'\x01')*(cap+1)
prime[:2]=b'\x00\x00'
for n in range(2,isqrt(cap)+1):
    if prime[n]:prime[n*n:cap+1:n]=b'\x00'*(((cap-n*n)//n)+1)
fac={};left=g
for p in range(2,cap+1):
    if prime[p] and left%p==0:
        e=0
        while left%p==0:left//=p;e+=1
        fac[p]=e
assert left==1
assert prod(p**e for p,e in fac.items())==g
assert len(fac)==60 and len(str(g))==613
def order(b,p):
    t=1;z=b%p
    while z!=1:z=z*b%p;t+=1
    return t
def odd(n):
    while n%2==0:n//=2
    return n
def lpf(n):
    k=1
    for p in range(2,isqrt(n)+1):
        while n%p==0:k=p;n//=p
    return max(k,n)
catalog=[]
for p in fac:
    if p>3 and p%4==3:
        a=order(3,p);b=order(5,p);h=max(odd(a),odd(b));m=lpf(lcm(a,b))
        assert h<512 and m<=19
        w=F(1,h)
        if p in (11,71,271):
            mx=0;counts=[]
            for e in range(2):
                aa=[pow(3,e+2*i,p) for i in range(odd(a))]
                for f in range(2):
                    bb=[pow(5,f+2*j,p) for j in range(odd(b))]
                    ct=Counter((x+y)%p for x in aa for y in bb)
                    counts.append(max(ct.values()));mx=max(mx,max(ct.values()))
            w=F(mx,odd(a)*odd(b))
            assert w=={11:F(3,25),71:F(4,175),271:F(1,81)}[p]
        catalog.append(dict(p=p,ord3=a,ord5=b,H=h,M=m,weight=w))
assert len(catalog)==46
tau=F(1,512)
def top(k,rows):
    return sum(sorted([r['weight'] for r in rows]+[tau]*k,reverse=True)[:k],F(0))
def core(m):return sum((r['weight'] for r in catalog if 7<=r['p']<=m),F(0))
budgets=[]
base=core(7)+top(21,[r for r in catalog if r['p']>7 and r['M']<=7])
budgets.append(dict(M=7,t='base',bound=base,slack=1-base))
for m in (11,13,17,19):
    active=[r for r in catalog if r['p']>m and r['M']==m]
    inactive=[r for r in catalog if r['p']>m and r['M']<m]
    for t in range(m,22):
        val=core(m)+top(t,active)+top(21-t,inactive)
        budgets.append(dict(M=m,t=t,bound=val,slack=1-val))
assert len(budgets)==29 and all(r['bound']<1 for r in budgets)
tight=max(budgets,key=lambda r:r['bound'])
assert tight['bound']==F(875703733,878169600)
bound22=core(11)+top(11,[r for r in catalog if r['p']>11 and r['M']==11])+top(11,[r for r in catalog if r['p']>11 and r['M']<11])
assert bound22==F(4413645449,4390848000)>1
result=dict(smooth_orders=hs,product3_digits=len(str(p3)),product5_digits=len(str(p5)),gcd=str(g),factors=fac,catalog=catalog,budgets=budgets,bound22=bound22,seconds=time.monotonic()-start)
out=Path(__file__).with_name('root_c21_results.json')
out.write_text(json.dumps(result,default=str,indent=2)+'\n')
print(json.dumps(dict(h_count=len(hs),factor_count=len(fac),catalog_count=len(catalog),gcd_digits=len(str(g)),largest_factor=max(fac),budget_count=len(budgets),tight=tight,bound22=bound22,seconds=result['seconds'],sha256=hashlib.sha256(out.read_bytes()).hexdigest()),default=str,indent=2))
