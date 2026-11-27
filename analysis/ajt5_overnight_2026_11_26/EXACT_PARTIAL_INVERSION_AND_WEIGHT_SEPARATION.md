# Exact partial inversion and separation of weighted and distinct observations

Exact inversion of the small split-prime multiplicities preserves the positive sign across **all 105 nonblocked phases**. It still leaves a factor of order \((\log\log B)^3\) between the resulting count and the distinct-pair count. There is also a two-sided obstruction to using the original representation weights. In both target classes, a set carrying \(1-o(1)\) of the representation weight carries \(o(1)\) of the distinct pairs. The distinct-pair sign remains open.

## Exact inverse multiplicity up to a growing cutoff

Keep the anchor \(S_0=3^a+25\cdot5^b\), label \(S=3^c+5^e\), shift \(\kappa=(S_0-S)/45\), and target \(n=S_0+45u\). Use the original even \(a,b\), balance strip \(39/40<5^b/3^a<122/125\), and sharp window
\[
1457\cdot3^a-123\cdot5^b<n\le729\cdot3^a+625\cdot5^b.
\]
The label limits are \(a/10\le c\le a/3,\ b/5\le e\le b/3,\ c\equiv a\pmod4,\ e\equiv b+2\pmod6\). Compare \(r=0\) and \(r=r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). Write \(B=5^b\), \(v=u+\kappa\), and \(W=r_2(u)r_2(v)\). All counts below use the same sharp window and coarse class \(n\equiv S_0\pmod{45}\).

For a nonblocked label, let \(D_r\) count distinct true pairs in class \(r\). Let \(L_2=\log\log B\), \(z=B^{1/L_2^3}\), and set
\[
A_z(u)=\prod_{\substack{q\le z\\q\equiv1\ (4)}}
\frac{1}{(1+v_q(u))(1+v_q(v))},
\qquad
V_{z,r}=\sum_{n\equiv r\ (49)}\frac{W}{16}A_z(u).
\]
This removes **all powers** of each split prime up to \(z\), including primes dividing \(\kappa\).

Uniformly over the nonblocked labels, the leading term of \(V_{z,r}\) has the same ratio between the two classes as the original representation count. The ratio is \(1\) in the 98 unit phases and \(7/8\) in the seven zero-mod-49 phases. Its size per label is
\[
V_{z,r}\asymp F_I(\kappa)\frac{B}{\log z},
\qquad
F_I(\kappa)=\prod_{\substack{q\mid\kappa\\q\equiv3\ (4)}}\frac{q-1}{q-2}.
\]
Consequently the excess over the full nonblocked grid is \(\gg B(\log B)^2/\log z\). The distinct bounds from the enlarged split-supported marking and the unmarked upper sieve give \(D_r\asymp F_I(\kappa)B/\log B\) on these same cells. Thus \(V_{z,r}/D_r\asymp L_2^3\) in **each** class.

### Why the local calculation is uniform

