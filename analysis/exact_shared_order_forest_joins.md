# Exact shared-order forest messages for the actual bases 3 and 5

A forest of hidden order overlaps permits **exact aggregation by edge messages**. Each message records which shared residues can be extended through one subtree. Keeping only the fact that each edge is separately feasible can fail, even on a three-prime path. I verified both outcomes for the native bases 3 and 5, with the same prime panel and the same coarse exponent class.

## Exact aggregation and a quantitative bound

Let \(h_{i,q}\) be the effective order for base \(q\in\{3,5\}\) in row \(i\). Fix a coarse exponent residue modulo \(a_q\) for each base. Filter each local relation by compatibility with those coarse residues before projecting out private digits.

For rows \(i,j\), put \(g_{ij,q}=\gcd(h_{i,q},h_{j,q})\). Join the rows by an edge if either \(g_{ij,q}\nmid a_q\). The edge records the remaining shared residues modulo \(g_{ij,q}\). Its alphabet has size
\[
B_{ij}=\prod_{q=3,5}\frac{g_{ij,q}}{\gcd(g_{ij,q},a_q)}.
\]
If the graph is a forest, every hidden shared prime-power digit belongs to exactly one edge. A digit occurring at three rows would create a triangle. The edge alphabets are therefore independent after the coarse residues are fixed.

