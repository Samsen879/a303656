# Eight interlaced sphere rays and a fixed-formula seed obstruction

The seed **\((m,e)=(142,78)\)** fills the \(42\)–\(54\) gap at normalized phase \(142/3\). The same lower exponent also admits \(e=74\), and the same composition gives a second new phase, \(30\), from \((90,46)\). With both new phases, the eight rays give
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{17/42}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda\in\{1,3\},
\]
effectively for all sufficiently large \(X\). Here \(A_\lambda\) counts distinct generated targets in class \(\lambda\bmod4\). The exponent \(17/42\) is sharp in the liminf for these eight rays.

### What repeats, and where it stops

For odd \(u,v\) with \(5^u>3^v\), put
\[
H_\pm=\frac{5^u\pm3^v}{2}.
\]
These halves are coprime, and \(5^{2u}-3^{2v}=4H_-H_+\). The Eisenstein norm criterion therefore applies to the halves separately. Each prime \(p\equiv2\bmod3\) must have even valuation in its half. The dyadic condition can be met for every odd \(u\) by taking \(v\equiv u\bmod4\), which gives \(v_2(H_+)=2\). The odd factors still need an exact norm certificate.

At \(u=71\), the choice \(v=39\) gives \(v_2(H_+)=2\), and \(v=37\) gives \(v_2(H_+)=4\). For both choices the replay verifies the two half norms directly, without needing any factorization or primality certificates. The nearby choice \(v=41\) instead gives \(v_2(5^{142}-3^{82})=5\), so the seed fails. This gives a repeatable test with a genuinely variable \(3\)-exponent. Establishing bounded spacing requires a way to supply new half-norm certificates across the lower exponents.

There is a quantitative obstruction to doing that with a **fixed menu of rational formulas**. For any fixed rational functions \(R,T\) with real coefficients, only finitely many pairs \((u,v)\) satisfy
\[
R(5^u,3^v)^2+3T(5^u,3^v)^2=5^{2u}-3^{2v}
\]
where both functions are defined. With a common denominator \(H\), clearing denominators gives a nonzero polynomial \(P(X,Y)\): an identity would assert that a sum of squares is negative on \(0<X<Y\) away from the poles. At any power-pair zero of \(P\), take a minimal vanishing set of monomials and divide by one of them. The normalized ratios lie in a group of rank at most two, and the resulting unit equation is nondegenerate. Evertse–Schlickewei–Schmidt bounds the number of ratio tuples in terms of the number of monomials alone. Each tuple fixes \(u\) or \(v\) through a \(5\)-adic or \(3\)-adic valuation. On the remaining one-variable slice, \(P\) has at most \(\deg P\) roots. An identically zero slice either has an identically zero denominator or contradicts the same real sign test. [Evertse–Schlickewei–Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04)

Thus a chart of bounded degree supplies only a bounded number of base pairs, uniformly in its coefficients. Even allowing cubing, a scheme that covers at least \(\delta U\) distinct half-exponents \(u\le U\) needs \(\gg_{\delta,D} U\) distinct charts of degree at most \(D\). Indeed, depths at least \(K\) supply only multiples of \(3^K\), and one can fix \(K\) with \(3^{-K}<\delta/2\). The factor choices in the actual certificates vary with the exponents and fall outside this fixed-formula restriction.

### Both classes and the new spacing

For either new seed, put \(Q=5^{m3^k}\), \(Z=3^{e3^k}\). The cubing construction supplies \(v^2+3w^2=4(Q-Z)\). For \(\lambda=1,3\), let \(S=x^2+y^2=3w^2+2\lambda Z-r^2>\lambda Z\) with \(r\) odd. Then
\[
n=5Q+\lambda Z-S
 =Q+(4-\lambda)Z+v^2+r^2,\qquad Q<n<5Q.
\]
The positive exponent pair is \((e3^k+\mathbf 1_{\lambda=1},\,m3^k)\). The retained orientations give the classes \(21\bmod24\) and \(3\bmod24\), respectively. The effective count carries over because \(Z\le Q^{\log3/\log5}\) and, on writing \(3w^2+2\lambda Z=3df^2\), the real norm \(\operatorname{Norm}(|w|+f\sqrt d)=-2\lambda Z/3\) still has support only at \(2,3\). Thus the exceptional-character deletion stays bounded, and the per-height count remains \(\gg_\varepsilon 2^k\sqrt Q/(\log Q)^{1+\log 2+\varepsilon}\) in each class. [Effective orientation count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The phases are \(18,22,26,82/3,30,34,42,142/3,54\), with \(54\) starting the next cycle. Adding \(142/3\) alone gives \(41/102\). With phase \(30\) as well, the largest ratio is \(42/34=21/17\). The last completed window ends above \(X^{17/21}\), giving the stated count. At \(X=5^{42\cdot3^j}\), the preceding lower power is \(5^{34\cdot3^j}\), and even all norm orientations yield only \(Q^{1/2+o(1)}\) targets per height. That gives the matching liminf ceiling.

### Exact replay

The failed signed control uses the same new height and correct odd classes. It has both signed norm identities, but its residual for the prescribed positive pair has \(7\)-valuation one.

```python
from fractions import Fraction as F

def norm(z):
    a,b = z
    return a*a + 3*b*b

def mul(z,t):
    a,b = z
    c,d = t
    return a*c-3*b*d, a*d+b*c

def signed(Q,Z,s,w,lam):
    x,y = (w-s,w) if lam == 1 else (w+s,w-2*s)
    S,r = x*x+y*y,w+s
    n = 5*Q+lam*Z-S
    assert S > lam*Z and 2*lam*Z-S == r*r-3*w*w
    assert Q < n < 5*Q and n%24 == (21 if lam == 1 else 3)
    return n,r

rows = [
    (142,78,(2262530631493322184585551,2313495106464959091760076),
            (4211331587784822801624628,1070904592557661319157598)),
    (142,74,(2880370095179268109631959,2071979069726532609835470),
            (4348202611821540406788884,869666167351174445534936)),
    (90,46,(3130211868925979,1212796818767394),
           (92387142908272,2175800184685108)),
]
for m,e,U,V in rows:
    q,s = 5**(m//2),3**(e//2)
    assert 2*norm(U) == q-s and 2*norm(V) == q+s
    Q,Z = q*q,s*s
    v,w = (4*c for c in mul(U,V))
    for k in range(2):
        assert Q == 5**(m*3**k) and Z == 3**(e*3**k) == s*s
        assert norm((v,w)) == 4*(Q-Z) and w > s and w%3
        for lam in (1,3):
            n,r = signed(Q,Z,s,w,lam)
            assert n == Q+(4-lam)*Z+v*v+r*r
        a,b = (Q-Z)//2,(Q+Z)//2
        choices = [mul((v,w),(a,j*b)) for j in (1,-1)]
        v,w = max(((x,abs(y)) for x,y in choices if y%3),
                  key=lambda z:z[1])
        Q,Z,s = Q**3,Z**3,s**3

Q,Z,s = 5**142,3**78,3**39
for lam in (1,3):
    n,_ = signed(Q,Z,s,s+5,lam)
    assert (n-Q-(4-lam)*Z)%49 == 7
assert (Q-3**82)%64 == 32
p = list(map(F,[18,22,26]))+[F(82,3),F(30),F(34),F(42),F(142,3),F(54)]
assert max(y/x for x,y in zip(p,p[1:])) == F(21,17)
```

The bound counts generated targets only. The signed failure concerns its prescribed positive pair, and bounded spacing for unrestricted admissible seeds remains open.
