# A true first root 248 and three adjacent columns on an infinite integer family

There are infinitely many positive \(m\) for which \(x=5m+4\) has least true shift \(248=5+3^5\), while all three parent columns \(d=4,8,12\) and their adjacent children work at the same point. This uses a new congruence class, independent of the obstruction on the old \(M,P\) class in [the quadratic pullback limit](FIRST_248_QUADRATIC_PULLBACK_DYADIC_LIMIT.md).

## A genuine seed and all earlier obstructions

At \(m=10000899126\), \(x=50004495634\), the four integer square-coordinate pairs for \(x-248\) and \(m-5^d-1\) (in increasing d order) are
\[
 (31019,221455),\quad(82402,56664),\quad(8270,99660),\quad(68630,71040).
\]
Every corresponding child \(x-5^{d+1}-3^2\) is five times the parent residual, so multiplication in \(\mathbb Z[i]\) by \(2+i\) proves it as well. Each smaller possible shift r is blocked by one prime \(3\bmod4\) of exact valuation one in \(x-r\), with the complete partition included in the replay. The product \(M'\) of the distinct blocker squares therefore preserves all exclusions under \(m\) congruence.

## Pell propagation of the two remaining norm gates

Set \(U_*=(34315,35520)\), \(G=(3443,-3594)\), \(g=\|G\|^2=24771085\) and \(L=4M'\). On \(U_n=U_*+LnG^\perp\), retain \(q=G\cdot U_n=-9512335\), and define \(m_n=5^{12}+1+4\|U_n\|^2\). Since \(q+g=(5^{12}-5^4)/16\), the two outer parents are the norms of \(2U_n\) and \(2(U_n+2G)\) respectively. Write \(s=G^\perp\cdot U_n=s_*+Lgn,\ s_*=245623470\). The first-root remainder and middle parent become the targets \(s^2+h_0\), \(s^2+h_3\) times the rational Gaussian norm constants \(20/g,\ 4/g\), where
\[
 h_0=q^2+g(5^{13}-239)/20=3204782529189581/2,\quad
 h_3=q^2+g(5^{12}-5^8)/4=1599972509339725.
\]

From the [two-gate seed construction](FIRST_248_RATIONAL_PULLBACK_SEED_EQUIVALENCE.md), set \(\lambda_i=1/(s_*^2+h_i)\), \(b=s_*(\lambda_0+\lambda_3)-1/s_*\), \(u_i=s_*\lambda_i-b/2\), \(a=\lambda_i-u_i^2\) (common for both i). The genuine seed implies that both \(\lambda_i\) are rational Gaussian norms. For any \(\xi,Y\) with \(Y^2=a\xi^2+b\xi\), we have
\[
 \lambda_i((s_*+\xi)^2+h_i)=(1+u_i\xi)^2+Y^2 .
\]
Exact rational checks below give \(a,b>0\), with \(a\) nonsquare since \(4s_*^2a\equiv2\bmod3\). Take a positive integer D clearing the denominators so \(A=D^2a,\ B=D^2b\) are integral. For any positive Pell unit of norm one in \(\mathbb Z[\sqrt A]\), a power becomes 1 modulo \(2ALg\) in both coefficients. Apply its successive powers to \((B,0)\) in
\[
 X^2-AZ^2=B^2.
\]
The new X grows unboundedly, and \(X=B+2A\xi\) for \(\xi\equiv0\bmod Lg\). Then \(Y=Z/(2D)\) solves the conic identity. This produces actual integer parameters n with both extra gates, preserving the blocker phase. A positive integer which is a rational Gaussian norm is an integer two-square norm by the even-valuation criterion at inert primes. Therefore the Pell method gives infinitely many real arithmetic points, not only rational-function identities. It does not establish the same result at the enormous fixed exponents in the old class, four columns, or the universal conjecture.

~~~python
from fractions import Fraction as F
from math import isqrt
m=10000899126
x=5*m+4
blocks={2:7,4:24419,6:12501123907,8:31,10:2083520651,14:103,26:3851,
        28:263,32:19,34:151,52:12899,82:11,86:7,106:199,126:11,
        128:7,134:23,152:32003,206:71,244:283}
assert set(blocks)=={5**e+3**f for e in range(4) for f in range(6)
                     if 5**e+3**f<248}
for r,p in blocks.items():
    assert p%4==3 and all(p%d for d in range(2,isqrt(p)+1))
    assert (x-r)%p==0 and (x-r)%(p*p)!=0
assert x-248==31019**2+221455**2
for d,a,b in [(4,82402,56664),(8,8270,99660),(12,68630,71040)]:
    assert m-5**d-1==a*a+b*b
    assert x-5**(d+1)-9==(2*a-b)**2+(a+2*b)**2
u,v=34315,35520
a,b=3443,-3594
g,s,q=a*a+b*b,-b*u+a*v,a*u+b*v
assert (g,s,q)==(24771085,245623470,-9512335)
assert q+g==(5**12-5**4)//16 and m==5**12+1+4*(u*u+v*v)
h0=q*q+F(g*(5**13-239),20)
h3=q*q+F(g*(5**12-5**8),4)
assert h0==F(3204782529189581,2) and h3==1599972509339725
lam=[1/(s*s+h) for h in (h0,h3)]
b=s*sum(lam)-F(1,s)
a=[l-(s*l-b/2)**2 for l in lam]
assert a[0]==a[1]>0 and b>0
v=4*s*s*a[0]
assert v.numerator*pow(v.denominator,-1,3)%3==2
~~~
