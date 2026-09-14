#!/usr/bin/env python3
"""Offline custody, exact finite BOTH/mutation and OPEN target replay."""
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
    print(json.dumps({'status':'PASS','actual_partial_cells':27648,'semantic_mutations':19,'normal':'PASS','optimized':'PASS','C279':'OPEN','certified_square_hits':0,'A303656':'UNRESOLVED'}))
if __name__=='__main__':main()
