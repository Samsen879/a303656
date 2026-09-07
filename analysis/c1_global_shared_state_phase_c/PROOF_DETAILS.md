# A303656 C=1 — Global shared-state realizability of typed pooled EITHER recursion

## Targeted Phase C: research report

**Primary outcome:** a single-nonregular classification, including fixed precisions and accepted sets with freely chosen shared residues; an actual arithmetic fractional/integer gap; and an original-fiber multi-use order/resultant criterion.

These are derivations and reference computations of this research session. They have not received an independent author's proof audit, proof-assistant formalization, or repository-native integration. No literature-priority claim is made.

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 71b8d428b32724c37e593bcfd9d5f06a42e72d21
main tree: 5609e47eed0c058c190ef59c61644e2fd4b8fad6
Phase B PRs #17, #20, #18, #19: merged
End-of-research main recheck: unchanged
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The six requested main REPORT.md texts were read completely through pinned connector reads, together with pooled DEFINITIONS.md and THEOREM_AUDIT.md. This is not a claim that every generated catalog, historical implementation, or auxiliary file in those directories was read or replayed. The precise source receipt is SOURCE_BINDING.json. There is no local repository checkout and no repository-native test claim. Every local program in this package is newly written standalone reference code.

The source seven-nonregular theorem applies to **simultaneous BOTH certificates**, not to a whole odd EITHER cover. Gate A below is about the latter. The existing theorem already excludes simultaneous certificates with one or two nonregular rows; that existing exclusion is not presented as a new result here. [S6]

## 2. GLOBAL QUANTIFIER MODEL

Fix an actual finite ledger of distinct primes q=3 mod 4, q!=5. For each q, a legal state contains K_q>=2, a nonempty accepted set E_q of positive odd integers below K_q, and one residue r_q modulo q^K_q shared by c=0,1. Put

\[
V_{q,c}(d)=r_q-3^c-5^d,\quad
w_q=\operatorname{ord}_q(5),\quad
s_q=v_q(5^{w_q}-1),\quad
\ell_q=w_qq^{\max(0,K_q-s_q)}.
\]

A clipped zero has valuation sentinel K_q and is never fatal. The original coarse period is U=lcm(t_2,{w_q}); the full period is L=lcm(t_2,{ell_q}). [S2,S5]

For a finite state-family search, choose one common full period Omega supporting every candidate state, or use the fixed induced coarse U when its definition is common to all candidates. The question is

\[
\boxed{\exists(s_q)_{q\in P}\in\prod_q\mathcal S_q\quad
\forall d\in\Omega:\ D_d(F_0(d;s),F_1(d;s))=1.}
\]

It is not forall d exists s_d. Restrictions of the domain, elimination of coordinates, and reuse of a provenance node all retain the same vector s.

A structured infinite parameter family is not silently turned into one finite ILP. A finite ILP below requires a frozen finite family or a proved finite incidence quotient. The unbounded theorems below are proved symbolically and do not depend on such a quotient.

## 3. SIX-STATE AUDIT

For coverage bits C0,C1 the six demands are

| Type | Truth function |
|---|---|
| FALSE | 0 |
| A0 | C0 |
| A1 | C1 |
| EITHER | C0 OR C1 |
| BOTH | C0 AND C1 |
| TRUE | 1 |

At a fixed global state and lower point, let T(z) be the top coverage word. Exact elimination is

\[
(\mathcal R D)(C)=\bigwedge_zD(C\cup T(z)).
\]

Write S_c=forall z T_c(z) and S_or=forall z(T0(z) OR T1(z)). Then

\[
\mathcal R(\mathrm{EITHER})=C_0\vee C_1\vee S_{or},
\qquad
\mathcal R(\mathrm{BOTH})=(C_0\vee S_0)\wedge(C_1\vee S_1).
\]

For a SPLIT, S_or is true and S0=S1=false. Thus EITHER becomes TRUE, while BOTH stays BOTH. This is exactly the P1 distinction, not a new replacement for P1. P2 cover clauses remain ORs of consistent guard/state conjunctions; P3 colored frontiers retain original row identities. [S5,S7]

The reference check visits 340 nonempty top words of lengths 1..4 and 8160 demand/lower-bit truth cells. Six-state closure and the EITHER/BOTH formulas pass. The actual 67/20771 SPLIT remains admissible; it is not a whole-domain cover. [S3,S5]

