# Full nonblocked signed comparison with representation weights

**The full nonblocked grid has a positive signed comparison for actual representation counts.** The 98 unit phases have equal leading terms in the two target classes. In each of the seven remaining nonblocked phases, the \(r_-\) leading term is exactly \(7/8\) of the \(r=0\) term. The total excess over the entire nonblocked grid is \(\gg B(\log B)^2\) in the sharp ordinary window. This counts pairs of square representations. The sign for distinct true pairs remains open.

## The comparison

Use even \(a,b\), \(A=3^a,\ B=5^b\), and \(39/40<B/A<122/125\). Set
\[
S_0=A+25B,\quad S=3^c+5^e,\quad \kappa=(S_0-S)/45,\quad
r_-=3^{a+4}+5^{b+2}+7\pmod{49}.
\]
Use the original compatible labels
\[
a/10\le c\le a/3,\quad b/5\le e\le b/3,\qquad
c\equiv a\pmod4,\quad e\equiv b+2\pmod6.
\]
Write \(n=S_0+45u\) and let \((L,U]\) be the interval for \(u\) induced by \(1457A-123B<n\le729A+625B\). Then \(U-L\asymp B\), \(\kappa\asymp B\), and \(8\mid\kappa\). For \(r_2(t)=\#\{(x,y)\in\mathbb Z^2:x^2+y^2=t\}\), define
\[
R_r(c,e)=\sum_{\substack{L<u\le U\\S_0+45u\equiv r\ (49)}}r_2(u)r_2(u+\kappa).
\]
There is an absolute \(\gamma>0\) such that, uniformly over the labels,
\[
R_r(c,e)=\pi^2(U-L)\,C(\kappa)\,\beta_7(r;c,e)+O(B^{1-\gamma}).
\]
Here \(C(\kappa)\gg1\) is common to the two target classes. The 7-adic factors are
\[
\beta_7(0;c,e)=\frac{56^2}{7^6},\qquad
\frac{\beta_7(r_-;c,e)}{\beta_7(0;c,e)}=
\begin{cases}
1 & r_--S\not\equiv0\pmod7,\\
0 & 7\mid r_--S,\quad49\nmid r_--S,\\
7/8 & r_-\equiv S\pmod{49}.
\end{cases}
\]

At \(r=0\), both norms have unit residues at 7. At \(r_-\), the anchor is also a unit since \(r_--S_0\equiv3\cdot3^a\pmod7\). Modulo 49 a unit has 56 norm representations, a residue of depth one has none, and zero has 49. The anchor unit makes the four-variable difference equation nonsingular at 7, so each solution mod 49 has exactly \(7^3\) lifts per further level. This gives the density and the exact ratio \(49/56\), including all higher depths in the zero class.

There are 21 compatible \(c\)-phases modulo 84 and seven compatible \(e\)-phases modulo 42. Since \(5^e\equiv25B\pmod7\), the required residue for \(3^c\) is \(3^{a+4}\pmod7\). For each \(e\)-phase, seven \(c\)-phases meet this congruence, and \(3^{12}\) has order seven modulo 49. Exactly one of those seven reaches zero modulo 49. Thus the grid has 98 unit, 42 blocked, and seven zero-mod-49 phases. The seven zero phases contain \(\asymp(\log B)^2\) actual labels. Each contributes a main-term excess \(\gg B\). The combined error from **all 105 nonblocked phases** is \(O(B^{1-\gamma}(\log B)^2)\). Adding the 42 blocked phases only increases the leading excess.

## Uniformity at the fixed congruence

The required estimate is a fixed-congruence version of the nonzero-level quadratic-form count. The modulus matters here, so apply the following reduction rather than applying an unrestricted shifted-correlation asymptotic.

Transform the two Gaussian coordinate pairs \(z_1,z_2\) to \(z_2-z_1,z_2+z_1\). The difference of norms becomes the split bilinear form \(D(x)=x_1x_3+x_2x_4\). The parity and target conditions become a union of coordinate classes \(x\equiv b\pmod{M}\) with fixed \(M=98\). Put \(P=\sqrt B\) and \(e_q(t)=e^{2\pi i t/q}\). In the delta expansion and Poisson summation, the complete sum for one such class at frequency \(d\) is
\[
S_{q,b}(d)=
\sum_{\substack{x\bmod Mq\\x\equiv b\ (M)}} e_{Mq}(d\cdot x)
\sum_{a\bmod q}^{*} e_q(a(D(x)-\kappa)).
\]
Fourier expansion of the class modulo \(M\) expresses it as a sum over \(\ell\bmod M\) with \(M\mid d+q\ell\). Each term is a unit phase times
\[
q^2\,\mathrm{Kl}\!\left(-\kappa,-D((d+q\ell)/M);q\right).
\]
The bilinear Gauss sum gives this identity at every \(q\), including powers of 2 and 7. Weil therefore gives
\[
|S_{q,b}(d)|\ll_{M,\epsilon}q^{5/2+\epsilon}(q,\kappa)^{1/2}.
\]

For a smooth weight \(W(x/P)\) of fixed compact support away from the origin, the delta integrals for \(q\ll P\) satisfy
\[
I_q(d)\ll P^4\|W\|_{C^K}\frac qP(1+|d|)^{-6}\quad(d\ne0),
\qquad
I_q(0)=P^4\left(\mathfrak I+O\bigl(\|W\|_{C^K}(q/P)^2\bigr)\right)
\]
for an absolute finite \(K\). One way to track the derivative loss is to Fourier-expand the delta kernel after a fixed cutoff in its second variable. Its transform is \(O_N((1+(q/P)|t|)^{-N})\). For the quadratic oscillatory integral, repeated integration by parts applies when \(|t|\) is small relative to \(P|d|/(Mq)\). In the complementary range the nondegenerate quadratic Fourier transform gives \(O((1+|t|)^{-2}\|W\|_{C^K})\), uniformly in the linear frequency. The zero-frequency estimate follows by pushing the weight forward under \(D\) and applying the kernel’s approximate-identity estimate. [Heath-Brown, delta identity and kernel estimates](https://ora.ox.ac.uk/objects/uuid%3Abbd3c62f-f010-44b5-8be5-87e903fb0084/files/m7ec02df6e1b8303a66e7a6015ecb6044)

With the Poisson prefactor \(P^{-2}(Mq)^{-4}\), summing the nonzero frequencies and extending the zero-frequency series both cost \(O_{M,\epsilon}(\|W\|_{C^K}B^{3/4+\epsilon})\). For example,
\(\sum_{q\ll P}q^{-1/2+\epsilon}(q,\kappa)^{1/2}\ll P^{1/2+\epsilon}\tau(\kappa)\) by expanding over divisors of \(\kappa\). At zero frequency, CRT and character orthogonality identify the series with the product of densities in the imposed classes. The real Jacobian \(4\) of the change of variables cancels its factor \(1/4\) at 2.

At odd primes \(q\ne7\), the density is
\[
(1-q^{-2})\sum_{j=0}^{v_q(\kappa)}q^{-j}.
\]
This follows by conditioning on the common \(q\)-depth of the first two bilinear coordinates. The 2-adic density is bounded above and below by absolute positive constants for \(8\mid\kappa\). For the lower bound, take both norm values \(1\bmod8\), choose each second coordinate divisible by 4, and solve for the odd first coordinate. Thus \(C(\kappa)\gg1\) and \(C(\kappa)\ll_\epsilon B^\epsilon\). In the original coordinates, polar integration gives the real factor \(\pi^2\) times interval length. Smooth majorants and minorants with transition width \(B^{-\tau}\) on the scaled interval have \(C^K\)-norm \(O(B^{K\tau})\). Taking \(\tau>0\) sufficiently small gives the stated power-saving error for the **sharp** window.

## Exact \(3,5\) controls

The first three checks use the narrow balanced grid. The integer targets at the end use a smaller pair outside the narrow strip and satisfy the exact ordinary-window inequalities. They show a true depth-two alternative, a true unit alternative at the same target where the deep label has odd depth three, and a true unit alternative in the \(r=0\) class.

```python
from collections import Counter

def grid(a, b):
    A, B = 3**a, 5**b
    r = (pow(3, a+4, 49) + pow(5, b+2, 49) + 7) % 49
    return A, B, A+25*B, r

R = Counter((x*x+y*y) % 49 for x in range(49) for y in range(49))
A, B, S0, r = grid(712, 486)
assert 39*A < 40*B and 125*B < 122*A
inv = pow(45, -1, 49)
for c, e, expected in [(72,98,56**2), (80,98,0), (80,122,56*49)]:
    assert 712 <= 10*c and 3*c <= 712
    assert 486 <= 5*e and 3*e <= 486
    assert (c-712)%4 == (e-488)%6 == 0
    S = 3**c + 5**e
    for rr, w in [(0,56**2), (r,expected)]:
        assert R[(rr-S0)*inv % 49] * R[(rr-S)*inv % 49] == w

A, B, S0, r = grid(52, 36)
Sd, Su = 3**8+5**8, 3**12+5**8
for x, S, k, y, z, rr in [
    (12696151464813, Sd, 7, 1859399199884, 13802633711, r),
    (12696151566639, Su, 1, 11772173149780, 5553033484619, r),
    (12696151452849, Su, 1, 12797700112021, 2374681137140, 0),
]:
    n = S0 + 45*x*x
    assert 1457*A-123*B < n <= 729*A+625*B and n%49 == rr
    assert n-S == 45*k*k*(y*y+z*z)
    if S == Sd:
        assert (n-Sd)%343 == 49
    if x == 12696151566639:
        assert (n-Sd)%2401 == 343
```

The comparison uses the coarse class \(n\equiv S_0\pmod{45}\) and the full representation weights \(r_2(u)r_2(u+\kappa)\). It requires no prime marking. Passing to distinct true pairs would require control of the reciprocal representation multiplicities in the two classes.
