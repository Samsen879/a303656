# A303656 C=1 two-anchor common-residue uniformization — Targeted Phase A

## 0. Verdict

```text
TWO-ANCHOR SAME-LOWER DYNAMIC GLUING INCOMPATIBILITY: PROVED
COMMON-FIBER RIGID-FRONTIER TAX: PROVED
COMMON-RESIDUE DEFICIT INVARIANT: PROVED
MINIMAL ACTUAL TWO-ROW JOINT COUNTEREXAMPLE: CONSTRUCTED
UNIVERSAL COMPLETE-CERTIFICATE NO-GO: NOT PROVED

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The main conclusion is not merely that the known `(67,20771)` example happens to use different lower assignments. There is a universal odd-prime mechanism behind that failure:

> With one residue `r_p` shared by anchors `c=0,1`, the same odd row can never have positive `p`-valuation at both anchors at the same exponent. Consequently the dynamic `p`-row is active at at most one anchor on any common lower assignment.

It follows that every simultaneous full `p`-fiber on one common lower assignment must be **rigid-only at at least one anchor**. Since every rigid row assigned to `p` occupies only one first `p`-adic branch, that anchor needs at least `p` active rigid rows. Therefore any system with fewer than `p` such rows has no two-anchor common saturated `p`-fiber.

For the beta-one pair `(p,q)=(67,20771)`, there is only one rigid row. Its common-fiber deficit is therefore at least `66`, independently of accidental CRT choices. A new explicit shared-residue system attains this lower bound exactly while retaining an exact `66+1` pointwise fiber at each anchor on different lower assignments.

This is a genuine global incompatibility principle for **same-lower-coordinate uniformization**. It is not a no-go theorem for arbitrary complete certificates, because a complete simultaneous certificate may use different lower branches for the two anchors, at least `p` rigid rows, different coordinates, or exact derived lower events.

## 1. Authority and scope

The source research and this repository-native integration are bound to:

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 1100eb5ba01d90e5b1001be0bdfa464860fdbb92
main tree: ad1269916bf420c564e34887a96c808033fe538b
```

The following directories were read before the new analysis:

```text
analysis/c1_entangled_coordinate_deficit/
analysis/c1_minimal_saturated_coordinate_inverse/
analysis/c1_contraction_tree_phase_a/
```

The source study was read-only. This integration adds only this analysis
directory on a dedicated audit branch; it does not modify `STATUS.md`, project
authority, a workflow, or `main`.

The exact finite computation is deliberately narrow:

```text
p = 67
q = 20771
K_p = K_q = 2
E_p = E_q = {1}
ord_67(5) = 22
ord_(67^2)(5) = 1474 = 22*67
ord_20771(5) = ord_(20771^2)(5) = 10385 = 155*67
lower modulus = lcm(22,155) = 3410
full period = 3410*67 = 228470
```

No enlarged prime search was performed. Universal statements below are proved symbolically; the finite enumeration is used only for the frozen actual pair.

## 2. Existing boundary reconstructed from the repository

The starting results distinguish three logically different layers:

1. a complete coarse certificate forces an actual fully covered odd-coordinate fiber for one selected anchor;
2. every fixed-anchor irredundant full fiber has the centered prefix-frontier form;
3. arithmetic realization still has separate common-residue, lower-coordinate CRT, lifting, local-zero, and both-anchor compatibility gates.

The existing positive system

```text
r_67 = 2 mod 67^2
r_20771 = 13471 mod 20771^2
```

has one exact `66+1` fiber at each anchor, but on lower assignments

```text
c=0: y=2728 mod 3410
c=1: y=1639 mod 3410.
```

This is pointwise compatibility. It does not give one common lower fiber, a lower-uniform cylinder, a joint admitted contraction, or a complete certificate.

The existing semantic contraction theorem also acts anchorwise. Two fixed-anchor trees may share original row parameters while having different centers, witnesses, and terminal residuals. A common tree requires a stronger joint decomposition property.

## 3. Formal setup

For an odd admitted row prime `p`, define the local quantity

