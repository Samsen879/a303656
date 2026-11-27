# K671 fixed-class countercontrol and a conditional angular test

The [existing exact K671 certificate](https://github.com/Samsen879/a303656/commit/d14f31522ea16dccb612fbd8cf46e07170eedb67) supplies one first chord and three second chords at the same target \(n(t)\). Its earlier negative control preserved the three rotations but did not preserve the larger class below. There is a stronger exact negative at the same ordinary height and **in the same larger CRT class**, with a different target integer:

- Keep the same \(H,D,J,E,c,t\) and \(m\in\{7592,7594,7596\}\) as the certificate, and put \(P_0=\operatorname{lcm}(m^2+1)\), \(M=42P_0^2DE\).
- Take \(t'=t+8M\), \(n(t')=J+2((t')^2+c^2)\), \(S'=n(t')-H\), \(R'=S'+2D\). The complete three primitive second chord checks still pass, with three distinct values of \(q\), ordinary height \(2^{671}\le n(t')-J<2^{672}\), and \(25^{128}\le n(t')\le9^{224}\).
- The original and shifted products \(SR,S'R'\) are both coprime to \(M/2\); moreover \(M\not\equiv0\bmod11\). Nevertheless \(R'\equiv99\bmod121\), so \(v_{11}(R')=1\). No first chord at the shifted target can exist in **any** direction by the two-square theorem. This is a countercontrol for using just the fixed CRT class to select a target; it does not say that the shifted target fails other label pairs.

Append the following to the exact replay in the linked certificate:
~~~python
M = 42*lcm(*(m*m+1 for m in ms))**2*D*E
assert t % 42 == 1 and M % 11
S0 = n-H
assert gcd(S0*(S0+2*D), M//2) == 1
nb = second(t+8*M)          # Includes exact height, coordinates, window and primitivity.
Sb, Rb = nb-H, nb-H+2*D
assert 2**K <= Sb < 2**(K+1)
assert gcd(Sb*Rb, M//2) == 1
assert (S0 % 121, (S0+2*D) % 121, Rb % 121) == (42,117,99)
~~~

## What would suffice beyond the CRT step

Use any family preserving the three second chords, the first endpoint hypotheses in the linked Gaussian reconstruction, and \(D/S=o(K^{-3})\). For each height \(K\), let \(\mathcal Z_K\) be **any finite multiset of actual** candidate products \(Z=\overline P Q\) with \(N(Z)=S(S+2D)\) at their respective targets and \(\gcd(S+D-\Re Z,D)=1\). For instance, one could attempt to choose products from simultaneously split-prime residual factors of the two actual endpoint quadratics; this is just one generation method and is unproved for growing height. Set \(A_j=\sum_{Z\in\mathcal Z_K}(Z/|Z|)^j\).

A sufficient, not necessary, estimate is \(A_0>0\) and \(\max_{1\le |j|\le K^3}|A_j|=o(A_0/K^2)\) on an unbounded set of heights. The window for \(q/S\) is the open interval \((1/(64K(K+1)),1/(64K^2))\). Using \(\sqrt{S(S+2D)}=S+D+O(D^2/S)\), the difference between \(q/S\) and \(1-\cos(\arg Z)\) is \(O(D/S)\). The middle third of the displayed window defines a positive angular arc of width \(w\asymp K^{-2}\), safely inside the strict window for large \(K\). A smooth nonnegative bump with support inside that arc and mean \(\asymp w\) has Fourier coefficients bounded by \(O(w(1+w|j|)^{-4})\). Its main term upon summation over \(\mathcal Z_K\) is \(\asymp A_0/K^2\). The sum of absolute Fourier coefficients is \(O(1)\), and the tail beyond \(K^3\) is \(O(K^{-3})\); the stated hypothesis on the low frequencies thus implies positive bump mass. The existing Gaussian reconstruction supplies actual coordinates at a winning target.

Neither the existence of the needed growing multisets nor their frequency cancellation is established. This argument does not prove simultaneous primality, replace an ordinary-height search, or establish growing simultaneous success.
