# Exact marginal centering in a legal high-band subfamily

This refines the [switched-product upper bound](https://github.com/Samsen879/a303656/commit/0873504a0676531277ed042872eb1635f0bae566) without claiming a signed bound. Work at \(\rho=1/375,\delta=5/32\), retaining the central conditions and further restricting \(B^{87/250}<t\le B^{699/2000}\), \(B^{57/250}<P\le B^{231/1000}\). Put \(a_*=qrh_0P<B^{0.2495}\), \(m=ts\), \(p=49a_*m-\kappa\), and keep the sharp window. On the parent lattice \(m=1\bmod4,\ a_*m=u_0\bmod7\), define \(A_{a_*}(m)\) as the indicator of the prescribed prime pair \(m=ts\); define \(B_{a_*}(m)\) as the indicator that \(p=\lambda v\) with both prime and \(B^{411/832}<\lambda\le2\sqrt B\). The factor \(t\) is smaller than \(s\) and \(\lambda\) is smaller than \(v\) in the sharp window. Thus the indicators have no multiplicity ambiguity.

For every digit \(x\bmod49\) above \(u_0\bmod7\), the \(A\)-marginal fixes \(t\) and counts \(s\) in a single reduced class modulo 196. Its prime main term does not depend on \(x\). The \(B\)-marginal fixes \(\lambda\) instead. If \(m_0\bmod196\) is the sole lattice residue for \(x\), then it counts \(v\) in the reduced class
\[
\lambda v=49a_*m_0-\kappa\pmod{9604a_*}.
\]
The exact window in \(v\) is independent of \(x\), so the main term is again independent of the digit. The fixed-modulus prime number theorem applies to the first marginal; for the second, Bombieri–Vinogradov applies averaged over \(a_*\), since the moduli are \(O(B^{0.2495})\) and \(v\gg B^{1/2}\). Each modulus is used once for fixed \(\lambda\) and digit: the disjoint factor ranges and split support recover \(q,r,P,h_0\) from \(a_*\). The maximum-interval form of the error is sufficient. Summing over \(\lambda\) costs its bounded harmonic weight because the scale for \(v\) is \(B/\lambda\). In either marginal the total absolute error, after summing the legal \(a_*\), is \(O_C(B/\log^C B)\) for any fixed \(C\).

For each \(a_*\), let \(\alpha_{a_*},\beta_{a_*}\) be the respective principal total counts divided by the length of the parent lattice (number of terms, up to the \(O(1)\) endpoint rounding). Let \(\psi\) be any nontrivial character of the seven-element fibre, evaluated at \(a_*m/u_0\bmod49\). The exact parent lattice weight sum is \(O(1)\), by complete seven-term cycles. Expanding and using the marginal estimates gives
\[
\sum_{a_*,m}\psi(m)A_{a_*}(m)B_{a_*}(m)=
\sum_{a_*,m}\psi(m)(A_{a_*}(m)-\alpha_{a_*})(B_{a_*}(m)-\beta_{a_*})+
O_C(B/\log^C B).
\]
Fourier inversion on the fibre relates the six nontrivial centered correlations to all digit deviations from their mean. This removes the two marginal effects but does not estimate the remaining centered overlap.

Inserting the other prime test into either marginal is material. For example imposing \(t\mid m\) in the \(v\)-marginal changes its progression modulus to \(9604a_*t\gg B^{0.576}\), while \(v\ll B^{421/832}\). Ordinary progression estimates for the \(v\)-marginal therefore cannot simply be reused for the overlap. This is a structural limitation of this attempted estimate, not a bound on the overlap itself. No new high-band finite witness or sign assertion is made.
