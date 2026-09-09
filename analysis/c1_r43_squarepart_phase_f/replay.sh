#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p .local-bin
python3 verify_python.py --mutations
c++ -O2 verify_native.cpp -lgmpxx -lgmp -o .local-bin/verify_native
.local-bin/verify_native .
c++ -O3 ecm_reference.cpp -lgmpxx -lgmp -o .local-bin/ecm_reference
# Deterministically reproduce the new 24-digit prime factor, not a random run.
.local-bin/ecm_reference C1806.txt 100000 5000000 1 810047
if [[ "${1:-}" == "--trial" ]]; then
 c++ -O3 trial.cpp -lgmpxx -lgmp -o .local-bin/trial
 .local-bin/trial C903.txt 1000000000000
 .local-bin/trial C1806.txt 1000000000000
fi
