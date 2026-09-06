#!/usr/bin/env python3
"""Shallow actual-order gateways and exact six-root allocation certificate."""
import argparse,json
from pathlib import Path
from arithmetic import factor, admitted, row

def run():
    vals={3:5**2+5+1,6:5**2-5+1,9:5**6+5**3+1,
          18:5**6-5**3+1,5:sum(5**i for i in range(5)),
          10:sum((-1)**i*5**(4-i) for i in range(5))}
    polys={};gateways={}
    for m,v in vals.items():
        f=factor(v);got=[]
        for p in f:
            if admitted(p) and row(p)['w']==m: got.append(p)
        polys[str(m)]=dict(value=v,factorization=f,exact_admitted_order_primes=got)
        for p in got:gateways[str(p)]=row(p)
    assert sorted(polys['3']['exact_admitted_order_primes']+polys['6']['exact_admitted_order_primes'])==[7,31]
    assert sorted(polys['9']['exact_admitted_order_primes']+polys['18']['exact_admitted_order_primes'])==[19,5167]
    assert sorted(polys['5']['exact_admitted_order_primes']+polys['10']['exact_admitted_order_primes'])==[11,71]
    f3=[0,9,18,21,24,25,26]  # denominator 27
    f5=[0,5,10,11,12,13,14]  # denominator 25
    cases=[]
    for a in range(7):
        for b in range(7-a):
            for k in range(7-a-b):
                options=[x for x in range(k+1) if f3[a]+9*x<27 and f5[b]+5*(k-x)<25]
                assert options
                x=options[0]
                cases.append(dict(pure3=a,pure5=b,mixed=k,mixed_to3=x,
                    three_mass=[f3[a]+9*x,27],five_mass=[f5[b]+5*(k-x),25]))
    assert len(cases)==84
    return dict(cyclotomic_identities=polys,gateway_rows=gateways,
        f3_numerators=f3,f3_denominator=27,f5_numerators=f5,f5_denominator=25,
        allocations=cases,allocation_cases=len(cases),mismatches=0,
        claim_scope='no complete admitted C=1 certificate with at most six original nonregular rows',
        proof_not_computation='unbounded prime sizes, arbitrary regular support rows and precision')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
    result=run();a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('PASS', result['allocation_cases'])
