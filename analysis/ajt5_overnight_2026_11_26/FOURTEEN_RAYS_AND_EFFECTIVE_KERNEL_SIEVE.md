# Fourteen sphere rays and an effective half-kernel sieve

**The seed \((138,170)\) closes the \(42\)–\(142/3\) gap at phase \(46\).** The fourteen rays now give an effective count of distinct generated targets in each odd class modulo \(4\),
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{17/38}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda=1,3.
\]

The kernel obstruction also strengthens quantitatively. Write \(\log_j\) for the \(j\)-fold iterated logarithm. There is an effective absolute \(\kappa>0\) such that, for \(1\le T\le\log_3 U\), only \(O(U/T+U^{1/2})\) half-exponents \(u\le U\) have an admissible partner for which **either** half’s squarefree kernel is supported on primes up to
\[
y=\kappa(\log U)(\log_2 U)\frac{\log_3 U}{T}.
\]
The bound also holds for the cubing closure of the restricted seeds. Taking \(T=\log_4 U\) gives a growing improvement over every fixed multiple of \(\log U\log\log U\). No numerical onset is supplied here.

### A truncated Chebotarev sieve

Let \(H_\pm=(5^u\pm3^v)/2\) with \(u,v\) odd. For an admissible pair, the squarefree kernels of both halves are supported on \(p\equiv1\bmod3\). Use sieve primes \(7\le\ell\le R=(\log y)^{1/100}\), omitting \(\ell\mid u\). At \(p\equiv1\bmod\ell\), a prime dividing either half must satisfy the previous common condition \(u a_\ell=v b_\ell\bmod\ell\), where \(a_\ell,b_\ell\) are the order-\(\ell\) residue logs of \(5,3\). Sieve out \(p\) when this condition fails.

The useful change is to count intersections of failures only for squarefree \(d\le R^2\), using
\[
K_d=\mathbb Q(\zeta_{3d},5^{1/\ell},3^{1/\ell}:\ell\mid d).
\]
The relative radical degrees are \(\ell^2\), and the extensions for distinct \(\ell\) are independent over the cyclotomic base. Thus the primes \(p\equiv1\bmod3\) failing every condition indexed by \(\ell\mid d\) have density \(1/(2d)\). At each \(\ell\), the factor is \(1/(\ell-1)\) for \(p\equiv1\bmod\ell\), times \((\ell-1)/\ell\) for failure of the linear condition.

