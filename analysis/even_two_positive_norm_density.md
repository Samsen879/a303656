# Positive-density even targets with two true representations

for every sufficiently large odd \(U\), let \(Q=5^{2U}\) and choose any set of at least \(\eta U\) odd labels \(V\in[1,U]\), with \(0<\eta<1/2\) fixed. There are \(\gg_\eta Q\) distinct targets \(Q<n<5Q\) in class \(6\bmod120\) with **two true positive representations**, at labels \((2V,2U)\) and \((2V+1,2U)\) for some selected \(V\). The labels share the same actual \(5\)-power. There is no signed upper expression in this construction.

### Two positive labels at even targets

Put \(T=5^U,\ Z=9^V,\ h=2Z\), and solve
\[
ab+cd=h,\qquad a,c,d\in I=[T,11T/10),\qquad
(a,b,c,d)\equiv(89,3,111,41)\pmod{120}.
\]
Set
\[
(u,v,x,y)=\tfrac12(a+b,c+d,b-a,d-c).
\]
Then \(P=u^2+v^2,\ S=x^2+y^2\) satisfy \(P-S=h\), so
\[
n=Q+Z+P=Q+3Z+S.
\]
The congruence gives \(n\equiv6\bmod120\) and makes both norms units at 5. It also gives \((a,h)=1\), since \(h\) is twice a power of 3. This last condition matters in the count. The box ensures \(P,S\asymp Q\) and \(Q<n<5Q\) uniformly for large \(U\), since \(h/Q=o(1)\) even at \(V=U\).

**Uniform congruence count.** For a class \(\rho=(a_0,b_0,c_0,d_0)\bmod m\) extending the class modulo 120 and satisfying \(a_0b_0+c_0d_0\equiv h\bmod m\), the count in this box is
\[
\frac{|I|^2\log(11/10)}{m^3}\prod_{p\nmid m}(1-p^{-2})
+O_\epsilon(T^{3/2+\epsilon}m^2). \tag{1}
\]
Here is the part that handles a prime shared by \(a\) and \(m\). Fix \(a\), let \(m_1\) be the full part of \(m\) supported on primes dividing \(a\), and put \(m_2=m/m_1,\ q=am_1,\ K=h-ab_0\). Then \(K\) is a unit modulo \(q\). The \(b\)-condition is equivalent to \(cd\equiv K\bmod q\) once the prescribed \(c,d\bmod m\) are imposed. Its part modulo \(m_2\) follows from compatibility and invertibility of \(a\bmod m_2\).

