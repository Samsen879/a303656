#!/usr/bin/env python3
"""Phase G finite reference checks. Standard library only; no network or scans.

Run: python3 reference.py --self-test --output evidence.json
This verifies explicit certificates and modular identities. The unbounded
lemmas are proved in PROOFS.md, not certified by finite tests.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
from math import gcd, prod
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parent
R1=878851
R2=625552508473588471
Q0=490398859
MULTIPLIERS=(1,3,31,93)
KNOWN=(20771,40487,53471161,1645333507,6692367337,188748146801)

class CheckFailure(RuntimeError): pass

def require(ok: bool, message: str) -> None:
    if not ok: raise CheckFailure(message)

def validate_certificates(document: dict[str,Any]) -> set[int]:
    cs=document['certificates']; verified:set[int]=set(); active:set[int]=set()
    def visit(n:int)->None:
        if n in verified:return
        require(n not in active, 'certificate cycle')
        require(str(n) in cs, f'missing certificate: {n}')
        c=cs[str(n)]
        require(c['n']==n, 'certificate label mismatch')
        if n==2:
            require(c['factors']=={} and c['witness'] is None,'bad base certificate')
            verified.add(2);return
        require(n>2 and n%2==1,'non-odd candidate')
        active.add(n)
        factors={int(p):e for p,e in c['factors'].items()}
        require(bool(factors) and all(type(e) is int and e>=1 and 2<=p<n for p,e in factors.items()),'bad factors')
        require(prod(p**e for p,e in factors.items())==n-1,'incomplete n-1 factorization')
        for p in factors:visit(p)
        a=c['witness']
        require(type(a) is int and 1<a<n,'bad Lucas witness')
        require(pow(a,n-1,n)==1,'Lucas Fermat failure')
        require(all(gcd(pow(a,(n-1)//p,n)-1,n)==1 for p in factors),'Lucas order failure')
        active.remove(n); verified.add(n)
    for n in sorted(map(int,cs)):visit(n)
    return verified

def exact_order(base:int,q:int,n:int,fs:dict[int,int],primes:set[int])->None:
    require(q in primes,'uncertified modulus')
    require(prod(p**e for p,e in fs.items())==n,'bad order factorization')
    require(all(p in primes and type(e) is int and e>=1 for p,e in fs.items()),'uncertified order factors')
    require((q-1)%n==0 and pow(base,n,q)==1,'order does not divide target')
    require(all(pow(base,n//p,q)!=1 for p in fs),'order drop failure')

def small_factors(n:int)->dict[int,int]:
    # Only used for the fixed tiny integer domain n<=651 and multipliers <=93.
    require(1<=n<=651,'small factorization gate')
    out={};d=2
    while d*d<=n:
        while n%d==0:out[d]=out.get(d,0)+1;n//=d
        d+=1
    if n>1:out[n]=out.get(n,0)+1
    return out

def index_factors(r:int,m:int)->dict[int,int]:
    out={r:1};out.update(small_factors(m));return out

def cyclo_squarefree_mod(base:int,fs:dict[int,int],modulus:int)->int:
    """Mobius product, only when every denominator is a unit."""
    require(all(e==1 for e in fs.values()),'not squarefree')
    ps=tuple(fs);t=len(ps);out=1
    for mask in range(1<<t):
        d=prod(ps[i] for i in range(t) if mask>>i&1)
        term=(pow(base,d,modulus)-1)%modulus
        if (t-mask.bit_count())%2:
            require(gcd(term,modulus)==1,'nonunit cyclotomic denominator')
            out=out*pow(term,-1,modulus)%modulus
        else:out=out*term%modulus
    return out

def quotient_prime_cyclo_mod(base:int,r:int,modulus:int)->int:
    den=(base-1)%modulus
    require(gcd(den,modulus)==1,'nonunit prime-index denominator')
    return (pow(base,r,modulus)-1)*pow(den,-1,modulus)%modulus

def crt2(a:int,m:int,b:int,n:int)->int:
    require(gcd(m,n)==1,'CRT not coprime')
    return (a+m*((b-a)*pow(m,-1,n)%n))%(m*n)

def qquot(base:int,q:int)->int:
    require(gcd(base,q)==1,'Fermat quotient nonunit base')
    z=pow(base,q-1,q*q)
    require((z-1)%q==0,'Fermat quotient requires prime')
    return (z-1)//q

def valuation_residue(z:int,q:int,precision:int)->int:
    if z==0:return precision
    e=0
    while z%q==0:e+=1;z//=q
    return e

# Low-degree exact polynomial algebra, coefficients in ascending order.
def trim(p:list[int])->list[int]:
    while len(p)>1 and p[-1]==0:p.pop()
    return p

def pmul(a:list[int],b:list[int])->list[int]:
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return trim(z)

def pdiv(a:list[int],b:list[int])->list[int]:
    a=a[:];out=[0]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and a!=[0]:
        i=len(a)-len(b)
        require(a[-1]%b[-1]==0,'polynomial quotient nonintegral')
        x=a[-1]//b[-1];out[i]=x
        for j,y in enumerate(b):a[i+j]-=x*y
        trim(a)
    require(a==[0],'polynomial nonzero remainder')
    return trim(out)

PHI={1:[-1,1]}
def phi_small(n:int)->list[int]:
    require(1<=n<=651,'polynomial degree gate')
    if n not in PHI:
        f=[-1]+[0]*(n-1)+[1]
        for d in range(1,n):
            if n%d==0:f=pdiv(f,phi_small(d))
        PHI[n]=f
    return PHI[n]

def subst_power(f:list[int],d:int,c:int=1)->list[int]:
    out=[0]*(d*(len(f)-1)+1)
    for i,a in enumerate(f):out[d*i]=a*c**i
    return trim(out)

def evaluate(f:list[int],x:int)->int:
    y=0
    for c in reversed(f):y=y*x+c
    return y

def evaluate_mod(f:list[int],x:int,mod:int)->int:
    y=0
    for c in reversed(f):y=(y*x+c)%mod
    return y

def self_tests(document:dict[str,Any],primes:set[int])->dict[str,Any]:
    bad=copy.deepcopy(document);bad['certificates'][str(Q0)]['witness']=1
    def rejects(fn)->bool:
        try:fn()
        except (CheckFailure,ValueError,KeyError):return True
        return False
    require(rejects(lambda:validate_certificates(bad)),'bad witness accepted')
    bad=copy.deepcopy(document);bad['certificates'][str(R1)]['factors']['3']=3
    require(rejects(lambda:validate_certificates(bad)),'bad factorization accepted')
    require(rejects(lambda:exact_order(5,R1,31,{31:1},primes)),'wrong exact order accepted')
    require(rejects(lambda:cyclo_squarefree_mod(1,{3:1},49)),'nonunit denominator accepted')
    require(pow(5,R1,Q0*Q0)!=1,'fixed base 5 incorrectly marked a target hit')
    return {'corrupted_Lucas_witness_rejected':True,'incomplete_factorization_rejected':True,
            'wrong_order_rejected':True,'nonunit_denominator_rejected':True,
            'variable_base_not_substituted_for_5':True}

def run(document:dict[str,Any],do_self_test:bool)->dict[str,Any]:
    primes=validate_certificates(document)
    source_rows=[]
    for p,n,expected in [(31,3,4),(R1,93,482192),(R2,31,7444),(Q0,93*R1,183120337)]:
        fs={3:1} if p==31 else ({3:1,31:1} if p==R1 else ({31:1} if p==R2 else {3:1,31:1,R1:1}))
        exact_order(5,p,n,fs,primes)
        lift=(pow(5,n,p*p)-1)//p
        require(lift==expected and lift!=0,'source regularity mismatch')
        source_rows.append({'prime':p,'base':5,'order':n,'lift_mod_prime':lift,'s':1})
    # Only the two small source factorizations are physically constructed.
    phi31=(5**31-1)//4
    phi93=(5**93-1)*4//((5**31-1)*(5**3-1))
    factors31=[1861,R2];factors93=[31,148429,R1,172974812463239310024750410929]
    require(all(p in primes for p in factors31+factors93),'uncertified source factors')
    require(prod(factors31)==phi31 and prod(factors93)==phi93,'first-relay product mismatch')
    indices=[r*m for r in (R1,R2) for m in MULTIPLIERS]
    B=prod([2,3,5,7,11,13,17,19,23,29])*150000
    inventory=[]
    for q in KNOWN:
        c=document['known_orders'][str(q)];n=c['order'];fs={int(p):e for p,e in c['order_factors'].items()}
        exact_order(5,q,n,fs,primes)
        require(pow(5,n,q*q)==1,'known Wieferich failed')
        z=(pow(5,n,q**3)-1)//(q*q)
        require(0<z<q,'known exact s=2 failed')
        require(n not in indices,'published inventory hits target')
        inventory.append({'q':q,'mod4':q%4,'order':n,'order_factorization':c['order_factors'],'s':2,'second_lift':z,'target_index':False})
    k=(B-1)//(2*R1)+1
    while k%2==0 or (1+2*k*R1)%20 not in (11,19):k+=1
    # Four exact-target variable-base countermodels; q is a source prime, not scanned.
    M=4*3**2*5**2*31**2*R1**2
    models=[]
    for m in MULTIPLIERS:
        n=m*R1
        omega=pow(5,(93//m)*Q0,Q0*Q0)
        A=crt2(5,M,omega,Q0*Q0)
        require(A!=5 and A%M==5 and A%25==5,'bad model base')
        exact_order(A,Q0,n,index_factors(R1,m),primes)
        exact_order(A,31,3,{3:1},primes)
        exact_order(A,R1,93,{3:1,31:1},primes)
        require(pow(A,3,31*31)==pow(5,3,31*31),'lower 31 changed')
        require(pow(A,93,R1*R1)==pow(5,93,R1*R1),'lower relay changed')
        q3=Q0**3;v=(pow(A,n,q3)-1)%q3
        require(valuation_residue(v,Q0,3)==2,'model not exact s=2')
        phi=cyclo_squarefree_mod(A,index_factors(R1,m),q3)
        require(valuation_residue(phi,Q0,3)==2,'cyclotomic valuation mismatch')
        transfers=[]
        for d in MULTIPLIERS:
            h=quotient_prime_cyclo_mod(pow(A,d,q3),R1,q3)
            val=valuation_residue(h,Q0,3)
            require(val==(2 if d%m==0 else 0),'multiplier valuation mismatch')
            require(qquot(pow(A,d,Q0*Q0),Q0)==d*qquot(A,Q0)%Q0,'quotient power mismatch')
            transfers.append({'d':d,'valuation':val,'residue_mod_q3':h})
        models.append({'multiplier':m,'r':R1,'n':n,'q':Q0,'base':A,'base_is_5':False,
                       'v5_base':1,'preserved_modulus':M,'root_s':2,
                       'proper_admitted_closure':[31,R1],'lower_orders':{'31':3,str(R1):93},
                       'lower_s':{'31':1,str(R1):1},'phi_residue_mod_q3':phi,'power_quotient':0,
                       'multiplier_transfer':transfers,
                       'interpretation':'VARIABLE-BASE ANALOGUE ONLY; NOT a base-5 B31 member; E8 CRT specialization'})
    # Small non-Wieferich roots verify that the conditions can all fail together as well.
    q=1303
    # Prime certificate may be absent; complete trial division is enough in this tiny test.
    require(all(q%d for d in range(2,37)),'toy q composite')
    g=2
    while not all(pow(g,(q-1)//p,q)!=1 for p in (2,3,7,31)):g+=1
    toy=[]
    for m in MULTIPLIERS:
        n=7*m;a=pow(g,(q-1)//n,q)
        if pow(a,n,q*q)==1:a+=q
        require(pow(a,n,q)==1 and pow(a,n,q*q)!=1,'toy regularity failed')
        fs=index_factors(7,m);q3=q**3
        vals=[]
        for d in MULTIPLIERS:
            z=quotient_prime_cyclo_mod(pow(a,d,q3),7,q3)
            val=valuation_residue(z,q,3)
            require(val==(1 if d%m==0 else 0),'regular transfer mismatch')
            vals.append(val)
        toy.append({'m':m,'n':n,'q':q,'base':a,'s':1,'transfer_valuations':vals})
    # Polynomial identities: a finite regression only, degrees <= 558.
    polynomial_checks=[]
    for r in (2,7):
        for d in MULTIPLIERS:
            left=subst_power(phi_small(r),d)
            right=[1]
            for m in MULTIPLIERS:
                if d%m==0:right=pmul(right,phi_small(r*m))
            require(left==right,'composition polynomial identity failure')
            polynomial_checks.append({'r':r,'d':d,'degree':len(left)-1,'passed':True})
    # Exact r^2-normalized aggregate residue without materializing huge values.
    aggregate=[]
    for r in (R1,R2):
        D=r*(5**93-1)
        z=(pow(5,93*r,D*r*r)-1)%(D*r*r)
        require(z%D==0,'aggregate division failure')
        z=z//D
        H=((5**93-1)//r)%r
        expected=(1-r*H*pow(2,-1,r))%(r*r)
        require(z==expected,'aggregate residue formula mismatch')
        aggregate.append({'r':r,'Z_mod_r2':z,'H':H,'kappa':(-H*pow(2,-1,r))%r,
                          'new_individual_q_obstruction':False})
    # Boundary control for ramification/Aurifeuillean hypotheses.
    minus=[1,-5,15,-25,25];plus=[1,5,15,25,25]
    require(pmul(minus,plus)==subst_power(phi_small(5),2,5),'ramified n=5 factorization failure')
    require(evaluate(phi_small(3),30)==7**2*19,'small square-hit control failure')
    require((2*30+1)%7!=0 and pow(30,3,49)==1,'simple-root regression failure')
    # This also has v5(30)=1 and 5 not dividing 3, so the irreducibility theorem
    # applies to Phi_3(30*T^2) despite a square divisor at T=1.
    reciprocity=[]
    for m in MULTIPLIERS:
        n=m*R1;fs=index_factors(R1,m)
        syms={str(p):(-1 if pow(p,(Q0-1)//2,Q0)==Q0-1 else 1) for p in fs}
        require(all(v==-1 for v in syms.values()),'edge reciprocity mismatch')
        D=n if n%4==1 else -n
        require(pow(D,(Q0-1)//2,Q0)==1,'quadratic subfield is not split')
        reciprocity.append({'m':m,'n':n,'D':D,'edge_symbols':syms,'D_symbol':1})
    finite_tests=self_tests(document,primes) if do_self_test else {}
    return {'schema':'A303656-phase-G-reference-v1','prime_certificates_verified':len(primes),
            'indices':indices,'source_regular_rows':source_rows,
            'source_first_relay_products':{'Phi31':phi31,'factors31':factors31,'Phi93':phi93,'factors93':factors93},
            'published_bound':{'B':B,'inherited_exhaustiveness_only':True,'full_search_replayed':False,
                               'known_odd_solutions_verified':inventory,'n878851_min_k_after_bound_and_old_congruences':k,
                               'corresponding_q_not_asserted_prime':1+2*k*R1},
            'variable_base_models':models,'regular_small_index_models':toy,
            'polynomial_composition_regressions':polynomial_checks,
            'aggregate_r_adic_regressions':aggregate,'reciprocity_regressions':reciprocity,
            'small_square_hit':{'p':3,'q':7,'base':30,'Phi':931,'factors':{'7':2,'19':1},'derivative_mod_q':5},
            'ramified_positive_control':{'n':5,'Phi5_5T2_factors':[minus,plus]},
            'auxiliary_Fermat_quotients':{str(q):{str(a):qquot(a,q) for a in bases} for q,bases in [(Q0,[3,5,31,R1]),(20771,[3,5,31,67])]},
            'mutation_tests':finite_tests,
            'nonclaims':{'unbounded_theorems_formalized':False,'n878851_closed':False,'any_target_index_closed':False,
                         'base5_B31_member_found':False,'new_stricter_terminal_prime_class':False,
                         'general_prime_scan':False,'old_k_scan_replayed':False,'large_target_integer_constructed':False,
                         'independent_author_or_software_stack':False,'GitHub_writes':'NONE'}}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=ROOT/'certificates.json')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    document=json.loads(args.certificates.read_text(encoding='utf-8'))
    out=run(document,args.self_test)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f'PASS: {out["prime_certificates_verified"]} recursive Lucas certificates; four exact-target variable-base models; no target scan.')
    print(f'Evidence SHA256: {hashlib.sha256(args.output.read_bytes()).hexdigest()}')
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (CheckFailure,ValueError,KeyError,OSError) as exc:
        raise SystemExit(f'FAIL: {exc}') from exc
