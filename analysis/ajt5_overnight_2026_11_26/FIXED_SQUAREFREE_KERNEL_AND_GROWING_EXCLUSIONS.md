# Fixed squarefree-kernel separation and small growing exclusions

The exponential separation extends to every **fixed squarefree \(d\)**, including \(d=10\). For actual prime-order pairs, a nonsquare kernel must grow at least as fast as \(6\ell+1\). That bound is sharp. A sieve extends the growing range on a set of primes whose complement has finite reciprocal sum.

### Fixed \(d\), including the rational leading term

Write
\[
H_-(\ell)=\frac{5^\ell-3^\ell}{2},\qquad
H_+(\ell)=\frac{5^\ell+3^\ell}{8}.
\]
For each fixed squarefree \(d\ge1\) and \(\varepsilon>0\), only finitely many odd integers \(\ell\) admit an integer \(N\) with
\[
|dN^2-H_\pm(\ell)|\le 5^{(1/2-\varepsilon)\ell}.
\]
Consequently, for distinct primes \(q_1,q_2\) dividing the same half, if \(R=H_\pm/(q_1q_2)=ds^2\), then for all sufficiently large \(\ell\)
\[
R(q_2-q_1)^2>5^{(1/2-\varepsilon)\ell}.
\]
Indeed, taking \(N=s(q_1+q_2)/2\) gives \(dN^2-H_\pm=R(q_2-q_1)^2/4\).

For the proof, take \(N\ge0\), write \(\ell=2n+1\) and \(H_\pm=A25^n+B9^n\), and set \(\alpha=\sqrt{A/d}\), \(\beta=B/(2d\alpha)\). The hypothesized error gives
\[
N=\alpha5^n+\beta(9/5)^n+O_d(\rho^n),\qquad
\rho=\max(5^{-2\varepsilon},81/125)<1.
\]
Apply the \(p\)-adic Subspace Theorem to \(X=(5^nN,25^n,9^n)\), using the forms \(X_0-\alpha X_1-\beta X_2,X_1,X_2\) at infinity and the coordinate forms at \(3,5\). The product is \(O_d(\rho^n)\), since the factors \(9^n,25^n,5^n\) cancel against the corresponding \(3\)- and \(5\)-adic bounds. Infinitely many solutions would therefore yield a fixed rational relation \(N=P5^n+Q(9/5)^n\) on an infinite subsequence. Comparing the two scales in order gives \(P=\alpha\) and \(Q=\beta\). [Schlickewei’s \(p\)-adic Subspace Theorem](https://doi.org/10.1515/crll.1976.288.86)

For squarefree \(d\), \(\alpha\) is irrational except at \(d=10\). At \(d=10\), the two coefficient pairs \((\alpha,\beta)\) are \((1/2,-3/20)\) and \((1/4,3/40)\). The leading term has \(5\)-adic valuation \(n\) and the second term has valuation \(-n-1\). Their sum has valuation \(-n-1\), contradicting \(N\in\mathbb Z\). The analytic finiteness threshold is ineffective and depends on \(d\).

### What can grow for actual prime-order pairs

For prime \(\ell>5\), every prime factor of either half is \(1\bmod 2\ell\), by the exact order of \(5/3\) or \(-5/3\). For two inert witnesses, \(R\equiv1\bmod3\). Removing the square \(s^2\) preserves both congruences, so
\[
d\equiv1\pmod{6\ell}.
\]
Thus \(d\le6\ell\) forces \(d=1\) for every prime \(\ell\). A fixed \(d>1\) can occur only at bounded \(\ell\), since any prime \(p\mid d\) requires \(2\ell\mid p-1\). In particular \(d=10\) occurs only in the formal approximation problem above.

For any \(\eta>0\), there is an exceptional set \(E_\eta\) of primes with \(\sum_{\ell\in E_\eta}1/\ell<\infty\) such that outside it:

- \(d\le \ell\log\ell/(\log\log\ell)^{1+\eta}\) forces \(d=1\).
- A composite squarefree \(d\) cannot lie below \(\ell^2(\log\ell)^2/(\log\log\ell)^{2+\eta}\).

For the first bound, on \(\ell\in(X,2X]\), sieve \(\ell,2u\ell+1\) and sum over \(u\ll\log X/(\log\log X)^{1+\eta}\). For the second, take two distinct prime divisors of \(d\), sieve \(\ell,2u\ell+1,2v\ell+1\), and sum over \(uv\ll T=(\log X)^2/(\log\log X)^{2+\eta}\). The uniform sieve bounds after summing are \(O(XU/\log^2 X)\) for \(u\le U\) and \(O(XT\log(2T)/\log^3 X)\) for \(uv\le T\). The local corrections have bounded mean in rectangles: they are products of factors \(1+O(1/p)\) at primes dividing \(u,v,u-v\), and their third moments are bounded by convergent divisor-sum Euler products. Dyadic rectangles give the \(\log(2T)\) factor. Both counts are \(O_\eta(X/[\log X(\log\log X)^{1+\eta}])\), giving the claimed reciprocal convergence. [Selberg’s upper sieve](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1950.1/ICM1950.1.ocr.pdf)

These growing ranges work by excluding nonsquare kernels. Separation for pairs with a surviving, varying nonsquare kernel remains unresolved.

### Sharp real control

At \(\ell=23\), the plus half has inert witnesses \(47,228092436443\) and kernel \(139=6\ell+1\). This reaches the first possible nonsquare kernel.

```python
from math import isqrt

ell, p, q, d = 23, 47, 228092436443, 139
H = (5**ell + 3**ell)//8
assert 25**ell - 9**ell == 16*((5**ell - 3**ell)//2)*p*q*d
assert H == p*q*d and d == 6*ell + 1 and p % 3 == q % 3 == 2
assert all(all(r % j for j in range(2, isqrt(r)+1)) for r in (ell,p,q,d))
for r in (p,q,d):
    g = -5*pow(3,-1,r) % r
    assert g != 1 and pow(g,ell,r) == 1
assert d*((p+q)//2)**2 - H == d*((q-p)//2)**2
```

Independent BigInt verified the genuine sharp 139 kernel and exact order 23 for each of its three half factors. The fixed-coefficient theorem includes the rational leading-term case d=10 only in the approximation problem, not among actual prime-order pairs. The growing ranges exclude small nonsquare kernels rather than proving separation uniformly over a surviving varying kernel.
