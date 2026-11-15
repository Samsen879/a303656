# Reproduction

From the repository root, using Python 3.11+ and the standard library only:

```bash
python3 analysis/triage_wave_2026_11_14/tools/replay.py
python3 analysis/triage_wave_2026_11_14/tools/check_joint_wieferich.py
```

The replay verifies every packet manifest entry, copies the packet into a
temporary directory, and executes `checks/root_c22_check.py`,
`checks/c22_independent_budget.py` and `c21_frozen/verify.py` there. Generated
JSON never writes into the retained packet. Nonzero exits or rational
mismatches fail the replay; timing and regenerated hash fields are not
mathematical comparisons.

Expected: `TRIAGE_REPLAY_PASS`, C21 29 budgets below 1 with worst margin
`2465867/878169600`; C22 catalog `80/60/46`, 33 budgets below 1, base
`155932663/190512000`, maximum at `M=11,t=11` equal to
`4238011529/4390848000`, slack `152836471/4390848000`.
The second tool prints `JOINT_WIEFERICH_CHECK_PASS` for the five named examples.
Neither tool verifies an analytic theorem or scans all primes below the
externally reported search bound. A303656: UNRESOLVED.

Verify integration-file custody from the package directory:

```bash
cd analysis/triage_wave_2026_11_14
sha256sum -c SHA256SUMS
```

The five uploaded full reports are retained as evidence, not executed by the
replay. Their original PDF/MD/TXT bytes are included in `SHA256SUMS`; receipt
does not add a mathematical verification or alter the expected replay results.
