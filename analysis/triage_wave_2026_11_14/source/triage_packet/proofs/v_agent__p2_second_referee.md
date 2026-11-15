# P2 second independent high-risk referee

## Verdict and audited statement

**ACCEPT the stated negative structural theorem.** I independently read the final main report Sections 4-5, FULL_QUARTER_MEAN.md, POSITIVE_DENSITY_UPGRADE.md, the relevant quarter-kernel budget/deduplication proof and GAMMA_AVERAGE_AUDIT.md, and reconstructed the argument. I also reopened the published Nowak 2005 primary paper and the fixed-progression Mertens primary reference. No gap was found in the four user-prioritized risks: boundary, moving cutoff, duplicate kernel labels, and uniform pair-sieve/actual-difference averaging.

The accepted statement is: with the literal repository quarter-tail T_y, actual failure incidences V_y=T_y-R, distinct actually occurring bad-kernel labels K_y, and y=n^(1/4), every fixed real C with (C-1)kappa>1 satisfies

    #{X<=n<2X : C K_y(n)>T_y(n)} >>_C X

for every sufficiently large X, where

    kappa = (1/4) integral_{1/2}^1
       log(4t-1)/(t sqrt(1-t)) dt.

In particular all C>=5 share the C=5 lower bound and starting threshold. There is no claimed effective numerical starting threshold.

This is a negative theorem about the specified constant-times-distinct-label completion. It is not an A303656 counterexample, and does not settle the eventual C=4 question or the original weak inequality.

## 1. Exact kernel structure and inherited filters

For a positive residual m=n-3^c-5^d counted by V_y, the oddpart condition makes the number of distinct odd-valuation inert primes positive and even. Every such prime exceeds n^(1/4). Four would have product >n, impossible. If one of the two had valuation at least 3, p^3 q>n would again be impossible. Thus m=pq u uniquely at the level of the unordered bad-kernel primes, where p<q, p,q>n^(1/4), v_p(m)=v_q(m)=1, and u is a positive sum of two squares.

Conversely, for X>=11^4, such a literal factorization satisfies the G23711 filters: neither p nor q is 3,7,11; u has even valuations at these primes; pq is 1 mod4, so oddpart(m) is 1 mod4. Zero residuals belong to R and T but not V or K, and are kept separate wherever reciprocals occur.

## 2. Uniform first moment and the pq~X boundary

The final main report uses H_X=D(X/2). Its cardinality is h_X+O(log X), where h_X=(log X)^2/(log3 log5), and D(2X) minus this core has O(log X) indexed pairs. The older FULL_QUARTER_MEAN supplement uses D(X/log^2 X) and O(log X loglog X) boundary pairs. Both are valid auxiliary choices; the stronger final version follows by endpoint subtraction with s/X in [0,1/2]. These are not conflicting definitions of the actual D(n).

Landau's scalar asymptotic is uniform at the two core residual endpoints in [X/2,2X]. The coefficients of the two leading terms differ by exactly the interval length X. This proves sum R~M_X, M_X=K_LR X h_X/sqrt(log X).

For any shift s<=2X, ignoring lower target boundaries only enlarges the quarter-tail count. Fix u in S2, u>0. For p>X^(1/4), p<=sqrt(2X/u), Chebyshev gives

    #q <= pi(2X/(up)) << X/(up log X),

because the argument is at least X^(1/4) whenever such a prime pair is possible. The p reciprocal sum in [X^(1/4),sqrt(2X)] is O(1). Landau partial summation gives

    sum_{u<=U,u in S2,u>0} 1/u << sqrt(log(2U)).

Thus every shift contributes O(X/sqrt(log X)) tail incidences, uniformly in s. This justifies discarding the noncore shifts; norm counting alone would not have done so.

If pq>X^(1-delta), then u<=2X^delta. The exact same argument proves

    boundary_per_shift
      << sqrt(delta) X/sqrt(log X)+X/log X,

