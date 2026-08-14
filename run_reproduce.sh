#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"
PYTHON_EXE="$(command -v "$PYTHON")"
PYTHON_BIN_DIR="$(dirname "$PYTHON_EXE")"
CXX="${CXX:-g++}"
LEVEL="${LEVEL:-quick}"          # quick | certified10m | certified100m | full | full1b | full1p6b
JOBS="${JOBS:-5}"
SKIP_STAGE0="${SKIP_STAGE0:-0}"
ONLY_STAGE0="${ONLY_STAGE0:-0}"
STAGE0_SCRIPT_TIMEOUT="${STAGE0_SCRIPT_TIMEOUT:-180}"
AUDIT_STORED="${AUDIT_STORED:-1}"
REPRO="${REPRO_DIR:-$ROOT/reproduce_work}"

case "$LEVEL" in
  quick|certified10m|certified100m|full|full1b|full1p6b) ;;
  *) echo "LEVEL must be quick, certified10m, certified100m, full, full1b, or full1p6b" >&2; exit 2 ;;
esac

rm -rf "$REPRO"
mkdir -p "$REPRO"/{bin,logs,output,stage0,chunks,direct}

"$PYTHON" - <<'PY'
import importlib
for name in ("numpy", "sympy", "z3"):
    importlib.import_module(name)
print("python_dependencies=OK")
PY

# ---------------------------------------------------------------------------
# Stage 0: verify archive hashes, rebuild the old verifier from source, and run
# the old bundle's own reproduction script.  No archived binary is trusted.
# ---------------------------------------------------------------------------
if [[ "$SKIP_STAGE0" != "1" ]]; then
  echo "4dadb8ce07cd0ccf56575ef0882d6bb02284a02c61e05cd1424e070d83b22ff3  $ROOT/baseline/a303656_p2cover_bundle.zip" | sha256sum -c -
  unzip -q "$ROOT/baseline/a303656_p2cover_bundle.zip" -d "$REPRO/stage0"
  BASE="$REPRO/stage0/a303656_p2cover"
  (
    cd "$BASE"
    sha256sum -c SHA256SUMS | tee "$REPRO/logs/stage0_internal_sha256.log"
    "$CXX" -O3 -std=c++17 src/verify_pruning.cpp -lgmpxx -lgmp -o "$REPRO/bin/verify_pruning"
    "$REPRO/bin/verify_pruning" cert/gcd_factor_B5000.txt "$REPRO/output/primes_B5000_verified.csv" \
      | tee "$REPRO/logs/stage0_verify_pruning.log"
    cmp "$REPRO/output/primes_B5000_verified.csv" output/primes_B5000_verified.csv
    timeout "$STAGE0_SCRIPT_TIMEOUT" env PATH="$PYTHON_BIN_DIR:$PATH" PYTHON="$PYTHON_EXE" \
      bash -x run_reproduce.sh \
      > "$REPRO/logs/stage0_bundle_run_reproduce.log" \
      2> "$REPRO/logs/stage0_bundle_run_reproduce.trace"
  )
  grep -qx 'eligible_prime_count=527' "$REPRO/logs/stage0_verify_pruning.log"
  grep -qx 'cardinality_lower_bound=598' "$REPRO/logs/stage0_verify_pruning.log"
  grep -qx 'minimum_primes_with_max_order_above_B=135' "$REPRO/logs/stage0_verify_pruning.log"
fi

if [[ "$ONLY_STAGE0" == "1" ]]; then
  find "$REPRO" -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > "$REPRO/SHA256SUMS.txt"
  echo "STAGE0_REPRODUCTION_PASS"
  echo "output_directory=$REPRO"
  exit 0
fi

# ---------------------------------------------------------------------------
# Clean builds of all audited current implementations.
# ---------------------------------------------------------------------------
# Build each translation unit from source.  Sequential compilation avoids
# memory pressure on small reproducibility machines; search-level parallelism
# is controlled separately by JOBS.
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/verifier_gmp.cpp" -lgmpxx -lgmp -o "$REPRO/bin/verifier_gmp"
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/search_bitset.cpp" -o "$REPRO/bin/search_bitset"
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/search_exhaustive_clean.cpp" -o "$REPRO/bin/search_exhaustive_clean"
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/search_factor_sieve.cpp" -o "$REPRO/bin/search_factor_sieve"
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/search_factor_sieve_clean.cpp" -o "$REPRO/bin/search_factor_sieve_clean"
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/search_twosquares_bitset.cpp" -o "$REPRO/bin/search_twosquares_bitset"
"$CXX" -O3 -std=c++17 -Wall -Wextra -pedantic "$ROOT/src/search_twosquares_clean.cpp" -o "$REPRO/bin/search_twosquares_clean"