Root each tree. A row keeps a local tuple only if its label on every child edge belongs to the message from that child. It then sends its surviving labels on the parent edge. A nonempty relation at every root is equivalent to feasibility. Inductively, each sent label has a witness throughout its subtree, and witnesses from distinct child subtrees agree on every common digit once the parent tuple is fixed. Generalized CRT then produces the exponents. This is the bottom-up semijoin argument specialized to the order digits. If every row’s relation is a Cartesian product of its allowed edge labels, separate edge checks already suffice. [Yannakakis, *Algorithms for Acyclic Database Schemes*](https://www.vldb.org/conf/1981/P082.PDF)

For a fixed coarse fiber, the dense shared grid has \(\prod_e B_e\) states. One bottom-up pass sends at most \(\sum_e B_e\) bits using membership vectors. This counts the messages, with the local relations already tabulated. There is also a test for when **plain** coarsening is safe. If row \(i\) rejects a fraction \(\delta_i\) of its incident label tuples, then at least
\[
\left(\prod_e B_e\right)\max\left(0,1-\sum_i\delta_i\right)
\]
shared assignments survive. This follows from the union bound under the uniform assignment of independent edge labels. In particular, a coarse false positive requires \(\sum_i\delta_i\ge1\).

For exact valuation-one hits, one may use the full prime-square orders directly. The replay uses the smaller prime-level orders and checks the conditions that justify them. At each \(p\), at least one base gains a factor \(p\) in its order modulo \(p^2\), and neither another row's order nor the fixed coarse modulus for the chosen base contains that factor. If the coarse stratum already fixes the lifting digit, use the full prime-square orders instead. A prime-level match with residual zero modulo \(p^2\) becomes an exact hit by adding one prime-level order to that base’s exponent. This changes only its private lifting digit. The argument applies within a fixed transient or periodic exponent stratum.

## Native positive and falsifier

Use primes \(7,11,31\), fix \(c\) even, and leave \(d\) unrestricted. The actual prime-level order pairs are \((6,6),(5,5),(30,3)\). The hidden graph is \(7\!-\!31\!-\!11\). The left edge has nine labels \((c\bmod6,d\bmod3)\) and the right edge has five labels \(c\bmod5\). Thus the dense fiber has 45 states, and the two messages into row 31 use 14 bits.

Fix target residues 0 at 7 and 1 at 11, modulo their prime squares. The leaf messages are \(\{(0,0),(2,1),(4,2)\}\) and \(\{1,2\}\), respectively.

| Target residue modulo \(31^2\) | Tuples at row 31 | Pass left message | Pass right message | Pass both |
|---:|---:|---:|---:|---:|
| 2 | 3 | 1 | 2 | 0 |
| 8 | 2 | 1 | 1 | 1 |

At residue 2, the CRT target is \(3{,}073{,}280\). Every pair of primes admits exact hits with even \(c\), but the full panel does not. This falsifies independent edge feasibility on a forest. At residue 8, the CRT target is \(1{,}745{,}184\), and \((c,d)=(3742,46037)\) gives all three exact hits.

This certifies a native discrepancy at fixed width. I did not establish a family with growing numbers of false-positive coarse classes or growing separator widths. The example concerns unrestricted simultaneous hits. The previous CRT blocking construction concerns avoidance below an ordinary height cutoff, and the public project’s N-009 concerns restricted active-shift families. [Public theorem index](https://github.com/Samsen879/a303656/blob/main/docs/THEOREM_INDEX.md)

## Inline replay

The standard-library replay computes the actual orders, builds the hidden graph, runs the tree reduction, and verifies the exact prime-square witnesses.

```python
from math import gcd, prod

P = (7, 11, 31)
coarse = (2, 1)  # c even, d unrestricted

def cycle(q, m):
    values = [1]
    while values[-1]*q % m != 1:
        values.append(values[-1]*q % m)
    return values

A = {p: tuple(cycle(q, p) for q in (3, 5)) for p in P}
h = {p: tuple(map(len, A[p])) for p in P}
L = {p: tuple(len(cycle(q, p*p)) for q in (3, 5)) for p in P}
assert list(h.values()) == [(6, 6), (5, 5), (30, 3)]
assert list(L.values()) == [(42, 42), (5, 55), (930, 93)]
assert all(h[r][j] % p for p in P for r in P if p != r for j in (0, 1))
assert all(any(L[p][j] == p*h[p][j] for j in (0, 1)) for p in P)

def separator(p, r):
    return tuple(gcd(x, y) for x, y in zip(h[p], h[r]))

neighbors = {
    p: [r for r in P if r != p and
        any(a % g for a, g in zip(coarse, separator(p, r)))]
    for p in P
}
assert neighbors == {7: [31], 11: [31], 31: [7, 11]}
assert [prod(g//gcd(g, a) for g, a in zip(separator(31, r), coarse))
        for r in neighbors[31]] == [9, 5]

def relations(targets):
    R = {}
    for p, t in zip(P, targets):
        R[p] = {
            tuple((c % u, d % v)
                  for u, v in (separator(p, r) for r in neighbors[p]))
            for c, x in enumerate(A[p][0])
            for d, y in enumerate(A[p][1])
            if c % gcd(coarse[0], h[p][0]) == 0 and (x+y-t) % p == 0
        }
    return R

def reduce_tree(R, p, parent=None):
    rows = R[p]
    for i, r in enumerate(neighbors[p]):
        if r != parent:
            child = reduce_tree(R, r, p)
            rows = {row for row in rows if row[i] in child}
    if parent is None:
        return rows
    j = neighbors[p].index(parent)
    return {row[j] for row in rows}

def target(residues):
    M = prod(p*p for p in P)
    return sum(t*(M//(p*p))*pow(M//(p*p), -1, p*p)
               for t, p in zip(residues, P)) % M

def hit(n, p, c, d):
    r = (n-pow(3, c, p*p)-pow(5, d, p*p)) % (p*p)
    return r != 0 and r % p == 0

bad = relations((0, 1, 2))
assert all(bad.values())
assert len(bad[31]) == 3
assert [sum(row[i] in reduce_tree(bad, r, 31) for row in bad[31])
        for i, r in enumerate(neighbors[31])] == [1, 2]
assert not reduce_tree(bad, 31)
n = target((0, 1, 2))
assert n == 3073280
for pair, w in [((7, 11), (2, 1597)), ((7, 31), (1890, 465)),
                ((11, 31), (12, 2))]:
    assert w[0] % 2 == 0 and all(hit(n, p, *w) for p in pair)

good = relations((0, 1, 8))
assert reduce_tree(good, 31) == {((4, 2), (2, 0))}
n = target((0, 1, 8))
assert n == 1745184
assert all(hit(n, p, 3742, 46037) for p in P)
```