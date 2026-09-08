#!/usr/bin/env python3
"""Verify local payload hashes and optionally replay without changing frozen files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    if not __debug__:
        raise RuntimeError('Run without -O.')
    entries={}
    for line in (root/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        digest,name=line.split('  ',1)
        path=(root/name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f'Invalid payload path: {name}')
        if name in entries:
            raise ValueError(f'Duplicate manifest entry: {name}')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Hash mismatch: {name}')
        entries[name]=digest
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt'}
    if actual!=set(entries):
        raise ValueError('Payload file set differs from checksum manifest.')
    expected=(root/'results.json').read_bytes()
    data=json.loads(expected)
    if data['assertion_failures']!=0 or data['github_writes']!='NONE':
        raise ValueError('Unexpected result status.')
    replayed=False
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='a303656-provider-') as tmp:
            output=Path(tmp)/'results.json'
            subprocess.run([sys.executable,'-B',str(root/'reference.py'),
                            '--output',str(output)],check=True,capture_output=True,text=True)
            if output.read_bytes()!=expected:
                raise ValueError('Reference replay differs from frozen results.')
            replayed=True
    print(json.dumps({'hashes':'PASS','payload_files':len(entries),
                      'reference_replay':'BYTE_IDENTICAL' if replayed else 'NOT_REQUESTED',
                      'github_access':False},indent=2))


if __name__=='__main__':
    main()
