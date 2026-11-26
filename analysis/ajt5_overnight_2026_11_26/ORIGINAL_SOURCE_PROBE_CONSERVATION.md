# Counting original sources at native-safe CRT probes

Fix full CRT probes satisfying the actual conditioning and passing every native or separately accounted-for test in the panel. If exact projection closes their retained phases, each probe must be hit by some original surviving source. Assign nonnegative weights to probes with the total weight hit by each one original source at most one. The number of distinct sources required to close the probes is at least the total weight, by summing over the original cover. This argument works with nonlinear contractions, because it is evaluated before projection; inherited pieces with the same origin never create new capacity. A source label can be essential to several projected pieces when it hits different relevant lifts, so a matching claim also needs explicit probe separation.

In the actual fixed-c 19/43 chart, the two safe strips at x=d mod 9 equal to 0 and 1 are respectively t=d mod 19 fixed at 0 with s=d mod 43 free, and s fixed at 22 with t free. If at most 16 original rigid sources are eligible, choose each other-axis digit outside all of their first-digit reads. If fully blind origins are inactive at these probes, closing both strips requires distinct original source types: one reads 19 but not 43 with its center at 0, the other reads 43 but not 19 with its center at 22.

In the narrower subfamily where every eligible original reads both axes with one fixed first-digit pair, the two strips contain 61 distinct pairs. Select one probe per pair. Each origin hits at most one; at least 61 origins are required. If every such origin also reads the first ternary digit, both probes at the intersection pair are distinguishable, giving 62. This does not replace the unrestricted minimum-source theorem.

An independent control uses four ordinary arithmetic rows at a represented target, with one synthetic origin on the two private digits. Coupling the allowed private states yields two projected strips with the same essential origin. Releasing those digits independently restores an escape on each strip. Thus original-label conservation holds, but the distinct-source matching does not transfer automatically across new conditioning. Details and raw-power checks follow.

```python
from itertools import product
from math import prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

def bad(n,q,d):
    r = (n-3-pow(5,d,q*q)) % (q*q)
    return r!=0 and r%q==0

u = 1749240030127890765912351734436595992951490159
v = 1808434766219862061671534508108331483094094788
n = 28+u*u+v*v
P = [(0,0,s) for s in range(43)] + [(1,t,22) for t in range(19)]
for x,t,s in P:
    d = crt([(0,2),(x,9),(2,5),(1,7),(t,19),(s,43)])
    assert all(not bad(n,q,d) for q in (3,7,11,19,43,1171,251,211,20771))
assert len(P)==62 and len({(t,s) for _,t,s in P})==61

# Independent represented target with four ordinary rows.
R = [(7,6,(2,3),2,3,8),(11,5,(5,),44,2,2),
     (19531,7,(7,),2,0,23014323),(67,22,(2,11),0,0,0)]
u = crt([(1,4)]+[(a,q*q) for q,_,_,_,a,_ in R])
v = crt([(0,4)]+[(b,q*q) for q,_,_,_,_,b in R])
n = 4+u*u+v*v
for q,w,f,e,_,_ in R:
    assert pow(5,w,q)==1 and all(pow(5,w//p,q)!=1 for p in f)
    assert pow(5,w,q*q)!=1 and (n-3-pow(5,e,q*q))%(q*q)==0

def safe(x,y,t,s,a,b,C=True):
    d = crt([(0,2),(x,3),(y,5),(t,7),(s,11),(a,19531),(b,67)])
    real = tuple(bad(n,q,d) for q,*_ in R)
    assert real==(x==2 and t!=2,y==4 and s!=0,t==2 and a!=2,s==0 and b!=0)
    return not (any(real) or (C and (a,b)==(2,0)))

for x,y,escape in ((2,0,(2,1,2,1)), (0,4,(3,0,3,0))):
    assert all(not safe(x,y,t,s,a,b)
               for t,s in product(range(7),range(11))
               for a,b in ((2,0),(3,1)))
    assert safe(x,y,*escape)
    assert safe(x,y,2,0,2,0,False)
print("PASS")
```
