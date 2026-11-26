# A uniform smooth-complement tail and exact joint lifting depth

**A sufficiently large smooth part of the complement gives a summable dyadic bound. The two square congruences alone do not let us charge the reader to smaller smooth divisors.** For a basis of the joint lattice, the reader’s square enters the common gcd at the full complement order. This remains true when both individual orders are large and that order has many small prime factors. [Pinned two-source result](https://github.com/Samsen879/a303656/blob/a9560b603bc37767b1d6e9afd3c79445f000c2f5/analysis/ajt5_overnight_2026_11_26/JOINT_QUOTIENT_TWO_ALIGNED_SOURCES.md)

### Where the square enters

Write \(D=pt\) for the two homogeneous sources and \(M=|\langle3,5\bmod q\rangle|/D\). Take rational monomials \(U,V\) from a basis of the joint relation lattice. Their images generate the cyclic complement of order \(M\). For
\[
G_j=\gcd\bigl(|\operatorname{num}(U^j-1)|,\,
                 |\operatorname{num}(V^j-1)|\bigr),
\qquad
\lambda_q=\min_{a=3,5}v_q(a^{q-1}-1),
\]
one has the exact formula
\[
v_q(G_j)=
\begin{cases}
0,&M\nmid j,\\
\lambda_q+v_q(j/M),&M\mid j.
\end{cases}
\]
At \(j=M\), one direction follows by lifting the two base congruences. For the converse, the basis generates \((D,0)\) and \((0,D)\), so simultaneous divisibility by \(q^e\) forces \(3^{DM}\equiv5^{DM}\equiv1\pmod{q^e}\). Since \(DM\mid q-1\), this implies \(e\le\lambda_q\). The formula for multiples follows by lifting the exponent.

Thus every proper divisor of a smooth \(M\) misses \(q\) in the common gcd. Also, multiplying the exponent by \(q\) manufactures a square even for an ordinary reader, so the square test must be made at \(M\). For fixed \(D,M\), the count of genuine candidates in \([X,2X)\) is bounded by
\[
\min\!\left(\frac{3X}{DM},\,\frac{\log G_M}{2\log X}\right).
\]
When \(M\asymp X\) for fixed \(D\), the congruence already leaves \(O(1)\) candidates per \(M\). Even an \(o(M)\) bound for \(\log G_M\) allows the \(2\log q\) needed by each of those candidates. Factoring \(M\) does not change that comparison.

### A uniform smooth-part bound

Let \(S_y(M)=\prod_{\ell\le y}\ell^{v_\ell(M)}\). For \(y\ge e^2\) and \(R\ge1\), the fraction of \(n\le N\) admitting one of these aligned zero branches with \(X\le q<2X\) and \(S_y(M)\ge R\) is
\[
\boxed{\displaystyle
  O\!\left((1+\log y)^8 R^{-1/\log y}\right)}
\]
uniformly in \(N\) and over all pairs of sources. This bound allows both individual orders to be large and allows a large prime factor in the rest of \(M\).

For a fixed pair, such a branch requires \(D^2q\mid n\). It also gives a \(y\)-smooth divisor \(m\ge R\) of \(M\), so \(q\equiv1\pmod{Dm}\). There are at most \(3X/(Dm)\) possible readers in the interval when \(Dm\le2X\). Their total contribution, using \(\lfloor N/(D^2q)\rfloor\), is at most
\[
\frac{3}{D^3}\sum_{\substack{m\ge R\\P^+(m)\le y}}\frac1m
\le
\frac{3R^{-\delta}}{D^3}
\prod_{\ell\le y}(1-\ell^{-1+\delta})^{-1},
\qquad \delta=1/\log y .
\]
The product is \(O((1+\log y)^8)\). Indeed \(\ell^\delta\le e\), the quadratic terms in its logarithm sum to a bounded amount, and \(\sum_{\ell\le y}1/\ell\le e\log(1+\log y)\) by the Euler product at \(1+\delta\). Finally \(\sum_{p<t}(pt)^{-3}\) converges.

In particular, \(S_y(M)\ge X^\kappa\) and \(y\le\exp((\log X)^{1-\epsilon})\), for fixed \(\kappa,\epsilon>0\), give a summable bound \(O((\log X)^8 e^{-\kappa(\log X)^\epsilon})\). This saving comes from the divisors of \(q-1\). It does not require an estimate for the frequency of common Wieferich primes. With \(y=X^\theta\) for fixed \(\theta>0\), this argument does not give a summable bound.

### Actual \(3,5\) control

For \(p,t=7,19\), the joint basis gives \(U=6075\) and \(V=(5/3)^{19}\). At \(q=9603931\), the complement is \(72210=2\cdot3\cdot5\cdot29\cdot83\). The two orders are \(14442\) and \(24070\), both above \(\sqrt q\), and the first common exponent is exactly \(72210\). The reader is ordinary. Its square fails at that exponent and appears at \(qM\), as predicted. At the same target below, all 133 repairs give exact valuations \(2,2,1\), and \(n=3+1+u^2+v^2\) is a true representation.

```python
from math import isqrt, lcm, prod

p,t,q = 7,19,9603931
F = (2,3,5,29,83)
M = prod(F)
for z in (p,t,q,*F):
    assert all(z%i for i in range(2,isqrt(z)+1))
assert q-1==p*t*M
assert all(pow(a,(q-1)//z,q)!=1 for a in (3,5) for z in (p,t))
Q = q*q
U,V = 6075,pow(5*pow(3,-1,Q),19,Q)
def order(a):
    e = M
    assert pow(a,e,q)==1
    for f in F:
        while e%f==0 and pow(a,e//f,q)==1:
            e //= f
    return e
assert (order(U),order(V))==(14442,24070)
assert all(pow(U,M//f,q)!=1 or pow(V,M//f,q)!=1 for f in F)
assert all(pow(a,M,Q)!=1 and pow(a,q*M,Q)==1 for a in (U,V))

u,v = 709193061264149510581,876168245340487601772
n = 4+u*u+v*v
H = lcm(6*p*p,18*t*t,q*(q-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
J,K = step(p*p),step(t*t)
for x in range(p):
    for y in range(t):
        c = 3*q*((q-1)//2)+J*x+K*y
        d = J*x+K*(11*y%t)
        def rem(m):
            return (n-pow(3,c,m)-pow(5,d,m))%m
        for z,j in ((p,J),(t,K)):
            if rem(z**3)==0:
                c += z*j
            assert rem(z**3) in range(z*z,z**3,z*z)
        assert rem(Q)==q and rem(3)==rem(4)==1
```

Adding a sufficiently large multiple of \(6p^3t^3q^2\) to \(u\) activates all replayed exponents and preserves the tests. The summable estimate covers the stated smooth-part regime, including genuine common Wieferich readers there. A square-specific saving for proportional complement order with only polynomial-scale smoothness remains open.

In the Rankin product, \(\ell^{-1+\delta}\le2^{-1/2}\) and each square is at most \(e^2/\ell^2\), so the quadratic remainder is uniformly bounded even at the small \(y\) endpoint. The exponent from the reciprocal prime sum is at most \(e^2<8\). The result is a uniform upper count in the specified highly smooth regime; it does not claim a new global decimal estimate.
