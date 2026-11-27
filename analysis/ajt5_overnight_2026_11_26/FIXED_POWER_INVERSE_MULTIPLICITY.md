# Exact split-prime reciprocal inversion through a fixed power

The reciprocal inversion can be extended to **\(y=B^\delta\) for a fixed \(\delta>0\)**. For any prescribed relative accuracy, \(\delta\) can be chosen small enough to achieve it uniformly in both target classes. This preserves a positive sign across all 105 nonblocked phases in the sharp ordinary window. The resulting count is still weighted. The factors above \(B^\delta\) have an unresolved signed comparison.

## Fixed-power inversion

Keep the original even \(a,b\), \(A=3^a,\ B=5^b\), balance strip \(39/40<B/A<122/125\), and window
\[
1457A-123B<n\le729A+625B.
\]
Write \(S_0=A+25B\), \(S=3^c+5^e\), \(n=S_0+45u\), and \(v=u+\kappa\), where \(\kappa=(S_0-S)/45\). The original label limits are \(a/10\le c\le a/3,\ b/5\le e\le b/3,\ c\equiv a\pmod4,\ e\equiv b+2\pmod6\). The target classes remain \(r=0\) and \(r=r_-=3^{a+4}+5^{b+2}+7\pmod{49}\).

For \(W=r_2(u)r_2(v)\), define
\[
A_y(u)=\prod_{\substack{q\le y\\q\equiv1\ (4)}}
   \frac1{(1+v_q(u))(1+v_q(v))},
\qquad
V_{y,r}=\frac1{16}\sum_{n\equiv r\ (49)}W A_y(u).
\]
This inverts the **full powers** of all split primes up to \(y\).

For every fixed \(\epsilon>0\) there is a fixed \(\delta>0\) such that, for sufficiently large \(B\), the estimates take the form
\[
V_{y,0}=M_y(1+O(\epsilon)),\qquad
V_{y,-}=b_7 M_y(1+O(\epsilon)),\qquad y=B^\delta.
\]
Here \(b_7=1\) on the 98 unit phases and \(b_7=7/8\) on the seven zero-mod-49 phases. The common main term is the class-zero representation main term divided by 16 and multiplied by
\[
Q_y=\prod_{\substack{q\le y\\q\equiv1\ (4)}}
          \frac{(1-1/q)^2}{\sigma_q(\kappa)},
\qquad
\sigma_q(\kappa)=(1-q^{-2})\sum_{j=0}^{v_q(\kappa)}q^{-j}.
\]
In particular \(M_y\asymp F_I(\kappa)B/\log y\), where \(F_I(\kappa)=\prod_{q\mid\kappa,\ q\equiv3(4)}(q-1)/(q-2)\).

### The medium-prime step

Use the representation-weighted probability law in the fixed target class. The previous congruence argument gives the local product law with error \(O(B^{-\gamma}d^C)\) for bounded tests of \(u\bmod d\) at split-supported \(d\). The polynomial modulus loss is important here. Choose a fixed \(\theta>0\) with \(\theta(C+1)<\gamma/2\) and put \(D=B^\theta\).

Let \(z=B^{1/(\log\log B)^3}\). For each split \(z<q\le y\), outside the event \(q^2\mid u\) or \(q^2\mid v\), its exact reciprocal equals
\[
1-\tau_q1_{q\mid uv},\qquad
\tau_q=
\begin{cases}
1/2,&q\nmid\kappa,\\
3/4,&q\mid\kappa .
\end{cases}
\]
At a collision both valuations are one, so the required factor is \(1/4\). The weighted local probability of the square event is \(O(q^{-2})\), uniformly in \(v_q(\kappa)\). The actual union of these events has probability \(O(z^{-1}+B^{-\gamma}y^{2C+1})\) by the congruence estimate at \(q^2\). This is negligible at the required scale for sufficiently small fixed \(\delta\).

Apply upper and lower sieve weights to independent marks conditional on \(u\), with marking probability \(\tau_q1_{q\mid uv}\). Their multiplicative main-term density is \(g(q)=\tau_q\nu_q(q\mid uv)\), where \(\nu_q\) is the local representation-weighted law. At a noncollision, \(g(q)=2/q+O(q^{-2})\). At a collision,
\[
\nu_q(q\mid uv)=1-\frac{(1-1/q)^3}{\sigma_q(\kappa)},\qquad
g(q)=3/q+O(q^{-2}).
\]
Mertens in the split class gives the sieve dimension bound with dimension 2 and uniform constants, even by bounding every medium-prime density by \(3/q+O(q^{-2})\).

The summed remainder still works **after** small-prime inversion. For squarefree \(d\le D\) supported on medium primes, put \(H_d=\prod_{q\mid d}\tau_q1_{q\mid uv}\). The small-prime Bonferroni calculation, now with \(H_d\) inserted, gives
\[
\mathbb E_W[A_zH_d]
=Q_zg(d)+O\!\left(g(d)(\log B)^{-K}
                         +B^{-\gamma+o(1)}d^C\right).
\]
The first error retains \(g(d)\) because all small-prime truncation events use moduli coprime to \(d\). The CRT main term factors before those errors are bounded. Their extra moduli and number of terms are \(B^{o(1)}\). Summing the displayed errors costs at most \(O((\log B)^{2-K})+O(B^{-\gamma+o(1)}D^{C+1})\), since \(\sum_{d\le D}g(d)\ll(\log B)^2\).