with an absolute constant uniform for 0<delta<1/4. This is the required control at pq~X; no Landau asymptotic is used for bounded cofactors.

For fixed delta, pq<=X^(1-delta) makes both cofactor endpoints >=X^delta/2. Scalar Landau subtraction is then uniform in p,q and core shift s. Fixed-4 Mertens partial summation gives the two-dimensional prime measure. The coefficient 1/8 is correct: two prime-density factors 1/2 and one unordered-pair factor 1/2. Integration along a+b=t gives the stated kappa_delta with coefficient 1/4.

The resulting inequalities are

    liminf_{X->infinity} sum V_y/M_X >= kappa_delta,
    limsup_{X->infinity} sum V_y/M_X <= kappa_delta+C sqrt(delta).

First X tends to infinity at fixed delta; then delta decreases to zero. The omitted integral is integrable at t=1, and the boundary constant is independent of delta. Therefore sum V_y~kappa M_X. There is no interchange requiring a uniform asymptotic for delta=delta(X).

## 3. Moving n^(1/4) and valuation-three repair

In the compact interior, the provisional cutoff X^(1/4) can disagree with n^(1/4) only when the smaller kernel prime lies in

    [X^(1/4),(2X)^(1/4)].

Outside that strip p>(2X)^(1/4), q>p. If either p or q divided the norm cofactor u, its valuation in u would be at least 2, forcing p^3 q>2X (or p q^3>2X). Thus the same strip also catches all possible valuation>=3 discrepancies in the provisional count.

The strip's reciprocal mass is O(1/log X), the q mass is O(1), and the fixed-delta Landau upper bound for each pair is O_delta(X/(pq sqrt(log X))). Hence the error per core shift is O_delta(X/log^(3/2) X), negligible at the required scale. Outside the compact interior, the preceding uniform product-boundary estimate already controls everything. This is the correct limit ordering.

## 4. Duplicate kernel loss

Let B_k(n) be the incidence multiplicity of the actual kernel k. Then

    0<=V_y-K_y<=sum_k binom(B_k,2).

For distinct numerical shifts, a shared kernel pq divides nonzero Delta=s_i-s_j. Since |Delta|<=2X, it has at most four prime divisors >X^(1/4) once X is sufficiently large, hence at most six candidate unordered pairs. Each pq>sqrt X yields at most sqrt X+1 targets n in an interval of length X. With O(log^4 X) indexed shift pairs this gives O(sqrt X log^4 X).

Equal numerical shifts must be counted separately. Orient them so that

    3^c(3^h-1)=5^d(5^k-1), h,k>=1.

LTE gives c=v_3(5^k-1)<=1+log_3 k=O(loglog X), and d=v_5(3^h-1) is fixed by h. For each (c,h), the equation determines k at most once, so there are O(log X loglog X) distinct indexed collision pairs. Each such pair can share only the unique residual kernel at any given n. Their total contribution is O(X log X loglog X).

Consequently

    sum(V_y-K_y)
      << sqrt X log^4 X + X log X loglog X
      = o(X log^(3/2) X).

This proves sum K_y~kappa M_X and sum T_y~(1+kappa)M_X without assuming label injectivity.

## 5. Uniform truncated pair sieve, including Delta~X

The proof correctly uses Nowak 2005 **Lemma 1**, a finite sieve inequality for arbitrary residue systems; it does not substitute his full-norm correlation theorem for truncated T_y.

For inert p<X^(1/4), p not dividing Delta, set only

    Omega(p^2)={s_i+jp,s_j+jp mod p^2 : 1<=j<p},

with all other levels empty. This removes exactly valuation one, never valuation two or zero residual. The two roots modulo p are distinct, so there are 2(p-1) excluded classes. Layer disjointness is automatic and

    theta(p^2)=1-2(p-1)/p^2>0,
    theta(p^2)^(-1)-1 >= 2/p,

including p=3. Apply the finite inequality with x=2X and sieve parameter Y=sqrt X. Keeping only d=t^2 gives the lower denominator sum over squarefree inert t<X^(1/4), coprime to Delta.

