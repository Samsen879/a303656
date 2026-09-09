# B7 branching: closed regular states, maximal generators, and exact size gates

## Scope and evidence convention

These are proposed, self-contained mathematical deductions for the intrinsic
basal-gateway B7 class of the pinned repository. They are not a repository
promotion, independent-author review, proof-assistant formalization, or a solution
of A303656. The source imports are identified in SOURCES.md. The finite executable
checks do not prove the universal quantifiers below by sampling.

Edge convention throughout: **larger admitted prime -> odd prime dividing its
exact multiplicative order of 5**. Arrows in an upward path are discussed in words,
not substituted for this edge convention.

## 1. Definitions and imported arithmetic

For an admitted prime p (p = 3 mod 4), put

    w(p) = ord_p(5),  s(p) = v_p(5^w(p)-1),
    O(p) = {odd prime divisors of w(p)},  H(p) = O(p) \ {3}.

An admitted prime is regular if s(p)=1 and nonregular if s(p)>=2. For an absolute
order DAG, expand every admitted label >3 whether or not it occurs in a particular
panel. Stop at 3 and at primes =1 mod4. Write T(p) for the terminal set and D(p)
for p together with its admitted descendants >3, excluding terminal 3. Put

    Gamma(p) = {v in D(p) : O(v)={3}}.

The class B7 consists of admitted nonregular q with T(q)={3}, every proper member
of D(q) regular, Gamma(q)={7}, and every w(v), v in D(q), squarefree. The last
formulation is equivalent to the Phase-D odd-order conditions since v_2(w(v))<=1
for every admitted prime. This is a restriction on w(v), NOT on v-1.

It does not require that 7 be the only vertex with a direct edge to 3.
In particular, w(43)=42 and w(7)=6 are compatible with the basal definition.

A **good regular state** R is a finite, nonempty set of actual regular admitted
primes >3 such that 7 belongs to R, all their exact orders are squarefree,
H(v) is contained in R for each v, and H(v) is nonempty for every v other than 7.
Here the actual order w(7)=6 is understood. All factors in H(v) must themselves
be admitted vertices, not free 1-mod-4 terminals.

Because edges strictly decrease, every vertex of a good state reaches 7. Thus a
good state is precisely a finite union of B7-compatible regular closures. It need
not be the closure of a single maximum, and it need not have a realizable
nonregular root above it. For q in B7, R=D(q)\{q} is a good regular state.

We import Phase-D's complete first-relay classification:

    A7={43,127,379,7603,19531,519499}.

All six primes are regular. Their orders are 42,42,21,42,7,21 respectively.
The least vertex other than 7 in any B7 basin belongs to A7, and |D(q)|>=3.
For |D(q)|=3 the 48 root-order indices are

    I(r)={kr : k in K},  r in A7,
    K={1,2,3,6,7,14,21,42}.

The source has excluded five indices, not all 48. Its finite-height regular
closure recursion already exists; the new recursion below retains exact closed
states and cardinality rather than replacing them by a union of all height-bounded
vertices.

For n>1 define the following finite sets without probabilistic primality labels:

    RegPrim(n) = {p prime : p=3 mod4, p does not divide n,
                           p | Phi_n(5), p^2 does not divide Phi_n(5)},
    SqPrim(n)  = {q prime : q=3 mod4, q does not divide n,
                           q^2 | Phi_n(5)}.

When p does not divide n, p | Phi_n(5) is equivalent to ord_p(5)=n. At exact order
n, the valuation of Phi_n(5) equals s(p). One proof of the converse uses that
X^n-1 is separable modulo p: distinct cyclotomic factors have disjoint root sets.
Exact order can instead be certified by a full power equality and all prime-divisor
order-drop inequalities. Thus these definitions are finite arithmetic gates,
not assertions that the sets have been completely factored in this session.

## E1. Inclusion-minimality is automatic for a fixed root

**Theorem.** D(q) is the unique least admitted-support-closed set containing a
fixed admitted q. Consequently any deletion of a proper vertex while retaining
q fails closure somewhere, regardless of whether D(q) is a tree or a branching
DAG.

**Proof.** Let E contain q and contain every admitted odd order factor >3 of each
of its vertices. Induction on the length of a path starting at q gives D(q)
contained in E. D(q) itself has the closure property. If a vertex of D(q) is
removed, choose a path from q to that vertex and its first omitted endpoint. The
previous retained vertex has a required order-support factor absent from the
retained set. QED.

Thus the proposed inclusion-minimal basin definition cannot by itself impose
indegree one, bounded branching, a tree, or a smaller nonregular root. Deleting
edges that are redundant for reachability is also not an arithmetic operation:
the exact order of a fixed prime cannot be changed.

