#!/usr/bin/env python3
"""Verify package hashes (when present) and replay deterministic results in isolation."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise RuntimeError('Assertions must remain enabled; do not use -O/PYTHONOPTIMIZE.')
    base = Path(__file__).resolve().parent
    manifest = base / 'SHA256SUMS.txt'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            expected, name = line.split('  ', 1)
            path = (base / name).resolve()
            if not path.is_relative_to(base) or not path.is_file():
                raise RuntimeError(f'Invalid manifest path: {name}')
            if sha256(path) != expected:
                raise RuntimeError(f'Hash mismatch: {name}')
    deterministic = ['results.json', 'computed_summary.json']
    with tempfile.TemporaryDirectory(prefix='a303656-phase-c-replay-') as tmp:
        target = Path(tmp)
        shutil.copy2(base / 'reference.py', target / 'reference.py')
        env = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1')
        run = subprocess.run([sys.executable, str(target/'reference.py')],
                             capture_output=True, text=True, env=env, timeout=45)
        if run.returncode:
            raise RuntimeError('Reference replay failed:\n' + run.stdout + run.stderr)
        for name in deterministic:
            if (target/name).read_bytes() != (base/name).read_bytes():
                raise RuntimeError(f'Deterministic output differs: {name}')
    receipt = {'status':'PASS', 'fresh_isolated_reference_replay':'PASS',
               'deterministic_files':{name:sha256(base/name) for name in deterministic},
               'reference_sha256':sha256(base/'reference.py'),
               'timings_compared':False, 'repository_tests_run':False,
               'github_writes':'NONE'}
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
