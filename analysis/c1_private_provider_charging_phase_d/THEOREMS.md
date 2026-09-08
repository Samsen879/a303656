# Center-provider ancestry and frozen-shadow charging — Phase D

## Scope and source convention

All source identifiers [S1]–[S8] refer to the pinned repository files in `SOURCE_BINDING.json`. The new statements below are mathematical deductions in this report, not already-promoted repository theorems. They have not been independently refereed or proof-assistant formalized. The executable checks support finite instances, not the universal quantifiers of the proofs.

Fix the repository's boundary-selected anchor c*, an exponent parity b with the original dynamic 3-row inactive, the original finite ledger, every original state, and the final induced ambient U. Use canonical positive cover clauses, with no artificial lower-cylinder refinement. An original row is inert, rigid, or dynamic at this anchor/parity; this classification is not the same as regular/nonregular. A nonregular row can be dynamic, and must not be mistaken for a rigid endpoint.

For every nonempty original row v, H_v denotes its fixed logarithm guard modulo w_v=ord_v(5). Write Q_(v,p) for its p-primary projection, using the whole p-coordinate if p does not divide w_v. Original dynamic rows have a proper own-coordinate shell bundle that omits the center. A cylindrical macro M has full original support S(M), original rigid support R(M), and an actual finite parent-witness DAG. A macro is never an original row.

We import [S1] T1–T3: the canonical guard is the intersection of original logarithm guards after stripping eliminated coordinates; each proper rigid parent in a nonempty inclusion-minimal slice-cover witness has a private original exact-shadow provider; shared original tokens satisfy the prefix-LCA restriction. In particular, proper rigid slices in one minimal witness are pairwise disjoint. We also import the exact cover-clause semantics [S2,S3].

## D1. Center-provider ancestry theorem

**Theorem.** Let M be a nonempty reachable canonical cylindrical macro. Every original dynamic token h in S(M) admits a certified occurrence-specific path

    h=v_0 < v_1 < ... < v_t=o,
    v_j divides w_(v_(j+1)),

ending at an original rigid row o in R(M). Every path token belongs to S(M). Consequently o is an original nonregular rigid origin. The assertion applies, in particular, when h is a private regular exact provider at a later coordinate.

**Proof.** Choose an occurrence of h in the finite proof DAG of M. Trace this occurrence backwards to a node W at which the original dynamic h-event was introduced into cylindrical provenance. That node eliminates the own coordinate h and its chosen witness includes the original dynamic h-event.

The dynamic bundle omits its center. If that omitted center is a cylinder rather than a singleton at the retained ambient depth, choose one fixed point in it (for example its least representative). Since W is a full slice-cover witness, some proper cylindrical parent C covers that point. Such a parent is unique: the proper rigid slices of the minimal witness are pairwise disjoint. This does not assert that one parent covers the entire omitted center cylinder. By T1/T2, the h-slice of C is the exact h-shadow of an original token v in S(C). Thus h divides w_v, and w_v divides v-1, giving v>h.

If v is an original rigid atom, stop. Otherwise v is an original dynamic token already introduced in C's earlier provenance, and repeat this construction there. Original inert rows are not fatal-event atoms and cannot be the selected endpoint or intermediate support token. The prime labels strictly increase and all tokens lie in the finite original ledger. The construction must terminate, and can terminate only at an original rigid atom. Each step remains in a parent support contained in S(M), proving the support assertion. Original rigid rows require s_o>=2 by the imported normal form. QED.

A fixed order on row IDs, parent receipts, and eligible exact providers makes the choice deterministic. No uniqueness of the arithmetic origin independent of the witness is asserted. If the current private provider itself is original rigid, its ancestry path has length zero.

**Important limits.** The theorem identifies an actual order-dependency path and a valid proof occurrence. It does not assert that H_h equals a projection of H_o, that o occurs only in M, that this origin has unused capacity, or that two occurrences must receive distinct endpoints. A nonregular dynamic helper must still be traced; nonregularity alone is not a stopping rule.

## D2. Original-support confinement and a relevant-helper bound

