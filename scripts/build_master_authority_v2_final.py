#!/usr/bin/env python3
"""Build the deterministic A303656 Master Authority V2 final-freeze candidate."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,shutil,zipfile
from datetime import datetime
from pathlib import Path

OLD='A303656_POST_TRIGGER_MASTER_AUTHORITY_AND_RESTART_GATE_REVIEW'
ROOT='A303656_POST_TRIGGER_MASTER_AUTHORITY_V2_FINAL_FREEZE_CANDIDATE'
FREEZE_STATUS='FINAL_FREEZE_CANDIDATE_PENDING_INDEPENDENT_WEB_EXACT_HASH_AUDIT'
DISPLAY_STATUS='FINAL FREEZE CANDIDATE — PENDING INDEPENDENT WEB EXACT-HASH AUDIT'
FIXED=(1980,1,1,0,0,0)

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha(p): return sha_bytes(p.read_bytes())
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n',encoding='utf-8',newline='\n')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2))
def load(p): return json.loads(p.read_text(encoding='utf-8'))

def md_table(headers,rows):
    return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+'\n'.join('| '+' | '.join(str(v).replace('|','\\|') for v in r)+' |' for r in rows)

def extract_v1(v1,stage):
    replace={'ARTIFACT_DEFECT_LEDGER.json','ARTIFACT_DEFECT_LEDGER.md','AUTHORITY_HIERARCHY.json','AUTHORITY_HIERARCHY.md','EXECUTIVE_VERDICT.md','FINITE_COMPUTATION_LEDGER.json','FINITE_COMPUTATION_LEDGER.md','MACHINE_VERDICT.json','MASTER_AUTHORITY_REPORT.md','MASTER_AUTHORITY_REPORT_zh.md','PACKAGE_FILE_LIST.txt','PACKAGE_MANIFEST.json','README.md','RESTART_GATE.json','RESTART_GATE.md','ROUTE_MATRIX.csv','ROUTE_MATRIX.json','ROUTE_MATRIX.md','SHA256SUMS.txt','SOURCE_ARCHIVE_INVENTORY.json','SOURCE_ARCHIVE_INVENTORY.tsv','THEOREM_LEDGER.json','THEOREM_LEDGER.md','environment.json'}
    with zipfile.ZipFile(v1) as z:
        for i in z.infolist():
            if i.is_dir(): continue
            rel=i.filename.split('/',1)[1]
            if rel in replace: continue
            target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(i))

def build(args):
    repo=args.repo.resolve(); out=args.output.resolve(); stage=args.stage.resolve()
    if stage.exists(): shutil.rmtree(stage)
    stage.mkdir(parents=True)
    v1=repo/'authority/audits/A303656_POST_TRIGGER_MASTER_AUTHORITY_AND_RESTART_GATE_REVIEW_V1_PRE_FINAL.zip'
    extract_v1(v1,stage)
    # Exact source custody additions.
    additions=[
      ('SRC-018','A303656_THETA_SERIES_POINTWISE_PHASE_A_DETERMINISTIC.zip','15496d228ebf6a49b0cc41bb1cc4d88594362ae9b694c7fa2cec6362f7b97909','theta-series/divisor-switching/pointwise route-closure authority'),
      ('SRC-019','A303656_SECOND_THREE_TRIGGER_COMPARATIVE_AUDIT.zip','bd279152b0ce0820347dd77b7a6cb5e737a04dcf3048542aae1b4783b8dc21f9','independent comparative adjudication of second trigger group')]
    for _,name,expected,_ in additions:
        src=repo/'authority/raw'/name
        if sha(src)!=expected: raise RuntimeError(f'hash mismatch: {name}')
        shutil.copyfile(src,stage/'source_archives'/name)
    audit=repo/'authority/audits/A303656_MASTER_AUTHORITY_INDEPENDENT_AUDIT_20260729.zip'
    if sha(audit)!='56c018791780e5037f2f5394266c05aecff8bea5e3a3238fedef84cfe83df57b': raise RuntimeError('independent audit hash mismatch')
    (stage/'independent_audits').mkdir(parents=True,exist_ok=True)
    shutil.copyfile(audit,stage/'independent_audits'/audit.name)
    recon=repo/'audit/phase0_5_authority_reconciliation'
    (stage/'phase0_5_reconciliation').mkdir(parents=True,exist_ok=True)
    for name in ['BOUNDED_NESTED_MANIFEST_RECONCILIATION.json','CONTROL_CHARACTER_LOGICAL_DEFECT_LEDGER.json','ROOT_MANIFEST_RECONCILIATION.md','RAW_REPAIRED_LINEAGE.json','WEB_AUTHORITY_CUSTODY.json']:
        shutil.copyfile(recon/name,stage/'phase0_5_reconciliation'/name)

    # Recover V1 machine ledgers from their authenticated ZIP.
    with zipfile.ZipFile(v1) as z:
        def oldjson(name): return json.loads(z.read(f'{OLD}/{name}'))
        theorem=oldjson('THEOREM_LEDGER.json'); finite=oldjson('FINITE_COMPUTATION_LEDGER.json'); routes=oldjson('ROUTE_MATRIX.json'); sources=oldjson('SOURCE_ARCHIVE_INVENTORY.json'); defects=oldjson('ARTIFACT_DEFECT_LEDGER.json')
    theorem['schema']='a303656-master-theorem-ledger-v2-final-freeze-candidate';theorem['freeze_status']=FREEZE_STATUS;theorem.pop('freeze_utc',None)
    for e in theorem['entries']:
        if e['id'] in {'P-005','P-007'}: e['classification']='ACCEPTED CONDITIONAL IMPLICATION'
        if e['id'].startswith('N-'): e['classification']='PROVED NEGATIVE STRUCTURAL THEOREM'
        if e['id']=='N-004':
            e.update(name='Exceptional-set spectral critical-scale and phase barrier',statement='Within the absolute-minor-spectrum / F3 localization mechanism audited in SRC-005, closure requires absolute minor-spectrum control at scale O(sqrt(X) log X), equivalently O((log X)/sqrt(X)) after the package normalization; the audited route lacks the required scale, phase alignment, or hereditary closure.',source_ids=['SRC-005'],scope_limit='The O(sqrt(X) log X) threshold is specific to the SRC-005 absolute-minor-spectrum / F3 localization mechanism. It is not asserted as a universal necessary threshold for all future exceptional-set inverse methods, and a future arithmetic bipartite expansion theorem is not excluded.')
        if e['id']=='N-009':
            e.update(statement='For arbitrarily large finite active-shift restrictions, actual valuation masks can produce arbitrarily large Helly obstructions; finite local/profinite consistency on those restrictions does not select one ordinary exponent pair completing all prime constraints.',scope_limit='This proves arbitrarily large Helly obstruction on arbitrary finite active-shift restrictions. It does not prove that the complete D(n) actual-mask family itself has unbounded Helly number, and it does not exclude a theorem using the full arithmetic witness graph.')
    theorem['entries'] += [
      {'id':'N-010','group':'NEGATIVE_STRUCTURAL_AUTHORITY','name':'Theta-series divisor-switching, modular-cusp and pointwise minor-arc route closure','statement':'The audited theta-series pointwise route does not deliver the required uniform pointwise conclusion through divisor switching, modular/cusp analysis, or the available minor-arc bounds.','classification':'PROVED NEGATIVE STRUCTURAL THEOREM','adjudication':'ACCEPTED_AS_ROUTE_CLOSURE_AUDIT','source_ids':['SRC-018','SRC-019'],'scope_limit':'Stops the audited theta-series trigger only; it is not a theorem that all analytic approaches are impossible.'},
      {'id':'C-001','group':'CONDITIONAL_AUTHORITY','name':'CRW fixed-parameter finite-reduction implication','statement':'If CRW(Q,E) holds for some explicit fixed (Q,E), then an explicit finite counterexample reduction follows.','classification':'ACCEPTED CONDITIONAL IMPLICATION','adjudication':'ACCEPTED_CONDITIONAL_ONLY','source_ids':['SRC-003','SRC-012'],'scope_limit':'No explicit fixed (Q,E) is known to satisfy CRW. CRW itself is NOT ESTABLISHED; route is INACTIVE / CONDITIONAL WATCH ONLY.'}]
    dump(stage/'THEOREM_LEDGER.json',theorem)
    write(stage/'THEOREM_LEDGER.md','# Theorem and conditional-authority ledger\n\n'+md_table(['ID','Classification','Name','Scope'],[(e['id'],e['classification'],e['name'],e['scope_limit']) for e in theorem['entries']]))

    finite['schema']='a303656-master-finite-computation-ledger-v2-final-freeze-candidate';finite['freeze_status']=FREEZE_STATUS;finite.pop('freeze_utc',None)
    for e in finite['entries']:
        e['classification']='INDEPENDENTLY AUDITED FINITE COMPUTATION' if e['id'] in {'F-001','F-002','F-005'} else 'CERTIFIED FINITE COMPUTATION'
    dump(stage/'FINITE_COMPUTATION_LEDGER.json',finite)
    write(stage/'FINITE_COMPUTATION_LEDGER.md','# Finite-computation ledger\n\n'+md_table(['ID','Classification','Explicit interval or domain','Result','Scope'],[(e['id'],e['classification'],e['explicit_bounds'],e['result'],e['scope_limit']) for e in finite['entries']]))

    routes['schema']='a303656-route-matrix-v2-final-freeze-candidate';routes['freeze_status']=FREEZE_STATUS;routes.pop('freeze_utc',None)
    routes['routes'] += [
      {'id':'R-019','route':'Theta-series / divisor-switching / pointwise minor-arc trigger','authority':'N-010','state':'STOPPED ROUTE','reason':'Independent route-closure audit accepted.','exact_restart_trigger':'A new primary theorem directly supplying the missing uniform pointwise control for the exact structured family.'},
      {'id':'R-020','route':'CRW fixed-parameter finite reduction','authority':'C-001','state':'INACTIVE_CONDITIONAL_WATCH_ONLY','reason':'The implication is accepted, but CRW is not established for any explicit fixed (Q,E).','exact_restart_trigger':'A proof of CRW(Q,E) for one explicit fixed pair with independently auditable constants.'}]
    dump(stage/'ROUTE_MATRIX.json',routes)
    rrows=[(r['id'],r['route'],r['state'],r['authority'],r['reason'],r['exact_restart_trigger']) for r in routes['routes']]
    write(stage/'ROUTE_MATRIX.md','# Route matrix\n\n'+md_table(['ID','Route','State','Authority','Reason','Restart trigger'],rrows))
    with (stage/'ROUTE_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['id','route','state','authority','reason','exact_restart_trigger']);w.writerows(rrows)

    sources['schema']='a303656-source-archive-inventory-v2-final-freeze-candidate';sources['freeze_status']=FREEZE_STATUS;sources.pop('freeze_utc',None)
    for sid,name,expected,role in additions:
        p=stage/'source_archives'/name
        sources['archives'].append({'id':sid,'canonical_name':name,'source_name':name,'package_path':'source_archives/'+name,'sha256':expected,'size_bytes':p.stat().st_size,'outer_zip_crc':'PASS','inner_manifest_status':'SEE_RECURSIVE_VALIDATION_AND_DEFECT_LEDGER','inner_manifest_record_count':None,'authority_role':role,'adjudication':'ACCEPTED','source_path_at_freeze':'authority/raw/'+name})
    dump(stage/'SOURCE_ARCHIVE_INVENTORY.json',sources)
    fields=['id','canonical_name','sha256','size_bytes','outer_zip_crc','inner_manifest_status','authority_role','adjudication']
    with (stage/'SOURCE_ARCHIVE_INVENTORY.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(sources['archives'])

    defects['schema']='a303656-master-artifact-defect-ledger-v2-final-freeze-candidate';defects['freeze_status']=FREEZE_STATUS;defects.pop('freeze_utc',None)
    defects['defects'] += [
      {'id':'D-014','artifact':'root SHA256SUMS.txt direct-scanner entries','severity':'PROVENANCE','status':'STALE HISTORICAL MANIFEST','details':'Two hashes bind the 1158fdb imported blobs; tracked commit 5fe0ee4 legitimately changed both sources.','disposition':'Preserve historical manifest and use the separately scoped current-source manifest.'},
      {'id':'D-015','artifact':'SRC-016 bounded refreshed nested Stage-0 manifests','severity':'REPRODUCIBILITY','status':'STALE_NESTED_MANIFEST','details':'20 byte mismatches: 12 logs and 8 structured results; all scientific payloads reconcile.','disposition':'Preserve raw ZIP; disclose non-byte-determinism; no scientific re-audit is required by these items.'},
      {'id':'D-016','artifact':'raw authority textual control characters','severity':'TYPOGRAPHY','status':'ARTIFACT DEFECT','details':'12 logical defects represented by 48 Phase-0 physical occurrences: 11 form-feed and one backspace logical defects.','disposition':'Raw bytes preserved; complete logical ledger included; repaired derivatives created: 0.'},
      {'id':'D-017','artifact':'three Phase-0 web-only authorities','severity':'CUSTODY','status':'RESOLVED_REPOSITORY_CUSTODY_ONLY','details':'Theta, comparative, and independent-audit ZIPs imported at exact web hashes.','disposition':'Git import establishes custody, not retroactive original-generation provenance.'}]
    dump(stage/'ARTIFACT_DEFECT_LEDGER.json',defects)
    write(stage/'ARTIFACT_DEFECT_LEDGER.md','# Artifact defect ledger\n\n'+md_table(['ID','Artifact','Status','Details','Disposition'],[(d['id'],d['artifact'],d['status'],d['details'],d['disposition']) for d in defects['defects']]))

    restart={'schema':'a303656-restart-gate-v2-candidate','status':'FAIL_CLOSED','rule':'TARGETED RESTART ONLY ON EXPLICIT RESTART GATE','allowed_triggers':['Indicator-level signed covariance theorem sufficient for the exact structured shift family.','HC-LT class lower-tail theorem.','Effective exceptional-set elimination.','Genuine representation-independent nonlinear descent.','Explicit finite reduction.','Credible independently certified counterexample candidate.','New primary literature theorem directly matching an A303656 blocker.'],'not_triggers':['new idea','more compute available','new model available','larger Pro quota','interesting heuristic'],'required_review':['exact statement and source custody','scope, constants, boundary, and uniformity audit','independent adversarial proof or certificate review','narrow scope authorization before computation']}
    dump(stage/'RESTART_GATE.json',restart);write(stage/'RESTART_GATE.md','# Fail-closed restart gate\n\nRestart is allowed only after one enumerated trigger is independently admitted. New ideas, compute, models, quota, or heuristics are not triggers.\n\n'+md_table(['Allowed trigger'],[(x,) for x in restart['allowed_triggers']]))

    verdict={'schema':'a303656-master-authority-v2-final-freeze-candidate-verdict','master_authority_v2':DISPLAY_STATUS,'project':'PAUSED','active_promoted_route':'NONE','low_cost_generic_theorem_hunts':'NOT ACTIVE','targeted_restart':'ONLY ON EXPLICIT RESTART GATE','codex_large_scale_research':'NOT AUTHORIZED','codex_ultra':'NOT AUTHORIZED','a303656':'UNRESOLVED','general_proof_obtained':False,'certified_counterexample_found':False,'validator_scope':'Artifact, ledger, custody, manifest, recursive archive, scope-correction, and governance consistency; not independent proof validation.'}
    dump(stage/'MACHINE_VERDICT.json',verdict)
    hierarchy={'schema':'a303656-authority-hierarchy-v2-candidate','order':['Web-side accepted mathematical scope','Exact raw source artifact hashes','Independent audits','Master V2 candidate ledgers','Repository historical reports'],'conflict_rule':'Never let local claims or repaired derivatives silently replace web authority or raw historical bytes.','candidate_status':verdict['master_authority_v2']}
    dump(stage/'AUTHORITY_HIERARCHY.json',hierarchy);write(stage/'AUTHORITY_HIERARCHY.md','# Authority hierarchy\n\n1. Web-side accepted mathematical scope.\n2. Exact raw source artifact hashes.\n3. Independent audits.\n4. Master V2 candidate ledgers.\n5. Historical local reports.\n\nConflicts remain explicit; this candidate is not final authority.')
    write(stage/'README.md',f"""# A303656 Master Authority V2 Final-Freeze Candidate

