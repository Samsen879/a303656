# Unified state space, exact escape, and blocker semantics

## 1. Two orientations that must not be confused

There are two valid but different recursions.

**Ascending escape:** fix the actual two-adic boundary, then assign odd CRT
coordinates in increasing order. A prefix fixes lower variables. A rigid event
is permanently excluded only after a necessary congruence has actually failed.

**Descending obstruction:** remove the largest remaining odd coordinate using
an exact saturation formula, or a complete linear sub-residual. Its provenance
remembers higher-coordinate covering witnesses. These removed coordinates are
not an ascending lower prefix.

The same frozen original ledger supplies both. We do not transfer a resource
“deleted” in one orientation to the other without checking the corresponding
pointwise exclusion.

## 2. Frozen ledger

An original row token is

    (q,K_q,r_q,E_q,w_q,s_q,anchor-specific exact normal forms).

One token means one actual prime and one shared residue state. An allowed
configuration family is useful only while searching row parameters. After a
state has been chosen, it must be used unchanged in every branch and anchor.
The final ambient U and all beta_p are retained separately from active events.

A geometric macro token records its exact CRT guard, parents, eliminated
coordinate, exact covering witness, and original row/state support. It does
not acquire a new prime identity, residue, or independent resource capacity.

## 3. Ascending state and the correct primal

An exact ascending state is

    A = (frozen ledger, prefix y, alive anchors S, surviving rigid events,
         certified exclusions, surviving blocker options, unassigned coordinates).

At a selected two-adic boundary retain precisely those anchors that are
currently two-adically safe. The K_2=2 constant predicate is handled before
induction; it is not a fictitious coordinate. With no two-adic row both
anchors initially survive.

For fixed lower y and next odd p, let B_c(y,z) be the union of actual rank-p
fatal slices at anchor c. Upon choosing z, update

    S' = S minus {c : B_c(y,z) is true}.

The true escape primal is

    exists c, exists d : every local row is safe at anchor c.

The stronger statement “exists one d safe at both anchors” is a sufficient
primal for a no-go but is not equivalent to it.

