# Exact local model and minimizer theorems — Phase K2

**Scope:** self-contained mathematical derivations with exhaustive rational certificates. Not externally refereed, not merged authority, and not a representation theorem. The 2/3 density is inherited from I2; the explicit 7/11 extension and classification are the present contribution relative to the inspected inputs. No historical priority claim is made.

## 1. Three different objects

Let D(n)={(c,d)>=0:3^c+5^d<=n}, m=n-3^c-5^d. Let b(m) be the sum-of-two-squares indicator, with b(0)=1. Define

R(n)=sum_{D(n)} b(m).

This counts exponent pairs, including repeated shifts with their multiplicity. It does not count choices of a,b. For m>0 put

L2(m)=[m/2^{v2(m)} = 1 mod4],  Lp(m)=[vp(m) is even] (p=3,7,11).

Set all these local indicators equal to one at m=0. Define G23, G237, G23711 as the numbers of pairs in D(n) passing the indicated local tests. Thus

0 <= R(n) <= G23711(n) <= G237(n) <= G23(n).

The three objects that must not be conflated are:

1. A finite quotient test: is m a sum of two squares modulo M?
2. An exact finite count G(n) on its target-dependent logarithmic grid, with full valuations.
3. An exact *limiting local orbit coefficient* rho(n), obtained by integrating prime-power lifts of exponent states.

Object 3 has a fixed period here. Object 2 does not. Object 1 modulo 2520 or 27720 cannot see the first odd-valuation obstruction at 7 or 11, because these moduli contain only their first powers. The weights below integrate ALL higher prime-power lifts; they do not equate divisibility to failure.

## 2. Definition of the local orbit coefficient

A precise construction is to count the local predicates on complete exponent periods modulo 2^k2,3^k3,7^k7,11^k11, after removing the transient rows c<k3, and then let the depths tend to infinity. At the 2-adic cutoff, leave vp>=k2-1 unresolved: two unit bits, not one, are necessary. At odd p, leave m=0 mod p^kp unresolved. Lower and upper cutoff densities have the same limit; the estimates in Section 6 prove this uniformly in n.

Equivalently the limit is given by the finite rational formula below. This is the completely explicit local score H_5544(n)=rho23711(n). Lower H means fewer locally admissible exponent states. It is not asserted to predict R.

For c,d modulo 6, define

A2(n;c,d)=w((n-3^c-5^d) mod8),

where w(0),...,w(7)=(1/2,1,1,0,1/2,1,0,0). Define

A3(n;d)=1 if 3 does not divide n-5^d;
A3(n;d)=3/4 if n=5^d mod9;
A3(n;d)=0 otherwise.

Define

A7(n;c,d)=1/8 if n=3^c+5^d mod7, and 1 otherwise.

Then

**rho237(n) = (1/36) sum_{c,d mod6} A2(n;c,d) A3(n;d) A7(n;c,d).**   (K-L1)

The formula has period 504=8*9*7. Its inherited 2/3 specialization is

rho23(n)=1/2 if 3|n;
=5/16 if n is odd and 3 does not divide n;
=7/32 if n mod24 is 2,4,8,22;
=13/32 if n mod24 is 10,14,16,20.

### Why the weights and their product are exact

Fix c and d modulo 6. The higher d-coordinate makes 5^d uniform on its fixed coset modulo 8 in Z2, modulo 9 in Z3, and modulo 7 in Z7. Indeed

v2(5^6-1)=3, v3(5^6-1)=2, v7(5^6-1)=1.

The remaining exponent periods are powers of 2,3,7 and are independent by CRT. After c>=k3, 3^c vanishes modulo 3^k3. The higher c-coordinates change the translations of these cosets but not their uniform measures. Hence the product is justified by independent higher d-coordinates, not by assuming that prime defects on the actual finite grid are independent.

On the 2-adic cosets, residues 1,2,5 mod8 always pass, residues 3,6,7 never pass, and residues 0,4 have measure 1/2 of passing. On 9Z3, the measure of even valuation is (2/3)/(1-1/9)=3/4. On pZp for p=7 or 11, the measure of even valuation is

sum_{j>=1}(1-1/p)*p^{-(2j-1)}=1/(p+1).

