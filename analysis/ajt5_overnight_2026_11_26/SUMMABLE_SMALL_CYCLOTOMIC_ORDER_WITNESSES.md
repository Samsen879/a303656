# Summable small witnesses and paired large cyclotomic witnesses

**Minimal forbidden orders with a bounded number of prime factors and a small inert witness have summable reciprocals.** For \(25,9\), the remaining prime-order problem reduces to two separate cyclotomic norm tests. A failed half must contain at least two distinct inert primes to odd valuation. I did not establish summability for the remaining orders or positive density of genuine multipliers.

### A reciprocal bound for small witnesses

Write \(\Omega(d)\) for the number of prime factors counted with multiplicity. Fix \(r\ge1\) and \(\eta>0\). The reciprocal sum converges over odd forbidden orders \(d\) with \(\Omega(d)\le r\) that have an exact odd-valuation witness \(q\) satisfying
\[
\operatorname{ord}_q(25/9)=d,\qquad
q\le \frac{d\log d}{(\log\log d)^{r+\eta}}.
\]
This applies to all such forbidden orders, hence also to the minimal ones. The reciprocal tail above \(X\) is \(O_{r,\eta}((\log\log X)^{-\eta})\).

For \(X<d\le2X\), write \(d=ap\) with \(p\) its largest prime factor. Then \(p\ge X^{1/r}\), \(\Omega(a)\le r-1\), and the witness has the form \(q=2uap+1\). For an even coefficient \(b\), the two-form upper sieve gives, uniformly in \(b\),
\[
\#\{Y<p\le2Y:p,\ bp+1\text{ prime}\}
\ll \frac{Y}{\log^2Y}H(b),\qquad
H(b)=\prod_{\substack{s\mid b\\s>2,\ s\text{ prime}}}\frac{s}{s-2}.
\]
To check uniformity, sieve \(n(bn+1)\) at \(z=Y^{1/10}\). Each prime has two roots unless it divides \(b\), when it has one. The Selberg weights are bounded by one, so the remainder is \(O(z^4)\). The denominator is at least the denominator for \(b=2\) divided by \(H(b)\), by separating the squarefree divisors supported on primes of \(b\). The denominator for \(b=2\) is \(\gg\log^2 z\), as follows from \(\sum_{d\le z,\ 2\nmid d}\mu^2(d)2^{\omega(d)}/d\gg\log^2 z\). The Dirichlet series of the unweighted coefficients \(\mu^2(d)2^{\omega(d)}\mathbf 1_{2\nmid d}\) is \(\zeta(s)^2\) times an Euler product absolutely convergent at \(1\). [Selberg’s sieve method](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1950.1/ICM1950.1.ocr.pdf)

Now \(\sum_{u\le U}H(u)\ll U\) by expanding the product over divisors, and \(\sum_{\Omega(a)\le r-1,\ a\le2X}H(a)/a\ll_r(1+\log\log X)^{r-1}\) by summing over prime factors. Applying the sieve at \(Y=X/a\) therefore bounds the dyadic count by
\[
\ll_{r,\eta} \frac{X}{\log X\,(\log\log X)^{1+\eta}}.
\]
Division by \(X\) and summation over dyadic intervals proves the reciprocal bound. In particular, almost every prime multiplier \(\ell\), relative to the primes, passes every inert prime up to \(\ell\log\ell/(\log\log\ell)^{1+\eta}\).

### The exact remaining cyclotomic problem

For an odd prime \(\ell>3\), put
\[
F_-=\frac{5^\ell-3^\ell}{2},\qquad F_+=\frac{5^\ell+3^\ell}{8}.
\]
These are odd, coprime, and each is \(1\bmod3\). Since \(25^\ell-9^\ell=16F_-F_+\), **\(\ell\) is admissible exactly when both halves are norms**. An odd prime divisor of \(F_-\) has order \(\ell\) for \(5/3\), and one of \(F_+\) has order \(2\ell\). Neither half is divisible by \(\ell\). If a half fails the norm test, its residue \(1\bmod3\) forces at least two odd inert valuations in that same half.

Summability of bad-prime reciprocals is necessary for positive upper density of admissible multipliers, since every multiple of a bad prime is excluded. The sieve bound removes the small-witness part of that necessary test. The remaining prime question is whether there is a summable set of \(\ell\) for which a half has **paired large witnesses**. Even resolving the prime sum would leave composite minimal orders. Prime powers of exponent at least two are summable automatically, but \(119=7\cdot17\) shows that admitting the primes separately does not settle their products.

There is no new unconditional density or phase-density conclusion here. The existing per-height exponent \(1/2\) and uniform constructed exponent \(13/34\) in both odd classes are unchanged.

```python
from math import isqrt

def prime(p):
    return p >= 2 and all(p%i for i in range(2,isqrt(p)+1))

def gap(d,q):
    return (pow(25,d,q)-pow(9,d,q)) % q

assert (5**7-3**7)//2 == 169**2+3*56**2
assert (5**7+3**7)//8 == 74**2+3*39**2
assert 25**17-9**17 == 758993440348**2+3*44742038272**2
assert (5**11+3**11)//8 == 23*266333
assert all(prime(q) and q%3==2 for q in (23,266333))

# 7 and 17 are valid, but their product is a minimal forbidden order.
q = 239
assert prime(q) and q%3==2 and gap(119,q)==0
assert gap(7,q) and gap(17,q) and gap(119,q*q)

# 37 passes the inert panel through 10*37, but fails at 1259.
assert all(gap(37,q) for q in range(75,371,74) if prime(q) and q%3==2)
q = 1259
assert prime(q) and q%3==2 and gap(1,q)
assert gap(37,q*q) == 280*q
```

Independent BigInt replay checked all three seed controls, exact paired inert failure for 11, minimal composite order 119, and a larger witness for 37 beyond its small panel. The sieve only bounds the small-witness range and says nothing by itself about density of genuinely admissible multipliers.
