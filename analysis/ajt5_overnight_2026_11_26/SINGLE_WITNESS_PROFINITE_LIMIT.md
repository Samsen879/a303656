# The original single-witness count has a profinite limit

Use all integer exponents in \(X^{1/8}\le 3^c\le X^{1/4}\) and \(X^{1/3}\le 5^d\le X^{1/2}\). Denote the resulting \(T\asymp(\log X)^2\) shifts by \(s=3^c+5^d\). They are distinct: if \(d\) differs, the gap between the 5-powers exceeds the entire 3-power span, and if \(d\) agrees then the 3-powers distinguish the shifts. Write
\[
 A_X(n)=T^{-1}\sum_s r_2(n-s),\qquad X<n\le2X.
\]
Here \(r_2\) counts signs and order. The random variable on these uniformly sampled integers converges in distribution, and in its first two moments, to a nonnegative \(F\in L^2(\widehat{\mathbb Z})\). Its finite-modulus conditional means are explicit. In particular the upper density of integers missed by this box in any dyadic interval is asymptotically at most \(\Pr_{\rm Haar}(F=0)\). Proving \(F>0\) almost everywhere would give density-one for the original single-witness problem. Neither positivity nor pointwise coverage is asserted here.

## Finite centers and the mixed moment

Put \(\rho_Q(t)=Q^{-1}\#\{(u,v)\bmod Q:u^2+v^2=t\}\). Let \(\mu_Q\) be the limiting distribution of the shift modulo \(Q\): eventually the nonunit factors of the bases have stabilized, and the independent exponent intervals, each of length \(\asymp\log X\), become uniform in their respective eventual periods. These distributions commute with reduction. Define
\[
 F_Q(n)=\pi \sum_{s\bmod Q}\mu_Q(s)\rho_Q(n-s).
\]
Counting lifts of two coordinates shows \(F_Q=\mathbb E(F_R\mid n\bmod Q)\) when \(Q\mid R\). At each fixed \(Q\), the lattice points representing \(n-s\) in a fixed \(n\)-class have annular area \(\pi X\) distributed among the relevant coordinate classes modulo \(Q\), with boundary error \(O_Q(\sqrt X)\) uniformly in the shift. Thus on writing \(\mathbb E_X\) for the dyadic mean,
\[
 \mathbb E_X[A_X F_Q]\longrightarrow \mathbb E_{\rm Haar}[F_Q^2],
 \qquad \mathbb E_X[F_Q^2]\longrightarrow \mathbb E_{\rm Haar}[F_Q^2].
\]

## Exact second moment and normalization

For nonzero \(h=s-t\), [Chamizo, Theorem 1.1 and Corollary 1.5](https://link.springer.com/article/10.1007/s00009-021-01959-3) applied at the two endpoints to the positive shift \(|h|\) gives
\[
 \mathbb E_X[r_2(n-s)r_2(n-t)]
 =\pi^2 K(h)+O_\epsilon(X^{-1/3+\epsilon}),\qquad
 K(h)=\kappa_2(h)\prod_{p\ {\rm odd}}\left((1-p^{-2})\sum_{j=0}^{v_p(h)}p^{-j}\right).
\]
Indeed \(|h|=O(\sqrt X)\), so the \(2/3\) error applies uniformly, and \(\kappa_2(h)=|2^{k+1}-3|/2^k\), with \(k=v_2(h)\). The factor \(\prod_{p\text{ odd}}(1-p^{-2})=8/\pi^2\) converts to the paper's divisor sum coefficient. The diagonal contributes \(O((1+\log X)/T)=o(1)\). For example, with \(f=r_2/4\), multiplicativity gives \(f^2\le f*f\) at each prime power: at split primes compare \((e+1)^2\) with \(\binom{e+3}{3}\), and the other primes are immediate. Then \(\sum_{m\le Y} f(m)\ll Y\) from lattice counting gives \(\sum_{m\le Y} f(m)^2\ll Y(1+\log Y)\).

To see that this is the same kernel as the profinite second moment, at odd \(p\) the Haar density of the norm of two Haar coordinates is
\[
 \rho_p(u)=(1-\chi_4(p)/p)\sum_{j\ge0}\chi_4(p)^j1_{p^j\mid u}.
\]
For a split prime transform to a product of two independent coordinates; at an inert prime count the unit norms over the residue field, then divide both coordinates by \(p\) if the norm is divisible by \(p\). Grouping two exponents in the resulting correlation by their minimum gives the odd factor of \(K\). At 2 the density is 2 on nonzero arguments with odd part \(1\bmod4\) and zero otherwise, up to a null set. This follows from the unit norm count (one coordinate odd, the other even; the odd square equation has four roots at depths at least 3), and for even norms the norm map scales by 2 under \((u,v)\mapsto(u+v,u-v)\) on the index-two sublattice of same-parity coordinates. Odd \(h\) and \(h=2\bmod4\) give correlations 1 and \(1/2\), respectively. For \(4\mid h\), the odd inputs contribute 1 and the even inputs half the correlation at \(h/2\). This gives the stated \(\kappa_2\).

## Passing from finite kernels to the limit

All these local densities are in \(L^2\). The finite density at \(p^a\) is the Haar conditional projection of \(\rho_p\), so as \(a\to\infty\) its two-point correlation tends to that of \(\rho_p\), uniformly in \(h\) by Cauchy–Schwarz and translation invariance. At any fixed finite set of primes their finite correlations multiply by CRT. Off-diagonal averaging of the resulting finite kernel agrees asymptotically with the square mean of \(F_Q\), by the finite shift distribution; the diagonal contribution to this comparison is \(O_Q(1/T)\).

For the large-prime factors, pairs of distinct shifts with equal \(d\) are a proportion \(O(1/\log X)\), with \(K(h)\ll\log\log(3X)\) by the usual split of \(\prod_{p\mid h}(1-1/p)^{-1}\) at \(p\asymp\log(3X)\). For different \(d\), at fixed first shift and second \(c\), divisibility \(p\mid h\), \(p\ne5\), imposes at most one class on the second \(d\) modulo \(\operatorname{ord}_p(5)\). If \(L\asymp\log X\) is the interval length, the averaged indicator, also conditional on the two \(d\)'s being different, is \(O(1/\operatorname{ord}_p(5)+1/L)\). The [order-tail estimate](AVERAGED_SHIFT_DISCRIMINANT.md) then applies verbatim to \(\prod_{p\mid h}(1+2/p)\): the small-order primes have summable reciprocal tails; the other primes use Jensen with weights proportional to \(1/(p\log p)\), and primes above \(L^2\) cost \(1+O(1/L)\) deterministically. The background \(\prod(1-p^{-2})\) also has a summable tail. Consequently the expected error from truncating the kernel at primes \(\le z\) tends to zero when \(X\to\infty\) and then \(z\to\infty\). These same estimates bound the total second moment.

Choose a divisibility chain \(Q_z\) absorbing all prime powers, with enough depth to approximate the finitely many local kernels at primes \(\le z\) up to total \(o(1)\). The mixed moment and second-moment calculations give
\[
 \lim_{z\to\infty}\limsup_{X\to\infty}\mathbb E_X[(A_X-F_{Q_z})^2]=0.
\]
The finite centers form a bounded \(L^2\) martingale and converge in \(L^2\) to a nonnegative \(F\), with Haar mean \(\pi\). Fixed-modulus equidistribution and the displayed approximation give convergence in distribution (test bounded Lipschitz functions), and the second moments converge by the same approximation. The zero-event upper bound is the closed-set half of weak convergence. There is no implication in the opposite direction. Restricting to one prescribed exponent phase may hide witnesses: \(c=26,d=50\bmod120\) gives shifts \(2\bmod4\), hence no witness on \(n=1\bmod4\).

## Local normalization replay

~~~python
from collections import Counter
from fractions import Fraction as F

for p,a,es in ((2,8,range(5)),(3,5,range(4)),(5,4,range(4)),(7,3,range(3))):
    q=p**a
    N=Counter((x*x+y*y)%q for x in range(q) for y in range(q))
    for k in es:
        h=p**k
        C=F(sum(N[t]*N[(t+h)%q] for t in range(q)),q**3)
        target=(F(abs(2**(k+1)-3),2**k) if p==2 else
                (1-F(1,p*p))*sum(F(1,p**j) for j in range(k+1)))
        assert C==target, (p,k,C,target)
~~~
