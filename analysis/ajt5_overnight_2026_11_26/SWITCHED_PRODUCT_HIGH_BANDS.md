# Switching \(tP\) gives a long variable beyond \(B/d\)

This extends the [long-variable dyadic estimate](https://github.com/Samsen879/a303656/commit/427f5c6bf3b6f37a5b1c88d1a0249c9c05cc8fb2) to selected bands where that argument loses its long interval. Keep the original central switched rows \(d=qrtPh_0\), with \(q,r\) in the inert bands \(B^\rho\) to \(B^{2\rho}\) and \(B^{2\rho}\) to \(B^{3\rho}\), \(t\) inert from \(B^{1/2-\delta}\) to \(B^{1/2-25\delta/26}\), \(P\) split from \(B^{14\delta/13}\) to \(B^{3\delta/2}\), and \(h_0\le B^{\delta/32}\) split-supported. Here \((\log B)^{-1/2}\le\rho<1/250\) and \(13\rho\le\delta\le5/32\). All original coprimalities and central restrictions remain in the count.

Set \(a_0=qrh_0\), \(z=tP\). In the deep packet \(p=49a_0sz-\kappa=\lambda v\), with actual prime \(s\equiv3\bmod4\). For \(\lambda=P^-(p)\) in \((B^{1/2-\delta/26},2\sqrt B]\), we have \(\lambda>N=B/d\) and \(v\) is prime when \(p\) is composite: \(\lambda^3\gg B\), whereas \(p\asymp B\). Fix \(q,r,h_0,s,\lambda\). The sharp window and exact digit \(a_0sz\equiv x\bmod49\) are retained; the CRT with \(z\equiv3\bmod4\) and \(\lambda\mid49a_0sz-\kappa\) gives a progression \(z=z_0+196\lambda j\). Noncontributing rows with incompatible congruences can be omitted. The switched product is injective in its original factorizations, since its inert factor and split factor are distinguishable.

Indeed \(B^{1/2+\delta/13}<z\le B^{1/2+7\delta/13}\). In the variable \(X=p+\kappa\), the window has \(29B<X_-<X_+<32B\) for sufficiently large \(B\), and \(X_+-X_-=(748B-728A)/45>(52/1755)B\). Whenever the progression contains a legal point, \(49a_0s<32B/B^{1/2+\delta/13}\). Its full \(j\)-interval therefore has length \(\gg B/(a_0s\lambda)\gg B^{\delta/13}\). Sieve the two linear forms \(z,v\) up to \(B^{\delta/2000}\). The legal \(tP\) survives this relaxation, and \(v\) is still sifted. As in the [preceding dimension-two bound](https://github.com/Samsen879/a303656/commit/427f5c6bf3b6f37a5b1c88d1a0249c9c05cc8fb2), counting CRT roots for integer \(j\) gives
\[
\ll \frac{BF(a_0s\lambda\kappa)}{a_0s\lambda(\delta\log B)^2},
\quad F(m)=\prod_{\ell\mid m,\ \ell>2}(\ell-1)/(\ell-2)
\]
over prime factors. Outside the finitely many fixed factors 2 and 7, collisions or nonunit slopes occur only at primes dividing \(a_0s\lambda\kappa\). The level of the upper sieve is a fixed small power of the long interval. It does not require a prime progression theorem at modulus \(\lambda\).

For each \(a_0\), the prime \(s\) lies between \(29B^{1/2-7\delta/13}/(49a_0)\) and \(32B^{1/2-\delta/13}/(49a_0)\); the lower endpoint has logarithm at least \(0.35\log B\). Prime harmonic summation thus contributes \(O(\delta)\), and \(q,r\) have bounded harmonic sums. For the \(h_0\)-sum the local identity \(1+F(\ell)/(\ell-1)=F(\ell)\) gives the Euler-product upper bound \(O(\sqrt{\delta\log B})\) after multiplying by the split part of \(F(\kappa)\): excluded split factors of \(\kappa\) below the cutoff cancel, and their tail is negligible by \(\log\kappa=O(\log B)\). Let \(W(\mathcal J)=\sum_{\lambda\in\mathcal J}1/\lambda\) over any prime subset of the high range. Summing yields the absolute normalized bound
\[
|E_\ell(\mathcal J)|\ll \delta^{-1/2}M_\ell W(\mathcal J),\qquad
M_\ell=BF_I(\kappa)/(\log B)^{3/2},
\]
where \(F_I\) is the inert part of \(F\). Every exact mod-49 digit is bounded this way, so any of the fixed bounded correction weights are allowed.

Compared with the central-family rough secondary order \(\delta^{3/2}M_\ell L/(\log B\log L)\), \(L=\log\log B\), a block of \(J+1\) dyadic bands below \(2\sqrt B\) costs \(O((J+1)\log L/(\delta^2L))\) in relative size, as long as \(J\log2\le(\delta/26)\log B\). In particular a growing block may be taken when \(\delta^2L/\log L\to\infty\). This is an absolute bound in that regime, not a signed estimate for the full tail. The product switch is not a construction of legal points in this new band. No such finite witness is asserted here.
