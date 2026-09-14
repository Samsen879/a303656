# Phase I: terminal peeling, actual module gluing, and two conditional escape architectures

## Status and dependencies

These are new mathematical deductions and explicit constructions in this research session. They are not promoted repository authority, independently authored referee reports, or proof-assistant formalizations. The standalone arithmetic tests establish the finite claims they actually check, not the unbounded statements below.

All statements concern the repository's finite admitted original-row C=1 class. Sources S1–S9 are pinned in SOURCE_BINDING.json. In particular, S1 supplies the boundary lemma, exact sparse elimination, six-descended-source obstruction, seven-source normal form, and the small-core theorem. S2 supplies original-support confinement and simultaneous, frozen-shadow charging. S4 supplies the seven-basin/O31 comparison. We do not re-prove these imported results from the finite examples.

An original odd row has a distinct prime p=3 mod4, precision K>=2, shared r mod p^K and positive odd accepted valuations E<K. Zero modulo p^K is never fatal. Set w_p=ord_p(5), s_p=v_p(5^w_p-1). N counts original nonregular primes s_p>=2, including those inactive or dynamic at a particular boundary. It does not count macros, witness occurrences, or regular helpers.

## I1. Threshold pruning and iterative terminal peeling

Fix the original ledger, ambient, states, the boundary-selected anchor c*, and a parity with the original dynamic 3-row inactive. Initially there are at most N rigid origins. Until the first essential nonlinear step, each source has at most one surviving linear seed.

**Threshold lemma.** After exact descending elimination of all coordinates p>N, every surviving source q satisfies max T(q)<=N, where T is the absolute admitted order-terminal closure. This is a necessary source test, not sufficient coverage.

**Proof.** At every coordinate p>N the number of proper cylinders is at most N<p, so the imported exact sparse-elimination theorem says that the full residual is linear. A surviving seed cannot drop an uneliminated odd order factor by intersection. Following any absolute order path of q, either a required admitted relay is absent/inactive, and the lineage disappears earlier, or the lineage inherits the next order factor. If the path terminates at a free prime lambda>N, there is no original admitted dynamic lambda-row. Fewer than lambda proper cylinders cannot cover that free coordinate, so this lineage disappears there. The terminal 3 is below the threshold. This argument is performed in the fixed ambient; no row is deleted and no period recomputed. QED.

**Peeling corollary.** Start with S_0=Q, the set of all original nonregular primes, and repeatedly set

    S_(i+1) = {q in S_i : max T(q) <= |S_i|}.

If a complete certificate exists, the stable set S_infinity has at least seven elements. If it has exactly seven, these seven are pure-3 and the surviving core has the imported seven-origin normal form.

**Proof.** The first threshold lemma leaves at most |S_1| possible origins below N. Continue descending through the additional coordinates greater than |S_1|. They are again sparse, so the same argument removes S_1\S_2 before any nonlinear step. Iterate. At the stable cutoff no completeness has been lost and no new source has been created. The imported six-descended-source obstruction gives |S_infinity|>=7. With seven surviving sources, elimination above seven is linear and the imported seven-source argument applies. If a nonregular original row outside this surviving pure-3 core were a required helper of it, that row would itself have pure-3 terminal closure and could not have been removed by these terminal thresholds. Thus the surviving proper basins are regular as in the equality argument. The removed sources also disappear above seven when analyzing the opposite parity; they do not provide an automatic repair of O31. QED.

This does NOT charge one unit to an origin at every later nonlinear witness. It bounds sources only while elimination is linear. It is not an N-only capacity theorem after a nonlinear expansion.

For the three actual roots below, max T equals 5,653,1429. Thus 40487 cannot survive to the first nonlinear stage when N<=652, and 1645333507 cannot do so when N<=1428. This does not mean the corresponding row has no fatal points, no local module, or no possible use in larger architectures. The actual partial ledger explicitly gives them useful partial fibers.

For N<=12, I1 specializes to S1's H={q:T(q) subset {3,5}} theorem: at least seven H roots; if exactly seven, all pure-3. N=13 is the first numerical threshold at which a free terminal 13 could cease to be sparse, not an existence theorem for such an origin or a complete certificate.

