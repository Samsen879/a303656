# Exact P5 sparse cross-class panel feasibility audit

This pipeline is deliberately limited to authenticated modular data, exact CRT
class construction, activation-cell intersection, prior-evaluation exclusion,
deduplication, and deterministic provisional panel geometry.

It must not call a `T(n)` backend, construct a winner mask for a new integer,
factor an integer, test two-square representability, or invoke a direct oracle.
Family Q is comparison-only and requires a new web review and freeze before any
future integer census.

Replay after source commit Q:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 analysis/p5_sparse_panel_feasibility/tools/run_audit.py \
  --root . \
  --output analysis/p5_sparse_panel_feasibility/results \
  --source-commit SOURCE_COMMIT_Q
```
