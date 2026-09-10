# Adversarial proof and computation audit

## Theorem gates

|Gate|Result|Reason|
|---|---|---|
|F2 preserved|PASS|No regular-tree exhaustion or finite-branching/finite-depth inference.|
|F4 exact full closure|PASS|Every terminal order contains all maximal generators; all order factors expanded.|
|Terminal3 excluded from all-odd|PASS|Separate order2/regularity sanity record, never an admitted all-odd row.|
|Actual base5 versus variable base|PASS|Every nonregular fixture declares b!=5 and is_base5_member=false; mutation rejected.|
|G1 global sign|PASS|Both calculations give the same (-1)^edge-count / (-1)^width; no invented positive product law.|
|G2 tame scope|PASS|gcd(m,q)=1 is explicit; q-th-power countertest shows why it cannot be removed.|
|G3 prime-base strengthening|PASS|Final arithmetic progressions are units; numeric prime-base examples have full certificates.|
|G4 Dirichlet step|PASS|CRT primes avoid zero residues; all labels can be chosen successively larger.|
|G4 exact orders|PASS|Order is chosen in the cyclic finite field; all prime-divisor order drops are necessary.|
|G4 lifting marks|PASS|Simple-root derivative is a unit; adding x^s gives exact valuation s.|
|G4 literal base5 claim|NOT MADE|Prime bases vary; this is a countermodel to specified base-uniform assumptions only.|
|G5 normalized integer|PASS|Unique singleton imprimitive p removed once; no multi-max imprimitive prime.|
|G5 significant terminal reduction|NOT CLAIMED|Odd q² is1 mod8, so removing q² preserves the signature.|
|Entire auxiliary directories read|NOT COMPLETED|All four core reports, B7 theorem file and four integration notes were read, not every auxiliary file.|
|Repository-native tests|NOT RUN|Only local standalone reference replay is claimed.|

## Corruption tests actually rejected

The verifier rejects: a fake base5-member flag; replacing a variable base by5; wrong root valuation; wrong lifting coefficient; omission of a maximal generator; wrong edge sign; missing head/proper state; Lucas witness1; incomplete p−1 factors; a prime-base claim without a certificate; inserting terminal3 into the all-odd rows; and a corrupted exact order.

Rejections remain active under `python -O`; no mathematical check relies on an assert statement.

## Numerical certificate standard

For each prime p, recursive certificates completely factor p−1. The witness g satisfies g^(p−1)=1 modp and gcd(g^((p−1)/r)−1,p)=1 for every prime r|p−1. For any prime divisor d of p, these tests force ord_d(g) to contain every prime power in p−1, hence d−1>=p−1 and d>=p. Thus p is prime. Factor primality is recursively certified down to2.

Order certificates test the full power and every prime-divisor drop. Lifting certificates test p^s and p^(s+1) and record the first nonzero coefficient. All model rows are jointly derived from a single integer base b.

## Independence and novelty

The generator may use SymPy to find factors and screen primes; the trusted replay uses no SymPy and re-proves all prime claims from certificates. This separates discovery from certificate checking but is not an independent author or an independent full software stack. All universal deductions are human-readable proofs in this same session, not formalized Lean/Coq results.

The basic CRT/Hensel lower-state-preserving counterexample was already in Cyclotomic Phase E E8. The single-edge reciprocity observation and F2/F4 are also inherited. This package's stated gain is the precise all-odd whole-DAG/antichain and tame-versus-wild route boundary, with full certified fixtures, plus the fixed-base mod8 signature. No new base5 terminal index has been closed.

## Scope of the optional finite discovery probe

Only the displayed four fork indices and q=1+2kn with odd k<=100000 and q mod20 in{11,19} were tested. The80000 empty modular-survivor result is not a full factorization or a squarefree certificate. The proof and evidence verifier do not depend on this absence result.

GITHUB WRITES PERFORMED: NONE.
