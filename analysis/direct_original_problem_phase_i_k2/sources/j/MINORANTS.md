# Finite-local support obstruction and the classical sieve comparison

This is mechanism 3. Theorems here block named classes, not every witness-sensitive sieve.

## Theorem J-M1 (finite-interval periodic minorant obstruction)

Let I be an interval containing L consecutive positive integers, M>=1, and let p=3 mod 4 be a prime not dividing M. Let f be M-periodic on the integers (its values and M may depend on the target n). Suppose

    f(m)<=1_{S2}(m) for every m in I,
    L>=M*p^2.

Then f is nonpositive on every residue class modulo M.

### Proof

For each residue a modulo M, CRT gives one class modulo M p^2 satisfying

    m=a mod M,  m=p mod p^2.

Every block of M p^2 consecutive integers contains a representative of that class. This representative has v_p(m)=1, so it is not a norm. Therefore f(a)=f(m)<=0. This works for every a. QED.

The global version needs no interval-length qualification: a fixed-period function which minorizes the norm indicator for all positive integers is everywhere nonpositive. It also applies to any periodic function whose positivity alone implies being a norm.

## Corollary J-M2 (arbitrary truncated divisor features)

Any function, linear or nonlinear, of the features 1_{d|m} for 1<=d<=H has period M=lcm(1,...,H). If the interval condition in J-M1 holds, it cannot be a nontrivial positive norm minorant on that whole interval. This includes sum_{d<=H} alpha_d(n) 1_{d|m}; allowing target-dependent coefficients does not help.

An entirely elementary sufficient condition avoiding any prime-distribution theorem is

    L >= 16*(H!)^3.

Choose a prime p=3 mod 4 dividing 4M-1; at least one exists and none divides M. Then p<4M, so M p^2<16M^3<=16(H!)^3. This sufficient condition is crude; the exact M p^2 condition is the actual theorem. It is NOT a prohibition on all polylogarithmic cutoffs, let alone on sieve level n^epsilon.

## Preservation of the local norm conditions

The same proof applies within a fixed admissible congruence class. To preserve a chosen m0's exact v2=t, even v3=e, and oddpart=1 mod 4, refine M to a multiple of 2^(t+2)3^(e+1) and preserve m0 modulo that modulus. Choose p>=7 outside it. The CRT nonnorm still passes L2 and L3; parity then supplies a second odd-valuation bad prime automatically. Complete valuations at any other fixed finite set of primes can similarly be preserved by adjoining their p^(v_p(m0)+1) moduli. The interval condition uses this REFINED modulus.

Concrete collision: in [1960,3920], 1994=2*997=25^2+37^2 is a norm, while 2114=2*7*151 is not. Both are 74 mod 120, and both pass L2/L3. Thus divisibility features d<=5, even supplemented by that congruence class, cannot distinguish them. This is one explicit class collision; it is not a claim that J-M1's all-class interval-length hypothesis holds for this short interval.

## What is NOT excluded

Weights depending on large prime pairs; on a divisor range whose period exceeds the interval; on more target-specific information than the fixed features; or whose inequality is only required at the actual sparse residuals are outside this obstruction. So are the exact r2 function and Psi_n: neither is a fixed-small-feature periodic function on the entire interval.

## Classical genuine norm minorant exists at a demanding level

Let P3(z) be the product of bad primes <=z. A lower sieve weight applied to gcd(m,P3(z)) satisfies

    sum_{d|gcd(m,P3(z))} lambda_d^- <= 1_{gcd(m,P3(z))=1}.

On the L2 domain m<=n, take z>=sqrt(n). If m fails, two distinct odd-valuation bad primes divide m; at least one is <=sqrt(m)<=z. Thus the right side is zero for every failure, and this IS a genuine norm minorant. It discards some valid norms having an even power of a small bad prime, but that is permitted for a lower bound.

If z<sqrt(n), truncated coprimality alone is NOT a norm witness: two larger bad primes may remain. Bad-kernel sieving does not fix the issue merely by renaming the truncated kernel.

The standard half-dimensional lower sieve requires a distribution level D with log(D)/log(z)>1 for a positive main-term coefficient, plus control of its remainders. At z around sqrt(n), that means a level beyond that sieve threshold, not just logarithmically many exponent samples. The supplied local-count theorem does not supply such distribution. No weighted signed-remainder substitute has been established here. This is why the periodic obstruction and the existence of deep classical lower weights are consistent.

## Level-D conclusion

A reusable, fully range-qualified theorem rules out the finite-local, short-truncated-feature subroute. It does not prove that the full direct route is impossible. Since the exact Phase I archive was unavailable, project-level novelty and any claimed comparison to PW-02 remain unaudited.
