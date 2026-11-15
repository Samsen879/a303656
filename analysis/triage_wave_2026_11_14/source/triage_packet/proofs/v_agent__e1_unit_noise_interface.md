# E1 primitive profile: new unit-noise interface and exact finite gate

## Verdict

**ACCEPT.** The E1 C32 primitive profile is exactly a fixed-noise convolution, up to its constant mass 15/32. The newly refereed A2 unit-noise method applies without a missing definition or model change. It converts E1's MP-LT condition into an exact finite primitive positivity gate. This supersedes the earlier assessment that E1 still requires a separate quantitative lower-quantile hypothesis after finite positivity.

The original weighted norm LP/POS is still a different assertion and is not substituted for this primitive gate. The E1 and E2 canonical primitive gates are also different; no global equivalence between them has been proved.

## 1. Exact identification of E1's noise

Let C32 be the 15 residue classes modulo 32 characterized by v2(r)<=3 and oddpart(r)=1 mod4. Define the **probability** noise nu_E1 on the profinite integers by

    at 2:  (32/15) 1_C32(r) dH_2(r);
    at odd inert p: normalized Haar on Z_p^times;
    at split p: additive Haar on Z_p.

Let rho_E1=mu*nu_E1, with the original full joint eventual-power shift law mu. For W_Q=product_{p<=Q,p inert}p, the finite-prefix density is

    F_Q(x) = (32/15) E_exponents[
       1_C32(x_2-s_2)
       product_{p<=Q,p inert}(1-1/p)^(-1)1_{p not dividing x_p-s_p}]
           = (32/15) P_Q^(32)(x).

This is exactly the profile of E1 proof 05, Section 7, and the main report. In particular P_Q has Haar mean m=15/32. It is not E2's all-odd-prime unit profile and is not the r2-weighted norm density.

Full output prefixes at p<=Q may include the split coordinates, but the density is independent of them because their noise is Haar. The finite prefix is locally constant modulo 32 W_Q. No assumption about independent local exponent distributions is involved.

Equivalently, if tau_0 has 2-adic Haar on 1+4Z_2, inert units, and split additive Haar, the unnormalized E1 noise is the fixed four-scale mixture

    (15/32)nu_E1
      =sum_{j=0}^3 2^(-j-2) (2^j)_*tau_0.

The normalized mixture weights are 8/15,4/15,2/15,1/15. This is a fixed mixture of scales 1,2,4,8, not a target-dependent selection of lambda=1,2,18.

## 2. Support theorem applies

For P>=5 condition on all full exponent coordinates at every prime <=P, including split primes. Those source coordinates may occur in the orders of inert output primes, so omitting them would be incorrect.

Tail Fourier coefficients vanish if a conductor contains a split prime, or a repeated inert prime. On an inert-supported squarefree P-rough conductor q, their square is 1/phi(q)^2. Conditional base-5 Parseval consequently gives a tail norm upper bound by

    sum_{q squarefree, inert-supported, P-rough}
      q/[phi(q)^2 r_P(ord_q5)],

which is a subseries of the already refereed unit-noise sum. Its bound is uniform in P and in the full lower source coordinates. The fixed 2-adic kernel is bounded and locally constant, so the same mixture formula establishes global absolute continuity, L2 density and the uniform **relative** conditional L2 estimate.

Let P_infinity=(15/32)F_infinity. Then P_Q is its nonnegative L2 martingale on full-prime prefixes, and

    {P_infinity=0}=union_{Q>=5}{P_Q=0} mod Haar-null.

Because every P_Q is locally constant, every nonempty finite zero set is a positive-measure cylinder. Hence

    [P_Q(x)>0 for every finite Q and every x]
      iff [P_infinity>0 Haar-a.e.].

No LP hypothesis is used to prove this equivalence.

## 3. Exact equivalence with MP-LT

E1 defines

    b_Q(t)=H{P_Q<t},
    T(Q)=sum_{q>Q,(q,5)=1}
          (q/phi(q))^2/[q ord_q5].

The already proved series converges, so T(Q)->0. It is strictly positive for each finite Q: there are arbitrarily large q coprime to 5 and every displayed summand is positive. No quantitative rate is needed here.

For every fixed C>0, the following are equivalent:

    (i) all finite P_Q are everywhere positive;
    (ii) P_infinity>0 Haar-a.e.;
    (iii) inf_{Q>=2,t>0}[b_Q(t)+C T(Q)/t^2]=0.

The constant C can be inserted or removed from the MP-LT statement without changing the condition.

