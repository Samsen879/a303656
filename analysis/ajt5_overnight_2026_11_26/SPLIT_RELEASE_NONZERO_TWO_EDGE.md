# Split-source release with a nonzero old observation

**One robustly safe split release does not force a saving.** With the actual bases \(3,5\), a singly ordinary relay can force the only digit the older reader sees. I found a two-edge example where every even relay repair in one fixed release gives the same nonzero observation and exact valuation \(1\) at the older reader. **With all split digits available, the isolated two-edge obstruction can be excluded**, including for a genuinely common Wieferich reader. This is the distinction left open by the zero-observation argument. [Pinned split-release note](https://github.com/Samsen879/a303656/blob/2e6df166d7714be5b79c33b9464163e47b5b0923/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_SPLIT_RELEASE_TAIL.md)

### All release digits versus one fixed release

Consider \(s\to p\to r\), with \(s\to q\) and \(n\equiv0\pmod q\). Freeze the other primary coordinates. Write \(d_u(v)=\max_{a=3,5}v_u(\operatorname{ord}_v a)\), and put \(a=d_s(q), b=d_s(p), h=d_p(r)\). Each is positive. Sample the two split coordinates on a grid deep enough for every row being tested.

A fraction \(1-s^{-a}\) of split pairs make the \(s\)-primary components at \(q\) unequal. This keeps \(q\) a unit regardless of subsequent relay changes. At most an \(s^{-b}\) fraction of the full split grid makes \(n-3^c-5^d\equiv0\pmod p\). To see this, fix the other axis and vary an axis on which the order has \(s\)-depth \(b\). A hit occupies at most one class modulo \(s^b\).

Suppose the older tests leave a subset of robustly safe split pairs of relative size \(\delta\) in the full grid, and the remaining relay coordinates can be chosen freely subject to the \(p\)-repair. For each pair making \(p\) a unit, no relay repair is needed. The same one-axis count at \(r\) then gives a forbidden fraction at most \(p^{-h}\), for **any** observation \(n\bmod r\). Thus choosing uniformly from the retained split pairs and then the available relay repairs gives an odd-valuation fraction at \(r\) of at most
\[
p^{-h}+(1-p^{-h})\min\!\left(1,\frac{s^{-b}}{\delta}\right).
\]
This also bounds the fraction that hits the first modulus at \(r\). It applies if \(r\) reads \(s\) directly as well, since the split pair is fixed when counting the relay digits.

In particular, \(\delta>s^{-b}\) suffices to find a split pair making \(p\) a unit, then a relay choice making \(r\) a unit. The isolated two-edge case has \(\delta=1-s^{-a}>s^{-b}\). This proves an escape while keeping \(q\) avoided, without using the lift at \(r\) or requiring \(r\mid n\).

For **one fixed split pair** on which \(p\) is a root, there is still a useful restricted bound. If both axes at \(p\) are ordinary and \(r\) reads only the first \(p\)-digit, the repairs form a line of \(p\) points. At \(r\) the sum on that line has the form \(C g^x+D j^x\). For a nonzero observation, distinct nontrivial characters give at most
\[
\left\lfloor\frac{1+\sqrt{4p-3}}2\right\rfloor
\]
hits. For each nonzero difference \(t\), the two hit equations at \(x,x+t\) uniquely determine \(Cg^x,Dj^x\), so at most one ordered pair of hits has difference \(t\). Equal characters or a single varying character give at most one hit, with the identically zero sum giving none. If \(r\) reads depth two, the second relay digits admissible for exact \(v_p=2\) omit one affine line, giving a hit fraction at most \(1/(p-1)\). At depth \(h\ge3\), the digits above the second are free and give \(p^{-(h-2)}\). The exceptional shallow case is a singly ordinary relay whose reader sees only the axis fixed by the repair.

### Actual \(3,5\) countercontrol

Take \((s,p,r,q)=(653,40487,20249573051,20249604443)\) and the same integer \(n\) throughout the replay. At the fixed release \(c=A+Bx,\ d=By\), \(q\) stays a unit for all \(x,y\). At \(p\), the \(5\)-axis is Wieferich and the \(3\)-axis is ordinary. Every even repair requires \(x\equiv0\pmod p\), and the baseline has exact \(v_p=2\). For every such repair the sum is \(2\bmod r^2\), while \(n\equiv2+r\bmod r^2\). Hence the forbidden fraction at the **nonzero** observation \(2\bmod r\) is exactly one. Changing the split release gives units at \(p,r,q\) simultaneously.

The reader \(r\) is ordinary and its own primary coordinate is frozen in this control. Releasing that coordinate allows an ordinary repair. The example tests the fixed-release inference with actual bases and exact odd and even lifts, without supplying a genuine common Wieferich reader.

```python
from math import isqrt, lcm

s,p,r,q = 653,40487,20249573051,20249604443
assert all(all(v % j for j in range(2,isqrt(v)+1)) for v in (s,p,r,q))
assert (r-1)%s and (q-1)%p
T = lcm(p-1,r-1,q-1)//(s*p)*r*q
A,B = T*p*p,T*s
n = 905821115546362579749734918238479885136652235
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert rem(A,0,p**3)==p*p and rem(A,0,r*r)==r
assert pow(3,A,p)!=1 and pow(3,A,q)!=1
assert B%p and pow(3,B,p)==1
assert pow(3,B,p*p)!=1 and pow(5,B,p*p)==1
assert pow(3,B,r)!=1
assert pow(3,B*p,r*r)==pow(5,B,r*r)==1
assert n%q==0 and rem(A,0,q)!=0
assert all(pow(a,B,q)==1 for a in (3,5))
assert all(rem(2*A+B,0,m)!=0 for m in (p,r,q))
assert pow(3,r-1,r*r)!=1
```

Adding a sufficiently large multiple of \(p^3r^2q\) to \(n\) activates the displayed exponent pairs with positive remainders and preserves the replay.

There is also a checkable **full old panel** condition. If
\[
\sum_{\substack{v\ \mathrm{reads}\ s\\ v\ \mathrm{an\ old\ row\ or}\ q}}
          s^{-d_s(v)}<1,
\]
one split pair makes every direct reader a unit. All relay digits can then stay fixed, so indirect rows retain their old values. This removes the old zero-observation assumption for that class. For a general crowded panel, a single robust release gives no lower bound on the retained split mass \(\delta\). The nonzero-observation tail outside these conditions remains open.
