# A303656 arithmetic realizability classification of \(\ell\)-adic prefix frontiers — Targeted Phase A

## 0. Verdict

```text
PRIMARY RESULT:
ONE-ANCHOR FIBERWISE REALIZABILITY THEOREM
+
COMPLETE SYMBOLIC CLASSIFICATION FOR beta <= 3
+
NEW WIEFERICH-LEAF INVENTORY INVARIANT
+
EXACT TWO-ANCHOR ROW-COMPATIBILITY CRITERIA

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The requested gap can be closed exactly at the following scope:

> Fix one odd coordinate \(\ell\), a target depth \(\beta\), one anchor
> \(c\), and one parameter-labelled abstract centered prefix frontier. First
> choose the actual rigid-resource rows and any required support row satisfying
> the three arithmetic gates. Let \(U\) be the coarse period induced by those
> rows together with any explicitly retained ambient rows. Then fix one
> compatible lower-coordinate CRT point of this final induced system (or
> compatibly extend a previously prescribed partial lower point). On that
> final lower fiber, the frontier is realized exactly.

This is a genuine arbitrary-\(\beta\) theorem. It does **not** assert that the frontier extends to a complete certificate, that one lower fiber works uniformly, or that separately realizable frontiers at the two anchors admit one common-residue system.

## 1. Authority and integration boundary

The research was bound to:

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 1100eb5ba01d90e5b1001be0bdfa464860fdbb92
main tree: ad1269916bf420c564e34887a96c808033fe538b
```

The bound `STATUS.md` still states:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The source study was read-only. This repository-native integration adds only
this analysis directory on a dedicated audit branch. It does not modify
`STATUS.md`, any authority record, a workflow, or `main`.

The principal source blobs reconstructed were:

```text
analysis/c1_entangled_coordinate_deficit/FORMAL_CLASS.md
  blob 2a788348cf9abdce43f47809b7b6fd6cb8f3f04d

analysis/c1_minimal_saturated_coordinate_inverse/
  source/A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A/DEFINITIONS.md
  blob 5908a3373a5e8d0997c6df387be59e17239f961a

analysis/c1_minimal_saturated_coordinate_inverse/
  source/A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A/ABSTRACT_CLASSIFICATION.md
  blob 7ad233f07750d6baeea4b822fd57e4c12f46f157

analysis/c1_minimal_saturated_coordinate_inverse/
  source/A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A/REALIZABILITY_AUDIT.md
  blob 27b255f6bedbf983f0d3ba58f64e1af8b7e0061a

analysis/c1_contraction_tree_phase_a/DEFINITIONS.md
  blob 922d31d72f74a8c81f75b5b3a64902c0ad6a0448
```

## 2. Reconstruction of the repository definitions

### 2.1 Admitted row data

The admitted odd rows are indexed by distinct primes

\[
p\equiv 3\pmod 4,\qquad p\ne 5.
\]

For every row one chooses:

\[
K_p\ge 2,\qquad r_p\pmod {p^{K_p}},\qquad
\varnothing\ne E_p\subset\{1,\ldots,K_p-1\},
\]

where every member of \(E_p\) is a positive odd valuation. The same residue \(r_p\) is used at anchors \(c=0,1\). A value zero modulo \(p^{K_p}\) is unresolved and is never accepted.

Put

\[
w_p=\operatorname{ord}_p(5),\qquad
s_p=v_p(5^{w_p}-1),\qquad
a_p=\max(0,K_p-s_p),
\]

\[
\ell_p=w_p p^{a_p},\qquad
U=\operatorname{lcm}(t_2,\{w_p\}),\qquad
L=\operatorname{lcm}(t_2,\{\ell_p\}),
\]

and for an odd rational prime \(\ell\),

\[
\beta_\ell=v_\ell(U)=\max_q v_\ell(w_q).
\]

The order-dependency graph has an edge \(p\to q\) when \(p\mid w_q\). Since \(w_q\mid q-1\), every edge is strictly increasing, so the graph is a DAG.

### 2.2 Final induced ambient system and fixed \(\ell\)-coordinate fiber

For the realization theorem, choose the finite actual resource rows and any
explicitly retained ambient rows before fixing the complete lower-coordinate
fiber. Let \(U\) be their resulting coarse period. Fix:

- an odd rational prime coordinate \(\ell\mid U\);
- \(\beta=v_\ell(U)\);
- one anchor \(c\in\{0,1\}\);
- one compatible assignment of every lower rational-prime coordinate of this
  final \(U\).

The fiber is

\[
X_{\ell,\beta}=\mathbf Z/\ell^\beta\mathbf Z.
\]

After translation, a chosen dynamic center lift is normalized to \(\zeta=0\).

If a lower point was prescribed before the resources were selected, the
theorem applies only after extending it compatibly to every newly introduced
lower prime power. It does not claim that the selected rows preserve an
externally frozen ambient \(U\) or its unextended coordinate system. Such a
stronger ambient-relative theorem would require restricting the resource sets
to rows whose relevant order factors are already supported by that frozen
\(U\).

