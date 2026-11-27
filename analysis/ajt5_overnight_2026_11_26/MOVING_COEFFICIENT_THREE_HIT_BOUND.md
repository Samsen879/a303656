# Three-hit elimination with moving reader coefficients

**Yes. Three equally spaced hits give a polynomial constraint even when both coefficients move.** A short ratio in the relay’s order-\(h\) subgroup lets the three hit equations cancel the forced exponent. The bound does not require the two coefficient characters to agree. In the actual \(3,5\) replay below they are distinct, and **one of 652 admissible releases** hits the older reader. [Pinned spare-primary result](https://github.com/Samsen879/a303656/blob/6ff6a53c6732c908c401c56b1e534a65b941753b/analysis/ajt5_overnight_2026_11_26/SPARE_PRIMARY_FAST_AXIS_ESCAPE.md)

### A three-hit bound

Let \(h\) be the spare prime and \(p\) the singly ordinary relay. On the common-scaling rooted family with \(v_p(n)=1\), its forced fast digit is \(f(j)=Cw^j\) in \(\mathbb F_p\), where \(w\) has order \(h\). Suppose the older reader \(r\) reads \(h\) shallowly and reads only the fast axis of \(p\), also shallowly. With the other read digits fixed, a hit at the nonzero observation \(N=n\bmod r\) has the form
\[
A\chi(j)G^{f(j)}+B\psi(j)=N\qquad\text{in }\mathbb F_r.
\]
Here \(G\) has order \(p\), and \(\chi,\psi\) are the actual \(h\)-characters on the spare line.

Assume \(\psi\) moves. Choose \(d\ne0\) and positive integers \(a,b\) with \(w^d=a/b\bmod p\). Set \(\alpha=\chi(d),\ \beta=\psi(d),\ z=\psi(j)\). If \(j,j+d,j+2d\) are all hits, the powers \(a,-(a+b),b\) cancel the forced exponents since \(a-(a+b)w^d+b(w^d)^2=0\bmod p\). They also cancel the common first coefficient. The remaining equation is
\[
(N-Bz)^a(N-B\beta^2 z)^b
=\alpha^{\,b-a}(N-B\beta z)^{a+b}.
\]
This polynomial equation has degree at most \(a+b\) and is nontrivial. At \(z=N/B\), the left side is zero and the right side is nonzero. Since \(\psi\) is injective, at most \(a+b\) starting labels give a triple hit. A hit set of size \(L\) contains at least \(3L-2h\) such starting labels, by intersecting its three translates. Hence
\[
\boxed{L\le \left\lfloor\frac{2h+a+b}{3}\right\rfloor.}
\]

A short ratio is guaranteed by the actual orders. Among the first \((p-1)/h+1\) positive integers, two lie in the same coset of \(\langle w\rangle\) in \(\mathbb F_p^\times\). Their ratio is a nonidentity \(w^d\), with \(a+b\le2(p-1)/h+1\). This gives a strict saving when that bound is below \(h\). To preserve other tests, it suffices that the set of already admissible releases is larger than the displayed hit bound. If \(\psi\) is constant, the hit equation instead fixes the \(p\)-primary component of the fast term. Injectivity of \(f\) gives at most one hit.

**Zero observations use a different test.** With absolute fast digits and \(v_p(n)=1\), the nonzero digit \(f(j)\) gives a nontrivial \(p\)-primary ratio at \(r\), so cancellation is impossible regardless of the moving \(h\)-coefficients. If \(p^2\mid n\), that protection can disappear. The earlier square-divisibility tail applies to its stated large-release class. A nonzero observation here does not imply \(r\mid n\).

### Exact \(3,5\) replay

The graph uses spare \(653\), relay \(40487\), older reader \(10250810005031\), and terminal \(10250810133019\). The actual slopes from \(653\) are \(401,315,223\), respectively. Thus the slope-\(401\) release keeps the relay rooted, moves both coefficients at the older reader at different rates, and protects the terminal on every nonzero label.

The ratio \(7/27=w^{263}\bmod40487\) gives \(a+b=34\) and the certified bound \(446<652\). The exact replay finds only label \(1\) hits, with valuation \(1\) at the older reader. All relay valuations are exactly \(2\). Both readers are ordinary controls.

```python
from math import isqrt, lcm

h,p,r,q = 653,40487,10250810005031,10250810133019
for a in (h,p,r,q):
    assert all(a%d for d in range(2,isqrt(a)+1))
assert h%4==1 and all(a%4==3 for a in (p,r,q))
assert pow(3,p-1,p*p)!=1 and pow(5,p-1,p*p)==1
assert all(pow(a,b-1,b*b)!=1 for a in (3,5) for b in (r,q))

def slope(v):
    k = (v-1)//h
    assert (v-1)%h==0 and k%h
    g,j = pow(3,k,v),pow(5,k,v)
    assert g!=1 and j!=1
    return next(i for i in range(1,h) if pow(j,i,v)==g)

assert (slope(p),slope(r),slope(q))==(401,315,223)
k = (r-1)//p
assert (r-1)%p==0 and k%p and (q-1)%p
assert pow(3,k,r)!=1 and pow(5,k,r)==1

H = lcm(p*p*(p-1),r*(r-1),q*(q-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
J,U = step(h),step(p*p)
assert 27*pow(pow(3,-J,p),263,p)%p==7

u = 149107875001118692279947202870596777050426831565979255
v = 126588739942886264306281776509729425317604280156376030
n = 2+u*u+v*v
assert (n%(p*p),n%r,n%q)==(p,8964266852559,0)

def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

hits=[]
for x in range(1,h):
    c,d = H+J*x,((p-1)//2)*p*r*q+J*(401*x%h)
    assert rem(c,d,p*p)==p
    A = pow(3,c,p*p)*((pow(3,U,p*p)-1)//p)%p
    c += U*pow(A,-1,p)
    if rem(c,d,p**3)==0:
        c += p*U
    assert rem(c,d,p**3) in range(p*p,p**3,p*p)
    assert rem(c,d,q) and rem(c,d,3)==rem(c,d,4)==1
    if rem(c,d,r)==0:
        assert rem(c,d,r*r)==r
        hits.append(x)
assert hits==[1]
```

The target has a true square-sum representation at \(c=d=0\). Adding a sufficiently large multiple of \(6p^3r^2q\) to \(u\) activates the replayed exponent pairs while preserving the tests. The bound resolves the stated moving-coefficient family when enough spare labels remain. It gives no general tail for nonzero readers outside that condition.

The polynomial comparison uses only common characteristics at the fixed older reader and the multiplicative recurrence for the separate forced digit modulo the relay. It does not identify their residue fields or treat multiple releases as independent.
