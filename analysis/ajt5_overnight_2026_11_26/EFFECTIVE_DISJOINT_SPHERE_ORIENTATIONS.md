# Effective sphere populations from independent orientations

Independent cubing choices give almost disjoint sets of **distinct targets at the same height**. On the \(25,9\) ray with seed \(7\), they yield an effective lower bound
\[
\#T_k\gg_\varepsilon
\frac{2^k\sqrt{Q_k}}{(\log Q_k)^{1+\log 2+\varepsilon}},
\qquad Q_k=25^{7\cdot3^k},
\]
for every fixed \(\varepsilon>0\) and all sufficiently large \(k\). Here \(\log\) is natural. Every counted target has a true positive representation with both exponents equal to \(14\cdot3^k\), and a signed witness with both exponents equal to \(14\cdot3^k+1\). The choices add no heights. The exact uniform cumulative exponent of this single ray is \(1/6\).

### Construction and collision bound

Put \(h=7\cdot3^k,\ Q=25^h,\ Z=9^h\), and let \(u=\sqrt{-3}\). Start with the exact norm
\[
25^7-9^7=23816^2+3\cdot42940^2.
\]
Multiply \(2(23816+42940u)\) by either sign of the \(u\)-coordinate in each factor
\[
\gamma_j=\frac{A_j-B_j}{2}+\frac{A_j+B_j}{2}u,\qquad
(A_j,B_j)=(25^{7\cdot3^j},9^{7\cdot3^j}),\quad 0\le j<k.
\]
The resulting \((v,w)\) satisfy \(v,w\in4\mathbb Z\) and \(v^2+3w^2=4(Q-Z)\). An odd \(r>0\) with
\[
S=3w^2+6Z-r^2=x^2+y^2>3Z
\]
gives the same integer in the two forms
\[
n=Q+Z+v^2+r^2=5Q+3Z-S,\qquad Q<n<5Q.
\]
The signed witness also satisfies \(6Z-S=r^2-3w^2\). For the retained choices \(3\nmid w\), the sphere has value \(3\bmod9\), so all three coordinates are units modulo \(3\). Together with \(v\in4\mathbb Z\) and \(r\) odd, this gives \(n\equiv3\bmod24\).

There are \(\gg2^k\) distinct retained values of \(v^2\) with \(3\nmid w\) and \(|w|\ge\sqrt Q/4\). Indeed, the shell norms \(A_j^2+A_jB_j+B_j^2\) are pairwise coprime. A prime dividing shell \(j\) sees \(A_j/B_j\) of order exactly \(3\), so it sees ratio \(1\) in all later shells. Each \(\gamma_j\) is coprime to its conjugate as an ideal, since the two integer coefficients are coprime and the shell norm is coprime to \(6\). Thus the \(2^k\) choices give distinct ideals, and at most four pairs can share \(v^2\). For each fixed prefix of length \(k-2\), the last signs \(++,+-,--\) give three distinct values of \(w/v\bmod3\). Their angles modulo \(\pi\) are separated by at least \(\pi/4\), since each \(\arg\gamma_j\) lies between \(\pi/3\) and \(\pi/3+\pi/48\). Of the two choices with \(3\nmid w\), one has angle at least \(\pi/8\) from the real axis. This gives the stated size bound.

Write \(T_v\) for the targets from a retained \(v^2\). At a common target from two unequal \(v_i^2\), the positive \(r_i\) satisfy
\[
(r_2-r_1)(r_2+r_1)=v_1^2-v_2^2.
\]
Hence \(|T_{v_1}\cap T_{v_2}|\le\tau(|v_1^2-v_2^2|)\). For any list of \(J\) distinct \(v^2\) at this height, the union therefore differs from \(\sum_v |T_v|\) by at most \(O_\eta(J^2 Q^\eta)\), for every \(\eta>0\). This also bounds overlap with a single previously selected orientation.

### Effective count on the retained spheres

