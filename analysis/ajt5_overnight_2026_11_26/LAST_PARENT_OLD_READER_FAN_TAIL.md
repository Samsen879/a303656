# Last-parent fan budgets for large complement releases

**A checkable fan budget makes the older-reader obstruction summable, even when genuine common Wieferich readers are present.** Under this budget, a nonzero older reader can be avoided at its last adjustable parent. The only remaining failure is a zero reader whose cancellation holds on that parent’s entire repair line. That gives the extra divisor of \(n\) needed for a path count. [Pinned large-factor release result](https://github.com/Samsen879/a303656/blob/9edc3c4f3d9f06c107f8594583c8791cdead8d5f/analysis/ajt5_overnight_2026_11_26/LARGE_COMPLEMENT_SOURCE_RELEASE.md)

### Assign each older exception to its last parent

Let the zero-observation terminal be \(q\), and release a prime \(s>\max(p,t)\) dividing its complement order, with \(s\ge q^\gamma\). In the actual order graph, use the cone reachable from \(s\) by paths with inert vertices after the initial source. Fix the primaries outside this cone, including other split-prime coordinates. Only inert rows need repairs; this convention ensures every counted path endpoint and step lands at an inert row. The two earlier sources remain fixed. For every reachable older common Wieferich reader \(r<q\), assign its unit test to its **largest parent in the cone**. Assign the terminal to \(s\), where a primary mismatch keeps \(q\) a unit regardless of subsequent repairs.

Require the assigned reads to be shallow. At an ordinary relay that can root, require either both axes to be ordinary or, if just one is ordinary, every assigned reader to read the free axis of the repair line. For each parent \(u\), let \(d_u^+\) count its assigned nonzero readers and \(d_u^0\) its assigned zero readers, including \(q\) at \(s\). The sufficient budget is
\[
d_u^+K(u)+d_u^0<u,\qquad
K(u)=\left\lfloor\frac{1+\sqrt{4u-3}}2\right\rfloor .
\]

Process the cone in increasing order. At a rooted ordinary relay, its repair line is fixed by the earlier choices. A nonzero assigned reader costs at most \(K(u)\) first digits by the ordered-difference bound. A zero assigned reader costs at most one digit unless its cancellation is identically true on the line. With two moving axes, that exceptional case requires the repair line to equal the forbidden direction through the absolute origin **and** the remaining coefficients to cancel. Merely matching the slope is insufficient.

At a unit relay, including an older common Wieferich row already made unit by its assigned parent, the digit grid is free. Each assigned test costs at most \(u\) points of the \(u^2\) grid. The same applies to a split source. Choose a second digit at an ordinary root to make valuation \(2\) exact. Shallow assigned tests do not read that digit. All other ordinary descendants can still be repaired when reached.

For \(s\ge q^{2/3}\), the budget and shallowness are automatic. For each \(u\ge s\), the possible inert readers satisfy \(r=ku+1\), \(k\equiv2\pmod4\), and there are at most \(\sqrt u/4+1/2\) of them up to \(q\). Multiplying by \(K(u)\) gives less than \(u\) for \(u\ge7\). The free-axis check for singly ordinary relays still applies.

### Summable exceptional tail

Under these conditions, failure requires one of two events.

- **The terminal is flat at \(s\).** For a doubly ordinary inert source, this is the aligned homogeneous line from the pinned result. Its zero observation gives \(s^2\mid n\), and its nonzero observation puts \(n\bmod s^2\) in the fixed Teichmüller coset. The upper-density tail is \(O_\gamma(Z^{-\gamma})\) over \(q>Z\).
- **An older exception is flat at its assigned parent.** It must be a zero observation, so the same integer satisfies \(qr\mid n\). This gives the path bound below.

For \(X\le q<2X\), fix \(s\ge X^\gamma\). Along a path from \(s\) to \(r\), every step has the form \(u\mapsto ku+1\) with \(k\equiv2\pmod4\). Since \(\sum_{k\equiv2(4)}k^{-4/3}<1\), summing over path lengths and over products of multipliers at most \(2X/s\) gives total endpoint weight \(O(X^{1/3}s^{-4/3})\). The \(1/q\) weight for \(q\equiv1\bmod s\) is \(O(1/s)\). Thus the full \(1/(qr)\) weight in the layer is
\[
O\!\left(X^{1/3}\sum_{s\ge X^\gamma}s^{-7/3}\right)
=O_\gamma\!\left(X^{-(4\gamma-1)/3}\right).
\]
Using \(\lfloor N/(qr)\rfloor\) and summing dyadic layers proves an upper-density tail of
\[
O_\gamma\!\left(Z^{-\gamma}+Z^{-(4\gamma-1)/3}\right),
\qquad \gamma>1/4,
\]
for the stated class. This does not charge any nonzero reader as a divisor of \(n\).

### Exact \(3,5\) control

In the selected graph, split source \(17\) reads into \(443\) and terminal \(50627\). The actual slopes on those two edges are \(4,1\). Thus release \((1,4)\) protects the terminal while permitting a root at \(443\). The forced repair slope at \(443\) aligns with zero reader \(50503\), which has exact valuation \(1\) on **all 443** repairs. Nonzero reader \(887\), with observation \(220\), hits only two repairs. A different release at the same target makes all four rows units. The tested readers are ordinary with their own digits frozen, so this is a control for the local obstruction and its removal.

```python
from math import isqrt, lcm

s,p,z,r,q = 17,443,50503,887,50627
for a in (s,p,z,r,q):
    assert all(a%d for d in range(2,isqrt(a)+1))
assert s%4==1 and all(a%4==3 for a in (p,z,r,q)) and s**4>q
assert all(pow(b,a-1,a*a)!=1 for a in (p,z,r,q) for b in (3,5))

def slope(u,v):
    k=(v-1)//u
    assert (v-1)%u==0 and k%u
    g,h=pow(3,k,v),pow(5,k,v)
    assert g!=1 and h!=1
    return next(i for i in range(1,u) if pow(h,i,v)==g)

assert [slope(u,v) for u,v in ((s,p),(s,q),(p,z),(p,r))]==[4,1,333,66]
assert (z-1)%s and (r-1)%s and (q-1)%p

n=4603770385775350523537022351
c0,d0=119901673309566,306541070442381
H=lcm(p*p*(p-1),z*(z-1),r*(r-1),q-1)
def step(k):
    return (H//k)*pow(H//k,-1,k)
J,E=step(p*p),step(s)
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert (c0%s,d0%s,n%q,n%z,n%r)==(1,4,0,0,220)
hits=[]
for x in range(p):
    c,d=c0+J*x,d0+J*(333*x%p)
    if rem(c,d,p**3)==0:
        c+=p*J
    assert rem(c,d,p**3) in range(p*p,p**3,p*p)
    assert rem(c,d,z*z)==z and rem(c,d,q)
    if rem(c,d,r)==0:
        hits.append((x,rem(c,d,r*r)//r))
assert hits==[(1,1),(185,319)]
assert all(rem(c0+J,d0+13*E,m) for m in (p,z,r,q))
```

The remaining gap is a failed fan budget or a charged read of only the fixed axis at a singly ordinary rooted relay. In those cases, the proof does not rule out a nonzero older exception.

The pointwise construction begins with an old-panel survivor (and a target with zero observation at the terminal). The computed tail concerns only certificates within the stated shallow and free-axis conditions; it does not give a new numerical density bound.
