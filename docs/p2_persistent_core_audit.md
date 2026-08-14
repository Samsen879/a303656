# P2-persistent obstruction core and control audit

## Technical summary

This selected-fixture audit separates static odd valuations from exact
valuation one.  It is an **EXACT FINITE COMPUTATION ON FIXED SELECTED
FIXTURES**; the core orderings are explicitly **HEURISTIC_P2_PERSISTENT_CORE**
constructions and are not minimum set covers.  The global A303656 problem
remains **UNRESOLVED**.

Reusable source commit is `f141f9f3786480b06609fed099aa4c8ffbfee39e` with parent `6e357619ee9309819aeb36caf0f1f3f974b4c0fb`.  The results commit is the Git commit
containing this generated report and is resolved explicitly during replay.
All declared dossier, pilot, and certified-baseline hashes passed before
analysis.  No counting executable, new integer scan, CRT solve, arithmetic
progression search, or T-evaluation at progression candidates was performed.

## Prime 3: 167 static pairs but only 143 p2-persistent pairs

For `n0=240000005594`, the exact valuation distribution is `{'0': 214, '1': 143, '2': 26, '3': 23, '5': 1}`.
Therefore prime 3 covers 167 pairs statically, 143 pairs persistently modulo
`3^2`, and 24 pairs have higher odd valuation and are excluded from the p2 core.

The modular explanation is exact.  `n0 ≡ 2 (mod 9)`.  For `c>=2`,
`3^c ≡ 0 (mod 9)`, while `5^d (mod 9)` cycles
`1,5,7,8,4,2` with period 6.  Thus `2-5^d` is divisible by 3 but
not by 9 exactly when `d ≡ 1 or 3 (mod 6)`, proving `v3=1` for
those pairs.  The `c=0` and `c=1` rows were evaluated separately by exact
division: `{'c=0': {'0': 8, '1': 6, '2': 2, '5': 1}, 'c=1': {'0': 9, '1': 5, '2': 2, '3': 1}, 'c>=2': {'0': 197, '1': 132, '2': 22, '3': 22}}`.

## Static and persistent definitions

For every fixture and prime `p ≡ 3 (mod 4)`, the audit reconstructs
`O_p={(c,d):v_p(r) odd}`, `C_p={(c,d):v_p(r)=1}`, and
`H_p={(c,d):v_p(r) odd and >=3}`.  It verifies `O_p=C_p disjoint-union H_p`
and checks every `C_p` pair directly modulo `p^2`.  Explicit pair sets,
separate rankings, both requested denominators, valuation-3/5/... splits,
and optional preserving moduli `p^(e+1)` are in
`analysis/p2_core/static_vs_p2_prime_coverage.csv`.

## Heuristic p2-persistent cores

The marginal ordering maximizes the exact number of newly covered pairs and
breaks ties by smaller prime.  The bit-cost ordering maximizes
`new/log2(p^2)`.  Scores are compared without floating point:
`a/log(p) > b/log(q)` iff `q^a > p^b`; an exact equality is broken by
smaller prime.

| ordering | k | covered active | covered losers | uncovered losers | M bits | M digits |
|---|---:|---:|---:|---:|---:|---:|
| MARGINAL_COVERAGE_GREEDY | 1 | 143/407 | 143/391 | 248 | 4 | 1 |
| MARGINAL_COVERAGE_GREEDY | 2 | 182/407 | 182/391 | 209 | 9 | 3 |
| MARGINAL_COVERAGE_GREEDY | 4 | 216/407 | 216/391 | 175 | 25 | 8 |
| MARGINAL_COVERAGE_GREEDY | 8 | 246/407 | 246/391 | 145 | 67 | 21 |
| MARGINAL_COVERAGE_GREEDY | 16 | 266/407 | 266/391 | 125 | 175 | 53 |
| MARGINAL_COVERAGE_GREEDY | 32 | 286/407 | 286/391 | 105 | 434 | 131 |
| COVERAGE_PER_MODULUS_BIT_GREEDY | 1 | 143/407 | 143/391 | 248 | 4 | 1 |
| COVERAGE_PER_MODULUS_BIT_GREEDY | 2 | 182/407 | 182/391 | 209 | 9 | 3 |
| COVERAGE_PER_MODULUS_BIT_GREEDY | 4 | 216/407 | 216/391 | 175 | 25 | 8 |
| COVERAGE_PER_MODULUS_BIT_GREEDY | 8 | 246/407 | 246/391 | 145 | 67 | 21 |
| COVERAGE_PER_MODULUS_BIT_GREEDY | 16 | 266/407 | 266/391 | 125 | 175 | 53 |
| COVERAGE_PER_MODULUS_BIT_GREEDY | 32 | 286/407 | 286/391 | 105 | 434 | 131 |

