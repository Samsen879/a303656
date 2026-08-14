#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${BUILD_DIR:?set BUILD_DIR to a nonexistent isolated build directory}"
LOG_DIR="${LOG_DIR:?set LOG_DIR to a new audit-log directory}"
SOURCE_COMMIT="${SOURCE_COMMIT:?set SOURCE_COMMIT to the exact source commit}"
GMP_ROOT="${GMP_ROOT:?set GMP_ROOT to a freshly extracted libgmp-dev root}"
GMP_VERSION="${GMP_VERSION:?set GMP_VERSION and verify it using the logged oracle query}"
PYTHON="${PYTHON:-python3}"
CXX="${CXX:-g++}"
CXX_PATH="$(command -v "$CXX")"
LOGGER="$ROOT/scripts/run_logged_command.sh"

if [[ -e "$BUILD_DIR" ]]; then
  echo "ERROR BUILD_DIR already exists: $BUILD_DIR" >&2
  exit 2
fi
if [[ -e "$LOG_DIR" ]]; then
  echo "ERROR LOG_DIR already exists: $LOG_DIR" >&2
  exit 2
fi
if [[ ! -f "$GMP_ROOT/usr/include/gmpxx.h" ||
      ! -f "$GMP_ROOT/usr/include/x86_64-linux-gnu/gmp.h" ||
      ! -f "$GMP_ROOT/usr/lib/x86_64-linux-gnu/libgmpxx.a" ||
      ! -f "$GMP_ROOT/usr/lib/x86_64-linux-gnu/libgmp.a" ]]; then
  echo "ERROR incomplete extracted GMP development root: $GMP_ROOT" >&2
  exit 2
fi

mkdir -p "$LOG_DIR"

logged() {
  local tag="$1"
  shift
  "$LOGGER" "$LOG_DIR" "$tag" -- "$@"
}

COMMON=(-O2 -std=c++17 -Wall -Wextra -Werror -pedantic)
SANITIZED=(-O1 -g -std=c++17 -Wall -Wextra -Werror -pedantic
  -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer)
GMP_INCLUDE=(-I"$GMP_ROOT/usr/include" -I"$GMP_ROOT/usr/include/x86_64-linux-gnu")
GMP_LIB=("$GMP_ROOT/usr/lib/x86_64-linux-gnu/libgmpxx.a"
  "$GMP_ROOT/usr/lib/x86_64-linux-gnu/libgmp.a")

logged 000_build_mkdir mkdir "$BUILD_DIR"
logged 001_environment_uname uname -a
logged 002_environment_os cat /etc/os-release
logged 003_environment_compiler "$CXX_PATH" --version
logged 004_environment_python "$PYTHON" --version
logged 005_python_syntax "$PYTHON" -m py_compile \
  "$ROOT/src/direct_scanner_provenance.py" \
  "$ROOT/tests/direct_boundary_property_tests.py" \
  "$ROOT/tests/direct_provenance_tests.py"

logged 010_compile_x "$CXX_PATH" "${COMMON[@]}" \
  "$ROOT/src/search_twosquares_bitset.cpp" -o "$BUILD_DIR/search_twosquares_bitset"
logged 011_compile_y "$CXX_PATH" "${COMMON[@]}" \
  "$ROOT/src/search_twosquares_clean.cpp" -o "$BUILD_DIR/search_twosquares_clean"
logged 012_compile_oracle "$CXX_PATH" "${COMMON[@]}" "${GMP_INCLUDE[@]}" \
  "$ROOT/tests/tiny_twosquares_oracle.cpp" "${GMP_LIB[@]}" \
  -o "$BUILD_DIR/tiny_twosquares_oracle"
logged 013_compile_multiplicity "$CXX_PATH" "${COMMON[@]}" -I"$ROOT" \
  "$ROOT/tests/exponent_pair_multiplicity_test.cpp" \
  -o "$BUILD_DIR/exponent_pair_multiplicity_test"

logged 014_gmp_runtime_version "$BUILD_DIR/tiny_twosquares_oracle" --gmp-version
if [[ "$(<"$LOG_DIR/014_gmp_runtime_version/stdout.log")" != "$GMP_VERSION" ]]; then
  echo "ERROR GMP_VERSION does not match the linked oracle runtime" >&2
  exit 2
