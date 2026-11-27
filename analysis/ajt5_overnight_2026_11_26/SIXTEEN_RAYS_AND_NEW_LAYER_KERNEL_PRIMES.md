# Sixteen sphere rays and new prime factors in lifted half-kernels

**The seed \((m,e)=(74,10)\) closes the \(70/3\)–\(26\) gap at phase \(74/3\).** The sixteen rays now have maximum consecutive ratio \(79/71\). In each odd class modulo \(4\), they give the effective lower bound
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{71/158}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda=1,3,
\]
for distinct generated targets. The exponent \(71/158\) is sharp in the liminf for these rays.

There is also a **linear lower bound on the largest kernel prime along certain prime-power lifts**. It applies even when a non-cubing multiplier preserves admissibility.

### What an odd multiplier does to the kernels

Let \(A=5^u>B=3^v\) with \(u,v\) odd, and put \(H_\pm(k)=(A^k\pm B^k)/2\) for odd \(k\). The squarefree kernel records the primes of odd valuation. At an odd prime \(p\nmid AB\), write \(o=\operatorname{ord}_p(A/B)\) and \(b=v_p(A^o-B^o)\). The valuation at an active prime is exactly \(b+v_p(k)\), with activity given by
\[
H_-(k):\ o\mid k,\qquad
H_+(k):\ o\mid2k,\ o\nmid k.
\]
Thus a prime in an old half changes kernel membership exactly when \(v_p(k)\) is odd. The valuation at \(2\) stays fixed. [Earlier cyclotomic valuation formulas](https://raw.githubusercontent.com/Samsen879/a303656/945ab5dbf0455c900e60a455d0f1c6a698c9da8d/analysis/ajt5_overnight_2026_11_26/DIVISOR_CLOSED_CYCLOTOMIC_SEED_ORDERS.md)

New primes can be forced. Suppose \(\ell\) is the largest prime divisor of an admissible multiplier \(k\), \(\ell^j\mid k\), \(\ell\nmid A+B\), and \(\ell\not\equiv1\bmod8\). The plus layer
\[
\frac{A^{\ell^j}+B^{\ell^j}}{A^{\ell^{j-1}}+B^{\ell^{j-1}}}
\]
is \(\ell\bmod8\), since \(A\equiv5\) and \(B\equiv3\bmod8\). It is odd and nonsquare. Every prime dividing the layer has exact order \(2\ell^j\): the hypothesis excludes \(\ell\), and LTE excludes a divisor of the denominator. Therefore some such prime occurs to odd valuation. It exceeds \(\ell\), so it cannot divide \(k\), and its odd valuation persists in \(H_+(k)\). Admissibility forces it to split in the Eisenstein field. For \(\ell\ne3\), it is consequently at least \(6\ell^j+1\).

There is a two-sided version that also works for \(\ell\equiv1\bmod8\). Put \(r=(\ell-1)/2\). If
\[
A>4^{r+1}B^{r+1},\qquad \ell\nmid A^2-B^2,
\]
then **each** layer has a new odd-valuation prime, of exact order \(\ell^j\) on the minus side and \(2\ell^j\) on the plus side. To see the nonsquare assertion, write either layer as \((C^\ell\mp D^\ell)/(C\mp D)\) with \(C=A^{\ell^{j-1}},D=B^{\ell^{j-1}}\). Truncate the square-root expansion at degree \(r\) in \(z=\pm D/C\). The coefficients \(\binom{2i}{i}/4^i\) have strictly decreasing \(2\)-adic valuations: the valuation is the binary digit sum of \(i\) minus \(2i\). Because \(C,D\) are odd, multiplying by \(C^{r-i}(\pm D)^i\) preserves this valuation. After multiplying by \(C^r\), the truncation has distance at least \(4^{-r}\) from any integer. The discarded terms have absolute value at most \(4D^{r+1}/C<4^{-r}\). The same order and persistence argument now applies on both sides.

In particular, **every admissible \(5^h\)-lift has a plus-kernel prime at least \(6\cdot5^h+1\)**. On a fixed base this is linear in the lifted half-exponent. The two-sided size condition makes the bound hold for both kernels. The certified transfer \((22,6)\to(110,30)\) gives exact first-layer witnesses \(181\) and \(211\), of orders \(5\) and \(10\), respectively. This pointwise threshold applies to the stated multiplier families. The unrestricted smooth-kernel count retains its previous scope.

### Seed, spacing, and replay

For the new phase, the half norms with \(A=5^{37}\) and \(B=3^5\) are certified below. Cubing gives \(Q=5^{74\cdot3^k}\), \(Z=3^{10\cdot3^k}\). The sphere identity supplies the positive pair \((10\cdot3^k+\mathbf1_{\lambda=1},\,74\cdot3^k)\) in classes \(21\bmod24\) and \(3\bmod24\), respectively. The same size and ternary conditions give the effective per-height count. [Effective fixed-height count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The new adjacent ratios are \(37/35\) and \(39/37\). The maximum moves to \(142/3\)–\(158/3\), so the last completed window ends above \(X^{71/79}\). At \(X=5^{(158/3)3^j}\), the preceding lower power is \(5^{(142/3)3^j}\), giving the matching liminf ceiling by the all-orientation bound.

The replay checks both odd classes at two actual heights. The failed controls have exact signed identities and residual \(59\)-valuation one at their prescribed positive pairs.

```python
from fractions import Fraction as F

def N(a,b):
    return a*a+3*b*b

def orient(a,b,c,d):
    z = [(a*c-3*b*j*d, abs(b*c+a*j*d)) for j in (1,-1)]
    return max((p for p in z if p[1]%3), key=lambda p:p[1])

a,b = 5950650705329,568490473120
c,d = 5788662893786,978292725964
q,s = 5**37,3**5
assert 2*N(a,b) == q-s and 2*N(c,d) == q+s
Q,Z = q*q,s*s
v,w = (4*z for z in orient(a,b,c,d))
for k,(j,h) in enumerate(((53,3245),(25,2596))):
    assert Q == 5**(74*3**k) and Z == 3**(10*3**k) == s*s
    assert N(v,w) == 4*(Q-Z) and w>s and w%3
    for good,t in ((True,w),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            S,r = x*x+y*y,t+s
            n = 5*Q+lam*Z-S
            assert Q<n<5*Q and S>lam*Z and n%24==(21 if lam==1 else 3)
            assert 2*lam*Z-S == r*r-3*t*t
            R = n-Q-(4-lam)*Z
            assert R==v*v+r*r if good else R%59**2==h and h%59==0
    v,w = orient(v,w,(Q-Z)//2,(Q+Z)//2)
    Q,Z,s = Q**3,Z**3,s**3

A,B = 5**11,3**3
assert A > 4**3*B**3 and N(7139528,27887948) == A*A-B*B
assert 2*N(5672065516204784191,5961139456458111376) == A**5-B**5
assert 2*N(1039944280322874512,6774865164020321818) == A**5+B**5
for sign,p,o in ((-1,181,5),(1,211,10)):
    C = (A**5+sign*B**5)//(A+sign*B)
    z = A*pow(B,-1,p)%p
    assert min(d for d in range(1,o+1) if pow(z,d,p)==1) == o
    assert C%p==0 and C%(p*p)!=0 and (A*A-B*B)%p!=0

ph = [F(18),F(178,9),F(22),F(70,3),F(74,3),F(26),F(82,3),F(30),
      F(290,9),F(34),F(110,3),F(38),F(42),F(46),F(142,3),F(158,3),F(54)]
assert max(b/a for a,b in zip(ph,ph[1:])) == F(79,71)
```

The population estimate counts the generated sets. The failed controls concern their specified positive exponent pairs.