```text
V_(p,c)(d) = r_p - 3^c - 5^d.
```

At precision `p^K`, a row is fatal only when the clipped valuation is a positive accepted odd value. A local zero modulo `p^K` is unresolved and is not accepted.

Fix an odd coordinate `p`, depth `beta=v_p(U)`, and a common assignment `y` of all lower rational-prime coordinates. Let

```text
F_p = Z / p^beta Z
```

be the top fiber. After lower coordinates are fixed:

- the dynamic row `p`, when active, is a union of accepted `p`-adic shells around one unresolved center;
- a rigid row `q` assigned to `p=P+(ord_q(5))` is either inactive or one cylinder
  `C_e(t)` with `e=v_p(ord_q(5))>=1`;
- every such rigid cylinder is contained in exactly one first branch `t mod p`.

The theorem concerns a genuine rank-`p` saturation witness: lower-ranked events have already been avoided and are not being counted as full-fiber coverage.

## 4. The universal anchor-exclusion invariant

### Theorem 1 — odd-row anchor exclusion

For every odd prime `p`, every shared residue `r_p`, and every exponent `d`, the row cannot have positive `p`-valuation at both anchors:

```text
p | V_(p,0)(d)  and  p | V_(p,1)(d)
```

is impossible.

Equivalently, if `F_(p,c)` denotes the set of exponents at which row `p` is fatal at anchor `c`, then

```text
F_(p,0) intersect F_(p,1) = empty.
```

#### Proof

The two local quantities differ by a constant:

```text
V_(p,0)(d) - V_(p,1)(d)
= (r_p-1-5^d) - (r_p-3-5^d)
= 2.
```

If `p` divided both quantities, then `p|2`, contradicting that `p` is odd. Fatality implies positive divisibility, so simultaneous fatality is impossible. The argument remains valid if one side is a local zero: a local zero is still divisible by `p`, although fail-closed semantics prevents counting it as fatal. QED.

### Corollary 1 — dynamic same-lower exclusion

Let `A_(p,c)(y)` be the indicator that the dynamic row `p` is active after fixing the common lower assignment `y`. Then

```text
A_(p,0)(y) + A_(p,1)(y) <= 1.
```

Indeed, dynamic activity requires the same lower exponent class to satisfy divisibility modulo `p`; Theorem 1 forbids that condition at both anchors.

This is the first decisive upgrade over the earlier pointwise examples. It is independent of `(67,20771)`, independent of lifting depth, and independent of any density estimate.

## 5. Two-anchor common-fiber classification

### Theorem 2 — dynamic/rigid dichotomy for a common fiber

Fix one odd coordinate `p` and one common lower assignment `y`. Suppose the rank-`p` events fully cover `F_p` at both anchors. Then exactly one of the following structural types occurs:

```text
RR: the dynamic row is inactive at both anchors;
DR: it is active at anchor 0 and inactive at anchor 1;
RD: it is inactive at anchor 0 and active at anchor 1.
```

The type `DD` is impossible. At every dynamic-inactive anchor, the full fiber is covered entirely by rigid cylinders. After taking an irredundant subcover, these cylinders form a complete `p`-ary prefix frontier.

#### Proof

The absence of `DD` is Corollary 1. If the dynamic row is inactive at anchor `c`, the rank-`p` cover equation reduces to

```text
F_p = union over active rigid q of C_(q,c)(y).
```

The one-anchor centered prefix-frontier theorem, specialized to no essential dynamic event, gives a rigid-only complete frontier. QED.

This theorem is an exact set-level classification. It does not replace coverage by the rational budget `D+R>=1`.

## 6. The rigid-frontier tax and deficit invariant

For an anchor `c` and lower assignment `y`, let

```text
B_(p,c)(y)
```

be the set of first `p`-adic digits hit by active rigid cylinders. Since every rigid cylinder assigned to `p` has depth at least one, one active rigid row contributes at most one element to `B_(p,c)(y)`.

At least one anchor is dynamic-inactive. Define the exact first-branch deficit

