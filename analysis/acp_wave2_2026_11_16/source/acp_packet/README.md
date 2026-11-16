# A303656 — ACP package (2026-11-16)

Exact search and certificates for the Abstract Covering Problem behind the local-positivity
statement (LP) for Zhi-Wei Sun's conjecture OEIS A303656.  Read `REPORT.md` (Chinese) first.

    ./run_all.sh            # replay every stored certificate (about 22 minutes on 2 cores)
    ./run_all.sh full       # also rebuild catalogue and fibre statistics from scratch (about 20 minutes more; the individual steps were run, the full mode was not replayed end-to-end)
    AUDIT=/path/to/A303656_Triage_Audit_2026-11-14 ./run_all.sh   # compare with the frozen C21 certificate

Requirements: python3 >= 3.9, numpy, gmpy2, ortools (toy_1d.py only), scipy (LP search only).

Status: all statements are AI-derived and machine-checked by the scripts here; nothing has been
reviewed by a human mathematician.  Theorem R in its general form is conditional on two lemmas of
the frozen C21 proof (see REPORT.md, section 3.3).
