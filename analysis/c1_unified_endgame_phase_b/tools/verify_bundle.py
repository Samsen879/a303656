#!/usr/bin/env python3
"""Verify byte integrity and optionally exact mathematical replay, without modifying the bundle."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def canonical(obj):
    if isinstance(obj, dict):
        return {k: canonical(v) for k, v in obj.items() if k != 'seconds'}
    if isinstance(obj, list):
        return [canonical(x) for x in obj]
    return obj


def math_hash(path: Path) -> str:
    obj = canonical(json.loads(path.read_text(encoding='utf-8')))
    data = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def verify_bytes():
    manifest = ROOT / 'SHA256SUMS.txt'
    expected = set()
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest, rel = line.split('  ', 1)
        target = (ROOT / rel).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            raise RuntimeError(f'Invalid or missing payload: {rel}')
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'Byte hash mismatch: {rel}')
        expected.add(rel)
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.name != 'SHA256SUMS.txt'}
    if actual != expected:
        raise RuntimeError(f'Manifest inventory mismatch: {sorted(actual ^ expected)}')
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    count = verify_bytes()
    hashes = json.loads((ROOT / 'results/math_hashes.json').read_text(encoding='utf-8'))
    for name, digest in hashes['generated_json'].items():
        if math_hash(ROOT / 'results' / name) != digest:
            raise RuntimeError(f'Frozen mathematical hash mismatch: {name}')
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='a303656_phase_b_') as tmp:
            out = Path(tmp) / 'replay'
            subprocess.run([sys.executable, '-B', str(ROOT/'tools/reference.py'), '--output-dir', str(out)],
                           check=True, capture_output=True, text=True)
            for name, digest in hashes['generated_json'].items():
                if math_hash(out / name) != digest:
                    raise RuntimeError(f'Replay mathematical mismatch: {name}')
            tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                                   cwd=ROOT, check=True, capture_output=True, text=True)
            print(tests.stderr.strip())
    print(json.dumps({'byte_payload_files': count, 'generated_json_files': len(hashes['generated_json']),
                      'replay': args.replay, 'integrity': 'PASS', 'mathematical_equality': 'PASS',
                      'github_writes': 'NONE'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
