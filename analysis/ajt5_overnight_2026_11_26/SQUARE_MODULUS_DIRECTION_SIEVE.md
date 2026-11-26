# A prime-square sieve for a genuine middle-area triple slice

Use the marked triple geometry of [CROSS_DIRECTION_DIVISOR_SLICE.md](CROSS_DIRECTION_DIVISOR_SLICE.md), with primitive first edge, \(A=\sqrt X,\ h\asymp H=Aw^2,\ k\asymp B=Aw,\ w=C/(\log X)^2\) for fixed \(C\). Take \(q=1\) or 5. Restrict to a fixed interior corridor where \(j/(qh)\) and \(\ell/(qk)\) are bounded away from 0, 1, and 2, their difference is bounded away from 0, and all three marked positions are in the ordinary positive-height geometry.

Require a prime square \(m=p^2\in[H/10,H]\) with \(p\nmid2qhk\), and write \(j=2qh+mu,\ \ell=2qk+mv\). Put \(P=h^2+k^2,\ \delta=s_0-s_1,\ \gamma=s_0-s_2\). Inserting into the exact norm-difference equations yields
\[
 \gamma-2\delta-2P\equiv0\pmod m.
\]
For fixed \(h,p\) and shifts there are at most two unit \(k\) classes mod \(p^2\), by simple-root lifting. The power box has \(O((\log X)^2)\) distinct shifts, so the number of labeled candidate directions is \(O_C(B\sqrt H(\log X)^5)=O_C(X^{3/4}\log X)\): each prime and shift triple contributes \(O(HB/p^2)=O(B)\) directions, and there are \(O(\sqrt H/\log H)\) primes. For each candidate primitive edge, its integral base positions in the ordinary sector lie on one line with steps \((k,h)\), so there are \(O(A/k)=O(1/w)\) choices. For each base position the congruence gives \(O(1)\) horizontal third displacements, and positivity leaves at most one vertical displacement at the required norm. Thus the marked true count is \(O_C(X^{3/4}(\log X)^3)\) in this slice.

## Exact second gate

Choose an integer solution \((a_*,b_*)\) of \(-2ha_*+2kb_*=\delta-P\), so an integral base point has \((a,b)=(a_*+kz,b_*+hz)\) with integer \(z\). Let
\[
 E=ku-hv,\quad
 T=q^2(\gamma-2\delta-2P)/m,\quad
 F_*=-2qa_*u+2qb_*v+4q(hu+kv)+m(u^2+v^2).
\]
Then \(z=(F_*-T)/(2qE)\) by direct substitution; \(E\ne0\) in the corridor. The prime-square direction sieve does not imply the integrality of this quotient.

```python
from fractions import Fraction as Q
h,k,j,l,q,m=13,41991,9,31863,5,121
a,b,n=657784181,182648,432680062134664111
s0,s1,s2=531446,531566,59174
assert (s0,s1,s2)==(3**12+5,3**12+125,3**10+125)
P,de,ga=h*h+k*k,s0-s1,s0-s2
assert P%m==64 and (ga-2*de-2*P)%m==0
assert a*a+b*b+s0==(a-h)**2+(b+k)**2+s1==n
x,y=Q(q*a-j,q),Q(q*b+l,q)
assert x*x+y*y+s2==n
assert ((4*x-3*y)/5,(3*x+4*y)/5)==(526113931,394821724)
a0,b0=37157,-20984
assert -2*h*a0+2*k*b0==de-P
for step,want in ((0,15664),(m,Q(47137993,3130))):
    assert (j-2*q*h)%m==(l+step-2*q*k)%m==0
    u,v=(j-2*q*h)//m,(l+step-2*q*k)//m
    E=k*u-h*v
    T=q*q*(ga-2*de-2*P)//m
    F=-2*q*a0*u+2*q*b0*v+4*q*(h*u+k*v)+m*(u*u+v*v)
    assert Q(F-T,2*q*E)==want
```