Proof of (ii) => (iii): choose a fixed t>0 with H{P_infinity<2t} small. For that fixed t, L2 convergence implies

    b_Q(t)<=H{P_infinity<2t}
             +H{|P_Q-P_infinity|>=t},

whose second term tends to zero. Also T(Q)/t^2 tends to zero. Choose Q large, and then let the originally chosen t tend to zero. These choices are all made before the integer X-limit in E1. After choosing Q,t, E1 still chooses fixed eta and only then takes X to infinity, so its valid parameter order is preserved.

Proof of (iii) => (i): along an approximating sequence with objective tending to zero, b_Q(t)<1/2 eventually. Since E P_Q=m=15/32,

    m>=t H{P_Q>=t}=t(1-b_Q(t)),

so t<=2m. Strict positivity of T(B) for every finite B then forces Q to tend to infinity. If a finite profile at Q0 vanished on a cylinder E of Haar mass alpha>0, every later profile would vanish there as well: the selector constraints are nested. Thus b_Q(t)>=alpha for every Q>=Q0 and every t>0, a contradiction.

The zero-set identity proves the remaining equivalence. In particular, E1 no longer needs an additional negative-log moment or minimum-value lower bound once finite primitive positivity has been proved.

## 4. Relation to E2's canonical unit gate

E2 uses normalized units at **all** odd primes and a target-dependent choice lambda(x) in {1,2,18}. E1 uses unit conditions only at inert primes, additive Haar at split primes, and the fixed C32 mixture of 2-adic valuation slices 0,1,2,3.

On the E2 branches lambda=1 or 2, a successful E2 selector also satisfies E1's finite primitive requirements after restricting to the inert-prime subset: the residual is in C32 and is a unit at every relevant inert prime. This is a valid restricted implication for those target classes.

On the special E2 classes x=2,4,8,22 mod24, the canonical lambda=18 selector instead has exact v3(residual)=2. E1 requires the residual to be a 3-adic unit. The E2 successful selectors on these classes therefore do not feed E1 by support inclusion. E1 can use its valuation-2 or valuation-3 2-adic slices there, while the canonical E2 scale 18 has 2-adic valuation 1. Conversely E1 imposes no split-prime unit conditions, which E2 does impose.

Consequently there is no global equivalence or global implication between these two finite gates supplied by kernel domination or by the new analytic support theorem. Any such statement for the actual mu would require a further arithmetic argument. The present audit neither assumes nor proves one.

## 5. Safe corollary from the newly refereed universal C22 theorem

This section treats C22 as the independently refereed input; it is an interface check, not a third complete audit of its finite budgets.

Let W be any squarefree product of at most 22 odd inert primes, **counting prime 3 if present**. Apply C22 with no external odd norm conditions, target set T equal to the primes dividing W, arbitrary target residues x mod p, and the finite 2-adic norm condition beta_8(x_2-s_2)>0. Its exact statement permits arbitrary unit-avoidance targets at all these primes, including 3, and yields a positive-measure exponent set.

Therefore

    J_W(x) = [1/(2 V(W))] E[
      beta_8(x-s) 1_{gcd(x-s,W)=1}]

is strictly positive for every x. This is the J_W in E1 proof 05, Section 9A: beta_8 equals the displayed exact S2 AP factor rho_8.

The finite 2-adic comparison in that section is valid for this same joint exponent law. Once odd exponent coordinates and the two exponent parities are fixed, all inert-prime conditions are fixed, because the 2-part of every inert-prime order is at most 2. The higher 2-primary coordinates remain Haar, and the shift is uniform in its fixed mod8 coset. Averaging C32 on these cosets gives

    (1/4,1,1,0,1/2,1,0,0),

while beta_8/2 is

    (1/2,1,1,0,1/2,1,0,0).

Thus pointwise

    (1/2)J_W <= P_W^(32) <= J_W.

It follows that P_W^(32) is everywhere positive whenever W has at most 22 distinct inert prime factors. Hence an E1 finite primitive zero requires **at least 23 distinct inert primes**.

This is not the original norm-model 23-root corollary: it imposes no joint-nonregularity requirement and no p^2 requirement. E1's modulus W is squarefree. The total count here deliberately includes prime 3 and makes no attempt to optimize its role.

## Updated research status

E1 hybrid covariance plus the new support theorem now gives an exact route:

    E1 finite primitive positivity <=> MP-LT
      => actual almost-all representation.

The finite primitive positivity gate is still OPEN. The C22 corollary excludes finite counterprofiles supported on at most 22 inert primes, but supplies no assertion for all finite prime sets. It does not prove original LP, actual almost-all, or the original all-n conjecture.