fi
logged 015_binary_hashes sha256sum \
  "$BUILD_DIR/search_twosquares_bitset" \
  "$BUILD_DIR/search_twosquares_clean" \
  "$BUILD_DIR/tiny_twosquares_oracle" \
  "$BUILD_DIR/exponent_pair_multiplicity_test"
logged 016_ldd_x ldd "$BUILD_DIR/search_twosquares_bitset"
logged 017_ldd_y ldd "$BUILD_DIR/search_twosquares_clean"
logged 018_ldd_oracle ldd "$BUILD_DIR/tiny_twosquares_oracle"
logged 019_readelf_x readelf -d "$BUILD_DIR/search_twosquares_bitset"
logged 020_readelf_y readelf -d "$BUILD_DIR/search_twosquares_clean"
logged 021_readelf_oracle readelf -d "$BUILD_DIR/tiny_twosquares_oracle"

logged 030_boundary_properties "$PYTHON" "$ROOT/tests/direct_boundary_property_tests.py" \
  --bin-dir "$BUILD_DIR" \
  --oracle "$BUILD_DIR/tiny_twosquares_oracle" \
  --multiplicity-test "$BUILD_DIR/exponent_pair_multiplicity_test"
logged 031_provenance_positive_negative "$PYTHON" "$ROOT/tests/direct_provenance_tests.py" \
  --python "$PYTHON" \
  --auditor "$ROOT/src/direct_scanner_provenance.py" \
  --bin-dir "$BUILD_DIR" \
  --source-dir "$ROOT/src" \
  --source-commit "$SOURCE_COMMIT" \
  --compiler "$CXX_PATH" \
  --gmp-version "$GMP_VERSION" \
  --work-dir "$BUILD_DIR/provenance"

logged 040_compile_x_sanitized "$CXX_PATH" "${SANITIZED[@]}" \
  "$ROOT/src/search_twosquares_bitset.cpp" -o "$BUILD_DIR/search_twosquares_bitset.sanitized"
logged 041_compile_y_sanitized "$CXX_PATH" "${SANITIZED[@]}" \
  "$ROOT/src/search_twosquares_clean.cpp" -o "$BUILD_DIR/search_twosquares_clean.sanitized"
logged 042_compile_multiplicity_sanitized "$CXX_PATH" "${SANITIZED[@]}" -I"$ROOT" \
  "$ROOT/tests/exponent_pair_multiplicity_test.cpp" \
  -o "$BUILD_DIR/exponent_pair_multiplicity_test.sanitized"
logged 043_sanitized_bin_mkdir mkdir "$BUILD_DIR/sanitized-bin"
logged 044_link_x_sanitized ln -s "$BUILD_DIR/search_twosquares_bitset.sanitized" \
  "$BUILD_DIR/sanitized-bin/search_twosquares_bitset"
logged 045_link_y_sanitized ln -s "$BUILD_DIR/search_twosquares_clean.sanitized" \
  "$BUILD_DIR/sanitized-bin/search_twosquares_clean"
set +e
logged 046_leak_sanitizer_probe env \
  ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 \
  "$BUILD_DIR/search_twosquares_bitset.sanitized" \
  --low 1 --high 1 --C 0 --D 0 \
  --json "$BUILD_DIR/leak-probe.json" --quiet
leak_probe_rc=$?
set -e
if [[ "$leak_probe_rc" -ne 1 ||
      "$(<"$LOG_DIR/046_leak_sanitizer_probe/stderr.log")" != *"LeakSanitizer has encountered a fatal error"* ]]; then
  echo "ERROR unexpected LeakSanitizer probe result: rc=$leak_probe_rc" >&2
  exit 2
fi
logged 047_boundary_properties_address_undefined env \
  ASAN_OPTIONS=detect_leaks=0:halt_on_error=1 \
  UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
  "$PYTHON" "$ROOT/tests/direct_boundary_property_tests.py" \
  --bin-dir "$BUILD_DIR/sanitized-bin" \
  --oracle "$BUILD_DIR/tiny_twosquares_oracle" \
  --multiplicity-test "$BUILD_DIR/exponent_pair_multiplicity_test.sanitized"

echo "BOUNDARY_HARDENING_SUITE_PASS"
echo "build_dir=$BUILD_DIR"
echo "log_dir=$LOG_DIR"
