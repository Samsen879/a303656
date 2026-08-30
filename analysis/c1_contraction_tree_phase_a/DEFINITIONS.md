# Formal definitions

## 1. Bound coarse system

Fix one anchor `c in {0,1}`.  Let

```text
U = product over l in Lambda of l^e_l
```

be the coarse exponent period, written through CRT as

```text
X(U) = product over l in Lambda of X_l,
X_l = Z / l^e_l Z.
```

Coordinates are ordered by their rational prime labels.  A coarse fatal event is **triangular** if it depends only on coordinates at or below a largest coordinate `tau(F)`.

For the admitted odd rows:

- a dynamic row `p` has `tau(F)=p`;
- a rigid row `q` is assigned to `tau(F)=P^+(w_q)`;
- a genuine two-adic event with `K_2>=3` has `tau(F)=2`;
- a `K_2=2` event is a constant boundary condition, not a coordinate event.

The ascending order-dependency DAG ensures this triangularity because every prime dividing `w_q` is strictly smaller than `q`.

## 2. Contraction state

A fixed-anchor contraction state is a tuple

```text
Sigma = (c, Lambda, Gamma, F, M, B_2, pi)
```

with the following data.

- `c`: the fixed anchor.
- `Lambda`: the active prime-coordinate set.
- `Gamma`: a compatible lower-coordinate CRT cylinder, or a finite disjoint union of such cylinders.
- `F`: the original row-fatal events restricted to `Gamma`.
- `M`: exact derived macro-events produced by earlier contractions.
- `B_2`: the two-adic boundary/event state.
- `pi`: provenance identifying the parent state and the exact saturation witness.

A simultaneous two-anchor object is a pair `(Sigma_0,Sigma_1)` sharing the original row parameters `r_p,K_p,E_p`, but it is not assumed to share active centers, saturation witnesses, or terminal residuals.

## 3. Active lower cylinder

Let `p` be the largest active coordinate.  For a lower assignment

```text
y in X_<p = product over l<p of X_l,
```

the active lower cylinder is

```text
C(y;p) = {x in X(U): x_<p=y}.
```

There are no active coordinates above `p` in a maximal-coordinate contraction state.  The `p`-fiber is naturally identified with `X_p`.

A row is active on `C(y;p)` when its lower congruence conditions are satisfied there.

## 4. Unresolved center

For a dynamic row `p`, the unresolved center on `C(y;p)` is the subset

```text
Z_p(y) subseteq X_p
```

of coarse `p`-digits for which a full local zero remains reachable, or is already forced, in the row-`p` full lifts.

A local zero is never accepted.  In the regular beta-one case

```text
s_p=1, K_p=2, E_p={1}, beta_p=1,
```

`Z_p(y)` is one digit and the other `p-1` digits are fatal.

For `beta_p>1`, `Z_p(y)` may be a nontrivial `p`-adic center cylinder.  Accepted shells and the unresolved center must be enumerated as actual sets; their densities are not substitutes for set equality.

## 5. Rigid shell and alignment

After all non-`p` coordinates are fixed, a rigid row assigned to coordinate `p` cuts out one residue class modulo `p^k`, where

```text
k = v_p(w_q).
```

Its slice in `X_p` is denoted `R_q(y)`.

A family of rigid slices is **aligned** with a dynamic center when

```text
Z_p(y) subseteq union_q R_q(y).
```

It is **exactly aligned** when the declared saturation witness is checked by direct set equality:

```text
(dynamic fatal shells) union (selected rigid slices) = X_p.
```

For beta one and one rigid row, exact alignment reduces to equality between the rigid digit and the unique dynamic center.  Equality of densities

```text
(p-1)/p + 1/p = 1
```

does not imply this equality of digits.

## 6. Actual saturation set

Let `F_p` be all events whose largest active coordinate is `p`.  Define

```text
Sat_p(Sigma) = {
  y in X_<p :
  for every z in X_p,
  at least one event in F_p covers (y,z)
}.
```

This is **actual fiber coverage**.  It is distinct from the budget condition

```text
D_{p,c}+R_{p,c} >= 1.
```

The budget condition is necessary for a union-bound proof to fail; it is neither a set identity nor an aligned-shell certificate.

## 7. Contraction edge

An exact semantic contraction at maximal coordinate `p` replaces all rank-`p` events by the macro-event `Sat_p(Sigma)` on `X_<p`.

For every lower assignment `y`, the defining identity is

```text
[for every z in X_p, Lower(y) or Top_p(y,z)]
iff
[Lower(y) or y in Sat_p(Sigma)].
```

Here `Lower(y)` means that an event of rank below `p` already covers the entire `p`-fiber.

A compact beta-one pair contraction is a special exact witness.  If the dynamic and rigid digits align, its residual congruences are

```text
x == b_p (mod w_p),
x == b_q (mod w_q/p).
```

The alignment equality is part of the edge certificate.  The residual congruences alone do not certify soundness.

## 8. Residual system

A general exact residual system is a finite disjunction of compatible lower-coordinate CRT cylinders.  Every finite subset of `X_<p` has such a point-cylinder representation.

An **admitted residual system** is stronger: every child must remain expressible in the designated local-mask/contraction grammar without arbitrary semantic macro-events.  The admitted class is not proved closed under exact contraction.

## 9. Contraction depth and rank

For whole-coordinate elimination, define

```text
rank(Sigma) = number of active coordinates.
```

Every exact maximal-coordinate contraction reduces this rank by one.  Hence depth is at most `|Lambda|`.

If a future grammar contracts one `p`-adic digit at a time, use instead

```text
rank_digit(Sigma) = sum_l e_l.
```

and require strict decrease on every edge.  The ascending DAG alone does not supply this decrease for an arbitrary syntactic rewrite.

## 10. Terminal/root cover

A state is terminal when no odd coordinate remains.

- With no two-adic row, the root domain is a singleton.
- With `K_2=2`, the constant boundary was handled before odd contraction.
- With `K_2>=3`, coordinate two remains as the final genuine coordinate and must be covered exactly by the two-adic event together with derived residual events.

A root cover means that the final exact residual predicate is true on the entire terminal domain.

## 11. Soundness invariant

At every node, the contracted system must represent exactly the set of lower assignments whose eliminated fibers were fully covered by the parent system.  In particular:

1. common row residues are not changed;
2. accepted valuation parity is not enlarged;
3. a local zero remains unresolved unless another named event covers it;
4. all exponent conditions retain their exact periodic meaning;
5. reverse CRT is applied only to the original correctly classified coarse events, or to an exactly equivalent contracted predicate;
6. simultaneous anchors remain separately tagged.

This invariant gives equivalence of root coverage and original coarse coverage.  The independently checked reverse CRT equivalence then transfers coarse escape/coverage to full-period escape/coverage.

## 12. Hereditary exact shell decomposability

A reachable state is **exact-shell decomposable at its maximal coordinate `p`** when `Sat_p(Sigma)` has a finite lower-cylinder decomposition such that every cylinder carries:

1. an exact set-level partition/cover of `X_p` by admitted dynamic shells and rigid slices;
2. explicit exclusion of local zeros from the row that generated them;
3. branch-local row use, so a row may certify distinct disjoint lower cylinders without being globally consumed;
4. residual moduli with all `p`-power dependence removed;
5. child states in the admitted residual grammar.

The system is **hereditarily exact-shell decomposable** when every reachable child satisfies the same property.  This is the missing structural hypothesis for a compact admitted-class contraction-tree theorem.
