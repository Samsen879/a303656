# Computation specification and replay contract

## Scope and chronology

The executable targets were developed with the mathematical exploration. This
written specification was consolidated after exploratory runs and before the
final sealed replay; it is not claimed to have been pre-registered before
all discovery. No enlarged prime scan or large-scale computation was used.

The program is standalone Python standard library. Arithmetic uses integers,
`Fraction`, finite bit masks, trial division, exact order reduction, Sylvester
matrices/Bareiss determinants and modular polynomial division. No floating
point value determines a mathematical result.

## Frozen targets

1. Sparse-cover and exact-centered-set identities: (p,beta,max_r) equal to
   (3,2,2), (3,3,2), (5,2,4), (7,1,6). All parity-compatible shell-index subsets.
   All first-digit blocker sets for p=3; empty blocker set in the other large
   local enumerations. Center zero is used by translation equivariance.
2. Boundary: every residue modulo 2^K, K=2,...,9; direct sum-of-two-squares
   residue sets, both exponent parities and the prescribed safe-anchor table.
3. Abstract triangular grammar: domain 2 x 3 x 7; all listed congruence seeds
   with odd modulus 3,7,21 and optional parity; zero, one or two seed geometries,
   repeated geometries allowed for distinct abstract origins; original dynamic
   signatures w_3=2,w_7=6. No claim of actual rigid-prime realization.
4. Actual pair: primes 67,20771; K=2,E={1}; residues 2,20775; U=L=228470.
   Direct modular-period predicates versus reconstructed normal forms, actual
   SPLIT, static blocker choices alive/5/31/67, and exact alive-anchor game.
5. Actual naive-potential example: primes31,20771, K=2,E={1}, anchor0,
   residues2,103861 and lower coordinates d=0 mod3,d=1 mod5.
6. Resultants: h=3,5,7 and Y=0,1,2; exact determinant and sealed closed
   polynomial expression. No nonzero-Y full factorization claim.
7. Actual paired cosets: q=20771,h=67,u=155; all 155 lower classes, comparing
   edge counts to degrees of finite-field polynomial gcds.
8. Complete finite factor identities at cyclotomic orders 3,6,9,18,27,54,5,10;
   factor primality, actual multiplicative orders and lifting exponents.
9. Descended-resource arithmetic supports: the four shallow 3-heads; complete
   p-ary tree depth profiles with <=6 leaves; all 714 5/6-row first-digit/deep
   multisets for the rank-5 witness-count inequality.
10. Adversarial regressions: current blocking, mixed-anchor row roles, actual
    SPLIT, local zero, ancestor coverage, center translations, fractional Hall
    gap, and an abstract seven-leaf frontier.

## Complexity and evidence limits

The local enumerations are bounded by explicit cylinder subsets and bit-mask
operations. The actual period has only 228470 classes; polynomial gcds have
degree67; the largest determinant has size14. A p=3,beta=2 local benchmark is
recorded before the larger enumerations. The exact trial divisions are for
specific integers, not an unbounded or expanded Wieferich scan.

The universal seven-prime theorem is proved analytically in MASTER_THEOREM.md.
Enumerating the stated finite domains is not a proof by exhaustion of all
admitted systems. A zero mismatch count certifies only the corresponding test
scope. Timings are measurements of this environment, not resource forecasts.

## Reproduction

From the bundle directory:

```sh
python3 -B tools/verify_bundle.py
out=$(mktemp -d)
python3 -B tools/reference.py --output-dir "$out/replay"
python3 -B -m unittest discover -s tests -v
python3 -B tools/verify_bundle.py --replay
```

The reference CLI requires an explicit output directory outside this bundle.
Frozen results are not overwritten by the verification command. `--quick`
reduces some finite domains; its outputs are not expected to match full-run
frozen results.

All files listed in SHA256SUMS.txt are byte-hashed. In addition,
`results/math_hashes.json` hashes canonical generated JSON after deleting only
keys named `seconds`. This allows exact replay of mathematical content without
pretending that wall-clock timings are deterministic. No numeric tolerance
or approximate comparison is used. Unit-test log durations are not compared.

## Software independence

No repository parser, mask generator, runner, or test implementation is
imported. Source arithmetic data and theorem definitions are acknowledged in
SOURCES.md. Direct modular values versus normal forms, and coset enumeration
versus polynomial gcds, are cross-checks within this one new software stack;
they are not called fully independent implementations.
