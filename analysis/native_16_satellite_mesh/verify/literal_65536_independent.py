"""All 131072 actual rotations: independent literal Gaussian division, stdlib only."""
import json,hashlib,sys
from pathlib import Path
from math import gcd,prod
from time import perf_counter,process_time
from datetime import datetime,timezone
wall=perf_counter();cpu=process_time()
source=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'sparse_construction/released_phase_65536.json'
raw=source.read_bytes();d=json.loads(raw);L,K,r=d['L'],d['K'],d['r'];assert (L,K,r)==(128,11520,16)
A,B=9**L,25**L;H,D,E=3*A+25*B,12*B-3*A,A+10*B;h=D-5
Y=1<<(K//4);lo,hi=13*Y//16,7*Y//8;y=d['y'];M=d['M']
assert y==d['yfirst'] and lo<=y<hi and y-M<lo and y%390==0
norms=[p for pack in d['packs'] for m,b,root,p in pack]
assert len(norms)==34 and M==390*prod(norms) and M.bit_length()==2817
assert all(gcd(p,q)==1 for j,p in enumerate(norms) for q in norms[j+1:])
assert all(gcd(p,10*D*E)==1 for p in norms)
for pack in d['packs']:
    assert len(pack)==17
    for m,b,res,p in pack:assert m*m+b*b==p and gcd(m,b)==1 and y%p==res

def mul(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def norm(z):return z[0]*z[0]+z[1]*z[1]
t,rem=divmod(5*y*y-h*y+5+3*h-E,10);assert rem==0
P=(h-3*t,t);Q=((P[0]+1,P[1]+3),(P[0]+3-y,P[1]-1-3*y))
S=norm(P);n=S+H
assert 1<<K<=S<1<<(K+1) and (25*B)**16<=n<=A**32
Qnorms=(n-(9*A+B),n-(A+5*B));assert tuple(map(norm,Q))==Qnorms
qs=set();stream=hashlib.sha256();checked=0
print('START',datetime.now(timezone.utc).isoformat(),'input_sha',hashlib.sha256(raw).hexdigest(),flush=True)
for edge,pack in enumerate(d['packs']):
    # Ordinary subset doubling on Gaussian integers, independent of Gray code.
    subset=[(pack[0][0],-pack[0][1])]
    for m,b,_,_ in pack[1:]:subset += [mul(Z,(m,-b)) for Z in subset]
    assert len(subset)==65536
    for mask,Z in enumerate(subset):
        assert gcd(*Z)==1
        bar=(Z[0],-Z[1]);den=norm(Z);num=mul(Q[edge],bar)
        quotient=[]
        for c in num:
            a,rem=divmod(c,den);assert rem==0;quotient.append(a)
        R=mul(quotient,bar);assert norm(R)==Qnorms[edge]
        x,z=R[0]-P[0],R[1]-P[1]
        assert x%2==z%2==1 and gcd(x,z)==1
        q=(x*x+z*z)//2;det=x*P[1]-z*P[0];gap=(D,E)[edge]
        assert q%2==1 and det%2==0 and 2*q*S==(gap-q)**2+det*det
        assert 64*K*K*q<S<64*K*(K+1)*q
        assert q not in qs;qs.add(q)
        stream.update(q.to_bytes((q.bit_length()+7)//8,'big'))
        checked+=1
        if checked%16384==0:print('PROGRESS',checked,'/131072','wall_s',round(perf_counter()-wall,3),'cpu_s',round(process_time()-cpu,3),flush=True)
assert checked==len(qs)==131072
report={'status':'PASS','input_sha256':hashlib.sha256(raw).hexdigest(),'L':L,'K':K,'r':r,
        'seeds_checked':checked,'distinct_q':len(qs),'ordinary_height':True,
        'all_seeds_integral_gaussian_division_primitive_parity_norm_critical':True,
        'q_stream_sha256':stream.hexdigest(),'cpu_seconds':process_time()-cpu,
        'wall_seconds':perf_counter()-wall,'completed_utc':datetime.now(timezone.utc).isoformat()}
Path(__file__).with_name('literal_65536_independent_result.json').write_text(json.dumps(report,indent=2)+'\n')
print('RESULT',json.dumps(report),flush=True)
