# Formal model specification — structural reduct, not integer arithmetic

## 1. Purpose and logic boundary

This document defines the exact finite structure checked by `verify.py`. Its purpose is to falsify the assertion that the listed order/provenance/resource/global-state constraints alone force a different original B7 root at a cheaper exact state.

The structure is **not** a model of the full arithmetic definition `w_Q=ord_Q(5)`, `s_Q=v_Q(5^w_Q-1)` for its seven endpoints. It is not a model of all integer arithmetic, and not a proof of formal independence from the repository's entire mathematical theory. It is a finite *reduct*: retain the stated combinatorial consequences and exact event kernels, but leave endpoint arithmetic realization as an explicit unsatisfied proof obligation.

The formal endpoint atoms are allowed only as witnesses inside this adversarial reduct. None is offered as an actual replacement prime.

## 2. Sorts

1. `RegularLabel`: the finite actual integer primes with certificates in `arithmetic_certificates.json`. Each has a verified exact base-5 order, full factorization of that order, and valuation s=1. Fourteen are in the core. Other certified labels support the finite B7 registry and the Z_{7} product; they are not extra ledger rows.
2. `Origin`: seven distinct formal row IDs Q_i, each of kind `FORMAL_ORIGINAL_NONREGULAR_ORIGIN`. These have no integer value. They have a declared order label n_i, a nonregular color s≥2, a single fixed symbolic residue expression, and a formal rigid-event kernel.
3. `OriginalRow`: disjoint union of the core RegularLabels and Origins. The actual special rows 3 and 2 are kept separately.
4. `Macro`: a derived cover-clause receipt with a set of OriginalRow supports, a fixed guard, and parent receipts. There is no coercion from Macro to Origin or prime.
5. `B7State`: all nonempty good closed subsets of the specified eight-label registry. Membership is closure-complete, not an arbitrary selected path.
6. `Exponent`: one common finite domain X = Z/54Z × product_{core p} Z/pZ. CRT identifies it with Z/LZ. No origin own digit is needed at K=2,s≥2; its formal event is independent of that digit.

The formal endpoint's requirement `Q>max(n_i,2e9,all helpers)` is recorded as a future realization constraint. For the structural DAG one places every endpoint above its own regular descendants. No fabricated integer prime satisfying the requirement is supplied.

## 3. Structural axioms

**A1 (original identities).** Seven distinct formal origins, one per basin. Every non-special row occurs in precisely one basin. All other core rows are actual regular primes. Origin IDs are never derived macros.

**A2 (full order closure).** For every core regular p, all odd prime divisors >3 of the *actual* w_p lie in its basin. The formal root's order is the product of the basin's maximal generators. Its full proper admitted closure is exactly R_i. Edges on actual labels strictly decrease. No 1-mod-4 free terminal occurs; 3 is the only terminal.

**A3 (normal-form depths).** The seven leaf depths are 1,1,2,2,3,3,3. In a depth-e basin, v3(w_x)≤e, v2(w_x)≤1, and vp(w_x)≤1 for p>3. This is an order restriction, not a claim that x−1 is squarefree. The specified heads are 31,7,19,5167,271,4159,31051.

**A4 (disjoint basins).** R_i plus its formal origin is disjoint from every other such basin. Terminal 3 and the common exponent separator are shared, not private resources.

**A5 (one state).** Fix K=2,E={1} for all odd rows, a single a_i per basin, actual r_p=(3+5^{a_i}) modp², and a single symbolic endpoint expression r_Q=Q+4 modQ². Fix r3=2 mod9 and r2=1 mod4. These choices do not depend on the universal exponent or on an OR branch.

**A6 (reachable provider receipts).** Each elimination of a private p-coordinate uses its centered depth-one incoming cylinder and the original regular p dynamic complement. An exact original provider already in the rigid parent's support has the necessary p-shadow. The omitted center is covered by that parent. Provenance records the operation, supports and fixed guards. Reversing these witnesses gives an increasing original-row ancestry path ending at its basin's original rigid origin.

**A7 (support and capacity).** Every macro support lies in its original origins' active basins. The seven final head shadows are a pairwise-disjoint minimal ternary frontier. Within each basin all fixed proper 3-shadows contain its final leaf, so the frozen-shadow width is 1. The seven simultaneous charges use seven distinct origins. No charges from different coordinates, OR alternatives or time levels are added.

**A8 (O31).** Every order in the 31-basin, including the formal origin order, is odd. Other basins may be parity-defective. This is a full-basin condition, not just an odd order at head31.

**A9 (exact B7 state and primitive incidence).** For every good registry state R, compute

    A(R)=R\union_{p in R} H(p),
    J(R)={delta*product(S):delta in {1,2,3,6}, A(R) subset S subset R}.

Different states have disjoint J. A represented primitive atom is assigned to the unique state containing its exact order in J. Actual regular atoms have valuation 1. The sole formal B7 square mark is

    Hit_hat(Q_B7, {7,43,127,6717031}), order 6717031, valuation mark 2.