### 2.3 Dynamic row

Only the admitted row with prime \(p=\ell\) can supply the dynamic event at coordinate \(\ell\). Put

\[
m=\min(a_\ell,\beta),\qquad
J=\{0\le j<m:s_\ell+j\in E_\ell\}.
\]

Because accepted valuations are odd,

\[
j\in J\Longrightarrow s_\ell+j\equiv1\pmod2.
\]

Thus all accepted shell indices lie in one fixed parity class determined by the actual integer \(s_\ell\). The shells are

\[
S_j(\zeta)=\{x:v_\ell(x-\zeta)=j\},
\]

and the dynamic event is

\[
A_J(\zeta)=\bigcup_{j\in J}S_j(\zeta).
\]

The center cylinder

\[
C_m(\zeta)=\{x:x\equiv\zeta\pmod{\ell^m}\}
\]

is unresolved by the dynamic row and is excluded from its fatal event.

### 2.4 Rigid row

A rigid fatal row with prime \(q\) is assigned to

\[
\ell=P^+(w_q).
\]

After lower coordinates are fixed, its nonempty slice is one cylinder

\[
C_e(t)=\{x:x\equiv t\pmod{\ell^e}\},
\qquad e=v_\ell(w_q),\quad1\le e\le\beta.
\]

One actual prime row supplies at most one such cylinder at one anchor and one fixed lower assignment.

### 2.5 Abstract centered prefix frontier

The existing inverse theorem proves that every irredundant full fiber cover has:

1. exactly one rigid cylinder \(C_e(\zeta)\) containing the dynamic center;
2. no other rigid cylinder intersecting that centered cylinder;
3. a complete prefix-code frontier in every unaccepted side branch before depth \(e\);
4. an essential dynamic row exactly when some accepted \(j<e\) occurs.

The only overlap is the accepted dynamic tail inside the centered cylinder:

\[
A_J(\zeta)\cap C_e(\zeta)
 =\bigcup_{\substack{j\in J\\j\ge e}}S_j(\zeta).
\]

This is the abstract geometry to be filtered arithmetically.

## 3. Main theorem: exact one-anchor arithmetic realizability

### 3.1 Resource sets

For every depth \(d\ge1\), define the active rigid resource set

\[
\mathcal R_{\ell,d}=
\left\{
q:\begin{array}{l}
q\text{ prime},\ q\equiv3\pmod4,\ q\ne5,\\
s_q\ge2,\\
P^+(w_q)=\ell,\\
v_\ell(w_q)=d
\end{array}
\right\}.
\]

Define the exact ambient-support set

\[
\mathcal S_{\ell,\beta}=
\left\{
q:\begin{array}{l}
q\text{ prime},\ q\equiv3\pmod4,\ q\ne5,\\
v_\ell(w_q)=\beta
\end{array}
\right\}.
\]

Unlike \(\mathcal R_{\ell,d}\), the support set imposes neither \(s_q\ge2\) nor \(P^+(w_q)=\ell\). A regular row may create the ambient \(\ell^\beta\)-coordinate while contributing no rigid leaf.

For an abstract frontier \(F\), let

\[
n_d(F)=\#\{\text{rigid frontier leaves of exact depth }d\}.
\]

### 3.2 Theorem A — fiberwise arithmetic realizability criterion

Fix \(\ell,\beta,c\) and one parameter-labelled abstract centered prefix
frontier \(F\). A *final-induced-system realization* means that a finite
collection of actual resource rows and any explicitly retained ambient rows
is chosen first, their orders induce a coarse period \(U\) with
\(v_\ell(U)=\beta\), and only then one compatible lower-coordinate CRT point of
that final system is fixed. A compatible previously prescribed partial lower
point may instead be extended to the new lower prime powers. Such a
realization of \(F\) exists if and only if all of the following gates hold.

#### Dynamic gate

When the dynamic row is present:

\[
\ell\equiv3\pmod4,\qquad \ell\ne5,
\]

and

\[
 s_\ell+j\text{ is odd for every }j\in J.
\]

Equivalently, the abstract parity label must equal the actual parity of \(s_\ell\). The requested depth \(m\) is then realized by choosing

\[
K_\ell=s_\ell+m.
\]

#### Rigid leaf-inventory gate

For every \(1\le d\le\beta\),

\[
n_d(F)\le |\mathcal R_{\ell,d}|.
\]

Each leaf requires its own distinct prime row.

#### Ambient-depth gate

Either an active leaf itself has depth \(\beta\), or an additional support row exists:

\[
n_\beta(F)>0
\quad\text{or}\quad
\mathcal S_{\ell,\beta}\ne\varnothing.
\]

No additional one-anchor `CENTER_BLOCKED` condition exists: after the resource
rows determine the final ambient coordinate system and a compatible lower
point has been fixed, every desired dynamic center and every desired rigid
cylinder position can be placed by choosing the row residue.

### 3.3 Proof of necessity

The dynamic conditions are direct consequences of the admitted-prime definition and the positive-odd-valuation condition.

