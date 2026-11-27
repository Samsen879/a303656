# Joint coordinate height obstruction for exact pinned norm factors

The two exact norm factorizations give a joint obstruction on the pinned \(H\) allocation. Let \(x_i\) and \(y_i\) be the four coordinates on the \(d\) and \(e\) edges, aligned real-to-real and imaginary-to-imaginary, with short factors matched to short factors. For every sufficiently large ordinary solution,
\[
\boxed{\displaystyle \prod_{i=1}^4 \operatorname{ht}(y_i/x_i)\ \ge\ A^{3/8}/56,}
\]
where \(\operatorname{ht}(n/d)=\max(|n|,d)\) in lowest terms. Thus a construction that reuses the four coordinates with rational corrections of height \(O(\ell^{k_i}(\log A)^C)\) fails cofinally if \(\sum k_i\le78\). This includes degree 19 in each of the four corrections.

### Exact factorization and the two elimination rows

Use the pinned \(A=3^a,\ B=5^b\), with \(a,b\) even and \(39/40<B/A<122/125\). Put \(U=\sqrt A,\ V=\sqrt B\). The edge products are \(d=2(A+75B)\) and \(e=20A+25B\). An ordinary match has true pairs \(vu=d,\ zw=e\), with \(v=H\ell\) and \(v+u=z+w=L<37U\). [Pinned P2 setup](https://github.com/Samsen879/a303656/commit/0853017858c4b0acfb92d5ce798f2ad0c878610f)

The odd parts of \(v,z\) give primitive integer norm factors satisfying
\[
\begin{aligned}
(x_1+x_2\sqrt{-3})(x_3+x_4\sqrt{-3})&=U+5V\sqrt{-3},\\
(y_1+y_2\sqrt{-5})(y_3+y_4\sqrt{-5})&=m(2U+V\sqrt{-5}),\qquad m\in\{1,2\}.
\end{aligned}
\]
For the first identity, if \(D\) is the odd part of \(v\), take a shortest vector in \(5Vx_1-Ux_2\equiv0\bmod D\), weighted by \(x_1^2+3x_2^2\). Its norm is a multiple of \(D\) and at most \(2D\) by planar lattice reduction. The value \(2D\) is impossible modulo 4. Dividing by this factor gives the integral companion of norm \(4(d/8)/D\). The second identity follows from the corresponding lattice for \(e/5\), where the shortest norm is less than three times the divisor. The ordinary bounds give \(|x_i|,|y_i|<13A^{1/4}\). The factors are primitive and their norms grow, so their coordinates are nonzero at sufficiently large height.

Set \(\rho_i=y_i/x_i\). Eliminating \(U,V\) gives
\[
\begin{aligned}
(\rho_1\rho_3-2m)x_1x_3&=(5\rho_2\rho_4-6m)x_2x_4,\\
(5\rho_1\rho_4-m)x_1x_4&=(m-5\rho_2\rho_3)x_2x_3.
\end{aligned}
\]
**Both rows survive.** Write \(P_x=\prod x_i\) and \(P_y=\prod y_i\). The exact norm equations force
\[
v_3(P_x)\equiv1,\quad v_3(P_y)\equiv0,\qquad
v_5(P_x)\equiv v_5(P_y)\equiv0\pmod2.
\]
For example, in \(x_1x_3-3x_2x_4=U\), the two term valuations at 3 must agree, including the extra factor 3 in the second term. If both products are divisible by 3, primitivity puts each product’s full 3-power in a single coordinate. Those coordinates are too small to reach \(v_3(U)\). If \(x_2x_4\) is a unit, the first product has valuation exactly one. The other three parity checks use the same argument with unit coefficients. Collapse of the first row would give \(P_y/P_x=12m^2/5\), contradicting the parity at 5. Collapse of the second would give \(P_y/P_x=(m/5)^2\), contradicting the parity at 3.

### The height and support bound

Let \(G_3=\gcd(x_1x_3,x_2x_4)\) and \(G_5=\gcd(x_1x_4,x_2x_3)\). The exact real and imaginary equations make these a 3-power and a 5-power, respectively. Primitivity puts \(G_3\) in both coordinates of one diagonal, and \(G_5\) in both coordinates of one column. The placements intersect, so
\[
G_3G_5\le \max_i |x_i|<13A^{1/4}.
\]
The reduced heights of \(x_1x_3/(x_2x_4)\) and \(x_1x_4/(x_2x_3)\) are at least \(U/(4G_3)\) and \(5V/(2G_5)\). Their product is at least \(A^{3/4}/26\). The two elimination rows bound those same heights above by \(17\prod_i\operatorname{ht}(\rho_i)\) and \(7\prod_i\operatorname{ht}(\rho_i)\). This gives the boxed bound.

Since \(H\asymp A^{28088000/56717661}\), the ordinary allocation has \(\ell\asymp A^\delta\) with \(\delta=541661/113435322\), and \(78\delta<3/8<79\delta\). In prime-support terms, the four matched pairs must have total weighted valuation discrepancy at least \((3/8)\log A-O(1)\). If the contribution from any fixed prime set is \(o(\log A)\), the remaining discrepancy must come from moving prime powers. Unrestricted coordinate ratios remain open.

### True \(3,5\) control

For \(A=3^6,\ B=5^4\), both norm factorizations below are exact. The \(e\)-pair gives \(K=822758\), where the \(d\)-remainder falls strictly between consecutive squares. This checks the joint arithmetic and the distinction between two true factor pairs and a common integer height.

```python
from fractions import Fraction as F
from math import gcd, prod

def mul(a, b, c, d, k):
    return a*c-k*b*d, a*d+b*c

def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

A, B = 3**6, 5**4
x, y = (38,29,3,1), (3,1,41,3)
assert mul(*x, 3) == (27,125)
assert mul(*y, 5) == (108,50)
assert [vp(prod(t),3) % 2 for t in (x,y)] == [1,0]
assert [vp(prod(t),5) % 2 for t in (x,y)] == [0,0]
a,b,c,d = x
r,s,t,u = (F(j,i) for i,j in zip(x,y))
assert (r*t-4)*a*c == (5*s*u-12)*b*d == -333
assert (5*r*u-2)*a*d == (2-5*s*t)*b*c == -31
assert gcd(a*c,b*d)*gcd(a*d,b*c) <= max(x)

assert 3967*24 == 2*(A+75*B)
assert 35*863 == 20*A+25*B
K = A+25*B+(35+863)**2
assert K-81*A-125*B == (863-35)**2
assert 652**2 < K-9*A-625*B == 425572 < 653**2
delta = F(1,2)-F(28088000,56717661)
assert 78*delta < F(3,8) < 79*delta
assert 26*17*7<56**2 and 4*37<13**2
print("OK")
```

For the original conjecture, a genuine common \(K\) would give shared-coordinate representations of \(K+t^2\). At a fixed target \(n\), this requires \(n-K\) to be a nonnegative square. The obstruction limits one construction of simultaneous labels and leaves the single-label existence question for \(n\) unresolved.

The coordinate-size input follows from \(u,v,w,z<L<37\sqrt A\). On the first edge the companion norm is \(d/(2D)\le4u\), since \(v\) has 2-adic depth at most three; on the second edge the analogous factor norms are at most \(2z\) and \(4w\). For the valuation comparisons, if two complementary products in one norm row are both divisible by the same prime, primitivity forces the prime power in each product into one coordinate of that product. The size bound then places each below the exponent of the corresponding growing pure-power right-hand side. Thus equality of the two left valuations is forced, including the factor 3 in the first real equation or the factor 5 in the first imaginary equation. This covers the nonzero-elimination premise; the argument does not impose any bounded support on unrestricted coordinate ratios.