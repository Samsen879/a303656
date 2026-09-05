# A303656 C=1 two-anchor common-residue Phase A

This repository-native integration is bound to repository commit
`1100eb5ba01d90e5b1001be0bdfa464860fdbb92` and tree
`ad1269916bf420c564e34887a96c808033fe538b`.

Source ZIP SHA-256:

```text
faf61d42c0c4315e6cddf9bd896807c3dad7a01c4aa8eb3b991ad472f65a82c9
```

Contents:

- `REPORT.md` — theorem statements, proofs, exact classification, scope, and missing hypotheses;
- `tools/reference_two_anchor.py` — standalone standard-library exact computation;
- `results/results.json` — machine-readable output;
- `tests/test_reference.py` — frozen-count and theorem-boundary regression tests;
- `manifest.json` and `SHA256SUMS.txt` — local bundle integrity records.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 tools/reference_two_anchor.py --output /tmp/a303656-phase2-results.json
python3 -m unittest discover -s tests -v
```

The result is a targeted same-lower structural advance. It does not prove that
a complete simultaneous certificate supplies a same-lower joint witness.
