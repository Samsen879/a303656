# C22: independent referee of the two-core-event correction

## Verdict

ACCEPT, with the same hypotheses and order of operations as the audited C21 theorem. This is a strengthening discovered in the current triage; it is not attributed to the original R2 report. The root count becomes at least 23, while LP and the original conjecture remain open.

## Exact statement

Let Q,T be disjoint finite sets of odd inert primes. Every prime in Q is regular for at least one of bases 3,5; prime 3 uses base 5. Give arbitrary finite norm precisions and residues at Q, one arbitrary finite 2-adic norm condition, and arbitrary unit-avoidance target residues at T. If |T|<=22, a positive-measure clopen exponent set satisfies all norm conditions and avoids all T targets in the joint eventual-power model.

All dependencies in the original C21 proof remain the same except the numerical target budget 22 and the following improved critical-core union bound.

## Two-core-event lemma

Fix a finite 2-primary exponent cylinder of positive Haar measure. On it, define

    E7 = {T3(alpha)+T5(beta)=z7 mod7},
    E11 = {T3(alpha)+T5(beta)=z11 mod11}.

The orders at 7 are 6 for both bases, so after fixing the 2-primary coordinates E7 depends only on (alpha_3,beta_3) mod3. The orders at 11 are 5 for both bases, so E11 depends only on (alpha_5,beta_5) mod5. These pairs of primary coordinates are independent Haar. Consequently E7 and E11 are independent for every fixed choice of targets and the fixed 2-cylinder.

Writing a=Pr(E7), b=Pr(E11), the existing exact bounds give 0<=a<=1/3 and 0<=b<=3/25. The function a+b-ab is increasing in both arguments on [0,1]^2. Hence

    Pr(E7 union E11)=a+b-ab <= 1-(1-1/3)(1-3/25)=31/75.

The old worst-case budget was 34/75. The improvement of the upper bound is 1/25. It would be incorrect to claim that the actual intersection always has mass at least 1/25; that is neither asserted nor needed.

If 7 or 11 is absent from Q union T, one may adjoin an arbitrary dummy unit-avoidance event at that prime. Proving positivity for the stronger event system suffices. This occurs only in the direct critical-branch union bound; it does not increase the recursive target-count budget. If the prime is already in Q or T, disjointness ensures there is exactly one associated residue condition.

## Filtration and restoration check

The critical branch first deletes regular norm factors at primes greater than M using positive-mass equivalence, not conditioning. Prime 3 is handled by beta parity, and then the proof chooses a pure 2-primary cylinder satisfying the 2-norm condition. Thus the whole odd Haar space remains available when the core union bound is applied. No lower odd norm-success event has been conditioned on. In particular, the primitive-unit E2 selectors, which can impose beta mod3 or mod9 restrictions, are outside this lemma's conditioning scope.

Regular factors are restored in increasing prime order after the direct avoidance construction. Their exponent coordinates are absent from every target order and from smaller norm conditions, exactly as in the audited C21 proof.

## Induction and finite budgets

Handle M<=7 first as the base case, including T={3}, M=2. If t=|T_M|<M, remove the t active targets, possibly replace the regular M-norm condition by one unit target at M, and invoke the lower-M induction. Target count is at most |T|-t+1<=22. The fresh M-fibre has bad mass at most t/M<1.

For the remaining critical branch, t>=M and |T|<=22 imply M in {11,13,17,19}. No additional order-prime category is introduced. The same H<512, P+(order)<=19 catalog is complete, with the same unknown-tail bound 1/512. Replace only the core term C_M by C_M-1/25 for M>=11, retaining the original active and inactive top-k allocations. There are 1+12+10+6+4=33 exact budget inequalities, including the M<=7 base.

Independent recomputation started from the products over the 80 odd 19-smooth exponents h<512. It used integer gcd, complete trial factorization, first-return multiplicative orders, and direct parity convolutions at 11,71,271. It recovered 60 prime factors, the 613-digit gcd, and 46 inert catalog rows. All 33 budgets are strictly below one.

    Base budget = 155932663/190512000.
    Maximum budget, M=t=11 = 4238011529/4390848000.
    Minimum good margin = 152836471/4390848000 > 0.

The probability independence was also checked directly in all four parity cylinders on the 225-cell joint order quotient; these computations corroborate the disjoint-coordinate proof.

## Finite-zero corollary

After deleting everywhere-positive split factors and first-power inert factors, use the theorem with T equal to the remaining joint-nonregular inert primes and Q equal to the remaining regular primes. If |T|<=22, the original finite integrand is positive on a positive-measure exponent set. Therefore

    f_q(a)=0 => at least 23 distinct primes p>3 with
    p=3 mod4, p^2 | q, and 3^(p-1)=5^(p-1)=1 mod p^2.

No assertion bounds the global number of such primes. No assertion removes ordinary small-exponent transient rows. The result does not change the repository C=1 seven-root certificate.

## Reproducible artifacts

- c22_independent_budget.py: independent exact catalog and budget reconstruction.
- c22_independent_budget.json: all 33 rational budgets, margins, and catalog rows.

Both files are located alongside this referee note. No external writes or repository changes were made.