In particular the 7-hit weight is 1/8, not zero. This proves (K-L1).

## 3. Exact global minimum for 2,3,7

**Theorem K-L2.** For every integer residue n,

rho237(n) >= 21/128,

with equality exactly when

n mod168 is 56 or 70,

equivalently, 7|n and n mod24 is 8 or 22.

The equality residues modulo the full density period 504 are

56, 70, 224, 238, 392, 406.

**Caution:** only the minimizer *set* has period 168. The entire function rho237 does not have period 168.

### Proof, reduced to a small explicit certificate

Put T(n)=(1/36)sum A2 A3 [7|n-3^c-5^d]. Then

rho237=rho23-(7/8)T.

For each d mod6 there is at most one c mod6 solving the 7-divisibility equation, since 3 is primitive modulo 7. As A2,A3<=1, T<=1/6. Outside n mod24 in {2,4,8,22}, rho23>=5/16, so

rho237 >= 5/16-7/48=1/6 > 21/128.

It remains to check only the four hardest 2/3 classes. The following table gives 288*T for all possibilities; columns are n mod7 = 0,1,2,3,4,5,6. It follows by substituting the six powers of 3 and 5 modulo 7 and the displayed weights. This is 12 rows of seven small integers, not an original-target scan.

| n mod24 | n mod9 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2|2|3|10|10|8|7|11|14|
|2|5|3|10|7|14|10|8|11|
|2|8|3|7|10|11|10|14|8|
|4|1|3|8|14|10|11|10|7|
|4|4|3|11|8|10|14|7|10|
|4|7|3|14|11|7|8|10|10|
|8|2|18|7|7|4|10|10|7|
|8|5|18|7|10|7|7|4|10|
|8|8|18|10|7|10|7|7|4|
|22|1|18|4|7|7|10|7|10|
|22|4|18|10|4|7|7|10|7|
|22|7|18|7|10|10|4|7|7|

The largest entry is 18, attained precisely in the stated equality family. Thus

7/32-(7/8)*(18/288)=21/128.

In classes 2 and 4 mod24 the best value is instead

7/32-(7/8)*(14/288)=203/1152 > 21/128.

This proves both the minimum and its exhaustive classification. `reference.py` independently checks all 504 residues using both Fraction weights and an integer numerator over 2304, and emits the full 24-row minimum certificate. QED.

## 4. Adding 11 exactly

Both 3 and 5 have order 5 modulo 11; their powers form H={1,3,4,5,9}. Let K(t) count ordered pairs (x,y) in H^2 with x+y=t mod11. Explicit enumeration gives

K(0)=0;
K(t)=2 for t in {1,3,4,5,9};
K(t)=3 for t in {2,6,7,8,10}.

The two nonzero values can also be deduced by scaling by squares and checking t=1,2. Since -1 is not in H, a zero sum is impossible.

Define

beta11(t)=1-11*K(t)/300
=1 at t=0;
=139/150 at a nonzero quadratic residue;
=89/100 at a quadratic nonresidue.

**Theorem K-L3.**

rho23711(n)=rho237(n)*beta11(n mod11).                          (K-L3)

The density has period 5544=504*11. Its global minimum is

**1869/12800 = (21/128)*(89/100),**

attained exactly when

n mod168 in {56,70},  n mod11 in {2,6,7,8,10}.

The minimizer set has period 1848 and consists of exactly the ten residues

238,392,406,560,574,728,910,1064,1414,1568.

There are 30 equality residues modulo the full period 5544 and 150 modulo 27720. The complete coefficient spectrum has second-smallest value 973/6400.

### Independence proof and its limits

Work first on c,d modulo 30. The coarse 2/3/7 weight depends only on c,d modulo 6; the 11-divisibility condition only on c,d modulo 5. These coordinates are independent by CRT. On a fixed pair of coarse states, the higher d-coordinate has independent primary periods, because

v2(5^30-1)=3, v3(5^30-1)=2, v7(5^30-1)=1, v11(5^30-1)=1.

The 11-hit coset has even-valuation probability 1/12. Hence each hit loses 11/12 and averaging its K(t) hits among 25 states gives beta11. This proves the exact factorization and then the minimum classification. It proves independence in THIS limiting orbit model, not independence of finite-target failures, selected extrema, or arbitrary further primes. QED.