No other represented origin has a B7 mark. The finite incidence relation explicitly respects the stronger no-common-prime-atom guard across distinct strata, not merely a prohibition on duplicated square marks. The actual normalization of Z_{7} is checked by its complete prime product. No numerical factorization of the other Z_R is claimed.

**A10 (complete typed demand).** For every x in the one shared exponent domain, A1 is fatal in the core odd subsystem plus row3, and A0 is rejected by the actual two-adic row. Therefore the model meets BOTH. A0 behavior of unknown endpoints is not independently reassigned; it is unneeded by this lower-envelope sufficient witness.

## 4. Exact event kernels

Write H_p(d) for `d=a_i mod w_p` at an actual regular p in basin i. Since s_p=1,

    fatal_p(d) iff H_p(d) and d != a_i mod p.

Proof: outside H_p the local value is nonzero modp. Inside H_p, LTE with p∤w_p gives valuation `1+v_p((d-a_i)/w_p)`, equivalently `1+v_p(d-a_i)` for the first own digit. At K=2 the center is local-zero sentinel 2 and is not accepted. Off-center valuation is exactly 1. All a_i are 0 mod each private p.

For a formal endpoint Q with order label n,

    fatal_Q_hat(d) iff d=0 mod n.

This is a defining axiom of the reduct, not an executable test modulo Q². If an actual prime Q with exact order n and s_Q≥2 existed, the *single* residue Q+4 would give this event at anchor1: its local value is Q+1−5^d, congruent to Q modQ² on that order class, and nonzero modQ outside it. This conditional calculation does not establish Q's existence.

The actual row3 event is `d odd and d !=0 mod3`, directly checked modulo9. The actual two-adic row rejects anchor0 because 1−1−5^d=3 mod4. At anchor1 its local class is1 mod4 and supplies no rejection.

For unknown endpoints, the anchor0 expression remains Q+3−5^d modQ². No assertion is made that it has an arbitrarily chosen mask.

## 5. Why the private-digit compression is exact

Every >3 lower guard in this model tests a first digit equal to 0, and every actual dynamic event tests its own digit different from0. Thus the truth of every event is invariant within the two classes `{0}` and `Z/pZ\{0}`. The full finite domain projects surjectively to

    Z/54Z × {center,noncenter}^{14}.

The verifier enumerates every binary class for each basin and every separator z. It checks representative regular-row values by genuine modular exponentiation, but the extension from representative1 to all nonzero digits follows from the exact kernel proof, not empirical extrapolation.

For fixed z the basins use disjoint private factors. Let V_i(z) be the set of possible A1 bits over its entire private block. The set of global possible A1 bits is exactly the iterated OR-product of these V_i and the row3 bit. Every combination is realizable by CRT; nothing is chosen separately for the same row. The verifier obtains `{1}` on all54 separator cells.

Full masks encode A0=1,A1=2,BOTH=3. Because the actual two-adic row supplies A0, the final possible mask set is `{3}` everywhere.

## 6. Provenance is not just reachability

Starting from a basin's formal rigid root, eliminate regular labels in descending order. The current guard contains a depth-one center at each next p. The p-dynamic event covers the noncenter under its fixed lower log. Intersecting the current parent with that log and deleting the eliminated coordinate gives the exact linear child.

At every step the verifier selects an original row in the current support whose p-primary logarithm guard is the incoming center; it records that row ID. Dynamic introduction and omitted-center coverage are therefore witnessed, not inferred from two tokens occurring in a common set. The chosen provider is either the original root or a larger regular row introduced earlier. Iterating the recorded choices terminates at the original root.

Each final basin macro has its actual head as an exact 3-provider. The seven final supports are disjoint and the head shadows form the seven-leaf partition. This is one actual witness in the *abstract event algebra*, not a union of unrelated histories. No statement of actual endpoint arithmetic reachability follows.

## 7. What is deliberately outside the model

To obtain an arithmetic certificate one would still need, simultaneously for seven distinct actual primes Q_i:

    Q_i=3 mod4,
    ord_{Q_i}(5)=n_i,
    5^{n_i}=1 mod Q_i²,
    Q_i greater than all required labels (and the inherited inventory bound).

These constraints are recorded but NOT solved, NOT assumed verified by a primality oracle, and NOT counted in the machine PASS. A formal origin cannot be multiplied numerically or silently inserted into a numeric CRT modulus. The finite state symbols Z_R and Hit_hat are not reinterpreted as evaluations of actual cyclotomic integers.

The model also makes no claim about square hits of unlisted actual primes or states whose labels are outside the registry. Such primes are not original roots of this finite certificate reduct. The in-certificate no-replacement proof does not need any bound on that outside universe.

Consequently the exact conclusion is non-implication from A1–A10. It is not non-implication from full number theory plus endpoint realization.
