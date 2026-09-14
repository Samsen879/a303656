#!/usr/bin/env python3
"""Deterministic offline compact evidence replay; NEVER scan an original-n window."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from functools import lru_cache
from pathlib import Path
P=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise ValueError(msg)
def read(path):return json.loads(path.read_text())
def jsonlines(path):return [json.loads(x) for x in path.read_text().splitlines()]
def run(cmd,cwd,env):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=600)
    require(r.returncode==0,r.stdout+r.stderr);return r.stdout
@lru_cache(None)
def factor(n):
    if n==0:return []
    out=[];p=2
    while p*p<=n:
        e=0
        while n%p==0:n//=p;e+=1
        if e:out.append([p,e])
        p=3 if p==2 else p+2
    if n>1:out.append([n,1])
    return out
def powers(b,n):
    v=[];x=1
    while x<=n:v.append(x);x*=b
    return v
def i2_panel():
    data=read(P/'sources/i2/results.json');require(data['bound']==10000000,'source finite bound')
    count=0
    for target in data['extremal_panel']:
        n=target['n'];rows=target['all_pair_rows'];expected={(c,d):n-x-y for c,x in enumerate(powers(3,n)) for d,y in enumerate(powers(5,n)) if x+y<=n}
        require({(r['c'],r['d']):r['residual'] for r in rows}==expected and len(rows)==len(expected),'inclusive source domain')
        success=0
        for r in rows:
            m=r['residual'];ff=factor(m);require(ff==r['factors'],'I2 exact factorization')
            ok=not any(p%4==3 and e%2 for p,e in ff);require(ok==r['success'],'I2 norm criterion');success+=ok;count+=1
            if ok:require(bool(r.get('unordered_square_pairs')),'successful I2 witness missing')
            for a,b in r.get('unordered_square_pairs',[]):require(a*a+b*b==m,'I2 explicit square pair')
        require(success==target['successful_pairs'],'source R mismatch')
    return count
def pilot_replay(tmp,env):
    source=P/'finite/pilot';compiler=shutil.which('g++');require(compiler is not None,'C++17 g++ required, no automatic installation')
    exe=tmp/'reference';run([compiler,'-O3','-std=c++17',source/'reference.cpp','-o',exe],tmp,env)
    retained=jsonlines(source/'extremals.jsonl');expected={r['n']:r for r in retained};require(len(expected)==1991,'retained unique count')
    points=tmp/'points.txt';points.write_text('\n'.join(map(str,sorted(expected)))+'\n');out=tmp/'reference.jsonl'
    run([exe,points,out,'counts'],tmp,env)
    for row in jsonlines(out):
        target=expected[row['n']]
        for k in ['R','R_inclusive','active','R_bulk','A23','minres','pairs','zero_pairs']:require(row[k]==target[k],f'pilot retained mismatch {row["n"]} {k}')
    for filename in ['baseline_reference.jsonl']+[f'window_{l}_validation.jsonl' for l in 'ABC']:
        frozen=jsonlines(source/'tests'/filename);points.write_text('\n'.join(str(r['n']) for r in frozen)+'\n');run([exe,points,out,'counts'],tmp,env)
        rows=jsonlines(out);require(rows==frozen,'saved baseline/control/top32 exact R or pair mismatch '+filename)
    windows=read(source/'WINDOWS.json');require([(w['label'],w['L'],w['U']) for w in windows]==[('A',10**8,10**8+2**18),('B',10**10,10**10+2**18),('C',10**12,10**12+2**18)],'fixed windows changed')
    for w in windows:require(w['status']=='COMPLETE' and w['independent_validation']=='PASS','incomplete source window')
    summaries=read(source/'cross_scale_summary.json');require([r['minimum_R'] for r in summaries]==[9,13,20],'window minima changed')
    return len(retained)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--with-producers',action='store_true');args=ap.parse_args()
    for row in read(P/'SELECTED_PAYLOAD.json'):require(hashlib.sha256((P/row['repository_relative_path']).read_bytes()).hexdigest()==row['sha256'],'source custody '+row['repository_relative_path'])
    require(all(r['producer_replay']=='PASS' for r in read(P/'SOURCE_RECEIPTS.json')),'failed source included')
    count=i2_panel();env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONOPTIMIZE',None)
    with tempfile.TemporaryDirectory(prefix='direct_original_audit_') as name:
        tmp=Path(name)
        # K is standard-library only; regenerate exact rational spectra and six existing grids.
        k=tmp/'k';shutil.copytree(P/'sources/k',k);run([sys.executable,'-B','reference.py','--out',tmp/'k_generated'],k,env)
        frozen=read(k/'results.json');fresh=read(tmp/'k_generated/results.json');require(frozen==fresh,'K exact output differs')
        require(fresh['rho237_minimum']=='21/128' and fresh['rho23711_minimum']=='1869/12800','K minimum identity')
        require(fresh['minimizers_mod1848']==[238,392,406,560,574,728,910,1064,1414,1568],'K exact classes')
        k2=tmp/'k2';shutil.copytree(P/'sources/k2',k2);run([sys.executable,'-B','verify.py'],k2,env)
        ml=tmp/'ml';shutil.copytree(P/'finite/ml_d2',ml);run([sys.executable,'-B','verify_candidate.py','--n','3920'],ml,env)
        v=read(ml/'candidate_verification.json');require(v['rho_lower_gt_2'],'finite rho interval')
        retained=pilot_replay(tmp,env)
        if args.with_producers:
            i4=tmp/'i4';shutil.copytree(P/'sources/i4',i4);run([sys.executable,'-B','reference.py','--out',tmp/'i4_receipt.json'],i4,env)
            j=tmp/'j';shutil.copytree(P/'sources/j',j);run([sys.executable,'-B','reference.py','--output',tmp/'j_receipt.json'],j,env)
            run([sys.executable,'-B','local_oracle.py'],k,env)
            run([sys.executable,'-B','reference.py','--output-dir',tmp/'k2_generated'],k2,env)
    run([sys.executable,'-B','-m','unittest','discover','-s',P/'tests'],P,env)
    print(json.dumps({'status':'PASS','I2_fixed_panel_rows':count,'K_rational_minima_and_classes':'PASS','K2_fixed_certificates':'PASS','ML_D2_finite_3920_interval':'PASS','all_retained_pilot_targets':retained,'baseline_controls_top32':'PASS','new_window_scans':0,'full_1e7_rescan':False,'analytic_proofs_certified_by_script':False,'A303656':'UNRESOLVED','with_optional_producers':args.with_producers}))
if __name__=='__main__':main()
