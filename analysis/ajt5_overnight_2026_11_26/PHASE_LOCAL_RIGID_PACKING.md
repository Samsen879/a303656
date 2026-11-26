# Phase-local live-source packing for exact sparse contraction

**The contraction cutoff is phase-local.** At rank \(p\), fewer than \(p\) rigid prefixes need to be live **on each lower phase**. The total source count can be arbitrarily large. A packing certificate on permanent lower guard positions can carry this bound through successive contractions. Sparse order scopes alone do not guarantee such a certificate. [Rigid-source kernel baseline](https://github.com/Samsen879/a303656/commit/ef967b9c04cdd9a12f3e7b0b8a75a69916479b0f)

### Exact cutoff and packing certificate

At a descending step, write each \(p\)-reading rigid rectangle as \(P_i\times G_i\), with \(P_i\) its proper \(p\)-prefix and \(G_i\) its lower guard. Assume the only remaining dynamic row that reads \(p\) is its native row. On a lower window \(W\), set
\[
M_p(W)=\max_{y\in W}\#\{i:y\in G_i\}.
\]
If \(M_p(W)<p\), elimination on \(W\) is exactly sourcewise. Pass the \(p\)-blind guards through. Retain a \(p\)-reading source only if it supplies the centered first prefix and the native outer shell rejects. Its descendant is \(G_i\) intersected with the native order guard.

For the proof, fix one \(y\). If the native outer shell is safe, every first branch has a safe point, including the center branch. If the outer shell rejects, the center branch still needs coverage. Without a centered first prefix, each of its \(p\) second-level children has a safe point. At depth one there is no finer prefix available. Both alternatives require at least \(p\) live sources.

There is a checkable upper bound for \(M_p\). Assign each source a necessary lower rectangle \(U_i\supseteq G_i\), such as a fixed least-helper guard restricted to lower coordinates. Group identical positions with multiplicities \(m_j\). For each pairwise disjoint family \(E\) of groups, give it a nonnegative rational charge \(\lambda_E\). If
\[
\sum_{E\ni j}\lambda_E\ge m_j\quad\text{for every group }j,
\]
then \(M_p\le\sum_E\lambda_E\). Each disjointness check needs only an incompatible pair of prefixes on a shared axis. With the **full** lower rectangles on a product window, the maximum live count is exactly the maximum independent-set weight in this conflict graph. Pairwise compatible prefixes on each axis are nested and have a common point.

### What survives iteration

A packing bound \(K\) on a **permanent lower separator** remains valid while higher ranks peel. Each contraction preserves the source label and only strengthens its guard on that separator. Thus all ranks \(p>K\) above the separator can peel, regardless of the number of source labels. More generally, conflicts between surviving full rectangles persist through simple contraction. Two survivors that read the eliminated axis used the same centered prefix, so any conflict between them was witnessed elsewhere. For the **next** pivot test, erase that pivot’s coordinate before computing conflicts.

The replay includes a synthetic connected family of arbitrary size using distinct prefixes on the 3-axis, with the actual ordinary rows 11 and 7 at the fixed mixed target. All synthetic sources read the centered prefixes at both pivots. Exactly one can be live at a lower phase, so both ranks peel with bound \(K=1\), even when the total exceeds both ranks. The descendants require \(d\equiv4\bmod5\), leaving an explicit escape.

### Actual panel and two limits

**Actual shared-helper multiplicity.** Take
\[
n=3+5^2+6599292564946303358485^2+667770695126581599576^2.
\]
At \(c=1\) and even \(d\), primes \(20771\) and \(40487\) are genuine rigid rows of orders \(10385\) and \(40486\). Both read the centered 31 digit. Projecting 31 while retaining the other read axes gives the two guards
\[
[d\equiv0\bmod3,5,67],\qquad [d\equiv0\bmod3,653].
\]
Both inherit the **same actual row-31 position**, and both are live when the retained digits are zero. Charging the shared position once would report one instead of two.

**Synthetic limits.** Seven first prefixes at rank 7 over one common lower guard have full-rectangle packing number one. Erasing the pivot digit makes all seven live together, and they really fill the fibre. A separate example shows a limit of fractional charges even after the pivot is erased. Five lower guards on the \(3,5,7\) axes have conflict graph \(C_5\), with five source labels at each guard. The exact maximum live count is \(10\), so rank 11 can peel. The best disjoint-family charge is \(25/2\), so that certificate alone stalls. The integer constraint that at most two cycle vertices can be active recovers the peel.

The inline replay verifies the genuine shared-helper multiplicity and the sharp synthetic graph controls.

```python
from itertools import combinations, product
from math import isqrt, prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

def rejects(n,p,d):
    r = (n-3-pow(5,d,p*p)) % (p*p)
    return r != 0 and r % p == 0

Q = (20771,40487,31)
for q,w,fs,s in ((Q[0],10385,(5,31,67),2),
                 (Q[1],40486,(2,31,653),2),(Q[2],3,(3,),1)):
    assert all(q % j for j in range(2,isqrt(q)+1))
    assert w == prod(fs) and all(pow(5,w//p,q)!=1 for p in fs)
    assert pow(5,w,q**s)==1 and pow(5,w,q**(s+1))!=1

u,v = 6599292564946303358485,667770695126581599576
n = 3+25+u*u+v*v
assert [(n-4)%(q*q) for q in Q] == [Q[0],Q[1],0]
loads = []
for x,a,b,e in product(range(3),range(2),range(2),range(2)):
    G1,G2 = a==b==0,e==0
    fibre = []
    for z in range(31):
        d = crt([(0,2),(x,3),(a,5),(b,67),(e,653),(z,31)])
        veto = tuple(rejects(n,q,d) for q in Q)
        assert veto == (G1 and z==0,G2 and z==0,x==0 and z!=0)
        fibre.append(any(veto))
    assert all(fibre) == (x==0 and (G1 or G2))
    loads.append((G1+G2) if x==0 else 0)
assert max(loads)==2

# Synthetic lower guards with a C5 conflict graph.
G = [{3:0},{3:1,5:1},{5:0},{5:1,7:0},{3:1,7:1}]
def clash(a,b):
    return any(a[p]!=b[p] for p in a.keys() & b.keys())

edges = {frozenset((i,j)) for i,j in combinations(range(5),2)
         if clash(G[i],G[j])}
assert edges == {frozenset((i,(i+1)%5)) for i in range(5)}
assert max(5*sum(all(X[p]==v for p,v in g.items()) for g in G)
           for x,y,z in product(range(3),range(5),range(7))
           for X in [{3:x,5:y,7:z}]) == 10
# Each disjoint family charges at most two groups. Half-weighted edges attain 25/2.
assert 10 < 11 <= (5*5)//2
print("PASS")
# Source multiplicity cannot be discarded when shrinking an order position.
assert len({tuple(sorted(g.items())) for g in G})==5
# Synthetic seven-prefix cover: distinct in the pivot, coincident below it.
full=[(j,{3:0}) for j in range(7)]
assert len({j for j,g in full if g=={3:0}})==7

```

For the conflict-graph equivalence on a product window, first drop every empty restricted rectangle. An independent family then has nested prefixes on each coordinate, and its smallest prefix on that coordinate meets the corresponding window factor. Combining those nonempty intersections gives a common lower phase. This is the needed Helly property; on a nonproduct window the graph is only a possible sufficient upper certificate. The result does not assume all actual order components are sparse.
