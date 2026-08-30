# Contraction-tree theorem audit

## Final mathematical verdict

```text
TARGETED PARTIAL ADVANCE
```

The literal candidate is ambiguous.  A universal theorem is true for **exact semantic fiber elimination**, but the intended stronger claim—automatic decomposition into beta-one or otherwise admitted row-level contractions—is not justified by completeness.  The correct theorem ladder is given below.

## T1. Exact semantic contraction theorem

Let

```text
X = X_1 x ... x X_m,
|X_i|=n_i,
```

where the coordinates are ordered increasingly by rational prime label.  Let `F` be a finite family of triangular events: every event `E` has a largest coordinate `tau(E)` and is independent of all higher coordinates.

For the maximal coordinate `m`, write

```text
A(y) = “some event of rank <m covers y”,
B(y,z) = “some event of rank m covers (y,z)”.
```

Define the exact saturation predicate

```text
Sat_m(y) iff for every z in X_m, B(y,z).
```

Then, for every lower assignment `y`,

```text
for every z, [A(y) or B(y,z)]
iff
A(y) or Sat_m(y).
```

### Proof

`A(y)` is independent of `z`.  Therefore universal quantification distributes over the disjunction with this constant term:

```text
forall z (A or B_z) = A or forall z B_z.
```

Replacing every rank-`m` event by the lower macro-event `Sat_m` is consequently exact for the full-fiber projection.  Iterating over maximal coordinates proves:

> For every finite triangular event system, the original system covers the whole product if and only if the iterated exact contraction reaches a covered root.

### Quantifier order

```text
for every finite triangular system F,
for every fixed anchor c,
for every exact maximal-coordinate elimination sequence,
the contraction invariant holds;
therefore F is complete at c iff the root is covered.
```

No density estimate enters this theorem.

### Effective bounds

Let

```text
N_k = product_{i<=k} n_i,
N_0=1.
```

Eliminating the largest coordinate at each level gives:

```text
depth <= m,
number of saturated point-fibers <= sum_{k=1}^m N_{k-1},
number of lower point cylinders needed for a fully explicit DNF <= |X|.
```

Thus a crude uniform bound is `<=(m+1)|X|` nodes.  For the C=1 coarse system, `|X|=U`.

### Application to the admitted class

After the `K_2=2` constant boundary is handled, every admitted coarse fatal event is triangular:

- dynamic row `p`: top coordinate `p`;
- rigid row `q`: top coordinate `P^+(w_q)`;
- `K_2>=3` event: coordinate two.

The ascending dependency DAG supplies the triangular ordering.  Hence every complete fixed-anchor coarse cover has an exact semantic contraction tree.  Reverse CRT transfers the root statement to the original full exponent period.

This theorem permits arbitrary exact lower macro-events.  It does not prove closure in the admitted row grammar.

## T2. Complete simultaneous certificate implies an actual odd saturated fiber

Assume a finite simultaneous certificate is complete for both anchors.  Choose an anchor using the exact two-adic anchor lemma:

- no two-adic row: either anchor has no two-adic obstruction;
- `K_2=2`: choose an anchor with a safe constant boundary;
- `K_2>=3`: choose an anchor with two-adic unsafe density at most `1/2`.

Run the exact semantic contraction tree for this anchor.  In the admitted class no odd row has top coordinate two: dynamic rows are assigned to their odd row prime, and the only possible `w_q=2` case is the regular row `q=3`, which cannot supply a positive rigid valuation below `s_3=1`.  If no odd-coordinate saturation node occurred, contraction would therefore end with only:

- no event at coordinate two, or
- a safe `K_2=2` constant boundary, or
- a genuine coordinate-two event that covers at most half of that coordinate.

None can cover the terminal domain.  Therefore:

> Every complete finite simultaneous certificate would induce, for an anchor supplied by the two-adic lemma, at least one **actual** saturated odd-coordinate fiber.

This strengthens the statement “some odd coordinate has budget at least one” only at the semantic fiber level.  It does not identify a beta-one pair or an admitted residual.

## T3. Completeness-to-beta-one chain audit

The proposed chain was

```text
complete finite certificate
=> some saturated odd coordinate
=> exact aligned fiber cover
=> sound lower-coordinate contraction.
```

The audit result is:

1. `complete => some actual odd saturated fiber`: **proved semantically**, as T2.
2. `density saturation D+R>=1 => actual fiber coverage`: **false**.
3. `actual fiber coverage => beta-one alignment`: **false in the abstract normal-form grammar**.
4. `actual fiber coverage => admitted residual closure`: **not proved and false for unrestricted exact macro-predicates**.
5. `aligned beta-one fiber => sound pair contraction`: **proved**, provided alignment is explicitly checked.

The actual arithmetic `67/20771` misalignment example gives the decisive failure in step 2.  The aligned and misaligned systems have the same lower congruences after formally removing the `67` coordinate, but only the aligned system covers the fiber.