## I2. A strengthened published-bound inventory corollary

Let B=970453984500000, the inclusive base-5 endpoint specified in Dorais–Klyve (2011), section 4.1. The six odd base-5 Wieferich primes below this bound are the OEIS A123692 odd entries read on 2026-09-10. Filtering p=3 mod4 leaves exactly

    20771, 40487, 1645333507.

The historical exhaustive search is an external dependency and was NOT rerun here. For a prime q not dividing 5, write q-1=w_q t with q not dividing t. Then LTE gives v_q(5^(q-1)-1)=v_q(5^w_q-1), so this inventory uses the same nonregular condition.

**Corollary.** Every complete admitted C=1 certificate requires at least seven original nonregular primes strictly greater than B.

**Proof.** If N>=13, at most three original nonregular primes are <=B, leaving at least ten above B. If N<=12, use S1's H theorem. Only 20771 among the three is in H, and it has T={3,5}, not {3}. If |H|=7, all seven pure-3 roots therefore exceed B. If |H|>=8, at most one H root is <=B, leaving at least seven above B. QED.

This is an exact consequence of the cited finite inventory and the imported unbounded structural theorem. It is not a claim of a new scan, of the absence of all further Wieferich primes, or of a probability model.

## I3. Canonical filling over arbitrary finite terminal boundaries

Let D=R union {q} be an actual finite absolute admitted closure above its terminal primes. Assume q is nonregular, all p in R are regular, and every prime in R occurs to exponent at most one in every w_v, v in D. Boundary terminal prime powers can have greater depths. Include parity whenever any order is even. Let W=lcm(w_v:v in D), and remove its private R-primary factors to obtain the boundary modulus B_D.

Choose one integer a that fixes a boundary class modulo B_D and fixes each private p-coordinate at a prescribed center. For the examples all private centers are zero. Define once and for all

    K_p=2, E_p={1},
    r_p=3^c+5^a mod p^2                 (p in R),
    r_q=3^c+5^a+q mod q^2.

**Filling theorem.** Every exponent d with d=a mod B_D is rejected at anchor c by at least one actual row in D, for every choice of the private coordinates.

**Proof.** If a private p-coordinate differs, choose the least such prime p. Every private divisor of w_p is a smaller admitted descendant and has matching digit. The boundary digits also match. Thus w_p divides d-a, but p does not divide d-a. Regularity gives exact valuation v_p(5^d-5^a)=1. If all private coordinates match, w_q divides d-a, and nonregularity gives 5^d=5^a mod q^2. The q-row has local value q mod q^2, again exact valuation one. Negative d-a can be handled with the multiplicative inverse of 5; the congruence and valuation conclusion is unchanged. QED.

This proves a sufficient whole-boundary-cylinder profile. It does not in general identify the full union's exact saturated profile, or assert that modules with overlapping private coordinates have independent escapes. For the three numerical modules in candidate_ledger.json the exact saturated union is separately proved by the finite equality/non-equality quotient and by the linear receipts.

The source E1 theorem is the pure-3 special case. Free terminal factors have not disappeared: they occur explicitly in B_D, and become obligations for a later combined cover.

## I4. Shared-original-row module gluing and the finite compatibility interface

For fixed finite modules, each allowed module state specifies actual (p,K,E,r_p) values for every original row it uses, and a proved full-fiber coverage guarantee.

**Gluing theorem.** A selection of such states can be literally merged, without lifting or reselecting any specified state, into one row ledger exactly when every shared original prime has the same K,E,r_p in all occurrences. With this consistency, all row residues admit one simultaneous integer CRT residue. Any family of proved module guarantees whose disjunction covers every mandatory anchor/fiber then gives the corresponding whole-ledger guarantee.

**Proof.** Necessity of state consistency is the original-row identity axiom. After coalescing identical shared rows, the distinct prime-power row moduli are coprime, so CRT supplies one residue. The local value of every retained row is unchanged. Adding fatal events cannot remove an already proved covering guarantee. The final Boolean demand is evaluated after this union: A0 uses C0, A1 uses C1, EITHER uses C0 OR C1, BOTH uses C0 AND C1, and TRUE is the always-true demand. QED.

