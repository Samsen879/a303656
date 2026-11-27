# Eighteenth certified sphere ray at phase 182/9

**The seed \((m,e)=(182,262)\) adds an eighteenth ray at phase \(182/9\)**, strictly inside \(178/9<182/9<22\). Both half-norms have explicit integer certificates. The largest phase ratio moves to \(42/38=21/19\), improving the uniform generated-population exponent from \(89/198\) to **\(19/42\)** in both odd classes.

### Seed certificate

At scale \(9\), the gap restricts \(m\equiv2\bmod4\) to \(182,186,190,194\). The corresponding upper endpoints for \(e\equiv2\bmod4\) under \(3^e<5^m\) are \(266,270,278,282\). Splitting the difference into \(5^{m/2}\pm3^{e/2}\) and removing powers of \(2\) gives two coprime odd parts. This reduces the search to two smaller norm tests per pair in a strip of 276 pairs.

For \(A=5^{91}\), \(B=3^{131}\), and \(N(x,y)=x^2+3y^2\), the certificates are

| Half | \(x\) | \(y\) |
|---|---:|---:|
| \((A+B)/8\) | 1884630968404488393574193593822 | 13430202510315397746466720933895 |
| \((A-B)/2\) | 32819044663843824833457230296681 | 16157833321322752107598891112924 |

Direct squaring verifies both rows. Since \(\gcd(91,131)=1\), this seed does not come from a common seventh-power lift or any other common lift of degree greater than one.

### Growing labels and exact same-height controls

Call the two rows \((a,b)\) and \((c,d)\). Start with \(v=8|ac-3bd|\), \(w=8(ad+bc)\). At depth \(k\), write \(Q=5^{182\cdot3^k}\), \(Z=3^{262\cdot3^k}\), and \(s=\sqrt Z\). Before cubing \(Q,Z\), multiply \(v+w\sqrt{-3}\) by
\[
\frac{Q-Z}{2}+(-1)^{k+1}\frac{Q+Z}{2}\sqrt{-3}.
\]
The recurrence preserves \(v^2+3w^2=4(Q-Z)\) and \(v,w\in4\mathbb Z\). The ratio \(w/v\bmod3\) alternates between \(2\) and \(1\).

It also preserves \(w^2>3Z\). The initial angle lies below \(\pi/3\) by an angle with tangent between \(1/10\) and \(1/8\). Each shell angle exceeds \(\pi/3\) by a decreasing amount less than \(1/160\). With alternating signs, the even-depth angles stay above \(\pi/4\), and the odd-depth angles have absolute sine at least \(1/\sqrt{101}\). The bounds \(Q/Z>160\) initially and \(Q/Z>160^3\) at odd depths give the claimed inequality.

For \(\lambda=1,3\), use
\[
S_1(t)=(t-s)^2+t^2,\qquad S_3(t)=(t+s)^2+(t-2s)^2,\qquad
n_\lambda(t)=5Q+\lambda Z-S_\lambda(t).
\]
At \(t=|w|\), both classes have true positive representations:
\[
Q<n_\lambda(t)<5Q,\qquad
n_\lambda(t)=Q+(4-\lambda)Z+v^2+(t+s)^2.
\]
The classes are \(21\bmod24\) for \(\lambda=1\) and \(3\bmod24\) for \(\lambda=3\). The positive exponent pairs \((c,d)\) are \((262\cdot3^k+1,182\cdot3^k)\) and \((262\cdot3^k,182\cdot3^k)\), respectively.

The same height windows and classes also contain signed witnesses for which the selected positive pair fails. At depth \(0\), take \(t=s+5\). In both classes the positive residual is \(37464=168\cdot223\bmod223^2\), so it has odd valuation at the Gaussian inert prime \(223\). At depth \(1\), take \(t=s+13\). The residual is \(1854=18\cdot103\bmod103^2\). This second failure repeats for every \(k\equiv1\bmod272\), since \(3^{272}\equiv1\bmod(2\cdot17\cdot103)\), and all the compared \(3^k\) are also zero modulo 3. This matches the exponents modulo \(103\cdot102\). These controls exclude the indicated exponent pairs only.

### Population and replay

The new phase splits the old gap into ratios \(91/89\) and \(99/91\). The largest ratio among all eighteen rays is now \(21/19\).

The effective sphere count transfers to the new ray in both classes. The sphere values \(3w^2+2\lambda Z\) are \(2,6\bmod8\), respectively, and both are \(3\bmod9\). Writing a sphere value as \(3Df^2\) with \(D\) squarefree gives
\[
w^2-Df^2=-2\cdot3^E,\qquad
E=262\cdot3^k-1\ \text{or}\ 262\cdot3^k.
\]
Thus the same two-ideal argument bounds the number of retained orientations per discriminant. The shell supports remain disjoint by exact order \(3\), and \(Z=Q^\gamma\) for fixed \(\gamma<1\), so the height trimming still saves a power. The resulting per-height lower bound is \(\gg_\epsilon 2^k\sqrt Q/(\log Q)^{1+\log 2+\epsilon}\) in each class. Across the eighteen rays this gives
\[
A_\lambda(X)\gg_\epsilon
\frac{X^{19/42}}{(\log X)^{1+\log 2-\log_3 2+\epsilon}}.
\]
The exponent is sharp as a lower limiting exponent for these sphere populations by the gap \(38\) to \(42\) and the per-height upper bound \(Q^{1/2+o(1)}\). It concerns generated targets, with no assertion about prescribed integers in the conjecture. [Effective sphere count and collision argument](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The following self-contained replay checks the exact certificates and controls:

```python
from fractions import Fraction as F
from math import gcd

def norm(a,b):
    return a*a+3*b*b

a,b = 1884630968404488393574193593822,13430202510315397746466720933895
c,d = 32819044663843824833457230296681,16157833321322752107598891112924
A,B = 5**91,3**131
assert 8*norm(a,b)==A+B and 2*norm(c,d)==A-B and gcd(91,131)==1
assert A*A>160*B*B
for m,e in ((182,266),(186,270),(190,278),(194,282)):
    assert 3**e<5**m<3**(e+4)
Q,Z,s = A*A,B*B,B
v,w = 8*abs(a*c-3*b*d),8*(a*d+b*c)
for k,(j,p,h) in enumerate(((5,223,37464),(13,103,1854))):
    assert Q==5**(182*3**k) and Z==3**(262*3**k)==s*s
    assert norm(v,w)==4*(Q-Z) and w*w>3*Z and w%3
    for good,t in ((True,abs(w)),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            S,r = x*x+y*y,t+s
            n = 5*Q+lam*Z-S
            assert Q<n<5*Q and S>lam*Z and n%24==(21 if lam==1 else 3)
            assert 2*lam*Z-S==r*r-3*t*t
            R = n-Q-(4-lam)*Z
            if good:
                assert R==v*v+r*r
            else:
                assert R%(p*p)==h and h%p==0 and h>0
    a,b = (Q-Z)//2,(-1)**(k+1)*((Q+Z)//2)
    v,w,Q,Z,s = a*v-3*b*w,a*w+b*v,Q**3,Z**3,s**3

assert pow(3,272,2*17*103)==1
p = list(map(F,"18 178/9 182/9 22 70/3 74/3 26 82/3 30 290/9 34 110/3 38 42 46 142/3 470/9 158/3 54".split()))
assert max(y/x for x,y in zip(p,p[1:]))==F(21,19)
```
