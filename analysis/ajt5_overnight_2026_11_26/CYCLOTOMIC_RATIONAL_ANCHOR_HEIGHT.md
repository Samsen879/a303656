# A height obstruction for actual rational anchors in the cyclotomic slope family

Use the plus-sign chart with $U=5^{73^k}$, $A=5U-131770$, $x=365U^q$ for positive $q\equiv5\bmod6$, $F=x^2-4x+A$, $r=A/x$, and $H=F/x$. The rational anchor equation is
$$
 w=\frac{(rt^2+2)^2+(H/2)^2+A-4}{H}.
$$
For a reduced rational $t=n/b$, $b>0$, set $L=\max(|n|,b)$ and $M=F/(4\gcd(F,A))$. The latter is an integer because $A$ is odd and $4\mid F$. If $w$ is integral, then
$$
 M\mid (n^2+b^2)\big(An^2+(4x-A)b^2\big).
$$
Indeed multiplying the anchor equation by $Fxb^4$ gives $(An^2+2xb^2)^2+F^2b^4/4+(A-4)x^2b^4$. Reducing this numerator modulo $F$, using $x^2\equiv4x-A\bmod F$, gives $A$ times the displayed product. Cancel the common divisor with $A$ to obtain the necessary divisibility.

In the stated parameter range $A>0$, $4x>A$ and $F>x^2/2$. The product is positive and at most $8xL^4$. As $M>x^2/(8A)$, it follows that
$$
 L^4>\frac{x}{64A}>\frac{365}{320}U^{q-1}.
$$
Thus a genuine rational anchor of height $O(U^C)$ for a fixed $C$ covers only bounded $q$. This does not give a matching upper bound or show that an anchor exists.

An exact local control illustrates why a nonunit root is not enough when reducing anchor congruences. At $k=6,q=371,p=23$, one has $v_p(A)=1$, $v_p(F)=2$ and $x$ is a unit. Thus $r$ has valuation one and $H$ has valuation two. A pole of $t$ would make $rt^2$ and its square dominate the numerator, so $t$ must be integral at $p$. Then modulo $p^2$ the numerator is $(rt^2+r)(rt^2+x)$. Its valuation is exactly one, as $t^2+1$ is a unit at this inert prime and the other factor is a unit. Therefore this parameter has no integer anchor at all, even though congruences retaining only a nonunit zero can appear to pass.

```python
p=23
M=p**3
u=pow(5,73**6,M)
a=(5*u-131770)%M
x=365*pow(u,371,M)%M
f=(x*x-4*x+a)%M
assert a%p==0 and a%p**2!=0
assert f%p**2==0 and f!=0 and x%p!=0
assert all((t*t+1)%p for t in range(p))
```
