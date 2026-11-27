# A factorization-free cyclotomic family of variable-slope quartics

For every integer $k\ge1$, set $d=1+73^k$, $M=5^{d-1}-1$, $A=5^d-131770$, $B=A-4$, and
$$
r=A/365,\quad H=r+A/r-4=M/73,\quad m=H/2.
$$
These are actual labels $(d,2;d+1,3)$. Set $Z=rt^2+2$, $w=(Z^2+m^2+B)/H$, $D=(r^2t^2+A)/m$. Direct expansion gives the two rational norm identities for $(w-D,t(D-r))$ and $(w-m-2Z,2(w-m)+Z)$, of norms $w^2-A$ and $5(w^2-B)$. Rotate both pairs by $(55-48i)/73$.

We choose $t$ without factoring $M$. Put $X_j=5^{73^{j-1}}$ and $F_j=1+X_j+\cdots+X_j^{72}$ for $1\le j\le k$. They multiply to $M/4$ and are pairwise coprime: at every prime dividing $F_j$, $5$ has order exactly $73^j$. The exceptional prime $73$ never divides $M$, since $73^k$ is coprime to $72$ and $5\not\equiv1\bmod73$. The same argument excludes $19$, using $18$. In the ring modulo $F_j$, let $G_j=\sum_{a=1}^{72}(a/73)X_j^a$. The usual finite Gaussian-sum calculation works in this ring: conjugation sends $X_j$ to $X_j^{-1}$ and fixes the sum since $(-1/73)=1$; in the product reindex $a=ub\bmod73$. The inner sum over $b=1,\ldots,72$ equals $72$ if $u=1$, and $-1$ otherwise by permuting the nonzero exponent classes. Hence $G_j^2=73$. Take
$$
t\equiv 5^{d/2}G_j/19\pmod{F_j}.
$$
This gives $361t^2\equiv365\bmod M/4$, since $5^d\equiv5\bmod M$. The congruence implies that both numerators defining $D,w$ vanish modulo the full odd part of $M$: there $r\equiv-361$, $r^2t^2+A\equiv0$, and $Z\equiv-363$ with $Z^2+B\equiv0$.

Complete the CRT with odd $t$, $t\equiv14\bmod73$, and $t\equiv1$ or $2\bmod5$. At $2$, $H$ has valuation two, $m$ has valuation one, $r,A$ are odd, and $B\equiv3\bmod8$; this gives integral $D$ and even $w$. The only remaining potential denominators are at $73$. After multiplying each output by $73^2$, its reduction modulo $73^2$ depends only on $A,M,t\bmod73^2$; this follows immediately by substituting $r=(A/5)/73$ and $H=M/73$, with $M$ a unit there. Moreover $A,M$ have the same residues as at $k=1$, since $73^k\equiv73\bmod(72\cdot73)$ for $k\ge1$. The replay verifies all 73 possible lifts of $t\equiv14\bmod73$ at $k=1$, which handles this finite check uniformly. Modulo $3$, $w\equiv1$. Modulo $5$, the choices $t=1,2$ give $w=1,4$, respectively.

The common progression $t=t_0+120\cdot73^2M\,n$ clears all nonconstant coefficients of the rational polynomials and makes them multiples of 30: before substituting, their denominators divide $4\cdot73^2M$ by the displayed formulas. The constants are the verified integral anchor. Thus we have positive unbounded quartics with $w\equiv16\bmod30$ for the first digit; for the second digit, taking the negative of $w$ gives a negative orbit with $w\equiv26\bmod30$, and preserves the norm identities. **This does not produce positive $w\equiv26\bmod30$**, nor a general solution of A303656.

```python
from fractions import Fraction as F
from math import gcd
def values(d,t):
 M=5**(d-1)-1; A=5**d-131770; B=A-4
 r,H=F(A,365),F(M,73); m=H/2
 z=r*t*t+2; w=(z*z+m*m+B)/H
 D=(r*r*t*t+A)/m
 P,Q=w-D,t*(D-r)
 U,V=w-m-2*z,2*(w-m)+z
 rot=lambda a,b:((55*a+48*b)/73,(55*b-48*a)/73)
 return w,*rot(P,Q),*rot(U,V)
for j in range(73):
 assert all(v.denominator%73 for v in values(74,14+73*j))
for k in (1,2):
 d=1+73**k; M=5**(d-1)-1
 for digit,sign,residue in [(1,1,16),(2,-1,26)]:
  t,L=0,1
  for q,a in [(2,1),(5,digit),(73,14)]:
   t+=L*((a-t)*pow(L,-1,q)%q); L*=q
  for j in range(1,k+1):
   x=5**(73**(j-1)); q=(x**73-1)//(x-1)
   G=sum(pow(x,a,q)*(1 if pow(a,36,73)==1 else -1) for a in range(1,73))
   assert G*G%q==73 and gcd(q,L)==1
   a=pow(5,d//2,q)*G*pow(19,-1,q)%q
   assert (361*a*a-365)%q==0
   t+=L*((a-t)*pow(L,-1,q)%q); L*=q
  assert L==365*M//2
  for n in range(2):
   w,P,Q,U,V=values(d,t+120*73**2*M*n)
   A=5**d-131770; B=A-4
   assert all(v.denominator==1 for v in (w,P,Q,U,V))
   assert w>0 and (sign*w)%30==residue
   assert P*P+Q*Q==w*w-A and U*U+V*V==5*(w*w-B)
```
