# Inverse statements: proved, refuted, and still unsupported

## K-I1. Proved inverse for a local count

Theorems K-L3/K-L4 give, for every sufficiently large n,

G23711(n)/J(n)<=763/5120 => n mod1848 in
{238,392,406,560,574,728,910,1064,1414,1568}.

K-L5 additionally gives the separated coarse-band equivalence, eventually uniformly in n:

G23711(n)/J(n)<8119/38400 iff n mod24 in {2,4,8,22}.

Neither statement has R on its left. Their proofs use a finite spectrum gap and a uniform local-count approximation. No numerical starting threshold is claimed. They must not be applied to the pilot scale as though the asymptotic error were already negligible.

## K-I2. Representation inverse not obtained

Only R<=G is known. The implication

R(n) small => G23711(n) small

is not a consequence. Remaining large bad primes can destroy an unknown fraction of the local survivors. Neither an R=0 inverse into a proper explicit family nor its large-prime completion has been proved.

In particular “finite local classification plus one missing lemma” must not be understood as permission to consider only the five 560 lifts. Counterexamples outside those lifts have not been excluded.

## K-N1. The exact-minimizer explanation of the finite hard tail is too strong

The five task-listed argmins have been individually verified on their ENTIRE actual exponent grids, not on a bulk subrectangle:

| n | verified R | G23711 | rho237 | in exact local minimum family? |
|---:|---:|---:|---:|---|
|100235446|9|28|217/1152|no|
|10000011172|13|43|203/1152|no|
|10000072156|13|45|203/1152|no|
|10000079932|13|42|217/1152|no|
|1000000244380|20|77|203/1152|no|

The additional named hard target 1000000205302 has verified R=23, G23711=60, and the minimum rho237=21/128 and rho23711=1869/12800.

Thus none of the five reported window-minimum targets lies in the exact minimizer family. The claim that these observed minima must minimize the local density is false. The two C-window targets also disprove an order-preserving relationship: the lower-density target has fewer local survivors (60 versus 77), but MORE norms (23 versus 20).

Scope: the individual representation counts and local memberships are independently certified; their ranks as full-window minima are supplied by the brief and not re-scanned. These finite examples do NOT refute an unspecified sufficiently-large inverse, an R=0 inverse, or a NEAR-minimizer family. Their rho237 values are only 29/27 or 31/27 times its global minimum. All six are in the coarse hard band of K-L5.

## K-N2. Exact finite G is not a fixed-period function

The request for an exact count depending only on n mod a fixed modulus requires correction. The actual logarithmic grid changes with n, and valuation parity is not bounded-depth data. K-L4 and the positive minimum show that G is unbounded along each fixed residue class; an exactly periodic count would be bounded. The same-exponent 7-parity collision in WHY_560.md provides a termwise demonstration of the issue.

What has been proved is a fixed-period exact COEFFICIENT with a uniform finite-grid error. One may also compute finite truncated counts periodically in n if the grid bounds and prime-power depths are retained as parameters. Neither is an exact fixed-period formula for G itself.

## K-N3. Local exponent rigidity does not itself force a norm

The two same-cell examples at 28280 and 915320 in WHY_560.md pass identical small-prime conditions and have different norm status. This is a literal-base, fixed-exponent example, not an arbitrary substitute multiset. It blocks a named automatic local-to-Gaussian conclusion. The broad finite-period minorant obstruction was already present in J-M1/J-M2 and is not claimed as new here.

## Data validation, without silently replacing the pilot

The actual directory A303656_ORIGINAL_N_SURVIVOR_PILOT, including its scanner/reference definition and JSONL records, was not retrieved. Therefore:

- Full 11-subclass enrichment and independence analysis is unavailable.
- False-positive/negative counts for the new exact-minimum classifier are unknown, not zero.
- No claim of full three-window replay or full Level B is made.

The window endpoints do, however, determine exact arithmetic denominators without any new target scan. Each full window contains 104 integers in 560 mod2520. The number in the exact 2/3/7 minimum family is 3122,3120,3121 for A,B,C; the number in the exact 2/3/7/11 minimum family is 1419,1417,1420. Per-lift mod27720 counts are saved explicitly.

For the coarse S1 classifier, the brief supplies the top256 numerators 251,255,256. Its full-window denominator is exactly 43691 in EACH window, computed from endpoints. Thus, conditional on those reported numerators:

| Window | TP | FN | FP relative to top256 | full-window predicted count |
|---|---:|---:|---:|---:|
|A|251|5|43440|43691|
|B|255|1|43436|43691|
|C|256|0|43435|43691|

These are not a raw-pilot replay. “FP” here means outside the primary top256 selection, NOT independently known to have a large numerical R. Its precision is about 0.57–0.59%, despite high recall: a broad necessary-signature candidate is not a narrow predictor of extrema. The supplied 560 enrichment numbers do not identify their own selection denominator, so no extremal counts were reverse-engineered from them.

## Least-bad metric guard

On an UNFILTERED full-grid histogram for the six named targets, the counts of least bad prime 3,7,11 are respectively:

(79,13,6), (137,27,17), (138,28,18),
(138,18,18), (174,42,20), (175,46,33).

Thus a reading of “7 and 11 dominate” as “3 has already been beaten in every unfiltered named target” is not supported. A prefiltered definition could explain the difference, but the scanner is missing and this is not assumed. LOCAL_MODEL.md gives both the raw and L2-filtered exact events so later replay can compare like with like.

## Outcome level

This is a rigorous local-minimizer and separated-band theorem package with adversarial finite checks: the mathematical component of Level B. Full Level B requires the unavailable raw empirical coupling. No Level A or Level C is claimed. The narrow counterexamples are NOT the full Level D assertion that no stable finite inverse structure exists. This is also not Level E: the output contains proved local mathematics, not just additional enrichment charts.