For an original rigid origin o, define its **active dynamic basin** B(o) as follows: start with o; from a current vertex v, include an original row h whenever h is dynamic at the fixed anchor/parity and h is an odd prime divisor of w_v; repeat. All vertices after o are actual original dynamic rows. Edges strictly decrease their prime labels. This is a finite subset of the original panel and of the absolute order-DAG closure. Dynamic 3 is inactive in the chosen boundary, so it is not added.

**Theorem.** Every nonempty reachable canonical cylindrical macro satisfies

    S(M) subset union_(o in R(M)) B(o).

**Proof.** An original rigid token in S(M) belongs to R(M) and to its own basin. For a dynamic token apply D1 and reverse its certified path. All intermediate vertices are actual dynamic rows until the endpoint rigid origin, exactly as required by B(o). QED.

Let R_0 be the original rigid seed pool. Then

    M_eff = | union_(o in R_0) B(o) |

bounds the number of original tokens that can participate in nonempty cylindrical provenance. In particular, it is at most the size of the finite union of absolute order closures of these particular root primes. Adding arbitrary regular rows outside those closures does not increase this bound.

**Completeness-preserving muting corollary.** For the whole fixed-boundary odd system, mute fatal events of dynamic rows outside this union, while retaining the original ledger, states, U, and every ambient depth. This preserves whether the whole system is complete, when evaluated by full exact contraction.

Indeed, if the full system is complete, full exact contraction has a nonempty TRUE clause at the terminal fixed-parity domain. Its entire proof support is confined by D2 and hence remains enabled. Conversely, muting events cannot create coverage. This does not assert equality of every intermediate residual predicate, and does not authorize deleting support rows and recomputing U. This argument is about the full fixed-boundary system, not about a bare local E_L record.

Combining confinement with [S1] T4 gives, on any selected parent-to-descendant path,

    sum_(merge nodes v on path)(arity(v)-1) <= M_eff-1.

The right side depends on the actual roots and their order basins, not merely on their number N. It is not a terminal-exclusion inequality.

## D3. Frozen-shadow width and simultaneous charging

Fix a remaining odd coordinate p and its full ambient depth beta_p. For each origin o define a finite family of **distinct proper** p-cylinders

    F_(o,p) = {Q_(v,p): v in B(o), p divides w_v}.

All shadows use one frozen anchor and state vector. Duplicate geometries count once. Including basin vertices whose other guards are incompatible with a particular lower point only enlarges this family and is therefore a safe upper bound. One may delete such vertices only with an explicit compatibility or reachability receipt.

Define

    kappa_(o,p) = maximum number of pairwise disjoint members of F_(o,p),

and set it to zero for an empty family. If D_(o,p) is the greatest depth in a nonempty family, then

    kappa_(o,p) <= min(|F_(o,p)|, p^D_(o,p)) <= |B(o)|.

**Laminar width lemma.** kappa_(o,p) equals the number of inclusion-minimal distinct members of F_(o,p).

**Proof.** Nonempty p-adic cylinders are nested or disjoint. Distinct inclusion-minimal members therefore form a pairwise-disjoint family. Every member contains an inclusion-minimal member of this finite family. A pairwise-disjoint collection of arbitrary members can be mapped to distinct minimal members contained in them. This proves both inequalities and hence equality. QED.

These are the finest members of the listed family, not the shallowest cylinders used to compute union measure. No unlisted refinement may be added to increase the count.

**Simultaneous charging theorem.** Let I be one nonempty inclusion-minimal slice-cover witness at p, at a common lower point y, with its fixed parent receipts. For each proper rigid parent i choose a private original exact provider v_i by [S1] T2 and a D1 endpoint o_i in R(M_i). Then, simultaneously for every origin o,

    |{i: o_i=o}| <= kappa_(o,p).

Also,

    sum_(i:o_i=o) mu_p(A_i) <= mu_p(union F_(o,p)).

