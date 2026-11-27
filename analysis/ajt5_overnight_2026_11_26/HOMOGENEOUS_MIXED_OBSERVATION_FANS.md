# Homogeneous ordinary fans and mixed observations

**Yes, for homogeneous ordinary relays.** If \(p^2\mid n\) at each adjustable relay, one nonzero digit at \(p\) protects **every** zero reader transverse to its forced slope. No parent matching is needed. Nonzero readers need a separate character-count budget, which actual order spacing guarantees for a large-prime sparse fan. In the \(103\to\{619,1031\}\) replay, the zero reader and the nonzero reader exclude different digits, leaving **101 of 103** exact even repairs. [Pinned direction-bundle result](https://github.com/Samsen879/a303656/blob/49c29dfc3410b9faf98abdd5fa2277e532743c07/analysis/ajt5_overnight_2026_11_26/ZERO_READER_DIRECTION_BUNDLE_HALL.md)

### A matching-free mixed-panel criterion

Fix \(n\) and the outside exponent phases. Assume both bases are ordinary at each adjustable relay \(p\), \(p^2\mid n\), and all adjusted cross-reads are at depth one. Use absolute first digits on the line
\[
(c_p,d_p)=(x_p,\mu_p x_p),\qquad
\mu_p=\frac{(3^{p-1}-1)/p}{(5^{p-1}-1)/p}\pmod p.
\]
At a root this is the actual repair line, since the two Teichmüller lifts cancel and \(n/p\equiv0\pmod p\). At a unit relay it can be used as the template. Thus the first digits form a product even if the relays read one another. At each root, choose a second digit to make the valuation exactly \(2\). Those second digits are invisible to the shallow reads.

At a **zero reader** \(r\), an edge \(p\to r\) is transverse if the two \(p\)-primary characters differ on this line. A hit requires their ratio to be one. Consequently \(x_p\ne0\) protects every transverse zero reader of \(p\) simultaneously. Use \(x_p\ne0\) at each adjustable relay, and check that every zero reader with relevant reads has a transverse parent. If every read aligns, the sum on the entire product is a common character times the sum of the two frozen coefficients. It vanishes everywhere precisely when those coefficients cancel. A single-axis read is automatically transverse. For a dual read with \(v_p(r-1)=1\), the test is exact modular arithmetic: writing \(k=(r-1)/p\) and \(\mu_p=u/v\bmod p\), alignment is equivalent to \(3^{vk}\equiv5^{uk}\pmod r\).

Charge each **nonzero reader** to its largest adjustable parent \(p\). At that step all its other read digits are fixed. Its hit count is at most
\[
K(p)=\left\lfloor\frac{1+\sqrt{4p-3}}2\right\rfloor.
\]
With distinct nontrivial characters, this is the ordered-difference bound. Equal characters or only one varying character cost at most one hit. Let \(B_p\) be the sum of those charges at \(p\). If \(B_p<p-1\) for all \(p\), an increasing-prime walk retains at least \(p-1-B_p\) of the \(p\) labels at each step. The joint fraction is at least \(\prod_p(p-1-B_p)/p\). This uses conditional counts, and later choices cannot alter a charged reader. Rows with no adjustable read must pass on the fixed outside phase.

### When arithmetic guarantees the budget

For inert readers \(r\le X\) that read \(p\), their cofactors \((r-1)/p\) are \(2\bmod4\). Thus the entire fan at \(p\) has at most
\[
D_p=\left\lfloor\frac{(X-1)/p+2}{4}\right\rfloor
\]
rows. In particular, \(p\ge X^{2/3}\) guarantees \(D_pK(p)<p-1\) for \(p\ge7\), even if every row is nonzero. Indeed the product is at most \((\sqrt p/4+1/2)(\sqrt p+1/2)\). In this range the reads are automatically shallow, and a row cannot read two such large parents because their product would exceed \(r-1\).

So for these large-prime fans, with the fixed rows passing, **failure of simultaneous unit avoidance on the homogeneous product requires an all-aligned zero reader whose frozen coefficients cancel**. Nonzero readers alone cannot exhaust the budget. This is a condition on actual reads and phases, with no supplied assignment.

### Exact mixed replay

Here the forced slope at \(103\) is \(17\). The actual slopes at \(619\) and \(1031\) are \(69\) and \(74\). The target has zero observation at \(619\) and observation \(614\) at \(1031\). The first excludes \(x=0\), the second excludes \(x=1\), and both exclusions have exact valuation \(1\). All 103 parent repairs have exact valuation \(2\).

```python
from math import isqrt, lcm

p,z,r = 103,619,1031
n = 1635848742953421941
for q in (p,z,r):
    assert q%4==3 and all(q%d for d in range(2,isqrt(q)+1))
    assert all(pow(a,q-1,q*q)!=1 for a in (3,5))

f3,f5 = ((pow(a,p-1,p*p)-1)//p for a in (3,5))
mu = f3*pow(f5,-1,p)%p
def slope(q):
    assert (q-1)%p==0 and (q-1)%(p*p)!=0
    g,h = (pow(a,(q-1)//p,q) for a in (3,5))
    assert g!=1 and h!=1
    return next(m for m in range(1,p) if pow(h,m,q)==g)

assert (mu,slope(z),slope(r))==(17,69,74)
assert r*r<p**3 and (n%(p*p),n%z,n%r)==(0,0,614)

H = lcm(p*p*(p-1),z*(z-1),r*(r-1))
J = (H//(p*p))*pow(H//(p*p),-1,p*p)
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

hits = {z:[], r:[]}
for x in range(p):
    c,d = 63757+J*x,5738130+J*(mu*x%p)
    if rem(c,d,p**3)==0:
        c += p*J
    assert rem(c,d,p**3) in range(p*p,p**3,p*p)
    assert rem(c,d,3)==rem(c,d,4)==1
    for q in hits:
        if rem(c,d,q)==0:
            assert rem(c,d,q*q)==q
            hits[q].append(x)
assert hits=={z:[0],r:[1]}
```

Both readers are ordinary with their own digits frozen. Adding a sufficiently large multiple of \(12p^3z^2r^2\) activates the finite replay with positive remainders. The criterion addresses homogeneous shallow panels. Nonhomogeneous forced lines and aligned zero rows outside this budget still require separate treatment.

The large-prime claim is for inert readers and odd ordinary parents; outside the designated shallow product all fixed rows must already pass. It is a unit-avoidance criterion, not an all-exponent obstruction theorem.
