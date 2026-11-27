# Raw switched medium-loss comparison below a fixed exponent cutoff

**There is an unconditional comparison for the part of the switched loss whose least additional inert prime is at most \(B^{4/25}\).** For every label in the seven original deep phases, the raw depth-two loss in this range is at most \(48/49\) of the raw depth-zero loss, for sufficiently large \(B\). The proof uses Bombieri–Vinogradov on the actual prime progressions and an explicit half-dimensional sieve bound. After normalizing by the two progression densities, the bounds still allow either sign.

### The range and the comparison

Keep \(A=3^a,\ B=5^b\), with \(a,b\) even and \(39/40<B/A<122/125\). Write
\[
S_0=A+25B,\qquad S=3^c+5^e,\qquad \kappa=(S_0-S)/45.
\]
Use \(a/10\le c\le a/3,\ b/5\le e\le b/3,\ c\equiv a\pmod4,\ e\equiv b+2\pmod6\), and the seven phases with \(S\equiv r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). The anchor is \(n=S_0+45p\), where \(p\equiv1\pmod4\) is prime, in the unchanged window
\[
1457A-123B<n\le729A+625B.
\]
For \(w=1\) use \(n\equiv0\pmod{49}\). For \(w=49\) use \(v_7(p+\kappa)=2\), giving \(n\equiv r_-\pmod{49}\). Their reduced progression densities are \(\alpha_1=1/84\) and \(\alpha_{49}=1/98\), with six lifts in the second class.

Fix \(0<\rho<1/250\) and mark inert primes \(q\in(B^\rho,B^{2\rho}]\), \(r\in(B^{2\rho},B^{3\rho}]\). Let \(K_{\ell,w}^{\le T}\) be the part of the previous switched remainder in which
\[
(p+\kappa)/w=qrtv,\qquad B^{4\rho}<t\le T=B^{4/25},
\]
and \(t\) is the least inert prime of \((p+\kappa)/(wqr)\). Thus \(v\) has no inert prime below \(t\). This is an exact Buchstab decomposition, including when \(t\mid v\). The primes \(q,r,t\) are uniquely determined, and \(q,r\) each have valuation one.

For label \(\ell\), write \(I=(L_p,U_p]\) for the exact prime interval induced by the target window. The sieve main term after division by \(\alpha_w\) is common to both classes:
\[
H_\ell=
 \bigl(\operatorname{Li}(U_p)-\operatorname{Li}(L_p)\bigr)
 \sum_{\substack{q,r,t\ \text{in the stated bands}\\(qrt,\kappa)=1}}
 \frac{V_{\ell,q,r}(t)}{(q-1)(r-1)(t-1)}.
\]
Here \(V_{\ell,q,r}(t)=\prod_{j<t}(1-g(j))\) over inert primes \(j\nmid7\kappa\). The local factor is \(g(j)=1/j\) for \(j=q,r\) and \(1/(j-1)\) otherwise. At \(q\) or \(r\) a sieve hit imposes a **second** power. A prime dividing \(\kappa\) cannot divide \(qrt\), because it would divide the much larger prime \(p\).

