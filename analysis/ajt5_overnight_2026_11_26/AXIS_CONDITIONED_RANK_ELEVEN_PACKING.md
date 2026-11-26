# One-axis conditioning for rank-eleven packing

## Scope

This gives an exact maximum-load algorithm on full three-axis prefix rectangles and a conditional rank-11 obstruction test. The head positions and native square-precision row below are real powers of 3 and 5 at a represented positive integer. The replay's weighted incoming multiplicities and sharpness examples are synthetic; it does not produce that many actual common-Wieferich sources. There is no change to the unconditional density bound or the minimum of seventeen hypothetical common inert sources.

## Exact algorithm

Decode a CRT coordinate as its reversed base-p digit string at the maximum depth D on that axis. Its prefix of depth e is then a half-open interval of length p^(D-e). Cut one axis at every interval endpoint. The set of active rectangles is constant across each endpoint cell. Within a cell, sweep the second axis in sorted endpoint order, applying range-add events on the coordinate-compressed third axis. Apply all events at the same coordinate before measuring the maximum over the following nonempty cell. A range-add/range-max segment tree returns the exact peak; the maximum over cells gives the answer. With N rectangles this needs O(N² log N) arithmetic operations after endpoint construction, with bit costs depending on endpoint depth and weight size. No prime-power residue space is enumerated. If the rectangles bound possible positions rather than give exact supports, the result is only an upper bound for the actual load.

## Rank-eleven refinement

At c=1 and even d, the five ordinary heads (19,1171,251,211,43) have the prefix guards in the replay; label them A through E. In the chart H defined by d=1 mod 5, the actual row 11 forbids all first 11-prefixes except center 6. Off H, row 11 is inactive. Let m count incoming genuine tagged supports and b count only those with strict descendants of the center as their 11-prefix. Off H the live maximum is bounded by m_C + max(m_A,m_E); on H the deep maximum is bounded by max(b_A+b_D,b_B+b_D,b_B+b_E). These follow by intersecting the prefix guards. Any unconditional vetoes or supports not captured by these bounds must be accounted for separately.

If both bounds are at most 10, no full rank-11 fiber occurs off H; on H a fully covering fiber must have a support supplying the entire center (a centered level-one prefix or an already-accounted-for unrestricted veto). Without either, the eleven second-level children require at least eleven strict-descendant supports. Thus the general maximum of 24 in the example is too coarse to decide this local obstruction. Both strict thresholds are sharp for synthetic supports at this real target. The checker tests a high-depth endpoint implementation, the two synthetic sharpness cases, and independent raw-power verification of the actual shallow chart.

```python
from itertools import product

u = 1749240030127890765912351734436595992951490159
v = 1808434766219862061671534508108331483094094788
n = 28+u*u+v*v
R = [(19,9,(3,),0),(1171,45,(3,5),46),(251,25,(5,),0),
     (211,35,(5,7),56),(43,42,(2,3,7),22),(11,5,(5,),6)]
for q,w,f,e in R:
    assert pow(5,w,q)==1 and pow(5,w,q*q)!=1
    assert all(pow(5,w//p,q)!=1 for p in f)
    assert (n-3-pow(5,e,q*q))%(q*q)==0
assert (n-4)%20771**2==20771

# Prefix pairs (residue, depth), on the 3, 5, 7 axes.
G = [((0,2),(0,0),(0,0)),((1,2),(1,1),(0,0)),
     ((0,0),(0,2),(0,0)),((0,0),(1,1),(0,1)),((1,1),(0,0),(1,1))]
def interval(p,D,a,e):
    r = 0
    for _ in range(e):
        a,b = divmod(a,p)
        r = p*r+b
    s = p**(D-e)
    return r*s,(r+1)*s

def peak(weights,D,inside=None):
    axes = (3,5,7)
    boxes = [tuple(interval(p,k,*a) for p,k,a in zip(axes,D,g))
             for g in G]
    pts = [sorted({0,p**k} | {e for b in boxes for e in b[i]})[:-1]
           for i,(p,k) in enumerate(zip(axes,D))]
    return max(sum(w for b,w in zip(boxes,weights)
                   if all(a<=t<c for (a,c),t in zip(b,xyz)))
               for xyz in product(*pts)
               if inside is None or ((xyz[1]//5**(D[1]-1)==1)==inside))

for D in ((2,2,1),(80,90,70)):
    assert peak((5,12,5,12,5),D)==24
    assert peak((5,12,5,12,5),D,False)==10
    assert peak((5,5,5,5,5),D,True)==10

def bad11(y,t,m):
    b = 2*(3*y%5)
    d = b+10*((t-b)*pow(10,-1,m)%m)
    r = (n-3-pow(5,d,121))%121
    return r!=0 and r%11==0

# Synthetic prefixes against the actual square-precision row.
for y,m,S in ((0,11,list(range(11))),
              (1,121,[6+11*j for j in range(11)])):
    native = {t for t in range(m) if bad11(y,t,m)}
    assert native | set(S)==set(range(m))
    assert set(range(m))-(native | set(S[:-1]))=={S[-1]}
print("PASS")

# Check the native half-guards and first-level centers from raw powers.
# All d tested here are even (the fixed c=1 chart).
from math import lcm
from math import gcd
for q,w,_,_ in R:
    period=lcm(2,w*q)
    phase={(d%w,d%q) for d in range(0,period,2) if (n-3-pow(5,d,q*q))%(q*q)==0}
    bad={(d%w,d%q) for d in range(0,period,2) if (n-3-pow(5,d,q*q))%(q*q) in range(q,q*q,q)}
    assert len(phase)==1
    (side,center),=phase
    assert bad=={(side,t) for t in range(q) if t!=center}
    if q==11: assert (side,center)==(1,6)
# Independent brute force for the entire 3x5x7 order box at shallow depth.
vals=[]
for d in range(lcm(2,9,25,7)):
    if d%2: continue
    live=[(n-3-pow(5,d,q))%q==0 for q,*_ in R[:5]]
    vals.append((d,sum(w for w,L in zip((5,12,5,12,5),live) if L),sum(5 for L in live if L)))
assert max(a for _,a,_ in vals)==24
assert max(a for d,a,_ in vals if d%5!=1)==10
assert max(a for d,_,a in vals if d%5==1)==10
print("INDEPENDENT RAW CHECK PASS")
```
