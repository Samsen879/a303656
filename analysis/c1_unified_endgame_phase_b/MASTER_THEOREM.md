# Master theorem: a first nonlinear descended-resource core

## 0. Scope, terminology and outcome

This document proves a necessary-core reduction, and a universal sparse-resource
no-go, in the **finite admitted original-row C=1 formal class** at the pinned
repository snapshot in `SOURCES.md`. It does not prove that the exceptional core
class is empty. It does not prove universal representability in A303656.

**Main conclusions.**

1. Every hypothetical complete simultaneous certificate admits a canonical,
   completeness-preserving, strictly descending sequence of **linear provenance
   contractions**, ending at an essential nonlinear core as defined below.
2. Before that first nonlinear step, every geometric rigid cylinder has a unique
   original rigid-prime origin. No original rigid origin has been duplicated.
3. At the critical coordinate p, an irredundant non-simple witness uses r >= p
   such origins, with r = 1 modulo p-1. Thus p is bounded by the number of
   original rigid seeds, not by the largest prime in the input.
4. In fact, **a complete certificate requires at least seven distinct original
   nonregular primes**. Neither their sizes nor the precisions are bounded.

“Canonical” means relative to the fixed numerical ordering of coordinates,
original row IDs and finite CRT representatives. It does not mean invariant
under arbitrary relabelling. “Minimal” means inclusion-minimal, not globally
minimum cardinality. These are mathematical proofs; finite tests in this bundle
support specified identities, but are not their universal justification.

The novel assertions are relative to the mathematical source stack read for this
study. No literature-priority claim or proof-assistant verification is made.

## 1. Formal class and imported normal forms

An original odd row has a distinct prime q = 3 modulo 4, precision K_q >= 2,
a residue r_q shared by c=0,1, and a nonempty set E_q of positive odd integers
less than K_q. Its local quantity is

    V_(q,c)(d) = r_q - 3^c - 5^d.

A local zero modulo q^K is unresolved, never accepted. Put

    w_q = ord_q(5),  s_q = v_q(5^w_q - 1),
    a_q = max(0,K_q-s_q),
    U = lcm(t_2,{w_q}),  L = lcm(t_2,{w_q q^a_q}).

A coarse event means that all full lifts of that coarse class are accepted by
that same original row. We use the pinned repository's exact normal form and
reverse-CRT theorem, not a replacement definition of a certificate.

At one fixed anchor an original row is inert, rigid, or dynamic. A rigid event is
one congruence modulo w_q and requires s_q >= 2. A dynamic row q has a lower
logarithm guard modulo w_q and, at its own q-coordinate, a fixed shell union

    D_q = union_(j in J_q) {x : v_q(x-zeta_q)=j},

where every j in J_q has the same parity, since s_q+j must be odd. In particular,
0 in J_q implies 1 not in J_q. The center is always omitted. A prime coordinate
has at most one original dynamic row.

We keep the final ambient U and its coordinate depths fixed when deleting
redundant events. Deleting an event from a subcover does not delete the original
support row or recompute U. Derived cylinders are not new arithmetic primes.

The fundamental order facts are

    w_q | q-1,  v_2(w_q) <= 1,  P^+(w_q) < q.

Consequently all odd-row full-period events depend on the 2-adic exponent only
through its parity.

## 2. A parity-flexible boundary anchor

### Lemma 2.1

For every shared residue r of a sound two-adic row, there is a single anchor
c_* which has a two-adically safe exponent of each parity. One may choose

    c_* = 1, if r = 0 or 1 modulo 4;
    c_* = 0, if r = 2 or 3 modulo 4.

For even r use the target local values {0,4}; for odd r use {1,5}.

### Proof

All four target values are sums of two squares. For the chosen c_*, both values
of r-3^c_*-T are 1 modulo 4. They differ by 4. For K>=3, the subgroup generated
by 5 modulo 2^K is exactly the units 1 modulo 4, and its exponent parity is
specified by whether the unit is 1 or 5 modulo 8. Thus the two targets supply
both parities. For K=2, the target residues coincide modulo 4 and every exponent
has the same 5-power residue, so either parity can be used. A sound local test
cannot reject a genuine sum-of-two-squares residue. QED.