Every rigid leaf is induced by one actual rigid row \(q\). Such a row must have a positive odd accepted valuation strictly below \(s_q\), so necessarily \(s_q\ge2\). Its assigned coordinate and depth are exactly

\[
P^+(w_q)=\ell,
\qquad v_\ell(w_q)=d.
\]

One row has at most one active logarithm modulo \(w_q\), hence at most one rigid cylinder on the fixed fiber. Distinct leaves therefore inject into distinct members of \(\mathcal R_{\ell,d}\).

Finally,

\[
\beta=v_\ell(U)=\max_qv_\ell(w_q),
\]

so some admitted row has exact \(\ell\)-order depth \(\beta\). If no active frontier leaf has that depth, this row is an additional support row.

### 3.4 Proof of sufficiency

First choose distinct rigid-resource rows for all leaves and, when required,
an ambient-support row. Together with any explicitly retained ambient rows,
these choices determine the final coarse period \(U\). By the depth gates,
every selected row has \(\ell\)-order depth at most \(\beta\), and some selected
or retained row has exact depth \(\beta\); hence \(v_\ell(U)=\beta\).

Now choose one compatible lower-coordinate CRT point of this final system. If
a partial lower point was prescribed earlier, extend each of its coordinates
to the higher powers introduced by the selected orders and choose values at
new lower coordinates. The construction is conditional on that extension
being compatible. This quantifier order is essential: the theorem does not
promise to add arbitrary resources while leaving a pre-existing frozen \(U\)
unchanged.

#### Realizing one rigid leaf

Take a desired leaf \(C_d(t)\) and a fresh prime \(q\in\mathcal R_{\ell,d}\). Write

\[
w_q=u_q\ell^d,
\qquad P^+(u_q)<\ell.
\]

The final fixed lower assignment specifies the exponent modulo \(u_q\), while the desired cylinder specifies it modulo \(\ell^d\). CRT gives one exponent class

\[
b_q\pmod{w_q}
\]

whose slice is exactly \(C_d(t)\).

Use

\[
K_q=2,\qquad E_q=\{1\},
\]

and choose

\[
r_q\equiv3^c+5^{b_q}(1+q)\pmod{q^2}.
\]

Because \(s_q\ge2\), the order of \(5\) modulo \(q^2\) is still \(w_q\). On the class \(b_q\pmod{w_q}\),

\[
v_q(r_q-3^c-5^d)=1;
\]

outside that class, the value is nonzero modulo \(q\). Thus this row supplies exactly the prescribed cylinder and no local zero.

Applying this independently to every rigid leaf realizes all rigid frontiers, since row residues at distinct primes are independent.

#### Realizing the dynamic bundle

Let \(d_*\) be the exponent represented by the desired center. Choose

\[
K_\ell=s_\ell+m,
\qquad
E_\ell=\{s_\ell+j:j\in J\},
\]

and

\[
r_\ell\equiv3^c+5^{d_*}\pmod{\ell^{K_\ell}}.
\]

Along the \(\ell\)-fiber, the exponent difference is a unit multiple of \(w_\ell(x-\zeta)\). Odd-prime LTE gives, outside the center cylinder,

\[
v_\ell(r_\ell-3^c-5^d)
=s_\ell+v_\ell(x-\zeta).
\]

Hence precisely the shells \(S_j(\zeta)\), \(j\in J\), are accepted. On \(C_m(\zeta)\), the local value is zero modulo \(\ell^{s_\ell+m}\), so it remains unresolved exactly as required.

#### Creating ambient depth without an active leaf

If \(n_\beta(F)=0\), choose \(q_*\in\mathcal S_{\ell,\beta}\) and add a row with

\[
K_{q_*}=2,\qquad E_{q_*}=\{1\},\qquad
r_{q_*}\equiv3^c\pmod{q_*^2}.
\]

At the fixed anchor,

\[
r_{q_*}-3^c-5^d\equiv-5^d\not\equiv0\pmod{q_*},
\]

so the support row contributes no fatal event, while its order forces exact ambient depth \(\beta\).

All selected active leaf rows have \(\ell\)-order depth at most \(\beta\), and at least one selected row has exact depth \(\beta\). Therefore the induced rank-\(\ell\) event family is exactly \(F\). This completes the proof.

## 4. New necessary invariant: Wieferich leaf inventory

### 4.1 Universal per-leaf invariant

Every rigid leaf at depth \(d\) consumes a distinct prime \(q\) satisfying

\[
q^2\mid5^{w_q}-1,
\qquad
w_q=\ell^d u,\quad P^+(u)\le\ell,
\]

and

\[
q\equiv1+2\ell^d\pmod{4\ell^d}.
\]

The last congruence follows from \(\ell^d\mid w_q\mid q-1\) and \(q\equiv3\pmod4\).

Thus an abstract leaf is not a freely available cylinder. It is a demand for a distinct admitted base-5 nonregular prime having one exact order signature.

### 4.2 Center-depth versus row-count bound

