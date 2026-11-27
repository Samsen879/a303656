# Lower-anchor matching despite tiled diagonal digit squares

**Exposing multiple lower anchors restores survival in the Chebotarev tiling family.** With both full primary cycles of length \(m=\ell^k\), the tiling ratios can block every unit diagonal anchor square. Even so, a perfect matching of surviving lower anchors is guaranteed after adding up to \(\varphi(m)/2-1\) arbitrary nonzero readers of the same full-order type. Each matched pair contains a cell that is a unit at every listed prime.

### Exact deletion from zero readings

Use full coordinates \(U,V\bmod m\), normalized so \(U=V=0\) means both primary exponent residues are zero. Assume both steps have exact order \(m\) at each listed prime. At a prime with \(n\equiv0\bmod p\), the collision set is empty or has the form
\[
U=\kappa V\pmod m,\qquad \kappa\in(\mathbb Z/m)^\times.
\]
Indeed, the frozen prime-to-\(\ell\) factors must cancel before an equality in the common order-\(m\) subgroup is possible. Once they cancel, the actual discrete-log ratio gives \(\kappa\).

Let \(\mathcal R\) be the set of distinct ratios that occur, and let \(r_s=|\mathcal R\bmod\ell^s|\). For a nonempty ratio set, the exact number of cells hit by these zero readings is
\[
Z=1+\sum_{s=1}^k\varphi(\ell^s)r_s.
\]
For a fixed \(V\) of valuation \(k-s\), two ratios produce the same \(U\) precisely when they agree modulo \(\ell^s\). The initial \(1\) accounts for \(V=0\).

In particular, even if **every** unit ratio occurs, at least \(2(m^2-1)/(\ell+1)\) cells avoid all zero readings. The surviving cells in that extreme case are exactly the pairs of unequal primary valuation. These are first-divisibility counts, so they also bound deletion by exact odd valuations.

### A matching bound for exposed lower anchors

Put \(L=\ell^{k-1}\), and let \(A,B\) be exposed sets of **unit** lower anchors modulo \(L\), with \(|A|\le |B|\). Each pair \((a,b)\) exposes the whole top-digit square
\[
U=a+Lx,\qquad V=b+Ly,\qquad x,y\bmod\ell.
\]
Define
\[
r(t)=|\{\kappa\in\mathcal R:\kappa\equiv t\bmod L\}|,\qquad
d(a,b)=\ell-r(ab^{-1}\bmod L).
\]
The zero readings leave exactly \(\ell d(a,b)\) unit cells in this square. The compatible ratios all have the same slope modulo \(\ell\), and their distinct lifts give distinct intercepts because \(b\) is a unit.

Every additional reader with \(n\not\equiv0\bmod p\) is a partial matching on the **full** \(U,V\) chart. Each \(U\) determines at most one \(V\), and conversely. Thus if \(h\) such readers empty every square in a rectangle \(X\times Y\subseteq A\times B\), necessarily
\[
\boxed{\quad \sum_{a\in X,\ b\in Y}d(a,b)
       \ \le\ h\min(|X|,|Y|).\quad}
\]
The left side charges the cells that still need deletion after the zero readings. The right side follows because a single reader can hit at most \(\ell\min(|X|,|Y|)\) cells in the rectangle. This holds for a common actual target and uses no independence assumption.

Join two lower anchors when their square has a unit survivor. By Hall’s theorem, the strict reverse inequality for every \(X,Y\) with \(|X|+|Y|>|B|\) guarantees a matching saturating \(A\). A failed Hall condition would give just such an empty rectangle.

For the Chebotarev family \(\mathcal R=\{1+Lj:0\le j<\ell\}\), take \(A=B=(\mathbb Z/L)^\times\). Then \(d(a,a)=0\) and \(d(a,b)=\ell\) off the diagonal. The boxed inequality forces an empty rectangle to have
\[
\max(|X|,|Y|)\le 1+\lfloor h/\ell\rfloor.
\]
Writing \(N=\varphi(L)\), the matching is therefore guaranteed when \(2(1+\lfloor h/\ell\rfloor)\le N\), equivalently \(h\le\varphi(m)/2-1\). This grows with the digit depth even though each diagonal square is fully tiled. [Chebotarev prime-selection theorem](https://link.springer.com/article/10.1007/BF03027290)

### Replay on the existing \(3,5\) control

For \(\ell=5,\ k=2\), the five actual ratios are \(1,6,11,16,21\bmod25\). They delete exactly \(105\) of the \(625\) full-chart cells, all at exact valuation one. The four unit lower anchors retain a perfect matching against any **nine** additional nonzero readers of full order \(25\) on both axes.

```python
from collections import Counter
from itertools import combinations, product
from math import lcm

P = (136651, 51151, 103651, 6151, 130651)
n = 1780728842053627736382578186834964108071957503893
D = lcm(*(p*((p-1)//25) for p in P))
E, C = D*pow(D, -1, 25), 25*D//2

R, bad = set(), set()
for p in P:
    assert n % (p*p) == p and pow(3,C,p) == p-1
    assert all(pow(g,p-1,p*p) != 1 for g in (3,5))
    g,h = pow(3,E,p), pow(5,E,p)
    assert pow(g,25,p) == 1 and pow(g,5,p) != 1
    k = next(j for j in range(25) if pow(g,j,p) == h)
    R.add(k)
    for u,v in product(range(25), repeat=2):
        z = (n-pow(3,C+E*u,p*p)-pow(5,E*v,p*p)) % (p*p)
        assert z and (z%p==0) == ((u-k*v)%25==0)
        if z%p == 0:
            bad.add((u,v))

assert R == {1,6,11,16,21} and len(bad) == 105
r = Counter(k%5 for k in R)
A = range(1,5)
sets = [X for j in A for X in combinations(A,j)]
assert all(sum(5-r[a*pow(b,-1,5)%5] for a in X for b in Y)
           > 9*min(len(X),len(Y))
           for X in sets for Y in sets if len(X)+len(Y)>4)
```

The five replay primes are ordinary on both axes. Chebotarev selects the order ratios modulo \(p\), while CRT controls the **remainder** modulo \(p^2\). A common-Wieferich constraint instead concerns the **bases** modulo \(p^2\) and would require a separate argument. The matching theorem applies to the stated reads on a full digit chart. It supplies no least-exponent height bound, and extension to a chronological prefix still requires checking the other rows in its protected closure.

Independent BigInt checked all 625 cells on the quinary chart, both-base ordinariness, all five exact ratios, and every lower-anchor Hall cut for nine additional readers. This is a matching of certified local unit cells, not a full Cartesian rectangle or an integer-height representation.