Status: **{DISPLAY_STATUS}**.

This derivative preserves the V1 repository/baseline snapshots and immutable raw sources, adds the three restored custody artifacts, separates N-004 from N-010, restores C-001 CRW conditional authority, fixes finite-ledger JSON/Markdown parity, and embeds Phase 0.5 reconciliation evidence.

`A303656: UNRESOLVED`. No general proof or certified counterexample is claimed.
""")
    report="""# Master Authority V2 final-freeze candidate report

This candidate closes the independent-audit completeness blockers without modifying accepted mathematical scope. N-004's O(sqrt(X) log X) scale is expressly limited to the SRC-005 absolute-minor-spectrum / F3 localization mechanism and is not a universal threshold for future exceptional-set inverse methods. N-009 is expressly limited to arbitrarily large Helly obstructions on arbitrary finite active-shift restrictions and does not assert unbounded Helly number for the complete D(n) actual-mask family. N-010 records the distinct theta-series route closure. C-001 preserves the conditional CRW implication while stating that CRW itself is not established. All finite entries render their exact JSON `explicit_bounds` in Markdown.

Raw historical defects remain disclosed. Validator PASS is package and governance consistency only, not independent proof validation.

PROJECT: PAUSED  
ACTIVE PROMOTED ROUTE: NONE  
A303656: UNRESOLVED
"""
    write(stage/'MASTER_AUTHORITY_REPORT.md',report);write(stage/'MASTER_AUTHORITY_REPORT_zh.md',report)
    write(stage/'EXECUTIVE_VERDICT.md',f'# Executive verdict\n\nMASTER AUTHORITY V2: **{DISPLAY_STATUS}**.\n\nRepository curation and public GitHub release remain unauthorized pending independent exact-hash audit and freeze.\n\nA303656: **UNRESOLVED**.')
    dump(stage/'environment.json',{'build_date':'2026-08-13','deterministic_zip_timestamp':'1980-01-01T00:00:00','builder':'scripts/build_master_authority_v2_final.py','repository_frozen_baseline':'23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67'})

    manifest={'schema':'a303656-post-trigger-master-package-manifest-v2-final-freeze-candidate','package_name':ROOT,'status':verdict['master_authority_v2'],'repository_frozen_baseline':'23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67','v1_source_sha256':sha(v1),'source_archive_count':len(sources['archives']),'source_archive_unique_sha256_count':len({x['sha256'] for x in sources['archives']}),'theorem_and_conditional_entry_count':len(theorem['entries']),'finite_computation_entry_count':len(finite['entries']),'route_count':len(routes['routes']),'defect_count':len(defects['defects']),'logical_control_defect_count':12,'phase0_physical_control_occurrence_count':48,'repaired_derivative_count':0,'scope_corrections':['N-004 mechanism-specific critical scale','N-009 finite-restriction Helly obstruction only'],'scope_guards':{'new_interval_scans':0,'new_CRT_searches':0,'new_T_evaluations':0,'source_archive_reconstructions':0,'certified_baseline_overwrites':0}}
    dump(stage/'PACKAGE_MANIFEST.json',manifest)
    # File list and hash manifest cover every other member.
    files=sorted(p for p in stage.rglob('*') if p.is_file() and p.name not in {'PACKAGE_FILE_LIST.txt','SHA256SUMS.txt'})
    write(stage/'PACKAGE_FILE_LIST.txt','\n'.join(p.relative_to(stage).as_posix() for p in files))
    files=sorted(p for p in stage.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    write(stage/'SHA256SUMS.txt','\n'.join(f'{sha(p)}  {p.relative_to(stage).as_posix()}' for p in files))
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in stage.rglob('*') if x.is_file()):
            rel=f'{ROOT}/{p.relative_to(stage).as_posix()}'
            zi=zipfile.ZipInfo(rel,FIXED);zi.create_system=3;zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(zi,p.read_bytes(),compresslevel=9)
    print(json.dumps({'path':str(out),'sha256':sha(out),'file_count':sum(1 for p in stage.rglob('*') if p.is_file())},sort_keys=True))

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--output',type=Path,required=True);p.add_argument('--stage',type=Path,required=True);a=p.parse_args();build(a)
if __name__=='__main__': main()
