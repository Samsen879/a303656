# Two-nonregular global shared-state pooled realizability — Phase D

## Scope and evidence

All claims concern finite admitted original-row ledgers, not A303656 itself.
They are proposed research deductions with proofs and a standalone laboratory,
not independently refereed or proof-assistant formalized results. No theorem
priority beyond the pinned repository reading is claimed. The general problem
has not been reduced to an order-signature-only analogue of C9.

Source snapshot: `Samsen879/a303656`, main
`3fb4b4b4f71018017c7ea014ae7a1380f27b6b94`, tree
`5ee6ab9e51f3e6d471991b7407de193d12777882`.
Source C6–C9 mean the statements in
`analysis/c1_global_shared_state_phase_c/PROOF_DETAILS.md` at that SHA.
Source P4/P5 and the joint reverse CRT are the pooled Phase-B statements.

## 1. Fixed formal class

Let P=R union {q1,q2}, q1<q2, with every row a different actual prime congruent
to 3 modulo 4. All p in R have s_p=1, and s_q1,s_q2>=2. Fix K_p>=2 and
nonempty E_p consisting of positive odd integers below K_p. The only freely
searched row parameters are the shared residues r_p modulo p^K_p.

Write

    V_(p,c)(d)=r_p-3^c-5^d, c=0,1,
    w_p=ord_p(5), s_p=v_p(5^w_p-1),
    ell_p=w_p p^max(0,K_p-s_p),
    U=lcm(t2,{w_p}), L=lcm(t2,{ell_p}).

A residue-zero local value is unresolved, never accepted. In this note a
whole odd pooled cover means every exponent has an accepted valuation at
at least one anchor and at least one odd row. It does not mean BOTH.
Optional two-adic coverage is not credited toward this objective. A full
supporting refinement of L can be used to discuss CRT projections, but is
never relabelled as the original coarse U.

All residues are chosen once. Different primes' choices are jointly realizable
by the ordinary CRT; two uses of the SAME prime do not have separate choices.

Denote the three fixed-K/E conditions of C9 for R union {q} by C9_R(q):
hereditary regular squarefree odd-order closure in R, accepted valuation 1 at
every required regular row, and an accepted odd h<s_q at the root. This
notation is a predicate on the source's single-nonregular subledger, not a
necessary condition imposed separately on every root of a two-root cover.

## 2. D0 — monotonicity and canonical compatibility

**Theorem.** If C9_R(q1) OR C9_R(q2), a two-root whole odd pooled cover exists.
If both predicates hold, their canonical regular states are compatible on
every shared support row, regardless of the overlap pattern.

**Proof.** C9 produces a cover using only one root and its regular support.
Adding the other original row cannot remove fatal events. More explicitly,
C9 uses r_p=2 modulo p^K_p on every required regular row. Two successful C9
constructions therefore impose identical residues on an overlap. The root
states r_q=q^h+2 are on different prime-power moduli. CRT realizes them together.
QED.

Thus the proposed implication “both individually satisfy C9, but a pooled
union may still fail solely from their support overlap” is false in this
unrestricted-residue, union-coverage class. It can be a real issue for frozen
states, restricted state families, or additional mandatory typed roles.

## 3. D1 — exact last-root trace and arithmetic state elimination

Let A={q1} union {p in R:p<q2} and

    N=lcm(w_q2,{ell_p:p in A}).

For ONE frozen state vector tau on A, let S(tau) be the full common escape set
of A modulo N and D(tau)=pi_(w_q2)(S(tau)). Every prime factor of N is below q2.
Let B_q2(r) be the at-most-two logarithms of q2's rigid FATAL components.
A dynamic guard is not a member of B merely because part of it is fatal.

**Frozen-state statement.** Independently of the states of regular rows above
q2, whole odd pooled completeness is equivalent to D(tau) subset B_q2(r).

**Proof.** Inclusion covers every exponent not already covered by A. If
inclusion fails, take an earlier common escape with log outside B. Its lower
coordinates are already fixed. At q2 choose the safe full center if its one
possible active anchor is dynamic; inactive and nonaccepted rigid cases are
already safe. The difference V0-V1=2 prevents a second simultaneous active
anchor. Extend through all larger regular rows using C6. This is a full common
escape. QED.