With no two-adic row take c_*=0. The choice does not assert common safety of
both anchors; for odd r that stronger assertion is false.

### Corollary 2.2

If the original system is complete at both anchors, its odd-row subsystem at
c_* is complete separately over each parity of the exponent.

Indeed, any odd-safe full exponent of a specified parity can be combined by
CRT with the safe two-adic exponent of that same parity. Higher two-adic bits
change no odd-row predicate, because v_2(w_q q^a_q)<=1. This would escape the
complete certificate at c_*. Equivalently, any odd-safe coarse point of that
parity gives such an exponent by reverse CRT.

If 2 does not divide U, the two parities are merely duplicate auxiliary labels
for this argument; no fictitious two-adic hazard is introduced.

### Choice of a distinguished parity b

The original row 3 has order w_3=2 and s_3=1. At the fixed anchor it is active
on at most one exponent parity. Select the other parity b. If it is absent or
inert, select b=0. By Corollary 2.2 a hypothetical complete certificate still
has a complete odd-row system at (c_*,b), **but its dynamic 3-row is inactive**.

All remaining sections until the paired-state discussion concern that fixed
anchor and parity. This is a logical reduction of the two-anchor problem,
not a claim that the two provenance trees synchronize.

## 3. The sparse local cover lemma

Let X=Z/p^beta Z, p odd. Let D be one admitted parity-shell bundle, possibly
empty, and let C_1,...,C_r be proper p-adic cylinders. They can be descended
geometric cylinders in this lemma; arithmetic primality is not needed.

### Lemma 3.1

If r<p, then

    D union C_1 union ... union C_r = X

holds if and only if 0 is an accepted shell index and one of the cylinders is
exactly the first-level centered cylinder C_1(zeta).

### Proof

If D is empty, or 0 is not accepted, D covers no point in any noncenter first
branch. Each of the p-1 noncenter branches needs a rigid cylinder. The center
point needs another one. Proper cylinders cannot span two first branches,
so at least p are necessary.

Suppose 0 is accepted. D covers the complement of the center first branch.
If the centered first-level cylinder is present, it completes the cover.
Otherwise, every cylinder meeting that branch is contained in one of its
second-level children. Since 1 is not accepted, each of the p-1 noncenter
second-level children requires a cylinder, and the center child requires one
to cover the center point. This again needs p cylinders. If beta=1 there are
no deeper proper cylinders and the conclusion is immediate. QED.

Call D plus a centered depth-one cylinder a **simple pair**. A full local
cover with no active simple pair therefore needs at least p rigid cylinders.

The centered prefix-frontier inverse theorem gives an additional fact: in an
irredundant full cover, the number r of rigid leaves satisfies

    r = 1 modulo p-1.

With no essential dynamic event this is the ordinary complete prefix-tree
identity. With a dynamic event there is one centered cylinder and a full
frontier in each unaccepted side branch; each such frontier has leaf count
1 modulo p-1, and side branches occur in groups of p-1.

## 4. Linear single-origin provenance

Start with one seed for every nonempty original rigid event at (c_*,b). A seed
contains its original prime identity q, its exact CRT guard, and an initially
empty helper lineage. Let N be the number of these seeds, after optional
canonical deletion of redundant original events at the fixed ambient U.
Every seed origin has s_q>=2, so N is at most the total number of nonregular
original primes in the system.

At the highest remaining odd coordinate p, a seed factors as a lower guard
G and one proper p-cylinder. The only possible dynamic event there is the
original p-row, with lower guard H_p and fixed bundle D_p.

A **linear contraction** replaces a top seed by one child precisely when:

- 0 belongs to the actual J_p;
- the seed's p-cylinder is C_1(zeta_p);
- G intersect H_p is nonempty.

The child has guard G intersect H_p, with the p-coordinate removed, the same
origin q, and helper p appended to its lineage. Top seeds not satisfying this
rule contribute no linear child. Lower events are retained. The original
dynamic p-event is removed with that coordinate.

Each seed has at most one child. Different seeds keep different origins, even
when their geometric guards coincide. Helpers may be shared between lineages;
this repeats the same frozen row state, not a new residue choice.

