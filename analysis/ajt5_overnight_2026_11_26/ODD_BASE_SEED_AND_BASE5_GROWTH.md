# One-candidate odd-base norm criterion and a genuine base-5 growth alternative

For an odd integer $b\ge3$ choose $c\in\{b,-b\}$ with $c\equiv1\pmod4$. Let $L_0$ be the product of the distinct primes $p\equiv3\pmod4$ having odd valuation in $c-1$. There exists a positive $L$ with $b^{2L}-1$ a sum of two squares if and only if $L_0$ works. In that case $L_0$ is minimal, and every $2^jL_0$ works.

For a prime $p\equiv3\pmod4$ dividing $c-1$, the lifting-the-exponent formula gives $v_p(c^{2L}-1)=v_p(c-1)+v_p(L)$. Thus every successful $L$ is a multiple of $L_0$, and the obstructing prime of an unsuccessful $L_0$ cannot divide $c-1$. If such a prime $p$ has odd valuation at $L_0$, its order divides $2L_0$, so lifting from $L_0$ to $L$ forces $p\mid L$. Now $(c^p-1)/(c-1)$ is positive and $3\bmod4$, so it contains a prime $q\equiv3\pmod4$ to odd valuation. Since $p\nmid c-1$ and $c^p\equiv c\pmod p$, we have $q\ne p$. No prime other than $p$ dividing $c-1$ can divide this sum, since it is $p$ modulo any such prime. Consequently $q$ has exact order $p$ for $c$, and $q>p$. Since $p\mid L$, lifting at $q$ forces $q\mid L$. Iteration gives an impossible increasing prime chain in the factors of a fixed $L$. Conversely, a good seed remains good under doubling because the additional factor $b^{2L}+1$ is a norm.

For base $5$, $L_0=1$ and the prime $3$ rules it out. For $203$, $c=-203$ and $L_0=3$ is a successful seed. For base $11$, $|c+1|=10$ is itself a norm but $L_0=3$ fails at $7$; the condition on $c+1$ alone is insufficient.

## Direct growth in the original base

Put $x=5m+4$. For every $d\ge0$, an actual representation $m-5^d-1=u^2+v^2$ gives
$$
x-5^{d+1}-9=(2u+v)^2+(u-2v)^2 .
$$
For integers $m\in[X,2X)$ and each $d$ with $5^d+1\le X/2$, the parent residual traverses a length-$X$ interval contained in $[X/2,2X]$. The classical Landau–Ramanujan asymptotic (see [Brink, Moree and Osburn, eq. (1)](https://arxiv.org/abs/1003.1094)) implies that the number of norms in each such interval is $(K+o(1))X/\sqrt{\log X}$ uniformly: apply the asymptotic to both endpoints, which are comparable to $X$. There are $(\log X)/\log5+O(1)$ eligible $d$. Hence the mean number of these positive adjacent columns is $(K/\log5+o(1))\sqrt{\log X}$, and some single $m$ in every sufficiently large interval attains at least this mean. This is an existence bound for a favorable integer at each scale. It does not guarantee any specified first root, bound exceptional integers, or prove A303656.

```python
from math import isqrt
assert 203**6-1==433218**2+8354202**2
assert (11**6-1)%7==0 and (11**6-1)%49!=0
assert (5**2-1)%3==0 and (5**2-1)%9!=0
m=3187
x=5*m+4
for d in range(6):
    r=m-5**d-1
    for u in range(isqrt(r)+1):
        v=isqrt(r-u*u)
        if u*u+v*v==r:
            break
    else:
        raise AssertionError(d)
    assert (2*u+v)**2+(u-2*v)**2==x-5**(d+1)-9
```
