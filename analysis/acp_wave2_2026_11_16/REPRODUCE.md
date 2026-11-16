# Reproduction

From the repository root.

## Independent checks (standard library only, about 5 minutes)

```bash
python3 analysis/acp_wave2_2026_11_16/tools/independent_checks.py
```

Expected final line: `ACP_INDEPENDENT_CHECKS_PASS`. These checks cover finite
statements only (packet hashes, the explicit `β`-line covering, the
Proposition H horizon, Lemma L4 for `M ≤ 13`, `p < 3000`, and the class `(0,0)`
`z = 0` fibre). They do not verify Theorem A, Theorem R or any analytic argument.

## Producer replay (about 25 minutes on 2 cores; replayed at integration, see `results/`)

Requirements: Python 3.9+, `numpy`, `gmpy2`, and `ortools` for the
one-parameter controls. Copy the packet out of the repository first, so that
generated files never land in the retained source:

```bash
tmp=$(mktemp -d)
cp -a analysis/acp_wave2_2026_11_16/source/acp_packet "$tmp/acp"
AUDIT="$PWD/analysis/triage_wave_2026_11_14/source/triage_packet" sh "$tmp/acp/run_all.sh"
```

Expected final line: `ALL CERTIFICATES REPLAYED`. `./run_all.sh full` also
rebuilds the catalogue and fibre statistics from scratch; the producer ran its
steps individually but not as one command.

## Package custody

```bash
cd analysis/acp_wave2_2026_11_16
sha256sum -c SHA256SUMS
```

A303656: UNRESOLVED.
