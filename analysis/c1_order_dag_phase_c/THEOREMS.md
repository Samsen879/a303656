# A303656 C=1 — extremal order-DAG Phase C
## Seven-origin pure-3 normal form, separated extras, and conditional completion

**Research status:** mathematical proofs proposed here, with an exact reference
laboratory. Not independently refereed or proof-assistant formalized. No repository
integration or authority change. All universal statements below are confined to
the finite admitted original-row C=1 formal class of the frozen repository.

Repository: `Samsen879/a303656`

Main: `71b8d428b32724c37e593bcfd9d5f06a42e72d21`

Tree: `5609e47eed0c058c190ef59c61644e2fd4b8fad6`

## 1. Imported formal statements and notation

An original row has a distinct prime q=3 mod 4, K_q>=2, shared residue r_q,
and accepted positive odd valuations E_q<K_q. At anchor c its value is
r_q-3^c-5^d. Local zero is unresolved, not fatal. Write

    w_q = ord_q(5), s_q = v_q(5^w_q-1),
    Q = {original q : s_q>=2}, N=|Q|.

The frozen ambient U and all coordinate depths are retained after muting events.
Derived seeds/macros have provenance; they are not new arithmetic rows.

The following are reconstructed/imported from the five requested directories:

* There is one boundary-selected anchor c_* safe two-adically on either exponent
  parity: c_*=1 for r_2=0,1 mod4 and c_*=0 for r_2=2,3 mod4. Choose a parity b on
  which the 3-row has no dynamic event. Completeness implies odd completeness at
  this fixed (c_*,b). Odd-row periods have 2-valuation at most one.
* An original rigid event contributes at most one seed at this fixed anchor and
  parity and requires s_q>=2. A dynamic row at coordinate p is one parity-shell
  bundle, omitting its center, with a fixed lower logarithm guard modulo w_p.
* With fewer than p proper p-cylinders, a parity-shell bundle covers the entire
  p-coordinate precisely by an active simple pair: shell 0 is accepted and a
  centered depth-one rigid cylinder is present.
* A linear contraction replaces a seed by its intersection with the original
  p-row's fixed lower guard after removing a centered depth-one p-cylinder. Each
  seed has at most one child and retains its original source. Intersections
  cannot erase an uneliminated prime factor or reduce its exponent.
* Before a first essential nonlinear step, the seed count never increases. At
  that step an irredundant witness has r distinct origins, p<=r and
  r=1 mod(p-1). No nonempty single-origin seed can become constant: its least
  helper would have to be the inactive row 3.
* Complete systems need at least seven original nonregular primes. More locally,
  the same argument applies to a complete linearly descended state with at most
  six retained sources: its inherited least-helper invariants give a contradiction.

The imported results are not justified by the finite tests in this bundle.

## 2. Order DAG and primed terminal Hall

Put O(q)={odd prime divisors of w_q}. Every edge q->p in O(q) strictly decreases
its numerical label because w_q divides q-1. Absolute terminals are 3 and primes
1 mod4 (including 5). Expand every admitted label >3, whether or not that row is
in the panel. Thus T(3)={3}, T(lambda)={lambda} for lambda=1 mod4, and
T(q)=union_{p in O(q)}T(p). This set is nonempty for admitted q>3: otherwise an
admitted prime of order 1 or 2 other than the regular prime 3 would be required.

At the distinguished parity, the panel frontier F'_P(q) stops at 3 or the first
missing panel row. Absolute paths can be truncated there. A receiving coordinate
lambda has lambda-1 single-anchor slots. Merging coincident actual relays retains
one outgoing guard per original row, not one per originating path.

