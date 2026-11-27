# Deletion-resilient actual exponent matchings in all eight residue classes

This is a graph-theoretic addendum to the R5-08 actual matching result, not an attribution of the public sieve or a claim of historical priority. The earlier result provides one logarithmic matching within a positive proportion in each class. Here the number of genuine labeled witness edges is \(\gg(\log X)^{3/2}\); a bounded-degree subgraph keeps that scale after adversarial deletion of a fixed small multiple of \(\log X\) exponent vertices. The remaining graph contains \(\gg\sqrt{\log X}\) **edge-disjoint** matchings of size \(\gg\log X\) each. Different matchings may share vertices. This is not a complete two-axis rectangle, and says nothing about arbitrary specified targets or density one.

## Public input and eight actual heads

Put \(L=\log X\). Use [Radomskii v7, Theorem 1.1 and Example 2](https://arxiv.org/html/2504.09954v7) for the order of cardinality \(X/\sqrt L\) and the pair upper bound \(O((h/\varphi(h))X/L)\) for odd primitive sums of two squares \(S'\), and the additive representation theorem. We do not use a specific asymptotic constant. Both residue parts of \(S'\) modulo 8, namely 1 and 5, still have cardinality \(\asymp X/\sqrt L\). Multiplication by 5 maps either part injectively into the other part at height \(5X\), remaining in \(S'\) because the integers in \(S'\) are supported on split primes. Thus each part contains at least half the total at height \(X/5\). The pair upper bound is inherited by restriction. It transfers to \(2S'\) at even gaps by dividing the gap by two, and odd gaps give zero. These sets consist of true positive norms.

For an odd target residue \(r\bmod8\), use \(S'\cap(1\bmod8)\); for an even residue use \(2S'\subset(2\bmod8)\). Fix the two exponent parities so that the shift \(3^c+5^d\) is respectively \(r-1\) or \(r-2\bmod8\). The four parity pairs have the four different even shift residues \(2,6,4,0\bmod8\). Keep actual labels and multiplicity even when distinct labels give equal shifts.

The labelled shift count up to \(X\) is \(\asymp L^2\), with the same order at \(X/2\), and any equality multiplicity is \(O(L)\) because a first exponent determines the other when the shift is given. For a first label and a fixed second-axis exponent, the congruence for the other label modulo \(p\ne3\) fixes at most one class modulo \(\operatorname{ord}_p(9)\) in the first-axis parity parameter. Thus each prime contributes at most \(O(L(1+L/\operatorname{ord}_p(9)))\) possible other labels. For any fixed \(a>1\), the sum \(\sum_{p\nmid a}\log p/(p\,\operatorname{ord}_p(a))\) converges. In the dyadic order bucket \([T,2T)\), primes up to \(T^2\) contribute \(O(\log(2T)/T)\) by Chebyshev; larger primes divide \(\prod_{j<2T}(a^j-1)\), whose logarithm is \(O_a(T^2)\), and contribute \(O_a(1/T)\). The finite excluded primes cost a constant. The \(+1\) endpoint count contributes \(O(L\log L)\) per first label for the theorem's cutoff \(p\le L^\alpha\). These estimates give the required weighted congruence bound \(O(L^4)\). The public representation theorem now gives \(\gg X\) targets \(n\le X\) in each class with \(\gg L^{3/2}\) labelled edges. By removing a sufficiently short initial segment, the same holds with \(n\ge cX\) for some fixed \(c>0\); no dyadic interval lower bound is claimed here.

## Degree control and robust matchings

For a fixed first-axis vertex, the remaining shifts are a single base-25 geometric list with a fixed prefactor. For a fixed second-axis vertex they form a base-9 list. Put \(W(d)=d/\varphi(d)\). For \(a=9,25\), the average \(\sum_{j\le CL}W(a^j-1)\ll L\) follows from the squarefree divisor expansion \(W(n)=\sum_{d\mid n}\mu^2(d)\prod_{p\mid d}(p-1)^{-1}\) and exact multiplicative orders. Each divisor is used at most \(CL/\operatorname{ord}_d(a)\) times. For the sum of weights of all divisors with order at most \(T\), the supporting primes divide \(\prod_{j\le T}(a^j-1)\); its logarithm is \(O_a(T^2)\). The reciprocal-prime product up to \(T^4\) bounds their divisor weight by a fixed power of \(\log(2T)\), and the larger primes cost a bounded factor. Dyadic summation of weight divided by order converges. The fixed power prefactor changes \(W\) by at most a constant. Since each gap exponent is realized in only \(O(L)\) pairs in a single list, the sum of \(W\) over nonzero ordered shifts is \(O(L^2)\).

The public pair bound now bounds the sum of squares of the degree of one vertex by \(O(XL)\): the off-diagonal contributes \(O((X/L)L^2)\), and the diagonal \(O(X\sqrt L)\). Summing over all \(O(L)\) vertices gives total degree energy \(O(XL^2)\). Markov retains \(\gg X\) of the preceding high-edge targets with \(E(n)=\sum_v\deg_n(v)^2\le K L^2\) for a sufficiently large fixed \(K\).

Discard vertices of degree above \(B\sqrt L\). Their edges are at most \(K L^{3/2}/B\) by charging each degree against its square. Choose \(B\) large enough so that a fixed proportion of the edges survives. Arbitrarily deleting up to \(\epsilon L\) further exponent vertices costs at most \(\sqrt{\epsilon K}L^{3/2}\) edges by Cauchy. Choose \(\epsilon\) small enough to maintain \(\gg L^{3/2}\) edges and maximum degree \(O(\sqrt L)\). This budget can absorb discarding all exponents below \(c' L\) on both axes for sufficiently small fixed \(c'\). A maximal matching has at least the remaining edge count divided by twice the maximum degree; as long as a fixed proportion of edges survives, this is \(\gg L\). Each removed matching has only \(O(L)\) edges, so repeat \(\gg\sqrt L\) times, producing edge-disjoint matchings. This argument supplies redundancy without assuming mixed-label independence.

## Finite native replay

At \(n=20091\equiv3\bmod8\), after removing exponent 0 from both axes, the following two actual matchings remain. Their primitive odd remainders are all \(1\bmod8\). This illustrates the graph claim, not the numerical asymptotic threshold.


```python
from math import gcd
n=20091
rows=(((4,4,8,139),(2,6,19,64),(6,2,4,139)),
      ((2,4,31,136),(4,6,17,64),(8,2,7,116)))
all_labels=set()
for m in rows:
    assert len({c for c,d,a,b in m})==len({d for c,d,a,b in m})==3
    for c,d,a,b in m:
        assert c*d>0 and c%2==d%2==0
        assert n==a*a+b*b+3**c+5**d and gcd(a,b)==1 and (a*a+b*b)%8==1
        assert (c,d) not in all_labels
        all_labels.add((c,d))
```
