#!/usr/bin/env python3
"""Standalone exact verifier for A303656 R2 certificate C21.

Python >=3.10, standard library only. No network, no prime table, no SymPy.
The code checks a finite proof certificate; it does not scan original n-values.
"""
from pathlib import Path
from math import isqrt, prod
from fractions import Fraction as F
from collections import Counter
import json, sys, hashlib
if hasattr(sys,'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)
D=Path(__file__).resolve().parent
certificate_path=D/'certificate.json'
c=json.loads(certificate_path.read_text())
assert c['format']=='A303656-R2-C21-v1'
assert c['target_budget']==21
cat=c['catalog']; B=cat['cutoff_exclusive']; Mmax=cat['max_order_prime']
assert (B,Mmax)==(512,19)


def prime(n):
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d!=0 for d in range(3,isqrt(n)+1,2))


def prime_factors(n):
    ans=[];d=2
    while d*d<=n:
        if n%d==0:
            ans.append(d)
            while n%d==0:n//=d
        d=3 if d==2 else d+2
    if n>1:ans.append(n)
    return ans


def smooth(n,M):
    return all(p<=M for p in prime_factors(n))


def order_by_direct_iteration(base,p):
    # Independent of the order-by-division implementation used in exploration.
    x=1
    for k in range(1,p):
        x=x*base%p
        if x==1:return k
    raise AssertionError(('no multiplicative order',base,p))


def odd(n):
    while n%2==0:n//=2
    return n


# Complete arithmetic certificate for all H<512 and all order primes <=19.
S=[h for h in range(1,B,2) if smooth(h,Mmax)]
assert S==cat['odd_smooth_orders']
P3=prod(3**(2*h)-1 for h in S)
P5=prod(5**(2*h)-1 for h in S)
assert P3==int(cat['product3']) and P5==int(cat['product5'])
fs={int(p):e for p,e in cat['complete_gcd_prime_factorization'].items()}
assert all(isinstance(e,int) and e>0 and prime(p) for p,e in fs.items())
G=prod(p**e for p,e in fs.items())
assert G==int(cat['gcd'])
assert P3%G==P5%G==0
Q3,Q5=P3//G,P5//G
assert Q3==int(cat['product3_over_gcd']) and Q5==int(cat['product5_over_gcd'])
assert int(cat['bezout_a'])*Q3+int(cat['bezout_b'])*Q5==1
# Divisibility plus Bezout is a complete proof that G is the gcd.

candidates=sorted(p for p in fs if p>3 and p%4==3)
rows={r['p']:r for r in cat['inert_candidate_rows']}
assert sorted(rows)==candidates and len(rows)==46
for p in candidates:
    r=rows[p]
    a=order_by_direct_iteration(3,p);b=order_by_direct_iteration(5,p)
    h3,h5=odd(a),odd(b);H=max(h3,h5)
    pp=max(prime_factors(a)+prime_factors(b))
    assert (a,b,h3,h5,H,pp)==(r['ord3'],r['ord5'],r['h3'],r['h5'],r['H'],r['Pplus'])
    assert H<B and pp<=Mmax

# Three finite convolution refinements. Count by set intersection for all z.
expected={11:F(3,25),71:F(4,175),271:F(1,81)}
for p,bound in expected.items():
    r=rows[p];h3,h5=r['h3'],r['h5']
    stored=c['local_refinements'][str(p)]
    assert stored['weight']==str(bound)
    maximum=0
    for e3 in (0,1):
        for e5 in (0,1):
            A={pow(3,e3+2*j,p) for j in range(h3)}
            V={pow(5,e5+2*j,p) for j in range(h5)}
            assert len(A)==h3 and len(V)==h5
            counts=[sum((z-x)%p in V for x in A) for z in range(p)]
            record=stored['parities'][f'{e3}{e5}']
            assert counts==record['counts']
            assert {str(k):v for k,v in Counter(counts).items()}==record['count_histogram']
            assert max(counts)==record['max'] and sum(counts)==h3*h5
            maximum=max(maximum,max(counts))
    assert F(maximum,h3*h5)==bound
for p,r in rows.items():
    bound=expected[p] if p in expected else F(1,r['H'])
    assert F(r['upper_weight'])==bound


def top(k,eligible):
    # Unknown candidates all have H>=512 and hence weight <=1/512.
    vals=[(F(r['upper_weight']),r['p']) for r in eligible]+[(F(1,B),'unknown H>=512')]*k
    vals.sort(key=lambda pair:pair[0],reverse=True)
    selected=vals[:k]
    return sum((w for w,p in selected),F(0)),[[p,str(w)] for w,p in selected]


computed=[]
base_rows=[r for r in rows.values() if r['p']>7 and r['Pplus']<=7]
base,sel=top(21,base_rows)
computed.append({'M':7,'t':'base','budget':str(F(rows[7]['upper_weight'])+base),'core':[[7,rows[7]['upper_weight']]],'targets':sel})
for M in (11,13,17,19):
    core=[p for p in range(7,M+1) if prime(p) and p%4==3]
    C=sum((F(rows[p]['upper_weight']) for p in core),F(0))
    active=[r for r in rows.values() if r['p']>M and r['Pplus']==M]
    inactive=[r for r in rows.values() if r['p']>M and r['Pplus']<M]
    for t in range(M,22):
        A,aa=top(t,active);I,ii=top(21-t,inactive)
        computed.append({'M':M,'t':t,'budget':str(C+A+I),'core':[[p,rows[p]['upper_weight']] for p in core],'active':aa,'inactive':ii})
assert len(computed)==29 # One base case, 28 critical inequalities.
assert computed==c['inequalities']
assert all(F(v['budget'])<1 for v in computed)
maxima={}
for M in (7,11,13,17,19):
    best=max((v for v in computed if v['M']==M),key=lambda v:F(v['budget']))
    maxima[str(M)]={k:v for k,v in best.items() if k in ('M','t','budget')}
assert maxima==c['maxima']
worst=max(computed,key=lambda v:F(v['budget']))
assert worst['budget']=='875703733/878169600'
summary={'status':'PASS','certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),'smooth_orders':len(S),'certified_gcd_prime_factors':len(fs),'complete_inert_candidates':len(rows),'local_exact_refinements':[11,71,271],'finite_inequalities':len(computed),'target_budget':21,'root_count_corollary':22,'maxima':maxima,'worst_margin':str(1-F(worst['budget']))}
(D/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
