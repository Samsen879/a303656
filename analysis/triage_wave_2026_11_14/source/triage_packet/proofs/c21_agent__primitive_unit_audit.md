# Primitive-unit canonical selectors: finite audit scope

This file records a scoped exploratory exact search. It does not prove all finite canonical selectors positive and does not decide the E2 abundance hypothesis or original LP.

## Normalization

Let q be an odd squarefree product containing 3 and 5, and lambda in {1,2,18}. At N_lambda=4 lambda q, the pushforward of tau (2-adic Haar on 1+4Z_2 and odd-prime unit Haar) by multiplication by lambda has phi(q) support residues. Its density relative to normalized counting measure is 4 lambda / V, where V=phi(q)/q. Thus convolution with the exact joint eventual-power law has density G_lambda=4 lambda a_lambda/V. At common modulus 72q, lambda=1 and 2 are pullbacks with respectively 18 and 9 lifts.

For lambda=18, write n mod27=5^d0, d0 mod18. Exact valuation v_3(n-T_5(beta))=2 is equivalent to beta mod18 being d0+6 or d0+12. The mod8 condition fixes alpha parity. Primitivity at 5 can restrict alpha to one class gamma mod4; if it does not, its allowed set is a union of such classes. Therefore all most restrictive canonical cores are the 72 pairs (gamma mod4,d0 mod18):

    alpha = gamma mod4,
    beta = d0+6 or d0+12 mod18.

At primes >5, shifts are computed jointly as 3^alpha+5^beta; no product-of-marginals substitution occurs.

## Explicit failure of importing the C21 p=271 bound

Choose n=75338 mod292680, with residues (mod8,27,5,271)=(2,8,3,0). This is a lambda=18 canonical class (n=2 mod24). Here d0=15 and gamma=3. At p=271, ord_p(3)=30 and ord_p(5)=27. The exact joint core grid has alpha mod60 in gamma mod4 and beta mod54 in 3 or 9 mod18: 15*6=90 cells. Exactly three hit shift=0 mod271, so conditional bad mass is 1/30, strictly larger than C21's unconditioned 1/81. This is a conditioning counterexample, not a zero selector and not a counterexample to LP.

## Completed finite covering searches

Script: unit_cover_search.py. No external solver is used.

1. P180={7,11,13,19,31,37,61,181}, C=D=180, 900 cells per core.
2. P360={7,11,13,19,31,37,41,61,73,181,241}, C=D=360, 3600 cells per core.

Each P is the set of odd prime divisors greater than 5 of gcd(3^L-1,5^L-1), for L=180 or 360. Actual periods C=lcm(4,ord_p3) and D=lcm(18,ord_p5) are used. These are sparse prime sets, NOT all primes up to 181 or 241.

For every one of the 72 cores, the search considers every possible one-residue target n_p at each p in P. It asks whether the bad events 3^alpha+5^beta=n_p modp can cover the entire core. A residue giving an empty bad event may be omitted without affecting feasibility: replacing it by any nonempty event only adds coverage.

At a node, U is the uncovered-cell bitset. For each unused prime p, compute b_p=max_z |U intersect E_(p,z)| exactly. If sum_p b_p<|U|, no completion can cover U, so prune. Otherwise choose a prime and enumerate all residue masks with |U intersect E_(p,z)|+sum_(other p)b_p >= |U|; every omitted branch violates a necessary upper bound. Thus pruning is sound and complete. All arithmetic and bit counts are exact integers.

Results:
- P180: 72/72 cores exhausted, no covering, maximum 5 recursion nodes per core, no node cap triggered.
- P360: 72/72 cores exhausted, no covering, maximum 32 recursion nodes per core, no node cap triggered.

JSON logs: unit_cover_L180.json and unit_cover_L360.json.

No larger search was dispatched. No conclusion is drawn for adding further primes, for full primorials beyond the pre-existing E2 checks, or for Y tending to infinity. The exact p271 conditioning counterexample remains the decisive obstruction to importing the C21 budget without a new proof.
