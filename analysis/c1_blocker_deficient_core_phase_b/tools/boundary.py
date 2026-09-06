#!/usr/bin/env python3
import json
from pathlib import Path
from math import gcd,lcm,prod
from arithmetic import row

def crt(pairs):
    x=0;M=1
    for a,m in pairs:
        if gcd(M,m)!=1:raise ValueError('pairwise coprime moduli required')
        x+=M*((a-x)*pow(M,-1,m)%m)
        M*=m
        x%=M
    assert all(x%m==a%m for a,m in pairs)
    return x,M

def run():
    q=1645333507;P=[3,1523,30469139,q]
    rows={p:row(p) for p in P}
    r={p:2 for p in P};r[q]=q+2
    constraints=[(0,2),(0,27),(1,761),(1,1429),(0,1523),(1,30469139)]
    d,M=crt(constraints)
    U=lcm(*(rows[p]['w'] for p in P))
    L=lcm(*(rows[p]['w']*p**max(0,2-rows[p]['s']) for p in P))
    assert U==L==M
    vals=[]
    for p in P:
        for c in (0,1):
            v=(r[p]-3**c-pow(5,d,p*p))%(p*p)
            kind='LOCAL_ZERO_UNRESOLVED' if v==0 else ('VALUATION_ONE_FATAL' if v%p==0 else 'VALUATION_ZERO_SAFE')
            assert kind!='VALUATION_ONE_FATAL'
            vals.append(dict(p=p,c=c,local_value_mod_p2=v,kind=kind))
    pair_logs=[0,rows[q]['w']//2]
    for c,a in enumerate(pair_logs):
        v=(r[q]-3**c-pow(5,a,q*q))%(q*q)
        assert v%q==0 and v!=0
    n,nmod=crt([(r[p],p*p) for p in P])
    return dict(P=P,K=2,E=[1],shared_residues=r,U=U,L=L,
        original_direct_core=[q],original_direct_neighborhood=[],
        dependency_released_route=[q,30469139,1429],
        q_rigid_anchor_logs=pair_logs,q_projected_digits_at_30469139=[a%30469139 for a in pair_logs],
        crt_constraints=[dict(residue=a,modulus=m) for a,m in constraints],
        common_odd_safe_exponent=d,row_evaluations=vals,
        compatible_global_residue=n,global_residue_modulus=nmod,
        not_a_complete_certificate=True,not_an_A303656_counterexample=True)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(run(),sort_keys=True,indent=2)+'\n')