## 5. Least-bad-prime events: exact predicates and local capacities

For failed m>0 define P(m)=min{p=3 mod4:vp(m) odd}. The exact events are

P=7 iff v3(m) is even and v7(m) is odd;
P=11 iff v3(m),v7(m) are even and v11(m) is odd.

The 2-adic test is not part of the definition of P. If the scanner first filters by L2, it must be imposed separately. The distinction changes the numerical capacities.

On an L2-filtered grid, the limiting masses are

mass(P=7,L2)=rho23-rho237;
mass(P=11,L2)=rho237-rho23711=rho237*(1-beta11).

These are exact rational orbit formulas, with the finite-grid errors given below. They are not the heuristic CD/p. For 560 mod2520, mass(P=7,L2)=7/128: fully one quarter of its 2/3-admissible mass. On a quadratic-nonresidue lift modulo 11, mass(P=11,L2)=231/12800: 11% of its 2/3/7-admissible mass.

Without L2, let tau3=(1/6)sum_d A3 and tau37=(1/36)sum_{c,d} A3 A7. The corresponding capacities are tau3-tau37 and tau37*(1-beta11). For 560 mod2520,

tau3=5/8, tau37=205/384,
mass(P=7)=35/384,
mass(P=11)=451/7680 on a quadratic-nonresidue lift modulo 11.

No claim that these raw masses equal the pilot's recorded metric is possible without its scanner definition. On the six named targets, an unrestricted failure histogram in fact has 3 as its largest least-bad prime category; see EXTREMAL_VALIDATION.json. This is not silently reconciled with the brief's 7/11 language.

## 6. Uniform theorem for the actual finite logarithmic grid

Let L=log n and

J(n)=(floor(log_3 n)+1)(floor(log_5 n)+1).

**Theorem K-L4.** Uniformly over integers n>=2, in asymptotic notation,

G23711(n)=rho23711(n)*J(n)+O(L^{9/5})
        =rho23711(n)*L^2/(log3 log5)+O(L^{9/5}).

Likewise G237(n)=rho237(n)*J(n)+O(L^{7/4}). The inherited 2/3 argument gives error O(L^{5/3}). Constants are absolute; no numerical threshold or useful error bound at the pilot scales is asserted.

### Proof with all cutoff costs

Choose B=L^{1/5}. For sufficiently large n take q2=2^k2, q3=3^k3, q7=7^k7, q11=11^k11 each comparable to B, with k2>=4,k3>=2,k7,k11>=1. Discard c<k3, costing O(L log B) pairs. For the other rows, 3^c=0 mod q3.

Define lower cutoff indicators to reject all unresolved cells, and upper cutoff indicators to admit them. At 2, a cell is unresolved when 2^{k2-1}|m, because otherwise the valuation and the unit modulo 4 are both visible modulo q2. At odd p, a cell is unresolved when p^kp|m. These cutoffs sandwich the true local indicators, also at m=0 by the adopted convention.

The d-period T of their product divides

lcm(ord_q2(5),ord_q3(5),ord_q7(5),ord_q11(5))=O(B^4),

since these orders are respectively 2^{k2-2}, 2*3^{k3-1}, 6*7^{k7-1}, and 5*11^{k11-1}.

For each fixed c and each d mod30, write d=d0+30t. The four higher t-periods are powers of 2,3,7,11. CRT makes them independent, and the valuation identities in Section 4 make each image the full indicated coset. The measure of unresolved cells is O(1/B), uniformly in n and c. Thus the lower and upper complete-d-period averages each differ by O(1/B) from the closed-form limiting average at this c mod30.

Counting a bounded periodic function through any finite d-interval differs from its length times the complete-period mean by at most T. Summing over O(L) c rows gives error O(L B^4). Averaging the limiting c mod30 weights costs only O(L) at the endpoints. The uncertainty in the densities costs O(L^2/B). Including the discarded rows, the rectangular count therefore differs from rho23711*J by

O(L^2/B + L B^4 + L log B)=O(L^{9/5}).

