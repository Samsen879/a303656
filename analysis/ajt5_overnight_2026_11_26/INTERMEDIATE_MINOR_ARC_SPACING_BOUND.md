# Spacing bound for intermediate and common-divisor minor arcs

Keep the two actual centered prime-tested indicators and exact windows from the [growing major-arc comparison](https://github.com/Samsen879/a303656/commit/736342e85f0c23abf95d7a27689fcf656b4244d1). Write \(X_g=B/g,\ H=(\log B)^K,\ Q_0=B^{1/2000},\ Y_g=\lceil X_g/H\rceil\). Around a reduced fraction \(b/d\) use the radius \(1/(dY_g)\). For \(R,h\ge1\) let \(\mathcal N_g(R,h)\) consist of the arcs with \(Q_0<d\le Y_g\) and either \(d\le Y_g/R\) or \(h\mid d\), together with their translates by \(-w_g/7\). Then
\[
\int_{\mathcal N_g(R,h)}
|\widehat u_g(\alpha+w_g/7)\widehat v_g(\alpha)|\,d\alpha
\ll \left(\frac H{Q_0}+\frac1R+\frac1h\right)\|u_g\|_2\|v_g\|_2.
\]

For a dyadic block \(Q\le d<2Q\) with \(h\mid d\), distinct reduced fractions are separated on the circle by at least \(h/(4Q^2)\), because the nonzero cross numerator is a multiple of \(h\). For each common real displacement, the additive large sieve on the row interval bounds each squared sum of Fourier values by \(O((X_g+Q^2/h)\|u_g\|_2^2)\) or the analogous \(v_g\)-bound. Translating a sampling set by \(w_g/7\) preserves all spacing. Cauchy–Schwarz and the width \(2/(QY_g)\) then give \(O((X_g/(QY_g)+Q/(hY_g))\|u_g\|_2\|v_g\|_2)\). Sum geometrically with \(h=1\) up to \(Y_g/R\), and with the required divisor \(h\) up to \(Y_g\). The translated arcs satisfy exactly the same estimate.

Taking \(R=B^{1/4000}\) and \(h\) the least power of 7 exceeding \(R\) yields \(O_K(B^{1-1/4000}\log B)\) after summing legal rows, using bounded centered indicators and \(\sum_g X_g\ll B\log B\). No prime test or shift has changed. This is below the secondary scale when the legal row harmonic factor is bounded below by an inverse power of \(\log B\).

The combined arc region has only \(O(HQ_0/X_g+1/R+1/h)\) measure per row. Its complement, where neither translated frequency has a small or qualifying common-divisor approximant, is still the main unresolved region. Applying Dirichlet to \(h\alpha\) to force denominator divisibility enlarges the resulting radius by a factor of \(h\), cancelling the putative spacing benefit. Thus this bound extends the justified region but supplies no conclusion about the full signed overlap.
