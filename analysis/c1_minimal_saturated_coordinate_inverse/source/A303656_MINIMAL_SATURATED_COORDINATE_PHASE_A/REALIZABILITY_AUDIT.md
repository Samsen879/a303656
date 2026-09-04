# Arithmetic realizability audit

## 1. Separation from the abstract cover theorem

The centered prefix-frontier theorem classifies exact cylinder events.  It does not assert that the required cylinder multiset is supplied by actual primes.  Arithmetic realizability imposes independent resource and compatibility conditions.

## 2. Dynamic row conditions

A dynamic event at coordinate `l` requires an admitted row with prime

```text
l == 3 (mod 4), l != 5.
```

Let

```text
w_l=ord_l(5),
s_l=v_l(5^w_l-1).
```

To expose `m` dynamic digits, one needs

```text
K_l>=s_l+m,
a_l=K_l-s_l>=m,
beta_l>=m
```

when the intended template uses all `m` digits.  Desired shell `j` can be accepted only if

```text
s_l+j is positive odd and s_l+j<K_l.
```

For one fixed anchor and one active coarse logarithm, varying `r_l mod l^K_l` can place the dynamic center at any desired `l`-adic digit string.  The zero at the exact center remains unresolved and cannot be counted as accepted.

An immediate universal obstruction is that an abstract template using a dynamic row at `l=5`, or at any `l==1 (mod 4)`, is not realizable in the formal class.

## 3. Rigid row resource lemma

Let `q` be a rigid row assigned to coordinate

```text
l=P^+(w_q), w_q=ord_q(5), e=v_l(w_q).
```

A positive accepted rigid valuation must satisfy

```text
0<h<s_q,
h odd,
s_q=v_q(5^w_q-1).
```

Therefore every rigid fatal cylinder requires a base-5 nonregular prime

```text
q == 3 (mod 4), q != 5, s_q>=2.
```

Order support alone is insufficient.  Although `ord_7(5)=6` contains the
coordinate factor `3`, its lifting depth is `s_7=1`, so no positive odd
`h<s_7` exists and `q=7` cannot supply an admitted rigid fatal cylinder.

Conversely, for one anchor, any full exponent class `b mod w_q` and any odd `h<s_q` can be made rigid fatal by choosing

```text
r_q == 3^c + 5^b(1+q^h u) mod q^K,
q not dividing u,
K>h.
```

Hence a template requiring `N_e` active rigid cylinders at coordinate `l` and depth `e` needs at least `N_e` distinct primes in

```text
Q_(l,e)={q:
 q prime,
 q==3 mod 4,
 q!=5,
 s_q>=2,
 P^+(ord_q(5))=l,
 v_l(ord_q(5))=e}.
```

One row supplies at most one rigid cylinder for one anchor and one lower-coordinate assignment.

## 4. Ambient beta support

The coordinate depth is

```text
beta_l=max_q v_l(w_q).
```

The dynamic row `l` does not support its own `l` coordinate because `l` does not divide `w_l|l-1`.  If no covering rigid row has order depth `beta_l`, the global system must contain an additional admitted support row with `v_l(w_q)>=beta_l`.  That support row may be inactive in the witness fiber.

Thus fiberwise deletion of a redundant event cannot automatically be interpreted as deleting the prime row from the global system.

## 5. Common-residue compatibility

Each prime row has one residue `r_q` shared by both anchors.  Suppose a rigid row is required at classes `b_0,b_1` and fixed positive valuations `h_0,h_1`.  Exact compatibility is the existence of units `u_0,u_1` such that

```text
3^0+5^b0(1+q^h0 u_0)
==
3^1+5^b1(1+q^h1 u_1)
(mod q^K).
```

This must be checked at full precision.  Anchorwise realizability does not imply common realizability.

For `K=2` and `h_0=h_1=1`, reduction modulo `q` gives

```text
5^b0-5^b1==2 mod q.
```

For `q>3`, this condition is also sufficient to choose nonzero first-lift coefficients on both sides.

The exact `q=20771` enumeration gives:

```text
w_q=10385,
compatible full-class pairs=5192,
SHA256=5b8afc6f24b4ecfa61aa56fdf51db2bc2b81e714bda1c3781d15d7cf1e1fcf4e.
```

The known common residue

```text
r=96315155
```

