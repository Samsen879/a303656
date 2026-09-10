# Proofs and countermodel — Phase G

## Imported authority and evidence scope

All source labels refer to `SOURCES.md`, pinned to main c6ca0dc061783ab993be6fa077c8f66cd730e28c. We use the precise admitted original-row C=1 class of those sources. A proof below means a mathematical deduction supplied for review, not proof-assistant certification or independent-author review. Finite Python checks certify the described instances only.

The requested strict different-prime SQD is NOT proved. The following results distinguish actual conditional theorems from a finite countermodel in an explicitly weaker formal language.

## G1. Unique in-certificate B7 original origin

**Theorem.** Let C be an actual complete C=1 certificate with exactly seven original nonregular primes. Let Q(C) be those seven primes. Let q be its B7 root and R=D(q)\{q}. Then

\[
\{(r,T): r\in Q(C),\ T\text{ a good B7 state},\ r^2\mid Z_T\}
=\{(q,R)\}.
\]

In particular no different original root of C supplies a B7 square hit at *any* exact state, and there is no cheaper in-certificate replacement.

**Proof.** Order-DAG Theorems7.1–7.2 supply the unique seven-leaf pure-3 normal form with a 7-headed depth-one basin and pairwise-disjoint full admitted descendant basins.[S2] In that basin every proper descendant is regular and every order is squarefree; the corresponding root q belongs to B7. The exact-state iff gives q²|Z_R.[S3,S4]

Suppose r∈Q(C), r²|Z_T for a good B7 state T. The same iff gives r∈B7 and D(r)\{r}=T. Every B7 basin contains7. If r≠q, then 7∈D(r)∩D(q), contrary to disjointness. Hence r=q. Exact order determines the unique descendant closure, so T=R; equivalently the normalized coprimality theorem forbids q from dividing any distinct Z_T.[S4] The reverse inclusion was already proved. QED.

**Sources excluded.** No proper descendant can replace q: all proper descendants of any of the seven origins are regular. A derived macro is not an original prime. In exactly-seven, all original nonregular rows are already the seven rigid origins at the chosen boundary. Center-provider ancestry must end at one of them and does not assert the existence of a new prime.[S5]

**Vacuity warning.** G1 does not exhibit a high-cost actual C. A proposed arithmetic implication whose consequent G1 forbids could be true because its antecedent is empty. Thus G1 is not an actual arithmetic counterexample to that implication.

## G2. Finite non-implication in the structural reduct

Let A_str be axioms A1–A10 in `MODEL.md`. Let Q be its origin sort, c(R)=|R|, and Hit_hat its formal admitted primitive-square relation. Consider

\[
\begin{split}
\mathsf{DPR}_{\rm int}:\quad
&\mathrm{Complete}_{\rm BOTH}\ \wedge\ |Q|=7\ \wedge\mathrm{Hit}_{\hat{}}(q,R)
\ \wedge\ c(R)>2\\
&\Longrightarrow\exists r\in Q\setminus\{q\},\ T:\ c(T)<c(R),\
\mathrm{Hit}_{\hat{}}(r,T).
\end{split}
\]

**Theorem.** A_str does not imply DPR_int. The structure specified in model.json is a finite countermodel.

**Proof.** We verify the hypotheses and failure of the consequent without pretending the formal endpoints are actual primes.

### (i) Actual regular support

Use the seven basins in REPORT.md, each with its own distinct formal origin. Every numerical helper is verified prime by a recursive full-(p−1) Lucas certificate. Exact base-5 order is certified by 5^w=1 modp and failure at w/l for every prime l|w. The nonidentity 5^w modp² certifies s=1. No probable-prime status is substituted.

Their orders have all odd support inside the specified basin, terminate only at3, and satisfy the required depth bounds. For example the B7 diamond has orders6,42,42,5461. The O31 fork has orders3,93,31. The formal endpoint order is the product of the maximal generators, which generates exactly the full regular support. All basins are disjoint as typed original-row sets. This proves A1–A4 and A8.

### (ii) ONE state and canonical covering

Fix a_i by the displayed CRT congruences, one time for each basin. Fix all row residues as in MODEL.md. For any universal exponent d in that basin's assigned parity/leaf, if some private regular digit differs from its center, take the numerically least such p. Every private factor of w_p is a smaller regular label and hence centered. The shared2,3 factors agree with a_i because d belongs to the assigned parity/leaf. Thus w_p|d−a_i, whereas p∤d−a_i, and the actual p-row has valuation1.

If every regular digit is centered, the endpoint's entire declared order divides d−a_i. Here n_i|a_i, so its formal rigid guard is active and covers. This proves full private-fiber coverage using one frozen state; no exponent-specific state is chosen.

The 31-basin is all-odd, so it retains its complete leaf at both parities. On even exponents the seven leaves partition all27 ternary cells. On odd exponents, row3 covers 3∤d and the31-basin covers3|d. Thus A1 is complete everywhere. The two-adic row supplies A0 everywhere. This proves A5 and A10. The formal roots' A0 masks are neither required nor independently chosen.

### (iii) Valid linear receipts and simultaneous charging

The exact descending elimination described in MODEL.md witnesses each dynamic introduction with its omitted center filled by the current original-origin parent. Each recorded provider is an original row of that parent's support and supplies the exact incoming shadow. Reversing these edges gives increasing provider ancestry terminating at the corresponding original origin; support is confined to that basin.

At coordinate3 the seven final clauses have supports in disjoint basins, exact private head providers, and pairwise-disjoint leaves forming a full frontier. Each basin's fixed shadows are nested around its leaf, so its width is1. Therefore the seven obligations charge bijectively to the seven origins. This proves A6 and A7, including actual event-algebra reachability rather than bare Hall feasibility. It does not turn an endpoint atom into an arithmetic row.

