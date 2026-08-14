#!/usr/bin/env python3
"""Generate exact-hash custody metadata without modifying authority ZIP bytes."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path

def sha256(path):
    digest=hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''): digest.update(block)
    return digest.hexdigest()

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--repo',type=Path,required=True); parser.add_argument('--import-commit',default='PENDING_FIRST_CUSTODY_COMMIT'); args=parser.parse_args(); repo=args.repo.resolve()
    v1=repo/'authority/audits/A303656_POST_TRIGGER_MASTER_AUTHORITY_AND_RESTART_GATE_REVIEW_V1_PRE_FINAL.zip'
    with zipfile.ZipFile(v1) as archive:
        name=next(n for n in archive.namelist() if n.endswith('/SOURCE_ARCHIVE_INVENTORY.json'))
        old=json.loads(archive.read(name).decode('utf-8'))['archives']
    records=[]
    for row in old:
        path=repo/'authority/raw'/row['canonical_name']
        records.append({'artifact_id':row['id'],'artifact_filename':path.name,'repository_path':path.relative_to(repo).as_posix(),'sha256':row['sha256'],'size_bytes':path.stat().st_size,'exact_hash_verified':sha256(path)==row['sha256'],'custody_source':'WEB-CUSTODIED / PHASE0 LOCAL EXACT-MATCH','date_imported':'2026-08-13','import_branch':'audit/authority-reconciliation-v2','import_commit':args.import_commit,'web_authority_status':row['adjudication'],'historical_generation_provenance':'NOT RETROACTIVELY ESTABLISHED BY GIT IMPORT','known_defects':'See Phase 0.5 logical-defect and manifest reconciliation ledgers'})
    additions=[
      ('SRC-018','authority/raw/A303656_THETA_SERIES_POINTWISE_PHASE_A_DETERMINISTIC.zip','15496d228ebf6a49b0cc41bb1cc4d88594362ae9b694c7fa2cec6362f7b97909','WEB-CUSTODIED / USER-DOWNLOADED','ACCEPTED AS ROUTE-CLOSURE AUDIT'),
      ('SRC-019','authority/raw/A303656_SECOND_THREE_TRIGGER_COMPARATIVE_AUDIT.zip','bd279152b0ce0820347dd77b7a6cb5e737a04dcf3048542aae1b4783b8dc21f9','WEB-CUSTODIED / USER-DOWNLOADED','INDEPENDENT COMPARATIVE ADJUDICATION'),
      ('AUD-001','authority/audits/A303656_MASTER_AUTHORITY_INDEPENDENT_AUDIT_20260729.zip','56c018791780e5037f2f5394266c05aecff8bea5e3a3238fedef84cfe83df57b','WEB-CUSTODIED / USER-DOWNLOADED','INDEPENDENT AUDIT / V2 BLOCKER AUTHORITY'),
      ('MASTER-V1','authority/audits/A303656_POST_TRIGGER_MASTER_AUTHORITY_AND_RESTART_GATE_REVIEW_V1_PRE_FINAL.zip','904c9c0d0ed6b1a496f1e25591b4ce6f9b1401200c18f40263c899c337ce08b2','PHASE0 LOCAL EXACT-MATCH','PRE-FINAL AUTHORITY DRAFT / SUPERSEDED BY V2 CANDIDATE WHEN GENERATED')]
    for aid,relative,expected,source,status in additions:
        path=repo/relative
        records.append({'artifact_id':aid,'artifact_filename':path.name,'repository_path':relative,'sha256':expected,'size_bytes':path.stat().st_size,'exact_hash_verified':sha256(path)==expected,'custody_source':source,'date_imported':'2026-08-13','import_branch':'audit/authority-reconciliation-v2','import_commit':args.import_commit,'web_authority_status':status,'historical_generation_provenance':'NOT RETROACTIVELY ESTABLISHED BY GIT IMPORT','known_defects':'See Phase 0.5 reconciliation ledgers'})
    if not all(r['exact_hash_verified'] for r in records): raise SystemExit('custody hash verification failed')
    payload={'schema':'a303656-web-authority-custody-v2-candidate','generated_date':'2026-08-13','frozen_repository_head':'23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67','statement':'The Git import commit establishes repository custody. It does NOT retroactively establish original generation provenance.','artifact_count':len(records),'artifacts':records}
    write_json(repo/'authority/manifests/WEB_AUTHORITY_CUSTODY.json',payload)
    lines=['# Web authority custody','','The Git import commit establishes repository custody. It does **not** retroactively establish original generation provenance.','','| ID | Repository path | SHA256 | Exact | Web status |','|---|---|---|---|---|']
    for r in records: lines.append(f"| {r['artifact_id']} | `{r['repository_path']}` | `{r['sha256']}` | {'YES' if r['exact_hash_verified'] else 'NO'} | {r['web_authority_status']} |")
    (repo/'authority/manifests/WEB_AUTHORITY_CUSTODY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PASS','artifact_count':len(records)},sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