Suppose a dynamic frontier has centered rigid depth \(e\) and uses \(N\) rigid rows in total. For every unaccepted \(j<e\), the \(\ell-1\) side branches each require at least one rigid leaf. Therefore

\[
N\ge1+(\ell-1)\#\{0\le j<e:j\notin J\}.
\]

Since \(J\) lies in one parity class:

- if \(s_\ell\) is odd, only even \(j\) may be accepted, so
  \[
  N\ge1+(\ell-1)\lfloor e/2\rfloor;
  \]
- if \(s_\ell\) is even, only odd \(j\) may be accepted, so
  \[
  N\ge1+(\ell-1)\lceil e/2\rceil.
  \]

Consequently, with

\[
a=\left\lfloor\frac{N-1}{\ell-1}\right\rfloor,
\]

one necessarily has

\[
e\le2a+1\quad(s_\ell\text{ odd}),
\qquad
e\le2a\quad(s_\ell\text{ even}).
\]

For a rigid-only frontier, the stronger bound \(N\ge1+e(\ell-1)\) holds for a centered leaf at depth \(e\).

This is a universal arithmetic obstruction because every required row is a distinct nonregular prime resource.

## 5. Inventory-generating recurrence: the arithmetic replacement for \(F_\ell(h)\)

Introduce variables \(x_d\), where one factor \(x_d\) records one rigid leaf of exact depth \(d\). For a rooted cylinder at depth \(d\) inside a fiber of total depth \(\beta\), define

\[
H_\beta=x_\beta,
\qquad
H_d=x_d+H_{d+1}^{\ell}
\quad(1\le d<\beta).
\]

Setting every \(x_d=1\) recovers the abstract recurrence

\[
F_\ell(0)=1,
\qquad F_\ell(h)=1+F_\ell(h-1)^\ell.
\]

The multivariate polynomial retains the information destroyed by \(F_\ell(h)\): the exact number of depth-\(d\) prime rows demanded by each frontier.

### Rigid-only class

The complete rigid-only fiber class is

\[
H_1^\ell.
\]

### Dynamic class

For fixed valid \((m,J,e)\), the centered prefix-frontier polynomial is

\[
P_{m,J,e}
=x_e
\prod_{\substack{0\le j<e\\j\notin J}}
H_{j+1}^{\ell-1},
\]

provided \(J\cap\{0,\ldots,e-1\}\ne\varnothing\).

### Exact arithmetic truncation

Write a monomial as

\[
x_1^{n_1}\cdots x_\beta^{n_\beta}.
\]

The one-anchor arithmetically realizable class is obtained exactly by:

1. deleting dynamic labels incompatible with the actual parity of \(s_\ell\);
2. retaining only monomials with
   \[
   n_d\le|\mathcal R_{\ell,d}|\quad(1\le d\le\beta);
   \]
3. when \(n_\beta=0\), retaining the monomial only if
   \[
   \mathcal S_{\ell,\beta}\ne\varnothing.
   \]

This is the requested `ARITHMETICALLY REALIZABLE FRONTIER CLASS` in an exact symbolic form.

## 6. Complete symbolic classification for \(\beta=1,2,3\)

The following classification is parameter-labelled: different values of \(m\) remain distinct labels even when they induce the same set family.

### 6.1 \(\beta=1\)

There are exactly two abstract classes:

| Type | Polynomial | Arithmetic conditions |
|---|---:|---|
| rigid-only | \(x_1^\ell\) | \(|\mathcal R_{\ell,1}|\ge\ell\) |
| dynamic pair | \(x_1\) | \(\ell\) admitted, \(s_\ell\) odd, \(|\mathcal R_{\ell,1}|\ge1\) |

Ambient support is automatic because every candidate has a depth-one active leaf.

### 6.2 \(\beta=2\)

Put

\[
H_1=x_1+x_2^\ell.
\]

The complete list is:

| Type | Parameter labels | Polynomial |
|---|---|---:|
| rigid-only | — | \(H_1^\ell\) |
| dynamic \(J=\{0\}\), \(s_\ell\) odd | \(m=1,2\) | one copy of \(H_1\) for each \(m\) |
| dynamic \(J=\{1\}\), \(s_\ell\) even | \(m=2\) | \(x_2H_1^{\ell-1}\) |

Hence the parameter-labelled abstract count is

\[
2^\ell+2^{\ell-1}+4.
\]

For the rigid-only family, refining exactly \(t\) top branches gives inventory

\[
(n_1,n_2)=(\ell-t,\ell t)
\]

with multiplicity \(\binom\ell t\). The arithmetic criterion applies directly to these two coordinates.

For \(J=\{0\}\), the two unlabelled possibilities are:

\[
(n_1,n_2)=(1,0)
\]

with an additional ambient support row, or

\[
(n_1,n_2)=(0,\ell).
\]

For \(J=\{1\}\), refining \(t\) of the \(\ell-1\) outer top branches gives

\[
(n_1,n_2)=(\ell-1-t,1+\ell t)
\]

with multiplicity \(\binom{\ell-1}{t}\).

### 6.3 \(\beta=3\)

