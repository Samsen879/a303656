# Deletion-resilient squarefree true labels in every dyadic interval and mod-8 class

For every sufficiently large \(X\) and each residue class \(b\bmod8\), there are \(\gg X\) distinct \(n\in[X,2X]\), \(n\equiv b\bmod8\), with the following property. On a fixed box of actual exponent choices of size \(\asymp\log X\) on each axis, draw an edge when the positive residual \(n-3^c-5^d\) is squarefree and a sum of two squares, and is at least \(n/2\). The graph has \(\gg(\log X)^{3/2}\) edges even after any \(\epsilon\log X\) exponent vertices are deleted, for one fixed \(\epsilon>0\). After such deletions it has \(\gg\sqrt{\log X}\) edge-disjoint matchings, each of size \(\gg\log X\). Constants may be taken uniform over the eight classes. This is a positive-proportion theorem for generated targets in each dyadic interval, not density one or a solution for an arbitrary prescribed \(n\).

## Squarefree norms in the required dyadic slab

Let \(L=\log X\), and fix a small absolute \(\delta>0\). Take squarefree \(A\le X^{1/4}\) supported on primes \(1\bmod4\) at most \(X^\delta\). By [Mertens in a fixed progression](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf), the unrestricted reciprocal sum of these finite squarefree products is \(\asymp\sqrt L\). In its probability weighting the primes occur independently with probabilities \(1/(p+1)\), so the expected \(\log A\) is \(O(\delta L)\). For small enough fixed \(\delta\), Markov's inequality keeps at least half the weight when imposing \(A\le X^{1/4}\).

Take \(q\) prime in \([X/A,3X/(2A))\), with \(q\equiv A^{-1}\bmod8\). Since these odd products use only primes \(1\bmod4\), the two possible classes for \(q\) are \(1,5\bmod8\). The fixed-progression prime number theorem supplies \(\gg X/(A L)\) choices uniformly, since every lower endpoint is at least \(X^{3/4}\). The factor \(q\) is the unique large prime of \(Aq\), so distinct choices give distinct squarefree primitive norms in \([X,3X/2)\) of residue \(1\bmod8\). Their count is \(\gg X/\sqrt L\). Applying the same argument at \(X/2\) and multiplying by 2 gives the even squarefree primitive norms of residue \(2\bmod8\) in the same slab.

For odd \(b\) use the first norms, and for even \(b\) the second. Fix both exponent parities to obtain \(3^c+5^d\equiv b-1\) or \(b-2\bmod8\), respectively. The four parity choices yield all four even residues. Use ranges
\[
 X^{1/8}\le3^c\le X^{1/4},\qquad
 X^{1/3}\le5^d\le X^{1/2}.
\]
Each axis has \(\asymp L\) options. The gaps on the second axis exceed the entire first-axis span, so the actual numerical shifts are distinct. Adding each shift to the norms above gives target \(n\in[X,2X]\), and the residual is at least \(X\ge n/2\). The total edge incidence in class \(b\) is at least \(c XL^{3/2}\).

## Pair and degree energies

