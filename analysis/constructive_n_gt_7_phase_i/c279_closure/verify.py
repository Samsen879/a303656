#!/usr/bin/env python3
"""Independent exact Pocklington/cubic exclusion and closure replay. Stdlib."""
import hashlib,json,math,sys
from pathlib import Path
P=Path(__file__).resolve().parent

def check(ok,message):
    if not ok: raise ValueError(message)

def certify(data):
    # Topological processing, rather than trusting certificate labels/receipts.
    nodes={int(k):v for k,v in data['prime_proofs'].items()}
    leaves={int(p) for v in nodes.values() for p in v['factors']} - set(nodes)
    certified=set()
    for p in sorted(leaves):
        check(2<=p<=10**9,'leaf bound')
        check(all(p%d for d in range(2,math.isqrt(p)+1)),'composite leaf')
        certified.add(p)
    while nodes:
        progress=False
        for n,v in list(nodes.items()):
            fs=[(int(p),e) for p,e in v['factors'].items()]
            check(n>1 and fs and all(type(e) is int and e>0 and 2<=p<n for p,e in fs),'node data')
            if any(p not in certified for p,e in fs): continue
            F=math.prod(p**e for p,e in fs)
            check((n-1)%F==0,'factor portion')
            for p,e in fs:
                a=v['witnesses'][str(p)]
                check(type(a) is int and 1<a<n,'witness domain')
                check(pow(a,n-1,n)==1,'Fermat')
                check(math.gcd(pow(a,(n-1)//p,n)-1,n)==1,'order gcd')
            if v['method']=='pocklington_sqrt': check(F**2>n,'sqrt mass')
            elif v['method']=='pocklington_cubic_nonsquare':
                check(F>1 and F**3>n,'cubic mass')
                s,r=divmod((n-1)//F,F);delta=r*r-4*s
                check(delta<0 or math.isqrt(delta)**2!=delta,'two-factor exclusion')
            else: raise ValueError('unknown theorem')
            certified.add(n);del nodes[n];progress=True
        check(progress,'missing or cyclic proof')
    return certified

def arithmetic(data):
    num=(5**279-1)*(5**3-1);den=(5**93-1)*(5**9-1)
    C,r=divmod(num,den);check(r==0,'closed formula division')
    phi={}
    for d in range(1,280):
        if 279%d: continue
        phi[d],r=divmod(5**d-1,math.prod(v for k,v in phi.items() if d%k==0))
        check(r==0,'cyclotomic recursion division')
    check(C==phi[279]==int(data['value']),'two evaluations')
    qs=list(map(int,data['prime_factors']))
    check(len(qs)==2 and len(set(qs))==2 and math.prod(qs)==C,'complete distinct product')
    certified=certify(data)
    for q in qs:
        check(q in certified,'prime certification')
        check(q%4==3 and 279%q!=0,'admission')
        check(pow(5,279,q)==1 and pow(5,93,q)!=1 and pow(5,9,q)!=1,'exact order')
        check(C%q==0 and C%(q*q)!=0 and pow(5,279,q*q)!=1,'valuation/square')
    return C,qs

def main():
    receipt=P/'SOURCE_RECEIPTS.json'
    if receipt.exists():
        hashes=json.loads(receipt.read_text())['selected_sha256']
        check(hashlib.sha256((P/'PRIMALITY_CERTIFICATE.json').read_bytes()).hexdigest()==hashes['PRIMALITY_CERTIFICATE.json'],'certificate source custody')
    data=json.loads((P/'PRIMALITY_CERTIFICATE.json').read_text())
    C,qs=arithmetic(data)
    result=P/'closure_result.json'
    if result.exists():
        expected=json.loads(result.read_text())
        check(expected['phi279_5']==str(C) and [f['q'] for f in expected['factors']]==list(map(str,qs)),'result identity')
        check(expected['squarefree'] is True and expected['Sq279_cardinality']==0 and expected['frozen_I7_order279_gate'] is False and expected['frozen_I7_instantiable'] is False,'closure result')
        for f in expected['factors']: check(f['prime_certified'] is True and f['mod4']==3 and f['order_5']==279 and f['valuation_in_phi']==1,'factor result')
        check(expected['t']==279 and expected['phi_factor_count']==2,'target/count')
        check(all(expected[k]=='UNRESOLVED' for k in ['general_N9_status','general_N_gt_7_status','A303656']),'scope result')
        for q,f in zip(qs,expected['factors']):
            check(f['order_residues']=={str(e):str(pow(5,e,q)) for e in [279,93,9]} and f['square_power_residue']==str(pow(5,279,q*q)),'recorded residues')
    print('PASS\nSq279_cardinality: 0\nFrozen_I7_order279_gate: FALSE\nFrozen_I7_architecture: CLOSED\nA303656: UNRESOLVED')

if __name__=='__main__': main()