Put

\[
H_2=x_2+x_3^\ell,
\qquad
H_1=x_1+H_2^\ell.
\]

The complete parameter-labelled list is:

| Type | Parameter labels | Polynomial |
|---|---|---:|
| rigid-only | — | \(H_1^\ell\) |
| dynamic \(J=\{0\}\), \(s_\ell\) odd | \(m=1,2,3\) | one copy of \(H_1\) for each \(m\) |
| dynamic \(J=\{0,2\}\), \(s_\ell\) odd | \(m=3\) | \(x_1+(x_2+x_3)H_2^{\ell-1}\) |
| dynamic \(J=\{2\}\), \(s_\ell\) odd | \(m=3\) | \(x_3H_1^{\ell-1}H_2^{\ell-1}\) |
| dynamic \(J=\{1\}\), \(s_\ell\) even | \(m=2,3\) | one copy of \(H_2H_1^{\ell-1}\) for each \(m\) |

Let

\[
F=1+2^\ell.
\]

The exact parameter-labelled count is

\[
F^\ell+(2F)^{\ell-1}+4F+4F^{\ell-1}.
\]

For \(\ell=3\), this gives

\[
729+324+36+324=1413,
\]

matching the independent literal generator.

## 7. Two-anchor common-residue theorems

The one-anchor theorem deliberately does not identify separate anchorwise choices. The common-residue obstruction can nevertheless be classified exactly row by row.

### 7.1 Theorem B — exact rigid two-anchor valuation criterion

Fix an actual rigid resource prime \(q\), desired full logarithm classes

\[
b_0,b_1\pmod{w_q},
\]

and desired finite positive odd valuations

\[
0<h_0,h_1<s_q.
\]

For realizability one may take \(K=1+\max(h_0,h_1)\le s_q\), so \(b_c\pmod{w_q}\) determines \(5^{b_c}\pmod{q^K}\). More generally, with selected exponent representatives and any \(K>\max(h_0,h_1)\), put

\[
\Delta=5^{b_0}-5^{b_1}-2,
\qquad
\nu=\min(v_q(\Delta),K),
\]

where \(\nu=K\) when \(\Delta\equiv0\pmod{q^K}\).

There exists one shared residue \(r_q\pmod{q^K}\) such that

\[
v_q(r_q-1-5^{b_0})=h_0,
\qquad
v_q(r_q-3-5^{b_1})=h_1
\]

if and only if the minimum of

\[
\{\nu,h_0,h_1\}
\]

is attained at least twice.

#### Proof

Set

\[
x=r_q-(1+5^{b_0}).
\]

Then the two requirements are

\[
v_q(x)=h_0,
\qquad v_q(x+\Delta)=h_1.
\]

The ultrametric inequality says that among the three valuations of \(x\), \(\Delta\), and \(x+\Delta\), a strict minimum cannot occur only once. This proves necessity. Conversely, in each of the three allowed minimum patterns, a unit coefficient for \(x/q^{h_0}\) can be chosen to avoid or force the required cancellation. Since \(q\) is odd, at least one admissible unit remains. This proves sufficiency.

#### Useful corollaries

- If \(h_0=h_1=h\), compatibility is equivalent to
  \[
  v_q(\Delta)\ge h.
  \]
- If \(h_0<h_1\), compatibility is equivalent to
  \[
  v_q(\Delta)=h_0.
  \]
- If \(h_1<h_0\), compatibility is equivalent to
  \[
  v_q(\Delta)=h_1.
  \]
- At the minimal choice \(h_0=h_1=1\),
  \[
  5^{b_0}-5^{b_1}\equiv2\pmod q.
  \]

This recovers the previous \(q=20771\) condition and upgrades it to arbitrary allowed rigid valuations.

A one-sided minimal-valuation row with \(E_q=\{h\}\) can be made fatal at one anchor and nonfatal at the other when the other anchor has no active logarithm modulo \(q\), or when

\[
v_q(\Delta)\le h.
\]

If \(v_q(\Delta)>h\), the ultrametric law forces the same valuation \(h\) at both anchors.

### 7.2 Theorem C — dynamic center-difference criterion

For one dynamic row \(\ell\) to have prescribed zero centers at exponents \(d_0,d_1\) under one shared residue modulo \(\ell^K\), it is necessary and sufficient that

\[
5^{d_0}-5^{d_1}\equiv2\pmod{\ell^K}.
\]

Let

\[
H_{\ell,s}=\langle5\rangle
\subset (\mathbf Z/\ell^{s_\ell}\mathbf Z)^\times.
\]

There exist some compatible centers at every precision \(K\ge s_\ell\) if and only if

\[
2\in H_{\ell,s}-H_{\ell,s}.
\]

A solution modulo \(\ell^{s_\ell}\) lifts to every higher precision because \(5^{w_\ell}\) generates the full principal subgroup

\[
(1+\ell^{s_\ell}\mathbf Z)/(1+\ell^K\mathbf Z).
\]

For \(\ell=31\),

\[
\langle5\rangle\pmod{31}=\{1,5,25\},
\]

