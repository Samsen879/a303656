# Selected PILOT-B obstruction dossier

Task: **SELECTED PILOT-B OBSTRUCTION DOSSIER**

Classification: **INDEPENDENTLY VERIFIED EXACT FINITE COMPUTATION ON FIXED
SELECTED FIXTURES**.

This computation does not scan a new interval.  It reads the existing
three-way validated PILOT-B `counts.csv`, processes ten fixed integers, and
does not run a T(n) counting executable, broad mining, CRT search, or set-cover
solver.  Every comparison below is a **COMPUTATIONAL OBSERVATION ON SELECTED
FIXTURES** and has no claimed global statistical significance.  The global
A303656 problem remains **UNRESOLVED**.

## Fixed panels and mechanical controls

The five low-tail values are unchanged:

| low-tail n | validated T | matched control m | validated T(m) | selection key `(|T-60|,|m-n|,m)` |
|---:|---:|---:|---:|---|
| 240000005594 | 16 | 240000002114 | 50 | `(10,3480,240000002114)` |
| 240000004802 | 18 | 240000003122 | 53 | `(7,1680,240000003122)` |
| 240000044158 | 19 | 240000048838 | 55 | `(5,4680,240000048838)` |
| 240000000968 | 20 | 240000000728 | 58 | `(2,240,240000000728)` |
| 240000001544 | 21 | 240000003584 | 53 | `(7,2040,240000003584)` |

The block subdivision is anchored at PILOT-B's fixed lower endpoint
`240000000001`, with width 10,000.  Eligible controls have the same residue
modulo 120 and exclude every low-tail member.  The three existing PILOT-B
count arrays were byte-identical at SHA256
`2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773`.
All five selected controls are distinct.

## Exact active domain

For every selected n, exact repeated integer multiplication gives 407 active
exponent pairs, 406 distinct numerical shifts, maximum `c=23`, and maximum
`d=16`.  The sole duplicate numerical shift is

```text
3^1 + 5^2 = 28 = 3^3 + 5^0.
```

Both source pairs remain separate records.  Independent verification confirms
that their remainder, classification, complete factorization, and obstruction
signature agree for every selected n.  Winner totals reproduce all ten
validated T values exactly: `16,18,19,20,21,50,53,55,58,53`.

## Complete-factorization and primality contract

The primary generator is `src/generate_obstruction_dossier.py`.  For every
positive remainder it constructs an exact Eratosthenes prime table through
the integer square root, performs complete trial division, and proves that
the ordered positive prime powers reconstruct the remainder.  Every reported
factor is additionally checked with the deterministic Miller--Rabin basis set

```text
2, 325, 9375, 28178, 450775, 9780504, 1795265022
```

which is valid for all unsigned 64-bit inputs.  Thus `PROVEN_PRIME` in this
finite contract means deterministic-for-uint64, not probable-prime-only.

The independent verifier is `src/verify_obstruction_dossier.py`.  It imports
no generator code.  It builds a separately coded odd-index prime sieve,
refactors every positive remainder from scratch, and verifies reported factors
with the independent deterministic bases

```text
2, 3, 5, 7, 11, 13, 17
```

under the proven bound `r < 240000100001 < 341550071728321`.  It separately
checks factor order, positive exponents, product reconstruction, congruence
modulo 4, valuation parity, Fermat's two-square classification, witness
equations, and canonicality by exhausting every smaller admissible `a`.
Remainder zero is handled separately and is never factored or passed to
Fermat's positive-integer criterion.

## Obstruction concentration

Top-k primes are ranked by descending all-obstruction losing-pair frequency,
then ascending prime.  A losing pair is covered once if its full obstruction
signature intersects the selected top-k set; it is never multiply counted.

| n | T | losers | distinct obstruction primes | signature diversity | top-1 | top-2 | top-4 | top-8 | top-16 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 240000005594 | 16 | 391 | 348 | 319 | 167/391 | 205/391 | 235/391 | 264/391 | 279/391 |
| 240000004802 | 18 | 389 | 345 | 332 | 166/389 | 199/389 | 238/389 | 261/389 | 277/389 |
| 240000044158 | 19 | 388 | 324 | 312 | 158/388 | 196/388 | 235/388 | 263/388 | 278/388 |
| 240000000968 | 20 | 387 | 343 | 320 | 165/387 | 202/387 | 228/387 | 250/387 | 268/387 |
| 240000001544 | 21 | 386 | 344 | 321 | 166/386 | 195/386 | 229/386 | 252/386 | 268/386 |
| 240000002114 | 50 | 357 | 312 | 312 | 125/357 | 154/357 | 189/357 | 214/357 | 231/357 |
| 240000003122 | 53 | 354 | 328 | 310 | 125/354 | 153/354 | 182/354 | 205/354 | 227/354 |
| 240000048838 | 55 | 352 | 317 | 294 | 139/352 | 173/352 | 193/352 | 215/352 | 230/352 |
| 240000000728 | 58 | 349 | 325 | 296 | 127/349 | 155/349 | 189/349 | 214/349 | 234/349 |
| 240000003584 | 53 | 354 | 293 | 282 | 145/354 | 183/354 | 201/354 | 223/354 | 246/354 |

Prime 3 is the largest single-prime cover in every selected fixture.  Its
coverage is about 40.7--43.0% in the five low-tail fixtures and about
35.0--41.0% in their controls.  These selected differences are descriptive,
not a population estimate or significance claim.  Complete canonical/all-prime
frequencies, obstruction-count distributions, signature frequencies, and
winner `c`, `d`, and shift distributions are in the machine artifacts.

## n0 surviving pairs

For `n0=240000005594`, 16 of 407 exponent pairs are winners.  Among its 391
losers, the primes meeting the predeclared 5% coverage threshold are:

```text
3: 167/391
7:  51/391
11: 47/391
23: 20/391
```

`analysis/obstruction_dossier/n0_surviving_pairs.json` contains all 16 winner
pairs, their complete remainder factorizations, canonical witnesses, and the
remainder residue modulo each of these four primes.  It is only a residue
table: no CRT was solved, n0 was not modified, and no simultaneous elimination
of its winners is claimed.

## Regression-only fixtures

The integers `2,3,5,25` are stored inside `panel.json` with
`purpose=SCHEMA_REGRESSION_ONLY`.  Their active-pair counts are `1,1,2,6`, and
each has exactly one winner.  The n=2 row exercises remainder zero and the
canonical witness `(0,0)`.  These records do not enter any PILOT-B frequency,
coverage, or comparison statistic.

## Artifacts and conclusion

The compact dataset is under `analysis/obstruction_dossier/`.  It contains
4,070 research records: 363 winners and 3,707 losers.  Every loser has at
least one independently verified prime congruent to 3 modulo 4 with odd
valuation; every winner has none.  No exact minimum-cover claim is made and no
greedy cover is reported.

The independently checkable result is:

> **VALIDATED SELECTED OBSTRUCTION DOSSIER**

The 26 raw command records (130 files) are outside Git in
`selected_obstruction_dossier_raw_logs_3a93ab744825780c14c58d177a5a8d97e887e1e2.tar.zst`,
SHA256 `27414cc35469b7153738ec1351b21b03a437ddc1b8646d523009927c5b3fec38`.
The checked-in `command_manifest.json` and `raw_log_archive.json` retain exact
return codes, stream hashes, sizes, and the archive creation command.
