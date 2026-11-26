# Integer work-parameter criterion for ten protected rows

Take K=C_e−9^j, C_e in {10941,10937}, 0≤j≤4. All these K are positive multiples of four with squarefree odd part. With fixed m=p²+2188, the chosen child residual is F(p)=5p²+K. In p≡a mod M, 4|M and a≡3 mod 4, genuine integer witnesses exist iff (i) no inert q|M divides both a and K and (ii) every inert valuation of F(a) below v_q(M) is even. Necessity in (i) uses the squarefree odd part. For sufficiency, a contact not frozen has unit derivative 10a and can be lifted to exact even depth. The 2-adic odd part is 1 mod 4, and split places impose no norm condition.

Put D=5K/4. Choose an auxiliary prime k>sqrt(D) coprime to 5DM, and w0 with w0²=D mod k, w0²=D−k²+5ak mod 5M, and w0=3k mod 5. Then for each integer t let
```
w=w0+5kMt
p=(w²+k²−D)/(5k)
x=p+(-2k+4w)/5
y=2p+(-4k−2w)/5.
```
The congruences ensure these are integers and p≡a mod M. Expansion gives x²+y²=5p²+K.

For completeness the auxiliary k can be chosen by prescribing a reduced class. At 2 take k odd and w of parity D; the derivative of k²−5ak+w²−D with respect to k is odd. At 5 choose unit k and w=3k mod 5, then lift in w. At q not dividing 10D, a local Gaussian norm pair for F(p) yields k=(5p−x−2y)/2 and w=(2x−y)/2. A unit k can be chosen: for a unit norm the mod-q circle has q±1 points, and the line k=0 removes at most two; at zero norm either p is a unit (inert) or the split lines supply a choice. At an odd q|D other than 5 with b=5a a unit, w²=k(b−k) admits k=b and w=0 (lift in k), and also k=bu with u and 1−u nonsquares (lift in w). These give both signs of (k/q). If b=0 the local hypothesis forces q split, and either unit sign for k is possible. For q|D absent from the progression there is no local restriction on k mod q. Since each of the ten D has an odd prime factor other than 5 of exponent one, at least one such sign can tune (D/k)=1 under quadratic reciprocity. CRT and Dirichlet then provide k, and CRT supplies w0.

This is a quadratic family for integer p, not a proof of endlessly many prime p. A fixed reduced class still has relative prime-witness density zero: there is a reduced inert auxiliary progression of positive prime density where F has two simple unit roots (−5K is not the squareclass of −1 since K is not a norm). The exact valuation-one exclusions have conditional measure 2/q at each auxiliary q. Finite CRT first and harmonic divergence second prove zero density, without ruling out infinitely many prime witnesses.

```python
from math import isqrt

assert 7 % 12 == 67 % 12
assert (5*7**2 + 10936) % 9 == 3
assert (5*67**2 + 10936) % 27 == 9
assert 5*67**2 + 10936 == 90**2 + 159**2
assert 10932 % 9 == 6                 # 3 | p 时恒有 v3 = 1

K, M, a, k, w = 10936, 2700, 67, 241, 8268
D = 5*K//4
assert (w*w+k*k-D) % (5*k) == (w-3*k) % 5 == 0
p = (w*w+k*k-D)//(5*k)
x, y = p+(-2*k+4*w)//5, 2*p+(-4*k-2*w)//5
assert p == 56767 and p % M == a
assert all(p % q for q in range(2, isqrt(p)+1))
assert x*x+y*y == 5*p*p+K
```
