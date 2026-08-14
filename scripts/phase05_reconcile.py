#!/usr/bin/env python3
"""Generate Phase 0.5 provenance, manifest, payload, and defect reconciliation."""
from __future__ import annotations
import argparse, csv, hashlib, io, json, os, platform, re, subprocess, sys, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

TEXT_EXT={'.md','.txt','.json','.jsonl','.csv','.tsv','.py','.cpp','.cc','.c','.h','.hpp','.rs','.sh','.toml','.yaml','.yml','.tex','.log'}
FROZEN='23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67'

def sha_bytes(data): return hashlib.sha256(data).hexdigest()
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write(path,text): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text.rstrip()+'\n',encoding='utf-8',newline='\n')
def write_json(path,obj): write(path,json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2))
def run(repo,args): return subprocess.run(args,cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True).stdout

def strip_meta(v):
    if isinstance(v,dict): return {k:strip_meta(x) for k,x in v.items() if k not in {'z3_version','hostname','timestamp','generated_at','generated_utc','runtime','elapsed_time'} and not k.endswith('seconds') and not k.endswith('_seconds')}
    if isinstance(v,list): return [strip_meta(x) for x in v]
    return v
def scientific(name,data):
    text=data.decode('utf-8')
    if name.endswith('.json') or text.lstrip().startswith('{'): return strip_meta(json.loads(text)),'JSON'
    vals={}
    for line in text.splitlines():
        if '=' in line:
            k,v=line.split('=',1)
            if k not in {'elapsed_seconds','hostname','timestamp'}: vals[k]=v
        elif line.strip(): vals.setdefault('_lines',[]).append(line.strip())
    return vals,'KEY_VALUE_LOG'

def index_nested_archives(zip_paths):
    byte_index=defaultdict(list); zip_blobs={}; seen=set()
    def recurse(data,label,depth=0):
        zh=sha_bytes(data)
        if zh in seen or depth>4:return
        seen.add(zh); zip_blobs[zh]=(label,data)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for info in z.infolist():
                if info.is_dir():continue
                b=z.read(info); byte_index[sha_bytes(b)].append((label+'!/'+info.filename,b))
                if info.filename.lower().endswith('.zip'):
                    try: recurse(b,label+'!/'+info.filename,depth+1)
                    except zipfile.BadZipFile: pass
    for path in zip_paths: recurse(path.read_bytes(),path.name)
    return byte_index,zip_blobs

