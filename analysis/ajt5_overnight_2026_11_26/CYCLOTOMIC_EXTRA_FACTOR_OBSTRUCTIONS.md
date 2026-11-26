# Two exact local obstructions for a cyclotomic slope family

In the plus-sign square-difference chart, fix $d=8+6n$, $X=5^d$, $U=X/5$, $A=X-131770$ and set $x=365U^q$. Take either $r=x$ or $r=A/x$, so $H=x+A/x-4$. This note concerns only this explicit slope family.

As $U\equiv5\bmod9$ and $A\equiv6\bmod9$, for $q=0,1,\ldots,5\bmod6$ the values of $H\bmod9$ are, respectively, $4,0,7,6,1,3$. The positive target congruence $w\equiv26\bmod30$ requires $v_3(H)=1$ by PLUS_QUARTIC_MOD3_RESTRICTION.md. Thus only $q\equiv3,5\bmod6$ can remain. In particular, the explicit $q=1$ three-term profile
$$
 H=\frac{(X-5)(5329X+26354)}{73X}
$$
fails at every such label. This does not classify three-term profiles outside the given slope family.

Furthermore, on $d=1+73^k$ with $k\equiv15\bmod52$, the iteration $U\mapsto U^{73}$ modulo $107$ gives $U=31$, $A=102$. The exact computation below gives $107\mid H$ for $q\equiv5,99\bmod106$. Both slopes are units modulo 107. If $w$ is integral, $t$ cannot have a pole at 107, because the $r^2t^4$ term would then dominate the numerator. Modulo 107 the numerator at $H=0$ factors as $(rt^2+r)(rt^2+A/r)$. Hence a root requires $t^2=-1$ or $t^2=-A/r^2$; neither is a square since $107\equiv3\bmod4$ and $-A\equiv5$ is a nonsquare. In particular this excludes $q=5$ on an infinite progression of labels, but not varying $q$ or all other progressions.

```python
p=107
cycle=[5]
for _ in range(51):
    cycle.append(pow(cycle[-1],73,p))
assert len(set(cycle))==52 and pow(cycle[-1],73,p)==cycle[0]
U=cycle[15]
A=(5*U-131770)%p
assert (U,A)==(31,102) and pow(-A,53,p)==p-1
hits=[]
for q in range(106):
    x=365*pow(U,q,p)%p
    if (x*x-4*x+A)%p==0:
        hits.append(q)
assert hits==[5,99]
assert [(x+6*pow(x,-1,9)-4)%9 for x in
        (pow(5,q+1,9) for q in range(6))]==[4,0,7,6,1,3]
```