whose difference set does not contain \(2\). Therefore one dynamic \(31\)-row can never be active at both anchors, at any precision. This is a universal `CENTER_BLOCKED` family, not a bounded-search inference.

### 7.3 Fixed-resource two-anchor problem as an exact CSP

Once the lower assignments at both anchors are fixed, every desired rigid leaf determines its full class \(b_c\pmod{w_q}\). A two-anchor realization can therefore be decided by a finite exact constraint problem:

1. assign each leaf to a distinct actual prime row;
2. allow one row to serve one leaf at each anchor only when Theorem B passes;
3. allow one-sided use only when the opposite-anchor event can be suppressed;
4. enforce Theorem C for the unique dynamic row when it is used at both anchors;
5. enforce exact ambient support and all lower-coordinate CRT constraints;
6. reject every use of a local zero as an accepted event.

This is a matching/CSP layer on top of the one-anchor inventory theorem. It is not captured by the scalar recurrence \(F_\ell(h)\).

## 8. Exact finite resource audit

### 8.1 Search domain

The standalone reference implementation exhausts

```text
3 <= q <= 10,000,000
q prime
q == 3 (mod 4)
q != 5
```

There are exactly `332398` admitted primes in this domain. For every candidate, the computation:

1. factors \(q-1\) exactly;
2. reduces the exact order \(w_q=\operatorname{ord}_q(5)\);
3. factors \(w_q\);
4. tests \(5^{w_q}\equiv1\pmod{q^2}\).

The bound was selected during exploratory Phase-3 work. The output is an exact finite computation, but no bounded absence is promoted to a universal theorem.

The only admitted base-5 nonregular rows in the entire domain are:

| \(q\) | \(w_q\) | factorization | \(s_q\) | assigned coordinate/depth |
|---:|---:|---|---:|---|
| 20771 | 10385 | \(5\cdot31\cdot67\) | 2 | \((67,1)\) |
| 40487 | 40486 | \(2\cdot31\cdot653\) | 2 | \((653,1)\) |

### 8.2 Support, order-signature, and active-resource counts

Here:

- `support` means \(v_\ell(w_q)=e\), with no largest-coordinate or lifting condition;
- `order signature` adds \(P^+(w_q)=\ell\);
- `active` also adds \(s_q\ge2\).

| \(\ell\) | depth \(e\) | support | order signature | active nonregular resource |
|---:|---:|---:|---:|---:|
| 3 | 1 | 83226 | 2 | 0 |
| 3 | 2 | 27727 | 2 | 0 |
| 3 | 3 | 9249 | 5 | 0 |
| 67 | 1 | 4873 | 645 | 1 |
| 67 | 2 | 72 | 35 | 0 |
| 67 | 3 | 1 | 1 | 0 |

For \(\ell=3\), the complete order-signature lists through depth three are:

```text
e=1: 7, 31
e=2: 19, 5167
e=3: 163, 271, 487, 4159, 31051
```

All are regular, so none supplies an active rigid leaf.

For \(\ell=67\), the regular primes

\[
80803,
\qquad w_{80803}=2\cdot3^2\cdot67^2,
\]

and

\[
6616787,
\qquad w_{6616787}=2\cdot11\cdot67^3,
\]

supply exact ambient depths two and three, respectively. They do not supply active leaves because both have \(s_q=1\).

This separates two notions that the abstract recurrence conflates:

> regular rows can create a deep ambient coordinate, while only nonregular rows can populate its rigid frontier.

## 9. Candidate-level status audit

The machine catalog uses the following primary status order:

```text
DYNAMIC_PARITY_BLOCKED
ORDER_BLOCKED
LIFTING_BLOCKED
SUPPORT_BLOCKED
LOCAL_ZERO_BLOCKED
ARITHMETICALLY_REALIZABLE
```

For `ORDER_BLOCKED`, `LIFTING_BLOCKED`, and `SUPPORT_BLOCKED`, the status is relative to the exact \(q\le10^7\) inventory. Outside the bound, the universal status is `UNKNOWN` unless a separate theorem applies.

### 9.1 Literal \(\ell=3\), \(\beta\le3\) catalog

Every one of the `1431` parameter-labelled candidates is stored individually with its cylinders, depth inventory, filters, status, and SHA-256.

| \(\beta\) | abstract candidates | dynamic parity blocked | order blocked | lifting blocked | explicitly realizable in bound |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 0 | 1 | 1 | 0 |
| 2 | 16 | 4 | 10 | 2 | 0 |
| 3 | 1413 | 324 | 1059 | 30 | 0 |

The parity exclusions are universal because \(s_3=1\). The order/lifting exclusions are bounded statements only.

### 9.2 Compressed \(\ell=67\), \(\beta\le3\) catalog

Since \(s_{67}=1\), only even shell indices are dynamically admissible.

#### \(\beta=1\)

| Status | Count |
|---|---:|
| `ARITHMETICALLY_REALIZABLE` | 1 |
| `LIFTING_BLOCKED` | 1 |

