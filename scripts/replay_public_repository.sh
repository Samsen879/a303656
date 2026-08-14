#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

python3 scripts/verify_public_repository.py

if [[ "${RUN_QUICK_FINITE_REPLAY:-0}" == "1" ]]; then
  python3 -m venv .venv
  . .venv/bin/activate
  python3 -m pip install -r requirements.txt
  SKIP_STAGE0=1 LEVEL=quick ./run_reproduce.sh
fi