```text
delta_p(y)
  = max over c with A_(p,c)(y)=0 of
      [p - |B_(p,c)(y)|].
```

### Theorem 3 — common-residue first-branch deficit

If `delta_p(y)>0`, the two anchors cannot both have a full rank-`p` fiber at `y`.

In particular, if the dynamic-inactive anchor has `N` active rigid rows, then

```text
delta_p(y) >= p-N.
```

Hence simultaneous common-fiber coverage requires at least `p` active rigid rows.

#### Proof

A rigid-only cover must meet every first branch of `F_p`. If a first digit is absent from `B_(p,c)(y)`, no deeper cylinder can cover any point in that branch. Thus `B_(p,c)(y)` must contain all `p` digits. Since each row supplies at most one first digit, at least `p` active rows are necessary. QED.

### Equality case

If exactly `p` rigid rows cover a dynamic-inactive anchor, every row must be a depth-one cylinder and the `p` first digits must occur exactly once. Any deeper cylinder would leave part of its first branch uncovered, and any repeated first digit would omit another branch.

Thus the lower bound is structurally sharp in the abstract cylinder grammar. It is not automatically arithmetically realizable: the `p` rows must be distinct actual nonregular primes with compatible orders, shared residues, lower CRT conditions, lifting depths, and local-zero behavior.

### Beta-one specialization

At `beta=1`:

- an active dynamic row covers `p-1` digits and leaves one unresolved center;
- an inactive dynamic row covers zero digits;
- every rigid row covers at most one digit.

With one dynamic row and one rigid row, one anchor is dynamic-inactive and therefore has at least

```text
p-1
```

uncovered digits. For `p=67`, this is an unconditional `66`-digit joint deficit.

## 7. A global Hall-type anchor-capacity invariant

The preceding theorem is local to one coordinate fiber. There is also a period-level necessary condition.

Let `Omega=Z/LZ` be the exact exponent period. Let `T_c(d)` be the indicator that a valid two-adic event already covers demand `(c,d)`. For each odd row `p`, let `F_(p,c)` be its fatal exponent set. By Theorem 1, for each fixed `p` the two sets have disjoint exponent projections.

For any subset `A subseteq Omega`, define

```text
Def(A)
 = sum_(d in A) [2-T_0(d)-T_1(d)]
   - sum_(odd rows p) |A intersect (F_(p,0) union F_(p,1))|.
```

### Theorem 4 — Hall-type necessary condition

Every complete simultaneous certificate satisfies

```text
Def(A) <= 0
```

for every `A subseteq Omega`.

#### Proof

After removing demands already covered by the two-adic event, the first term counts the remaining anchor-exponent demand vertices. One odd row can cover at most one of `(0,d)` and `(1,d)` for each `d`, by Theorem 1. The second term is therefore an upper bound on total odd-row capacity over `A`, even before correcting for overlaps between different rows. A positive deficit leaves at least one demand uncovered. QED.

This is a necessary condition, not a sufficient set-cover test. Different odd rows can overlap heavily, so `Def(A)<=0` does not certify completeness.

## 8. Finite compatibility system / hypergraph model

For fixed `p`, `beta`, and lower assignment `y`, form a two-layer demand hypergraph.

### Demand vertices

```text
(c,z),  c in {0,1},  z in Z/p^beta Z.
```

### Dynamic hyperedge

At anchor `c`, the dynamic row contributes either:

- the accepted-shell union around its center, or
- the empty set when its lower divisibility condition is inactive.

The two dynamic hyperedges cannot both be active at the same `y`.

### Rigid paired hyperedge

Each rigid row `q` contributes a paired object

```text
(C_(q,0)(y), C_(q,1)(y)),
```

where either component may be empty. Both components are constrained by one shared `r_q`; they are not independently selectable.

### Constraints

A valid assignment must simultaneously satisfy:

1. one shared residue for each row;
2. exact order and lifting depth;
3. accepted positive odd valuations only;
4. common lower-coordinate CRT compatibility;
5. exact dynamic-center / rigid-cylinder positions;
6. local zeros remain unresolved in their own row;
7. both anchor layers are set-theoretically covered.

