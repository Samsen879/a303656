# The matched-digit character factors on both sides

In the [literal marked loss problem](https://github.com/Samsen879/a303656/commit/12d66c6b0b5864f86f5ef5141d7556c9c49652e7), put \(m=ts\), \(p=49gm-\kappa\), and keep the sharp target window and all prime tests. For the matched digit \(u_*\bmod49\), let \(p_*=49u_*-\kappa\); both are units at 7. On the parent fibre \(gm=u_*\bmod7\), take characters satisfying \(\theta(1+7b)=e(6b/7)\bmod49\) and \(\xi(1+343b)=e(b/7)\bmod2401\) on the respective order-seven subgroups. Then for any nontrivial \(k_0\bmod7\),
\[
\theta(gm/u_*)^{k_0}=\xi(p/p_*)^\beta,\qquad
\beta=6k_0p_*u_*^{-1}\bmod7.
\]
Writing \(gm-u_*=7b\) gives \(p-p_*=343b\), so both phase exponents are \(6k_0bu_*^{-1}\bmod7\). The right-side character power is independent of the row \(g\).

For \(s=ru\) the left phase factors on \(g,t,r,u\); for \(v=ru\) the right one factors on \(\lambda,r,u\). Any sum over factorizations of a fixed product therefore has the same phase on every retained summand. In particular, take the nonnegative, literal-prime-tested matrix on coordinates \(tr,u\) on the left (with \(\lambda\) summed), or on \(\lambda r,u\) on the right. Its twisted matrix equals the unsigned one multiplied on each side by a diagonal unitary (and possibly a scalar phase). Their singular values are identical. More generally, twisting the separate inputs in an unrestricted multilinear norm is an isometry. There may be arithmetic cancellation for the two specified character vectors, but it does not appear in these unrestricted norms.

There is also a size constraint before keeping the last prime mask. If \(T,R,U\) are the dyadic sizes of \(t,r,u\), then \(TRU\asymp X_g\), and for \(\log_B R<411/832-699/2000\) with fixed slack the reciprocal coordinates \(tr\) and \(u\) are shorter than \(\lambda\) and have no modular collisions within their supports. Nonzero-frequency Parseval then gives exactly the diagonal square sum minus the zero-frequency term. A Cauchy bound from those diagonals has the \(\sqrt{X_g}\) power scale; the principal count has scale \(X_g/\lambda\). Even ignoring the final prime mask, the ratio of these power scales is at least \(B^{11231/104000}\), since \(g>B^{57/250}\) and \(\lambda>B^{411/832}\). This is a limitation of the diagonal Cauchy estimate, not of all methods on the signed sum.

The fibre relation can be checked independently with any 7-adic unit inputs, for example the seven lifts of \(u_*=19\), \(\kappa=24\). This illustrative check is not a prime-overlap witness.
