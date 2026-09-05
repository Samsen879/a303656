"""Necessary original-resource cardinality/charge convolution over Z/modulus.

No macro is counted as a resource. False means a rigorous obstruction for the
supplied exact state table. True means only that this relaxation did not refute.
"""
from __future__ import annotations
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import os
from random import Random
import json
from direct_check import direct_csp, direct_masks
from run_small_models import DOMAINS, pair_catalog, cyclic_states


def cardinality_charge_filter(state_masks, domain_size, charges, modulus):
    if modulus < 2 or len(charges)!=2*domain_size:
        raise ValueError('Require one charge per anchor-point demand and modulus>=2.')
    N=2*domain_size
    full=(1<<domain_size)-1
    if any(a & ~full or b & ~full for states in state_masks for a,b in states):
        raise ValueError('Mask exceeds the fixed demand domain.')
    row_profiles=[]
    for states in state_masks:
        if not states:
            return {'passes':False,'reason':'empty original row state space'}
        profiles=set()
        for a,b in states:
            mask=a | (b<<domain_size)
            charge=sum(charges[k] for k in range(N) if mask>>k&1)%modulus
            profiles.add((mask.bit_count(),charge))
        row_profiles.append(profiles)
    sums={(0,0)}
    for profiles in row_profiles:
        sums={(s+t,(a+b)%modulus) for s,a in sums for t,b in profiles}
    target=sum(charges)%modulus
    # At t excess incidences, their total charge lies in the t-fold sumset
    # of actual demand charges. This deliberately forgets where overlap occurs.
    omega={v%modulus for v in charges}
    max_excess=max((s-N for s,_ in sums),default=-1)
    excess=[{0}]
    for _ in range(max(0,max_excess)):
        excess.append({a+b if a+b<modulus else a+b-modulus for a in excess[-1] for b in omega})
    survivors=sorted((s,q) for s,q in sums if s>=N and (q-target)%modulus in excess[s-N])
    return {'passes':bool(survivors),'demand_count':N,'modulus':modulus,
            'target_charge':target,'profile_sum_states':len(sums),
            'surviving_profiles':survivors,
            'sum_maximum_row_capacities':sum(max(s for s,_ in ps) for ps in row_profiles)}


def run():
    exact=cyclic_states(3,(1,1,2))
    relaxed=cyclic_states(3,(1,1,2),relaxed=True)
    charges=[0,-1,-2,0,1,2]
    a=cardinality_charge_filter(exact,3,charges,3)
    b=cardinality_charge_filter(relaxed,3,charges,3)
    assert not a['passes'] and b['passes']
    relations=[[(0,1),(0,2)],[(0,1),(1,0)],[(0,1),(2,0)]]
    state_table=[[(1<<x,1<<y) for x,y in r] for r in relations]
    bad=cardinality_charge_filter(state_table,3,charges,3)
    direct=direct_csp(state_table,3)
    assert bad['passes'] and not direct['solutions'] and direct['anchor_counts']==[2,2]
    rng=Random(57721)
    records=[]
    for dims in DOMAINS:
        n=1
        for d in dims:n*=d
        cat=pair_catalog(dims,True)
        blocked=feasible=false_passes=0
        for test in range(100):
            states=[]
            for row in range(2+test%3):
                choices=[cat[rng.randrange(len(cat))] for _ in range(2+test%2)]
                states.append([tuple(direct_masks(dims,[r[c]])[0] for c in (0,1)) for r in choices])
            costs=[rng.randrange(7) for _ in range(2*n)]
            filtered=cardinality_charge_filter(states,n,costs,7)
            original=direct_csp(states,n)
            feasible+=bool(original['solutions'])
            blocked+=not filtered['passes']
            false_passes+=filtered['passes'] and not original['solutions']
            assert not original['solutions'] or filtered['passes']
        records.append({'domain':dims,'tested_state_systems':100,
                        'feasible_systems':feasible,'filter_blocked_systems':blocked,
                        'infeasible_systems_not_blocked':false_passes,
                        'unsound_rejections':0})
    output={'cyclic_translation_obstructed':a,'off_diagonal_relaxation_not_obstructed':b,
            'charge_not_sufficient':{'relations':relations,'direct':direct,'filter':bad,
                                     'zero_charge_but_noncovering_choice':[[0,1]]*3},
            'finite_filter_soundness_crosschecks':records}
    out=Path(os.environ.get('A303656_OUTPUT_DIR', Path(__file__).resolve().parents[1]/'results'))
    out.mkdir(parents=True, exist_ok=True)
    p=out/'cardinality_charge_filter.json'
    p.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    print(json.dumps(output,sort_keys=True,indent=2))

if __name__=='__main__':run()