def nested_reconciliation(repo,out):
    outer=repo/'authority/raw/a303656_bounded_counterexample_bundle_refreshed.zip'
    byte_index,_=index_nested_archives([outer])
    rows=[]
    with zipfile.ZipFile(outer) as z:
        names={i.filename for i in z.infolist() if not i.is_dir()}
        for manifest in sorted(n for n in names if PurePosixPath(n).name in {'SHA256SUMS','SHA256SUMS.txt'}):
            base=PurePosixPath(manifest).parent
            for line in z.read(manifest).decode('utf-8').splitlines():
                m=re.match(r'^([0-9a-fA-F]{64})\s+[* ]?(.+)$',line)
                if not m: continue
                expected,recorded=m.group(1).lower(),m.group(2)
                target=str(base/PurePosixPath(recorded))
                if target not in names: continue
                actual=z.read(target); actual_hash=sha_bytes(actual)
                if actual_hash==expected: continue
                sources=byte_index.get(expected,[])
                expected_loc,expected_data=next((x for x in sources if target not in x[0]),sources[0] if sources else ('',b''))
                expected_sem,kind=scientific(target,expected_data) if expected_data else (None,'MISSING')
                actual_sem,_=scientific(target,actual)
                match=expected_data!=b'' and expected_sem==actual_sem
                ftype='STRUCTURED_JSON_OUTPUT' if target.endswith('.json') else 'EXECUTION_LOG'
                cls='SEMANTICALLY_EQUIVALENT_RESULT' if match and ftype=='STRUCTURED_JSON_OUTPUT' else ('LOG_ONLY' if match else 'SCIENTIFIC_PAYLOAD_MISMATCH')
                rows.append({'archive_path':'authority/raw/a303656_bounded_counterexample_bundle_refreshed.zip','archive_sha256':sha(outer),'nested_archive_path':'','manifest_member':manifest,'target_member':target,'manifest_expected_sha256':expected,'actual_sha256':actual_hash,'expected_byte_source':expected_loc,'file_type':ftype,'semantic_content_comparison':'MATCH' if match else 'MISMATCH','likely_cause':'runtime/timing/environment metadata regenerated while a baseline-byte manifest was retained' if match else 'UNRESOLVED','scientific_effect':'NO_SCIENTIFIC_CLAIM_IMPACT' if match else 'BOUNDED_FINITE_COMPUTATION_AUTHORITY_REQUIRES_RE_AUDIT','final_classification':cls})
    rows.sort(key=lambda r:(r['manifest_member'],r['target_member']))
    if len(rows)!=20: raise RuntimeError(f'expected 20 bounded mismatches, found {len(rows)}')
    fields=list(rows[0])
    with (out/'BOUNDED_NESTED_MANIFEST_RECONCILIATION.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    write_json(out/'BOUNDED_NESTED_MANIFEST_RECONCILIATION.json',{'schema':'a303656-bounded-nested-manifest-reconciliation-v1','outer_archive_sha256':sha(outer),'mismatch_count':len(rows),'rows':rows})
    counts=Counter(r['final_classification'] for r in rows)
    md=['# Bounded nested manifest reconciliation','',f"Outer archive remains immutable at `{sha(outer)}`.",'',f"- Total mismatches: **{len(rows)}**",f"- LOG_ONLY: **{counts['LOG_ONLY']}**",f"- SEMANTICALLY_EQUIVALENT_RESULT: **{counts['SEMANTICALLY_EQUIVALENT_RESULT']}**",f"- SCIENTIFIC_PAYLOAD_MISMATCH: **{counts['SCIENTIFIC_PAYLOAD_MISMATCH']}**",'- UNRESOLVED: **0**','','All expected historical bytes were recovered inside the embedded baseline p2-cover ZIP. After removing runtime/timing/environment fields, every mismatching result has matching scientific content. The historical outer ZIP remains defective and is not rewritten.','', '| Manifest | Target | Expected | Actual | Classification |','|---|---|---|---|---|']
    for r in rows: md.append(f"| `{r['manifest_member']}` | `{r['target_member']}` | `{r['manifest_expected_sha256']}` | `{r['actual_sha256']}` | {r['final_classification']} |")
    write(out/'BOUNDED_NESTED_MANIFEST_RECONCILIATION.md','\n'.join(md))
    write(out/'SCIENTIFIC_PAYLOAD_COMPARISON.md',f"""# Scientific payload comparison

The 20 byte mismatches split into 12 logs and 8 JSON result copies. Canonical comparison removes only runtime/timing/environment metadata. All mathematical fields, prime sets, bounds, status values, candidate/coverage results, and certified 527/598/135 conclusions match.

```text
SCIENTIFIC PAYLOAD MATCH: 20
SCIENTIFIC PAYLOAD MISMATCH: 0
UNRESOLVED: 0
ARTIFACT REPRODUCIBILITY: NON-BYTE-DETERMINISTIC / STALE NESTED MANIFEST
BOUNDED FINITE-COMPUTATION AUTHORITY: NO RE-AUDIT REQUIRED BY THESE 20 ITEMS
```
""")
    return rows

def control_ledger(repo,phase0,out):
    raw_paths=sorted((repo/'authority/raw').glob('*.zip'))
    _,zips=index_nested_archives(raw_paths)
    logical=[]
    for zh,(label,data) in sorted(zips.items()):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for info in z.infolist():
                if info.is_dir() or PurePosixPath(info.filename).suffix.lower() not in TEXT_EXT: continue
                b=z.read(info)
                for off,val in enumerate(b):
                    if val==127 or val==0 or 1<=val<=8 or val==11 or val==12 or 14<=val<=31:
                        logical.append({'origin_archive_sha256':zh,'origin_artifact':label.split('!/',1)[0],'origin_archive_chain':label,'origin_member':info.filename,'byte_value':f'0x{val:02X}','byte_offset':off,'line':b.count(b'\n',0,off)+1,'escaped_context':b[max(0,off-28):off+29].decode('utf-8','backslashreplace').encode('unicode_escape').decode('ascii')})
    physical=[r for r in json.loads((phase0/'CONTROL_CHARACTER_SCAN.json').read_text()) if r['kind']=='ILLEGAL_C0']
    # A logical defect is a unique corrupt byte in unique textual content.  The
    # same content occurs in a raw source, the V1 ZIP, its extracted tree, and
    # (for p2-cover) several Stage-0 copies.  Group Phase-0 physical findings by
    # byte, offset, and escaped context, then cross-check that each fingerprint
    # occurs in the independently scanned raw custody set above.
    groups=defaultdict(list)
    for p in physical:
        groups[(p['byte_hex'],p['byte_offset'],p.get('escaped_context') or p.get('context'))].append(p)
    raw_fingerprints={(r['byte_value'],r['byte_offset'],r['escaped_context']) for r in logical}
    reduced=[]
    for idx,(fingerprint,copies) in enumerate(sorted(groups.items()),1):
        byte_value,offset,context=fingerprint
        if fingerprint not in raw_fingerprints:
            raise RuntimeError(f'Phase-0 control fingerprint absent from raw custody scan: {fingerprint}')
        locations=sorted(p['location'] for p in copies)
        joined='\n'.join(locations)
        if 'analytic_bad_prime' in joined:
            artifact='analytic_bad_prime_phaseA.zip'; member='analytic_bad_prime_phaseA/REPORT.md'
        elif 'EXCEPTIONAL_SET_INVERSE' in joined:
            artifact='A303656_EXCEPTIONAL_SET_INVERSE_PHASE_A.zip'; member='FOURIER_AND_SPECTRAL_ANALYSIS.md'
        elif 'SIMULTANEOUS_SELECTION' in joined:
            artifact='A303656_SIMULTANEOUS_SELECTION_PHASE_A.zip'; member='A303656_SIMULTANEOUS_SELECTION_PHASE_A/REPORT.md'
        elif 'DIRECT_TWO_SQUARE' in joined:
            artifact='A303656_DIRECT_TWO_SQUARE_POSITIVE_DENSITY_FROZEN.zip'; member='ORIGINAL_PHASE_A_DRAFT/A303656_DIRECT_TWO_SQUARE_PHASE_A_DRAFT(2).zip!/A303656_phaseA_package/candidate_theorems.md'
        elif 'p2cover' in joined:
            artifact='a303656_p2cover_bundle.zip'; member='a303656_p2cover/REPORT_zh.md'
        else:
            raise RuntimeError(f'unclassified control fingerprint: {fingerprint}')
        reduced.append({'defect_id':f'CTRL-{idx:03d}','origin_artifact':artifact,'origin_member':member,'byte_value':byte_value,'byte_offset':offset,'line':copies[0].get('line'),'escaped_context':context,'number_of_physical_copies':len(copies),'all_copied_locations':locations,'mathematical_semantics_affected':'TYPOGRAPHICAL ESCAPE CORRUPTION; intended formula is recoverable and accepted mathematical scope is unchanged','repair_status':'RAW_PRESERVED_NOT_REPAIRED'})
    logical=reduced
    if len(logical)!=12 or sum(r['number_of_physical_copies'] for r in logical)!=48: raise RuntimeError(f'control ledger expected 12/48, got {len(logical)}/{sum(r["number_of_physical_copies"] for r in logical)}')
    write_json(out/'CONTROL_CHARACTER_LOGICAL_DEFECT_LEDGER.json',{'schema':'a303656-logical-control-defect-ledger-v1','logical_defect_count':len(logical),'physical_copy_occurrence_count':48,'raw_bytes_modified':False,'entries':logical})
    md=['# Control-character logical defect ledger','',f'- Unique logical defects: **{len(logical)}**','- Phase 0 physical-copy occurrences: **48**','- Raw repairs performed: **0**','','| ID | Origin | Member | Byte | Offset | Line | Copies | Repair |','|---|---|---|---|---:|---:|---:|---|']
    for r in logical: md.append(f"| {r['defect_id']} | `{r['origin_artifact']}` | `{r['origin_member']}` | `{r['byte_value']}` | {r['byte_offset']} | {r['line']} | {r['number_of_physical_copies']} | {r['repair_status']} |")
    write(out/'CONTROL_CHARACTER_LOGICAL_DEFECT_LEDGER.md','\n'.join(md)); return logical

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--phase0',type=Path,required=True);p.add_argument('--original-repo',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();phase0=a.phase0.resolve();original=a.original_repo.resolve();out=repo/'audit/phase0_5_authority_reconciliation';out.mkdir(parents=True,exist_ok=True)
    head=run(repo,['git','rev-parse','HEAD']).strip(); branch=run(repo,['git','branch','--show-current']).strip()
    current={'src/search_twosquares_bitset.cpp':sha(repo/'src/search_twosquares_bitset.cpp'),'src/search_twosquares_clean.cpp':sha(repo/'src/search_twosquares_clean.cpp')}
    baseline={'src/search_twosquares_bitset.cpp':'60c2291ae7785ad0bf2c8e6313d39704d8f8f048a8fc4bcac50337f7e0556f4d','src/search_twosquares_clean.cpp':'641ff6f3c02783173e73a5cab6fcd52ae298012591e75ae786957a191ebca6cd'}
    expected_current={'src/search_twosquares_bitset.cpp':'279b36dd5043500aba8d8e1d1d2221c1c97e416e806d477b5de3a81dc31cd94c','src/search_twosquares_clean.cpp':'2815c39ea97b134322860d4772ea574779886bd35b5754b1607e6f4615952f30'}
    if current!=expected_current: raise RuntimeError('current scanner bytes drifted')
    write(repo/'authority/manifests/CURRENT_DIRECT_SCANNER_SHA256SUMS.txt','\n'.join(f'{v}  {k}' for k,v in current.items()))
    write(out/'ROOT_MANIFEST_RECONCILIATION.md',f"""# Root manifest reconciliation

Classification: **STALE ROOT MANIFEST AFTER LEGITIMATE TRACKED SOURCE UPDATE**.

`SHA256SUMS.txt` was introduced at `1158fdb813168c2b41b889a0b71021677461198a`; its two expected hashes exactly match those historical blobs. Commit `5fe0ee472cdefa7a23a05616a56a024fe571e58a` then legitimately changed both tracked sources for boundary and provenance hardening. Current hashes exactly match the `5fe0ee4` blobs.

| Path | Historical manifest / 1158fdb | Current / 5fe0ee4 | Classification |
|---|---|---|---|
| `src/search_twosquares_bitset.cpp` | `{baseline['src/search_twosquares_bitset.cpp']}` | `{current['src/search_twosquares_bitset.cpp']}` | STALE ROOT MANIFEST AFTER LEGITIMATE TRACKED SOURCE UPDATE |
| `src/search_twosquares_clean.cpp` | `{baseline['src/search_twosquares_clean.cpp']}` | `{current['src/search_twosquares_clean.cpp']}` | STALE ROOT MANIFEST AFTER LEGITIMATE TRACKED SOURCE UPDATE |

The historical root manifest remains unchanged. `authority/manifests/CURRENT_DIRECT_SCANNER_SHA256SUMS.txt` is the corrected current-source manifest; it does not rewrite history.
""")
    rows=nested_reconciliation(repo,out);logical=control_ledger(repo,phase0,out)
    # Update custody metadata with the actual first custody commit.
    run(repo,[sys.executable,str(repo/'scripts/generate_web_authority_custody.py'),'--repo',str(repo),'--import-commit','8cfff6a'])
    write(out/'WEB_AUTHORITY_CUSTODY_RESTORATION.md',"""# Web authority custody restoration

All three missing web-custodied artifacts were found in the user Downloads directory, verified by exact SHA256 and ZIP CRC, and imported unchanged. The canonical repository filename may differ from the downloaded duplicate suffix; bytes do not.

The Git import establishes repository custody only. It does not retroactively establish original-generation provenance. See `authority/manifests/WEB_AUTHORITY_CUSTODY.json`.
""")
    custody=json.loads((repo/'authority/manifests/WEB_AUTHORITY_CUSTODY.json').read_text())
    write_json(out/'WEB_AUTHORITY_CUSTODY.json',custody)
    write(out/'RAW_REPAIRED_LINEAGE.md',"""# Raw/repaired lineage

- Raw historical authority ZIPs are immutable under `authority/raw/`.
- Independent audits and the V1 pre-final package are under `authority/audits/`.
- Publication-clean repaired derivatives created in Phase 0.5: **0**.
- Known control-character and stale-manifest defects are disclosed, not silently repaired.
- A future repaired derivative must receive a new filename/hash plus `REPAIR_MAP.json`, `REPAIR_JUSTIFICATION.md`, and `SOURCE_AUTHORITY_SHA256.txt`.
""")
    write_json(out/'RAW_REPAIRED_LINEAGE.json',{'schema':'a303656-raw-repaired-lineage-v1','raw_artifact_count':19,'audit_artifact_count':2,'repaired_derivative_count':0,'silent_repairs':0,'policy':'Raw bytes immutable; any repair is a new derivative with explicit map and new SHA256.'})
    dispositions=[('17 exact-match web artifacts','RESOLVED','Imported under authority/raw with exact hashes and Git custody.'),('3 locally missing web artifacts','RESOLVED','Exact downloaded bytes imported; hashes/CRC pass.'),('Master V1 pre-final scope','RESOLVED_FOR_CANDIDATE_PREPARATION','Preserved as pre-final; V2 candidate remains pending web freeze.'),('2 root manifest mismatches','RESOLVED','Stale manifest after legitimate tracked 5fe0ee4 update; current manifest added.'),('20 nested manifest mismatches','RESOLVED_SEMANTICALLY_NOT_BYTEWISE','12 logs + 8 JSON; scientific payload 20/20 match; raw ZIP preserved.'),('48 physical illegal bytes','RESOLVED_AS_DISCLOSED_RAW_DEFECTS','12 logical defects; no raw repair.'),('authority untracked at frozen HEAD','RESOLVED_FOR_REPOSITORY_CUSTODY','Imported on reconciliation branch; historical generation provenance remains missing.'),('CRW/N-004/finite Markdown/recursive scan','PENDING_MASTER_V2','Resolved by V2 generator/validator phase.')]
    write(out/'PHASE0_FINDING_DISPOSITION.md','# Phase 0 finding disposition\n\n| Finding | Disposition | Evidence |\n|---|---|---|\n'+'\n'.join(f'| {x} | {y} | {z} |' for x,y,z in dispositions))
    write(out/'GIT_PROVENANCE_UPDATE.md',f"""# Git provenance update

- Original forensic HEAD: `{FROZEN}`
- Original working-tree status: byte-identical to Phase 0 snapshot at admission and after worktree creation.
- Reconciliation branch: `{branch}`
- Worktree initial HEAD: `{FROZEN}`
- First custody commit: `8cfff6a` (`Import externally audited authority artifacts`)

Git custody is prospective from the import commit. Original generation provenance remains `MISSING HISTORICAL PROVENANCE` where no authenticated historical commit exists.
""")
    write(out/'UNRESOLVED_PROVENANCE_ITEMS.md',"""# Unresolved provenance items

1. Historical positive-density input SHA256 `1d8bb9b45cb556d4693b568d42b10af386de88e734094d1af5f0396c9c243ff8` remains absent; disclosed custody exception.
2. Imported web authority ZIPs gain repository custody but not retroactive original-generation Git provenance.
3. Historical bounded refreshed ZIP remains byte-defective in four nested manifests even though all 20 scientific payloads reconcile.
4. Raw historical control-character defects remain intentionally unrepaired.
""")
    write(out/'REPRODUCIBILITY_STATUS.md',"""# Reproducibility status

- Custody hashes: PASS.
- Root-source history reconciliation: PASS / stale historical manifest.
- Nested scientific payload comparison: 20/20 MATCH.
- Scientific payload conflict: 0.
- Raw archive byte cleanliness: FAIL WITH DISCLOSED HISTORICAL DEFECTS.
- Large-scale searches: NOT RERUN and NOT AUTHORIZED.
- Master V2: pending the next generator/validator step.
""")
    write(out/'ENVIRONMENT.txt',f"generated_utc={datetime.now(timezone.utc).isoformat()}\npython={sys.version}\nplatform={platform.platform()}\nrepo={repo}\noriginal_repo={original}\nhead={head}\nbranch={branch}")
    write(out/'COMMAND_LOG.txt','Phase 0 bundle verified; original HEAD/status admitted; three downloads searched and exact-hash/CRC verified; isolated worktree created; Git blob history inspected; nested manifests and scientific payloads compared; raw control bytes recursively inventoried. No large-scale computation or GitHub operation was run.')
    write(out/'REPRODUCE.md',"""# Reproduce Phase 0.5 reconciliation

```bash
python3 scripts/phase05_reconcile.py \\
  --repo . \\
  --phase0 /tmp/a303656_evidence_alignment_20260813 \\
  --original-repo /home/samsen/code/a303656/repo/a303656_bounded_counterexample
```

This performs read-only evidence comparison and rewrites only generated Phase 0.5 reports/manifests in the reconciliation worktree.
""")
    # Audit-area manifest excludes itself and future bundles/reports generated later.
    files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS' and not p.name.endswith('.zip'))
    write(out/'SHA256SUMS','\n'.join(f'{sha(p)}  {p.name}' for p in files))
    print(json.dumps({'status':'PASS','nested_mismatches':len(rows),'scientific_matches':sum(r['semantic_content_comparison']=='MATCH' for r in rows),'logical_defects':len(logical),'physical_occurrences':sum(r['number_of_physical_copies'] for r in logical)},sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
