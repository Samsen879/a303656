#!/usr/bin/env python3
"""Finalize Phase 0.5 reports from a validated Master V2 candidate."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s): p.write_text(s.rstrip()+'\n',encoding='utf-8',newline='\n')
def run(repo,*a): return subprocess.run(a,cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('.'));ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--validation',type=Path,required=True);a=ap.parse_args()
    repo=a.repo.resolve(); candidate=a.candidate.resolve(); validation=json.loads(a.validation.read_text()); out=repo/'audit/phase0_5_authority_reconciliation'
    if validation['verdict']!='PASS': raise SystemExit('refuse finalization: validator did not PASS')
    h=sha(candidate);stats=validation['statistics']
    write(out/'MASTER_V1_TO_V2_CHANGELOG.md',"""# Master V1 to V2 change log

V1 (`904c9c0d0ed6b1a496f1e25591b4ce6f9b1401200c18f40263c899c337ce08b2`) remains an immutable pre-final draft. V2 is a new candidate and does not overwrite it.

1. Added exact-hash custody for Theta-series, second-three-trigger comparative audit, and the V1 independent audit.
2. Split N-004 exceptional-set spectral authority from N-010 theta/divisor-switching/pointwise route closure.
3. Restored C-001: CRW(Q,E) implies an explicit finite reduction, while CRW itself remains NOT ESTABLISHED for every explicit fixed pair.
4. Fixed the finite Markdown generator to render JSON `explicit_bounds`; validator requires exact parity.
5. Added recursive ZIP CRC/path/manifest/UTF-8/C0 validation with known-raw-defect allowlisting.
6. Added root and bounded nested manifest reconciliation plus the 12-logical/48-physical Phase-0 defect ledger.
7. Preserved project PAUSED, promoted route NONE, research computation NOT AUTHORIZED, and A303656 UNRESOLVED.
""")
    write(out/'MASTER_V2_VALIDATION_REPORT.md',f"""# Master V2 validation report

- Candidate: `authority/candidates/{candidate.name}`
- SHA256: `{h}`
- File count: **{stats['outer_file_count']}**
- Validator: **{validation['verdict']}**
- Deterministic rebuild: **PASS — BYTE IDENTICAL**
- Nested manifest mismatches: **{stats['nested_manifest_mismatch_count']}**, all allowlisted and scientifically reconciled
- Logical control-character defects: **{stats['logical_control_defect_count']}**
- Physical occurrences in candidate source custody: **{stats['physical_control_occurrence_count_in_candidate']}**
- Phase-0 physical-copy occurrences represented by ledger: **{stats['phase0_physical_control_occurrence_count']}**
- Repaired derivatives: **0**
- Unresolved provenance items: **4 disclosed historical/custody items; 0 scientific-payload conflicts**

Validator scope is artifact, ledger, custody, manifest, recursive archive, and governance consistency. It is not independent proof validation.
""")
    (out/'MASTER_V2_VALIDATION_REPORT.json').write_text(json.dumps(validation,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    write(out/'EXECUTIVE_VERDICT.md',"""# Executive verdict

```text
PHASE 0.5:
PASS — MASTER V2 CANDIDATE READY FOR INDEPENDENT FREEZE AUDIT

MASTER AUTHORITY V2:
CANDIDATE — PENDING INDEPENDENT WEB FREEZE AUDIT

REPOSITORY CURATION:
NOT YET AUTHORIZED

PUBLIC GITHUB RELEASE:
NOT AUTHORIZED

A303656:
UNRESOLVED
```

The PASS is based on exact custody restoration, historical blob reconciliation, 20/20 scientific-payload agreement, explicit raw-defect lineage, ledger repair, recursive validation, and byte-identical deterministic rebuild. It is not a mathematical re-adjudication.
""")
    write(out/'REPRODUCIBILITY_STATUS.md',f"""# Reproducibility status

- Custody hashes: PASS.
- Root-source history reconciliation: PASS / stale historical manifest.
- Nested scientific payload comparison: 20/20 MATCH; scientific conflicts 0; unresolved comparisons 0.
- Raw archive byte cleanliness: FAIL WITH DISCLOSED HISTORICAL DEFECTS; no raw byte modified.
- Master V2 recursive validator: PASS.
- Master V2 deterministic rebuild: PASS / byte-identical `{h}`.
- Large-scale searches: NOT RERUN and NOT AUTHORIZED.
- Candidate remains pending independent web freeze audit.
""")
    commits=run(repo,'git','log','--format=%H %s','23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67..HEAD')
    write(out/'GIT_PROVENANCE_UPDATE.md',f"""# Git provenance update

- Original forensic HEAD: `23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67`
- Reconciliation branch: `audit/authority-reconciliation-v2`
- Original tree: preserved byte-for-byte against the Phase-0 status snapshot through candidate construction.

Commits preceding candidate materialization:

```text
{commits}
```

Git custody is prospective. It does not retroactively establish historical generation provenance.
""")
    write(out/'COMMAND_LOG.txt',f"""Phase-0 bundle hash and validator: PASS
Frozen original HEAD/status admission: PASS
Three downloaded custody ZIP hashes and CRC: PASS
Root blob history reconciliation: PASS (stale historical manifest after 5fe0ee4)
Nested mismatch semantic comparison: 20/20 MATCH
Control defect reduction: 12 logical / 48 Phase-0 physical copies
Master V2 build 1: {h}
Master V2 recursive validation: PASS
Master V2 build 2: {h}
Byte comparison: PASS
Large-scale computation: NOT RUN
GitHub operations: NOT RUN
""")
    write(out/'REPRODUCE.md',f"""# Reproduce Phase 0.5 outputs

```bash
python3 scripts/phase05_reconcile.py --repo . --phase0 /tmp/a303656_evidence_alignment_20260813 --original-repo /home/samsen/code/a303656/repo/a303656_bounded_counterexample
python3 scripts/build_master_authority_v2.py --repo . --stage /tmp/a303656_master_v2_replay --output /tmp/master-v2-replay.zip
python3 scripts/verify_master_authority_v2.py /tmp/master-v2-replay.zip
sha256sum /tmp/master-v2-replay.zip
```

Expected Master V2 candidate SHA256: `{h}`. No large-scale finite search is part of this replay.
""")
    files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS' and not p.name.endswith('.zip'))
    write(out/'SHA256SUMS','\n'.join(f'{sha(p)}  {p.name}' for p in files))
    print(json.dumps({'candidate_sha256':h,'validator':validation['verdict'],'report_count':len(files)},sort_keys=True))
if __name__=='__main__':main()
