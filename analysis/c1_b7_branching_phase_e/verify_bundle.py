#!/usr/bin/env python3
"""Verify package SHA256 custody; optionally replay deterministic finite checks."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

OUTPUTS = ('results.json', 'C4_FORK_120.json', 'C4_FORK_120.txt',
           'ACTUAL_REGULAR_CERTIFICATES.json')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    protected: set[str] = set()
    for line in (base / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = (base / name).resolve()
        if path.parent != base or name in protected or len(expected) != 64:
            raise ValueError('invalid manifest entry')
        protected.add(name)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('checksum mismatch: ' + name)
    present = {p.name for p in base.iterdir() if p.is_file() and p.name != 'SHA256SUMS.txt'}
    if protected != present:
        raise ValueError('manifest/file set mismatch')
    print(f'SHA256: PASS ({len(protected)} protected files)')
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='b7-phase-e-') as tmp:
            completed = subprocess.run(
                [sys.executable, '-B', str(base / 'reference.py'), '--output-dir', tmp],
                check=True, capture_output=True, text=True,
            )
            parsed = json.loads(completed.stdout)
            if parsed.get('status') != 'PASS':
                raise ValueError('reference did not return PASS')
            for name in OUTPUTS:
                if (base / name).read_bytes() != (Path(tmp) / name).read_bytes():
                    raise ValueError('fresh replay mismatch: ' + name)
        print('FRESH REPLAY: PASS (4 outputs BYTE_IDENTICAL)')
        print(completed.stdout.strip())

if __name__ == '__main__':
    main()
