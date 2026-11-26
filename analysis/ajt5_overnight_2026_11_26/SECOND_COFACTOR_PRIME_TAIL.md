# Prime part of the signed second-cofactor tail

This is a one-sided estimate specifically for prime divisors in the final interval. It leaves the composite tail unresolved.

Use the notation and residue conditions of [the second-cofactor Type II setup](SECOND_COFACTOR_TYPE_II_DIVISORS.md), with the rebalanced spectrum whose four small exponents are \(43/2500\), next two \(14/625\), next two \(1757/10000\), last \(\lambda=107/200\). These exponents sum to one. Let \(H=|\mathcal P|\sum_a1/\varphi(a)\), with \(a\) in the split prime slot of exponent \(\alpha=1/16\). Let the prime tail start at \(X^{\kappa_0}\) for \(\kappa_0=13/28-1/100000\), and end at a constant times \(X^{\kappa_1}\), \(\kappa_1=15/32\), with the original smooth weight bounded between zero and one.

Fix the first-eight product, \(a\), and prime \(j\equiv3\bmod4\). The last prime lies in one primitive class modulo \(M_0aj\), or there is no solution. The interval version of [Montgomery–Vaughan, *The Large Sieve*, Theorem 2](https://personal.science.psu.edu/rcv4/personal/Publications/large_sieve.pdf) applies because the last-prime interval has fixed relative width and \(\lambda-\alpha-\kappa_1=3/800>0\). Normalize by the fixed-progression prime number theorem for the last prime slot. For \(u=\log_X j\) the upper bound, relative to \(|\mathcal P|/(\varphi(a)\varphi(j))\), is \(2\lambda/(\lambda-\alpha-u)+o(1)\), uniformly through the range. Summing over \(j\equiv3\bmod4\) cancels the factor two via the half-density of that progression. Thus the negative contribution from primes alone has magnitude at most \((B+o(1))H\), where
\[
 B=\lambda\int_{\kappa_0}^{\kappa_1}\frac{du}{u(\lambda-\alpha-u)}
 =\frac{\lambda}{\lambda-\alpha}\log\frac{\kappa_1(\lambda-\alpha-\kappa_0)}
 {\kappa_0(\lambda-\alpha-\kappa_1)}
 <0.901 .
\]

For comparison, in the putative full signed decomposition the normalized short main term tends to \(C_E\), where \(E=\operatorname{rad}(M_0 h)\) has support \(2,3,5,7,11,13,41,73,6481\), and
\[
 C_E=\frac\pi4\prod_{q\mid E}(1-\chi_4(q)/q)
 \prod_{q\nmid E}\left(1+\frac{\chi_4(q)}{q(q-1)}\right).
\]
The factors with a minus sign outside \(E\) have \(q\equiv3\bmod4,\ q\ge19\). Dropping positive factors, comparison with the progression \(19+4k\) bounds their total deficits by \(1/342+1/72\). Thus \(C_E>0.91153159\), and the prime part alone leaves a margin greater than \(0.01H\). In deriving this comparison no upper bound has been used on the composite tail. In particular the margin is not a lower bound for the full representation sum.

Exact rational upper and lower checks:

~~~python
from fractions import Fraction as F
from math import prod
E = (2,3,5,7,11,13,41,73,6481)
chi = lambda q: 0 if q%2==0 else (1 if q%4==1 else -1)
arctan_lower = sum((-1)**k*x**(2*k+1)/(2*k+1)
                   for x in (F(1,2), F(1,3)) for k in range(6))
assert arctan_lower > F(157,200)
main = F(157,200)*prod(1-F(chi(q),q) for q in E)*(1-F(1,342)-F(1,72))
lam, a = F(107,200), F(1,16)
lo, hi = F(13,28)-F(1,100000), F(15,32)
r = hi*(lam-a-lo)/(lo*(lam-a-hi))
u = (r-1)/(r+1)
upper = 2*(sum(u**(2*k+1)/(2*k+1) for k in range(12)) + u**25/(25*(1-u*u)))
loss = lam/(lam-a)*upper
assert main > F(911,1000) and loss < F(901,1000)
assert main-loss > F(1,100)
~~~
