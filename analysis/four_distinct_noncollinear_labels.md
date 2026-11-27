# Four distinct exponent labels: a noncollinear construction and affine obstruction

**Four distinct labels on each axis are possible at ordinary height.** The explicit family below has \(\Theta((\log X)^2)\) distinct targets up to \(X\). For its exact offsets, a determinant obstruction rules out a free affine parameter even when the four rows may use different directions. The power-law question remains open outside that template.

## Four labels at one target

Take \(T=5^U,\ W=3^V\), where \(U\ge5\) and \(\lceil U/2\rceil\le V\le U\). Set
\[
n=450T^2+1218TW+7578W^2.
\]
The labels are \((c,d)=(2V+c_0,2U+d_0)\).

| \((c_0,d_0)\) | Square coordinates |
|---|---|
| \((2,0)\) | \(20T,\ 7T+87W\) |
| \((4,1)\) | \(21T+21W,\ 2T+84W\) |
| \((0,2)\) | \(19T+59W,\ 8T-64W\) |
| \((6,3)\) | \(17T+57W,\ 6T-60W\) |

In each row, adding \(3^c+5^d\) to the two squares gives \(n\) by coefficient comparison. Every residual is positive. The determinant of the first two coordinate differences is
\[
-4T^2+162TW-2994W^2<0
\]
because its discriminant is negative, so the witnesses are genuinely noncollinear.

For \(Q=125T^2\), the bound \(W/T\le243/3125\) gives \(Q<n<5Q\). At fixed \(U\), the target increases strictly with \(V\). Adjacent \(U\)-layers are disjoint since \(Q\) grows by a factor of \(25\). Summing the number of allowed \(V\) over \(U\) gives the stated count. Both exponent axes grow on the order of \(\log n\).

At \(U=5,V=3\), the target is \(4{,}502{,}824{,}362\), with exponent pairs \((8,10),(10,11),(6,12),(12,13)\). At this same target the crossed label \((8,12)\) fails: its positive residual is \(247\bmod361\), so \(v_{19}=1\).

## Exact affine obstruction

Write the four shifts as \(s_i=a_iT^2+b_iW^2\), with \(a_i=5^{d_i}\), \(b_i=3^{c_i}\). A shared-direction solution \(z_i=z+\ell_iw\) requires
\[
s_i-s_0=-2\ell_i(z\cdot w)-\ell_i^2N(w),\qquad \ell_0=0.
\]
Thus both ordered coefficient lists must be quadratic in the **same** four rational parameters.

For coefficient points \((a_i,b_i)\) spanning an affine plane, let \(r_i\) be the signed triangle cofactors, so \(r\) annihilates \(1,a,b\). Any four distinct parameters must satisfy \(r\cdot\ell=r\cdot\ell^2=0\). A zero cofactor already rules this out by the Vandermonde formula. Otherwise normalize \(\ell_0=0,\ell_1=1\). Eliminating \(\ell_3\) gives
\[
r_2(r_2+r_3)\ell_2^2+2r_1r_2\ell_2+r_1(r_1+r_3)=0.
\]
Its discriminant is \(4r_0r_1r_2r_3\). The product must be a rational square. For the displayed ordinary-height family the primitive cofactors are
\[
(705,-571,-189,55).
\]
Their product has \(v_7=1\), giving an exact exclusion.

**This also rules out row-dependent affine directions** of the form
\[
z_i(T,W,t)=A_i(T,W)+tB_i(T,W),
\qquad A_i,B_i\text{ fixed rational affine-linear maps}.
\]
To see this, compare the quadratic and linear coefficients of \(t\). The homogeneous parts of the \(B_i\) have a common Gram matrix. For the degree-two parts in \(T,W\), constant terms in the anchors and directions do not participate. In rank two, constant rational orthogonal changes align them to one direction \(F(T,W)\). Each rotated homogeneous anchor difference is linear in \(F\) and perpendicular to \(F\) identically. Its matrix in \(F\)-coordinates is therefore skew-symmetric, so the difference is \(\ell_i JF\) for a constant rational \(\ell_i\), where \(J\) is a quarter-turn. This recovers the cofactor test. The leading coefficients on both axes are strictly negative because they are negatives of squared lengths.

