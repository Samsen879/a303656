# Growing determinants improve the three-label construction

For every \(\epsilon>0\), this gives \(\gg_\epsilon X^{4/11-\epsilon}\) distinct \(n\le X\) with the original three true labels (fixed within each height batch) and successive Gaussian gcd norms \(2,10\). It improves the sparse family count in [the determinant-one construction](INDEPENDENT_SHIFTS_SIGNED_GCD.md), without claiming pointwise coverage.

Retain the directions \(p=(a,b)\equiv(1,1)\) and \(q=(c,d)\equiv(614,615)\bmod M\), \(M=19680\). Set \(\det(p,q)=h\equiv1\bmod M\), with \(h\) squarefree. Write \(f=3^j\), \(j\equiv1\bmod8\), \(A=131220f^2\), \(B=66430f^2\). For \(a\) prime to \(h\), set \(t=c/a\bmod h\); then \(q\equiv tp\bmod h\). The system
\[
 Z\cdot p=A-\|p\|^2/2,\qquad Z\cdot q=B-\|q\|^2
\]
has an integral solution exactly when
\[
 (a^2+b^2)t(t-1/2)\equiv B-At\pmod h .
\]
This is Cramer's rule modulo \(h\), using \(a\) as a unit. The half-norm is integral since \(a,b\) are odd. The same residue checks as in the determinant-one construction now apply: \(h\equiv1\bmod M\) preserves the residues of \(Z\), including computing \(\|p\|^2/2\bmod M\) from the odd coordinates modulo \(M\). Thus \(1+i\) times \(Z,Z+p,Z+2q\) keep the norm increments \(524880f^2,6560f^2\) and the two Gaussian gcd norms.

Fix \(0<\eta<1/4\) and take \(h\in[L^\eta,2L^\eta]\). There are \(\asymp L^\eta\) squarefree choices in the class \(1\bmod M\). For each prime \(\ell\mid h\), omit \(t=0,1/2\) and any root of \(B-At\); the latter is not the zero polynomial modulo \(\ell\), since all prime factors of \(A\) divide \(M\). For each remaining \(t\), the desired nonzero sum of two squares modulo \(\ell\) has \(\ell-\chi_\ell(-1)\) representations, of which at most two have \(a=0\). Thus the local count, multiplied by CRT, gives \(h^2 L^{-o(1)}\) admissible triples \((a,b,t)\bmod h\).

Choose \(a\in[L,2L)\) in each combined class modulo \(Mh\); there are \(\asymp L/h\) choices. For this \(a\), choose \(b,c\in[L,2L)\) in their forced classes modulo \(Mh\), subject to \(bc\equiv-h\bmod a\). The target and step are units modulo \(a\). For the two progression pieces \(I_b,I_c\), their count is
\[
 \frac{\varphi(a)}{a^2}|I_b||I_c|+O(a^{1/2+o(1)}).
\]
For clarity, use the [Weil–Estermann Kloosterman bound](https://www.cambridge.org/core/journals/mathematika/article/abs/on-kloostermans-sum/DED1120FD0994F590EA6E980D07D0F43) after finite Fourier inversion. Both zero frequencies give the main term. For a divisor \(e\mid a\), the sum of the absolute Fourier coefficients on nonzero multiples of \(e\) is \(O((a/e)\log a)\) by the geometric-series bound and invertible step. Bounding \(\sqrt{\gcd(r,s,a)}\) by the sum of \(\sqrt e\) over common divisors gives the error for both nonzero frequencies by summing \(e^{-3/2}\), and for a single zero frequency by summing \(e^{-1/2}\) over divisors and using \(|\widehat I(0)|\le a\). Divisor and logarithm losses are \(a^{o(1)}\). The main term is \(L^{1-o(1)}/h^2\), and beats the error for fixed \(\eta<1/4\).

Each such pair fixes \(d=(h+bc)/a\), which is \(O(L)\) and in the required classes: modulo \(h\) it equals \(bt\), and modulo \(M\) it equals 615. This counts \(L^{2-o(1)}/h\) direction pairs per \(h\), hence \(L^{2-o(1)}\) across the determinant band. Fix \(f\asymp L,\ 5^D\asymp L^{6-2\eta}\) with even \(D\) for the full batch. Then the Cramer solution is \(O(L^3/h)\), so \(n\asymp L^{6-2\eta}\). A fixed \(n\) fixes each of the three norms and hence has only \(n^{o(1)}\) ordered triples of coordinates; those triples recover both directions. This gives \(X^{1/(3-\eta)-o(1)}\) distinct integers. Taking fixed \(\eta\) sufficiently close to \(1/4\) gives the stated bound.

Exact positive and integrality-negative controls:

~~~python
M,h,f = 19680,19681,3**9
c = 614-856*M
def numerators(c):
    d = c+h
    A = 131220*f*f-1
    B = 66430*f*f-c*c-d*d
    return d*A-B,B-c*A
u,v = numerators(c)
assert u%h == v%h == 0 and numerators(c+M)[0]%h
x,y = u//h,v//h
Z = [(x,y),(x+1,y+1),(x+2*c,y+2*(c+h))]
R = [2*(a*a+b*b) for a,b in Z]
n = 3**30+5**20+R[0]
assert n == 7564653112199776123967318007046124
assert all(n == r+3**e+5**20 for r,e in zip(R,(30,26,18)))
~~~
