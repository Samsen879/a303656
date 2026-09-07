#!/usr/bin/env python3
"""Read-only payload verification and optional exact standalone replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def verify_bytes() -> int:
    expected = set()
    for line in (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        digest, relative = line.split('  ', 1)
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise RuntimeError(f'Invalid payload path: {relative}')
        if relative in expected:
            raise RuntimeError(f'Duplicate payload entry: {relative}')
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'Payload checksum mismatch: {relative}')
        expected.add(relative)
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts
              and p.name != 'SHA256SUMS.txt'}
    if expected != actual:
        raise RuntimeError(f'Inventory mismatch: {sorted(expected ^ actual)}')
    return len(expected)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    count = verify_bytes()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='a303656_order_dag_phase_c_') as tmp:
            out = Path(tmp) / 'results'
            result = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'reference.py'), '--output-dir', str(out)],
                check=True, capture_output=True, text=True)
            expected = json.loads((ROOT/'results/reference_results.json').read_text())
            actual = json.loads((out/'reference_results.json').read_text())
            if expected != actual:
                raise RuntimeError('Exact mathematical replay differs from frozen output')
            tests = subprocess.run(
                [sys.executable, '-B', '-m', 'unittest', '-v'], cwd=ROOT,
                check=True, capture_output=True, text=True)
            print(result.stdout.strip())
            print(tests.stderr.strip())
    print(json.dumps({'integrity': 'PASS', 'payload_files': count,
                      'exact_mathematical_replay': 'PASS' if args.replay else 'NOT RUN',
                      'repository_native_replay': False, 'github_writes': 'NONE'}, indent=2))


if __name__ == '__main__':
    main()
