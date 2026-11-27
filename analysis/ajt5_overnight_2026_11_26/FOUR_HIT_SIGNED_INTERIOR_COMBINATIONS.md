# Fixed signed four-hit shapes with a genuine interior point

In the same two-order chart as FOUR_HIT_POSITIVE_COMBINATIONS, fix m≥q+2 and q≥1. Consider 0,v,w,mv−qw with coordinate diameter ≤R, 2R<D=rs and v=(ah,bk), w=(ch,dk), with positive coefficients ≤M, both steps nonzero, and ad≠bc. For the fixed actual n and primes p not dividing n where both axis multipliers have exact odd order D, the number of (p, shape with start) pairs is O_(m,q)(R² M⁴/log D). This is a divisibility result, not a two-square or pointwise coverage theorem.

The affine coefficients (m−q−1,−m,q,1) have three positives and one negative: v is genuinely interior. Up to permutation and overall sign this differs from the earlier positive-combination shapes. For m≤q one can rebase at w to write the final offset as m(v−w)+(q+1−m)(−w), though applying the old bound after rebasing still requires the same-sign-per-axis and coefficient cap checks. For m=q+1 three points are collinear.

For the interior case absorb gcds into h and k. Put U=3^(720h), V=5^(720k), Z=V^b, P=ma−qc, Q=mb−qd, A=U^a−1, C=U^c−1, L=U^P−1, and T0=A+C(Z−1). Any two distinct hit points cannot repeat exactly one axis, by exact order and the diameter. Thus the eligible tuples satisfy a≠c, b≠d, P∉{0,a,c}, Q∉{0,b,d}. The two polynomials are
```
F = A^b Z^d − T0^b
G = [A^(q+1) Z^m − T0^q (A+L(Z−1))]/(Z−1).
```
The second division is exact, and U^max(0,−P) clears Laurent powers without changing the field roots. The leading Z coefficient is a monomial in U times A^(q+1), a unit in a realized finite-field hit. Thus fixed p,h gives at most m−1 values of k by exact order and the short window. First two hits determine the start uniquely as before.

## Nonzero resultant

Use a valuation on an algebraic function-field extension in residue characteristic zero. In a common root, Z=0 would force a=c. Z=1 is excluded by G's value A^q(mA−qC−L), nonzero since the exponents 0,a,c,P differ. Write eta=T0/A and T=Z^m/eta^q, so eta^b=Z^d and T^b=Z^Q.

For P,Q of the same sign, take ν(U)=−1. If ν(Z)>0 then ν(eta)>0 and A(eta−1)=C(Z−1) forces a=c. If ν(Z)<0, then ν(eta)−ν(Z)=a−c. Also A(T−1)=L(Z−1) tests the pole terms when P,Q>0, and the unit terms when both are negative. In either case the two equations imply ν(Z)=−a, ν(eta)=−c, incompatible with ad≠bc. If ν(Z)=0, one of Z−1 and eta−1 has positive valuation and the other zero since a≠c. If a>c then P>a and ν(T−1)<0, impossible. If c>a, ν(Z−1)=c−a and ν(T−1)=c−max(P,0). This last value cannot be negative; equality would mean P=c. If positive, T^b=Z^Q equates it with ν(Z−1) in residue characteristic zero, forcing P=a.

For P<0<Q take ν(U)>0 instead. If ν(Z)<0, the two units A,C in the relation for eta force ν(eta)=ν(Z), hence b=d. If ν(Z)>0, T−1 and Z−1 are units but L has a pole, impossible. If ν(Z)=0, the pole forces Z→1 and then eta→1 and T→1, contradicting the equality of ν(T−1) and ν(Z−1) given by T^b=Z^Q. For the other mixed sign, swap axes: gcd(b,d)=1 lets one extract V as an integral Laurent product of Z and eta; it is transcendental since C/A is nonconstant and Z≠1. The same argument therefore applies.

After swapping axes if appropriate, let A0=max(a,c)≥B0=max(b,d). The resultant has degree O_(m,q)(A0B0) and log coefficient norm O_(m,q)(B0) by the Sylvester determinant (fixed count of F rows, each of log norm O(B0); O(B0) bounded G rows). Nonzero specializations cost total cleared log height O_(m,q)(R²). Both directions of the Cauchy bound put any zero specialization at |h|=O_(m,q)(B0), leaving O_(m,q)(R) pairs (h,k).

For every zero specialization, at least one original rational cross determinant is nonzero. If both vanished, normalize at the interior vertex. The three external positive reads X_i,Y_i would satisfy Y_i=1+σ(X_i−1) and both weighted products would be 1, with weights (m−q−1,q,1). The strictly concave weighted log sum of the positive factors 1+t(X_i−1) cannot have three distinct zeros at 0,1,σ. Distinctness follows because a nonzero power of 3 cannot equal a nonzero power of 5. Each of these exact rational determinants costs log height O_(m,q)(R). Divide the total height by log(2D+1) for prime counts and sum over M⁴ tuples.

## Exact same-target control

Below the true 3v−w fourth point has remainder 799p modulo p² and the alternative has residue 116 even with the same three-hit condition. Both step signs are negative, and both fourth offsets have P<0<Q. The true two-square remainder is separately at the chart head.

```python
from fractions import Fraction
from math import gcd, isqrt

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

L,z = 146651884329720, 1 << (H//2-4)
x,y = (z+(a-z)%L for a in (61827877807697,135417323161960))
n = S(0,0)+85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert n%(p*p) == 1223507

o,v = (133,187),(-36,-67)
def read(w):
    u,k = (a+b for a,b in zip(o,w))
    assert 0 <= u < J and 0 <= k < J
    return (n-S(u,k,p*p))%(p*p)

for w,expected in [((-123,-30),1005941),((-117,-113),37886)]:
    assert v[0]*w[1] != v[1]*w[0]
    f = tuple(3*a-b for a,b in zip(v,w))
    assert all(read(z) in range(p,p*p,p) for z in ((0,0),v,w))
    assert read(f) == expected
    h,k = (-gcd(a,b) for a,b in zip(v,w))
    a,b,c,d = v[0]//h,v[1]//k,w[0]//h,w[1]//k
    P,Q = 3*a-c,3*b-d
    assert h < 0 and k < 0 and P < 0 < Q
    U,V = pow(3,720*h,p),pow(5,720*k,p)
    A,C,L,Z = U**a-1,U**c-1,pow(U,P,p)-1,pow(V,b,p)
    T = A+C*(Z-1)
    assert A%p and C%p and (Z-1)%p and T%p
    assert (A**b*Z**d-T**b)%p == 0
    assert ((A*A*Z**3-T*(A+L*(Z-1)))%p == 0) == (expected%p == 0)
    if expected%p == 0:
        X,Y = Fraction(3)**(720*v[0])-1,Fraction(5)**(720*v[1])-1
        for i,j in (w,f):
            det = X*(Fraction(5)**(720*j)-1)-Y*(Fraction(3)**(720*i)-1)
            assert det and det.numerator%p == 0 and det.denominator%p

assert 1005941 == 799*p and 37886%p == 116
print(n%p,read((15,-171)),read((9,-88))%p)  # 1018 1005941 116
```