The criterion is exact for merging the specified states, not for completeness of arbitrary modules. Shared-coordinate modules require an exact combined fiber check; pairwise Hall feasibility, profile masses, and independently chosen local states are not sufficient. Nor may one commute universal quantification with an OR without a proof. A complete finite module-state CSP can instead retain every original state variable, all separator/private coordinates, and direct local incidences. Finite domains then give a finite decision problem. A bound on N alone does NOT bound prime values, precision, or the number of state options.

For the actual partial ledger, shared row 31 has r31=4 in both modules. Its use in two module receipts does not create two original rows or twice the capacity in a single simultaneous witness.

## I5. Literal-order inflation / split-fiber identity

Suppose k distinct actual admitted nonregular primes q_j have exact order km, j=0,...,k-1. At one fixed anchor and K=2,E={1}, fix their residues to realize the rigid logs b+jm mod km. Their fatal events have the exact union

    union_j {d=b+jm mod km} = {d=b mod m}.

Each row is distinct and used once; this is not a repeated reference to one prime. It trades additional original roots for finer, prescribed-order fibers. Shared helpers are permissible only with I4 state consistency. This identity is the reason N is a meaningful constructive parameter beyond the equality case.

## I6. Conditional N=8: split the 31 duty by parity

All regular rows in this theorem are numerically certified in the accompanying library. In particular,

    w31=3, w1303=62, w258065887=186,
    s31=s1303=s258065887=1.

The even 31-module has actual regular support {31,1303} and one uninstantiated nonregular terminal of exact order 1303. Set r31=r1303=4 and use the root log 0. Its inherited boundary is even d, d=0 mod3.

The odd 31-module has actual support {31,258065887} and one uninstantiated nonregular terminal of exact order 258065887. Set r31=4 and r258065887=2. Its terminal log is 0. Indeed the canonical exponent is odd and divisible by 3*31*258065887; modulo 186 it is 93 and modulo 258065887 it is zero. Its class modulo the lifted order 186*258065887 is therefore 93*258065887. Consequently 5^a=-1 mod 258065887^2. Regularity would NOT imply 5^93=-1 modulo the prime square; using the lifted exponent is essential. This covers odd d, d=0 mod3. Both modules use the identical actual state at row31. Neither entire basin is all-odd.

Add six modules with the following regular supports, root orders, and selected even-parity leaves:

| module | actual regular support | root order | leaf |
|---|---|---:|---|
| B7 | 7,43 | 903 | 1 mod3 |
| H19 | 19,191 | 191 | 2 mod9 |
| H5167 | 5167 | 5167 | 5 mod9 |
| H271 | 271 | 271 | 8 mod27 |
| H4159 | 4159 | 4159 | 17 mod27 |
| H31051 | 31051 | 31051 | 26 mod27 |

Each uses I3's canonical states. Add r3=2 mod9, r2=1 mod4. Even d is covered by the original seven ternary duties. Odd d not divisible by 3 is covered by row3; odd d divisible by3 is covered by the extra odd 31-module. Anchor0 is rejected by the two-adic row on every exponent. Thus BOTH holds under the eight terminal existence hypotheses.

There are 8 nonregular terminal slots, 11 regular rows above3, and the regular row3: 20 original odd rows conditional on instantiation. There are 8 parity-tagged module roles but only 7 participating leaf origins on the selected even parity. The extra origin is genuinely used on the opposite parity rather than being a redundant copy.

**Scope:** This supplies a sufficient conditional architecture with no single O31 basin. It does not prove actual complete N=8 certificates exist, or refute a possible deeper fixed-base theorem forcing O31 in every actual certificate. No terminal is certified in this architecture. The enormous prime-index value Phi_258065887(5) is NOT materialized or searched here.

## I7. Conditional N=9: three depth-two roots over the single actual helper 31

Keep the six modules in I6. Replace its two 31-modules with three distinct uninstantiated admitted nonregular primes of exact order

    279 = 9*31.

For j=0,1,2 choose root log 93j mod279 and residue

    r_qj = 3 + 5^(93j) + qj mod qj^2.

