# Denominator-two four-hit shapes and the lost sign

In an actual two-order short exponent chart, fix 2f=mv+jw. Its affine coefficients are (m+j−2,−m,−j,2). The true fixtures (m,j)=(3,3),(9,−5) have primitive relations whose coefficients all have absolute value >1, so no relabeling makes one point an integer affine combination of the others.

Let v=(ah,bk), w=(ch,dk) with positive coefficients at most M, nonzero signed h,k, and ad≠bc. Put U=3^(360h), V=5^(360k), P=ma+jc, Q=mb+jd. Require hP,kQ to be even as integers; the real fourth multipliers are U^P,V^Q. Define A=U^(2a)−1, C=U^(2c)−1, L=U^P−1, Z=V^(2b), B=A+C(Z−1), K=A+L(Z−1). The third read is eta=B/A, the required fourth read is Omega=K/A. For l=max(j,0), q=max(−j,0), the necessary polynomials are
```
F = A^b Z^d − B^b
G = [A^(2+q) Z^m B^l − A^l B^q K²]/(Z−1).
```
The numerator is exactly divisible by Z−1, and U^max(0,−2P) clears any Laurent denominators. Exact order and pairwise distinct axes make A,C,Z−1 units in a realized hit. The equation for G imposes a square only. When p≡3 mod 4, actual V^Q is a square (since kQ is even), so the sign can be recovered by also requiring Omega to be a square. The fifth real fixture below has Omega=−V^Q: both squared relations pass, but the fourth true remainder is 500 modulo p.

## Sparse case and proof boundaries

For fixed m,j with m,j≥2, or j=−q, q≥2, m≥q+4, the number of realized (p, short shape with start) pairs is O_(m,j)(R² M⁴/log D) in the standard chart with common exact order D=rs, 2R<D, p not dividing n and coordinate diameter ≤R. Normalize gcd(a,c)=gcd(b,d)=1 by absorbing factors into h,k. Eligible hits have a≠c,b≠d, P∉{0,2a,2c}, Q∉{0,2b,2d} by nonrepetition of axis coordinates. The finite-field leading coefficient of G is a monomial times A^(2+q) C^l and its Z-degree is m+l−1. Exact order limits k to that many values for fixed p,h and the first two hits uniquely fix the start.

Here is the nonvanishing argument for Res_Z(F,G). A hypothetical common root is neither Z=0 (F and a≠c) nor Z=1 (G is A^(q+l+1)(mA+jC−2L), up to the Laurent clearing factor). The root satisfies eta^b=Z^d, Omega^(2b)=Z^Q and the two equations A(eta−1)=C(Z−1), A(Omega−1)=L(Z−1). Work at characteristic-zero function-field valuations:
- If P,Q have the same sign use ν(U)=−1. Positive ν(Z) forces a=c. Negative u=ν(Z) gives ν(eta)=u+2a−2c and then u=−2a, ν(eta)=−2c: for P,Q>0 substitute 2ν(Omega)=m u+jν(eta) into the pole equation, using m+j−2>0; for P,Q<0 use that Omega−1 and L are units. Both contradict ad≠bc. For u=0 and a>c, P>2a forces a pole in Omega−1. For u=0 and c>a, the relation for eta forces ν(Z−1)=2(c−a); ν(Omega−1)=2c−max(P,0). Negative is impossible, zero forces P=2c, positive forces P=2a by Omega^(2b)=Z^Q and residue characteristic zero.
- For P<0<Q use ν(U)>0. Negative ν(Z) forces b=d, and positive ν(Z) would give a pole against a unit in the fourth-hit equation. When ν(Z)=0 the pole of L forces Z→1, then eta→1. But (eta−1)/(Z−1)→1 from C/A, against d/b from eta^b=Z^d.
- For P>0>Q reconstruct V from Z=V^(2b), eta=V^(2d) using gcd(b,d)=1 and a square root. It is transcendental since C/A is nonconstant. Use ν(V)>0, so Omega=±V^Q has a pole, and (eta−1)/(Z−1)→1. If ν(U)<0, this ratio equals C/A, a nonunit valuation since a≠c. If ν(U)>0, the fourth-hit identity equates a pole to a unit. If ν(U)=0, that identity forces U^(2a)→1 and the third forces U^(2c)→1. The ratio C/A then tends to c/a, not 1. This handles both formal signs.

