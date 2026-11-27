# Deterministic incidence of omitted primes across translated prefixes

Track one active cell through translations of its 5-exponent by E. Its remainders have form R_j=N-A g^j with A a power of 5 and g=5^E. For p other than 5 dividing R_j, it divides R_i exactly when i=j modulo ord_p(g). Thus an omitted prime with that translation order hits at most ceil(L/ord_p(g)) cells of a consecutive row of length L. A sum of such bounds strictly below L rules out a cover, with no assumption of independence.

There is an exact repeated-prime test without finding the primes. Let D_m=lcm(g^h-1:1<=h<=m), with D_0=1. For p other than 5 dividing R_j, another hit exists in the row exactly when p divides gcd(R_j,D_max(j,L-1-j)). This is because a positive multiple of the order fits in at least one direction from j. Common odd-valuation hits obey the same bound.

At the exact target of ANCHORED_RECTANGLE_FIXED_DIVISORS.md, both tags y=1 and y=14 give seven positive panel survivors under d=778+462y+1782j (0<=j<=6), c=31. Each row has pairwise gcd 25. The second row exhibits distinct exact odd valuations at 463 and 107. Across both rows there are exactly three shared inert primes, 463,103,547, each appearing at exactly one pair, with exact valuation one at both members. The only extra shared prime is the split prime 61.

Every remainder is 1 modulo 4, so any failure to be a sum of two squares needs at least two distinct inert primes with odd valuation. If all fourteen tagged cells fail, that would require at least 28 incidences; only three can be repeated across witnesses, so at least 25 distinct omitted inert primes are needed. Equivalently no chosen set of at most 24 omitted inert primes can itself account for failure of all fourteen cells. This does not rule out contributions from more primes or prove a two-square representation.

```python
from itertools import combinations
from math import gcd, lcm, prod

Z = (1783,5023,11419697846380955982026777206637491,163)
P = (19,127,199,271,4159)
f = [3**(1+2310*j)+5**(82+2310*j) for j in range(9)]
pairs = [(9,24)] + [(0,p) for p in Z]
pairs += [(f[j]+p,p*p) for p,j in zip(P,(0,1,2,2,5))]
M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = f[-1]+1+(u-f[-1]-1) % M

E = 1782
g = 5**E
D = [1]
for h in range(1,7):
    D.append(lcm(D[-1],g**h-1))

assert E%81 == 0 and 3**4651+5**17938 < n
for y in (1,14):
    R = [n-3**31-5**(778+462*y+E*j) for j in range(7)]
    assert all(r>0 and r%4==1 and all(r%p for p in Z+P) for r in R)
    assert all(gcd(r,D[max(j,6-j)])==1 for j,r in enumerate(R))
    assert all(gcd(a,b)==25 for a,b in combinations(R,2))

assert R[0]%463**2 == 146*463 and R[5]%107**2 == 84*107
assert [j for j,r in enumerate(R) if r%463==0] == [0]
assert [j for j,r in enumerate(R) if r%107==0] == [5]
assert pow(g,7,463)==1 and g%463!=1
assert pow(g,53,107)==1 and g%107!=1
print("Seven active witnesses per row, with distinct 463 and 107 odd hits")

# Independent cross-row analysis: 28 required inert incidences, at most
# three repeated primes, each shared by exactly two witnesses.
from math import isqrt
R14=[n-3**31-5**(778+462*y+E*j) for y in (1,14) for j in range(7)]
gcds={(i,j):gcd(R14[i],R14[j])//25 for i,j in combinations(range(14),2)}
assert set(gcds.values())=={1,61,103,463,547}
for p in set(gcds.values())-{1}:
    assert all(p%d for d in range(2,isqrt(p)+1))
edges={ij:p for ij,p in gcds.items() if p%4==3}
assert edges=={(0,7):463,(5,8):103,(6,13):547}
assert all(R14[i]%p**2 and R14[j]%p**2 for (i,j),p in edges.items())
assert 2*len(R14)-len(edges)==25
print("Failure of all fourteen witnesses would need at least 25 omitted inert primes")
```
