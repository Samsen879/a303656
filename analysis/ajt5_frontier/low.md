# One child row changes the minimum covering support

Fix digit 4 and the short-window direction A={0,6} (mask 65). Write x=5m. Use the parent root 5(5^d+3^c) and child root 5^e+3^c−4. Define W0 by the following negative obligations.

| Side | Column | c |
|---|---|---|
| Parent | 1, 2, 3, 4, 5 | 0…9 |
| Parent | 7 | 0…11 |
| Child | 0, 1, 6, 7 | 0…10 |

W0 has 106 labels on 105 roots. W1 adds child (0,11), root 177144, for 106 distinct roots. All these residuals are strictly positive for m≥255273. A palette covers a root K at m if x−K has odd valuation at one of its distinct primes p≡3 (mod 4). Multiplication of a parent residual by 5 preserves each such valuation.

**For each T≥255273, the minimum palette size over all m≥T is 15 for W0 and 16 for W1.** Each minimum permits m and the palette to vary. Neither statement requires the true parent D(m) to equal A.

The W1 proof separately tests omission of 3 with budget 15 and every residue of x modulo 27 with remaining budget 14. At a given residue the roots whose difference is a unit modulo 3 or has valuation exactly two must all survive 3. Discarding every other root relaxes the cover. The R4 standard-library verifier checks integer weights and strict inequalities for these survivors, recomputing the complete difference-prime catalogue, all multi-root classes, and the free default branch. The 28 cases use 2 branching nodes and 42 integer leaves. At x≡4 modulo 27, the split on 7 has its default and all seven classes. This proves the lower bound 16 for W1.

A W0 cover of size at most 14 would give a W1 cover of size at most 15 at a possibly different integer. For each W0 row preserve one witnessing odd valuation h at its prime p by fixing m modulo p^(h+1), taking the largest required exponent for each p. Choose any fresh inert prime q. Also impose 5m≡177144+q modulo q². CRT gives arbitrarily large consistent m, contradicting the W1 bound. This proves the W0 lower bound.

The [fresh integer control](low_control.json) gives an actual 249-bit m and 15 primes. The [replay](low_verify.py) verifies 106 negative atoms, two square identities, and the three screened column sets below. These are membership tests for the indicated palette.

| Scope | Surviving columns |
|---|---|
| Parent d≤7, c≤9 | {0,6} |
| Child e≤8, c≤10 | {2,3,4,8} |
| Parent d≤7, c≤12 | {0,2,6} |

The control has a genuine 0→0 edge. Its first parent square representation at d=0 uses c=1. Its first child representation at e=0 uses c=11. The checker returns REFUTED with these two identities and the negative prefix, and PARTIAL after removal of the child identity. To construct this example, a residue cover for W0 was lifted modulo prime powers, then integer translates were tested for the two square identities. Only direct integer checks on the recorded coordinates enter acceptance.

The replay preserves the W0 valuations, imposes the extra residue at q=47, and checks every W1 row again at the resulting m with 16 primes. Each exhibited cover repeats at arbitrarily large m by the same prime-power congruences. Square identities are asserted only for the recorded W0 example.

From the repository root, run:

```sh
python3 -O analysis/ajt5_frontier/low_verify.py
```

Optional SciPy regeneration writes to a new output path:

```sh
proof_dir=$(mktemp -d)
python3 analysis/ajt5_frontier/low_generate.py "$proof_dir/w1.jsonl"
```

The [proof stream](low_w1.jsonl) is generated independently of the study archive. This finite projection and its exact costs give no complete NO_BRIDGE certificate.
