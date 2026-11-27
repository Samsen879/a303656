# A true odd-valuation blocker outside a positive weighted window panel

There is one actual integer \(n\) for which an active \(9\times9\) translated exponent subwindow has 62 surviving cells and weight \(475/625\) under a fixed ten-prime exact valuation-parity test. Nevertheless all 81 cells fail the true sum-of-two-squares condition at a single omitted prime 59. This finite result concerns the stated translated subwindow, not the whole exponent box or any specified asymptotic window; \(n\) has an explicit representation at the origin.

For \(11\le t\le19,\ 1\le s\le9\), put \(R_{t,s}=n-9^{29t}-25^{29s}\). For the \(n\) below, binomial expansion modulo \(59^2\) gives \(R_{t,s}\equiv-59(41t+s)\). No cell has \(41t+s\equiv0\bmod59\), so each has \(v_{59}=1\). All \(R_{t,s}\) are positive. The two axes each have step-29 orders 3 modulo 7 and 9 modulo 19, and \((t,s)=(13,4)\) has exact \(v_7=v_{19}=2\). Thus this test includes a shared small order factor and nontrivial square-modulus lifting.

A self-contained exact replay:

```python
from itertools import product

a = 2**2048 + 2959652075281432229956307366992653
b = 5186614880710251122967214263896868
n = 2 + a*a + b*b
panel = (3, 7, 11, 19, 23, 31, 43, 47, 79, 223)

def valuation(m, p):
    e = 0
    while m % p == 0:
        m //= p
        e += 1
    return e

for base in (9, 25):
    for p, order in ((7, 3), (19, 9)):
        assert next(j for j in range(1, order+1)
                    if pow(base, 29*j, p) == 1) == order

R = lambda t,s: n - 9**(29*t) - 25**(29*s)
assert valuation(R(13, 4), 7) == valuation(R(13, 4), 19) == 2
passed = []
for t, s in product(range(11, 20), range(1, 10)):
    r = R(t, s)
    assert r > 0 and r % 59**2 == (-59*(41*t+s)) % 59**2
    assert valuation(r, 59) == 1
    if all(valuation(r, p) % 2 == 0 for p in panel):
        passed.append((5-abs(t-15))*(5-abs(s-5)))
assert (len(passed), sum(passed)) == (62, 475)
```

## Exact maximal width at the fixed non-origin cell

For this same \(n\) and blocker 59, fix the anchor \((i,j)=(377,116)\) in ordinary \((9^i,25^j)\) exponents. Take strictly active square windows with independently chosen positive steps on the axes, and require odd \(v_{59}\) at every cell. The largest width is **10**. With both steps fixed at 29 the largest is **9**; if the anchor must be the lower corner with those steps, it is **7**.

For any width at least two on both axes, comparing successive cells on each axis modulo 59 forces both steps to be multiples of 29, since both multiplicative orders are 29. Thus both initial coordinates are also multiples of 29, since the specified anchor is in the window. The proof is a small complete enumeration with no bound on the original steps assumed: for \(n\) above, each coordinate alone must have \(9^{29t}<n\) or \(25^{29s}<n\), giving respectively \(0\le t<45,\ 0\le s<31\). For each positive step and each possible location of the anchor \((13,4)\) inside the window, subtract step times location to get the origin, and check positivity at the upper corner and the exact valuation of every cell. The width-10 witness is \(t=10+3u,\ s=2+2v\) for \(0\le u,v<10\). Exactly 192 width-11 windows are active; none has all valuations odd. Similarly with both scaled steps one, 45 width-nine windows are active (four blocked), and 50 width-ten windows are active (none blocked). For the lower-corner test, widths seven and eight have one active window each, and only width seven is blocked. Any larger active blocked window would contain a smaller one through the same anchor.

