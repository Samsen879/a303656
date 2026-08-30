# Deterministic repository package

The complete compact repository-native package is stored as ten base64 text
parts under `package_parts/`.

## Reconstruction

From this directory:

```bash
cat package_parts/repository_package.tar.xz.b64.part* \
  | base64 --decode \
  > /tmp/A303656_MINIMAL_SATURATED_COORDINATE_REPO_PACKAGE.tar.xz

echo "1aba57b1b27f9564e840f2271b50a3090598e18266c300142d77bde0f3276efc  /tmp/A303656_MINIMAL_SATURATED_COORDINATE_REPO_PACKAGE.tar.xz" \
  | sha256sum -c -

mkdir -p /tmp/a303656-coordinate-inverse/package
tar -xJf /tmp/A303656_MINIMAL_SATURATED_COORDINATE_REPO_PACKAGE.tar.xz \
  -C /tmp/a303656-coordinate-inverse/package
```

Equivalent Python entry point:

```bash
python3 unpack_repository_package.py /tmp/a303656-coordinate-inverse
```

The archive expands directly into the `package/` directory:

```text
package/
  README.md
  REPORT.md
  DEFINITIONS.md
  ABSTRACT_CLASSIFICATION.md
  REALIZABILITY_AUDIT.md
  COUNTEREXAMPLES.md
  tools/
  tests/
  results/
  manifest.json
  SHA256SUMS.txt
```

## Validation

```bash
cd /tmp/a303656-coordinate-inverse/package
PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/integrity.py verify --root .
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 tools/run_tests.py --root .
rm -rf tools/__pycache__ tests/__pycache__
PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/integrity.py verify --root .
```

The split representation is a connector-transport mechanism only. The Git
blob SHA of every part was checked against the corresponding local source
part before commit construction. Reconstruction and the full 24-test suite
were also replayed locally from the split representation.

Authenticated source ZIP:

```text
cf6e7a5dfb6287129fa1df501e4691c0d10fe2163d3572a2ca4502947fbaf9f1
```

Repository package `tar.xz`:

```text
1aba57b1b27f9564e840f2271b50a3090598e18266c300142d77bde0f3276efc
```
