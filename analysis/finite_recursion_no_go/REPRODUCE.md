# Reproduction

Run from the repository root.  The default path is offline and standard-library
only.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B analysis/finite_recursion_no_go/verify.py
```

Run the independent implementation directly:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  analysis/finite_recursion_no_go/tools/reference_audit.py \
  --limit 5000 --output /tmp/thread3-reference-audit.json
sha256sum /tmp/thread3-reference-audit.json
```

Expected JSON SHA256:

```text
9e5f698a08eb8374617bd3d49f8aa7753233b15ec134bf8b09a71aa3233bcbe4
```

The producer comparison replay additionally needs NumPy and SymPy.  Supply an
already available interpreter; the wrapper does not install anything:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  analysis/finite_recursion_no_go/verify.py \
  --with-producer \
  --producer-python /path/to/python-with-numpy-and-sympy
```

The comparison ignores only the producer certificate's self-reported Python
and NumPy/SymPy environment fields.  Mathematical fields must match exactly.
