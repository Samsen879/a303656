# Final report — minimal saturated odd-coordinate inverse classification

## 1. Authority binding

Verified before research:

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 29fee0317b268d2b2747f9564efc445fdd6da7f9
main tree: 0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55
```

The bound `STATUS.md` states:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

No GitHub state was modified.

## 2. Required-source audit

The required files were read at the bound commit.  Their blob SHAs are frozen in `results/source_binding.json`.

The starting theorem is only

```text
complete certificate
=> at a suitable anchor c,
   D_(l,c)+R_(l,c)>=1 for some odd l.
```

It is a necessary rational budget statement, not a coverage criterion.  The existing beta-one contraction result applies only after exact center alignment on a fixed lower assignment.

## 3. Formal definitions

For fixed odd coordinate `l`, depth `beta=v_l(U)`, anchor `c`, and lower-coordinate assignment:

- the dynamic row is a union of accepted shells `S_j` of mass `(l-1)/l^(j+1)`;
- accepted `j` lie in one parity class because valuations are positive odd;
- the unresolved center is never dynamically accepted;
- each active rigid row assigned to `l` is one cylinder of depth `e=v_l(w_q)` and mass `l^-e`.

Atom-minimal rational budgets, row-minimal fiber covers, and arithmetic realizability are treated separately.

## 4. Rational classification

### New theorem R1

For the genuine distinct-dynamic-depth mass system, every atom-minimal budget with total at least one has total exactly one.  It is classified by

```text
h_0=1,
h_e=l h_(e-1)-[(l-1)epsilon_e+n_e],
h_e>=0,
h_B=0.
```

Strict excess is impossible at atom level.  Repeated rigid depths are allowed.  Repeated dynamic depth is outside the model and gives an immediate strict-excess counterexample.

### New theorem R2

With atom count `A` and largest denominator depth `B`,

```text
B<=A-1.
```

The sharper expanded-leaf bound is

```text
B<=floor((M-1)/(l-1)),
M=sum n_e+(l-1)sum epsilon_e.
```

No absolute depth bound exists without an atom-count bound.

### New theorem R3

One dynamic row and one rigid row have exact total mass one iff the dynamic row contains every shell from depth one through the rigid depth.  Odd-valuation parity therefore makes the beta-one pair the unique admitted two-row equality pattern.

Row-minimal two-row strict-excess covers still exist through deeper overlap tails bundled in the same dynamic row.

## 5. Exact-cover classification

### New theorem F1 — centered prefix-frontier inverse theorem

Every fiberwise irredundant full cover has:

1. exactly one rigid cylinder containing a fixed lift of the unresolved center;
2. no other rigid cylinder intersecting it;
3. complete prefix-code frontiers in every unaccepted side branch before its depth;
4. an essential dynamic row iff at least one accepted shell lies before that depth.

Conversely every such construction is an irredundant full cover.

The only overlap is the dynamic accepted tail inside the centered cylinder.  Multiplicity is at most two, and

```text
budget = 1 + accepted-tail mass.
```

### Beta one

- beta-one dynamic pair, when `s_l` is odd;
- rigid-only partition into all `l` digits.

### Beta two

- rigid-only labelled count `2^l`;
- `J={0}`: exactly two templates;
- `J={1}`: labelled count `2^(l-1)`;
- no overlap, by parity.

### Arbitrary beta

The exact recurrence is

```text
F_l(0)=1,
F_l(h)=1+F_l(h-1)^l.
```

For fixed `beta,m,J,e`, the labelled template count is the product of the relevant side-branch frontier counts.  Fixed depth is finite and effective.  A uniform finite literal list is false.

## 6. Complete certificate to template occurrence

### New theorem G1 — greedy actual-fiber witness

At the anchor supplied by the existing exact two-adic lemma, if the finite admitted system is complete, increasing-coordinate greedy avoidance must stop at an odd coordinate whose assigned dynamic and rigid events actually cover the full fiber for the lower assignment already chosen.

Otherwise one chooses an uncovered digit at every coordinate; later coordinates do not alter earlier events; reverse CRT then gives a full safe exponent, contradicting completeness.

Taking an irredundant subcover and applying F1 yields:

```text
complete certificate
=> actual odd fiber cover
=> one parameterized centered prefix-frontier template occurs.
```

This is the requested inverse theorem.  It is strictly stronger than `D+R>=1` and does not treat density as coverage.

## 7. Arithmetic realizability

An active rigid cylinder needs a nonregular prime `q` with

```text
q==3 mod 4,
s_q>=2,
P+(ord_q(5))=l,
v_l(ord_q(5))=e.
```

A template requiring `N_e` depth-`e` rigid cylinders needs `N_e` distinct such primes.  Ambient `beta` may require additional inactive support rows.

A dynamic coordinate needs `l==3 mod 4`, `l!=5`, adequate `K_l-s_l`, parity-compatible accepted valuations, and order support for `beta_l`.

Both anchors must share each row residue.  The exact common-residue congruence is an independent gate.

The actual pair `(67,20771)` realizes the beta-one exact partition at anchor one after fixing `d==0 mod 3410`: `66+1`, no overlap, no holes.  The local zero of the 67-row fails closed and is covered by the 20771-row.

A distinct shared-residue example, `r_67=2` and `r_20771=13471`, realizes
exact `66+1` fibers at both anchors on lower assignments `2728 mod 3410` and
`1639 mod 3410`.  This is positive pointwise compatibility only; it does not
establish uniform lower-coordinate saturation or a complete certificate.

## 8. Adversarial results

The package contains exact counterexamples to:

- `budget>=1 => coverage`;
- `strict budget excess => coverage`;
- `exact cover => beta-one pair`;
- `exact dynamic cover => depth-one centered rigid row`;
- `rigid mass one => rigid union coverage`;
- `row-minimal => exact partition`;
- `one lower assignment => all lower assignments`;
- `abstract template => arithmetic realization`;
- `order-coordinate divisibility => admitted rigid row` (the `q=7` boundary);
- `separate anchor realization => common-residue realization`;
- mixing the constant `K_2=2` boundary into odd-coordinate induction;
- a depth-independent finite literal template list.

All counterexample records have SHA-256 identifiers in `results/counterexamples.json`.

For the anchor-compatibility item, the exact pair `(67,20771)` gives a prescribed class-zero beta-one `66+1` partition separately at each anchor, while the necessary row residues disagree modulo both primes.  The obstruction is to that prescribed pair, not to all alternate class choices or larger systems.

## 9. Exact computation bounds

### Rational

```text
l in {3,5,7}
max denominator depth = 5
max atom count = 12
bounded independent brute force: l=3, depth<=3, rigid count<=4 per depth
```

### Fibers

```text
complete parameter-labelled generation: l=3,beta<=3; l=5,beta<=2
independent subset brute force: l=3,beta=2
```

Generated parameter-labelled template counts (the label retains `m` and `s_l` parity, so these are not counts of distinct unlabelled set systems):

```text
(l,beta)=(3,1): 2
(3,2): 16
(3,3): 1413
(5,1): 2
(5,2): 52
```

### Arithmetic

```text
all q prime, q==3 mod4, q!=5, q<=500000
searched primes = 20806
nonregular hits = 20771, 40487
```

The known prime `1645333507` is checked separately.  Bounded absence is not a theorem.

## 10. Tests and hashes

The deterministic suite contains exact-fraction, beta-one, beta-two, bounded brute-force, arithmetic, common-residue, independent `K_2=2`, local-zero, deterministic-ZIP, text-hygiene, and corruption fail-closed tests.  The sealed run executes **31 tests**, all passing.  Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m unittest discover -s tests -p 'test_*.py'
```