"$PYTHON" -m py_compile \
  "$ROOT/src/common.py" "$ROOT/src/verifier.py" "$ROOT/src/search_z3_direct.py" \
  "$ROOT/src/search_z3_cegis.py" "$ROOT/src/search_exhaustive_python.py" \
  "$ROOT/src/prime_analysis.py" "$ROOT/src/run_factor_chunks.py" \
  "$ROOT/src/aggregate_factor_chunks.py" "$ROOT/src/run_twosquares_chunks.py" \
  "$ROOT/src/aggregate_twosquares_dual.py" "$ROOT/src/aggregate_direct_components.py" "$ROOT/src/verify_direct_outputs.py" \
  "$ROOT/src/audit_formal_results.py" "$ROOT/tests/toy_tests.py" \
  "$ROOT/tests/direct_small_crosscheck.py" "$ROOT/tests/factor_small_crosscheck.py"

# ---------------------------------------------------------------------------
# Stage 1: theorem-verifier fault injection and A/B/C toy consistency.
# ---------------------------------------------------------------------------
set +e
"$PYTHON" "$ROOT/src/verifier.py" --n 2 --primes 3 --quiet-pairs > "$REPRO/logs/toy_zero_python.log" 2>&1
rc_py_zero=$?
"$REPRO/bin/verifier_gmp" --n 2 --primes 3 --quiet-pairs > "$REPRO/logs/toy_zero_gmp.log" 2>&1
rc_cpp_zero=$?
"$PYTHON" "$ROOT/src/verifier.py" --n 5 --primes 3 --quiet-pairs > "$REPRO/logs/toy_p3_python.log" 2>&1
rc_py_p3=$?
"$REPRO/bin/verifier_gmp" --n 5 --primes 3 --quiet-pairs > "$REPRO/logs/toy_p3_gmp.log" 2>&1
rc_cpp_p3=$?
set -e
[[ "$rc_py_zero" -eq 1 && "$rc_cpp_zero" -eq 1 && "$rc_py_p3" -eq 1 && "$rc_cpp_p3" -eq 1 ]]
grep -q '^zero_remainder_count=1$' "$REPRO/logs/toy_zero_python.log"
grep -q '^zero_remainder_count=1$' "$REPRO/logs/toy_zero_gmp.log"

TOY_PRIMES='3,7,11,19'
set +e
"$PYTHON" "$ROOT/src/search_z3_direct.py" --low 2 --high 50 --C 3 --D 2 --primes "$TOY_PRIMES" \
  --timeout-ms 5000 --json "$REPRO/output/toy_A.json" > "$REPRO/logs/toy_A.log" 2>&1
rc_A=$?
"$PYTHON" "$ROOT/src/search_z3_cegis.py" --low 2 --high 50 --C 3 --D 2 --primes "$TOY_PRIMES" \
  --timeout-ms 2000 --max-iterations 50 --json "$REPRO/output/toy_B.json" \
  --jsonl "$REPRO/logs/toy_B.jsonl" > "$REPRO/logs/toy_B.log" 2>&1
rc_B=$?
"$REPRO/bin/search_bitset" --low 2 --high 50 --C 3 --D 2 --primes "$TOY_PRIMES" --window 31 \
  --json "$REPRO/output/toy_C.json" --quiet > "$REPRO/logs/toy_C.log" 2>&1
rc_C=$?
set -e
[[ "$rc_A" -eq 1 && "$rc_B" -eq 1 && "$rc_C" -eq 1 ]]

# Two direct enumeration algorithms versus Python brute force.
A303656_BIN="$REPRO/bin" "$PYTHON" "$ROOT/tests/direct_small_crosscheck.py" \
  > "$REPRO/logs/direct_small_crosscheck.log" 2>&1

