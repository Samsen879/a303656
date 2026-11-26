# Five simultaneous targets: the critical \(5\)-primary grid

The [four-target avoidance induction](SINGLE_WITNESS_FOUR_TARGET_AVOIDANCE.md) extends to five inert root targets for the actual bases 3 and 5. Thus any first finite blocker for the growing single-witness box must occur at the sixth or a later common Wieferich inert prime, should such primes exist. This is not yet density one.

The ordinary-prime repairs and the descending induction remain unchanged except when the largest source prime is 5 and five targets each read its first digit but no higher digit. At \(r\ge7\) the bound \(5/r<1\) suffices. At \(r=3\) at most the prime 7 can have maximal read depth one (it must divide \(3^6-1\)), so the sum is at most \(1/3+4/9<1\). At \(r=5\) fewer than five affected targets, or one target reading deeper, also give sum less than one.

## What could cover the critical grid?

Use the two absolute 5-primary digits \(x,y\in\mathbb F_5\) after fixing all other primary coordinates. A single-reading target deletes at most one whole row or column. A double-reading target can delete at most five cells in a partial matching, given by \(a g^x+b h^y=n_t\bmod t\) with \(g,h\) generating the order-five group. If it deletes five cells, both axis values run over their entire cosets. Summing gives \(5n_t=0\bmod t\), hence \(n_t=0\bmod t\) since \(t\ne5\), and the two cosets are negatives of each other. The absolute-coordinate quantities \(a,b\) have orders prime to 5; so does \(a/(-b)\). But this quotient lies in the order-five subgroup, hence \(a=-b\) and the matching contains \((0,0)\). Every full matching also intersects every whole row and column. Two different types of whole lines intersect. Covering all 25 cells with five sets of size at most five would require disjoint full sets, and is thus only possible with five parallel single-reading lines.

## Varying a lower digit rules out permanent coverage

In that last case all targets read the 5-primary digit and were temporarily removed, so no smaller target remains from the old problem. Choose the parity of \(d\) to get a unit at 3, and satisfy the condition at 2 as in the previous induction; the old ordinary prime at 3, if present, already passes. Both 3-primary exponent coordinates now remain free. At least one reading axis has a target order divisible by 3: if not, all five reading orders divide 10, whereas \(3^{10}-1=2^3\cdot11^2\cdot61\) and \(5^{10}-1=2^3\cdot3\cdot11\cdot71\cdot521\) give at most two applicable inert primes on either axis. Changing that reading axis's 3-primary coordinate moves the corresponding order-five coset to a different coset; the required root lies in at most one. The other axis is unchanged. This erases the line without hurting 2 or 3. With fewer than 25 covered cells, choose a survivor. Repair larger ordinary primes in ascending order; their own primary coordinates are not read by any target. As before all these conditions admit a positive-measure cylinder.

The true local replay below has five saturated bad sets at one lower branch but only 15 cells in their union. At the same \(n\) a change of lower branch removes all five bad sets. The primes here are ordinary targets used to check the combinatorics; this does not exhibit a common Wieferich prime or a true blocker.

~~~python
from itertools import product
from math import isqrt

P = (31, 271, 811, 21871, 196831)
orders = ((30,3), (30,27), (810,405),
          (810,10935), (196830,98415))
n = 5076183076267154711438992138029717
C, step = 98415, 39366
grid = list(product(range(5), repeat=2))

assert n % 4 == 1 and n % 3 == 0
assert [n % p**2 for p in P] == [16,262,0,0,0]
for p, pair in zip(P, orders):
    assert p % 4 == 3 and all(p % j for j in range(2,isqrt(p)+1))
    assert any(pow(a,p-1,p*p) != 1 for a in (3,5))
    for a,o in zip((3,5),pair):
        assert pow(a,o,p) == 1
        assert all(pow(a,o//r,p) != 1 for r in (2,3,5) if o%r == 0)

def shift(c,x,y,m):
    return (pow(3,c+step*x,m) + pow(5,C+step*y,m)) % m

def bad(c,p):
    return {(x,y) for x,y in grid if (n-shift(c,x,y,p)) % p == 0}

B = [bad(C,p) for p in P]
assert [len(b) for b in B] == [5]*5
assert len(set.union(*B)) == 15 and all((0,0) in b for b in B[2:])
assert all((n-shift(C,x,y,p*p)) % (p*p) != 0
           for p,b in zip(P,B) for x,y in b)
assert all(not bad(C+10,p) for p in P)
assert all((n-shift(c,x,y,4)) % 4 == 1 and (n-shift(c,x,y,3)) % 3
           for c in (C,C+10) for x,y in grid)

~~~