The imported transitive guard theorem implies escape when every source subset
S satisfies |S|<=sum_{lambda in F'_P(S)}(lambda-1). Expanding an admitted relay p
cannot increase terminal capacity: the sum of lambda-1 over distinct odd factors
of w_p is at most product(lambda)-1 <= (p-3)/2 < p-1. Therefore matching to absolute
terminal slots is also sufficient. A complete system must violate absolute Hall.
This is a sufficient-policy obstruction, not an exact equivalence with completeness.

### Lemma 2.1: inclusion-minimal circuits

If S is inclusion-minimal with |S|>C(T(S)), C(A)=sum_{lambda in A}(lambda-1), then

    |S| = 1+C(T(S)),        deg_S(lambda)>=lambda.

Proof. Let m=|S|. For any q in S, minimality and integrality give
m-1<=C(T(S\{q}))<=C(T(S))<m. All quantities equal m-1, and removing q cannot remove
any positive-capacity terminal. If lambda has d<m neighbors, deleting all its
neighbors gives m-d<=C(T(S))- (lambda-1)=m-lambda, whence d>=lambda. If d=m,
C(T(S))>=lambda-1 implies m>=lambda. QED.

For sizes at most 19 the signatures are:

    3:{3}; 5:{5}; 7:{3,5}; 9,11:none; 13:{13}; 15:{3,13};
    17:{5,13} or {17}; 19:{3,5,13} or {3,17}.

A small circuit can sit in a larger Q. In particular seven pure-3 roots have
35 minimal three-root circuits, NOT one minimal seven-root terminal circuit.

## 3. Exact selected cyclotomic arithmetic

If q is prime and w=ord_q(5), then q does not divide w. In the factorization of
5^w-1, q occurs only in Phi_w(5): if q divided Phi_d(5) for a proper divisor d of
w, then 5^d=1 modq. Hence

    v_q(Phi_w(5)) = s_q,
    nonregularity <=> q^2 divides Phi_w(5).

The selected identities, with all factors certified prime, include:

    Phi_3(5)=31,                 Phi_6(5)=3*7,
    Phi_9(5)=19*829,             Phi_18(5)=3*5167,
    Phi_27(5)=109*271*4159*31051,
    Phi_54(5)=3*163*487*16018507,
    Phi_5(5)=11*71,              Phi_10(5)=521,
    Phi_7(5)=19531,              Phi_14(5)=29*449,
    Phi_15(5)=181*1741,          Phi_30(5)=61*7621.

All are squarefree. The admitted primitive factors in the first two ternary
depths are 7,31 and 19,5167. At depth three they are

    G3={163,271,487,4159,31051,16018507}.

Every listed gateway is regular. The only admitted primitive gateway of pure
7-depth one is 19531. There is no admitted primitive mixed (3-depth1,5-depth1)
gateway because every prime factor of Phi_15(5) and Phi_30(5) is 1 mod4.

At depth four, independently checked complete products are

    Phi_81(5)=4861*11419697846380955982026777206637491,
    Phi_162(5)=3*1783*5023*2066067271380136212224701233463.

All factors are certified prime and occur once; the exact-order factors are
regular. This re-verifies R_(3,e)=empty for e=1,2,3,4. It does NOT exclude
nonregular primes whose orders have larger odd prime factors but whose DAGs
ultimately end at 3.

The attempted extension of the mixed depth-one obstruction already encounters
actual admitted regular gateways at mixed depths (2,1):

    Phi_45(5)=1171*169831*297315901,
    Phi_90(5)=60081451169922001.

Here 1171 and 169831 have exact order 45 and s=1; the other two factors are 1 mod4.
Thus the depth-(1,1) zero cannot be extrapolated to all mixed depths.

## 4. New cross-strip lemma for linearly descended seeds

Work in a complete linear history at fixed (c_*,b). Consider a nonempty seed
whose remaining odd guard is supported on 3 and 5, with 3-depth at most one and
5-depth exactly one. Let A3 be the union of the fixed first 3-cylinders of helpers
7 and 31, and A5 the union of the fixed first 5-cylinders of helpers 11 and 71;
absent/inactive helpers contribute nothing. Then the seed is contained in

    (A3 x X5) union (X3 x A5).                  (CS)

Proof. If there is no helper, its original order is 5,10,15 or30. The complete
factorizations show that no such original nonregular row exists. Otherwise let
h be its numerically least helper. Every odd factor of w_h greater than 5 would
have to have been eliminated by a still smaller helper. Also the 3 and 5 depths
of w_h cannot exceed those retained in the seed. Thus w_h has odd part 3,5 or15.
Orders 15 and30 have no admitted primes. Orders 3 and6 force h=31 or7, placing
the seed in the corresponding A3 strip. Orders 5 and10 force h=11 or71, placing
it in an A5 strip. QED.

Likewise every linearly descended rank-3 depth-one seed lies in A3.
The sets A3 and A5 are fixed across ALL seeds; row states are not reselected.

## 5. New exclusion of a seven-source first nonlinear step at p=5

Assume at most seven original sources survive in the current linear state and
that the first essential nonlinear coordinate is 5. Write n for top seeds and
k for retained lower seeds. Then n>=5 and n+k<=7.

A full irredundant 5-frontier with at most seven leaves has exactly five leaves,
all at depth one: a deeper leaf would require at least nine. Every minimal top
witness therefore chooses one seed in each first 5-branch. For n=5,6,7 the maximum
numbers of such witnesses are 1,2,4 respectively (the last maximum is attained
by branch multiplicities 2,2,1,1,1). Counting ALL alternative witnesses, the full
exact contraction at 5 leaves at most

    1+2=3, 2+1=3, or 4+0=4

proper 3-cylinders. None is constant: a constant intersection would require all
five constituents to have 3-free lower guards, but such top seeds lie in only
the two fixed 5-branches of 11 and71. Retained lower seeds cannot be constant
by the inherited least-helper invariant.

A full union of at most four proper 3-cylinders must contain a depth-one cylinder
in every first branch: an irredundant deeper ternary frontier needs at least five.
Choose a first branch B outside A3; it exists since A3 has at most two branches.
A retained lower seed cannot equal B. If a contracted macro equals B, every
constituent lower guard is either unrestricted or exactly B, hence has 3-depth
at most one. By (CS), all five constituent top cylinders must then lie in A5,
which has at most two first 5-branches. They cannot cover X5. Contradiction.

This excludes p=5 for seven sources without identifying a local five-leaf witness
with a global terminal Hall circuit. It counts every alternative before using
geometry and arithmetic.

## 6. New exclusion of a seven-source first nonlinear step at p=7

An essential witness at 7 needs seven distinct origins. Thus exactly seven top
seeds and no lower seeds remain. Let G be the intersection of all seven lower
guards. Every nonlinear covering clause must use all seven origins, so all its
lower guards are G or G intersect H_7, where H_7 is the fixed dynamic guard.

If no simple pair is available geometrically, the entire exact residual is at
most one such clause. A clause involving H_7 is proper because w_7=6 retains a
3-factor. A rigid-only clause cannot be constant: seven proper 7-cylinders can
cover without a dynamic row only as the seven different first branches. If all
lower guards were unrestricted, every such depth-one seed would have least
helper of order 7 or14, or be an original rigid row of such order. The latter
do not exist, and the former all use the one fixed 7-branch of the regular helper
19531. Seven distinct first branches are impossible.

If a simple pair is geometrically available, any essential nonlinear witness
must occur with the dynamic row inactive, since G activates its centered seed.
Thus it is rigid-only and again consists of the seven different first branches.
There is exactly one centered first-branch seed. The full residual is contained
in the union of its simple-pair guard and G. Each is a proper CRT cylinder on
coordinates below 7, hence has measure at most 1/3. No lower dynamic event remains:
3 is inactive and 5 has no admitted row. Two such cylinders cannot cover.

This excludes p=7. The argument does not suppose that one chosen nonlinear clause
is the whole residual; the possible simple-pair clause is included explicitly.

## 7. Seven-origin pure-3 normal form

### Theorem 7.1

For a complete system with exactly seven original nonregular primes, the first
essential nonlinear step at the distinguished (c_*,b) is rank 3, with all seven
original sources surviving. Its irredundant frontier has depth profile

    (number at depth1, depth2, depth3) = (2,2,3).

The depth-one heads are exactly 7 and31; the depth-two heads are exactly 19 and
5167; the three depth-three heads are three distinct members of G3. Their fixed
guards form a full prefix frontier, up to its actual positions.

Proof. The first rank is <=7, hence is 3,5 or7. Sections5 and6 eliminate 5 and7.
The source shallow-head bound is 2/3+2/9=8/9, so a full ternary frontier requires
a depth>=3 leaf. Seven leaves force maximum depth3 and the unique complete-tree
profile (2,2,3). A depth-one leaf cannot be an original rigid resource. It must
use a head from 7,31, and the two disjoint first leaves force one of each. A
remaining depth-two leaf cannot use either shallower head, since its guard would
lie inside a previously occupied first branch. It must use 19 or5167; the two
leaves force both. The remaining three depth-three leaves cannot use those four
shallower heads and cannot be raw rigid resources, so they have distinct heads
from G3, one for each last sibling branch. QED.

### Theorem 7.2: arithmetic DAG consequences

For each root q, let D(q) be q together with every admitted descendant >3 in its
absolute order DAG. In the situation of Theorem7.1:

1. T(q)={3} for every q. Every proper admitted descendant is present in the
   actual panel and is a dynamic helper at the chosen anchor/parity.
2. Every proper admitted descendant is regular. The seven sets D(q) are pairwise
   disjoint; in particular Q is an order-reachability antichain.
3. If q's final leaf has depth d in {1,2,3}, then every x in D(q) satisfies

       v_3(w_x)<=d,       v_p(w_x)<=1 for every odd p>3.

   All odd support above 3 belongs to that same actual regular basin. No free
   odd terminal except 3 is allowed in the root's closure. Every proper helper
   must accept valuation 1, and each linear incoming cylinder must be centered
   at its actual fixed dynamic center. These support constraints concern ord_x(5),
   not all prime factors of x-1.
4. The actual row3 must exist and have a nonempty dynamic component on the other
   parity at c_*.

Proof. A surviving linear seed cannot drop a remaining coordinate except through
its actual centered dynamic helper, and intersecting that helper's lower guard
introduces all odd factors of its order. Induct down the absolute order DAG.
A missing or non-admitted coordinate >3 would stop the seed; hence its only
terminal is 3 and every admitted descendant >3 is an actual helper. All seven
nonregular original rows supply rigid seeds at c_*, so none can also be a dynamic
helper there. Thus every proper descendant is regular and no root reaches another.
Every eliminated p>3 must have depth one; the retained 3-depth never decreases.
This proves (1), the regularity in (2), and (3).

For disjointness, a shared admitted descendant would have a shared last gateway
g->3. Its fixed 3-cylinder contains both final leaves. At depth1 the only such
gateways are 7,31, and each cylinder is already one of the two first leaves. At
depth2 the only gateways are 19,5167, and each is one of the two second leaves.
Neither can contain another disjoint frontier leaf. A gateway of depth3 cannot
contain two distinct leaves of depth at most3. No greater gateway depth is
possible. Thus no admitted descendant can be shared.

If row3 has no dynamic event on either parity, apply the same argument at both
parities of c_*, each of which must be complete. Both would require the fixed
7-row to be dynamically active. Its order6 guard permits only one parity. This
contradicts completeness and proves (4). QED.

This is an exact necessary normal form, not an enumeration of all possible prime
values or an existence theorem for a seven-root arithmetic ledger. Its terminal
Hall obstruction is a three-root circuit with four further difficult roots, not
a seven-root minimal Hall circuit.

## 8. Small core plus separated extra roots

Let N<=12 and define

    H = {q in Q : T(q) subset {3,5}}, E=Q\H.

### Theorem 8.1: terminal-pruning dichotomy

A complete system must satisfy

    |H|>=7; and if |H|=7, every q in H has T(q)={3}.

In the equality case the seven H roots have all the normal-form properties of
Section7, including the disjoint regular basins. Equivalently, H of size at most
six is harmless even when embedded in Q with up to twelve roots; H of size seven
containing a 5-terminal is also excluded.

Proof. There are at most N<=12 original rigid seeds. At every coordinate p>=13
this is strictly fewer than p, so the exact saturation equals the linear residual
by the sparse lemma. Eliminate these coordinates in decreasing order. Completeness
is preserved, source count cannot increase, and the original ledger/U stay frozen.

Every q in E reaches an absolute terminal lambda>=13. A seed surviving along
that path would have to contract through each admitted relay and inherit its
next factor. At the free terminal no dynamic row exists, so it cannot survive
below 13. Missing/inactive relays only cause it to disappear earlier. Therefore
all surviving seeds below13 originate in H. The six-descended-source theorem
excludes |H|<=6. If |H|=7, all seven must remain and be active. Coordinate11 is
linear, and Sections5--7 force a rank3 (2,2,3) frontier, hence T(q)={3} for all H.
No E root can be a helper below a pure3 H root, since its large terminal would
then also belong to that H root. Thus all proper descendants are regular as in
Theorem7.2. QED.

This gives a genuine core-plus-extras theorem. It does not assume a minimal Hall
circuit has size seven, nor delete E roots merely because a matching intention
has been announced. Their deletion is justified by exact linear saturation.
An ascending alternative for |H|<=6 routes each E root towards a >=13 terminal;
these paths stay above12 and cannot increase the small-coordinate loads.

## 9. New interface with the bounded inventory

The imported complete inventory at q<=2,000,000,000 contains exactly
20771,40487,1645333507. This session does not replay that range scan, but separately
verifies these primes, their exact orders/lifting exponents and their entire
absolute closures:

    20771:       w=5*31*67,                    T={3,5};
    40487:       w=2*31*653,                   T={3,653};
    1645333507:  w=2*3^3*30469139,             T={3,761,1429}.

For the last closure, 30469139 has order1429*1523 and 1523 has order2*761.
Only 20771 belongs to H, and it is not pure3.

### Corollary 9.1

Every complete certificate requires at least SEVEN original nonregular primes
strictly greater than 2,000,000,000.

Proof. If N>=13, the inventory gives N-3>=10 such primes. If N<=12, apply Theorem8.1.
For |H|=7, all H are pure3 and hence none is one of the three listed primes.
For |H|>=8, at most one H prime is listed, leaving at least7 outside the bound.
QED.

The unbounded theorem is the terminal-pruning/normal-form result; the numerical
cutoff occurs only in this corollary. No density or rarity extrapolation is used.
The total-root lower bound remains seven. If k of the three listed primes are
actually included in a panel, that panel needs at least 7+k nonregular roots;
including all three therefore forces at least10, not an unconditional >=10.

## 10. P4 failure and a joint release/allocation abstraction

For one frozen state, let C_(q,p) be the union of the rigid log projections of q
onto p^{v_p(w_q)}, with at most two components for paired blocking, one for the
selected-anchor version. For a finite parity-shell bundle, the worst dynamic
envelopes are D_p<p/(p+1) when s_p is odd and D_p<1/(p+1) when s_p is even;
D_p=0 at a free coordinate. The inequalities are strict because the bundle has
finite depth and omits its center. An allocation A assigns one allowed p to each original
rigid row. Write B_p(A) for the exact projected union and D_p for a valid uniform
conditional dynamic mass bound. The imported P4 theorem proves escape if

    D_p + mu(B_p(A)) < 1 for every p.

Thus a complete certificate must satisfy, for every A, failure at some p. This is
failure of a sufficient test, not an equivalence with coverage. Scalar mass>=1
never establishes an exact full union.

### Lemma 10.1: exact residual-slack obstruction

Keep the ambient, all row states, and all dynamic components fixed. Let S be an
inclusion-minimal set of rigid roots not allocatable under this P4 sufficient
criterion. For q in S and any successful allocation of S\{q}, write

    delta_p = 1-D_p-mu(B_p)>0.

Every blocker option p of q then satisfies

    delta_p <= mu(C_(q,p)\B_p) <= t_(q,p)/p^{v_p(w_q)},  t_(q,p)<=2.

Otherwise adding q at that p preserves every strict budget. QED.

This is the correct multi-root extension of the single-root deep/free-blocker
argument. A high order multiplicity is not universally impossible; in a failing
minimal set, every such option must face sufficiently small residual slack.
For exactly seven roots, the stronger squarefree-above3 conclusion instead
follows from the proved complete-system linear normal form in Section7.

### Lemma 10.2: joint selected-anchor release/allocation sufficiency

At the fixed boundary, choose a set R of actual rows to kill by positive-divisibility
guards. Each r in R selects an odd b(r)|w_r. Let F_p be the exact union of their
fixed positive-log projections at p, counting each actual sending row once.
Assign the remaining original rigid events to blockers, with exact unions B_p.
If

    1_{p not in R} D_p + mu(F_p union B_p) < 1   for every p,             (HY)

then there is a one-anchor escape. The row3 is already inactive and is not
assigned a nonexistent odd factor.

Proof. Choose coordinates increasingly. Every released row r is made nondividing
at b(r)<r before its own coordinate is reached, so its dynamic hazard is genuinely
zero there. All other dynamic activity depends only on already fixed lower guards
and is bounded by D_p. Choose a point outside the exact forbidden union at each
coordinate. An assigned rigid event has a necessary order projection violated no
later than its largest order coordinate. CRT and the inherited reverse-lift theorem
complete the escape. QED.

This contains selected-anchor P4 when R is empty and transitive guard forests when
all nonregular hazards are released and all receiving rows are also released.
It keeps positions, depths, dynamic slack, and relay coalescence in one abstraction.
It is still a sufficient policy, not an exact primal characterization.

For an ordinary Hall/min-cut relaxation, retain only options with depth>=e_p and
at most t_p projected components. Set k_p to the largest nonnegative integer with
D_p+k_p*t_p/p^{e_p}<1. A matching with capacities k_p implies P4 escape. Therefore
completeness forces a deficient subset in every such retained-option graph.
This is an exact min-cut statement for that chosen slot relaxation only. Variable
depths, overlapping positions, release choices and global row states do not acquire
an ordinary-flow min-max theorem merely by this encoding.

## 11. Why the proof does not raise the total bound to eight

For seven sources, Sections5 and6 exclude ranks5 and7, leaving the real rank3
normal form. It has seven distinct actual regular heads and a full (2,2,3)
frontier; the relevant cyclotomic head inventory does not eliminate it.
In particular T(q)={3} does NOT say w_q=3^e or2*3^e, or even that3 divides
w_q directly. Larger admitted factors can relay to3. The original R_(3,e)
exclusions cannot be applied to all pure3-terminal roots.

At eight sources, the rank5 alternative count can already be eight (first-digit
multiplicities2,2,2,1,1), rather than four. A proper 3-residual can then have a
seven-leaf deep frontier. Our depth-one cross-strip argument no longer applies.
At nine sources a 5-frontier can itself have depth2. A raw original rank3
nonregular leaf must have depth at least5 by R_(3,1..4)=empty; if such a leaf is
essential in a rigid-only ternary frontier, the depth tax forces at least11
leaves. This does not charge 11 origins for an arbitrary reusable nonlinear
macro, nor assert existence of a depth5 raw resource. At eleven sources rank11
also becomes a possible first nonlinear coordinate. The imported rank/leaf tax
gives these remaining candidate local witness sizes, not existence claims:

    N=7:     p3:{7}, p5/p7 excluded here;
    N=8:     p3:{7}, p5:{5},   p7:{7};
    N=9,10:  p3:{7,9},p5:{5,9},p7:{7};
    N=11,12: p3:{7,9,11},p5:{5,9},p7:{7},p11:{11}.

Theorem8.1 adds the low-terminal restrictions at every N<=12. No complete arithmetic
seven-root family has been produced, but no proof that this class is empty has
been obtained either. Therefore no total-root bound >=8,...,>=13 is asserted.

## 12. Conditional arithmetic completion theorem

This gives a sharply stated surviving arithmetic requirement, not seven invented
prime rows and not an assertion that a complete certificate already exists.

Fix actual regular heads

    H0={31,7,19,5167,271,4159,31051}.

For each h in H0 assume a finite chain of actual admitted primes

    h=p_0 < p_1 < ... < p_k=q_h,   k>=1,
    ord_{p_i}(5)=p_{i-1} for 1<=i<=k,
    s_{p_i}=1 for i<k, and s_{q_h}>=2.                       (CHAIN)

### Theorem 12.1

If (CHAIN) holds for all seven heads, there exists a complete finite admitted
C=1 certificate with exactly the seven nonregular roots q_h, all K=2 and E={1}
for the odd rows.

Proof. Chains above distinct heads are disjoint: a prime-order chain has a unique
predecessor; none of these heads can occur above another in such a chain. All
intermediate rows are regular by hypothesis.

Work at c=1. Set r_p=4 for each regular intermediate p above its head, and set
r_{q_h}=q_h+4 mod q_h^2. The root is rigid exactly at d=0 mod p_{k-1}.
A regular intermediate p_i with r=4 covers d=0 mod p_{i-1} whenever d!=0 mod p_i.
Inducting down the chain, its union with all higher rows therefore covers the
entire condition d=0 mod h. No assertion about a new prime macro is used.

Choose head parameters so that its own h-coordinate center is zero and its
lower logarithm guard is, respectively,

    h=31: d=0 mod3;
    h=7: d=4 mod6   (even parity and d=1 mod3);
    h=19: d=2 mod9;
    h=5167: d=14 mod18 (even parity and d=5 mod9);
    h=271: d=8 mod27;
    h=4159: d=17 mod27;
    h=31051: d=26 mod27.

For a desired log ell mod w_h choose d_h=ell mod w_h and d_h=0 mod h by CRT,
and take r_h=3+5^{d_h} mod h^2. Its regular dynamic row covers the complement of
the h-center under that guard, and the chain covers the h-center. Thus that
whole lower guard is covered.

For even d, the seven guards form exactly the full ternary frontier
C1(0),C1(1),C2(2),C2(5),C3(8),C3(17),C3(26).
For odd d, use row3 with K=2, r_3=2 mod9. Its accepted valuation-one set is
precisely d odd and d!=0 mod3. The remaining odd exponents d=0 mod3 are covered
by the head31 chain. Hence the odd-row system is complete at c=1 on both parities.

Finally choose the sound two-adic row K_2=2,r_2=1 mod4. At c=0 its local value is
1-1-5^d=3 mod4 for every d, so that anchor is always rejected. At c=1 the local
class is1 mod4 and the already complete odd subsystem supplies rejection.
All row residues come from one global residue by CRT over pairwise coprime prime
squares. Every regular row's own prime occurs in its parent's order; row3's prime
occurs in the heads' orders. Consequently the final induced U contains all needed
regular p-digits and L=U. No unsupported coarse digit or accepted local zero is
introduced. This proves complete C=1 coverage conditionally on (CHAIN). QED.

The reference fixture checks the ACTUAL regular heads and row3, including 1,051,299
full-period regular-row comparisons, and the 54 collapsed parity/3^3 classes. It
has not instantiated any q_h. Its formal upstream seeds are labelled conditional.

For every admitted prime p, Phi_p(5)=3 mod4 and Phi_p(5)=1 modp. Thus it has some
admitted prime factor q different from p with exact order p, and q>p. This proves
that arbitrary-length actual admitted prime-order chains exist. It does NOT
prove a nonregular hit on any chain. At such a hit the exact arithmetic requirement
is q^2|Phi_p(5), not merely q|Phi_p(5). Primitive-divisor existence alone cannot
supply that square factor. For h=7 the first parent is specifically19531 and is
regular; the unbounded higher chain remains the arithmetic gap.

Thus a purely abstract terminal-count proof cannot reject this conditional
completion by pretending that regular gateways count as nonregular roots.

## 13. Next single mathematical target

Define B7 to be the class of admitted nonregular roots with T(q)={3}, whose entire
proper admitted descendant closure is regular, whose only last gateway into3 is7,
whose orders throughout that basin are squarefree above3, and whose 3-depths
throughout are at most1. Every seven-root complete certificate must contain a
member of B7 (the source of the depth-one leaf headed by7).

The next single target is to prove B7 empty or to produce a certified actual
member, retaining the exact order-DAG definition. Empty B7 would raise the total
bound to at least8. A member would not be a complete certificate, but would
instantiate a previously unfilled mandatory arithmetic basin. Prime-order
chains from7 form only a sufficient subfamily; proving no hit on those chains
alone would not exclude all of B7.

## 14. Evidence and scope

`reference.py` is standard-library-only and verifies 93 recursive full n-1 Lucas
certificates, 20 selected cyclotomic products/orders, the three source-root DAGs,
2,187 labeled seven-root terminal graphs, prefix profiles with at most12 leaves,
and the conditional regular-row fixture. Ten regression tests pass, including
corrupted primality certificates. Discovery used SymPy; primality is not trusted
to its probable-prime declarations. All computations were local standalone runs.

No full local repository checkout, repository-native test replay, or repetition
of the 2e9 scan was performed. Source diffs and pinned files were read through
the GitHub connector. The five requested directories were retrieved via the
merged package diffs, with load-bearing current-main files fetched separately.
No proof-assistant or independent-author verification is claimed.

    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED
    GITHUB WRITES PERFORMED: NONE
