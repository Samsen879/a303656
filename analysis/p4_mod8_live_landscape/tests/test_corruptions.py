#!/usr/bin/env python3
import argparse,csv,json,shutil,subprocess,sys,tempfile
from pathlib import Path

def load(p):return json.loads(Path(p).read_text())
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('cert_a');ap.add_argument('cert_b');ap.add_argument('results');ap.add_argument('--root',default='.');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root).resolve();ver=root/'analysis/p4_mod8_live_landscape/tools/verifier.py'
 cases=[]
 def add(name,kind,mut):cases.append((name,kind,mut))
 add('initial_HEAD_mismatch','arg',None)
 add('n_mod40_mutation','auth',lambda x:x['scope'].__setitem__('n_mod40',33))
 add('historical_panel_scope_expansion','auth',lambda x:x['scope'].__setitem__('historical_panels_automatically_covered',True))
 add('flipped_c_parity','auth',lambda x:x['partition'].__setitem__('definition','c even and d even'))
 add('flipped_d_parity','auth',lambda x:x['partition'].__setitem__('definition','c odd and d odd'))
 add('omitted_excluded_boundary_pair','auth',lambda x:x['domain'].__setitem__('excluded_pair',None))
 add('D8_count_corruption','auth',lambda x:x['partition'].__setitem__('direct_count',106))
 add('A8_count_corruption','auth',lambda x:x['partition']['A8_indices'].pop())
 add('duplicate_shift_pair_merger','auth',lambda x:x['domain'].__setitem__('duplicate_shift_28_pairs',[[1,2]]))
 add('pair_bit_order_mutation','auth',lambda x:x['partition'].__setitem__('D8_index_digest','0'*64))
 add('baseline_mask_mutation','base',lambda x:x['CAL-227'].__setitem__('mask_digest','0'*64))
 add('baseline_H8_expected_corruption','base',lambda x:x['CAL-227'].__setitem__('covered_live',198))
 add('tuple_omission','certa',lambda x:x.__setitem__('tuple_count',x['tuple_count']-1))
 add('tuple_duplication','certa',lambda x:x.__setitem__('tuple_count',x['tuple_count']+1))
 add('H8_stream_corruption','certa',lambda x:x.__setitem__('stream_digest','0'*64))
 add('maximizing_mask_omission','certa',lambda x:x['top_band_masks'].pop())
 add('freshness_registry_interval_deletion','registry_interval',None)
 add('prior_sparse_point_deletion','registry_sparse',None)
 add('class_integer_freshness_conflation','csv',None)
 add('empirical_weight_injection','auth',lambda x:x['scope_guards'].__setitem__('empirical_weight_inputs',1))
 add('accidental_T_backend_invocation','auth',lambda x:x['scope_guards'].__setitem__('T_backend_invocations',1))
 add('accidental_direct_oracle_invocation','auth',lambda x:x['scope_guards'].__setitem__('direct_oracle_invocations',1))
 add('accidental_factorization_invocation','auth',lambda x:x['scope_guards'].__setitem__('factorization_invocations',1))
 add('truncated_mask_bytes','top',lambda x:x['masks'][0].__setitem__('mask_hex',x['masks'][0]['mask_hex'][:-2]))
 add('extra_mask_bytes','top',lambda x:x['masks'][0].__setitem__('mask_hex',x['masks'][0]['mask_hex']+'00'))
 results=[]
 for name,kind,mut in cases:
  with tempfile.TemporaryDirectory() as td:
   td=Path(td);rd=td/'r';shutil.copytree(a.results,rd);ca=td/'a.json';cb=td/'b.json';shutil.copy(a.cert_a,ca);shutil.copy(a.cert_b,cb)
   cmd=[sys.executable,str(ver),str(ca),str(cb),str(rd),'--root',str(root)]
   if kind=='arg':cmd+=['--expected-initial-head','0'*40]
   elif kind=='certa':x=load(ca);mut(x);dump(ca,x)
   elif kind in ('auth','base','top'):
    fn={'auth':'authorities.json','base':'baseline_audit.json','top':'top_band_masks.json'}[kind];p=rd/fn;x=load(p);mut(x);dump(p,x)
   elif kind.startswith('registry'):
    p=td/'registry.json';x=load(root/'analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json')
    (x['interval_union'].pop() if kind.endswith('interval') else x['sparse_points'].pop());dump(p,x);cmd+=['--registry',str(p)]
   elif kind=='csv':
    p=rd/'class_freshness_manifest.csv';rows=list(csv.DictReader(p.open()));rows[0]['previously_designed_class']='False' if rows[0]['previously_designed_class']=='True' else 'True'
    with p.open('w',newline='') as f:w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
   r=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   results.append({'name':name,'return_code':r.returncode,'rejected':r.returncode!=0})
   if r.returncode==0:raise SystemExit('corruption accepted: '+name)
 report={'schema':'a303656-p4-mod8-live-corruption-tests-v1','all_rejected':True,'tests':results}
 if a.output:Path(a.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
