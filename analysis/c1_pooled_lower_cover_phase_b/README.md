# A303656 pooled-lower-cover Phase B

Read-only research package bound to main
`44e522dd6e88504e2b9829f0b27359e6c45a76ff`.

**Verdict:** the universal pooled-lower branch is NOT eliminated. The package
contains a typed pooled inverse/contraction grammar, a new full-depth
allocated-blocker theorem, a sparse nonregular-subclass no-go including
`1645333507`, the cutoff-free resource zero `R_(3,4)=empty`, and a conditional
squarefree order-closed seed construction. No actual terminal seed or complete
C=1 certificate is supplied. Project authority remains unchanged.

## Reading

`REPORT.md` is the 16-section mathematical report. `DEFINITIONS.md` gives the
complete finite-instance grammar and exact demand semantics.
`THEOREM_AUDIT.md` lists proof obligations, counterexamples, and scope guards.
`SOURCE_BINDING.json` records actual GitHub readings and their limits.

`COMPUTATION_SPEC.md` is the original frozen specification; its SHA256 is
`08046d28e3e4e54420293695951122615b2167a94f24fc13f32992e41ece90b0`.
The additive target specification and the later U/L interpretation are kept
separately rather than silently modifying that specification.

## Reproduction

Python 3.10+ is sufficient for the verifier, reference runner, and tests.
No third-party packages, network connection, or repository checkout are needed
for verification. Run from this package root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 tools/verify_bundle.py --replay
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -m unittest discover -s tests -v
```

For a separately retained output directory:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 tools/reproduce.py --output-dir /tmp/a303656-pooled-replay
```

The runner rejects output paths inside this immutable package. Canonical
results omit timings. The manifest excludes itself and runtime `__pycache__`.

`tools/discover_certificates.py` is OPTIONAL historical discovery code and
requires SymPy. It is not imported by any verification path. The delivered
primality certificates are verified using complete recursive full-order
Lucas certificates with standard-library integers only.

## Contents and limits

The `results/` directory includes exact row-geometry counts, the full actual
SPLIT mask receipt, paired rigid and mixed-type actual-row examples, abstract
prefix/configuration checks, occupied-coordinate blocker tests, certified
cyclotomic factors, and the actual regular skeleton's full-period escapes.

Finite tests are complementary implementations by one author, not independent
research teams or independently authored software stacks. The source repository
was not cloned or modified; its entire historical archive, CI, and prime scans
were not replayed. This package has not been integrated or promoted on GitHub.

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