All generated JSON is produced by `tools/reproduce.py`.  Internal file hashes are in `manifest.json` and `SHA256SUMS.txt`.  The principal machine-output hashes are:

```text
rational catalog:
11747525b9f5d2ac7a85dd8b345757484e70880b0d51596ca8bb77a338823b09

fiber catalog:
b24cc723e8d58e2d0abb64cb5862db804c6d6f747e31493dba5c906e904a0f35

arithmetic audit:
00e7c84aeff72abebc1a45bef1adb57e3b52c93ca23fde34bdc25a59fef05742
```

The outer ZIP hash is intentionally recorded beside the archive rather than inside the hashed payload.

## 11. Repository-integration recommendation

Recommend a theorem-only integration under a new analysis directory, after an independent repository-native review of:

1. the greedy actual-fiber witness lemma;
2. the distinction between fiberwise irredundant subcover and global deletion of a prime row;
3. the centered-lift convention when `m<beta`;
4. the prefix-frontier count and beta-two labelled classification;
5. the common-residue scope language.

Do not promote an active route.  Do not call the parameterized template a complete certificate.  Preserve all current authority state.

## 12. Final verdict

```text
PROMOTABLE INVERSE THEOREM
```

Reason: the package proves a general actual-fiber witness from completeness and an exact arbitrary-depth parameterized classification of every resulting irredundant fiber cover.  The result is theorem-level and not merely bounded enumeration.  Arithmetic assembly and global certificate existence remain unresolved.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```
