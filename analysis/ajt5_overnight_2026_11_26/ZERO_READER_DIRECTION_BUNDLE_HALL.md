# Direction bundles for shallow zero-reader Hall certificates

**Yes. A capacitated Hall test works if rows that share a direction can be assigned as one bundle.** The bundle version is exact for the coefficient-free ray assignment once the set of relays to keep unit is fixed and the bundle partition may be chosen. In the actual \(3,5\) panel below, seven readers share one direction at relay \(7\). Per-reader Hall fails, bundle Hall succeeds, and the exact replay retains **114 of 133** choices. Relay \(19\) is forced onto a homogeneous line aligned with \(31123\), so relay \(7\) supplies the bypass. [Pinned transverse-assignment result](https://github.com/Samsen879/a303656/blob/de4b15a09ba6625112e3a522ed41a95d3c97c75f/analysis/ajt5_overnight_2026_11_26/ZERO_READER_TRANSVERSE_ASSIGNMENT.md)

### Direction-capacity Hall criterion

Fix the target \(n\), the outside phases, and a set \(U\) of zero-observation rows required to be units. Include in \(U\) any adjustable relays whose outgoing assignments rely on their staying unit. The adjustable relays are doubly ordinary; those not already certified unit are assumed to have zero observation. All adjusted cross-reads have depth one.

Let \(\ell_{pr}\) be the forbidden direction at parent \(p\) for reader \(r\), obtained from \(g^x=h^y\) in absolute first digits. It is a line through the origin, including a coordinate axis when only one axis is read. A nonzero point on any other ray protects \(r\) regardless of the downstream coefficients.

For a zero-observation relay \(p\), use the following menu \(A_p\) of directions. One may restrict the menu to nonzero finite slopes if both coordinates must move on the template.

| Status of \(p\) | Directions available uniformly |
|---|---|
| Certified unit, including a relay in \(U\) once guarded | All menu directions |
| May root and \(p^2\mid n\) | Only the homogeneous repair direction \(\mu_p\) |
| May root and \(v_p(n)=1\) | Every menu direction except \(\mu_p\) |

Here \(\mu_p\) is the ratio of the two Fermat quotients. In the last case every rooted line is parallel to \(\mu_p\) and misses the origin, so it meets each listed direction in exactly one nonzero point. In the homogeneous case the repair line is itself the only available ray.

Remove any row with an edge \(\ell_{pr}\notin A_p\), since that parent protects it for every allowed choice. For the remaining rows, use capacity
\[
c_p=|A_p|-1.
\]
Partition the rows into bundles. A bundle is eligible for \(p\) if every row in it reads \(p\) and all those edges have the same forbidden direction there. For every subfamily \(\mathcal C\) of bundles, require
\[
|\mathcal C|\ \le\ \sum_{p\in N(\mathcal C)}c_p .
\]
This is an ordinary capacitated matching test on bundles and parents. A matching uses at most \(c_p\) distinct directions at \(p\), so one allowed ray remains for its template. Proceed in topological order. A relay in \(U\) is protected by its earlier assigned parent before it needs to use its enlarged menu. The second digits used for exact even repair preserve all shallow protections.

Singleton bundles give the conventional per-reader Hall test. Allowing a choice of partition makes the bundle condition lossless **within the stated ray menus**. Given successful ray choices, pick one guarding parent for each remaining row and group by parent and forbidden direction. Those bundles already have a capacity-respecting matching. A failed Hall test for a particular partition therefore establishes only that the partition is inadequate.

The same certificate gives a positive conditional budget. If \(b_p\) distinct assigned directions lie in \(A_p\), a nonhomogeneous root has at least \(|A_p|-b_p\) distinct protecting points. A transverse unit or homogeneous line has \(p-1\) nonzero protecting points. Taking the appropriate minimum at each relay and multiplying the conditional fractions gives a joint lower bound without assuming independence.

### One fixed-target replay

Take parents \(7,19\) and readers
\[
2003,\ 2143,\ 4271,\ 4327,\ 4663,\ 5867,\ 31123.
\]
All seven edges from \(7\) have forbidden slope \(3\). Only \(31123\) reads \(19\), with slope \(11\). The target has \(v_7(n)=1\) and \(19^2\mid n\). The \(19\)-repair forces slope \(11\), so it cannot guard \(31123\). The \(7\)-repair is \(d_7=c_7+2\), and its menu has seven projective directions, giving capacity six. Seven singleton bundles fail Hall. One shared-direction bundle passes.

In the replay, \(c_7=1\) yields exact valuation \(1\) at \(31123\) for every even repair at \(19\). Every other first digit at \(7\) makes all seven readers units. Both relay valuations are exactly \(2\) throughout.

```python
from math import isqrt, lcm

p,t = 7,19
R = (2003,2143,4271,4327,4663,5867,31123)
r = R[-1]
n = 8130007602535266267379815318856843001

for z in (p,t,*R):
    assert z%4==3 and all(z%d for d in range(2,isqrt(z)+1))
    assert all(pow(a,z-1,z*z)!=1 for a in (3,5))

def slope(u,z):
    assert (z-1)%u==0 and (z-1)%(u*u)!=0
    g,h = (pow(a,(z-1)//u,z) for a in (3,5))
    assert g!=1 and h!=1
    return next(m for m in range(1,u) if pow(h,m,z)==g)

assert [slope(p,z) for z in R]==[3]*7 and slope(t,r)==11
assert (t-1)%p and all((z-1)%t for z in R[:-1])
assert [n%(z*z) for z in (p,t,r)]==[14,0,r]
assert all(n%z==0 for z in R)

H = lcm(p*p*(p-1),t*t*(t-1),r*(r-1),*(z-1 for z in R))
def step(k):
    return (H//k)*pow(H//k,-1,k)
U,V = step(p*p),step(t*t)
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

good = 0
for x in range(p):
    for y in range(t):
        c = 37254231+U*x+V*y
        d = 819593082+U*((x+2)%p)+V*(11*y%t)
        for z,j in ((p,U),(t,V)):
            if rem(c,d,z**3)==0:
                c += z*j
            assert rem(c,d,z**3) in range(z*z,z**3,z*z)
        assert rem(c,d,3)==rem(c,d,4)==1
        if x==1:
            assert rem(c,d,r*r)==r
        else:
            assert all(rem(c,d,z) for z in R)
            good += 1
assert good==114
```

This is a finite phase certificate. Adding a sufficiently large multiple of the test moduli to \(n\) makes the replayed remainders positive while preserving every test. The readers here are ordinary, with their own digits frozen for the unit tests. The result gives a transferable sufficient condition for shallow zero panels, without asserting that every actual order graph admits the required bundles or unit set.
