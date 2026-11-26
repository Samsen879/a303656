# A single omitted prime blocks every cell of the certified short prefix

Keep the exact target and anchored rectangle of TERNARY_PREFIX_HEIGHT_CERTIFICATE.md. In the 3-by-6 prefix, nine cells pass the original nine readers, and all 18 remainders are positive. Yet every cell has valuation one at the omitted inert prime 463. Both exponent steps are multiples of 462, so modulo its square the remainder divided by 463 is 123+156x+167y modulo 463. It never vanishes in the prefix. This obstruction coexists with n exceeding the largest prefix offset by a factor of more than 2^35727.

The entire active anchored box comprises 468 cells. Only (5,14) has even valuation at 463, specifically two; this does not establish the two-square status of that cell. The short-prefix obstruction persists in the fixed arithmetic progression n+t M*463², where M is the CRT modulus defining the original observations. That only disproves the inference from the finite fixed prefix to a norm; other exponent pairs can survive, and no change to density is claimed.

A useful restricted positive transfer is the following. Let a surviving R>0 have R=1 modulo 4 and even valuation at all tested inert primes. Let D divide R and be a certified odd sum of two squares. Let q1<q2 be the smallest two still-eligible inert primes. If R/D<q1*q2, then R is a sum of two squares: division by the odd norm preserves all inert valuation parities and leaves a cofactor 1 modulo 4, so two distinct odd-valuation inert primes would be needed for failure. The product threshold is sharp from this information alone. For a common D across the whole anchored rectangle, its divisibility follows from divisibility of the first remainder and both first offset differences by geometric-series identities. Height slack alone does not imply a small cofactor.

```python
from itertools import product
from math import gcd, isqrt, prod

Z = (1783,5023,11419697846380955982026777206637491,163)
P = (19,127,199,271,4159)
f = [3**(1+2310*j)+5**(82+2310*j) for j in range(9)]
pairs = [(9,24)] + [(0,p) for p in Z]
pairs += [(f[j]+p,p*p) for p,j in zip(P,(0,1,2,2,5))]
M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = f[-1]+1+(u-f[-1]-1) % M

def F(x,y):
    return 3**(31+2310*x)+5**(778+462*y)

q = 463
assert q%4 == 3 and all(q%k for k in range(2,isqrt(q)+1)) and M%q
assert [pow(g,s,q*q) for g,s in ((3,2310),(5,462))] == [1+209*q,1+38*q]
assert (n-F(0,0))%q**2 == 123*q
assert (-209*3**31)%q == 156 and (-38*5**778)%q == 167

R = [n-F(x,y) for x,y in product(range(3),range(6))]
S = [r for r in R if all(r%p for p in Z+P)]
assert len(S) == 9 and gcd(*R) == q and gcd(*S) == 25*q
assert n.bit_length() >= F(2,5).bit_length()+35728
assert all(r>0 and r%4==1 and r%q==0 and r%q**2!=0 for r in R)

assert F(11,38)<n<min(F(12,0),F(0,39))
assert [(x,y) for x,y in product(range(12),range(39))
        if (123+156*x+167*y)%q==0] == [(5,14)]
assert (n-F(5,14))%q**3 == 138*q*q
print("All 18 prefix cells blocked by 463; one even shell in the active box")

# Check all active cells directly, independently of the affine formula.
box=[(x,y) for x,y in product(range(12),range(39))]
assert all(F(x,y)<n for x,y in box)
assert [(x,y) for x,y in box if (n-F(x,y))%q**2==0]==[(5,14)]
assert n>2**35727*F(2,5)
print("All 468 active cells and height slack independently checked")
```
