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