The fixed-congruence circle-method argument extends to an extra modulus \(d\) with error \(O(d^C B^{1-\gamma})\) for absolute \(C,\gamma>0\). Here \(d\) is supported on split primes, and the congruence may be any bounded function of \(u\bmod d\). To track the dependence, use coordinate classes modulo \(M=98d\) after the change to the split bilinear form. The finite Fourier expansion of one class has at most \(M^4\) terms. Weil’s bound for each bilinear complete sum is independent of \(M\), and replacing the Poisson frequency by its value divided by \(M\) costs only a fixed power of \(M\) in the integral estimates. Summing the coordinate classes costs another \(M^4\). The endpoint smoothing has fixed derivative order and the local main term of any selection is bounded by the unrestricted one. This gives the polynomial modulus loss in the sharp window. In particular, all moduli \(B^{o(1)}\) used below retain a power saving. [Heath-Brown’s quadratic-form circle method](https://ora.ox.ac.uk/objects/uuid%3Abbd3c62f-f010-44b5-8be5-87e903fb0084/files/m7ec02df6e1b8303a66e7a6015ecb6044)

Normalize \(W\) to a probability measure in either target class. At a split prime \(q\), put \(G_q(t)=(1+v_q(t))(1+v_q(t+\kappa))\). The local law has density proportional to \(G_q\) against Haar measure on \(\mathbb Z_q\). Its normalizer satisfies
\[
(1-1/q)^2\int_{\mathbb Z_q} G_q(t)\,dt
=\sigma_q(\kappa)
=(1-q^{-2})\sum_{j=0}^{v_q(\kappa)}q^{-j}.
\]
Thus the local expected reciprocal is \((1-1/q)^2/\sigma_q(\kappa)\). The main terms for finitely many split primes multiply by CRT and are the same in the two 7-adic classes.

The local integral can also be computed by expanding each valuation into divisibility indicators. The cross-terms with minimum index \(j\ge1\) vanish unless \(q^j\mid\kappa\), and otherwise sum to \(q^{-j}(1+2/(q-1))\). The zero-minimum terms give \(1+2/(q-1)\), proving the stated normalization.

To use this product for all \(q\le z\), truncate valuations at \(K=C_A L_2\). The weighted probability of \(v_q(u)\ge K+1\), or of the corresponding event for \(v\), is \(O((K+1)^2q^{-K-1})\) in the local law. On that ball each factor in \(G_q\) has second moment \(O((K+1)^2)\), which gives the bound even when \(q\mid\kappa\). The sum of the truncation errors is \(O_A((\log B)^{-A})\) with sufficiently large \(C_A\).

For the resulting factors \(f_q\in[0,1]\), apply Bonferroni to \(\prod_q(1-(1-f_q))\) through \(C'_A L_2\) terms. The sum of the local means of \(1-f_q\) is \(O(L_2)\), so the first omitted elementary symmetric sum is \(O_A((\log B)^{-A})\) for large enough \(C'_A\). Each intersection uses a modulus at most \(z^{O(L_2^2)}=B^{o(1)}\), and the number of terms is \(B^{o(1)}\). Therefore in either class
\[
\mathbb E_{W,r}[A_z]
=\prod_{\substack{q\le z\\q\equiv1\ (4)}}
\frac{(1-1/q)^2}{\sigma_q(\kappa)}
+O_A((\log B)^{-A}).
\]
Multiplying by the representation asymptotic cancels the small split factors exactly. Split factors above \(z\) have product \(1+o(1)\) uniformly since \(\kappa\asymp B\). The remaining inert product is \(\asymp F_I(\kappa)\), and the split Mertens product is \(\asymp1/\log z\). This also gives an error \(o(B/\log z)\) per label, so the 98 unit phases cannot compensate for the seven positive leading differences in this partially inverted count.

## Where the distinct mass lies

There is a quantitative separation even before partial inversion. Define
\[
X=\sum_{\substack{q\le z,\ q\equiv1\ (4)\\q\nmid\kappa}}
\left(1_{q\mid u}+1_{q\mid v}\right),
\qquad {\cal H}=\{X\ge(7/4)L_2\}.
\]
Uniformly in every nonblocked cell, for some absolute \(c_0>0\),
\[
\frac{\sum_{{\cal H}^c}W}{\sum W}\ll(\log B)^{-c_0},
\qquad
\frac{D_r({\cal H})}{D_r}
\ll
\frac{\sqrt{L_2}}{(\log B)^{(7/4)\log 2-1}} .
\]
These compare masses within each fixed class and label.

For \(q\nmid\kappa\) the two divisibility events are disjoint. Their union has probability
\[
\rho_q=\frac{2(2q-1)}{q(q+1)}=\frac4q+O(q^{-2})
\]
under the representation-weighted local law. The sum of these probabilities is \(2L_2+O(\log L_2)\). The same uniform modulus estimate matches the first \(O(L_2)\) centered moments of \(X\) to those of independent Bernoulli variables with probabilities \(\rho_q\), with error \(B^{-\gamma+o(1)}\). Indeed the expansion uses at most \(z^{O(L_2)}\) terms and moduli of that size. The Bernoulli moment bound \(\mathbb E|X-\mathbb EX|^{2j}\ll(CjL_2)^j\) follows from the exponential moment bound for \(|t|\le1\). Taking \(j\) a sufficiently small fixed multiple of \(L_2\) gives the first inequality. On \({\cal H}\), \(W\ge16\,2^{(7/4)L_2}\). The representation bound gives \(\sum W/D_r\ll\log B\sqrt{L_2}\), which gives the second inequality.

Thus the positive representation excess survives on \({\cal H}\), while almost all distinct pairs in both classes lie on its complement. The exact statistic still needed after partial inversion is
\[
D_r
=V_{z,r}\,
\mathbb E_{V_z,r}\!\left[
\prod_{\substack{q>z\\q\equiv1\ (4)}}
\frac{1}{(1+v_q(u))(1+v_q(v))}
\right].
\]
The expectation has order \(L_2^{-3}\) in each class. Its signed comparison remains unresolved. Chamizo’s Theorem 1.1 controls the unrestricted **representation** correlation for shifts of the size used here. Freiberg–Kurlberg–Rosenzweig’s Conjecture 1.1 concerns the **indicator** correlation for fixed shifts. The former supplies no reciprocal tail comparison, and the latter does not give a theorem for these growing shifts in fixed residue classes. [Chamizo, Theorem 1.1](https://link.springer.com/article/10.1007/s00009-021-01959-3) · [Freiberg–Kurlberg–Rosenzweig, Conjecture 1.1](https://arxiv.org/html/1701.01157v1)

## Exact replay

The first check uses two actual labels in the narrow balanced strip. The second reuses two existing ordinary-window targets at the same deep label on the smaller \((a,b)=(52,36)\) fixture, outside the narrow strip. Each target contributes one distinct pair. Their weights are \(768\) and \(32\).

```python
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt, prod

def norms(m):
    return Counter((x*x+y*y) % m for x in range(m) for y in range(m))

A, B = 3**712, 5**486
assert 39*A < 40*B and 125*B < 122*A
S0 = A + 25*B
r = (pow(3,716,49) + pow(5,488,49) + 7) % 49
N = norms(49)
for c,e,ratio in [(72,98,Fraction(1)), (80,122,Fraction(7,8))]:
    S = 3**c + 5**e
    k, rem = divmod(S0-S, 45)
    assert rem == k % 8 == 0
    inv = pow(45,-1,49)
    def w(t):
        return N[(t-S0)*inv % 49] * N[(t-S)*inv % 49]
    assert Fraction(w(r),w(0)) == ratio
    p = 13
    P = norms(p)
    W = [P[u]*P[(u+k)%p] for u in range(p)]
    assert k%p and Fraction(W[0]+W[-k%p],sum(W)) == Fraction(2*(2*p-1),p*(p+1))

cert = {
    3457555897226619419244977: (11563666243,3629366173),
    642461230011986270401: (156186067,2237),
    11563666243: (1927277707,),
    3629366173: (725293,),
    1927277707: (321212951,),
}
def prime(p):
    if p not in cert:
        return p >= 2 and all(p%d for d in range(2,isqrt(p)+1))
    F = prod(cert[p])
    return ((p-1)%F == 0 and F*F > p and pow(2,p-1,p) == 1
            and all(prime(q) and gcd(pow(2,(p-1)//q,p)-1,p) == 1
                    for q in cert[p]))

def r2(n, factors):
    assert prod(q**j for q,j in factors) == n
    assert all(prime(q) and (q%4 != 3 or j%2 == 0) for q,j in factors)
    return 4*prod(j+1 for q,j in factors if q%4 == 1)

A, B = 3**52, 5**36
S0, S = A+25*B, 3**8+5**8
r = (pow(3,56,49)+pow(5,38,49)+7)%49
for x, phase, f, g, expected in [
    (12696151452849, 0, [(3,10),(1269901,2),(41143,2)],
     [(5,1),(13,1),(4057,1),(642461230011986270401,1)], 768),
    (12696151464813, r, [(3,2),(43,2),(467,2),(210748991,2)],
     [(7,2),(3457555897226619419244977,1)], 32),
]:
    n = S0 + 45*x*x
    assert 1457*A-123*B < n <= 729*A+625*B and n%49 == phase
    assert r2(x*x,f)*r2(x*x+(S0-S)//45,g) == expected
```