At `beta=1`, a rigid row that is active at both anchors is an edge between one digit on the anchor-0 side and one digit on the anchor-1 side. If one anchor is dynamic-inactive, the projection of all rigid edges onto that side must cover all `p` digit vertices. With exactly `p` rows this projection is a bijection. If both anchors are rigid-only and every row is active on both sides, an exact `p`-row cover is a perfect matching between the two digit sets.

At larger `beta`, first-digit coverage is only the first Hall gate. Inside every unaccepted first branch, the rigid cylinders must recursively form complete prefix frontiers.

This model separates three different questions that were previously easy to conflate:

```text
rowwise common-residue compatibility;
common lower-assignment compatibility;
actual two-layer fiber coverage.
```

## 9. Exact computation: two independently organized checks

The reference program `tools/reference_two_anchor.py` imports no repository code and uses only Python's standard library.

### Method A — symbolic logarithm / constraint propagation

- solve `5^a0-5^a1=2 mod 67^2` for shared dynamic residues;
- solve `5^b0-5^b1=2 mod 20771` for shared rigid residues;
- impose center alignment `a_c=b_c mod 67` at each anchor;
- solve the lower CRT conditions modulo `22` and `155`;
- count valid full lifts of `r_20771 mod 20771^2`, excluding local zeros.

### Method B — direct residue and fiber enumeration

- enumerate every `r_67 mod 67^2` directly and recover both center logs;
- enumerate every `r_20771 mod 20771` directly and recover both rigid logs;
- independently run a nested join rather than the signature hash-join;
- for selected systems, enumerate all `3410` lower assignments, both anchors, and all `67` top digits;
- separately enumerate the full `228470` exponent period.

The methods agree exactly. They are algorithmically independent formulations inside one standalone implementation; they are not claimed to be independent software stacks.

## 10. Exhaustive `(67,20771)` classification

### 10.1 Shared dynamic residues

There are exactly

```text
603
```

residues `r_67 mod 67^2` for which both anchors possess a dynamic center on some lower assignment.

They reduce to nine mod-`67` compatibility classes:

| `r_67 mod 67` | anchor-0 log mod 22 | anchor-1 log mod 22 |
|---:|---:|---:|
| 0 | 11 | 18 |
| 2 | 0 | 11 |
| 4 | 7 | 0 |
| 6 | 1 | 7 |
| 25 | 16 | 4 |
| 28 | 21 | 2 |
| 43 | 13 | 10 |
| 46 | 15 | 5 |
| 65 | 18 | 12 |

In every class the two lower logs differ. Exact enumeration gives

```text
same lower class mod 22: 0 of 603.
```

This finite result is a replay of the universal anchor-exclusion theorem, not its proof.

### 10.2 Shared rigid residues

There are exactly

```text
5192
```

compatible ordered rigid class pairs `(b_0,b_1) mod 10385` satisfying

```text
5^b0 - 5^b1 = 2 mod 20771.
```

Among them,

```text
33
```

have `b_0=b_1 mod 155`, so a rigid row can genuinely be active at both anchors on one common lower `q/67` assignment. Thus the obstruction is not that shared residues universally prevent simultaneous rigid activity.

For all `5192` pairs, the two exact local-zero lifts modulo `20771^2` are distinct. Hence every class pair has

```text
20771-2 = 20769
```

valid full shared residues at which both anchor valuations are exactly one rather than local zeros.

### 10.3 Exact pointwise `66+1` fibers at both anchors

After imposing dynamic/rigid center alignment at both anchors, there are exactly

```text
693
```

compatible dynamic-rigid class combinations. They yield

```text
692 distinct ordered pairs (y_0,y_1) mod 3410.
```

After the valid `q^2` lifts are included, the number of shared residue systems

```text
(r_67 mod 67^2, r_20771 mod 20771^2)
```

that realize one exact `66+1` fiber at each anchor pointwise is

```text
693 * 20769 = 14,392,917.
```

