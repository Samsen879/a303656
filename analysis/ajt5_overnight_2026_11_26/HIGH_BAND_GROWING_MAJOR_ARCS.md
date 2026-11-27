# Growing major arcs for the signed centered high-band overlap

In the [legal high-band centered comparison](https://github.com/Samsen879/a303656/commit/9f4edec3023038301508d4dd494d791b126069a2), write \(g=a_*\) and parametrize the parent lattice by \(m=m_0+28j\) on its exact window, with \(X_g=B/g\). Let \(U_g,V_g\) be the two indicators from that comparison after subtracting their bounded constant marginal centers. The six nontrivial conductor-49 twists restricted to this lattice translate one additive frequency by \(w_g/7\), \(7\nmid w_g\). Indeed \(gm/u_0\) varies linearly in \(j\) within the seven-element fibre over \(1\bmod7\), with nonzero slope. Thus the twisted overlap is the integral of \(\widehat U_g(\alpha+w_g/7)\overline{\widehat V_g(\alpha)}\), up to a phase.

For fixed \(K>0\), put \(H=(\log B)^K\). Include arcs of width \(H/(dX_g)\) about every reduced \(b/d\) with \(d\le B^{1/2000}\), and their translates by \(-w_g/7\). Then the sum over legal rows of the integral of the absolute product on this union is \(O_{D,K}(B/\log^D B)\) for every fixed \(D>0\).

To see the cancellation at \(7\mid d\), partition residues of \(j\bmod d\) into fibres \(j\mapsto j+d/7\). Fix \(t\) in the \(U\)-marginal or \(\lambda\) in the \(V\)-marginal. The moduli for \(s\) and \(v\) are respectively \(28d\) and \(1372gd\); the numerators change by \(4d\) and \(196gd\) before inversion of the fixed prime. The reduced-class test is constant on a fibre, including at 7 where the residues are units. For each prefix of the sharp window the principal term of the prime count is constant there too, and the primitive additive phases cancel. A constant marginal center likewise has no fibre main term. A residue-class endpoint error of \(O(1)\) is enough for the latter.

If the maximum prefix error per class is \(E_{g,d}\), finite Parseval bounds the Euclidean norm over primitive numerators by \(dE_{g,d}\); partial summation at the offset costs \(O(1+H)\). The other transform has norm \(O(X_g)\) over rational numerators, by its bounded coefficients and the lattice residue count. Multiply the two bounds by the arc width \(O(H/(dX_g))\). If \(7\nmid d\), the twist produces a primitive denominator \(7d\) on the first factor instead; apply the same argument there, with constant-factor changes to the widths. The translated family needs at most \(7B^{1/2000}\) in the denominator bound.

For the first progression-error sum apply maximal Bombieri–Vinogradov at the prime scale \(B/(gt)\gg B^{0.4}\), then sum the harmonic weights over \(g,t\). For the second, apply it at \(v\)-scale \(B/\lambda\gg B^{1/2}\) on each dyadic \(\lambda\) block. The exponent margin is
\[
\frac14-\left(\frac5{375}+\frac5{1024}+\frac{231}{1000}\right)-\frac1{2000}
=\frac{109}{384000}>0.
\]
A modulus \(1372gd\) has at most \(\tau(gd)\) preimages. The weighted error sum still saves arbitrary logarithms: Cauchy–Schwarz combines unweighted Bombieri–Vinogradov with the trivial estimate \(E_x(M)\ll x/\phi(M)\) and \(\sum_{M\le x}\tau(M)^2/\phi(M)\ll\log^8 x\). The latter follows from \(M/\phi(M)\le\tau(M)\) and \(\tau^3\le\tau_8\). Summing the dyadic blocks and the \(O(1)\) endpoint contributions preserves the stated savings.

This removes the specified growing union of arcs at the secondary scale. It does not bound the rest of the signed integral, where both frequencies are outside those arcs. No primality check was relaxed for the indicators in this argument.
