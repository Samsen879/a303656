# Quadratic lift for two mixed critical edges

This continues the mixed \((1,3)\) edge of the A303656 project. The certificates concern generated targets for [Sun's Conjecture 4.1(i)](https://arxiv.org/pdf/1701.05868#page=24). The finite progression, the cofinal construction, and the obstruction have different quantifiers.

Run from the repository root with Python 3.9 or later and assertions enabled.

~~~sh
python3 -I -B analysis/c3_quadratic_mixed_lift/verify.py
~~~

Expected output

~~~text
finite: 1080 245 3875464
base6: 432 [72, 18, 12, 0]
conjugate: 180 [120, 70, 25, 10, 6, 0]
~~~

## Exact target lift

Set \(A=9^L,\ B=25^L,\ H=3A+25B,\ D=12B-3A,\ E=A+10B,\ h=D-5,\ V=-3+i\). With \(N(z)=z\bar z\), use
\[
 P=h+Vt,\qquad Q_1=P-iV,\qquad Q_2=P-V+iVy,\qquad
 t=\frac{5y^2-hy+5+3h-E}{10}.
\]
Take \(y\equiv0\pmod2\) and \(y\equiv3-Eh^{-1}\pmod5\). Here \(h\) is a unit modulo 5. These conditions give integral \(t\). Direct expansion yields
\[
 N(Q_1)-N(P)=2D,\qquad N(Q_2)-N(P)=-20t+10y^2-2hy+10+6h=2E.
\]
At \(n=N(P)+H\) the labels are \((2L+1,2L+2)\), \((2L+2,2L)\), and \((2L,2L+1)\). The raw displacements from the common anchor are \((1,3)\) and \((3-y,-1-3y)\). Both edges change both exponents.

For all sufficiently large \(L\), choose \(K\) divisible by 4 within a bounded distance of \(90L\). Put \(Y=2^{K/4}\) and \(13Y/16\le y<7Y/8\). There \(t=y^2/2+O(By)\) and \(S=N(P)\sim5y^4/2\) uniformly. This gives \(2^K\le S<2^{K+1}\) and \((25B)^{16}\le n\le A^{32}\). The three true norms along these cofinal generated targets are unconditional. Critical-band seeds additionally require rotations.

A rational-affine second endpoint \(W+Ut\) in the original \(t\) would have \(N(U)=10\), \(U\cdot W=-3h\), \(N(W)=h^2+2E\), so its squared determinant would equal \(\Delta=h^2+20E\). For \(L\ge2\),
\[
 \Delta-(h+8)^2=8B+68A+16>0,\qquad
 (h+9)^2-\Delta=16B-74A-9>0.
\]
This excludes rational-affine endpoints for that third label on the original target polynomial. The quadratic change of parameter supplies an integral endpoint anyway.

## Oriented division and critical certificates

For a primitive Gaussian divisor \(G=u+iv\) of norm \(M>1\) coprime to 10, set \(I=-uv^{-1}\pmod M\). Since \(\gcd(v,M)=1\), evaluation at \(I\) identifies the quotient by \(G\) with \(\mathbb Z/M\). Substitute \(t(y)\) into the coordinates to obtain
\[
\begin{array}{ll}
 G\mid Q_1:&5y^2-hy+5-E-(h+10)I\equiv0\pmod M,\\
 G\mid Q_2:&5y^2+(-h+10I)y-5-E-hI\equiv0\pmod M .
\end{array}
\]
The corresponding discriminants are \(F_1(I)=\Delta-100+20(h+10)I\) and \(F_2=\Delta\). Each quadratic has a root precisely when its discriminant is a square modulo the full \(M\), including prime powers. The checker independently tests these congruences by substituting into the raw coordinates.

For a rotation \(R=(Q_j/Z)\bar Z\), where \(Z=m-ib\), put \(S=N(P)\), \((D_1,D_2)=(D,E)\), \((x,z)=R-P\), and \(q=(x^2+z^2)/2\). Then
\[
 2qS=(D_j-q)^2+(xP_2-zP_1)^2.
\]
Here \(P_1,P_2\) denote coordinates. The anchor coordinates have the same parity. The raw chord coordinates are odd, and conjugating an odd-norm divisor preserves parity. Thus \(q\) is odd and the determinant is \(2w\) for an integer \(w\). A critical certificate also requires \(\gcd(x,z)=1\) and \(64K^2q<S<64K(K+1)q\), where \(K=\lfloor\log_2 S\rfloor\). Expanding the scalar product yields
\[
 \left|q/S-2b^2/N(Z)\right|\le D_j/S+|Q_j-P|/\sqrt S .
\]

### Fixed-exponent verification

At \(L=12,\ K=1080\), the checker uses four stored residues, with two divisors for each edge, to reconstruct the base period \(M_0\) and the first representative in \([13Y/16,7Y/8)\), \(Y=2^{270}\). Its rational inequalities give \(0.49y^2<t<0.51y^2\), \(h<t/100\), and \(2^K\le S<2^{K+1}\) throughout. The uniform physical error is below \(2^{-260}\). Each ideal ratio clears both band endpoints, and the four ratios are separated by more than twice the error bound.

The replay checks actual Gaussian division, true norms, determinant parity, primitivity, and distinct numerical seeds at the first, middle, and last representatives modulo \(T=M_0DE\). For the whole class, \(y\) and \(t\) are fixed modulo \(DE\), and every rotation denominator is coprime to \(DE\). This fixes each chord modulo its gap. An odd prime dividing both chord coordinates would have to divide that gap by \(N(R)-N(P)=2D_j\). The parity and physical bounds hold uniformly, and \(n\) increases strictly with \(y\). There are exactly **3,875,464** targets in this chosen class and interval, with two seeds per edge and four distinct \(q\)'s per target. This is a count of the certified progression.

Reversing any one of the four divisor orientations preserves its norm and fails exact division at the verified representatives. At \(L=6,\ K=593\), the angle of \(6712-i\) passes the ideal angle test. Its norm contains the split prime 197, at which \(\Delta\) is a nonsquare. Since \(10(n-A-5B)=(10t-3h)^2+\Delta\), this prime cannot divide the second endpoint norm anywhere on that first target polynomial.

### Conditional unbounded lifting

Suppose that along an unbounded set of \(L\) there are two whole oriented Gaussian meshes of coprime norms \(M_1,M_2\) coprime to \(10DE\), passing both discriminant tests. Suppose that their logarithmic norm costs are \(O(J^2)\) and their angular gaps are \(\exp(-\Omega(J))\). With \(J\) a sufficiently small constant times \(\sqrt K\), their insertion leaves room in the \(y\)-window, even after including a primitivity period. Indeed, the combined period is at most \(10M_1M_2\operatorname{rad}(DE)\), with \(\log_2(DE)<10L+O(1)\), versus a window of length \(\asymp2^{K/4}\).

For an odd \(p\mid DE\), a fixed rotation \(\kappa\ne1\bmod p\) forbids at most two \(y\)-classes. At least one coordinate of its chord is a nonzero quadratic, with leading Gaussian coefficient \((\kappa-1)V/2\). Here \(p\ne5\). At \(\kappa=1\), the raw chord is nonzero modulo \(p\). At 3 only the first gap is present. At larger primes a pair of rotations forbids at most four residues. Selecting each \(y\)-class by averaging over the surviving pairs therefore keeps a fraction at least \(\tfrac13\prod_{p\mid DE,\ p\ge7}(1-4/p)\gg(1+\omega(DE))^{-4}\). Selecting disjoint angle subintervals and using the uniform physical error \(O(2^{-K/4})\) gives exponentially many distinct numerical seeds per edge, of order \(\exp(\Omega(\sqrt K))\). The supply of compatible meshes is the conditional input.

## New unconditional obstruction for a complete base-6 block

Take \(\pi_j=6^{2j+1}+(-1)^ji\). Consider requiring the raw first endpoint \(Q_1\) to contain an entire set of these axes, at least once per axis, in a uniform orientation. For the block of conjugate factors \(\bar\pi_j\), four primes exclude every \(L\).

| Prime | Axis \(j\) | Period for \(A,B\) | Cumulative surviving classes modulo 432 |
|---:|---:|---:|---:|
|13|1|6|72|
|97|1|48|18|
|73|4|36|12|
|109|13|27|0|

Each row uses \(I=(-1)^j6^{2j+1}\pmod p\), with \(I^2=-1\). A necessary condition for that oriented division is that \(F_1(I)\) be a square or zero modulo \(p\). The checker verifies the primes, their periods and the intersection. Omitting any single row leaves a surviving class in that reduced panel, in row order \(14,63,9,57\bmod432\).

The globally reversed block of factors \(\pi_j\) is also excluded. It uses the opposite sign of \(I\).

| Prime | Axis \(j\) | Period for \(A,B\) | Cumulative surviving classes modulo 180 |
|---:|---:|---:|---:|
|13|1|6|120|
|37|0|18|70|
|73|4|36|25|
|61|7|15|10|
|181|7|45|6|
|241|2|60|0|

The first 14 axes in the first orientation and the first 8 in the second orientation suffice. Each row recurs at \(j+(2j+1)k\) with the same \(I\): increasing the exponent multiplies the power of 6 by \((-1)^k\), and the alternating sign cancels it. Thus any consecutive block of 27 full axes in the first orientation, or 15 in the reversed orientation, fails for every \(L\). Additional factor powers cannot fix a failed congruence modulo \(p\).

The exclusion is specific to preloading complete uniformly oriented base-6 blocks into the stated raw \(Q_1\). Arbitrary subsets, axis-by-axis changes of orientation, and other endpoint representations remain open. Neither this exclusion nor the cofinal three-norm lift settles arbitrary prescribed targets or Sun's conjecture.
