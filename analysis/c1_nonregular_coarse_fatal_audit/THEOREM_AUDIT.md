# Independent theorem audit

## Scope

Let `p != 5` be an odd prime, `w_p = ord_p(5)`, and
`s_p = v_p(5^w_p-1)`. An odd row accepts only named positive odd valuations
strictly below its precision; zero modulo `p^K` is unresolved.

## T1: lifting geometry

For every `K >= 1`,

```text
ord_(p^K)(5) = w_p p^max(0,K-s_p).
```

Indeed, reduction modulo `p` forces every exponent returning to one to be
`w_p t`, and odd-prime LTE gives valuation `s_p+v_p(t)`. The preimage of
`<5> mod p` has size `w_p p^(K-1)`, so the index of `<5> mod p^K` in that
preimage is `p^(min(s_p,K)-1)`.

For an active coarse logarithm `b mod w_p`, normalize
`u=(r_p-3^c)5^-b`. If `h=min(v_p(u-1),K)` is below `min(s_p,K)`, every lift
has the fixed valuation `h`. If `K<=s_p` and `h=K`, every lift is unresolved.
Otherwise `s_p<K`, `<5^w_p>` generates
`(1+p^s Z)/(1+p^K Z)`: there is a unique `q0 mod p^(K-s)` and every nonzero
difference has valuation `s_p+v_p(q-q0)`.

## T2: reverse CRT

For rows with `a_p=max(0,K_p-s_p)`, set

```text
U = lcm(t_2, all w_p)
L = lcm(t_2, all w_p p^a_p)
beta_p = v_p(U).
```

Then `U|L` and

```text
L/U = product_p p^max(a_p-beta_p,0).
```

For fixed `d=x+Uk`, the `p` row depends on `k` only modulo its displayed
`p`-power. If `x` is nonfatal for every row, choose one safe residue of `k`
for each row. These moduli are pairwise coprime, so CRT gives one common safe
lift. The two-adic state is unchanged because its exponent period divides
`U`. This proves the reverse implication without an order-disjointness
assumption.

## Closed fatal formula

The implementation in `tools/model.py` uses the T1 trichotomy directly. In a
dynamic fiber it tests whether the frozen `beta_p` digits still agree with
`q0`. If they do and `beta_p<a_p`, unresolved zero remains reachable. If they
already differ, the valuation is fixed below `beta_p`; if all `a_p` digits are
frozen, equality is unresolved and inequality has one fixed exact valuation.
No full fiber is enumerated by this formula.

## T3 and T4

If, for either anchor, the sum of fatal-set sizes inside the two-adic-safe set
is smaller than that safe set, the union bound and T2 give an escape.

When every `beta_p=0`, regular rows have no fatal coarse class. Each
nonregular row has at most one active rigid class modulo `w_p`, hence fatal
mass at most `1/w_p`. Independently, one of the anchors retains two-adic-safe
density at least `1/2`. Therefore an order-decoupled panel with
`sum_(s_p>=2) 1/w_p < 1/2` is incomplete for every optional sound two-adic
row.

For `20771`, `40487`, and `1645333507`, independent arithmetic verifies
`s_p=2`, order decoupling, and total shell mass
`675001461539/5578836432127965 < 1/2`. The conclusion applies to every subset
of this panel, not to arbitrary additions or to a complete list of base-5
nonregular primes.

## Quantifier boundary

The conclusion is only that the finite local-mask system leaves a positive
admissible remainder without an accepted local witness for sufficiently large
members of its CRT progression. It does not prove that remainder is a sum of
two squares, a fixed positive exponent bound, or A303656.