Let \(N=3w^2+6Z=3d f^2\), with \(d\) squarefree. Here \(d\) is even and \(d\equiv1\bmod3\), so \(-12d\) is fundamental. A fixed \(d\) occurs only \(O(1)\) times among the retained positive \(|w|\). In the real field \(\mathbb Q(\sqrt d)\), the element \(|w|+f\sqrt d\) has norm \(-2\cdot3^{2h}\). Its ideal uses the unique ramified prime above \(2\), and all its \(3\)-valuation lies on one of the two primes above \(3\), since \(3\nmid w\). There are at most two ideals. Generators in the required interval \([\sqrt Q/2,3\sqrt Q]\) differ by units, and any real quadratic unit greater than \(1\) is at least \((1+\sqrt5)/2\). Thus omitting a possible Landau–Page exceptional character costs only \(O(1)\) orientations. [Landau–Page, Lemma 7.1](https://arxiv.org/pdf/1412.5029#page=32)

For the other orientations let \(\chi=\chi_{-12d}\), \(L=\log Q\), and \(\ell=\log L\). In a zero-free disk of radius \(c/L\) centered at \(s_0=1+c/(L\ell)\), periodic summation gives \(|L(s,\chi)|\ll L\). The Euler product gives \(L(s_0,\chi)\gg1/(L\ell)\). Applying Harnack to \(\log(CL)-\log|L(s,\chi)|\) at \(s_0\) and \(1\), whose separation is \(1/\ell\) of the radius, gives \(L(1,\chi)\asymp L(s_0,\chi)\).

Since \(N\equiv6\bmod8\), Gauss’s formula gives \(12h(-4N)\) primitive representations, with exactly two thirds having the marked coordinate \(r\) odd. The order class-number formula and \(\prod_{p\mid f}(1-1/p)\gg1/\ell\) give a first moment \(\gg\sqrt Q\,L(1,\chi)/\ell\). Trimming \(0<N-r^2\le3Z\) deletes only \(O(Z/\sqrt Q+1)\) possible \(r\), each of weight \(Q^{o(1)}\). This is negligible because \(Z=Q^{\log9/\log25}\). [Gauss’s formula, Theorem 30.1.3](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_30)

For clarity, the moment estimate used to convert that weight into distinct \(r\) is
\[
\sum_{1\le r<\sqrt N}r_2(N-r^2)^t
\ll_t \sqrt Q\,L^{2a}\ell^{O_t(1)}L(1,\chi)^b,
\qquad a=2^{t-1}-1,\quad b=2^{t-1},\quad 1<t\le2.
\]
Apply the one-polynomial case of de la Bretèche–Tenenbaum’s Theorem 3.1 to the primitive irreducible polynomial \(X^2-N\), with interval parameters \(x=y=\lceil\sqrt N\rceil\) and multiplicative weight \((r_2/4)^t\). For \(p\nmid2N\) the combined local factor has first-order coefficient
\[
(a+b\chi_{-4}(p))(1+\chi_{12d}(p))
\le 2a+b\chi_{-4}(p)+b\chi(p).
\]
At \(p\mid2N\), the normalized exact-valuation count is bounded by the divisibility count, and \(X^2\equiv N\bmod p^j\) has at most \(4p^{\lfloor j/2\rfloor}\) roots. The resulting factors \(1+O_t(1/p)\) cost only \(\ell^{O_t(1)}\), by splitting at \(p=L\). Comparing the truncated \(\chi\)-product with \(L(s_0,\chi)\) costs another \(\ell^{O(1)}\): the prime tail from \(\sqrt N\) to \(\exp(1/(s_0-1))\) has reciprocal sum \(O(\log\ell)\), and the weighted tail beyond it is bounded. [De la Bretèche–Tenenbaum, Theorem 3.1 and (3.5)](https://arxiv.org/pdf/2403.19320#page=4)

Hölder now gives \(|T_v|\gg_t\sqrt Q\,L^{-E_t}\ell^{-O_t(1)}\), with
\[
E_t=\frac{2a+t-b}{t-1}=1+\frac{2^{t-1}-1}{t-1}.
\]
Taking a fixed \(t>1\) sufficiently close to \(1\) gives the claimed lower bound after summing and subtracting the collision error.

### Height limit and exact control

The shell construction gives at most \(O(2^k\sqrt Q)\) targets per height. Even allowing **every** norm pair at that height gives at most \(Q^{1/2+o(1)}\), since a quadratic field has at most \(\tau(4(Q-Z))\) ideals of that norm and the Eisenstein field has six units. The windows are contained in \((Q_k,5Q_k)\) and \(Q_{k+1}=Q_k^3\). Consequently, for the cumulative count \(A(X)\) on this ray, the lower and upper limiting values of \(\log A(X)/\log X\) are \(1/6\) and \(1/2\), respectively. Improving the uniform exponent requires changing the admissible heights.

The following replay gives three distinct true targets at \(h=63\). It also checks a repair failure on the same \(25,9\) base. At \(h=2\) the active inert primes are exactly \(2,17\). Multiplying the index by \(34\) makes both valuations even but introduces odd valuation at \(137\).

```python
from itertools import product

A, B = 25**7, 9**7
assert A-B == 23816**2 + 3*42940**2
shells = []
for _ in range(2):
    shells.append(((A-B)//2, (A+B)//2))
    A, B = A**3, B**3

Q, Z, s = A, B, 3**63
targets = set()
for signs in product((1, -1), repeat=2):
    v, w = 47632, 85880
    for e, (a, b) in zip(signs, shells):
        v, w = a*v-3*e*b*w, a*w+e*b*v
    assert v*v + 3*w*w == 4*(Q-Z)
    if w % 3:
        w = abs(w)
        r = w+s
        S = r*r+(w-2*s)**2
        n = Q+Z+v*v+r*r
        assert n == 5*Q+3*Z-S and S > 3*Z
        assert Q < n < 5*Q and n % 24 == 3
        targets.add(n)
assert len(targets) == 3

assert 25**2-9**2 == 2**5*17
D = 25**68-9**68
for p, e in ((2, 6), (17, 2), (137, 1)):
    assert D % p**e == 0 and D % p**(e+1) != 0
```

The population result concerns the constructed \(n\equiv3\bmod24\) targets. It gives neither a density-one statement nor a pointwise result for the original conjecture.

Independent BigInt verified three distinct actual same-height targets, signed and positive identities, and the failed inert repair control. The exceptional character is removed with only bounded loss using the fixed-discriminant ideal argument. The count is population on a single ray and does not improve the lacunary heights.