The degree is at most \(2d^3\) and the root discriminant is at most \(3d^5\). For the latter, the cyclotomic contribution is at most \(3d\), and adjoining the two radicals for each \(\ell\) multiplies the root discriminant by at most \(15\ell^2\), using the polynomial discriminants. The Lagarias–Odlyzko range \(\log y\ge10[K_d:\mathbb Q](\log|\Delta_{K_d}|)^2\) holds effectively for \(d\le R^2\). The field is normal over \(\mathbb Q\). In the Stark bound quoted as Theorem 1.4, the reciprocal scale is the maximum of \(4\log|\Delta_{K_d}|\) and a constant times the root discriminant, both \(O(d^5)\). Hence \(1-\beta\gg d^{-5}\) for a possible exceptional zero. Consequently, even after summing over conjugacy classes, the intersection count is
\[
\frac{\operatorname{Li}(y)}{2d}+O_A\big(y/(\log y)^A\big)
\]
uniformly in the frozen exponent phase, for every fixed \(A\). Removing primes \(p\le R\) is absorbed in this error. [Lagarias–Odlyzko, Theorems 1.3–1.4](https://aareyanmanzoor.github.io/assets/articles/lagarias-odlyzko.pdf#page=5)

For the sieve calculation, let \(P\) be the product of the retained sieve primes and \(G=\sum_{r\mid P,\ r\le R}1/\varphi(r)\). Squaring divisor weights supported on \(d\mid P,\ d\le R\), with \(\lambda_1=1\), gives main quadratic form
\[
\sum_{d,e}\frac{\lambda_d\lambda_e}{[d,e]}
=\sum_r\varphi(r)\left(\sum_{r\mid d}\frac{\lambda_d}{d}\right)^2.
\]
Taking the inner sums to be \(\mu(r)/(\varphi(r)G)\) gives \(1/G\) and weights \(|\lambda_d|\le d\). The total weighted error is at most \(R^4\) times the uniform Chebotarev error. Also
\[
G\gg\frac{\log R}{W_R(u)},\qquad
W_R(u)=\prod_{\substack{7\le\ell\le R\\\ell\mid u}}(1-1/\ell)^{-1}.
\]
Indeed, the unrestricted squarefree sum with \((r,30)=1\) is \(\gg\log R\). Splitting off the excluded prime divisors of \(u\) bounds it above by \(G W_R(u)\).

Thus a frozen phase admits \(O(W_R(u)y/(\log y\log R))\) possible kernel primes. The mean of \(W_R(u)\) is bounded by expanding its product and averaging divisibility, so \(W_R(u)>T\) costs \(O(U/T)\) half-exponents. There are \(\exp(O(R))\) phase patterns. Each fixed kernel gives \(O(1)\) exponent pairs uniformly in the kernel, by the unit equation obtained from \(5x\pm z\sqrt{10C}\) when \(H_\pm=Cz^2\) and \(x=5^{(u-1)/2}\). Thus the remaining count is at most \(\exp(O(R+Ty/(\log y\log R)))\). At the stated cutoff, \(\log R\asymp\log_3 U\) and an effective small \(\kappa\) makes this at most \(U^{1/4}\). For the cubing closure, apply the same estimate with the base cutoff \(U/3^k\) and the same \(y,T\). The exceptional terms form a geometric sum and the other terms cost only \(O(U^{1/4}\log U)\). [Evertse–Schlickewei–Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04)

### Phase \(46\) and exact controls

The new seed has \(e>m\), but the margin needed for the fixed-height estimates holds: \(3^{170}<5^{119}\) follows from \(3^{10}<5^7\). Under cubing, \(Q=5^{138\cdot3^k}\) and \(Z=3^{170\cdot3^k}\) retain \(Z<Q^{119/138}\). With \(v^2+3w^2=4(Q-Z)\), the usual sphere identity gives \(n=Q+(4-\lambda)Z+v^2+r^2\) in the two classes \(21\bmod24\) and \(3\bmod24\). Both positive exponents grow. [Effective fixed-height count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The new ratios are \(46/42\) and \((142/3)/46\). The maximum becomes \(38/34=19/17\), so the last completed window ends above \(X^{17/19}\). At \(X=5^{38\cdot3^j}\), the preceding lower power is \(5^{34\cdot3^j}\), giving the matching liminf ceiling \(17/38\) for these rays.

The replay checks both classes at depths zero and one. At the same heights the signed controls have exact odd valuation at \(43\) or \(103\) for their prescribed positive residuals.

```python
from fractions import Fraction as F

def N(a,b):
    return a*a + 3*b*b

def orient(a,b,c,d):
    z = [(a*c-3*b*j*d, abs(b*c+a*j*d)) for j in (1,-1)]
    return max((p for p in z if p[1]%3), key=lambda p:p[1])

a,b = 753340213290939970244329,305238405367721618793260
c,d = 473335938622185318192878,455699482269374512153180
q,s = 5**69,3**85
assert 2*N(a,b) == q-s and 2*N(c,d) == q+s
Q,Z = q*q,s*s
assert Z < 5**119
v,w = (4*z for z in orient(a,b,c,d))
for k,(j,p,h) in enumerate(((1,43,129),(29,103,6695))):
    assert Q == 5**(138*3**k) and Z == 3**(170*3**k) == s*s
    assert N(v,w) == 4*(Q-Z) and w > s and w%3
    for good,t in ((True,w),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            r,S = t+s,x*x+y*y
            n = 5*Q+lam*Z-S
            assert Q < n < 5*Q and S > lam*Z
            assert n%24 == (21 if lam == 1 else 3)
            assert 2*lam*Z-S == r*r-3*t*t
            R = n-Q-(4-lam)*Z
            assert (R == v*v+r*r if good else R%(p*p) == h == p*(h//p))
    v,w = orient(v,w,(Q-Z)//2,(Q+Z)//2)
    Q,Z,s = Q**3,Z**3,s**3

ph = [F(18),F(178,9),F(22),F(70,3),F(26),F(82,3),F(30),F(290,9),
      F(34),F(38),F(42),F(46),F(142,3),F(158,3),F(54)]
assert max(b/a for a,b in zip(ph,ph[1:])) == F(19,17)
```

The population bound concerns generated targets. The kernel estimate constrains one proposed source of dense seed heights, and the failed controls concern their prescribed positive pairs.
