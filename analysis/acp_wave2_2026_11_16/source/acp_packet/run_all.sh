#!/bin/sh
# One-command replay of every certificate of the ACP package (A303656).
#   ./run_all.sh                 quick mode (~22 min on 2 cores): verifies all stored certificates exactly
#   ./run_all.sh full            also rebuilds the catalogue (gcd of two ~10^9-bit numbers) and all
#                                fibre statistics from scratch and compares them with the stored files (~20 min more)
#   ./run_all.sh full lp         additionally re-runs the LP searches that produced the measures nu0
#   AUDIT=/path/to/A303656_Triage_Audit_2026-11-14 ./run_all.sh   also compares with the frozen C21 certificate
# Requirements: python3 (>=3.9), numpy, gmpy2, ortools (only toy_1d.py); scipy only for "lp".
set -e
cd "$(dirname "$0")"
MODE=${1:-quick}; LP=${2:-}
mkdir -p logs out
echo "== 1. Phase-1 validation suite"
python3 src/validate.py $AUDIT | tee logs/validate.log | tail -3
if [ "$MODE" = "full" ]; then
  echo "== 2. rebuild catalogue B=32768 and fibre statistics from scratch"
  python3 src/build_catalogue.py 32768 out/catalogue_B32768.json | tee logs/catalogue_rebuild.log
  python3 src/compute_weights.py out/catalogue_B32768.json out/weights_B32768.json | tail -1
  python3 - <<'PY'
import json
a=json.load(open('out/catalogue_B32768.json')); b=json.load(open('certs/catalogue_B32768.json'))
assert a==b, "catalogue differs"
a=json.load(open('out/weights_B32768.json')); b=json.load(open('certs/weights_B32768.json'))
assert a==b, "weights differ"
print("[PASS] rebuilt catalogue and weights are identical to the stored certificates")
PY
  if [ "$LP" = "lp" ]; then
    for c in 00 01 10 11; do python3 src/search_lp.py certs/weights_B32768.json 16384 45 $c out/nu_c$c.json | tail -2; done
  fi
fi
echo "== 3. independent catalogue checks (primality, orders, completeness by brute-force scan and modular route)"
python3 src/verify_catalogue.py certs/catalogue_B32768.json 110000000 2048 | tee logs/verify_catalogue.log
echo "== 4. independent recomputation of fibre statistics"
python3 src/verify_weights.py certs/weights_B32768.json | tee logs/verify_weights.log
echo "== 5. Theorem A (no covering with all H_p < 16384): exact check of the four measure certificates"
for c in 00 01 10 11; do
  python3 src/verify_lp_cert.py certs/weights_B32768.json certs/nu_B16384_N45_c$c.json out/theoremA_c$c.json | grep -E '"status"|"class"|bound_float'
done
echo "== 6. Theorem R (K-target theorem): exact budgets"
python3 src/verify_root_budget.py certs/weights_B32768.json 29 out/theoremR_haar_K29.json haar | tee logs/theoremR_haar.log
python3 src/verify_root_budget.py certs/weights_B32768.json 146 out/theoremR_K146.json \
  certs/nu_B16384_N45_c00.json certs/nu_B16384_N45_c01.json certs/nu_B16384_N45_c10.json certs/nu_B16384_N45_c11.json | tee logs/theoremR_K146.log
echo "== 7. Proposition H (horizon of all measure arguments)"
python3 src/horizon.py out/horizon.json
echo "== 8. Phase 2B: M = t frontier (Lemma L4 brute force, census, explicit local tiling)"
python3 src/frontier.py certs/weights_B32768.json out/frontier.json | tee logs/frontier.log
echo "== 9. one-parameter controls (CP-SAT, time-limited instances may report UNKNOWN)"
python3 src/toy_1d.py certs/weights_B32768.json out/toy_1d.json | cut -c1-400 | tee logs/toy_1d_replay.log
echo "ALL CERTIFICATES REPLAYED"