By the exact cover-clause formula, the linear residual is a **subset** of the
full exact saturation residual. It need not equal that residual. We only
continue linearly when this sub-residual is itself complete over the remaining
domain. Thus we never equate an incomplete contraction with the full one.

Optional canonical pruning keeps an inclusion-minimal subcover after a
successful step. It mutes redundant events without changing U or inventing
new row states. Helper provenance is retained even if that original event is
no longer a free-standing current event.

### Lemma 4.1: no terminal seed on the distinguished parity

A nonempty seed cannot descend linearly all the way to a constant at parity b.

### Proof

If it has no helper, its original rigid order would have no odd factor.
The only possibilities w_q=1,2 give no admitted nonregular rigid resource:
q with order 1 divides 4, and the admitted prime with order 2 is 3, with s_3=1.

Otherwise take the numerically least helper h in its lineage. Every odd factor
of w_h is smaller than h. To disappear from the final guard it must also have
been eliminated by a helper. Minimality of h forbids this. Hence w_h=1 or 2,
forcing h=3. But the dynamic 3-row is inactive at b, so a nonempty linear
contraction through it is impossible. Guard intersections can add congruences
or become empty; they cannot erase an uneliminated prime factor. QED.

## 5. Canonical essential-core theorem

Fix deterministic deletion and representative orders. At each highest odd
coordinate p, form the linear-only residual described above.

If it is complete, prune canonically and continue at lower rank. If it is not
complete, choose the first lower point y escaping that residual. The parent
state was complete, so its actual active rank-p slices at y cover X_p. Neither
a lower event nor a simple pair is active at y, or y would have belonged to
the linear residual. Delete redundant active top slices in the fixed order
and retain the resulting irredundant full witness.

### Theorem 5.1

Every hypothetical complete admitted simultaneous system reaches such a
nonlinear step. Its witness has r distinct rigid-seed origins satisfying

    p <= r <= N,     r = 1 modulo p-1.

Each witness cylinder is a linearly descended cylinder with a single original
nonregular-prime origin and a compatible chain of actual dynamic helpers.
The lower point y is not covered by lower events or by any linear pair clause.
At p=3 the witness is rigid-only. At p=5 it is also rigid-only.

### Proof

Every successful linear step strictly decreases the number of uneliminated
odd coordinates, and never increases the number of seeds. If all steps were
successful, completeness would hold on the final singleton parity domain.
Lemma 4.1 says it has no nonempty seed, and no odd dynamic event remains,
which is impossible. Therefore a failing linear step occurs. The construction
at that step gives the stated full witness. Lemma 3.1 and the inverse frontier
classification give r>=p and r=1 modulo p-1. Single-origin injectivity gives
r<=N. The 3-row is inactive by construction and no admitted dynamic 5-row
exists. QED.

This is an essential first nonlinear step, not an arbitrary nonlinear cover
that might be redundant in a complete system. The preceding global pruning
and local witness deletion are inclusion-minimal operations. The algorithm
is finite and exact, but no polynomial-time complexity bound is claimed.

### A blocker component of the same necessary class

For the fixed-anchor original rigid seeds, make a bipartite graph to free odd
coordinates lambda dividing w_q, with lambda not in the original row-prime
set P. Give lambda capacity lambda-1. A full capacitated matching would assign
each seed one free blocker with at most lambda-1 forbidden first digits. The
one-anchor version of #14 would then construct an odd escape of parity b.
Consequently some seed subset Q' obeys the Hall deficiency

    |Q'| > sum_(lambda in neighbors(Q')) (lambda-1).

One may select the first such Q' canonically. This is a worst-case digit-count
necessary condition, not an exact optimization of overlapping forbidden
positions. The Hall-deficient subset and the local nonlinear witness are not
asserted to have the same origins; claiming that identification would need a
new theorem.

## 6. Helper-head arithmetic at coordinate 3

Here “head” means the numerically least helper in a nonempty linear lineage.
It is an actual original dynamic prime, not a newly created prime resource.

### Lemma 6.1

The union of all linearly descended seeds of rank 3 and depth at most 2 lies
inside at most two fixed depth-one 3-cylinders and two fixed depth-two
3-cylinders. Its measure is therefore at most 8/9.

