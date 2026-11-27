# Ninth sphere ray, binomial norm classification, and varying kernels

**Phase \(38\) closes the \(34\)–\(42\) gap.** Both \((m,e)=(38,38)\) and \((38,22)\) give exact Eisenstein norm seeds at that phase. The nine rays now give, in each odd class modulo \(4\),
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{9/22}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda\in\{1,3\},
\]
effectively for all sufficiently large \(X\). Here \(A_\lambda\) counts distinct generated targets. The exponent \(9/22\) is sharp in the liminf for these nine rays.

### A non-cubing specialization and its algebraic limit

Let \(N(a,b)=a^2+3b^2\). The new diagonal seed comes from
\[
\frac{5^{19}-3^{19}}2=N(3038279,318864),\qquad
\frac{5^{19}+3^{19}}2=N(179768,1779982).
\]
Multiplying the two norm elements and scaling gives a norm for \(5^{38}-3^{38}\). In fact,
\[
\frac{25^{19}-9^{19}}{25-9}
  =N(578265601036,2732701737265).
\]
This is a genuine norm transfer by multiplier \(19\) at the actual \(25,9\) specialization.

**Generic binomial transport has an exact classification, even with unbounded degrees.** For positive integers \(a,b,c,d\), the quotient
\[
\frac{X^a-Y^b}{X^c-Y^d}
\]
is a norm from \(\mathbb Q(\sqrt{-3})(X,Y)\) to \(\mathbb Q(X,Y)\) exactly when \((a,b)=3^j(c,d)\) for some integer \(j\). To see this, work in the Laurent polynomial ring. If the slopes differ, the primitive binomial of the numerator gives a conjugation-invariant prime of valuation one, absent from the denominator. A norm has even valuation at every such prime. For equal slopes, write the two binomials using the same primitive monomial \(T\), with powers \(g,h\). The factors \(\Phi_\ell(T)\) for \(3\nmid\ell\) stay irreducible over \(\mathbb Q(\sqrt{-3})\), since \(\mathbb Q(\zeta_\ell)\) does not contain \(\zeta_3\). Their valuations match exactly when \(g,h\) have the same \(3\)-free part. Repeated cubing supplies the converse through
\[
A^2+AB+B^2=N\big((A-B)/2,(A+B)/2\big).
\]
Thus the multiplier-\(19\) certificate uses arithmetic of the specialized factors that the generic quotient cannot supply.

### What bounded spacing would require

There is also a uniform obstruction to using a finite list of coefficients in radical certificates for the two halves. For each fixed degree \(D\ge2\) and either sign, the equation
\[
5^u\pm3^v=Cz^D
\]
has \(O_D(1)\) pairs of positive exponents for each positive integer \(C\), with the bound **independent of \(C\)**. Write \(u=r\bmod D\), \(W=5^{(u-r)/D}\), and \(\theta^D=C/5^r\). In \(K=\mathbb Q(\theta,\zeta_D)\), put \(\alpha_j=W-\zeta_D^j\theta z\). Their product is \(\mp3^v/5^r\), and each is integral outside \(5\), so all are units outside the primes above \(3,5\). The identity
\[
\frac{\alpha_1}{(1-\zeta_D)W}
-\frac{\zeta_D\alpha_0}{(1-\zeta_D)W}=1
\]
is a nondegenerate two-term unit equation. Its group rank is bounded in terms of \(D\), because the field degree is at most \(D\varphi(D)\) and the extra primes divide \(D\). A solution fixes \(\theta z/W\), hence \(3^v/5^u\), which fixes both exponents. This gives the claimed uniform bound by Evertse–Schlickewei–Schmidt. [Primary unit-equation theorem](https://annals.math.princeton.edu/2002/155-3/p04)

In particular, positive lower density of half-exponents \(u\le U\) would require \(\gg U\) distinct squarefree kernels for **each** half among the underlying seeds. This requirement survives cubing: depths at least \(K\) contribute only multiples of \(3^K\), so for a fixed positive density one can discard those depths and count at most \(K\) heights per base seed. A sufficient bounded-spacing theorem would give a fixed \(G\) and \(\eta>0\) such that every sufficiently large interval \([M,M+G]\) contains an admissible \(m\equiv2\bmod4\) with an admissible \(e\equiv2\bmod4\) and \(3^e\le5^{(1-\eta)m}\). A fixed sufficiently deep cubing step would then preserve bounded spacing and give an effective \(X^{1/2-\varepsilon}\) generated population in both classes. The algebraic restrictions above leave the supply of those varying arithmetic certificates open.

### Spacing and exact same-height tests

The sorted phases are
\[
18,\ 22,\ 26,\ 82/3,\ 30,\ 34,\ 38,\ 42,\ 142/3,\ 54 .
\]
The largest ratio is now \(22/18=11/9\). The last completed height therefore exceeds \(X^{9/11}\). The new ray meets the same size and ternary conditions as the existing rays, so the effective per-height count applies in both classes. At \(X=5^{22\cdot3^j}\), the preceding lower power is \(5^{18\cdot3^j}\), and even all norm orientations give only \(Q^{1/2+o(1)}\) targets per height. This gives the matching liminf ceiling. [Effective orientation count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The replay checks true positive and signed identities at depths zero and one for both odd classes. At each of the same heights it also produces signed controls whose prescribed positive residual has exact odd valuation at a Gaussian inert prime.

```python
from fractions import Fraction as F

def norm(a,b):
    return a*a + 3*b*b

a,b,c,d = 3038279,318864,179768,1779982
s = 3**19
Q,Z = 5**38,s*s
assert 2*norm(a,b) == 5**19-s and 2*norm(c,d) == 5**19+s
assert 2*norm(3051239,274884) == 5**19-3**11
assert 2*norm(157252,1780638) == 5**19+3**11

v,w = 4*(a*c-3*b*d),4*(a*d+b*c)
assert v%8 == w%8 == 0 and 16*norm(v//8,w//8) == Q-Z
for k,j,p,h in ((0,5,7,7),(1,49,23,207)):
    assert Q == 5**(38*3**k) and Z == 3**(38*3**k) == s*s
    assert norm(v,w) == 4*(Q-Z) and w > s and w%3
    for good,t in ((True,w),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            r,S = t+s,x*x+y*y
            n = 5*Q+lam*Z-S
            assert S > lam*Z and Q < n < 5*Q
            assert n%24 == (21 if lam == 1 else 3)
            assert 2*lam*Z-S == r*r-3*t*t
            R = n-Q-(4-lam)*Z
            if good:
                assert R == v*v+r*r
            else:
                assert R%(p*p) == h and h%p == 0 and h != 0
    a,b = (Q-Z)//2,(Q+Z)//2
    v,w = a*v+3*b*w,a*w-b*v
    Q,Z,s = Q**3,Z**3,s**3

phases = [F(18),F(22),F(26),F(82,3),F(30),F(34),
          F(38),F(42),F(142,3),F(54)]
assert max(b/a for a,b in zip(phases,phases[1:])) == F(11,9)
```

The population theorem counts generated targets. The failed controls concern their specified positive exponent pairs.
