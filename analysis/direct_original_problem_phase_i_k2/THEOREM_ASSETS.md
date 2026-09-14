# Canonical proved assets and quantifier boundaries

Proofs are linked below in byte-identical producer sources. Source names identify
first occurrence in the inspected lineage, not historical priority. Finite
scripts certify finite arithmetic, not analytic proofs or effective thresholds.
No new theorem is invented by this integration. Existing frozen authority and
generated indexes are untouched. Only NEW AUTHORITY rows of the novelty matrix
are curated here as theorem assets; later synonyms do not get new IDs.

## I2 — additive reset

Use the ORIGINAL domain `D(n)={(c,d)>=0:3^c+5^d<=n}` and b(0)=1;
R counts successful exponent pairs, not r2 weights or distinct shifts.

I2-D1, integers X>=2 and 1<=H<=X/2: the count of n in [X,2X] within a
nonnegative distance H of a shift is at most
`4(2H+1)+2(H+1)(floor(log3(2X/H))+floor(log5(2X/H))+2)`.
Hence any explicit residual restriction h(n)=o(n) covers only density zero,
even without requiring a norm. This does not say representable n have density
zero. I2-D2 gives shift-free dyadic subinterval length at least 97X/1700.
I2-D3 bounds small-square-coordinate support by
`(floor(Y)+1)(floor(sqrtX)+1)(floor(log3X)+1)(floor(log5X)+1)`.
All proofs: [DIRECT_THEOREMS.md](sources/i2/DIRECT_THEOREMS.md).

I2-P1: L=log n, C=floor(log3(n/4)), D=floor(log5(n/4)), m=n-3^c-5^d≥n/2.
L2(m)=[oddpart(m)≡1 mod4], L3(m)=[v3(m) even],
T23=sum over the bulk rectangle of L2L3. Uniformly,
`T23=lambda(n mod24)(C+1)(D+1)+O(L^(5/3))` with absolute implied constant.
Lambda is 1/2 if3|n, 5/16 if n odd coprime3, 7/32 in {2,4,8,22} mod24,
and 13/32 in {10,14,16,20}. The proof keeps shared exponent parity and higher
2/3 lifts; no unconditional independent-prime product is substituted.
This is local survival, not a global norm result.

## I4 — pointwise / divisor switching

Definitions: A23 is the SAME L2/L3 bulk survivor set, M=|A23|,
A_q counts q-divisible residuals INSIDE it with pair multiplicity.
All proof details: [POINTWISE_THEOREMS.md](sources/i4/POINTWISE_THEOREMS.md).

PW-01: fixed 0<alpha<1/4, q≤L^alpha, (q,30)=1,
`sum |A_q-M Gamma_q| <<_alpha L^(5/3+4alpha/3)` uniformly for sufficiently
large n. Gamma is a COMMON-truncation joint-period torus density ratio, not
multiplicative and not asserted near1/q. Source construction takes
U=L^((1-alpha)/3), 2^k~U,3^ell~U, discards c<ell, and retains unit bits at2.
This is not polynomial-n level of distribution.

PW-02: any multiset 1≤m_i≤n, fixed0<a<b≤1, bad primes in (n^a,n^b],
N_p divisible or odd-valuation incidences, g(p)=1/p or1/(p+1):
`sum |N_p-Mg(p)| >= M sum g(p)-M²/(a n^a)`.
For M~L² the floor is `(1/2 log(b/a)+o(1))M`. It blocks the conventional
polynomial-band absolute-remainder random-integer model, NOT all signed or
specially supported sieve weights. The finite inequality is elementary; the
asymptotic uses fixed-modulus Mertens, with source citation in LITERATURE.md.

PW-03: odd u>=1, d_u(s)=sum_{h|u}chi4(h)h^(-s), F_u(s)=u^(s/2)d_u(s).
For real s>0, d_u(s)>0. If u≡1 mod4, F_u is EVEN ENTIRE with nonnegative
Taylor coefficients; vanishing order at0 is the number k of DISTINCT odd
bad-prime defects, F_u(0)=r2(u)/4, and a failure satisfies
`F_u(2s)>=2^k F_u(s)>=4F_u(s)`.
The underlying divisor identity alone is classical background; the centered
coefficient/vanishing/dilation structure is the canonical retained asset.

PW-04: Z=F_u/tau(u), omega=(4Z(kappa/L)-Z(2kappa/L))/3.
For u=oddpart(m)≡1 mod4,m≤n, `omega≤Z(0)=r2(m)/(4tau(u))≤b(m)` and
`0≤Z(0)-omega≤(cosh kappa-4cosh(kappa/2)+3)/3`.
For0<kappa≤1, omega>0 on norms and omega≤0 on failures. This exact sign/support
relation yields NO pointwise positivity theorem for its sum over the sparse
grid. Tau(u), not tau(m), is used. Complementary-divisor pairing retains the
possibly NEGATIVE square-root diagonal; see [DIVISOR_SWITCH.md](sources/i4/DIVISOR_SWITCH.md).

AUX-01: y≥n^(1/4), positive bulk residualm<n passing L2 and all bad-prime
even-valuation tests throughy. A failure has EXACTLY two distinct p<q>y,
p,q≡3 mod4, each exponent1, and uniquely m=pqr with b(r)=1,r<n/y².
The resulting pair-count switching identity is exact, not an upper bound.
J-K1/K2 restatements do not create independent theorem records. Pure parity
and size completion is not claimed historically novel.