The single shared helper31 is fixed to r31=4. Since ord_(31^2)(5)=93, all three root recipes use the same helper state. Each module fills respectively the depth-two leaf 0,3,6 mod9 over every private31 coordinate. Their orders and that of31 are odd, so this three-module cover of d=0 mod3 holds on both parities. No individual root is in B31^odd: its v3(w) is 2 rather than at most1.

The selected complete frontier has

    (depth1, depth2, depth3) = (1,5,3),
    leaves: 1 mod3;
            0,3,6,2,5 mod9;
            8,17,26 mod27.

All nine leaves are disjoint and cover the ternary domain. The three final depth-two exact providers above31 are the three distinct roots themselves, not three copies of row31. Their root guards carry the 3^2 factor. Row31's shallower shadow contains their three leaves consistently; its sharing therefore does not violate exact-provider privacy or inflate its original-row identity. The six other frontier providers are distinct actual heads. Ancestry terminates at the corresponding original terminal slot, conditionally on its certification.

Adding r3=2 mod9 and r2=1 mod4 proves BOTH just as above. The original odd row count is 9 roots + 9 regular rows above3 + row3 = 19. Its 27,648 exact formal-guard quotient cells are replayed without pretending to perform arithmetic at the unknown terminals.

Define

    Sq(n)={q prime: q=3 mod4, q does not divide n, q^2 divides Phi_n(5)}.

**Exact finite instantiation theorem for this frozen architecture.** Its nine terminal slots admit distinct actual prime values, and the displayed canonical states then form a complete admitted C=1 certificate, if and only if

    |Sq(279)| >= 3,
    |Sq(n)| >= 1 for n in {903,191,5167,271,4159,31051}.

**Proof.** At a primitive cyclotomic prime, exact order is n and the cyclotomic valuation is s_q. Thus every listed square hit supplies exactly the required actual nonregular terminal; all its proper admitted descendants are the already certified support in the corresponding table. Distinct exact orders cannot belong to the same prime. At n279 the condition explicitly requires three distinct primes. All shared helper residues have been verified equal, so I4 and the covering argument give one global state. Conversely, any instantiation of these frozen slots supplies the listed distinct primitive square divisors by its certified exact order and nonregularity. QED.

This is an iff for instantiation of THIS architecture. It does NOT say every N=9 certificate has these orders, and it does NOT globally reduce N=9 existence to seven integers. No square hit at any of the seven targets is established here.

## I8. Exact finite computational gate and negative certificates

The new first target is the 126-digit integer

    C279 = (5^279-1)(5^3-1) / ((5^93-1)(5^9-1)).

Its exact decimal representation is in targets/phi_279.txt. Independent recursive and Moebius-product evaluations agree. It is certified composite by a Fermat base-2 witness. No prime <=10000 divides it. Neither fact proves squarefreeness or supplies an admitted square hit.

All seven I7 target integers are materialized; the largest has 21,704 digits. This is a fixed arithmetic gate, not a scan over all prime roots. Once completely certified factors have been removed from C279, suppose k distinct qualifying square-hit primes have been found, their full valuations removed, and all other removed prime factors also have certified valuations. Let R be the remaining integer. Every new qualifying prime exceeds the published B. Therefore

    R < (B+1)^(2*(3-k))

with k<3 certifies that there cannot be enough further distinct square hits. This can close the frozen architecture without a full factorization, but it may not close N=9 as a whole. The published bound is an explicit dependency of this pruning rule; an independently certified smaller lower bound can be substituted.

## I9. What a complete C=1 certificate would mean

A sound complete original-row C=1 ledger gives, for every integer n in its CRT residue class and every d>=0, a local obstruction to n-3^c-5^d being a sum of two squares, for each tested anchor c=0,1. Consequently those n have no representation with c<=1. It does not exclude representations with c>=2. In the canonical r2=1 mod4 state, all even c are additionally rejected by the same two-adic calculation, but odd c>=3 remain unhandled.

An A303656 counterexample needs a bridge covering every relevant exponent c, or an explicit integer n with independently verified exclusion of all feasible c,d. An uninstantiated conditional construction is weaker still. Our actual three-root ledger fails even the full C=1 BOTH condition, with a stored exact escape. No counterexample to A303656 is claimed.
