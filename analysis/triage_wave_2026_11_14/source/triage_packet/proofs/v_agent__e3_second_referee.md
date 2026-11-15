# E3 second independent referee: fixed-W nonnegative exponent reweighting

## Verdict

**ACCEPT the fixed-W classwise Cauchy ceiling in Section 4 and the general omitted-residue extension in Appendix D.** I read these proofs directly, independently reconstructed the weight-uniformity and endpoint arguments, and checked the fixed-modulus AP input in a primary paper. No decisive gap was found.

This acceptance concerns the true S2 indicator with arbitrary finite nonnegative exponent weights depending on X and n mod W. It does not automatically accept all separate signed-weight, bounded-residual-weight, sequential-countermodel, or finite-optimization claims in the report.

## Precise accepted statement

Fix W>=1. For every X and W-class a, assign arbitrary finite nonnegative real weights w_{X,a}(c,d) on D(2X). Set

    T_X(n)=sum_{(c,d) in D(2X)} w_{X,n mod W}(c,d)
             1_{S2}(n-3^c-5^d),  X<=n<=2X,

where negative residuals give zero and the zero residual gives one. In a W-cell put A_a=sum T_X, B_a=sum T_X^2, and define Q_W=sum_a A_a^2/B_a with 0/0=0.

For inert p not dividing 15W let

    S_p=<3>+<5> in F_p,
    H_p=F_p minus S_p,
    k_p=|H_p|,
    eta_p=k_p/[p^2(p-k_p)].

Then

    limsup_{X->infinity} sup_{w>=0} Q_W(X;w)/|[X,2X]|
      <= product_{p inert, p not dividing 15W}(1+eta_p)^(-1)
      <1.

In particular 11 not dividing W implies the upper bound 1210/1211.

The theorem bounds this **support certificate**, not the actual support density. Cauchy makes Q_W a lower bound for representable support; an upper bound on this lower-bound certificate cannot be reversed into an upper bound on actual representation density.

## 1. Fixed-modulus norm AP factors are the relevant input

For every fixed modulus q, positive sums of two squares in any residue r have asymptotic K delta_q(r) t/sqrt(log t), with the displayed delta table in the report. I checked the finite valuation-stripping argument: at a nonzero prime-power residue remove the exact known valuation; at a zero residue remove p^k for split p or 2 and p^(2 ceil(k/2)) for inert p, then delete that local modulus. Inert odd valuations are impossible. The resulting multiplier belongs to S2 and has odd part 1 mod4, so this gives an exact bijection with a reduced class and introduces no infinite valuation interchange.

Consequently delta factors multiplicatively at coprime output moduli. In particular, for inert p,

    delta_p(0)=p^(-2),
    delta_p(b)=(p+1)/p^2 for b not zero.

The p^2 here comes from the arithmetic fact that a positive norm divisible by inert p is divisible by p^2. No uniform distribution of exponent pairs modulo p^2, under arbitrary weights or otherwise, is asserted or needed.

The reduced-class input was checked in Gorodetsky, arXiv:2111.12662v4, Section 1A. It is an unconditional background theorem, separate from the later GRH-dependent bias theorem.

## 2. Uniformity for arbitrarily X-dependent weights

Split shifts at s=2X-sqrt X. For every good shift s<=2X-sqrt X and every active residue of any of the finitely many fixed moduli used, the norm first moment on

    [max(0,X-s),2X-s]

equals delta_q(r) F_X(s)(1+o(1)), uniformly in s and r. For s>X the upper endpoint is >=sqrt X, so the scalar AP asymptotic is uniformly valid on the whole tail. For s<=X, one gets a uniform additive approximation over all endpoints 0<=t<=2X by using the scalar asymptotic on [epsilon X,2X], monotonicity below epsilon X, and then epsilon decreasing to zero. Endpoint subtraction has interval length exactly X and yields a uniform relative error because fixed q has a positive minimum among its finitely many active delta values.

The possible zero residual contributes at most one to a column, absorbed by F_X(s)>>sqrt X/sqrt(log X). Inactive residue classes contain no positive norm; the zero residual cannot be an inactive class because delta_q(0)>0.

Every good column has the **same** prescribed hole-event mass ratio, independently of its shift. Nonnegative weights preserve a uniform relative error upon summation. Their size, normalization, and variation with X are immaterial. This is why the final supremum over all nonnegative weights is legitimate.

## 3. Shifts close to 2X and negative residuals

