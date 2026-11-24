# Prime explanations of complete NO_BRIDGE certificates

A prime explanation chooses a prime congruent to 3 modulo 4 with odd valuation in each residual used to establish a negative endpoint. Count distinct primes across the whole certificate. For every integer `m ≥ 2` and every `r = 0,…,4`, a complete actual NO_BRIDGE explanation requires at least **16 distinct primes**, or **25 distinct primes if it omits 3**. These statements are lower bounds. Existence of a complete explanation, and attainability of either budget, remain open.

## From active rows to residue classes

Take a finite palette of size at most the budget. A row survives when its nonnegative residual has even valuation at every palette prime, with zero always surviving. A pair of surviving rows at parent index d and child index e ∈ {d,d+1} rules out an explanation on that palette. Each endpoint would need an odd valuation at a palette prime for every active row in that column to certify the column negative.

For each digit write x=5m. The parent label P(d,c) has root 5(5^d+3^c). The child label Q(e,c) has root 5^e+3^c−r. The parent difference equals 5 times its residual, which leaves all inert valuations unchanged. The child difference equals its residual. Distinct labels with equal roots impose one condition. The positivity check in the replay rebuilds the whole root universe for every digit. Its maximum is 2,735,330, reached at P(6,12), so every row is strictly active for m≥547067. The separate finite bridge scan covers all 2,735,325 pairs with 2≤m≤547066. A zero residual is the actual square sum 0²+0² at that boundary.

For the large range, take A to consist of those d in 0,…,7 with a surviving selected parent row. For d outside A all selected parent rows are blocked. If no edge survives, every selected row at e in A ∪ (A+1) is blocked. This gives 256 possible directions for each of five digits, including the empty direction. The replay reconstructs labels for every one.

| Palette budget | Selected parent rows | Selected child rows | Empty direction |
|---|---|---|---|
| 15, including palettes that use 3 | d≤6, c≤12 and d=7, c≤11 | e ∈ A ∪ (A+1), c≤13 | All selected parent rows |
| 24, palette omits 3 | Same base | e ∈ A ∪ (A+1), c≤12 | Two separate continuations at d=8 |

For budget 24, close each nonempty mask by adjoining each missing d flanked by two members d−1 and d+1. The added d introduces no new child index. Its parent rows disappear, so the closed system is a subset of the original obligations. The verifier tests this inclusion directly for each mask. The 1,275 nonempty digit/direction pairs thus reduce to 565 proof records. The other five records each replay two continuations with common parent base B. If P(8,1) is blocked, all of B ∪ {P(8,1)} must be blocked. If this row survives, child Q(8,c_r) must be blocked, giving B ∪ {Q(8,c_r)}. The proof excludes each system separately.

| r | c_r | Q root |
|---:|---:|---:|
| 0 | 1 | 390628 |
| 1 | 2 | 390633 |
| 2 | 5 | 390866 |
| 3 | 2 | 390631 |
| 4 | 4 | 390702 |

The parent continuation used here is **P(8,1)**, root **1953140**. Replacing it by P(8,0), root 1953130, breaks this argument. The [24-prime control](global_p80_control.json) has an exact valuation-one blocker at every one of the 103 base labels and at P(8,0), while every selected prime is coprime to the P(8,1) residual. The verifier checks primality and each divisibility claim directly. The integer was obtained by lifting each chosen residue modulo p², combining these congruences with x≡0 (mod 5) by CRT, and setting m=x/5. This control establishes feasibility on those finite parent rows. The common parent continuation is stored once per digit. The five child continuations differ. No C10 rectangle witness is used.

## Integer replay

For all distinct roots K,L with K≠L, factor |K−L|. Every prime that can hit two roots belongs to this finite catalogue. Each non-3 inert prime p takes one residue class x mod p, so even removing every root in that class overestimates what it can kill. Any prime outside the catalogue can account for at most one root. The replay allows unlimited singleton choices subject to the total budget.

In a leaf with remaining budget b the data give integers D>0 and 0≤w(K)≤D for every live root. For each remaining multiroot prime p, take z(p) as the positive part of its greatest class weight minus D. Any b choices cover weight at most bD+Σz(p). The replay requires Σw(K)>bD+Σz(p). At a branch it checks every live multiroot residue and removes that class at cost one. The required default drops the prime's multiroot classes at cost **zero**. An actual singleton hit can still be charged against the remaining singleton budget.

With 3 available, the first tree excludes all coverings using at most 15 non-3 primes. Each of the three other alternatives spends one on 3. It removes either the whole class x mod 3 or a regenerated maximal mask of roots with odd 3-adic valuation. For exact masks, let H be the maximum valuation of a nonzero root difference. Choose a nearest root K to x in the 3-adic metric. Up to depth H, matching digits up to the first differing digit fixes the valuation pattern. Beyond H only K can continue matching, and both parities are realized at depths H+1 and H+2. Testing each root and the representatives K+t·3^h for t∈{1,2}, 0≤h≤H+2 therefore covers all masks. For all four refined directions the regression suite also derives the same nine masks directly modulo 27 by removing valuation one and every depth at least three. An empty killed set is already handled by the full non-3 tree. Coarse removal and removal of supersets can only make coverage easier.

The [search](global_generate.py) uses SciPy to propose weights. The [replay](global_verify.py) uses standard-library integer arithmetic and the R4 independent root catalogue, strict parser and ternary mask enumeration. It checks every direction in order, rejects missing alternatives and checks the normalized strict margin at every leaf.

| Replay | Directions | Records | Non-3 branch nodes | Integer leaves | Minimum normalized margin |
|---|---:|---:|---:|---:|---:|
| all15 | 1,280 | 1,280 | 0 | 5,152 | 1/12 |
| no3_24 | 1,280 | 570 | 459 | 4,407 | 1/420 |

For all15 the leaves comprise 1,280 no-3 alternatives, 3,836 coarse classes and 36 exact masks. The four refined directions are r=4 and A encoded as 65, 80, 97 or 112, in each case with x≡1 (mod 3). The locally regenerated compressed all15 stream has SHA-256 `eddd459ce610e60118b6bc6084ee13f8191ed3a6eaa7c65ea45b2318cf372685`, matching the reported digest. Both streams were generated from the repository code and accepted by the integer replay.

Run this command from the repository root to replay both stored proofs.

```sh
python3 -O analysis/ajt5_frontier/global_verify.py
```

To regenerate the proofs, replace DIR below with an existing temporary directory.

```sh
python3 analysis/ajt5_frontier/global_generate.py all15 DIR/global_all15.jsonl.gz
python3 analysis/ajt5_frontier/global_generate.py no3_24 DIR/global_no3_24.jsonl.gz
python3 analysis/ajt5_frontier/global_verify.py --proof-dir DIR
```

A surviving row can still have an odd valuation at an unselected prime. Arithmetic square witnesses on both ends are needed for an actual bridge. Likewise a feasible finite blocking pattern can have a surviving edge outside its window.
