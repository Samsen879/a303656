# Round 4 · integer AJT5 certificates

**A303656 and unrestricted AJT5 remain UNRESOLVED.** This research layer is based on draft [#53](https://github.com/Samsen879/a303656/pull/53) at `89040d540558994b8c90c9d3d03ff34edee9c91e`. All complete integer no-bridge certificates would require **at least 15 distinct inert primes** in a prime explanation of their negative endpoints, or **at least 24 if 3 is excluded**. The lower bounds follow from new, independently generated and checked finite proofs and the activation argument below. There is no known complete positive integer NO_BRIDGE fixture here.

| Scope | Outcome | Evidence |
|---|---|---|
| One supplied integer claim | Exact unitary-divisor verification for NO_BRIDGE and EMPTY_D | Strict [checker](../../src/ajt5_integer_certificates.py), [arithmetic and mutation tests](../../tests/ajt5_integer_tests.py) |
| All `2 ≤ m ≤ 547066`, all five digits | A genuine bridge in each of 2,735,325 pairs, zero empty parents | [Endpoint replay](../../scripts/check_ajt5_integer_boundary.py) and full D-table digest below |
| Every palette of at most 14 inert primes | A surviving edge with parent d≤6, parent c≤12, child c≤14. Independently, one with parent d≤7, parent c≤12, child c≤13 | Separate finite proofs and separate small endpoints |
| Every palette omitting 3, size ≤22 | A surviving edge with parent d≤6 and c≤12 on both sides | All 640 orientations and the small endpoint |
| Every palette omitting 3, size ≤23 | Exclusion of a complete blocking system, hence of a complete actual certificate with this support | All 1,280 orientations including both states of parent index 7 |
| Fixed parent box d≤6, c≤12, budget 23 without 3 | All 91 parent labels can be blocked. A higher genuine bridge exists at the example | Independently constructed [integer and palette](fixtures/no3_23_window.json) |
| General counterexample, constructive proof of Sun, attainable complete 15- or 24-prime certificate | Open | Neither bounded-window satisfiability nor palette survival gives this conclusion |

## Concrete integer submissions

Write `D(x) = {d : x = a²+b²+3^c+5^d}` with nonnegative integers a,b,c,d. The input is UTF-8 JSON with integer numeric tokens. Arrays are unordered evidence. A positive record is a single exact witness. A negative column is a collection of unitary divisors indexed by c.

```json
{"kind":"NO_BRIDGE","m":2,"r":0,"positive":[{"side":"parent","d":0,"c":0,"a":0,"b":0},{"side":"child","d":0,"c":0,"a":2,"b":2}],"negative":[]}
```

This submission is refuted by the edge 0→0. For NO_BRIDGE the checker derives n=5m+r with m≥2 and 0≤r≤4. For EMPTY_D, use `{"kind":"EMPTY_D","n":16,"positive":[],"negative":[{"side":"target","d":0,"units":[{"c":0,"u":7}]}]}`; this supplies partial evidence. In either format a negative column record has exactly the fields `side,d,units`. Each unit has exactly `c,u`. Numeric fields exclude booleans. Duplicate keys, repeated atom indices in one column, repeated columns, inactive indices, unknown fields, false identities and false divisors invalidate the submission, including evidence beyond anything needed for an early verdict. File size (8 MiB), integer size (4,096 bits) and nesting (64 levels) have explicit resource limits.

The checker derives every active d from `5^d+1 ≤ x` and every active c from `3^c ≤ x−5^d`. A negative endpoint requires verified atoms for **every** active c. Missing entries supply no information. For each active parent j, **both** edges (j,j) and (j,j+1) must have a negative endpoint. A no-bridge finding also needs an actual parent square witness. A child square witness then yields AJT5_ONLY_AT_CHILD. Complete negative coverage of the child gives SUN_FAILURE_AT_CHILD. With other evidence, the proved no-bridge result retains CHILD_EXISTENCE_UNKNOWN. A standalone EMPTY_D needs complete negative coverage at every active d for its own n>1.

| CLI exit | Outcome |
|---:|---|
| 0 | VERIFIED_NO_BRIDGE or VERIFIED_EMPTY_D |
| 1 | REFUTED by a witnessed edge, positive target or certified empty parent |
| 2 | INVALID submission or arithmetic |
| 3 | PARTIAL coverage or missing parent witness |
| 4 | UNKNOWN_RESOURCE |

**Unitary-divisor lemma.** For R>0, the two-square theorem says that a sum of two squares has even valuation at every prime p≡3 mod 4, and conversely. An odd valuation gives u equal to the full power of p in R. Then u≡3 mod 4 and gcd(u,R/u)=1. Conversely, if u>0 divides R, u≡3 mod 4 forces some p≡3 mod 4 to have odd valuation in u. Coprimality puts its entire power in u. The checker tests all three conditions using integers. It accepts a unit such as 15 for 60 and rejects 15 for 45. Distinct submitted divisors can use the same explanatory prime. Zero is represented by 0²+0² and has no negative certificate.

The [1339 mutant](fixtures/nonunitary_1339.json) has 48 positive residuals in six alleged negative columns. Exactly two fail coprimality. At child (2,2), 6664=42²+70² and 119 shares 7 with the quotient. At child (3,1), 6570=3²+81² and 15 shares 3. Both fake divisors have exact order one as composite bases. A weakened checker would certify no bridge. The literal square oracle finds **1→2, 2→2, 2→3, 3→3**. The tests also exhaust the three-valued edge algebra separately from arithmetic and compare all residuals from 0 through 1500 with literal square enumeration.

## Restricted prime palettes

An inert prime here means p≡3 mod 4. For a finite set Q of distinct such primes, a residual survives if it is zero, or is positive with even valuation at every p in Q. Let D(Q,C,x) contain d when some active c≤C survives. An actual square witness survives every Q. Each palette result quantifies **for every m≥2, every digit r and every permitted Q, there exists a surviving edge**. Its exponents may depend on all three. Its endpoints can fail to be actual representations. For example at m=16,r=3 both columns on 0→1 survive Q={3} while both columns lack actual representations. The two windows for size 14 have independent witnesses.

For large m, suppose a specified window has no surviving bridge. Orient the low parent indices by membership in D(Q,12,m). For every index outside that set, every selected active parent row must be killed. For every index inside it, all selected active child rows at e=d,d+1 must be killed. This argument includes an empty low parent set and requires no actual seed. A complete actual certificate explained by Q would cover all these edges with negative endpoints, precluding such a survivor. Choosing one odd inert divisor prime from each negative atom gives that implication for the unitary input language as well.

The [integer replay](../../src/verify_ajt5_palette.py) derives each direction and its labeled rows. At x=5m, the normalized roots are K=5(5^d+3^c) on the parent and K=5^e+3^c−r on the child. Every inert valuation of x−K agrees with the original residual, since 5 is a unit at these primes. Equal roots share one modular obligation, with all original labels retained. For example r=3, low membership {1} gives 104 labels on 103 roots, including two labels at 140. Negative roots are allowed.

| Proof | r, masks | Parent negative rows | Child negative rows | First m with all selected residuals positive |
|---|---:|---|---|---:|
| no3_22 | 5×128 | d≤6, c≤12 | e∈A∪(A+1), c≤12 | 547067 |
| no3_23 | 5×256 | d≤6, c≤12 plus d=7, c≤11 when 7∉A | e∈A∪(A+1), c≤12, including e=7,8 when 7∈A | 547067 |
| all14_d7 | 5×256 | Same parent rows as no3_23 | e∈A∪(A+1), c≤13 | 547067 |
| all14_d6 | 5×128 | d≤6, c≤12 | e∈A∪(A+1), c≤13 plus c=14 for e≤2 | 956599 |

In both 256-mask proofs, 7∈A is determined using the true active range and c≤12. If 7∉A, the proof uses only c≤11 at d=7. If 7∈A, both child columns 7 and 8 are obligated. Thus all subbranches of the split are covered, including when no lower parent bit survives. The checked J7 true branch with A={7} has 117 labels. This larger collection of directly active obligations yields a fresh proof without relying on a previously selected set of directions.

### How the integer exclusions work

1. A non-3 prime covering two distinct roots divides their nonzero difference. The verifier generates all candidate colors by full trial division of the pairwise differences of the root universe. For each such prime it groups the actual roots by their residues. Each prime can take only one residue class. All other primes cover at most one distinct root. Giving fresh singleton colors unlimited availability is a relaxation.
2. At a leaf of remaining budget b, the certificate gives an integer scale D>0 and weights in [0,D] in ascending live-root order. For each available prime take z to be the maximum of zero and the largest class weight minus D. Every selected class costs at most D+z in covered weight. Since a prime is paid at most once, b colors cover weight at most bD+Σz. A leaf passes only when Σweights−Σz>bD. A branch on p must contain **every** live class of size at least two plus the default. A selected class removes its roots and spends one. The default spends zero and permits singleton use via the relaxation. All children exclude p from future multi-root use.
3. With 3 available, the no-3 case uses budget 14. Using 3 leaves 13 non-3 colors. For each x modulo 3 the proof may remove all congruent roots, a conservative relaxation. Two residue classes in the d≤6 proof need finer coverage. Let H be the largest v₃ difference between distinct roots. The verifier enumerates representatives K+t·3^h for t=1,2 and h=0,…,H+2, and the roots themselves. Pick a nearest root, maximizing v₃(x−K). At depth ≤H the last matching digit fixes every valuation. Beyond H only this root's parity can vary, and H+1,H+2 realize both parities. Exact equality at a root preserves the zero residual. Thus every actual odd-valuation set lies in a regenerated maximal mask in the correct residue class. Each maximal mask requires a proof. An empty mask is covered by the full budget-14 proof. The search producer instead descends a ternary digit tree.
4. Each actual m has one residue at each prime. Allowing arbitrary choices among those classes, or removing more roots than their actual odd valuations, only enlarges the covering problem. No satisfiability or positive representation conclusion uses these relaxations. The finite exclusions apply to all larger m because the same labeled rows stay strictly active.

| Replay | Directions | Non-3 branch nodes | Integer leaves |
|---|---:|---:|---:|
| no3_22 | 640 | 160 | 1,858 |
| no3_23 | 1,280 | 127 | 2,228 |
| all14_d7 | 1,280 | 0 | 5,120 |
| all14_d6 | 640 | 15 | 2,679 |

The [proof search](../../scripts/generate_ajt5_palette_proofs.py) uses SciPy to propose a dual, quantizes it and emits integer data. The verifier imports no optimizer or search code. It rebuilds labels, roots, colors, 3-adic alternatives, tree state and strict inequalities. The compressed [proofs](proofs/) are generated integer certificates. The original research archives were unavailable for byte-level replay. These results come from fresh proofs of the stated conclusions.

### Activation and the finite endpoint

For each c below, parent columns show the first m with a nonnegative residual. Child columns show the first m with a **strictly positive** residual for every r at the named e. The latter equals floor((5^e+3^c)/5)+1. For any specific r, nonnegativity starts at ceil((5^e+3^c−r)/5). A boundary with equality contributes an actual square witness.

| c | 3^c | Parent d=3 | Parent d=6 | Parent d=7 | Child e=2 | Child e=7 | Child e=8 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 177147 | 177272 | 192772 | 255272 | 35435 | 51055 | 113555 |
| 12 | 531441 | 531566 | 547066 | 609566 | 106294 | 121914 | 184414 |
| 13 | 1594323 | 1594448 | 1609948 | 1672448 | 318870 | 334490 | 396990 |
| 14 | 4782969 | 4783094 | 4798594 | 4861094 | 956599 | 972219 | 1034719 |

At m=531565,531566,531567, parent d=3,c=12 gives −1,0,1. At m=531582 the [first twelve blockers](fixtures/c12_partial.json) all verify, then c=12 gives 16. The small square oracle verifies minimality at this fixed d: before 531566 the row is inactive, and through 531581 every square-pair residual at c=12 already has an earlier positive c. At m=547066 parent d=6,c=12 is exactly zero. At m=956598 child e=2,c=14 gives −1 for r=3 and 0 for r=4.

The finite scan constructs S2 by explicit nonnegative square pairs, including (0,0). It shifts by the permitted 3-powers and 5-powers with 16-bit lanes for D. All 2,735,335 masks from 0 through 2,735,334 have little-endian uint16 SHA-256 `4ddb8029360990b2bfb2fd551ca010d896c78f927e1b45786ef85333a445be24`. Frozen R1 square and valuation engines independently matched every S2, T and D entry at this endpoint. All pairs have an actual d≤7 / child c≤13 bridge.

The d≤6 / child c≤14 scan through 956598 covers 4,782,985 pairs. Its sole actual low-parent miss is (513014,4). The same pair is the sole d≤6 / child c≤12 miss through 547066. At the long-window exception, factor the 112 active residuals in all child columns adjacent to genuine low parent indices. Their sets of odd inert factors have exact minimum hitting-set size **44**, by recursively selecting one prime of an uncovered row. Hence any 14-prime palette leaves some such edge. For a palette omitting 3 the actual parent identity 513014=147²+701²+3+1 and the child e=1,c=4 residual 3(140²+914²) suffice. These arguments supply the small endpoints for the respective screened statements.

The 23-prime fixed-window control certifies every parent d=0,…,6 and c=0,…,12 with a prime of exact valuation one. Its parent seed has d=7,c=0. For r=4 the identity 5(a²+b²)=(a−2b)²+(2a+b)² gives a true edge 7→8 with child c=2. Thus the fixed low-parent window has a sharp no-3 budget of 22; the complete-system exclusion through 23 uses additional indices.

## Arbitrarily late first c in a fixed column

For any fixed d,C≥0 choose distinct primes p_j≡3 mod 4 for j<C, each avoiding Δ_j=3^C−3^j. There are infinitely many such primes: a finite list with product L misses a prime divisor congruent to 3 modulo 4 of 4L−1. Each Δ_j excludes finitely many primes. Seek m=5^d+3^C+a²+b². Require a²+b²≡p_j−Δ_j modulo p_j². Modulo p_j the target is nonzero. The squares and the target minus the squares each have (p_j+1)/2 elements, so they intersect. At least one coordinate is a unit. Varying it by a multiple of p_j lifts the norm to the required residue modulo p_j², since its doubled coordinate is invertible modulo p_j. CRT combines each coordinate independently. Every earlier residual is positive and congruent to p_j modulo p_j², so it has exact valuation one. At C the residual has the exhibited square pair. Increasing a by multiples of the product of the squared primes yields infinitely many m. This theorem concerns a specified parent column. [Executable construction](../../scripts/ajt5_first_c.py).

## Reproduction and R5 handoff

From the repository root, standard-library acceptance runs with:

```sh
(cd analysis/ajt5_integer_certificates && sha256sum -c SHA256SUMS)
python3 -O tests/ajt5_integer_tests.py
python3 src/verify_ajt5_palette.py
python3 scripts/check_ajt5_integer_boundary.py
python3 src/ajt5_integer_certificates.py analysis/ajt5_integer_certificates/fixtures/nonunitary_1339.json
python3 scripts/ajt5_first_c.py 3 15
```

The fourth command should exit 2 with an invalid unitary divisor. The verifier can replay one case with `--variant no3_23`. For optional fresh proof search, run the following in an environment with SciPy (generation used 1.17.0). Changes in optimizer choices can give different valid proof bytes.

```sh
proof_dir=$(mktemp -d)
for case in no3_22 no3_23 all14_d7 all14_d6; do
  python3 scripts/generate_ajt5_palette_proofs.py "$case" "$proof_dir/$case.jsonl.gz"
done
python3 src/verify_ajt5_palette.py --proof-dir "$proof_dir"
```

R5 starts at budgets **15 overall and 24 without 3**. These are first open budgets. A concrete candidate needs a parent square witness and covered endpoints through every active exponent. A surviving palette edge needs actual square identities on both sides before it can count as a true bridge. A single side or finite projection leaves the corresponding arithmetic question open.
