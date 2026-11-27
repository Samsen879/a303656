# Effective population across five interlaced sphere rays

The five interlaced rays give an **effective population bound in both odd classes** for the constructed targets, without a claim for arbitrary target selection. Let \(A_\lambda(X)\) count their constructed targets \(n\le X\) with \(n\equiv\lambda\pmod4\), for \(\lambda=1,3\). For every \(\varepsilon>0\) and all sufficiently large \(X\),
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{13/34}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}}.
\]
The threshold and constants are effective; no numerical threshold is supplied here. The stronger logarithmic loss obtained below is \((\log X)^{1+\log 2-\log_3 2}\exp(O(\sqrt{\log\log X\,\log\log\log X}))\). The power \(13/34\) is sharp in the liminf for these five rays, even allowing all norm orientations.

### Both classes at every height

Use the five verified seed tuples \((m,e,a,b)\) in the replay below. Each satisfies \(5^m-3^e=a^2+3b^2\). For depth \(k\), put \(Q=5^{m3^k}\), \(Z=3^{e3^k}\) and \(B=5Q\). Independent conjugation in the \(k\) cubing factors gives
\[
v^2+3w^2=4(Q-Z),\qquad v,w\in4\mathbb Z.
\]
For \(\lambda\in\{1,3\}\), take an odd \(r>0\) with
\[
S=x^2+y^2=3w^2+2\lambda Z-r^2>\lambda Z.
\]
The two identities are
\[
n=B+\lambda Z-S=Q+(4-\lambda)Z+v^2+r^2,\qquad
2\lambda Z-S=r^2-3w^2.
\]
Thus \(Q<n<B\), and the second expression for \(n\) is a true positive representation. Both \(3\)-powers and both \(5\)-powers grow. When \(3\nmid w\), the sphere is \(3\bmod9\), so all three coordinates are units modulo \(3\). The two classes obtained are \(21\bmod24\) for \(\lambda=1\) and \(3\bmod24\) for \(\lambda=3\). [Five seed identities and the class exchange](https://raw.githubusercontent.com/Samsen879/a303656/945ab5dbf0455c900e60a455d0f1c6a698c9da8d/analysis/ajt5_overnight_2026_11_26/FIVE_INTERLACED_SPHERE_SEEDS.md)

For each seed and \(k\ge3\), there are \(\gg2^k\) distinct \(v^2\) with \(3\nmid w\) and \(|w|\ge\sqrt Q/4\). The shell norms are pairwise coprime because a prime dividing one shell sees the ratio of its two powers at order \(3\), which becomes order \(1\) in all later shells. The two conjugate factors in one shell are coprime as ideals. Hence all sign vectors give distinct ideals, and at most four resulting pairs share one \(v^2\). For each fixed prefix of \(k-2\) signs, the three tails \(++,+-,--\) give all three values of \(w/v\bmod3\). The last two factor angles lie in \([\pi/3,\pi/3+\pi/48]\), since their smaller-to-larger power ratios are at most \((9/25)^3\). The three resulting angles modulo \(\pi\) are separated by at least \(\pi/4\). At least one of the two nonzero ternary phases is therefore at distance at least \(\pi/8\) from the real axis. This proves the size bound with the same retained orientations for both classes.

Within one class and height, two orientations with \(v_1^2\ne v_2^2\) meet in at most \(\tau(|v_1^2-v_2^2|)\) targets, by factoring \(r_2^2-r_1^2=v_1^2-v_2^2\). The sum of pairwise overlaps is \(O_\eta(4^k Q^\eta)\) for every \(\eta>0\).

### Why the effective count survives the class switch

Write \(N_\lambda=3w^2+2\lambda Z=3d f^2\) with \(d\) squarefree. Then \(d\) is even, \(d\equiv1\bmod3\), and the fundamental discriminant is \(-12d\). The key identity, valid in **both** classes, is
\[
\operatorname{Norm}_{\mathbb Q(\sqrt d)/\mathbb Q}(|w|+f\sqrt d)
=-2\lambda Z/3.
\]
The prime above \(2\) is ramified. All the \(3\)-valuation lies on one of the two split primes, since \(3\nmid w\). For a fixed \(d\) and \(\lambda\) there are at most two possible ideals, and their positive generators here lie in \([\sqrt Q/2,3\sqrt Q]\). Consecutive generators differ by a unit of size at least the golden ratio, so there are at most eight retained orientations for any \(d\) in each class. A single Landau–Page exceptional character among conductors up to \(24Q\) therefore removes at most sixteen orientations across both classes. [Landau–Page, Lemma 7.1](https://arxiv.org/pdf/1412.5029#page=32)

Here is the quantitative count after this deletion. Put \(L=\log Q\), \(\ell=\log L\), and \(\chi=\chi_{-12d}\). The zero-free disk at \(1+c/(L\ell)\), of radius \(c/L\) for a small absolute \(c\), gives \(L(1,\chi)\asymp L(1+c/(L\ell),\chi)\gg (L\ell)^{-1}\). Indeed, periodic summation bounds the modulus by \(O(L)\) in the disk, the Euler product gives the lower bound at its center, and Harnack applied to \(\log(CL)-\log|L(s,\chi)|\) compares the two values a distance \(1/\ell\) of the radius apart.

Both \(N_\lambda\equiv2,6\bmod8\) use the same Gauss formula \(r_3^{\rm prim}(N_\lambda)=12h(-4N_\lambda)\). Exactly two thirds of these triples have the marked coordinate odd. The order class-number formula gives a first moment \(\gg\sqrt Q\,L(1,\chi)/\ell\). The cutoff \(S>\lambda Z\) removes only \(O(1+Z/\sqrt Q)\) possible marked coordinates, each of weight \(Q^{o(1)}\) by the effective divisor bound. Since \(Z\le Q^{\log3/\log5}\), the discarded mass is negligible. [Gauss’s formula, Theorem 30.1.3](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_30)

Uniformly for \(1<t\le2\), let \(\alpha=2^{t-1}-1\) and \(\beta=2^{t-1}\). The one-polynomial moment bound on \(X^2-N_\lambda\) with weight \((r_2/4)^t\) gives
\[
\sum_{1\le r<\sqrt{N_\lambda}}r_2(N_\lambda-r^2)^t
\ll \sqrt Q\,L^{2\alpha}\ell^{O(1)}L(1,\chi)^\beta.
\]
For \(p\nmid2N_\lambda\), the linear coefficient of the combined local factor is \((\alpha+\beta\chi_{-4}(p))(1+\chi_{12d}(p))\le 2\alpha+\beta\chi_{-4}(p)+\beta\chi(p)\). At bad primes the root bound \(4p^{\lfloor j/2\rfloor}\) modulo \(p^j\) gives factors \(1+O(1/p)\), costing \(\ell^{O(1)}\). Comparing the truncated \(\chi\)-product with the Euler product at \(1+c/(L\ell)\) also costs \(\ell^{O(1)}\). The constants are uniform in \(t\) because the weights all satisfy the same growth bound \(\tau^2\). [De la Bretèche–Tenenbaum, Theorem 3.1 and (3.5)](https://arxiv.org/pdf/2403.19320#page=4)

Hölder gives a logarithmic exponent \(1+(2^{t-1}-1)/(t-1)\) per orientation, with an additional factor \(\exp(-O(\log\ell/(t-1)))\). Choosing \(t-1=\sqrt{\log\ell/\ell}\), summing over retained orientations and subtracting the overlap bound gives, in **each** class at each sufficiently large height,
\[
\gg \frac{2^k\sqrt Q}{L^{1+\log2}}\exp\!\big(-O(\sqrt{\ell\log\ell})\big)
\]
distinct targets.

### Interlacing and replay

The normalized lower exponent phases are \(2,22/9,26/9,34/9,14/3,6\), with the last phase starting the next cycle. Their largest consecutive ratio is \(17/13\). The largest completed window \(B\le X\) therefore has \(B>X^{13/17}\) for large \(X\). On each ray \(2^k\asymp(\log B)^{\log_3 2}\), giving the stated uniform count. Conversely, at \(X=5^{34\cdot3^k}\) the \(34\)-window has yet to contribute and the preceding lower power is \(5^{26\cdot3^k}\). Even all norm pairs at a single height give at most \(Q^{1/2+o(1)}\) targets, by the quadratic ideal divisor bound and \(O(\sqrt Q)\) marked coordinates per pair. This proves the sharp liminf on these rays.

The replay checks the five seed norms, both classes at depth two, and a negative control showing why the genuine \((26,10)\) ray cannot be replaced by the equal-exponent \((26,26)\) seed.

```python
from fractions import Fraction as F
from itertools import product

seeds = [(2,2,4,0), (22,6,7139528,27887948),
         (26,10,1220699108,1808048), (34,34,758993440348,44742038272),
         (14,10,5128,45008)]
for m,e,a,b in seeds:
    Q,Z = 5**m,3**e
    assert a*a+3*b*b == Q-Z
    shells = []
    for _ in range(2):
        shells.append(((Q-Z)//2,(Q+Z)//2))
        Q,Z = Q**3,Z**3
    s = 3**(9*e//2)
    targets = {1:set(), 3:set()}
    for signs in product((1,-1), repeat=2):
        v,w = 2*a,2*b
        for sign,(c,d) in zip(signs,shells):
            v,w = c*v-3*sign*d*w,c*w+sign*d*v
        assert v*v+3*w*w == 4*(Q-Z) and v%4 == w%4 == 0
        w = abs(w)
        if w%3 == 0 or w <= s:
            continue
        r = w+s
        for lam,x,y in ((1,w-s,w),(3,w+s,w-2*s)):
            S = x*x+y*y
            n = Q+(4-lam)*Z+v*v+r*r
            assert n == 5*Q+lam*Z-S and S > lam*Z
            assert 2*lam*Z-S == r*r-3*w*w and Q<n<5*Q
            assert n%24 == (21 if lam == 1 else 3)
            targets[lam].add(n)
    assert [len(targets[j]) for j in (1,3)] == [1 if m == 2 else 3]*2

phase = [F(2),F(22,9),F(26,9),F(34,9),F(14,3),F(6)]
assert max(y/x for x,y in zip(phase,phase[1:])) == F(17,13)
assert (25**13-9**13) % 53**2 == 50*53
```

For a preassigned \(n\), its least larger power of \(5\) identifies a candidate height. When that height belongs to a ray, the conjugation choices give \(O((\log n)^{\log_3 2})\) square tests for the positive representation. The population theorem counts the generated successes. The existence of a successful test for every preassigned \(n\) remains open.
