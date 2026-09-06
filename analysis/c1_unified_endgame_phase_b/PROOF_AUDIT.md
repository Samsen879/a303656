# Adversarial proof audit and limits

This is the producing researcher's audit, not an independent referee report.

## Load-bearing proof checks

| Claim | Audit question | Resolution |
|---|---|---|
| Boundary-selected anchor | Are two different anchors secretly used for the two parities? | No. The mod4 table fixes one c_*; the two targets differ by4 and give both parities for that same anchor. |
| Chosen bad parity | Does adjusting higher two-adic digits change odd-row events? | No. Every odd-row period has 2-valuation at most1; CRT preserves parity. |
| Exact coarse coverage | Is full-period coverage being replaced by pointwise coarse masks without justification? | The source fixed-anchor reverse-CRT theorem supplies the implication, with local zeros left unaccepted. |
| Sparse local lemma | Could an accepted depth-one shell fill the center branch and avoid the p-cylinder tax? | If shell0 is accepted, shell1 is not. Without C1(center), the p child subtrees inside the center branch require p rigid cylinders. |
| Linear descent | Are omitted nonlinear witnesses silently treated as absent? | No. Linear residual is a subset; descent continues only after verifying that this sub-residual remains complete. |
| Source injection | Can one prime acquire two children before the stopping time? | No. Each seed has one fixed top cylinder and at most one fixed compatible dynamic helper; at most one child is generated. |
| Least helper | Could an odd order factor vanish without appearing in the lineage? | No. The descending phase fixes only parity, not other lower coordinates. Guard intersections never erase an uneliminated odd factor. |
| Ambient support | Are coordinates lost when redundant original events are muted? | No. U and every ambient depth remain frozen throughout subcover pruning. |
| Coordinate3 bound | Is the original 81-row tax applied to macros? | No. The new argument uses four fixed actual dynamic-helper guards, capacity8/9, and the geometric depth-three seven-leaf tax. |
| Coordinate5 count | Is macro reuse ignored? | All minimal five-branch witnesses are counted. With five/six top seeds there are at most one/two. This is a one-step exact clause bound, not generic conservation of macro count. |
| Coordinate5 constants | Could the exact residual be a covered constant? | Not from a five-branch witness: all 3-free depth-one5 lineages are trapped in the two fixed helper positions11/71. A nonempty intersection containing a proper3 guard stays proper. |
| Same source across anchors | Does rigid blocking delete the other-anchor dynamic role? | No. Event-kind-specific deletion is enforced. A mixed-role regression guards against this bug. |
| Gate B definition | Is E_L defined by global completeness itself? | No. Its tests are local frontier, lineage, guard, budget and Hall conditions. Completeness-preserving history is additional provenance of the extraction theorem. |

## Scope checks

The seven-prime bound concerns original nonregular cardinality, not the largest
prime size. It does not assert a seven-prime complete example. It does not
bound the total number of regular helper/support rows.

The local core may have five leaves at rank5 when at least seven initial seed
origins occur elsewhere in the system. The theorem does not assert that every
local core independently needs seven leaves. The rank3 rigid-only prebranch
core does have that seven-origin tax.

The paired-resultant theorem is retained at its original rank and lower-point
scope. There is no replacement of the origin prime's true order by a macro's
current geometric modulus.

A fixed greedy blocker policy can fail while exact escape succeeds. A losing
common-safe game can coexist with a winning one-anchor game. Neither failure
is used as a complete-certificate witness.

## Remaining audit boundary

No independent author has checked the new global proof and no proof assistant
has formalized it. The reference lab does not enumerate all possible original
prime systems, depths or residues. Its 15 tests and finite exact audits verify
specified implementation contracts and supporting arithmetic identities.

The highest-priority independent review is Lemma7.2's coordinate5 witness count
and 3-free-helper argument, together with the fixed-ambient and fixed-parity
hypotheses of the least-helper reasoning. No unresolved contradiction in those
arguments was found during this audit; this is not a substitute for independent
review.