**No internal B7 descent.** If q belongs to B7, no proper vertex of D(q) belongs
to B7 because all are regular. Any genuinely smaller B7 witness extracted from
a putative minimal member must introduce a different actual nonregular prime
outside D(q). A graph-only deletion does not supply it.

## E2. The mandatory maximal-generator antichain

For a good regular state R define

    A(R)=R \ union_{v in R} H(v).

These are precisely the vertices with no incoming edge from another vertex of
R, equivalently the maximal vertices under order reachability. They are not
necessarily just the numerically largest vertex. The numerically largest vertex
always belongs to A(R), and A(R) is nonempty.

For S contained in R write Cl(S)=union_{p in S}D(p), with Cl(empty)=empty.

**Theorem.**

    Cl(S)=R  if and only if  A(R) is contained in S.

**Proof.** A maximal vertex cannot be reached from any other vertex, so every
set generating all of R must include it. Conversely take v in R. If it is not
maximal, follow an incoming edge to a strictly larger vertex in R. The process
terminates because R is finite. Reversing this path shows that v is a descendant
of a maximal vertex. Therefore A(R) generates R, and every S containing it does
as well. QED.

The reachability-reduced graph is a useful representation of this partial order,
but **all original exact-order edges remain part of the arithmetic data**.

## E3. Exact terminal-index family and closure cost

Put Delta={1,2,3,6} and define

    J(R)={delta * product_{p in S} p : delta in Delta,
                                      A(R) contained in S contained in R}.

**Theorem.** For every good regular state R,

    {q in B7 : D(q)\{q}=R} = union_{n in J(R)} SqPrim(n),
    |J(R)| = 4 * 2^(|R|-|A(R)|).

**Proof, forward.** Set S=H(q). Squarefreeness gives w(q)=delta*product(S) for
one delta in Delta. The proper admitted closure is Cl(S)=R, so E2 forces
A(R) contained in S. The exact-order cyclotomic valuation identity gives
q in SqPrim(w(q)).

**Proof, converse.** Let n be in J(R) and q in SqPrim(n). Then ord_q(5)=n and
q>n>=max(R), the last inequality holding because max(R) belongs to A(R).
The admitted support of n is exactly S. Its closure is R by E2. Every proper
admitted descendant is regular, every order is squarefree, the unique basal
gateway is 7, and the only absolute terminal is 3. The root is nonregular by
the square condition, and its nonempty admitted support prevents a new basal
gateway. Thus q is in B7 with precisely the asserted closure. Finally, the
optional primes R\A(R) may each be included or omitted, and unique prime
factorization separates their choices and the four Delta choices. QED.

For an index whose admitted support consists of good regular vertices, define

    c(n)=1+|union_{p|n, p>3} D(p)|.

This is the **exact terminal basin cost** of every prime in SqPrim(n), not the
sum of the separate branch sizes. Shared descendants are counted once. An
empty square-hit set does not change the cost assigned to its candidate index.

The pair consisting of the actual closed state and its mandatory antichain is a
canonical critical structure. It is stronger than choosing one convenient path,
but it does not give a uniform bound on the state's size.

## E3.1. One primitive-only critical integer for each closed state

Set

    a_R=product_{p in A(R)}p,
    b_R=6*product_{p in R\A(R)}p,
    W_R=Phi_(a_R)(5^b_R).

Both products are squarefree and gcd(a_R,b_R)=1. Then

    W_R=product_{d|b_R}Phi_(a_R*d)(5)
       =product_{n in J(R)}Phi_n(5).

To see the polynomial identity, for coprime a,b a complex root z satisfies
ord(z^b)=a precisely when ord(z)=a*d for some d|b. All the roots are simple,
and comparing monic factors gives Phi_a(X^b)=product_{d|b}Phi_(a*d)(X).

Let p=max(R), and put

    Z_R = W_R/p  if A(R)={p},
    Z_R = W_R    if |A(R)|>=2.

**Theorem.** Z_R is an integer, all its prime factors are strictly greater than
p, and

    {q in B7:D(q)\{q}=R}
       ={q prime : q=3 mod4, q^2 divides Z_R}.

Thus Z_R is a single, explicitly given primitive-only integer encoding all the
terminal order choices of that fixed state. This is not a complete factorization
claim and does not reduce the base-5 order of every divisor to a_R.

