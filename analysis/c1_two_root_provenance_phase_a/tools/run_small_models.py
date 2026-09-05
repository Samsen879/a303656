from __future__ import annotations
import json
import os
from itertools import product, combinations_with_replacement, permutations
from pathlib import Path
from random import Random
from fractions import Fraction
from contraction import contract_provenance, contract_geometry, symbolic_roots, evaluate_polynomial
from direct_check import direct_masks, direct_minimal_covers, initial_rank_saturations, direct_csp

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('A303656_OUTPUT_DIR', ROOT / 'results'))
OUT.mkdir(parents=True, exist_ok=True)
DOMAINS = [(2,2),(2,3),(3,3),(2,2,2),(2,3,2),(3,3,2)]


def safe_json(obj):
    if isinstance(obj, (set, frozenset)):
        return [safe_json(x) for x in sorted(obj, key=lambda a: repr(a))]
    if isinstance(obj, tuple):
        return [safe_json(x) for x in obj]
    if isinstance(obj, list):
        return [safe_json(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): safe_json(v) for k, v in obj.items()}
    if isinstance(obj, Fraction):
        return str(obj)
    return obj


def save(name, obj):
    (OUT/name).write_text(json.dumps(safe_json(obj), sort_keys=True, indent=2)+'\n')


def shape_catalog(dims):
    full = tuple((1 << n)-1 for n in dims)
    patterns = sorted(set(product(*[[((1 << n)-1)] + [1 << a for a in range(n)] for n in dims])))
    return [None]+[p for p in patterns if p != full]


def rank(shape, dims):
    if shape is None:
        return -1
    return max(k for k,(s,n) in enumerate(zip(shape,dims)) if s != (1 << n)-1)


def pair_catalog(dims, exclusion=True, fixed_rank=False):
    shapes = shape_catalog(dims)
    masks = direct_masks(dims, shapes)
    result = []
    for i,a in enumerate(shapes):
        for j,b in enumerate(shapes):
            if a is None and b is None:
                continue
            if exclusion and masks[i]&masks[j]:
                continue
            if fixed_rank and a is not None and b is not None and rank(a,dims) != rank(b,dims):
                continue
            result.append((a,b))
    return result


def check_case(dims, rows, trace=False):
    info = {'domain': dims, 'rows': rows, 'anchors': []}
    for c in (0,1):
        shapes = [r[c] for r in rows]
        expected = direct_minimal_covers(dims, shapes)
        actual = contract_provenance(dims, shapes, trace=trace)
        geometric = contract_geometry(dims, shapes)
        assert expected == actual['minimal_supports'], (dims, rows, c, expected, actual)
        assert bool(expected) == geometric == actual['covered']
        info['anchors'].append(actual)
    masks0 = direct_masks(dims, [r[0] for r in rows])
    masks1 = direct_masks(dims, [r[1] for r in rows])
    info['pointwise_exclusive'] = all(not (a&b) for a,b in zip(masks0,masks1))
    info['initial_rank_saturations'] = [initial_rank_saturations(dims,[r[c] for r in rows]) for c in (0,1)]
    return info


def examples():
    r3 = [((1,3),(2,3)), ((2,1),(1,1)), ((2,2),(1,2))]
    i1 = [((1,3),(2,1)), ((2,3),(1,1)), (None,(3,2))]
    overlap5 = [((3,1),(3,2))]*2 + [((3,2),(3,1))]*3
    overlap3 = [((3,1),(3,2))]*2 + [((3,2),(3,1))]
    result = {
        'I2_I3_I4_three_row': check_case((2,2),r3,True),
        'I1_original_rank_three_row': check_case((2,2),i1,True),
        'I5_five_row_six_macros': check_case((2,2),overlap5,True),
        'I6_three_row_covered_mass_failure': check_case((2,2),overlap3,True),
        'I6_masses': {'original_sum_per_anchor':'3/2','new_provenance_clause_sum':'2',
                      'deduplicated_geometry_mass':'1'},
        'scope': 'ABSTRACT PRODUCT-CYLINDER ROWS; NOT ACTUAL PRIME ROWS'
    }
    save('counterexamples.json', result)
    return result


def exhaustive_minimality():
    dims=(2,2)
    catalogs={False:pair_catalog(dims,True,False), True:pair_catalog(dims,True,True)}
    result=[]
    for fixed_rank,cat in catalogs.items():
        pre_masks=[tuple(direct_masks(dims,[s])[0] for s in row) for row in cat]
        per_n=[]
        for nrows in range(0,4):
            checked=joint=bad_fiber=bad_rank=0
            first_fiber=first_rank=None
            for indices in combinations_with_replacement(range(len(cat)), nrows):
                checked+=1
                unions=[0,0]
                for j in indices:
                    for c in (0,1): unions[c] |= pre_masks[j][c]
                if unions != [15,15]: continue
                joint+=1
                rows=[cat[j] for j in indices]
                sats=[initial_rank_saturations(dims,[r[c] for r in rows]) for c in (0,1)]
                has_common=any(set(sats[0][k])&set(sats[1][k]) for k in (0,1))
                common_rank=any(sats[0][k] and sats[1][k] for k in (0,1))
                if not has_common:
                    bad_fiber+=1
                    if first_fiber is None: first_fiber=rows
                if not common_rank:
                    bad_rank+=1
                    if first_rank is None: first_rank=rows
                # Exhaustive independent root + all row-enable subfamilies.
                check_case(dims,rows)
            per_n.append({'rows':nrows,'systems_up_to_row_permutation':checked,'both_roots':joint,
                          'no_common_original_rank_full_fiber':bad_fiber,
                          'no_common_original_saturation_rank':bad_rank,
                          'first_fiber_counterexample':first_fiber,'first_rank_counterexample':first_rank})
        result.append({'fixed_rank_per_row_between_anchors':fixed_rank,'row_pair_catalog_size':len(cat), 'counts':per_n})
    save('exhaustive_minimality.json',result)
    return result


