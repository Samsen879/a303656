# A counted family of odd signed targets from simultaneous norms

**There are \(\gg X/(1+\log X)^{15}\) distinct odd targets in each class \(1,3\bmod4\) up to \(X\) for which every finite modulus admits a passing exponent pair with arbitrarily large \(c\).** This holds for every sufficiently large \(X\). The construction uses one power \(5^D\) per scale and makes that power larger than every target it produces.

### Counting simultaneous norms

Set \(P=1\) or \(3\), and write \(B=5^D\). It suffices to construct
\[
S=x^2+y^2,\qquad 2P-S=r^2-3t^2,\qquad S\equiv1\pmod4,\quad S\equiv2\pmod3.
\]
For \(n=B+P-S\), keep \(d=D\) and switch only the parity of the \(3\)-exponent. At inert primes \(p>3\), the residual on the fixed odd-order phase is either \(-S\) or \(2P-S\). The second value occurs only where \(3\) is a nonsquare, so its real quadratic norm expression forces even valuation. At \(3\), the tail residual \(P-S\) is a unit. At \(2\), the parity switch makes the residual \(1\bmod4\). These are the hypotheses of the [verified parity-switch criterion](https://github.com/Samsen879/a303656/commit/113a6db2f798576db459b525e1204d5598ee8d19).

Here is a parametrization with enough integer points to count. Let \(Y=\sqrt B/1000\). For each \(m\in[Y/2,Y]\) coprime to \(6\), put \(s=2m\). For every pair modulo \(m\) with \(F(a,b)=a^2+ab+b^2\equiv P\pmod m\), take its representatives modulo \(6m\) with \(a\equiv3,\ b\equiv0\pmod6\), then add \(12m\) to \(a\). Set
\[
t=\frac{P-F(a,b)}s+a+b-\frac s2,\qquad
(x,y,r)=(t+a,t+b,t+s-a-b).
\]
The quotient is integral, and expanding gives \(x^2+y^2+r^2-3t^2=2P\). The coordinates \(x,y\) have opposite parities. Modulo \(3\), \(a=b=0\) and \(t\equiv(P-2)s\ne0\), so \(S\equiv2\pmod3\). The construction is injective into quadruples because \(s=x+y+r-3t\), \(a=x-t\), and \(b=y-t\).

For \(p^e\mid m\), there are \(p^{e-1}(p-\left(\frac{-3}{p}\right))\) solutions modulo \(p^e\). Modulo \(p\) this is the norm count in the split algebra or quadratic field, and each solution has \(p\) lifts at the next depth because \(p\nmid 6P\). Thus there are at least \(\varphi(m)\) pairs for each \(m\). Möbius inversion gives
\[
\sum_{\substack{m\le Y\\(m,6)=1}}\varphi(m)
=\frac{Y^2}{6}\prod_{p>3}(1-p^{-2})+O(Y\log Y).
\]
Taking the difference at \(Y\) and \(Y/2\) yields \(\gg B\) distinct quadruples for each \(P\).

All coordinates have absolute value at most \(150s\), while \(|x-y|=|a-b|>3s\). Consequently \(S\asymp B\) and \(S<0.18B\). For large \(B\), every target lies in \((B/2,B)\) and satisfies \(n\equiv P\pmod4\).

### From quadruples to distinct targets

Let \(W(S)\) count the constructed quadruples at one \(S\). Then
\[
W(S)\ll \tau(S)\tau(S-2P).
\]
For the real norm, divide \(r,t\) by \(g=\gcd(r,t)\). The primitive pair determines a root of \(z^2\equiv3\pmod{|2P-S|/g^2}\). Two pairs with the same \(g\) and root differ by a unit \(\pm(2+\sqrt3)^k\). There are \(O(1)\) such pairs in the box, since both real embeddings have absolute value \(\asymp\sqrt B\) before division by \(g\). The root count is at most \(2^{\omega(|2P-S|/g^2)}\), whose sum over \(g^2\mid |2P-S|\) is \(\tau(|2P-S|)\). The Gaussian norm has the same argument with roots of \(-1\) and four units.

By Cauchy–Schwarz and \(\tau(j)^4\le d_{16}(j)\),
\[
\sum_S W(S)^2\ll B(1+\log B)^{15}.
\]
Here the bound for the shifted product uses Cauchy–Schwarz on \(\tau(S)^2\tau(S-2P)^2\), and \(\sum_{j\le B}d_{16}(j)\le B(1+\log B)^{15}\) by summing over the first fifteen factors. Applying Cauchy–Schwarz once more to \(\sum_S W(S)\gg B\) proves the distinct-target bound. Taking the largest power \(B\le X\) gives \(B>X/5\), so the result holds at every sufficiently large \(X\).

### Controls and scope

```python
for c, d, x, y, r, t, n in (
    (0, 3,  5, -4,  -3,  -4,  85),
    (1, 4, -8, -5, -28, -17, 539),
):
    S = x*x + y*y
    assert n == 3**c + 5**d - S and 5**d > n
    assert 2*3**c - S == r*r - 3*t*t
    assert S % 4 == 1 and (n - 5**d) % 3 != 0

from math import gcd
def v(n,p):
    e=0
    while n%p==0: n//=p; e+=1
    return e
def prime(p):
    return p>=2 and all(p%q for q in range(2,int(p**.5)+1))
for P in (1,3):
    for m in (5,7,11,25,35,49,55,77):
        choices=[(a,b) for a in range(m) for b in range(m) if (a*a+a*b+b*b-P)%m==0]
        cnt=1
        for p in range(5,m+1):
            if m%p==0 and prime(p):
                e=v(m,p); sign=pow(-3,(p-1)//2,p)
                cnt*=p**(e-1)*(p-(1 if sign==1 else -1))
        assert cnt==len(choices)
        for a0,b0 in choices:
            a=next(a for a in range(6*m) if a%6==3 and a%m==a0)+12*m
            b=next(b for b in range(6*m) if b%6==0 and b%m==b0)
            s=2*m
            t,z=divmod(P-(a*a+a*b+b*b),s)
            assert z==0
            t+=a+b-s//2
            x,y,r=t+a,t+b,t+s-a-b
            S=x*x+y*y
            assert S%4==1 and S%3==2 and 2*P-S==r*r-3*t*t
            assert max(map(abs,(x,y,r,t)))<=150*s and abs(x-y)>3*s
            assert (x+y+r-3*t,x-t,y-t)==(s,a,b)
print("actual controls, primitive fibers and reconstruction passed")
```

The replay also checks composite norm-fiber counts and the integer parametrization.

The bound does not establish positive density. Because \(5^D>n\), every residual in the certified fixed-\(d\) column is negative as an integer. A pointwise representation still needs a pair in the positive-height range \(3^c+5^d\le n\).

For the real norm multiplicity, \(t\) is invertible modulo the absolute primitive norm unless that modulus is 1, in which case the residue test is vacuous. If two primitive pairs have the same root \(r/t\), multiplying one by the conjugate of the other and dividing by their common signed norm gives an element of \(\mathbb Z[\sqrt3]\) of norm 1: both numerator coordinates vanish modulo the absolute norm. The two pairs therefore differ by a unit. Both real embeddings are between constant multiples of \(\sqrt B/g\) in absolute value, so only a fixed number of such units can occur within the same box. The primes 2 and 3 allow at most one root at depth one, and no roots at depth two. This justifies the stated prime-by-prime divisor bound.
