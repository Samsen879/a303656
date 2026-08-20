# C=1 nonregular coarse-fatal repository audit

## Verdict

```text
BOUNDED NEGATIVE STRUCTURAL THEOREM AUDIT: PASS
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The audit independently confirms T1 lifting geometry, the T2 reverse CRT
implication, the T3 union-bound class, and the T4 order-decoupled shell-sparse
class. It does not establish an arbitrary-nonregular universal no-go or a
complete `C=1` certificate.

## Provenance

- Base: `9ae583fcaa7b0a46ed638d7ab25423b55e1a8f8d`.
- Base tree: `86f5b202972981ab2d028c6613fa74f7f07eaa68`.
- Source commit: `b42ed4f266d73311da80d3e642e1347375ddecbb`.
- External directory `SHA256SUMS.txt` SHA-256:
  `90abe6a18b28c27f124d0e16fd0d057b87aa9f95b0fedcb6dc80867ed5c0cb73`.
- Claimed outer ZIP SHA-256: **not verified; byte not supplied**.

## Independent closed-form audit

The repository implementation computes fatality from the rigid/unresolved/
dynamic trichotomy. It does not enumerate a prime row's compatible full fiber.
For each nonfatal coarse class, T2 combines one safe residue modulo
`p^max(a_p-beta_p,0)` for every row by CRT.

The adversarial replay fixes

```text
p rows: (3,K=4), (7,K=2), (19,K=2)
U=18, L=7182, beta_3=2, a_3=3.
```

Across 120 deterministic residue systems, 12,960 closed-form fatal decisions
matched full-period brute force. The record hash is
`bf6d55c505b3ba4b388b2407149e68caf6e07eda17263fdf4e96406124dc0906`.
No tested system was a complete certificate; this count is diagnostic, not a
universal theorem.

## Known nonregular panel

Independent arithmetic verifies:

| p | ord_p(5) | s |
|---:|---:|---:|
| 20,771 | 10,385 | 2 |
| 40,487 | 40,486 | 2 |
| 1,645,333,507 | 1,645,333,506 | 2 |

Their coarse LCM is `11,157,672,864,255,930`; every panel prime is coprime to
it. The exact shell mass is
`675001461539/5578836432127965 < 1/2`. Hence every system using only any subset
of this panel is incomplete, even with one sound two-adic row.

## Additional checks

- unresolved local zero remains fail-closed;
- two-adic characterization matched direct square residues for `2<=K<=12`
  (8,188 residues);
- unit and corruption tests: `10/10 PASS`;
- frozen public authority validator: `PASS`.

## Boundary

A local escape only invalidates the named finite local-mask certificate. It
does not prove the remainder is a sum of two squares. Additional primes inherit
the corollary only when the complete enlarged panel still satisfies the stated
T4 hypotheses. No route is promoted by this audit.
