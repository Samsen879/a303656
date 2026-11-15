# Second independent referee: A2 unit-noise extension and E2 canonical branches

## Verdict

**ACCEPT with explicit definitions and scope.** I independently reconstructed the Fourier estimate, relative conditional L2 argument, prefix normalization, and limiting lower-tail identity before consulting the other referee's proof text. No new research hypothesis is needed for the support theorem beyond the already audited A2 smooth-order/rough-conductor estimate. The canonical finite positivity assertion remains OPEN. The theorem below does not identify it with the original weighted norm LP and does not give an unconditional almost-all theorem.

The essential conventions are: mu is the original joint eventual-power law of T3(alpha)+T5(beta), with alpha,beta independent Haar elements of the entire profinite integers, and every cross-prime order dependency retained; all Haar measures on proper compact subsets are normalized probability measures; the prefix filtration contains **complete** p-adic output coordinates and the conditional source past contains **complete** lower exponent coordinates.

## 1. The measure and its prefix density

Let G=product_p Z_p with product additive Haar H. Define the probability measure

    tau = Haar_probability(1+4 Z_2)
          x product_{p odd} Haar_probability(Z_p^times).

For lambda in {1,2,18}, let rho_lambda=mu*(lambda_*tau), where lambda_* is multiplication by the integer lambda. For Y>=5, let F_Y be the sigma-field of all full output coordinates at p<=Y. Set

    q_Y = product_{3<=p<=Y} p,
    V_Y = product_{3<=p<=Y}(1-1/p).

The local density of lambda_*tau is

    p=2: 2^(v_2(lambda)+2)
         1_{r == lambda mod 2^(v_2(lambda)+2)},

    p odd: p^(v_p(lambda))/(1-1/p)
           1_{v_p(r)=v_p(lambda)}.

Consequently the finite-prefix kernel K_lambda,Y is bounded and locally constant and has constant nonzero value

    product_local_constants = 4 lambda / V_Y.

Its support is exactly

    r == lambda mod 4 lambda,
    gcd(r/lambda,q_Y)=1.

The second condition is read after the first gives divisibility by lambda. At p|lambda the second condition is necessary: it imposes exact v_p(r)=v_p(lambda), not merely r divisible by lambda. In particular lambda=18 requires exact v_3(r)=2, detected modulo 27, and this is present in 4 lambda q_Y=72 q_Y.

Thus, for every x and Y>=5,

    G_lambda,Y(x) = (4 lambda/V_Y) a_lambda,Y(x),

where a_lambda,Y is precisely the E2 limiting exponent-pair fraction satisfying the two selector congruences. Both sides are canonical locally constant functions of x modulo 4 lambda q_Y. This equality does not need a local-constancy theorem for mu: convolution with K_lambda,Y already preserves its finite additive period.

For a finite normalization check, when q=15, the supports have 8 residues in moduli 60,120,1080 for lambda=1,2,18, respectively. The densities are 15/2,15,135. At q=105, the supports have 48 residues in moduli 420,840,7560, giving 35/4,35/2,315/2. I enumerated both the congruence definition and the local exact-valuation definition independently and obtained exact agreement. These checks confirm the formulas but do not replace their proof.

## 2. Uniform conditional tail L2

Fix integer P>=5 and condition on theta=(alpha_l,beta_l) for every prime l<=P, with full l-adic coordinates, not finitely many digits. The remaining exponent coordinates remain independent Haar. For every output prime p<=P, T3 and T5 depend only on this theta because the prime factors of ord_{p^k}(b) are <=p, while the own-base coordinate is zero. This keeps the actual arithmetic dependence rather than replacing it by independent local powers.

For p>P, lambda is a unit and multiplication by lambda preserves normalized Haar on Z_p^times. Its additive Fourier coefficient at a primitive character of conductor p^k is -1/(p-1) when k=1, and zero for k>=2. Therefore only squarefree P-rough conductors q contribute, and

    |tau_hat(a/q)|^2 = 1/phi(q)^2.

Write r_P(t)=t/product_{l<=P}l^(v_l(t)). Conditional on theta, the base-5 power modulo q is uniform on a multiplicative coset of cardinality r_P(ord_q 5). Full finite Parseval gives

    sum_{a mod q}|sigma_5,theta_hat(a/q)|^2
       = q/r_P(ord_q 5).

The conditional base-3 factor has modulus <=1. Enlarging primitive numerator sums to all numerators therefore gives the tail square norm bound

    C_unit(P) = sum_{q squarefree, (q,Q_P)=1}
       q/[phi(q)^2 r_P(ord_q 5)].

This sum is uniformly bounded in P. To see it directly, for T>=1 put Y=max(P,T) and sum q/phi(q)^2 over those q with r_P(ord_q5)<=T. Every prime divisor p of such q has Y-smooth ord_p5, so this partial sum is at most

    product_{p>P, P^+(ord_p5)<=Y} [1+p/(p-1)^2].

The exact identity

    1+p/(p-1)^2
     = (1-1/p)^(-1) [1+1/(p(p-1))]

reduces the product to the A2 product bound multiplied by an absolutely convergent, uniformly bounded Euler product. The audited A2 smooth-order harmonic-tail estimate and the Mertens product ratio yield

    A_unit,P(T) << max(1,log T/log P).

Tonelli integration against dT/T^2 gives C_unit(P)<=C_unit, with C_unit independent of P and theta. No prime independence, order regularity, or positivity hypothesis occurs here.

Fourier uniqueness and L2 Plancherel now give a jointly measurable normalized conditional tail density g_theta with ||g_theta||_2^2<=C_unit. The measurable version can be chosen by the same countable finite-quotient martingale construction as in A2.

## 3. Absolute continuity, relative L2, and zeros

