# Quantifier crosswalk

The proved deficit theorem has the order

```text
for every finite admitted system S,
for every fixed anchor c,
first require the K_2=2 constant two-adic condition to be safe when present;
then, if every genuine rational-prime CRT coordinate budget is strictly below one,
then there exists x mod U safe at c,
and there exists d mod L safe at c.
```

There is no preliminary condition when the two-adic row is absent.  For
`K_2=2`, the preliminary condition is `Theta_c=0`, because the row has period
one and may exist even when `2` does not divide `U`.  For `K_2>=3`, `2|U` and
`Theta_c` is instead included in the genuine coordinate-two budget.

The necessary condition has the different order

```text
for every complete certificate S,
choose an anchor c supplied by the exact two-adic lemma;
then there exists an odd l|U with D_{l,c}+R_{l,c}>=1.
```

For `K_2=2`, the selected anchor is completely two-adically safe.  For
`K_2>=3`, it has `Theta_c<=1/2`.  With no two-adic row there is no boundary.
In every case the admitted odd rows contribute neither a dynamic nor a rigid
coordinate-two saturation, so completeness forces failure at an odd
coordinate.

It is not a sufficient certificate test.  The contraction lemma is conditional
on a fixed assignment of every non-`p` coordinate; only when the rigid digit
equals the dynamic center is the entire `p` fiber closed.

All local conditions are periodic modulo `L`, so finite-period coverage is
equivalent to coverage for all nonnegative exponents.  Reverse CRT combines
one safe lift choice modulo each remaining pairwise-coprime
`p^max(a_p-beta_p,0)`.

The theorems are effective for a supplied finite system.  They give no uniform
system-independent numerical bound, no complete `C=1` classification, and no
implication from local noncoverage to a sum-of-two-squares representation.
