# Elementary short gaps by rounding Gaussian norm coordinates

**Every prescribed class modulo \(Q=27\cdot2^k\) has an actual in-window witness within**
\[
O\!\left(QX^{1/4}+\frac{Q^2}{\sqrt X}\right)
\]
**above any integer \(T\in[X,2X]\).** The constant is absolute, for all sufficiently large \(X\) and all \(k\ge3\). In particular, the gap is \(O(QX^{1/4})\) for \(Q\le X^{3/4}\), or \(O(X^{1/4})\) measured in consecutive members of that class. The construction uses the two actual exponent windows of draft PR #86. It gives a genuine sum of two squares by rounding its coordinates, with no prime-counting input. [Draft PR #86](https://github.com/Samsen879/a303656/pull/86/files)

### The local choice

Use \(X^{1/8}\le3^c\le X^{1/4}\) and \(X^{1/3}\le5^d\le X^{1/2}\), and write \(\lambda=3^c+5^d\). Fix an integer representative \(b\) of the target class and take \(D=1\) for odd \(b\) and \(D=2\) for even \(b\). Choose \(c,d\bmod4\) so that \(b-\lambda\equiv D\bmod 8D\). This is possible because \(3^c+5^d\bmod16\), over these choices, runs through all even classes. Thus \(r=(b-\lambda)/D\) is an odd integer congruent to \(1\bmod8\).

Keep the chosen \(d\bmod4\). If \(5^d\not\equiv b\bmod3\), the residual is a unit modulo \(27\), since \(c\ge3\) for large \(X\). Otherwise refine \(d\) by imposing \(5^d\equiv b-9\bmod27\). The order of \(5\bmod27\) is \(18\), and this extra condition has the required parity, so the two conditions on \(d\) are compatible. The residual then equals \(9\bmod27\). In either case choose \(s,t\bmod27\) with \(s^2+t^2\equiv r\bmod27\). Every unit modulo \(27\) is a norm by lifting a solution modulo \(3\) using a coordinate that is a unit. Every residue \(9\) times a unit is a norm by scaling a solution modulo \(3\) by \(3\).

These are only fixed-period restrictions on the exponents. There are \(\asymp(\log X)^2\) distinct labels in the resulting box, and the argument below applies to **each** of them with the same gap bound. In particular, two genuinely distinct labels can be chosen in advance and both will give witnesses in the same interval and class. Their output integers may differ.

### Why the shorter coordinate step works

Set \(2^j=2^k/D\), and \(U=\lfloor(T-\lambda)/D\rfloor\asymp X\). For \(j\ge7\), choose the largest \(\ell\ge2\) such that
\[
M=2^{2\ell+3}\le 2^j,\qquad 27M\le\sqrt U.
\]
Such an \(\ell\) exists for sufficiently large \(X\). Since \(r-2^{2\ell}\equiv1\bmod8\), choose a root of this value modulo \(M\). Combine that root class with \(x\equiv s\bmod27\), then take the largest nonnegative \(x\) in the combined class with \(x\le\sqrt U\). Its step is \(27M\), so
\[
0\le U-x^2\le 54M\sqrt U.
\]

The imposed congruence makes \((r-x^2)/2^{2\ell}\equiv1\bmod8\). It therefore has a square root \(z\bmod2^{j-2\ell}\). Here the square-root fact follows by induction: for \(m\ge3\), changing an odd root by \(2^{m-1}\) preserves its square modulo \(2^m\) and toggles the next bit. Choose \(y\) in the class
\[
y\equiv 2^\ell z\bmod 2^{j-\ell},\qquad y\equiv t\bmod27,
\]
strictly above \(\sqrt{U-x^2}\) and within one step \(P=27\cdot2^{j-\ell}\) of it. This gives \(x^2+y^2\equiv r\bmod Q/D\). Hence
\[
N=\lambda+D(x^2+y^2)\equiv b\bmod Q,\qquad N>T.
\]
For \(D=1\) the norm coordinates are \(x,y\). For \(D=2\) they are \(|x+y|,|x-y|\).