**Proof of the imprimitive cleanup.** Each index n in J(R) is squarefree and
contains p. If a prime l<=p divides Phi_n(5), l is not 5. If l did not divide n,
its exact order would be n>=p>=l, impossible. Thus n=l*m with l not dividing m.
For such squarefree indices,

    Phi_(l*m)(X) = Phi_m(X^l)/Phi_m(X)
                = Phi_m(X)^(l-1) modulo l.

Consequently l divides Phi_m(5), and since l does not divide m its exact order
is m. If l<p, then p divides m, contradicting m=ord_l(5)<=l-1. Therefore l=p.
If A(R) contains a second vertex r, it would divide m=w(p), so p->r would be
an incoming edge to r within R, contradicting r in A(R). Thus there are no small
prime factors at all in the multiple-maximum case.

If A(R)={p}, the unique possible imprimitive index is n=p*w(p). It does occur
in J(R), since w(p) divides b_R by the state's squarefree closure conditions.
The LTE increase from 5^w(p)-1 to 5^(p*w(p))-1 is exactly one at p. Hence the
imprimitive factor p occurs once in Phi_(p*w(p))(5), and no other index in J(R)
contains p as an imprimitive factor. Equivalently, in this singleton case
W_R=(5^(p*b_R)-1)/(5^b_R-1) has p-valuation one by LTE. This proves the exact
cleanup. The same order argument handles the prime 2; 5 is excluded by the
constant term Phi_n(0)=1 for n>1.

Every remaining prime q>p is coprime to every index in J(R). It divides at most
one of their cyclotomic values, since its base-5 exact order is unique. Therefore
q^2 divides Z_R exactly when it belongs to SqPrim(n) for one of those indices.
Apply E3. QED.

Examples checked as exact integer identities without factoring the large values:

    R={7}:          Z_R=Phi_7(5^6)/7;
    R={7,43}:       Z_R=Phi_43(5^42)/43;
    R={7,43,127}:   Z_R=Phi_5461(5^42).

For the last state this single integer encodes all eight {43,127} fork indices.
The replay checks its regular factor 6717031 appears exactly once. Only the
fixed-state arithmetic ledger has been compressed; no global bound on R,
no same-prime order descent, and no absence of admitted square factors is inferred.

## E4. Canonical finite-size recursion

Define F_1={{7}}. Given R in F_k, consider every nonempty S contained in R and
all delta in Delta. Set n=delta*product(S). For every p in RegPrim(n) with
p>max(R), insert R union {p} in F_(k+1), deduplicating equal states.

The new maximal-generator set is exactly

    A(R union {p}) = (A(R)\S) union {p}.

One must NOT demand A(R) contained in S for these intermediate transitions.
Such a demand would silently discard valid forks. Containment of all maxima is
required only at a terminal step intended to generate the entire state.

**Theorem.** F_k is precisely the family of good regular states of cardinality
k. Every F_k is finite and effectively computable in the mathematical sense.
Every good state has a unique history of numerical insertion, though equal
states may be encountered by an implementation that does not canonicalize.

**Proof.** A legal extension is an actual regular admitted prime, its exact order
is squarefree, and its nonempty admitted support is contained in the old state.
It introduces no new terminal or basal gateway. Conversely, list any good state
in increasing numerical order. The least vertex is 7. Every prefix is a good
state because all dependencies are smaller; the next vertex has precisely a
nonempty subset of the prefix as admitted support and one of the four Delta
factors. It passes the specified transition. Its true exact order determines
the transition uniquely. For finiteness, there are finitely many states at level
one. A fixed finite state has finitely many supports and hence finitely many
explicit cyclotomic integers; each integer has finitely many prime divisors.
Induction proves level finiteness. Exact integer factorization and primality can
in principle be performed by terminating trial division. This is an effective
finiteness statement, not an efficient algorithm or a claim of executed full
factorizations. The formula for A follows by removing the old vertices now hit
by the new edges and adding the new largest vertex. QED.

In particular F_2={{7,r}:r in A7}. This imports the six first-relay roots instead
of reproving them as the main result.

For any fixed M>=2 set

    C_(<=M)=union_{1<=k<=M-1} union_{R in F_k} J(R).

It is a finite, explicitly recursively specified family and satisfies the exact
identity

    {q in B7: |D(q)|<=M}=union_{n in C_(<=M)} SqPrim(n).

The first four extension orders contribute no nonregular primes by the imported
first-relay proof. The recursive size bound M is fixed before generation. There
is no uniform M proved here for all B7 members, and the union over all M is not
proved finite. Finitely branching is not finite depth.

## E5. The complete four-vertex classification

Suppose D(q)={7,r,s,q}, with 7<r<s<q. The first-relay theorem gives r in A7.
There are exactly two cases.

