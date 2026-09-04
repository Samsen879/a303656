# Adversarial counterexamples

Machine-readable records and hashes are in `results/counterexamples.json`.

## 1. Budget one but fiber not covered

Take `l=3`, `beta=1`, dynamic center zero, and accepted shell `S_0={1,2}`.  Add one rigid depth-one digit at residue `1`, not at the center.

```text
dynamic mass = 2/3,
rigid mass = 1/3,
total = 1.
```

The rigid event overlaps the dynamic shell and cell `0` is uncovered.  Hence rational equality is not sufficient for actual coverage.

The same failure persists above the saturation threshold.  At
`l=3`, `beta=m=3`, take `J={0,2}` and put the depth-one rigid cylinder at
digit `1` rather than the center.  The mass is `29/27>1`, but center-side
cells remain uncovered.  Thus strict excess is not sufficient either.

## 2. Exact cover without a beta-one pair

At `l=3`, `beta=1`, take all three rigid depth-one digits and no dynamic event.  This is an exact row-minimal partition of the fiber, with budget one, but contains no dynamic beta-one pair.

This is the smallest exact-cover counterexample to the claim that every covered fiber must contain a beta-one pair.

A dynamic variant shows why the arbitrary-depth theorem must allow a proper
refinement of the unresolved center.  At `l=3`, `beta=2`, take the outer
dynamic shell and the three depth-two center children `C(2,0)`, `C(2,3)`, and
`C(2,6)`.  They form a row-minimal exact partition with no depth-one centered
rigid row.

Repeated rigid masses also separate budget from union coverage.  Three
depth-one rigid rows at residues `0,0,1` have total mass one, but cover only
digits zero and one; the duplicate row is redundant and digit two is a hole.

## 3. Row-minimal overlap tail

Take `l=3`, `beta=m=3`, `s_l` odd, and

```text
J={0,2}.
```

The dynamic row covers `S_0` and `S_2`; one centered depth-one rigid cylinder covers the whole center branch.

```text
total budget = 29/27,
uncovered cells = 0,
multiplicity-one cells = 25,
multiplicity-two cells = 2.
```

Deleting either row creates a hole, so the cover is row-minimal.  The shell `S_2` is redundant only at valuation-atom level, not at row level.  Therefore row deletion alone cannot reduce every minimal cover to an exact partition.

## 4. Coverage only for one lower assignment

A rigid row may be one cylinder for one fixed lower-coordinate assignment and empty for another.  With a beta-one dynamic shell, assignment A can align the rigid cylinder with the center and cover the fiber, while assignment B leaves the center uncovered.

Thus a fiber template is conditional on the lower assignment reached by coordinate induction.  It is not a global statement about all lower assignments.

## 5. Abstract template not arithmetically realizable

An abstract beta-one template with a dynamic row at coordinate `l=5` is valid as a cylinder picture but impossible in the admitted arithmetic class, which requires dynamic row primes `p==3 mod 4`, `p!=5`.

There is also a rigid-label boundary using an admitted-looking order factor:
`ord_7(5)=6` is divisible by `3`, but `s_7=1`, so there is no positive odd
valuation `h<s_7`.  Hence `q=7` cannot supply a depth-one rigid fatal cylinder
at coordinate `3`.

## 6. Anchorwise saturation not common-residue realizability

Using the actual pair `(l,q)=(67,20771)` and the fiber `d=3410t`, each anchor separately has a class-zero beta-one exact partition:

```text
c=0: r_67=2, r_20771=q+2;
c=1: r_67=4, r_20771=q+4.
```

In each case the dynamic row covers 66 cells and the rigid row covers the unique center.  No single common-residue system realizes this prescribed pair: both the dynamic residues modulo 67 and the rigid residues modulo `q` disagree.

This demonstrates that separately realizable prescribed anchor templates do not tensor into one common system.  It does not exclude different class choices or a larger system.

Conversely, common-residue compatibility is not universally destructive.  A
single system with residues `r_67=2` and `r_20771=13471` gives exact `66+1`
partitions at both anchors, on lower assignments `2728 mod 3410` and
`1639 mod 3410`, respectively.  This is pointwise positive evidence only:
the assignments differ, so it proves neither uniform lower-coordinate
saturation nor a complete certificate.

## 7. K2 boundary must remain separate

The exact existing case

```text
K_2=2,
U=5,
2 does not divide U,
old coordinate-only hypothesis passes,
direct safe count=0
```

is a constant two-adic obstruction.  It is not an odd-coordinate event and is rejected before the odd inverse classification begins.

`tools/arithmetic_realizability_checker.py` independently replays all 55 exponent classes and records zero two-adically safe cells, zero direct safe cells, and `2 not dividing U`.

## 8. Finite-template claim

A depth-independent finite literal template list is false:

- rigid-only complete prefix frontiers have unbounded refinement depth;
- one dynamic row can contain arbitrarily deep accepted overlap tails while the cover remains two-row and row-minimal.

The corrected result is a parameterized prefix-frontier classification with a finite effective catalog for each fixed `beta`.