Rounding \(y\) costs at most \(2P\sqrt{U-x^2}+P^2\) in the normalized norm. The first term is \(O(QX^{1/4})\) because \(P\sqrt M\asymp Q\). Maximality gives \(M\asymp\min(2^j,\sqrt U)\), so the second term is \(O(Q+Q^2/\sqrt X)\). For \(j<7\), \(Q\) is bounded. When \(j<3\), reduce the available congruence \(r\equiv1\bmod8\) to modulus \(2^j\). Use \(x^2\equiv r\bmod2^j\), \(y\equiv0\bmod2^j\), and the same two roundings with bounded steps. This gives \(O(X^{1/4})\) in that case.

The gain comes from trading the two step sizes. Forcing the difference \(r-x^2\) to have valuation \(2\ell\) makes the step for \(x\) of order \(2^{2\ell}\), while the step for \(y\) shrinks to order \(Q/2^\ell\). Capping the first step at the size of \(\sqrt U\) gives the \(Q^2/\sqrt X\) term.

### Exact replay

At \(X=T=10^{12}\), \(Q=27\cdot2^{20}\), and \(b=T\bmod Q\), the label \((c,d)=(4,7)\) gives
\[
N=1\,224\,737\,099\,776
 =1\,082\,497^2+230\,081^2+3^4+5^7.
\]
The actual label \((4,6)\) at the **same** \(N\) leaves a positive residual with \(v_{19}=1\), so that label fails the sum-of-two-squares criterion. This standard-library replay checks the rounding as well as both labels.

```python
from math import isqrt

X = T = 10**12
Q, D, j, ell = 27 * 2**20, 2, 19, 5
M = 2**(2 * ell + 3)
P = 27 * 2**(j - ell)
label = 3**4 + 5**7
U = (T - label) // D
x, y = 656289, 426208

assert 27 * M <= isqrt(U) < 27 * 4 * M
assert x <= isqrt(U) < x + 27 * M
assert (T - label - D * (x*x + y*y)) % Q == 0
assert y - P <= isqrt(U - x*x) < y

N = label + D * (x*x + y*y)
assert N == 1224737099776
assert N - T == 224737099776 and N % Q == T % Q == 7671808
assert N == (x+y)**2 + (x-y)**2 + label
assert 3**16 <= X <= 3**32
assert all(5**(2*d) <= X <= 5**(3*d) for d in (6, 7))

bad = N - 3**4 - 5**6
assert bad > 0 and bad % 19 == 0 and bad % 19**2 == 209
```

This is a gap bound for ordinary witnesses. The construction may place different labels at different integers, so it provides neither a positive-fraction estimate nor the robust matchings of PR #86. In the class of a specified target \(T\), it certifies \(N>T\) with \(N-T\) a multiple of \(Q\). The witness is an exact representation of \(N\), and the representability of \(T\) remains open.

## Synchronizing two fixed mixed labels in a compatible class

