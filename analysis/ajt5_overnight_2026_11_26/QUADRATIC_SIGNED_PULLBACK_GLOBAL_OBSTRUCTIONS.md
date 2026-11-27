# Two global obstructions for quadratic signed-shell pullbacks

This continues [the quadratic discriminant criterion](https://github.com/Samsen879/a303656/commit/6f21b336bd41a851617d2f8c8b0a2f389f574065). The obstructions proved here are for specified classes of quadratic maps and hold for every (d=17^j), (jge1). Passing the two displayed local square tests is not enough. Neither obstruction is a statement about existence of a new numerical mixed multiplier.

The reciprocal argument uses normalized integral valuations on the real field (F). Every rational nonzero prefactor has even valuation because its ramification index is even. The condition (Cequiv0mod17) forces the native discriminant to be nonzero: the displayed congruence is a nonzero square modulo 17. Thus the argument also rules out a tangent rational fiber in the reciprocal branch class.

**No quadratic rational map with a rational fiber at \(1\) can make both signed shells norms at \(d=17\) or \(17^2\) if its two branch values have product \(9/25\).** This is a global obstruction. A concrete map in this class passes the separate square tests at both \(3\) and \(17\). I also obtained an independent obstruction when \(1\) itself is a branch value and the other branch value is infinity or is not a \(7\)-adic unit.

### Reciprocal branch values

Put \(\lambda=3/5\), \(L=\mathbb Q(\zeta_d)\), and \(F=\mathbb Q(\zeta_d+\zeta_d^{-1})\). The class in the first result consists of discriminants
\[
\Delta(U)=a(U^2+\lambda^2)+bU,\qquad a\ne0.
\]
A rational fiber at \(1\) requires \(\Delta(1)\) to be a rational square, possibly zero. The quadratic discriminant criterion requires both \(\Delta(\pm\lambda\zeta_d)/(-3)\) to be squares in \(L\).

Set \(s=\zeta_d+\zeta_d^{-1}\) and \(h=\zeta_d-\zeta_d^{-1}\). Since \(\zeta_d\) is a square, the two candidates have the same square classes as
\[
R_\varepsilon=-\frac{a\lambda^2s+\varepsilon b\lambda}{3},
\qquad \varepsilon=\pm1.
\]
Each \(R_\varepsilon\) is real. A nonzero real element that is a square in \(L\) is either totally positive or totally negative. Its square root is respectively fixed or negated by complex conjugation. The sum \(R_++R_-\) changes sign across real embeddings because \(s\) does. Thus if both are squares, one \(R_\varepsilon\) must be totally negative and have the form \(h^2y^2\) with \(y\in F\).

For \(d=17^j\), the prime above \(17\) in \(F\) is totally ramified with even index \(e=8\cdot17^{j-1}\). The element \(s-2=(\zeta_d-1)^2/\zeta_d\) has valuation one, as does \(h^2=(s-2)(s+2)\). Therefore the negative \(R_\varepsilon\) must have odd valuation. Writing
\[
R_\varepsilon=-\frac{a\lambda^2}{3}\bigl((s-2)+C\bigr),
\qquad C=2+\frac{\varepsilon b}{a\lambda},
\]
forces \(C\equiv0\bmod17\). Otherwise the rational term \(C\) dominates, giving an even valuation. The native fiber now gives
\[
\Delta(1)/a=1+\lambda^2+b/a\equiv(1-\varepsilon\lambda)^2\bmod17.
\]
This is a nonzero square since \(\lambda\equiv4\bmod17\), so \(a\) is a square in \(\mathbb Q_{17}\). Yet
\[
\frac{R_\varepsilon}{a h^2}
=-\frac{\lambda^2}{3(s+2)}
 \left(1+\frac C{s-2}\right)
\equiv-\frac{\lambda^2}{12}\pmod{\mathfrak p_{17}},
\]
a nonsquare because \(-3\) is a nonsquare modulo \(17\). This contradicts \(R_\varepsilon=h^2y^2\). The argument holds for every \(j\ge1\).

### A second obstruction at a ramified native fiber

Suppose \(1\) is a branch value. If the other branch value is infinity, simultaneous squareness would force
\[
\frac{1-\lambda\zeta_d}{1+\lambda\zeta_d}
\]
to be a square in \(L\). Its rational norm is \(P_d^-(1)/P_d^+(1)\). For \(d=17^j\), write \(A=5^{17^{j-1}}\) and \(B=3^{17^{j-1}}\). Modulo \(7\), seventeenth powering inverts both \(A\) and \(B\), and \(A/B\) has order \(3\). Thus the minus and plus shells reduce respectively to \(-1/(AB)\) and \(1/(AB)\). Their ratio is \(-1\bmod7\), a nonsquare.

If the second branch value is a finite rational \(v\), the square test gains the factor \((v-\lambda\zeta_d)/(v+\lambda\zeta_d)\). When \(v=0\) or \(v_7(v)\ne0\), this factor’s rational norm is \(1\bmod7\). The homogeneous cyclotomic values have the same leading or constant unit after normalization at \(7\). The same obstruction therefore applies.

### Exact controls

The reciprocal map
\[
f(T)=\frac{82T^2+9}{41T^2+50}
\]
has \(f(1)=1\), branch values \(2,9/50\), and \(\Delta(U)=-8200U^2+17876U-2952\), with \(\Delta(1)=82^2\). At \(3\), the discriminant has valuation one on both target roots and its normalized residue is a scalar times \(\pm\zeta_d\), a square in the even-degree residue field. At \(17\), \(\Delta(\pm\lambda\zeta_d)\) has residues \(14,10\), so both quotients by \(-3\) are local squares. The global reciprocal obstruction still applies. The ramified map \(1+15T^2\) also passes both separate local tests, and the mod-\(7\) argument excludes simultaneous norms.

Both native shells at \(d=17\) are actual integer norms, with coordinates \((512959,198560)\) and \((225833,121632)\). 

Quadratic maps outside the stated classes remain unresolved. Even a formal solution at \(17\) or \(289\) would still require an actual power-ratio specialization and new mixed-shell certificates to yield an independent numerical generator.

```python
def D(u):
    return -8200*u*u+17876*u-2952
assert D(1)==82**2
assert (-8200%9,17876%9,-2952%9)==(8,2,0)
l=3*pow(5,-1,17)%17
assert [D(e*l)%17 for e in (1,-1)]==[14,10]
assert [D(e*l)*pow(-3,-1,17)%17 for e in (1,-1)]==[1,8]
assert [20*(1-e*l)%17 for e in (1,-1)]==[8,15]
assert pow(-3,8,17)==16
for a,b in ((5,3),(pow(5,-1,7),pow(3,-1,7))):
    assert (a-b)*(a+b)%7
    Hm=(pow(a,17,7)-pow(b,17,7))*pow(a-b,-1,7)%7
    Hp=(pow(a,17,7)+pow(b,17,7))*pow(a+b,-1,7)%7
    assert Hm*pow(Hp,-1,7)%7==6
assert (512959**2+3*198560**2)*2==5**17-3**17
assert (225833**2+3*121632**2)*8==5**17+3**17
```