More generally, if \(q\) is an odd prime not dividing 15 and both ordinary steps are multiples of the corresponding orders, the divided residual modulo \(q\), starting from an activated corner, is affine in the two step counts. If both coefficients are nonzero, an all-\(v_q=1\) rectangle of side lengths \(M,N\) must have \(M+N\le q\): when an axis covers all classes it hits the excluded line, and otherwise the two residue sets of sizes \(M,N\) cannot avoid translating into each other if their sizes sum to more than \(q\). This last bound concerns valuation exactly one, not all odd valuations; the exact width-10 enumeration above tests all odd valuations.

## Growing active windows with one fixed surviving anchor

For each sufficiently large prime \(q\equiv3\bmod4\), let \(D=(q-1)/2,\ X=2^{q^2-1}\), \(W\) be the largest odd integer at most \(\sqrt{q-1}\), and write \(h=9^{377}+25^{116}\). There exists an actual integer \(n=2+u^2+v^2\in[X,2X)\) with the following properties:

1. At the fixed anchor the residual \(n-h\) is positive and is a unit at every prime \(p\equiv3\bmod4,\ p\le\sqrt{\log n}\). The \(\log\) is natural.
2. Every cell \(0\le i,j<W\) at exponents \((377+Di,116+Dj)\) is strictly active, with residual of exact \(q\)-valuation 1. Here \(q>\sqrt{\log n}\) is outside the observed panel.
3. The origin remains an explicit true norm. The guaranteed window width satisfies \(W/(\log n)^{1/4}\to(\log2)^{-1/4}\).

Indeed, \(9^D,25^D\equiv1\bmod q\). The \(W^2<q\) offsets have at most \(W^2\) divided shifts \((9^{377+Di}+25^{116+Dj}-h)/q\bmod q\), so choose a missing \(k\bmod q\) and set \(n\equiv h+qk\bmod q^2\). For all sufficiently large \(q\), this is a unit target for the norm \(n-2\), since \(q\nmid h-2\). Every nonzero target modulo \(q\) has a two-square representation by the finite-field norm map, and a coordinate with nonzero derivative lifts it modulo \(q^2\). Separately, for every \(p\equiv3\bmod4,\ p\le\sqrt{\log(2X)}\), prescribe \(u,v\equiv0,0\bmod p\) if \(h\not\equiv2\bmod p\), and \(1,0\bmod p\) otherwise. This enforces \(n-h\not\equiv0\bmod p\). These are independent from \(q\) because \(\sqrt{\log(2X)}=q\sqrt{\log2}<q\).

The common coordinate modulus has logarithm \(O(q\log q)\), even counting all integers in the panel as potential primes. Choose \(u\) between \(\sqrt X\) and \(\sqrt X\) plus one modulus, and \(v\) between zero and one modulus. This has \(X\le n<2X\) for sufficiently large \(q\). Since the maximum exponent is \(O(q^{3/2})\), all cells are active. The omitted \(k\) forces their exact valuation 1, whereas the panel at the anchor only sees units. This growing statement concerns one fixed observed survivor, not a positive density of survivors in the full box.

A finite control for this exact version is \(q=167,\ D=83,\ W=11,\ k=11,\ v=0\), and
\[
u=2^{13944}+6532292378186422400920212684040670 .
\]
Direct modular exponentiation verifies the panel (through prime 139), the stated height range, and exact valuation 1 on all 121 cells. This control is independent of the earlier \(q=59\) construction.

## Strengthening: every cell passes the observed panel at cubic-log width

The congruence choices in the previous construction can instead force **all** cells in the growing window to be units at every observed inert prime. Simultaneously the height can be decreased to
\[
 X=2^{4q\lceil\sqrt q\rceil},\qquad X\le n<2X.
\]
Using the same \(D=(q-1)/2\), \(W\) (largest odd integer at most \(\sqrt{q-1}\)), and fixed anchor, we obtain \(W/(\log n)^{1/3}\to(4\log2)^{-1/3}\), for sufficiently large \(q\equiv3\bmod4\). The exact omitted-prime valuation is still one in every cell, and the origin still has a true two-square residual.