## 4. ROW STATE FAMILY

Use the following authoritative record:

```text
(q,K,E,r mod q^K,w,s,
 anchor0 normal form, anchor1 normal form,
 original ranks/depths, full logarithms,
 paired positions, lower guards, local-zero information)
```

The normal forms and positions are **derived from** (q,K,E,r); they are not independently selectable parameters.

For t_c=r-3^c, an anchor is inactive when t_c modulo q is outside <5>. Otherwise it has a unique logarithm b_c modulo w. A valuation h_c<min(s,K) is constant over d=b_c mod w; it is a rigid fatal component exactly when h_c is accepted. When K>s and t_c lies in the lifted subgroup, the anchor instead has a dynamic center modulo w*q^(K-s), with fatal parity shells around that center. A row may be rigid on one anchor and dynamic on the other. [S5]

The identity V_q,0-V_q,1=2 implies that at a fixed lower prefix the same odd row cannot be positively divisible at both anchors. For a regular row s=1, every nonempty component is dynamic and always has a safe center lift.

For q=20771 and 40487, K=2,E={1}, the program enumerates mod-q logarithms and groups all q^2 shared residues by at most two excluded lifts. This is a complete **structured** K=2 state classification, not a literal loop over q^2 residues. It covers respectively 431434441 and 1639197169 states.

## 5. INTEGER CONFIGURATION FORMULATION

For a fixed original ledger and finite legal families, introduce

\[
x_{q,s}\in\{0,1\},\qquad \sum_{s\in\mathcal S_q}x_{q,s}=1.
\]

Let h_{q,s,c}(d) be the actual fatal incidence. An A_c demand gives

\[
\sum_{q,s}h_{q,s,c}(d)x_{q,s}\ge1.
\]

EITHER gives one inequality using the pooled incidence max(h0,h1). BOTH gives the two separate anchor inequalities. TRUE gives none; FALSE makes the instance infeasible. These constraints, imposed for every cell, are an exact finite integer formulation. They do not assign different states to different vertices.

Typed macro clauses can be encoded with witness variables constrained by all original state tokens and all guard literals. Alternatives stay OR; state-token conjunctions from different states of the same q are false. Repeated references to the same q,s are idempotent, not additional prime capacity. Exact event families also retain any additional events of the selected state; selecting a subcover does not suppress them. [S5,S7]

### Theorem C1 — an ACTUAL configuration relaxation gap

Take

\[
P=\{3,7,31,43,1303\},\quad K_q=2,\quad E_q=\{1\}.
\]

Their exact orders are 2,6,3,42,62, all with lifting exponent 1. Hence

\[
U=1302=2\cdot3\cdot7\cdot31,\qquad
L=72949758=1302\cdot43\cdot1303.
\]

The rows 43 and 1303 are real regular support rows: their orders install the required 7 and 31 coordinates. Their own primes do not divide U, so their coarse fatal masks are empty. Freeze their residues at 2. Do not omit them while continuing to call 1302 the coarse U: without them, the {3,7,31} skeleton has U=6 and full L=1302.

Use these actual shared-residue families:

\[
\mathcal S_3=\{2+3k:0\le k<3\},
\]
\[
\mathcal S_7=\{a+7k:a\in\{2,5,6\},0\le k<7\},
\]
\[
\mathcal S_{31}=\{a+31k:a\in\{2,6,26\},0\le k<31\}.
\]

Give all states within each family equal fractional weight. At **every** coarse exponent, the expected pooled incidences are

\[
\frac23,\qquad\frac6{21}=\frac27,\qquad\frac{30}{93}=\frac{10}{31},
\]

and therefore their sum is

\[
\boxed{\frac{830}{651}>1.}
\]

These are one set of global fractional distributions, not cell-dependent optimizations. For q=7 the three mod-7 residues partition its six logarithm guards into pairs; for q=31 the three mod-31 residues supply its three anchor-0 logarithms. Within an active mod-q class, exactly one of the q lifts is a local zero and the others have valuation 1. This proves the uniform fractions directly.

Nevertheless, no integral choice is a pooled cover. All five rows are regular, so ascending coordinate selection always chooses a safe dynamic center when necessary. More specifically, the first three coarse rows leave at least one escape in each parity. Exact enumeration of all 5859 choices gives:

| Common coarse escapes | State vectors |
|---:|---:|
| 2 | 217 |
| 14 | 434 |
| 38 | 868 |
| 62 | 434 |
| 218 | 868 |
| 224 | 868 |
| 248 | 868 |
| 434 | 1302 |

The best coverage is 1300/1302. The all-r=2 vector leaves {0,651}. For every one of the 5859 vectors, a full escape is also constructed by CRT from its first coarse escape a:

\[
d\equiv a\pmod{1302},\qquad d\equiv0\pmod{43\cdot1303}.
\]

Direct modular evaluation confirms safety at both anchors for all five actual rows. The 72,949,758-cell full period is **not** enumerated.

Consequently, every nonnegative weighted row-configuration Hall inequality for this EITHER problem can hold while integral feasibility fails. Indeed fractional coverage implies, for every f>=0,

\[
\sum_df(d)\le\sum_q\sum_s x_{q,s}\sum_df(d)H_{q,s}(d)
\le\sum_q\max_s\sum_df(d)H_{q,s}(d).
\]

This upgrades the source's abstract regression to an actual arithmetic example. It does not assert that every strengthened LP or extended formulation is inadequate.

### Actual non-TU minor

The q=3 columns r=2,5,8 on cells d=0,2,4 give

\[
\begin{pmatrix}0&1&1\\1&1&0\\1&0&1\end{pmatrix},\qquad\det=-2.
\]

Thus the natural original row-state incidence matrix is not totally unimodular. Adding the one-state-per-row constraints cannot remove this existing non-TU minor. A special restricted subclass could still have a better integral formulation; no universal impossibility of all network formulations is claimed.

## 6. CROSS-FIBER COLLISION THEOREM / COUNTEREXAMPLE

### Theorem C2 — original rigid multi-use compatibility

Fix an actual rigid row q with w=u*h, h=p^e and p=P+(w). Once its global state is fixed, it has at most one rigid logarithm b_c per anchor.

If that same anchor is required to supply original leaves at multiple fibers, their assembled exponent conditions must all describe the same b_c modulo w. Their requested rigid valuations must also agree: on a single logarithm guard every accepted h<s is constant. Different exact positions at that anchor cannot be repaired by choosing a new state at another fiber.

In particular, if both anchors of this q must be rigid-active at lower representatives Y1,...,Ym, then

\[
\boxed{Y_i\equiv b_0\equiv b_1\pmod u\quad\text{for every }i.}
\]

Hence u divides every Y_i-Y_1. When this holds, repeated use in different ambient fibers is legal and consumes no new prime.

For prescribed b0,b1 and rigid odd valuations h0,h1<s, the remaining common-residue test is exactly the source condition: the minimum of

\[
v_q(5^{b_0}-5^{b_1}-2),\ h_0,\ h_1
\]

must occur at least twice (with appropriate finite clipping). [S2] This condition is not two independently chosen anchor states.

### Actual incompatible lower fibers

For q=20771, w=10385, original h=67, u=155, K=2,E={1}:

| Lower Y | b0 | b1 | Shared r modulo q^2 | Top positions |
|---:|---:|---:|---:|---|
| 7 | 2177 | 9772 | 16 | (33,57) |
| 8 | 1558 | 10238 | 17555 | (17,54) |

Each row of this table is an individually legal paired rigid state; both valuations are exactly 1. There is no single state supplying paired rigid leaves in both lower classes, because 7!=8 modulo 155.

The complete same-lower catalog has 28 nonempty classes and 33 edges. Any two distinct nonempty classes are incompatible for simultaneous paired use of this one q: 378 class pairs. The q=40487 catalog has 62 nonempty lower classes and 652 edges, giving 1891 such incompatible class pairs.

This is an actual forall-fiber/exists-state versus exists-state/forall-fiber separation. It is **not** a theorem that an arbitrary complete cover must allocate both named fibers to this same prime.

### Actual compatible reuse

For the same q=20771, the one state r=16, b0=2177,b1=9772 works at both Y=7 and Y=162, since their difference is 155. With an actual 67-row in the ambient ledger, the lower modulus is 3410, so these are distinct ambient lower fibers, but their q-relevant projections coincide. This is a concrete counterexample to charging every fiber reuse as a new prime or a state collision.

### Theorem C3 — many exact valuation constraints

For prescribed centers a_i=3^{c_i}+5^{d_i} modulo q^K and prescribed exact valuations 0<h_i<K, put H=max h_i and choose a_* with h_*=H. There is one r satisfying all v_q(r-a_i)=h_i if and only if:

1. h_i<H implies v_q(a_i-a_*)=h_i;
2. h_i=H implies a_i=a_* modulo q^H;
3. the forbidden next digits (a_i-a_*)/q^H modulo q, over h_i=H, do not exhaust all q digits.

Proof: every solution is r=a_*+q^H t. For h_i<H the lower valuation is determined by a_i-a_*. At height H the only forbidden condition is t=(a_i-a_*)/q^H mod q. Avoiding all those digits is necessary and sufficient; higher digits are free.

Pairwise compatibility is not generally sufficient. For the actual row q=3,K=2,E={1}, anchor 0 at d=0,2,4 has centers 2,8,5 modulo 9. Each pair of valuation-one demands has a legal shared residue, but all three exclude every lift of r=2 modulo 3. These are three exponent cells of one original fiber, not three distinct lower guards. Together with the rigid example above, they separate positional/lift collisions from lower-guard collisions.

For repeated original rigid uses with h<s, same-anchor centers agree modulo q^(h+1). Thus repeated same-anchor uses collapse to one constraint; at most two anchor-center restrictions remain. One must not invent arbitrarily many independent next-digit restrictions by repeating the same rigid class.

## 7. MULTI-FIBER RESULTANT ANALYSIS

For original h=p^e and a fixed nonnegative ordinary integer Y, write

\[
R_h(Y)=\operatorname{Res}_T(T^h-5^{Yh},(T-2)^h-5^{Yh}).
\]

The source proves R_h(Y)!=0 for odd h and q|R_h(Y) for paired rigid use. [S4]

### Theorem C4 — support collision or resultant redundancy

If a single state supplies paired original rigid leaves at Y1,...,Ym, then

\[
u\mid G:=\gcd(Y_2-Y_1,\ldots,Y_m-Y_1),\qquad
q\mid\gcd_iR_h(Y_i).
\]

For a fixed q that passes the first condition,

\[
5^{Y_ih}\equiv5^{Y_1h}\pmod q,
\]

since w=u*h divides h(Y_i-Y_1). Thus the defining polynomial pairs, and therefore their resultants, coincide modulo q. Requiring the additional resultants is then redundant modulo that q.

Conversely, q=20771 divides both R_67(7) and R_67(8), as certified by the explicit common roots above, but the two original paired uses are state-incompatible. A resultant-gcd test can pass while the global state test fails.

This does not make all multi-use arithmetic filtering useless. It identifies the stronger missing filter: the lower order must divide G.

### Theorem C5 — exact finite-support paired-resource criterion

Suppose not all fixed ordinary Y_i are equal, so G>0 after taking absolute gcd. Let M be the largest divisor of G with all prime factors strictly below p. For a frozen ambient lower modulus M0, replace G first by gcd(G,M0); this makes the supported-candidate condition invariant under changing ordinary representatives by M0.

Define

\[
V_{p,e}(M)=\frac{5^{Mp^e}-1}{5^{Mp^{e-1}}-1}
=\prod_{u\mid M}\Phi_{up^e}(5).
\]

Among actual primes q>p, q=3 mod4, there exists **some** paired original rigid state at K=2,E={1}, active at every listed lower class, if and only if

\[
\boxed{q^2\mid V_{p,e}(M),\qquad q\mid R_{p^e}(Y_1).}
\]

Here positions are not prescribed; any prescribed colored top positions must additionally pass the same-b_c compatibility test of C2.

Proof of necessity: C2 gives u|M. Exact order and nonregularity then give q^2|V by the source finite-support cyclotomic invariant. Paired use gives q|R. [S4]

Proof of sufficiency: q^2|V with q>p forces exact order w=u*p^e, u|M, and s_q>=2. The polynomial T^h-5^(Y1*h) splits into simple roots in F_q because h divides w divides q-1; its roots are exactly 5^Y1<5^u>. Resultant zero therefore gives a0,a1 in this coset with a0-a1=2. They determine b0,b1. Choose a common r modulo q^2 avoiding at most two zero lifts. All Y_i agree modulo u, so the same state works everywhere. This proves the equivalence within the stated potential-position scope.

This is a finite exact arithmetic filter without a prime-size cutoff. It does not prove that the global typed problem forces any particular repeated allocation. OR alternatives cannot be converted into simultaneous uses.

