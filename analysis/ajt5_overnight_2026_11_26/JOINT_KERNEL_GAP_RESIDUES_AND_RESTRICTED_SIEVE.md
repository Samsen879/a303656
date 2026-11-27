# Joint cyclotomic kernel and gap restrictions

**The exact orders give two joint restrictions on the kernel and the gap.** At the first possible nonsquare kernel \(d=6\ell+1\), a congruence rules out the minimum gap in two explicit prime classes. For gaps divisible by many small primes, a sieve excludes nonsquare kernels beyond the previous \(\ell\log\ell\) scale, outside a set of prime exponents with finite reciprocal sum.

### The first kernel forces gap residues

Let \(\ell>5\) be prime, and let \(q_1<q_2\) be distinct inert prime divisors of the same half
\[
H_-=(5^\ell-3^\ell)/2,\qquad H_+=(5^\ell+3^\ell)/8.
\]
Write \(H_\pm=d s^2q_1q_2\) with \(d\) squarefree, and put \(\Delta=q_2-q_1=6\ell j\). The exact orders of \(5/3\) and \(-5/3\) in their respective halves give \(p\equiv1\bmod 2\ell\) for every prime divisor \(p\) of the half. Inertness of the two witnesses gives \(d\equiv1\bmod6\ell\) and \(6\ell\mid\Delta\).

Suppose \(H=H_+\) and \(d=6\ell+1\). This \(d\) must be prime, since two prime factors would give \(d\ge(2\ell+1)^2\). The element \(-5/3\bmod d\) has odd order and is a square. Since \(d\equiv1\bmod3\), quadratic reciprocity then gives \((d/5)=1\), forcing \(\ell\equiv3\bmod5\). Now \(H_+\equiv\ell\bmod8\), and
\[
dH_+\equiv q_1q_2\equiv 1+q_1\Delta\pmod8.
\]
This gives the first two columns below. If \(s^2\equiv1\bmod5\), the two inert witnesses are each \(\pm2\bmod5\). Their product forces \(j\equiv0\bmod5\) for \(\ell\equiv1\bmod4\) and \(j\equiv\pm2\bmod5\) for \(\ell\equiv3\bmod4\), giving the last column.

| \(\ell\bmod40\) | Required \(j\bmod4\) | Smallest \(j>0\) allowed by these congruences when \(s^2\equiv1\bmod5\) |
|---|---:|---:|
| \(3\) | \(0\) | \(8\) |
| \(13,33\) | odd | \(5\) |
| \(23\) | \(2\) | \(2\) |

Thus in the classes \(3,23\bmod40\), the gap \(6\ell\) is impossible even with an arbitrary square factor \(s^2\).

### A growing-kernel exclusion for gaps with many small prime divisors

For every prime \(7\le p<2\ell+1\) dividing \(\Delta\), both witnesses are units and coincide modulo \(p\). The exact factorization therefore forces
\[
\left(\frac{dH_\pm}{p}\right)=1. \tag{1}
\]
There is an absolute \(\kappa>0\) such that, outside a set \(E\) with \(\sum_{\ell\in E}1/\ell<\infty\), **no nonsquare kernel**
\[
1<d\le \ell\log\ell\,
 \exp\!\left(\kappa\frac{\log\log\ell}{\log\log\log\ell}\right)
\]
can occur if \(\Delta\) is divisible by at least three quarters of the primes in \([7,\lfloor(\log\log\ell)/10\rfloor]\).

Here is the count. On \(\ell\in(X,2X]\), put \(Y=\log\log X\), \(z=\lfloor Y/10\rfloor\), and let \(r\) count the panel primes \(7\le p\le z\). In the stated range \(d\) must be prime, so \(d=6k\ell+1\) with \(k\le U\ll\log X\exp(\kappa Y/\log Y)\). Fix a reduced phase of \(\ell\) modulo \(M=\operatorname{lcm}_{7\le p\le z,\ p\ {\rm prime}}(p,p-1)\). This fixes each \(H_\pm\bmod p\). For uniform \(k\) modulo the panel prime product, the tests (1) are independent by CRT, each with probability at most \(1/2\). The panel can gain at most one prime across the dyadic block, so at least \(3r/4-1\) tests must pass. Weighting a pass by \(3\) bounds the fraction of such \(k\) by
\[
3(2/3^{3/4})^r.
\]
The panel product is \(o(U)\) when \(U\) is taken at the stated upper scale, so the same bound up to an absolute constant holds over \(1\le k\le U\).

For each phase and \(k\), the two-form Selberg sieve for \(\ell\) and \(6k\ell+1\) gives \(O(XF(6k)F(M)/(M\log^2 X))\), where \(F(a)=\prod_{p>2,\ p\mid a}(1-2/p)^{-1}\). Uniformity follows from the two distinct roots away from \(6kM\) and \(M=X^{o(1)}\). Expanding over squarefree divisors gives \(\sum_{k\le U}F(6k)^2\ll U\). Cauchy–Schwarz thus retains half the exponential saving when summing the allowed \(k\), and \(F(M)\le z^{O(1)}\). Since \(r\sim Y/(10\log Y)\), a sufficiently small \(\kappa\) gives a dyadic count \(O(Xe^{-cY/\log Y}/\log X)\) for some \(c>0\). Its reciprocal sum converges. [Selberg’s upper sieve](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1950.1/ICM1950.1.ocr.pdf) · [Prime number theorem](https://www.jstor.org/stable/1969455)

### Exact \(25,9\) control

At \(\ell=23\), the genuine plus-half pair \(47,228092436443\) has \(d=139=6\ell+1\) and \(j\equiv2\bmod20\). Its gap passes (1) at \(11\). The same kernel and half forbid any gap divisible by \(7\).

```python
from math import isqrt

ell, p, q, d = 23, 47, 228092436443, 139
H = (5**ell + 3**ell)//8
assert H == p*q*d and d == 6*ell + 1
assert 25**ell - 9**ell == 8*(5**ell - 3**ell)*H
assert all(all(a % b for b in range(2, isqrt(a)+1)) for a in (ell,p,q,d))
assert p % 3 == q % 3 == 2
for a in (p,q,d):
    g = -5*pow(3,-1,a) % a
    assert g != 1 and pow(g,ell,a) == 1
j, rem = divmod(q-p, 6*ell)
assert rem == 0 and j % 20 == 2 and d*H % 8 == 5
assert (q-p) % 11 == 0 and pow(d*H,5,11) == 1
assert (q-p) % 7 != 0 and pow(d*H,3,7) == 6
```

The growing exclusion requires the small-prime divisibility hypothesis on the gap. Exponential separation for unrestricted gaps and varying nonsquare kernels remains unresolved.

Independent BigInt checked all four residue classes and the exact 7- and 11-adic gap restrictions on the genuine exponent-23 pair. The sieve cannot remove its explicit small-prime-rich gap hypothesis; no general exponential separation or density conclusion is asserted.