Let W(A) mean that some completion leaves at least one alive anchor. Then

    W(A) = OR_(z in X_p) W(A with p=z and surviving set S'),
    W(terminal,S) = [S is nonempty].

This is exact finite backtracking with no exchange of quantifiers. Its dual
is a finite losing tree: every possible next digit leads to another losing
state, ending with no alive anchor. This is an exact Boolean dual, not a new
linear-programming strong-duality theorem. The local algorithm in the code
uses whole coordinate residues z modulo p^beta, not merely first digits.

A common-safe algorithm artificially retains the initial S unchanged. An
actual SPLIT can stop that stronger algorithm while leaving a valid one-anchor
escape. The alive-anchor recurrence is therefore necessary for an exact
interface with pooled branches.

## 4. Temporal blocker states

For each anchor-specific rigid event of q, a blocker lambda must be an odd
prime divisor of w_q. A global static plan may assign q one such coordinate
or leave it alive. Its rigid events at the two anchors then contribute at
most two forbidden first digits.

At the current ascending prefix, distinguish:

- **preblocked:** an already chosen coordinate violates the necessary rigid
  logarithm congruence. The event is empty for every future extension;
- **currently blockable:** the next coordinate is its assigned blocker, but
  the required exclusion has not yet been chosen;
- **future blockable:** a later unassigned order coordinate remains;
- **unavailable:** no remaining valid option under the selected policy.

These labels apply to **rigid events**. A row rigid at one anchor can be
dynamic at the other. Blocking its rigid event must not delete its other-anchor
dynamic event. The regression suite explicitly tests this implementation pitfall.

A current assignment becomes preblocked only after selecting a digit outside
all its forbidden positions. Future intention is never sufficient.

For a top S1/Kraft argument, rows assigned to the top coordinate itself have
not been preblocked by the lower point. They remain resources in a full-fiber
mass calculation. They may be omitted within the jointly restricted domain
X_p minus the blocker set, but that changes the remaining demand from X_p to
that restricted domain. One cannot retain a demand of mass one after this
conditional omission.

## 5. Hybrid local escape theorem

Fix an actual common lower prefix y. Let F_p be the union of currently
required forbidden first digits, B_F their first-level cylinders, and let
D_0,D_1 be the dynamic shell bundles at the two anchors. Let R_0,R_1 contain
all remaining non-preblocked rigid top cylinders. At a common lower point
at most one original dynamic p-row is active, by odd-row anchor exclusion.

If D_(p,c) denotes a correct upper bound on its conditional normalized mass,
and R^rem_(p,c) is a correct upper bound on the corresponding rigid mass, then

    |F_p|/p + max(D_(p,0),D_(p,1))
                + R^rem_(p,0) + R^rem_(p,1) < 1

implies a coordinate residue z modulo p^beta outside all these events.

**Proof.** The forbidden union has measure at most the left hand side, by the
union bound and the exclusion of simultaneous dynamic activity. The domain
has measure one, so the complement is nonempty. QED.

This proves the proposed inequality in its sound temporal interpretation.
Keeping currently blockable rigid events inside R^rem is conservative. A
sharper joint check may remove such cylinders because they are contained in
B_F; the actual choice must still avoid B_F. This is a set-inclusion argument,
not advance certification that the row is already dead.

The bound is sufficient, not necessary. Its failure is not a critical-core
certificate and is not proof that either anchor has a full fiber.

## 6. Exact centered forbidden-set theorem

Let D be the one active parity-shell bundle (or the empty bundle), and let
R^+ be all actual remaining rigid cylinders together with the blocker
first-level cylinders. Blocker cylinders are geometric constraints, never
arithmetic resources. Choose the dynamic center zeta; for an empty D any
center may be chosen. The exact union is full if and only if:

1. some member of R^+ contains zeta; write e for the smallest depth of such
   a centered cylinder;
2. for every j<e not accepted by D, each noncenter child of the depth-j
   center node is fully covered by R^+.

**Proof.** Without a centered cylinder, zeta is a hole. With one at depth e,
its whole subtree is covered. Outside that subtree, accepted side shells
are covered by D, while unaccepted side subtrees have no dynamic coverage
and must be covered by R^+. These sets partition the coordinate. QED.

For each demanded side cylinder B, the correct mass test uses

    mu(B intersect union R^+) = mu(B),

not an inside-only sum that omits an available ancestor. Cylinder intersections
are either empty or nested. Remove duplicate/contained cylinders before adding
masses, or recurse on the prefix trie. This gives an exact rational union
measure and retains positions.

The dynamic-heavy case alone cannot cover the coordinate because its center
is omitted. In a blocker-heavy case, F_p may exhaust all first digits, but
this can be failure of a particular plan rather than of the original system.
A rigid-heavy mass bound need not be an exact full frontier. A pooled
paired-rigid cover need not be full at either anchor. A mixed case is tested
by this exact centered theorem, not by classifying the sign of a scalar bound.

## 7. Global blocker optimization

A static sufficient-policy search can be encoded with binary variables

    x_(q,lambda), x_(q,alive),   sum_lambda x_(q,lambda)+x_(q,alive)=1.

Only lambda|w_q is allowed. For every position a, a binary y_(lambda,a)
records whether at least one assigned rigid event forbids it. Enforce the
exact OR by

    y_(lambda,a) >= x_(q,lambda) for each incident q,
    y_(lambda,a) <= sum_(q incident to a) x_(q,lambda).

The first-digit cost is sum_a y_(lambda,a)/lambda, not twice the number of
rows when positions overlap. Prefix-dependent guard/activity and preblocking
variables must be added to make conditional remaining capacities exact.
Current preblocking implications are enforced only after the corresponding
coordinate choice. Per-coordinate one-hot variables for z and Boolean event
truth constraints give a finite integer feasibility model for a frozen U.

One can optimize the maximum sufficient hybrid load, the number of rows
permanently excluded before a selected top coordinate, or a genuine alive-
anchor escape. These objectives are different. A bad optimum for the
sufficient hybrid-load relaxation is not an infeasibility certificate for
the exact primal.

The free-coordinate uniform case reduces to capacitated bipartite matching:
capacity floor((lambda-1)/2) for a paired worst-case assignment, or lambda-1
for a selected single anchor. General position-sharing and row configurations
do not have a proved ordinary flow or matroid min-max theorem here.

The code exhausts the four static options alive,5,31,67 for the actual
20771 rigid row and checks one deterministic greedy policy for each. It does
not claim a generic optimal ILP solver. The independent exact backtracking
game handles digit choices without this incomplete greedy-policy restriction.

## 8. S1, pooled branches and a conditional blocker--Kraft theorem

At the greatest original odd rank p, retain the source notation

    A_c(y) = lower original events already cover anchor c,
    S_c = {y : rank-p fiber is full at anchor c}.

Completeness at both anchors implies

    Y minus (A_0 union A_1) subset S_0 intersect S_1.

Thus a common lower survivor forces a joint top full fiber, while the absence
of such a survivor can produce the genuine pooled obligation

    A_0 union A_1 = Y.

It does not produce A_0=Y or A_1=Y. Its anchor labels cannot be dropped.

A valid conditional unified escape/no-go argument is:

- construct a common-safe two-adic boundary and a lower ascending escape,
  using exact unions or the hybrid sufficient inequalities;
- remove only rigid events actually preblocked on those chosen lower
  coordinates;
- at the maximal original rank, exclude a full rigid-only frontier at each
  possible dynamic-inactive anchor, using exact positions/configurations or
  active original Kraft deficits.

S1 and dynamic anchor exclusion then contradict completeness. With F empty
this recovers #15 S3. With a complete free-blocker assignment it recovers the
escape mechanism of #14. Stronger original position/Hall tests from #16 can
replace a scalar top rigid deficit.

This conditional theorem alone does not reach Phase B. The unconditional
first-nonlinear-core theorem in `MASTER_THEOREM.md` supplies the stronger
reduction. It uses a parity-flexible selected anchor instead of assuming a
false common boundary or converting pooled coverage to individual completeness.

## 9. Configuration dual weights and their limit

For original q, let F_q be the finite family of permitted whole paired states.
A feasible global choice selects one state per original q, independent of
which proof branch later cites it. For residual demands D_c and nonnegative
weights f_c, coverage necessarily gives

    sum_c integral_(D_c) f_c
      <= sum_q max_(C_0,C_1 in F_q)
                     sum_c integral_(D_c intersect C_c) f_c.

Removing demands already covered by a dynamic event is legitimate. Adding
all alternative configurations of the same row as capacities is not.
This includes branch/antichain Hall inequalities and ordinary active Kraft
necessity, but is generally only a fractional relaxation. The four-demand,
two-row counterexample in `COUNTEREXAMPLES.md` passes every such weighted
inequality and has no integral configuration cover.

No theorem proving all exact losing trees require impossible arithmetic
resources has been obtained. The weighted inequalities are tools for
refuting particular candidate cores, not a proved complete dual description.

## 10. Descending core record

A descending state has

    C = (frozen original ledger, selected anchor/parity,
         active original dynamic events, single-origin seeds and lineages,
         retained ambient depths, blocker options, exact residual predicate).

In the linear phase its rank is the number of uneliminated odd coordinates;
seed count is nonincreasing. Before the first nonlinear merge, each seed
origin is unique, and its depth/position is inherited from original guards
and fixed helper-row logarithms. Original resources are not independently
reselected at each level.

At the first essential nonlinear merge add the exact lower witness, an
irredundant actual geometric frontier, and the seed-origin injection. These
records define E_L in `MASTER_THEOREM.md`. After a nonlinear merge multiple
clauses may reuse one original source. There is no proved monotone weighted
resource potential covering that stage.
