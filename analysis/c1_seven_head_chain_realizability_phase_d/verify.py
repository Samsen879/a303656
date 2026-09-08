#!/usr/bin/env python3
"""Independent, standard-library evidence checker, not a full C=1 certificate.

Default: recursive Lucas primality proofs, exact orders/valuations, complete and
partial factor identities, 1,051,305 actual row cases, conditional 54-cell cover,
all recorded admitted A/B streams, and the independent huge-31 bounded replay.
--replay-search additionally rebuilds and reruns both distinct native search cores.
No network, repository imports, SymPy, or GitHub writes.
"""
from pathlib import Path
from math import gcd,prod
from collections import deque
import argparse,csv,hashlib,json,subprocess,sys,tempfile,time
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(100000)
R=Path(__file__).resolve().parent

def need(ok,message):
 if not ok:raise ValueError(message)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--replay-search',action='store_true');opt=ap.parse_args()
 start=time.perf_counter();D=json.loads((R/'evidence.json').read_text());C=D['prime_certificates'];checked=set()
 need(D['authority']['main_sha']=='3fb4b4b4f71018017c7ea014ae7a1380f27b6b94' and D['authority']['main_tree']=='5ee6ab9e51f3e6d471991b7407de193d12777882','frozen authority')
 need(D['literal_head_order']==[31,7,19,5167,271,4159,31051],'literal head list')
 need(D['authority']['github_writes']=='NONE' and D['authority']['project']=='PAUSED' and D['authority']['active_promoted_route']=='NONE','state guard')
 def prime(n):
  n=int(n)
  if n in checked:return
  z=C[str(n)];need(int(z['n'])==n,'prime key')
  if n==2:need(z['kind']=='base','base proof');checked.add(n);return
  f={int(q):int(e) for q,e in z['factors'].items()}
  need(n>2 and n%2==1 and all(e>=1 for e in f.values()),'Lucas input')
  need(prod(q**e for q,e in f.items())==n-1,'full N-1 factor identity')
  for q in f:need(q<n,'recursive decrease');prime(q)
  a=int(z['a']);need(pow(a,n-1,n)==1,'Lucas Fermat witness')
  for q in f:need(gcd(pow(a,(n-1)//q,n)-1,n)==1,'Lucas gcd witness')
  checked.add(n)
 for n in C:prime(n)
 nodes={int(k):v for k,v in D['nodes'].items()}
 for q,z in nodes.items():
  prime(q);need(int(z['prime'])==q,'node key');w=int(z['order']);f={int(r):e for r,e in z['order_factorization'].items()}
  need(prod(r**e for r,e in f.items())==w,'order factor product')
  for r in f:prime(r)
  need((q-1)%w==0 and pow(5,w,q)==1,'order upper condition')
  for r in f:
   t=pow(5,w//r,q);need(t!=1 and str(t)==z['order_exclusions'][str(r)],'exact order exclusion')
  s=z['s'];need(s>=1,'s positive');need(pow(5,w,q**s)==1 and pow(5,w,q**(s+1))!=1,'exact valuation')
  need(z['regular']==(s==1) and z['admitted']==(q%4==3),'node classes')
  need(str(pow(5,w,q*q))==z['power_mod_q2'],'order lift')
  need(str(pow(5,w,q**(s+1)))==z['power_mod_q_s_plus_1'],'first nonunit lift')
  need(str(pow(5,q-1,q*q))==z['fermat_power_mod_q2'],'separate Fermat test')
 # Factor identities use arithmetic, not source table statuses.
 families={int(z['exponent']):z for z in D['families']}
 for n,z in families.items():
  prime(n);fs={int(p):e for p,e in z['proven_prime_factors'].items()};F=prod(p**e for p,e in fs.items())
  for p,e in fs.items():
   prime(p);need(nodes[p]['order']==str(n),'exact preimage edge')
   need(nodes[p]['s']==e,'factor multiplicity equals exact lift')
  need(pow(5,n,4*F)==1,'symbolic integer cofactor/divisibility')
  need(z['cofactor_expression']==f'(5^{n}-1)/{4*F}','exact cofactor expression')
  if 'cofactor_file' in z:
   b=(R/z['cofactor_file']).read_bytes();need(hashlib.sha256(b).hexdigest()==z['cofactor_sha256'],'cofactor digest')
   co=int(b);need(4*F*co+1==5**n,'full exact factor identity')
   need(len(str(co))==z['cofactor_digits'] and co%4==z['cofactor_mod4'],'cofactor metadata')
   if z['complete']:need(co==1,'complete factorization')
  else:need(not z['complete'],'symbolic factorization is not complete')
 # Rebuild the seven actual CRT rows independently from their defining congruences.
 actual_cases=0
 for z in D['conditional_fixture']['rows']:
  p,w=z['h'],z['w'];ell=z['ell'];a=z['center_mod_wh'];r=z['r_mod_h2']
  need(a%p==0 and a%w==ell and 0<=a<p*w,'head CRT center')
  need(r==(3+pow(5,a,p*p))%(p*p),'head shared residue')
  for d in range(p*w):
   value=(r-3-pow(5,d,p*p))%(p*p)
   fatal=(value%p==0 and value!=0)
   need(fatal==(d%w==ell and d%p!=0),'direct full-period head row')
   actual_cases+=1
 for d in range(6):
  value=(2-3-pow(5,d,9))%9
  need((value%3==0 and value!=0)==(d%2==1 and d%3!=0),'row3 full-period')
  actual_cases+=1
 need(actual_cases==D['conditional_fixture']['actual_local_row_comparisons'],'local count')
 for z in D['conditional_fixture']['collapsed_classes']:
  d=z['d_mod_54'];covered=[]
  for h in D['conditional_fixture']['rows']:
   if d%h['w']==h['ell']:covered.append(h['h'])
  if d%2 and d%3:covered.append(3)
  need(covered==z['conditional_cover_rows'] and bool(covered),'CONDITIONAL collapsed cover')
 for c in [0,1]:
  v=(1-3**c-1)%4
  need((v not in {0,1,2})==(c==0),'two-adic exact square-sum classes')
 # New conditional head replacement corollary; exact head orders are already proved.
 from itertools import permutations
 G=[163,271,487,4159,31051,16018507];variant_cases=0
 for assigned in permutations(G,3):
  guards=[(3,0),(6,4),(9,2),(18,14)]
  for q,a in zip(assigned,[8,17,26]):
   w=int(nodes[q]['order']);need(w in (27,54) and nodes[q]['s']==1,'alternative head arithmetic')
   ell=next(t for t in range(w) if t%27==a and (w==27 or t%2==0))
   guards.append((w,ell))
  for d in range(54):
   need(any(d%w==ell for w,ell in guards) or (d%2 and d%3),'alternative conditional parity cover')
   variant_cases+=1
 need(variant_cases==6480,'alternative conditional cases')
 # A/B match is a recorded execution check; --replay-search performs a new execution.
 scans={int(p):v for p,v in D['targeted_searches'].items()};paired=[]
 for p,v in scans.items():
  for folder,z in v.items():
   rows=list(csv.DictReader((R/folder/f'n_{p}.csv').open()))
   need([int(x['q']) for x in rows]==z['q_hits'],'recorded hit list')
   for x in rows:
    k=int(x['k']);q=int(x['q']);need(int(x['n'])==p and 1<=k<=z['K'] and q==2*p*k+1,'progression hit')
    need(pow(5,p,q)==1,'divisor hit exact power')
   receipt=json.loads((R/folder/f'n_{p}.json').read_text())
   need(int(receipt['K'])==z['K'] and receipt['modular_tests']==z['modular_tests'],'execution receipt')
  if 'search' in v and 'replay_search' in v:
   need(v['search']['K']==v['replay_search']['K'],'A/B same K')
   need([q for q in v['search']['q_hits'] if q%4==3]==v['replay_search']['q_hits'],'A/B admitted hits')
   paired.append(p)
 # Huge 31 replay intentionally uses a different traversal/filter/pow implementation.
 big=json.loads((R/'large31_independent_replay.json').read_text());p=big['exponent'];K=big['K']
 wheel=prod([3,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]);hits=[];nt=0
 for k in range(1,K+1,2):
  q=2*p*k+1
  if q%5 in (1,4) and gcd(q,wheel)==1:
   nt+=1
   if pow(5,p,q)==1:hits.append([k,q])
 need(hits==big['hits'] and nt==big['modular_tests'],'huge 31 independent replay')
 Q=big['relay'];need(all(pow(5,Q,2*Q*k+1)!=1 for k in range(1,big['relay_K_for_same_q_bound']+1,2)),'31 next relay bounded replay')
 # Independent breadth-first finite exclusion proof. No inference past a frontier.
 for h,b in D['terminal_lower_bounds'].items():
  need(b['scope']=='literal exact-prime-order chains only','lower-bound scope must not be inflated')
  bound=int(b['strictly_greater_than']);queue=deque([int(h)]);seen=set()
  while queue:
   p=queue.popleft()
   if p in seen:continue
   seen.add(p);need(nodes[p]['admitted'] and nodes[p]['s']==1,'bounded path endpoint must be regular')
   z=families[p]
   if z['complete']:children=list(map(int,z['proven_prime_factors']))
   else:
    last=(bound-1)//(2*p)
    if last%2==0:last-=1
    if p==big['exponent']:limit=big['K'];children=[q for k,q in hits]
    elif p==Q:limit=big['relay_K_for_same_q_bound'];children=[]
    else:
     need(p in paired,'independent A/B required for this bounded node')
     limit=scans[p]['search']['K'];children=scans[p]['replay_search']['q_hits']
    need(last<=limit,'unsearched node would invalidate lower bound')
   queue.extend(q for q in children if q%4==3 and q<=bound)
 # Inventory independently recertified, but bounded inventory exhaustiveness imported.
 need([q for q in nodes if nodes[q]['role']=='chain_factor' and nodes[q]['s']>=2]==[],'no terminal was instantiated')
 need(D['outcome']['all_seven_chains_exist']=='OPEN' and not D['conditional_fixture']['full_actual_certificate'],'logical output guards')
 if opt.replay_search:
  with tempfile.TemporaryDirectory(prefix='a303656_chain_replay_') as tmp:
   exes={}
   for source,name,link in [('target_divisors.cpp','a',[]),('target_divisors_gmp.cpp','b',['-lgmpxx','-lgmp'])]:
    exe=str(Path(tmp)/name);subprocess.run(['g++','-O3','-std=c++17',str(R/source),'-o',exe]+link,check=True);exes[name]=exe
   for p in paired:
    K=scans[p]['search']['K']
    for name,folder in [('a','search'),('b','replay_search')]:
     run=subprocess.run([exes[name],str(p),str(K)],capture_output=True,text=True,check=True)
     need(run.stdout==(R/folder/f'n_{p}.csv').read_text(),'fresh native search replay '+str(p))
 result={'arithmetic_proofs':'PASS','certified_primes_in_recursive_DAG':len(checked),'node_records':len(nodes),'complete_first_preimages':[7,19,31],
  'partial_factor_families':sum(not z['complete'] for z in families.values()),'actual_local_row_comparisons':actual_cases,'conditional_collapsed_classes':54,'additional_conditional_head_variant_cases':variant_cases,
  'recorded_independent_A_B_domains':len(paired),'huge31_python_replay':'PASS','finite_terminal_lower_bounds':'PASS',
  'fresh_all_native_search_replay':'PASS' if opt.replay_search else 'NOT_REQUESTED; recorded A/B domains and hits checked',
  'full_actual_C1_certificate_verified':False,'all_seven_chains_exist':'OPEN','github_writes':'NONE','seconds':time.perf_counter()-start}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
