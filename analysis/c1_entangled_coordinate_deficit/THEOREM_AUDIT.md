# Independent theorem audit

## Verdict

```text
TARGETED PARTIAL STRUCTURAL ADVANCE: PASS
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

Prime-power lifting geometry, the exact rigid/dynamic fatal normal form, and
the arbitrary-entanglement reverse CRT theorem were already present on the
bound main.  They are dependencies here, not new results.

## T1: ascending dependency DAG

If `p->q`, then `p|ord_q(5)|q-1`, hence `p<q`.  Therefore cycles and
nontrivial SCCs are impossible.  Taking the `p`-valuation of the LCM defining
`U` gives `beta_p=max_q v_p(w_q)`; the optional two-adic period contributes
nothing for odd `p`.  A sink has `beta_p=0`, while the exact chain
`11->67->20771` shows that a source may have positive beta.

## T2: boundary-corrected prime-coordinate strict-deficit criterion

Fix an anchor `c`.  Factor `U=product_l l^e_l` and choose the rational-prime
coordinates increasingly.  Assign each dynamic fatal row `p` to coordinate
`p`.  Assign each rigid fatal row `q` to
`lambda_q=P^+(w_q)`.  Set

```text
D_{l,c} = rho_{l,c} for a dynamic l-row, otherwise 0,
R_{l,c} = sum_{q rigid fatal, lambda_q=l} l^(-v_l(w_q)).
```

First handle the optional two-adic row.

```text
no two-adic row: no preliminary condition;
K_2=2: require the fixed anchor c to be two-adically safe, equivalently
       Theta_c=0;
K_2>=3: assign Theta_c to the genuine coordinate two, since 2|t_2|U.
```

After that boundary check, define

```text
H_{l,c}=D_{l,c}+R_{l,c}+1_{l=2 and K_2>=3} Theta_c
```

for every genuine rational-prime coordinate `l|U`.  If `H_{l,c}<1` for every
such `l`, then a coarse safe class exists, and hence a full safe exponent
exists.  When `U=1`, the coordinate family is empty and the unique coarse
class is safe once the constant boundary has passed.

Proof: the active congruence of a dynamic `p`-row uses only coordinates
dividing `w_p`, all smaller than `p`; after they are fixed, the event occupies
exactly `rho_{p,c}` of the `p` coordinate.  A rigid `q`-row depends only on
coordinates dividing `w_q`; after coordinates below `P^+(w_q)` are fixed, it
is empty or one residue in the largest-prime coordinate, of the displayed
fraction.  For `K_2=2`, `5^d==1 (mod 4)`, so the two-adic condition is
constant in `d`: an unsafe anchor has no safe exponent, while a safe anchor
contributes no coordinate hazard.  For `K_2>=3`, the two-adic event depends
only on the genuine coordinate two and occupies exactly `Theta_c` of it.  A
fiberwise union bound strictly below one permits one safe choice at each
step.  Later coordinates do not change an earlier assigned event.  Reverse
CRT then lifts the final coarse class.

This proof is effective and uniform over every finite admitted system.  The
strict inequality is essential.

### Rejected old wording and exact counterexample

The previous statement checked only

```text
1_{l=2} Theta_c+D_{l,c}+R_{l,c}<1 for l|U.
```

It was false when `K_2=2` and `2` did not divide `U`.  Take the odd row
`p=11, K=2, r=0, E={1}`, the two-adic row `K_2=2, r_2=1`, and anchor `c=0`.
Direct calculation gives

```text
w_11=5, s_11=1, a_11=1, t_2=1, U=5, L=55, beta_11=0.
```

Since `-1-5^d` is never divisible by 11, every odd-coordinate hazard is zero,
so the old hypothesis passes.  But
`1-3^0-5^d==3 (mod 4)` for every `d`, which is not a two-square residue.
Thus all 55 full-period exponents are unsafe.  The corrected theorem rejects
the example at its constant boundary before coordinate induction.

## T3: necessary saturated odd coordinate

The boundary cases are as follows.

- With no two-adic row, choose either anchor.  There is no constant boundary
  and no `Theta_c` hazard.
- With `K_2=2`, the exact two-adic count lemma gives an anchor that is
  completely two-adically safe, so `Theta_c=0` and the corrected T2 boundary
  passes.
- With `K_2>=3`, the lemma gives an anchor with `Theta_c<=1/2`.  This is a
  genuine coordinate-two hazard and is strictly below one.

For `p==3 (mod 4)`, `v_2(w_p)<=1`.  The only admitted prime with `w_p=2` is
`p=3`; it is regular, and a rigid valuation below `s_3=1` cannot be a positive
accepted odd valuation.  No dynamic row has coordinate two either.  Hence
`D_{2,c}=R_{2,c}=0` in all three cases, and coordinate two cannot be the
saturated coordinate.  If a complete certificate existed, corrected T2 must
therefore fail at an odd coordinate, so

```text
D_{l,c}+R_{l,c} >= 1
```

for at least one odd `l`.  This is necessary, not sufficient.

## T4: beta-one saturation and contraction

For a regular dynamic row with `s_p=1`, `K_p=2`, `E_p={1}`, and `beta_p=1`,
an active lower cylinder has `p-1` fatal `p`-digits and one unresolved center.
A rigid row `q` with `p||w_q`, conditioned on its non-`p` coordinates,
selects one `p`-digit.  It closes the fiber exactly when that digit is the
dynamic center.  The pair then contracts to

```text
x==b_p (mod w_p),
x==b_q (mod w_q/p).
```

When `p=P^+(w_q)`, every remaining factor is lower than `p`, so this is a
genuine lower-coordinate contraction.  It does not by itself prove that a
finite contraction tree reaches a global cover.

## Common-residue and two-adic checks

For two active anchors in one row, writing

```text
A_i=5^b_i, u_i=(r_p-3^i)A_i^-1, epsilon_i=u_i-1,
Delta=A_0-A_1-2
```

gives `Delta+A_0 epsilon_0-A_1 epsilon_1==0 (mod p^K)`.  Hence a unique
strict minimum among the three clipped valuations below `K` is impossible.
The common-residue sample `p=20771`, `r=96315155` has the two distinct rigid
classes `6528` and `2`, so no universal two-anchor factor saving follows.

A residue modulo `2^K` is a sum of two squares exactly when it is zero or its
odd part is `1 mod 4`.  Counting `5^d` over its exact period gives one anchor
with two-adic unsafe density at most one half.  Direct square-residue sets
independently reproduce the complete distributions for `2<=K<=10`.

## Exact chain boundary

At `c=1`, the rows

| p | w | s | K | r | E |
|---:|---:|---:|---:|---:|:---:|
| 11 | 5 | 1 | 2 | 4 | {1} |
| 67 | 22 | 1 | 2 | 4 | {1} |
| 20771 | 10385 | 2 | 2 | 20775 | {1} |

have `U=L=228470`, `beta_11=beta_67=1`.  On `d==0 (mod 310)` their first
witness partition is `670+66+1=737`.  The full anchor nevertheless has
176,698 safe cells.  This is a saturated fiber obstruction to naive DAG
peeling, not a complete certificate.

## Logical boundary

A safe local-mask exponent only proves that the named finite local certificate
is incomplete.  It does not prove that the positive remainder is a sum of two
squares.  For any fixed escape `(c,d)`, positivity along the associated global
CRT progression holds only once `n>3^c+5^d`.
