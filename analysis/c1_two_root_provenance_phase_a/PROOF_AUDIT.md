# Adversarial proof audit

This is an internal audit of the new arguments, not external peer review.

## Primary theorem: possible failure points checked

**1. Is a rigid event really one full order congruence?**
Yes, this is the admitted original-row normal form in the bound sources. A
positive accepted rigid valuation lies strictly below s_q. There is at most one
active logarithm class modulo w_q per anchor. The theorem does not apply this
normal form to derived macros.

**2. Why do only nonregular rows require blockers?**
A positive odd h < s_q requires s_q>=2. A regular row (s_q=1) has no such rigid
fatal event. It may be dynamic or coarse-inert, which are handled separately.

**3. Can a row be dynamic at one anchor and rigid at the other?**
The proof allows this. Only its rigid-anchor logarithm contributes a forbidden
blocker digit. Its dynamic-anchor event is handled at its own row-prime
coordinate. The uniform pool includes all potential rigid rows and overcounts
at most two digits per original row.

**4. Does choosing a blocker destroy a required dynamic escape?**
No: the blocker is an odd coordinate lambda with lambda not in P. There is no
original dynamic lambda-row. This premise is essential; the familiar 66+1 full
67-fiber demonstrates why coordinate 67 itself is not a valid free blocker when
the dynamic 67-row is present.

**5. Can a later coordinate reactivate an excluded row?**
A blocked rigid row requires d=a modulo w_q, and lambda divides w_q. Violating its
first lambda digit permanently excludes it. A dynamic p-row depends only on p
and primes below p, so later coordinates cannot reactivate it either.

**6. Why can both dynamic anchors be avoided with one digit?**
After lower coordinates are fixed, d modulo w_p is fixed, hence so is 5^d modulo
p. Both positive p-divisibilities would imply p divides 2. Thus at most one
anchor is active. That event has a nonempty excluded local-zero center cylinder.
This is stronger than merely asserting two arbitrary disjoint fatal slices.

**7. Could an unresolved zero be accidentally accepted?**
The chosen dynamic center is a nonfatal coarse choice, not a claim that the row
accepts a zero. At full precision local zeros remain unresolved. The joint
reverse CRT lemma uses only the existence of a nonfatal lift, never acceptance
of zero. Direct valuation tests and deeper odd-shell unit tests enforce this.

**8. Does common coarse escape have a common full lift?**
For each original prime only one anchor can be divisible on the entire fixed
coarse class. Its extra exponent digits above v_p(U) are private to that row;
other row orders already divide U. Choosing the safe local extension and merging
these independent prime-power digits gives a common full odd-safe lift. The
proof is symbolic; finite direct tests are supplementary.

**9. Does the optional two-adic row invalidate the construction?**
The blocker coordinates are odd, and the construction works for every prescribed
coordinate-two assignment. Select one safe anchor/class from the exact source
lemma. K2=2 is a constant boundary and is never given a fictitious coordinate.
The proof does not claim both anchors are two-adically safe.

**10. Does the theorem need identical contraction trees?**
No. Construct a safe original point first; exact universal fiber elimination
preserves the escape under projection in either tree separately. No coordinate,
branch, witness, residual, or macro is identified between anchors.

**11. Is the inventory conclusion a finite-scan extrapolation?**
No. The sieve/exponent test exhausts the explicit 10^7 prime range. The symbolic
blocker theorem supplies all-residue and all-precision quantifiers for the
resulting finite nonregular pool. No nonregular absence above the bound is used.

**12. Are additional regular support rows harmless?**
They may refine U, beta, and L, and may add dynamic events. They cannot supply a
dynamic row at 5 or 653, so the first-digit blockers persist. At any actual row
prime there is still only one original dynamic row, with a proper fatal slice.
Thus the proof is not tied to a frozen shallow ambient period.

## Genuine boundary

The verified nonregular resource 1645333507 has order
2 * 3^3 * 30469139, with both odd factors admissible as dynamic row primes.
A panel containing those dynamic rows has no structural free-order-factor
blocker for this resource. This shows a gap in coverage of the theorem's
hypothesis, not a counterexample to the conclusion or a complete certificate.

## Other results: limitations checked

- Three-row minimality is only for proper product cylinders on 2 x 2; no actual
  prime realization is claimed.
- I1 and I2 have ambiguous unqualified formulations. The report states precisely
  the original-rank and proper-residual versions tested.
- Macro-count and naive-mass examples are bookkeeping diagnostics; general
  exponential macro growth and fixed-state Hall capacity already occur in sources.
- Partial-assignment antichains represent exact truth on product state choices;
  they need not be all one-hot semantic prime implicants.
- Cardinality/charge is only a necessary filter; an explicit passing-but-UNSAT
  example is retained.
- Residue trie compression preserves multiplicities, representatives and zeros;
  state products are not advertised as exhaustive system searches.
- Geometry-only exact truth agrees with provenance when states are frozen.
  The positive relaxation example changes the allowed paired-state relation.
- No local-certificate no-go proves universal sum-of-two-squares representability.

## Novelty and authority

These are new derivations in this research session relative to the source
arguments used here. No comprehensive literature novelty claim, external referee
acceptance, repository-wide audit, route promotion, or problem resolution is made.
