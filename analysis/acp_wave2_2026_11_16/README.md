# ACP wave 2026-11-16: the abstract covering problem behind LP

**A303656: UNRESOLVED.** There is no general proof and no certified
counterexample. This post-freeze package preserves the wave-2 research packet
and adds an independent check script. It does not alter the frozen authority.

All statements below were produced and checked by AI models and by exact
programs. No human mathematician has reviewed them; nothing is formalized.
The producer packet was generated in a separate Claude session (reported by the
project owner as Claude Fable 5.2); this integration and the independent checks
were done in another Claude session. See [source custody](SOURCE_CUSTODY.md).

## Question

The [2026-11-14 triage wave](../triage_wave_2026_11_14/README.md) reduced
almost-all representability to local positivity (LP) and showed that a finite
zero `f_q(a) = 0` needs at least 23 joint base-3/base-5 Wieferich primes
`p ≡ 3 mod 4`. Wave 2 asked a dichotomy question:

> Treat a finite set of actual primes `p > 3`, `p ≡ 3 mod 4` as if they were
> joint-nonregular (ignore their Wieferich status, keep the real arithmetic of
> `F_p`). Can their bad events cover the exponent space, i.e. produce a zero
> in this "pretend" model?

- **(N)** never: then LP holds unconditionally, and almost-all follows (given A2 and V).
- **(Y-finite)** only with primes from an explicit finite list: check that list directly.
- **(Y-infinite)** for infinitely many prime sets: local arguments cannot prove LP.

**Verdict: undecided.** No covering was found, the lower bounds rose sharply,
and it is proved that the measure methods used so far cannot settle (N).

## Results (labels as in the producer report)

Full statements and proofs: [producer report (Chinese)](source/acp_packet/REPORT.md).

| Result | Statement (short) | Label |
|---|---|---|
| ACP formalization (Lemmas L1, L2, Proposition P1) | Fix a parity class `c`. For inert `p > 3`, the fibre is `F_p^c(z) = {(a,b) : 3^{c1} 9^a + 5^{c2} 25^b ≡ z mod p}`. The bad set of every inert prime, regular or not, lies inside a fibre. For a pretend joint-nonregular prime a suitable lift `a mod p²` makes the whole fibre bad. So a zero exists iff some parity class (not killed by the 2-adic and prime-3 conditions) is covered by inert fibres. | PROVED (candidate) |
| Lemma L3 (richness) | In a minimal covering, every odd prime `ℓ` dividing some `h3·h5` is used by at least `ℓ` primes. | PROVED (candidate) |
| Lemma L4 + Theorem F | Points of `x + y = z` in two cosets of `μ_M`: `z ≠ 0` gives at most `M − 1` (at most `(M−1)/2` for different cosets). An exact tiling of a fresh `M`-fibre by `M` traces happens only for `M` parallel lines of one type. | PROVED (candidate) |
| Theorem A | No covering uses only primes with `H_p < 16384`. Every covering needs a prime with `H_p ≥ 16384`, so `p ≥ 32771`. | PROVED + finite computation (candidate) |
| Theorem R(146), pure model (`Q = ∅`) | Every covering uses at least 147 fibres. | PROVED + finite computation (candidate) |
| Theorem R(146), general | `f_q(a) = 0` needs at least 147 distinct joint-nonregular primes. Conservative Haar-only version: 30. | CONDITIONAL on C21 (H1) rigidity and (H2) regular averaging + finite computation (candidate) |
| Proposition H | For any measure `μ`, `Σ_p max_z μ(F_p(z)) ≥ Σ_p 1/p`, and the reciprocal sum over inert `7 ≤ p ≤ 473899` is `≥ 1`. Fractional coverings exist, so no union bound, LP dual or measure certificate can prove (N). A proof needs integrality (one residue per prime). | PROVED NEGATIVE STRUCTURAL THEOREM (candidate) |
| One-parameter controls | A single `β`-line is covered by 18 inert primes (explicit, `N = 315`); the `α`-line with `h3 | 315` is not. Any obstruction must be two-dimensional. | finite computation |

Producer-flagged risks, retained verbatim in substance:

- class `11` at `K = 146` has margin about `1.07·10⁻³`; it is integer arithmetic
  but sensitive to any single catalogue weight. Cite the Haar-only 30-root
  version when a conservative statement is needed;
- the measures `ν0` came from a floating-point LP; correctness rests on the exact
  verifier, which shares mass-computation code (`core_tools.py`) with the search;
- Theorem A was certified at `B = 16384` only; the `B = 32768` rich core
  (593 primes) has no certificate;
- the producer did not search the literature on two-parameter covering problems.

## What this integration adds

1. **Independent finite checks** ([`tools/independent_checks.py`](tools/independent_checks.py),
   standard library only, no shared code): packet hashes; the 18-prime `β`-line
   covering; the Proposition H horizon with directed-rounding bounds; Lemma L4 by
   brute force for `M ≤ 13`, `p < 3000` (observed maxima match the producer's
   table); and the empty `z = 0` fibre in class `(0,0)`. All pass.
2. **Full replay** of the producer's `run_all.sh` (quick mode, with the frozen
   C21 comparison) in a fresh environment; the outcome is recorded in
   [source custody](SOURCE_CUSTODY.md).
3. **Two observations not stated in the producer report:**
   - (N) ⇒ LP does not use the C21 lemmas (H1)/(H2): the bad set of every inert
     prime, regular or not, lies in a fibre, so any real zero yields a fibre
     covering by distinct inert primes;
   - if Theorem R(146) holds, the hypothesis of the 2026-11-14 conditional
     synthesis weakens from "at most 22" to "at most 146" joint-nonregular
     primes `p ≡ 3 mod 4`. This weakened form is a synthesis of this
     integration and was not separately refereed. Since no joint-nonregular
     prime is known at all (none below `9.7·10¹⁴`), the practical difference is
     small.

## Route consequence

- Raising the root threshold (23 → 147 → …) cannot reach LP: Proposition H caps
  every measure-based budget.
- (N) is now an explicit two-parameter covering-congruence problem with primes
  `≡ 3 mod 4`; see the [handoff note](../../docs/ALMOST_ALL_ROUTE_HANDOFF.md) for
  a precise statement and restart points.
- A303656 remains **UNRESOLVED**; LP remains **OPEN**; every-n representability
  is untouched.
