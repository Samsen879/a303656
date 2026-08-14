# Root manifest reconciliation

Classification: **STALE ROOT MANIFEST AFTER LEGITIMATE TRACKED SOURCE UPDATE**.

`SHA256SUMS.txt` was introduced at `1158fdb813168c2b41b889a0b71021677461198a`; its two expected hashes exactly match those historical blobs. Commit `5fe0ee472cdefa7a23a05616a56a024fe571e58a` then legitimately changed both tracked sources for boundary and provenance hardening. Current hashes exactly match the `5fe0ee4` blobs.

| Path | Historical manifest / 1158fdb | Current / 5fe0ee4 | Classification |
|---|---|---|---|
| `src/search_twosquares_bitset.cpp` | `60c2291ae7785ad0bf2c8e6313d39704d8f8f048a8fc4bcac50337f7e0556f4d` | `279b36dd5043500aba8d8e1d1d2221c1c97e416e806d477b5de3a81dc31cd94c` | STALE ROOT MANIFEST AFTER LEGITIMATE TRACKED SOURCE UPDATE |
| `src/search_twosquares_clean.cpp` | `641ff6f3c02783173e73a5cab6fcd52ae298012591e75ae786957a191ebca6cd` | `2815c39ea97b134322860d4772ea574779886bd35b5754b1607e6f4615952f30` | STALE ROOT MANIFEST AFTER LEGITIMATE TRACKED SOURCE UPDATE |

The historical root manifest remains unchanged. `authority/manifests/CURRENT_DIRECT_SCANNER_SHA256SUMS.txt` is the corrected current-source manifest; it does not rewrite history.
