# Second Gram allocation pin and a native rational local-flexibility obstruction

Continue [the fixed Gaussian-difference allocation count](https://github.com/Samsen879/a303656/commit/f1a50813b5a2521b546c72e8592c8c56cdaeef57). Fixing an endpoint marker can pin an additional factor, but counting all its Gaussian representations spends the same allocation weight. Finite modular checks do not choose that second allocation even with the *oriented* first difference and strict real critical band fixed. The exact rational control below is independently constructed from the previous native \((4,3),(3,4)\) pair, rather than relying on an inaccessible workspace fixture. This is not a counterexample with a second integral target, nor an improved mean-value bound.

Let \(z_i=\bar a_i c_i\), \(N(a_i)=S_i\), \(N(c_i)=S_i+2D_i\), and use the ordinary height notation \(e=U_2-U_1,b=D_1+D_2,g=D_2-D_1,H=2n-U_1-U_2\), \(L=(n-U_1)(n-U_2)-(D_1^2+D_2^2)/2\), \(\bar z_1z_2=L-j+ih\), and \(d=2j\). Set \(x=dH-ebg,y=2h,\mathcal R=(d+e^2)(d+b^2)(d+g^2)\). Then \(x^2-dy^2=\mathcal R\).

Put \(P=a_1\bar a_2\) and \(W_b=P-c_1\bar c_2\). Direct multiplication gives \(N(W_b)=d+b^2\), \(\bar W_b P=v_b-ih\) with \(2v_b=-bH-eg+d+b^2\). At a good split prime \(p^k\Vert d+b^2\), use \(\sqrt d=-bi\) in the two split components modulo \(p^k\). Then \(x+y\sqrt d\equiv2b\bar W_bP\bmod p^k\). Its component valuations dominate those of \(\bar W_b\); their sums are each \(k\) because that prime divides only the second Gram factor. Thus \(W_b\) pins the second allocation. But a full norm circle has \(k+1\) choices of its own Gaussian allocation at this prime, exactly the weight removed. A support restriction or narrow integral angular range is still needed.

For the finite-local obstruction fix \(\Delta=z_1-z_2\) and \(C=N(\Delta)=d+e^2\). A rational Pell point \((x',y')\) on the same conic recovers
\[
 H'=(x'+ebg)/d,\quad n'=(H'+U_1+U_2)/2,\quad
 z_1'=\frac{eH'+bg+C+i y'}{2\bar\Delta},\quad z_2'=z_1'-\Delta .
\]
At a good split prime dividing the second factor, \(d,C\) are units. Hensel gives a root \(\kappa^2=d\), and locally one can prescribe \(x'+\kappa y'=p^r u,\ x'-\kappa y'=(\mathcal R/p^r)u^{-1}\) for any unit \(u\) and \(0\le r\le k\). Rational parametrization of the conic from its known point and weak approximation allow arbitrary finite precision at those good primes, the original first-factor primes and the real place. The rational solution need not be integral away from the checked primes.

Here is an explicit opposite-allocation instance. At the actual native target of bit length 301, the two original seeds are distinct and in the strict \(K=300\) band. For the second factor \(p=277\) occurs exactly once, and the two split readings are \((0,45)\bmod277\). The exact rational variant keeps the same oriented \(\Delta\), the strict real band inequalities and all original target/point readings modulo \(30C\), and changes those readings to \((41,0)\). The denominator is not asserted to be a unit at every prime.


```python
from fractions import Fraction as F
from math import gcd

K,X=300,1<<300
u,a=472984194841387909896403492694189266281840,3395
xx=a*u+9**3+2*25**4-(a*a+1)//2
n=xx*xx+u*u+3*9**3+5*25**4
a1=(1238240656117444633368032107716581205155788446,
    1022396213763583296740059539842408420297582288)
c1=(1237638945231334085263186942097216682418805929,
    1023124519121177798984074135516404730073639771)
a2,c2=(xx,-u),(xx+1,u-a)
def N(z): return z[0]**2+z[1]**2
def bar(z): return z[0],-z[1]
def mul(v,w):
    a,b=v; c,d=w
    return a*c-b*d,a*d+b*c
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
U,V=2*9**4+3*25**3,2*9**3+3*25**4
D,E=9**4+2*25**3,9**3+2*25**4
z,w=mul(bar(a1),c1),mul(bar(a2),c2)
def cert(n,U,D,z):
    S=n-U-D
    q=n-U-z[0]
    assert X<S<2*X and 64*K*K*q<S<64*K*(K+1)*q
    assert 2*q*S==(D-q)**2+z[1]**2
    return q
assert cert(n,U,D,z)!=cert(n,V,E,w)
for (r,s),af,cf,U0,D0 in [((4,3),a1,c1,U,D),((3,4),a2,c2,V,E)]:
    assert 25**(16*s)<=n<=9**(32*r) and 9**r<=25**s
    assert N(af)==n-U0-D0 and N(cf)==n-U0+D0
    dr,di=sub(af,cf)
    assert dr%2 and di%2
    assert ((dr+di)//2)**2+((dr-di)//2)**2==cert(n,U0,D0,mul(bar(af),cf))

e,b,g=V-U,D+E,E-D
H,L=2*n-U-V,(n-U)*(n-V)-(D*D+E*E)//2
dot,h=mul(bar(z),w)
d=2*(L-dot)
dx,dy=sub(z,w)
C=dx*dx+dy*dy
P=mul(a1,bar(a2))
W=sub(P,mul(c1,bar(c2)))
v,k=mul(bar(W),P)
assert N(W)==d+b*b and k==-h and 2*v==-b*H-e*g+d+b*b
x,y=d*H-e*b*g,2*h
R=(d+e*e)*(d+b*b)*(d+g*g)
assert C==d+e*e and x*x-d*y*y==R
p=277
assert all(p%j for j in range(2,17))
assert R%p==0 and R%(p*p)!=0 and (d+b*b)%p==0
k=14171
assert k*k%(p*p)==d%(p*p) and k%p==(-b*60)%p
assert ((x+k*y)%p,(x-k*y)%p)==(0,45)
m=30*C
J=4*d*C*m
t=F(J*((1-p)*pow(k*J,-1,p*p)%(p*p)),1+J*p*p*2**10000)
X1=(x*(1+d*t*t)+2*d*y*t)/(1-d*t*t)
Y1=(y*(1+d*t*t)+2*x*t)/(1-d*t*t)
def modp(t): return t.numerator*pow(t.denominator,-1,p)%p
assert X1*X1-d*Y1*Y1==R
assert (modp(X1+k*Y1),modp(X1-k*Y1))==(41,0)
H1=(X1+e*b*g)/d
n1=(H1+U+V)/2
z1=((e*H1+b*g+C)*dx-Y1*dy,(e*H1+b*g+C)*dy+Y1*dx)
z1=tuple(t/(2*C) for t in z1)
z2=sub(z1,(dx,dy))
assert sub(z1,z2)==(dx,dy)
assert X<n1<2*X
assert 25**48<n1<9**128 and 25**64<n1<9**96
assert cert(n1,U,D,z1)>0 and cert(n1,V,E,z2)>0
for a,b in zip((n1,*z1,*z2),(n,*z,*w)):
    assert gcd(a.denominator,m)==1
    assert (a.numerator-b*a.denominator)%m==0
```
