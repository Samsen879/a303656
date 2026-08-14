#!/usr/bin/env python3
"""Build compact authorities, landscape, freshness, and feasibility artifacts."""
import argparse,csv,hashlib,json,struct
from collections import Counter,defaultdict
from pathlib import Path

LOW,HIGH,N0,L4=183968950234,246731069451,240000005594,1129118760
P=(3,7,11,23); BASE_TUPLES={'CAL-216':(2,41,74,504),'CAL-227':(2,41,50,504),'CAL-230':(2,7,32,504),'G231-COMMON':(2,7,50,17)}

def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def pairs():
 out=[];a=1
 for c in range(24):
  b=1
  for d in range(17):
   if a+b<=LOW:out.append((c,d,a+b))
   b*=5
  a*=3
 return out
def masks(ps,p):
 out=[]
 for t in range(p*p):
  m=0
  for i,(_,_,s) in enumerate(ps):
   q=(t-s)%(p*p)
   if q%p==0 and q:m|=1<<i
  out.append(m)
 return out
def cover(mm,t):return mm[0][t[0]]|mm[1][t[1]]|mm[2][t[2]]|mm[3][t[3]]
def crt(t):
 mods=(40,9,49,121,529); vals=(34,*t); x=0;m=1
 for v,q in zip(vals,mods):
  k=((v-x)*pow(m,-1,q))%q;x+=m*k;m*=q
 return x%m
