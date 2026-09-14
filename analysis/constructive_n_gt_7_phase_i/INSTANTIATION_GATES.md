# Frozen arithmetic gates — I7 conjunction false

Source I7's iff concerns instantiation of THIS architecture only, not all N=9
certificates. It requires `|Sq(279)|>=3` and `|Sq(t)|>=1` for each
`t in {903,191,5167,271,4159,31051}`. Subsequent exact certification proves
`|Sq(279)|=0`; the necessary/sufficient instantiation conjunction for THIS
frozen I7 is false, and I7 is CLOSED. See `c279_closure/PROOF.md`.
The other six gates are not evaluated by this closure task and remain unknown.
All nine terminal primes must be distinct. Exact differing
orders separate families; the three order279 slots need explicit distinctness.

Sq(t) consists of admitted primitive square-divisor primes of Phi_t(5):
prime q, q≡3 mod4, q∤t, ord_q(5)=t, q²|Phi_t(5).
Formal atoms, probable primes, regular valuation-one factors, and repeated
use of a single prime cannot fill distinct terminal slots.

For order279 verify primality by replayable proof, and individually check
`pow(5,279,q)==1`, `pow(5,93,q)!=1`, `pow(5,9,q)!=1`,
`pow(5,279,q*q)==1`; retain full exact factor valuations.

The published lower gate B=970453984500000 is an inherited merged Phase G
dependency (analysis/c1_b31_squarehit_phase_g). Known admitted roots below B
have other orders, so any qualifying order279 q exceeds B. No historical scan
is rerun. For k removed qualifying hits, with all removed factors/valuations
certified and exact remainder R, `R<(B+1)^(2*(3-k))` kills ONLY the frozen
architecture. Inconclusive search never establishes squarefreeness or emptiness.
