# A one-prime Fourier interface for unbalanced inert factors

Let $F(p)=p^2+2188$ and let $S$ be any subset of integer inputs in $(X,2X)$ consisting of primes. For a set $I$ of primes $q<X$ each admitting two roots of $F$ modulo $q$, define
$$
D_I=\sum_{q\in I}\left(\#\{p\in S:q\mid F(p)\}-\frac2{q-1}|S|\right).
$$
Writing $\widehat S(\theta)=\sum_{p\in S}e^{2\pi ip\theta}$ gives the exact identity
$$
D_I=\sum_{q\in I}\frac1q\sum_{h=1}^{q-1}\left(\sum_{a^2=-2188\bmod q}e^{-2\pi iha/q}+\frac2{q-1}\right)\widehat S(h/q).
$$
The root count Fourier expansion contributes $2|S|/q$ at frequency zero, not $2|S|/(q-1)$. Since every input is a unit modulo each $q$, $\sum_{h=1}^{q-1}\widehat S(h/q)=-|S|$, which accounts exactly for the correction. This interface uses modulus $q$ rather than $qr$ but requires control of the same set $S$ that survives the other sieve. A theorem about the roots alone would not give the needed mixed cancellation.

Separately, for actual factorization $F(p)=E^2bqr$ write $m_0=E^2bq$. If $a^2+2188\equiv0\bmod m_0$, then on the same parameter $j$,
$$
 p=a+m_0j,\qquad r=m_0j^2+2aj+(a^2+2188)/m_0.
$$
For a good prime $\ell\nmid2\cdot2188m_0$, the two polynomial zeros are disjoint: $p=0$ cannot be a root of $F$. Thus there are exactly $1$ or $3$ distinct forbidden classes for the primality of these two values, according to whether $-2188$ is a nonsquare or square modulo $\ell$. The replay below compares an actual long progression ($m_0=47$ at height $970$) and an actual short one ($m_0=41071$ at height $2710$); both retain the identity. This note gives neither cancellation for $D_I$ nor an analytic upper bound on the unbalanced case.

```python
from math import isqrt
for p,b,q,r,X in ((971,1,47,20107,970),(2711,613,67,179,2710)):
    assert all(v%4==3 and all(v%j for j in range(2,isqrt(v)+1)) for v in (p,q,r))
    m=b*q
    a,j=p%m,p//m
    assert p*p+2188==m*r and q*q>X
    assert r==m*j*j+2*a*j+(a*a+2188)//m
    assert (m<X)==(p==971)
```
