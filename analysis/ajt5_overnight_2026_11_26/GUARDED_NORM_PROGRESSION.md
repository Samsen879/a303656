# A guarded row: genuine integer witnesses but a prime-value gap

For the parent m=p²+2188 and its fixed child row f=0, the residual is 5p²+10940. It is a Gaussian norm iff p²+2188 is one. For integers p in a progression a mod M with 4|M and a≡3 mod 4, necessary and sufficient finite tests are: at 547, exclude a=0 mod 547 if that prime divides M; at any other inert q^h||M, if v_q(a²+2188)<h then it must be even. Indeed high zero at q≠547 is a simple unit root and can be lifted to exact even valuation; 2 automatically passes and split places impose no square-sum condition.

Here is a constructive proof of sufficiency. Extend the 2-adic progression to a specified odd class mod 8 if needed. Choose a prime k>sqrt(547) coprime to 547 M so both congruences v0²≡547 mod k and v0²≡547−k²+ak mod M are solvable. For the second, at 2 take k≡7 a^(-1) mod 8. At each odd q|M pick local p≡a and local square-sum coordinates x,y for p²+2188 with x not congruent to p mod q. Such coordinates are possible: a nonzero norm residue has q±1 solutions and at most two have x=p; a zero has either coordinates divisible by q (inert) or a split line (split), and the former here has p a unit. Then k=(p−x)/2 and v=y/2 give the required residue with k a unit. At 547 if present, require k a nonzero square: write a=w²+z² mod 547 with w,z nonzero, use k=w² and v=wz mod 547, and lift by the unit derivative in v. If absent choose a harmless square class for k mod 547 anyway. CRT and Dirichlet choose prime k in these prescribed classes, and reciprocity gives sqrt(547) mod k since k≡1 mod 4. The two congruences for v0 combine by CRT. Now v=v0+kMt, p=k+(v²−547)/k, x=p−2k, y=2v. Then p≡a mod M and x²+y²=p²+2188 identically, giving unbounded genuine integer bridges. It does not make the quadratic polynomial p prime infinitely often.

For fixed reduced a mod M the prime witnesses have zero relative density: choose a new finite panel of inert ell≡1 mod 547. Each has two unit simple roots of p²+2188, with 2(ell−1) lifted unit classes mod ell² of exact odd valuation. The fixed-period prime density bound is product(1−2/ell); the harmonic sum over these ell diverges by the prime number theorem in progressions. Take the prime count limit first, then enlarge the panel. This does not rule out infinitely many prime witnesses.

Exact true/false and quadratic progression controls:

```python
from math import isqrt

for p in (31, 41203):
    assert p % 188 == 31
    assert all(p % d for d in range(2, isqrt(p) + 1))
assert 5*31**2 + 10940 == 5*47*67
assert 5*41203**2 + 10940 == 10293**2 + 91556**2

M, a, k, v0 = 8836, 5859, 509, 12831
v = v0 + k*M
p = k + (v*v - 547)//k
x, y = p - 2*k, 2*v
assert (v*v - 547) % k == 0 and p % M == a
assert p == 39967195451
assert all(p % d for d in range(2, isqrt(p) + 1))
assert (2*x-y)**2 + (x+2*y)**2 == 5*p*p + 10940
```
