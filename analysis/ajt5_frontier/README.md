# Round 5 · support of complete AJT5 and EMPTY_D explanations

**A303656 and unrestricted AJT5 remain UNRESOLVED.** For every parent m≥2 and digit r=0,…,4, a complete explanation of actual NO_BRIDGE requires **at least 16 distinct inert primes**, or **at least 25 if the explanation excludes 3**. A complete EMPTY_D explanation for any x≥2 independently requires **at least 17**. Existence of any such complete explanation remains open.

An inert prime is a prime congruent to 3 modulo 4. Write D(x) for the exponents d≥0 such that x=a²+b²+3ᶜ+5ᵈ for nonnegative integers a,b,c. An actual bridge uses d∈D(m) and e∈D(5m+r) with e=d or d+1. An explanation for a negative column must exhibit an odd inert valuation for every active c in that column. The support counts the union of the explanatory primes across the complete certificate. A positive row, including a zero residual, cannot be killed by such a prime.

| Scope | Independently checked result |
|---|---|
| Complete NO_BRIDGE, 3 allowed | Budget 15 excluded across all five digits and all 256 parent directions per digit. The large-m proof uses the short d=7 parent column and child c≤13. [Proof](global.md) |
| Complete NO_BRIDGE, 3 excluded | Budget 24 excluded. The nonempty directions reduce to 565 closed systems. Each empty direction uses the base plus one parent tail and, separately, the base plus one child tail. The verified parent tail is P(8,1). An explicit 24-prime integer blocks the proposed substitute P(8,0) together with the base. [Proof and control](global.md) |
| Complete EMPTY_D | Budget 16 excluded. Every x from 2 through 547066 is represented. Above that boundary 103 labels give 102 distinct roots, with all 622 non-3 multiroot primes accounted for. The exact 3-adic and default branches give 46 leaves. [Proof](empty.md) |
| Fixed W0/W1 windows at r=4 | The minimum support over m≥T, T≥255273, rises from 15 to 16 upon adding child row (0,11), root 177144. A fresh 249-bit W0 integer has a genuine 0→0 edge first realized at child c=11. [Witness and proof](low.md) |
| R4 low-parent window | The frozen integer with a 23-prime cover of its low parent rows has a genuine bridge for every child digit. All five square identities are checked. [Coordinates and local screens](controls.md) |
| Concrete certificate CLI | Bad source or invalid input gives JSON INVALID/2, a valid refutation gives REFUTED/1, resource failure gives UNKNOWN_RESOURCE/4. Missing coverage remains PARTIAL/3. [Input contract and tests](checker.md) |

## Finite boundary

The strict large-m cutoff is m=547067. At m=547066 the parent row (6,12) has residual zero. The original square-pair and valuation programs were both rerun at the unchanged boundary. They agreed at all 2,735,335 entries of S2, T and D and recounted 2,735,325 pairs. The little-endian uint16 D digest was `4ddb8029360990b2bfb2fd551ca010d896c78f927e1b45786ef85333a445be24`. The R4 bounded bridge replay found no misses with d≤7 and child c≤13.

For the no-3 route the [finite verifier](finite.py) sieves positive residuals having **no divisor** p≡3 mod 4 other than 3. Through the same endpoint every m≥3 and digit has adjacent rows with both residuals in this stricter set, d,e≤8 and c,c′≤12. The indicator bytes through 2,735,334 have SHA-256 `78c72a93a411f6787f3959c18caf4489e7a9ede451c3b2037f1467a77c8b188b`. At m=2 the parent identity is 2=0²+0²+1+1. For r=0,…,4, the child e=0 uses c′=(0,0,0,1,1) with square pairs (2,2), (0,3), (1,3), (0,3), (1,3). This finite computation and the J7 proof use their respective windows. The standalone uniform C10 rectangle is outside this verification.

## Reproduction

From the repository root run the following commands. The proof files contain integers. Verification needs Python's standard library. Optional search used SciPy 1.17.0. Each linked proof description gives its generation command. See [SHA256SUMS](SHA256SUMS) for the fresh certificate and control bytes.

```sh
(cd analysis/ajt5_frontier && sha256sum -c SHA256SUMS)
python3 -O analysis/ajt5_frontier/global_verify.py
python3 -O analysis/ajt5_frontier/empty_verify.py
python3 -O analysis/ajt5_frontier/finite.py
python3 -O analysis/ajt5_frontier/low_verify.py
python3 -O analysis/ajt5_frontier/controls.py
python3 -O analysis/ajt5_frontier/test_proofs.py
python3 -O analysis/ajt5_frontier/test_checker_cli.py
python3 scripts/check_ajt5_integer_boundary.py
```

To repeat the independent entry-by-entry finite comparison with a C++17 compiler, use a new temporary directory.

```sh
out=$(mktemp -d)
g++ -std=c++17 -O3 src/ajt5_scan.cpp -o "$out/scan"
g++ -std=c++17 -O3 src/ajt5_valuation_replay.cpp -o "$out/valuation"
"$out/scan" 547066 "$out/squares"
"$out/valuation" 547066 "$out/squares" "$out/valuation_tables"
sha256sum "$out/squares/masks.u16le"
```

## Five-round pathway and remaining questions

| Round | What carries forward |
|---|---|
| [1 · exact replay](https://github.com/Samsen879/a303656/pull/51) | Two implementations compared the bounded bridge search. The literal second counting gate left two cases. |
| [2 · sufficient gates](https://github.com/Samsen879/a303656/pull/52) | Parity and certified residue gates supplied reusable positive certificates. An unsuccessful gate leaves the edge question open. |
| [3 · row-local ablation](https://github.com/Samsen879/a303656/pull/53) | Exact row-local deletions and child negatives exposed the limits of sufficient evidence. |
| [4 · integer certificates](https://github.com/Samsen879/a303656/pull/54) | Full-column checks, exact unitary divisors and the finite endpoint excluded complete-support budgets 14 and 23 without 3. |
| [5 · prime support](global.md) | The two complete NO_BRIDGE lower bounds increase by one. EMPTY_D has its own separate bound. |

These are fresh repository-native proofs based on the public R4 head `c9062069297d5250541720c0ad1470104c51ee5f`. The original study ZIPs were unavailable for byte-level replay. The regenerated budget-15 proof matches both published documentary SHA-256 values, for the gzip file and the decompressed integer stream. The EMPTY_D digest in SHA256SUMS identifies a separately generated proof. The new integer proofs, tests and square identities establish the entries above independently. The original 249-decimal-digit W0 example's square coordinates, the original fixed-window 17/no-3 24 witnesses, Gaussian/Pell families, position inequalities, analytic results and the conditional ACP p=163 result have no independent acceptance claim here. This work draws no AJT5 conclusion from ACP.

One proposed next target is the **16-prime NO_BRIDGE frontier**. Start with a verified finite 16-prime cover and test whether a single palette covers every active row of a candidate negative column at the same integer. A surviving row should be tested for an actual square identity before treating it as a bridge. This is a research question. The five-round campaign ends here.
