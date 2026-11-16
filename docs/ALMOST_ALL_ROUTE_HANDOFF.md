# Almost-all route: state at pause (2026-11-16)

**A303656: UNRESOLVED.** There is no general proof and no certified
counterexample. Work is paused again after two research waves in November 2026.
This note records where the almost-all route stands, what is solid and what is
not, where it is stuck, and where a restart should begin. It is a handoff
document. It adds no new theorem, and the frozen authority is unchanged.

Everything below rests on AI-produced and AI-refereed arguments plus exact
programs. No human mathematician has reviewed any of it.

## 1. The chain in one page

Notation: `R(n)` counts exponent pairs `(c,d)` with `n − 3^c − 5^d` a sum of two
squares. `f_q` is the finite eventual-power local density profile and `f_∞` its
profinite limit. LP means `f_q(a) > 0` for every `q` and `a`. POS means
`f_∞ > 0` Haar-almost everywhere.

| Step | Statement | Source | Review status |
|---|---|---|---|
| V | `limsup X⁻¹ #{n ∈ [X,2X] : R(n) = 0} ≤ Haar{f_∞ = 0}`, hence POS ⇒ almost-all | [triage wave](../analysis/triage_wave_2026_11_14/README.md) | candidate, AI-refereed |
| A2 | `{f_∞ = 0} = ∪_q {f_q = 0}` a.e., hence POS ⇔ LP | triage wave | candidate, AI-refereed |
| ACP | a finite zero exists iff some parity class is covered by inert fibres `{3^α + 5^β ≡ z_p mod p}` in the pretend model | [ACP wave](../analysis/acp_wave2_2026_11_16/README.md) | candidate, AI-derived |
| C22 / R(146) | a zero needs at least 23 (C22), resp. 147 (R(146), conditional on C21's (H1)/(H2)), distinct joint-nonregular primes `p ≡ 3 mod 4` with `p² ∣ q`; the Haar-only conservative version gives 30 | triage wave, ACP wave | finite budgets machine-checked; framework AI-refereed |
| Fact | a joint-nonregular prime (`3^{p−1} ≡ 5^{p−1} ≡ 1 mod p²`) is a base-3 Wieferich prime; only 11 and 1006003 are known (none else below `9.7·10¹⁴`), and neither is base-5 Wieferich | [OEIS A014127](https://oeis.org/A014127), repo checks | verified for the named primes |

**Conditional almost-all theorem (synthesis, not separately refereed).** If at
most 22 primes `p ≡ 3 mod 4` satisfy `3^{p−1} ≡ 5^{p−1} ≡ 1 (mod p²)`, then
`#{n ≤ X : R(n) = 0} = o(X)`. With R(146) the bound 22 becomes 146. The
hypothesis is unproved, but no such prime is known at all, and the heuristic
expected number above `10¹⁵` is of order `10⁻¹⁶`.

## 2. Where it is stuck

### Every n (the conjecture itself): a tool barrier

For a fixed `n` there are only `Θ((log n)²)` residuals `n − 3^c − 5^d`. Sieve,
circle-method and second-moment arguments all average over `n` and do not reach
a single `n`. The repository's closed routes (N-001 to N-010, PF-N-001 to
PF-N-004, the L5,3 lemma) record where each pointwise attempt fails. Comparable
"sparse set plus sums of two squares, for every n" statements appear to be open
in general. A restart here needs a new pointwise tool, not more sessions.

### Almost-all: an explicit two-parameter covering problem

The open part of the almost-all route is one combinatorial number theory
question (the ACP, statement (N)):

> **Open question.** Fix a parity class `(c1, c2) ∈ {0,1}²`. Do there exist
> finitely many distinct primes `p_1, …, p_k > 3`, all `≡ 3 mod 4`, and residues
> `z_i mod p_i`, such that for every pair `(a, b)` of non-negative integers some
> `i` satisfies `3^{c1}·9^a + 5^{c2}·25^b ≡ z_i (mod p_i)`?
>
> If the answer is "no" for every parity class not excluded by the 2-adic and
> prime-3 conditions, LP holds, and with A2 and V almost all `n` are
> representable unconditionally. Equivalently (by CRT): is there an integer `Z`
> such that `Z − 3^α − 5^β` is divisible by one of finitely many primes
> `≡ 3 mod 4` for all `α, β` in a parity class?

What is known about it (candidate results):

- Any covering needs at least 147 primes, including one with `H_p ≥ 16384`.
- Proposition H: fractional coverings exist, so union bounds, LP duals and any
  measure certificate cannot prove "no". A proof must use integrality: each
  prime contributes exactly one residue.
- A single line (fix `α`, vary `β`) can be covered (18 inert primes); the
  obstruction, if any, is two-dimensional.
- Theorem F: at a fresh `M`-fibre, an exact tiling by `M` traces forces `M`
  parallel lines of one type, and the tiling then lives only on a set of lower
  points of measure at most `1/m_p`; the rest must be covered by the lower
  system, which reproduces the problem at smaller order primes.

My assessment (heuristic, not a theorem): the evidence leans toward "no", but
this has the flavour of Erdős-type covering questions in two exponential
parameters, and I do not know of a theorem that decides such questions.

## 3. What not to redo

- **Raising root thresholds** (23 → 147 → …). Proposition H caps every
  measure-based budget below a finite horizon; this cannot reach LP. Since no
  joint-nonregular prime is known, larger thresholds also add little in practice.
- **Pointwise every-n attacks** with averaging tools, and every route listed as
  closed in the theorem index or the post-freeze index.
- **Searching for real joint-Wieferich primes** as a counterexample strategy.
  Even (Y) would need many of them, and none is known below `9.7·10¹⁴`.

## 4. Restart points, in recommended order

1. **Human review** before any new mathematics. Priority:
   (i) the A2 zero-set theorem, the deepest step (Pomerance–Shparlinski range,
   conditional Paley–Zygmund, local constancy);
   (ii) the C21 framework, (H1) rigidity and (H2) regular averaging, and the
   completeness of Theorem R's direct budgets;
   (iii) the V weighted transfer, which is closer to standard technique.
   One expert confirmation would be worth more than further AI waves.
2. **Literature check** (leads, not verified here):
   - two-parameter covering congruences of Erdős type, for example whether the
     analogous question for `p + 2^a + 2^b` has a covering, and work of Crocker
     and later authors on integers not of that form;
   - bounds for the number of solutions of `x + y = z` with `x, y` in
     multiplicative subgroups or their cosets (Stepanov's method; Garcia–Voloch;
     Heath-Brown–Konyagin). These bear on the conjectured bound below. Check
     exact statements and constants in the sources before using them.
   If the analogous two-parameter covering questions are recognised open
   problems, the almost-all route has reached its natural end, and the right
   output is a write-up of the conditional theorem plus Proposition H.
3. **Integrality descent.** Turn Theorem F's recursion into a descent over
   order primes. A first target is the producer's conjecture that a type-B
   curve (both orders divisible by `M`) has at most `(M+1)/2` points on a fresh
   `M`-fibre. Lemma L4 proves only `M − 2` in the same-coset case.
4. **Write-up.** A short note: the conditional almost-all theorem, Proposition H
   (why measure methods stop), and the open covering question in section 2.

## 5. How the work was done (for reproducibility)

- Wave 1 (2026-11-11 to 11-14): parallel GPT web Pro sessions, one lane each,
  each ending with a fixed result card; independent referee sessions; one triage
  session. Integrated in PR #49.
- Wave 2 (2026-11-16): one Claude session (reported as Claude Fable 5.2) on the
  dichotomy, with exact certificates and a one-command replay.
- What worked: one sharp reformulation (almost-all as local positivity on `Ẑ`)
  followed by focused attack. Breadth across many routes, earlier in the
  project, produced mostly no-go results.
- All prompts used are kept in [`docs/research_prompts/`](research_prompts/README.md),
  so a restart can reuse them.
