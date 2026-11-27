# Growing genuine columns for base 17, and a base-5 obstruction to the same construction

For this comparison only, replace base $5$ by $17$ and let a column $d$ be genuine at $x$ if $x-3^c-17^d$ is a sum of two integer squares for some nonnegative $c$. For $J\ge0$, put $N=1+2^J$, $x=27+17^{2N}$, $m=1+17^{2N-1}$; then $x=17m+10$.

At $x$, the roots $2,18,26$ have respective square coordinates $(17^N,5),(17^N,3),(17^N,1)$, using columns $0,1,1$. The root $2$ is the smallest possible. More importantly, for every $j=0,\ldots,J$, let $i=N-2^j$. The column $2i$ at $x$ and the adjacent column $2i-1$ at $m$ have residuals
$$
x-27-17^{2i}=17^{2i}(17^{2^{j+1}}-1),\qquad
m-1-17^{2i-1}=17^{2i-1}(17^{2^{j+1}}-1).
$$
Both are genuine positive norms. The factorization $a^{2^{j+1}}-1=(a^2-1)\prod_{\ell=1}^j(a^{2^\ell}+1)$ applies with $a=17$, $17^2-1=12^2+12^2$, and $17=1^2+4^2$. Each factor is a norm and products are norms. The pair $2N,2N-1$ has zero residual on both sides. Thus there are at least $J+3$ distinct positive-residual columns, or $J+4$ when zero is allowed. Since $J=\log_2\log x+O(1)$, this genuinely grows with height.

The same difference-power mechanism cannot simply use base $5$. If $5^{2L}-1$ were a sum of two squares for $L\ge1$, the valuation at $3$ would be $1+v_3(L)$ by lifting the exponent, forcing $3\mid L$. Let $p$ be the largest prime $3\bmod4$ dividing $L$. The odd integer $(5^p-1)/4$ is $3\bmod4$, hence has a prime factor $q\equiv3\bmod4$ to odd valuation. This $q$ is not $p$ by Fermat's theorem, and the order of $5$ modulo $q$ is $p$, since $q\nmid4$ and $p$ is prime. Thus $q>p$. Applying the valuation formula at $q$ to $5^{2L}-1$ yields $v_q((5^p-1)/4)+v_q(2L/p)$, odd because $q\nmid L$. This is a contradiction. The obstruction addresses this construction, not every possible growing family for base $5$.

Exact replay of the integer coordinates for several base-17 family members:

```python
def mul(s,t):
    a,b=s
    c,d=t
    return a*c-b*d,a*d+b*c
def norm(s):
    return sum(a*a for a in s)
for J in range(6):
    N=1+2**J
    x=27+17**(2*N)
    m=1+17**(2*N-1)
    assert x==17*m+10
    cols={0,1}
    for c,d,a in [(0,0,5),(0,1,3),(2,1,1)]:
        assert x-3**c-17**d==norm((17**N,a))
    w=(12,12)
    for j in range(J+1):
        i=N-2**j
        if j: w=mul(w,(17**(2**(j-1)),1))
        assert norm(w)==17**(2**(j+1))-1
        cols.add(2*i)
        assert x-27-17**(2*i)==norm(mul((17**i,0),w))
        assert m-1-17**(2*i-1)==norm(mul((17**(i-1),0),mul((1,4),w)))
    cols.add(2*N)
    assert x-27-17**(2*N)==m-1-17**(2*N-1)==0
    assert len(cols)==J+4
```