Let k_theta(x)=K_lambda,P(x-s_{<=P}(theta)). Prefix and tail noise coordinates are independent. Hence the convolution law has the density

    G_lambda(x,y) = integral k_theta(x) g_theta(y) dtheta,
    G_lambda,P(x) = integral k_theta(x) dtheta.

For P=5 this proves global absolute continuity and L2 integrability, since K_lambda,5 is bounded and has finite Haar mass. Weighted Cauchy-Schwarz, followed by Tonelli, gives at every admissible x with G_lambda,P(x)>0

    integral [G_lambda(x,y)/G_lambda,P(x)]^2 dH_{>P}(y)
       <= C_unit.

At a prefix zero, the future density is zero almost everywhere. At a positive prefix, the support of the future normalized density has Haar measure at least C_unit^(-1).

Let A_lambda={G_lambda>0}. Thus

    E_H[1_{A_lambda}|F_P]
       >= C_unit^(-1) 1_{G_lambda,P>0}.

The sigma-fields F_P increase to the whole product Borel sigma-field. Levy upward convergence consequently proves

    {G_lambda=0} = union_{P>=5}{G_lambda,P=0}   mod H-null.

This is the desired new support theorem. Finite-prefix zero sets are finite unions of clopen arithmetic cylinders. The result uses **uniform relative** conditional L2; ordinary nonnegative-martingale convergence alone would not suffice.

## 4. Canonical E2 scheme and Delta_Y

Use exactly E2's canonical scale function

    lambda(x)=1 if x is odd;
    lambda(x)=18 if x mod24 lies in {2,4,8,22};
    lambda(x)=2 for the other even classes.

This function is F_5-measurable. Let

    H_Y(x)=G_{lambda(x),Y}(x),
    H_infinity(x)=G_{lambda(x)}(x).

Then H_Y=E_H[H_infinity|F_Y] for Y>=5. It is a nonnegative L2 martingale. It is **not necessary, and is not asserted, that its integral equal 1**: the piecewise choice of lambda need not retain probability normalization.

Piecewise application of the support theorem gives

    {H_infinity=0}
      = union_{Y>=5}{H_Y=0}
      = union_{Y>=5}{a_Y=0}                 mod H-null.

All three scales have prime factors <=3, so no missing prefix occurs. The canonical condition is already determined on every original E2 branch: lambda=1 uses modulus 4q_Y and lambda=2,18 use 8q_Y,72q_Y. The common refinement 72q_Y therefore represents the same fractions, not a new selector model.

The E2 threshold event is

    a_Y(x)<Y^(-1/4)
    iff H_Y(x)<(4 lambda(x)/V_Y)Y^(-1/4).

The latter threshold tends to zero, since V_Y^(-1)<<log Y. On {H_infinity>0}, martingale convergence makes the threshold indicator eventually zero. On {H_infinity=0}, the support theorem places almost every point in a finite-prefix zero set, after which every further a_Y is exactly zero by the nested selector constraints. Thus the threshold indicator tends almost everywhere to 1_{H_infinity=0}. Dominated convergence proves

    lim_{Y->infinity} Delta_Y
      = H({H_infinity=0})
      = H(union_Y{a_Y=0}).

Each finite canonical zero is a nonempty clopen cylinder of positive Haar mass, and the zero sets increase as Y grows. Hence

    Delta_Y -> 0
    iff a_Y(r)>0 for every finite Y>=5 and every r mod72q_Y.

No quantitative lower bound for the minimum positive a_Y(r), no negative-log moment bound, and no effective rate in Y is required for this equivalence. The theorem supplies a qualitative collapse of E2's lower-tail target to its own finite primitive positivity problem.

## 5. Exact consequences and exclusions

1. Combining the new equivalence with E2's previously audited integer bounded-weight reduction gives: **canonical primitive finite positivity implies actual almost-all representation.** This is a conditional theorem, because canonical finite positivity has not been proved.

2. A finite zero branch supplies a permanent obstruction to this canonical selector-abundance condition and makes lim Delta_Y>0. It does **not** by itself give an integer nonrepresentation, a lower bound for actual exception density, or a zero of the original r2-weighted norm profile.

3. Canonical primitive positivity is not original LP. The primitive noise forces exact selected valuations at every prime in the prefix, including units at all other odd primes; the norm noise allows arbitrary even inert valuations. The new support theorem must be labelled as a different measure and a different LP. Its proof uses the A2 analytic method, not an equality of the two profiles.

4. mu is the eventual law, and a_Y is a limiting fraction. The finite ordinary initial rows (for example c<3 in the lambda=18 branch, or d=0 at the 5-adic own-base component) have density zero in the growing exponent rectangle and do not change a_Y. They cannot be erased from the original integer problem. E2's positive-fraction implication still concerns genuine ordinary exponent pairs because any positive limiting selector mass is realized by a positive proportion of the actual large rectangles.

5. The strongest audit dependencies are the corrected, already refereed A2 smooth-order estimate and the full-lower-coordinate conditioning convention. No unconditional LP, POS, or W6 integer SM is used in the new support theorem.

6. The original norm-model C21/22-root obstruction threshold does not transfer to this primitive LP. Here all odd primes, including split and regular primes, impose unit avoidance. C21 permits external regular **norm** conditions, which are weaker and structurally different. Only A2's analytic tail method has been transferred, not the norm-model finite-obstruction classification.

## Referee conclusion

The proposed theorem is mathematically coherent with the supplied A2 and E2 models. The lambda=18 prime-power interface, full exponent dependence, tail Fourier weights, absolute continuity, finite-prefix local constancy, canonical piecewise martingale, and vanishing-threshold limit all check out. No decisive gap was found. Promote the exact support/lower-tail equivalence with the new measure stated explicitly; retain canonical primitive finite positivity as an exact open arithmetic target.

