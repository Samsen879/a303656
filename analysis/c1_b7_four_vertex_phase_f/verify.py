#!/usr/bin/env python3
"""Fail-closed, standard-library verifier; no probable-prime oracle is used.
Optional exact probe replay requires g++; p-1 replay additionally requires GMP.
"""
import argparse, csv, hashlib, itertools, json, math, subprocess, tempfile, time
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
A=(43,127,379,7603,19531,519499);K=(1,2,3,6,7,14,21,42)
def require(b,message):
    if not b:raise ValueError(message)
def load(n):return json.loads((ROOT/n).read_text())
def prime_factors(n):
    out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p=3 if p==2 else p+2
    if n>1:out.append(n)
    return out

def phi5(n):
    fs=prime_factors(n);up=down=1
    for bits in itertools.product((0,1),repeat=len(fs)):
        d=n
        for p,b in zip(fs,bits):
            if b:d//=p
        if sum(bits)%2:down*=pow(5,d)-1
        else:up*=pow(5,d)-1
    q,r=divmod(up,down);require(r==0,'nonintegral cyclotomic expression');return q

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--replay-probes',action='store_true');ap.add_argument('--replay-pminus1',action='store_true');args=ap.parse_args()
    begin=time.monotonic();checks=[]
    cs=load('prime_certificates.json');done=set();active=set()
    def prime(n):
        if n in done:return
        require(n not in active,'certificate cycle');active.add(n)
        c=cs[str(n)]
        if c['kind']=='trial':
            require(2<=n<10000,'trial certificate bound')
            require(all(n%d for d in range(2,math.isqrt(n)+1)),f'composite trial {n}')
        elif c['kind']=='pocklington':
            F=1;seen=set()
            for ps,e,a in c['factors_witnesses']:
                p=int(ps);require(1<p<n and p not in seen and isinstance(e,int) and e>0,'bad Pocklington factor');seen.add(p)
                prime(p);F*=p**e
                require((n-1)%p==0 and pow(a,n-1,n)==1,'Pocklington Fermat condition')
                require(math.gcd(pow(a,(n-1)//p,n)-1,n)==1,'Pocklington gcd condition')
            require(F*F>n and (n-1)%F==0,'Pocklington size/divisibility gate')
        else:raise ValueError('unknown certificate kind')
        active.remove(n);done.add(n)
    for n in cs:prime(int(n))
    checks.append(f'{len(done)} recursive primality certificates PASS')
    orders={3:2,7:6,43:42,127:42,379:21,7603:42,19531:7,519499:21}
    def order(p,n,fs=None):
        fs=prime_factors(n) if fs is None else fs
        require(pow(5,n,p)==1 and all(pow(5,n//l,p)!=1 for l in fs),'exact-order failure')
    for p in (7,)+A:
        prime(p);order(p,orders[p]);require(pow(5,orders[p],p*p)!=1,'nonregular base relay')
    initial={7:[19531],14:[29,449],21:[379,519499],42:[7,43,127,7603]}
    for n,ff in initial.items():
        require(phi5(n)==math.prod(ff),'first-relay factorization mismatch')
        for p in ff:require(all(p%d for d in range(2,math.isqrt(p)+1)),f'initial prime {p}')
    Z7=(5**42-1)//(2*42**2)
    require(Z7==math.prod([29,31,449,*A]),'base critical integer mismatch')
    checks.append('six first relays and squarefree base Z7 PASS')
    rr=load('relays.json');require(len(rr)==28,'relay count')
    local=[x for x in rr if x['p']<=10**10];require(len(local)==23,'bounded relay count')
    s_to_r={}
    for x in rr:
        p,n,r=x['p'],x['n'],x['r'];prime(p);require(p%4==3 and r in A and p not in A and p>r,'relay admission')
        require(n in [k*r for k in K],'relay order family');order(p,n)
        z=pow(5,n,p*p);require(z!=1 and (z-1)//p==x['lifting_coefficient'],'relay regularity')
        require(p not in s_to_r,'duplicate relay in two families');s_to_r[p]=r
    checks.append('28 actual regular serial relays PASS')
    states=load('states.json');inds=load('indices.json')
    expected=set()
    for r,s in itertools.combinations(A,2):
        for k in K:expected.add(('fork',r,s,k*r*s))
    for x in rr:
        r,s=x['r'],x['p']
        for k in K:
            for e in (0,1):expected.add(('serial',r,s,k*s*r**e))
    require({(x['shape'],x['r'],x['s'],x['n']) for x in inds}==expected,'index reconstruction')
    require(len(inds)==len({x['n'] for x in inds})==568,'raw/distinct index count')
    require(not({x['n'] for x in inds}&{r*k for r in A for k in K}),'three-vertex overlap')
    require(len(states)==len({(x['r'],x['s']) for x in states})==43,'state reconstruction')
    rw={x['p']:x['n'] for x in rr}
    for x in inds:
        n,r,s=x['n'],x['r'],x['s'];ws=orders[s] if x['shape']=='fork' else rw[s]
        actual=[p for p,w in ((3,2),(7,6),(r,orders[r]),(s,ws)) if n%p==0 and n//p==w]
        want=[] if x['imprimitive_prime']=='' else [x['imprimitive_prime']]
        require(actual==want,'imprimitive correction mismatch')
        require(x['admitted_q_mod20']==('3,7' if n%2==0 else '11,19'),'parity metadata')
    checks.append('120 fork + 448 certified serial indices; disjointness and order loss PASS')
    # Independently evaluate rational logarithm bounds using a different truncation.
    def L(x):
        z=(x-1)/(x+1);v=Fraction(0);t=z
        for j in range(160):v+=2*t/(2*j+1);t*=z*z
        return v,v+2*t/(321*(1-z*z))
    l2=L(Fraction(2));l54=L(Fraction(5,4));lo5=2*l2[0]+l54[0];hi5=2*l2[1]+l54[1]
    lo10=3*l2[0]+l54[0];hi10=3*l2[1]+l54[1];err=Fraction(8,5**42)
    for x in states:
        r,s=x['r'],x['s']
        if x['shape']=='fork':
            D=42*(r-1)*(s-1);lo=D*lo5/hi10-err;hi=D*hi5/lo10+err
            require(x['imprimitive_factor']==1,'fork normalization')
        else:
            k=s.bit_length()-1;v=L(Fraction(s,1<<k));lslo=(k*l2[0]+v[0])/hi10;lshi=(k*l2[1]+v[1])/lo10
            D=42*r*(s-1);lo=D*lo5/hi10-lshi-err;hi=D*hi5/lo10-lslo+err
            require(x['imprimitive_factor']==s,'serial normalization')
        require(lo.numerator//lo.denominator==hi.numerator//hi.denominator==x['aggregate_digits']-1,'aggregate decimal digit bound')
    for x in load('materialized_aggregates.json'):
        r,s=x['r'],x['s'];num=(5**(42*r*s)-1)*(5**42-1);den=(5**(42*r)-1)*(5**(42*s)-1)
        F,rem=divmod(num,den);require(rem==0,'fork quotient')
        b=F.to_bytes((F.bit_length()+7)//8,'big')
        require(hashlib.sha256(b).hexdigest()==x['sha256_big_endian'],'materialization hash')
        low=10**(x['digits']-1);require(low<=F<10*low,'integer digit-bound check')
    checks.append('43 certified aggregate sizes; three materialized fork hashes PASS')
    # Short independent small-integer search proves the global three-state priority.
    W=43*(42743-1);small=[]
    for s in range(3,W//43+2,4):
        if any(s%d==0 for d in range(2,math.isqrt(s)+1)):continue
        for r in A:
            if s<=r or r*(s-1)>W or (s-1)%r:continue
            w=math.gcd(42*r,s-1)
            if pow(5,w,s)!=1:continue
            for l in (2,3,7,r):
                while w%l==0 and pow(5,w//l,s)==1:w//=l
            if w%r==0 and pow(5,w,s*s)!=1:small.append((r,s))
    require(set(small)=={(127,2287),(43,9547),(43,42743)},'independent priority search')
    checks.append('independent short relay search for three globally smallest serial states PASS')
    ff=load('fork_factors.json');ss=load('serial_factors.json')
    require(len(ff)==28 and len(ss)==62,'terminal factor counts')
    require(len({x['p'] for x in ff+ss})==90,'terminal prime factor uniqueness')
    for x in ff+ss:
        p,n,r,s=x['p'],x['n'],x['r'],x['s'];prime(p);order(p,n)
        require((x['shape'],r,s,n) in expected and p%4==3,'terminal factor family/admission')
        require(pow(5,n,p*p)!=1 and not x['square_hit'],'unexpected square hit')
        m=p*p
        if x['shape']=='fork':num=(pow(5,42*r*s,m)-1)*(pow(5,42,m)-1)%m;den=(pow(5,42*r,m)-1)*(pow(5,42*s,m)-1)%m
        else:num=(pow(5,42*r*s,m)-1)%m;den=s*(pow(5,42*r,m)-1)%m
        require(math.gcd(den,p)==1,'aggregate denominator is nonunit')
        z=num*pow(den,-1,m)%m
        require(z==x['aggregate_mod_p2'] and z%p==0 and z!=0,'aggregate valuation')
    checks.append('90 admitted terminal prime factors, exact order and valuation one PASS')
    for x in load('pminus1_results.json'):
        n=x['n'];C=phi5(n)
        for f in x['certified_factors']:
            p=f['p'];prime(p);order(p,n);require(C%p==0 and C%(p*p)!=0,'p-1 factor multiplicity');C//=p
        b=C.to_bytes((C.bit_length()+7)//8,'big')
        require(C.bit_length()==x['residual_bits'] and hashlib.sha256(b).hexdigest()==x['residual_sha256_big_endian'],'p-1 cofactor hash')
        require(not x['complete_factorization'] and not x['square_part_certified'],'false closure metadata')
    checks.append('selected p-1 factors and unresolved exact cofactors PASS')
    if args.replay_probes or args.replay_pminus1:
        with tempfile.TemporaryDirectory() as td:
            if args.replay_probes:
                exe=Path(td)/'probe';subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'probe.cpp'),'-o',str(exe)],check=True)
                for mode,bound,fn in [('relay',10**10,'relay_probe_1e10.csv'),('fork',10**12,'fork_probe_1e12.csv'),('serial',10**12,'serial_probe_1e12.csv')]:
                    inp=(ROOT/'relay_probe_1e10.csv').read_text() if mode=='serial' else ''
                    p=subprocess.run([str(exe),mode,str(bound)],input=inp,capture_output=True,text=True,check=True,timeout=90)
                    require(p.stdout==(ROOT/fn).read_text(),'probe replay mismatch: '+mode)
                checks.append('all three full bounded C++ probe replays PASS (same implementation)')
            if args.replay_pminus1:
                exe=Path(td)/'p1';subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'pminus1_lab.cpp'),'-lgmpxx','-lgmp','-o',str(exe)],check=True)
                p=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=90)
                require(p.stdout==(ROOT/'pminus1_lab.log').read_text(),'p-1 replay mismatch')
                checks.append('GMP p-1 full replay PASS (same implementation)')
    manifest=ROOT/'SHA256SUMS.txt'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            h,fn=line.split('  ',1);require(hashlib.sha256((ROOT/fn).read_bytes()).hexdigest()==h,'manifest mismatch '+fn)
        checks.append('SHA256 manifest PASS')
    result={'status':'PASS','checks':checks,'seconds':round(time.monotonic()-begin,6),
        'limits':['Phase E original ZIP was not available','not a complete enumeration of S_r','no whole state closed','same-implementation replay is not independent coverage validation','standalone verification is not repository-native testing']}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
