#!/usr/bin/env python3
"""Read-only, standard-library certificate replay. No network / repository imports.
Usage: python verify.py --self-test
       python verify.py --suite all
Separate suites allow bounded-time execution without weakening any check.
"""
from pathlib import Path
from math import gcd,prod,isqrt
import argparse,copy,json,sys
from verify_certificates import verify_all,InvalidCertificate,require
from exact_arithmetic import factor_small,phi_recursive,phi_value,phi_derivative,cofactor_digits,strong_mr_composite
sys.set_int_max_str_digits(0)
BASE=Path(__file__).resolve().parent
RELAYS={43:42,127:42,379:21,7603:42,19531:7,519499:21}
TS=[1,2,3,6,7,14,21,42]
OLD={43,86,127,129,258}
NEW={254,301,379,381,602,758,762}
CLOSED=OLD|NEW

def load():
 return [json.loads((BASE/p).read_text()) for p in ('primality_certificates.json','arithmetic_records.json','order_table.json')]

def check_record(rec,primes):
 n=rec['n'];q=int(rec['q']);w=rec['exact_order']
 require(q in primes,'uncertified prime in arithmetic record')
 primitive=n%q!=0
 require(rec['primitive']==primitive,'primitive flag inconsistent')
 require(w==(n if primitive else RELAYS.get(q)),'wrong exact order / exceptional factor')
 require((q-1)%w==0 and pow(5,w,q)==1,'claimed order not an order')
 drops={str(p):str(pow(5,w//p,q)) for p in factor_small(w)}
 require(all(v!='1' for v in drops.values()) and drops==rec['order_drop_residues'],'exact-order drop failure')
 z=pow(5,w,q*q)
 require(z!=1 and z==int(rec['mod_q_squared']),'regularity / modular witness failure')
 require((z-1)%q==0 and (z-1)//q==int(rec['lifting_coefficient']),'lifting coefficient error')
 require(rec['q_mod_4']==q%4 and rec['admitted']==(q%4==3),'admission error')
 require(rec['proven_prime'] is True and rec['s_q']==1 and rec['valuation_in_Phi']==1,'invalid valuation or proof flag')
 # Primitive valuation = s_q. Exceptional n=q*ord_q has valuation 1 by LTE.
 if not primitive:require(n==q*w and n//q%q!=0,'exceptional index failure')

def check_metadata(recs,rows):
 expected={r*t for r in RELAYS for t in TS}
 require(len(rows)==48 and {r['n'] for r in rows}==expected,'48-index domain changed')
 require(len(recs)==75 and len({r['q'] for r in recs})==75,'factor occurrence inventory changed')
 require({r['n'] for r in rows if r['status'].startswith('EXCLUDED')}==CLOSED,'exclusion set changed')
 for row in rows:
  n=row['n'];r=row['r'];qs=row['known_prime_factors'];F=prod(map(int,qs))
  require(r in RELAYS and n in [r*t for t in TS],'relay/index mismatch')
  require(len(qs)==len(set(qs)),'duplicate claimed prime factor')
  require(sorted(qs,key=int)==sorted([x['q'] for x in recs if x['n']==n],key=int),'missing/extra arithmetic record')
  require(str(F)==row['known_product'],'known product mismatch')
  require(row['cofactor_expression']==f'Phi_{n}(5)/({F})','cofactor expression mismatch')
  require(row['derivative_gcd']==(r if n==r*RELAYS[r] else 1),'exception classification error')
  require(row['Phi_digits']==cofactor_digits(n),'Phi digit count failed')
  if n in CLOSED:
   require(row['cofactor_digits']==1 and row['cofactor_status']=='UNIT' and not row['square_prime_may_remain'],'closed cell misclassified')
  else:
   require(row['cofactor_digits']==cofactor_digits(n,F),'cofactor digit count failed')
   require(row['square_prime_may_remain'] is True,'unproved squarefree claim')
   require(row['status']==('OPEN_PARTIAL_FACTORIZATION' if F>1 else 'OPEN_NO_FACTOR_EXTRACTED'),'open status mismatch')
   require(row['cofactor_status'] in ('PROVEN_COMPOSITE','UNKNOWN_NOT_PRP_TESTED_SYMBOLIC'),'unapproved cofactor status')
  phase='D_REVERIFIED' if n in OLD else 'E_NEW' if n in NEW else None
  require(row['exclusion_phase']==phase,'new/imported exclusion mismatch')
 return {'indices':48,'closed':12,'new':7,'open':36,'factor_records':75}

def check_closed(rows):
 checked=0
 for row in rows:
  if row['n'] not in CLOSED:continue
  n=row['n'];F=prod(map(int,row['known_prime_factors']))
  require(phi_recursive(n)==phi_value(n)==F,'complete factorization product failed')
  checked+=1
 return {'complete_squarefree_products':checked}

def check_cofactors(rows,part):
 count=0
 for row in rows:
  if row['cofactor_status']!='PROVEN_COMPOSITE':continue
  n=row['n']
  if (part=='a' and n>8000) or (part=='b' and n<=8000):continue
  C=int((BASE/row['cofactor_decimal_file']).read_text());F=int(row['known_product'])
  require(C>1 and len(str(C))==row['cofactor_digits'],'cofactor decimal error')
  require(C*F==phi_recursive(n)==phi_value(n),'partial product failed')
  require(all(C%int(q)!=0 for q in row['known_prime_factors']),'known factor repeats in cofactor')
  require(strong_mr_composite(C,row['compositeness_MR_base']),'compositeness witness failed')
  count+=1
 return {'composite_cofactors_checked':count}

def check_gates(primes):
 products={7:[19531],14:[29,449],21:[379,519499],42:[7,43,127,7603]}
 admitted=set()
 for n,fs in products.items():
  require(all(p in primes for p in fs),'uncertified gate factor')
  require(prod(fs)==phi_recursive(n),'first-relay product failure')
  for p in fs:
   w=6 if p==7 else (RELAYS[p] if p in RELAYS else n)
   require(pow(5,w,p)==1 and all(pow(5,w//d,p)!=1 for d in factor_small(w)),'gate exact order failure')
   require(pow(5,w,p*p)!=1,'nonregular gate factor')
   if p%4==3 and w==n:admitted.add(p)
 require(admitted==set(RELAYS),'first-relay inventory mismatch')
 require(20771 in primes,'missing nonregular control prime')
 n=10385;q=20771
 require(factor_small(n)=={5:1,31:1,67:1},'control order support')
 require(pow(5,n,q)==1 and all(pow(5,n//p,q)!=1 for p in factor_small(n)),'control exact order failure')
 require(pow(5,n,q*q)==1 and pow(5,n,q**3)!=1,'control s!=2')
 for n,w in [(301,1),(602,1),(903,1),(1806,43)]:
  require(gcd(phi_recursive(n),phi_derivative(n))==w,'derivative gcd regression')
 require(pow(5,1806,43**2)==1 and pow(5,42,43**2)!=1,'imprimitive square-hit regression')
 return {'first_relay_products':4,'relay_primes':6,'derivative_gcds':4,'nonregular_control':20771}

def check_small_relays():
 """Independent full-closure check; orders found by repeated multiplication,
 not the producer's factor-removal algorithm or eligibility recursion.
 """
 data=json.loads((BASE/'small_relay_inventory.json').read_text())
 require(data['bound_inclusive']==2287,'small-relay bound changed')
 ps=[p for p in range(7,2288,4) if all(p%d for d in range(2,isqrt(p)+1))]
 require(len(ps)==data['prime_count']==173,'small-relay prime inventory')
 arithmetic={3:(2,1,{2:1})}
 for p in ps:
  z=5%p;w=1
  while z!=1:z=(z*5)%p;w+=1
  require(w<p,'small-prime multiplicative order failure')
  k=1
  while pow(5,w,p**(k+1))==1:k+=1
  arithmetic[p]=(w,k,factor_small(w))
 eligible=[]
 for row,p in zip(data['rows'],ps):
  require(row['p']==p,'small-relay row order changed')
  w,k,f=arithmetic[p]
  require((row['w'],row['s'],row['order_factors'])==(w,k,{str(a):b for a,b in f.items()}),'small-relay arithmetic mismatch')
  seen=set();todo=[p];terminals=set();basal=set();valid=True
  while todo:
   x=todo.pop()
   if x in seen:continue
   if x==3 or x%4==1:terminals.add(x);continue
   require(x in arithmetic and x<=p,'missing descendant arithmetic')
   seen.add(x);wx,sx,fx=arithmetic[x]
   valid=valid and sx==1 and all(e==1 for e in fx.values())
   odd={t for t in fx if t!=2}
   if odd=={3}:basal.add(x)
   todo.extend(odd)
  compatible=bool(valid and terminals=={3} and basal=={7})
  require(row['regular_B7_compatible_basin']==compatible,'small-relay closure mismatch')
  if compatible:eligible.append(p)
 require(len(data['rows'])==len(ps) and data['eligible']==eligible==[7,43,127,379,2287],'small-relay gate changed')
 survivors=sorted(r*t for r in RELAYS for t in TS if r*t<2287 and r*t not in CLOSED)
 require(survivors==[889,903,1137,1778,1806,2274],'low-order survivor list mismatch')
 require(43*127>2287 and arithmetic[2287][:2]==(254,1),'low-order branching / depth gate failure')
 return {'small_relay_primes_checked':173,'small_regular_B7_compatible':[7,43,127,379,2287],'B7_root_order_lower_bound':889,'four_vertex_root_order_lower_bound':2287,'low_order_survivors':survivors}

def negative_tests(certs,recs,rows,primes):
 checks=[]
 def rejects(name,fn):
  try:fn()
  except (InvalidCertificate,ValueError,KeyError,AssertionError):checks.append(name);return
  raise AssertionError('Mutation accepted: '+name)
 d=copy.deepcopy(certs);d['9']={'kind':'trial'};rejects('composite trial leaf',lambda:verify_all(d))
 key=next(k for k,r in certs.items() if r['kind']=='ec');d=copy.deepcopy(certs);d[key]['y']=str((int(d[key]['y'])+1)%int(key));rejects('EC point mutation',lambda:verify_all(d))
 d=copy.deepcopy(certs);d[key]['q']='2';rejects('EC Hasse threshold',lambda:verify_all(d))
 d=copy.deepcopy(certs);d[key]['a']='0';d[key]['b']='0';rejects('singular EC curve',lambda:verify_all(d))
 d=copy.deepcopy(certs);d[key]['q']=key;rejects('EC cyclic child',lambda:verify_all(d))
 key=next(k for k,r in certs.items() if r['kind']=='pocklington');d=copy.deepcopy(certs)
 d[key]['witnesses'][next(iter(d[key]['witnesses']))]=1;rejects('Pocklington witness mutation',lambda:verify_all(d))
 def record_mut(name,selector,k,v):
  r=copy.deepcopy(next(r for r in recs if selector(r)));r[k]=v;rejects(name,lambda:check_record(r,primes))
 record_mut('wrong exact order',lambda r:r['n']==301,'exact_order',43)
 record_mut('regular promoted nonregular',lambda r:r['n']==301,'s_q',2)
 record_mut('wrong admission',lambda r:r['q']=='66221','admitted',True)
 record_mut('imprimitive promoted primitive',lambda r:r['q']=='43','primitive',True)
 record_mut('wrong Phi multiplicity',lambda r:r['n']==602,'valuation_in_Phi',2)
 record_mut('lost exact-order drop test',lambda r:r['n']==301,'order_drop_residues',{})
 rr=copy.deepcopy(rows);r=next(r for r in rr if r['n']==301);r['known_prime_factors'].pop();rejects('omitted product factor',lambda:check_metadata(recs,rr))
 rr=copy.deepcopy(rows);r=next(r for r in rr if r['n']==903);r['square_prime_may_remain']=False;rejects('unproved cofactor squarefreeness',lambda:check_metadata(recs,rr))
 rr=copy.deepcopy(rows);r=next(r for r in rr if r['n']==903);r['status']='EXCLUDED_COMPLETE_SQUAREFREE_FACTORIZATION';rejects('all48 overpromotion',lambda:check_metadata(recs,rr))
 require(len(checks)==15,'mutation test count')
 return {'negative_tests_rejected':len(checks),'tests':checks}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--suite',choices=['all','core','cofactors-a','cofactors-b'],default='all');ap.add_argument('--self-test',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
 certs,recs,rows=load();primes=verify_all(certs);out={'suite':args.suite,'prime_certificate_nodes':len(primes),'certificate_types':{k:sum(r['kind']==k for r in certs.values()) for k in ('trial','pocklington','ec')}}
 if args.suite in ('all','core'):
  for r in recs:check_record(r,primes)
  out.update(check_metadata(recs,rows));out.update(check_closed(rows));out.update(check_gates(primes));out.update(check_small_relays())
 if args.suite in ('all','cofactors-a'):out['cofactors_a']=check_cofactors(rows,'a')
 if args.suite in ('all','cofactors-b'):out['cofactors_b']=check_cofactors(rows,'b')
 if args.self_test:out.update(negative_tests(certs,recs,rows,primes))
 out['PASS']=True
 text=json.dumps(out,indent=2);print(text)
 if args.output:args.output.write_text(text+'\n')
if __name__=='__main__':main()
