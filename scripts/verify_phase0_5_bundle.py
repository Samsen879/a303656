#!/usr/bin/env python3
"""Validate the deterministic Phase 0.5 reconciliation bundle."""
import argparse,hashlib,re,zipfile
from pathlib import PurePosixPath,Path
ROOT='A303656_PHASE0_5_AUTHORITY_RECONCILIATION_20260813';TEXT={'.md','.txt','.json','.csv','.py'};BAD=set(range(0,9))|{11,12}|set(range(14,32))|{127}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('zip',type=Path);a=p.parse_args();errs=[]
 with zipfile.ZipFile(a.zip) as z:
  if z.testzip():errs.append('CRC')
  blobs={n.split('/',1)[1]:z.read(n) for n in z.namelist() if not n.endswith('/')}
  req={'reports/EXECUTIVE_VERDICT.md','reports/MASTER_V2_VALIDATION_REPORT.md','reports/WEB_AUTHORITY_CUSTODY.json','MASTER_V2_REFERENCE.json','GIT_COMMIT_LIST.txt','CHANGE_RECORD.txt','SHA256SUMS','scripts/build_phase0_5_bundle.py','scripts/verify_phase0_5_bundle.py'}
  if req-set(blobs):errs.append('missing:'+','.join(sorted(req-set(blobs))))
  for n,b in blobs.items():
   if PurePosixPath(n).suffix.lower() in TEXT:
    try:b.decode('utf-8')
    except UnicodeDecodeError:errs.append('UTF8:'+n)
    if any(x in BAD for x in b):errs.append('C0:'+n)
  seen=set()
  for line in blobs['SHA256SUMS'].decode().splitlines():
   m=re.match(r'^([0-9a-f]{64})  (.+)$',line)
   if not m:errs.append('manifest syntax');continue
   h,n=m.groups();seen.add(n)
   if n not in blobs or sha(blobs[n])!=h:errs.append('hash:'+n)
  if seen!=set(blobs)-{'SHA256SUMS'}:errs.append('manifest coverage')
 print('PASS' if not errs else 'FAIL\n'+'\n'.join(errs));raise SystemExit(bool(errs))
if __name__=='__main__':main()