Define H_q=E_q intersect {h:0<h<s_q}. If H_q is nonempty set h_q=min H_q.
For D subset Z/w_q, define the explicit arithmetic predicate J_q(D):

* D is empty; or
* H_q is nonempty and |D|=1; or
* H_q is nonempty, D={a,b} with a!=b, and
  5^a-5^b = 2 OR -2 modulo q^h_q.

No other set passes. In particular a set of size at least three fails.

**Free last-root statement.** Some r_q2 gives D(tau) subset B_q2(r_q2) iff
J_q2(D(tau)). Consequently

    two-root whole odd pooled realizability
      iff exists ONE lower state vector tau with J_q2(D(tau)).       (D1)

**Proof of arithmetic elimination.** A singleton is supplied at anchor 0 by
r=1+5^a+q^h modulo q^(h+1), then lifted to precision K. Since h<s, powers
are constant modulo q^(h+1) on a fixed log class. For a two-element D, each
log must be assigned to a different anchor. If a is on anchor 0 and b on 1,
the centers A0=1+5^a and A1=3+5^b must agree modulo q^h, yielding the +2
congruence. Swapping anchors yields -2. Conversely, when the centers agree
modulo q^h, choose r=A0+q^h t avoiding the at-most-two forbidden next digits
which would make either center's valuation exceed h. Since q>2 there is a
choice. Both valuations are exactly h, so both rigid guards are accepted.
Necessity with unequal accepted rigid valuations follows by taking their
minimum, which is at least h_q. QED.

This removes the last root's entire q2^K state search and shows explicitly
where its paired arithmetic enters. It still quantifies over the lower
configuration tau; it is NOT an order-closure-only classification of all
interacting two-root systems.

## 4. D2 — a non-helpful upper root above a nonaccepted first shell

Suppose s_q1 is NOT in E_q1. In particular this holds whenever s_q1 is even,
and for every nonregular q1 in the K=2,E={1} starting class.

**Theorem.** If q1 divides w_q2, then

    two-root whole odd pooled realizability iff C9_R(q1).           (D2)

The same conclusion holds if q2 reaches q1 along a strictly decreasing
order path whose intermediate vertices are actual regular support rows.

**Proof.** Sufficiency is D0. For necessity freeze a purported cover and use
D1. If S(tau) is empty, the lower one-root system covers; hence C9 holds.
Otherwise choose a common-safe prefix immediately below coordinate q1
which occurs in S(tau). At its fixed q1-log a rigid component, if present,
is nonfatal. An inactive/nonfatal rigid branch permits all q1 first digits.
In the dynamic case the noncenter first digits have valuation s_q1, not
accepted by hypothesis; the center first digit has a safe full center lift.
Thus all q1 first digits have safe lifts. Every later row in A is regular,
so each lift extends to S(tau). As q1 divides w_q2 this yields at least q1>2
distinct elements in D(tau), contradicting D1.

For a regular intermediate p>q1, the proof of C7 applies to the q1-containing
escape set at coordinates ABOVE q1: the only remaining higher rows in A
are regular, so all safe prefixes extend. A two-point projection involving p
therefore forces activity of the p-row at every safe prefix and a two-point
projection modulo w_p. Iterate down the path until q1 and apply the same
first-digit argument. QED.

This is a whole-domain arithmetic iff for a substantial serial subclass,
not a mere prescribed-fiber collision. It is a deduction from the existing
escape/width mechanisms; it is not claimed to be a strict improvement over
every possible Phase-C Hybrid plan.

## 5. Closures and separating coordinates

To avoid the repository's overloaded T notation, write C_i for the dependency
closure of root i: include every odd prime dividing w_qi; whenever a required
coordinate p is an actual REGULAR row, include every odd factor of w_p and
continue. Missing/nonadmitted coordinates remain coordinate vertices, not
invented rows. If the other nonregular root is encountered, record a serial
interaction instead of treating it as a regular relay.

For the following separator statements assume neither root occurs in the
other's closure. Put R_i=R intersect C_i and

    N_i=lcm(w_qi,{ell_p:p in R_i}),       g=gcd(N_1,N_2).

