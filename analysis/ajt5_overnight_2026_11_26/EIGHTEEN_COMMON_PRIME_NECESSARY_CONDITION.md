# A finite all-exponent obstruction needs at least eighteen common exceptional primes

If a finite modulus M excludes n−3^c−5^d from the square-sum residues for every pair c,d>=0, at least eighteen distinct inert primes q satisfy q²|M and 3^(q−1)=5^(q−1)=1 mod q². This is a necessary condition on a hypothetical finite certificate, not an existence, density-one, or pointwise theorem.

## Put all pivot results on the same slice

The [exact modulus bridge](https://github.com/Samsen879/a303656/commit/1c648df4be90efe9065023067ec0125f4d1dbf59) joins square coordinates by CRT. Split prime powers always pass. An inert factor vetoes exactly odd valuations strictly below its precision, while zero passes. At 2, zero and the top valuation pass; lower valuations pass exactly for odd part 1 modulo four. The original precision is kept throughout.

Choose c odd for n=0,1 mod 4 and even otherwise, with c positive, and a parity of d making 5^d distinct from n modulo 3. Use [the simultaneous muting construction](https://github.com/Samsen879/a303656/commit/c3cee9bfda27490e465f67c818cb6c7b85ff3b9e) to reserve c modulo 800730 and mute 3,31,71,5167,19531 in increasing refinements. The inert divisors of the reservation period are all ordinary to base 5. Process base-5 exceptional but base-3 ordinary inert rows in increasing order; at each q preserve the reservation, earlier cube observations of base-3 powers, and its own power modulo q. Whenever the base-5 parity class has a collision log e, ordinary base-3 lifting gives n−3^c−5^e=q² mod q³. This removes a rigid seed: at base-5 depth two the row can remain dynamic, and at larger depth the valuation stays two. Any remaining rigid seed therefore comes from a distinct common exceptional prime that occurs in M to exponent at least two.

After the last change in c fix a passing two-adic class of d, retaining d parity and all inert order guards. For odd n the chosen c makes the residual 1 mod 4. For even n, n−3^c is 1 mod 4 and the chosen parity powers of 5 realize the corresponding coset modulo powers of two, so the residual can be chosen congruent to 0 or 4 at the full binary precision. Inert row orders have binary part at most 2. The compatible residue choices lift to actual nonnegative exponents without a height requirement.

## Exhaust all first pivots at budget seventeen

The same exact linear contractions as in [the budget-sixteen integration](https://github.com/Samsen879/a303656/commit/eb8c39342b2b4c6f84ccd3dc2dacb50c81cc39d1) keep at most one guard per original seed. A first essential nonlinear projection at p requires at least p reading sources, so the possible first ranks above 3 are 5,7,11,13,17.

- **5:** the [guarded rank-five formula](https://github.com/Samsen879/a303656/commit/9c2a6653449ff0016adb4b782b9db848c6227844) needs at least 20 total for the whole relevant lower-only range 0<=k<=12.
- **7, 11, 13:** RANK7_SEVENTEEN_SOURCE_ESCAPE.md, RANK11_SEVENTEEN_SOURCE_ESCAPE.md, and RANK13_SEVENTEEN_SOURCE_ESCAPE.md apply on this same slice and with the same exact linear history. Their respective guaranteed escape masses are 6/135, 4/135, and 39/135 on the lower coordinates.
- **17:** the split row has no native veto. With precisely 17 first-position singletons and no lower-only sources, an everywhere flat cover would need unrestricted lower guards for all singletons. Each such position needs a distinct actual head of order 17 or 34, raw or least surviving helper; any such inert head is 1 mod 17 and 3 mod 4, hence at least 35. All heads divide the product of the two cyclotomic values (25^17−1)/24, smaller than 35^17. A singleton with a proper lower constraint therefore exists and misses a point of the window outside the native 7 and 11 guards, with 13 free.
- **Linear through to 3:** the [ternary leaf bound](https://github.com/Samsen879/a303656/commit/e80d98299a361f515c77dca2fa71def8f2f85405) uses actual least-helper prefixes (enlargements preserve any cover), with distinct caps 1,1,6,4 at the first four depths and at least 81 leaves in total.

Thus budget 17 cannot close the slice. The exact contraction history and modulus semantics then give an actual exponent pair passing all original local square-sum tests, contradicting a finite all-exponent certificate.

```python
from math import gcd, lcm

def order(a,p):
    return next(j for j in range(1,p) if pow(a,j,p)==1)

assert order(3,31)==30 and order(5,31)==3
D=90
for p,w,choices,blocked in [(5167,738,41,9),(71,35,7,5),(19531,6510,31,7)]:
    assert order(3,p)==w and order(25,p)==blocked
    assert w//gcd(D,w)==choices>blocked
    D=lcm(D,w)
assert D==800730==2*3**2*5*7*31*41
assert all(pow(5,p-1,p*p)!=1 for p in (3,7,31))
assert all((n-pow(5,int(n==1),3))%3 for n in range(3))
for e in range(3,8):
    m=2**e
    for b in (0,1):
        S={pow(5,d,m) for d in range(b,m//4,2)}
        assert S==set(range(1+4*b,m,8))
        assert all(x in S or (x-4)%m in S for x in range(1,m,4))

# Rank 5, with ternary masses in units of 1/81 and k <= 17-5.
U=lambda k: 9+3*min(6,k-1)+max(0,k-7) if k else 0
assert min(k+1+4*min(5,(62-U(k))//9) for k in range(13))==20

assert 17==1+4**2 and 17<33 and 24*35**17>25**17-1
I=[1]
for L in (1,1,6,4):
    I.append(3*I[-1]-L)
assert I==[1,2,5,9,23] and 1+2*sum(I)==81

A=lambda k: 12+4*(k-1) if k else 0
caps=(18,18,24,24,28,28,36,36,36,54,54)
assert min(72-c-A(17-t) for t,c in enumerate(caps,7))==6
assert max(12*s+q*(9-3*s)+4*(4-s-q) for s in range(2) for q in range(3))==28
assert (72-28-A(6),72-28-A(5),72-36-A(4))==(12,16,12)
assert (72-36-A(6),72-12)==(4,60)
assert (72-9-A(4),72-12-4*4)==(39,44)
print("PASS")

from itertools import product
from fractions import Fraction
def accepted(r,p,e):
    r%=p**e
    if not r or p%4==1: return True
    v=0
    while r%p==0: v+=1; r//=p
    return (v>=e-1 or r%4==1) if p==2 else (v%2==0)
for p,e in ((2,1),(2,2),(2,6),(3,3),(5,3),(7,3),(11,2),(13,2)):
    M=p**e
    P={x*x%M for x in range(M)}
    assert {(a+b)%M for a,b in product(P,P)}=={r for r in range(M) if accepted(r,p,e)}
for n in range(4):
    c=1 if n in (0,1) else 2
    assert (n-3**c)%4==(1 if n%2==0 else 2)
def rank5(k):
    u=Fraction(U(k),81)
    from math import ceil
    return k+1+4*min(5,ceil(9*(Fraction(2,3)-u)))
assert min(map(rank5,range(13)))==20
print("Independent prime-power semantics, parity, and exact rank-five inequality checked")
```
