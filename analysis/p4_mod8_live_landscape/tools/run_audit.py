#!/usr/bin/env python3
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path

def run(name,cmd,cwd,raw,env):
 out=raw/(name+'.stdout.log');err=raw/(name+'.stderr.log');start=time.monotonic()
 with out.open('wb') as o,err.open('wb') as e:r=subprocess.run(cmd,cwd=cwd,stdout=o,stderr=e,env=env)
 return {'command':cmd,'return_code':r.returncode,'wall_seconds':time.monotonic()-start,'stdout':out.name,'stderr':err.name}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',default='.');ap.add_argument('--raw',required=True);ap.add_argument('--results',required=True);a=ap.parse_args()
 root=Path(a.root).resolve();raw=Path(a.raw).resolve();results=Path(a.results).resolve();raw.mkdir(parents=True,exist_ok=True);results.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['A303656_FORBID_T_BACKENDS']='1';env['A303656_FORBID_DIRECT_ORACLE']='1';env['A303656_FORBID_FACTORIZATION']='1'
 tools=root/'analysis/p4_mod8_live_landscape/tools';certa=raw/'enumerator_a.json';certb=raw/'enumerator_b.json';records={}
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip();required='f452f2dbf66ba9f72f9fe035e367fcc0a8a31310'
 ancestry=subprocess.run(['git','merge-base','--is-ancestor',required,'HEAD'],cwd=root).returncode==0
 tracked=subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=root,text=True)
 gate={'schema':'a303656-p4-mod8-live-initial-gate-v1','required_initial_head':required,'execution_head':head,
  'required_head_is_execution_ancestor':ancestry,'tracked_worktree_clean':tracked=='','tracked_status':tracked.splitlines(),
  'existing_fixed_P4_authority':'analysis/p4_residue_landscape/metadata.json','prior_registry_authority':'analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json'}
 if not ancestry or tracked:raise SystemExit('initial repository gate failed')
 (results/'initial_repository_gate.json').write_text(json.dumps(gate,indent=2,sort_keys=True)+'\n')
 commands=[('enumerator_a',[sys.executable,str(tools/'enumerator_a.py'),str(certa)]),('enumerator_b',[sys.executable,str(tools/'enumerator_b.py'),str(certb)]),
  ('builder',[sys.executable,str(tools/'build_results.py'),str(certa),str(certb),str(results),'--root',str(root)]),
  ('verifier',[sys.executable,str(tools/'verifier.py'),str(certa),str(certb),str(results),'--root',str(root)]),
  ('unit_tests',[sys.executable,str(root/'analysis/p4_mod8_live_landscape/tests/test_exact.py')]),
  ('corruption_tests',[sys.executable,str(root/'analysis/p4_mod8_live_landscape/tests/test_corruptions.py'),str(certa),str(certb),str(results),'--root',str(root),'--output',str(results/'corruption_tests.json')]),
  ('final_verifier',[sys.executable,str(tools/'verifier.py'),str(certa),str(certb),str(results),'--root',str(root)])]
 for name,cmd in commands:
  records[name]=run(name,cmd,root,raw,env)
  if records[name]['return_code']!=0:
   (raw/'return_codes.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n');raise SystemExit(name+' failed')
 (raw/'return_codes.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
 manifest={'schema':'a303656-p4-mod8-live-command-manifest-v1','records':records,'raw_archive_path':str(raw),
  'raw_file_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(raw.iterdir()) if p.is_file()}}
 (results/'command_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 core_names=['authorities.json','baseline_audit.json','class_freshness_manifest.csv','corruption_tests.json','landscape.json','promotion_feasibility.json','top_band_masks.json','verification_report.json']
 metadata={'schema':'a303656-p4-mod8-live-metadata-v1','source_commit':head,'source_parent_commit':required,
  'results_commit':'RESULT_COMMIT_CONTAINING_THIS_FILE','raw_archive_path':str(raw),
  'core_artifact_sha256':{n:hashlib.sha256((results/n).read_bytes()).hexdigest() for n in core_names},
  'protected_hashes_after':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in [
   'README.md','REPORT_zh.md','output/formal_results_audit.json','output/final_packaging_audit.json','cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt',
   'analysis/p4_residue_landscape/metadata.json','analysis/k4_survivor_incidence/pair_order.csv','analysis/p4_maximizer_census/pair_frequencies.csv',
   'analysis/fifth_prime_marginal_coverage/results/frozen_base_masks.json','analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json']}}
 (results/'metadata.json').write_text(json.dumps(metadata,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
