# Exact P5 Family-U unbalanced full sparse census

This directory evaluates only the 457 fresh Family-U descriptions frozen by
the authenticated Design C authority at results commit
`1a3b130536245ef8fcd318b591e1dd37c03eef06`.

The source phase is deliberately evaluator-free.  Run the source tests before
creating the source commit.  Formal evaluation is accepted only when the
runner is invoked from a clean checkout whose `HEAD` is the declared source
commit and whose direct parent is the expected results commit.

No Family R/Q description, adaptive extension, outside-panel integer, or
description-weighted primary distribution is permitted.

Final source commit S:
`cc8932e6bc62c325202c01a39d353c1aac115c93`.

Compact results are under `results/`.  The exact verifier conclusion is
`VALIDATED EXACT P5 FAMILY-U UNBALANCED FULL SPARSE CENSUS`; the mathematical
problem remains unresolved.  See
`docs/p5_family_u_unbalanced_full_sparse_census.md` for the narrative report.