The realized candidate is the dynamic \(S_0+C_1\) pair supplied by \((67,20771)\). The rigid-only candidate needs 67 distinct active depth-one resources; only one occurs in the bounded pool.

#### \(\beta=2\)

The abstract count is

\[
2^{67}+2^{66}+4
=221360928884514619396.
\]

| Status | Count |
|---|---:|
| `ARITHMETICALLY_REALIZABLE` | 2 |
| `DYNAMIC_PARITY_BLOCKED` | \(2^{66}\) |
| `LIFTING_BLOCKED` | 1 |
| `ORDER_BLOCKED` | \(2^{67}+1\) |

The two realized labels are \(J=\{0\}\), centered depth one, with \(m=1\) or \(m=2\). They induce the same unlabelled set family.

#### \(\beta=3\)

Let

\[
F=1+2^{67}=147573952589676412929.
\]

The exact abstract count is

\[
T_3=F^{67}+(2F)^{66}+4F+4F^{66}
\approx3.16039811918\times10^{1351}.
\]

The bounded status partition is:

| Status | Exact count |
|---|---:|
| `ARITHMETICALLY_REALIZABLE` | \(4\) |
| `DYNAMIC_PARITY_BLOCKED` | \(4F^{66}\) |
| `LIFTING_BLOCKED` | \(1\) |
| `ORDER_BLOCKED` | \(F^{67}+(2F)^{66}+4F-5\) |

The four realized parameter labels are:

```text
(m,J,e) = (1,{0},1)
(m,J,e) = (2,{0},1)
(m,J,e) = (3,{0},1)
(m,J,e) = (3,{0,2},1)
```

They form only two unlabelled event systems: the exact partition \(S_0+C_1\), and the overlap-tail cover \((S_0\cup S_2)+C_1\).

Within the bounded resource pool, the explicit fraction is approximately

\[
1.27\times10^{-1351}.
\]

This ratio is a descriptive fact about the bounded pool, not a universal asymptotic statement.

## 10. New actual \(\beta=2,3\) realizations

The existing shared-residue system

\[
r_{67}=2,
\qquad r_{20771}=13471
\]

was extended using regular ambient-support rows.

The two anchor fibers use lower assignments

```text
anchor 0: 2728
anchor 1: 1639
```

inside the relevant lower modulus. These assignments are allowed to differ. The same row residues are used at both anchors.

### 10.1 Prime data

| row prime | order | \(s_q\) | role |
|---:|---:|---:|---|
| 67 | 22 | 1 | dynamic row |
| 20771 | 10385 | 2 | active depth-one rigid row |
| 80803 | 80802 | 1 | regular exact \(67^2\)-support |
| 6616787 | 6616786 | 1 | regular exact \(67^3\)-support |

The support rows use \(K=2,E=\{1\}\) and one shared residue. In the selected finite systems their own coordinate depth is zero, and regularity makes them coarse-inert.

### 10.2 Exact fiber counts at both anchors

| \(\beta\) | support row | \(U\) | step \(M=U/67^\beta\) | \(m,J\) | fiber size | dynamic | rigid | overlap | holes |
|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | — | 228470 | 3410 | \(1,\{0\}\) | 67 | 66 | 1 | 0 | 0 |
| 2 | 80803 | 137767410 | 30690 | \(1,\{0\}\) | 4489 | 4422 | 67 | 0 | 0 |
| 2 | 80803 | 137767410 | 30690 | \(2,\{0\}\) | 4489 | 4422 | 67 | 0 | 0 |
| 3 | 6616787 | 1025601830 | 3410 | \(1,\{0\}\) | 300763 | 296274 | 4489 | 0 | 0 |
| 3 | 6616787 | 1025601830 | 3410 | \(2,\{0\}\) | 300763 | 296274 | 4489 | 0 | 0 |
| 3 | 6616787 | 1025601830 | 3410 | \(3,\{0\}\) | 300763 | 296274 | 4489 | 0 | 0 |
| 3 | 6616787 | 1025601830 | 3410 | \(3,\{0,2\}\) | 300763 | 296340 | 4489 | 66 | 0 |

Every line was enumerated separately at both anchors. Thus the machine output contains fourteen exact anchor-fiber records.

These are stronger positive examples than the original \(\beta=1\) witness: they prove that a shallow active frontier can be embedded into genuinely deeper ambient coordinates by regular order-support rows. They still prove neither uniform lower-coordinate saturation nor a complete two-anchor certificate.

## 11. Common-residue finite audit

For \(q=20771\), \(K=2\), and \(h_0=h_1=1\), exact enumeration gives:

```text
compatible class pairs: 5192
pair-list SHA256:
5b8afc6f24b4ecfa61aa56fdf51db2bc2b81e714bda1c3781d15d7cf1e1fcf4e
known pair (6528,2): present
pair (0,0): absent
```

For dynamic rows, the exact scan

```text
ell prime
ell < 10000
ell == 3 (mod 4)
ell != 5
```

finds precisely the following \(\ell\) for which

