# C=1 entangled coordinate-deficit audit

This directory records an independent repository-native audit of a targeted
structural result for finite fail-closed `C=1` local-mask systems.  It preserves
the project state:

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

The new result is a dependency-aware prime-coordinate deficit criterion.  It
is accompanied by a necessary saturated odd-coordinate condition and an exact
beta-one saturation/contraction example.  It is not a universal `C=1` no-go,
a complete certificate, a representation theorem, or a route promotion.

The intake ZIP had SHA-256
`8c300e869ebfa0a4a559e38d9667a469b3e352dd9b9dfbd9425ae200d55cb4e0`;
its internal `SHA256SUMS.txt`, manifest, sizes, and payload hashes passed before
the repository audit began.

## Unit tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s analysis/c1_entangled_coordinate_deficit/tests -p 'test_*.py'
```

## Deterministic replay

```bash
python3 analysis/c1_entangled_coordinate_deficit/tools/verify.py \
  --output-dir /tmp/a303656-c1-entangled-results
```

The verifier imports no candidate code.  It uses direct modular enumeration
for the admitted `228470`-cell chain period, exact rational arithmetic for the
coordinate examples, and square-residue sets for the two-adic replay.
