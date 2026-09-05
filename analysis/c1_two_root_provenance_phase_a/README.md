# A303656 two-root provenance — Phase A repository integration

Start with `REPORT.md` (Chinese, with English technical terminology). The primary
result is a genuine-arithmetic **free-coordinate rigid-blocker subclass no-go**,
not a universal no-go or a resolution of A303656.

## Bound authority

- Repository: `Samsen879/a303656`, ID `1333945235`.
- Main: `0200beede923c56e0284d9555c1dabaf91fa1755`.
- Tree: `23f10c12181c5caa394f7a3fb1acb6e79cc02fe6`.
- PRs #11–#13 were merged and their first-parent ancestry was verified.
- This directory is a repository-native integration of the reviewed source package.
- Project remains PAUSED; active promoted route NONE; A303656 UNRESOLVED.

`results/source_binding.json` records connector-read source identities. Source Git blob
IDs are GitHub-reported identities, not claims that source bytes were downloaded
and locally rehashed. All executable tools here are standalone and import no
other analysis implementation as their computational kernel.

## Reproduce

Python 3.10+ and its standard library suffice. No network, credentials, external
solver, floating-point arithmetic, or repository installation is required.

```sh
python3 tools/verify_integration.py
out=$(mktemp -d)
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 tools/reproduce.py --output-dir "$out/replay"
python3 -m unittest discover -s tests -v
python3 tools/finalize_integration.py --verify
```

`reproduce.py` reruns the full bounded experiments and unit tests into an
explicit directory outside this integration tree, then byte-compares compact
outputs and verifies generated-catalog hashes. In particular it
repeats the source's existing `10^7` prime bound using a sieve and the Fermat
exponent nonregularity test; this is **not** an enlarged prime search. The sieve
uses about ten million bytes, plus interpreter and paired-state catalog storage.

Individual commands:

```sh
python3 tools/run_small_models.py
python3 tools/run_arithmetic.py
python3 tools/charge_filter.py
python3 tools/rigid_blocker_audit.py
python3 -m unittest discover -s tests -v
```

## Contents

- `REPORT.md`: fourteen requested report sections, full blocker proof, joint
  reverse CRT proof, scopes, counterexamples, CSP, and actual-prime replay.
- `PROOF_AUDIT.md`: adversarial checks, nonclaims, and remaining boundary.
- `tools/contraction.py`: exact guarded-slice contraction, row provenance, and
  state-sensitive partial-assignment algebra.
- `tools/direct_check.py`: separately organized original-system truth tables.
- `tools/residue_states.py`: exact low-digit p-adic trie paired-mask quotient.
- `tools/charge_filter.py`: necessary original-resource cardinality/charge filter.
- `tools/rigid_blocker_audit.py`: existing-bound independent inventory replay,
  arithmetic boundary check, joint reverse CRT tests, constructive blocker tests.
- `results/`: explicit exact experiment outputs and counterexamples.
- `results/generated_catalog_receipt.json`: hashes, sizes, and counts for the
  deterministically generated 2346- and 25963-state catalogs. The 229442-byte
  and 2562114-byte catalogs are intentionally not stored in Git; full replay
  regenerates and verifies them in the requested temporary output directory.

## Scope guards

The `2 x 2` three-row counterexample is abstract, not an actual prime realization.
Its minimality is only in the explicitly enumerated proper-product-cylinder
model. It does not disprove the genuine arithmetic H1 hypothesis.

The arithmetic theorem covers every finite admitted system whose nonregular row
pool is contained in `{20771,40487}`, regardless of the number or size of regular
rows, precisions, accepted odd valuation sets, or shared residues. The independent
finite inventory then extends it to every panel whose odd row primes are at most
`10^7`. No claim is made about all larger primes.

The known prime `1645333507` is independently checked as a boundary resource: its
order has no universally non-admitted odd prime factor. That is not a complete
certificate and not a counterexample to the theorem.

Exact state-product counts are **not** numbers of full systems enumerated.
Correct frozen-state geometry and provenance have identical root truth. Different
answers arise only after the allowed original state relation has been relaxed.

A macro is never a new prime or new capacity. Local zeros remain fail-closed.
Independent computations here are algorithmically separate implementations by the
same laboratory, not independent authors or different-language stacks.