## J — ONLY the finite-interval strengthening

J-M1: an M-periodic f minorizing b(m) on an interval containing L consecutive
POSITIVE integers, with p≡3 mod4 prime,p∤M and L≥Mp², is nonpositive on EVERY
residue modM. CRT forces m≡p modp² in every class inside the interval.
J-M2: features [d|m] for d≤H have period lcm(1,...,H); the SAME interval
hypothesis applies. Crude sufficient length16(H!)³ is source-proved using a
bad prime dividing4M-1. Refined moduli can preserve complete finite-prime
valuations; their larger length condition must also be retained.
Proof: [MINORANTS.md](sources/j/MINORANTS.md).
The GLOBAL progression obstruction was already I2-L2 background. Only the
explicit interval/feature strengthening is added, not a duplicate global no-go.
Grid-only inequalities, enormous periods, nonlocal/signed methods and large-pair
weights are outside this theorem's scope.

## K — exact full-valuation local layer

Source K defines m>=0 on D(n), Lp=[vp(m) even] for p=3,7,11 and L2 as above
for positive m; all indicators equal1 at m=0. G23711 counts these local pairs;
R≤G23711≤G237≤G23. J(n)=(floor(log3n)+1)(floor(log5n)+1).
Limiting local orbit coefficients are NOT exact periodic finite G counts.

K-L1/L2: rho237=(1/36)sum_{c,d mod6} A2 A3 A7 with explicit rational lift
weights in [LOCAL_MODEL.md](sources/k/LOCAL_MODEL.md). The function period504
differs from the equality-set period168. `rho237>=21/128`, equality iff
7|n and n mod24∈{8,22}, equivalently n mod168∈{56,70}.

K-L3: rho23711=rho237 beta11(n mod11), justified by specific period CRT.
Beta11=1 at0,139/150 at nonzero quadratic residues,89/100 at nonresidues.
`rho23711>=1869/12800`; equality iff the above mod168 condition and
n mod11∈{2,6,7,8,10}. Exact minimizers mod1848:
`238,392,406,560,574,728,910,1064,1414,1568`.
Full function period5544, not1848; no arbitrary-prime independence is claimed.

K-L5: hard mod24 set H={2,4,8,22},
`max_H rho23711=161/768`, `min_other rho23711=2047/9600`, gap23/6400.
This provides a rigorous LOCAL mechanism for the observed hard band, not an
inverse theorem for R=0 or a predictor of every lowest-R target.

K-L4: uniformly in n asymptotically,
`G23711=rho23711 J+O(L^(9/5))`, hence G23711>>L².
The proof balances uncertainty L²/B and period-boundary LB⁴ at B=L^(1/5),
with transients and actual-grid boundary costs explicitly kept.
No usable numerical error constant/threshold at pilot scales is supplied.
Source K-I1 [local-count inverse](sources/k/INVERSE_THEOREMS.md) follows the
coefficient spectrum gap ONLY with G on the left. Substituting R≤G is invalid.

## K2 — three precise stronger-template obstructions

K2-N1: Phase K lower bound plus Landau B(x)<<x/sqrt(logx) gives
`sum_[X,2X] R << X(logX)^(3/2)` and
`#{R>=eta G} << X/(eta sqrt(logX))` for fixedeta>0.
More generally fixedkappa>0,beta<1/2 gives
`#{R>=kappa G/(logn)^beta} << X(logX)^(beta-1/2)=o(X)`.
Therefore these UNIFORM lower-bound shapes are impossible; beta=1/2 and R>0
are not disproved. Averaging refutes a stronger uniform claim, not pointwise
representation. Proof: [LEAST_BAD_PRIME.md](sources/k2/LEAST_BAD_PRIME.md).

K2-N2: for ANY fixed C>0 and realalpha, the atom-free smooth bound
`N_p^G(n)<=CG(n)/(p(logp)^alpha)` fails for arbitrarily large literal n.
Take consecutive primes IN THE3mod4 PROGRESSION p<q<2p, p>19, n=pq+2.
Then pair(0,0) passes all local tests and has least bad primep, so N_p^G>=1
whereas G≤J=O(log²p). Infinitely many balanced pairs follow from divergence
of the progression's reciprocal-prime sum: eventual ratios≥2 would force
convergence. This requires no short-gap conjecture. The source cites Mertens
in [LITERATURE.md](sources/k2/LITERATURE.md), whose relevant formula was checked
against the primary paper during integration. This family is not an original
counterexample: a single failed residual does not imply R=0.

K2-N3: integer A_p>=0,0≤mu_p≤1/2 implies |A_p-mu_p|≥mu_p.
For H~log²n,Q=n^theta and ordinary mu_p=H/(p+1), the absolute sum above2H
is ≥(1/2+o(1))H loglogn. For the source's explicitly COMPARABLE positive smooth
least-prime models c1H/[p(logp)^alpha]≤mu≤c2H/[p(logp)^alpha], alpha>0,
p>max(3,2c2H), the floor is >>H/(logH)^alpha, much larger than H/logn.
This blocks that smooth-main-term + ALL-absolute-discrepancies template, not
signed cancellation, selected weights, genuinely different orbit models, or
all sieve methods. Proof: [SPARSE_GRID_BOUNDS.md](sources/k2/SPARSE_GRID_BOUNDS.md).

No large-prime range collective saving or pointwise norm transfer was proved.
ML-K2 remains UNPROVED; the direct original-n program is PAUSED.