# Exact factor classifiers versus Python/SymPy brute force.
"$PYTHON" "$ROOT/tests/factor_small_crosscheck.py" \
  --primary "$REPRO/bin/search_factor_sieve" \
  --clean "$REPRO/bin/search_factor_sieve_clean" \
  > "$REPRO/logs/factor_small_crosscheck.log" 2>&1

# Explicit valuation 3 and 5 branch probes.
for impl in search_factor_sieve search_factor_sieve_clean; do
  quiet=(); [[ "$impl" == search_factor_sieve ]] && quiet=(--quiet)
  "$REPRO/bin/$impl" --low 29 --high 29 --C 3 --D 2 --group-span 1000 --max-odd 1 \
    --json "$REPRO/output/${impl}_n29_v1.json" "${quiet[@]}" > "$REPRO/logs/${impl}_n29_v1.log"
  "$REPRO/bin/$impl" --low 29 --high 29 --C 3 --D 2 --group-span 1000 --max-odd 3 \
    --json "$REPRO/output/${impl}_n29_v3.json" "${quiet[@]}" > "$REPRO/logs/${impl}_n29_v3.log"
  "$REPRO/bin/$impl" --low 245 --high 245 --C 5 --D 4 --group-span 1000 --max-odd 3 \
    --json "$REPRO/output/${impl}_n245_v3.json" "${quiet[@]}" > "$REPRO/logs/${impl}_n245_v3.log"
  "$REPRO/bin/$impl" --low 245 --high 245 --C 5 --D 4 --group-span 1000 --max-odd -1 \
    --json "$REPRO/output/${impl}_n245_allodd.json" "${quiet[@]}" > "$REPRO/logs/${impl}_n245_allodd.log"
done
"$PYTHON" - "$REPRO" <<'PY'
import json, pathlib, sys
out = pathlib.Path(sys.argv[1]) / "output"
for impl in ("search_factor_sieve", "search_factor_sieve_clean"):
    a = json.loads((out / f"{impl}_n29_v1.json").read_text())
    b = json.loads((out / f"{impl}_n29_v3.json").read_text())
    c = json.loads((out / f"{impl}_n245_v3.json").read_text())
    d = json.loads((out / f"{impl}_n245_allodd.json").read_text())
    assert a["first_failure_histogram"][0]["shift"] == "2"
    assert b["first_failure_histogram"][0]["shift"] == "4"
    assert c["first_failure_histogram"][0]["shift"] == "2"
    assert d["first_failure_histogram"][0]["shift"] == "4"
print("valuation_branch_toys=PASS")
PY

# ---------------------------------------------------------------------------
# Dual all-prime factor search helpers.
# ---------------------------------------------------------------------------
run_factor_pair() {
  local lo="$1" hi="$2" maxodd="$3" tag="$4" C="$5" D="$6" span="$7"
  "$REPRO/bin/search_factor_sieve" --low "$lo" --high "$hi" --C "$C" --D "$D" \
    --group-span "$span" --max-odd "$maxodd" --json "$REPRO/output/${tag}_primary.json" --quiet \
    > "$REPRO/logs/${tag}_primary.log" 2>&1
  "$REPRO/bin/search_factor_sieve_clean" --low "$lo" --high "$hi" --C "$C" --D "$D" \
    --group-span "$span" --max-odd "$maxodd" --json "$REPRO/output/${tag}_clean.json" --quiet \
    > "$REPRO/logs/${tag}_clean.log" 2>&1
  "$PYTHON" - "$REPRO/output/${tag}_primary.json" "$REPRO/output/${tag}_clean.json" <<'PY'
import json, sys
A = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2]))
keys = ["low", "high", "C", "D", "finite_bound_3_rhs", "finite_bound_5_rhs",
        "max_odd", "admissible_pair_count_at_high", "distinct_shift_count_at_high",
        "integers_tested", "candidate_count", "candidates", "first_failure_histogram"]
assert all(A[k] == B[k] for k in keys)
assert A["candidate_count"] == 0
print("factor_pair_comparison=PASS")
PY
}

