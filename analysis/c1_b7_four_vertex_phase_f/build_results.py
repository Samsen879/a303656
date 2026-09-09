"""Discovery/enumeration builder. All primality conclusions are rechecked by verify.py."""
import csv, hashlib, itertools, json, math, sys, time
from pathlib import Path
from fractions import Fraction
from sympy import factorint, isprime
ROOT=Path(__file__).resolve().parent
A=(43,127,379,7603,19531,519499); K=(1,2,3,6,7,14,21,42)
P89=14693679385278593849609206715278070972733319459651094018859396328480215743184089660644531
P89fac={2:1,3:3,5:1,7:2,19:1,29:1,31:1,43:1,127:1,379:1,449:1,829:1,883:1,5167:1,7603:1,19531:1,280729:1,406729:1,519499:1,2161279:1,24132781:1,1692416503:1,23792163643711:1}
certs={}
def prove(n):
    if str(n) in certs:return
    if n<10000:
        if n<2 or any(n%d==0 for d in range(2,math.isqrt(n)+1)):raise ValueError(('composite',n))
        certs[str(n)]={'kind':'trial'};return
    ff=P89fac if n==P89 else {int(p):int(e) for p,e in factorint(n-1,limit=20000).items()}
    used=[];F=1
    for p,e in sorted(ff.items(),reverse=True):
        if not isprime(p):continue # Discovery filter only; recursive certificate is mandatory.
        prove(p);used.append((p,e));F*=p**e
        if F*F>n:break
    if F*F<=n:raise ValueError(('insufficient Pocklington factorization',n,ff))
    witnesses=[]
    for p,e in used:
        for a in range(2,1000):
            if pow(a,n-1,n)==1 and math.gcd(pow(a,(n-1)//p,n)-1,n)==1:break
        else:raise ValueError(('no witness',n,p))
        witnesses.append([str(p),e,a])
    certs[str(n)]={'kind':'pocklington','factors_witnesses':witnesses}

def read_probe(name):
    out=[]
    for row in csv.reader((ROOT/name).open()):
        shape,r,s,p,n=row;r,s,p,n=map(int,(r,s,p,n))
        prove(p)
        fac=list(factorint(n))
        assert p%4==3 and pow(5,n,p)==1 and all(pow(5,n//l,p)!=1 for l in fac)
        z=pow(5,n,p*p);assert (z-1)%p==0
        out.append(dict(shape=shape,r=r,s=s,p=p,n=n,lifting_coefficient=(z-1)//p,square_hit=(z==1)))
    return out

relays=read_probe('relay_probe_1e10.csv')
# Exact integers transcribed from the fixed-SHA Phase D files; proved anew here.
extra=[(43,172827552198815888791,43),(43,43955934961951833386625799,129),
       (43,236419892853700126919767791480523,258),(127,P89,127),(43,26041733579107,602)]
for r,p,n in extra:
    prove(p);assert pow(5,n,p)==1 and all(pow(5,n//int(l),p)!=1 for l in factorint(n))
    z=pow(5,n,p*p);assert z!=1 and (z-1)%p==0
    relays.append(dict(shape='relay',r=r,s=0,p=p,n=n,lifting_coefficient=(z-1)//p,square_hit=False,source='fixed-SHA Phase D; fresh Pocklington proof'))
relays.sort(key=lambda x:(x['r'],x['p']))
fork_hits=read_probe('fork_probe_1e12.csv');serial_hits=read_probe('serial_probe_1e12.csv')
assert not any(x['square_hit'] for x in relays+fork_hits+serial_hits)
for p in (7,)+A:prove(p)
base_orders={7:6,43:42,127:42,379:21,7603:42,19531:7,519499:21}
for p,n in base_orders.items():
    assert pow(5,n,p)==1 and pow(5,n,p*p)!=1
    assert all(pow(5,n//int(l),p)!=1 for l in factorint(n))

# Rational logarithm intervals: atanh series and a rigorous geometric tail bound.
def ln_bounds(x,N=180):
    z=(x-1)/(x+1);zz=z*z;t=z;v=Fraction(0)
    for j in range(N):v+=t/(2*j+1);t*=zz
    v*=2;return v,v+2*t/((2*N+1)*(1-zz))
l2=ln_bounds(Fraction(2));l54=ln_bounds(Fraction(5,4))
l5=(2*l2[0]+l54[0],2*l2[1]+l54[1]);l10=(3*l2[0]+l54[0],3*l2[1]+l54[1])
log5=(l5[0]/l10[1],l5[1]/l10[0]);err=Fraction(8,5**42)
def log_int_bounds(n):
    k=n.bit_length()-1;v=ln_bounds(Fraction(n,1<<k))
    return ((k*l2[0]+v[0])/l10[1],(k*l2[1]+v[1])/l10[0])
def aggregate_digits(shape,r,s):
    if shape=='fork':D=42*(r-1)*(s-1);a,b=D*log5[0]-err,D*log5[1]+err
    else:
        D=42*r*(s-1);ls=log_int_bounds(s)
        a,b=D*log5[0]-ls[1]-err,D*log5[1]-ls[0]+err
    aa=a.numerator//a.denominator;bb=b.numerator//b.denominator
    assert aa==bb,(shape,r,s)
    return aa+1
states=[];indices=[]
for r,s in itertools.combinations(A,2):
    ds=aggregate_digits('fork',r,s)
    states.append(dict(shape='fork',r=r,s=s,terminal_index_count=8,aggregate_digits=ds,M=42*r*s,
                       expression=f'((5^{42*r*s}-1)*(5^42-1))/((5^{42*r}-1)*(5^{42*s}-1))',
                       closure_status='OPEN',imprimitive_factor=1))
    for k in K:indices.append(dict(shape='fork',r=r,s=s,n=k*r*s,k=k,optional_r=1,imprimitive_prime='',admitted_q_mod20='3,7' if k%2==0 else '11,19',status='OPEN'))
for t in relays:
    r,s,w=t['r'],t['p'],t['n'];ds=aggregate_digits('serial',r,s)
    states.append(dict(shape='serial',r=r,s=s,order_s=w,terminal_index_count=16,aggregate_digits=ds,M=42*r*s,
                       expression=f'(5^{42*r*s}-1)/({s}*(5^{42*r}-1))',closure_status='OPEN',imprimitive_factor=s))
    for e in (0,1):
        for k in K:
            n=k*s*r**e
            indices.append(dict(shape='serial',r=r,s=s,n=n,k=k,optional_r=e,imprimitive_prime=s if n==s*w else '',admitted_q_mod20='3,7' if n%2==0 else '11,19',status='OPEN'))
assert len({x['n'] for x in indices})==len(indices)==568
assert not ({x['n'] for x in indices}&{r*k for r in A for k in K})
# Numerically ranked three smallest serial states are globally smallest: any omitted
# s <=10^10 would have been in the exact bounded enumeration, and s>10^10 is larger.
small_serial=sorted([x for x in states if x['shape']=='serial'],key=lambda x:x['aggregate_digits'])[:3]
assert [(x['r'],x['s']) for x in small_serial]==[(127,2287),(43,9547),(43,42743)]
# A short second enumeration independently certifies those three minima, no large scan.
W=max(x['r']*(x['s']-1) for x in small_serial)
independent=[]
for r in A:
    for s in range(2*r+1,W//r+2,4*r):
        if s>10000 and any(s%d==0 for d in range(2,math.isqrt(s)+1)):continue
        if s<=10000 and (s<2 or any(s%d==0 for d in range(2,math.isqrt(s)+1))):continue
        e=math.gcd(42*r,s-1)
        if pow(5,e,s)!=1:continue
        n=e
        for l in (2,3,7,r):
            while n%l==0 and pow(5,n//l,s)==1:n//=l
        if n%r==0 and pow(5,n,s*s)!=1:independent.append((r,s))
assert set(independent)=={(x['r'],x['s']) for x in small_serial}
# Check aggregate divisibility and non-square valuations without expanding huge integers.
for t in fork_hits+serial_hits:
    r,s,p,n=t['r'],t['s'],t['p'],t['n'];mod=p*p
    if t['shape']=='fork':
        num=(pow(5,42*r*s,mod)-1)*(pow(5,42,mod)-1)%mod
        den=(pow(5,42*r,mod)-1)*(pow(5,42*s,mod)-1)%mod
    else:num=(pow(5,42*r*s,mod)-1)%mod;den=s*(pow(5,42*r,mod)-1)%mod
    assert math.gcd(den,p)==1
    residue=num*pow(den,-1,mod)%mod
    assert residue%p==0 and residue!=0
    t['aggregate_mod_p2']=residue

# Materialize the three smallest fork aggregates, store canonical big-endian hashes.
material=[]
for t in sorted([x for x in states if x['shape']=='fork'],key=lambda x:x['aggregate_digits'])[:3]:
    r,s=t['r'],t['s'];start=time.monotonic()
    num=(5**(42*r*s)-1)*(5**42-1);den=(5**(42*r)-1)*(5**(42*s)-1)
    F,rem=divmod(num,den);assert rem==0
    blob=F.to_bytes((F.bit_length()+7)//8,'big')
    material.append(dict(r=r,s=s,bit_length=F.bit_length(),bytes=len(blob),sha256_big_endian=hashlib.sha256(blob).hexdigest(),digits=t['aggregate_digits'],seconds=round(time.monotonic()-start,6)))

# Fresh exact interpretation of selected Pollard p-1 gcds (a gcd can be composite).
p1factors={2287:[],4574:[119527769,128712361],5461:[6717031],6861:[69316463449],10922:[3211069],16383:[]}
p1results=[]
def phi_value(n):
    fs=list(map(int,factorint(n)));a=b=1
    for mask in range(1<<len(fs)):
        d=n;sgn=0
        for j,p in enumerate(fs):
            if mask>>j&1:d//=p;sgn+=1
        if sgn%2:b*=5**d-1
        else:a*=5**d-1
    q,t=divmod(a,b);assert t==0;return q
for n,pp in p1factors.items():
    N=phi_value(n);C=N;entries=[]
    for p in pp:
        prove(p);e=0
        while C%p==0:C//=p;e+=1
        assert e==1 and pow(5,n,p*p)!=1
        assert pow(5,n,p)==1 and all(pow(5,n//int(l),p)!=1 for l in factorint(n))
        entries.append(dict(p=p,valuation=e,p_mod_4=p%4,exact_order=n))
    bb=C.to_bytes((C.bit_length()+7)//8,'big')
    p1results.append(dict(n=n,B1=10000,bases=[2,3],certified_factors=entries,
                          residual_bits=C.bit_length(),residual_sha256_big_endian=hashlib.sha256(bb).hexdigest(),
                          residual_expression=f'Phi_{n}(5)/'+str(math.prod(pp)),
                          complete_factorization=False,square_part_certified=False))
(ROOT/'pminus1_results.json').write_text(json.dumps(p1results,indent=2)+'\n')

for name,rows in [('relays',relays),('states',states),('indices',indices),('fork_factors',fork_hits),('serial_factors',serial_hits)]:
    (ROOT/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (ROOT/(name+'.csv')).open('w',newline='') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
(ROOT/'prime_certificates.json').write_text(json.dumps(certs,indent=2)+'\n')
(ROOT/'materialized_aggregates.json').write_text(json.dumps(material,indent=2)+'\n')
summary=dict(fork_states=15,fork_raw_indices=120,fork_distinct_indices=120,
    certified_serial_states=28,certified_serial_indices=448,certified_total_indices=568,
    serial_states_by_r={str(r):sum(t['r']==r for t in relays) for r in A},
    complete_serial_census=False,relay_discovery_bound=10**10,fork_terminal_probe_bound=10**12,
    serial_terminal_probe_bound=10**12,admitted_fork_prime_factors=len(fork_hits),
    admitted_serial_prime_factors=len(serial_hits),square_hits=0,closed_four_vertex_states=0,
    success_level='D (independent reconstruction; Phase E source absent)',smallest_serial_states=small_serial)
(ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2));print('Materialized',material);print('Prime certificate nodes',len(certs))
