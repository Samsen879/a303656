# Phase G B31 terminal square-hit route audit

## Consolidation and authority

This integration consolidates overlapping Phase G producer artifacts. It does
not create multiple theorem identities from shared producer cores. Full ZIP
custody and byte-sharing classifications are in `SOURCE_CUSTODY.md` and
`SOURCE_CONSOLIDATION.json`. Only one copy of the canonical shared core is
committed; transport ZIPs and the exact duplicate payload are not committed.

Integration base is main `c6ca0dc061783ab993be6fa077c8f66cd730e28c`,
tree `57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06`. The merged repository
owns the exact eight-index three-vertex equivalence. Phase G adds route audits
and bounded external evidence only; it does not duplicate Phase F theorem
identity.

The exact indices remain:

```text
878851
2636553
27244381
81733143
625552508473588471
1876657525420765413
19392127762681242601
58176383288043727803
```

## A. Power-substitution dependence

For prime `r`, positive `d` with `gcd(r,d)=1`, and an indeterminate `X`,

```text
Phi_r(X^d) = product_{e|d} Phi_{er}(X).
```

In the applied case, `r` is one of the two relay primes and `d|93`. If `q>93`
is prime, `q` does not divide `a`, and `ord_q(a)=m r` for `m|93`, then the
standard primitive-order localization gives

```text
v_q(Phi_r(a^d)) = v_q(Phi_{mr}(a))  if m|d,
                   0                 otherwise.
```

Thus substituting `5 -> 5^d` does not manufacture an independent second
Wieferich or square-hit condition. This prunes that substitution route only.

## B. 5-adic irreducibility route audit

Let `ell` be prime, `ell` not divide `n`, `c` be a nonzero rational number,
and `d>=2`. If `gcd(v_ell(c),d)=1`, the producer proof establishes that
`Phi_n(c T^d)` is irreducible over the rationals. For `ell=5`, `c=5`, and
`d=2`, all eight target indices satisfy the hypotheses, so
`Phi_n(5 T^2)` is irreducible over `Q`.

Polynomial irreducibility does not imply `Phi_n(5)` is squarefree. The
authenticated separation example is `Phi_3(30 T^2)`, which satisfies the
irreducibility hypotheses while its value at `T=1` is
`Phi_3(30)=931=7^2*19`. No square-hit exclusion follows from irreducibility.

## C. Standard Aurifeuilian inapplicability

For the standard Granville-Pleasants criterion as used by
Allombert-Belabas, the squarefree representative for base 5 is `a*=5`, with
`a*=1 mod 4`; the applicable odd-index case requires every prime dividing
`a*` to divide the index. None of the eight indices is divisible by 5.
Therefore the standard Aurifeuilian criterion used by that method does not
apply to these eight indices.

This says only that this standard criterion is unavailable. It does not say
that no algebraic, numerical, norm, or other factorization exists.

Primary references: Allombert and Belabas, *Practical Aurifeuillian
Factorization*, J. Theor. Nombres Bordeaux 20 (2008), 543-553,
`https://doi.org/10.5802/jtnb.641`; Granville and Pleasants,
*Aurifeuillian Factorization*, Math. Comp. 75 (2006), 497-508,
`https://doi.org/10.1090/S0025-5718-05-01766-7`.

## D. Bounded external computational gate

Dorais and Klyve, *A Wieferich Prime Search up to 6.7 x 10^15*, Journal of
Integer Sequences 14 (2011), Article 11.9.2, section 4.1, reports a complete
search for bases 3, 5, and 7 through the inclusive endpoint

```text
(2*3*5*7*11*13*17*19*23*29)*150000 = 970453984500000
```

and reports no new base-5 solutions. The journal page records publication on
2011-10-16. Source:
`https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.html`.

This repository did not replay the historical exhaustive search. Accepting the
published computation gives only `q > 970453984500000` for a target base-5
Wieferich prime not among the six known solutions, whose exact orders are
independently recertified by the included finite replay.

For `n=878851`, write `q=1+2kn`. The target congruences require
`k mod 10` in `{5,9}`. The raw first integer `k` above the bound is
`552115197`; the first satisfying those congruences is `k=552115199`, giving
`q=970453989512699`. This number is not asserted prime, a cyclotomic factor,
or a square hit.

Label: `BOUNDED EXTERNAL COMPUTATIONAL GATE`. It is not theorem closure and is
not authorization to extend a scan.

## E. Exact specialization ownership

Phase F owns the exact eight-index three-vertex equivalence and normalized
closed-state criteria. Phase G replays the index list and finite identities,
but adds no second copy of that theorem. No B31 terminal index is closed.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_integration.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v tests/test_integration_scope.py
```

The verifier authenticates both canonical producer manifests against the
single shared core, confirms the wrapper-only differences, runs normal and
optimized isolated replays, checks the finite mutation controls, validates
the custody classification and dependency hashes, and independently checks
the published-bound arithmetic and first admissible `k`.

## Explicit nonclaims and project state

```text
n=878851 CLOSED:
NO

FOUR-INDEX r=878851 FAMILY CLOSED:
NO

B31 THREE-VERTEX EMPTY:
NO

B31^odd EMPTY:
NO

ACTUAL B31^odd MEMBER:
NONE

EXACTLY-SEVEN:
NOT KILLED

N>=8:
NOT PROVED

A303656:
UNRESOLVED

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
```
