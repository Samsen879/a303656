# The large-prime-pair attack and its audited limits

The quarter-cutoff factorization and identity D5-D6 are inherited from Phase J.
This file audits the proposed counting arguments, rather than rebranding that
identity as a new theorem.

## No injection from failure points to unlabelled pairs has been proved

Choosing the two least bad primes assigns a pair to every failure, but different
residuals may receive the same pair. In the quarter-cutoff range the pair is
unique **for one residual**, not necessarily different across the grid. Thus
one may count incidences `B_{p,q}` and sum them, but cannot silently replace
incidence multiplicity by the number of distinct pairs.

Nor does a small multiplicity force few failures if there are many possible pairs.
The order argument applied modulo pq only bounds a single fiber. The total
number of candidate pq up to n is not O(log n); generic divisor estimates or
`u<sqrt(n)` do not supply the needed restriction to the actual two-power grid.

## A bounded all-failing incidence model

FINITE_CERTIFICATES supplies sixteen positive integers `m_i=p_i q_i` below
`N=4,000,000`. All 32 primes are distinct, 3 mod 4, greater than 1000 and less
than 2000. In particular each exceeds N^(1/4).

Every m_i passes L2,L3,L7,L11, every quotient u_i=1 is a Gaussian norm, and
**every m_i fails** the norm test. Each bad prime occurs at only one point;
each pair and assigned divisor occurs at only one point as well.

This disproves the purely combinatorial implication

`local conditions + pq<=N + small u + injective divisor assignment + tiny prime fibers`
`=> a norm survivor`.

It is **not** a literal `n-3^c-5^d` grid and therefore does not disprove the
original problem, nor a theorem that genuinely uses its additive relations.
Its value is to isolate the missing information: product size and incidence
sparsity alone cannot prohibit complete coverage.

For arbitrary finite H the same conceptual countermodel can be obtained using
2H distinct 3 mod 4 primes in a sufficiently high dyadic interval. Such intervals
exist by divergence of their reciprocal prime series (otherwise their dyadic
counts would eventually be bounded and the series would converge). If the
interval is `[T,2T]`, use ambient bound `4T^2+1`; all products fit, and all its
primes exceed the fourth root for large T. Thus the obstruction is not peculiar
to sixteen points.

## Direct equation and divisor switching

In the actual tail the equation is
\[
3^c+5^d+pqu=n,
\quad p,q>n^{1/4},\quad p,q=3\pmod4,
\quad u\in\mathcal S_2,\quad u<\sqrt n.
\]
Fixing u or pq produces a sparse exponential congruence problem. Conversely,
fixing (c,d) makes p,q determined by the factorization, so the crude bound is
one tail incidence per point. Neither direction by itself saves any points.
The possible u range is much longer than the logarithmic grid. Summing a
generic divisor bound over the grid loses, rather than gains, relative to G.

The Gaussian fact that u is a norm is already true in the all-failing model.
It must be combined with additional common-n arithmetic, not counted as an
independent source of saving. No estimate `V_y=o(G)` or `V_y<T(y;n)` has been
established here.

## Phase K's same-local-cell adversarial pair

At `(c,d)=(3,2)`:
\[
28280-27-25=28228=2^2+168^2=4\cdot7057,
\]
whereas
\[
915320-27-25=915268=4\cdot19\cdot12043.
\]
Both targets are 560 mod 27720 and 8 mod 16; both residuals pass the four filters.
Their full bad kernels differ: 1 versus 19*12043. All prime factors are certified
by trial division in the reference checks.

A claim using only this common local data fails this test. The missing inequality
in MISSING_LEMMA explicitly uses actual large-prime kernels over the entire grid,
so it distinguishes the available arithmetic information; this distinction is
not a proof of that inequality.
