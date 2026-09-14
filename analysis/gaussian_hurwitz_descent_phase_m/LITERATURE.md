# Inspected sources and applicability ledger

Access date: 2026-09-14. Version-specific statements below refer to the actual
inspected text, not a title-only search result. Formal results M-D1–M-D4 and
the finite operator classification have self-contained proofs in this package;
no claim of historical priority is made.

## Source records

**V. John Voight, Quaternion Algebras, archived version 0.9.14 (2018).**
Author-hosted full text:
https://jvoight.github.io/quat/quat-book-v0.9.14.pdf
Inspected: Lemma 11.2.8, Lemma 11.3.2, Chapter 11 factorization context,
Main Theorem 28.4.3. PDF pages 168 and 464 were visually checked.

Exact inputs in compact form: for alpha,beta∈H, beta≠0, division gives
alpha=beta·mu+rho, N(rho)<N(beta), with a left-handed counterpart. No primitive
hypothesis is required. For a quaternion algebra B over a global field F,
if S includes a split place, B¹(F) is dense in the restricted norm-one adelic
product away from S. This is a statement about the ambient algebraic group,
not about a prescribed finite integral norm shell.

**MY. Jonah Mendel and Jiahui Yu, S-arithmetic groups acting simply
transitively on products of Bruhat–Tits trees, arXiv:2305.04448v3 (8 June 2026).**
https://arxiv.org/pdf/2305.04448
Theorem A, PDF page 1, visually checked. For totally real K, totally definite
B/K, and a maximal order O of class number one, all but finitely many prime
ideals p admit a congruence arithmetic lattice commensurable with
O[1/p]^×/o_K[1/p]^× acting simply transitively on the p-adic tree's vertices.
Its congruence quotients yield Ramanujan Cayley graphs of degree Np+1.
The exceptional-prime qualification is retained; Theorem A alone is not used
to certify a particular p=5 instance. The introduction describes the classical
Lipschitz LPS construction, but we do not claim to have independently checked
all statements in the original LPS paper.

**P. Arnold K. Pizer, Ramanujan Graphs, AMS/IP Studies in Advanced Mathematics
7 (1998), pp. 159–178.** Author's research article, inspected scanned text:
https://gkorpal.github.io/files/pizer.pdf
Proposition 4.7, printed pages 168–169 (PDF pages 9–10), visually checked.
For the paper's Brandt matrices at level N=qM, with E(qM)=0 and m coprime to N,
row sums are sigma_1(m), the matrices are symmetric, and the nontrivial
eigenvalues have absolute value at most sigma_0(m)sqrt(m). In particular,
m=p gives the 2sqrt(p) bound. Vertices index ideal classes; unit weights and
level hypotheses are part of the construction.

## Applicability table — deductions made in this report

| input | group/order and conditions | pointwise or average? | fixed norm M? | individual representations? | forces N(w)=5^d? |
|---|---|---|---|---|---|
| Hurwitz Euclidean division | H; beta nonzero; no primitivity requirement | exact per division | no: the remainder norm changes | acts on input elements | no |
| Strong approximation | B¹; at least one split place in S; appropriate local open sets | density in local products | only the group norm-one equation, not our prescribed integral shell | rational group elements, not the required coordinate target | no |
| MY Theorem A | class-number-one maximal definite order; all but finitely many p | exact tree action | no | tree vertices are lattice classes | no |
| Pizer Proposition 4.7 | level/copimality and equal-unit-weight hypotheses | spectral bound | not our fixed representation norm | ideal classes, not all q with N(q)=M | no |

For Hamilton's algebra the splitting at 5 follows explicitly from the matrix
model and the lift of a square root of -1. Taking S={infinity,5} meets the
ambient strong-approximation hypothesis. This does not establish integrality
of all successive norm-5 moves or hit a specified archimedean coordinate
condition. M-D1 supplies an actual invariant that survives the proposed action.

Class number one for ideals does not assert transitivity on the points of a
fixed norm shell. Likewise, a 5-adic tree vertex is not a quaternion
representation q of a specified rational integer M. These distinctions are
why importing a tree-transitivity theorem would not settle this task.

## Why a spectral gap is not a hitting proof

This is an elementary calculation, not an imported Ramanujan theorem. Suppose
P is a symmetric stochastic transition matrix on V vertices, uniform stationary
measure, and its restriction perpendicular to constants has operator norm
rho<1. For a target subset T,

    |P^t(x,T)-|T|/V| ≤ rho^t sqrt(|T|).

This follows by applying the spectral bound and Cauchy–Schwarz to the centered
point mass and target indicator. It proves positive hitting probability once
rho^t<sqrt(|T|)/V — but only if |T|>0 is already known. It does not prove
nonemptiness. If a component has no targets, no amount of mixing changes that.
Our quotient graphs need not be regular with the unweighted adjacency used
in the lab; an LPS or Brandt spectral bound cannot simply be assigned to them.

For raw integral fixed-pair targets the exact identity is

    |T_M| = sum_(d≥0,5^d≤M) r2(M-5^d) r2(5^d),
    r2(0)=1,   r2(5^d)=4(d+1).

It is a counting identity, not a lower bound. No uniform positive bound for
this exact target size or a relevant mixing scale was established.

## The p-adic target is not just a ray

For a nonzero Gaussian integer w, N(w) being a 5-power is equivalent to
w∈Z[i][1/5]^× ∩ Z[i]. The condition includes the absence of Gaussian prime
factors at **every** place away from 5. A local tree ray or apartment at 5
alone does not impose those exclusions. Mixed exponents of 2+i and 2-i remain
permitted throughout. This diagnosis does not rule out a future genuinely
new global coupling, but no exact target-hitting theorem was acquired here.

## Literature status

The inspected sources provide algebraic and graph-theoretic tools, not a
prescribed-coordinate theorem closing A303656. No claim is made that this
was an exhaustive literature review of all restricted quadratic forms. The
route stopped after the explicit finite and infinite obstructions, rather
than continuing an ungated theorem hunt.
