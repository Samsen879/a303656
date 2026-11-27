# A fixed Gaussian difference pins a split allocation and saves two logarithmic powers

This extends [the earlier allocation-conditioned Gram counts](https://github.com/Samsen879/a303656/commit/a78e2b755e8037caf6e4557c2662c6948e170d67) for **true** critical-band numerical pairs. Fixing the Gaussian difference at its constrained angle both reduces the archimedean region and removes the Pell allocation weight of its own norm factor. The result bounds every shell in the indicated range, but it still does not sum the remainder of the signed diagonal to \(O(X)\).

For the multivariable mean-value theorem, use the three primitive irreducible forms \(x^2+y^2+\delta_i\), with \(0,b^2-e^2,g^2-e^2\) distinct. At the smallest claimed \(J\), the smaller box center is \(\gg X^{1/6}/K\), while the coefficient size of the product is \(O(X^{3/8})\); the required fixed power \(1/4\) is thus allowed. Box side length \(\asymp\sqrt J/K^2\) is between a fixed square-root power of either center and the smaller center. At good primes the first-order factor for \(Q_0\) cancels its own sieve root count even though the zero norm level differs from a nonzero norm level. Only \(Q_1,Q_2\) have the split-prime first-order weight 2 and inert weight 0, leaving the signed character Euler product. Bad local valuation densities are bounded uniformly, permitting the already verified bounded discriminant average.

Fixing the Gaussian difference of the two certificate points gives a **factor \(K^2\) saving on every intermediate deficit shell** for \(X=2^K\). For \(X^{1/3}\le J\ll X^2/K^4\), the number of distinct cross-label numerical-seed pairs with deficit \(J<j\le2J\) is
\[
\boxed{N_X(J,2J)\ll K^2J.}
\]
The previous bound for a shell was \(O(K^4J)\). The new estimate imposes no divisibility condition on \(j\). It gives an \(O(X)\) contribution from native relative angles \(O(X^{-1/2})\) after Fejér normalization. The larger relative angles and the unrestricted signed diagonal remain open.

### Fixing the Gaussian difference fixes a Pell allocation

For each label retain \(A_i=9^{r_i}, B_i=25^{s_i}\), \(A_i\le B_i\), \(B_i^{16}\le n\le A_i^{32}\), and \(X\le n<2X\). Put
\[
U_i=2A_i+3B_i,\quad D_i=A_i+2B_i,\quad S_i=n-U_i-D_i,\quad M_i=S_i(S_i+2D_i).
\]
A true seed satisfies \(64k_i^2q_i\le S_i\le64k_i(k_i+1)q_i\) and \(2q_i S_i=(D_i-q_i)^2+4w_i^2\), with \(k_i=\lfloor\log_2S_i\rfloor\). It determines one point \(z_i=n-U_i-q_i+2iw_i\) of norm \(M_i\). Its angle is \(\sqrt2/(8K)+O(K^{-2})\).

Order the labels by \(U_1<U_2\). Define
\[
\begin{split}
e&=U_2-U_1,\qquad b=D_1+D_2,\qquad g=D_2-D_1,\qquad H=2n-U_1-U_2,\\
L&=(n-U_1)(n-U_2)-(D_1^2+D_2^2)/2,\qquad \bar z_1z_2=L-j+ih,\qquad d=2j .
\end{split}
\]
The Gram equation and the first exact norm are
\[
 (dH-ebg)^2-d(2h)^2=(d+e^2)(d+b^2)(d+g^2),
 \qquad N(\Delta)=d+e^2,\quad \Delta=z_1-z_2 .
\]
In addition,
\[
 \bar\Delta z_1=v+ih,\qquad 2v=eH+bg+N(\Delta).
\]
Thus \(\Delta,n,h\) recover both Gaussian points, with no allocation multiplicity left at that step.

Take a split prime \(p\) outside
\[
\mathcal B=2ebg(e^2-b^2)(e^2-g^2)(b^2-g^2)
\]
with \(p^k\Vert N(\Delta)\). In the two split components modulo \(p^k\), identify \(\sqrt d=-ei\). The Pell element then satisfies
\[
 dH-ebg+2h\sqrt d\ \equiv\ -2e(v+ih)
 =-2e\bar\Delta z_1\pmod {p^k}.
\]
The two component depths are at least the corresponding depths of \(\bar\Delta\). Both depth sums equal \(k\), because \(p\) divides only the first Gram factor. The depths are therefore **fixed by \(\Delta\)**. At a good inert prime the ideal allocation is unique. If \(d\) is square, the same comparison applies to the two ordinary integer factors. For each remaining ideal there are \(O(1)\) possible generators at ordinary height. The larger Pell conjugate is \(\asymp dX\) in a fixed-ratio interval, and successive real quadratic units grow by at least the golden ratio.

For \(j\asymp J\), the distance between the radii of \(z_1,z_2\) is \(O(X^{1/16})\), while their tangential separation is \(\asymp\sqrt J\). In the frame rotated by their mean angle, the real part of \(\Delta\) is the difference of radii times \(\cos((\arg z_1-\arg z_2)/2)\), and its imaginary part is the sum of radii times the corresponding sine. Hence for \(J\ge X^{1/3}\) the difference lies in an annular sector of angular width \(O(K^{-2})\) and area \(O(J/K^2)\).

The arithmetic weight in this sector involves the three polynomials
\[
 Q_0=N(\Delta),\qquad Q_1=N(\Delta)+b^2-e^2,\qquad Q_2=N(\Delta)+g^2-e^2.
\]
At good primes \(Q_0\) has weight \(1\), because its Pell allocation is fixed. The other two weights are \(r_2/4\). At bad primes all weights are bounded by fixed powers of the divisor function. Cover the sector by \(O(K^2)\) axis-parallel boxes of side \(\asymp\sqrt J/K^2\), rotating by units as needed. In each box the smaller coordinate is \(\asymp\sqrt J/K\), and the product polynomial has coefficient height \(O(X^{3/8})\). These satisfy the box hypotheses of de la Bretèche and Tenenbaum’s Theorem 3.1 with fixed exponents \(1/2,1/4\). At a good odd prime the three root sets are disjoint, each nonzero norm level has \(p-\chi_4(p)\) points, and the local product is \(1+2\chi_4(p)/p+O(p^{-2})\). The \(Q_0\) term cancels. At bad odd primes a norm-level congruence modulo \(p^\ell\) has density \(O((\ell+1)p^{-\ell})\), uniformly in the level, by splitting into a product of two coordinates or using the inert norm. This leaves a bad-prime factor \(\prod_{p\mid\mathcal B}(1+C/p)\). Its bounded mean over the actual exponent box follows from the order-of-\(9\) argument in the previous turn, applied to the linear factors of \(\mathcal B\). Summing the box areas and \(O(K^4)\) label pairs proves the stated bound. [De la Bretèche and Tenenbaum, Theorem 3.1](https://tenenb.perso.math.cnrs.fr/PPP/NTpols.pdf).

### A necessary native 3-adic phase

If (s_1
otequiv s_2mod3), (r_ige2), then (v_3(B_2-B_1)=1). For (nequiv1mod3) the two (R_i=n-A_i-B_i) are both divisible by 3 and differ to exact depth one; for (nequiv2mod3) the same holds for the two (S_i=n-3A_i-5B_i). These pairs cannot be two-square values simultaneously unless both valuations are even, hence both divisible by 9, which is impossible. Thus the actual target phase here requires (nequiv0mod3). The replay checks a native pair in this phase and a failed deficit; this note does not assert a full local support density.

### Standalone replay

The exact control has labels \((4,3),(3,4)\), two distinct seeds in the \(t=8\) band, and pinned Pell components \((0,9)\) modulo \(37\). A perturbed deficit stays in the same angular window while forcing the forbidden target phase at \(3\).

```python
from math import prod

K, X = 300, 1 << 300
u, a = 472984194841387909896403492694189266281840, 3395
x = a*u + 9**3 + 2*25**4 - (a*a+1)//2
n = x*x + u*u + 3*9**3 + 5*25**4

def N(z): return z[0]**2 + z[1]**2
def bar(z): return z[0], -z[1]
def sub(z,t): return z[0]-t[0], z[1]-t[1]
def mul(z,t):
    a,b = z
    c,d = t
    return a*c-b*d, a*d+b*c

def cert(r,s,P,Q):
    A,B = 9**r,25**s
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    f,g = sub(P,Q)
    assert X<=n<2*X and A<=B and B**16<=n<=A**32
    assert f%2 and g%2 and N(P)==S and N(Q)==S+2*D
    q = ((f+g)//2)**2 + ((f-g)//2)**2
    z = mul(bar(P),Q)
    if z[1]<0: P,Q,z = bar(P),bar(Q),bar(z)
    assert q%2 and z[1]%2==0 and z[0]==n-U-q
    assert 2*q*S==(D-q)**2+z[1]**2 and S.bit_length()-1==K
    assert 64*K*K*q<=S<=64*K*(K+1)*q
    return P,Q,z,U,D,q

p = (1238240656117444633368032107716581205155788446,
     1022396213763583296740059539842408420297582288)
t = (1237638945231334085263186942097216682418805929,
     1023124519121177798984074135516404730073639771)
a1,c1,z,U,D,q = cert(4,3,p,t)
a2,c2,w,V,E,qq = cert(3,4,(x,u),(x+1,a-u))
assert q!=qq and n%3==0
e,b,g = V-U,E+D,E-D
H,L = 2*n-U-V,(n-U)*(n-V)-(D*D+E*E)//2
dot,h = mul(bar(z),w)
j = L-dot
d,P = 2*j,N(z)*N(w)
delta = sub(z,w)
assert j>X and 0<h*h*K**4<P
assert [N(delta),N(sub(mul(a1,bar(a2)),mul(c1,bar(c2)))),
        N(sub(mul(a1,c2),mul(a2,c1)))] == [d+l*l for l in (e,b,g)]
assert (d*H-e*b*g)**2-d*(2*h)**2==prod(d+l*l for l in (e,b,g))

p = 37
assert (2*e*b*g*(e*e-b*b)*(e*e-g*g)*(b*b-g*g))%p
assert (d+e*e)%p==0 and (d+e*e)%(p*p)!=0
pin = []
for i in (6,-6):
    v = (d*H-e*b*g-2*h*e*i)%p
    assert v == -2*e*(delta[0]-i*delta[1])*(z[0]+i*z[1])%p
    pin.append(v)
assert pin == [0,9]

m = 25*2**16
jp = j+m*((3-j)*pow(m,-1,9)%9)
dp = 2*jp
assert jp>j and 0<(P-(L-jp)**2)*K**4<P
assert e%9==0 and g%9==3 and (dp+e*e)%9==6
assert prod(dp+l*l for l in (e,b,g))%27==9
print("Two true seeds, pinned split allocation, and false deficit verified")
```
