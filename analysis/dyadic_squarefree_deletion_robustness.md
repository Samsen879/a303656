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