run_factor_chunked_empty() {
  local scanner="$1" maxodd="$2" tag="$3" lo="$4" hi="$5" C="$6" D="$7"
  local directory="$REPRO/chunks/$tag"
  mkdir -p "$directory"
  set +e
  "$PYTHON" "$ROOT/src/run_factor_chunks.py" --scanner "$scanner" --low "$lo" --high "$hi" \
    --chunk-size 10000000 --jobs "$JOBS" --C "$C" --D "$D" --group-span 5000000 \
    --max-odd "$maxodd" --out-dir "$directory" --summary "$REPRO/output/${tag}_summary.json" \
    > "$REPRO/logs/${tag}.log" 2>&1
  local rc=$?
  set -e
  [[ "$rc" -eq 1 ]]
}

compare_factor_dirs() {
  "$PYTHON" - "$1" "$2" <<'PY'
import json, pathlib, sys
def read(directory):
    out = {}
    for path in pathlib.Path(directory).glob("chunk_*.json"):
        data = json.loads(path.read_text())
        out[(data["low"], data["high"])] = data
    return out
A = read(sys.argv[1]); B = read(sys.argv[2]); assert A.keys() == B.keys() and A
keys = ["low", "high", "C", "D", "finite_bound_3_rhs", "finite_bound_5_rhs",
        "max_odd", "admissible_pair_count_at_high", "distinct_shift_count_at_high",
        "integers_tested", "candidate_count", "candidates", "first_failure_histogram"]
for key in A:
    assert all(A[key][field] == B[key][field] for field in keys)
    assert A[key]["candidate_count"] == 0
print("independent_factor_chunk_comparison=PASS")
PY
}

if [[ "$LEVEL" == quick ]]; then
  factor_high=240000100000
else
  factor_high=240010000000
fi
for mode in 1 3 -1; do
  case "$mode" in 1) name=exact1;; 3) name=odd13;; -1) name=allodd;; esac
  run_factor_pair 240000000001 "$factor_high" "$mode" "$name" 23 16 1000000
done

if [[ "$LEVEL" == certified100m || "$LEVEL" == full || "$LEVEL" == full1b || "$LEVEL" == full1p6b ]]; then
  for mode in 1 3 -1; do
    case "$mode" in 1) name=exact1;; 3) name=odd13;; -1) name=allodd;; esac
    run_factor_chunked_empty "$REPRO/bin/search_factor_sieve" "$mode" "${name}_primary_100m" 240000000001 240100000000 23 16
    run_factor_chunked_empty "$REPRO/bin/search_factor_sieve_clean" "$mode" "${name}_clean_100m" 240000000001 240100000000 23 16
    compare_factor_dirs "$REPRO/chunks/${name}_primary_100m" "$REPRO/chunks/${name}_clean_100m"
  done
fi

if [[ "$LEVEL" == full || "$LEVEL" == full1b || "$LEVEL" == full1p6b ]]; then
  run_factor_chunked_empty "$REPRO/bin/search_factor_sieve" 1 exact1_primary_band282 282300000001 282400000000 23 16
  run_factor_chunked_empty "$REPRO/bin/search_factor_sieve_clean" 1 exact1_clean_band282 282300000001 282400000000 23 16
  compare_factor_dirs "$REPRO/chunks/exact1_primary_band282" "$REPRO/chunks/exact1_clean_band282"
fi

