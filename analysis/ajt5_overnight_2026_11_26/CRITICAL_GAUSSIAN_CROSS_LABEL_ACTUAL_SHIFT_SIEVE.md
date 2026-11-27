# Cross-label second-moment saving from the actual four shift differences

This extends [the Gaussian critical-band analysis](https://github.com/Samsen879/a303656/commit/a156012c35c99c312ff4f2c0f32ba1fcc8859a2a) to genuinely different numerical labels, across the full gap range. The uniform per-pair factor \(K^{-\eta}\), up to powers of \(\log K\), does not absorb the \(O(K^4)\) number of label pairs. The full \(O(X)\) second moment remains open. The native positive collision and both matched failures below were independently replayed.

The moment step uses only the discriminant-uniform **upper** bound (the published erratum preserves that bound and supplies the corrected version). All four factors are distinct and monic, with coefficients polynomially bounded at the needed height. At a bad prime, if the largest requested valuation is \(v\ge1\), the local exact valuation count over modulus \(p^{v+1}\) is at most \(p\): fix a linear factor attaining \(v\). The local weights grow only polynomially in \(v\), giving a uniform \(1+O(1/p)\) bound. The total loss over the actual bad-prime factors is therefore at most a fixed power of \(1+\log K\).

### Cross-label bound

Let \(X=2^K\), and let \(\mu_i(n)\) count distinct numerical seeds \(q\) for label \(i=(r_i,s_i)\) in the fixed \(t=8\) band. For distinct labels \(i,j\), uniformly over the original height restrictions,
\[
\sum_{X\le n<2X}\mu_i(n)\mu_j(n)
 \ll \frac{X}{K^\eta}(1+\log K)^C,
\qquad
\eta=\frac{17-8\,2^{3/4}}5>0.70,
\]
for an absolute constant \(C\). Summing over labels gives \(O(XK^{4-\eta}(1+\log K)^C)\) for the cross-label contribution. This improves the angle-free bound, but it is still larger than \(X\). It gives neither a full second-moment bound of order \(X\) nor a density conclusion.

### Where the four differences enter

Write \(H=3A+5B,\ J=A+B\), so \(S=n-H,\ R=n-J\). Every certificate forces **both \(S\) and \(R\) individually** to be Gaussian norms. In fact, \(q\mid D^2+4w^2\) and the numerical norm condition on \(q\) give a Gaussian factorization
\[
D+2iw=\alpha\beta,\qquad N(\alpha)=q.
\]
At split primes one allocates the required factors between the two conjugate primes. At inert primes the exponent in \(q\) is even, so the required rational prime power divides \(D+2iw\). The numbers \(\beta-\bar\alpha\) and \(\beta+\bar\alpha\) have norms \(2S\) and \(2R\), and division by \(1+i\) gives the claimed norms.

Use this factorization for label \(i\) and write \(\alpha=f(a+ib)\), \(\beta=c+id\), with \(f\mid D\), \((a,b)=1\) and \(a\ge |b|\). Then
\[
ac-bd=D/f,\qquad a\asymp \frac{\sqrt X}{fK}.
\]
The critical band gives \(2w/q=8\sqrt2K+O(1)\). In particular \(d\) lies in an interval of length \(O(fa)\) centred at \(8\sqrt2Kfa\). This short interval is the angular input.

For label \(j\), put \(e_1=H-H'\) and \(e_2=H-J'\). Its two shifts are \(S+e_1,S+e_2\). At an inert prime \(\ell\) away from \(2af(H'-J')\) and the four cross differences, set \(Q=f^2(a^2+b^2)\) and \(y=\Im(\alpha\beta)\). The determinant equation determines \(c\bmod\ell\) from \(b,d\), and the map \(d\mapsto y\) has unit slope because \(-1\) is nonsquare. For either \(e=e_1,e_2\),
\[
S+e\equiv0\pmod\ell
\quad\Longleftrightarrow\quad
y^2=-(Q-D)^2-2eQ\pmod\ell.
\]
The right side, regarded first as a quadratic in \(Q\), has discriminant \(4e(e-2D)\). The two discriminants thus contain exactly the four cross differences
\[
H-H',\quad J-H',\quad H-J',\quad J-J'.
\]
After substituting \(Q=f^2(a^2+b^2)\), the polynomial in \(b\) still has a simple root over the algebraic closure: the two roots in \(Q\) are distinct and at most one can correspond to \(b=0\). The quadratic character bound gives \(\ell+O(\sqrt\ell)\) solutions for each shift. Apart from at most four roots with \(y=0\), the lift in \(d\) is simple. The two shifts give disjoint residue sets modulo \(\ell\). Consequently the density of the forbidden event “one of the second label’s shifts has valuation exactly one” among \((b,d)\bmod\ell^2\) is
\[
\rho(\ell)=\frac2\ell+O(\ell^{-3/2}).
\]
This is a necessary norm test for label \(j\). [Weil, *On Some Exponential Sums*](https://pmc.ncbi.nlm.nih.gov/articles/PMC1079093/).

### Counting with that test

For each fixed \(f,a\), sieve the determinant congruence \(bd\equiv-D/f\bmod a\) over the two interval coordinates. For squarefree \(m\) made of good sieving primes, CRT gives \(O(C^{\omega(m)}m^3)\) forbidden residue pairs modulo \(m^2\). The step \(m^2\) is coprime to \(a\). Completing the two interval progressions gives principal density \(\rho(m)=\prod_{\ell\mid m}\rho(\ell)\) and error
\[
O_\epsilon\!\left(fa^{1/2+\epsilon}\sqrt{D/f}\right)
\]
per residue pair. This uses the complete Kloosterman bound with its gcd factor, summed over common frequency divisors. Rounding the two interval counts fits within the same error. [Estermann, *On Kloosterman’s sum*](https://www.cambridge.org/core/journals/mathematika/article/abs/on-kloostermans-sum/DED1120FD0994F590EA6E980D07D0F43).

Use Selberg weights supported on divisors up to \(z=X^{1/100}\). The density \(2/\ell\) on inert primes gives sieve dimension one. Omitting the primes in the bad product costs at most \((1+\log K)^C\), since that product is polynomially bounded in \(X\). The squared weights reach \(m\le z^2\). Summing the errors over those \(m\), over \(a\asymp\sqrt X/(fK)\), and over \(f\mid D\) costs \(O_\epsilon(z^8X^{25/32+\epsilon})\), which is power-smaller than the principal bound. Hence
\[
\sum_n\mu_i(n)\mathbf1_{\mu_j(n)>0}
 \ll \frac{X}{K^3}(1+\log K)^C .
\tag{1}
\]
The factor \(K^{-2}\) comes from the first label’s critical band, and the additional \(K^{-1}\) comes from the second label’s two inert-prime tests. Gaussian-coordinate aliases can only enlarge this upper bound. [Williams, *Mertens’ theorem for arithmetic progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf).

To include the second label’s multiplicity, set \(W=\mu_i\mu_j\). Equation (1) in both directions bounds \(\sum_n W^{1/2}\). Also \(\mu_i\le r_2(S_i)r_2(R_i)/4\), since \(S_i,R_i\) are norms on certificate support. Apply Henriot’s corrected discriminant-uniform upper bound to the four distinct monic linear shifts with the multiplicative function \((r_2/4)^{7/4}\) on each. Its prime-power values are divisor-bounded. At good split primes the four first-order weights are \(2^{7/4}\) each. At inert primes they vanish. The resulting bound is \(XK^{4(2^{3/4}-1)}(1+\log K)^C\) for \(\sum W^{7/4}\). The bad Euler factors are \(1+O(1/\ell)\), since a specified maximal valuation of any linear shift confines \(n\) to one class modulo that prime power. Hölder with exponents \(3/5,2/5\) on \(W^{1/2},W^{7/4}\) gives the claimed \(\eta\). [Henriot, discriminant-uniform bound](https://doi.org/10.1017/S0305004111000752) · [Erratum](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf/nairtenenbaum_uniform_with_respect_to_the_discriminanterratum.pdf).

### Standalone exact controls

The positive pair uses labels \((3,4)\) and \((5,4)\), with actual \(k=300\). Its circle norms have gcd **40**, so it is genuinely in the large-denominator cross-label region. Conjugating one of the second label’s coordinates preserves its certificate equation and fails the band. Perturbing the first-label construction by \(u\mapsto u+2\) retains its certificate and forces \(v_7(n-J')=1\), excluding **every** seed at the second label.

```python
from math import gcd, prod

B, u, a = 25**4, 472951892684017552074359691128816302960416, 3395
A = 9**3
C = A+2*B-(a*a+1)//2

def first(u):
    x = a*u+C
    return x*x+u*u+3*A+5*B, (x,u), (x+1,a-u)

def cert(n,r,Z,R):
    A = 9**r
    D, S = A+2*B, n-3*A-5*B
    assert A<=B and B**16<=n<=A**32
    assert S.bit_length()-1==300
    x,y = Z
    v,w = R
    assert x*x+y*y==S and v*v+w*w==S+2*D
    f,g = x-v,y-w
    assert f%2 and g%2 and (x*w-y*v)%2==0
    q = ((f+g)//2)**2+((f-g)//2)**2
    w = abs(x*w-y*v)//2
    assert q%2 and 2*q*S==(D-q)**2+4*w*w
    return q, 64*300**2*q<=S<=64*300*301*q

n,Z,W = first(u)
V = (607410763822442259841404666945642760763528316,
     1486349191038268230937114062551772143991609494)
T = (608285098757375500972063850274213712214731511,
     1485991585553971787286526417919416493370082037)
q,ok = cert(n,3,Z,W)
qq,ok2 = cert(n,5,V,T)
assert ok and ok2 and abs(q-qq).bit_length()==270
assert not cert(n,5,V,(T[0],-T[1]))[1]

L1,L2 = (3*9**3+5*B,9**3+B), (3*9**5+5*B,9**5+B)
M1,M2 = (prod(n-h for h in L) for L in (L1,L2))
assert gcd(M1,M2)==40 and (M1//40)**4>(1<<300)**7

nf,Z,W = first(u+2)
assert cert(nf,3,Z,W)[1] and B**16<=nf<=9**(5*32)
assert prod(abs(h-j) for h in L1 for j in L2)%7
assert (nf-L2[1])%7==0 and (nf-L2[1])%49!=0
```
