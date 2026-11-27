# Uniform escape at the first large nonlinear rank with a tight source budget

**On the selected muted slice, a first essential nonlinear projection at any odd prime \(p\ge13\) needs more than \(p+1\) surviving sources.** Rows \(3\) and \(31\) suffice for this exclusion. No additional heads need to be muted. At \(13\) and \(19\) there is a literal lower product box. For general \(p\), the same escape argument works by projecting at most three guards through the lower rows. [Prior guarded projection and source conventions](https://github.com/Samsen879/a303656/commit/d4491ad99d97b61ea18ce0851a79bb76b206fdae)

### The unavoidable guards

After the higher linear projections, each source still has one label and one product guard. An essential \(p\)-fibre needs at least \(p\) top sources. With fewer, the only possible full fibre uses an active dynamic row and a centered first-level source. Thus the \(p+1\) budget leaves at most one lower-only guard \(L\).

Let \(H_p\) be the pivot row’s actual order guard, or the empty set for a split or inactive row. Outside \(H_p\), a full fibre needs a first-level source in every branch. A deeper irredundant \(p\)-ary frontier costs at least \(2p-1>p+1\). If flat witnesses are possible, at least \(p-1\) first branches have singleton source groups. Every flat alternative must use each such singleton’s live lower guard.

Some singleton has a **proper** lower guard \(G\). An unrestricted first-level source must come from a raw order \(p,2p\), or from a least helper of one of those orders. Each such prime can supply only one first digit. There are fewer than \(p-1\) candidate primes: they divide \(\Phi_p(5)\Phi_{2p}(5)=(5^{2p}-1)/24\), and each is at least \(2p+1\). For \(p\ge13\), the product of \(p-1\) such primes would already exceed that cyclotomic product.

The entire projection is therefore contained in \(L\cup G\cup H_p\). If flat witnesses are impossible, omit \(G\).

### Exact lower-box test at \(13\) and \(19\)

On a product box \(B\) where the lower rows and the pivot are inactive, a lower-only guard can close the hole only by containing all of \(B\), or by complementing the flat guard along **one and the same coordinate**. This is exact when \(L\) exists: only \(p\) top sources remain, so the flat guard is a single intersection of product guards. If the two proper guards restrict different coordinates, those coordinates can be chosen independently to miss both.

- **Rank \(13\).** The pivot is split and has no norm veto. At \(n=89,c=1\), even \(d\), rows \(7,11\) exclude \(d\equiv1\pmod3\) and \(d\equiv4\pmod5\), respectively. On the remaining product box, a proper singleton has relative mass at most \(1/2\).
- **Rank \(19\).** The pivot is ordinary with exact order \(9\). At \(n=77,c=1\), even \(d\), row \(7\) excludes \(d\equiv2\pmod3\), while row \(19\) has the live guard \(d\equiv4\pmod9\). Cutting both leaves the ternary residues \(\{0,1,3,6,7\}\bmod9\). A proper singleton has relative mass at most \(3/5\).

At either rank, the only complementary pair that could close the box consists of two pure first ternary guards. Each retained first ternary branch still has at least two second-level children, and every other coordinate retains more than two first branches. But \(L\) cannot be a pure first ternary guard: raw orders \(3,6\) give no rigid source, and their only helpers are \(7,31\). Row \(7\) is still below the pivot, and \(31\) is muted. In mass terms, \(\mu_B(L)\le1/4\), so even the rank-\(19\) sum is at most \(17/20\).

### Why the exclusion is uniform

For larger \(p\), keep all the lower dynamic rows and project the at-most-three guards \(L,G,H_p\) through them. At every odd rank above \(3\), three is below the branching number. Exact projection therefore uses only single-source centered contractions, with at most one descendant per guard.

A descendant that becomes a first ternary guard **through a contraction** must use \(7\) or \(31\) as its least helper. With \(31\) muted, all these descendants share the one first branch from \(7\). Neither \(L\) nor \(H_p\) can enter that step as a pure first ternary guard. Only \(G\) can supply a different first branch directly. No guard becomes constant, because a contraction adds the helper’s nonempty odd order guard. Thus there are at most three proper ternary guards and at most two distinct first branches. Their union has measure at most \(7/9\). Since row \(3\) is inactive, an uncovered ternary phase lifts to a full escape.

### Runnable replay

```python
from math import isqrt, prod
from fractions import Fraction as F

for p, plus, minus in (
    (13, (305175781,), (5227, 38923)),
    (19, (191, 6271, 3981071), (761, 19609, 213029)),
):
    assert prod(plus) == (5**p-1)//4
    assert prod(minus) == (5**p+1)//6
    for o, factors in ((p, plus), (2*p, minus)):
        for q in factors:
            assert all(q % j for j in range(2, isqrt(q)+1))
            assert pow(5,o,q) == 1 and pow(5,o,q*q) != 1
            assert all(pow(5,o//r,q) != 1 for r in (2,p) if o%r == 0)
assert 27*24 > 25*25  # Uniform pure-order product bound.

def guard(n,p,o):
    odd = o//(2 if o%2 == 0 else 1)
    return {d%odd for d in range(0,2*o,2) if (n-3-pow(5,d,p))%p == 0}

assert 89 == 3+1+2**2+9**2 and 77 == 3+1+3**2+8**2
assert pow(5,2,13) == 12 and pow(5,4,13) == 1
assert (guard(89,7,6), guard(89,11,5)) == ({1}, {4})
assert (guard(77,7,6), guard(77,11,5), guard(77,19,9)) == ({2}, set(), {4})
assert pow(5,9,19**2) == 115  # Order 9, ordinary lift.
assert (74-pow(5,4,19**3)) % 19**3 == 332*19
assert (74-pow(5,382,19**3)) % 19**3 == 5*19**2

U = {x for x in range(9) if x%3 != 2 and x != 4}
assert U == {0,1,3,6,7}
G = {x for x in U if x%3 == 0}
assert G | {x for x in U if x%3 == 1} == U  # Forbidden pure-first L.
assert U - (G | {1}) == {7}               # A deeper L leaves a hole.
assert F(3,5)+F(1,4) == F(17,20)
assert all({(x*x+y*y)%169 for x in range(169) for y in range(169)} == set(range(169)) for _ in [0])
print("OK")
```

The argument deliberately overcharges the whole pivot guard, so its projection preserves every possible actual pivot failure. Lower rows are projected exactly against this larger cover. At ranks above 3, at most three carried guards are fewer than the rank, so the inherited single-source contraction rule applies. The uniform result does not itself raise the overall thirteen-prime necessary bound: for larger total budgets one of the smaller ranks can still be the first nonlinear projection.
