#!/usr/bin/env python3
"""Build deterministic Phase 0.5 reconciliation bundle from committed evidence."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
ROOT='A303656_PHASE0_5_AUTHORITY_RECONCILIATION_20260813';FIXED=(1980,1,1,0,0,0)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n',encoding='utf-8',newline='\n')
def run(repo,*a):return subprocess.run(a,cwd=repo,text=True,stdout=subprocess.PIPE,check=True).stdout
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--stage',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();stage=a.stage.resolve();out=a.output.resolve()
 if stage.exists():shutil.rmtree(stage)
 stage.mkdir(parents=True)
 (stage/'reports').mkdir()
 (stage/'scripts').mkdir()
 for x in sorted((repo/'audit/phase0_5_authority_reconciliation').iterdir()):
  if x.is_file() and not x.name.endswith('.zip'):shutil.copyfile(x,stage/'reports'/x.name)
 for name in ['phase05_reconcile.py','generate_web_authority_custody.py','build_master_authority_v2.py','verify_master_authority_v2.py','finalize_phase05_reports.py','build_phase0_5_bundle.py','verify_phase0_5_bundle.py']:
  shutil.copyfile(repo/'scripts'/name,stage/'scripts'/name)
 candidate=repo/'authority/candidates/A303656_POST_TRIGGER_MASTER_AUTHORITY_V2_CANDIDATE.zip'
 ref={'path':'authority/candidates/'+candidate.name,'sha256':sha(candidate),'size_bytes':candidate.stat().st_size,'included_in_reconciliation_bundle':False,'reason':'Referenced by exact hash to avoid nesting the large authority candidate.'}
 write(stage/'MASTER_V2_REFERENCE.json',json.dumps(ref,sort_keys=True,indent=2))
 write(stage/'GIT_COMMIT_LIST.txt',run(repo,'git','log','--format=%H %P %aI %s','23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67..HEAD'))
 write(stage/'CHANGE_RECORD.txt',run(repo,'git','diff','--name-status','23eecc0137cf9ddd0d0640b2ac9e1f5fa3b10c67..HEAD'))
 files=sorted(x for x in stage.rglob('*') if x.is_file())
 write(stage/'SHA256SUMS','\n'.join(f'{sha(x)}  {x.relative_to(stage).as_posix()}' for x in files))
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for x in sorted(y for y in stage.rglob('*') if y.is_file()):
   zi=zipfile.ZipInfo(f'{ROOT}/{x.relative_to(stage).as_posix()}',FIXED);zi.create_system=3;zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,x.read_bytes(),compresslevel=9)
 print(json.dumps({'path':str(out),'sha256':sha(out),'file_count':sum(1 for x in stage.rglob('*') if x.is_file())},sort_keys=True))
if __name__=='__main__':main()
