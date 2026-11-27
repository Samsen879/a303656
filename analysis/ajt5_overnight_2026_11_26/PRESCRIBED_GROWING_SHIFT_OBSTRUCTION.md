# Prescribed targets obstruct a growing coordinate-shift interval

There is **no uniform guarantee of finding a shift \(|\sigma|\le A^{1/4}/1000\)** from a supplied \(S_0\) representation. On the actual balanced mod-\(11\) phase, I obtain cofinally two nearby prescribed targets. At the first, shift \(2\) succeeds and every other shift in that window fails except the sign-equivalent choice. At the second, the entire window fails from its supplied ordinary representation.

### An exact test for a prescribed target

Keep \(W=\sqrt A\), \(S_0=A+25B\), \(S_2=81A+125B\), \(e=20A+25B\), and the ordinary window \(729A+B<K\le729A+625B\). Given \(n=S_0+L^2+t^2\), the other square required after shift \(\sigma\) is
\[
D_\sigma=L^2-4e+2t\sigma-\sigma^2.
\]
For \(|\sigma|\le S\), all these values lie within \(E_0=2|t|S+S^2\) of \(D_0\). If \(|t|\le1100\sqrt W\) and \(S\le\sqrt W/1000\), the interval has length less than \(5W\). Distinct ordinary squares are more than \(44W\) apart, since their roots exceed \(22W\). Thus there is **at most one square \(M^2\) to test**, without enumerating shifts. Once that square is found, test \(n-S_2-M^2\) for squarehood and check whether either signed root is within \(S\) of \(t\). [Prior shifted-edge equation](https://github.com/Samsen879/a303656/commit/00700ed4f949d623ba883e97356bb82e231fdc19)

There is also a uniform bound for arbitrary \(t\) when \(n\le1322A\). For \(S\le A^{1/6}\), at most two signed shifts can give ordinary completions. Three would give a noncollinear lattice triangle on the graph \(M(u)=\sqrt{n-S_2-u^2}\), with \(u=t-\sigma\). On the span of those points, \(M>22W\) and \(|M''|\le1322/(22^3W)\). The triangle determinant is therefore at most \(4\cdot1322 S^3/(22^3W)<1\), although it is a nonzero integer.

### Two actual targets

To obtain an exact positive control with \(t=O(A^{1/4})\), use the shift-\(2\) equation \(rL+t=e+r^2+1\), with \(r\equiv1\bmod11\). Define
\[
r_*=\sqrt{(e+1)/20},\qquad
\psi(r)=\frac{e+1+20r^2-19r}{11r}.
\]
Take \(r_0\) to be the first point of that progression above \(r_*\), and \(J=\lfloor\psi(r_0)\rfloor+1\). Let \(R\) be the larger root of \(20R^2-(11J+19)R+e+1=0\). Choose the first progression point \(r>R\), and put
\[
L=11J-19(r-1),\qquad t=20r^2-(11J+19)r+e+1.
\]
The identity \(\psi(r)-\psi(r_*)=20(r-r_*)^2/(11r)\) puts \(R<r_*+2\sqrt W\), and \(r-R\le11\). Factoring the quadratic at \(R\) then gives \(0<t\le1100\sqrt W\). For \(W\ge10^8\) in the balanced strip, \(1.48W<r<1.51W\), \(30W<L<32W\), and \(M=L-2r>26W\). Both coordinates \(L,t\) are divisible by \(11\).

Set \(n=S_0+L^2+t^2\) and \(n'=S_0+(L+11)^2+t^2\). Both are in the target phase \(36\bmod121\). For \(|\sigma|\le\sqrt W/1000\), the remainder at \(n\) differs from \(M^2\) by less than \(3W\). It is square exactly when \((\sigma-2)(2t-\sigma-2)=0\). In particular, shift \(4\) passes the mod-\(11\) check and fails the exact test at the **same target and first representation**.

At \(n'\), the entire remainder interval moves up by \(22L+121\). The margins to \((M+12)^2\) and \((M+13)^2\) are
\[
48r-2L-23>3W,\qquad 4L-52r+48>3W,
\]
respectively. Thus every remainder in the window lies strictly between those consecutive squares. Both initial heights and all candidate shifted heights in these controls are ordinary.

### Independent replay

```python
from math import isqrt

a, b = 574422, 392104
W, B = 3**(a//2), 5**b
A = W*W
assert a%10 == 2 and b%110 == 64 and 39*A < 40*B and 125*B < 122*A
S0, S2, S3, U = A+25*B, 81*A+125*B, 729*A+B, 729*A+625*B
e = 20*A+25*B

above11 = lambda v: 1+11*((v+10)//11)
r0 = above11(isqrt((e+1)//20))
J = (e+1+20*r0*r0-19*r0)//(11*r0)+1
C = 11*J+19
r = above11((C+isqrt(C*C-80*(e+1)))//40)
L, t = 11*J-19*(r-1), 20*r*r-C*r+e+1
M = L-2*r
n, n1 = S0+L*L+t*t, S0+(L+11)**2+t*t
assert (n%121,n1%121) == (36,36)
assert n-S2 == M*M+(t-2)**2

S = isqrt(W)//1000
E = 2*t*(S+2)+S*S+4
assert 0 < t and 4 <= S and E < 3*W < 2*M-1
D4 = n-S2-(t-4)**2
assert D4%11 == 3 and 0 < abs(D4-M*M) <= E
F = 22*L+121
assert (M+12)**2 < M*M+F-E <= M*M+F+E < (M+13)**2
assert S3 < S0+L*L-E and S0+(L+11)**2+E <= U
```

The counterexamples rule out uniform success for every fixed exponent \(\eta<1/4\) from the supplied representation. They leave larger shift ranges and other first representations open. The second target already has a genuine \(S_0\) witness, so the obstruction concerns transfer to \(S_2\), not representability in the original conjecture.

### Bound details

Along the same unbounded phase-compatible balanced sequence as in the prior note, \(1.489W<r_*<1.491W\) for \(W\ge10^8\). Since \(0<r_0-r_*\le11\), the identity for \(\psi\) gives \(\psi(r_0)-\psi(r_*)<1/100\). At \(r_*+2\sqrt W\) the same difference from \(\psi(r_*)\) is greater than 4. Thus the increasing-side root \(R\) is strictly below this endpoint. The other root is \(r_*^2/R\); from \(0<r-R\le11\),
\[
0<t\le 220(2(R-r_*)+11)<1100\sqrt W.
\]
This proves the stated bounds for \(r\) and then \(L=(e+r^2+1-t)/r\) by the balanced-strip bounds. The initial and shifted reduced heights are of the form \(S_0+L_i^2+2t\sigma-\sigma^2\), where \(L_i\) is \(L\) or \(L+11\). They lie in the ordinary window since \(30W<L<32W\) and \(|2t\sigma-\sigma^2|<3W\). This obstruction tests the supplied representation, not all representations on the first level.