Yet the exhaustive common-lower count is

```text
0.
```

Thus the phenomenon is not “there are too few pointwise compatible residues.” There are more than fourteen million such systems in the frozen modulus space, and none upgrades to one common lower beta-one fiber.

## 11. Direct replay of the repository example

For

```text
r_67 = 2
r_20771 = 13471,
```

direct enumeration of all lower assignments gives

```text
Sat_0 = {2728}
Sat_1 = {1639}
Sat_0 intersect Sat_1 = empty.
```

Both selected fibers are exact `66+1` partitions with no overlap and a fail-closed dynamic local zero filled by the rigid row.

Over one common lower assignment, the minimum total number of holes across the two anchor fibers is `67`, attained at four lower assignments. The system is therefore classified as:

```text
pointwise: yes
individual fiberwise exact: yes
same-lower simultaneous: no
lower-uniform: no
anchor-uniform joint contraction: no
complete two-anchor certificate: no
```

## 12. A sharp minimal actual joint counterexample

The repository example contains more incompatibility than is needed: its rigid lower classes also differ. To isolate the universal dynamic obstruction, use the same actual primes and set

```text
r_67 = 0 mod 4489
r_20771 = 4494 mod 431434441.
```

The exact logarithm data are:

| quantity | anchor 0 | anchor 1 |
|---|---:|---:|
| dynamic center mod `1474` | 737 | 788 |
| dynamic lower class mod `22` | 11 | 18 |
| rigid class mod `10385` | 7236 | 9096 |
| rigid lower class mod `155` | 106 | 106 |
| aligned top digit mod `67` | 0 | 51 |

The rigid lower condition is **identical** at both anchors. Pointwise CRT gives

```text
c=0: y=2431 mod 3410
c=1: y=106 mod 3410.
```

Direct fiber enumeration gives:

| common lower `y` | anchor | dynamic cells | rigid cells | holes | result |
|---:|---:|---:|---:|---:|:---|
| 2431 | 0 | 66 | 1 | 0 | exact `66+1` |
| 2431 | 1 | 0 | 1 | 66 | fails sharply |
| 106 | 0 | 0 | 1 | 66 | fails sharply |
| 106 | 1 | 66 | 1 | 0 | exact `66+1` |

Across all `3410` common lower assignments,

```text
minimum total joint holes = 66 = 67-1.
```

This attains the rigid-frontier lower bound. The failure can no longer be attributed to a rigid CRT mismatch: the rigid row is simultaneously active under `y=106 mod 155`; the only missing resource is the other anchor's dynamic shell, which shared-residue anchor exclusion forbids.

### Minimality statement

Within the fixed beta-one grammar consisting of one dynamic row and one rigid row:

- two rows are the minimum needed for even one exact pointwise full fiber;
- each anchor separately has such a pointwise fiber;
- requiring one common lower assignment makes the system unsatisfiable;
- deleting either anchor coverage requirement restores satisfiability.

Thus this is a minimal unsatisfiable two-anchor subsystem in that explicit grammar. No claim is made that `(67,20771)` is the smallest possible actual prime pair over all unsearched primes.

## 13. Exact evidence ladder

The terms are used as follows.

### Pointwise

```text
for each anchor c, there exists some lower assignment y_c
with one full p-fiber.
```

The repository example and the sharp example both pass.

### Fiberwise

The named fiber is checked by direct set enumeration, not merely by mass. Both examples pass individually at their own `y_c`.

### Lower-uniform

At minimum, there is one common lower assignment `y` at which both fibers are full; a stronger version asks for a nontrivial lower cylinder. Both examples fail already at the point level.

### Anchor-uniform

One common admitted contraction branch, with shared row parameters and compatible residuals, works for both anchors. Failure of common point-level saturation rules this out for the two-row mechanism.

### Full certificate

Every exponent class is covered at both anchors. Full-period enumeration rejects both systems by a very large margin. No complete certificate is produced.

## 14. Is the obstruction accidental or global?

### What is global

The following principle is unconditional for the admitted odd rows:

