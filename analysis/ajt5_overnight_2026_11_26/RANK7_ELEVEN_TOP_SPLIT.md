# Sixteen uncovered units in the eleven-top, five-lower rank-seven case

Use the fixed target and muted order slice of RANK_SEVEN_SIXTEEN_SOURCE_ESCAPE.md. Its window W has 72 units of weight 1/135, split into two 36-unit ternary halves. With eleven top sources only flat full-fiber witnesses are possible. Two deficient rank-seven branches lack any whole-ternary-half source. A nonshallow singleton caps the top union at 18 units; otherwise a shallow singleton restricts it to one half B. If row 19's pure second-ternary guard misses the opposite half, at least 36-5*4=16 units already survive on that half. If either deficient branch has at most two sources, the old 12-unit per-source cap leaves at least 72-24-28=20 units.

The remaining case has three sources in each deficient branch and one in each of the five other branches. Row 19's position is in the opposite half. On B, a top first-prefix with a full second-ternary lower guard needs an order-63 or order-126 head: the least helper's lower order divides 9, its 7-depth is at most one, and smaller possible heads either give the opposite row-19 guard, are muted or unprocessed, or are the five already committed shallow mixed heads. Direct rigid orders 63 and 126 are excluded by the squarefree factorizations in the replay. There are exactly four ordinary inert heads of the two orders, each contributing just one pair of 7-digit and ternary residue. Hence one deficient branch has at most two distinct full second-ternary guards.

On B there are three full residue classes modulo nine, each of 12 units. With two full classes, a remaining nonfull guard contributes at most four units in the third class; with one, each remaining nonfull guard contributes at most six units outside it; with none, each costs at most nine units. These are rectangle-prefix bounds: either the nonfull guard is on one finer ternary cell, or it is restricted on the quinary axis. Duplicating a full guard cannot enlarge the union. Thus that deficient branch limits the top witnesses to at most 28 units. The original lower-only coverage bound is 28 units, so at least 72-28-28=16 units survive in this case. The previous guarantee for this case was eight. This refinement alone does not increase the unrestricted 17-source threshold.

The replay proves the head factorizations and checks sharpness of the projected guard geometry, using synthetic incoming labels. The geometric sharpness check does not assert existence of these labels as genuine common Wieferich primes.

```python
from itertools import product
from math import isqrt, prod

def prime(q):
    if q != 23792163643711:
        return all(q % j for j in range(2, isqrt(q)+1))
    fs = (2,3,3,5,7,11,29,37,89,35951)
    return (prod(fs)==q-1 and all(map(prime,fs)) and pow(3,q-1,q)==1
            and all(pow(3,(q-1)//p,q)!=1 for p in set(fs)))

a,z = 5**3,5**21
heads = set()
for w,N,F in (
    (63,(z*z+z+1)//(a*a+a+1),(280729,2161279,23792163643711)),
    (126,(z*z-z+1)//(a*a-a+1),(883,406729,24132781,1692416503)),
):
    assert prod(F)==N and len(set(F))==len(F) and all(map(prime,F))
    for q in F:
        if q%4==3:
            assert pow(5,w,q)==1 and pow(5,w,q*q)!=1
            assert all(pow(5,w//r,q)!=1 for r in (2,3,7) if w%r==0)
            heads.add(q)
assert heads=={883,2161279,1692416503,23792163643711}

# Exact projected guard geometry of the hybrid control.
W = {(x,y) for x,y in product(range(27),range(4)) if x%3!=2}
low = {(x,y) for x,y in W if x%9==0 or x in (3,6,12,15)}
flat = {(x,y) for x,y in W if x%3==1 and (x%9 in (1,4) or x==7)}
assert len(low)==len(flat)==28 and not low&flat
assert W-low-flat == {(x,y) for x in (16,21,24,25) for y in range(4)}
print("PASS")

# Exhaust rectangle guard families on the 36-cell endangered half.
from itertools import combinations_with_replacement
B={(x,y) for x in range(1,27,3) for y in range(4)}
full=[{(x,y) for x,y in B if x%9==r} for r in (1,4,7)]
other=[{(x,y) for x,y in B if x%m==r and (j is None or y==j)}
       for m in (3,9,27) for r in range(m) for j in (None,0,1,2,3)
       if not (m==3 and j is None) and not (m==9 and j is None)]
for k,cap in ((0,27),(1,24),(2,28)):
    assert max(len(set().union(*f,*g))
               for f in combinations_with_replacement(full,k)
               for g in combinations_with_replacement(other,3-k))==cap
print("Caps for deficient 7-branch independently replayed")
```
