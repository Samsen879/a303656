# A weighted joint primary block avoids six inert roots

The [simultaneous root-avoidance lemma](SINGLE_WITNESS_FOUR_TARGET_AVOIDANCE.md) extends to six targets for the bases 3 and 5. For a freely moving set of primary coordinates \(S\), put
\[
 D_{t,a}(S)=\prod_{r\in S}r^{v_r(\operatorname{ord}_t(a))}
 \quad\text{and}\quad D_t(S)=\max_a D_{t,a}(S)
\]
over unit axes. A target \(t\) removes at most \(1/D_t(S)\) of the common grid: with the other axis fixed, the stronger axis runs uniformly through its coset, so at most one residue hits the prescribed root. The losses on the two axes need not multiply. If the sum of weights for all targets affected by \(S\) is less than one, a simultaneous choice exists.

For six targets and largest primary source \(r\ge7\), proceed by descending induction as before: temporarily withdraw the targets reading \(r\); when \(r\) is inert, add it as a unit-residual substitute. At most six targets remain and the new largest source is smaller. The \(r\)-variables can then move freely, since \(r\) itself passes as a unit and earlier tests do not read the variables. The withdrawn targets have total loss at most \(6/r<1\). As before repair ordinary primes above \(r\) by their own digits in increasing order.

Once the largest source is at most 5, choose the parities to pass 2 and avoid the root at 3; the prime 5 is split. This frees the 3- and 5-primary coordinates together, with no other odd inert test at or below 5. Give each remaining inert target \(t>3\) the weight \(1/D_t(\{3,5\})\). Here \(D_t\) is the maximum odd part of either base's order because \(v_2(t-1)=1\) and there are no larger sources. The only possible \(D_t=3\) is at 7 (from \(t\mid3^6-1\)), and the only possible \(D_t=5\) is at 11: factor \(3^{10}-1\) and \(5^{10}-1\) to reduce to 11 and 71, then note \(3^{10}\ne1\bmod71\). The case \(D_t=1\) would require \(t\mid8\). Consequently the weight is at most
\[
 1/3+1/5+4/9=44/45<1.
\]
If all sources are at most 3, \(D_t=5\) is absent, with bound \(1/3+5/9<1\). The same ordinary repairs and finite cylinders finish the proof. This avoids the need to classify five-cover equality cases at a single prime.

Hence for each of the first six common Wieferich inert primes, include it and all earlier common Wieferich inert primes as targets and impose all ordinary earlier inert tests. For every terminal residue, the lemma finds a surviving phase that avoids it. In particular no first blocker occurs at any of these first six primes, if they exist. This does not exclude a seventh or later terminal and is not a density-one theorem.

The replay uses actual 3,5 shifts and six ordinary target primes, with exact local valuations. In particular a double-read target removes three cells of a 25-cell grid, not the single cell predicted by multiplying the two reciprocal orders.

~~~python
from itertools import product
from math import isqrt

P = (11, 31, 271, 811, 21871, 196831)
O = ((5,5), (30,3), (30,27), (810,405),
     (810,10935), (196830,98415))
n = 541876231729143866152902799267321221
C, E = 98415, 39366
G = list(product(range(5), repeat=2))

assert 3**6-1 == 8*7*13 and 3**10-1 == 8*11**2*61
assert 5**10-1 == 8*3*11*71*521 and pow(3,10,71) != 1
assert [n % p**2 for p in P] == [2,16,262,0,0,0]
for p, pair in zip(P, O):
    assert p % 4 == 3 and all(p % j for j in range(2,isqrt(p)+1))
    assert any(pow(a,p-1,p*p) != 1 for a in (3,5))
    assert any(o%5 == 0 for o in pair) and all(o%25 for o in pair)
    for a,o in zip((3,5),pair):
        assert pow(a,o,p) == 1
        assert all(pow(a,o//r,p) != 1 for r in (2,3,5) if o%r == 0)

def shift(c,x,y,m):
    return (pow(3,c+E*x,m) + pow(5,C+E*y,m)) % m

def bad(c,p):
    return {(x,y) for x,y in G if (n-shift(c,x,y,p)) % p == 0}

B = [bad(C,p) for p in P]
assert [len(b) for b in B] == [3,5,5,5,5,5]
assert len(set.union(*B)) == 15
assert all((n-shift(C,x,y,p*p)) % (p*p)
           for p,b in zip(P,B) for x,y in b)
assert [len(bad(C+10,p)) for p in P] == [3,0,0,0,0,0]
assert all((n-shift(c,x,y,4)) % 4 == 1 and (n-shift(c,x,y,3)) % 3
           for c in (C,C+10) for x,y in G)

~~~