Keep the \(q^2\) congruence and omitted phase from above. At every observed \(p\equiv3\bmod4,\ p\le\sqrt{\log(2X)}\), instead prescribe \(u^2+v^2=-2\bmod p\), which has a solution by the surjective finite-field norm map. Now \(n\equiv0\bmod p\). For \(p>5\) the two offsets are nonzero squares, whose sum cannot vanish modulo \(p\) because \(-1\) is nonsquare; at \(p=3\) they are zero and one. Hence each observed valuation is zero in every cell. The observed threshold is \(O(q^{3/4})<q\), and the joint coordinate modulus has logarithm \(O(q^{3/4}\log q)\), so CRT still fits the new height. Strict activity holds since the largest ordinary exponent is bounded by \(q^{3/2}/2+O(1)\), and \(4\log2>(\log25)/2\). The proof does not impose nonzero even valuations at specific observed primes, unlike constructions that also require such lifts.

For an independent exact control at \(q=167\) retain \(D=83,\ W=11,\ k=11\), with \(X=2^{8684}\), and take
\[
 u=2^{4342}+28451650812436210842,\qquad
 v=25480078662247451187,\qquad n=2+u^2+v^2 .
\]
The observed threshold is between 77 and 78; all observed inert primes up to 71 divide \(n\). Direct modular exponentiation at all 121 positive cells gives valuation zero for every observed prime and valuation one at 167. This does not preclude representations outside the chosen window.

## Mixed directions: the shortest-relation scale

Still fix the anchor \((377,116)\), use \(D=(q-1)/2\), and put \(X=2^{q^2-1}\). In the following result a window is the image of an integer parameter square under an integer \(2\times2\) matrix with nonzero determinant; it need not be an axis-parallel square in the exponent plane. Work with the affine first-order lift modulo \(q^2\) as above, and let \(F(t,s)=at+bs\bmod q\) be its linear part. If \(F\ne0\), let \(\lambda\) be the shortest nonzero sup-norm length in \(\{(t,s)\in\mathbb Z^2:F(t,s)=0\}\); then \(\lambda\le\lfloor\sqrt q\rfloor\) by pigeonhole. For all sufficiently large admissible \(q\), the maximal mixed square width, allowing the omitted phase to be chosen and requiring all cells active at a height in \([X,2X)\), has order
\[
 \Theta(q/\sqrt\lambda).
\]
In particular there is an unconditional width \(\Omega(q^{3/4})=\Omega((\log n)^{3/8})\) for this mixed model. If \(F=0\), a nonzero phase gives width \(\Theta(q)\) directly. This is a distinct geometry from the Cartesian cubic-log construction.

For the lower bound choose a shortest relation \(r=(r_1,r_2)\) and \(m=\lceil\sqrt\lambda\rceil\). Construct each row \((u_j,v_j)\) of a matrix \(A\) by taking \(m\le v_j<2m\) with \(v_j\equiv-r_j\bmod m\), then \(u_j=(r_j+(m+1)v_j)/m\). These entries are positive and give \(A(m,-m-1)^T=r\). If the determinant vanishes, add \((m+1,m)\) to a row whose other row has nonzero corresponding \(r_j\); this changes the determinant. In all cases row sums are at most \(8m\). The composed form has coefficients proportional modulo \(q\) to \(m+1,m\), so on a square of width \(W=\lfloor q/(32m)\rfloor\) its image has at most \((2m+1)(W-1)+1<q\) residues. A missing phase is realized by the same square-coordinate CRT: \(n=0\bmod p\) for every observed inert prime, and \(n=h+qk\bmod q^2\) at the blocking prime. The coordinate shifts before multiplying by \(D\) are at most \(q/4\). Hence the ordinary exponents are at most \(q^2/8+377\) and all cells are active at the specified height. Distinct parameter cells give distinct exponent pairs since the determinant is nonzero.

