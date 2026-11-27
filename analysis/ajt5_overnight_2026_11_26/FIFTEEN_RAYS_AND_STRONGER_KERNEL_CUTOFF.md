# Fifteen sphere rays and a stronger effective smooth-kernel cutoff

**Phase \(110/3\) closes the \(34\)–\(38\) gap**, using the exact seed \((m,e)=(110,30)\). It comes from multiplying the old label \((22,6)\) by \(5\). The fifteen rays now give, in each odd class modulo \(4\),
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{35/78}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda=1,3,
\]
effectively for sufficiently large \(X\). This counts distinct generated targets.

**The smooth-kernel threshold also improves.** Write \(L_j(U)\) for the \(j\)-fold iterated logarithm. For every fixed \(0<\theta<1\), there is an effective \(\kappa_\theta>0\) such that only \(O_\theta(U^\theta)\) half-exponents \(u\le U\) have an admissible partner for which either half’s squarefree kernel is supported on primes up to
\[
y=\kappa_\theta L_1(U)L_2(U)L_3(U).
\]
The same bound holds after cubing the restricted base seeds. This removes the slowly diverging divisor in the previous cutoff. No numerical onset is supplied here.

### Exceptional-zero audit and abelian range

For squarefree \(d\) supported on primes \(\ell\ge7\), put
\[
E_d=\mathbb Q(\zeta_{3d}),\qquad
K_d=E_d(5^{1/\ell},3^{1/\ell}:\ell\mid d).
\]
The earlier Stark estimate is valid. The degree is \(2\varphi(d)d^2\), and the root discriminant is at most \(3d^5\) by the cyclotomic and radical polynomial discriminants. In Stark’s bound quoted by Lagarias–Odlyzko, both terms in the lower bound for \(1-\beta\) are therefore \(\gg d^{-5}\). [Lagarias–Odlyzko, Theorems 1.3–1.4](https://aareyanmanzoor.github.io/assets/articles/lagarias-odlyzko.pdf#page=5)

There is a sharper audit for these particular fields. The group \(\operatorname{Gal}(K_d/E_d)\) is abelian of odd order. In the Hecke factorization of \(\zeta_{K_d}\), the nontrivial characters occur in conjugate pairs, so a **simple real** exceptional zero comes from \(\zeta_{E_d}\). The Dirichlet factorization of \(\zeta_{E_d}\) then puts it in a real primitive character of conductor \(q\mid3d\). The class-number formula gives \(L(1,\chi)\gg q^{-1/2}\), effectively. Splitting the derivative series at \(q\) and bounding the tail by periodic summation gives \(L'(\sigma,\chi)\ll\log^2(3q)\) near \(1\). Hence
\[
1-\beta\gg \frac{1}{\sqrt{3d}\log^2(3d)}.
\]

The prime intersections used in the sieve have \(p\equiv1\bmod3d\), so their Frobenius classes lie in \(\operatorname{Gal}(K_d/E_d)\). This is the abelian subgroup required by Thorner–Zaman’s Theorem 1.4. The logarithm of its conductor parameter is \(O(d\log(3d))\). Indeed, for a cyclic degree-\(\ell\) radical extension, the conductor–discriminant formula bounds each nontrivial character’s conductor using the polynomial discriminant to the power \(1/(\ell-1)\). Multiplying those bounds over the radicals, and including the degree and discriminant of \(E_d\), gives the claimed size. The exceptional term has the subtractive sign on the counted classes, and the gap estimate above makes it negligible even in the signed sieve sum. With \(R=(\log y)^{2/5}\), for all squarefree \(d\le R^2\) the intersection count is uniformly
\[
\frac{\operatorname{Li}(y)}{2d}
  +O_A\!\left(\frac{y}{(\log y)^A}\right)
\]
for every fixed \(A\). This enlarges the analytic range of \(R\). The gain in the kernel cutoff comes from the arithmetic reduction below. [Thorner–Zaman, Theorem 1.4](https://arxiv.org/pdf/1803.02823#page=3)

### Why the divisor loss disappears

Let \(H_\pm=(5^u\pm3^v)/2\) with \(u,v\) odd. Strip the entire \(R\)-smooth part \(g\) of \(\gcd(u,v)\), writing \(u=gu_0,\ v=gv_0\). For \(p>R\), if \(p\) divides the reduced half \((5^{u_0}\pm3^{v_0})/2\), its valuation there equals its valuation in \(H_\pm\), by LTE and \(p\nmid g\). Thus a \(y\)-smooth kernel stays \(y\)-smooth after reduction. Above \(R\), its kernel primes also still satisfy \(p\equiv1\bmod3\).

Now \((u_0,v_0)\) is nonzero modulo **every** sieve prime \(7\le\ell\le R\), so all those primes can be used. At \(p\equiv1\bmod\ell\), the necessary residue-log relation \(u_0 a_\ell=v_0 b_\ell\) is one nonzero linear equation. Its failure has density \(1/\ell\) among rational primes, and intersections over \(\ell\mid d\) have the densities used above. The Selberg quadratic form with weights supported on squarefree divisors \(d\le R\) has optimum \(1/G\), where
\[
G=\sum_{\substack{r\le R\\(r,30)=1}}\frac{\mu^2(r)}{\varphi(r)}
\gg\log R.
\]
The weights have absolute value at most \(d\), so the uniform intersection errors are summable. Each frozen reduced phase therefore has \(O(y/(\log y\log R))\) possible kernel primes above \(R\).

There are \(\exp(O(R\log R))\) reduced phase patterns. The small primes below \(R\) add at most \(2^{\pi(R)}\) kernel choices. Each fixed kernel gives \(O(1)\) exponent pairs uniformly, by the two-term unit equation from \(5x\pm z\sqrt{10C}\) when \((5^{u_0}\pm3^{v_0})/2=Cz^2\). Finally, there are at most \((1+\log U/\log2)^{\pi(R)}=U^{o(1)}\) choices of the restoring multiplier \(g\le U\). This also absorbs any subsequent \(3^k\). Since \(\log R\asymp L_3(U)\), choosing \(\kappa_\theta\) sufficiently small gives \(O_\theta(U^\theta)\). [Evertse–Schlickewei–Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04)

### Phase gain and exact controls

The new consecutive ratios are \(55/51\) and \(57/55\). The largest remaining ratio is \(26/(70/3)=39/35\), giving \(35/78\). At \(X=5^{26\cdot3^j}\), the preceding lower height is \(5^{(70/3)3^j}\), so the all-orientation ceiling \(Q^{1/2+o(1)}\) gives the matching liminf exponent for these fifteen rays. [Effective fixed-height count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The replay verifies the new seed, the same valuation-one prime on each side before and after removing the common factor \(5\), and both odd classes at two depths. At each height it also checks signed witnesses whose prescribed positive residuals fail at a Gaussian inert prime.

```python
from fractions import Fraction as F

def N(a,b):
    return a*a+3*b*b

def orient(a,b,c,d):
    z = [(a*c-3*b*j*d, abs(b*c+a*j*d)) for j in (1,-1)]
    return max((p for p in z if p[1]%3), key=lambda p:p[1])

a,b = 5672065516204784191,5961139456458111376
c,d = 1039944280322874512,6774865164020321818
q,s = 5**55,3**15
assert 2*N(a,b) == q-s and 2*N(c,d) == q+s
for sign,p in ((-1,201769),(1,6103519)):
    for u,v in ((55,15),(11,3)):
        H = (5**u+sign*3**v)//2
        assert H%p == 0 and H%(p*p) != 0

Q,Z = q*q,s*s
v,w = (4*z for z in orient(a,b,c,d))
for k,(j,p,h) in enumerate(((5,23,368),(41,11,66))):
    assert Q == 5**(110*3**k) and Z == 3**(30*3**k) == s*s
    assert N(v,w) == 4*(Q-Z) and w > s and w%3
    for good,t in ((True,w),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            S,r = x*x+y*y,t+s
            n = 5*Q+lam*Z-S
            assert Q<n<5*Q and S>lam*Z and n%24==(21 if lam==1 else 3)
            assert 2*lam*Z-S == r*r-3*t*t
            R = n-Q-(4-lam)*Z
            assert R==v*v+r*r if good else R%(p*p)==h and h%p==0
    v,w = orient(v,w,(Q-Z)//2,(Q+Z)//2)
    Q,Z,s = Q**3,Z**3,s**3

ph = [F(18),F(178,9),F(22),F(70,3),F(26),F(82,3),F(30),F(290,9),
      F(34),F(110,3),F(38),F(42),F(46),F(142,3),F(158,3),F(54)]
assert max(b/a for a,b in zip(ph,ph[1:])) == F(39,35)
```

The kernel theorem restricts a source of seed heights. The population theorem counts the generated sets, and the failure controls test the specified positive exponent pairs.
