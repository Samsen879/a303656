# First rank eleven is excluded through seventeen sources

Use the fixed-target muted slice and exact linear history of RANK_ELEVEN_SIXTEEN_SOURCE_ESCAPE.md. The first rank-eleven pivot cannot close that slice through 17 original rigid sources. At least 4/135 of the lower (3,5) phase space admits a lift through both 7 and 11. This does not resolve the other first pivots at budget 17.

Write t for the number reading rank 11 and ell for the lower-only sources. With t>=11 and t+ell<=17, the rank-11 normal form adds no new minimal shape: extending a rigid flat frontier needs at least 21, as does expanding the nested dynamic witness. Restrict to the 72/135 window outside the native order-five row-11 guard and the native row-7 guard. In this window only rank-11 flats matter. Any flat has at least 22−t>=5 singleton first positions. Only three exact ordinary inert heads of order 11 or 22 can supply unrestricted singleton guards, so a flat needs a particular proper singleton guard G. Its projection is contained in G together with the ell unchanged lower guards.

If at most six terms in this overcover read 7, only 7-blind terms could forbid an entire 7-fiber. The proper G costs at most 36 units of 1/135. All pure second-ternary lower-only guards share the one row-19 position (at most 12 units in total), and each other lower guard costs at most four after the old mutes and the row-11 cut. Thus at least 72−36−12−5*4=4 units survive.

Otherwise all seven terms read 7, so t=11 and ell=6. The rank-11 flat projects exactly the intersection of its eleven original guards. To close a 7-fiber, that intersection and all six lower guards must supply distinct first positions; expansion would need 13 terms. Remove those first positions from the six lower terms and intersect the remaining ternary/quinary guards. If the intersection is nonempty its depths a,b cannot have a<=1,b=0: only five available heads of orders 21 or 42 can give six different positions, since the smaller heads are muted or unprocessed. Nor can a=0,b<=1: only the two actual order-35 heads are available, by the primitive norm exclusions. Any other term has either a>=2, b>=2, or a,b>=1, leaving intersection mass at most 12/135, 2/75, or 9/135 respectively in the window. Thus at least 60/135 escapes this two-flat case.

The replay verifies the head inventories and an actual target realizing six ordinary order guards for the two-flat geometry, with synthetic original rigid assignments. These assignments are not genuine common Wieferich primes.

```python
from math import gcd, isqrt, prod
from itertools import product

P = {}
for w in range(1, 71):
    P[w], rem = divmod(5**w-1, prod(v for d,v in P.items() if w%d==0))
    assert rem == 0

def prime(q):
    return q > 1 and all(q%d for d in range(2, isqrt(q)+1))

F = {3:(31,), 6:(3,7), 5:(11,71), 10:(521,), 9:(19,829),
     18:(3,5167), 15:(181,1741), 30:(61,7621), 7:(19531,),
     14:(29,449), 21:(379,519499), 42:(7,43,127,7603),
     11:(12207031,), 22:(23,67,5281)}
H = {}
for w, fs in F.items():
    assert prod(fs) == P[w] and len(set(fs)) == len(fs)
    assert all(map(prime, fs))
    H[w] = {q for q in fs if q%4==3 and pow(5,w,q)==1
            and all(pow(5,d,q)!=1 for d in range(1,w))}
    assert all(pow(5,w,q*q)!=1 for q in H[w])

assert H[11] | H[22] == {23,67,12207031}
assert H[7] | H[14] == {19531}
assert H[21] | H[42] == {43,127,379,7603,519499}
assert P[35] == 211*631*(249459**2+544090**2)
assert gcd(249459,544090) == 1
assert P[70] == 233260120**2+130734441**2
assert gcd(233260120,130734441) == 1
for q in (211,631):
    assert prime(q) and q%4==3 and pow(5,35,q*q)!=1
    assert pow(5,35,q)==1 and all(pow(5,d,q)!=1 for d in (5,7))
assert [72-36-12-4*(b-12) for b in (16,17)] == [8,4]

u = 52594046247613030401989925906979838297552655344087959375232163
v = 58292572836098051272495976043826279908406478692127458428776408
n = 4+u*u+v*v
assert n%12 == 5
for q,w in ((3,2),(31,3),(71,5),(5167,18),(19531,7)):
    assert all((n-3-pow(5,d,q))%q for d in range(0,2*w,2))

rows = [(379,21,0),(519499,21,6),(43,42,12),(127,42,18),
        (7603,42,24),(2161279,63,36)]
for q,w,e in [(7,6,2),(11,5,4),*rows]:
    assert prime(q) and pow(5,w,q)==1 and pow(5,w,q*q)!=1
    assert all(pow(5,d,q)!=1 for d in range(1,w))
    assert (n-3-pow(5,e,q*q))%(q*q)==0
    r = (n-3-pow(5,e+2*w,q*q))%(q*q)
    assert r and r%q==0

# The synthetic 11-flat projects to z=2. Other positions use actual order guards.
W = {(x,y) for x,y in product(range(27),range(4)) if x%3!=2}
D = {(d%27,d%5,d%7): d for d in range(0,2*27*5*7,2)}
covered = set()
for x,y in W:
    bits = set()
    for z in range(7):
        d = D[x,y,z]
        assert all((n-3-pow(5,d,q))%q for q in (7,11))
        if z==2 or any((n-3-pow(5,d,q))%q==0 for q,_,_ in rows):
            bits.add(z)
    if len(bits)==7:
        covered.add((x,y))

assert covered == {(x,y) for x,y in W if x%9==0}
assert len(W-covered) == 60
assert {e%7 for _,_,e in rows} | {2} == set(range(7))
print("PASS")
```
