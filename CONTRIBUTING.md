# Contributing

Contributions must preserve the evidence hierarchy and the `UNRESOLVED` project status unless accompanied by an independently checkable proof or counterexample certificate and a separate authority review.

## Required discipline

- Use exact integer arithmetic for formal finite computations.
- State every finite interval or domain explicitly.
- Preserve commands, return codes, environments, manifests, raw logs, and hashes.
- Do not trust precompiled binaries; rebuild from source.
- Do not silently repair historical archives.
- Distinguish proved, conditional, finite, observational, heuristic, unknown, and superseded claims.
- Add or update validators when changing generated authority views.

Run before submitting changes:

```bash
python3 scripts/verify_public_repository.py
```
