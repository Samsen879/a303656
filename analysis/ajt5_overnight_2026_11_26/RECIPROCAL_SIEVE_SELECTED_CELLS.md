# Reciprocal completion for selected true-prime cells

In the [centered legal high-band setup](https://github.com/Samsen879/a303656/commit/9f4edec3023038301508d4dd494d791b126069a2), put \(C=49g,\ X_g=B/g\). Retain the exact window and matched digit, and write \(Cts-\lambda v=\kappa\) with all four factors prime. In one dyadic bin for \(t\) and one for \(\lambda\), the true count per row and digit is
\[
\ll X_g F(g\kappa)/(\log B)^4,\qquad
F(n)=\prod_{\ell>2,\ \ell\mid n}(\ell-1)/(\ell-2).
\]

Fix \(\lambda\) prime and write \(x=t,y=s\). Both variables are smaller than \(\lambda\) in the stated central bands. There are no contributing pairs if \(\lambda\mid\kappa\); otherwise the exact congruence is \(xy=\kappa C^{-1}\bmod\lambda\). For squarefree \(d\) coprime to \(14\lambda\), count hyperbola points in the sharp window, with the exact digit and \(x,y=3\bmod4\), for which \(d\mid xyv\). The local sieve density satisfies \(\ell^2\rho(\ell)=3\ell-2\) away from \(C\kappa\) and \(2\ell-1\) on its prime divisors: the zero-product condition gives \(2\ell-1\), and otherwise \(Cxy=\kappa\bmod\ell\) adds \(\ell-1\) disjoint pairs. At 196, there are 42 residue pairs per digit.

The sharp hyperbola region of area \(\mathcal A\) can be bracketed by at most \(O(J)\) rectangles with total area discrepancy \(O(X_g/J)\). For each residue pair modulo \(196d\), complete the reciprocal congruence modulo \(\lambda\). The ordinary Kloosterman square-root bound gives error \(O(\sqrt\lambda\log^2 B)\) per rectangle and residue pair. With the local counts this gives the main term \(42\mathcal A\,\rho(d)/(196^2\lambda)\), independent of the matched digit, and error
\[
O\left(X_g\rho(d)/(\lambda J)+Jd^2\sqrt\lambda\log^2B\right).
\]
The term \(1/\lambda\) in the main coefficient absorbs the difference from \((\lambda-1)/\lambda^2\) in the error. As all side lengths are \(O(\lambda)\), completion has the usual interval logarithms.

Take \(z=B^{1/20000}\), \(J=\lceil z\rceil\), and the Selberg upper square weight on \(xyv\) at divisor cutoff \(z\), with squarefree \(d\) and \(\omega_1=1\). The minimizing coefficients have absolute value at most one. Its main quadratic form is \(1/G(z)\), \(G(z)=\sum_{d\le z}\prod_{\ell\mid d}\rho(\ell)/(1-\rho(\ell))\) over squarefree allowed \(d\). A truncated Euler product to \(z^b\) for sufficiently small fixed \(b\), with the expected \(\log d\) below \((\log z)/2\), gives \(G(z)\gg (\log B)^3/F(g\kappa)\). Indeed the generic local factor is \(((1-1/\ell)(1-2/\ell))^{-1}\) and is reduced by \((\ell-2)/(\ell-1)\) on the exceptional primes. In the expanded square the lcm is at most \(z^2\), with multiplicity bounded by \(3^{\omega(d)}\). The completion error is \(O(Jz^6\sqrt\lambda\log^{O(1)}B)\); the strip error is \(O(X_g\log^{O(1)}B/(\lambda J))\). Both save a power compared with \(X_g/\lambda\), since \(X_g/\lambda^{3/2}\gg B^{301/384000}\). Every true prime triple has weight one. Finally \(\sum_{\lambda\text{ in one dyadic prime bin}}1/\lambda=O(1/\log B)\), giving the claimed estimate.

For at most \(M\) selected cells per row, subtract the two marginal terms and the [already-controlled arc regions](https://github.com/Samsen879/a303656/commit/63f86d5978b240552b69766e33104ee195f6add9) from the whole-circle signed overlap. Their proofs persist for the separate bin restrictions, summing at most quadratically many logarithmic errors. The sum of absolute signed integrals on the remaining large region over the selected rows and cells is therefore \(O(MB\mathcal H/\log^4B)+O_D(B/\log^DB)\), with \(\mathcal H=\sum_gF(g\kappa)/g\). For \(M=O(\log B)\) this is smaller than the stated secondary scale. It does not control all cells or their fraction of the true prime-pair mass.

The signed difference of the **sieve weight** itself saves a power even across all cells, by the common digit main coefficient and the completion errors. Transferring it to actual four-prime counts still requires a signed loss estimate for the weight minus the literal triple-prime indicator (with \(\lambda\) still prime); no such transfer is established here.