### Proof

A seed with no helper would be an original rigid prime of rank 3 and depth
1 or 2. Such resources are empty by the squarefree cyclotomic identities
proved in #16.

For any other such seed let h>3 be its least helper. All odd factors of w_h
must be at most 3: a larger factor smaller than h would have to be another
smaller helper, which is impossible. Also, the 3-depth of w_h cannot exceed
the surviving seed's depth, since intersection only increases coordinate
precision. Thus

    w_h = 3^e or 2*3^e, with 1<=e<=2.

The complete factorizations

    Phi_3(5)=31,             Phi_6(5)=3*7,
    Phi_9(5)=19*829,         Phi_18(5)=3*5167

give exactly the admitted helper heads

    e=1: 7,31;       e=2: 19,5167.

The factors 3 have the wrong order; 829 is not 3 modulo 4. Each of the four
actual helpers has one fixed logarithm guard at the selected anchor. All seeds
using a given head are contained in its same fixed 3-cylinder. Counting that
head once gives total union measure at most

    2/3 + 2/9 = 8/9.

The bound permits overlap and allows incompatible heads, so it is an upper
bound, never an unjustified availability assertion. QED.

### Corollary 6.2

A rigid-only full rank-3 fiber of linearly descended seeds requires at least
seven distinct original rigid origins.

If it were full, Lemma 6.1 forces a leaf at depth at least 3 in an irredundant
ternary frontier. A complete p-ary frontier having a leaf at depth D has at
least 1+(p-1)D leaves: along that leaf's ancestral path each level has p-1
other nonempty child subtrees. For p=3,D=3 this gives seven.

This does **not** assert the raw original-resource 81-row tax for macros.
It is a different, helper-aware seven-origin tax before nonlinear branching.

## 7. The coordinate-5 bottleneck with at most six seeds

### Lemma 7.1

A rank-5 linearly descended seed of top depth one whose lower guard has no
3-factor lies in one of at most two fixed first 5-branches, determined by the
original helper rows 11 and 71.

### Proof

There is no unprocessed odd coordinate below 5 other than 3. If there is no
helper, the original rigid row would have w_q=5 or 10. But

    Phi_5(5)=781=11*71,    Phi_10(5)=521,

and 11,71 are regular, while 521 is 1 modulo 4. Thus there is no such raw
rigid resource.

With a helper, take its least member h>5. An odd factor of w_h above 5 would
require a smaller helper; a factor 3 would survive in the lower guard.
Therefore w_h=5^e or 2*5^e. The final top depth is one, so e=1. The same full
factorizations force h=11 or 71. Each helper has just one fixed logarithm
class modulo 5 at the fixed anchor. QED.

### Lemma 7.2

An essential first nonlinear step at p=5 is impossible if N<=6.

### Proof

There is no dynamic 5-row. A full irredundant 5-ary frontier with at most six
leaves has exactly five leaves, all at depth one. This follows either from
leaf count 1 modulo 4 and the depth tax, or directly from the prefix tree.

Let n be the number of current top seeds, k the number of retained lower
seeds. Essential saturation implies n>=5, and n+k<=N<=6. All minimal
rank-5 slice-cover witnesses consist of one depth-one seed in each of the
five first branches. With n<=6, their total number is at most n-4: with five
seeds there is at most one witness; with six, at most one first branch can
have two options, giving at most two witnesses. Deeper top cylinders cannot
participate in a cover with this many seeds.

Now perform the **full exact** #13 contraction at 5, not just the linear
sub-contraction. The number of resulting cover macros plus retained lower
seeds is at most

    (n-4)+k <= N-4 <= 2.

Every nonempty resulting macro has a proper 3-cylinder guard. For otherwise
all five constituent lower guards would be 3-free. Lemma 7.1 places all such
constituents in at most two fixed first 5-branches, so they cannot cover all
five. Nonempty guard intersection cannot turn a proper 3-guard into the whole
3-domain. Retained lower seeds are also proper 3-cylinders: no linear seed can
be constant at this stage without the inactive helper 3 (Lemma 4.1).

