# Eighteen disjoint actual start triples at one target

For the fixed verified H-bit target and the original actual 3,5 chart, the replay gives 18 genuine four-hit configurations with exact-once inert valuation at their corresponding witnesses. Their first three addresses are pairwise disjoint, so any common address set hitting all those triples needs at least 18 addresses. Seventeen triples are witnessed by the same physical p=1259 and have seventeen distinct starting phase products; they cannot be treated as repeat swaps of one product or as a single triple per prime. The remaining triple uses q=8807, with the same n constructed by CRT. The origin has a genuinely positive two-square remainder. Translating the q configuration by (8,19) keeps every point in the original grid and multiplies both phase terms by the same unit, but changes their common read from 54 to 2168 at the now-fixed n; all four translated points therefore fail.

## Conditional increasing packing

Suppose K distinct qualified primes supply central four-hit configurations, each at a common nonzero residue of its own, and a step (a_p,b_p) of sup norm ≤L such that x^a_p=y^b_p, where x=3^720,y=5^720 and each order is at least D>J. If 1+floor(J/(8L))≥9(K−1)+2, each configuration can be translated by a multiple of that step while remaining in the chart. The resulting common residue values are distinct because the total exponent translations are shorter than D. A previously used address forbids at most three translations, and avoid a single translation with residue equal to the origin read. Choose the translations before fixing n. At each prime lift the selected read modulo p² avoiding at most four bad values, then prescribe U,V by CRT so n=S(0,0)+85(U²+V²) realizes all reads. For each p not dividing 85 the required norm is a unit; every finite-field unit is a sum of two squares, and one nonzero coordinate lifts. The product-p² height budget and an appropriate ordinary chart with reserve at height H ensure strict positive remainders and one same n.

This would give a growth obstruction if sufficiently many actual qualified primes with central seeds and the stated budget were available together. No such unbounded supply was proved. It concerns address **cardinality**, not a weighted gcd-budget lower bound. The verified example is finite and is not a conjecture counterexample.

```python
from math import gcd, isqrt

H,J,t,r,s,p,q = 3720000,310,155521,17,37,1259,8807
D,C,E = r*s,3*t+80,t+144
for a in (t,r,s,p,q):
    assert a > 1 and all(a%d for d in range(2,isqrt(a)+1))
for a in (p,q):
    assert a%4 == 3 and (a-1)%D == 0 and J < D
    for b in (3,5):
        assert all(pow(b,720*((a-1)//d),a) != 1 for d in (r,s))
        assert pow(b,a-1,a*a) != 1

M,P,L = 146651884329720,q*q,H//2-4
assert M%(p*p) == 0 and gcd(M,P) == 1 and M*P < 1<<(L-4)
assert max(2*(C+720*(J-1)), 3*(E+720*(J-1))) < H-5

def coord(a,b,m):
    c = a + M*((b-a)*pow(M,-1,P)%P)
    return (pow(2,L,m)+(c-pow(2,L,M*P))%(M*P))%m

def N(m):
    u = coord(61827877807697,0,m)
    v = coord(135417323161960,39021647,m)
    return (pow(3,C,m)+pow(5,E,m)+85*(u*u+v*v))%m

assert (N(p*p),N(q*q)) == (1223507,54)

def phase(z,m):
    i,j = z
    assert 0 <= i < J and 0 <= j < J
    return pow(3,C+720*i,m),pow(5,E+720*j,m)

def sub(a,b):
    return a[0]-b[0],a[1]-b[1]

def det(a,b):
    return a[0]*b[1]-a[1]*b[0]

rows = [
 (578,23283,34563,14713),(1279,15784,55261,5034),
 (2057,11961,49601,19041),(2394,38800,46404,10113),
 (2985,14713,48217,11961),(3257,10113,68134,11961),
 (5519,22148,45019,25880),(81732,5776,45896,11961),
 (95824,7812,47624,56163),(50093,8143,23017,34235),
 (13891,26821,89186,45496),(86710,15056,31782,47624),
 (22856,25880,46892,40112),(40628,30190,40112,38800),
 (33520,80782,88180,55261),(37035,41417,87367,47624),
 (53358,70775,95773,80782)]
old = [tuple(divmod(z,J) for z in row) for row in rows]
new = ((34,175),(277,148),(292,169),(266,159))
used = set()
for a,row in [(p,z) for z in old]+[(q,new)]:
    o,u,v,f = row
    U,V,F = sub(u,o),sub(v,o),sub(f,o)
    h,k = gcd(U[0],V[0]),gcd(U[1],V[1])
    assert 2 <= h <= 14 and 2 <= k <= 14 and h%r and k%r
    assert U[0]*V[0] > 0 and U[1]*V[1] > 0
    assert max(abs(U[0]//h),abs(V[0]//h),
               abs(U[1]//k),abs(V[1]//k)) <= 90
    e,m,l = det(U,V),det(F,V),det(U,F)
    assert e and e%(r*h*k) == 0
    if e < 0:
        e,m,l = -e,-m,-l
    g = gcd(e,gcd(m,l))
    assert m > 0 and l > 0 and m+l < e
    assert (e//g)%r == 0 and e//g <= 408
    assert all((N(a*a)-sum(phase(z,a*a)))%(a*a)
               in range(a,a*a,a) for z in row)
    assert used.isdisjoint(row[:3])
    used.update(row[:3])

def product(z):
    a,b = phase(z,p)
    return a*b%p

assert len(used) == 54 and 18**24 > J**5
assert len({product(row[0]) for row in old}) == 17
assert len({product(z) for row in old for z in row[:3]}) == 45
assert pow(3,720*8,q) == pow(5,720*19,q)
assert [sum(phase((i+8,j+19),q))%q for i,j in new] == [2168]*4
assert N(q) == 54
print("OK")
```