One may refine both N_i by 2 to expose parity explicitly. These are analysis
periods, not newly asserted original coarse periods. Shared FREE coordinates
count in g just as shared row coordinates do.

For one globally consistent regular state vector sigma, let S_i be the
common escape set of R_i modulo N_i. For a supply set B_i of at most two
rigid root logs put

    E_i = pi_g {d in S_i : d mod w_qi not in B_i}.                    (5.1)

A supply set may omit an extra event carried by its realizing root state.
It is not an assertion that the extra event has been suppressed. Allowed
supply sets are exactly those satisfying J_qi(B_i); empty supply is always
allowed. Necessity may choose the actual full rigid set, while sufficiency
only needs the chosen supplied subset.

## 6. D3 — exact separator / profile theorem

**Theorem.** With roots incomparable as above, a frozen state, using its FULL ACTUAL rigid log sets B_i, is odd-pooled
complete iff its two escape profiles E_1 and E_2 are disjoint.
For free states, existence is equivalent to choosing ONE state on every
shared regular row, one global private state vector per side, and permitted
root supply sets B_1,B_2 for which E_1 intersect E_2 is empty.

**Proof.** Nonempty profile intersection gives two private escaping exponents
which agree modulo g. The noncoprime CRT joins them modulo lcm(N1,N2). Their
root logs avoid all rigid events; neither root's own prime coordinate occurs
in these closures or in the other root's dependencies, so choose their safe
dynamic centers as needed. Any outside regular row can be handled in increasing
order: an outside coordinate does not occur in the already fixed closure
conditions, precisely by hereditary closure. C6 completes a full escape.
Conversely, every full common escape projects to both profiles. For the
existence statement, necessities use actual rigid sets; sufficiency chooses
states realizing the selected supply sets, whose extra coverage cannot hurt.
QED.

For one shared relay p, freeze its r_p and all common lower-coordinate data.
Compute the two finite families of complete escape profiles on the common
separator, by ranging over each side's ONE private state vector. The exact
criterion is that some pair of these profiles be disjoint. Quantifiers are

    exists r_p, private state vector 1, private state vector 2
      such that for every separator z,
      side 1 covers its entire private fiber OR side 2 does.        (D3)

Private vectors cannot be reselected for each z. This gives an exact
integer/profile classification, not an unjustified network-flow theorem.
It keeps both “same induced state” and “compatible distinct roles” and
rejects incompatible roles by the residue conditions in Section 9.

An intersection of two fully hereditary REGULAR support closures is itself
hereditary. If it consists of exactly one prime p and there are no common
free coordinates, w_p can have no odd factor. The only admitted prime of
order 1 or 2 is p=3 (order 2). Thus a literally one-prime global hereditary
intersection is necessarily {3}; a first shared relay p>3 brings its own
lower closure and must not be modelled as an isolated p.

## 7. D4 — disjoint-coordinate iff, with OR not AND

**Theorem.** If C_1 and C_2 have disjoint odd coordinate sets (including free
coordinates) and neither contains the other root, then

    two-root whole odd pooled realizability
      iff C9_R(q1) OR C9_R(q2).                                    (D4)

**Proof.** Sufficiency is D0. The necessity part of C7–C9 remains valid with
parity fixed: all odd-digit choices and regular-safe extensions remain
available. Hence failure of C9_R(qi) implies that every choice of its states
leaves a common escape on EACH parity. If both C9 predicates fail, pick a
common parity and one escape on each independent odd-coordinate closure.
CRT combines them; outside regular rows and root centers are handled as in
D3. Thus the pooled union also fails. QED.

The tensor identity at a fixed separator value z is

    forall(x1,x2) [C1(z,x1) OR C2(z,x2)]
      iff [forall x1 C1(z,x1)] OR [forall x2 C2(z,x2)].

It does not require both sides individually to cover. If a nontrivial common
coordinate remains, the covering side may change with z, and D3 rather than
the simplified D4 must be used. In particular seven disjoint basins ABOVE 3
are not disjoint coordinate systems: they still share 3 and parity.

## 8. D5 — common-defect width obstruction for incomparable roots