### Fixed arithmetic checks

The exact gcds for Y=0,1,2 are

| Original h | gcd(R_h(0),R_h(1),R_h(2)) |
|---:|---:|
| 3 | 56=2^3*7 |
| 5 | 3872=2^5*11^2 |
| 7 | 3712=2^7*29 |

All nine resultants were independently organized as a Sylvester/Bareiss determinant and a rational polynomial Euclidean recurrence. Here G=M=1, and the order-collapse filters are Phi_3(5)=31, Phi_5(5)=11*71, Phi_7(5)=19531, all squarefree. Therefore no nonregular resource survives these specific simultaneous demands. This is not an arbitrary-Y or arbitrary-original-rank no-go.

For q=20771 and compatible Y=7,162, the program checks q^2|V_(67,1)(155) by modular arithmetic and validates the same paired state. This guards against mistakenly rejecting legal cross-fiber reuse.

Everything in this section refers to **original arithmetic rank and depth**. A derived macro is not a new q, and its current rank cannot be substituted into R_h or V_(p,e).

## 8. P5 ADVERSARIAL CHECK

The source P5 seed consists of one actual nonregular q and a finite regular admitted set T, closed under odd order support, such that

\[
U_*:=\operatorname{lcm}(w_q,\{w_p:p\in T\})=2^\epsilon M,
\qquad M=\prod_{p\in T}p.
\]

With K=2,E={1}, fixed r_p=2 and r_q=q+2, P5 gives a complete odd pooled cover. It explicitly does not supply an actual eligible q, and (c,d)=(1,0) is a full-certificate escape. [S5]

No state collision occurs: residues are selected once. As d varies, the proof selects which already-fixed row and anchor covers d; it never selects a new row state. The regular rows handle the least nonzero support coordinate, and q handles the terminal trace M|d. The terminal trace has at most two logarithms, exactly what one paired q can supply.

The classification below proves a converse and extends the accepted-valuation part of this construction. It does not reject P5.

## 9. OPPOSITE-ANCHOR OBLIGATIONS

At a maximal original coordinate, let A_c(y) be lower coverage and S_c(y) be full top coverage. Simultaneous completeness remains

\[
\boxed{\forall y\ (A_0(y)\vee S_0(y))\wedge(A_1(y)\vee S_1(y)).}
\]

A0-only cells require S1; A1-only cells require S0. EITHER lower coverage removes neither requirement. [S3,S5]

A typed obligation graph should therefore have state literals as resource nodes and anchor-tagged unmet cells as demand nodes. A node can be supported only by an actual state incidence or a type-correct provenance clause. With binary state options and at most two supporting literals per clause, the usual implications not-l1 -> l2 and not-l2 -> l1 are exact; contradiction requires a literal and its negation in one strongly connected component. Merely seeing an alternating sequence of anchor colors is not such a contradiction. General clauses require an integer/SAT hypergraph rather than a parity-cycle slogan.

For P5, d=0 leaves an explicit anchor-1 demand: every regular local value is -2 and the q-row local value is q-2. Repeated SPLITs do not erase it. The source seven-nonregular theorem implies that no addition of only regular rows, or re-selection of the states in a one-nonregular ledger, can make a simultaneous certificate. A hypothetical successful completion must have at least seven original nonregular primes. [S6]

## 10. SINGLE-NONREGULAR CLASSIFICATION

This is the main unbounded deduction of this phase. It concerns **odd pooled EITHER coverage**, with no use of a favorable two-adic boundary predicate.

### Lemma C6 — extension of every regular-safe prefix

Fix a finite regular-row system and its global states. In a CRT domain supporting all its full row periods, fix parity and process odd prime coordinates increasingly. At a regular row p, the logarithm guards involve only smaller prime coordinates. At most one anchor is active. An inactive row imposes no restriction; an active row always has an unresolved full center. Choose it and continue.

Thus any prefix that avoids the earlier regular rows extends to a common escape of all regular rows. Higher regular rows cannot remove an already legal lower prefix. The argument also holds in any finite period refinement, but such a refinement is not claimed to add a new original support row.

### Lemma C7 — two-point projection rigidity

Let S be the common full escape set of a fixed regular system, in a supporting CRT period. For W dividing that period, suppose

\[
|\pi_W(S)|\le2.
\]

For every odd p|W:

