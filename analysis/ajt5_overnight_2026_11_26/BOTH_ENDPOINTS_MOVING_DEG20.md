# A symmetric degree-20 double-moving orbit via a quadratic root scale

Use the same true label and notation as in [the moving-parent quartic](MOVING_PARENT_QUARTIC.md). Thus \(A=9633855,\ B=9633851,\ H=9633860,\ m=H/2\), and \(HF(s)=(s^2-2+im)^2+B\). Let
\[
 P(T)=(T^2-2B+imB)^2+B^3,\quad
 h(T)=\frac{T}{HB}\left[(T^2/B-2)^2+m^2+B\right].
\]
For a root T of P, \(s=T/\sqrt B\) is a root of F. Hence \(w(s)^2=B\), by \(N(F)=w^2-B\), and \(h(T)=T w(s)/B=\pm s\). As F is even, \(P\mid F(h)\) (P is squarefree because F is). Consequently
\[
 W=w(h),\qquad Z=\overline P F(h)/P
\]
satisfy \(N(Z)=W^2-B\) and \(N(G(h))=W^2-A\). This real polynomial substitution has degree five and is odd. The common W is even of degree 20. The parent real gap is of degree 10. The monic ratio \(\overline P/P\) first differs from 1 at order \(T^{-2}\) with nonzero imaginary coefficient, giving imaginary degree 18 for Z; its real gap has degree 16 by the norm identity as in [degree 28](BOTH_ENDPOINTS_MOVING_DEG28.md).

At \(T_*=3028742658131969740807652132\), exact substitution gives integral \(s=h(T_*)\equiv8404257\bmod H^2\). The original parent rotation and child scale can therefore be recovered at the new anchor, undoing the norm-one factor \(\overline P/P\) by a constant rational rotation at \(T_*\). That factor is defined there because \(P\) has no real root: its imaginary part could vanish only at \(T^2=2B\), where the real part is \(B^2(B-m^2)\ne0\). Clear denominators by taking \(T=T_*+Kn\) with K divisible by 30 and every resulting coefficient denominator. This supplies unbounded genuine integer points with \(W\equiv26\bmod30\) and both leading-direction gaps moving.

## Sharpness for this real quadratic root-scale model

Allow the retained root to be \(u\alpha\), where \(u\in\mathbb Q(\sqrt B)^\times\) and \(\alpha\) is any original root of F. The [original root-field calculation](BOTH_ENDPOINTS_MOVING_DEG28.md) gives \(K=\mathbb Q(i,\sqrt B)\), \([\mathbb Q(i,\alpha):K]=2\), and only \(\pm\alpha\) are F roots in \(\mathbb Q(i,\alpha)\). Thus a real rational polynomial \(h\) with \(F(h(u\alpha))=0\) must have \(h(u\alpha)=\pm\alpha\). If \(\deg h\le4\), comparison of the odd part over \(K\) gives \(u(c_1+c_3u^2\alpha^2)=\pm1\). The value \(\alpha^2=2+i(\pm\sqrt B-m)\) is nonreal, hence \(c_3=0\) and \(u\) must be rational. Then the even part, a rational polynomial of degree at most two in \(\alpha^2\), vanishes identically: \(\alpha^2\) has four distinct conjugates \(2\pm i(\pm\sqrt B-m)\). Thus h is just a real linear scaling, for which the full-factor swap gives a conjugate of the original child and still has constant child gap. The degree-20 construction is therefore minimal in this retained-root scale model, not a bound for general quadratic or rational pullbacks.

### Offline replay, SymPy

~~~python
import sympy as S
T,x = S.symbols("T x", real=True)
I = S.I
A,B,H,m = 9633855,9633851,9633860,S.Integer(4816930)
p = lambda v:S.Poly(v,T,extension=I)
w = ((x*x-2)**2+m*m+B)/H
F = w-m+I*(x*x-2)
h = T*((T*T/S.Integer(B)-2)**2+m*m+B)/(H*B)
P = p((T*T-2*B+I*m*B)**2+B**3)
W = p(w.subs(x,h))
Z = p(F.subs(x,h)).exquo(P)*p(S.conjugate(P.as_expr()))
assert W.degree() == 20 and (W-p(S.re(Z.as_expr()).expand())).degree() == 16
assert p(S.im(Z.as_expr()).expand()).degree() == 18
assert Z*p(S.conjugate(Z.as_expr())) == W*W-p(B)
assert p((h*h+A)/m).degree() == 10
t0 = 3028742658131969740807652132
s = h.subs(T,t0)
assert s.is_Integer and (s-8404257) % H**2 == 0
w0, d = w.subs(x,s), (s*s+A)/m
xy = [w0, S.expand((w0-d+I*s*(d-1))*(-1647087+1757216*I)/2408465),
      S.expand(F.subs(x,s)*(1+2*I))]
assert all(S.re(y).is_Integer and S.im(y).is_Integer for y in xy)
assert w0 % 30 == 26
~~~
