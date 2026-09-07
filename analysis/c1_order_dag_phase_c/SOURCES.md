# Sources and authority custody

All mathematical repository dependencies are pinned to main
`71b8d428b32724c37e593bcfd9d5f06a42e72d21`, tree `5609e47eed0c058c190ef59c61644e2fd4b8fad6`.
The main SHA/tree were checked at the start and rechecked before sealing.
PRs17,20,18,19 were separately confirmed merged; `source_binding.json` records
their actual merge commits and dates. All connector actions were reads.

## Required source packages

* `analysis/c1_kraft_hall_phase_a/` — full merged PR #16 diff read.
* `analysis/c1_unified_endgame_phase_b/` — full merged PR #17 diff read.
* `analysis/c1_seven_prime_audit_phase_b/` — full merged PR #20 diff read.
* `analysis/c1_pooled_lower_cover_phase_b/` — full merged PR #18 diff read.
* `analysis/c1_blocker_deficient_core_phase_b/` — full merged PR #19 diff read.

Load-bearing current-main files were fetched separately: STATUS, Unified
MASTER_THEOREM, Pooled THEOREM_AUDIT, Blocker THEOREM_AUDIT, and Seven Audit
scan_summary.json. A recursive main-tree read was also obtained. Diff reading
is not a local checkout or independent byte-hash authentication of every source.

## Pinned references

- https://github.com/Samsen879/a303656/blob/71b8d428b32724c37e593bcfd9d5f06a42e72d21/STATUS.md
- https://github.com/Samsen879/a303656/blob/71b8d428b32724c37e593bcfd9d5f06a42e72d21/analysis/c1_unified_endgame_phase_b/MASTER_THEOREM.md
- https://github.com/Samsen879/a303656/blob/71b8d428b32724c37e593bcfd9d5f06a42e72d21/analysis/c1_blocker_deficient_core_phase_b/THEOREM_AUDIT.md
- https://github.com/Samsen879/a303656/blob/71b8d428b32724c37e593bcfd9d5f06a42e72d21/analysis/c1_pooled_lower_cover_phase_b/THEOREM_AUDIT.md
- https://github.com/Samsen879/a303656/blob/71b8d428b32724c37e593bcfd9d5f06a42e72d21/analysis/c1_seven_prime_audit_phase_b/results/scan_summary.json

## Mathematical dependency map

THEOREMS Sections1--2 reconstruct the boundary-selected anchor, sparse local
saturation, single-origin provenance, original seven-prime lower bound, and
terminal guard release from the source stack. Section10 retains the exact scope
of the imported P4 sufficient criterion. The new proofs are Sections4--9, the
residual-slack/joint-policy refinements, and the conditional construction.

The bounded inventory is an imported certified source result, not a new scan.
Its three specific primes, orders, lifting exponents and full absolute terminal
sets are independently recalculated by this standalone program.

The selected cyclotomic factor discoveries are not relied on as primality claims.
Every factor used in the reference proof is authenticated by recursive full n-1
Lucas certificates and exact products. Discovery used SymPy; verification uses
only the standard library. No external unproved Wieferich-distribution claim is
used. These are not two independently staffed implementations.

No source text containing user identity details or private project files is
republished. No proof-assistant check, independent referee decision, repository
state change or mathematical promotion is claimed.
