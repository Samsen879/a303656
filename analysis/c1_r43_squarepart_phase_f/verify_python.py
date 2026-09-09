#!/usr/bin/env python3
"""Dependency-free verifier of positive arithmetic claims. No probable-prime oracle.
Optional --mutations runs rejection tests. The 10^12 trial exclusion is replayed
by trial.cpp, not inferred from this fast verification.
"""
import json, hashlib, sys
from pathlib import Path
from math import gcd, isqrt, prod
P=Path(__file__).resolve().parent

def require(condition, message):
    if not condition: raise ValueError(message)

def check_primes(certificate):
    proven=set()
    for node in certificate['nodes']:
        p=int(node['p'])
        if p==2:
            require(node.get('base_case') is True,'base case');proven.add(p);continue
        require(p>2 and p%2==1 and p not in proven,'node validity')
        fs=[(int(r),int(e)) for r,e in node['factorization_p_minus_one']]
        require(len({r for r,e in fs})==len(fs),'distinct predecessor primes')
        require(all(r in proven and e>0 for r,e in fs),'unproved predecessor')
        require(prod(r**e for r,e in fs)==p-1,'p-1 product')
        a=int(node['a'])
        require(1<a<p and pow(a,p-1,p)==1,'Fermat certificate')
        for r,e in fs:require(gcd(pow(a,(p-1)//r,p)-1,p)==1,'Lucas gcd')
        proven.add(p)
    require(all(int(p) in proven for p in certificate['roots']),'root unproved')
    return proven

def mobius(n):
    m=n;count=0;d=2
    while d*d<=m:
        if m%d==0:
            m//=d;count+=1
            if m%d==0:return 0
        d+=1
    if m>1:count+=1
    return (-1)**count

def cyclo(n,a=5):
    num=den=1
    for d in range(1,n+1):
        if n%d:continue
        mu=mobius(n//d)
        if mu==1:num*=a**d-1
        if mu==-1:den*=a**d-1
    q,r=divmod(num,den);require(r==0,'cyclotomic exact division');return q

def verify(data,certificate):
    proven=check_primes(certificate)
    for key,rec in data['values'].items():
        v=int(rec['decimal'])
        require(rec['hex']==hex(v),'hex mismatch')
        require(rec['bits']==v.bit_length() and rec['digits']==len(str(v)),'lengths')
        require(hashlib.sha256(str(v).encode()).hexdigest()==rec['sha256_decimal_no_newline'],'decimal digest')
        require(isqrt(v)==int(rec['isqrt']),'isqrt')
        require(int(rec['fermat_base2_residue'])==pow(2,v-1,v),'Fermat residue')
        require(rec['fermat_base2_composite']==(pow(2,v-1,v)!=1),'composite flag')
        require(v%4==rec['mod4'] and v%13==rec['mod13'],'modular record')
    N={n:cyclo(n) for n in (903,1806)}
    for n in N:require(N[n]==int(data['values']['N'+str(n)]['decimal']),'N reconstruction')
    require(cyclo(903,-5)==N[1806],'signed identity')
    require(cyclo(903,25)==N[903]*N[1806],'product identity')
    require(gcd(N[903],N[1806])==1,'gcd N pair')
    for r in data['prime_factors']:
        q=int(r['p']);n=r['n'];w=r['order']
        require(q in proven,'factor unproved')
        require(q%4==r['mod4'] and q%5==r['mod5'],'prime congruences')
        require(pow(5,w,q)==1,'order divisibility')
        for t,res in r['proper_order_tests'].items():
            require(pow(5,int(t),q)==int(res)!=1,'proper order test')
        # Do not trust a possibly truncated set of proper-order tests.
        for ell in (2,3,7,43):
            if w%ell==0:require(str(w//ell) in r['proper_order_tests'],'missing proper test')
        v=N[n];e=0
        while v%q==0:v//=q;e+=1
        require(e==r['multiplicity']==1,'multiplicity')
        require(pow(5,w,q*q)==int(r['lift_power_mod_p_squared'])!=1,'lifting')
        require((N[n]//q)%q==int(r['quotient_mod_p'])!=0,'quotient valuation')
    C903=int(data['values']['C903']['decimal']);C1806=int(data['values']['C1806']['decimal']);R=int(data['values']['R1806']['decimal'])
    require(N[903]==149930509*1562986310551*C903,'903 product')
    require(N[1806]==43*246201060546547*C1806,'1806 product')
    require(C1806==147304138944416276237689*R,'fresh split')
    for name,v,n in [('C903',C903,903),('C1806',C1806,1806),('R1806',R,1806)]:
        require(gcd(v,n)==1 and v%1806==1,'order exceptions')
        require(pow(2,v-1,v)!=1,'composite witness absent')
        require(isqrt(v)**2!=v,'non-square')
        L=data['trial_bound']; k=data['values'][name]['omega_upper_bound_from_trial']
        require((L+1)**k<=v<(L+1)**(k+1),'Omega size conditional bound')
        require(isqrt(v//(L+1))==int(data['values'][name]['possible_repeated_prime_upper_bound']),'q-square bound')
    require(C903%4==3 and C1806%13==R%13==5,'small nonsquare certificates')
    require(gcd(C903,C1806)==gcd(R,147304138944416276237689)==1,'residual gcds')
    return len(proven)

if __name__=='__main__':
    data=json.loads((P/'arithmetic_audit.json').read_text());cert=json.loads((P/'primality_certificates.json').read_text())
    neighbors=json.loads((P/'neighbor_partial_factorizations.json').read_text())
    for name,rows in neighbors.items():
        original=int((P/(name+'.txt')).read_text())
        for delta,row in rows.items():
            factors=row['small_prime_factors']
            for q,e in factors:
                require(q>=2 and e>0 and all(q%d for d in range(2,isqrt(q)+1)),'neighbor small prime')
            require(prod(q**e for q,e in factors)*int(row['remaining_decimal'])==original+int(delta),'neighbor partial product')
    print('PASS: neighbor exact partial products; small-prime trial proofs (no residual prime claim)')
    count=verify(data,cert);print('PASS: arithmetic; signed/product identities; exact order; multiplicities; composite/nonsquare witnesses; '+str(count)+' Lucas prime nodes')
    if '--mutations' in sys.argv:
        from copy import deepcopy
        cases=[]
        c=deepcopy(cert);c['nodes'][-1]['a']='1';cases.append(('prime witness',data,c))
        c=deepcopy(cert);c['nodes'][-1]['factorization_p_minus_one'][-1][1]+=1;cases.append(('prime predecessor exponent',data,c))
        d=deepcopy(data);d['prime_factors'][-1]['multiplicity']=2;cases.append(('false repeated prime',d,cert))
        d=deepcopy(data);d['values']['R1806']['decimal']=str(int(d['values']['R1806']['decimal'])+2);cases.append(('residual mutation',d,cert))
        d=deepcopy(data);d['values']['C903']['fermat_base2_residue']='1';cases.append(('false PRP',d,cert))
        d=deepcopy(data);d['prime_factors'][-1]['proper_order_tests'].pop('903');cases.append(('missing exact-order test',d,cert))
        for name,d,c in cases:
            try:verify(d,c)
            except (ValueError,KeyError):print('REJECTED mutation:',name)
            else:raise RuntimeError('Mutation accepted: '+name)