(a) p must be an actual regular admitted row, and 1 must belong to E_p.

(b) v_p(W)=1.

(c) At every earlier-safe prefix, the p-row must be active at some anchor; consequently

\[
|\pi_{w_p}(S)|\le2.
\]

Proof. If p is absent, inactive at some safe prefix, or valuation 1 is not accepted, all p first digits have safe lifts. Lemma C6 extends each one to S, producing at least p>=3 distinct W-projections.

If p^2|W, consider an active center. Its p-1 second digits with v_p(d-center)=1 have local valuation 2 and are safe because accepted valuations are odd. The central second digit has a safe center lift as well. Thus all p lifts of its central first digit occur in the safe projection modulo p^2. This also holds at K=2: all these lifts have the same unresolved row value. Lemma C6 again yields at least p distinct W-projections.

Hence (a),(b) hold. The same argument rules out any safe prefix on which the p-row is inactive. Therefore every d in S belongs to one of the at most two fixed guards b_p,0 or b_p,1 modulo w_p, giving (c). QED.

No measure estimate or fractional Hall inequality is used in this proof.

### Theorem C8 — exact frozen-state terminal trace

This is first a full-exponent statement. The source joint reverse-CRT theorem identifies whole odd full pooled coverage with odd coarse pooled coverage; no simultaneous two-adic safety claim is added. [S5]

Let q be the only nonregular row and R_<q the regular original rows below q. Define

\[
M_q=\operatorname{lcm}(w_q,\{\ell_p:p\in R_{<q}\}),
\]

\[
D_q=\pi_{w_q}\{d\bmod M_q:\text{every }p\in R_{<q}\text{ is safe at both anchors}\}.
\]

Let B_q be the set of logarithms of q's **rigid fatal** components. It has at most two elements. Do not include dynamic guards merely because they contain some fatal exponents.

For the frozen global states, and arbitrary additional regular rows above q,

\[
\boxed{\text{complete odd pooled cover}\quad\Longleftrightarrow\quad D_q\subseteq B_q.}
\]

Proof. If D_q is contained in B_q, any exponent not covered by a lower regular row lies in a globally fatal rigid q-class, so it is covered.

Otherwise take an earlier regular escape with logarithm outside B_q. All prime coordinates in M_q are below q. Extend any missing lower digits compatibly; choose the q-coordinate to avoid its possible dynamic component, using the safe center. A nonaccepted rigid component is already safe. Difference 2 prevents another anchor from introducing a simultaneous q-divisibility obligation at this logarithm. Then extend through all higher regular rows by C6. This produces a full common odd escape, a contradiction to pooled completeness. QED.

### Definition — hereditary regular order closure

Starting with every odd prime factor of w_q, recursively add every odd prime factor of w_p for each required p. Denote the minimal resulting set by T(q).

The closure passes the **regular squarefree support gate** when the odd part of w_q and the odd part of every w_p in the closure are squarefree, and every required p is an actual regular admitted prime. All dependencies decrease strictly, so this definition is well founded and finite for a fixed q.

Equivalently define a class H recursively: p belongs to H exactly when p is regular and admitted, the odd part of w_p is squarefree, and every odd prime factor of w_p belongs to H. Then the arithmetic closure gate for q is that its odd order part is squarefree and its odd factors belong to H.

### Theorem C9 — single-nonregular realizability, fixed K and E

Fix an actual finite prime ledger P=R union {q}, where every p in R is regular and q is nonregular. Fix **all** K_p and accepted sets E_p. Permit the shared residues r_p to range freely over their complete legal residue rings.

There exists one global shared-residue vector producing a complete odd pooled cover if and only if all three conditions hold:

\[
\boxed{\begin{array}{l}
\text{the regular squarefree closure gate passes and }T(q)\subseteq R;\\
1\in E_p\quad\text{for every }p\in T(q);\\
E_q\cap\{h:0<h<s_q,\ h\text{ odd}\}\ne\varnothing.
\end{array}}
\]

**Necessity.** By C8, the regular escape trace modulo w_q has at most two values. Apply C7 first to W=w_q and then to each required w_p. This forces all of the recursive support and squarefreeness conditions and forces valuation 1 to be accepted by each support row. The trace is nonempty by C6, so B_q is nonempty, requiring an accepted rigid valuation h<s_q at q.

**Sufficiency.** Let T=T(q), M=product(p in T), and choose any accepted h<s_q at q. Put

