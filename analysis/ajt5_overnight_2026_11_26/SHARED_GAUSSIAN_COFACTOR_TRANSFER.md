# Shared Gaussian cofactor transfer on prescribed targets

A shared Gaussian factor \(2+i\) gives an **exact transfer criterion at a prescribed target** in an explicit height interval. I constructed cofinally genuine \(3,5\) targets where it produces an ordinary \(S_2\) representation even though **every shift in a growing window from the supplied \(S_0\) representation fails**.

### The prescribed-target criterion

Use the balanced strip \(39/40<B/A<122/125\), with \(S_0=A+25B\), \(S_2=81A+125B\), \(S_3=729A+B\), and \(U=729A+625B\). Suppose the supplied ordinary representation is \(n-S_0=L^2+t^2\), with \(2+i\mid L+it\). As \(S_2-S_0=4e\) and \(5\mid e\), the quotient \(Q=(n-S_2)/5\) is integral. [Checked shift setup](https://github.com/Samsen879/a303656/commit/fa3c2590b576431c6c79f106c6c1c17d73389c64)

If
\[
891A-30B<n\le U,
\]
then an ordinary \(S_2\) representation sharing that oriented factor exists **if and only if** every prime \(3\bmod4\) has even valuation in \(Q\). To construct it, take any one representation \(Q=u^2+v^2\) and normalize it to \(u\ge v\ge0\). Then
\[
(2+i)(u-iv)=(2u+v)+i(u-2v),\qquad
(2u+v)^2\ge4Q.
\]
Thus its height is at least \(S_2+4(n-S_2)/5>S_3\), and at most \(n\le U\). The conjugate orientation works as well. This needs one quotient representation, which can be obtained from a factorization of \(Q\), or supplied directly. It needs no enumeration of the second remainder’s representations.

### One target, two paths

On the balanced phase \(a\equiv2\bmod10,\ b\equiv64\bmod110\), write \(W=\sqrt A\). For any fixed \(0<\eta<1/6\), choose \(s\asymp A^\eta\) with \(s\equiv1\bmod55\). The following construction gives an initial \(L+it\) and a second point \((L-2r)+i(t-2s)\) at the **same** target:
\[
rL+st=e+r^2+s^2,\qquad r\equiv b_0=1+11s\pmod{55s}.
\]
This progression gives \(r\equiv1\bmod11\) and \(r\equiv2s\bmod5\). With \(L,t\) multiples of \(11\), the equation ensures that \(2+i\) divides both \(L+it\) and \(2(r+is)\), hence both representations.

Here is the size argument behind the construction. Write \(r=b_0+55sj\) and \(L=11x\). Integrality of \(t/11\) fixes \(x\bmod s\) to
\[
x_0=\frac{e+b_0^2+s^2}{11}\pmod s.
\]
Set \(x=x_0+s(J-95j)\), where \(J\) is chosen by the function
\[
\psi(r)=\frac{(e+s^2)/r+20r-11x_0-19b_0}{11s}.
\]
Its minimum is at \(r_*=\sqrt{(e+s^2)/20}\), and
\[
\psi(r)-\psi(r_*)=\frac{20(r-r_*)^2}{11sr}.
\]
Take \(J=\lfloor\psi(r_0)\rfloor+2\), with \(r_0\) the first progression point above \(r_*\). If \(R>r_*\) solves \(\psi(R)=J\), take the second progression point \(r>R\). Then \(0.9\sqrt{sW}<R-r_*<2\sqrt{sW}\), and \(55s<r-R\le110s\). Factoring the quadratic that gives \(t\) yields \(t\asymp\sqrt{sW}\). Also \(30W<L<32W\), \(M=L-2r>26W\), and \(n=S_0+L^2+t^2\) lies in the criterion’s interval for sufficiently large \(W\). Both witness heights are ordinary.

Fix this \(n\) and its supplied \((L,t)\). Trying any \(|\sigma|\le s\) changes the successful square \(M^2\) by
\[
(\sigma-2s)(2t-\sigma-2s).
\]
This is strictly negative since \(t/s\to\infty\), and has size \(O(s^{3/2}\sqrt W)=o(W)\). Every remainder in that growing window therefore lies strictly between \((M-1)^2\) and \(M^2\). The cofactor path succeeds at the very same \(n\), with both labels genuinely represented.

### Independent replay

This control takes \(s\asymp A^{1/8}\).

```python
from math import isqrt

a, b = 574422, 392104
W, B = 3**(a//2), 5**b
A = W*W
assert a%10 == 2 and b%110 == 64 and 39*A < 40*B and 125*B < 122*A
S0, S2, S3, U = A+25*B, 81*A+125*B, 729*A+B, 729*A+625*B
e = 20*A+25*B

s = 1+55*((isqrt(isqrt(W))+54)//55)
b0, P = 1+11*s, 55*s
x0 = ((e+b0*b0+s*s)//11) % s
r0 = b0+P*((isqrt((e+s*s)//20)-b0)//P+1)
J = (e+s*s+20*r0*r0-(11*x0+19*b0)*r0)//(11*s*r0)+2
C = 11*s*J+11*x0+19*b0
r = b0+P*(((C+isqrt(C*C-80*(e+s*s)))//40-b0)//P+2)
L = 11*(x0+s*(J-95*((r-b0)//P)))
t, rem = divmod(e+r*r+s*s-r*L,s)
assert rem == 0
n = S0+L*L+t*t
assert n%121 == 36 and 891*A-30*B < n <= U
assert (L-2*t)%5 == (r-2*s)%5 == 0

# Compute one quotient witness by Gaussian division.
x = (2*L+t-4*r-2*s)//5
y = (2*t-L-4*s+2*r)//5
u,v = sorted((abs(x),abs(y)),reverse=True)
M,T = 2*u+v,u-2*v
assert (M,T) == (L-2*r,t-2*s) and M*M+T*T == n-S2
assert S3 < min(S0+L*L,S2+M*M) <= max(S0+L*L,S2+M*M) <= U

# Every remainder for |sigma| <= s is between consecutive squares.
assert t > 3*s and 3*s*(2*t+3*s) < 2*M-1
```

The transfer criterion applies with \(n\) fixed. The cofinal construction supplies controls for it. The narrow-window obstruction is for the supplied \(S_0\) representation and leaves open whether a different first representation permits a smaller shift.

The fixed-target criterion tests the quotient rather than predicting that it is a norm; its gain is an ordinary-height oriented witness from any one quotient representation. For the family construction, the modular equation reduces to \(2L+t\equiv0\pmod5\) because \(r\equiv2s\pmod5\), \(e\equiv0\pmod5\) and \(5\nmid s\). The resulting divisibility is \(L-2t\equiv0\pmod5\). The progression offset is \(O(s)\), so \(\psi(r_0)-\psi(r_*)=O(s/W)=o(1)\); \(J-\psi(r_*)\) lies between 1 and \(2+o(1)\). Substituting this in the difference-of-values identity gives the stated square-root-scale gap. Here \(s^{3/2}\sqrt W=o(W)\) is exactly the strict requirement \(\eta<1/6\).