In rank one, alignment instead leaves a common projection and one perpendicular coordinate \(p_iT+q_iW\) per row. Constant-only directions give the same equations. Coefficient comparison then forces
\[
(A-a_i)(B-b_i)=p_i^2q_i^2=K
\]
with \(K\) common. If \(K=0\), at most two rows fit. If \(K>0\), increasing \(a_1<a_2<a_3\) forces decreasing \(b_1>b_2>b_3\), with
\[
\frac{b_1-b_2}{b_2-b_3}
=\frac{a_2-a_1}{a_3-a_2}\frac{A-a_3}{A-a_1}<\frac14.
\]
For decreasing powers of \(3\) the left side exceeds \(2\). This excludes rank one. The same proof applies if the identities are required only at \(T=5^U,W=3^U\) for infinitely many \(U\), with at least three \(t\)-values per layer: comparison in \(t\), followed by the distinct exponential rates \(5^a3^b\), forces the coefficient identities.

### Sign, integrality, and the finite check

A square cofactor product alone can pass while the curvature fails. For actual power lists \(a=(1,25,125,625)\) and \(b=(3,9,1,27)\), both rational branches have **positive** leading coefficients on both axes. In the finite normalized box with both maximum offsets at most \(15\), this was the only positive square product among \(4{,}968{,}600\) pairings. The exact \(v_7\) exclusion above is independent of this enumeration.

The dot-product gate is separate. With primitive integral line differences and an integral direction \(w\), the required value of \(z\cdot w\) must be divisible by \(\gcd(w_x,w_y)\). A three-row control uses offsets \((c,d)=(0,2),(3,6),(4,0)\) and parameters \((0,1,4)\). At \(T=5,W=3\) the required direction norm is \(130068=252^2+258^2\), but the required dot product is \(-260151\). Every direction of that norm has both coordinates even, so the integral chart fails despite the correct sign and a true direction norm.

### Independent replay

```python
from fractions import Fraction as F
from itertools import combinations, permutations
from math import gcd, isqrt, prod
import sys

rows = [(2,0,20,7,0,87), (4,1,21,2,21,84),
        (0,2,19,8,59,-64), (6,3,17,6,57,-60)]

def area(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def cofactors(P):
    return [(-1)**i*area(*(P[:i]+P[i+1:])) for i in range(4)]

T,W = 5**5,3**3
n = 450*T*T+1218*T*W+7578*W*W
Z = []
for c,d,a,b,u,v in rows:
    assert (a*a+b*b+5**d,a*u+b*v,u*u+v*v+3**c) == (450,609,7578)
    x,y = a*T+u*W,b*T+v*W
    assert n-3**(6+c)-5**(10+d) == x*x+y*y > 0
    Z.append((x,y))
assert n == 4502824362 and (n-3**8-5**12)%361 == 247
assert area(*Z[:3]) == -4*T*T+162*T*W-2994*W*W < 0
assert 450*3125**2+1218*243*3125+7578*243**2 < 625*3125**2

r = cofactors([(5**d,3**c) for c,d,*_ in rows])
r = [x//gcd(*r) for x in r]
assert r == [705,-571,-189,55] and prod(r)%49 == 7*(prod(r)//7%7) != 0

A,B = (1,25,125,625),(3,9,1,27)
r = cofactors(list(zip(A,B)))
D = prod(r)
assert isqrt(D)**2 == D
for sign in (-1,1):
    u = F(-r[1]*r[2]+sign*isqrt(D), r[2]*(r[2]+r[3]))
    v = -(r[1]+r[2]*u)/r[3]
    assert len({0,1,u,v}) == 4
    for P in (A,B):
        lead = (P[2]-P[0]-u*(P[1]-P[0]))/(u*(u-1))
        assert lead > 0
        assert P[0]+(P[1]-P[0]-lead)*v+lead*v*v == P[3]

h,k = 390868-634,754-634
G = 252**2+258**2
assert 4*h-k == 12*G and G%4 == 0 and (h+G)%4 == 2

if "--bounded" in sys.argv:
    E = [(0,)+e for e in combinations(range(1,16),3)]
    L = [tuple(5**d for d in e) for e in E]
    R = [p for e in E for p in permutations(3**c for c in e)]
    hits = []
    for a in L:
        for b in R:
            v = prod(cofactors(list(zip(a,b))))
            if v > 0 and isqrt(v)**2 == v:
                hits.append((a,b))
    assert len(L)*len(R) == 4968600 and hits == [(A,B)]

print("PASS")
```