# ---------------------------------------------------------------------------
# Dual direct enumeration of a^2+b^2.  Candidate emptiness here verifies the
# original representation statement itself on the stated finite interval.
# ---------------------------------------------------------------------------
run_direct_pair() {
  local lo="$1" hi="$2" C="$3" D="$4" tag="$5"
  local xdir="$REPRO/direct/${tag}_x" ydir="$REPRO/direct/${tag}_y"
  mkdir -p "$xdir" "$ydir"

  # Restart the runner every 100,000,000 integers.  The final aggregator still
  # enforces gap-free, non-overlapping coverage of the full requested interval.
  local band_lo="$lo" band_index=0 band_hi bx by btag
  while (( band_lo <= hi )); do
    band_hi=$((band_lo + 100000000 - 1))
    if (( band_hi > hi )); then band_hi="$hi"; fi
    btag=$(printf '%03d' "$band_index")
    bx="$REPRO/direct/${tag}_band${btag}_x"
    by="$REPRO/direct/${tag}_band${btag}_y"
    "$PYTHON" "$ROOT/src/run_twosquares_chunks.py" \
      --scanner "$REPRO/bin/search_twosquares_bitset" --source "$ROOT/src/search_twosquares_bitset.cpp" \
      --low "$band_lo" --high "$band_hi" --chunk-size 10000000 --jobs "$JOBS" --C "$C" --D "$D" \
      --out-dir "$bx" --summary "$REPRO/output/${tag}_band${btag}_x_summary.json" \
      > "$REPRO/logs/${tag}_band${btag}_x.log" 2>&1
    "$PYTHON" "$ROOT/src/run_twosquares_chunks.py" \
      --scanner "$REPRO/bin/search_twosquares_clean" --source "$ROOT/src/search_twosquares_clean.cpp" \
      --low "$band_lo" --high "$band_hi" --chunk-size 10000000 --jobs "$JOBS" --C "$C" --D "$D" \
      --out-dir "$by" --summary "$REPRO/output/${tag}_band${btag}_y_summary.json" \
      > "$REPRO/logs/${tag}_band${btag}_y.log" 2>&1
    cp "$bx"/chunk_*.json "$xdir"/
    cp "$bx"/chunk_*.candidates.txt "$xdir"/
    cp "$by"/chunk_*.json "$ydir"/
    cp "$by"/chunk_*.candidates.txt "$ydir"/
    band_lo=$((band_hi + 1))
    band_index=$((band_index + 1))
  done

  "$PYTHON" "$ROOT/src/aggregate_twosquares_dual.py" --x-dir "$xdir" --y-dir "$ydir" \
    --low "$lo" --high "$hi" --summary "$REPRO/output/${tag}_dual_summary.json" \
    > "$REPRO/logs/${tag}_dual.log" 2>&1
  "$PYTHON" - "$REPRO/output/${tag}_dual_summary.json" <<'PY'
import json, sys
z = json.load(open(sys.argv[1]))
assert z["complete_gapless_independent_crosscheck"]
assert z["candidate_count_x"] == z["candidate_count_y"] == 0
print("direct_pair_comparison=PASS")
PY
}

case "$LEVEL" in
  quick)
    run_direct_pair 240000000001 240000100000 23 16 direct_100k ;;
  certified10m)
    run_direct_pair 240000000001 240010000000 23 16 direct_10m ;;
  certified100m)
    run_direct_pair 240000000001 240100000000 23 16 direct_100m ;;
  full)
    run_direct_pair 240000000001 240100000000 23 16 direct_100m
    run_direct_pair 282420000001 282440000000 24 16 direct_cross_C24
    run_direct_pair 762930000001 762950000000 24 17 direct_cross_D17 ;;
  full1b)
    run_direct_pair 240000000001 241000000000 23 16 direct_1b
    run_direct_pair 282420000001 282440000000 24 16 direct_cross_C24
    run_direct_pair 762930000001 762950000000 24 17 direct_cross_D17 ;;
  full1p6b)
    run_direct_pair 240000000001 241600000000 23 16 direct_1p6b
    while read -r tag lo hi; do
      [[ -z "${tag:-}" || "$tag" == \#* ]] && continue
      run_direct_pair "$lo" "$hi" 23 16 "direct_far_${tag}"
    done < "$ROOT/output/direct/far_windows/windows.tsv"
    run_direct_pair 1000000000001 1000001000000 25 17 direct_log_1e12
    run_direct_pair 10000000000001 10000001000000 27 18 direct_log_1e13
    run_direct_pair 100000000000001 100000001000000 29 20 direct_log_1e14
    run_direct_pair 282420000001 282440000000 24 16 direct_cross_C24
    run_direct_pair 762930000001 762950000000 24 17 direct_cross_D17 ;;
esac

if [[ "$AUDIT_STORED" == "1" ]]; then
  "$PYTHON" "$ROOT/src/audit_formal_results.py" \
    --output "$REPRO/output/formal_results_audit.json" \
    > "$REPRO/logs/stored_formal_results_audit.log"
  "$PYTHON" "$ROOT/src/verify_direct_outputs.py" > "$REPRO/logs/stored_direct_outputs_audit.log"
fi

find "$REPRO" -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > "$REPRO/SHA256SUMS.txt"
echo "REPRODUCTION_PASS"
echo "level=$LEVEL"
echo "output_directory=$REPRO"
