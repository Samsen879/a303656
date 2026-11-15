# Triage wave 2026-11-14: almost-all route

**A303656: UNRESOLVED.** There is no general proof and no certified
counterexample. This post-freeze analysis package preserves the triage packet
and adds isolated arithmetic replay tools; it does not alter frozen authority.

Proofs were produced and cross-checked by AI models. No human mathematician has reviewed them; nothing is formalized.

The Round-1 R1-b/R1-c original manuscript was not obtained and V/L are
independent reconstructions. The user subsequently supplied the full reports
A2, R2, V, E2 and L; all five are now **PRESENT** under
[`source/full_reports/`](source/full_reports/). They supplement the retained
referee notes and certificates without upgrading any mathematical status.
A2's eleven-root and R2/C21's twenty-two-root statements are historical source
versions; C22's twenty-three-root condition is recorded in the triage packet.
See [source custody](SOURCE_CUSTODY.md) and the original
[packet README](source/triage_packet/README.md).

## Evidence labels and main claims

The labels below retain the requested candidate and review qualifications.
Machine checks certify finite arithmetic, not the analytic arguments. The
conditional synthesis is new in this integration and was not separately
refereed. Neither the index classifications nor a passing replay upgrades a
candidate to a human-reviewed or formalized theorem.

Here `f_q` denotes the finite eventual-power norm profile and `f_inf` its
profinite limit, with the joint exponent pushforward measure retained.
POS is positivity of `f_inf` Haar-almost everywhere; LP is positivity of every
finite profile at every residue. `R(n)=0` means the original integer has no
representation. Eventual powers and ordinary nonnegative exponent rows are
different objects.

### a) A2 zero-set theorem (candidate, AI-refereed)

`{f_inf = 0} = union_q {f_q = 0}` a.e.; hence **POS ⇔ LP**.
Classification: **PROVED (candidate)**. Available evidence:
[A2 independent audit](source/triage_packet/proofs/a2_agent__a2_independent_audit.md).

### b) V weighted integer L2 transfer (candidate, AI-refereed)

`limsup X^{-1} #{n in [X,2X] : R(n)=0} <= Haar{f_inf = 0}`;
hence **POS ⇒ almost-all**. Classification: **PROVED (candidate)**.
Available evidence: [V independent review](source/triage_packet/proofs/v_agent__review.md).
This weighted transfer does not establish unweighted integer SM.

### c) C22 (PROVED NEGATIVE STRUCTURAL THEOREM in the model, candidate, AI-refereed, finite budgets machine-checked)

Any finite eventual-power zero `f_q(a) = 0` requires **>= 23 distinct primes**
`p > 3` with `p ≡ 3 mod 4`, `p^2 | q`, and
`3^(p-1) ≡ 5^(p-1) ≡ 1 mod p^2`.
Classification: **PROVED NEGATIVE STRUCTURAL THEOREM (candidate)**.
Scope: **eventual-power model**. Available evidence:
[second referee](source/triage_packet/proofs/a2_agent__c22_second_referee.md)
and [independent referee](source/triage_packet/proofs/c21_agent__c22_independent_referee.md).

C21 replays 29 budgets, all below 1, with worst margin `2465867/878169600`.
C22 reconstructs 80 smooth exponents, 60 prime factors and 46 inert rows;
all 33 budgets are below 1. Its base is `155932663/190512000`, its maximum
at `M=11, t=11` is `4238011529/4390848000`, and its slack is
`152836471/4390848000`. The joint 7/11 core bound is `31/75`, replacing
`34/75` within this model calculation.

This does not replace the repository's ordinary admitted `C=1` seven-root
conclusion. A finite eventual-power zero can leave ordinary transient `c`
rows; it is not itself an integer counterexample certificate.

### d) CONDITIONAL synthesis (new in this integration, from a+b+c; not separately refereed)

If at most 22 primes `p ≡ 3 mod 4` satisfy
`3^(p-1) ≡ 5^(p-1) ≡ 1 mod p^2`, then
`#{n <= X : R(n) = 0} = o(X)`.
Classification: **ACCEPTED CONDITIONAL IMPLICATION (candidate; synthesis not separately refereed)**.

Indeed, the hypothesis and c) exclude every finite eventual-power zero,
giving LP; a) gives POS; b) gives the dyadic almost-all bound and hence the
stated natural-density conclusion. The hypothesis is not established here.

Supporting fact (external search bound as supplied in the integration
request): such a prime must be a base-3 Wieferich prime.
[OEIS A014127](https://oeis.org/A014127) lists only 11 and 1006003, with none
further up to `9.7e14` (Dorais–Klyve). Neither is base-5 Wieferich, as
[the modular-power check](tools/check_joint_wieferich.py) verifies. Thus no
such joint prime is known, and none exists below `9.7e14` on that reported
search bound. The tool checks only the named examples; it does not replay
the external exhaustive search. It also checks the base-5 examples 20771,
40487 and 1645333507, which are not base-3 Wieferich and are `3 mod 4`.

**This does NOT address every n, and LP itself remains OPEN.**

## e) Other lane results: packet-summary scope only

These retain the packet's bridge names and OPEN qualifications; no stronger
classification is inferred from the subsequently supplied reports.

- **E2 unit-noise bridge**: for fixed canonical `λ(x) in {1,2,18}`,
  `lim Δ_Y = Haar(union_Y {a_Y=0})`; thus `Δ_Y → 0` iff all finite canonical
  branches are positive. This primitive positivity remains **OPEN**. It
  implies norm LP; the converse is unproved. The joint measure, full lower
  exponent conditioning, exact `v3=2` for λ18, and the fact that the piecewise
  martingale need not have mean 1 are retained.
- **E1 C32 bridge**: MP-LT iff all finite C32 primitive profiles are positive
  iff the corresponding primitive limit is positive Haar-a.e. The unit-noise
  support theorem supplies the finite-positivity-to-quantile interface; the
  finite gate remains **OPEN**. No global equivalence or implication between
  the E1 and E2 gates is proved. The packet's C22 corollary gives positivity
  with at most 22 inert unit primes including 3, hence an E1 finite zero
  requires at least 23 distinct inert primes; it has no joint-nonregular or
  `p^2` requirement.
- **W6 model bridge**: `W_inf^(6) = E[f_inf/π | bad-prime coordinates]` with
  the same zero set a.e. This does not prove unweighted integer SM.
- **P3 78-consecutive blocks; C1/C2 partial results**: the supplied packet
  README gives no summary or evidence labels for these lanes. They are not
  reconstructed or assigned a status here. Adding full-report source bytes
  does not expand this packet-summary-only integration into those lanes.

The packet warns that λ18 conditioning can make the 271 bad mass `1/30`,
exceeding C21's unconditioned `1/81`: budgets cannot be transplanted directly.
The catalog's absence of joint-nonregular rows does not justify dropping
regular artificial targets introduced by induction.

## Reproduction

See [REPRODUCE.md](REPRODUCE.md). Both tools use only the Python standard
library. Original packet bytes are covered by its manifest; all integration
files are covered by this package's `SHA256SUMS`.
