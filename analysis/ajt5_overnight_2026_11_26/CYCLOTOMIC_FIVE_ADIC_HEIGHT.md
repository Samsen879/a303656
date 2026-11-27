# A square-root height lower bound already forced at 5

Use the same cyclotomic actual-anchor chart as CYCLOTOMIC_RATIONAL_ANCHOR_HEIGHT.md, with $V=U^q$, $x=365V$, $r=A/x$, $H=r+x-4$, and $t=n/b$ a reduced rational. Put $N=v_5(V)$ and $L=\max(|n|,b)$. Then any integral $w$ necessarily has
$$
 L\ge\sqrt{V/5}.
$$
This bound is from a single local condition; it is not a sufficient test for a true anchor.

Indeed $v_5(A)=1$, so $v_5(r)=v_5(H)=-N$. If $v_5(t)<0$, the $(rt^2+2)^2$ term has uniquely lowest valuation in the numerator, and if $v_5(t)>0$, $(H/2)^2$ has uniquely lowest valuation. In either case $w$ has negative valuation. Thus $n,b$ are 5-adic units. Set $R=Vr$ and $C=VH$, both 5-adic units with $C\equiv R\bmod V$. Multiplying the defining equation by $V^2b^4$ gives
$$
 wCVb^4=(Rn^2+2Vb^2)^2+(C/2)^2b^4+(A-4)V^2b^4.
$$
Reduction modulo $V$ in the 5-adic integers yields $V\mid4n^4+b^4$. Factor this as $(2n^2+2nb+b^2)(2n^2-2nb+b^2)$. The two factors cannot both be divisible by 5 because their difference is $4nb$. Hence one of these positive quadratic factors is divisible by all of $V$, but either is at most $5L^2$. This proves the claim.

For the first actual pair $k=1,q=5$ there are four simple unit root branches at modulus $V=5^{365}$; the replay checks all four and the unique quadratic-factor assignment. The local lift itself tests no other prime.

```python
v=5
roots=[1,2,3,4]
for _ in range(364):
    w=5*v
    lifts=[[r+v*j for j in range(5) if (4*(r+v*j)**4+1)%w==0]
           for r in roots]
    assert all(len(branch)==1 for branch in lifts)
    roots=[branch[0] for branch in lifts]
    v=w
assert v==5**365 and len(set(roots))==4
for n in roots:
    f=(2*n*n+2*n+1,2*n*n-2*n+1)
    assert sum(a%v==0 for a in f)==1
```