With A0=max(a,c)≥B0=max(b,d) after exchanging axes if necessary, the Sylvester bound gives degree O_(m,j)(A0B0), log coefficient norm O_(m,j)(B0), and total nonzero specialized log height O_(m,j)(R²). The direct and reciprocal polynomial root bounds put any zero specialization at |h|=O_(m,j)(B0), leaving O_(m,j)(R) pairs (h,k). At each, the original unsquared rational cross determinants cannot both vanish. For positive combinations the function (1+t(λ−1))^(m/2)(1+t(ξ−1))^(j/2) is strictly convex on the positive-factor interval and cannot meet its secant in a third point. The exponents are ≥1 and both slopes have the same nonzero sign. For the signed interior case use the positive weights (m−q−2,q,2) after rebasing at v; the weighted log sum is strictly concave and cannot have three zeros. Each short determinant has log height O_(m,j)(R). Divide the resulting height bound by log(2D+1) and sum over M⁴ coefficient tuples. This is a chart divisibility bound with the specified fixed coefficients, not a pointwise criterion for the conjecture.

## Exact same-target replay

The two positive/negative pairs keep identical first three hits; the final line is the additional unfiltered-square false positive. The same n has a separate true two-square witness at the head.

```python
from math import gcd, isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
D = r*s
def prime(q):
    return q > 2 and q%2 and all(q%d for d in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p == 2*D+1 and p%4 == 3
assert t%720 == 1 and 16*t <= H <= 24*t and J == H//12000 and 2*J < D
for q in (3,5):
    assert pow(q,720*D,p) == 1
    assert all(pow(q,720*(D//e),p) != 1 for e in (r,s))

def S(u,v,m=None):
    return pow(3,3*t+80+720*u,m) + pow(5,t+144+720*v,m)

M,z = 146651884329720, 1 << (H//2-4)
x,y = (z+(a-z)%M for a in (61827877807697,135417323161960))
n = S(0,0)+85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert n%(p*p) == 1223507

cases = [
    (3,3,(48,176),(13,-45),(107,-9),108274,1),
    (5,3,(48,176),(13,-45),(107,-9),908471,0),
    (9,-5,(171,9),(7,72),(51,120),275721,1),
    (11,-5,(171,9),(7,72),(51,120),1351412,0),
    (3,3,(61,131),(10,7),(92,63),1102125,-1),
]
for m,j,o,v,w,expected,sign in cases:
    assert gcd(m,gcd(j,2)) == 1
    assert min(map(abs,(m+j-2,-m,-j,2))) > 1
    assert v[0]*w[1] != v[1]*w[0] and all(a*b > 0 for a,b in zip(v,w))
    f2 = tuple(m*a+j*b for a,b in zip(v,w))
    assert all(a%2 == 0 for a in f2)
    f = tuple(a//2 for a in f2)
    def read(z):
        u,k = (a+b for a,b in zip(o,z))
        assert 0 <= u < J and 0 <= k < J
        return (n-S(u,k,p*p))%(p*p)
    assert all(read(z) in range(p,p*p,p) for z in ((0,0),v,w))
    assert read(f) == expected and (expected%p == 0) == (sign == 1)

    h,k = (gcd(a,b)*(1 if a>0 else -1) for a,b in zip(v,w))
    a,b,c,d = v[0]//h,v[1]//k,w[0]//h,w[1]//k
    U,V = pow(3,360*h,p),pow(5,360*k,p)
    P,Q = m*a+j*c,m*b+j*d
    A,C,L = pow(U,2*a,p)-1,pow(U,2*c,p)-1,pow(U,P,p)-1
    Z,E,O = pow(V,2*b,p),pow(V,2*d,p),pow(V,Q,p)
    assert A%p and C%p and (Z-1)%p and E and O
    assert (A*(E-1)-C*(Z-1))%p == 0
    W = (1+L*(Z-1)*pow(A,-1,p))%p
    assert (O*O-pow(Z,m,p)*pow(E,j,p))%p == 0
    if sign:
        assert W == sign*O%p
    else:
        assert (W*W-O*O)%p
    print(m,j,tuple(a+b for a,b in zip(o,f)),expected%p,sign)
```
