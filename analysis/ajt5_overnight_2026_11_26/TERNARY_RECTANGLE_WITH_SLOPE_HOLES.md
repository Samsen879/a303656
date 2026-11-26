# Sharp local branching bound with stripes and slope holes

At a surviving parent in the ternary exponent tree, let U,V be the available next digits after coordinate restrictions and single-axis stripes; put a=|U|, b=|V|. For primitive exponents an active zero reader with equal positive ternary order depths imposes one absolute slope class; its last digit cuts a diagonal j-alpha i=delta with alpha nonzero. Unequal depths impose no collision. The full ternary primary holes are safe to remove conservatively even when the prime-to-3 observations would let some of their cells survive.

Let z be the number of allowed diagonal offsets. Each diagonal intersects U×V in at most min(a,b) and at least a+b-3 cells. Thus at least L=max(0,ab-(3-z)min(a,b),z(a+b-3)) children remain before two-axis nonzero readers. This is sharp from these three cardinalities alone: if an axis has size 0 or 1 the assertion is direct, if one has size three the diagonal occupancies are constant, and for a=b=2 the sizes are 2,1,1. Under the odd-c even-d anchors, each new two-axis inert nonzero reader on this level deletes at most one cell by SECOND_SLOPE_DIGIT_ESCAPE.md. Therefore L>m provides a sufficient child-extension criterion against m such readers. This may be iterated only at surviving parents that meet the corresponding active-coordinate and reader conditions; there is no general saturation or height bound.

At the same earlier target, the branch c=31+2310x,d=778+462y passes through a stripe from 127 and then one from 271. At its third level, x in {0,9}, y in {0,9,18}, the absolute 5023 slope hole removes one offset. L(2,3,2)=4 guarantees four panel survivors; raw arithmetic verifies five positive survivors because one cell on the conservative diagonal is not hit in its prime-to-3 phase. The check does not give a two-square certificate or change the global conclusions.

```python
from itertools import product
from math import prod

Z = (1783,5023,11419697846380955982026777206637491,163)
P = (19,127,199,271,4159)
f = [3**(1+2310*j)+5**(82+2310*j) for j in range(9)]
pairs = [(9,24)] + [(0,q) for q in Z]
pairs += [(f[j]+p,p*p) for p,j in zip(P,(0,1,2,2,5))]
M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = f[-1]+1+(u-f[-1]-1) % M
assert n.bit_length() == 43100 and all(n%p for p in P)

def primary(g,p):
    t = p-1
    while t%3 == 0:
        t //= 3
    return pow(g,t,p)

assert [s for s in range(1,81,3) if any(
    primary(3,p) == pow(primary(5,p),s,p) for p in Z)] == [46]

def c(x): return 31+2310*x
def d(y): return 778+462*y
def hit(p,I,J):
    return {(x,y) for x,y in product(I,J)
            if (n-pow(3,c(x),p)-pow(5,d(y),p))%p == 0}

for p,r in zip(P,(1,1,1,2,2)):
    assert pow(3,2310*3**r,p) == pow(5,462*3**r,p) == 1
    assert (pow(3,2310*3**(r-1),p),pow(5,462*3**(r-1),p)) != (1,1)

assert [hit(p,range(3),range(3)) for p in P[:3]] == [
    {(1,2)}, {(1,y) for y in range(3)}, set()]
assert [hit(p,(0,3,6),(0,3,6)) for p in P[3:]] == [
    {(x,3) for x in (0,3,6)}, set()]

I,J = (0,9),(0,9,18)
assert {(x,y) for x,y in product(I,J)
        if d(y)*pow(c(x),-1,81)%81 == 46} == {(0,0),(9,18)}
assert set.union(*(hit(p,I,J) for p in Z+P)) == {(0,0)}
assert (n-3**c(0)-5**d(0)) % 5023**2 == 1554*5023
assert n > 3**c(9)+5**d(18)
print("Two stripe cuts, one exact zero hole, five active panel survivors")

# Independently exhaust every cardinality triple for the local sharp bound.
Q=[{x for x in range(3) if mask>>x&1} for mask in range(8)]
best={}
for U,V,W in product(Q,repeat=3):
    key=tuple(map(len,(U,V,W)))
    slots=sum((j-i)%3 in W for i,j in product(U,V))
    best[key]=min(best.get(key,9),slots)
assert all(x==max(0,a*b-(3-z)*min(a,b),z*(a+b-3))
           for (a,b,z),x in best.items())
assert (n-3**31-5**4936)>0 and all((n-3**31-5**4936)%p for p in Z+P)
print("Sharp bound checked for every local cardinality triple")
```