\[
2\notin\langle5\rangle-\langle5\rangle\pmod{\ell^{s_\ell}}:
\]

```text
31, 71, 4159, 4999, 6271, 8419, 8971, 9311
```

Each listed prime gives a universal dynamic two-anchor center obstruction. No density or infinitude claim is made from this finite list.

The rigid minimum-valuation criterion was independently exhaustively checked over all residues for:

```text
q=3, K=4
q=5, K=3
```

with no discrepancy.

## 12. Interpretation: why the abstract tree collapses

The abstract recurrence treats every node refinement as free. Arithmetic imposes five independent costs.

### 12.1 Refinement multiplies rare-prime demand

Replacing one depth-\(d\) leaf by its children costs \(\ell\) distinct deeper rigid rows. At \(\ell=67\), one refinement immediately demands 67 rows of the next exact order depth.

### 12.2 Rigid leaves require nonregularity, not merely order divisibility

A prime with the right \(v_\ell(w_q)\) is insufficient. It must also satisfy

\[
q^2\mid5^{w_q}-1.
\]

The \(q\le10^7\) audit has thousands of ambient support rows at \(\ell=67\), but only one active nonregular leaf row.

### 12.3 Dynamic depth has one fixed parity

An abstract catalog may include both parity labels. An actual coordinate has one fixed \(s_\ell\), deleting every dynamic family in the opposite parity class.

### 12.4 Ambient depth and active depth are different resources

Regular rows can increase \(\beta\) without supplying any rigid leaf. This permits shallow frontiers to survive inside deep fibers, but it does not make refined deep frontiers realizable.

### 12.5 Two anchors turn independent leaves into a matching problem

Every row has one shared residue. Prescribed classes must satisfy exact difference and valuation constraints, and one row may be impossible to activate at both anchors or impossible to suppress at only one. Separate anchorwise realizability is therefore strictly weaker than common-residue realizability.

## 13. Status semantics

The requested labels should be read as follows.

| Label | Meaning |
|---|---|
| `ABSTRACT_VALID` | passes the centered prefix-frontier theorem |
| `ARITHMETICALLY_REALIZABLE` | has an explicit actual-prime construction or passes the exact resource theorem against a complete supplied resource set |
| `DYNAMIC_PARITY_BLOCKED` | actual \(s_\ell\)-parity forbids the requested shell set; universal |
| `ORDER_BLOCKED` | the audited finite pool has too few primes with the required order signature; bounded unless independently proved |
| `LIFTING_BLOCKED` | enough order signatures may exist, but too few have \(s_q\ge2\); bounded unless independently proved |
| `SUPPORT_BLOCKED` | no audited row supplies exact ambient \(\beta\); bounded unless independently proved |
| `CENTER_BLOCKED` | a prescribed dynamic center fails the exact shared-residue difference condition |
| `LOCAL_ZERO_BLOCKED` | the construction attempts to count a zero modulo \(p^K\) as accepted; universally invalid |
| `COMMON_RESIDUE_BLOCKED` | no row assignment/matching satisfies the shared-residue valuation constraints |
| `UNKNOWN` | the symbolic theorem reduces the question to arithmetic resources or global compatibility not presently classified |

Within the valid one-anchor centered catalog, `CENTER_BLOCKED` and `LOCAL_ZERO_BLOCKED` never occur: center positions are freely placeable and the centered rigid frontier already covers the unresolved local zero. They reappear when prescribed two-anchor centers or malformed candidates are imposed.

## 14. Scope boundary and next mathematical gate

What is now proved:

```text
abstract centered frontier
+
actual dynamic parity
+
depth-by-depth nonregular leaf inventory
+
exact ambient support
<=>
after selecting those resources/support and letting their orders plus retained
rows induce final U, there exists one compatible final lower fiber (or a
compatible extension of a prescribed partial lower point) on which the
one-anchor frontier is realized exactly.
```

This equivalence does not quantify over an externally frozen `U` that the
selected resources are forbidden to refine.

What remains unresolved:

```text
classification of the global sets R_(ell,d);
uniformity over lower-coordinate assignments;
exact simultaneous two-anchor matching over a whole system;
hereditary closure under contraction;
existence or impossibility of a complete C=1 certificate;
A303656 itself.
```

The strongest next gate is no longer another abstract-tree enumeration. It is an arithmetic/common-residue problem:

> determine whether the two-anchor matching/CSP can be ruled out structurally using the Wieferich leaf inventory, the dynamic difference-set obstruction, and the ascending order DAG, before any larger prime search is authorized.

## 15. Reproduction

From the extracted bundle root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 tools/phase3_reference.py --output-dir results
```

The implementation uses only the Python standard library. It regenerates:

```text
results/resource_scan_B10000000.json
results/l3_beta_le_3_literal_catalog.json
results/l67_beta_le_3_compressed_catalog.json
results/actual_67_beta_1_2_3_embeddings.json
results/common_residue_audit.json
results/summary.json
results/prime_lists/*.txt
```

All bounded-search files include explicit scope warnings. No output changes the repository authority state.
