# EMPTY_D prime support

For every integer x ≥ 2, a complete prime explanation of D(x) = ∅ would use **at least 17 distinct primes congruent to 3 modulo 4**. Here D(x) consists of the exponents d for which x = a² + b² + 3ᶜ + 5ᵈ with nonnegative integers a,b,c,d. An explanation must assign to every active (d,c) an inert prime of odd valuation in its positive residual. A zero residual is represented by 0² + 0². The result concerns EMPTY_D alone. It leaves the AJT5 prime bound, attainability of 17, and the existence of such an x separate questions.

## Large x

Use d = 0,…,7 and c = 0,…,12, omitting (7,12). Of the 103 labels there are 102 different roots K = 5ᵈ + 3ᶜ. Their maximum is 547066, so every x − K in this window is strictly positive from x = 547067 onward. A complete explanation must kill every one of these roots.

For p ≠ 3, all killed roots lie in a single residue class modulo p. The verifier sieves every prime through the largest difference and retains every p ≡ 3 mod 4 other than 3 that has a multiple-root residue class. This gives 622 primes. Larger primes and primes without a coincidence can each cover at most one root. Allowing a selected residue to kill all its members, and allowing an arbitrary singleton for the price of one prime, can only increase possible coverage. This enumeration is independent of the producer's factorization of root differences.

If 3 is absent the budget is 16. With 3 present, enumerate exact odd-valuation masks and spend one on 3. To see the enumeration is exhaustive, let H be the greatest 3-adic valuation of a nonzero pairwise root difference. Include x = K for every root (skipping that zero residual). Otherwise take a nearest root K maximizing h = v₃(x − K). For h ≤ H, one of K + t·3ʰ for t = 1,2 agrees with x modulo 3ʰ⁺¹. Every root valuation is at most h, so this sample reproduces the full mask. For h > H all other valuations equal v₃(K − K′), and depths H+1 and H+2 reproduce either parity at K. This yields 188 distinct masks. Each lies in one of the 17 inclusion-maximal masks. Removing an entire maximal mask gives an easier covering problem for the remaining 15 primes. The producer independently follows the ternary digit tree.

Each leaf gives a positive integer scale s and a weight in [0,s] for each live root in increasing order. For each available p take its largest residue-class weight, and let zₚ be the excess over s, floored at zero. A cover by b primes has total weight at most bs + Σzₚ, counting excess at most once per prime. Each leaf strictly exceeds that upper bound. An internal node enumerates all multiple-root residues of a selected prime p, removes the corresponding roots and consumes one prime. Its mandatory default branch removes p from further multiple-root use, **keeps all roots and the entire budget**, and still permits singletons. This includes both an unused p and a selected p covering at most one root. The generated proof has four internal nodes and 46 leaves, with least strict excess divided by s equal to 1/6.

The regression fixture uses roots {0,11,77} and x = 143. All three residuals have exact valuation one at 11. A forged tree branches on 7 and claims to exclude a one-prime cover. Its default leaf would pass if the checker incorrectly charged one prime on that branch. The verifier rejects this leaf by integer arithmetic.

## Finite x

For 2 ≤ x ≤ 547066 the verifier directly marks every a²+b² up to the endpoint by enumerating a ≤ b, including zero. Bit shifts by each positive power value 3ᶜ (starting with 1) and then each 5ᵈ (also starting with 1) give the actual four-term representation set. Every one of the 547065 target bits is set. This includes the zero-residual boundary at (d,c) = (6,12). Thus the finite interval admits no actual EMPTY_D, regardless of budget.

## Reproduction

From the repository root, the standard-library command checks the saved proof, the finite interval and the forged default branch.

```sh
python3 -O analysis/ajt5_frontier/empty_verify.py
```

Optional fresh search uses SciPy. The replay accepts the integer inequalities independently of provider or optimizer choices. To check a generated proof directly, run the following from the repository root.

```sh
proof_dir=$(mktemp -d)
python3 analysis/ajt5_frontier/empty_generate.py "$proof_dir/empty_proof.json"
python3 analysis/ajt5_frontier/empty_verify.py "$proof_dir/empty_proof.json"
```