def sample_suite(samples_per_stage=250):
    rng=Random(303656)
    records=[]
    for dims in DOMAINS:
        for exclusion in (False,True):
            cat=pair_catalog(dims,exclusion)
            joint=single=total_macros=0
            enabled_checks=0
            for sample in range(samples_per_stage):
                nrows=1+sample%6
                rows=[cat[rng.randrange(len(cat))] for _ in range(nrows)]
                out=check_case(dims,rows)
                if exclusion: assert out['pointwise_exclusive']
                roots=[a['covered'] for a in out['anchors']]
                joint+=all(roots); single+=sum(roots)
                total_macros+=sum(a['derived_clause_count_before_absorption'] for a in out['anchors'])
                enabled_checks+=2*(1<<nrows)
            records.append({'domain':dims,'pointwise_exclusion':exclusion,'row_pair_catalog':len(cat),
                            'tested_pair_systems':samples_per_stage,'covered_anchor_roots':single,
                            'double_roots':joint,'all_enable_assignments_checked':enabled_checks,
                            'generated_macros':total_macros,'mismatches':0})
    save('six_domain_crosschecks.json',records)
    return records


def cyclic_states(n, offsets, duplicate_lower=1, relaxed=False):
    result=[]
    for shift in offsets:
        states=[]
        for a in range(n):
            targets=[b for b in range(n) if b != a] if relaxed else [(a+shift)%n]
            for b in targets:
                masks=tuple(sum(1 << (y*n+v) for y in range(duplicate_lower)) for v in (a,b))
                states.append(masks)
        result.append(states)
    return result


def csp_suite(samples_per_domain=50):
    records=[]
    for relaxed in (False,True):
        states=cyclic_states(3,(1,1,2),2,relaxed)
        direct=direct_csp(states,6)
        symbolic=symbolic_roots((2,3),states)
        for assignment in product(*(range(len(s)) for s in states)):
            actual=tuple(assignment) in direct['solutions']
            assert evaluate_polynomial(symbolic['joint'],assignment)==actual
        records.append({'model':'off_diagonal_pair_relaxation' if relaxed else 'exact_translation_coupling',
                        'domain':[2,3],'state_counts':[len(s) for s in states],
                        'direct':direct,'symbolic':symbolic})
    assert len(records[0]['direct']['solutions'])==0
    assert len(records[1]['direct']['solutions'])==12
    save('state_sensitive_csp_witness.json',records)
    rng=Random(271828)
    randomized=[]
    for dims in DOMAINS:
        cat=pair_catalog(dims,True)
        n=1
        for x in dims:n*=x
        checks=0;false_positive_unions=0;exact_sat=0
        for sample in range(samples_per_domain):
            nrows=2+sample%3
            states=[]
            for p in range(nrows):
                selected=[cat[rng.randrange(len(cat))] for _ in range(2+sample%2)]
                states.append([tuple(direct_masks(dims,[pair[c]])[0] for c in (0,1)) for pair in selected])
            direct=direct_csp(states,n)
            symbolic=symbolic_roots(dims,states)
            exact_sat+=bool(direct['solutions'])
            for choices in product(*(range(len(s)) for s in states)):
                checks+=1
                assert evaluate_polynomial(symbolic['joint'],choices)==(choices in direct['solutions'])
            unions=[0,0]
            for ss in states:
                for pair in ss:
                    for c in (0,1):unions[c]|=pair[c]
            false_positive_unions+=(unions==[(1<<n)-1]*2 and not direct['solutions'])
        randomized.append({'domain':dims,'state_systems':samples_per_domain,'assignments_checked':checks,
                           'exact_sat_systems':exact_sat,'marginal_union_false_positives':false_positive_unions,
                           'mismatches':0})
    save('csp_crosschecks.json',randomized)
    return randomized


def charge_suite():
    out=[]
    for n in range(2,6):
        counts={'n':n,'offset_vectors':0,'charge_blocked':0,'charge_zero_but_unsat':0,
                'feasible_offset_vectors':0,'valid_joint_assignments':0}
        perms=list(permutations(range(n)))
        for shifts in product(range(1,n),repeat=n):
            counts['offset_vectors']+=1
            solutions=sum(len({(a+delta)%n for a,delta in zip(perm,shifts)})==n for perm in perms)
            if sum(shifts)%n:
                counts['charge_blocked']+=1
                assert solutions==0
            elif not solutions:
                counts['charge_zero_but_unsat']+=1
            counts['feasible_offset_vectors']+=bool(solutions)
            counts['valid_joint_assignments']+=solutions
        out.append(counts)
    save('tight_capacity_charge.json',out)
    return out


if __name__=='__main__':
    examples()
    e=exhaustive_minimality()
    s=sample_suite()
    c=csp_suite()
    q=charge_suite()
    print(json.dumps(safe_json({'exhaustive':e,'sample_systems':sum(r['tested_pair_systems'] for r in s),
                               'csp_assignments':sum(r['assignments_checked'] for r in c),'charge':q}),indent=2))