All 32 intermediate steps, selected primes, exact products, new pair sets,
and residue bindings `t_p=n0 mod p^2` are stored in the CSV/JSON outputs.
Every combined class is only `n ≡ n0 (mod M)`; no alternate CRT residue
was computed.

## Exact activation cell and candidate density

The maximal integer cell with the same 407 source pairs is `[183968950234,246731069451]`.
The next activation occurs at `246731069452`.  The sole
duplicate active shift is 28, supported by `(1,2)` and `(3,0)`, and both
source pairs remain present.  Counts of `n0+kM` in this cell and in
PILOT-B, plus the nearest nonzero k on each side when present, are purely
arithmetic density calculations in `activation_cell.json`; T was not
evaluated at any such point.

## Corrected controls and normalization

The previous controls matched modulo 120 only.  The corrected controls are
selected from the existing PILOT-B counts with modulus 360 and the same
fixed block/key rule.  Their selections are:

| low-tail n | corrected control | T(control) | selection key |
|---:|---:|---:|---|
| 240000005594 | 240000009194 | 46 | `(14, 3600, 240000009194)` |
| 240000004802 | 240000001202 | 50 | `(10, 3600, 240000001202)` |
| 240000044158 | 240000048838 | 55 | `(5, 4680, 240000048838)` |
| 240000000968 | 240000006368 | 47 | `(13, 5400, 240000006368)` |
| 240000001544 | 240000004064 | 47 | `(13, 2520, 240000004064)` |

Duplicate corrected controls: `[]`.
Equal residues modulo 9 give identical prime-3 p2-persistent pair sets
because all ten low/corrected fixtures have the same active domain; this
was also checked pair-for-pair.

Absolute and losing-pair-normalized obstruction-prime counts, signature
counts, p2-prime counts, prime-3 static/p2 coverage, and frequency-ranked
top-k p2 union coverage are in `normalized_comparison.json`.  The audit
records each prior qualitative statement as surviving all five pairs,
surviving partially, or not surviving after normalization/modulo-9 matching.
Every comparison is only a **COMPUTATIONAL OBSERVATION ON SELECTED FIXTURES**.

## Higher odd valuations and limitations

Pairs of valuation 3, 5, and higher are reported separately and never enter
p2-core totals.  The optional `p^(e+1)` values are labeled
**HIGHER_PRIME_POWER_OBSERVATION**.  They are not mixed into M.

This audit does not prove a counterexample, a minimum core, a useful CRT
class outside the activation cell, or any infinite statement.  It does not
evaluate whether the uncovered pairs can be eliminated simultaneously.

## Corrections found by this audit

1. The earlier all-odd-valuation top-k tables are static obstruction
   tables, not p2-persistent coverage.  At n0, prime 3 changes from
   167 static pairs to 143 persistent pairs; the omitted 24 pairs have
   valuation 3 or 5.
2. The old controls were matched modulo 120, which does not bind modulo
   9.  With corrected modulo-360 controls, prime-3 p2 coverage is exactly
   equal within every matched pair, so a strict low-tail advantage for
   prime-3 p2 coverage does not survive.
3. The old absolute advantages in distinct obstruction primes, signature
   diversity, and p2-prime counts survive for all five pairs, but each
   survives only partially after division by losing-pair count.  The same
   partial result holds for the corrected controls.
4. Frequency-ranked top-k p2 union comparisons depend on k and denominator;
   they are recorded per pair rather than summarized as a universal
   concentration claim.

## Independent verification

`src/verify_p2_persistent_core.py` imports no primary analysis module.  It
independently checks the active domain, factor products/primality and direct
valuations, the mandatory prime-3 distribution, every C_p congruence, both
greedy histories, corrected controls, activation endpoints, modulus sizes,
normalization, and input/baseline hashes.  Its result is stored in
`analysis/p2_core/verification_report.json`.

## Conclusion

**VALIDATED P2-PERSISTENT CORE AUDIT**
