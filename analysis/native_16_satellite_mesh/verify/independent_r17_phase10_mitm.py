"""Independent all-root phase10 MITM for frozen r=17 factors.

Derives each second root from Vieta rather than reading a root-pair file.
Reads producer JSON data only; never imports its search/verifier core.
"""
import hashlib,json,sys
from bisect import bisect_left
from fractions import Fraction as F
from math import gcd,prod
from pathlib import Path
from time import perf_counter,process_time
wall=perf_counter();cpu=process_time()
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'sparse_construction'
source=base/'released_phase_r17_boundary.json';raw=source.read_bytes();d=json.loads(raw)
L,K,r=(d[k] for k in ('L','K','r'));assert (L,K,r)==(128,11520,17)
A,B=9**L,25**L;D,E=12*B-3*A,A+10*B;h=D-5
Y=1<<(K//4);lo=13*Y//16;hi=7*Y//8
pairs=[];ps=[];frozen=[]
for edge,pack in enumerate(d['packs']):
    assert len(pack)==18
    for m,b,u,p in pack:
        assert m*m+b*b==p and gcd(m,b)==1 and gcd(p,10*D*E)==1
        I=m*pow(b,-1,p)%p;assert I*I%p==p-1
        linear=-h if edge==0 else -h+10*I
        const=5-E-(h+10)*I if edge==0 else -5-E-h*I
        v=(-linear*pow(5,-1,p)-u)%p
        assert 0<=u<p and 0<=v<p and u!=v
        assert (5*u*u+linear*u+const)%p==(5*v*v+linear*v+const)%p==0
        ps.append(p);pairs.append((u,v));frozen.append((edge,m,b,p,I))
assert len(ps)==len(set(ps))==36
assert all(gcd(p,q)==1 for j,p in enumerate(ps) for q in ps[j+1:])
M=10*prod(ps);assert M*39==d['M'] and M.bit_length()==3016
coef=[(M//p)*pow(M//p,-1,p) for p in ps]
constant=sum(u*c for (u,v),c in zip(pairs,coef))%M
increments=[(v-u)*c%M for (u,v),c in zip(pairs,coef)]
def sums(values):
    result=[0]
    for z in values:result += [(a+z)%M for a in result]
    return result
left=sums(increments[:18]);right_unsorted=sums(increments[18:])
right_index=sorted(range(len(right_unsorted)),key=right_unsorted.__getitem__)
right=[right_unsorted[k] for k in right_index]
assert len(left)==len(right)==1<<18
assert len(set(left))==len(set(right))==1<<18
hits=0;minimum=M;minimum_masks=None;maximum=-1;maximum_masks=None
for k,a in enumerate(left):
    begin=(lo-constant-a)%M;end=begin+(hi-lo)
    if end<=M:hits+=bisect_left(right,end)-bisect_left(right,begin)
    else:hits+=len(right)-bisect_left(right,begin)+bisect_left(right,end-M)
    b=(constant+a)%M;j=bisect_left(right,M-b) if b else len(right)
    j%=len(right);residue=(b+right[j])%M
    if residue<minimum:minimum=residue;minimum_masks=(k,right_index[j])
    j=(bisect_left(right,M-b)-1)%len(right)
    residue=(b+right[j])%M
    if residue>maximum:maximum=residue;maximum_masks=(k,right_index[j])
assert hits==0 and minimum>=hi
assert minimum%10==0
for value,(leftmask,rightmask) in ((minimum,minimum_masks),(maximum,maximum_masks)):
    for j,(p,(u,v)) in enumerate(zip(ps,pairs)):
        mask=leftmask if j<18 else rightmask;bit=j if j<18 else j-18
        assert value%p==(v if mask>>bit&1 else u)
minimum_negative_absolute=M-maximum
minimum_absolute=min(minimum,minimum_negative_absolute)
assert 0<minimum<M and 0<maximum<M
assert minimum_absolute>2*Y
# For every real y with |y|>=2Y, each error h|y| and |C| is <y^2/20.
# Thus t>.49y^2>0 and S>=t^2>.49^2*(2Y)^4>2Y^4=2^(K+1).
C=5+3*h-E
assert 20*h<2*Y and 20*abs(C)<(2*Y)**2
assert 49**2*16>2*100**2
assert minimum_absolute.bit_length()==2977
# Upgrade from a window obstruction to a height/angle mismatch for every legal y.
signed_abs_lower=1<<2976
assert minimum_absolute>=signed_abs_lower
assert 20*h<signed_abs_lower and 20*abs(C)<signed_abs_lower**2
assert 10000*h<49*signed_abs_lower**2
# Hence t>.49y^2, h<t/100, and S>(1+2.99^2)*.49^2*y^4>y^4.
assert F(49,100)**2*(1+F(299,100)**2)>1
actual_K_lower=4*2976;assert actual_K_lower==11904
# Every frozen subset angle is between its positive carrier and .01 radians.
for pack in d['packs']:
    assert all(m>0 and b>0 for m,b,_,_ in pack)
    assert sum((F(b,m) for m,b,_,_ in pack),F(0))<F(1,100)
carrier_ratio_lower=min(F(2*pack[0][1]**2,pack[0][3]) for pack in d['packs'])
# Since S>y^4, the physical error is <max(D,E)/y^4+4/|y|<5/|y|.
assert max(D,E)<signed_abs_lower**3
physical_error_upper=F(5,signed_abs_lower)
assert carrier_ratio_lower-physical_error_upper>F(1,64*11521**2)
assert actual_K_lower>=11521
# Thus every actual q/S exceeds 1/(64*K_actual^2), violating criticality.

# The full prime certificate makes these two roots the complete local inventory.
certificate=base/'r17_lucas_primes.json'
proof=json.loads(certificate.read_text());proven={2}
for text in sorted(proof,key=int):
    n=int(text);rec=proof[text]
    if n==2:continue
    fs=rec['factors'];a=rec['a']
    assert fs and len({q for q,e in fs})==len(fs)
    assert all(q in proven and q<n and e>=1 for q,e in fs)
    assert prod(q**e for q,e in fs)==n-1
    assert pow(a,n-1,n)==1
    assert all(gcd(pow(a,(n-1)//q,n)-1,n)==1 for q,e in fs)
    proven.add(n)
assert all(p in proven for p in ps);primality_complete=True
report={'status':'PASS',
        'input_sha256':hashlib.sha256(raw).hexdigest(),'phase_modulus':10,
        'phase_residue':0,'M_bits':M.bit_length(),'root_assignments_checked':1<<36,
        'MITM_halves':[1<<18,1<<18],'window_hits':hits,
        'minimum_nonnegative_root_representative':minimum,
        'minimum_representative_bits':minimum.bit_length(),
        'minimum_root_masks':list(minimum_masks),'window_upper_bound':hi,
        'maximum_nonnegative_root_representative':maximum,
        'maximum_root_masks':list(maximum_masks),
        'minimum_negative_representative_absolute':minimum_negative_absolute,
        'minimum_negative_representative_absolute_bits':minimum_negative_absolute.bit_length(),
        'minimum_signed_representative_absolute':minimum_absolute,
        'all_signed_root_representatives_absolute_gt_2Y':True,
        'no_generated_target_with_S_less_than_2powKplus1':True,
        'actual_K_lower_for_every_signed_loaded_target':actual_K_lower,
        'carrier_ideal_ratio_lower':[carrier_ratio_lower.numerator,carrier_ratio_lower.denominator],
        'all_frozen_subset_rotations_noncritical_at_every_legal_y':True,
        'complete_prime_two_root_inventory_proven':primality_complete,
        'wall_seconds':perf_counter()-wall,'cpu_seconds':process_time()-cpu}
Path(__file__).with_name('independent_r17_phase10_mitm_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],': every2^36 root assignment misses phase10 window')
print('minimum nonnegative representative bits',minimum.bit_length(),'window upper bits',hi.bit_length())
print('minimum root masks',minimum_masks,'prime inventory complete',primality_complete)
print('minimum negative absolute bits',minimum_negative_absolute.bit_length(),'maximum masks',maximum_masks)
print('PASS: min signed absolute >2Y; no generated target anywhere in S<2^(K+1)')
print('PASS: every loaded target has actualK>=11904; every frozen rotation violates criticality')
print('cpu_s',round(process_time()-cpu,3),'wall_s',round(perf_counter()-wall,3))