Let W=gcd(w_q1,w_q2), and S be the common escape set of all relevant regular
rows in a period supporting both closures. A two-root cover implies

    |pi_W(S)| <= 4.                                               (8.1)

Indeed every regular escape must lie in one of at most four rigid root logs
by the incomparable-root argument. If an odd p>=5 divides W, (8.1) forces:

* p is an actual regular row and accepts valuation 1;
* v_p(W)=1;
* p's own entire regular squarefree closure passes the C9 support gate,
  with valuation 1 accepted throughout it.

**Proof.** Missing p, inactivity at a safe prefix, or rejection of valuation 1
would each produce all p first digits in the safe projection, exceeding 4.
If p^2 divides W, the p safe second digits over a regular center similarly
exceed 4. Every safe prefix must therefore activate p, whence
|pi_(w_p)(S)|<=2; apply C7 recursively to w_p. QED.

For example a common factor 5, 11, 19 or 67 is impossible in this subclass:
5 is nonadmitted; 11 leads to 5; 19 has order 9; 67 leads to 11. A common
factor 31 passes. These exclusions are structural corollaries. In particular
several named examples also admit pre-existing Hybrid release proofs, so
this is not advertised as strict new exclusion beyond all old methods.
The threshold 3 is genuinely left open by the four-point bound.

## 9. D6 — exact common-relay residue collision

For a regular p and a requested center-prefix role (c,b,z,m), with
b modulo w_p, z modulo p^m, and m+1<=K_p, use CRT to form t satisfying

    t=b mod w_p,    t=z mod p^m.

The actual role is equivalent to

    r_p = A(c,b,z,m) := 3^c+5^t mod p^(m+1).                       (9.1)

**Proof.** Regularity gives ord_(p^(m+1))(5)=w_p p^m. Thus a full logarithm's
lower log and p-center prefix uniquely specify its power at this precision.
A state has that center prefix exactly when (9.1) holds. QED.

For multiple mandatory roles alpha, a shared state exists iff

    A_alpha = A_beta mod p^(min(m_alpha,m_beta)+1) for all pairs.  (9.2)

Compatible congruences determine r modulo the largest required power; all
higher digits may be chosen freely. This is necessary and sufficient for
center roles, not a claim that arbitrary deep shells themselves give full
coverage. In particular a valuation-one simple-pair role additionally needs
1 in E_p. Other prescribed valuation obligations must retain the C3
forbidden-next-digit test; they are not all equalities of type (9.1).

At K=2,E={1}, suppose a mandatory p-fiber's other events cover just one digit
z, and the p-row must cover every other digit. Then the regular row's center
must be z, and its anchor may be 0 or 1. The exact allowed set is therefore

    {1+5^t, 3+5^t} modulo p^2.                                   (9.3)

For multiple such whole-fiber demands, intersect these sets. Empty
intersection is a real global state collision. If a cover clause has OR
alternatives, (9.2)/(9.3) apply within each selected conjunction; competing
branches must not be conjoined.

Compatible distinct roles exist: p=7,r=2 has an anchor-0 center at d=0
and anchor-1 center at d=21, both with p-coordinate 0. Indeed
1+5^0=3+5^21=2 modulo 49. Different anchors do not automatically collide.

### Actual two-root collision fixture

P={3,31,20771,40487}, all K=2,E={1}; freeze

    r3=2, r20771=20773, r40487=40493.
    U=L=40688430, M=U/31=1312530.

On d=0 mod M, the fixed rows cover only x=d mod31=0, supplied by q20771
at anchor0. On d=437511 mod M they cover only x=1, supplied by q40487 at
anchor0. The 3-row is safe throughout both fibers; other root events are
inactive there. Both fibers have lower 31-log d=0 mod3.

For x=0, t=0 and the allowed shared-31 states are {2,4} mod961.
For x=1, t=63 mod93, 5^63=683 mod961, and they are {684,686} mod961.
The sets are disjoint. Direct enumeration of all 961 states on the 62
mandatory cells yields coverage histogram

    2 cells: 899 states; 60 cells: 58 states; 61 cells: 4 states.

