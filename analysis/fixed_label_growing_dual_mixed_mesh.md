# A fixed-label growing mesh on two actual mixed edges

**Verified the fixed-\(L\), growing-\(K\) mesh theorem.** For every fixed \(L\ge1\), \(0<c<\sqrt{5/96}\), and \(0<\delta<1/4-(24/5)c^2\), every sufficiently large multiple \(K\) of four gives at least \(2^{\delta K}\) distinct generated #93 targets with \(2^K\le S<2^{K+1}\). At each target, the two mixed edges each have \(2^{\lfloor c\sqrt K\rfloor}\) primitive critical seeds. All numerical \(q\) values are distinct across both edges. The stated gap, span, and common-interval constants survive at the actual integer targets.

### Prime supply and Gaussian normalization

Khale et al., p. 1, explicitly state Coleman’s estimate for a **fixed ideal modulus and a specified ray class**, counting prime ideals of rational-prime norm. Its angular width is \(>X^{-5/24+\epsilon}\) and its radial interval length satisfies \(X^{19/24+\epsilon}\le h\le X\). In the identity ray class modulo \((C_L)\), the generator \(\pi\equiv1\bmod C_L\) is unique because no other Gaussian unit is \(1\bmod C_L\). Thus the exponent \(g\) in their angular normalization is \(1\), and the angle is the actual argument of that generator. The chosen prime itself lies in the negative sector. Its conjugate defines the positive control angle. [Khale et al., p. 1](https://arxiv.org/pdf/2008.09677)

The following direct published disk estimate independently supplies the necessary primes: Coleman–Swallow’s published equation (1.4) gives a positive weighted asymptotic for Gaussian integers in an actual residue class in a disk centered at \(w\), with radius \(r\ge |w|^{7/12}\log^{C}|w|\), \(r<\gamma|w|\), and modulus norm eventually below a fixed power of \(\log|w|\). To supply a packet of angular half-width \(\eta\asymp X^{-1/\rho}\), put the disk center at modulus \(\sqrt{3X/2}\) and at the packet’s negative central angle, with radius \(r=|w|\eta/4\). The disk stays in the packet and \(X<Nz<2X\). Since \(\rho>24/5\), the radius meets the lower bound by a power margin. The main term is of order \(X\eta^2\) for the fixed modulus. The total contribution of higher prime powers and degree-two primes is \(O(X^{1/2}\log^2 X)=o(X\eta^2)\). This supplies \(\gg_{C_L}X\eta^2/\log X\) degree-one primes uniformly in the moving center, more than enough at every layer. [Coleman–Swallow, Acta Arithmetica 120, p. 350, (1.4)](https://www.impan.pl/shop/en/publication/transaction/download/product/82013)

### Exact roots, primitive chords, and distinct seeds

Use \(A=9^L,\ B=25^L,\ D=12B-3A,\ E=A+10B,\ h=D-5\). The #93 lift takes
\[
t=(5y^2-hy+5+3h-E)/10,\qquad P=(h-3t,t),\quad
Q_1=P+(1,3),\quad Q_2=P+(3-y,-1-3y)
\]
with \(10\mid y\), \(S=N(P)\), and \(n=S+3A+25B\). The norm differences are \(2D,2E\), giving the three true exponent labels \((2L+1,2L+2),(2L+2,2L),(2L,2L+1)\). [Public #93 lift and oriented division formulas](https://github.com/Samsen879/a303656/pull/93/files)

Put \(\Delta=h^2+20E\), \(\alpha=\Delta-100+20(h+10)i\), and \(C_L=160DE\Delta N(\alpha)\). The two oriented divisibility quadratics in \(y\) have discriminants \(\alpha\) and \(\Delta\), evaluated modulo the selected prime ideal. For the second one, with \(I^2=-1\) in the residue field, \((-h+10I)^2-20(-5-E-hI)=\Delta\). Gaussian quadratic reciprocity gives the square conditions directly. Every odd primary prime factor of either discriminant sees \(\pi\equiv1\) modulo that factor. The supplementary symbols for \(i\) and \(1+i\) are both \(+1\) since \(\pi\equiv1\bmod8\). Neither discriminant vanishes modulo \(\pi\). Thus every chosen prime supplies a root for its assigned endpoint. Distinct rational norms let all roots enter one integer CRT class together with \(y\equiv0\bmod10\). [Gao–Zhao, §2.1, equations (2.1)–(2.2)](https://arxiv.org/pdf/2210.08840)

For **every** carrier-plus-subset product \(G\), the rotated endpoint \(R=(Q_j/G)\bar G\) is integral and \(R\equiv Q_j\bmod 2DE\). Its chord \(R-P\) has odd coordinates. If an odd prime divided both coordinates, it would divide the norm gap \(2D_j\), with \(D_j=D\) or \(E\), and would therefore divide both coordinates of the corresponding raw chord. The first raw chord is primitive, and the second has gcd dividing \(10\) and equal to \(1\) when \(10\mid y\). This proves simultaneous primitivity without an extra CRT condition.

The ideal ratio is \(r_G=2\operatorname{Im}(G)^2/N(G)\). All control angles lie in \((0,\pi/2)\), so equal ideal ratios would imply that the quotient of the two products is rational. Gaussian prime valuations rule this out because the rational norms are globally distinct, only one orientation is loaded at each norm, and the two edges have private carriers. If each full edge product has norm at most \(U\), distinct ideal ratios differ by at least \(2/U^2\). For the actual \(q=N(R-P)/2\), direct expansion gives
\[
|q/S-r_G|\le D_j/S+|Q_j-P|/\sqrt S=O_L(2^{-K/4})
\]
uniformly on the whole parameter window.

### Mesh constants and height

Define \(a_K=\arcsin(1/\sqrt{128K(K+1)})\), \(b_K=\arcsin(1/(K\sqrt{128}))\), \(W_0=b_K-a_K\), \(W=W_0/3\), and \(\theta_0=a_K+W\). Both carriers have their positive control angle within \(W/(100J)\) of \(\theta_0\). The full subset supports straddle \([\theta_0+W/20,\theta_0+19W/20]\) because the sum of satellite weights is \((1+o(1))W\). For decreasing positive weights \(w_j\), the subset gap is bounded by the larger of the smallest weight and the positive excess of any weight over the sum of all smaller weights: add weights starting from the smallest, each time taking the old set and its translate. Apply this to the packet tolerances below.

Write \(J=\lfloor c\sqrt K\rfloor\), \(\lambda=2-1/(2J)\), and let \(W\) be one third of the critical angular width. The satellite centers are \(W(\lambda-1)\lambda^{-j}\), with tolerances \(W\lambda^{-j}/(100J)\). Each weight minus the sum of the smaller weights is at most \(W\lambda^{-J}\), as is the smallest weight. Inserting weights from smallest to largest gives the same bound on every subset-sum gap. Since \(\lambda^{-J}\le(4/3)2^{-J}\), mapping through \(2\sin^2\theta\) gives ideal gaps at most \((4/9+o(1))\beta_K2^{-J}\), where \(\beta_K=1/[64K^2(K+1)]\). The individual span is \((1/3+o(1))\beta_K\), and the common interior has length \((3/10+o(1))\beta_K\).

Take \(X_j\asymp(K^2J\lambda^j)^\rho\), \(0\le j\le J\), with \(24/5<\rho<(1/4-\delta)/c^2\). The two primes per layer can have distinct rational norms, and the layer annuli are disjoint. Then
\[
2\log_2 U=\rho J^2+O(J\log K),\qquad M_{\rm CRT}\le10U^2.
\]
The strict budget both makes \(2/U^2\) dominate the physical error and puts at least \(2^{\delta K}\) CRT representatives in \([13Y/16,7Y/8)\), \(Y=2^{K/4}\). On that window, \(S=(5/2)y^4+O_L(y^3)\) is increasing and lies in \([2^K,2^{K+1})\). The physical error is also \(o(\beta_K2^{-J})\), so the claimed actual gap \(\beta_K2^{-J}\), span \(>\beta_K/4\), and common interval of length \(\ge\beta_K/8\) all follow.

**Strongest verified claim:** the full simultaneous mesh bound holds at every generated target in the counted CRT window. **Weakest dependency:** prime supply in shrinking packets is an external analytic theorem. The published 2005 disk estimate supplies exactly what the construction needs independently of access to the 1990 proof.

The scope is strictly fixed \(L\) with growing \(K\). In fact \(C_L>B^8\), so preloading even two nonreal primes in this residue class on one endpoint forces its norm above \(C_L^4>B^{32}>A^{32}\). The old ordinary-height cap is therefore incompatible with this particular loading method. The result provides no coverage guarantee for a prescribed integer.
### Exact finite mesh-lemma replay

This integer endpoint check verifies the elementary subset-gap mechanism and a negative unsoftened-dyadic control. The existence of sufficiently many primes is the analytic argument above, not an inference from this finite replay. See [#125](https://github.com/Samsen879/a303656/pull/125) for a separate finite literal 3/5 certificate with native ordinary height.

```python
"""Exact combinatorial audit of the variable-precision mesh lemma.

This does not certify a finite list of ray primes. The analytic prime
supply and the actual 3/5 divisibility theorem are proved separately.
It enumerates all endpoint packet errors through J=10 and includes
a negative control for unconstrained perturbations of dyadic weights.
"""
from fractions import Fraction as F

def subset_sums(weights):
    values=[0]
    for w in weights:
        values += [a+w for a in values]
    return sorted(set(values))

states=0
max_gap_ratio=F(0)
for J in range(2,11):
    q=F(4*J-1,2*J)
    denominator=100*J*(4*J-1)**J
    centers=[50*(2*J-1)*(2*J)**j*(4*J-1)**(J-j)
             for j in range(1,J+1)]
    errors=[(2*J)**j*(4*J-1)**(J-j) for j in range(1,J+1)]
    allowed_gap=100*J*(2*J)**J
    assert F(allowed_gap,denominator)==q**(-J)
    assert q**(-J)<=F(4,3)*F(1,2**J)
    for mask in range(1<<J):
        weights=[a+(e if mask>>j&1 else -e)
                 for j,(a,e) in enumerate(zip(centers,errors))]
        assert all(a>b>0 for a,b in zip(weights,weights[1:]))
        tail=0
        local_bound=weights[-1]
        for w in reversed(weights):
            local_bound=max(local_bound,w-tail)
            tail+=w
        assert local_bound<=allowed_gap
        values=subset_sums(weights)
        observed=max(b-a for a,b in zip(values,values[1:]))
        assert observed<=local_bound
        states+=1
        max_gap_ratio=max(max_gap_ratio,F(observed,allowed_gap))

# The same relative error scale around ratio exactly 2 does not suffice.
J=16
dyadic=[F(1,2**j) for j in range(1,J+1)]
dyadic[0]+=F(1,100*J)
values=subset_sums(dyadic)
largest=max(b-a for a,b in zip(values,values[1:]))
assert largest==F(1,2**J)+F(1,100*J)
assert largest>40*F(1,2**J)
print("endpoint-packet states:",states)
print("max observed gap / proved allowed gap:",max_gap_ratio)
print("unprotected dyadic control: gap / final scale =",largest*2**J)
print("PASS: the negative tail margin is needed; the softened mesh absorbs it")
```
