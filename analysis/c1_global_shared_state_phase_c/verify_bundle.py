#!/usr/bin/env python3
"""Verify local integrity and finite deterministic replay, not theorem correctness."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile

def main() -> None:
    root=Path(__file__).resolve().parent
    lines=(root/'SHA256SUMS.txt').read_text().splitlines()
    for line in lines:
        expected,name=line.split('  ',1)
        p=(root/name).resolve()
        if p.parent!=root:raise RuntimeError('Unexpected manifest path')
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual!=expected:raise RuntimeError(f'Checksum mismatch: {name}')
    with tempfile.TemporaryDirectory(prefix='a303656-shared-state-') as tmp:
        out=Path(tmp)/'results.json'
        subprocess.run([sys.executable,'-B',str(root/'reference.py'),'--output',str(out)],
                       cwd=root,check=True)
        if out.read_bytes()!=(root/'results.json').read_bytes():
            raise RuntimeError('Deterministic mathematical output mismatch')
    subprocess.run([sys.executable,'-B','-m','unittest','-v'],cwd=root,check=True)
    print(f'PASS: {len(lines)} file hashes; exact JSON replay; named unit tests.')
    print('Scope: local reference package only; no native repository replay or formal proof verification.')

if __name__=='__main__':main()