Boundary shifts s>2X-sqrt X can contribute only when n is in the terminal segment E_X=[2X-sqrt X,2X]. Thus their nonnegative contribution is supported on e_a=O_W(sqrt X) targets in a W-cell of size N_a comparable to X/W.

Let c_a=A_a^2/(N_a B_a). The exact inequality

    A_a(boundary)<=sqrt(e_a B_a)

gives, whenever c_a>=eta>0,

    A_a(boundary)/A_a <=sqrt(e_a/(N_a c_a))=o_{W,eta}(1),

uniformly over every possible choice of weights. If c_a is smaller than a fixed eta below the proposed ceiling, no additional argument is needed to bound the certificate. This dichotomy handles arbitrary huge boundary weights and arbitrarily tiny means; it never divides by an uncontrolled first moment.

Negative residuals were set to zero from the start. The boundary argument therefore covers the full D(2X) and cannot be defeated by moving all weight onto shifts near 2X.

## 4. General hole factors and legitimate multiple-prime product

For p not dividing 15, all ordinary powers are units and their residues run in <3> and <5>. Thus every actual shift avoids H_p, with no transient exception. If n mod p is in H_p, then n-s is a nonzero residue mod p for **every** shift s, so each has the same norm first-moment probability

    rho_p=k_p(p+1)/p^2,

while the ordinary counting probability of this output event is q_p=k_p/p.

For a fixed finite prime set P, the joint hole-event first moments factor because delta_{W product p} factors and all the relevant residual residues are units at those p. This factorization holds separately for every shift before weighting. The counting probabilities factor by ordinary output CRT. No cross-prime independence of the eventual exponent measure mu, or of the arbitrary exponent weights, is used.

Inclusion-exclusion gives every exact hole/nonhole pattern. Cauchy within those patterns gives the multiplicative loss

    product_p [rho_p^2/q_p+(1-rho_p)^2/(1-q_p)]
      =product_p(1+eta_p),

because

    (rho_p-q_p)^2/[q_p(1-q_p)]
      =k_p/[p^2(p-k_p)].

For each fixed finite prime set, all errors are uniform over weights using the previous boundary dichotomy. There are finitely many W-cells, so their certificate ceilings sum correctly.

## 5. Infinite product and p=11

The finite prime set is fixed before taking the X-limsup and the supremum over weights. Only after that limit is proved does one take the infimum of the finite-product constants. This is not a growing-modulus AP asymptotic.

Writing s_p=|S_p| gives s_p>=ord_p5 and

    eta_p<=1/(p s_p)<=1/(p ord_p5).

The convergent order series in Section 3 ensures the product is positive and convergent. For primes p=11 or 59 mod60, 3 and 5 are quadratic residues while -1 is not, so 0 is omitted by every shift. There are infinitely many such primes and fixed W removes only finitely many. Hence the product is strictly smaller than one.

At p=11, <3>=<5>={1,3,4,5,9}; their sumset is all ten nonzero residues, so k_11=1 and

    eta_11=1/(11^2*10)=1/1210.

The one-prime ceiling is exactly 1210/1211. The proof remains valid if weights choose only a proper subset of the available shifts: the common omitted residue remains omitted.

## 6. Relation to E2 and prohibited extrapolations

There is no contradiction with E2's growing outer Y. E3 states for every **fixed** W a gap 1-Theta_W>0, which can shrink as W absorbs more hole-primes. It does not give a positive gap uniform in W. A sequence W_j can therefore have the iterated limit j->infinity after X->infinity approach one without violating any E3 ceiling.

In addition, this particular E3 theorem fixes the residual weight to the true indicator 1_{S2}, while E2 uses a bounded triangular residual weight and branch selectors. The report itself correctly separates the exponent-weight and residual-weight axes. This audit does not combine their hypotheses into a theorem allowing both arbitrary choices simultaneously.

Reject the following extrapolations: an upper bound on actual representable density; an obstruction to every growing-W method; arbitrary nonperiodic dependence of weights on n; arbitrary signed cancellation; or a claim that the product proof assumes or proves independent local exponent distributions.

## Primary source checked

Ofir Gorodetsky, Sums of two squares are strongly biased towards quadratic residues, arXiv:2111.12662v4, Section 1A, reduced fixed-modulus background formula:
https://arxiv.org/pdf/2111.12662 . Only that unconditional background result was used, not the GRH-dependent main bias theorem.

