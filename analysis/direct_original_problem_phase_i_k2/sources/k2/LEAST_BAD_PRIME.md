# K2 negative theorems: the objective and least-prime capacities

The notation is fixed in `LARGE_PRIME_DECOMPOSITION.md`.

## K2-N1. A uniform fixed fraction of local survivors cannot be norms

**Statement.** Assume the accepted uniform lower bound `G(n)>=a_0(log n)^2`.
For every eta>0,
\[
\#\{n\in[X,2X]\cap\mathbb Z:R(n)\ge\eta G(n)\}
\ll\frac{X}{\eta\sqrt{\log X}}.                            \tag{N1}
\]
In particular, there do not exist eta>0 and N0 such that
\[
\sum_pN_p^G(n)\le(1-\eta)G(n)\quad(n\ge N_0).
\]
The task's fixed-eta Level B target is therefore false, not merely unproved.

**Proof.** Let B(t) count nonnegative sums of two squares at most t. Landau's
counting theorem gives `B(t)=O(t/sqrt(log t))`; see reference L1 in LITERATURE.
For every fixed pair `(c,d)` with powers at most 2X, the number of n in `[X,2X]`
whose residual is a norm is at most B(2X). Summing over exponent pairs, including
multiplicities, gives
\[
\sum_{X\le n\le2X}R(n)\le J(2X)B(2X)
\ll X(\log X)^{3/2}.                                      \tag{N2}
\]
Pairs with zero residual are included by B; no boundary convention is suppressed.
Each n counted on the left of N1 contributes at least `eta*a_0*(log X)^2` to N2.
Division proves N1. The same proof works on integer dyadic intervals with either
endpoint convention. QED.

**Corollary (log-loss barrier).** For fixed kappa>0 and beta<1/2,
\[
\#\{X\le n\le2X:R(n)\ge\kappa G(n)/(\log n)^\beta\}
\ll_{\beta,\kappa}X(\log X)^{\beta-1/2}=o(X).
\]
Thus a universal lower bound of this form cannot have beta<1/2. The borderline
beta=1/2 (the former LC-K target) is **not disproved**. Neither is positivity of R.
An average is used here only to disprove a proposed universal estimate, never to
substitute for pointwise completion.

## K2-N2. Literal atoms defeat smooth termwise least-bad capacities

**Statement.** For every fixed C>0 and real alpha, the bound
\[
N_p^G(n)\le \frac{C G(n)}{p(\log p)^\alpha}                 \tag{N3}
\]
fails for arbitrarily large literal targets n and eligible primes p. The same
holds with G replaced by J.

**Proof.** There are infinitely many pairs of consecutive primes p<q congruent
to 3 mod 4 with q<2p. No prime-gap estimate is needed: if eventually every such
successor exceeded 2p, their reciprocal series would converge geometrically,
contrary to the Mertens progression formula (reference L2).

For any such pair above 19 put `n=pq+2`. The literal exponent pair `(0,0)` has
residual `pq`. It satisfies L2 since pq=1 mod 4, and its 3-, 7-, 11-valuations
vanish. Every prime below p has even (indeed zero) valuation. Thus its **least**
remaining bad prime is exactly p and `N_p^G(n)>=1`.
But `n<=2p^2+2` and `G(n)<=J(n)=O((log p)^2)`, so the right side of N3 tends
to zero. QED.

For every fixed theta<1/2 these counterexamples eventually have p>n^theta.
They therefore occur in genuinely large-prime ranges. They are not counterexamples
to representability of n: the failure is one residual, not all exponent pairs.

**Exact finite certificate.** With
\[
p=100003,\quad q=100019,\quad n=10002200059,
\]
exact trial division proves both primalities. The full literal grid has
\[
J=|\mathcal D|=315,\quad G=82,\quad R=33,\quad N_{100003}^G=1.
\]
For comparison `G/p=82/100003<0.001`. Also
\[
10002200059=33798^2+94127^2+3^0+5^5.
\]
`ATOM_GRID.json` stores every residual factorization; FINITE_CERTIFICATES gives
all derived counts. The infinite family, not one finite example, disproves arbitrary
fixed constants C.

## What least-prime conditioning does and does not give

Equation D4 is an exact partition and can be iterated without loss. A model with
odd-valuation density `1/(p+1)` would formally predict a least-prime factor of
approximately `1/(p sqrt(log p))`. This is a **model**, not an established formula
for the two short exponential orbits. N2 already refutes a termwise atom-free
upper bound of that shape. Adding `+1` per prime avoids that counterexample but
summing those errors to sqrt(n) does not give a witness-sensitive error budget.

The integer-distance theorem in SPARSE_GRID_BOUNDS gives a stronger quantitative
reason why taking absolute values after this conditioning still loses too much.