### Fork

If H(s) does not contain r, it equals {7}; hence s is another member of A7.
The good state R={7,r,s} has maximal antichain {r,s}. Therefore

    C4_fork={k*r*s : r<s in A7, k in K}.

There are binomial(6,2)*8=120 distinct indices. Every primitive admitted square
hit at one of these indices is exactly a four-vertex fork B7 member, and every
such member occurs here. The entire numeric list is generated in C4_FORK_120.txt.

For {r,s}={43,127}, its eight indices are

    5461,10922,16383,32766,38227,76454,114681,229362.

### Serial

Otherwise r divides w(s), and all other allowed factors are 2,3,7. Define

    S_r=union_{k in K} RegPrim(kr).

Each s in S_r has D(s)={7,r,s}. None belongs to A7. The state R={7,r,s} has
A(R)={s}, so its 16 terminal indices are

    delta*7^e*r^f*s,  delta in Delta, e,f in {0,1}.

Thus

    C4_serial=union_{r in A7} union_{s in S_r}
              {delta*7^e*r^f*s : delta in Delta, e,f in {0,1}},
    C4=C4_fork union C4_serial.

The S_r are finite and pairwise disjoint: the exact closure of a member identifies
its unique first relay. Unique prime factorization makes all the displayed
indices distinct, including across the fork and serial families. In particular

    |C4|=120+16*sum_{r in A7}|S_r|.

This is a complete, finite factor-parametrized formula for all four-vertex B7
orders. The six S_r were NOT completely materialized in this session; only the
fork family is a fully emitted numeric list. Five independently certified members
of S_43 are 9547,42743,18471511,558801427,7866608083; they are examples, not its
complete inventory.

**Proof of exhaustiveness.** H(s) is a nonempty subset of {7,r}. If r is absent
we are in the fork case. If r is present we are in the serial case, independently
of whether the extra edge s->7 is present. E3 then gives all and only the listed
terminal possibilities. Conversely the stated regular states are good and E3
turns every admitted primitive square hit into the appropriate B7 member. QED.

This goes beyond the Phase-D 48-index, three-vertex gate without claiming a
uniform bound on arbitrary B7 basins.

## E6. Certified arithmetic obstructions to naive local reductions

### An actual regular diamond

The prime t=6717031 satisfies

    t-1=2*3*5*41*43*127,
    w(t)=5461=43*127,
    5^127 mod t=6238090,  5^43 mod t=3428912,
    5^5461 mod t^2=5828690216189=1+867748*t.

Hence t is regular. Primality is certified both by complete trial division and
by the full-(t-1) Lucas certificate in results.json: base 3 has full power 1 and
gcd(3^((t-1)/l)-1,t)=1 for every l in {2,3,5,41,43,127}, whose product is t-1.
Those small factors are themselves certified prime. The Lucas criterion follows
by reducing the equalities modulo any prime divisor of t: its multiplicative
group order must be divisible by t-1, forcing that divisor to be at least t.

Together with w(43)=w(127)=42 and w(7)=6, this gives the actual regular closure

    t -> 43 -> 7,
    t ->127 -> 7,

with the additional true 3-edges from 43,127,7. Its admitted closure has four
vertices, its terminal set is {3}, and its sole basal gateway is 7. Deleting
either incomparable branch loses a necessary exact-order factor of t.

It refutes tree/branch-redundancy lemmas asserted for all B7-compatible regular
basins. It does NOT refute a theorem restricted to actual nonregular B7 roots:
t itself is not B7, and no nonregular prime above this state is supplied.

At the last step of any spine to t, the possible predecessor is 43 or 127, and
the cofactor is respectively 127 or 43. Neither is in K. Thus the proposed
universal eight-multiplier local rule fails on this actual regular state.
Moreover the maximum-factor spine runs through 127 and misses the basin's least
proper relay 43. A canonical maximum-factor spine need not pass through the
first relay of the entire basin.

### A transitive edge cannot be arithmetically erased

The actual regular prime u=42743 has

    w(u)=602=2*7*43,
    5^602 mod u^2=1230955658=1+28799*u.

Its closure is {7,43,u}. The edge u->7 is redundant for reachability because
u->43->7 also exists, but removing the factor 7 from its exact order would give
86, which is false. The replay checks u does not divide Phi_86(5).

### The abstract nonregular-root model