realizes classes `(6528,2)`.  The prescribed pair `(0,0)` is separately realizable at each anchor but not by one common residue, since modulo `q` anchor zero requires `r==2` while anchor one requires `r==4`.

This blocks that prescribed one-row assignment only; it does not exclude a larger system using additional rows.

The checker also completes the surrounding beta-one fibers with the actual dynamic partner `l=67` and `d=3410t`:

```text
c=0: (r_67,r_q)=(2,q+2),
c=1: (r_67,r_q)=(4,q+4).
```

Both are exact `66+1` partitions.  They cannot be the two anchors of one common-residue system because both row residues disagree modulo their respective primes.  This remains a prescribed class-zero incompatibility, not a universal two-anchor no-go.

There is also a positive pointwise compatibility example.  The single shared
system `r_67=2`, `r_20771=13471` gives an exact `66+1` partition at anchor zero
on lower assignment `2728 mod 3410`, and at anchor one on lower assignment
`1639 mod 3410`.  The dynamic center is a fail-closed local zero in each fiber
and the rigid row fills it.  Because the lower assignments differ, this proves
neither uniform lower-coordinate saturation nor a complete certificate.

## 6. Both-anchor template compatibility

A two-anchor template must pass all of the following simultaneously:

1. every row has one shared `r_p`;
2. dynamic centers and rigid classes satisfy the common-residue congruence;
3. the same order data determine `U`, `beta`, and all lower-coordinate dependencies;
4. a lower-coordinate assignment used for one row is compatible with the other active rows;
5. the selected two-adic anchor condition is respected;
6. every local zero remains unresolved.

The inverse theorem is conditional on the actual witness fiber produced by a complete system, so these constraints are automatically satisfied there.  They are not automatic when constructing a system from an abstract template.

## 7. Local-zero fail-closed condition

At precision `p^K`, the exact zero has clipped valuation `None`, not `K` and not an accepted odd valuation.  Any template that asks the dynamic row to cover its own center is invalid.

The exact actual-prime replay uses

```text
l=67, q=20771, c=1,
r_67=4, r_20771=20775.
```

After fixing the coordinate-11 center inside the chain, take

```text
d==0 mod 3410.
```

Across the 67-cell coordinate fiber:

```text
dynamic 67-row count = 66,
rigid 20771-row count = 1,
overlap = 0,
holes = 0.
```

At `d=0`, the 67-row local value is zero and fails closed; the 20771-row has valuation one and fills the center.

## 8. Frozen actual-prime search

The search domain was frozen before execution; it was not enlarged after observing the output:

```text
q_max = 500000,
at most 249999 odd integer candidates before primality filtering,
sieve storage = 500001 bytes plus interpreter overhead,
no adaptive extension of the bound.
```

The reference search exhausts

```text
3<=q<=500000,
q prime,
q==3 mod 4,
q!=5.
```

The complete searched list contains 20,806 primes and is stored in `results/searched_primes.txt` with its SHA-256 in `results/arithmetic_realizability.json`.

For every candidate, the checker factors `q-1`, computes `ord_q(5)` exactly, and tests `5^w==1 mod q^2`.  It finds exactly:

| q | w_q | s_q | P+(w_q) | depth |
|---:|---:|---:|---:|---:|
| 20771 | 10385 | 2 | 67 | 1 |
| 40487 | 40486 | 2 | 653 | 1 |

No largest-coordinate rigid depth at least two occurs in this frozen range.  This is bounded evidence only.

The known panel also verifies:

| q | w_q | s_q | P+(w_q) | dynamic partner admitted? |
|---:|---:|---:|---:|:---:|
| 20771 | 10385 | 2 | 67 | yes |
| 40487 | 40486 | 2 | 653 | no (`653==1 mod 4`) |
| 1645333507 | 1645333506 | 2 | 30469139 | yes |

The distribution and infinitude of the required nonregular order signatures remain open here.

## 9. Realizability verdict

- The beta-one template has an actual one-anchor realization at `(67,20771)`.
- Some abstract templates are universally impossible because their dynamic coordinate is not an admitted prime.
- Higher-depth rigid resources were absent in the frozen search, but no universal nonexistence is claimed.
- Both-anchor assembly remains a genuine compatibility problem and cannot be inferred from separate anchor budgets.