**Proof.** Reversing D1 puts v_i in B(o_i). The exact-provider property gives A_i=Q_(v_i,p), a proper member of F_(o_i,p). The slices A_i of distinct rigid parents in this one witness are pairwise disjoint. Thus those charged to o form a disjoint subfamily of F_(o,p), proving both inequalities. QED.

This proof works for every choice of certified endpoints, not just an optimized charging map. The original dynamic parent, if present, is not a proper rigid parent and is not counted on the left. It has a private original token, but treating that as an extra nonregular endpoint would be an additional unproved assertion.

**Quantifiers.** The theorem bounds one same-coordinate, same-lower-point, same-state simultaneous witness. It does not add charges from alternative OR witnesses, different lower fibers, different anchors, or ancestor/descendant time levels. For a specified collection of t witnesses, summing their individual bounds gives the weak bound t*kappa; it does not yield a one-use original resource law.

## D4. Hall and state-labelled hypergraph interfaces

For the rigid parents of one fixed witness I, define Gamma(i) to consist of original rigid endpoints obtainable from an exact private provider of i by a certified center-ancestry path in its actual proof receipts. This definition is stricter than arbitrary macro co-support and stricter than an unlabelled abstract order path. D1 makes Gamma(i) nonempty.

For every J subset I,

    |J| <= sum_(o in union_(i in J) Gamma(i)) kappa_(o,p).

**Proof.** Choose a certified provider and endpoint for every i in J. D3 bounds each resulting endpoint load. Sum the bounds. QED.

Thus the associated bipartite graph has a capacitated matching to kappa_(o,p) slots at each origin. This is a necessary certificate extracted from an existing valid witness; it is not a sufficient condition for arithmetic realizability. A constructive encoding may use triples (parent, exact provider, origin) with a stored ancestry path, a single-provider constraint within the witness, and the origin capacity. Different candidate histories require a state-labelled hypergraph/CSP, not a union of incompatible edge sets.

Do not apply this graph unchanged to BOTH or EITHER demands. [S7] requires anchor-tagged state literals and the correct Boolean demand type. Even single-anchor Hall feasibility loses exact shadow positions, all other CRT factors, dynamic-center witnesses, and original-state compatibility.

## D5. Exactly-seven: unit basin capacity is saturated, not deficient

Assume a hypothetical complete admitted C=1 certificate has exactly seven original nonregular primes. Import [S5] Theorems 7.1–7.2 at the distinguished boundary. Its first essential nonlinear witness is the seven-leaf rank-3 frontier with profile (2,2,3), reached by seven distinct linear origins. The roots have pairwise-disjoint actual regular basins; every proper admitted descendant appears as a helper in its corresponding surviving lineage.

Every nontrivial fixed 3-shadow in one such basin contains that lineage's final 3-cylinder. Consequently all proper 3-shadows of a basin are nested. Each basin has a nonempty proper head shadow. D3 therefore gives

    kappa_(o,3)=1 for each of the seven origins.

A private provider lies in one and only one basin, so the seven parent obligations charge bijectively to the seven roots. The capacitated Hall demand and available capacity are both seven. The seven leaves have total mass

    2/3 + 2/9 + 3/27 = 1.

This produces no positive deficit. More importantly, this first essential nonlinear step is already at the last odd coordinate 3. Its full contraction can produce TRUE on the fixed-parity domain immediately. No next odd-coordinate step is implied, and no eighth parent is forced.

The conditional prime-order-chain construction of [S5] Theorem 12.1 is compatible with this equality case and uses one globally frozen state vector. Its nonregular chain endpoints have not been instantiated. Thus it is not an actual complete certificate, but it prevents us from claiming that the remaining failure is merely an unaccounted future recursive fee.

**Conclusion:** the charging audit does not exclude exactly seven and does not raise the bound to N>=8.

## Scope of the positive result

There is a general center-ancestry theorem, an actual-root-basin confinement theorem, and a bounded-capacity theorem for one fixed-state simultaneous frontier. There is no N-only capacity theorem, no global cut unit-injection theorem, and no contradiction-producing resource exhaustion before TRUE. These distinctions are part of the statements, not optional caveats.
