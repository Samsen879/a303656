# Definitions and scope separation

## 1. Bound formal class

Let `P` be a finite set of distinct primes `p == 3 (mod 4)`, `p != 5`.  Row `p` has precision `K_p>=2`, one residue `r_p mod p^K_p` shared by anchors `c in {0,1}`, and a nonempty set

```text
E_p subset {1,...,K_p-1}
```

of positive odd accepted valuations.  A local value equal to zero modulo `p^K_p` is unresolved and never accepted.

Put

```text
w_p = ord_p(5),
s_p = v_p(5^w_p-1),
a_p = max(0,K_p-s_p),
ell_p = w_p p^a_p,
U = lcm(t_2,{w_p}),
beta_p = v_p(U),
L = lcm(t_2,{ell_p}).
```

The optional two-adic row is treated before odd-coordinate classification.  It is not inserted into a fictitious odd-coordinate budget.

## 2. Fixed coordinate and fixed lower assignment

Fix an odd rational prime `l|U`, one anchor `c`, and values of every rational-prime coordinate below `l`.  All events assigned to coordinate `l` then have one of the following exact forms.

The fiber is

```text
F_(l,beta) = Z/l^beta Z,  beta=v_l(U).
```

A translation normalizes one chosen lift of the dynamic center to `zeta=0`.

## 3. Dynamic event

If the admitted row `p=l` is dynamic, put

```text
m=min(a_l,beta),
J={0<=j<m : s_l+j in E_l}.
```

Because `E_l` contains only odd valuations,

```text
j in J  =>  s_l+j is odd.
```

Thus `J` lies in one parity class.  Define the shell

```text
S_j(zeta)={x in F_(l,beta): v_l(x-zeta)=j}.
```

Its size and mass are

```text
|S_j|=(l-1)l^(beta-j-1),
mu(S_j)=(l-1)/l^(j+1).
```

The dynamic event is

```text
A_J(zeta)=union_(j in J) S_j(zeta).
```

It excludes the unresolved center cylinder

```text
C_m(zeta)={x:x==zeta mod l^m}.
```

For classification one fixes a canonical full lift `zeta mod l^beta`; shells with `j>=m` merely decompose the unresolved center cylinder and are never dynamic.

## 4. Rigid event

A rigid fatal row `q` assigned to coordinate `l=P^+(w_q)` is, after lower coordinates are fixed, either empty or one cylinder

```text
C_e(t)={x in F_(l,beta): x==t mod l^e},
e=v_l(w_q), 1<=e<=beta.
```

Its mass is `l^-e`.

## 5. Three levels

### Level 1: abstract rational budget

Dynamic atoms have masses

```text
d_e=(l-1)/l^e, e=j+1,
```

with at most one dynamic atom at each depth.  Rigid atoms have masses

```text
r_e=1/l^e
```

with arbitrary multiplicity.  Positions are forgotten.

`atom-minimal` means deleting any single mass atom drops the total below one.

### Level 2: exact fiber cover

Positions are restored.  One dynamic row is a bundle of all shells in `J`; it is deleted as one row.  A collection is `row-minimal` when it covers the whole fiber and deleting any row event creates a hole.

This differs from atom-minimality: accepted shells in one dynamic row cannot be deleted separately.

### Level 3: arithmetic realizability

An abstract cylinder must be supplied by an actual prime, order, lifting depth, common residue, and accepted positive odd valuation.  Separate anchorwise choices are not automatically compatible with one common residue.

## 6. Fiberwise subcover versus global row deletion

The inverse theorem takes an irredundant **subcover of one fixed ambient fiber**.  Removing an event from this subcover is a set-cover operation with `U` and `beta` held fixed.  It is not claimed that deleting the corresponding prime from the global admitted system leaves `U` unchanged.

## 7. Coverage multiplicity

For events `E_1,...,E_r`, the multiplicity of cell `x` is

```text
M(x)=#{i:x in E_i}.
```

A partition has `M(x)=1` everywhere.  A saturated budget only says the sum of event masses is at least one; it does not imply coverage.

## 8. Complete certificate scope

A complete finite local certificate covers every exponent class modulo `L` at both anchors.  The inverse theorem produces a necessary odd-coordinate template occurrence.  It does not show that any template extends to a complete certificate or that escaping a certificate proves a sum-of-two-squares representation.
