#!/usr/bin/env python3
"""Exact, offline Phase K2 verifier. Python >=3.10; standard library only.

No interval of original targets is scanned. Only fixed residue spaces and the
six explicitly supplied targets in POINT_CERTIFICATES.json are processed.
All certificate prime factors are verified by trial division, not probable-
prime tests. Run: python reference.py --out .
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt, prod
from pathlib import Path
import json

TARGETS=(100235446,10000011172,10000072156,10000079932,
         1000000244380,1000000205302)
MODULI=(8,9,5,7,24,40,56,72,120,168,280,360,840,2520,11,27720)
W=2**18

def a2(n:int,c:int,d:int)->F:
    return (F(1,2),F(1),F(1),F(0),F(1,2),F(1),F(0),F(0))[(n-pow(3,c,8)-pow(5,d,8))%8]

def a3(n:int,d:int)->F:
    r=(n-pow(5,d,9))%9
    return F(1) if r%3 else F(3,4) if r==0 else F(0)

def a7(n:int,c:int,d:int)->F:
    return F(1,8) if (n-pow(3,c,7)-pow(5,d,7))%7==0 else F(1)

@lru_cache(None)
def rho237(n:int)->F:
    n%=504
    # Integer numerator over 36*2*4*8=2304.
    w2=(1,2,2,0,1,2,0,0)
    total=0
    for c in range(6):
        for d in range(6):
            x=w2[(n-pow(3,c,8)-pow(5,d,8))%8]
            r=(n-pow(5,d,9))%9
            y=4 if r%3 else 3 if r==0 else 0
            z=1 if (n-pow(3,c,7)-pow(5,d,7))%7==0 else 8
            total+=x*y*z
    return F(total,2304)

def rho23(n:int)->F:
    return sum((a2(n,c,d)*a3(n,d) for c in range(6) for d in range(6)),F(0))/36

def beta11(n:int)->F:
    t=n%11
    k=sum((pow(3,c,11)+pow(5,d,11))%11==t for c in range(5) for d in range(5))
    return 1-F(11*k,300)

def rho4(n:int)->F:
    return rho237(n%504)*beta11(n)

def vp(x:int,p:int)->int:
    if x<=0: raise ValueError('valuation requires a positive integer')
    e=0
    while x%p==0: x//=p; e+=1
    return e

def l2(m:int)->bool:
    return m==0 or (m//2**vp(m,2))%4==1

def local(m:int,ps:tuple[int,...])->bool:
    return m==0 or (l2(m) and all(vp(m,p)%2==0 for p in ps))

def powers(b:int,n:int)->list[int]:
    out=[]; x=1
    while x<=n: out.append(x); x*=b
    return out

def factor_small(n:int)->dict[int,int]:
    out={}; p=2
    while p*p<=n:
        while n%p==0: out[p]=out.get(p,0)+1; n//=p
        p+=1
    if n>1: out[n]=out.get(n,0)+1
    return out

def power_orbit(b:int,m:int)->dict:
    seen={}; vals=[]; x=1%m
    while x not in seen:
        seen[x]=len(vals); vals.append(x); x=x*b%m
    s=seen[x]
    return {'base':b,'modulus':m,'preperiod':s,'period':len(vals)-s,
            'prefix':vals[:s],'cycle':vals[s:]}

def norm_mask(m:int)->list[bool]:
    # CRT reduces exact solvability x^2+y^2=r mod m to its prime powers.
    components=[]
    for p,e in factor_small(m).items():
        q=p**e; sq={x*x%q for x in range(q)}
        ss={(x+y)%q for x in sq for y in sq}
        components.append((q,ss))
    return [all(r%q in ss for q,ss in components) for r in range(m)]

def quotient_density(n:int,m:int)->F:
    u=power_orbit(3,m)['cycle']; v=power_orbit(5,m)['cycle']; mask=norm_mask(m)
    return F(sum(mask[(n-x-y)%m] for x in u for y in v),len(u)*len(v))

def count_residue(start:int,width:int,m:int,r:int)->int:
    if width<0 or m<1: raise ValueError('invalid interval/modulus')
    r%=m
    return (start+width-1-r)//m-(start-1-r)//m

def primes_upto(n:int)->list[int]:
    if n<2:return []
    s=bytearray(b'\x01')*(n+1);s[:2]=b'\x00\x00'
    for p in range(2,isqrt(n)+1):
        if s[p]:s[p*p::p]=b'\x00'*((n-p*p)//p+1)
    return [p for p in range(2,n+1) if s[p]]

def verify_point_certificates(path:Path)->tuple[list[dict],dict]:
    data=json.loads(path.read_text())
    assert tuple(row['n'] for row in data)==TARGETS
    factors={int(p) for row in data for x in row['pairs'] for p in x['factorization']}
    trial_primes=primes_upto(isqrt(max(factors)))
    divisibility_checks=0
    for p in sorted(factors):
        assert p>=2
        for q in trial_primes:
            if q*q>p:break
            assert p%q, ('composite certificate factor',p,q)
            divisibility_checks+=1
    summaries=[]
    for row in data:
        n=row['n']; p3=powers(3,n); p5=powers(5,n)
        expected={(c,d) for c,x in enumerate(p3) for d,y in enumerate(p5) if x+y<=n}
        seen=set(); R=0; gs=Counter(); hist=Counter(); conditioned=Counter()
        for x in row['pairs']:
            c=x['c'];d=x['d'];m=x['m'];seen.add((c,d))
            assert m==n-3**c-5**d and m>=0
            fs={int(p):e for p,e in x['factorization'].items()}
            assert all(isinstance(e,int) and e>=1 for e in fs.values())
            assert (m==0 and not fs) or prod(p**e for p,e in fs.items())==m
            bad=sorted(p for p,e in fs.items() if p%4==3 and e%2)
            assert bad==sorted(x['bad_primes'])
            norm=not bad
            assert norm==x['norm'];R+=norm
            if bad:hist[bad[0]]+=1
            for name,ps in [('23',(3,)),('237',(3,7)),('23711',(3,7,11))]:
                flag=local(m,ps);gs[name]+=flag
                assert flag==x['local_flags'][name]
            if bad and local(m,(3,7,11)):conditioned[bad[0]]+=1
        assert len(seen)==len(row['pairs']) and seen==expected
        assert R==row['R'] and len(expected)==row['grid']
        assert dict(gs)==row['G']
        assert str(rho237(n%504))==row['rho237'] and str(rho4(n))==row['rho23711']
        assert row['is_local_minimizer_237']==(rho237(n%504)==F(21,128))
        assert row['is_local_minimizer_23711']==(rho4(n)==F(1869,12800))
        out={k:v for k,v in row.items() if k not in ('pairs','least_bad_hist')}
        out['least_bad_hist_recomputed']={str(p):v for p,v in sorted(hist.items())}
        out['least_bad_after_G23711']={str(p):v for p,v in sorted(conditioned.items())}
        out['rho237_ratio_to_minimum']=str(rho237(n%504)/F(21,128))
        out['global_window_rank_independently_replayed']=False
        summaries.append(out)
    assert 6105**2+9297**2+3**25+5**16==1000000205302
    return summaries,{'targets':len(data),'grid_rows':sum(r['grid'] for r in data),
       'distinct_prime_factors':len(factors),'largest_prime_factor':max(factors),
       'trial_divisibility_checks':divisibility_checks,
       'primality_method':'exhaustive trial division by all primes <= sqrt(p)',
       'complete_grid_coverage_verified':True,'factor_products_verified':True}

def extra_counterexamples()->dict:
    cases=[(560,1,2,{2:2,7:1,19:1}),
           (277760,1,2,{2:2,7:2,13:1,109:1}),
           (28280,3,2,{2:2,7057:1}),
           (915320,3,2,{2:2,19:1,12043:1})]
    out=[]
    for n,c,d,fs in cases:
        m=n-3**c-5**d
        assert prod(p**e for p,e in fs.items())==m
        for p in fs:
            assert p>=2 and all(p%q for q in range(2,isqrt(p)+1))
        bad=sorted(p for p,e in fs.items() if p%4==3 and e%2)
        out.append({'n':n,'c':c,'d':d,'m':m,'factorization':fs,'bad_primes':bad,
            'L2':l2(m),'G23711':local(m,(3,7,11)),'n_mod27720':n%27720,'n_mod16':n%16})
    assert 336**2+406**2==277760-3-25
    return {'same_modulus_different_7_parity':out[:2],
            'same_rigid_cell_success_and_failure':out[2:],
            'scope':'residual counterexamples only; neither n is claimed unrepresentable'}

def build(out:Path)->dict:
    out.mkdir(parents=True,exist_ok=True)
    table=[rho237(n) for n in range(504)]
    assert min(table)==F(21,128)
    mins=[n for n,v in enumerate(table) if v==min(table)]
    assert mins==[56,70,224,238,392,406]
    assert all((n in mins)==(n%168 in (56,70)) for n in range(504))
    # Independent Fraction implementation of every cell, not the scaled-integer implementation.
    for n in range(504):
        assert table[n]==sum((a2(n,c,d)*a3(n,d)*a7(n,c,d)
                        for c in range(6) for d in range(6)),F(0))/36
    table4=[table[n%504]*beta11(n) for n in range(5544)]
    assert min(table4)==F(1869,12800)
    min4=[n for n,v in enumerate(table4) if v==min(table4)]
    assert all((n in min4)==(n%168 in (56,70) and n%11 in (2,6,7,8,10)) for n in range(5544))
    spectrum4=sorted(set(table4))
    assert spectrum4[1]==F(973,6400)
    assert (spectrum4[0]+spectrum4[1])/2==F(763,5120)
    hard24={2,4,8,22}
    band_inside=max(table4[n] for n in range(5544) if n%24 in hard24)
    band_outside=min(table4[n] for n in range(5544) if n%24 not in hard24)
    assert band_inside==F(161,768) and band_outside==F(2047,9600)
    assert band_outside-band_inside==F(23,6400)
    assert (band_inside+band_outside)/2==F(8119,38400)
    band={'hard_mod24':[2,4,8,22],'maximum_rho237_inside':'161/768',
      'minimum_rho237_outside':'23/96','maximum_rho23711_inside':str(band_inside),
      'minimum_rho23711_outside':str(band_outside),'rho23711_gap':'23/6400',
      'separating_threshold':'8119/38400','scope':'local-density band, not an inverse theorem for R'}
    min168=[n for n in range(168) if n in (56,70)]
    min1848=[n for n in range(1848) if n%168 in (56,70) and n%11 in (2,6,7,8,10)]
    lifts=[]
    for k in range(11):
        r=560+2520*k
        lifts.append({'k':k,'residue_mod27720':r,'n_mod11':r%11,
          'K11':sum((pow(3,c,11)+pow(5,d,11))%11==r%11 for c in range(5) for d in range(5)),
          'beta11':str(beta11(r)),'rho23711':str(rho4(r)),
          'is_minimizer':rho4(r)==min(table4),
          'finite_quotient_norm_density_mod27720':str(quotient_density(r,27720))})
    assert [x['residue_mod27720'] for x in lifts if x['is_minimizer']]==[560,8120,18200,20720,23240]
    rows24=[]
    for r in range(24):
        candidates=list(range(r,504,24));best=min(table[n] for n in candidates)
        rows24.append({'n_mod24':r,'min_rho237':str(best),
          'minimizers_mod504':[n for n in candidates if table[n]==best]})
    # Short minimum proof certificate: weighted 7-hit mass on the four hardest 23-classes.
    critical=[]
    for r in (2,4,8,22):
        rows=[]
        for t in range(9):
            if t%3!=r%3:continue
            vals=[]
            for z in range(7):
                n=next(n for n in range(r,504,24) if n%9==t and n%7==z)
                mass=sum((a2(n,c,d)*a3(n,d) for c in range(6) for d in range(6)
                       if (n-pow(3,c,7)-pow(5,d,7))%7==0),F(0))/36
                vals.append(int(mass*288));assert F(vals[-1],288)==mass
            rows.append({'n_mod9':t,'288_times_weighted_7_hit_mass_by_n_mod7':vals})
        critical.append({'n_mod24':r,'rows':rows})
    residues={'definition':'exact limiting local orbit densities; not exact finite-grid counts',
      'coarse_hard_band':band,
      'rho237_period':504,'rho237_minimum':'21/128','rho237_minimizers_mod504':mins,
      'minimizer_set_reduced_period_237':168,'minimizers_mod168':min168,
      'rho23711_period':5544,'rho23711_minimum':'1869/12800',
      'rho23711_minimizers_mod5544':min4,'minimizer_set_reduced_period_23711':1848,
      'minimizers_mod1848':min1848,
      'rho237_minimizers_mod2520':[n for n in range(2520) if n%168 in (56,70)],
      'rho23711_minimizers_mod27720':[n for n in range(27720) if n%1848 in min1848],
      'rho237_by_residue_mod504':list(map(str,table)),
      'rho23711_by_residue_mod5544':list(map(str,table4)),
      'row_minimum_certificate_mod24':rows24,'critical_7_hit_certificate':critical,
      'lifts_of_560_mod2520':lifts,
      'second_smallest_rho23711':str(spectrum4[1]),'local_count_inverse_threshold':'763/5120'}
    orbit_rows=[]
    for m in MODULI:
        orbit_rows.append({'M':m,'n_residue':560%m,'orbit_3':power_orbit(3,m),
           'orbit_5':power_orbit(5,m),'finite_norm_residues': [r for r,v in enumerate(norm_mask(m)) if v],
           'eventual_quotient_norm_density':str(quotient_density(560,m))})
    points,prime_receipt=verify_point_certificates(Path(__file__).with_name('POINT_CERTIFICATES.json'))
    windows=[]
    for label,start,tp in [('A',10**8,251),('B',10**10,255),('C',10**12,256)]:
        predicted_s1=sum(count_residue(start,W,24,r) for r in (2,4,8,22))
        lift_denoms=[dict(k=x['k'],residue_mod27720=x['residue_mod27720'],
                         full_window_count=count_residue(start,W,27720,x['residue_mod27720']),
                         extremal_count=None) for x in lifts]
        windows.append({'window':label,'start':start,'end_exclusive':start+W,'targets':W,
          'S1_24_class_confusion':{'basis':'TP supplied by brief, NOT raw-pilot replay; denominators exact from endpoints',
            'selected_hardest_count':256,'full_window_predicted_hard':predicted_s1,
            'TP':tp,'FN':256-tp,'FP':predicted_s1-tp,'TN':W-predicted_s1-(256-tp),
            'precision':str(F(tp,predicted_s1)),'recall':str(F(tp,256)),
            'enrichment_with_actual_denominator':str(F(tp*W,256*predicted_s1))},
          'full_window_560_count':count_residue(start,W,2520,560),
          'full_window_exact_237_minimizer_count':sum(count_residue(start,W,168,r) for r in min168),
          'full_window_exact_23711_minimizer_count':sum(count_residue(start,W,1848,r) for r in min1848),
          'lifts_of_560':lift_denoms,
          'exact_minimizer_TP':None,'exact_minimizer_FP':None,'exact_minimizer_FN':None,
          'raw_pilot_validated':False})
    validation={'raw_pilot_available':False,'scanner_definition_audited':False,
        'full_window_representation_data_available':False,
        'extremal_subclass_independence_test_performed':False,
        'points':points,'windows':windows,'prime_receipt':prime_receipt,
        'limitations':['No assertion that the six targets exhaust extrema or controls.',
          'Window minimum ranks and S1 TP counts are reported inputs, not independently replayed.',
          'Null means unavailable, not zero. No enrichment denominator was guessed.',
          'Five task-listed argmins lie outside the exact local minimizer family; this does not refute a near-minimizer inverse or an R=0 inverse.']}
    # Exact least-bad capacities and the literal exponent-rigidity identity.
    tau3=sum((a3(560,d) for d in range(6)),F(0))/6
    tau37=sum((a3(560,d)*a7(560,c,d) for c in range(6) for d in range(6)),F(0))/36
    assert tau3==F(5,8) and tau37==F(205,384)
    assert tau3-tau37==F(35,384)
    assert tau37*(1-beta11(560))==F(451,7680)
    assert rho23(560)-rho237(560%504)==F(7,128)
    assert rho237(560%504)*(1-beta11(560))==F(231,12800)
    for nn in (0,8):
        for cc in (1,3):
            for dd in (0,2):
                assert ((nn-pow(3,cc,16)-pow(5,dd,16))%16==4)==((cc+dd-3-nn//4)%4==0)
    assert [vp(5**30-1,p) for p in (2,3,7,11)]==[3,2,1,1]
    extras=extra_counterexamples()
    summary={'authority_commit':'fd8aa2d5dd2cff758f2eb021c486ff9e2c3d1f38',
       'authority_tree':'325265d83abae42acadc59f8107d88d1375085be',
       'why560':'PARTIALLY EXPLAINED: proved minimizing core, extra 5/mod9 specificity not explained',
       'exact_local_minimizer_classification':True,'representation_inverse_proved':False,
       'counterexample_forced_into_finite_family':False,'second_stage_completion_proved':False,
       'local_G_inverse_proved':True,'full_level_B_claimed':False,
       'level':'local-minimizer theorem component of B; full pilot coupling unavailable; not A, C or full D',
       'rho237_minimum':'21/128','rho23711_minimum':'1869/12800',
       'coarse_hard_band':band,
       'minimizers_mod1848':min1848,'lifts_minimizing_560':[x['residue_mod27720'] for x in lifts if x['is_minimizer']],
       'uniform_G_error_exponent':'9/5','finite_G_fixed_period_claimed':False,
       'original_n_inverse_route':'CONTINUE EXPLORATORY',
       'new_original_n_window_scans':0,'point_targets_verified':list(TARGETS),
       'more_large_computation':'NO','codex_needed_next':'NO',
       'A303656':'UNRESOLVED','github_writes_performed':'NONE',
       'prime_receipt':prime_receipt,'proof_scope':'self-contained derivations, not externally refereed or merged authority'}
    def dump(name,obj):
        (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    dump('RESIDUE_CLASSES.json',residues);dump('ORBITS.json',orbit_rows)
    dump('EXTREMAL_VALIDATION.json',validation);dump('COUNTEREXAMPLES.json',extras)
    dump('results.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path(__file__).parent)
    build(parser.parse_args().out)
