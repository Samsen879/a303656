# Growing exponent rectangles have a true-norm lower first moment

**The missing first moment holds on an explicit growing 3,5 rectangle.** For all sufficiently large \(X\) and every integer \(1\le H\le(\log X)/100\), take
\[
(c,d)=(4H+3+4i,\ 1+2j),\qquad 0\le i,j<H.
\]
Among primes \(X/2<p\le X\), \(p\equiv1\pmod{12}\), this menu gives
\[
\gg \frac{XH^2}{(\log X)^{3/2}}
\]
incidences of **positive true two-square remainders** at \(n=5p+52\). The constant is independent of \(X,H\). In fact, the counted remainders have no inert prime divisor. Combined with the verified overlap bound, the result gives a positive relative proportion with a second witness already at area \(H^2\asymp\sqrt{\log X}\). At \(H=\lfloor(\log X)/100\rfloor\), a positive relative proportion have \(\gg\sqrt{\log X}\) additional witnesses with pairwise distinct \(c\)- and \(d\)-labels. [Verified overlap bound](https://github.com/Samsen879/a303656/commit/8074e7521723ac324f1226656a6fd4e3fc3a59f9)

### Uniform lower sieve and the large-prime subtraction

Put \(A=(3^c+5^d-52)/5\) and \(m=p-A\). The menu gives \(A\equiv8\pmod{12}\), so \(m\equiv1\pmod4\) and \(3\nmid m\). Uniformly over the menu, \(0<A<X/4\) and \(4\max(3^c,5^d)\le5p+52\) for large \(X\). The offsets are distinct because the gaps between successive \(3^c\) exceed the entire \(5^d\) span. The actual remainder is \(5m\).

Fix a small absolute \(\varepsilon>0\), write \(s=1+\varepsilon\), and take \(z=X^{1/(2s)}\). Let \(S_A(z)\) count the indicated primes for which no inert prime below \(z\) divides \(m\). For squarefree sieve moduli \(r\) supported on inert primes \(q\ge7\) with \(q\nmid A\), the conditions \(p\equiv A\pmod r\) and \(p\equiv1\pmod{12}\) give one reduced class modulo \(12r\). Bombieri–Vinogradov supplies level \(D=X^{1/2}/(12(\log X)^B)\), with total error \(O(X/(\log X)^3)\) for sufficiently large \(B\), uniformly in \(A\) by its maximum over reduced classes. Primes dividing \(A\) cannot divide \(m\), since \(p>A\).

The half-dimensional sieve has local density \(g(q)=1/(q-1)\) at the included primes. Its product-ratio hypothesis is uniform: omitting primes dividing \(A\) can only decrease \(V(w)/V(z)\) from the full inert-prime product. Also \(V(z)\gg(\log X)^{-1/2}\). Since \(\log D/\log z\to s\) and the lower sieve function satisfies \(f_{1/2}(1+t)\asymp\sqrt t\) near \(t=0\), the lower bound is
\[
S_A(z)\ge c_0\sqrt{\varepsilon}\,\frac{X}{(\log X)^{3/2}}
\]
for an absolute \(c_0>0\) and all sufficiently large \(X\) after \(\varepsilon\) is fixed. [Half-dimensional sieve, Theorem 2.1 and the expansion at the sifting limit](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

A survivor containing any inert prime has exactly two inert factors, counted with multiplicity. Their number is even because \(m\equiv1\pmod4\), and \(z^3>X\). Thus \(m=kq_1q_2\), with \(z\le q_1\le q_2\), \(k\le V=X/z^2\), and every prime factor of \(k\) split. Write \(W(a)=a/\varphi(a)\). For fixed \(k,q_1\), the two forms \(t\) and \(kq_1t+A\) must both be prime. The uniform Selberg upper bound on \(t\le L=X/(kq_1)\) is
\[
\ll \frac{L}{(\log X)^2}W(A)W(k)W(q_1).
\]
Indeed, \(\log L\gg\log X\), and \((kq_1,A)>1\) gives no solutions with \(p>A\). Otherwise the forms exclude two classes at primes away from \(kq_1A\) and one at its prime divisors. The Selberg square from the previous uniform bound applies with a small power of \(L\) as support. Its CRT error is independent of the coefficients.

Now \(\sum_{z\le q_1\le\sqrt X}W(q_1)/q_1\ll\varepsilon\), and the split-prime Euler product gives \(\sum_{k\le V,\ k\ {\rm split\ only}}W(k)/k\ll\sqrt{\log(2V)}\ll\sqrt{\varepsilon\log X}\). Thus the total to subtract is at most
\[
C_0W(A)\varepsilon^{3/2}\frac{X}{(\log X)^{3/2}}
\]
with absolute \(C_0\). This subtraction includes \(q_1=q_2\), so the retained count certifies the stronger inert-free property.

### Averaging the coefficient loss

The menu satisfies \(\sum_{i,j}W(A)\ll H^2\). To see this, use \(\log(2A)\ll H\) to bound the product from primes \(q>H+2\) by an absolute constant. Expanding the remaining product by its largest contributing prime, Mertens’ bound gives
\[
W(A)\ll 1+\sum_{\substack{q\le H+2\\q\mid A}}\frac{\log(2q)}q.
\]
For each fixed \(i\) and \(q\nmid30\), the condition \(q\mid A\) requires \(25^j=(52-3^c)/5\bmod q\). It has at most one class modulo \(\operatorname{ord}_q(25)\). The order contribution is summable: in \([U,2U)\) the primes of order at most \(U^{1/3}\) divide \(\prod_{j\le U^{1/3}}(25^j-1)\), so there are \(O(U^{2/3}/\log U)\). The larger orders give a block contribution \(O(U^{-1/3})\) to \(\sum_q\log(2q)/(q\,\operatorname{ord}_q(25))\), as do the smaller orders. The interval endpoint error contributes \(O(\log(H+2)/H)\) to the mean. This proves the claimed uniform average.

Choose \(\varepsilon\) once, small enough that the averaged \(O(\varepsilon^{3/2})\) subtraction is at most half the \(c_0\sqrt\varepsilon\) lower bound. The remaining \(m\) are positive and have only split prime factors, so \(5m\) is a true norm. If \(M(p)\) counts these hits, the previous single-cell and pair bounds on the enclosing rectangle give
\[
\sum_p M(p)^2\ll \frac{XH^2}{(\log X)^{3/2}}+
\frac{XH^4}{(\log X)^2}\left(1+\frac{\log\log X}{H}\right).
\]
Cauchy–Schwarz gives \(\gg X/\log X\) primes with \(M(p)\gg H^2/\sqrt{\log X}\) when \(H^2\gtrsim\sqrt{\log X}\). Greedily choosing a cell and deleting its row and column removes at most \(2H-1\) hits each time, giving the stated number of distinct labels for \(H\asymp\log X\). The conclusion is a positive proportion in the prescribed prime family. Density one and pointwise coverage remain open.

### Exact controls and standalone replay

The pinned cell \((7,1)\) separates three cases. At \(p=2053\), \(m\) is inert-free. At \(p=1933\), \(m\) passes the inert-prime panel below \(7\), but \(7\) and \(43\) each have valuation one. At \(p=3613\), \(v_7(m)=2\) and the remainder is a genuine norm, even though the stricter inert-free count discards it. The replay also checks two witnesses with both axes changed from the \(H=2\) menu at one prime.

```python
from math import isqrt

def prime(p):
    return p > 1 and all(p % q for q in range(2, isqrt(p)+1))

def A(c,d):
    f = 3**c + 5**d
    assert (f-52) % 5 == 0
    return (f-52)//5

def m(p,c,d):
    assert prime(p) and p % 12 == 1
    assert 4*max(3**c,5**d) <= 5*p+52
    t = p-A(c,d)
    assert t > 0 and t % 4 == 1 and t % 3
    return t

for H in range(1,9):
    shifts = {A(4*H+3+4*i,1+2*j) for i in range(H) for j in range(H)}
    assert len(shifts) == H*H and all(a > 0 and a % 12 == 8 for a in shifts)

assert A(7,1) == 428
assert m(2053,7,1) == 5**3*13 and 5*m(2053,7,1) == 58**2+69**2
assert m(1933,7,1) == 5*7*43
assert m(3613,7,1) == 7**2*65 and 5*m(3613,7,1) == 7**2+126**2

p = 11479141
a,b = m(p,11,1),m(p,15,3)
assert 5*p == 2069**2+7288**2
assert a == 11443721 and prime(a) and a % 4 == 1
assert b == 5*37*173*269
assert all(prime(q) and q % 4 == 1 for q in (5,37,173,269))
assert 5*a == 3102**2+6899**2 and 5*b == 2**2+6561**2
print("all exact controls passed")
```

The near-threshold lower sieve is used with fixed small \(\varepsilon\), then \(X\) tends to infinity; in particular the actual parameter \(\log D/\log z\) eventually exceeds \(1+\varepsilon/2\). For the two-prime upper sieve, \(t=q_2\ge z\), \(kq_1^2<X\), and hence \(L=X/(kq_1)\ge q_1\ge z\). A small absolute power of \(L\) keeps both candidate primes above the sieve support. At 2 the forms have the same excluded class; this changes only an absolute factor. Finally apply the second moment after discarding \(M(p)\) below a small constant multiple of \(H^2/\sqrt{\log X}\), leaving a positive fraction of the first moment on the retained primes. The corresponding multiplicity and greedy matching conclusions are unconditional on this prescribed prime family, not on all integers.
