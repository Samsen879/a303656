# Four-hit sparsity for fixed positive combinations

Fix an actual n, a short exponent chart of axis widths <D, and primes p not dividing n where the two axis multipliers 3^720 and 5^720 both have exact odd order D=rs. Fix positive integers m,l. Count hits of 0,v,w,mv+l w with coordinate diameter ≤R, 2R<D, v=(ah,bk), w=(ch,dk), all four coefficients in [1,M], hk nonzero, ad≠bc. Then the number of (p, realized shape with start) pairs is O_(m,l)(R² M⁴/log D). This is about a restricted divisibility chart.

Write U=3^(720h), V=5^(720k), Z=V^b, A=U^a−1, C=U^c−1, L=U^(ma+lc)−1. The third hit gives eta=(A+C(Z−1))/A. The fourth and eta^b=Z^d give
```
F = A^b Z^d − [A+C(Z−1)]^b
G = [Z^m (A+C(Z−1))^l − A^l − A^(l−1) L(Z−1)]/(Z−1).
```
The division is exact as polynomials. In a realized shape A,C,Z−1 are units because the nonzero differences have size <D. If a=c, the third hit gives eta=Z, forcing b=d by exact order and the diameter bound, contrary to ad≠bc. Thus such tuples contribute zero. We may work with a≠c.

For nonvanishing of Res_Z(F,G), take the valuation ν(U)=−1, with residue characteristic zero, extending it to a hypothetical common root. Z=0 contradicts a≠c; Z=1 fails G because L has higher degree than mA+lC. Let u=ν(Z), v0=ν(eta), with du=bv0. If u>0 then both Z−1 and eta−1 have valuation zero, forcing a=c in A(eta−1)=C(Z−1). If u<0, the same equation gives v0−u=a−c, while Z^m eta^l−1=(L/A)(Z−1) gives (m−1)u+lv0=−((m−1)a+lc). Thus u=−a and v0=−c, contrary to ad≠bc. If u=0, the fourth-hit equation forces ν(Z−1)≥(m−1)a+lc>0 and the third then gives positive ν(eta−1). The identity eta^b=Z^d in residue characteristic zero equates those two valuations, again forcing a=c.

Exchange chart axes to have A0=max(a,c)≥B0=max(b,d). The Sylvester determinant has a fixed number of F rows, each of log coefficient norm O(B0), and O(B0) G rows of bounded coefficient norm. This gives degree O_(m,l)(A0 B0) and log coefficient norm O_(m,l)(B0). Summing the log of its nonzero cleared numerator over 0<|h|≤R/A0 costs O_(m,l)(R²). For each p,h, G has degree m+l−1 and leading coefficient C^l≠0. The map k↦V^b is injective in the short interval (span ≤2R), and the first two hits determine the start uniquely by the two-axis linear system, since n is nonzero mod p and thus the two axis multipliers along v differ.

For zero resultants at actual U, apply the Cauchy bound to the polynomial and to its reciprocal after removing any factors U, giving |h|=O_(m,l)(B0) and leaving O_(m,l)(R) pairs (h,k). At least one original rational cross determinant is nonzero for every such shape. Otherwise the strictly convex positive-real function f(t)=(1+t(λ−1))^m (1+t(ξ−1))^l, with λ=U^a and ξ=U^c, would match the same secant at 0,1,ρ=(V^b−1)/(λ−1). The points are distinct (a nontrivial power of 3 cannot equal a nontrivial power of 5), both factors positive on their hull by the assumed third hit, and λ−1 and ξ−1 have the same sign. The remaining rational determinant has cleared logarithmic height O_(m,l)(R). Each p≥2D+1, so divide the total O_(m,l)(R²) height by log(2D+1), then sum over at most M⁴ coefficient tuples.

## Same actual target: 2v+2w positive and negative controls

This geometry is distinct from mv+w: the primitive affine coefficient multiset is (3,−2,−2,1), up to sign. For first-point 3-term weight θ, let κ=θ(1−θ)(λ−μ)(ξ−eta). Conditional on the first three hits, the fourth hit at 2(v+w) is equivalent to (1+κ)^2+θ(1−θ)(λξ−μ eta)^2=1, by the weighted second-moment identity. Below, the two fourth-point readouts are 1 and 327 modulo 1259. The exact-once divisible points are blocked from being two-square norms by the inert prime; the actual two-square witness is the separate head point. Arbitrary signed fourth combinations and the general pointwise gap are unaddressed.

```python
from math import isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
D = r*s
def prime(q):
    return q > 2 and q%2 and all(q%d for d in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p == 2*D+1 and p%4 == 3
assert t%720 == 1 and 16*t <= H <= 24*t and J == H//12000 and 2*J < D
for q in (3,5):
    assert pow(q,720*D,p) == 1
    assert all(pow(q,720*(D//ell),p) != 1 for ell in (r,s))

def S(u,v,m=None):
    return pow(3,3*t+80+720*u,m) + pow(5,t+144+720*v,m)

M,z = 146651884329720, 1 << (H//2-4)
x,y = (z+(a-z)%M for a in (61827877807697,135417323161960))
n = S(0,0)+85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert n%(p*p) == 1223507

u,v,h,k = 274,110,3,18
def read(i,j):
    assert 0 <= u+i < J and 0 <= v+j < J
    return (n-S(u+i,v+j,p*p))%(p*p)

th = pow(3,3*t+80+720*u,p)*pow(n,-1,p)%p
L,T = pow(3,720*h,p),pow(5,720*k,p)
for g,l,expected,K0,E0 in [(11,13,647126,1056,1),(10,30,556986,1034,327)]:
    assert h*l != k*g
    assert all(read(i,j) in range(p,p*p,p) for i,j in ((0,0),(h,k),(g,l)))
    assert read(2*(h+g),2*(k+l)) == expected
    C,B = pow(3,720*g,p),pow(5,720*l,p)
    K = th*(1-th)*(L-T)*(C-B)%p
    E = ((1+K)**2+th*(1-th)*(L*C-T*B)**2)%p
    assert (K,E,(n*(1-E))%p) == (K0,E0,expected%p)
assert 647126%p == 0 and 556986%p == 508
```
