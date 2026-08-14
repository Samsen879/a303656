#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

CXX=${CXX:-g++}
$CXX -O3 -std=c++17 src/verify_pruning.cpp -lgmpxx -lgmp -o verify_pruning
./verify_pruning cert/gcd_factor_B5000.txt output/primes_B5000_verified.csv | tee logs/verify_pruning.log

python src/method_a_bitset.py \
  --primes 7,11 --max-universe 1000000 \
  --json output/method_a_7_11.json | tee logs/method_a_7_11.log

python src/method_b_lazy.py \
  --primes 7,11,19 --disable-pruning --disable-heuristic \
  --max-iterations 1 --candidate-timeout-ms 5000 --oracle-timeout-ms 30000 \
  --json output/method_b_exact_oracle_7_11_19.json \
  | tee logs/method_b_exact_oracle_7_11_19.log

# Optional: regenerate the factorization certificate from scratch.
# This requires SymPy and takes longer than merely checking the certificate.
if [[ "${REGENERATE_CERT:-0}" == "1" ]]; then
  $CXX -O3 -std=c++17 src/generate_gcd.cpp -lgmpxx -lgmp -o generate_gcd
  ./generate_gcd 5000 output/G5000.hex
  python src/factor_gcd.py 5000 output/G5000.hex output/gcd_factor_B5000.regenerated.txt
  cmp output/gcd_factor_B5000.regenerated.txt cert/gcd_factor_B5000.txt
fi
