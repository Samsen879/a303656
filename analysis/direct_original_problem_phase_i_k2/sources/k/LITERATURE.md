# Focused primary-source adaptation audit

## 1. Covering systems

Filaseta, Ford, Konyagin, Pomerance and Yu, *Sieving by large integers and covering systems of congruences*, arXiv:math/0507374. Original PDF, printed pp.4 and 6, equation (1.2), Lemma 2.1; screenshots inspected.

Source: `https://arxiv.org/pdf/math/0507374`

For a residue system C with moduli n_i, their lemma bounds the uncovered density below by

prod_i(1-1/n_i) - sum_{i<j,gcd(n_i,n_j)>1} 1/(n_i*n_j).

Repeated moduli are allowed in their residue-system framework. For fixed c in our problem, a soluble divisibility condition gives a d-congruence modulo ord_p(5), with higher refinements needed for valuation parity. The bound does not establish a positive uncovered count in the finite O(log n)-length exponent interval: neither the required dependency control nor the boundary estimate is available. No completion theorem is imported.

## 2. Residue bias for sums of two squares

Ofir Gorodetsky, *Sums of two squares are strongly biased towards quadratic residues*, arXiv:2111.12662v4, 2 May 2023; original first page inspected.

Source: `https://arxiv.org/pdf/2111.12662`

The work studies comparative prefix counts in arithmetic progressions, with conditional natural-density bias results. These are not uniform statements about each target's sparse set n-3^c-5^d. They do not supply an inverse or LC-K. Its introductory two-square criterion agrees with the indicator used in the factorization verification.

## Relation to the new work

The exact local formula, the 504/5544 classifications, and the finite local-count estimate in LOCAL_MODEL.md are derived directly here. They do not rely on either paper asserting a pointwise exceptional-set theorem. No general literature review or generic sieve restart is intended.
