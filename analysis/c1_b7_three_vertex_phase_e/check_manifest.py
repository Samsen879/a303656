"""Verify local payload integrity; does not replace mathematical replay."""
from pathlib import Path
import hashlib
p=Path(__file__).resolve().parent
lines=(p/'SHA256SUMS.txt').read_text().splitlines()
for line in lines:
 expected,name=line.split('  ',1)
 actual=hashlib.sha256((p/name).read_bytes()).hexdigest()
 if actual!=expected:raise SystemExit('HASH MISMATCH: '+name)
print('PASS:',len(lines),'payload SHA256 hashes')