One may put an uninstantiated, nonregular-coloured formal root Q above the actual
state {7,43,127}, with formal exact-order label 5461. Its coloured support graph
has a four-vertex, inclusion-minimal fork, compatible with terminal, gateway,
and multiplicity combinatorics. What it lacks is an actual admitted prime Q with
Q^2 | Phi_5461(5). This formal model is not an arithmetic counterexample and
cannot decide whether a smallest actual B7 member has three vertices. It merely
locates the omitted arithmetic premise of a graph-only proof.

## E7. What a critical spine and cyclotomic composition do not supply

A deterministic path exists: repeatedly follow the largest admitted odd factor
until reaching 7. In reverse traversal every step has w(child)=parent*m with
squarefree m, coprime to the parent. However m records side-support primes; E6
shows that they cannot in general be ignored or put in K.

For a fixed numerical largest predecessor p there is a finite overfamily

    m divides 6 * product_{7<=r<p, r prime=3 mod4}r.

That bound depends on p and can grow without bound. It is a safe local alphabet,
not a uniform finite multiplier set or a global critical family.

For a prime l not dividing m, the cyclotomic identity is

    Phi_(m*l)(5)=Phi_m(5^l)/Phi_m(5).

If an actual q has exact order m*l, it divides the numerator but not the
 denominator. A square hit in that numerator is at base 5^l, not a square hit
in Phi_m(5) at base 5. More generally q cannot divide 5^d-1 for a proper divisor
d of its exact order. The identity therefore does not transfer the same prime
to a smaller admissible terminal index.

Together with E1, this means that a successful compression needs a new actual
nonregular prime outside the old basin, with separately certified support and
square divisibility. No such transfer theorem is proved here.

## E8. Why the regular-state tree cannot close by finite exhaustion under emptiness

**Conditional structural theorem.** If B7 is empty, every finite good regular
state has a strictly larger good regular extension. In particular good regular
states exist with arbitrarily large cardinality under that hypothesis.

**Proof.** Let p=max(R). Since p is an admitted odd prime,

    Phi_p(5)=1+5+...+5^(p-1)=3 mod4,
    Phi_p(5)=1 modp.

The first congruence forces some prime divisor z=3 mod4; the second excludes z=p.
Also 2 and 5 do not divide this integer. Thus z is a primitive exact-order-p
factor, so z>p and w(z)=p. Its proper admitted closure is D(p), a good regular
closure contained in R. If z were nonregular, it would be B7. Under emptiness
it is therefore regular, and R union {z} is a good state. Iteration proves the
claim. QED.

This does not refute the possibility of some different global finite critical
family theorem. It refutes the expectation that proving B7 empty should make the
regular-state generation tree reach a finite fixed point. A regular extension is
not a nonregular square hit.

## 2. The exact missing square-hit descent statement

For a good state R with |R|>=3 and n in J(R), consider:

    SqPrim(n) nonempty
    => exists a good R', |R'|<|R|, and n' in J(R')
       with SqPrim(n') nonempty.                         (SQD)

If SQD were proved, minimizing |R| would reduce existence of any B7 member to
|D(q)|=3, since the size-two case is already excluded. Closing Task 1's 48 cases
would then prove B7 empty. SQD is NOT established, and the actual regular
fixtures are not counterexamples to its square-hit hypothesis. It requires the
new-prime transfer that E1 and E7 show cannot be replaced by deleting branches.

## 3. Provider and whole-certificate interface

Phase-D provider confinement bounds active helpers by the actual root basins;
it does not give a bound depending only on the number of nonregular roots.
In exactly seven, basin disjointness is between the seven different roots, not
between branches within one root. All fixed ternary shadows within one basin
contain its final leaf, giving capacity one irrespective of the number of
regular vertices. Seven obligations and seven units of capacity are equality,
not a contradiction.

The source's arbitrary-branching B7 filling theorem already supplies a single
state construction conditional on an actual q. Thus mere branching or extra
3-edges cannot be used as a state-incompatibility assertion. The actual partial
fork mask in this package uses R={7,43,127}, a=152908, K=2,E={1}, residues
33 mod49,1428 mod1849,11159 mod16129. Of the 38227 exponents d=4 mod6 in full
period L=229362, exactly 38226 are covered; the sole hole is d=152908. This is a
regular partial system, with U=42 rather than L. No nonregular root was added
and no complete C=1 certificate was constructed.

## 4. Final verdict

A: no minimal-actual-B7 three-vertex theorem proved.
B: no global finite critical family or uniform depth bound proved.
C: exact finite cardinality recursion, and complete factor-parametrized M=4 gate;
   all 120 fork indices emitted, but serial factor sets not fully materialized.
D: actual regular diamond/shortcut counterexamples to naive local lemmas;
   correct invariant is the closed state, maximal generators, and union cost.

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