The fundamental lemma now brackets the medium product by \( \prod_{z<q\le y}(1-g(q))\) with relative error \(O(s^{-s/2})\), where \(s=\theta/\delta\). Its local factors differ from the exact inverse factors by \(O(q^{-2})\), hence by \(1+O(z^{-1})\) in the product. Choose \(s\) large enough for the desired accuracy and then fix \(\delta=\theta/s\). This crosses a positive power of \(B\) while keeping the total error below the \(Q_y\) scale. The sieve input is the fundamental lemma in Theorem 2.2 of Kurlberg–Lester–Rosenzweig. The growing-modulus input is the polynomial-loss extension of the bilinear quadratic-form count. [Fundamental lemma, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136) · [Heath-Brown’s delta method](https://ora.ox.ac.uk/objects/uuid%3Abbd3c62f-f010-44b5-8be5-87e903fb0084/files/m7ec02df6e1b8303a66e7a6015ecb6044)

## What the sign covers

The row bound \(\sum_c F_I(\kappa_{c,e})\ll\log B\) keeps the total error over the unit phases under control. It follows by expanding the inert Euler product and using \(\operatorname{ord}_d(81)\ge\log(d+1)/\log81\) on the \(c\)-progression, after removing the factor at 3. The resulting series of Euler coefficients divided by \(\log d\) converges: for \(d>1\) integrate \(d^{-t}\) over \(t>0\) and use the inert-prime Euler factor bound \(O(t^{-1/2})\) near zero. The additional \(+1\) in counting each progression contributes at most the coefficient sum through \(O(B)\), which is \(O(\sqrt{\log B})\). Thus the sum of \(M_y\) on the full nonblocked grid is \(O(B(\log B)^2/\log y)\). The seven zero-mod-49 phases contribute a fixed positive fraction of this scale because they contain \(\asymp(\log B)^2\) labels and \(F_I\ge1\). Choosing \(\epsilon\) sufficiently small gives
\[
\sum_{\text{105 nonblocked phases}}(V_{y,0}-V_{y,-})
\gg \frac{B(\log B)^2}{\log y}.
\]

For the distinct count \(D_r\) on one label, the exact remaining identity is
\[
D_r=V_{y,r}\,
\mathbb E_{V_y,r}\!\left[
\prod_{\substack{q>y\\q\equiv1\ (4)}}
\frac1{(1+v_q(u))(1+v_q(v))}
\right].
\]
The earlier distinct upper and lower bounds in the same cells give \(V_{y,r}/D_r\asymp1/\delta\), improving the previous growing loss to a fixed one. The residual expectation has order \(\delta\) in each class. Its comparison between classes remains open.

## Exact replay

The balanced label \((a,b,c,e)=(712,486,72,98)\) tests a collision at 5 and a noncollision at 13. The second check reuses two already verified true targets at the same label \((8,8)\) on the smaller \((52,36)\) fixture. They satisfy the sharp window and the two target classes, with \(B/A\) outside the narrow strip. At the illustrative cutoff \(B^{1/5}\), their residual denominators are 6 and 2. This cutoff is used only for the finite control.

```python
from collections import Counter
from fractions import Fraction as F
from math import gcd, isqrt, prod

A, B = 3**712, 5**486
assert 39*A < 40*B and 125*B < 122*A
k = (A + 25*B - 3**72 - 5**98)//45
for q, depth, rho, g in [
    (5, 1, F(5,9), F(5,12)),
    (13, 0, F(25,91), F(25,182)),
]:
    m = q*q
    assert (k%q == 0) == bool(depth) and k%m
    N = Counter((x*x+y*y)%m for x in range(m) for y in range(m))
    w = [N[t]*N[(t+k)%m] for t in range(m)]
    assert F(sum(w),m**3) == (1-F(1,m))*sum(F(1,q**j) for j in range(depth+1))
    assert F(sum(w[t] for t in range(m) if t*(t+k)%q == 0),sum(w)) == rho
    assert (F(3,4) if depth else F(1,2))*rho == g

cert = {
    3457555897226619419244977:(11563666243,3629366173),
    642461230011986270401:(156186067,2237),
    11563666243:(1927277707,), 3629366173:(725293,),
    1927277707:(321212951,),
}
def prime(p):
    if p not in cert:
        return p >= 2 and all(p%d for d in range(2,isqrt(p)+1))
    Q = prod(cert[p])
    return ((p-1)%Q == 0 and Q*Q > p and pow(2,p-1,p) == 1
            and all(prime(q) and gcd(pow(2,(p-1)//q,p)-1,p) == 1
                    for q in cert[p]))

A, B = 3**52, 5**36
S0, S = A+25*B, 3**8+5**8
r = (pow(3,56,49)+pow(5,38,49)+7)%49
for x, phase, fu, fv, tail in [
    (12696151452849, 0, [(3,10),(1269901,2),(41143,2)],
     [(5,1),(13,1),(4057,1),(642461230011986270401,1)], 6),
    (12696151464813, r, [(3,2),(43,2),(467,2),(210748991,2)],
     [(7,2),(3457555897226619419244977,1)], 2),
]:
    u = x*x
    n = S0+45*u
    assert 1457*A-123*B < n <= 729*A+625*B and n%49 == phase
    for t, f in [(u,fu), (u+(S0-S)//45,fv)]:
        assert prod(p**j for p,j in f) == t
        assert all(prime(p) and (p%4 != 3 or j%2 == 0) for p,j in f)
    assert prod(j+1 for p,j in fu+fv if p%4 == 1 and p**5 > B) == tail
```
