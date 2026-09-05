#!/usr/bin/env python3
"""Independent arithmetic audit of the free-coordinate rigid blocker theorem.

The bounded resource scan repeats the EXISTING 10^7 bound; it does not enlarge
it. It uses the Fermat-exponent Wieferich criterion, rather than reducing the
order at every prime as in the source inventory.
"""
from __future__ import annotations
from pathlib import Path
from math import isqrt, lcm
from itertools import product
from random import Random
from collections import defaultdict
import hashlib, json, os
from residue_states import power_cycle, direct_mask
from contraction import contract_provenance

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('A303656_OUTPUT_DIR', ROOT/'results'))
OUT.mkdir(parents=True, exist_ok=True)


def factor(n):
    result={}
    d=2
    while d*d<=n:
        while n%d==0:
            result[d]=result.get(d,0)+1;n//=d
        d=3 if d==2 else d+2
    if n>1:result[n]=result.get(n,0)+1
    return result


def order_of_5(p):
    w=p-1
    for f in factor(p-1):
        while w%f==0 and pow(5,w//f,p)==1:w//=f
    return w


def repeat_frozen_inventory(bound=10_000_000):
    prime=bytearray(b'\x01')*(bound+1);prime[0:2]=b'\x00\x00'
    for d in range(2,isqrt(bound)+1):
        if prime[d]:
            start=d*d
            prime[start:bound+1:d]=b'\x00'*(((bound-start)//d)+1)
    count=0;hits=[];digest=hashlib.sha256()
    for q in range(3,bound+1,4):
        if not prime[q]:continue
        count+=1;digest.update(f'{q}\n'.encode())
        # q does not divide (q-1)/ord_q(5), so this is equivalent to
        # q^2 | 5^ord_q(5)-1. No probabilistic primality is used.
        if pow(5,q-1,q*q)==1:
            w=order_of_5(q)
            s=2
            while pow(5,w,q**(s+1))==1:s+=1
            hits.append({'prime':q,'order':w,'order_factorization':factor(w),'lifting_depth':s})
    assert count==332398
    assert [h['prime'] for h in hits]==[20771,40487]
    assert hits[0]['order']==10385 and hits[1]['order']==40486
    blockers={20771:5,40487:653}
    for h in hits:
        ell=blockers[h['prime']]
        assert h['order']%ell==0 and (ell==5 or ell%4==1)
    result={'bound':bound,'scope':'EXACT FINITE INVENTORY; NO CLAIM ABOVE THE BOUND',
            'method':'Eratosthenes sieve + 5^(q-1) mod q^2; exact order only for hits',
            'admitted_prime_count':count,'prime_list_newline_sha256':digest.hexdigest(),
            'nonregular_rows':hits,'paired_blocker_assignment':blockers,
            'loads':[{'coordinate':5,'original_row_count':1,'maximum_forbidden_digits':2,'guaranteed_remaining_digits':3},
                     {'coordinate':653,'original_row_count':1,'maximum_forbidden_digits':2,'guaranteed_remaining_digits':651}],
            'bounded_panel_no_go':'all finite admitted P subset of primes <= bound; arbitrary K,E,shared residues; optional sound two-adic row',
            'larger_formal_subclass':'any finite P with all nonregular primes contained in {20771,40487}; no size bound on regular rows'}
    (OUT/'rigid_blocker_inventory.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('inventory',count,hits,flush=True)
    return result


def check_large_known_boundary():
    q=1645333507
    assert factor(q)=={q:1}
    w=order_of_5(q)
    f=factor(w)
    assert w==1645333506 and f=={2:1,3:3,30469139:1}
    assert pow(5,w,q*q)==1 and pow(5,w,q**3)!=1
    # Not blocked by a coordinate which is universally non-admitted.
    # A panel omitting 3 or 30469139 can still use a panel-relative blocker.
    result={'prime':q,'order':w,'order_factorization':f,'lifting_depth':2,
            'structurally_ineligible_odd_order_factors':[],
            'implication':'the structural blocker criterion does not cover every known nonregular row',
            'not_a_complete_certificate':True}
    (OUT/'blocker_boundary_resource.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('boundary',result,flush=True)


def joint_reverse_crt_tests():
    rng=Random(20260905)
    configurations=[[(3,2),(7,2)],[(3,4),(7,2)],[(3,2),(11,2)],[(3,2),(7,2),(11,2)]]
    records=[]
    for spec in configurations:
        cycles=[power_cycle(p,k) for p,k in spec]
        ws=[order_of_5(p) for p,k in spec]
        U=lcm(*ws);L=lcm(*(len(c) for c in cycles))
        tests=60;coarse_checks=0;full_checks=0
        for _ in range(tests):
            row_masks=[]
            for (p,k),pw in zip(spec,cycles):
                choices=[h for h in range(1,k,2)]
                accepted=frozenset(h for h in choices if rng.randrange(2)) or frozenset([choices[0]])
                r=rng.randrange(p**k)
                mask=direct_mask(p,k,accepted,pw,r);period=len(pw)
                row_masks.append([[(mask>>(c*period+d%period))&1 for d in range(L)] for c in (0,1)])
            for x in range(U):
                lifts=range(x,L,U)
                coarse_safe=all(not all(row[c][d] for d in lifts) for row in row_masks for c in (0,1))
                full_safe=any(all(not row[c][d] for row in row_masks for c in (0,1)) for d in lifts)
                assert coarse_safe==full_safe
                coarse_checks+=1
            full_checks+=L
        records.append({'row_prime_precisions':spec,'U':U,'L':L,'residue_valuation_systems':tests,
                        'coarse_classes_checked':coarse_checks,'full_period_cells_per_system':L,
                        'full_period_cell_checks':full_checks,'mismatches':0})
    (OUT/'joint_reverse_crt_checks.json').write_text(json.dumps(records,sort_keys=True,indent=2)+'\n')
    print('joint reverse CRT',records,flush=True)


def constructive_paired_blocker_tests():
    """All paired rigid digits with dependent lower dynamic guards, exact sets.

Coordinates 3,5,7. Five is free (no original dynamic 5-row). The regular
3- and 7-like events are proper centered beta-one shells. The two 7-guards
are distinct coordinate-3 singleton cylinders, so the paired dynamic exclusion
is imposed on the whole lower assignment. One original rigid row fixes a
5-digit and 7-digit at each anchor. These are abstract normal-form tests,
not a claim to realize a prime with order 35.
"""
    count=0;choices_checked=0
    for b0,b1,z0,z1 in product(range(5),range(5),range(7),range(7)):
        if (b0,z0)==(b1,z1):continue # shared-row pointwise exclusion
        x5=next(x for x in range(5) if x not in (b0,b1))
        # For each lower-3 choice, only one of the anchor-7 guards is active.
        # A lower 3-row is active only at anchor0, with center1.
        x3=1
        active0=x3==0;active1=x3==1
        assert not(active0 and active1)
        center0=(b0+z1)%7;center1=(b1+z0)%7
        x7=center0 if active0 else center1 if active1 else 0
        for c in (0,1):
            fatal3=(c==0 and x3!=1)
            fatal7=((active0 if c==0 else active1) and x7!=(center0 if c==0 else center1))
            rigid=(x5==(b0 if c==0 else b1) and x7==(z0 if c==0 else z1))
            assert not(fatal3 or fatal7 or rigid)
        count+=1
        # Independent complete-product verification of the constructed cell
        # and existence of common odd-safe cells.
        safes=[]
        for y3,y5,y7 in product(range(3),range(5),range(7)):
            covered=[]
            for c in (0,1):
                active=(y3==c)
                center=center0 if c==0 else center1
                covered.append((c==0 and y3!=1) or (active and y7!=center) or
                               (y5==(b0 if c==0 else b1) and y7==(z0 if c==0 else z1)))
            if not any(covered):safes.append((y3,y5,y7))
        assert (x3,x5,x7) in safes
        for c in (0,1):
            shapes=[(5,31,127) if c==0 else None,
                    (1<<c,31,127^(1<<(center0 if c==0 else center1))),
                    (7,1<<(b0 if c==0 else b1),1<<(z0 if c==0 else z1))]
            assert not contract_provenance((3,5,7),shapes)['covered']
        choices_checked+=105
    result={'abstract_domain':[3,5,7],'paired_rigid_states_checked':count,
            'complete_product_cells_checked':choices_checked,'contraction_root_checks':2*count,'mismatches':0,
            'scope':'ARITHMETIC-INSPIRED NORMAL FORM, NOT ACTUAL PRIME REALIZATIONS'}
    (OUT/'paired_blocker_constructive_checks.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('constructive',result,flush=True)

if __name__=='__main__':
    repeat_frozen_inventory()
    check_large_known_boundary()
    joint_reverse_crt_tests()
    constructive_paired_blocker_tests()
