# Unequal subgroup orders and a truncated-box cover bound

For nonzero $n$ in $\mathbb F_p$, consider $A+B=n$ with $AB\ne0$ and partition solutions into pairs of cosets for multiplicative subgroups $H,K$ of sizes $h,k$. The exact total number of unordered pairs within one coset block, summed over all blocks, is
$$
\frac{(h-1)(k-1)-(\gcd(h,k)-1)}{2}.
$$
Indeed the ratio pair $(z,w)\in(H-\{1\})\times(K-\{1\})$ determines its ordered root pair uniquely by $A=n(1-w)/(z-w)$ and $B=n(z-1)/(z-w)$, unless $z=w$, which is impossible for a pair. Conversely every off-diagonal choice gives nonzero coordinates for both roots. Subtract the $\gcd(h,k)-1$ excluded diagonal choices and divide by two. A restricted set of exponent cosets can only decrease this total. For $n=0$, the count of roots in a block equals the cardinality of the intersection of the first coset with the negative of the second, either zero or $\gcd(h,k)$.

For a box $0\le x<X,0\le y<Y$ and coarse steps $U,V$, let the two base orders modulo $p$ be $R,S$. Write $r=\gcd(R,U),s=\gcd(S,V)$ and $h=R/r,k=S/s$. The number of copies of any one root in the subgrid with coarse anchors $(a,b)$ is at most $\lceil X_a/h\rceil\lceil Y_b/k\rceil$, where $X_a$ is the count of indices $a+Ut$ in the box, and $Y_b$ is analogous. Sum these weights over anchors congruent to $i\bmod r$ and $j\bmod s$ to get $W_x(i),W_y(j)$; these anchors read the same cosets. If the block has $m_{ij}$ roots, its weighted contribution is at most $W_x(i)W_y(j)(1_{m_{ij}>0}+\binom{m_{ij}}2)$. The cap follows from $m\le1_{m>0}+\binom m2$. This bounds the finite panel union after summing, with no independence assumption.

The replay uses bases $2,5$ with even exponents, a single $n=2+Q^2$, and $Q$ the product of the eight panel primes. In the entire strict $n/4$ even-exponent box of $646$ cells, the plain row/column bounds sum to $747$, while taking the better weighted bound prime by prime gives $591$. All eight primes hit the origin, so at most $584$ distinct cells are covered; actual coverage is $274$. In particular at least $62$ cells have no panel divisor. At $151$, the fine orders are $5,15$ and the weighted pair term and actual hit count are both $8$. Separately the origin itself is a true norm, even though it is hit by all eight primes at valuation $2$. No claim is made about primes outside the panel.

```python
from math import gcd,prod,comb

P=(7,11,19,23,31,43,47,151)
N=2+prod(P)**2
X,Y=38,17
assert 4*4**(X-1)<N<=4*4**X and 4*25**(Y-1)<N<=4*25**Y
ordinary=weighted=0
covered=set()
for p in P:
    order=lambda u: next(i for i in range(1,p) if pow(u,i,p)==1)
    R,S=order(4),order(25)
    r,s=gcd(R,6),gcd(S,5)
    h,k=R//r,S//s
    ceil=lambda n,d:(n+d-1)//d
    xw=[sum(ceil(len(range(a,X,6)),h) for a in range(i,min(6,X),r)) for i in range(r)]
    yw=[sum(ceil(len(range(b,Y,5)),k) for b in range(j,min(5,Y),s)) for j in range(s)]
    bound=pair_weight=0
    for i in range(r):
        for j in range(s):
            m=sum((pow(4,i+6*u,p)+pow(25,j+5*v,p)-N)%p==0
                for u in range(h) for v in range(k))
            pair_weight+=xw[i]*yw[j]*comb(m,2)
            bound+=xw[i]*yw[j]*((m>0)+comb(m,2))
    on={(x,y) for x in range(X) for y in range(Y)
        if (pow(4,x,p)+pow(25,y,p)-N)%p==0}
    raw=min(X*ceil(Y,S),Y*ceil(X,R))
    assert len(on)<=min(raw,bound)
    ordinary+=raw
    weighted+=min(raw,bound)
    covered|=on
    assert (N-2)%(p*p)==0 and (N-2)%(p**3)!=0
    if p==151:
        assert (R,S,h,k,pair_weight,len(on))==(15,75,5,15,8,8)
assert (ordinary,weighted,len(covered))==(747,591,274)
assert X*Y-(weighted-len(P)+1)==62
```
