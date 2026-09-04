# Counterexamples and exact diagnostic examples

## 1. Actual arithmetic saturation without coverage

This is the strongest defect found because it lives inside the admitted odd-row arithmetic at a fixed anchor.

Take anchor `c=1` and the dynamic row

```text
p=67,
K_p=2,
r_p=4,
E_p={1},
w_p=22,
s_p=1.
```

Take the nonregular rigid prime

```text
q=20771,
w_q=10385=155*67,
s_q=2,
K_q=2,
E_q={1}.
```

The coarse period is

```text
U=lcm(22,10385)=228470.
```

Fix all non-`67` coordinates by the lower cylinder

```text
d == 0 (mod 3410),
3410=lcm(22,155).
```

Write `d=3410t`, `t mod 67`.

### Dynamic row

Because `r_p-3=1`, the row tests `1-5^d mod 67^2`.  The order modulo `67^2` is `22*67`.  Thus:

```text
t=0: local zero, unresolved;
t=1,...,66: valuation 1, fatal.
```

The dynamic mass is `66/67`.

### Aligned rigid row

Set the rigid logarithm `b=0` and

```text
r_q = 3 + 5^0 + q = 20775 (mod q^2).
```

The rigid row selects `t=0`, exactly the dynamic center.  The fiber is covered and contracts soundly to

```text
d==0 (mod 22),
d==0 (mod 155),
```

or `d==0 (mod 3410)`.

### Misaligned rigid row

Set `b=155` and

```text
r_q = 3 + 5^155 + q
    = 360322407 (mod q^2).
```

The rigid condition is

```text
d == 155 (mod 10385).
```

On `d=3410t=155*22t`, this becomes

```text
22t == 1 (mod 67),
```

so `t=64`.  This digit is already dynamic-fatal.  The union covers only `66` digits and leaves the local-zero center `t=0` uncovered.

Nevertheless,

```text
D+R = 66/67 + 1/67 = 1.
```

Moreover, after formally deleting the `67` factor, `b=0` and `b=155` both reduce to the same residual congruence modulo `155`.  Therefore a contraction evaluator that records only

```text
x==b_p (mod w_p),
x==b_q (mod w_q/67)
```

but omits the digit-alignment check gives the same child for a sound and an unsound parent.

Machine-readable evidence: `results/aligned_misaligned_pair.json`.

## 2. Smallest density-saturation counterexample in the abstract beta-one grammar

Search domain:

- one odd coordinate of size `n`;
- one complement-of-singleton dynamic event;
- one rigid singleton;
- odd `3<=n<=11`.

The first example is `n=3`:

```text
dynamic center: 0
dynamic fatal digits: {1,2}
rigid digit: 1
budget: 2/3+1/3=1
actual union: {1,2}
uncovered: {0}
```

This proves that union-bound equality is not exact coverage.  Minimality is only within this explicitly enumerated grammar.

## 3. Exact coverage without a beta-one pair

Search grammar:

- at most one complement-of-singleton dynamic event;
- any subset of distinct rigid singletons.

The smallest exact cover with no aligned dynamic/rigid pair occurs at size `3`:

```text
no dynamic event;
rigid digits {0},{1},{2}.
```

Thus actual saturation does not classify itself as a beta-one pair.  This is an abstract normal-form countermodel, not an arithmetic complete certificate.

## 4. Beta greater than one and multiple shells

For a `3^2=9` coordinate, take a dynamic shell

```text
{1,2,4,5,7,8},
```

leaving the unresolved center cylinder

```text
{0,3,6}.
```

Three rigid singleton shells are required to cover that center.  No single rigid slice closes it.  This exact cover demonstrates why a theorem restricted to one beta-one pair does not address `beta_p>1` or multiple-shell saturation.

## 5. Local-zero corruption

Take

```text
p=3, K=2, r=2, E={1}, c=0.
```

On the coarse class `d==0 (mod 2)`, the full-period lifts are:

```text
d=0: local zero;
d=2: valuation 1;
d=4: valuation 1.
```

Correct fail-closed semantics says the coarse class is not fatal.  A deliberately corrupted evaluator that clips zero to `K-1=1` marks the class fatal.  This is the minimal test showing that local zeros cannot be absorbed into an accepted shell.

Machine-readable evidence: `results/local_zero_corruption.json`.

## 6. `K_2=2` constant-boundary obstruction

With

```text
p=11, K=2, r=0, E={1}, c=0,
K_2=2, r_2=1,
```

the odd row contributes no fatal exponent, while the two-adic remainder is unsafe for every exponent.  Direct full-period safe count is zero even though coordinate-only odd hazards vanish.  The boundary must be checked before coordinate induction.

The safe constant case `r_2=0` leaves all `55` exponents safe; `K_2=3,r_2=0` is a genuine period-two hazard and leaves `55` of `110` exponents safe.

## 7. Naive pair-contraction nonconfluence

Use a lower coordinate of size `2` and a top coordinate of size `3`.

- Dynamic event `D` covers top digits `{0,1}` for both lower values.
- `R0` covers the center digit `2` only over lower value `0`.
- `R1` covers the center digit `2` only over lower value `1`.

The original system is complete.  Exact branch-local contraction reuses `D` on both lower fibers and derives residual set `{0,1}`.

A naive global rule that consumes `D` after pairing it with the first rigid row gives:

```text
R0 first -> residual {0};
R1 first -> residual {1}.
```

The two results differ and both lose coverage.  Terminating sound contraction therefore requires branch-local provenance, not global destructive row consumption.

## 8. Residual nonclosure

On a lower coordinate of size `5` and a top coordinate of size `3`, let top events saturate exactly the lower fibers `0` and `2`.  Exact contraction yields the lower macro-predicate

```text
{0,2}.
```

It is neither one rigid singleton nor a beta-one complement in the reference grammar.  It is representable as a finite DNF of point cylinders, but not as one admitted row event.  Semantic closure and admitted-class closure are different claims.

## 9. Fixed-anchor versus simultaneous-anchor conflict

An abstract two-anchor model can have:

```text
anchor 0 terminal residue: 0;
anchor 1 terminal residue: 1.
```

Each fixed-anchor tree closes, but no common terminal residue exists.  This refutes only the inference that two fixed-anchor trees must share one branch.  It does not refute simultaneous completeness, because the two anchor slices may be covered differently.

## Scope of “smallest”

The package proves minimality only for the explicitly enumerated abstract grammars described above.  It does not claim that `67/20771` is the smallest arithmetic misalignment over all admitted primes, and it does not produce a complete arithmetic certificate counterexample.