There is no simultaneous solution although either fiber separately is
coverable. This is an ACTUAL paired-root, common-regular-state example.
It is not a new unrestricted no-go for these two prime values: source P4
already excludes every system with nonregular roots only 20771 and 40487.
The point here is the exact residue-collision mechanism and its use in
mandatory role clauses, not a relabelled prime-inventory result.

## 10. D7 — multi-use resultants, and an actual large gcd

Use the original source definition

    R_h(Y)=Res_T(T^h-5^(Yh),(T-2)^h-5^(Yh)), h odd, Y>=0.

Suppose ONE original row q with w_q=u h must be paired-rigid-active at
ALL specified ordinary lower representatives Y1,...,Ym. Then

    u divides G=gcd(Y2-Y1,...,Ym-Y1),
    q divides gcd(R_h(Y1),...,R_h(Ym)).                            (10.1)

The first condition is independent of and stronger in some cases than the
second: both anchors' fixed logs must project to every specified lower
class. When u|G, the polynomial pairs are identical modulo q, since
w_q divides h(Yj-Y1). The resultant congruences are then not independent
new congruence conditions. This part reconstructs C2/C4, not a new theorem.

### New exact computation at the actual h=67 pair

For Y=7,8, both resultants were computed exactly, by the original resultant
and by a half-degree identity. Their absolute bit lengths are 72347 and
82614. Their positive integer gcd is

    2^67 * 269^15 * 1609^3 * 1877^4 * 3083 * 4289 * 4691
         * 5897 * 7639 * 20771 * 27337.                           (10.2)

Every displayed factor was certified prime by trial division, and the product
was compared to the Euclidean gcd of the two complete integers. Signed
hexadecimal integers are retained in the bundle; no giant decimal rendering
is needed for reproducibility.

The actual q=20771 divides (10.2), and has legal individual paired states

    Y7: b0=2177,b1=9772,r=16;
    Y8: b0=1558,b1=10238,r=17555.

But its u=155 does not divide 8-7, so it cannot serve both in one state.
This checks the failure of “resultant gcd pass implies multi-use” with the
literal large integer gcd rather than just two modular common-root checks.

There is also an all-prime exclusion for this mandatory paired demand.
G=1 forces u=1 and w_q=67. Put V=(5^67-1)/4. Exact integer Euclid gives

    gcd(V, gcd(R67(7),R67(8))) = 432821 = 269*1609.                (10.3)

Both factors are 1 modulo 4. Hence NO admitted prime, even before imposing
nonregularity, has the required exact-order and simultaneous paired-use
data. This is a finite-support, unbounded-q exclusion of the stated mandatory
original-row demand, not a universal whole-cover exclusion.

Y=7,162 remains a compatible reuse for q20771: their difference is 155.
The same original row is reusable when its q-relevant lower projections
agree; it does not consume a fresh prime for each ambient fiber.

### An intersection-first extension

For general specified restrictions on the ORIGINAL logs, require
b0=b1=Yj modulo uj, uj|w. Generalized CRT must first give a common Y modulo
M=lcm(uj); then both logs lie in that one coset. Its power-coset size is
h*=w/M=gcd(w/uj), and paired existence at K=2,E={1} is equivalent to
q|R_(h*)(Y), provided h* is odd. When h*=1, R1(Y)=-2, so no odd q can work.
This uses the coset intersection of original log constraints; it does not
assign an original arithmetic rank to a derived macro.

### Half-degree exact identity used for the arithmetic check

For h=2m+1, set

    E_h(Z)=sum_{k=0}^m binom(h,2k) Z^k,
    O_h(Z)=sum_{k=0}^m binom(h,2k+1) Z^k,
    A=5^(Yh).

Then

    R_h(Y)=(-2)^h Res_Z(E_h(Z), A^2-Z O_h(Z)^2).                   (10.4)

To prove this, write T=X+1. The two original polynomials become
E_h(X^2)+X O_h(X^2)-A and -E_h(X^2)+X O_h(X^2)-A.
Subtract them, swap the odd/even degree resultant pair (no sign on swapping
h and h-1), and pair the roots X and -X of E_h(X^2). Their products are
A^2-Z O_h(Z)^2; both resultant expressions have the same leading-coefficient factor h^h. This gives
(10.4). The verifier also accounts for the leading-coefficient power when
the second polynomial is reduced modulo E_h.

