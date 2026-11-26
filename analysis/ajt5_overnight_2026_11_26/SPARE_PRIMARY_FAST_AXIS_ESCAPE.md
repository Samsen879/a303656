# Spare-primary escapes for singly ordinary fast-axis reads

**Yes. A spare primary can move the forced fast digit without disturbing the terminal mismatch.** The useful case is when it multiplies both terms at the rooted relay by the same nontrivial character. The relay then stays rooted, but the forced digit varies injectively unless the target is divisible by the relay prime squared. That remaining square-divisibility obstruction gives an \(O_\gamma(Z^{-2\gamma})\) upper-density tail in the large-release setting. [Pinned last-parent result](https://github.com/Samsen879/a303656/blob/5044c814b4835d9bdba66c7f3d506a8d68799ea8/analysis/ajt5_overnight_2026_11_26/LAST_PARENT_OLD_READER_FAN_TAIL.md)

### Spare-primary criterion

Let \(u\) be singly ordinary, with fast base \(a\) and slow base \(b\). Let an earlier adjustable prime \(h\) supply a first-digit line with parameter \(j\in\mathbb F_h\). Require a shallow read at \(u\) that makes at least one term vary. With the other read primaries fixed, the actual values modulo \(u\) are \(A(j)=A_0\chi(j)\) and \(B(j)=B_0\psi(j)\). Work with a set \(S\) of \(h\)-labels that preserves the existing terminal mismatch and the tests already guarded. The mismatch can be on a distinct frozen primary, or on \(h\) itself with only mismatch-preserving labels retained.

For the charged readers that see only the fast axis at \(u\), form a forbidden digit set \(F\subset\mathbb F_u\). A zero reader can be protected by excluding digit \(0\), even if it reads \(h\). For a **nonzero** reader, require its remaining coefficients to stay fixed modulo that reader. Then its nontrivial \(u\)-character excludes at most one fixed digit. This coefficient condition can be checked on the actual read graph by keeping its other read primaries frozen. In particular, the reader must be blind to the varied \(h\)-digits and to any other repairs that would change its coefficients.

The following cases give a sufficient test.

- If \(n\not\equiv0\pmod u\), at most \(K(h)=\lfloor(1+\sqrt{4h-3})/2\rfloor\) labels root \(u\), by the ordered-difference bound. If \(|S|>K(h)\), choose \(u\) unit, then choose its free fast digit outside \(F\), provided \(|F|<u\).
- If \(n\equiv0\pmod u\) and \(A+B\) is not identically zero, at most one label roots \(u\). The same unit choice works when \(|S|>1\).
- If \(A+B\equiv0\) throughout the line, the two characters coincide and are nontrivial. On the rooted repair, the absolute fast digit is
  \[
  x(j)=\frac{(u-1)(n/u)}{f_u(a)A(j)}\pmod u .
  \]
  The Teichmüller terms cancel because \(B=-A\), and the slow base has zero Fermat quotient. If \(u^2\nmid n\), the displayed map is injective. Thus \(|S|>|F|\) suffices, followed by the second-digit adjustment to exact valuation \(2\). If \(u^2\mid n\), the digit stays zero for every release. This is the arithmetic obstruction in this case when \(0\in F\).

The criterion applies inside the inert-only repair cone. Subsequent ordinary repairs can proceed in order as long as the designated coefficients stay fixed and the previously guarded tests retain their protection. Genuine exceptional rows outside this local assignment still need their own guards. In particular, the argument gives no fixed forbidden digit for a nonzero reader whose coefficient changes with \(h\).

### Summable square-divisibility tail

Suppose the initial released prime \(s\mid q-1\) satisfies \(s\ge q^\gamma\), with \(\gamma>0\), and \(u\) is reachable from \(s\) along paths with inert vertices after the source. Allow \(u=s\). In the remaining arithmetic obstruction, the same integer satisfies \(qu^2\mid n\). No divisibility by a nonzero older reader is used.

Each path step has the form \(w\mapsto kw+1\), \(k\equiv2\pmod4\). Summing over all path lengths, with repeated endpoints allowed, gives
\[
\sum_{u\ \mathrm{reachable}} u^{-2}
\le s^{-2}\sum_{j\ge0}
  \left(\sum_{k\equiv2\ (4)} k^{-2}\right)^j
\ll s^{-2}.
\]
On \(X\le q<2X\), the \(1/q\) weight for \(q\equiv1\pmod s\) is \(O(1/s)\). The total density contribution, using \(\lfloor N/(qu^2)\rfloor\), is therefore \(O(\sum_{s\ge X^\gamma}s^{-3})=O_\gamma(X^{-2\gamma})\). Summing the dyadic layers proves the tail.

### Same-target replay

Here split source \(653\) has actual slopes \(401\) at singly ordinary relay \(40487\) and \(442\) at terminal \(20249604443\). Along slope \(401\), all 652 nonzero releases keep the terminal mismatch and keep \(40487\) rooted. Its forced fast digit takes 652 distinct values. Older reader \(20249573051\) sees only that fast axis and has nonzero observation \(19494101598\). Exactly one release gives it valuation \(1\), and all the others give a unit. The older reader and terminal are ordinary controls.

```python
from math import isqrt, lcm

h,p,r,q = 653,40487,20249573051,20249604443
for a in (h,p,r,q):
    assert all(a%d for d in range(2,isqrt(a)+1))
assert h%4==1 and all(a%4==3 for a in (p,r,q)) and h**4>q
assert pow(3,p-1,p*p)!=1 and pow(5,p-1,p*p)==1
assert all(pow(a,b-1,b*b)!=1 for a in (3,5) for b in (r,q))

def slope(v):
    k=(v-1)//h
    assert (v-1)%h==0 and k%h
    g,j=pow(3,k,v),pow(5,k,v)
    assert g!=1 and j!=1
    return next(i for i in range(1,h) if pow(j,i,v)==g)

assert (slope(p),slope(q))==(401,442)
assert (r-1)%h and (q-1)%p and (r-1)%p==0 and ((r-1)//p)%p
assert pow(3,(r-1)//p,r)!=1 and pow(5,(r-1)//p,r)==1

H=lcm(p*p*(p-1),r*(r-1),q*(q-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
J,U=step(h),step(p*p)
u=2915711843946576141303302104147912343124555199
v=3078549161199172022486922909358713143490715344
n=2+u*u+v*v
assert (n%(p*p),n%q,n%r)==(p,0,19494101598)

def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

digits,hits=set(),[]
for x in range(1,h):
    c,d=H+J*x,((p-1)//2)*p*r*q+J*(401*x%h)
    assert rem(c,d,p*p)==p
    A=pow(3,c,p*p)*((pow(3,U,p*p)-1)//p)%p
    f=pow(A,-1,p)
    digits.add(f)
    c+=U*f
    if rem(c,d,p**3)==0:
        c+=p*U
    assert rem(c,d,p**3) in range(p*p,p**3,p*p)
    assert rem(c,d,q) and rem(c,d,3)==rem(c,d,4)==1
    if rem(c,d,r)==0:
        assert rem(c,d,r*r)==r
        hits.append(x)
assert len(digits)==652 and hits==[1]
```

The target also has the displayed true square-sum representation at \(c=d=0\). Increasing \(u\) in that representation by a sufficiently large multiple of the replay moduli activates every checked exponent pair. The remaining cases are panels with too few admissible spare labels or with a nonzero reader whose other coefficients move along with the spare primary.

The restricted tail charges only the actual obstruction \(qu^2\mid n\) after the spare-label and coefficient conditions have been verified. It does not bound failures of those auxiliary conditions. The injective map concerns the absolute fast digit on the shallow repair, so replacing higher local digits for the even lift cannot change a guarded reader.
