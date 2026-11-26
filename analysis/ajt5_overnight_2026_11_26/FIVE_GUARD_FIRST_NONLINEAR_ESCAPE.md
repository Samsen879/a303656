# Five-guard escape at first nonlinear rank with up to p+3 sources

**The projection still rules out a complete cover at \(p+2\) and \(p+3\) sources.** On the selected muted slice, for every odd prime \(p\ge11\), a first essential nonlinear projection at \(p\) with at most \(p+3\) surviving rigid sources leaves an exponent phase uncovered. The proof needs rows 3 and 31 inactive and allows the other lower dynamic rows to remain live. At \(p=11\), it handles 13 or 14 sources while retaining row 11’s actual order-five guard. [Previous projection and source conventions](https://github.com/Samsen879/a303656/commit/a2a3e97e9924f9761a17bec4806b29c1bb79c026)

### Why five lower guards suffice

Fix the target \(n\), the anchor \(c\), and the parity of \(d\). A rigid source carries one product of prime-power residue classes. A dynamic row at \(r\) has a fixed lower-order guard \(H_r\), given by the actual base-5 logarithm at that same target and parity. Inside \(H_r\), its rejected \(r\)-adic shells have odd valuation. Its center is safe. With fewer than \(r\) proper \(r\)-prefixes, a full fibre therefore needs an active first shell and a centered first-level prefix. If the first shell is safe, all \(r\) first branches need a prefix. If it is rejected and the centered first-level prefix is absent, all \(r\) children inside the center branch need a prefix, since the next shell is safe. This also gives the single-source contraction rule for the higher linear history. [Guarded rank-11 projection](https://github.com/Samsen879/a303656/commit/d4491ad99d97b61ea18ce0851a79bb76b206fdae)

At the first essential pivot \(p\), at least \(p\) sources read \(p\). This leaves at most three lower-only guards \(L_1,L_2,L_3\). Charge the entire actual pivot guard \(H_p\) to the projected cover. Outside \(H_p\), a full fibre must use all \(p\) first-level branches. A deeper complete prefix tree costs at least \(2p-1>p+3\) leaves. If flat alternatives exist, at least \(p-3\) first branches have just one source each. Every flat alternative needs every one of those singleton sources.

At least one singleton has a **proper** lower guard \(G\). An unrestricted first-level \(p\)-source must come directly from order \(p\) or \(2p\), or inherit that order from its numerically least helper. Any other odd factor of that helper’s order could disappear only through a still smaller helper, and intersections preserve prefix depth. Each candidate prime supplies just one first digit. These inert primes divide \((5^{2p}-1)/24\) and have the form \(1+2pj\) for odd \(j\). The product of \(p-3\) distinct candidates would be at least
\[
(2p+1)(6p+1)^{p-4} > 25^p/24.
\]
The inequality starts at \(p=11\) and follows uniformly by using \(23\) and \(67\) as lower bounds for the two bases. At 11 the exact factorization gives just three inert candidates, \(23,67,12207031\). Thus \(L_1\cup L_2\cup L_3\cup G\cup H_p\) contains **every** projected failure. If flat alternatives are absent, omit \(G\).

### The lower ranks

- **Ranks \(r\ge7\).** Keep the actual lower dynamic rows. Five guards are below the branching number, so each projection uses single-source contractions and retains at most one descendant per guard. A contraction adds the helper’s actual lower-order guard. For an inert helper \(r>3\) this guard has an odd factor, since order 1 or 2 would imply \(r\mid24\).
- **Rank 5.** The split prime has no dynamic veto. A new covering term needs all five guards in distinct first-level branches, and its lower guard is their intersection. For that intersection to cover the whole ternary axis, all five must be pure first-level 5-guards. Actual orders \(5,10\) supply only the fixed positions of rows 11 and 71. This applies to a direct actual guard and to a guard inherited from a least helper. Only an unchanged \(G\) can supply another position. Hence a nonlinear term at 5, if present, is a single proper ternary guard, with no lower-only guard left over.
- **Rank 3.** If rank 5 produces no new term, at most five proper ternary prefixes remain. A complete ternary frontier of that size is either three first-level leaves or two first-level leaves and all three children of the remaining branch. Orders \(3,6\) supply only rows 7 and 31. With 31 muted, the first-level positions can only be row 7’s fixed position and an unchanged \(G\). If both occur, \(G\) has already been used. Outside row 7’s branch, a second-level position must then come from row 19 or 5167, the actual order-\(9,18\) heads. A direct pivot guard from either row gives the **same** position as a guard inherited from that row. Two positions cannot fill the three children. Even with 5167 live, the ternary union has mass at most \(25/27\).

An uncovered ternary phase lifts through the exact lower projections and then through the pivot overcover. This settles the first-pivot cases \(p\ge11\) under the stated budget. An increased **global** source bound would still require checking the smaller first pivots and the all-linear case.

### Inline replay

The replay checks the named orders and constructs one represented target with rows 7, 11 and 19 all live at the **same** \(n,c=1,d\equiv0\pmod2\). The final two checks are synthetic controls for the rank-five intersection and the missing third ternary child. The runnable replay below checks these controls.

```python
from math import isqrt, prod

for o, value, fs, heads in (
    (3, 31, (31,), {31}), (6, 21, (3, 7), {7}),
    (5, 781, (11, 71), {11, 71}), (10, 521, (521,), set()),
    (9, 15751, (19, 829), {19}), (18, 15501, (3, 5167), {5167}),
    (11, (5**11-1)//4, (12207031,), {12207031}),
    (22, (5**11+1)//6, (23, 67, 5281), {23, 67}),
):
    assert prod(fs) == value and len(set(fs)) == len(fs)
    assert all(all(q % j for j in range(2, isqrt(q)+1)) for q in fs)
    actual = {q for q in fs if q % 4 == 3 and pow(5, o, q) == 1
              and all(pow(5, j, q) != 1 for j in range(1, o))}
    assert actual == heads and all(pow(5, o, q*q) != 1 for q in heads)

assert 24*23*67**7 > 25**11 and 67 > 25
P = 8*3*7*19*31*71*5167*19531
u, v = (a + P*((2-a)*pow(P, -1, 11) % 11) for a in (3, 8))
n = 3 + 1 + u*u + v*v

def guard(q, o):
    odd = o // (2 if o % 2 == 0 else 1)
    return {d % odd for d in range(0, 2*o, 2) if (n-3-pow(5,d,q)) % q == 0}

assert n % 4 == 1
assert (guard(7,6), guard(11,5), guard(19,9)) == ({2}, {4}, {4})
assert all(not guard(q,o) for q,o in ((3,2),(31,3),(71,5),(5167,18),(19531,7)))
assert {x for x in range(3) if all(y != 4 or x == 1 for y in range(5))} == {1}
def missing(ps):
    return {x for x in range(9) if all(x % m != a for a,m in ps)}
ps = [(0,3), (1,3), (2,9), (5,9)]
assert missing(ps) == {8} and missing(ps + [(8,9)]) == set()
print("PASS", n)
from fractions import Fraction as F
assert 2*F(1,3)+2*F(1,9)+F(1,27)==F(25,27)
assert F(1,3)+4*F(1,9)<F(25,27)

```

The pivot overcover counts all alternatives, using a compulsory proper singleton guard for the flat alternatives outside the pivot guard, not a single chosen witness. After reduction to the ternary axis, in the two-distinct-first-branches case only two second-level head positions can still contribute outside both first branches, and the remaining allowance is at most one third-level guard. With at most one first branch, the coarser bound is 1/3+4/9. No new unconditional common-prime count is claimed without analysis of the smaller first pivots and all-linear possibilities.