## 11. A conditional genuinely cooperative serial construction

This shows why the nonaccepted-shell condition in D2 must not be removed.
Assume an ACTUAL finite hereditary order-closed set T of support primes below
q2 contains q1 as its only nonregular prime, and q1 belongs to the required
hereditary closure of q2; every odd order part in T and
at q2 is squarefree, with all odd factors again in T. Assume s_q1 is odd,
s_q1 in E_q1, all regular support rows accept 1, and q2 accepts an odd h<s_q2.
Take r_p=2 for every p in T and r_q2=q2^h+2.

For the least p in T not dividing d, the same signed LTE argument as P5
now gives valuation s_p: it is 1 for a regular row and the accepted odd
s_q1 at the nonregular relay. If all p divide d, q2 supplies the terminal
rigid event. Hence this is a whole odd pooled cover.

Choosing E_q1={s_q1} makes q1 fail C9's rigid-valuation gate; q2's
single-nonregular closure fails because q1 is a nonregular descendant.
Thus these hypotheses would produce genuinely non-rowwise cooperation.
NO actual prime family with these hypotheses has been instantiated here.
This conditional construction is not an actual D-level success and does not
claim existence of a base-5 prime with the required odd lifting exponent.

## 12. Integer and typed obligations

For a fixed legal finite family use one-hot x_(p,s) in {0,1}, with sum_s x=1.
For each residual EITHER cell d use sum_(p,s) H_(p,s)(d)x_(p,s)>=1, where H
is the actual pooled incidence. For an A_c demand use the c incidence.
BOTH gives two tagged constraints. TRUE gives none; FALSE is infeasible.
Contraction clauses retain all original-state tokens and OR alternatives.

D1 compresses the upper-root choices; D3 eliminates independent private
coordinate blocks to profiles; D6 and D7 supply arithmetic inconsistency
cuts. None allows a different state at each residual cell.

The Phase-C 5859-state, U=1302 fractional gap is independently re-evaluated.
An exactly-two extension is also certified by adjoining two deliberately
inert nonregular states:

    q20771: r=344840143 mod q^2;
    q40487: r=477301244 mod q^2.

At each, anchor0 has a nonunit target and anchor1 is a local-zero power
class. Both full fatal masks are empty. Their actual induced extended
periods are U=284819010 and L=15958124311290. The COARSE fractional coverage
kernel remains period1302 with capacity830/651; every integral vector still
has a common escape. The nonregular rows are honestly counted as original
rows, but this is an inert extension, not new interacting-root arithmetic.

For simultaneous completeness the original condition remains
(A0 OR S0) AND (A1 OR S1) on every lower cell. A0-only cells still demand A1,
and conversely. The already proved at-least-seven result excludes two-root
BOTH certificates; it is not newly proved by the present pooled analysis.

## 13. Exactly-seven interface and remaining target

Order-DAG Theorem7.2 already excludes shared admitted relays above 3 between
the seven mandatory basins. A new argument cannot assume an overlap which
the surviving normal form already forbids. The basins still share the
3-adic boundary and parity, where D3's profile viewpoint may be useful.

A pair of basins in the seven-root frontier is required to supply its assigned
leaves, not to be a WHOLE two-root EITHER cover. Thus a two-root whole-domain
no-go cannot kill a pair merely because its private union is not complete.
The explicit conditional seven-chain construction in source Theorem12.1
also prevents asserting unconditional incompatibility of every such pair.

No actual new unrestricted two-root whole-cover prime class is claimed to
survive every old P4/Hybrid policy and be eliminated only here. No actual
whole odd pooled cover was found. The new exact exclusions are at the
mandatory role / multi-use level; D1–D5 are structural reductions and scoped
classification statements, with overlap with previous escape mechanisms.

**Next single target:** fixed K=2,E={1}, incomparable roots, each failing
C9, with dependency closures sharing only the 3-adic boundary and parity.
Classify the two complete global-state escape-profile families and decide
whether disjoint profiles can occur, starting from the actual regular
ternary heads 7,31,19,5167. Keep all parity and opposite-anchor information.
This is a focused mathematical target, not permission to invent the upper
nonregular roots or to scan primes without a gate.

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