def members(r):
 x=r
 if x<LOW:x+=((LOW-x+L4-1)//L4)*L4
 out=[]
 while x<=HIGH:out.append(x);x+=L4
 return out
def designed_tuples(root):
 s=set()
 with open(root/'analysis/p4_maximizer_census/class_panel.csv') as f:
  for r in csv.DictReader(f):s.add(tuple(int(r[k]) for k in ('t3','t7','t11','t23')))
 with open(root/'analysis/k4_ap_pilot/backend_a_counts.csv') as f:
  for r in csv.DictReader(f):
   n=int(r['n']);s.add(tuple(n%(p*p) for p in P))
 p=root/'analysis/p5_sparse_panel_feasibility/results/occupied_fresh_class_manifest.jsonl'
 for line in p.open():
  for d in json.loads(line)['descriptions']:s.add(tuple(d['fixed_P4_tuple']))
 p=root/'analysis/p5_family_u_census/results/panel_reconstruction_manifest.json'
 for d in load(p).get('descriptions',[]):
  t=d.get('fixed_P4_tuple') or d.get('base_fixed_P4_tuple')
  if t:s.add(tuple(t))
 return s
def registry_member(n,reg,sparse):
 return n in sparse or any(a<=n<=b for a,b in reg['interval_union'])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('cert_a');ap.add_argument('cert_b');ap.add_argument('outdir');ap.add_argument('--root',default='.')
 a=ap.parse_args();root=Path(a.root);out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
 A=load(a.cert_a);B=load(a.cert_b)
 fields=('tuple_count','histogram','minimum','maximum','argmax_count','first_argmax','stream_digest','t3eq2','partition','top_band_masks')
 if any(A[k]!=B[k] for k in fields):raise SystemExit('enumerators disagree pointwise or on derived landscape')
 ps=pairs();dead_idx=[i for i,(c,d,_) in enumerate(ps) if c&1 and not(d&1)];live_idx=[i for i in range(407) if i not in set(dead_idx)]
 dead=sum(1<<i for i in dead_idx);live=((1<<407)-1)^dead
 idxbytes=lambda z:b''.join(struct.pack('<H',i) for i in z)
 literal=[]
 for cp in (0,1):
  for dp in (0,1):literal.append({'c_parity':cp,'d_parity':dp,'3c_mod8':pow(3,cp,8),'5d_mod8':pow(5,dp,8),'remainder_mod8':(2-pow(3,cp,8)-pow(5,dp,8))%8})
 auth={'schema':'a303656-p4-mod8-authority-v1','scope':{'n0':N0,'n_mod40':34,'n_mod8':2,'historical_panels_automatically_covered':False},
  'domain':{'c_range':[0,23],'d_range':[0,16],'rectangle_count':408,'excluded_pair':[23,16],
   'excluded_shift':3**23+5**16,'activation_cell':[LOW,HIGH],'pair_count':407,'ordering':'lexicographic c then d',
   'pair_order_sha256':sha((root/'analysis/k4_survivor_incidence/pair_order.csv').read_bytes()),'duplicate_shift_28_pairs':[[1,2],[3,0]]},
  'partition':{'definition':'c odd and d even','direct_count':len(dead_idx),'closed_form_count':12*9-1,
   'literal_table_count':sum(1 for c,d,s in ps if (2-pow(3,c,8)-pow(5,d,8))%8==6),
   'D8_indices':dead_idx,'A8_indices':live_idx,'D8_index_digest':sha(idxbytes(dead_idx)),'A8_index_digest':sha(idxbytes(live_idx)),
   'D8_mask_digest':sha(dead.to_bytes(51,'little')),'A8_mask_digest':sha(live.to_bytes(51,'little'))},
  'theorem':{'literal_mod8_table':literal,'sum_of_two_squares_mod8':[0,1,2,4,5],
  'statement':'For n congruent 34 mod 40 and c odd,d even, n-3^c-5^d is 6 mod 8, which is not a sum of two squares.'},
  'scope_guards':{'T_backend_invocations':0,'direct_oracle_invocations':0,'factorization_invocations':0,
   'empirical_weight_inputs':0,'post_hoc_score_inputs':0,'fifth_prime_inputs':0,'P5_or_P6_searches':0}}
 (out/'authorities.json').write_text(json.dumps(auth,indent=2,sort_keys=True)+'\n')
 mm=[masks(ps,p) for p in P]; frozen=load(root/'analysis/fifth_prime_marginal_coverage/results/frozen_base_masks.json')
 frozen_by_role={role:int.from_bytes(bytes.fromhex(b['coverage_mask_hex']),'little') for b in frozen['bases'] for role in b['roles']}
 baseline={}
 for name,t in BASE_TUPLES.items():
  m=cover(mm,t); stored=frozen_by_role[name]
  if m!=stored:raise SystemExit('authenticated baseline mask mismatch '+name)
  h=(m&live).bit_count();baseline[name]={'tuple':list(t),'mask_digest':sha(m.to_bytes(51,'little')),'raw_G':m.bit_count(),
   'covered_dead':(m&dead).bit_count(),'covered_live':h,'live_residual':300-h,'total_guaranteed_obstruction':107+h}
 expected={'CAL-227':199,'CAL-216':189,'G231-COMMON':184,'CAL-230':183}
 if any(baseline[k]['covered_live']!=v for k,v in expected.items()):raise SystemExit('baseline H8 gate failed')
 rows=list(csv.DictReader(open(root/'analysis/p4_maximizer_census/pair_frequencies.csv')))
 exposed=[int(r['pair_index']) for r in rows if int(r['exposure_count'])>0]
 never=[int(r['pair_index']) for r in rows if int(r['exposure_count'])>0 and int(r['winner_count'])==0]
 inter=[i for i in exposed if i in set(dead_idx)]
 baseline['G231_NEVER_WIN_identity']={'exposed_count':len(exposed),'never_win_count':len(never),'never_win_indices':never,
  'D8_intersection_indices':inter,'exact_identity':never==inter}
 (out/'baseline_audit.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
 reg=load(root/'analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json');sparse=set(reg['sparse_points']);designed=designed_tuples(root)
 frozen_digests={b['base_mask_digest'] for b in frozen['bases']}; bmask={k:cover(mm,t) for k,t in BASE_TUPLES.items()}
 class_rows=[];mask_rows=[];groups=defaultdict(list)
 for rec in A['top_band_masks']:
  m=int.from_bytes(bytes.fromhex(rec['mask_hex']),'little'); rem=[ps[i] for i in live_idx if not(m>>i)&1]
  rec=dict(rec);rec['live_residual']=300-rec['H8'];rec['remaining_live_c_distribution']=dict(sorted(Counter(c for c,d,s in rem).items()))
  rec['remaining_live_d_distribution']=dict(sorted(Counter(d for c,d,s in rem).items()))
  rec['symmetric_differences']={k:(m^v).bit_count() for k,v in bmask.items()};rec['new_vs_frozen_base_masks']=rec['mask_digest'] not in frozen_digests
  mask_rows.append(rec)
 # second deterministic pass only over 8,001 top-band tuples
 top_by_hex={r['mask_hex']:r for r in mask_rows}
 for t3 in range(9):
  for t7 in range(49):
   for t11 in range(121):
    z=mm[0][t3]|mm[1][t7]|mm[2][t11]
    for t23 in range(529):
     m=z|mm[3][t23];hx=m.to_bytes(51,'little').hex()
     if hx not in top_by_hex:continue
     t=(t3,t7,t11,t23);r=crt(t);mem=members(r);ev=[n for n in mem if registry_member(n,reg,sparse)];fr=[n for n in mem if n not in set(ev)]
     row={'tuple':list(t),'mask_digest':top_by_hex[hx]['mask_digest'],'crt_residue':r,'modulus':L4,'member_count':len(mem),
      'previously_designed_class':t in designed,'previously_evaluated_integer_count':len(ev),'fresh_integer_count':len(fr),
      'minimum_fresh_integer':min(fr) if fr else None,'maximum_fresh_integer':max(fr) if fr else None,
      'member_digest':sha(b''.join(struct.pack('<Q',n) for n in mem)),'fresh_member_digest':sha(b''.join(struct.pack('<Q',n) for n in fr))}
     class_rows.append(row);groups[row['mask_digest']].append(row)
 for r in mask_rows:
  g=groups[r['mask_digest']];r['previously_designed_class_count']=sum(x['previously_designed_class'] for x in g);r['fresh_class_count']=len(g)-r['previously_designed_class_count']
  r['previously_evaluated_integer_count']=sum(x['previously_evaluated_integer_count'] for x in g);r['fresh_integer_count']=sum(x['fresh_integer_count'] for x in g)
 if len(class_rows)!=sum(r['tuple_multiplicity'] for r in mask_rows):raise SystemExit('class manifest multiplicity mismatch')
 (out/'top_band_masks.json').write_text(json.dumps({'schema':'a303656-p4-mod8-top-band-v1','threshold':A['maximum']-2,'masks':mask_rows},indent=2,sort_keys=True)+'\n')
 with open(out/'class_freshness_manifest.csv','w',newline='') as f:
  keys=('t3','t7','t11','t23','mask_digest','crt_residue','modulus','member_count','previously_designed_class','previously_evaluated_integer_count','fresh_integer_count','minimum_fresh_integer','maximum_fresh_integer','member_digest','fresh_member_digest');w=csv.DictWriter(f,keys);w.writeheader()
  for r in class_rows:w.writerow({**{f't{i}':r['tuple'][j] for j,i in enumerate((3,7,11,23))},**{k:r[k] for k in keys if k not in ('t3','t7','t11','t23')}})
 landscape={k:A[k] for k in ('tuple_count','histogram','minimum','maximum','argmax_count','first_argmax','stream_digest','t3eq2')}
 landscape['histogram_sum']=sum(A['histogram'].values());landscape['distinct_maximizing_mask_count']=sum(r['H8']==A['maximum'] for r in mask_rows)
 landscape['distinct_top_band_mask_count']=len(mask_rows);landscape['raw_G_among_maximizers']=sorted({r['raw_G'] for r in mask_rows if r['H8']==A['maximum']})
 landscape['covered_dead_among_maximizers']=sorted({r['covered_dead'] for r in mask_rows if r['H8']==A['maximum']})
 landscape['class_freshness_manifest_sha256']=sha((out/'class_freshness_manifest.csv').read_bytes())
 (out/'landscape.json').write_text(json.dumps(landscape,indent=2,sort_keys=True)+'\n')
 def feasibility(sel):
  ns=[r for r in sel if r['new_vs_frozen_base_masks']];fc=sorted((r['fresh_class_count'] for r in ns),reverse=True);fi=sorted((r['fresh_integer_count'] for r in ns),reverse=True)
  return {'distinct_masks':len(sel),'distinct_new_masks':len(ns),'fresh_classes':sum(fc),'fresh_classes_per_mask':{r['mask_digest']:r['fresh_class_count'] for r in ns},
   'balanced_at_least_two_masks':len(fc)>=2 and fc[1]>=2,'maximum_equal_classes_per_mask_best_two':fc[1] if len(fc)>=2 else 0,
   'maximum_equal_classes_per_mask_across_all_new_masks':min(fc) if fc else 0,'maximum_equal_integers_per_mask_best_two':fi[1] if len(fi)>=2 else 0,
   'fresh_integers_per_class_range':[min((x['fresh_integer_count'] for x in class_rows if x['mask_digest'] in {r['mask_digest'] for r in sel}),default=0),max((x['fresh_integer_count'] for x in class_rows if x['mask_digest'] in {r['mask_digest'] for r in sel}),default=0)]}
 feas={'maximizers':feasibility([r for r in mask_rows if r['H8']==A['maximum']]),'top_band':feasibility(mask_rows)}
 gate=A['maximum']>=200 and feas['maximizers']['distinct_new_masks']>=2 and feas['maximizers']['fresh_classes']>=4 and feas['maximizers']['balanced_at_least_two_masks']
 feas['promotion_gate']={'eligible_for_future_panel_design_consideration':gate,'T_census_executed':False,'balanced_panel_may_be_frozen_without_T':gate}
 (out/'promotion_feasibility.json').write_text(json.dumps(feas,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