After eliminating 5, at most two proper 3-cylinders and no active dynamic
3-event remain. They cannot cover the 3-domain. If there is no 3-coordinate,
these allegedly proper surviving guards are necessarily empty, giving the
same contradiction. Exactness of the full contraction contradicts the parent
state's completeness. QED.

The macros in this one-step counting argument may have several origins; they
are counted as geometric residual clauses, not as new original primes. No
arithmetic raw-resource theorem is applied to them.

## 8. Universal seven-nonregular-prime necessary bound

### Theorem 8.1

Every complete finite admitted simultaneous C=1 certificate has at least
seven distinct original primes q satisfying s_q>=2. More precisely, the
boundary-selected anchor's canonically retained original rigid subcover has
at least seven such origins.

### Proof

Assume N<=6. Apply Theorem 5.1 to the distinguished parity where dynamic 3 is
inactive. The critical p is an odd prime at most N, so p is 3 or 5.
Corollary 6.2 excludes p=3. Lemma 7.2 excludes p=5. This contradiction proves
N>=7. Since initial rigid origins inject into the original nonregular primes,
the latter number is at least seven as well. QED.

This is not a prime-panel statement. Precisions, accepted sets, regular-row
counts, prime sizes, and the number of higher support coordinates are
unrestricted within the finite admitted class.

## 9. Explicit exceptional class E_L

A member is a **local descended-resource obstruction record**, not a renamed
complete certificate. It consists of:

- a frozen admissible original arithmetic ledger (P,K,r,E,U), selected anchor
  c_* and parity b as in Section 2, and a declared initial rigid-seed budget
  N>=7;
- compatible single-origin seed lineages, using only the actual linear rule
  in Section 4, with no duplication of an original seed origin before the
  recorded rank p;
- an exact lower point y and an inclusion-minimal full centered-frontier
  witness at p, with r>=p distinct rigid origins and r=1 modulo p-1;
- absence at y of all retained lower coverage and of every active simple-pair
  clause, and the inactive dynamic 3 boundary;
- surviving original blocker options and a free-coordinate Hall deficiency
  on the declared initial seed pool, not asserted to be the same origin set
  as the local frontier;
- the original paired row states and retained support moduli, unchanged.

Membership in this necessary exceptional class does **not** require that the
input ledger already be globally complete, or a converse reconstruction of a
complete certificate. Its positive covering test is the one recorded local
fiber. Legal lineage transitions and local absence conditions are checked from
exact guards. The declared N is an initial resource budget: the local frontier
itself need not have seven leaves when p=5 and additional lower resources are
present elsewhere.

For records extracted from a hypothetical complete system, Theorem 5.1
additionally supplies a deterministic completeness-preserving history and
inclusion-minimal subcover receipts at fixed U. Those are proof provenance for
the extraction, not a hidden global-completeness assumption in the definition
of E_L. Every local witness is inclusion-minimal; no globally minimum input
size or isomorphism-canonical form is claimed.

Theorems 2--8 prove

    complete simultaneous admitted certificate  =>  a member of E_L.

The implication is necessary, not sufficient. A bare geometric frontier, or
an independently chosen list of helper guards, is not a member with a certified
actual original arithmetic ledger. The abstract seven-leaf frontier in the
results is not an arithmetic realization or a complete certificate.

## 10. What remains unproved

The linear history terminates at E_L; a general nonlinear continuation with
an arithmetic decreasing potential is not proved. After nonlinear branching,
several lower clauses can cite the same original origin in compatible but
different witnesses. Raw prime counts, raw Kraft mass and sums of macro masses
are no longer interchangeable.

To close the proposed endgame, one needs an arithmetic demand-capacity theorem
for **state-compatible descended-resource frontiers and their lower-demand
alternatives**, not another application of the raw original-prime Kraft
inequality to macros. This is the remaining closure gap identified here.

The exact finite alive-anchor game and configuration formulation in
`DEFINITIONS.md` remain valid across pooled branches, but their finite
termination is not an arithmetic impossibility theorem. Thus Gate C is not
claimed. No genuine actual complete counterexample is constructed, so Gate D
is not claimed. Gate A, universal finite-certificate no-go, is not claimed.
