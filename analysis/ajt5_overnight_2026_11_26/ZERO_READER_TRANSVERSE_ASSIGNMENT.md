# Assign zero-observation readers to transverse parent lines

**Yes, under a checkable assignment of readers to relays.** A zero reader needs only one parent whose primary components disagree. The forbidden directions at that parent depend on the actual orders of \(3,5\) and can be computed before fixing the downstream coefficients. The resulting conditional budgets multiply along the DAG.

In the actual graph \(7\to43\), with \(2867327\) reading both relays, **252 of 301 choices avoid both downstream zero observations**. Both rooted relay slopes align with the terminal. The successful choices use \(7\) to make \(43\) a unit, which frees \(43\) to use a transverse template. [Pinned triangular result](https://github.com/Samsen879/a303656/blob/9f2a7f96a3203534da04365d588c7cfa091b90ca/analysis/ajt5_overnight_2026_11_26/NESTED_TRIANGULAR_RELAY_AVOIDANCE.md)

### A coefficient-free criterion

Use absolute first digits \(x=c\bmod p,\ y=d\bmod p\) at an ordinary relay \(p\). For a depth-one edge \(p\to r\), let \(g,h\) be the \(p\)-primary components of \(3,5\bmod r\). At a zero observation \(n\equiv0\pmod r\), a hit requires
\[
g^x=h^y.
\]
Indeed, the ratio of the two terms must be \(-1\), whose odd-primary components are trivial. The forbidden set at \(p\) is therefore a line through the origin. It is \(y=mx\) when both axes are read, and a coordinate axis when only one is read. A point outside this line protects \(r\) regardless of the other coefficients.

Assign each zero row required to be a unit to one earlier adjustable parent. This set of rows may include relays that must stay on their unit templates. At each \(p\), collect the **distinct** forbidden lines for the rows assigned to it in \(\mathcal L_p\). Choose a unit template through the origin with nonzero finite slope outside their directions; the criterion requires such a slope to be available. For nonempty \(\mathcal L_p\), the exact local counts are

| Actual line at \(p\) | Choices protecting all rows assigned to \(p\) |
|---|---:|
| Transverse unit template | \(p-1\) |
| Homogeneous repair line of slope \(\mu\) | \(0\) if its direction is in \(\mathcal L_p\), otherwise \(p-1\) |
| Nonhomogeneous repair line of slope \(\mu\) | \(p-|\mathcal L_p|+\mathbf1_{\{\text{direction }\mu\in\mathcal L_p\}}\) |

For the nonhomogeneous line, each nonparallel forbidden line costs one point, and those points are distinct. An empty assigned set costs nothing.

At a rooted, doubly ordinary zero-observation relay, the repair slope is
\[
\mu_p=\frac{(3^{p-1}-1)/p}{(5^{p-1}-1)/p}\pmod p.
\]
The intercept is zero exactly when \(p^2\mid n\). The two terms are opposite modulo \(p\), their Teichmüller lifts cancel, and the affine repair equation has right-hand side \(n/p\bmod p\). Thus an aligned homogeneous repair is an unavoidable ratio kernel **on that edge and fibre**. A nonhomogeneous deviation instead has the finite intersection cost in the table.

Walk in topological order. A relay already protected by an earlier parent is a unit and uses its transverse template. Every other relay must have a positive count on each possible repair line. If \(k_p\) is the minimum count that can arise at \(p\), the joint retained fraction in the sequential line family is at least \(\prod_p k_p/p\). This multiplies conditional lower bounds. The second digits used to realize exact valuation \(2\) preserve every shallow protection.

### Exact witness and boundary

The actual slopes on \(7\to43,\ 7\to2867327,\ 43\to2867327\) are \(2,1,41\). The rooted slopes at \(7,43\) are \(1,41\). Assign \(43\) to \(7\) and the terminal to \(43\), using template slope \(1\) at both relays. The six nonzero digits at \(7\) protect \(43\). On each of those fibres, the 42 nonzero template digits at \(43\) protect the terminal. On the remaining ancestor fibre, \(43\) is rooted and all 43 terminal choices have valuation \(1\). The certified fraction \((6/7)(42/43)\) is exact.

There is no general guarantee that one template with both axes moving is transverse to **every** outgoing edge. The actual \(7\)-edges to \(379,43,2003,547,127,211\) realize all six nonzero forbidden slopes. This concerns template feasibility. It leaves open whether other parents can protect those rows.

```python
from math import isqrt, lcm

p,t,r = 7,43,2867327
n = 2200863781493824589919

def slope(u,v):
    assert (v-1)%u==0 and (v-1)%(u*u)!=0
    g,h = (pow(a,(v-1)//u,v) for a in (3,5))
    assert g!=1 and h!=1
    return next(m for m in range(1,u) if pow(h,m,v)==g)

assert [slope(u,v) for u,v in ((p,t),(p,r),(t,r))]==[2,1,41]
fan = (379,43,2003,547,127,211)
assert [slope(7,v) for v in fan]==list(range(1,7))
for z in {p,t,r,*fan}:
    assert z%4==3 and all(z%d for d in range(2,isqrt(z)+1))
    assert all(pow(a,z-1,z*z)!=1 for a in (3,5))

H = lcm(p*p*(p-1),t*t*(t-1),r*(r-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
U,V = step(p*p),step(t*t)
c0,d0 = 228*p*t*r,357*p*t*r
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert (n%(p*p),n%(t*t),n%(r*r))==(0,0,r)
bad = []
for x in range(p):
    for y in range(t):
        c = c0+U*x+V*y
        d = d0+U*x+V*((41 if x==0 else 1)*y%t)
        if rem(c,d,p**3)==0:
            c += p*U
        if rem(c,d,t**3)==0:
            c += t*V
        assert rem(c,d,p**3) in range(p*p,p**3,p*p)
        f = rem(c,d,t**3)
        assert (x==0 and f in range(t*t,t**3,t*t)) or (x!=0 and f%t)
        assert rem(c,d,3)==rem(c,d,4)==1
        if rem(c,d,r)==0:
            assert rem(c,d,r*r)==r
            bad.append((x,y))

assert bad==[(x,y) for x in range(p) for y in range(t) if x==0 or y==0]
assert p*t-len(bad)==252
```

The terminal is ordinary with its own digit frozen in this replay. Adding a sufficiently large multiple of \(12p^3t^3r^2\) to the target makes all replayed remainders positive while preserving the tests. The criterion resolves panels admitting the stated parent assignment. General panels with unavoidable aligned parents or exhausted template directions remain open.
