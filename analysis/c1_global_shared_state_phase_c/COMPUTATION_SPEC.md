# Frozen computation specification — shared-state Phase C

Authority: Samsen879/a303656, main 71b8d428b32724c37e593bcfd9d5f06a42e72d21,
tree 5609e47eed0c058c190ef59c61644e2fd4b8fad6.

This specification is written before executing the reference enumerations below.
No prime scan, repository writes, native-repository replay, or full 72-million-cell
period enumeration is authorized or claimed.

## A. Actual integer configuration gap

Actual primes P={3,7,31,43,1303}, all K=2 and E={1}.
State families are shared across both anchors and the entire domain:
S3={2+3k:0<=k<3}; S7={a+7k:a in {2,5,6},0<=k<7};
S31={a+31k:a in {2,6,26},0<=k<31}; S43=S1303={2}.
Verify primality, exact orders, regularity, U=1302, and L=U*43*1303.
Rows 43 and 1303 have empty coarse fatal masks because beta=0 and s=1;
they are actual support rows, not synthetic ambient-coordinate inflation.
Exhaust all 3*21*93=5859 global state choices on all 1302 coarse cells.
Compute exact coverage/escape distributions. Independently verify the uniform
rational fractional solution on every cell. Verify a determinant-2 incidence
minor from the three actual 3-row states and cells d=0,2,4.
The integer verdict uses actual masks; no fractional/integer equivalence is assumed.

## B. Six demands

Enumerate all 340 nonempty top words of lengths 1 through 4 over the four
anchor-coverage subsets. Test all six monotone demands at all four lower
coverage subsets: 8160 exact truth comparisons. Audit SPLIT explicitly.

## C. Paired original rigid states

For q=20771 and q=40487 only, verify q, w, s. Enumerate all powers of 5
modulo q over w exponents, all difference-2 pairs, and all same-lower pairs
at original h=67 and 653 respectively. Compare two differently organized
coset enumerations. Select two distinct nonempty lower classes for each q;
provide legal shared q^2 residues for each individually, and the exact
state collision between them. No full q^2-residue enumeration is claimed.

## D. Exact integer resultants

For h in {3,5,7} and ordinary Y in {0,1,2}, compute the Sylvester determinant
with fraction-free Bareiss elimination; cross-check with rational polynomial
Euclidean resultant computation. Report fixed-h pairwise and three-way gcds.
These fixed original-depth calculations do not establish an all-Y prime bound.

## E. Exact valuation-family criterion

Exhaust every 1-, 2-, and 3-element set of constraints (a,h) with a modulo 9,
h=1, q=3. Compare actual enumeration of r modulo 9 against the maximum-radius
and forbidden-next-digit criterion. Check actual centers 1+5^d for d=0,2,4.

## F. Regular projection lemma checks

For q=3,7,11, all r modulo q^K at K=2,3 and every nonempty permitted odd
valuation set, compare full masks against the regular dynamic normal form.
For each active lower logarithm guard, check that its common safe projection
modulo q^2 contains all q centered first-digit lifts; when K=2 refine the
exponent period analytically by q, without claiming this creates a coarse
coordinate in a certificate. This checks the local width lemma, not the
unbounded theorem by exhaustion.

## Quantifiers and evidence boundaries

A: forall one global state vector, exists a coarse common escape; but exists
one fractional configuration assignment covering every coarse cell.
B/E/F: exact tests in explicitly finite domains, not general theorem proofs.
C: exists a legal paired state separately in each named fiber; there is no
single paired rigid state serving both distinct lower classes.
D: fixed original h and ordinary integer representatives only.
All unbounded claims in the report require the accompanying mathematical proofs.