## T4. Termination audit

### Is the ascending DAG sufficient?

It is sufficient for **triangular dependence**.  It is not sufficient by itself for an arbitrary syntactic contraction procedure.

A terminating procedure additionally needs:

1. contraction only at a maximal active coordinate, or another explicit well-founded rank;
2. exact removal of that coordinate from every child residual;
3. finite branching;
4. branch-local event use rather than global destructive consumption.

Under exact maximal-coordinate semantic contraction, these conditions hold automatically and depth is at most the number of active coordinates.

### Re-activation

An eliminated coordinate cannot reappear in the semantic theorem because the child predicate is defined on the lower product only.  A syntactic rewrite can reintroduce it if residual moduli are not fully divided by the eliminated prime; such a rewrite is outside the theorem.

### Multiple rigid rows and branching

Multiple rows may close different lower cylinders.  The dynamic event must be reusable branch-locally.  Treating a row as globally consumed after its first pair contraction is unsound and order-dependent.  The `2 x 3` exact example in `results/abstract_search.json` demonstrates this.

### Confluence

The exact saturation predicate `Sat_p` is canonical.  Different DNF decompositions may give different trees, but all represent the same lower set.

Universal projection over independent coordinates is semantically confluent because universal quantifiers commute.  The implementation exhaustively checks both elimination orders for all `4096` subsets of a `2 x 3 x 2` product.

Naive pairwise row-consumption is not confluent.

### Repeated dependencies and overlaps

Distinct row primes do not prevent many rows from sharing one coordinate prime through their orders.  Overlapping rigid shells can inflate `R` without increasing actual union size.  Neither repeated coordinate use nor overlap breaks semantic well-foundedness, but both invalidate density-only or globally destructive contraction rules.

## T5. Conditional admitted-class contraction-tree theorem

### Hypothesis: hereditary exact shell decomposability

For every reachable fixed-anchor state and its maximal coordinate `p`, require:

1. the actual saturation set `Sat_p` has a finite decomposition into lower CRT cylinders;
2. each cylinder has an exact set-level cover of `X_p` by admitted dynamic shells and rigid slices;
3. all local-zero centers are covered only by other valid events;
4. rows may be reused on distinct branches;
5. every child residual removes all `p`-dependence and remains in the admitted contraction grammar;
6. the same conditions hold recursively for every child.

### Theorem

> For every finite admitted fixed-anchor system passing the appropriate two-adic boundary, if the system is complete and hereditarily exact-shell decomposable, then it has a finite, sound admitted-class contraction tree.  Its depth is at most the number of active prime coordinates and its point-cylinder expansion has at most `sum N_{k-1}` internal saturated fibers.

### Proof

Induct on the number of active coordinates.  At the maximal coordinate, hereditary exact shell decomposability supplies an exact finite cylinder decomposition of `Sat_p` and admitted lower children.  The contraction identity from T1 proves soundness and completeness preservation.  Every child has one fewer coordinate.  Apply the induction hypothesis.  The stated bounds follow from the number of possible lower assignments.

### Simultaneous anchors

If both anchor slices satisfy the hypothesis, one obtains two sound fixed-anchor trees sharing the original row parameters.  A single common tree requires a stronger **joint** decomposability condition; it is not implied by separate completeness.

This is Outcome C.  The sole structural gap is not termination once exact contractions exist; it is the existence of a hereditary exact admitted decomposition.

## T6. Two-adic cases

### No two-adic row

There is no preliminary boundary and no coordinate-two event.  Odd contractions retain no hidden two-adic condition.

### `K_2=2`

The condition is constant in `d`.  An unsafe fixed anchor is already terminally covered by this boundary and need not have an odd saturation.  For the necessary odd-saturation theorem, choose the safe anchor supplied by the two-adic lemma.  The boundary is not represented as a fictitious coordinate.

### `K_2>=3`

Coordinate two is genuine and is retained through every odd contraction.  It is processed last.  The selected anchor has unsafe density at most `1/2`, but derived lower events may combine with it at the root.

## T7. Root-cover obstruction and two anchors

No invariant was found that forbids a root cover for both anchors.

The common-residue compatibility rule constrains clipped valuations but does not force equal active logarithms, equal dynamic centers, or equal terminal residuals.  Distinct fixed-anchor terminal residues obstruct only a **shared contraction branch**.  They do not obstruct two separate covers, because a complete certificate is allowed to cover the two anchor slices by different rows and different branches.

Therefore this phase does not prove a conditional universal no-go beyond the exact statement:

```text
if either fixed-anchor exact root is uncovered,
the simultaneous certificate is incomplete.
```

No fixed-anchor no-go is promoted to a simultaneous two-anchor no-go.

## Logical boundary

The contraction theorems concern finite fail-closed local-mask coverage.  A local escape does not prove a sum-of-two-squares representation.  No complete certificate, universal C=1 no-go, or solution of A303656 is claimed.
