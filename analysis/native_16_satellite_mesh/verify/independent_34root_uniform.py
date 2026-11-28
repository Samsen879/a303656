"""Independent exact audit of the r=16 released-phase theorem.

Reads JSON data only. Uses full Lucas primality certificates, elementary
finite-field counting, rational Taylor bounds, and complete small-prime trial.
It does not import or read any producer verifier.
"""
import hashlib,json,sys
from fractions import Fraction as F
from math import gcd,isqrt,prod
from pathlib import Path
from time import perf_counter,process_time

wall=perf_counter();cpu=process_time()
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'sparse_construction'
source=base/'released_phase_65536.json';raw=source.read_bytes();d=json.loads(raw)
proof=json.loads((base/'r16_lucas_primes.json').read_text())
roots=json.loads((base/'released_phase_65536_two_roots.json').read_text())
L,K,r=(d[k] for k in ('L','K','r'));assert (L,K,r)==(128,11520,16)
A,B=9**L,25**L;H,D,E=3*A+25*B,12*B-3*A,A+10*B;h=D-5
Y=1<<(K//4);lo=13*Y//16;hi=7*Y//8;R=1<<r

# Complete Lucas criterion with recursively proven prime divisors of n-1.
proven={2}
for text in sorted(proof,key=int):
    p=int(text);record=proof[text]
    if p==2:continue
    factors=record['factors'];a=record['a']
    assert factors and len({q for q,e in factors})==len(factors)
    assert all(q in proven and q<p and e>=1 for q,e in factors)
    assert prod(q**e for q,e in factors)==p-1
    assert pow(a,p-1,p)==1
    assert all(gcd(pow(a,(p-1)//q,p)-1,p)==1 for q,e in factors)
    proven.add(p)

flat=[(edge,m,b,root,p) for edge,pack in enumerate(d['packs']) for m,b,root,p in pack]
assert len(flat)==len(roots)==34
ps=[]
for (edge,m,b,stored,p),(e0,m0,b0,p0,u,v) in zip(flat,roots):
    assert (edge,m,b,p)==(e0,m0,b0,p0) and p in proven
    assert m*m+b*b==p and gcd(m,b)==1 and gcd(p,390*D*E)==1
    assert 0<=u<p and 0<=v<p and u!=v and stored==u
    I=m*pow(b,-1,p)%p;assert I*I%p==p-1
    if edge==0:
        f=lambda y:(5*y*y-h*y+5-E-(h+10)*I)%p
    else:
        f=lambda y:(5*y*y+(-h+10*I)*y-5-E-h*I)%p
    assert f(u)==f(v)==0 and p!=5
    ps.append(p)
assert len(set(ps))==34
M=390*prod(ps);assert M==d['M'] and M.bit_length()==2817
N0=(hi-lo)//M;assert N0==722769304356234345
# Thus the complete distinct family has 2^34 root classes, each with N0 or N0+1 points.

# Complete trial division to 2^24; tail distinct-prime counts are <=24 each.
trial_bound=1<<24
sieve=bytearray(b'\x01')*(trial_bound+1);sieve[:2]=b'\x00\x00'
for p in range(2,isqrt(trial_bound)+1):
    if sieve[p]:sieve[p*p:trial_bound+1:p]=b'\x00'*((trial_bound-p*p)//p+1)
rem=[D,E];small=[[],[]];prime_count=0
for p in range(2,trial_bound+1):
    if not sieve[p]:continue
    prime_count+=1
    for edge in (0,1):
        if rem[edge]%p:continue
        e=0
        while rem[edge]%p==0:rem[edge]//=p;e+=1
        small[edge].append((p,e))
assert small==[[(3,1),(573737,1)],[(13,1)]]
assert prime_count==1077871 and all(n<(1<<600) for n in rem)
assert gcd(D,E)==1

# The fixed y=0 mod390 protects both rotations +/-1 at the small primes 3 and13.
for edge,ell in ((0,3),(1,13)):
    pack=d['packs'][edge]
    assert pack[0][1]%ell==0 and pack[0][0]%ell!=0
    assert all(m%ell==0 and b%ell!=0 for m,b,_,_ in pack[1:])
    t0=(5+3*h-E)*pow(10,-1,ell)%ell
    P=((h-3*t0)%ell,t0)
    Q=((P[0]+1)%ell,(P[1]+3)%ell) if edge==0 else ((P[0]+3)%ell,(P[1]-1)%ell)
    assert all(any((sgn*Q[j]-P[j])%ell for j in (0,1)) for sgn in (-1,1))

# Independent discriminant count of the exceptional prime's entire bad-phase union.
ell=573737;assert ell in proven or all(ell%q for q in range(2,isqrt(ell)+1))
pack=d['packs'][0]
def mulmod(z,w):return ((z[0]*w[0]-z[1]*w[1])%ell,(z[0]*w[1]+z[1]*w[0])%ell)
zs=[(pack[0][0]%ell,-pack[0][1]%ell)]
for m,b,_,_ in pack[1:]:zs += [mulmod(z,(m%ell,-b%ell)) for z in zs]
assert len(zs)==R and all(v for u,v in zs)
ratios={-u*pow(v,-1,ell)%ell for u,v in zs};assert len(ratios)==63294
E5=E*pow(5,-1,ell)%ell;hist=[0,0,0]
for z in ratios:
    discriminant=(4*z+4*E5-3)%ell
    symbol=pow(discriminant,(ell-1)//2,ell)
    hist[1 if symbol==0 else 2 if symbol==1 else 0]+=1
assert hist==[31519,0,31775]
bad_known=hist[1]+2*hist[2];assert bad_known==63550
tail_coefficient=R*(2*24+24);assert tail_coefficient==4718592
good_bounds=[n-bad_known*(n//ell+1)-tail_coefficient*(n//trial_bound+1) for n in (N0,N0+1)]
good=min(good_bounds);assert good==439432868807057773
total=good*(1<<34);assert total==7549399201255086676070367232 and total>(1<<92)

# Uniform dyadic geometry: Taylor bounds and binary subset grids, without sampling.
def atan_bounds(x):
    lower=x-x**3/3
    return lower,lower+x**5/5
W=F(*d['dyadic_W']);delta=W/R;eps=F(1,1<<2800)
carriers=[];errors=[]
for pack in d['packs']:
    carriers.append(atan_bounds(F(pack[0][1],pack[0][0])))
    error=F(0)
    for j,(m,b,_,_) in enumerate(pack[1:],1):
        lower,upper=atan_bounds(F(b,m));target=W/(1<<j)
        error+=max(abs(lower-target),abs(upper-target))
    errors.append(error)
    assert error<F(*d['dyadic_total_error_limit'])==delta/100
for (lower,upper),error in zip(carriers,errors):
    assert delta-2*error-(upper-lower)>0
    assert delta+2*error+(upper-lower)<F(101,100)*delta
offset_lower=carriers[1][0]-carriers[0][1]
offset_upper=carriers[1][1]-carriers[0][0]
integer_offset=offset_lower//delta;assert integer_offset==30245
cross_clearance=min(offset_lower-integer_offset*delta,(integer_offset+1)*delta-offset_upper)-sum(errors)
assert cross_clearance>delta/16
overlap=min(c[0]+W-delta-e for c,e in zip(carriers,errors))-max(c[1]+e for c,e in zip(carriers,errors))
assert overlap>W/3
theta_lower=min(c[0]-e for c,e in zip(carriers,errors))
theta_upper=max(c[1]+W-delta+e for c,e in zip(carriers,errors))
assert F(1,16*K)<theta_lower<theta_upper<F(1,100)
assert 2*(theta_lower-theta_lower**3/6)**2>F(1,64*K*(K+1))+eps
assert 2*theta_upper**2<F(1,64*K*K)-eps
# f(theta)=2sin^2(theta) has f'>2theta>1/(8K) here.
assert delta/(128*K)>2*eps
assert F(max(D,E),1<<K)+F(4*Y,1<<(K//2))<eps

# Entire y-window: S has exactly K+1 bits and every n has ordinary height.
assert 20*h<lo and 20*abs(5+3*h-E)<lo*lo
assert 10000*h<49*lo*lo
assert F(49,100)**2*(1+F(299,100)**2)*F(13,16)**4>1
assert 10*F(51,100)**2*F(7,8)**4<2
assert (25*B)**16<1<<K and (1<<(K+1))+H<A**32

report={'status':'PASS','input_sha256':hashlib.sha256(raw).hexdigest(),
        'certified_prime_norms':34,'complete_distinct_root_classes':1<<34,
        'minimum_candidates_each_branch':N0,'known_bad_phases':bad_known,
        'complete_small_prime_trial_bound':trial_bound,'trial_primes':prime_count,
        'tail_distinct_prime_bounds':[24,24],'tail_union_coefficient':tail_coefficient,
        'good_bounds_for_two_candidate_counts':good_bounds,
        'good_targets_lower_all_branches':total,
        'each_target_primitive_outputs':2*R,'ordinary_height':True,
        'common_angle_span_gt_W_over_3':True,'each_mesh_maxgap_lt_1_01_delta':True,
        'cross_mesh_angle_separation_gt_delta_over_16':True,
        'all_actual_q_critical_and_distinct_uniformly_in_window':True,
        'wall_seconds':perf_counter()-wall,'cpu_seconds':process_time()-cpu}
Path(__file__).with_name('independent_34root_uniform_result.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: complete 34-prime/two-root inventory, all 2^34 CRT classes')
print('PASS: good per class >=',good,'and total >=',total,'> 2^92')
print('PASS: 65536 angles per edge; overlap >W/3, gap <1.01delta, cross separation >delta/16')
print('PASS: all good targets uniformly ordinary-height, 131072 primitive critical distinct q')
print('cpu_s',round(process_time()-cpu,3),'wall_s',round(perf_counter()-wall,3))