For the upper bound let \(H\) be the largest absolute row sum of the matrix for any such square. Physical activity bounds the coordinate span and gives \(H(W-1)=O(q)\). If the determinant is a multiple of \(q\) then \(H\ge\sqrt q\), already yielding \(W-1=O(\sqrt q)\). Otherwise the kernel lattice for the composed form has shortest length \(\lambda'\ge\lambda/H\). A square of width \(O(q/\lambda')\), with a sufficiently large absolute constant, represents every residue of this form: choose a shortest vector, which is primitive in \(\mathbb Z^2\) since its length is below \(q\); extend it to a lattice basis of determinant \(q\), shortening the second vector by multiples of the first. Its perpendicular component is \(q\) divided by the length of the first and its parallel component can be made at most half that length. A fundamental parallelogram therefore has diameter \(O(q/\lambda')\). Applying this around the center of any such square gives a lattice representative of every coset inside the square. Missing a phase forces \(W-1=O(qH/\lambda)\). Combining the two bounds gives the claimed scale.

An exact control: \(q=167,\ D=83,\ W=15\), matrix with rows \((5,2),(1,2)\), omitted phase \(k=9\), and
\[
u=2^{13944}+5478876004446096141820128341025639,\qquad
v=1621275203427700299744875168658198,\qquad n=2+u^2+v^2 .
\]
The composed lift coefficients are \(114,2\bmod167\), giving 93 values. Direct modular powering certifies all 225 cells positive with exact valuation one at 167 and zero at every observed inert prime (the largest is 139). The origin stays a genuine norm. This is a statement about a square of parameters, not a claim that every exponent pair in the enclosing rectangle fails.

## A single outside prime is sparse in the full ordinary exponent box

Let \(I=1+\lfloor\log_3 n\rfloor,\ J=1+\lfloor\log_5 n\rfloor\), and count ordinary exponents \(0\le c<I,\ 0\le d<J\), including odd exponents and the active boundary. For \(q\nmid15\), let \(r=\operatorname{ord}_q3,\ s=\operatorname{ord}_q5\), and let \(T_q(n)\) count roots of \(3^c+5^d\equiv n\bmod q\) in one full \(r\)-by-\(s\) period. On any subset of the box, the number of positive residuals with odd \(v_q(n-3^c-5^d)\) is at most
\[
 \min\{J\lceil I/r\rceil,\ I\lceil J/s\rceil,\
       T_q(n)\lceil I/r\rceil\lceil J/s\rceil\}.
\]
For fixed \(d\), the equation modulo \(q\) allows at most one residue class of \(c\bmod r\); the symmetric bound and period bound follow the same way. An actual odd valuation must meet that equation. There are at least \((I-1)(J-1)\) positive-residual cells because the corresponding powers are at most \(n/3,n/5\). Finally \(q+1\le3^r\), so \(r\ge\log(q+1)/\log3\). For \(q>\sqrt{\log n}\), all these facts give a uniform \(O_\rho(1/\log\log n)\) upper bound on the odd-valuation fraction in any subset containing at least a fixed fraction \(\rho>0\) of the active box. No such assumption follows merely from calling the subset “the survivors”; the earlier chosen thin grids need not occupy a fixed positive fraction.

For the exact \(q=59\) integer in the first section, the full ordinary active box has 4,562,522 cells. The blocker rejects 79,968 by odd valuation, of which 27 have valuation three. The subbox specified by \(4\cdot3^c,4\cdot5^d\le n\) contains 4,558,176 cells and has the same rejection count. With the observed panel \(p\equiv3\bmod4,\ p\le\sqrt{\log n}\), there are 3,349,436 exact even-valuation survivors, of which 58,669 are rejected at 59. These counts can be reproduced by computing the powers of 3 and 5 below \(n\), using positivity as a monotone end-of-row cutoff, precomputing residues modulo \(p^6\), and using direct integer division if a positive residual is zero modulo \(p^6\). This box-scale result does not bound the effect of an unbounded union of outside primes.
