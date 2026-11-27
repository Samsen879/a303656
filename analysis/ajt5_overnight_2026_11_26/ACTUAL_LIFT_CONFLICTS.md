# Exact lift optimization and a minimal three-row greedy failure

This is a finite ordinary-window result. It strengthens the algorithmic side of [CHEAP_LIFT_SET_ORDER_DELETION.md](CHEAP_LIFT_SET_ORDER_DELETION.md); a finite panel cannot generally certify a full sum of two squares.

## Exact selection on a finite panel

Fix a finite panel of inert primes, positive steps on the two exponent axes, lower endpoints, and optionally upper endpoints. Keep only positive residuals \(R=n-3^c-5^d\). For each panel prime \(p\), allow valuation zero at multiplicative cost 1 or valuation exactly two at cost \(p\), and exclude all other valuations. Thus a feasible point costs the product of its lifted primes.

The row factor depends only on the two axis residues modulo its actual multiplicative orders modulo \(p^3\), provided the base is a unit. A nonunit power can instead be evaluated directly on the finitely many preperiod exponents, then retained as a constant after stabilization. On each pair of unit-phase residue classes the componentwise first representatives in the specified intervals minimize the sum of the powers. Testing these representatives retains exactly the classes with a positive residual. A finite factor solver can minimize this product by eliminating one phase coordinate at a time: multiply all factors containing that coordinate on the same assignment before minimizing over the coordinate. Treat excluded assignments as absent, and record minimizing choices for reconstruction. The positivity factor must participate in the same elimination.

There is also a conflict-based exact method, independent of whether the oracle uses phase elimination or direct enumeration. The oracle checks feasibility with a specified set of rows forced to be units, retaining ordinary-height and row-admissibility constraints on every query. First check unconstrained panel feasibility. Whenever forcing a set of rows to be units fails, successively remove dispensable rows to obtain an inclusion-minimal conflict. Every feasible lift set hits every reported conflict. Propose a minimum-product hitting set of the conflicts already found, then verify by forcing its complement to be units. Each failed query discovers a conflict disjoint from the proposal. On the first success the actual lift set is contained in the proposal, so its cost is at most the hitting-set lower bound, and hence equal to the true optimum. This is finite termination, not a polynomial-time claim.

## Actual three-row obstruction to greedy selection

Take \(n=179997339\), start \((14,10)\), steps \((2,2)\), and panel \(\{7,11,19\}\). The positive-residual window consists of precisely the following points:

| \((c,d)\) | Residual | Square decomposition | Lifted primes |
| --- | ---: | --- | --- |
| \((14,10)\) | 165448745 | \(308^2+12859^2\) | \(7,11\) |
| \((16,10)\) | 127184993 | \(817^2+11248^2\) | \(19\) |

The residuals factor as \(5\cdot7^2\cdot11^2\cdot5581\) and \(13\cdot19^2\cdot41\cdot661\). Thus both are actual square sums, and all other inert primes are units at both points. The minimal unit conflicts are exactly \(\{7,19\}\) and \(\{11,19\}\). Buying the cheapest member of each newly uncovered conflict buys 7 and 11 in either order; neither can be removed afterward. The exact optimum buys 19, at cost \(19<77\). Three rows are minimal for this particular rule: on a nonempty feasible panel with at most two rows the conflicts are singleton requirements, or a single two-row conflict for which its cheapest member is optimal.

For every even \(D\ge10\), set \(n=5^D+170231714\) and start at \((14,D)\) with the same steps. The two points remain the entire window: \(3^{14}<3^{16}<170231714<3^{18}\) and \(5^{D+2}-5^D\ge234375000>170231714\). The residuals are unchanged. The obstruction therefore holds at unbounded actual targets with no extra positive points in these forward windows.

## Minimal replay

```python
from itertools import combinations
from math import isqrt, prod

C = 170231714
assert 3**14 < 3**16 < C < 3**18
assert 24*5**10 > C
assert 5**10 + C == 179997339
r1, r2 = C-3**14, C-3**16
assert (r1, r2) == (308**2+12859**2, 817**2+11248**2)
factors = ({5:1, 7:2, 11:2, 5581:1},
           {13:1, 19:2, 41:1, 661:1})
for r, ff in zip((r1,r2), factors):
    assert r == prod(p**e for p,e in ff.items())
    assert all(all(p % d for d in range(2,isqrt(p)+1)) for p in ff)
P = (7,11,19)
H = [{p for p in P if r % p**2 == 0} for r in (r1,r2)]
assert H == [{7,11},{19}]
bad = [set(K) for j in range(4) for K in combinations(P,j)
       if all(set(K) & L for L in H)]
minimal = [K for K in bad if not any(J < K for J in bad)]
assert {frozenset(K) for K in minimal} == {frozenset({7,19}),
                                           frozenset({11,19})}
assert prod({min(K) for K in minimal}) == 77
assert min(map(prod,H)) == 19
```
