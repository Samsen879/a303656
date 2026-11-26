# A degree-28 integral two-moving orbit by reciprocal pullback

Use the exact label, rational polynomials \(w,D,G,F\), constants \(A,B,H,m\), and old coordinate rotation from [the moving-parent quartic](MOVING_PARENT_QUARTIC.md) and [the direct degree-36 pullback](BOTH_ENDPOINTS_MOVING_DEG36.md). In particular \(F=w-m+i(s^2-2)\), \(N(F)=w^2-B\), and \(N(G)=w^2-A\). The symbol \(N\) denotes product with the coefficientwise conjugate.

For rational \(\mu\), set
\[
 E(T)=T^4F(\mu+1/T),\quad f(T)=\mu+(1-H^2N(E(T)))/T.
\]
Here \(E(0)=1/H\), so \(f\) is a polynomial. In each case below \(E\) has degree 4, hence \(f\) has degree 7. Since \(T\) is a unit modulo \(E\), one has \(f\equiv\mu+1/T\bmod E\), and consequently \(E\mid F(f)\). Define
\[
 W=w(f),\qquad Z=\frac{\operatorname{lc}E}{\overline{\operatorname{lc}E}}
                   \overline E\,F(f)/E .
\]
Then \(N(Z)=W^2-B\), the leading term of \(Z\) equals that of \(W\), and \(N(G(f))=W^2-A\). This gives the following two choices at the same actual label:

* \(\mu=-8404257/7\): \(f(0)=8404257\) because \(w\) has no cubic term, so the linear term of \(H^2N(E)\) is \(8\mu\). The parent/child differences from W have degrees 14 and 26.
* \(\mu=0\): \(f\) is odd and W is even. At \(T_0=15680393\) the underlying \(f(T_0)\) lands at another genuine integer anchor. The differences have degrees 14 and 24.

The child degree calculation can be read off the monic normalization \(E/\operatorname{lc} E\). In the two cases the highest nonreal coefficient is one and two degrees below the leading term, respectively (checked exactly below). The resulting imaginary degree of Z is 27 and 26, respectively, since \(\Im F(f)\) has degree 14. For \(D_c=W-\Re Z\), the norm identity gives \(D_c(2W-D_c)=(\Im Z)^2+B\), implying the indicated degrees. At each anchor, undo the unit multiplying \(F(f(T_0))\) in Z by one constant rational rotation, and apply the old constant rational parent rotation and child scaling \(1+2i\). All anchor coordinates are then integers, and \(W(T_0)\equiv26\bmod30\). Substituting \(T=T_0+Kn\) for K a multiple of 30 and every coefficient denominator after these operations gives genuine integral coordinates and preserves that residue. The norms' moving directions are measured after aligning their respective leading coefficients to W, as in the degree-36 note; the constant rotations do not change them.

### A sharp bound for the Möbius-retained-factor model

Let \(E\) be the primitive degree-4 pullback of \(F\) under an invertible real rational Möbius transformation \((aT+b)/(cT+d)\), and suppose a real rational polynomial \(f\) satisfies \(E\mid F(f)\). The only roots of \(F\) in the field of any one root \(\alpha\) over \(\mathbb Q(i)\) are \(\pm\alpha\). To see this, write their two squared values as \(r_\pm=2-im\pm i\sqrt B\) over \(K=\mathbb Q(i,\sqrt B)\), where \(B=9633851\) is nonsquare. Their product \(C=A-m^2-4im\) has Gaussian norm congruent to 2 modulo 3. Thus neither C nor C/B is a square in \(\mathbb Q(i)\), so C is not a square in K. The relative norm of either squared value from K to \(\mathbb Q(i)\) is C, so neither is a square in K. Adjoining \(\sqrt{r_+}\) cannot make \(r_-\) a square: that would require either \(r_-\) or \(r_-/r_+\) a square in K. The same proof with signs exchanged applies to the other root. It also shows that F is irreducible over \(\mathbb Q(i)\).

At a root of \(E\) the value of \(f\) must therefore be plus or minus the original Möbius image. It follows by irreducibility, and by real coefficients and conjugation, that \(E\overline E\) divides \((cT+d)f\mp(aT+b)\). The factors are coprime since F and its conjugate have no common root (a common root would have \(s^2=2\) and \(B=m^2\)), and the Möbius map is injective. If \(c\ne0\), the expression cannot vanish identically for a polynomial \(f\), giving degree at least 7. If \(c=0\), the only possibilities below degree 8 are the two signed exact affine images; the direct swap then keeps the child difference constant after the leading direction is aligned. This bound concerns only this model. It does not rule out a lower-degree orbit using other factors or parametrizations, or imply a growing-label or conjecture-level result.

### Offline replay (SymPy)

~~~python
import sympy as S
T, s = S.symbols("T s", real=True)
I = S.I
A = 5**10 + 9 - 131779
B = S.Rational(5**11 + 27 - 658897, 5)
H, m = A + 5, S.Rational(A + 5, 2)
s0 = 8404257
w = ((s*s-2)**2 + m*m + B)/H
F = w-m+I*(s*s-2)
C = A-m*m-4*I*m
assert not S.integer_nthroot(B, 2)[1]
assert S.expand(C*S.conjugate(C)) % 3 == 2
for mu, anchor, gap in [(S.Rational(-s0,7), 0, 26),
                        (0, 15680393, 24)]:
    P = lambda x: S.Poly(x, T, extension=I)
    E = P(S.expand(T**4*F.subs(s, mu+1/T)))
    Ec = P(S.conjugate(E.as_expr()))
    N = (E*Ec).mul_ground(H**2)
    f = P(mu + S.cancel((1-N.as_expr())/T))
    W = P(w.subs(s, f.as_expr()))
    Ff = W-P(m)+I*(f*f-P(2))
    Z = (Ff.exquo(E)*Ec).mul_ground(E.LC()/S.conjugate(E.LC()))
    Zr = P(S.re(Z.as_expr()).expand())
    assert f.degree() == 7 and W.degree() == 28
    assert Zr.LC() == W.LC() and (W-Zr).degree() == gap
    t = f.eval(anchor)
    if anchor == 0:
        assert t == s0
    D0 = (t*t+A)/m
    w0 = w.subs(s,t)
    G0 = w0-D0+I*t*(D0-1)
    F0 = F.subs(s,t)
    xy = [w0, S.expand(G0*(-1647087+1757216*I)/2408465),
          S.expand(F0*(1+2*I))]
    assert w0 % 30 == 26
    assert all(S.re(x).is_Integer and S.im(x).is_Integer for x in xy)
~~~