Use half-dimensional sieve level \(t^2\) for each triple. With a squarefree sieve divisor \(d\le t^2\), the full prime modulus is \(M_wqrtd\), with \(M_w=196\) or \(1372\). Its size is
\[
O(B^{5\rho}t^3)\le O(B^{5\rho+12/25}),
\]
strictly below the Bombieri–Vinogradov level by a fixed power. Each modulus has only \(O_\rho(1)\) decompositions, since each marked prime exceeds \(B^\rho\) and the three bands are disjoint. Once the triple is fixed, the modulus determines \(d\). This controls the summed progression errors uniformly for the actual shifts and both sharp endpoints. No equidistribution assumption about the exponent labels is needed. [Bombieri, *On the large sieve*](https://doi.org/10.1112/S0025579300005313).

The two sieve bounds at \(s=2\) now give
\[
(f_{1/2}(2)-o(1))H_\ell
\le \frac{K_{\ell,w}^{\le T}}{\alpha_w}
\le (F_{1/2}(2)+o(1))H_\ell,\qquad
\frac{F_{1/2}(2)}{f_{1/2}(2)}
=\frac{2}{\log(3+2\sqrt2)}<\frac87.
\]
The strict inequality follows from the first five terms of the series for \(2\operatorname{arctanh}(1/\sqrt2)\). Multiplying by \(\alpha_{49}/\alpha_1=6/7\) proves the raw \(48/49\) bound. The result is uniform per label, so summing over the actual seven phases preserves it. [Nath and Xie, Lemma 3.6 and §5](https://arxiv.org/html/2501.16723v1#S5).

This range carries genuine loss mass. Put
\[
M_\ell=\frac{B}{(\log B)^{3/2}}
 \prod_{\substack{j\mid\kappa\\j\equiv3\ (4),\ j\ \mathrm{prime}}}\frac{j-1}{j-2}.
\]
For fixed \(\rho\), Mertens’ theorem in the inert prime class gives \(H_\ell\asymp M_\ell((4\rho)^{-1/2}-(4/25)^{-1/2})\). The remaining counts with \(T<t\le B^{1/2-12\rho}\) are \(O(M_\ell)\), by the upper sieve on the count with no additional inert prime through \(T\). Thus as \(\rho\) decreases, the proved band captures \(1-O(\sqrt\rho)\) of each unsigned switched count in the large-\(B\) limit. That does not settle \(\Delta K\): the common main term cancels in the normalized difference, and the normalized upper and lower bounds still overlap, even though the raw comparison is strict. These are counts of failed alternates, not counts of true norms.

### Same-label replay

The six controls use \((a,b,c,e)=(712,486,80,122)\). In each class there is a true alternate, an exact two-inert failure, and an exact four-inert failure in the newly compared range. Both four-inert examples have least additional inert prime \(4211\). All three depth-two controls use \(p+\kappa\equiv49\pmod{343}\).

The primality certificate uses \(Q=2^{378}\). Its modular witness forces each prime divisor of \(p\) to be \(1\bmod Q\). If \(p<Q^3\) were composite, a factorization \(p=(1+Qu)(1+Qv)\) would have \(uv<Q,\ u+v<Q\). The base-\(Q\) digits of \((p-1)/Q\) would then be \(uv,u+v\), with square discriminant. The replay excludes this and certifies the exact inert support by constructing an odd primitive sum of two squares for the remaining cofactor.

```python
from fractions import Fraction
from math import gcd, isqrt, prod

s0 = sum(Fraction(1, 2**j*(2*j+1)) for j in range(5))
assert 2*s0*s0 > Fraction(49, 16)
A, B = 3**712, 5**486
S0, S = A+25*B, 3**80+5**122
k, rem = divmod(S0-S, 45)
L = (1457*A-123*B-S0)//45 + 1
U = (729*A+625*B-S0)//45
r = (pow(3,716,49)+pow(5,488,49)+7)%49
Q = 1 << 378
P = (59, 67, 4211, 4219)
assert 39*A < 40*B and 125*B < 122*A and S%49 == r == 27
assert rem == k%8 == 0 and B < 59**375 < B**2 < 67**375 < B**3
assert B**4 < 4211**375 and 4211**25 < B**4
assert all(t%4 == 3 and all(t%d for d in range(2,isqrt(t)+1)) for t in P)

for w,count,j,s in [(1,0,1088,5), (49,0,88,5), (1,2,429,5),
                    (49,2,952,13), (1,4,209,13), (49,4,173,5)]:
    F = prod(P[:count])
    G = w*F
    f = 4*((isqrt((L+k)//G)+4)//4+j)
    h,rem = divmod(((k+1+Q)*pow(G,-1,2*Q)-f*f-1)%(2*Q),8)
    assert rem == 0
    v = h%2
    for i in range(2,377):
        v += (h-2*v*v-v)%(1<<i)
    x = 1+4*v
    mod = 49 if w == 1 else 7
    want = -S*pow(45*F,-1,49) if w == 1 else pow(F,-1,7)
    z = next(t for t in range(mod) if (t*t+f*f-want)%mod == 0)
    x += Q*((z-x)*pow(Q,-1,mod)%mod)
    m = x*x+f*f
    p = G*m-k
    d,e = divmod((p-1)//Q,Q)
    D = e*e-4*d
    assert L <= p <= U < Q**3 and p%Q == 1 and ((p-1)//Q)%2
    assert pow(s,(p-1)//2,p) == p-1 and (D < 0 or isqrt(D)**2 != D)
    assert gcd(x,f) == gcd(m,7*prod(P)) == 1 and m%2 == 1
    assert (S0+45*p)%49 == (0 if w == 1 else r)
    assert (p+k)%7 != 0 if w == 1 else (p+k)%343 == 49
    print(w, count, p.bit_length(), (p+k)%343)
```
