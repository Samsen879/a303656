#!/usr/bin/env python3
"""Verify the sealed package manifest, rejecting missing/corrupted/unlisted files."""
import hashlib
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]

def verify(root=ROOT):
    root=Path(root).resolve();manifest=root/'SHA256SUMS.txt'
    expected={}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest,name=line.split('  ',1)
        path=(root/name).resolve()
        if not path.is_relative_to(root) or name in expected:
            raise ValueError('invalid or duplicate manifest path')
        if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('invalid SHA256')
        if not path.is_file():raise FileNotFoundError(name)
        got=hashlib.sha256(path.read_bytes()).hexdigest()
        if got!=digest:raise AssertionError(f'checksum mismatch: {name}')
        expected[name]=digest
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
            and p!=root/'SHA256SUMS.txt' and '__pycache__' not in p.parts}
    if actual!=set(expected):raise AssertionError(f'unlisted/missing files: {actual^set(expected)}')
    return len(expected)

if __name__=='__main__':
    try:print(f'PASS: {verify()} protected files')
    except (OSError,ValueError,AssertionError) as e:
        print(f'FAIL: {e}',file=sys.stderr);raise SystemExit(1)