The full rectangle has 3^c,5^d<=n. A pair outside D(n) has 3^c+5^d>n, hence either 3^c>n/2 or 5^d>n/2. Each base has at most one power in (n/2,n], so removing those pairs costs O(L). For the auxiliary rectangular argument local predicates can be interpreted p-adically on signed residuals; only O(L) nonpositive boundary pairs need treatment. This proves the theorem on the actual nonnegative-residual domain, without imposing m>=theta*n.

For 2/3/7 alone take three prime-power scales comparable to B=L^{1/4}; the period cost is O(B^3), yielding O(L^{7/4}). The same reasoning with two scales gives the known O(L^{5/3}). QED.

**Consequences:** fixed small primes cannot eliminate the entire grid for all sufficiently large n. This does not imply that the surviving grid contains a norm. Also, finite G grows unboundedly even along a fixed n residue class. Therefore a formula for its exact value depending ONLY on n mod a fixed M, without grid heights or valuation-depth information, is impossible. The corrected fixed-period statement is for rho, with a controlled finite-grid error.

## 7. An inverse theorem for G — not for R

Put delta0=1869/12800, delta1=973/6400, and tau=(delta0+delta1)/2=763/5120. By K-L4, for every sufficiently large n,

G23711(n)/J(n) <= tau  =>  n mod1848 belongs to the ten-class minimizer set.

Indeed the normalized error is O(L^{-1/5}); eventually it is smaller than (delta1-delta0)/2=77/25600. Any non-minimal residue has coefficient at least delta1 and cannot satisfy the premise.

This is a genuine local-count inverse implication. It cannot be applied after replacing G by R: R<=G is the wrong direction for inferring a small G from a small R. No representation inverse is hidden in this corollary.

## 8. Verification boundaries

`reference.py` performs exhaustive integer/Fraction classification, all requested finite quotient orbits, and exact verification of six named target grids. `local_oracle.py` additionally enumerates raw prime-power exponent states and checks 20 independent lower/upper rational brackets, including periods up to 332640. This is bounded residue-state verification, not an original-n production scan. The symbolic proofs, not agreement of a few decimal approximations, justify the theorems.

## 9. A separated coarse hard band survives BOTH extra primes

The fine minimizer family is too narrow to contain the five task-listed argmins. The following weaker, exactly classified band is a better mathematical match to S1.

**Theorem K-L5 (coarse-band separation).** Let H24={2,4,8,22}. Then

max_{n mod24 in H24} rho237(n)=161/768,
min_{n mod24 outside H24} rho237(n)=23/96.

After adding 11,

max_{n mod24 in H24} rho23711(n)=161/768,
min_{n mod24 outside H24} rho23711(n)=2047/9600.

The second gap is **23/6400>0**. In particular, with theta=8119/38400,

rho23711(n)<theta  iff  n mod24 in H24.

### Proof

Within H24, the critical table in Section 3 has smallest entry 3, so its largest density is 7/32-(7/8)*(3/288)=161/768. Outside H24, exact evaluation of the same 36-cell formula gives the following grouped row minima, including all remaining classes:

| n mod24 | minimum rho237 over its lifts mod504 |
|---|---:|
|0,6|25/64|
|3,9,12,15,18,21|41/96|
|1,11,13,23|283/1152|
|5,7,17,19|23/96|
|10,20|775/2304|
|14,16|83/256|

Each grouped entry is the minimum of 21 explicitly specified residues and 36 rational cells per residue; `row_minimum_certificate_mod24` records every equality residue and the complete function table independently checks them. Thus the minimum outside is exactly 23/96.

Multiplication by beta11, whose range is [89/100,1], makes the inside maximum no larger than 161/768 and the outside minimum no smaller than (23/96)*(89/100)=2047/9600. Both endpoints occur, because the n mod11 coordinate is independent of n mod504 under CRT. Their difference is 23/6400. QED.

By K-L4, an asymptotic finite-local-count corollary is

G23711(n)/J(n)<theta  iff  n mod24 in H24,

for all sufficiently large n. This corollary still does not replace G with R. No effective threshold is supplied. S1's supplied cross-scale counts show high recall for precisely this band; they do not by themselves certify concentration on the MUCH smaller exact minimizer set.
