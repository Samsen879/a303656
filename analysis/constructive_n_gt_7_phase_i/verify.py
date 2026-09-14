#!/usr/bin/env python3
"""Offline historical BOTH/OPEN replay plus current certified I7 closure."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    selected=json.loads((P/'SELECTED_PAYLOAD.json').read_text())
    for x in selected:require(hashlib.sha256((P/x['repository_relative_path']).read_bytes()).hexdigest()==x['sha256'],'payload custody')
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONOPTIMIZE',None)
    with tempfile.TemporaryDirectory(prefix='constructive_n_gt7_') as tmp:
        tmp=Path(tmp);producer=tmp/'producer';shutil.copytree(P/'reference/producer',producer)
        for flag,out in [([],tmp/'normal.json'),(['-O'],tmp/'optimized.json')]:
            subprocess.run([sys.executable,*flag,'-B','verifier.py','--mutations','--output',str(out)],cwd=producer,env=env,check=True,stdout=subprocess.PIPE,text=True)
            r=json.loads(out.read_text());require(r['status']=='PASS' and len(r['mutations'])==19 and all(m['rejected'] for m in r['mutations']),'semantic controls')
            require(r['actual']['cells']==27648 and r['actual_complete_certificate'] is False,'actual scope')
        subprocess.run([sys.executable,'-B',str(P/'reference/c279/verify_factors.py')],env=env,check=True,stdout=subprocess.PIPE,text=True)
    for script in ['verify.py','independent_verify.py']:
        replay=subprocess.run([sys.executable,'-B',str(P/'c279_closure'/script)],env=env,check=True,stdout=subprocess.PIPE,text=True)
        require('Sq279_cardinality: 0' in replay.stdout and 'Frozen_I7_architecture: CLOSED' in replay.stdout,'current closure replay')
    for filename,phrase in [('README.md','ARCHITECTURE: CLOSED'),('ARCHITECTURE.md','CLOSED BY'),('INSTANTIATION_GATES.md','|Sq(279)|=0'),('C279_GATE.md','frozen I7 architecture=CLOSED')]:
        require(phrase in (P/filename).read_text(),'stale current I7 status')
    print(json.dumps({'status':'PASS','actual_partial_cells':27648,'semantic_mutations':19,'normal':'PASS','optimized':'PASS','historical_C279':'OPEN','C279':'CLOSURE_CERTIFIED','Sq279_cardinality':0,'frozen_I7':'CLOSED','A303656':'UNRESOLVED'}))
if __name__=='__main__':main()
