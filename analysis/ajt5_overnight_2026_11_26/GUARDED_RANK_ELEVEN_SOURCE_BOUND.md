# Guarded rank-eleven exclusion and a thirteen-common-prime necessary condition

**Rank \(11\) cannot be the first essential nonlinear projection with eleven or twelve rigid sources on the selected muted slice.** The depth-four audit also closes the all-linear route. Together with the guarded rank-\(5\) and rank-\(7\) exclusions, this raises the necessary count for a finite all-exponent modulus obstruction to **at least thirteen common base-\(3\), base-\(5\) exceptional primes**. The argument supplies a necessary condition for a hypothetical obstruction. [Guarded rank-seven result](https://github.com/Samsen879/a303656/commit/c0d8aee19ff506f97e4e0bf63b2efc6025d4692e)

### Depth-four audit

After muting \(31,5167\), the actual inert ternary heads at depths \(1,2,3,4\) number \(1,1,6,4\). I rechecked the complete cyclotomic products, the Lucas primality certificates for the large factors, the exact orders, and ordinary base-\(5\) lifting. At depth four the orders are \(81,162\), with
\[
\Phi_{81}(5)=4861\cdot11419697846380955982026777206637491,\qquad
\Phi_{162}(5)=3\cdot1783\cdot5023\cdot2066067271380136212224701233463.
\]
The split factor \(4861\) and the imprimitive factor \(3\) contribute no head. All four remaining factors are ordinary. [Published order inventory](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md)

An all-linear ternary cover with at most twelve leaves has at most five internal nodes. At most one child of the root can be a leaf. A deepest path of length \(D\) therefore costs at least \(D+1\) internal nodes, so \(D\le4\). The available fixed guards through that depth have total measure at most \(1/3+1/9+6/27+4/81=58/81\).

### Rank \(11\) with live lower guards

After the higher linear steps, each surviving source retains its label, one \(11\)-prefix, and a fixed product guard on \(3,5,7\). Row \(11\) has exact base-\(5\) order \(5\) and lifting depth one. Its active guard \(H_{11}\) is one first \(5\)-adic branch, or empty.

With at most twelve sources, the exact \(11\)-fibre alternatives are a flat witness of eleven first-level prefixes, a centered first-level simple pair on \(H_{11}\), or a nested witness on \(H_{11}\). The nested witness needs ten second-level side prefixes and a source for the center. The center is supplied at level two, or at level three when valuation \(3\) is detected. Replacing a required prefix by deeper ones costs at least twenty-one sources. Each flat or nested witness intersects its own live lower guards, and the projection takes their union. With twelve sources there are at most two alternatives of either shape. Simple pairs have separate guards and remain inside \(H_{11}\).

Now take the lower product block
\[
U\times V\times\mathbb Z_7,\qquad
U=\mathbb Z_3\setminus H_7,\quad V=\mathbb Z_5\setminus H_{11}.
\]
Here \(H_7\) is row \(7\)’s actual first ternary guard at the fixed parity, or empty. Rows \(7,11\) are both inactive on this block, row \(3\) is muted, and \(5\) is split. Outside \(H_{11}\), the only possible coverage comes from a flat witness or a lower-only source.

An essential rank-\(11\) witness consumes at least eleven sources, leaving at most one lower-only guard \(L\). If flat witnesses exist, at least ten of the first \(11\)-branches have singleton source groups. At most three first branches can have an unrestricted lower guard. Such a source would need raw order \(11\) or \(22\), or a least helper of that order. The squarefree products
\[
\Phi_{11}(5)=12207031,\qquad
\Phi_{22}(5)=23\cdot67\cdot5281
\]
exclude raw rigid sources. The three inert helpers \(12207031,23,67\) each supply one fixed first digit. Thus some singleton has a **proper** lower guard \(G\), required by every flat alternative.

Relative to the block, \(G\) covers at most \(1/2\). The lower-only guard \(L\) covers at most \(1/4\): a pure first ternary guard is impossible because row \(7\) has yet to be eliminated and row \(31\) is muted. Any deeper ternary restriction covers at most \(1/6\), a \(5\)-restriction at most \(1/4\), and a \(7\)-restriction at most \(1/7\). These bounds also cover products of unequal depths. The block therefore has a point outside \(L\cup G\). Without a flat witness, \(L\) alone would have to cover it.

That point has a safe \(11\)-lift, and exact lifting through the higher projections gives a full escape. This rules out completion by any later nonlinear projection.

### Minimal replay

The fixture uses the represented target \(89=3+1+2^2+9^2\). At \(c=1\) and even \(d\), row \(7\) reads \(d\equiv1\bmod3\), while row \(11\) reads \(d\equiv4\bmod5\). The test cylinders are synthetic and retain their lower product guards.

```python
from fractions import Fraction as F
from math import isqrt

assert (5**11-1)//4 == 12207031
assert (5**11+1)//6 == 23*67*5281
for p, o in [(12207031,11), (23,22), (67,22)]:
    assert all(p%j for j in range(2,isqrt(p)+1))
    assert pow(5,o,p) == 1 and pow(5,o,p*p) != 1
    assert all(pow(5,j,p) != 1 for j in range(1,o))
assert F(1,3)+F(1,9)+F(6,27)+F(4,81) == F(58,81)

assert [d for d in range(0,6,2) if (86-pow(5,d,7))%7 == 0] == [4]
assert [d for d in range(0,10,2) if (86-pow(5,d,11))%11 == 0] == [4]
assert pow(5,6584,11**4) == 86

# Each record carries one lower product guard and one 11-prefix.
def check(point, rows, K=4):
    x,y,z = point
    live = {(j,g) for guard,j,g in rows
            if all(v % m == a for v,(a,m) in zip(point,guard))}
    flat = all((j,1) in live for j in range(11))
    nested = (all((j,2) in live for j in range(6,121,11) if j != 50)
              and ((50,2) in live or K >= 4 and (1260,3) in live))
    rule = (0,0) in live or flat or y == 4 and ((6,1) in live or nested)

    def bad(t):
        d = t + 1331*((y-t)%5)
        d += (d%2)*5*1331
        r = (86-pow(5,d,11**K)) % 11**K
        return (r != 0 and r%11 == 0 and (r%121 != 0 or r%1331 == 0)
                or any((t-j)%11**g == 0 for j,g in live))
    assert rule == all(bad(t) for t in range(1331))
    return rule

g = ((0,3),(1,5),(2,7))
flat = [(g,j,1) for j in range(11)]
assert check((0,1,2),flat) and not check((0,1,3),flat)
h = ((2,3),(4,5),(5,7))
nested = [(h,j,2) for j in range(6,121,11) if j != 50] + [(h,1260,3)]
assert check((2,4,5),nested) and not check((2,4,5),nested,3)
assert not check((2,1,5),nested)
from math import gcd,prod
factor = {
  11419697846380955982026777206637491:[2,3,3,3,3,5,614267,159701,143715885159696840787],
  143715885159696840787:[2,3,41,584210915283320491],
  584210915283320491:[2,3,5,11,1770336106919153],
  1770336106919153:[2,2,2,2,126949,871578403],
  2066067271380136212224701233463:[2,3,3,3,3,2029,10562011,158143499,3763131871],
}
def certify(p):
    if p not in factor:
        return p>1 and all(p%d for d in range(2,isqrt(p)+1))
    qs=factor[p]
    assert prod(qs)==p-1 and all(certify(q) for q in set(qs))
    return any(pow(a,p-1,p)==1 and all(gcd(pow(a,(p-1)//q,p)-1,p)==1
                  for q in set(qs)) for a in range(2,1000))
p,q=11419697846380955982026777206637491,2066067271380136212224701233463
assert (5**81-1)//(5**27-1)==4861*p
assert (5**81+1)//(5**27+1)==3*1783*5023*q
assert all(certify(v) for v in (3,4861,p,1783,5023,q,5281))
for v,o in ((p,81),(1783,162),(5023,162),(q,162)):
    assert v%4==3 and pow(5,o,v)==1 and pow(5,o,v*v)!=1
    assert all(pow(5,o//l,v)!=1 for l in (2,3) if o%l==0)
print("OK")

```

All lower-only guards in this linear history are proper by the same least-helper rule: a constant raw guard would require odd order support to be empty, and a minimum helper with empty odd support would have to be the inactive row 3. The relative box measures keep the whole 7-coordinate intact and remove only one first cylinder from each active 3- or 5-guard. Thus the safe point is recovered before any putative later nonlinear projection. The modulus conclusion uses the all-exponent bridge and refers only to a hypothetical finite obstruction, with no new numerical density claim.
