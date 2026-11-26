# Three same-integer norms: an exact gate and a Pell synchronization

For nonnegative targets \(N_0,\ldots,N_{r-1}\), let \(D_j\) be the gcd of all products of \(j\) distinct targets, using \(\gcd(0,\ldots,0)=0\). All targets are Gaussian norms if and only if all \(D_j\) are Gaussian norms. For positive targets, the valuation of \(D_j\) at an inert prime is the sum of the \(j\) smallest target valuations, so parity of all these sums is equivalent to parity of the individual valuations. If there are zeros, for \(j\) up to the number of positive targets the zero products are ignored by the gcd; for larger \(j\), the gates are zero. The statement is also valid for Eisenstein norms, with the Eisenstein inert primes. A positive or zero activity test comes first: taking absolute values of negative targets is not an allowed replacement.

For the original chain \(m,5m,25m\), fixed \(c=0\) and \(d,e,f=0,1,2\), put \(A=m-1\). The three residuals are \(A-1,5A-1,25A-1\). There are two separately genuine unbounded double-norm curves:
\[
\begin{aligned}
F(t)&=10t^2+6t+2,&F(t)-1&=(1+3t)^2+t^2,&5F(t)-1&=(3+5t)^2+(5t)^2,\\
G(u)&=250u^2+42u+2,&5G(u)-1&=(3+35u)^2+(5u)^2,&25G(u)-1&=(7+75u)^2+(25u)^2 .
\end{aligned}
\]
They synchronize only at the seed, because \(F(t)=G(u)\) is equivalent to
\[
(250u-50t+6)(250u+50t+36)=216.
\]
Of the signed divisors of 216, only 6 is \(6\bmod50\); the second factor is 36. Therefore \(t=u=0,\ m=3\). Arbitrarily high separate points with a common seed do not suffice for two given curves to synchronize.

However, keeping the second curve and replacing the first by the equation \(x^2=G(u)-1=250u^2+42u+1\) works. It is equivalent to \(X^2-10Y^2=191,\ X=250u+21,\ Y=5x\). The seed \((21,5)\) and a norm-one unit \((19+6\sqrt{10})^{10}\) produce an unbounded integer progression with both coordinate congruences preserved (\(a\equiv1\bmod250,\ 5\mid b\) for the unit \(a+b\sqrt{10}\) and \(50b\equiv0\bmod250\)). The resulting three simultaneous norm coordinates are \((x,0),(3+35u,5u),(7+75u,25u)\) at the shared \(m=G(u)+1\). At any finite set of strictly positive seed rows and primes, preserve exact valuations by taking a further unit power returning to the seed modulo a multiple of all the required prime powers, as usual. The construction does not say newly activated rows are preserved and is not a universal three-target theorem.
