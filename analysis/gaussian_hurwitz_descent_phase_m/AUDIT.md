# Proof and implementation audit

## Checked claims

The full norm-5 element list is forced by squared-coordinate patterns. Both
implementations verify the six left and right unit classes. The producer
checks all 625 residue vectors, all inverse operators, norm preservation,
and normalization by signed-permutation generators. Its int64 bounds are
small for the frozen norms (maximum M=3919); all arithmetic is exact.

The independently written standard-library verifier uses scalar/vector
quaternion multiplication and pair-of-squares enumeration. It matches every
quotient edge in every panel, all raw state and fixed-pair target counts,
the finite symmetry orbits, and the arithmetic H_bad values. It directly
checks the 1175 sublevel component and both displayed quaternion products.
It does not import reference.py, NumPy, or operators.npz.

Bottleneck values are additionally computed by a minimax version of Dijkstra's
algorithm. Its recurrence is cost(v)=min_paths max_(u on path) H_bad(u).
Multi-source initialization at all targets gives the exact minimum barrier
for every vertex with a reachable target. The 1175 result is independently
certified without relying on that recurrence, by a two-vertex sublevel cut
and an explicit path attaining height 13.

## Corrections made during audit

The first cross-implementation comparison disagreed only on self-loops:
the producer included the identity unit edge, while the initial audit omitted
it. The audit was corrected to initialize each adjacency set with its own
vertex. All edges then agreed. This changes no component, height barrier,
or path-to-target result. The delivered scripts consistently retain loops.

The task's matrix expression was identified as an anti-homomorphism under
its left-j convention; the correct homomorphism is stated explicitly.
Hurwitz content, not ordinary coordinate gcd, is used at 2. Half-integral
states and zero pairs are not marked as targets. Global raw connectivity,
global sufficiency of kappa_5=1, and historical novelty are not asserted.

## Evidence limits

PASS means independent implementation replay by the same assistant. It is
not an external mathematical referee or independent-author review. The
infinite-family invariant, matrix subgroup result, and bounded-lift theorem
stand on their written proofs, not on finite experiments. No theorem was
formally checked in Lean, Coq, or another proof assistant.

The package is ready for adversarial review, not automatically for repository
integration. GitHub remained read-only throughout.
