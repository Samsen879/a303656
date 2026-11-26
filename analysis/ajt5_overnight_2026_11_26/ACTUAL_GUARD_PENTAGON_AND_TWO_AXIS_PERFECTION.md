# Perfect two-axis packing and an actual three-axis guard pentagon

**Two retained CRT axes give a perfect conflict graph. Three axes already allow an induced \(C_5\) from actual ordinary order guards.** I realized the five-cycle at one represented target, with all five heads above rank 11. The weighted gap \(10\) versus \(25/2\) is genuine for those guard positions. A rank-11 ledger with five genuine rigid descendants at each position remains conditional. [Phase-local packing baseline](https://github.com/Samsen879/a303656/commit/e917d1eefc8f3b08676b6814b114d9bcffe908b6)

### Exact packing on two axes

Erase the pivot coordinate and restrict to a product window. On each remaining axis, nonempty clipped prefixes form a laminar family. Its compatibility graph has a universal vertex in every connected induced subgraph: a maximal prefix in that component contains all the others. Therefore the single-axis conflict graph has neither an induced \(P_4\) nor an induced \(2K_2\).

The full conflict graph is the union of the axis conflict graphs. On an induced cycle of length at least five, each axis can supply at most two cycle edges. Three edges would contain either three consecutive edges or two disconnected edges, giving one of the forbidden induced subgraphs. In particular, a conflict graph on \(k\) axes has no induced cycle of length at least five and greater than \(2k\).

For two axes, the **complement** also has no induced cycle of length at least five. Suppose it had a cycle \(v_0,\ldots,v_{\ell-1}\). Each axis compatibility graph contains the cycle, so each has a universal vertex there. Those vertices must be distinct and adjacent in the cycle. Call them \(v_0,v_1\), respectively. In the first graph with \(v_0\) removed, \(v_1\) has only the neighbor \(v_2\). The graph is still connected, so \(v_2\) must be universal there. Symmetrically, \(v_{\ell-1}\) is universal in the second graph with \(v_1\) removed. This gives the chord \(v_2v_{\ell-1}\) in both graphs, a contradiction.

The conflict graph and its complement are therefore perfect. For integer multiplicities, duplicate each position as many times as it is charged. The same proof applies to the expanded family. Coloring the compatibility graph partitions the copies into pairwise disjoint families, using exactly the maximum simultaneous live weight. This proves that the two-axis packing bound is exact for full lower guards. For necessary helper tags, the same calculation gives an upper bound on the live-source count. [Strong Perfect Graph Theorem](https://arxiv.org/abs/math/0212070)

### An arithmetic pentagon

Write \(x=d\bmod9,\ y=d\bmod25,\ z=d\bmod7\), with \(c=1\) and even \(d\). The following five heads all have base-5 lifting depth **one**.

| Guard | Head | Exact order | Lower position |
|---|---:|---:|---|
| \(A\) | 19 | 9 | \(x=0\) |
| \(B\) | 1171 | 45 | \(x=1,\ y\equiv1\pmod5\) |
| \(C\) | 251 | 25 | \(y=0\) |
| \(D\) | 211 | 35 | \(y\equiv1\pmod5,\ z=0\) |
| \(E\) | 43 | 42 | \(x\equiv1\pmod3,\ z=1\) |

The order-35 head is certified directly from the fixed value \(\Phi_{35}(5)=211\cdot631\cdot4201\cdot85280581\) and modular powers. CRT makes all five guards actual at one \(n=3+5^2+u^2+v^2\). Fixing each head’s own digit off its center then makes its square-precision veto exactly the listed guard. The replay also includes **20771 as a separate genuine rigid row** on the same target. With the five native digits free, the ordinary rows have private centers and peel in this panel.

The incompatibilities are exactly \(AB,BC,CD,DE,EA\). For multiplicities \(m_i\), the maximum live weight of the five positions is \(\max_i(m_i+m_{i+2})\), with cyclic indices. At five copies per position this is \(10\), whereas the best unconditioned fractional disjoint-family charge is \(25/2\). Each disjoint family charges at most two groups, and putting \(5/2\) on each cycle edge attains the lower bound.

**A one-axis cut recovers the rank-11 certificate.** At \(z=0\), use the disjoint pairs \(AB,CD\). At \(z=1\), use \(AE,BC\). At other \(z\), use \(AB\) and the singleton \(C\). Each branch costs at most \(10\). Thus five groups of at most five incoming labels would pass this part of the phase-local test. To realize those labels as rigid descendants would require actual incoming rigid sources at the centered first prefixes of the five helpers, with the appropriate surviving lower guards. The ordinary veto rows supply the positions.

The inline replay checks the actual guard graph, exact weighted maximum, and one-axis cut.

```python
from itertools import combinations, product
from math import isqrt, prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

# Prime, order, prime divisors of order, center exponent, norm coordinates.
R = [(19,9,(3,),0,3,123), (1171,45,(3,5),46,3,1200701),
     (251,25,(5,),0,0,59514), (211,35,(5,7),56,0,33248),
     (43,42,(2,3,7),22,0,797)]
for q,w,fs,d,a,b in R:
    assert all(q % j for j in range(2,isqrt(q)+1))
    assert pow(5,w,q)==1 and all(pow(5,w//p,q)!=1 for p in fs)
    assert pow(5,w,q*q)!=1
    assert (25+a*a+b*b-pow(5,d,q*q))%(q*q)==0

Q = 20771
assert pow(5,10385,Q*Q)==1 and pow(5,10385,Q**3)!=1
P = 12*31*71*5167*19531
S = [(q,a,b) for q,_,_,_,a,b in R] + [(Q,0,151149254)]
u = crt([(7,P),(1,7),(2,11)]+[(a,q*q) for q,a,b in S])
v = crt([(0,P),(3,7),(2,11)]+[(b,q*q) for q,a,b in S])
n = 28+u*u+v*v
assert n%12==5 and (n-4)%(Q*Q)==Q

def veto(q,d):
    r = (n-3-pow(5,d,q*q))%(q*q)
    return r!=0 and r%q==0

G = [set() for _ in R]
for x,y,z in product(range(9),range(25),range(7)):
    d = crt([(0,2),(x,9),(y,25),(z,7),(0,31),(0,67)]
            + [((e+1)%q,q) for q,_,_,e,_,_ in R])
    mask = tuple(veto(q,d) for q,_,_,_,_,_ in R)
    assert mask==(x==0, x==1 and y%5==1, y==0,
                  y%5==1 and z==0, x%3==1 and z==1)
    assert veto(Q,d)==(y%5==0)
    for i,on in enumerate(mask):
        if on:
            G[i].add((x,y,z))

edges = {(i,j) for i,j in combinations(range(5),2) if not G[i]&G[j]}
assert edges=={(0,1),(1,2),(2,3),(3,4),(0,4)}
for z in range(7):
    groups = ((0,1),(2,3)) if z==0 else (((0,4),(1,2)) if z==1 else ((0,1),(2,)))
    assert all(len(g)==1 or g in edges for g in groups)
    assert set().union(*map(set,groups)) == {
        i for i,T in enumerate(G) if any(w[2]==z for w in T)}
print("PASS")
assert max(sum(5*(p in g) for g in G) for p in product(range(9),range(25),range(7)))==10

```

The ordinary heads with their own digits fixed give the five actual positions; the five copies per position are weights for testing the certificate, not five verified rigid sources per position. On two axes the coloring conclusion uses the Strong Perfect Graph Theorem after checking both the conflict graph and its complement for induced cycles of length at least five. No theorem for arbitrary three-axis guards is inferred from the exact cut in this example.
