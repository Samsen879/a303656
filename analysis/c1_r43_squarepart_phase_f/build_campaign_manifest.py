from pathlib import Path
import re,json,math,hashlib
P=Path(__file__).resolve().parent
# Input bindings are recorded from the commands actually invoked in this session.
inputs={
'ecm903_benchmark.log':('R903_v1.txt','reconstruction'),
'ecm1806_benchmark.log':('C1806_trial.txt','reconstruction'),
'ecm1806_tier0.log':('C1806_trial.txt','reconstruction'),
'ecm903_tier0.log':('C903.txt','normalized'),
'ecm1806_tier0b.log':('C1806.txt','normalized'),
'ecm903_tier1.log':('C903.txt','normalized'),
'ecm1806_tier1.log':('C1806.txt','normalized'),
'ecm903_tier2a.log':('C903.txt','normalized'),
'ecm903_tier2a_resume.log':('C903.txt','normalized'),
'ecm1806_tier2a.log':('C1806.txt','normalized'),
'ecm903_tier2b.log':('C903.txt','normalized'),
'ecm1806_tier2b.log':('C1806.txt','normalized'),
'ecm903_tier2c.log':('C903.txt','normalized'),
'ecm903_tier3.log':('C903.txt','normalized'),
'ecm1806_tier3.log':('C1806.txt','normalized'),
'ecm1806_remainder_tier2.log':('R1806_after_new_factor.txt','remainder'),
'fresh_factor_replay.log':('C1806.txt','duplicate_positive_replay')}
rows=[];summary={};seen=set()
for file,(inp,group) in inputs.items():
 t=(P/file).read_text();m=re.search(r'B1 (\d+) B2 (\d+) D (\d+) curves (\d+) sigma_start (\d+)',t)
 assert m,file
 b1,b2,D,requested,start=map(int,m.groups())
 curves=re.findall(r'^CURVE (\d+) SIGMA (\d+) (.*)$',t,re.M)
 factors=sorted(set(re.findall(r'FACTOR (\d+)',t)))
 if 'NO_FACTOR COMPLETE' in t:state='completed_no_factor';assert len(curves)==requested
 elif factors:state='factor_found'
 else:state='timeout_partial';assert file=='ecm903_tier2a.log'
 digest=hashlib.sha256((P/inp).read_bytes()).hexdigest()
 row={'log':file,'input':inp,'input_file_sha256':digest,'group':group,'B1':b1,'nominal_B2':b2,'D':D,
      'stage2_prime_interval_upper_exclusive':b1+4*D*((b2-b1+4*D-1)//(4*D)),
      'requested_curves':requested,'completed_curves':len(curves),'sigma_start':start,
      'completed_sigmas':[int(c[1]) for c in curves],'factors':factors,'state':state}
 rows.append(row)
 if group in ('normalized','remainder'):
  k=(inp,b1,b2);summary[k]=summary.get(k,0)+len(curves)
  for _,sig,status in curves:
   unique=(digest,b1,b2,int(sig));assert unique not in seen,unique;seen.add(unique)
(P/'campaign_manifest.json').write_text(json.dumps({'historical_phase_e_effort':'UNAVAILABLE_NOT_INFERRED','ecm_engine':'custom C++/GMP reference port of SymPy 1.14.0; not GMP-ECM','ecm_runs':rows,'aggregate':[{'input':k[0],'B1':k[1],'B2':k[2],'completed_unique_curves':v} for k,v in summary.items()],
 'trial_exclusion':{'bound':10**12,'candidate_progression':'q=1807+1806*k; every integer, not just primes','candidates_per_C':(10**12-1807)//1806+1,'logs':['trial903_1e12.log','trial1806_1e12.log'],'R1806_inherits_from_exact_divisibility':True},
 'p_minus_1':{'C903_and_C1806':{'B1':10**6,'B2':10**7,'bases':[2,3,7]},'C903_and_R1806_additional':{'B1':10**6,'B2':10**8,'bases':[2]},'result':'all tested gcds 1'},
 'p_plus_1':{'C903_and_C1806':{'B1':10**6,'B2':'NOT_RUN','P_values':[3,4,16]},'result':'all tested gcds 1'},
 'rho':{'C903_and_C1806':{'seeds':[1,3],'requested_evaluations_per_seed':1000000,'actual_evaluations_per_seed':1000062},'result':'all tested gcds 1'},
 'not_run':['official GMP-ECM software','P+1 stage 2','NFS/SNFS','repository-native checkout/tests','Phase E original-log replay']},indent=2)+'\n')
print('ECM verified log aggregation:')
for k,v in summary.items():print(k,v)
