#!/usr/bin/env python3
"""Rebuild all gate-v2 results from checked-in authorities, with raw return codes."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from common import sha256_file, write_json


def run(cmd: list[str], root: Path, log: Path) -> int:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(cmd, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    log.write_text(p.stdout)
    return p.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args(); root=a.root.resolve(); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    logs=out/"logs"; logs.mkdir(exist_ok=True); tools=root/"analysis/p4_prospective_gate_v2/tools"
    steps = [
        ("registry", [sys.executable,str(tools/"build_registry.py"),"--root",str(root),"--output",str(out)]),
        ("candidates", [sys.executable,str(tools/"build_candidates.py"),"--root",str(root),"--registry",str(out/"historical_exposure_registry.json"),"--output",str(out)]),
        ("results", [sys.executable,str(tools/"build_results.py"),"--root",str(root),"--output",str(out)]),
        ("verify", [sys.executable,str(tools/"verifier.py"),"--root",str(root),"--results",str(out)]),
        ("corruptions", [sys.executable,str(tools/"run_corruption_tests.py"),"--root",str(root),"--results",str(out),"--output",str(out/"corruption_tests.json")]),
    ]
    codes={}
    for name,cmd in steps:
        codes[name]=run(cmd,root,logs/f"{name}.log")
        if codes[name] != 0:
            write_json(out/"return_codes.json",codes); return codes[name]
    write_json(out/"return_codes.json",codes)
    files={p.relative_to(out).as_posix():sha256_file(p) for p in sorted(out.rglob("*")) if p.is_file() and p.name not in ("result_manifest.json",)}
    write_json(out/"result_manifest.json",{"schema":"a303656-p4-gate-v2-result-manifest-v1","files":files,"all_raw_return_codes_zero":all(v==0 for v in codes.values())})
    return 0


if __name__ == "__main__": raise SystemExit(main())