### (iv) Exact state/coprimality guard

The B7 regular state R={7,43,127,6717031} has maximal antichain {6717031}. Every n∈J(R) contains that generator, and n=6717031 belongs to J(R). The sole formal B7 square mark is at this exact index/state. Primitive order localization assigns each represented regular prime factor and each formal prime atom to at most one stratum. All distinct-state incidences are disjoint. Actual regular factors have valuation1, not2. This proves A9, and c(R)=4>2.

The registry is closed under all good substates within its specified eight labels. There are cheaper states, including {7,43} of cost2, but they have no formal square-hit mark. None of the other six origin basins contains7, so no other origin is a B7 atom at any exact state; this is independent of the registry bound. Thus the consequent of DPR_int is false. QED.

### Scope of this proof

This is a genuine finite countermodel to the explicitly displayed structural implication, not an arithmetic counterexample. The decisive omitted realization axiom is `there exists an actual prime Q_i with exact order n_i and 5^n_i=1 modQ_i²`, for each of the seven endpoint atoms. A_str contains the *consequences* of such an endpoint on its event kernel, not its arithmetic existence.

Even a successful formal proof of DPR_int in a stronger arithmetic theory could therefore rely on disproving the modeled high-cost arithmetic antecedent. Our countermodel does not rule that out.

## G2.1. Deletion minimality does not imply a small B7 state

**Finite proposition.** In the preceding fixed-state model every one of its21 non-special core original rows is indispensable for complete coverage at the selected boundary. In particular no regular helper is redundant, despite c(R)=4.

**Proof.** `finite_model_data.json` gives for each deleted row a separator z and a simultaneous private exponent vector, with an integer CRT representative modulo the original L. The verifier evaluates all remaining abstract endpoint guards, all actual regular row kernels, all actual remaining regular values modulo p², and row3. All are safe at anchor1. The two-adic row is also safe there. The period is retained unchanged; no quotient is shrunk by deleting a row.

These are 21 explicit finite witnesses, each checked rather than inferred from a coverage count. They prove the proposition for this fixed finite model. QED.

This is not an arithmetic globally minimum certificate, nor a lower bound on the cost of all possible replacement certificates. Generator indispensability follows already from exact closure; it does not supply a different prime.

## G3. Conditional transplantation of an independently supplied actual B7 root

**Theorem.** Suppose an actual exactly-seven complete C=1 certificate exists. Fix its six arithmetic basins other than the7-headed basin. Let t be any independently supplied actual B7 root, with actual proper regular state T. Then those same six basins together with D(t) admit a complete exactly-seven C=1 certificate with one newly constructed global residue vector and legal K=2,E={1} for the odd rows.

No assertion is made that this operation preserves the original frozen residues or arbitrarily preassigned K,E.

**Proof.** Every vertex v∈D(t) reaches7: for proper descendants this follows from the good-state definition and strict descent; t reaches its nonempty proper support and hence7. Each of the six fixed basins excludes7 by the old certificate's disjointness with its7-headed basin.

If v belonged to D(t) and one fixed basin D(q_i), that basin's full admitted closure would contain the path v→…→7. It would then contain7, a contradiction. Thus D(t) is disjoint from all six, including their original roots. The six roots and t remain distinct.

The new7-headed basin satisfies all depth-one arithmetic conditions: proper descendants regular, terminal3, unique gateway7, all orders squarefree. The other six basins retain their original normal-form conditions, and their31-basin retains O31. Seven-Basin E5 applies to this prescribed actual arithmetic input, giving one canonical complete state with K=2,E={1}, r3=2 mod9 and r2=1 mod4.[S6] It proves BOTH, not only the odd pooled cover. QED.

**Interpretation.** Reconstructing a single global state is permitted here because the conclusion is a new complete certificate, not a statement about the old frozen state. There is no fresh state *per exponent or per occurrence*. The theorem does not produce t and does not turn a formal marked atom into a prime.

## G4. What an honest minimum-certificate argument proves

**Corollary.** Assume the actual exactly-seven certificate class is nonempty, and allow the legal global state to be reselected as in G3. Minimize the total number of original regular helper rows (over complete certificates; arbitrary unused regular extras may be counted too). A minimizer exists because this count is a nonempty subset of the nonnegative integers. The B7 root of any minimizer has minimum basin cost among all actual B7 roots.

**Proof.** Let C minimize that count and have B7 proper state R. If an independently supplied actual B7 root t had |T|<|R|, G3 would construct a complete certificate using T and the old other six basins, with only the standard extra rows2 and3. Those basin sets are disjoint, so the regular-core count falls by exactly |R|−|T|. If C had further unused regular rows, omitting them in the new canonical certificate only decreases the count more. The number of nonregular origins remains seven. This contradicts minimality. QED.

A lexicographic refinement by total vertices and numerical labels can be well-founded, but is unnecessary: the first coordinate already strictly decreases for the legitimate operation G3.

**This does not prove the requested normal-form improvement.** It yields `certificate-minimum B7 cost = actual B7 minimum cost`, not `minimum cost=2`. A minimal hit state has no cheaper actual hit by definition. Establishing that its cost is2 still needs a square-hit existence/descent theorem. Nor does G4 preserve an arbitrarily frozen old global state.

## Route conclusion

The proposed in-certificate source of q' is absent by G1, and the finite model shows that all listed structural-state mechanisms can hold with a high-cost marked B7 origin and no replacement. Stop that structural route. An external actual-root existence theorem remains an arithmetic question; if such a root is established, G3 supplies the class-preserving global-state interface.