Let \(W(h)=h/\varphi(h)\) for positive actual differences. For two primitive odd norms with gap \(h\), the uniform pair count is \(O(XW(h)/L)\) by [Radomskii, Example 2](https://arxiv.org/html/2504.09954v7). Since the even residuals are twice odd primitive norms, use the bound at half scale with gap \(h/2\) whenever that is integral; \(W(h/2)\le W(h)\). Restricting to squarefree residuals or to a slab can only make the upper bounds smaller.

We give the congestion calculation, keeping numerical gaps with their multiplicities. For a fixed labelled shift and a prime \(p\ne3\), fixing the comparison shift's \(5\)-axis exponent leaves at most \(O(1+L/\operatorname{ord}_p(9))\) values on the \(3\) axis, because the parity was fixed. Thus at most \(O(L+L^2/\operatorname{ord}_p(9))\) shifts collide modulo \(p\). At \(p=3\) use \(O(L^2)\). [Radomskii's Lemma 3.1](https://arxiv.org/html/2504.09954v7#S3) with \(s=1\) gives an \(O(L^2)\) sum of \(W(h)\) per label: its truncated prime weight is \(\log p/p\), the \(O(L)\) term contributes \(O(L\log L)\), and
\[
 \sum_{p\nmid b} \frac{\log p}{p\operatorname{ord}_p(b)}<\infty
\]
for either \(b=9\) or 25. To see the last convergence, the primes of order at most \(t\) divide \(\prod_{j\le t}(b^j-1)\) of logarithmic size \(O(t^2)\). The sum of their \(\log p/p\) is \(O(1+\log t)\) by a split at \(t^2\); dyadic division by \(t\) is summable. The total \(W\)-sum over two labels is consequently \(O(L^4)\). The edge-count second moment is \(O(X L^3)\), including the diagonal, so Cauchy–Schwarz gives \(\gg X\) distinct targets with \(\gg L^{3/2}\) edges.

For a single exponent vertex, only one axis varies. By the same lemma and the one-dimensional collision bound \(O(1+L/\operatorname{ord}_p(b))\), the \(W\)-sum is \(O(L)\) per one-axis label, hence \(O(L^2)\) total at that vertex. The pair bound and diagonal give total degree-squared \(O(XL)\) at a fixed vertex summed over targets. Summing the \(O(L)\) vertices on both axes gives \(O(X L^2)\) for the combined degree energy. Markov therefore keeps \(\gg X\) of the targets already found while requiring \(\sum_v \deg(v)^2\ll L^2\).

Deleting \(k\le\epsilon L\) vertices at one of these targets loses at most \(\sqrt{k\sum_v \deg(v)^2}\) edges. Small fixed \(\epsilon\) thus leaves \(\gg L^{3/2}\) edges. Now discard vertices of degree above \(C\sqrt L\), for large fixed \(C\): at most \((C\sqrt L)^{-1}\sum_v \deg(v)^2\) additional edges can be lost. The remaining graph has maximum degree \(O(\sqrt L)\), so a greedy maximal matching has size \(\gg L\). Remove its edges and repeat. Each matching removes at most \(O(L)\) edges because there are \(O(L)\) vertices. This gives \(\gg\sqrt L\) edge-disjoint matchings, and the entire argument applies after any permitted deletion.

## Independent exact finite controls

One example per residue modulo 8. At each, six true squarefree remainders are at least \(n/2\). The replay checks two edge-disjoint size-three matchings and survival of a size-three matching after deletion of any single vertex. Finite controls do not prove the asymptotic count.

~~~python
from itertools import combinations
from math import isqrt
data=[[156280,[[2,3,89,385],[2,7,145,239],[4,1,263,295],[4,5,257,295],[6,3,149,365],[8,1,55,383]]],[156265,[[1,3,256,301],[1,7,76,269],[3,5,133,368],[5,1,121,376],[7,1,272,283],[7,3,17,392]]],[156274,[[1,3,89,385],[1,7,145,239],[3,1,161,361],[3,5,151,361],[5,3,209,335],[7,1,211,331]]],[781307,[[2,6,283,828],[2,8,127,612],[4,2,600,649],[4,4,115,876],[6,2,548,693],[10,6,483,688]]],[781268,[[2,8,185,597],[4,2,301,831],[4,4,89,879],[6,4,15,883],[6,6,115,867],[8,2,459,751]]],[781269,[[1,4,329,820],[1,8,79,620],[3,2,356,809],[5,2,451,760],[5,4,424,775],[7,6,244,839]]],[781262,[[1,6,195,853],[1,8,185,597],[3,2,561,683],[3,6,571,663],[9,4,555,673],[11,2,451,633]]],[156271,[[2,3,256,301],[2,7,76,269],[4,1,236,317],[6,1,119,376],[6,5,236,311],[8,3,223,316]]]]
for residue,(n,edges) in enumerate(data):
    assert n%8==residue and len(edges)==6
    for c,d,u,v in edges:
        m=n-3**c-5**d
        assert c>0 and d>0 and m>=n/2 and m==u*u+v*v
        assert m%8==(1 if n%2 else 2)
        assert all(m%(q*q) for q in range(2,isqrt(m)+1))
    def match(B):
        return len({edges[i][0] for i in B})==len({edges[i][1] for i in B})==3
    choices=[set(B) for B in combinations(range(6),3) if match(B)]
    assert any(not A & B for A,B in combinations(choices,2))
    for j in [0,1]:
        for v in {e[j] for e in edges}:
            assert any(all(edges[i][j]!=v for i in B) for B in choices)
print('eight mod-8 squarefree deletion controls passed')
~~~

## Refinement to mod 24 and a true squarefree-only ceiling

### Mod-\(24\) refinement and obstruction

A positive squarefree two-square residual is never divisible by \(3\). Since \(c>0\) throughout the windows for large \(X\), a fixed \(d\)-parity therefore excludes \(n\equiv5^d\bmod3\). In the draft’s chosen parity box, this rules out one third of each mod-\(8\) class.

For **even** targets, a squarefree norm residual is always \(2\bmod8\), so the target residue modulo \(8\) forces both label parities, even if the whole window is allowed. The forbidden classes modulo \(24\) are
\[
\boxed{2,\ 4,\ 8,\ 22.}
\]
This proves the \(5/6+O(1/X)\) ceiling for squarefree residuals in the full windows, before any exponent deletion.

For **odd** targets, the residual can be \(1\) or \(5\bmod8\). Switching between them switches the required \(d\)-parity, so one can avoid the forbidden mod-\(3\) value in every odd mod-\(24\) class. To obtain a positive fraction in each of the resulting 20 classes, fix the admissible parity box and prescribe the residual modulo \(24\). In the draft’s \(Aq\) construction, omit the prime \(3\) and choose \(q\) in the reduced class that gives the required odd residual. For even residuals, apply the same construction to half the residual and multiply by \(2\). The reciprocal-product and fixed-progression estimates keep the same order of magnitude. The energy upper bounds continue to hold on the smaller target class, and the matching proof carries over unchanged. This gives positive-proportion coverage within each admissible class. Density one within those classes and unrestricted A303656 remain open. [Williams, *Mertens’ Theorem for Arithmetic Progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf) · [Sun, Conjecture 4.1(i)](https://arxiv.org/abs/1701.05868)

### Exact same-target replay in the windows

At \(X=10^{10}\), the actual axes are \(c\in\{3,4,5\}\) and \(d\in\{5,6,7\}\). At \(n=10000000051\equiv19\bmod24\), the original residual-\(1\bmod8\) box has just \((4,6)\), whose residual is divisible by \(3\). The alternative residual-\(5\bmod8\) box gives **two genuine squarefree witnesses at the same target**:
\[
\begin{aligned}
n-3^4-5^5&=11693^2+99314^2,\\
n-3^4-5^7&=2263^2+99974^2.
\end{aligned}
\]
For the even obstruction, \(1000016\equiv8\bmod24\) at \(X=10^6\) has an ordinary in-window norm residual \(309^2+951^2\) at \((2,3)\). It is divisible by \(9\), as the squarefree obstruction permits. The following standard-library checks verify these in-window controls.

```python
from math import isqrt

def axes(X):
    return ([c for c in range(30) if 3**(8*c) >= X >= 3**(4*c)],
            [d for d in range(30) if 5**(3*d) >= X >= 5**(2*d)])

def squarefree(m):
    return all(m % (j*j) for j in range(2, isqrt(m) + 1))

def residual(n, c, d):
    return n - 3**c - 5**d

X, n = 10**10, 10000000051
C, D = axes(X)
assert X <= n <= 2*X and n % 24 == 19
assert (C, D) == ([3, 4, 5], [5, 6, 7])
assert [(c, d) for c in C for d in D
        if residual(n, c, d) % 8 == 1] == [(4, 6)]
assert residual(n, 4, 6) % 3 == 0
for c, d, x, y in [(4, 5, 11693, 99314), (4, 7, 2263, 99974)]:
    m = residual(n, c, d)
    assert c in C and d in D and 2*m >= n
    assert m == x*x + y*y and m % 8 == 5 and squarefree(m)

X, n = 10**6, 1000016
C, D = axes(X)
assert X <= n <= 2*X and n % 24 == 8
assert [(c, d) for c in C for d in D
        if residual(n, c, d) % 8 == 2] == [(2, 3)]
m = residual(n, 2, 3)
assert 2*m >= n and m == 309**2 + 951**2 and m % 9 == 0
```
## Restoring all target classes with the single fixed square multiplier 9

**The factor \(3^2\) restores all four forbidden classes.** In every sufficiently large dyadic interval, a positive fraction of each class modulo \(24\) has the full deletion-robust conclusion of draft PR #82 in the original exponent windows. In the four restored classes \(2,4,8,22\bmod24\), the residual is exactly \(9\) times a squarefree two-square norm coprime to \(3\). The construction can in fact work separately in **every class modulo \(216\)**, with a fixed exponent box chosen for that class. This is a positive-fraction result. [Draft PR #82](https://github.com/Samsen879/a303656/pull/82/files)

### The residue change

Fix a target class \(n\equiv b\bmod216\) above one of the four forbidden classes. An even squarefree two-square norm is \(2\bmod8\), and multiplication by \(9\) preserves that residue. Thus the required exponent parities are still the unique ones satisfying
\[
3^c+5^d\equiv b-2\pmod8.
\]
In these forbidden classes, that \(d\)-parity satisfies \(5^d\equiv b\bmod3\).

Choose \(c\ge3\) with the required parity, and choose \(d\bmod18\) by
\[
5^d\equiv b-18\pmod{27}.
\]
The order of \(5\bmod27\) is \(18\): \(25\) has order \(9\) by lifting the exponent, and \(5\equiv-1\bmod3\). Since \(b-18\) is a unit, the exponent class exists uniquely. Reducing modulo \(3\) shows it has the required parity. Every actual label in this box therefore leaves
\[
m=n-3^c-5^d\equiv18\pmod{27},\qquad m\equiv2\pmod8.
\]
Equivalently, \(m\equiv18\bmod216\). In particular \(v_3(m)=2\), and \(m/9\equiv2\bmod24\).

Take \(m=18u\), where \(u\) is an odd squarefree norm supported on split primes, \(u\equiv1\bmod12\), and \(u\in[X/18,X/12]\). The squarefree product and large-prime construction from the draft gives \(\gg X/\sqrt{\log X}\) such \(u\) in this fixed reduced class. Then \(m/9=2u\) is squarefree, and if \(u=x^2+y^2\) the **ordinary residual** is
\[
m=[3(x+y)]^2+[3(x-y)]^2.
\]
The exponent windows remain \(X^{1/8}\le3^c\le X^{1/4}\) and \(X^{1/3}\le5^d\le X^{1/2}\). Restricting to the fixed classes of \(c,d\) leaves \(\asymp\log X\) actual exponents on each axis. The target is formed by adding the actual label to \(m\in[X,3X/2]\), so \(n\in[X,2X]\) and \(m\ge n/2\) for sufficiently large \(X\). [Draft squarefree norm construction](https://github.com/Samsen879/a303656/pull/82/files) · [Williams, *Mertens’ Theorem for Arithmetic Progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf)

For the other 20 mod-\(24\) classes, retain strictly squarefree residuals. In each refinement modulo \(216\), fix a compatible parity box and a \(d\)-class modulo \(18\) that makes the residual a unit modulo \(3\). Since \(c\ge3\), the whole box then has a fixed residual class modulo \(216\). For odd targets use that reduced class directly. For even targets divide the prescribed residual class by \(2\) and use the resulting reduced class modulo \(108\) for the odd squarefree norm. The fixed-progression prime theorem applies in each case.

### Scaling the energy and matching argument

Write \(L=\log X\). In a restored box, the difference \(h\) of two distinct labels is divisible by \(216\), so the odd primitive norm cofactors are separated by the integer gap \(h/18\). Radomskii’s pair estimate at scale \(X/18\) is
\[
O\!\left(\frac{X}{L}\frac{|h|/18}{\varphi(|h|/18)}\right)
\ll \frac{X}{L}\frac{|h|}{\varphi(|h|)}.
\]
The fixed target congruence only restricts the count. On the two axes the varying bases are \(9\) and \(5^{18}\). The draft’s reciprocal-order argument applies to both fixed bases, so the full edge second moment remains \(O(XL^3)\), and the summed degree energy remains \(O(XL^2)\). [Radomskii, Example 2 and Lemma 3.1](https://arxiv.org/html/2504.09954v7)

The first moment is \(\gg XL^{3/2}\). Consequently, \(\gg X\) distinct targets in the chosen class have \(\gg L^{3/2}\) edges and degree energy \(O(L^2)\). Deleting at most \(\epsilon L\) exponent vertices costs at most \(\sqrt{\epsilon L\sum_v d_v^2}\). After discarding vertices of degree above \(C\sqrt L\), a fixed fraction of the edges remains. A greedy maximal matching has size \(\gg L\), and each repetition removes only \(O(L)\) edges, so \(\gg\sqrt L\) edge-disjoint matchings can be taken after any permitted deletion. There are only finitely many mod-\(216\) classes, so the constants can be made uniform. [Draft PR #82 matching argument](https://github.com/Samsen879/a303656/pull/82/files)

### New same-target replay

At \(X=10^8\), take \(n=100000370\equiv146\bmod216\), in the restored class \(2\bmod24\). The actual axes are \(c\in\{3,4\}\), \(d\in\{4,5\}\). The only label that could leave an even squarefree norm modulo \(8\) is \((3,5)\), and it gives
\[
n-3^3-5^5=99997218
=9(169^2+3329^2)=507^2+9987^2.
\]
The residual divided by \(9\) is squarefree. The residual itself is divisible by \(9\) and fails the strict-squarefree condition. The inline replay checks the restored rule modulo \(216\).

```python
from math import isqrt

for b in range(216):
    if b % 24 in {2, 4, 8, 22}:
        c, d = next((c, d) for c in (0, 1) for d in (0, 1)
                    if (3**c + 5**d + 2) % 8 == b % 8)
        choices = [e for e in range(18) if pow(5, e, 27) == (b-18) % 27]
        assert len(choices) == 1 and choices[0] % 2 == d
        assert (b - 3**(3 if c else 4) - 5**choices[0]) % 216 == 18

X, n = 10**8, 100000370
C = [c for c in range(30) if 3**(8*c) >= X >= 3**(4*c)]
D = [d for d in range(30) if 5**(3*d) >= X >= 5**(2*d)]
assert (C, D) == ([3, 4], [4, 5])
assert X <= n <= 2*X and n % 216 == 146
assert [(c, d) for c in C for d in D
        if (n - 3**c - 5**d) % 8 == 2] == [(3, 5)]
m = n - 3**3 - 5**5
assert 2*m >= n and m % 27 == 18
assert m == 9*(169**2 + 3329**2) == 507**2 + 9987**2
assert all((m//9) % (j*j) for j in range(2, isqrt(m//9)+1))
```
## Any fixed admissible inert modulus, via increasing-prime repair

**Increasing-prime repair works for every fixed finite set of inert primes at which at least one of \(3,5\) is non-Wieferich.** It replaces the reciprocal-order condition and preserves the mod-\(216\) choice. For any fixed target modulus supported on \(2,3\) and such inert primes, every target class has a positive fraction of deletion-robust targets in each sufficiently large dyadic interval. The ordinary residual is a squarefree norm times a square multiplier of at most \(9\prod_{p\in S}p^2\). The constants depend on the fixed modulus and prime set. [Draft PR #82](https://github.com/Samsen879/a303656/pull/82/files)

### Increasing-prime repair

Refine the target modulus to a fixed \(M'\) divisible by \(216\) and \(p^3\) for every added inert prime \(p\in S\). Work in one target class \(n\equiv b\bmod M'\). Start with the mod-\(216\) choice of \(c\)-parity and \(d\bmod18\), taking \(c\ge v_3(M')\). This gives the intended \(2\)-valuation and either \(v_3(m)=0\) or \(v_3(m)=2\) for \(m=b-3^c-5^d\).

Process the added primes in increasing order. If \(m\) is a unit at \(p\), retain it. Otherwise choose \(B\in\{3,5\}\) with \(B^{p-1}\not\equiv1\bmod p^2\), and vary just its exponent. Take a step \(T\) that preserves mod \(216\) and all processed prime-power congruences, and is a multiple of \(\operatorname{ord}_p(B)\). Such a \(T\) can be chosen coprime to \(p\): periods at an earlier prime \(q<p\) divide \(q^{j-1}(q-1)\), and the base conditions use only powers of \(2,3\) in the period. Consequently,
\[
v_p(B^T-1)=1.
\]
Modulo \(p^3\), \(B^T\) generates the full subgroup \(1+p\mathbb Z/p^3\mathbb Z\). As the exponent moves by \(Tz\), \(0\le z<p^2\), the residual runs through every lift of its current value modulo \(p\). Choose the lift \(m\equiv p^2\bmod p^3\), which forces **exactly** \(v_p(m)=2\). Later steps preserve it.

After the last repair, freeze both exponents modulo their periods at the full modulus \(M'\). For base \(3\), use its unit period away from the \(3\)-part and keep \(c\ge v_3(M')\). Every actual label in the resulting box now has the same residual class modulo \(M'\). This final freezing handles prescribed prime powers above \(p^3\) and preserves the **full** target congruence.

### Transfer to the dyadic theorem

Write the residual as \(m=D u\), where
\[
D=2^\epsilon\,3^{2\eta}\!\prod_{p\text{ repaired}}p^2,
\]
and \(\epsilon,\eta\in\{0,1\}\) come from the mod-\(216\) box. The prescribed class for \(u\bmod M'/D\) is reduced and is \(1\bmod4\). The squarefree split-prime construction supplies \(\gg X/\sqrt{\log X}\) such \(u\) with \(X\le Du\le3X/2\). In the ordinary windows \(X^{1/8}\le3^c\le X^{1/4}\) and \(X^{1/3}\le5^d\le X^{1/2}\), the fixed exponent classes retain \(\asymp\log X\) choices per axis. Adding the actual labels gives targets in \([X,2X]\) with ordinary positive residuals \(m\ge n/2\). [Draft norm construction](https://github.com/Samsen879/a303656/pull/82/files)

For a label gap \(h\), the primitive cofactors have gap \(h/D\), an integer since the full label residues are fixed. The pair bound is at most \(O((X/\log X)|h|/\varphi(|h|))\). The varying bases remain fixed powers of \(3,5\), so the edge second moment remains \(O(X(\log X)^3)\) and the summed degree energy \(O(X(\log X)^2)\). This gives a positive fraction of distinct targets in each refined class with the draft’s deletion and matching conclusion: after any permitted \(\epsilon_0\log X\) exponent deletions, \(\gg(\log X)^{3/2}\) edges and \(\gg\sqrt{\log X}\) edge-disjoint matchings of size \(\gg\log X\). Every original target class has such refinements. [Radomskii, Example 2 and Lemma 3.1](https://arxiv.org/html/2504.09954v7) · [Draft matching proof](https://github.com/Samsen879/a303656/pull/82/files)

If both bases are Wieferich at a prime, this step has a precise limitation. Once both powers are held fixed modulo \(p\) by period increments, they are fixed modulo \(p^2\) as well, so an initial odd valuation \(1\) cannot be repaired within those increments. I make no assertion about how many such primes exist. The result treats each fixed admissible modulus and a positive fraction of its targets. It supplies neither a uniform growing-modulus estimate nor a pointwise representation theorem. [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### A concrete modulus and inline replay

A simpler union bound already works at modulus \(216\cdot7\cdot11\cdot19\cdot23\cdot31\cdot43\cdot47=455358995784\), because the sum of reciprocal orders of \(9\) at those seven primes is below one while holding the 5-exponent fixed. The increasing-prime method needs no reciprocal-order restriction. The replay verifies an eleven-prime set for which the previous reciprocal-order sum already exceeds \(1\), but every prime has a usable base. It also checks an actual same-target repair at \(7\): \(c=18\to24\) with \(d=31\) preserves the mod-\(216\) residual and changes \(v_7(m)\) from \(1\) to \(2\). Both labels lie in the ordinary windows, and the repaired residual is an exact two-square norm.

```python
from fractions import Fraction
from math import isqrt, prod

S = (7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79)
orders = [next(k for k in range(1, p) if pow(9, k, p) == 1)
          for p in S]
assert sum(Fraction(1, k) for k in orders) > 1
assert all(any(pow(b, p-1, p*p) != 1 for b in (3, 5)) for p in S)

P = (37, 337, 421, 673, 757, 1009, 1093, 1429, 1597,
     1933, 2017, 2269, 2437, 2521, 2689)
assert len(set(P)) == len(P)
assert all(p % 4 == 1 and all(p % j for j in range(2, isqrt(p)+1))
           for p in P)
u = prod(P)
m = 18 * 49 * u
n = m + 3**24 + 5**31
old = n - 3**18 - 5**31
X = n

assert n % 216 == 176 and m % 216 == old % 216 == 18
assert old % 49 == 42 and m % 343 == 49
assert all(3**(8*c) >= X >= 3**(4*c) for c in (18, 24))
assert 5**93 >= X >= 5**62 and 2*min(old, m) >= n
assert m == 889841198059910972404599**2 + 275335832956678969820835**2
```