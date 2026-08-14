#!/usr/bin/env python3
"""Fail-closed recursive validator for the Master V2 final-freeze candidate."""
from __future__ import annotations
import argparse,hashlib,io,json,re,sys,zipfile
from collections import Counter
from pathlib import PurePosixPath,Path

ROOT='A303656_POST_TRIGGER_MASTER_AUTHORITY_V2_FINAL_FREEZE_CANDIDATE'
TEXT={'.md','.txt','.json','.jsonl','.csv','.tsv','.py','.cpp','.cc','.c','.h','.hpp','.rs','.sh','.toml','.yaml','.yml','.tex','.log'}
ILLEGAL=set(range(0,9))|{11,12}|set(range(14,32))|{127}
REQUIRED_SOURCES={'SRC-018':'15496d228ebf6a49b0cc41bb1cc4d88594362ae9b694c7fa2cec6362f7b97909','SRC-019':'bd279152b0ce0820347dd77b7a6cb5e737a04dcf3048542aae1b4783b8dc21f9'}

def shab(b): return hashlib.sha256(b).hexdigest()
def badpath(n):
    p=PurePosixPath(n)
    return p.is_absolute() or '..' in p.parts or '\\' in n

def validate(path):
    errors=[];warnings=[];stats=Counter();physical=[];manifest_mismatches=[]
    raw=path.read_bytes()
    try: outer=zipfile.ZipFile(io.BytesIO(raw)); outer.testzip()
    except Exception as e: return {'verdict':'FAIL','errors':[f'outer ZIP: {e}']}
    names=[i.filename for i in outer.infolist() if not i.is_dir()]
    if any(badpath(n) for n in names): errors.append('unsafe outer member path')
    if len(names)!=len(set(names)): errors.append('duplicate outer member')
    prefix=ROOT+'/'
    if any(not n.startswith(prefix) for n in names): errors.append('incorrect root directory')
    members={n[len(prefix):]:outer.read(n) for n in names}
    required={'PACKAGE_MANIFEST.json','MACHINE_VERDICT.json','THEOREM_LEDGER.json','FINITE_COMPUTATION_LEDGER.json','FINITE_COMPUTATION_LEDGER.md','ROUTE_MATRIX.json','RESTART_GATE.json','SOURCE_ARCHIVE_INVENTORY.json','ARTIFACT_DEFECT_LEDGER.json','SHA256SUMS.txt','PACKAGE_FILE_LIST.txt','phase0_5_reconciliation/CONTROL_CHARACTER_LOGICAL_DEFECT_LEDGER.json','phase0_5_reconciliation/BOUNDED_NESTED_MANIFEST_RECONCILIATION.json'}
    missing=required-set(members)
    if missing: errors.append('missing required outer members: '+','.join(sorted(missing)))
    # Top-level JSON and clean text.
    for n,b in members.items():
        if PurePosixPath(n).suffix.lower() in TEXT:
            try: b.decode('utf-8')
            except UnicodeDecodeError: errors.append(f'non-UTF8 text: {n}');continue
            if any(x in ILLEGAL for x in b): errors.append(f'illegal C0/DEL outside raw nested archives: {n}')
        if n.endswith('.json'):
            try: json.loads(b)
            except Exception as e: errors.append(f'invalid JSON {n}: {e}')
    # Outer hash manifest and deterministic file list.
    if 'SHA256SUMS.txt' in members:
        seen=set()
        for line in members['SHA256SUMS.txt'].decode().splitlines():
            m=re.match(r'^([0-9a-f]{64})  (.+)$',line)
            if not m: errors.append('malformed outer SHA256SUMS line');continue
            h,n=m.groups();seen.add(n)
            if n not in members or shab(members[n])!=h: errors.append(f'outer manifest mismatch: {n}')
        expected=set(members)-{'SHA256SUMS.txt'}
        if seen!=expected: errors.append(f'outer manifest coverage mismatch missing={sorted(expected-seen)} extra={sorted(seen-expected)}')
    if 'PACKAGE_FILE_LIST.txt' in members:
        listed=set(members['PACKAGE_FILE_LIST.txt'].decode().splitlines())
        expected=set(members)-{'PACKAGE_FILE_LIST.txt','SHA256SUMS.txt'}
        if listed!=expected: errors.append('PACKAGE_FILE_LIST coverage mismatch')
    # Machine authority and ledger constraints.
    machine=json.loads(members['MACHINE_VERDICT.json'])
    exact={'master_authority_v2':'FINAL FREEZE CANDIDATE — PENDING INDEPENDENT WEB EXACT-HASH AUDIT','project':'PAUSED','active_promoted_route':'NONE','low_cost_generic_theorem_hunts':'NOT ACTIVE','targeted_restart':'ONLY ON EXPLICIT RESTART GATE','codex_large_scale_research':'NOT AUTHORIZED','codex_ultra':'NOT AUTHORIZED','a303656':'UNRESOLVED'}
    for k,v in exact.items():
        if machine.get(k)!=v: errors.append(f'machine verdict {k} != {v}')
    if machine.get('general_proof_obtained') is not False or machine.get('certified_counterexample_found') is not False: errors.append('solution-state contradiction')
    theorem=json.loads(members['THEOREM_LEDGER.json']); ids=[x['id'] for x in theorem['entries']]
    if len(ids)!=len(set(ids)): errors.append('duplicate theorem/conditional ID')
    for i in {'N-004','N-009','N-010','C-001'}:
        if i not in ids: errors.append(f'missing required authority ID {i}')
    byid={x['id']:x for x in theorem['entries']}
    if byid.get('N-004',{}).get('source_ids')!=['SRC-005']: errors.append('N-004 remains source-conflated')
    n004=byid.get('N-004',{})
    if 'O(sqrt(X) log X)' not in n004.get('statement','') or 'absolute-minor-spectrum / F3 localization mechanism' not in n004.get('statement',''):
        errors.append('N-004 mechanism-specific scale statement missing')
    if 'not asserted as a universal necessary threshold for all future exceptional-set inverse methods' not in n004.get('scope_limit',''):
        errors.append('N-004 universal-threshold disclaimer missing')
    n009=byid.get('N-009',{})
    if 'arbitrarily large finite active-shift restrictions' not in n009.get('statement','') or 'arbitrarily large Helly obstructions' not in n009.get('statement',''):
        errors.append('N-009 finite-restriction Helly statement missing')
    if 'does not prove that the complete D(n) actual-mask family itself has unbounded Helly number' not in n009.get('scope_limit',''):
        errors.append('N-009 complete-family disclaimer missing')
    if byid.get('N-010',{}).get('source_ids')!=['SRC-018','SRC-019']: errors.append('N-010 sources incorrect')
    if byid.get('C-001',{}).get('classification')!='ACCEPTED CONDITIONAL IMPLICATION' or 'NOT ESTABLISHED' not in byid.get('C-001',{}).get('scope_limit',''): errors.append('CRW conditional discipline missing')
    finite=json.loads(members['FINITE_COMPUTATION_LEDGER.json']);fids=[x['id'] for x in finite['entries']]
    if len(fids)!=len(set(fids)): errors.append('duplicate finite ID')
    fmd=members['FINITE_COMPUTATION_LEDGER.md'].decode()
    for e in finite['entries']:
        if not e.get('explicit_bounds') or e['explicit_bounds'] not in fmd: errors.append(f'finite JSON/Markdown explicit_bounds mismatch: {e["id"]}')
    routes=json.loads(members['ROUTE_MATRIX.json']);rids=[x['id'] for x in routes['routes']]
    if len(rids)!=len(set(rids)): errors.append('duplicate route ID')
    restart=json.loads(members['RESTART_GATE.json'])
    if restart.get('status')!='FAIL_CLOSED' or len(restart.get('allowed_triggers',[]))!=7: errors.append('restart gate not fail-closed/complete')
    sources=json.loads(members['SOURCE_ARCHIVE_INVENTORY.json']);sids=[x['id'] for x in sources['archives']]
    if len(sids)!=len(set(sids)): errors.append('duplicate source ID')
    for sid,h in REQUIRED_SOURCES.items():
        e=next((x for x in sources['archives'] if x['id']==sid),None)
        if not e or e['sha256']!=h or shab(members.get(e.get('package_path',''),b''))!=h: errors.append(f'required source custody mismatch: {sid}')
    ah='56c018791780e5037f2f5394266c05aecff8bea5e3a3238fedef84cfe83df57b'
    if shab(members.get('independent_audits/A303656_MASTER_AUTHORITY_INDEPENDENT_AUDIT_20260729.zip',b''))!=ah: errors.append('independent audit custody mismatch')

    allow=json.loads(members['phase0_5_reconciliation/BOUNDED_NESTED_MANIFEST_RECONCILIATION.json'])['rows']
    allowed={(x['manifest_expected_sha256'],x['actual_sha256']) for x in allow}
    logical=json.loads(members['phase0_5_reconciliation/CONTROL_CHARACTER_LOGICAL_DEFECT_LEDGER.json'])
    known={(x['byte_value'],x['byte_offset'],x['escaped_context']) for x in logical['entries']}

    def scan_zip(data,label,depth=0):
        if depth>6: errors.append(f'nested ZIP depth exceeded: {label}');return
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                if z.testzip(): errors.append(f'ZIP CRC failure: {label}')
                infos=[i for i in z.infolist() if not i.is_dir()]
                if len({i.filename for i in infos})!=len(infos): errors.append(f'duplicate nested member: {label}')
                if any(badpath(i.filename) for i in infos): errors.append(f'unsafe nested path: {label}')
                blobs={i.filename:z.read(i) for i in infos}
                for n,b in blobs.items():
                    child=label+'!/'+n
                    ext=PurePosixPath(n).suffix.lower()
                    if ext in TEXT:
                        try: b.decode('utf-8')
                        except UnicodeDecodeError: errors.append(f'non-UTF8 expected text: {child}')
                        for off,val in enumerate(b):
                            if val in ILLEGAL:
                                ctx=b[max(0,off-28):off+29].decode('utf-8','backslashreplace').encode('unicode_escape').decode('ascii')
                                fp=(f'0x{val:02X}',off,ctx);physical.append((child,fp))
                                if fp not in known: errors.append(f'unledgered control defect: {child}@{off}')
                    if ext=='.zip': scan_zip(b,child,depth+1)
                for mn,mb in blobs.items():
                    if PurePosixPath(mn).name not in {'SHA256SUMS','SHA256SUMS.txt'}: continue
                    try: lines=mb.decode('utf-8').splitlines()
                    except UnicodeDecodeError: continue
                    base=PurePosixPath(mn).parent
                    for line in lines:
                        m=re.match(r'^([0-9a-fA-F]{64})\s+[* ]?(.+)$',line)
                        if not m: continue
                        exp,target=m.group(1).lower(),str(base/PurePosixPath(m.group(2)))
                        if target not in blobs: continue
                        act=shab(blobs[target])
                        if act!=exp:
                            manifest_mismatches.append((label,mn,target,exp,act))
                            if (exp,act) not in allowed: errors.append(f'unallowlisted nested manifest mismatch: {label}!/{mn} -> {target}')
        except zipfile.BadZipFile: errors.append(f'bad nested ZIP: {label}')
    for e in sources['archives']:
        scan_zip(members[e['package_path']],e['package_path'])
    # The 20 defect records occur in four stale manifests; all must be observed.
    if len(manifest_mismatches)!=20: errors.append(f'nested manifest mismatch count {len(manifest_mismatches)} != 20')
    observed_known={fp for _,fp in physical}
    if observed_known!=known: errors.append(f'control-defect fingerprint coverage mismatch observed={len(observed_known)} ledger={len(known)}')
    stats.update({'outer_file_count':len(members),'nested_manifest_mismatch_count':len(manifest_mismatches),'logical_control_defect_count':len(observed_known),'physical_control_occurrence_count_in_candidate':len(physical),'phase0_physical_control_occurrence_count':logical['physical_copy_occurrence_count'],'repaired_derivative_count':0})
    return {'schema':'a303656-master-v2-final-freeze-recursive-validation-v1','verdict':'PASS' if not errors else 'FAIL','validator_scope':'Artifact, ledger, custody, manifest, recursive archive, explicit N-004/N-009 scope guards, and governance consistency; not independent proof validation.','errors':errors,'warnings':warnings,'statistics':dict(stats)}

def main():
    p=argparse.ArgumentParser();p.add_argument('zip',type=Path);p.add_argument('--json-output',type=Path);a=p.parse_args();r=validate(a.zip)
    text=json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2);print(text)
    if a.json_output:a.json_output.write_text(text+'\n',encoding='utf-8')
    raise SystemExit(0 if r['verdict']=='PASS' else 1)
if __name__=='__main__':main()
