# The principal term matches, but the original lifts do not match character by character

This exact identity isolates a limitation of the prime-progression part of the switched-prime calculation. It is not an estimate for the simultaneous-prime correlation or a determination of its sign.

Let \(p=wds-\kappa\), with \(w=1\) on the shallow side and \(w=49\) on the deep side, and count primes \(s\equiv3\bmod4\) weighted by \(\log s\). The original window for \(s\) is \(J\) or \(J/49\), respectively. Fix lifts \(p+\kappa\equiv u\) or \(49j\bmod343\), with \(7\nmid uj d\). Require \(e\mid p\), where \((e,14d\kappa)=1\). With \(\chi=\chi_4\chi_{343}\chi_e\) and \(\Theta_\chi(I)=\sum_{s\in I,\ s\text{ prime}}\chi(s)\log s\), put
\[
b_\chi=\overline{\chi_4(3)\chi_{343}(ud^{-1})\chi_e(\kappa d^{-1})}.
\]
Multiplying the raw depth-two-minus-depth-zero difference by \(\varphi(1372)\) gives
\[
\frac{1}{\varphi(e)}\sum_\chi b_\chi
 \bigl(49 c_\chi\Theta_\chi(J/49)-\Theta_\chi(J)\bigr),
\]
where \(c_\chi=0\) if \(\chi_{343}\) does not factor modulo 7, and otherwise \(c_\chi=\chi_e(49)\overline{\chi_7(j/u)}\), with \(\chi_7\) the induced character. Indeed, the shallow residue for \(s\) is \(ud^{-1}\bmod343\) and \(\kappa d^{-1}\bmod e\); the deep one is \(jd^{-1}\bmod7\) and \(\kappa(49d)^{-1}\bmod e\). Character orthogonality gives the formula since \(\varphi(1372)/\varphi(28)=49\). The counted primes are units in their respective moduli.

For the principal character, the length contribution is exactly \(49|J/49|-|J|=0\). Conductor-49 and conductor-343 characters in the 7-part appear only on the shallow side. For the actual lift pair \(u=264,\ j=1\), the ratio \(j/u\) is \(3\bmod7\), a nonsquare. Thus the quadratic \(\chi_7\), paired with any real \(\chi_e\), has \(c_\chi=-1\) (since 49 is a square). A power term with exponent \(\beta\) would have deep-minus-shallow multiplier \(-49^{1-\beta}-1\), not \(49^{1-\beta}-1\). This is a statement about coefficients and does not assert that any such term occurs. The residue check is \(264\equiv5\bmod7\), \(5\cdot3\equiv1\bmod7\), and the nonzero squares modulo 7 are \(1,2,4\).

In the rough-composite upper band \(P^-(p)>p^{1/3}\), \(p=\lambda v\) has exactly two prime factors counted with multiplicity (when \(p\) is composite). For fixed \(\lambda\) coprime to \(14d\), choose the CRT residue \(s_0\) imposing the required lift, \(s_0\equiv3\bmod4\) and \(\lambda\mid wds_0-\kappa\). With \(M_1=1372\), \(M_{49}=28\), the exact two prime tests are
\[
s=s_0+M_w\lambda t,\qquad
v=(wds_0-\kappa)/\lambda+M_wwd\,t,
\]
with the original interval and \(\lambda\le v<\lambda^2\). The determinant of the slope-and-constant matrix is \(-M_w\kappa\). A progression estimate for \(s\) alone leaves the primality test on \(v\) inside the sum.
