# Guarded rank-five exclusion with at most twenty sources

**On the muted slice, a first essential nonlinear elimination at \(5\) needs at least 21 surviving rigid sources.** This includes mixed 5-adic prefix depths and keeps every ternary guard live throughout the calculation. It excludes rank \(5\) as the first nonlinear step with ten or twelve common sources. The argument leaves rank \(7\) and the all-linear route to rank \(3\) open. [Published muting step](https://github.com/Samsen879/a303656/blob/c3cee9bfda27490e465f67c818cb6c7b85ff3b9e/analysis/ajt5_overnight_2026_11_26/LOW_ORDER_HELPER_MUTING.md)

### Exact normal form

Fix \(n,c\) and the parity of \(d\), with rows \(3,31,5167,71\) inactive. Before the first nonlinear step, each surviving cylinder has one original rigid-prime source. At a higher odd coordinate \(p\), its only single-source contraction is through the actual dynamic row at \(p\). That row must reject the outer shell, and the source must supply the centered first-level cylinder. The center itself is safe, and the next shell is safe whenever the outer shell is rejected, so a deeper cylinder cannot substitute. The contraction removes the centered digit and intersects the source’s remaining guard with the helper’s order guard. It preserves the source label and cannot erase a still-uneliminated order factor.

At rank \(5\), write source \(s\) as \(G_s\times T_s\), with a ternary guard \(G_s\) and a 5-adic prefix \(T_s\). If \(F_v\) is the set of ternary points at which the entire prefix \(v\) is covered by sources at or below it, then
\[
F_v=\bigcup_{s:T_s=v}G_s\ \cup\ \bigcap_{j=0}^{4}F_{vj}.
\]
At the last depth the child term is empty. Thus a complete prefix witness contributes the **intersection** of its leaves’ guards, and alternative witnesses contribute a union. Each leaf retains its source label. A nine-leaf witness can have four first-level leaves and five second-level leaves under the remaining child.

### Why twenty sources fail

The least helper in a surviving lineage can read only \(3\) and \(5\) in its odd order. Any other odd factor would have required a still smaller helper to remove it. The actual orders give two restrictions. [Exact cyclotomic products and order guards](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md)

- A first-level 5-cylinder with ternary depth at most one lies either over the fixed ternary branch \(A\) of row \(7\), or in the fixed first 5-branch of row \(11\). The relevant orders are \(3,6,5,10,15,30\). Their cyclotomic products at \(5\) are squarefree, so none supplies a raw rigid source. Rows \(31,71\) are muted, and orders \(15,30\) have no inert helper. If \(7\) or \(11\) is absent or inactive, choose its designated branch arbitrarily.
- Among lower-only sources, the depth-one guards lie in \(A\). There is at most one distinct depth-two guard, from row \(19\), and at most six distinct depth-three guards, from the actual order-\(27,54\) inventory. There is no raw rigid source of those shallow orders.

Put \(W=\mathbb Z_3\setminus A\), and let \(k\) be the number of lower-only sources. Their union covers at most
\[
u(k)=\frac19+\frac{\min(6,k-1)}{27}+\frac{\max(0,k-7)}{81}
\]
of \(W\) for \(k\ge1\), with \(u(0)=0\). In each of the four nonspecial 5-branches, either there are at least five deeper sources, or any full fibre there needs a live first-level source. Each such first-level source covers at most \(1/9\) of \(W\). Including the special branch, the total source count is therefore at least
\[
k+1+4\min\!\left(5,\left\lceil 9(2/3-u(k))\right\rceil\right).
\]

With at most twenty sources, a genuine rank-\(5\) step needs at least five top sources, so \(k\le15\). The only case where the bound is at most twenty is \(k=7\), with exactly three sources in each nonspecial branch. Those three must all be first-level sources whose guards lie in \(W\), since they must cover at least \(1/3\) of \(W\). Equality also forces all seven lower-only sources to contribute in \(W\). This leaves \(A\) uncovered. Hence at least 21 sources are necessary.

### Attempts to break the lemma

A nine-leaf mixed witness works when all its guards are \(0\bmod3\). Changing just one leaf’s guard to \(1\bmod3\) destroys coverage while preserving the entire 5-adic projection. The replay also gives a complete 21-source **abstract** configuration for the strip and measure constraints used above. It is a test of those constraints, not an arithmetic certificate.

The deeper-leaf exception is real at the helper level. Row \(251\) is ordinary and has exact base-\(5\) order \(25\). On the represented target below, at \(c=91\), its valuation-one event is \(d\equiv0\pmod{25}\), \(d\not\equiv0\pmod{251}\), independent of the ternary coordinate. So extending the first-level strip rule to depth two would be false.

Independent inventory and fibre replay:

```python
from fractions import Fraction as F
from math import ceil

# Each tuple is one source: ternary residue/depth, 5-adic residue/depth.
def full(rows):
    return {x for x in range(3**max(e for _,e,_,_ in rows))
            if all(any((x-a) % 3**e == (y-j) % 5**f == 0
                       for a,e,j,f in rows)
                   for y in range(5**max(f for _,_,_,f in rows)))}

mixed = [(0,1,j,1) for j in range(4)] + [(0,1,4+5*j,2) for j in range(5)]
assert full(mixed) == {0}
assert full(mixed[:-1] + [(1,1,24,2)]) == set()

L = [(0,1,0,0), (1,2,0,0)]
L += [(a+9*j,3,0,0) for a in (4,7) for j in range(3)]
T = [(0,0,0,1)] + [(a,2,j,1) for a in (2,5,8) for j in range(1,5)]
assert len(L+T) == 21 and full(L+T) == set(range(27))
assert full(L[1:]+T) == {x for x in range(27) if x % 3}

def bound(k):
    u = F(0) if k == 0 else F(1,9)+F(min(6,k-1),27)+F(max(0,k-7),81)
    return k+1+4*min(5, ceil(9*(F(2,3)-u)))
assert [k for k in range(16) if bound(k) <= 20] == [7]

p = 251
n = 4 + 800367031622345800**2 + 632558068701596649**2
assert pow(5,25,p) == 1 and pow(5,5,p) != 1 and pow(5,25,p*p) != 1
assert (n-pow(3,91,p*p)-1) % (p*p) == 0
assert (n-pow(3,91,p*p)-pow(5,50,p*p)) % (p*p) == 167*p
from math import prod,isqrt
V={1:[2,2],2:[2,3],3:[31],6:[3,7],9:[19,829],18:[3,5167],27:[109,271,4159,31051],54:[3,163,487,16018507],5:[11,71],10:[521],15:[181,1741],30:[61,7621]}
def phi5(d):
    return (5**d-1)//prod(phi5(e) for e in range(1,d) if d%e==0)
for d,fac in V.items():
    assert phi5(d)==prod(fac)
    assert all(all(p%i for i in range(2,isqrt(p)+1)) for p in fac)
    if d>2: assert len(fac)==len(set(fac))
def inert(d):
    return {p for p in V[d] if p%4==3 and pow(5,d,p)==1 and
            all(pow(5,e,p)!=1 for e in range(1,d) if d%e==0)}
assert inert(3)|inert(6)=={7,31}
assert inert(9)|inert(18)=={19,5167}
assert inert(27)|inert(54)=={163,271,487,4159,31051,16018507}
assert inert(5)|inert(10)=={11,71} and not (inert(15)|inert(30))
print("OK")
```

This is a rank-five exclusion for the selected muted slice when projecting every higher coordinate by single-source contractions. It does not say that the first nonlinear coordinate has to be rank five. For any fixed ternary coordinate missed by the lower-only seeds, all five first branches must be covered. Inside a nonspecial branch with fewer than five deeper sources, those deeper cylinders cannot cover even one fibre across that branch without some active first-level source, since each deeper one fixes the next digit. Hence the depth-one measure estimate applies on the entire uncovered ternary set there. At equality with 20 sources, all three first-level cylinders per nonspecial branch must individually attain the full measure (1/9) on the complement of the fixed first ternary branch. They therefore cannot cover any part of that branch. This keeps the measured guards attached to every source, even at mixed depths.