With w(t)=mu(t)^2 2^omega(t)/t on inert-supported t and Gamma(Delta)=product_{p|Delta,p inert}(1+2/p), multiplicative splitting gives

    Gamma(Delta) V_Y >= sum_{t<X^(1/4)}w(t).

The latter is >>log X with an absolute starting threshold: use the finite Euler product P(z)=product_{p<=z,inert}(1+2/p) comparable to log z, take z=Z^epsilon for a fixed small epsilon, and apply Markov to log t under normalized weights w(t)/P(z). Its mean is O(log z), so a fixed positive fraction of the weight lies at t<Z. No Delta-dependent Tauberian threshold is introduced.

This proves

    pair_count << X Gamma(Delta)/log X

uniformly for 0<|Delta|<=2X. The requested nonprimitive-coefficient concern is bypassed legitimately: the proof is a direct residue-system sieve for n-s_i and n-s_j, both with leading coefficient 1. No theorem about arbitrary nonprimitive affine coefficients is invoked or asserted.

## 6. Averaging Gamma on the actual shift grid

For w as above, fixed-4 Mertens gives sum_{r<=2X}w(r)<<log X. If ord_r(5)<=z, then r divides product_{j<=z}(5^j-1), whose logarithm is O(z^2). Splitting its prime divisors at z^2 proves

    sum_{ord_r5<=z}w(r)<<log(2z),

and nonnegative Tonelli yields the convergent weighted Romanoff series sum_r w(r)/ord_r5.

For actual nonzero shift differences, first expand Gamma(Delta)=sum_{r|Delta}w(r), which restricts r<=2X. After this finite truncation, enlarge the grid to the full containing rectangle. Fixing c_i,c_j,d_j leaves one congruence for 5^(d_i), with at most O(log X/ord_r5+1) solutions. This gives

    sum_{s_i!=s_j}Gamma(s_i-s_j)<<log^4 X.

It is legal to allow equal shifts in this upper congruence count because the divisor range was already truncated using the original nonzero differences. Gamma(0) is never expanded.

For the true zero-difference contribution to T_y^2, every numerical shift has multiplicity at most two. Three positive-sum representations would force the middle powers to be <s/3 and <s/5. Thus the number of equal-shift ordered pairs is O(log^2 X), and their crude total is O(X log^2 X). Together with the pair bound this proves

    sum T_y(n)^2 << X log^3 X.

## 7. Positive-density deduction and exclusions

The exact first moments give

    sum(C K_y-T_y)/sum R -> (C-1)kappa-1.

When the limit is positive, sum(C K_y-T_y)>>_C X log^(3/2) X. Since (C K_y-T_y)_+<=C T_y, Cauchy with the preceding second moment gives a positive proportion of targets, for every sufficiently large dyadic X.

The analytic lower bound kappa>3/10 in the final report is correct: after r=sqrt(1-t), log z>2(z-1)/(z+1) and the first four positive atanh terms give kappa>477/(1120 sqrt2)>3/10. Hence C=5 has a fixed positive margin. No floating-point quadrature is needed for the theorem.

This audit does not revalidate the separate Baker-Davenport constant-2 certificate, all optional private-prime incidence laws, or the C=4 finite numerical example. None is needed for the accepted C>=5 negative theorem. The final main report's D(X/2) core and the older supplement's D(X/log^2 X) core are compatible proof variants, not an unresolved contradiction.

## Primary references reopened

- Nowak, published 2005, Lemma 1, printed p.73: https://doiserbia.nb.rs/ft.aspx?id=0350-13020591071N . Also independently checked the arXiv text https://arxiv.org/pdf/math/0410010 .
- Languasco-Zaccagnini, fixed-progression Mertens formula (1), explicitly fixed q>=3 and (a,q)=1: https://arxiv.org/pdf/0906.2132 . Used only at q=4,a=3.