\[
r_p=2\pmod{p^{K_p}}\quad(p\in T),\qquad
r_q=q^h+2\pmod{q^{K_q}}.
\]

Other regular rows may have arbitrary legal residues, since adding coverage cannot destroy a cover. Fix any nonnegative d.

If some p in T does not divide d, choose the least such p. Every odd factor of w_p lies in T below p and divides d; because the order is squarefree in odd primes, its odd part divides d. If w_p is odd or d is even, w_p divides d, and

\[
v_p(1-5^d)=s_p+v_p(d)=1.
\]

Anchor 0 is fatal. If w_p is even and d is odd, 5^d=-1 modulo p and the plus version of LTE gives v_p(1+5^d)=1, so anchor 1 is fatal. Both valuations are accepted.

If every p in T divides d, then M|d. The odd part of w_q divides d, and because h<s_q the order modulo q^(h+1) is still w_q. Thus 5^d is 1, or -1 in the even-order/odd-d case, modulo q^(h+1). On anchor 0 or 1 respectively, the local value is q^h modulo q^(h+1), hence has exact accepted valuation h. Every exponent is covered by a fixed actual row-state at one anchor. QED.

For K=2,h=1 this is exactly the source P5 construction. At arbitrary fixed K the new construction need **not** have U=L; the proof is for all integers d and does not identify the two periods.

### Explicit newly excluded hereditary signatures

The regular primes 11,19,67 have orders 5,9,22 respectively. They fail H because 5 is not admitted, 9 has repeated odd depth, and 67 leads to 11 then 5. Therefore a single-nonregular q with any of 11,19,67 dividing w_q cannot produce a whole odd pooled cover with only regular additional rows, even if its direct odd factors are squarefree and all directly supported.

This is stronger than requiring only direct support in P4.2. In contrast, 3,7,31,43,127,1303 pass the hereditary regular gate. These are illustrative certified signatures, not a new prime scan or a complete list of H.

### What this does not classify

With additional restrictions on allowed residues in S_q, the three signature/accepted-set conditions need not be sufficient: they may exclude the displayed residues. Use C8 and the global integer configuration formulation instead. No actual nonregular q passing the arithmetic closure gate is supplied by this package.

## 11. GATE B AND GATE C

### Gate B — two nonregular rows

Freeze the regular states and a common full domain. Remove every already satisfied typed demand. For a residual vertex v, let C_i(v) be the states of nonregular q_i that cover it with the required type. Then the exact feasible state-pair graph is

\[
\mathcal E=(\mathcal S_{q_1}\times\mathcal S_{q_2})\setminus
\bigcup_v[(\mathcal S_{q_1}\setminus C_1(v))\times(\mathcal S_{q_2}\setminus C_2(v))].
\]

The residual demand is globally realizable iff E is nonempty. BOTH uses separate tagged vertices; EITHER uses one pooled vertex. Opposite-anchor obligations use their actual remaining tags. This is a forbidden-rectangle CSP, not two separate anchor matchings.

C2-C5 remove impossible state pairs or forced original suppliers. No general arithmetic classification of every two-nonregular whole odd pooled system is proved here. The existing at-least-seven theorem separately excludes two-nonregular simultaneous BOTH certificates. [S6]

### Gate C — the two-row, one-nonregular minimal motif

The source actual 67/20771 SPLIT is a smallest original-row-count pooled full-fiber motif. It does not extend globally. [S5]

More generally, **no two-row ledger consisting of one regular p and one nonregular q can be a whole odd pooled cover**. By C9, T(q) would have to fit inside {p}. It is nonempty because a nonregular admitted prime cannot have order 1 or 2. The order of p can have no odd prime factor: it would be a smaller required support prime, not p. Thus p=3. Squarefree closure then restricts the nonregular q to order 3 or 6; Phi_3(5)=31 and Phi_6(5)=3*7 supply only regular admitted order candidates. Contradiction.

This proves a global nonextension result in the single-nonregular two-row class. It does not classify every minimal frontier with several nonregular origins, nor does it forbid reusing one legal original leaf in different supported ambient fibers.

## 12. EXACT COMPUTATION

All computations use Python standard-library integers, modular powers, exact Fractions, and exact determinants. The computation specifications were written before their corresponding runs. No q cutoff was increased.

