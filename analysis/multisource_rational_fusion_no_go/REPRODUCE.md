# Reproduction

From the repository root, with Python 3 and no third-party packages:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s analysis/multisource_rational_fusion_no_go/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_public_repository.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/privacy_scan.py
git diff --check
```

The first command checks exact rational identities and authority wording.
It does not prove MF-R for arbitrary rational functions; [PROOF.md](PROOF.md)
is the mathematical authority. The public verifier checks repository custody
and frozen authority consistency, not this theorem's proof.
