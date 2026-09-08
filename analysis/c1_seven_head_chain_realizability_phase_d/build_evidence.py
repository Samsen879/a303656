#!/usr/bin/env python3
"""Discovery-to-certificate producer. SymPy is NOT used by verify.py."""
from pathlib import Path
from math import prod,gcd,lcm
import csv,json,sys,sympy as sp,hashlib,platform,subprocess
sys.set_int_max_str_digits(100000)
R=Path(__file__).resolve().parent
HEADS=[(31,3,0),(7,6,4),(19,9,2),(5167,18,14),(271,27,8),(4159,27,17),(31051,27,26)]
first={7:[19531],19:[191,6271,3981071],31:[1861,625552508473588471]}
family={n:set(a) for n,a in first.items()}
scans={}
for dirname in ['search','replay_search']:
 for file in sorted((R/dirname).glob('n_*.csv')):
  p=int(file.stem[2:]);j=json.loads(file.with_suffix('.json').read_text())
  rows=list(csv.DictReader(file.open()));qs=[int(a['q']) for a in rows]
  family.setdefault(p,set()).update(qs)
  scans.setdefault(p,{})[dirname]={'K':int(j['K']),'q_hits':qs,'modular_tests':j['modular_tests']}
proof={}
def certify(n):
 n=int(n)
 if str(n) in proof:return
 if n==2:proof['2']={'n':'2','kind':'base'};return
 assert sp.isprime(n),('composite discovery candidate',n)
 f={int(q):int(e) for q,e in sp.factorint(n-1).items()}
 for q in f:certify(q)
 for a in range(2,1000):
  if pow(a,n-1,n)==1 and all(gcd(pow(a,(n-1)//q,n)-1,n)==1 for q in f):break
 else:raise RuntimeError('Lucas witness not found')
 proof[str(n)]={'n':str(n),'kind':'full_n_minus_1_Lucas','a':a,'factors':{str(q):e for q,e in sorted(f.items())}}

def node(q,w,role):
 certify(q)
 fac={int(p):int(e) for p,e in sp.factorint(w).items()}
 for p in fac:certify(p)
 assert pow(5,w,q)==1
 ex={str(p):str(pow(5,w//p,q)) for p in fac};assert all(v!='1' for v in ex.values())
 s=1
 while pow(5,w,q**(s+1))==1:s+=1
 return {'prime':str(q),'order':str(w),'order_factorization':{str(p):e for p,e in fac.items()},'order_exclusions':ex,
  's':s,'admitted':q%4==3,'regular':s==1,'role':role,'power_mod_q2':str(pow(5,w,q*q)),
  'power_mod_q_s_plus_1':str(pow(5,w,q**(s+1))),'fermat_power_mod_q2':str(pow(5,q-1,q*q))}
nodes={}
for h,w,ell in HEADS:nodes[h]=node(h,w,'literal_head')
for h in [163,487,16018507]:nodes[h]=node(h,54,'alternative_depth3_head')
nodes[3]=node(3,2,'two_anchor_fixture_row3')
for p,qs in family.items():
 for q in qs:nodes[q]=node(q,p,'chain_factor' if q%4==3 else 'nonadmitted_rejected_edge')
for q,w in [(20771,10385),(40487,40486),(1645333507,1645333506),(53471161,13367790)]:
 nodes[q]=node(q,w,'imported_inventory_independently_recertified')
for q,x in nodes.items():
 x['known_children']=[str(v) for v in sorted(family.get(q,set()))]
 x['child_list_complete']=q in first
 x['expansion_status']='COMPLETE_FACTORIZATION' if q in first else ('PARTIAL_PREIMAGE_ENUMERATION' if q in family else ('REJECTED_NONADMITTED' if not x['admitted'] else 'UNEXPANDED'))
# Materialize only moderate cyclotomic values; enormous ones are exact expressions.
fam=[]
for p,qs in sorted(family.items()):
 for q in qs: assert nodes[q]['order']==str(p)
 den=4*prod(qs)
 row={'exponent':str(p),'proven_prime_factors':{str(q):1 for q in sorted(qs)},'complete':p in first,
      'cofactor_expression':f'(5^{p}-1)/{den}','cofactor_primality':'NOT_APPLICABLE' if p in first else 'OPEN'}
 if p<=40000:
  value=(5**p-1)//4;assert value%prod(qs)==0
  co=value//prod(qs)
  # Every found prime has exact multiplicity one; test independently later.
  if p in first:assert co==1
  text=str(co)+'\n';fn=f'cofactors/Phi_{p}_remaining.txt';(R/fn).write_text(text)
  row.update(cofactor_file=fn,cofactor_digits=len(str(co)),cofactor_mod4=co%4,cofactor_sha256=hashlib.sha256(text.encode()).hexdigest())
  if p in [191,271]:row['external_table_label']='P121' if p==191 else 'P171';row['cofactor_primality']='OPEN_INDEPENDENT_PRIMALITY; primary table labels P; BPSW screening passed'
 else:
  row['cofactor_storage']='EXACT_SYMBOLIC_INTEGER_NOT_MATERIALIZED'
 fam.append(row)
# Reconstruct actual heads by CRT; do not import the source reference fixture.
fixture=[]
for h,w,ell in HEADS:
 center=h*((ell*pow(h,-1,w))%w)
 r=(3+pow(5,center,h*h))%(h*h)
 fixture.append({'h':h,'w':w,'ell':ell,'center_mod_wh':center,'r_mod_h2':r,'K':2,'E':[1]})
# Exhaustive exact local row comparison, including all local zeros as safe.
count=0
for z in fixture:
 h,w,ell=z['h'],z['w'],z['ell'];r=z['r_mod_h2'];power=1;M=h*h
 for d in range(w*h):
  value=(r-3-power)%M
  fatal=value%h==0 and value!=0
  expect=d%w==ell and d%h!=0
  assert fatal==expect,(h,d)
  count+=1;power=power*5%M
 assert power==1
for d in range(6):
 v=(2-3-pow(5,d,9))%9
 assert (v%3==0 and v!=0)==(d%2==1 and d%3!=0)
 count+=1
collapsed=[]
for d in range(54):
 cover=[z['h'] for z in fixture if d%z['w']==z['ell']]
 if d%2==1 and d%3!=0:cover.append(3)
 assert cover
 collapsed.append({'d_mod_54':d,'conditional_cover_rows':cover})
# Record finite directed-prefix terminal exclusion; no conclusion at unbounded depth.
bounds={31:1251105016947176942000001,7:3906200000001,19:3820000001,
        271:54200000001,4159:831800000001,5167:1033400000001,31051:6210200000001}
for p,v in scans.items():
 if 'search' in v and 'replay_search' in v:
  a,b=v['search'],v['replay_search'];assert a['K']==b['K']
  assert [q for q in a['q_hits'] if q%4==3]==b['q_hits']
large=json.loads((R/'large31_independent_replay.json').read_text())
assert large['hits']==[[215,268987578643643042531]] and not large['relay_divisor_hits']

def check_bound(p,B,trace):
 assert nodes[p]['regular'] and nodes[p]['admitted']
 need=(B-1)//(2*p)
 if p in first:
  children=sorted(family[p]);method='complete_factorization'
 else:
  rec=scans[p]
  if p==625552508473588471:
   K=large['K'];children=[q for _,q in large['hits']];method='GMP/Python_bounded_preimages'
  elif p==268987578643643042531:
   K=large['relay_K_for_same_q_bound'];children=[];method='Python_all_odd_k_bounded_preimages'
  else:
   assert 'search' in rec and 'replay_search' in rec
   K=rec['search']['K'];children=rec['search']['q_hits'];method='uint128/GMP_bounded_preimages'
  assert need<=K,(p,B,need,K)
 trace.append({'p':str(p),'needed_k_max':need,'method':method})
 for q in children:
  if q%4==3 and q<=B:check_bound(q,B,trace)
traces={}
for h,B in bounds.items():
 traces[str(h)]=[];check_bound(h,B,traces[str(h)])
# All seven literal basins automatically disjoint by unique prime predecessor.
seen={}
for h,_,_ in HEADS:
 todo=[h]
 while todo:
  p=todo.pop()
  if p in seen:assert seen[p]==h
  seen[p]=h
  todo += [q for q in family.get(p,[]) if q%4==3]

result={'schema':'a303656.seven_head_phase_d.exact_evidence.v1',
 'authority':{'repository':'Samsen879/a303656','repository_id':1333945235,'main_sha':'3fb4b4b4f71018017c7ea014ae7a1380f27b6b94','main_tree':'5ee6ab9e51f3e6d471991b7407de193d12777882','github_writes':'NONE','project':'PAUSED','active_promoted_route':'NONE','a303656':'UNRESOLVED'},
 'literal_head_order':[h for h,w,ell in HEADS],
 'nodes':{str(q):x for q,x in sorted(nodes.items())},'prime_certificates':proof,'families':fam,
 'targeted_searches':{str(p):v for p,v in sorted(scans.items())},
 'conditional_fixture':{'rows':fixture,'row3':{'q':3,'r':2,'K':2,'E':[1]},'two_adic':{'K':2,'r':1},'actual_local_row_comparisons':count,'collapsed_classes':collapsed,'hypothetical_upstream_seeds':True,'full_actual_certificate':False},
 'terminal_lower_bounds':{str(h):{'scope':'literal exact-prime-order chains only','strictly_greater_than':str(B),'trace':traces[str(h)]} for h,B in bounds.items()},
 'outcome':{'all_seven_chains_exist':'OPEN','conditional_certificate_instantiated':'NO','full_certificate_independently_verified':'NO','kills_exactly_seven':'NO','all_seven_head_statuses':'OPEN','actual_admitted_nonregular_chain_hits':0,'success_level':'C (finite preimage classifications and bounded obstructions), with D partial data'},
 'environment':{'python':sys.version,'platform':platform.platform(),'discovery_sympy':sp.__version__,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],'verifier_requires':'Python standard library only; search replay additionally g++ and GMP headers/libraries'}}
from itertools import permutations
G3=[163,271,487,4159,31051,16018507]
variant_count=0
for gs in permutations(G3,3):
 guards=[(3,0),(6,4),(9,2),(18,14)]
 for h,a in zip(gs,[8,17,26]):
  w=int(nodes[h]['order']);ell=a if w==27 or a%2==0 else a+27
  guards.append((w,ell))
 for d in range(54):
  assert any(d%w==ell for w,ell in guards) or (d%2==1 and d%3!=0)
 variant_count+=1
result['new_conditional_alternative_head_corollary']={'depth3_candidates':G3,'unordered_head_sets':20,'ordered_assignments':variant_count,'collapsed_cases':variant_count*54,'status':'CONDITIONAL_ONLY; not equivalence of arithmetic chain existence; all actual terminal hypotheses remain open'}
(R/'evidence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('nodes',len(nodes),'prime_certificates',len(proof),'families',len(fam),'local_comparisons',count,'matched_search_domains',sum('search'in v and 'replay_search'in v for v in scans.values()))
for z in fixture:print(z)
print('bounds',bounds)
