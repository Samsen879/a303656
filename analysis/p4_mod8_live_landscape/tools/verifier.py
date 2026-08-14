#!/usr/bin/env python3
import argparse,csv,hashlib,json,subprocess
from pathlib import Path

EXPECTED_HEAD='f452f2dbf66ba9f72f9fe035e367fcc0a8a31310'
EXPECTED_HASHES={
'analysis/p4_residue_landscape/metadata.json':'00f6e27dc5ec2557ba7ac0223c872088c56e02167f9f703c7f4eb534d08ea217',
'analysis/k4_survivor_incidence/pair_order.csv':'5f3b6ea52f9d3d5e544f10ae17a3752cbf1a476d9575a2e0a6ae4c502ed0452b',
'analysis/p4_maximizer_census/pair_frequencies.csv':'000fb139714a25fe6da2304ca8fdc67dfdc5782fb48d0c265d0cb22cf664dbb0',
'analysis/fifth_prime_marginal_coverage/results/frozen_base_masks.json':'11d54f3c9d714c36bd6afd130a30daa0e074f71b106052bb10fe4889361a88a3',
'analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json':'428f5abee8462d21777326c9fbdf9aa215d722f43d9ceaed75b980e30c4158af'}
def load(p):return json.loads(Path(p).read_text())
def fail(s):raise SystemExit('EXACT P4 MOD-8-LIVE COVERAGE LANDSCAPE NOT VALIDATED: '+s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('cert_a');ap.add_argument('cert_b');ap.add_argument('result_dir');ap.add_argument('--root',default='.');ap.add_argument('--expected-initial-head',default=EXPECTED_HEAD);ap.add_argument('--registry');a=ap.parse_args();root=Path(a.root)
 try:
  subprocess.run(['git','merge-base','--is-ancestor',a.expected_initial_head,'HEAD'],cwd=root,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError:fail('initial HEAD mismatch or ancestry failure')
 for p,h in EXPECTED_HASHES.items():
  if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:fail('protected authority hash mismatch: '+p)
 if a.registry and hashlib.sha256(Path(a.registry).read_bytes()).hexdigest()!=EXPECTED_HASHES['analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json']:fail('prior registry mutation')
 A=load(a.cert_a);B=load(a.cert_b)
 for k in ('tuple_count','histogram','minimum','maximum','argmax_count','first_argmax','stream_digest','t3eq2','partition','top_band_masks'):
  if A.get(k)!=B.get(k):fail('enumerator disagreement at '+k)
 if A['tuple_count']!=28227969 or sum(A['histogram'].values())!=28227969:fail('tuple omission or duplication')
 if A['partition']['dead_count']!=107 or A['partition']['live_count']!=300:fail('partition count corruption')
 rd=Path(a.result_dir);auth=load(rd/'authorities.json');base=load(rd/'baseline_audit.json');land=load(rd/'landscape.json');top=load(rd/'top_band_masks.json');fresh=list(csv.DictReader(open(rd/'class_freshness_manifest.csv')));feas=load(rd/'promotion_feasibility.json')
 if auth['scope']!={'historical_panels_automatically_covered':False,'n0':240000005594,'n_mod40':34,'n_mod8':2}:fail('mod-40 scope mutation')
 if auth['domain']['pair_count']!=407 or auth['domain']['excluded_pair']!=[23,16] or auth['domain']['duplicate_shift_28_pairs']!=[[1,2],[3,0]]:fail('pair domain corruption')
 if auth['partition']['direct_count']!=107 or auth['partition']['closed_form_count']!=107 or auth['partition']['literal_table_count']!=107:fail('D8 independent count corruption')
 if auth['partition']['definition']!='c odd and d even' or len(auth['partition']['D8_indices'])!=107 or len(auth['partition']['A8_indices'])!=300:fail('parity or A8/D8 index corruption')
 if auth['partition']['D8_index_digest']!=A['partition']['dead_indices_digest'] or auth['partition']['A8_index_digest']!=A['partition']['live_indices_digest']:fail('pair bit-order mutation')
 if auth.get('scope_guards')!={'P5_or_P6_searches':0,'T_backend_invocations':0,'direct_oracle_invocations':0,'empirical_weight_inputs':0,'factorization_invocations':0,'fifth_prime_inputs':0,'post_hoc_score_inputs':0}:fail('forbidden input or backend invocation')
 exp={'CAL-227':199,'CAL-216':189,'G231-COMMON':184,'CAL-230':183}
 if any(base[k]['covered_live']!=v for k,v in exp.items()):fail('baseline H8 corruption')
 bd={'CAL-216':'92cf2935795f45f8f3e5b68930bc5f4dd5fb87d7a279fb9285637337d0bf2fcb','CAL-227':'69f65ed672284ac9caa227af4c518051b71ddfb2c04cf1bfb80db040c12fb88a','CAL-230':'0c5af57d6002d3814b95ab2dbc749bb800533051391fd7fa74f9f55886f135db','G231-COMMON':'4f06ade9cb4e7612cdf690ea5c0b71173802073e9210979b474d00335f9d5c35'}
 if any(base[k]['mask_digest']!=v for k,v in bd.items()):fail('baseline mask mutation')
 if not base['G231_NEVER_WIN_identity']['exact_identity'] or base['G231_NEVER_WIN_identity']['never_win_count']!=60:fail('G231 NEVER-WIN identity corruption')
 if land['stream_digest']!=A['stream_digest'] or land['histogram']!=A['histogram'] or land['maximum']!=A['maximum']:fail('landscape stream/count corruption')
 if len(top['masks'])!=len(A['top_band_masks']):fail('maximizing/top-band mask omission')
 for r in top['masks']:
  b=bytes.fromhex(r['mask_hex'])
  if len(b)!=51 or hashlib.sha256(b).hexdigest()!=r['mask_digest']:fail('truncated or extra mask bytes')
 if len(fresh)!=sum(r['tuple_multiplicity'] for r in top['masks']):fail('freshness class manifest mismatch')
 if hashlib.sha256((rd/'class_freshness_manifest.csv').read_bytes()).hexdigest()!=land['class_freshness_manifest_sha256']:fail('freshness class/integer conflation or row mutation')
 if feas['promotion_gate']['T_census_executed']:fail('accidental T backend invocation')
 report={'schema':'a303656-p4-mod8-live-verification-v1','validation_conclusion':'VALIDATED EXACT P4 MOD-8-LIVE COVERAGE LANDSCAPE',
  'interpretation_label':'MOD-8-LIVE COVERAGE STRICTLY IMPROVES THE KNOWN P4 LANDSCAPE' if A['maximum']>=200 else 'MOD-8-CORRECTED P4 CARDINALITY SHOWS NO FURTHER IMPROVEMENT',
  'checks':{'protected_hashes_unchanged':True,'enumerators_pointwise_digest_agree':True,'tuple_count_exact':True,'histogram_complete':True,
   'no_T_evaluation':True,'no_factorization':True,'no_direct_two_square_oracle':True,'no_empirical_weight':True}}
 (rd/'verification_report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(report['validation_conclusion'])
if __name__=='__main__':main()
