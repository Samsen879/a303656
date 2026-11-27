# Incidence-product criterion and its limit at the translated prefix

For each candidate remainder R_i=1 mod 4, remove a certified odd norm part and all known exact odd inert factors, leaving cofactor U_i. Any candidate failing the two-square criterion needs at least two distinct odd-valuation inert primes in R_i. In a selected subset I, subtract the known incidences from this requirement cell by cell. If every remaining eligible inert prime can hit at most one selected witness, failure everywhere forces at least b_I distinct eligible primes to divide product_(i in I) U_i, where b_I is the remaining incidence demand. Therefore that product being below the product of the b_I smallest eligible primes would certify a two-square remainder. This criterion needs no probability assumption; it requires actual cofactor control.

For the 14 offsets of TRANSLATED_PREFIX_INERT_INCIDENCE.md, remove the norm divisor 25 and the exact odd hits of 103,107,463,547 where present. These supply seven of the 28 needed incidences; the pairwise gcd data then require 21 different private inert primes if all cells fail. The original cofactor product has 603,274 bits, and the size inequality does not close.

The replay constructs a different target less than 2^741 below the original. It preserves all 14 offsets, retained congruences, each remainder's bit length, known exact odd hits, and the complete pairwise gcd matrix. Every new remainder is smaller but positive. CRT assigns 21 distinct private primes, each hitting exactly its intended cell, all at exact valuation one. Together with the four known primes, these verify failure at all 14 cells of the new target. The construction disproves using just the original size upper bounds and verified incidence data as a norm certificate. It supplies no information about whether the original target has a genuine two-square remainder among its 14 witnesses, and is not a counterexample to A303656.

```python
from itertools import combinations
from math import gcd, isqrt, lcm, prod

Z = (1783,5023,11419697846380955982026777206637491,163)
P = (19,127,199,271,4159)
f = [3**(1+2310*j)+5**(82+2310*j) for j in range(9)]
pairs = [(9,24)] + [(0,p) for p in Z]
pairs += [(f[j]+p,p*p) for p,j in zip(P,(0,1,2,2,5))]
M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = f[-1]+1+(u-f[-1]-1) % M

ds = [778+462*y+1782*j for y in (1,14) for j in range(7)]
F = [3**31+5**d for d in ds]
R = [n-f for f in F]
edges = {(0,7):463, (5,8):103, (6,13):547}
ij = list(combinations(range(14),2))
def audit(R):
    return [gcd(R[i],R[j]) for i,j in ij]

shape = [25*(61 if (i,j)==(2,11) else edges.get((i,j),1)) for i,j in ij]
assert audit(R) == shape
K = [([107] if i==12 else [])+[p for e,p in edges.items() if i in e]
     for i in range(14)]
assert prod(r//(25*prod(k)) for r,k in zip(R,K)).bit_length() == 603274

ps = [1019,1031,1039,1051,1087,1091,1103,1151,1163,1187,1223,
      1231,1259,1279,1283,1291,1303,1307,1319,1327,1367]
assert len(set(ps)) == 21 and prod(ps).bit_length() == 215
for p in ps+[103,107,463,547]:
    assert p%4==3 and all(p%d for d in range(2,isqrt(p)+1))
assert all(len({pow(5,d,p) for d in ds})==14 for p in ps)

A = prod(p*p for p in ps)
B = lcm(M,125,61**2,103**2,107**2,463**2,547**2)
it = iter(ps)
add = [[next(it) for _ in range(2-len(k))] for k in K]
v = sum((F[i]+p)*(A//(p*p))*pow(A//(p*p),-1,p*p)
        for i,L in enumerate(add) for p in L) % A
n0 = n+B*((v-n)*pow(B,-1,A)%A)-16*A*B
S = [n0-f for f in F]

assert 0<n-n0<2**741 and n0.bit_length()==n.bit_length()==43100
assert n0%B==n%B and audit(S)==shape
assert all(s.bit_length()==r.bit_length()==43100 and s%4==1
           and all(s%p for p in Z+P) for r,s in zip(R,S))
assert all(len(k+a)==2 and all(s%p==0 and s%p**2 for p in k+a)
           for s,k,a in zip(S,K,add))
print("Same incidence and smaller remainders, with 25 explicit obstructing primes")

assert all(0<s<r for s,r in zip(S,R))
assert len({p for row in add for p in row} | {103,107,463,547})==25
# Independently enforce uniqueness of every added prime's hit location.
for i,L in enumerate(add):
    for p in L:
        assert [j for j,s in enumerate(S) if s%p==0]==[i]
print("Countercontrol private incidence independently checked")
```
