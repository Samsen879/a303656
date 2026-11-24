# A uniform exclusion of 16-prime AJT5 explanations

**Result.** For every m≥2, r∈{0,1,2,3,4} and set Q of at most 16 distinct primes congruent to 3 modulo 4, some adjacent pair of active parent and child residuals both survive Q. Consequently no one such Q can explain enough complete negative columns to certify actual NO_BRIDGE, even if a genuine parent seed is supplied. A complete explanation would require **at least 17 distinct inert primes**, or **at least 25 without 3** by the pinned R5 proof. Attainability of these bounds, unrestricted AJT5, and A303656 remain open. No new conclusion about EMPTY_D follows.

Here an active row for y has R=y−5ᵈ−3ᶜ≥0. It survives Q if R=0 or every p∈Q has even valuation in R. Two square witnesses give an actual bridge, including at zero. Two palette survivors alone leave the square question open. The dependency order is [R1 finite replay](https://github.com/Samsen879/a303656/pull/51), [R2 sufficient gates](https://github.com/Samsen879/a303656/pull/52), [R3 ablation](https://github.com/Samsen879/a303656/pull/53), [R4 integer certificates](https://github.com/Samsen879/a303656/pull/54), [R5 support bounds](https://github.com/Samsen879/a303656/pull/55), then this 16-prime exclusion. The [dependency manifest](upstream.json) pins the R5 inputs at commit `8122d1d9b9d3f6cdcd2c4829bfa5a2965087d5d4`.

## What proves the exclusion

1. The no-3 integer proof from R5 replays with a budget of 24 non-3 primes. For the new case, put 3 in Q and allow 15 other primes. Write x=5m. Parent roots are K=5(5ᵈ+3ᶜ), child roots K=5ᵉ+3ᶜ−r. Multiplication by 5 preserves every inert valuation.
2. For one fixed (m,r,Q), let A contain each d≤7 with **any** surviving active parent row. If there is no surviving edge, every active parent row outside A, and every active child row at e∈A∪(A+1), must be killed by this same Q. These alternatives include the empty A. Fill A with every j≤7 whose two target indices already belong to that child set. This leaves child obligations unchanged and deletes some parent obligations. The verifier regenerates and checks inclusion for all 5×256 directions at each window level. There are 114 closed masks per digit.
3. At 1,018 of the 1,710 closed-direction/mod-3 cases, integer weights from R5 already suffice at the increased budget. In the other 692 cases split x modulo 27 into all nine children of its mod-3 class. Roots with x−K a 3-unit or congruent to 9 or 18 mod 27 certainly survive 3. Removing every other root allows more coverage, including some even valuations at depths ≥4. Every actual assignment for one integer is included. After this split, try the R5 rows first and add higher rows only when the proposed integer bound fails. No floating-point decision is used in replay.

| Level | Obligated parent columns outside A | Obligated child columns | New mod-27 leaves |
|---|---|---|---:|
| 0 | c≤12 except d=7 stops at 11 | c≤13 | 6,146 |
| 1 | c≤12 | c≤14 | 33 |
| 2 | c≤13 | c≤15 | 47 |
| 3 | c≤14 | c≤16 | 2 |

4. For distinct live roots a,b, any non-3 prime hitting both divides |a−b|. The integer verifier independently factors the differences and reconstructs all multiroot prime/residue classes. For one actual m, each selected prime has only one possible residue x mod p. Replacing its odd-valuation hits by the entire residue class relaxes coverage. A prime outside the catalogue can cover at most one root. At a leaf, integer weights w(K)∈[0,S] give a maximum covered weight of 15S+Σzₚ, where zₚ=max(0, largest p-class weight−S). This includes singleton uses. If Σw is strictly greater, no actual choice of 15 primes or CRT residues works. All **7,246 leaves** pass with **zero** non-3 prime branches. The smallest normalized excess is **2051/500000**. At r=1, A={4}, x≡4 mod 27, the 57 weights sum to 20,847,143 at scale 1,000,000 and total penalty 5,843,041. The strict excess is 4,102.
5. The largest root in any window actually used is 43,049,845. Every obligation is strictly positive for **m≥8,609,970**. The two frozen R1 engines were rerun over their original 2≤m≤10,000,000 domain. Independent square enumeration and valuation arithmetic agreed on all 50,000,005 S2, T and D entries. All 49,999,995 parent/digit pairs had actual bridges. This covers the boundary, including zero residuals, without extending the published m range. The leaf proof handles arbitrarily large m.

The bound is uniform over Q and m. For a hypothetical actual NO_BRIDGE at fixed m,r, a finite upper bound on its required support is the total number of active rows of m and 5m+r combined: each row of a truly negative column has an odd inert factor by the two-square theorem. This upper bound varies with m. The computation establishes no uniform upper bound on support, and 17 is a necessary condition.

## Integer countercontrol

The pinned R5 repository supplies a W1 CRT cover using 16 primes but no positive W1 square seed. The earlier study's original square fixture was unavailable here. Starting from the pinned W0 control, the construction preserves a witnessed valuation h by fixing the integer modulo pʰ⁺¹ for every used prime, and imposes x≡177144+47 mod 47² at the extra W1 child row. A search of **433 translates of this one progression** found the [263-bit control](control.json) with a genuine parent seed and child square witness.

All 107 W1 labels are covered by the same 16 primes. Over the full active range the palette completely blocks 21 of 113 parent columns and 23 of 114 child columns. There are 157 surviving exponent edges. At parent column zero the first survivor is c=1; at child column zero it is c=12. Both survivors have exact square identities. Supplying all supported negative atoms and both positive witnesses to the R5 checker gives **REFUTED/1, edge 0→0**. With only the parent witness it gives **PARTIAL/3**. This refutes the inference from W1 coverage to actual NO_BRIDGE.

| Fixed negative obligations | First uncovered exponent using this Q |
|---|---|
| Parent d=1,2,3,4,5,7 | Fully covered, 10, fully covered, 13, fully covered, fully covered |
| Child e=0,1,6,7 | 12, fully covered, 12, fully covered |

## Reproduction and cost

From the root of this checkout, run the commands below with Python 3.12 and a C++17 compiler available as g++. Acceptance reads the [complete gzip-compressed JSONL proof](proof.jsonl.gz) and the hash-checked R5 inputs directly from this repository. It runs offline with the Python standard library and compiler.

```sh
cd analysis/ajt5_budget16
sha256sum -c SHA256SUMS
python3 -O accept.py
```

The command replays the new integer certificates, the no-3 proof, the two finite engines, the full control through the concrete CLI, and five adversarial tests. Tests cover a non-strict leaf, malformed weights, missing residues, the free default, false CRT steps, duplicate palette members and false square coordinates. An optional A303656_REPO environment variable can point to a checkout containing the pinned inputs. Compare the resulting counts, hashes and verdict with [receipt.json](receipt.json). Timing fields vary by host.

To regenerate the discoveries, install SciPy and SymPy (discovery used 1.17.0 and 1.14.0 respectively). Record both generation and checking time. Alternative LP optima can produce different valid integer proofs.

```sh
OPENBLAS_NUM_THREADS=1 python3 discover.py regenerated.jsonl.gz
python3 -O replay.py regenerated.jsonl.gz
python3 control_search.py
python3 -O check_control.py
```

The initial proof search took 278.5 seconds. Full acceptance against the checkout took 57.6 seconds, including the new integer replay, no-3 replay and the original finite search. The offline replay used the same pinned inputs. The compressed certificate has SHA-256 `c115aa8aad404ffbb25419ccabef817ad0e0f547393c4df40253d6b2407a9957`.

**Next leverage point.** If investigating budget 17 separately, start with r=1, A={4}, x≡4 mod 27. The displayed strict inequality stops excluding coverage when the non-3 budget rises from 15 to 16. Testing exact prime-power compatibility there would distinguish an actual CRT cover of those finite rows from a limitation of this particular weight vector. No budget-17 search was run.