**Two actual labels can share a target within \(O(\sqrt{QX}+Q)\) above any prescribed height in an explicit class modulo \(Q=27\cdot2^k\).** Both exponent axes change. The class depends on the chosen pair of labels, which stays fixed throughout the height window. The gap is sublinear when \(Q=o(X)\). An exact control below shows that other classes can contain common targets for the very same labels even when this particular progression misses the entire class. This extends the single-witness construction in a different direction. [Draft PR #89](https://github.com/Samsen879/a303656/pull/89)

### A shared progression for two labels

For all sufficiently large \(X\), choose the least \(c,d\) with \(3^c\ge X^{1/8}\) and \(5^d\ge X^{1/3}\). The labels
\[
L_0=3^c+5^d,\qquad L_1=3^{c+1}+5^{d+1}
\]
both satisfy the original windows \(X^{1/8}\le3^e\le X^{1/4}\) and \(X^{1/3}\le5^f\le X^{1/2}\). In particular \(3^{c+1}\le9X^{1/8}\) and \(5^{d+1}\le25X^{1/3}\).

Put
\[
h=\frac{L_1-L_0-2}{4}=\frac{3^c-1}{2}+5^d,\qquad C=L_1+2h^2.
\]
For every integer \(z\),
\[
\boxed{C+2z^2
=L_1+(h+z)^2+(h-z)^2
=L_0+(h+z+1)^2+(h-z+1)^2.}
\]
Take absolute values for nonnegative norm coordinates. The identity follows because adding \(1\) to both coordinates increases the norm by \(4h+2=L_1-L_0\). Conversely, any common representation with exactly this signed coordinate shift must have the unshifted coordinates sum to \(2h\), so this mechanism gives exactly the progression \(C+2z^2\).

Since \(C=O(X^{2/3})\), its quadratic term can be rounded at ordinary height. For the class \(b=C\bmod Q\), the exact condition is
\[
C+2z^2\equiv C\pmod Q
\quad\Longleftrightarrow\quad
P\mid z,\qquad P=9\cdot2^{\lceil(k-1)/2\rceil}\asymp\sqrt Q .
\]
For any integer \(T\in[X,2X]\), take the first multiple of \(P\) strictly above \(\sqrt{(T-C)/2}\). Its target \(N\) satisfies
\[
0<N-T\le 4P\sqrt{(T-C)/2}+2P^2=O(\sqrt{QX}+Q).
\]
Both residuals are at least \(N/2\) for sufficiently large \(X\). For \(Q=o(X)\), consecutive outputs of this progression at height \(\asymp X\) are separated by \(4Pz+2P^2\asymp\sqrt{QX}\). Thus the gap bound has the correct order for this progression itself.

More generally, the exact compatibility test for a class \(b\bmod Q\) is that \(b-C\) be even and \((b-C)/2\) be a square modulo \(Q/2\). If the test passes, a single root class modulo \(Q/2\) gives a gap \(O(Q\sqrt X+Q^2)\) by the same rounding argument. The smaller step in the class \(C\bmod Q\) comes from the divisibility condition on roots of zero.

### Exact positive and control

At \(X=10^{12}\), take the pair \((4,6),(5,7)\), which is in the stated windows, and \(Q=27\cdot2^{12}\). The class \(C\bmod Q\) is \(55522\). The first output above \(10^{12}\) in that class is \(1\,001\,116\,661\,986\).

There is also a common target \(1\,000\,006\,088\,738\) in class \(47138\bmod Q\), obtained by the signed shift \((1,3)\). The entire class is inaccessible to the \((1,1)\) shift, since \(N-C\equiv1\bmod3\) there and \(2z^2\bmod3\) takes only the values \(0,2\). This isolates the obstruction to the fixed coordinate shift.

```python
from math import isqrt

X = 10**12
Q, P = 27 * 2**12, 9 * 2**6
c, d = 4, 6
L0, L1 = 3**c + 5**d, 3**(c+1) + 5**(d+1)
h = (L1 - L0 - 2) // 4
C = L1 + 2*h*h

for e, f in ((c, d), (c+1, d+1)):
    assert 3**(4*e) <= X <= 3**(8*e)
    assert 5**(2*f) <= X <= 5**(3*f)

z = P * (isqrt((X-C)//2) // P + 1)
N = C + 2*z*z
assert C + 2*(z-P)**2 <= X < N
assert N == 1001116661986 and N % Q == C % Q == 55522
assert N == L1 + (h+z)**2 + (h-z)**2
assert N == L0 + (h+z+1)**2 + (h-z+1)**2

x, y = -945507, 325611
other = L1 + x*x + y*y
assert other == L0 + (x+1)**2 + (y+3)**2 == 1000006088738
assert X < other <= 2*X and other % Q == 47138
assert (other-C) % 3 == 1
```

The result is a gap guarantee in a compatible class for a fixed pair. It certifies two representations of the same output \(N>T\). It does not certify the specified integer \(T\), and the progression alone gives no positive-fraction or robust-matching theorem.
