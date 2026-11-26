# Triangular avoidance across nested shallow relays

A nested relay retains the joint saving, up to a term for the ancestor choices that force a descendant repair. For the actual graph \(7\to43\), with \(3011\) reading both relays, the replay finds **300 safe choices out of 301** at one fixed \(n\). The two descendant root fibres have different repair lines, so this is genuinely nested. [Pinned diamond result](https://github.com/Samsen879/a303656/blob/d41c184bf2075f33864c7cda2fb1c04bdd28d607/analysis/ajt5_overnight_2026_11_26/SPLIT_DIAMOND_JOINT_AVOIDANCE.md)

### A sufficient triangular condition

Let \(p<t<r\), with both axes ordinary at \(p,t\). Freeze the other exponent primaries. Require \(t\) to read \(p\) at depth one, and \(r\) to read both \(p,t\) at depth one. Each read may use one or both axes. Use the affine first-digit repair line at a rooted relay and a fixed diagonal at a unit relay. Each root-line point can be lifted to exact valuation \(2\). The higher digits used in those lifts are invisible to the downstream rows under the depth-one hypothesis.

Write
\[
K(N)=\left\lfloor\frac{1+\sqrt{4N-3}}2\right\rfloor.
\]
For a nonzero observation, the character argument applies whenever the two characters are jointly injective. For a given nonzero difference, the two hit equations either determine both character values uniquely or force their common multiplier to be \(1\). The latter would make the difference zero. Thus there are at most \(K(N)\) hits on a group of size \(N\).

Let \(E\) be the number of ancestor choices for which \(t\) is a root. If \(n\not\equiv0\pmod t\), applying that argument to the ancestor line gives \(E\le K(p)\). On the other \(p-E\) fibres, \(t\) can use the **same** diagonal. Embed these fibres in the hypothetical product of that diagonal with the ancestor line. At a nonzero observation \(n\bmod r\) this entire product has at most \(K(pt)\) hits. On each exceptional fibre, condition on the ancestor and apply the \(K(t)\) bound to the actual descendant repair line. Hence
\[
\#\{\text{hits at }r\}
\le \min\!\bigl(pK(t),\,K(pt)+E K(t)\bigr).
\]
In particular, for a nonzero observation at \(t\), the bad fraction is \(O((pt)^{-1/2})\). For several such downstream rows, sum their bounds on the **same** triangular family. If the sum is below \(pt\), a single choice avoids them all. No independence is used. Any pre-existing robust split avoidance also survives if the split digits stay fixed.

### Zero observations

On an ancestor fibre \(x\), write the descendant line as \((u,m_xu+b_x)\). At \(r\), let \(g,h\) be the two \(t\)-primary generators and \(A_x,B_x\) the coefficients with the \(t\)-digits zero. For \(n\equiv0\pmod r\), the hit equation is
\[
(gh^{-m_x})^u=-B_xh^{b_x}/A_x .
\]
Its exact count is zero if the right side lies outside the image, and \(t/\operatorname{ord}(gh^{-m_x})\) otherwise. Thus a fibre can have zero, one, or \(t\) hits. These counts are conditional on \(x\) and are summed over \(x\).

If \(n\not\equiv0\pmod t\), this gives the stronger bound **\(p+t-1\) hits** at a zero-observation \(r\). Choose a transverse diagonal on the \(t\)-unit fibres, so their quotient has order \(t\). On a rooted fibre, the slope is a fixed nonzero multiple of \(3^c/5^d\bmod t\). For its quotient to be trivial at \(r\), the slope must equal one specified value. The resulting ratio, together with \(3^c+5^d\equiv n\not\equiv0\pmod t\), determines both terms modulo \(t\). They identify at most one ancestor choice. Only that fibre can contribute \(t\) hits.

When the observation at \(t\) is zero, its own root set on the ancestor line is likewise a character coset and can be the whole line. In that case the bound \(E\le K(p)\) does not apply. The conditional kernel formula still applies at \(r\).

### Exact replay

Both bases give the edges \(7\to43,\ 7\to3011,\ 43\to3011\). The descendant root fibres have lines \(v=31u\) and \(v=10u+32\pmod{43}\). The sole downstream hit has exact valuation \(1\); its two relay valuations are both exactly \(2\).

```python
from math import isqrt, lcm

p,t,r = 7,43,3011
n = 1944229405446293
for z in (p,t,r):
    assert z%4==3 and all(z%j for j in range(2,isqrt(z)+1))
    assert all(pow(a,z-1,z*z)!=1 for a in (3,5))
for u,z in ((p,t),(p,r),(t,r)):
    assert (z-1)%u==0 and (z-1)%(u*u)!=0
    assert all(pow(a,(z-1)//u,z)!=1 for a in (3,5))

H = lcm(p*p*(p-1),t*t*(t-1),r*(r-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
U,V,W = map(step,(p*p,t*t,H//(p*p*t*t)))
c0,d0 = H+5*W,4*W
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert n%t==13 and n%r==2059
roots,hits = [],[]
for x in range(p):
    c,d = c0+U*x,d0+U*x
    assert rem(c,d,p*p)==0
    if rem(c,d,p**3)==0:
        c += p*U
    f = rem(c,d,t*t)
    m,b = 1,0
    if f%t==0:
        a3 = pow(3,c,t*t)*((pow(3,V,t*t)-1)//t)
        a5 = pow(5,d,t*t)*((pow(5,V,t*t)-1)//t)
        inv = pow(a5,-1,t)
        m,b = (-a3*inv)%t,(f//t*inv)%t
        roots.append((x,m,b))
    for y in range(t):
        C,D = c+V*y,d+V*((m*y+b)%t)
        if rem(C,D,t**3)==0:
            C += t*V
        f7,f43 = rem(C,D,p**3),rem(C,D,t**3)
        assert f7 and f7%(p*p)==0
        assert f43%t or (f43 and f43%(t*t)==0)
        assert rem(C,D,3)==rem(C,D,4)==1
        if rem(C,D,r)==0:
            assert f43 and f43%(t*t)==0 and rem(C,D,r*r)==r
            hits.append((x,y))
assert roots==[(0,31,0),(1,10,32)] and hits==[(0,0)]
```

A sufficiently large multiple of \(12p^3t^3r^2\) added to \(n\) makes every replayed remainder positive while preserving the tests. The bounds concern this finite triangular phase family. Deeper cross-reads and arbitrary chains of rooted descendants remain outside the proof.

For multiple zero targets, adding bounds is justified only after choosing a common diagonal transverse to all the corresponding unit-fiber character quotients, or by using the exact per-fiber counts along the same predetermined diagonal. The \(p+t-1\) bound above is asserted for a single zero target.