```text
shared residue + same exponent + two anchors
=> one odd row cannot be p-divisible at both anchors.
```

Therefore direct dynamic-to-dynamic gluing on one common lower assignment is universally impossible, and every common saturated odd fiber pays a rigid-only frontier cost of at least `p` active rows at one anchor.

The `(67,20771)` one-rigid-row failure is consequently structural, not an accidental mismatch.

### What remains only arithmetic / system-dependent

The theorem does not rule out:

- a rigid-only frontier supplied by at least `p` compatible actual rows;
- different lower branches for `c=0` and `c=1`;
- saturation at different odd coordinates;
- one anchor being covered by lower-ranked events before the current coordinate;
- exact semantic macro-events produced by prior contraction;
- a terminal interaction with a valid two-adic event.

The abstract `p`-row lower bound is sharp, so no contradiction follows from logic alone once enough rigid resources are permitted.

Within the repository's frozen search through `q<=500000`, `q=20771` is the only found nonregular row whose largest order prime is the admitted dynamic coordinate `67`. Hence the searched resource count is `1<67`, and common `67`-fiber gluing is excluded inside that frozen panel. This is bounded evidence, not a theorem about all primes.

## 15. Strongest conditional no-go and exact missing hypothesis

### Conditional theorem

Assume a class of simultaneous certificates satisfies both hypotheses:

**H1 — joint-witness hypothesis.** Every complete simultaneous certificate exposes some odd coordinate `p` and one lower assignment `y`, after lower-ranked events have been avoided, such that the rank-`p` events must cover the full `p`-fiber at both anchors simultaneously.

**H2 — rigid-resource deficit.** At that `(p,y)`, fewer than `p` rigid rows assigned to `p` are active on at least one dynamic-inactive anchor.

Then no complete simultaneous certificate exists in that class.

#### Proof

By Theorem 1, at least one anchor is dynamic-inactive at `(p,y)`. H2 gives fewer than `p` active rigid rows there. Theorem 3 leaves a first branch uncovered, contradicting H1. QED.

### Precise missing bridge

The repository currently proves only:

```text
complete simultaneous certificate
=> for one selected anchor,
   some odd coordinate and some lower assignment has a full fiber.
```

It does not prove that the other anchor must saturate the same coordinate on the same lower assignment. That is exactly H1. Separate fixed-anchor contraction trees may legitimately take different branches, as the pointwise examples demonstrate.

Even if H1 were proved, a full no-go would still require a universal arithmetic version of H2: an upper bound below `p` on simultaneously compatible active rigid resources. The current bounded prime scan supplies such a bound only in its frozen finite domain.

A common admitted contraction tree would additionally require **joint hereditary exact shell decomposability**: the simultaneous saturation sets must admit a common lower-cylinder decomposition, every branch must retain exact shared-residue provenance, and every child must remain in the admitted residual grammar.

## 16. Final answer to the phase question

The two-anchor obstruction has two layers:

1. **Not accidental:** same-lower dynamic gluing fails by the universal constant-difference identity `2`; every common saturated odd fiber needs a rigid-only anchor and at least `p` active rigid rows.
2. **Not yet a universal complete-certificate no-go:** arbitrary systems may separate anchor branches or supply large rigid frontiers. The existing one-anchor witness theorem does not force a simultaneous common lower fiber.

The strongest unconditional result of this phase is therefore the same-lower dynamic-gluing incompatibility together with the common-fiber rigid-frontier-tax theorem. The strongest conditional global result is the H1+H2 no-go above. The exact missing hypothesis is not “more pointwise compatible residues”; the computation shows millions of those. It is a theorem forcing a **joint witness on one common lower assignment**, followed by a universal arithmetic shortage of the `p` rigid rows that such a witness requires.

## 17. Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 tools/reference_two_anchor.py --output /tmp/a303656-phase2-results.json
python3 -m unittest discover -s tests -v
python3 tools/finalize_integration.py --verify
```

The script fails closed on every frozen count and writes a canonical result hash. `SHA256SUMS.txt` protects the report, implementation, and result file.
