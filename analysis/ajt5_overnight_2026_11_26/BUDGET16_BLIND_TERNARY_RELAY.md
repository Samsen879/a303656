# A blind source can acquire a ternary guard through ordinary relays

The budget-16 analysis retains a difficult lower-only class with a guard consisting of one residue modulo 9. A direct rigid order 9 or 18 is excluded by its squarefree cyclotomic product. The relevant induced guard passes through the actual row-19 order guard. Being blind to 19 and 43 in the original order is not enough to exclude that induced guard.

The replay constructs a represented target with c=1 and even d, the row-7 guard at d=2 mod 3, the row-11 guard at d=4 mod 5, and the row-19 guard at d=0 mod 9. With x=d mod 9, t=d mod 19 and a=d mod 191, the exact ordinary vetoes are x=0 and t!=0 for reader 19; t=0 and a!=0 for reader 191; a=0 for reader 383 after its own ordinary digit is frozen off center. The exact orders of 19,191,383 are 9,19,382 respectively. Projecting a first gives t=0, then projecting t gives x=0. The origin reads neither 19 nor 43, but every native-safe lift on the displayed 19-center strip must use a=0, and hence is hit by the pinned origin. Releasing the origin's private digit restores a safe lift. Changing only the last reader's target modulo 383² so that it reads a=1 instead is a separate failure control that preserves the other observations.

A genuine rigid origin for the shortest route would need its actual order and logarithm to match the 191-center, as well as a positive odd valuation below the relevant lifting depth and the required common exception condition. Longer routes must align the actual phases and centers at each contraction. No genuine rigid origin is provided by the ordinary example. In the original budget the exposed row-19 guard can still cost 12 of the endangered 36 units of size 1/135. This probe argument alone cannot reclaim those units or improve the 17-source threshold.

```python
from itertools import product
from math import prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

P = 12*31*71*5167*19531
fixed = [(7,6,(2,3),2,3,8),(11,5,(5,),44,2,2),(19,9,(3,),0,0,0),
         (43,42,(2,3,7),22,1,1167),(191,19,(19,),0,0,0)]

def target(e,u0,v0):
    R = fixed+[(383,382,(2,191),e,u0,v0)]
    u = crt([(3,P)]+[(a,q*q) for q,_,_,_,a,_ in R])
    v = crt([(8,P)]+[(b,q*q) for q,_,_,_,_,b in R])
    n = 4+u*u+v*v
    for q,w,fs,h,_,_ in R:
        assert pow(5,w,q)==1 and pow(5,w,q*q)!=1
        assert all(pow(5,w//p,q)!=1 for p in fs)
        assert (n-3-pow(5,h,q*q))%(q*q)==0
    return n

def veto(n,q,d):
    r = (n-3-pow(5,d,q*q)) % (q*q)
    return r!=0 and r%q==0

def phase(x,t,s,a,b):
    return crt([(0,2),(x,9),(2,5),(1,7),(0,11),(t,19),
                (s,43),(a,191),(b,383)])

n, m = target(0,0,0), target(192,2,121147)
assert (n-m)%(P*prod(r[0]**2 for r in fixed))==0
for N,e,expected in ((n,0,{0}),(m,192,set())):
    covered = set()
    for x in (0,1,3):
        masks = []
        for t,a in product(range(19),range(191)):
            d = phase(x,t,22,a,e+1)
            row = tuple(veto(N,q,d) for q in (19,191,383))
            assert row==(x==0 and t!=0,t==0 and a!=0,a==e%191)
            masks.append(any(row))
        if all(masks):
            covered.add(x)
    assert covered==expected

for s in range(43):
    d = phase(0,0,s,0,1)
    assert all(not veto(n,q,d) for q in (3,7,11,19,43,191))
    assert veto(n,383,d) and not veto(n,383,phase(0,0,s,0,0))
print("PASS")

# The pinned last reader's targeted 191 digit really changes.
for S in range(43):
    assert not veto(m,383,phase(0,0,S,0,193))
    assert veto(m,383,phase(0,0,S,1,193))
print("All native-strip digits checked against shifted last center")
```
