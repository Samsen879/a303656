# Output status

The authoritative machine-readable claim set is `formal_results_audit.json`.
Only datasets listed there, and rechecked by `src/audit_formal_results.py` and
`src/verify_direct_outputs.py`, are used for the final mathematical conclusions.

Other files preserve exploratory, diagnostic, benchmark, interrupted, or
superseded runs.  Their presence is for transparency and does not promote them
to certified results.
