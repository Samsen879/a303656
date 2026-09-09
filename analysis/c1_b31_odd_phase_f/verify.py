#!/usr/bin/env python3
"""Standard-library verifier for the local B31-odd Phase F arithmetic evidence.

Uses recursive full n-1 Lucas certificates, not probable-prime declarations.
No network, repository checkout, third-party math library, or source code import.
The infinite-domain theorems require the written proofs; tests do not prove them.
"""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, math
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def verify_primes(certificates: dict[str, Any]) -> set[int]:
    verified: set[int]=set()
    visiting: set[int]=set()
    def visit(p: int) -> None:
        if p in verified: return
        require(p not in visiting, 'cyclic prime certificate')
        require(str(p) in certificates, f'missing prime certificate: {p}')
        c=certificates[str(p)]
        require(int(c['p'])==p, 'prime label mismatch')
        if p==2:
            verified.add(p); return
        require(p>2 and p%2==1, 'invalid prime label')
        visiting.add(p)
        fs={int(q):int(e) for q,e in c['n_minus_1'].items()}
        require(all(1<q<p and e>0 for q,e in fs.items()), 'invalid n-1 factors')
        require(math.prod(q**e for q,e in fs.items())==p-1, 'incomplete n-1 factorization')
        for q in fs: visit(q)
        a=int(c['a'])
        require(1<a<p, 'invalid Lucas witness')
        require(pow(a,p-1,p)==1, 'Lucas Fermat condition fails')
        require(all(math.gcd(pow(a,(p-1)//q,p)-1,p)==1 for q in fs),
                'Lucas order condition fails')
        visiting.remove(p); verified.add(p)
    for key in certificates: visit(int(key))
    return verified

def trial_factor(n: int) -> dict[int,int]:
    f: dict[int,int]={};p=2
    while p*p<=n:
        while n%p==0:
            f[p]=f.get(p,0)+1;n//=p
        p=3 if p==2 else p+2
    if n>1:f[n]=f.get(n,0)+1
    return f

def phi_value(n: int) -> int:
    # Called only for the small indices in complete factorization certificates.
    f=trial_factor(n); primes=list(f);num=den=1
    for mask in range(1<<len(primes)):
        d=math.prod(primes[i] for i in range(len(primes)) if mask>>i&1)
        term=pow(5,n//d)-1
        if mask.bit_count()%2:den*=term
        else:num*=term
    require(num%den==0,'cyclotomic division nonexact')
    return num//den

def verify_rows(data: dict[str,Any], primes: set[int]) -> None:
    for label,r in data['rows'].items():
        p,w,s=int(label),int(r['w']),int(r['s'])
        require(p in primes and int(r['p'])==p,'uncertified row prime')
        fs={int(q):int(e) for q,e in r['w_factorization'].items()}
        require(all(q in primes and e>0 for q,e in fs.items()),'uncertified order factors')
        require(math.prod(q**e for q,e in fs.items())==w,'order factorization mismatch')
        require(w>0 and (p-1)%w==0,'order does not divide p-1')
        require(pow(5,w,p)==1 and all(pow(5,w//q,p)!=1 for q in fs),'order drop test fails')
        require(s>=1 and pow(5,w,p**s)==1,'claimed valuation too large')
        z=pow(5,w,p**(s+1))
        require(z!=1 and z==int(r['mod_p_to_s_plus_1']),'claimed valuation wrong')
        require(r['mod4']==p%4 and r['mod20']==p%20,'congruence mismatch')
        require(r['odd_order']==(w%2==1),'odd order flag wrong')
        require(r['admitted']==(p%4==3),'admission flag wrong')
        require(r['regular']==(s==1),'regularity flag wrong')
        expected=(pow(5,w,p*p)-1)//p if s==1 else 0
        require(int(r['lifting_coefficient'])==expected,'lifting coefficient mismatch')

def descendants(p: int, rows: dict[str,Any]) -> tuple[set[int],set[int]]:
    if p==3 or p%4==1:return set(),{p}
    require(str(p) in rows,'closure row is missing')
    ds,ts={p},set()
    for ell in map(int,rows[str(p)]['w_factorization']):
        if ell==2:continue
        require(ell<p,'nondecreasing order edge')
        a,b=descendants(ell,rows);ds|=a;ts|=b
    return ds,ts

def good_state(R: set[int], rows: dict[str,Any]) -> bool:
    if 31 not in R or 3 in R:return False
    for p in R:
        r=rows.get(str(p))
        if r is None or p%4!=3 or int(r['s'])!=1 or int(r['w'])%2!=1:return False
        if any(int(e)!=1 for e in r['w_factorization'].values()):return False
        factors=set(map(int,r['w_factorization']))
        if not factors<=R|{3}:return False
        ds,ts=descendants(p,rows)
        if not ds<=R or ts!={3}:return False
    return True

def family(R: set[int], rows: dict[str,Any]) -> tuple[set[int],list[int]]:
    require(good_state(R,rows),'not a good regular state')
    proper=set()
    for p in R:proper|=descendants(p,rows)[0]-{p}
    A=R-proper
    optional=sorted(R-A)
    J=[]
    for mask in range(1<<len(optional)):
        S=A|{optional[i] for i in range(len(optional)) if mask>>i&1}
        for e in [0,1]:J.append(3**e*math.prod(S))
    return A,sorted(J)

def verify_arithmetic(data: dict[str,Any], replay_probe: bool=True) -> dict[str,int]:
    primes=verify_primes(data['primality_certificates'])
    verify_rows(data,primes)
    for group in ['first_layer_factorizations','shallow_source_identities_recomputed']:
        for item in data[group]:
            n=int(item['n']);fs={int(p):int(e) for p,e in item['factorization'].items()}
            require(all(p in primes and e==1 for p,e in fs.items()),'uncertified or repeated full factor')
            value=phi_value(n)
            require(value==int(item['value'])==math.prod(p**e for p,e in fs.items()),'complete product mismatch')
    first=set()
    for item in data['first_layer_factorizations']:
        n=int(item['n'])
        for p in map(int,item['factorization']):
            row=data['rows'][str(p)]
            if p%4==3 and int(row['w'])==n:
                require(row['regular'],'unexpected terminal square hit')
                first.add(p)
    require(first==set(map(int,data['first_relay_set']))=={878851,625552508473588471},'first relay set wrong')
    expected={c*r for c in [1,3,31,93] for r in first}
    require(expected=={int(z['n']) for z in data['three_vertex_orders']},'three-vertex family wrong')
    for z in data['three_vertex_orders']:
        require(math.prod(int(p)**int(e) for p,e in z['factorization'].items())==int(z['n']), 'terminal order product mismatch')
    for q,z in data['sanity_closures'].items():
        d,t=descendants(int(q),data['rows'])
        require(d==set(map(int,z['D'])) and t==set(map(int,z['T'])),'sanity closure mismatch')
    for RR in data['actual_regular_closed_states']:
        R=set(map(int,RR));require(good_state(R,data['rows']),'regular state invalid')
        A,J=family(R,data['rows'])
        require(len(J)==2**(1+len(R)-len(A)),'state family size wrong')
        # Finite independent check of the maximal-generator criterion.
        sr=sorted(R)
        for mask in range(1,1<<len(sr)):
            S={sr[i] for i in range(len(sr)) if mask>>i&1}
            closure=set().union(*(descendants(p,data['rows'])[0] for p in S))
            require((closure==R)==(A<=S),'maximal-generator criterion mismatch')
    # Source-normal-form geometry, using the actual mandatory even heads.
    require(int(data['rows']['7']['w'])==6 and int(data['rows']['5167']['w'])==18,'even gateway orders')
    profiles=[]
    for a in range(3):
        for b in range(3):
            for c in range(7):
                if a+b+c==7 and 9*a+3*b+c==27:profiles.append((a,b,c))
    require(profiles==[(2,2,3)],'shallow seven-leaf profile')
    leaves=[(3,0),(3,1),(9,2),(9,5),(27,8),(27,17),(27,26)]
    require(all(sum(d%m==a for m,a in leaves)==1 for d in range(27)),'selected frontier not exact')
    for center in range(27):
        # Necessary full coverage of both the lost 7 leaf and lost 5167 leaf
        # by a regular row3 accepting positive odd valuations.
        covered=True
        for d in range(27):
            if not (d%3==1 or d%9==5):continue
            delta=(d-center)%27
            if delta==0:covered=False;break
            v=0
            while delta%3==0:delta//=3;v+=1
            if (1+v)%2==0:covered=False;break
        require(covered==(center%3==0),'opposite parity center restriction')
    for d in range(54):
        if d%2==0:
            require(any(d%m==a for m,a in leaves),'selected even frontier')
        else:
            row3=(2-3-pow(5,d,9))%9
            fatal3=(row3%3==0 and row3!=0)
            require(fatal3==(d%3!=0),'row3 opposite-parity fixture')
            require(fatal3 or d%3==0,'conditional odd completion')
    total=0;nhits=0
    if replay_probe:
        for z in data['bounded_divisor_probe']:
            n=int(z['n']);fs=set(map(int,next(x for x in data['three_vertex_orders'] if int(x['n'])==n)['factorization']))
            found=[];tested=0
            for k in range(1,int(z['k_max'])+1,2):
                q=2*k*n+1
                if q%20 not in (11,19):continue
                tested+=1
                if pow(5,n,q)!=1:continue
                if not all(pow(5,n//p,q)!=1 for p in fs):continue
                require(q in primes,'unclassified modular hit in probe')
                found.append((q,k,pow(5,n,q*q)))
            expected_hits=[(int(h['q']),int(h['k']),int(h['lifting_remainder'])) for h in z['hits']]
            require(found==expected_hits,'probe replay mismatch')
            require(tested==z['tested']==20000,'probe count mismatch')
            require(all(z!=1 for q,k,z in found),'unexpected nonregular hit')
            total+=tested;nhits+=len(found)
    return {'prime_certificates':len(primes),'rows':len(data['rows']),'probe_candidates':total,'probe_prime_hits':nhits}

def mutation_tests(data: dict[str,Any]) -> int:
    count=0
    mutations=[]
    z=copy.deepcopy(data);z['rows']['878851']['odd_order']=False;mutations.append(z)
    z=copy.deepcopy(data);z['rows']['878851']['lifting_coefficient']='0';mutations.append(z)
    z=copy.deepcopy(data);z['primality_certificates']['625552508473588471']['a']='1';mutations.append(z)
    z=copy.deepcopy(data);z['first_layer_factorizations'][1]['value']=str(int(z['first_layer_factorizations'][1]['value'])+1);mutations.append(z)
    z=copy.deepcopy(data);z['first_relay_set'].append('31');mutations.append(z)
    for z in mutations:
        try:verify_arithmetic(z,False)
        except (ValueError,KeyError):count+=1
        else:raise ValueError('corruption was not rejected')
    for R in [{31,3},{31,7},{31,19},{878851}]:
        require(not good_state(R,data['rows']),'malformed state accepted');count+=1
    return count

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-probe',action='store_true')
    args=parser.parse_args()
    data=json.loads((HERE/'arithmetic_certificates.json').read_text())
    result=verify_arithmetic(data,not args.skip_probe)
    result['mutation_tests_rejected']=mutation_tests(data)
    result['status']='PASS'
    result['proof_scope']='finite evidence only; infinite statements use REPORT.md'
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