Write \(c=c_0+m_1x,\ d=d_0+m_1y\) and complete the \(x,y\) progressions modulo \(a\). Their steps \(m_2\) are units modulo \(a\). The completed sum over \(t=c\bmod q\), with \(t\equiv c_0\bmod m_1\) and \(d\equiv K\bar t\bmod q\), is an average of Kloosterman sums \(S_q(r+ja,sK)\), up to unit phases. Since
\[
\gcd(r+ja,sK,q)\mid m_1\gcd(r,s,a),
\]
the Weil bound gives \(O(\tau(q)m_1\sqrt a\,\gcd(r,s,a)^{1/2})\). The interval Fourier coefficients contribute \(O_\epsilon(a^\epsilon)\) after normalization and exclusion of the zero pair. Indeed, on frequencies divisible by \(k\mid a\) the sum of the nonzero coefficients is \(O((a/k)\log a)\), so the gcd weight costs at most \(O(\log^2a\sum_{k\mid a}k^{-1/2})\). The zero pair counts \(\varphi(q)/\varphi(m_1)\) residues. After dividing by \(a^2\), its factor is \(a^{-1}\prod_{p\mid a,\ p\nmid m}(1-1/p)\). Expanding this product and summing over \(a\equiv a_0\bmod m\) gives (1). [Weil’s Kloosterman estimate](https://pmc.ncbi.nlm.nih.gov/articles/PMC1079093/)

**First moment.** Give a witness full weight \(2^{-\Omega_+(P)-\Omega_+(S)}\), where \(\Omega_+\) counts split-prime multiplicities. In the sieve at a split prime give a coordinate product local weight \(1,1/2,0\) for valuations 0,1, or at least 2 respectively. A pair's survival weight is the product of the two local weights, realized by independent artificial marks at the sieved primes; the sieve inputs are nonnegative (see also the [weighted setup in #62](https://github.com/Samsen879/a303656/pull/62)). At every split \(p>5\), the determinant is a unit. On \(P-S=h\) the two excluded residues modulo \(p^2\) are distinct, so the unnormalized weighted density is exactly
\[
(1-1/p)^2(1-2/p^2).
\]
Summing (1) over the compatible residue classes at \(m=120d^2\), with marking probabilities between zero and one, gives remainder \(O_\epsilon(T^{3/2+\epsilon}d^{12})\). Through \(D=Q^{1/200}\), with \(\epsilon=1/20\), the sum is \(O(Q^{21/25})\). The lower sieve to a sufficiently small fixed power of \(Q\) gives \(\gg Q/\log Q\) witness weight per label. Primes above the sifting range contribute only \(O(1)\) split factors with multiplicity in \(PS\), since \(P,S\asymp Q\). Thus the actual weight \(2^{-\Omega_+(P)-\Omega_+(S)}\) has the same lower bound. Its mass at a single target and label is at most \(16\), by \(r_2/4\) and \(e+1\le2^e\).

**Cross-label mean.** For \(V\ne W\), the four roots \(Q+9^i,\ Q+3\cdot9^i\), \(i=V,W\), are distinct. The inert-prime upper sieve gives \(O(QF_C(\Delta)/\log^2Q)\) common weight, where \(\Delta\) is the product of the six differences and \(F_C(m)=\prod_{p\mid m}(1+C/p)\). At good inert primes the four roots forbid exactly \(4(p-1)\) classes modulo \(p^2\). At squarefree \(d\) the CRT error is \(O(4^{\omega(d)}d)\).

The mean of \(F_C(\Delta)\) is bounded on this actual panel. For each difference \(\log|m|=O(U)\), so the weighted divisor expansion can be truncated at \(d\le U\) at bounded cost: remove primes above \(U^\delta\), then use the bound \(O_C(\delta\log U)\) for the mean of \(\log d\) on the remaining divisors. After removing 2 and 3, each nonconstant divisibility test is \(81^j\equiv r\bmod d\) with the other label fixed. Its mean is \(O(1/\operatorname{ord}_d(81)+1/U)\). The order-weighted sum converges by dyadic summation against \(\prod_{k\le t}(81^k-1)\), and Hölder combines the six differences. Thus the total cross weight is \(O(Q)\). With total first moment \(H\gg_\eta Q\) and second moment at most \(16H+O(Q)\), Cauchy–Schwarz proves the claimed distinct-target count.

This gives **positive lower density for the generated two-positive family** in class \(6\bmod120\), by taking the largest odd \(U\) with \(5Q\le X\). It leaves density one and prescribed targets open.

### Inline replay

The positive control uses both \(3^6\) and \(3^7\) with \(5^{14}\). The nearby control retains the first label but has valuation one at 11 in the second positive residual. The modulus check also exercises the shared-prime branch of (1).

```python
from math import gcd

T, Z = 5**7, 9**3
Q, h = T*T, 2*Z
a,b,c,d = 78209,-90117,83151,84761
assert tuple(t%120 for t in (a,b,c,d)) == (89,3,111,41)
assert all(T <= t and 10*t < 11*T for t in (a,c,d))
assert a*b+c*d == h and gcd(a,h) == 1
u,v,x,y = (a+b)//2,(c+d)//2,(b-a)//2,(d-c)//2
n = Q+Z+u*u+v*v
assert n == Q+3*Z+x*x+y*y == 13187576406
assert Q < n < 5*Q and n%120 == 6

m1 = 197**2
q, K = a*m1, h-a*(b%(120*m1))
assert a == 197*397 and gcd(K,q) == 1
assert c*d%q == K%q

bad = Q+Z+(u+840)**2+v*v
assert bad == 13178279286 and Q < bad < 5*Q and bad%120 == 6
assert (bad-Q-3*Z)%121 == 11
```