| Check | Executed domain | Result |
|---|---|---|
| Actual configuration ILP | 5859 shared-state vectors, all 1302 coarse cells | 0 complete; max 1300 covered |
| Fractional configuration witness | all 1302 coarse cells | uniform 830/651 coverage capacity |
| Full escape lifts | one direct full CRT witness per 5859 vectors | all five rows and both anchors safe |
| Six demands | 340 top words; 8160 truth cells | 0 violations |
| Paired positions | q=20771,40487; entire exact w-periods | 5192/40485 pairs; 33/652 same-lower edges |
| Structured q^2 states | all mod-q bases plus exceptional lift groups | 431434441/1639197169 states accounted for |
| Integer resultants | h=3,5,7; Y=0,1,2 | Bareiss equals rational Euclid |
| Multi-use order filter | three G=1 cases and compatible q20771 reuse | exact checks pass |
| Valuation-family lemma | all 129 sets of 1..3 constraints (a,1), a mod9 | formula equals direct solutions |
| Regular width | 1880 states at q=3,7,11; K=2,3 | 1830700 anchor-cell checks; 2040 width tests |
| Accepted-set sensitivity | q=3, K=4,5; all residues and E={1},{3},{1,3} | higher-shell/valuation-1 tests pass |
| Named unit tests | 13 tests | PASS |

The resultants and paired counts have two differently organized checks, but the package is one reference software environment, not two independent software stacks. Symbolic unbounded statements C6-C9 are proved above, not inferred from these finite tables.

The complete deterministic data are in results.json; the program is reference.py. Full q^2 enumeration, full 72-million-cell L enumeration, a new nonregular-prime scan, and repository-native replay were not performed and are not claimed.

## 13. STRONGEST NEW NECESSARY CONDITION

For the one-nonregular pooled survivor, direct squarefree support is not enough. Its entire recursive odd order-support closure must consist of actual regular admitted rows with valuation 1 accepted, and the terminal q must accept a rigid valuation below s_q. With unrestricted shared residues this necessary condition is also sufficient, via C9.

For general stateful pooled recursion, any genuinely forced repeated original paired use must pass the common lower-order/position constraints before its resultants are used. When ordinary lower differences have G>0, the supplier satisfies the finite-support square-divisor and paired-resultant conditions of C5. Such conditions cannot be imposed on unselected OR alternatives or on a descended macro's current depth.

The actual configuration example proves that weighted rowwise Hall tests cannot replace the global integral state problem even when every row is an actual prime and U is supported by actual rows.

## 14. CAN THE POOLED BRANCH NOW BE UNIVERSALLY ELIMINATED?

**NO.**

The phase does not provide a universal odd pooled no-go, a complete actual odd pooled cover, a simultaneous C=1 certificate, a counterexample to A303656, or a proof of A303656. It gives an exact single-nonregular realization classification and explicit global configuration obstructions.

An actual q passing C9 would give a whole odd EITHER cover under the displayed residue construction. This package does not establish whether such a q exists. Several-nonregular pooled systems require further state-compatible analysis. Even an odd EITHER construction would leave the separate simultaneous BOTH obligations.

## 15. NEXT SINGLE TARGET

**TWO-NONREGULAR TERMINAL-TRACE CLASSIFICATION.**

For q1<q2, preserve one global state for q1 while classifying the trace of all lower escapes modulo w_q2. Determine when that trace is contained in the at-most-two rigid logarithms of q2, with q1's dynamic and rigid components kept as one paired state. Seek a structural forbidden-rectangle/state-collision theorem rather than a larger prime scan. This is the next unclosed step after the single-nonregular classification, not a claim that q1 may be reselected for each trace cell.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

## Source key

All paths below are pinned to the main SHA in section 1; Git blob identities and the reading boundary are in SOURCE_BINDING.json.

[S1] analysis/c1_two_anchor_common_residue_phase_a/REPORT.md

[S2] analysis/c1_prefix_frontier_realizability_phase_a/REPORT.md

[S3] analysis/c1_two_anchor_sync_phase_a/REPORT.md

[S4] analysis/c1_kraft_hall_phase_a/REPORT.md

[S5] analysis/c1_pooled_lower_cover_phase_b/REPORT.md and THEOREM_AUDIT.md

[S6] analysis/c1_unified_endgame_phase_b/REPORT.md

[S7] analysis/c1_pooled_lower_cover_phase_b/DEFINITIONS.md
