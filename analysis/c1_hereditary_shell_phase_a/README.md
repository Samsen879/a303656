# A303656 hereditary provenance-cylinder shell Phase A

Repository-native integration for authority commit
`1100eb5ba01d90e5b1001be0bdfa464860fdbb92`.

Source ZIP SHA-256:

```text
0e2cbeb8b226dee16b44cc0783a07e45da57d7738ad924af1503337f9d2d0fde
```

Files:

- `REPORT.md` — proved scoped theorem, obstruction criterion, arithmetic witness,
  exact-computation summary, and route verdict.
- `tools/hereditary_shell_classifier.py` — independent standard-library exact
  reference implementation.
- `results/results.json` — complete machine-readable output.
- `SHA256SUMS.txt` — hashes of the three substantive files.

Run:

```bash
python3 tools/hereditary_shell_classifier.py --output /tmp/a303656-phase1-results.json
python3 -m unittest discover -s tests -v
python3 tools/finalize_integration.py --verify
sha256sum -c SHA256SUMS.txt
```

The script writes its selected output deterministically and does not access
GitHub.
