# Distinct-reader load on common exceptional terminals

**Branching forces a tradeoff between the number and the size of common exceptional terminals.** In a divisor-minimal tail modulus, suppose \(q\) is a retained inert prime ordinary to both bases and \(v_q(n)=1\). Put
\[
B_q=\left\lfloor\frac{1+\sqrt{4q-3}}2\right\rfloor,\qquad
b_q=\left\lceil\frac q{B_q}\right\rceil.
\]
Let \(K\) count the retained common exceptional primes above \(q\), let \(H\) be the largest, and let \(r_0\) be a lower bound on the smallest direct reader of \(q\). Then \(K\ge1\) and
\[
H\ \ge\ r_0(2q)^{\lceil b_q/K\rceil-1},
\]
with strict inequality if \(b_q>K\). For example, a retained valuation-one row at \(379\) requires either **at least 20 common exceptional primes above it** or one at least **\(5{,}171{,}835\)**. The first possible inert direct reader is \(6823\), which gives the latter bound. [Valuation-one branching lemma](https://github.com/Samsen879/a303656/commit/9cbc462725e174347eca539a3146d2edaa2006b6)

### Why sharing a terminal has a size cost

Take the distinct active readers supplied by the precision-essential witness at \(q\). There are at least \(b_q\). At each non-common row choose one larger successor reading its prime to the necessary depth on an ordinary axis. Precision closure supplies this edge, since the row is retained at precision at least two. Stop at a common exceptional row. The chosen edges form an increasing forest. [Exact precision closure](https://github.com/Samsen879/a303656/commit/fac27d29f366a0aed19e2ce917577d8084e9166e)

At a vertex \(v\), the incoming branches carry disjoint sets of initial reader primes. Every incoming predecessor prime divides \(v-1\). If \(v\) is itself an initial reader of \(q\), then \(q\mid v-1\) as well. Thus a merge must pay for the product of its distinct incoming primes, and absorption into another direct reader must pay for the incoming prime **and** \(q\). Induction gives \(v\ge r_0(2q)^{j-1}\) when \(v\) carries \(j\) initial readers, strictly for \(j\ge2\). Some terminal carries at least \(\lceil b_q/K\rceil\), proving the bound. This handles paths that merge at a later vertex and paths that run through another initial reader.

### Weighted bound across several gates

Choose a cutoff \(X\) and valuation-one ordinary gates \(q\le X\). For a potential reader \(\ell\), use the certified shallow charge \(w_{q\ell}\), between zero and \(B_q\), from its actual orders and target residue. For a deep reader of maximum read depth \(d\), use \(w_{q\ell}=q^{2-d}/\theta_q\), where \(\theta_q\) is the parent’s exact passing fraction among the higher lifts at a first repair point. These weights obey \(\sum_\ell w_{q\ell}\ge q\): either the shallow rows cover all \(q\) first points, or at a missed point the deeper rows alone must cover fraction \(\theta_q\). Therefore at least
\[
b_q^{>X}=\left\lceil
  \frac{\bigl(q-\sum_{\ell\le X}w_{q\ell}\bigr)_+}{B_q}
\right\rceil
\]
direct readers must lie above \(X\).

Route these readers in one forest above \(X\). A reader shared by several gates is **one physical vertex**. Its order carries the product of the distinct gate primes it reads. These primes are at most \(X\), so they are distinct from all incoming forest predecessors. The same product induction yields
\[
\prod_{\substack{\tau>X\\\tau\ {\rm retained\ common}}}\tau
\ \ge\ \prod_{q\le X}q^{\,b_q^{>X}},
\]
with the right product over the selected gates. At an individual reader, the exponent of a gate prime can be strengthened to its **maximum** read depth across the two bases. The two base orders divide the same \(\ell-1\), so their depths cannot be added.

### Real branch reuse

At \(n=1068534901851147339\), rows 43 and 71 both veto at one exact repair of row 7. Each can be repaired independently. The same row \(91591\) passes on each partial repair and has exact valuation one on the combined repair. It reads both 43 and 71 in both base orders. It is ordinary, and the panel has another passing exponent pair. This tests physical reuse without supplying a minimal tail obstruction.

```python
from math import isqrt

p,r,s,h = 7,43,71,91591
for q,ws,F in [(r,(42,42),(2,3,7)), (s,(35,5),(5,7)),
               (h,(91590,45795),(2,3,5,43,71))]:
    assert q%4==3 and all(q%d for d in range(2,isqrt(q)+1))
    for a,w in zip((3,5),ws):
        assert pow(a,w,q)==1 and pow(a,w,q*q)!=1
        assert all(pow(a,w//j,q)!=1 for j in F if w%j==0)
assert (h-1)%(2*r*s)==0 and (h-1)%p!=0

n,c,u,v = 1068534901851147339,8388819691,6828109050,26466135360
def R(c,d,q,e=2):
    m=q**e
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert R(1,2,p)==28 and all(R(1,2,q,1) for q in (r,s,h))
for d,w in [(2,(0,r,s)),(2+u,(0,0,s)),(2+v,(0,r,0))]:
    assert tuple(R(c,d,q) for q in (p,r,s))==w and R(c,d,h,1)
assert [R(c,2+u+v,q) for q in (p,r,s,h)]==[0,0,0,h]
assert R(1,50332918142,p)==0
assert all(R(1,50332918142,q,1) for q in (r,s,h))

q=379
for j,d in ((1,3),(3,5),(5,17),(7,3)):
    assert (1+2*q*j)%d==0
assert all(6823%d for d in range(2,isqrt(6823)+1))
B=(1+isqrt(4*q-3))//2
assert (B,(q+B-1)//B,2*q*6823+1)==(19,20,5171835)
print("PASS")
```

The branching demand applies only to retained ordinary gates with **exact** \(v_q(n)=1\). Higher-valuation rows can occur along the routes, where the proof uses only their order dependencies. The bounds apply in the fixed tail \(c\ge v_3(M)\). They constrain terminal size and reuse without establishing a new unconditional count of common exceptional primes.

For the weighted multi-gate induction, the local label primes are at most the cutoff and the forest predecessors are strictly above it, so their factors do not overlap. At a merge the incoming subtrees are disjoint in the chosen forest; a physical reader is one vertex regardless of how many gate labels it carries. The examples do not supply a minimal obstruction and the already proved all-target count of common exceptional primes is not increased here.
