# Branching torsion reader charge

**If \(k\) torsion phases survive the unchanged rows, blocking all their repairs needs at least \(k\) distinct higher readers.** Equality requires \(k\) shallow, two-axis, zero-target readers, each vetoing a different whole repair line. This holds at full parent precision and allows a reader’s coefficients to vary across the torsion phases.

### Shared-reader bound

Let \(R>3\) be inert and ordinary to both bases, with precision \(E\ge2\) and \(v_R(n)=1\). Use a tail chart with a common \(R\)-primary exponent phase and an inherited torsion family in \(\mu_p\). Keep only the \(k\) torsion values for which **every row unchanged by the \(R\)-primary variation passes**. This includes lower rows and higher rows that read no \(R\)-digit. On opening both \(R\)-primary axes, the parent has \(k\) distinct parallel first-digit repair lines \(y=mx+b_T\). [Isolated relay baseline](https://github.com/Samsen879/a303656/commit/ce60e055e2d229471e886495bc5543964f97ae14)

Here are the charges for a distinct reader \(\ell\).

| Reader | Upper bound on its charge |
|---|---:|
| One shallow axis | \(k\) first points |
| Both axes shallow, zero target and matching characters along a repair line | \(R\) first points, all on at most one line |
| Both axes shallow, nonmatching characters and nonzero target | \(\displaystyle C(k,R)=\left\lfloor\frac{k+\sqrt{k^2+4k(R-1)}}2\right\rfloor\) first points across the whole family |
| Other shallow cases | \(k\) first points |
| Depth \(D_\ell\ge2\), the larger of its two read depths | At most \(R^{1-D_\ell}\) of the lifts at each first point where it can veto |

For the shared nonmatching bound, let \(k_{\ell,T}\) count the reader’s actual vetoes on line \(T\). A pair at ordered separation \(\delta\ne0\bmod R\) gives two collision equations modulo \(\ell\). Their coefficient rows are \((1,1)\) and \((\alpha^\delta,\beta^{m\delta})\), where \(\alpha,\beta\) are the reader’s order-\(R\) characters. The determinant is nonzero, so the two original power values are uniquely determined. Their \(R\)-primary components recover \(x,y\) because the anchors share their \(R\)-primary exponent phase. The first point then determines its parent line. Thus the same separation cannot occur twice, even across different torsion phases of this reader. Hence
\[
\sum_T k_{\ell,T}(k_{\ell,T}-1)\le R-1,
\]
and Cauchy–Schwarz gives \(C(k,R)\).

At each first repair point, the parent’s exact passing fraction \(\lambda_E\) among the higher lifts is strictly greater than \(1-1/R\). For \(E\ge4\), the fraction with valuation two is \(1-1/R\), and the zero class also passes. For \(E=2,3\), every lift passes. If \(K_\ell\) is a shallow reader’s exact hit count and \(H_\ell\) counts first points where a deeper reader can veto, full coverage therefore requires
\[
kR\lambda_E
\ \le\
\sum_{\ell\ {\rm shallow}}K_\ell+
\sum_{\ell\ {\rm deep}}H_\ell R^{1-D_\ell}.
\]
The same inequality holds on every subfamily. At a point missed by all shallow readers, the deeper weights must sum to at least \(\lambda_E\), so **at least \(R\) deep readers** are needed there.

Since \(k\le p\le(R-1)/2\), the nonmatching cap is strictly below \(R\). With at most \(k\) readers, deeper rows cannot fill any missing point. Covering the \(kR\) first points then requires exactly \(k\) readers attaining the \(R\)-point cap, proving the equality statement. For example, with all 43 phases at \(R=98299\) admissible and no resonant zero-target reader, the necessary count is at least \(\lceil43\cdot98299/2077\rceil=2036\).

In a divisor-minimal tail modulus there is an additional depth requirement. Lowering an essential \(R^E\) by one gives a witness with residual valuation \(E-1\). On either ordinary axis, repairing just that last digit preserves every reader of depth at most \(E-2\). Some reader of depth at least \(E-1\) on that axis must actually veto. Consequently, under the family hypothesis, an essential \(E\ge4\) rules out the \(k\)-reader equality case. [Exact precision closure](https://github.com/Samsen879/a303656/commit/fac27d29f366a0aed19e2ce917577d8084e9166e)

### Real controls and replay

At parent 43, reader 431 gives **four exact vetoes across three** of the seven inherited torsion lines. In the countercontrol at parent 98299, keeping lower row 431 removes exactly one of the 43 inherited phases. Opening 98299 preserves that veto. The charge therefore uses **42** lines on that chart.

```python
from itertools import product
from math import lcm

def r(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

def veto(z,p):
    return z!=0 and z%p==0

# One higher reader has four exact hits across three torsion lines.
n,Q,P,L = 11951677183,431,555990,90510
T = pow(3,P,43**2)
assert T==pow(5,2*P,43**2) and T%43!=1 and pow(T,7,43**2)==1
hits=[]
for t,x in product(range(7),range(43)):
    y=(pow(pow(T,t,43),-1,43)-30*x)*pow(15,-1,43)%43
    c,d=1+P*t+L*x,772+2*P*t+L*y
    assert r(n,c,d,49)==r(n,c,d,43**2)==0
    if veto(r(n,c,d,Q*Q),Q):
        hits.append((t,x,y))
assert hits==[(0,5,13),(0,34,41),(2,22,5),(6,32,32)]

# Keeping lower row 431 prunes the inherited phase t=0.
n,d0,R,H = 48079306635932553700031,33697459974838,98299,431
L=lcm(42,(R-1)*R//43,5*H)
J=lcm(42*43**3,R-1,215*H)
Z=pow(3,L,R*R)
assert Z==pow(5,41*L,R*R) and Z%R!=1 and pow(Z,43,R*R)==1
assert all(pow(a,J,m)==1 for a in (3,5) for m in (49,43**4,H*H))
pruned=[]
for t in range(43):
    c,d=1+L*t,d0+L*(41*t%43)
    for h in (2,3):
        z,step=43**h,43**(h-1)*L
        delta=r(n,c,d,z*43)
        assert delta%z==0
        slope=pow(5,d,43)*((pow(5,step,z*43)-1)//z)
        d+=step*(delta//z*pow(slope,-1,43)%43)
    assert r(n,c,d,49)==r(n,c,d,43**4)==0 and r(n,c,d,R*R)==R
    if veto(r(n,c,d,H*H),H):
        pruned.append(t)
assert pruned==[0]
print("PASS")
```

The reader bound is local to an admissible opened family. Divisor minimality supplies a witness for the depth requirement, but does not by itself supply the full torsion family or make the unchanged rows pass on it. Moving \(c\) also requires the tail \(c\ge v_3(M)\) or a separate small-\(c\) ternary check.

The \(2036\) bound uses normalization by the parent-passing fraction. A shallow reader with \(K_\ell\) hits covers exactly \(K_\ell\lambda_E\) units of the parent-passing set, not \(K_\ell\) units. Dividing by \(\lambda_E\), a deep reader covers at most \(k/\lambda_E\) because \(H_\ell\le kR\) and \(D_\ell\ge2\). On the 43-line chart this is less than \(2077\); every nonresonant shallow reader also covers at most \(2077\) units. The count is conditional on all 43 lines surviving the unchanged rows; the 42-line control illustrates why this qualification is necessary.
