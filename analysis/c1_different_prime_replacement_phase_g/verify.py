#!/usr/bin/env python3
"""Verify the finite STRUCTURAL reduct, not existence of its formal root primes.

Standard library only. No network, factoring search, repository import, or
arithmetic verification of a formal endpoint occurs here. Run:
  python3 -B verify.py
  python3 -B verify.py --out /tmp/phase_g_results.json --check-hashes
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
class CheckError(Exception):
    pass

def require(test: bool, message: str) -> None:
    if not test:
        raise CheckError(message)

def product_factors(f: dict[str, int]) -> int:
    require(all(int(p) >= 2 and isinstance(e, int) and e > 0 for p, e in f.items()), 'bad factorization')
    return math.prod(int(p) ** e for p, e in f.items())

def crt(equations: list[tuple[int, int]]) -> tuple[int, int]:
    a, m = 0, 1
    for b, n in equations:
        require(n > 0 and math.gcd(m, n) == 1, 'CRT moduli not coprime')
        a += m * ((b - a) * pow(m, -1, n) % n)
        m *= n
        a %= m
    return a, m

def verify_arithmetic(data: dict[str, Any]) -> dict[str, Any]:
    nodes = data['prime_certificates']
    done: set[int] = set()
    visiting: set[int] = set()
    def prime(n: int) -> None:
        if n in done:
            return
        require(n not in visiting and str(n) in nodes, 'cyclic/missing primality certificate')
        visiting.add(n)
        c = nodes[str(n)]
        require(c['n'] == n, 'primality label mismatch')
        if n == 2:
            require(c.get('base_case') is True, 'missing base case')
        else:
            require(n > 2 and n % 2 == 1 and not c.get('base_case', False), 'invalid prime base case')
            f = c['n_minus_one_factorization']
            require(product_factors(f) == n - 1, 'incomplete n-1 product')
            for l in f:
                require(int(l) < n, 'nondecreasing prime certificate')
                prime(int(l))
            a = c['lucas_witness']
            require(1 < a < n and pow(a, n - 1, n) == 1, 'Lucas full power failed')
            for l in f:
                require(math.gcd(pow(a, (n - 1)//int(l), n) - 1, n) == 1, 'Lucas order drop failed')
        visiting.remove(n)
        done.add(n)
    for n in nodes:
        prime(int(n))
    orders = data['order_certificates']
    for label, c in orders.items():
        p, w, f = c['p'], c['w'], c['w_factorization']
        require(str(p) == label and p in done and p != 5, 'bad order label')
        require(product_factors(f) == w and (p-1) % w == 0, 'bad order product')
        for l in f:
            prime(int(l))
        require(pow(5, w, p) == c['full_power_mod_p'] == 1, 'base-5 full power failed')
        for l in f:
            v = pow(5, w//int(l), p)
            require(v == c['order_drop_mod_p'][l] and v != 1, 'base-5 order drop failed')
        v = pow(5, w, p*p)
        require(v == c['lift_mod_p2'] and v % p == 1, 'lift receipt mismatch')
        require(c['regular'] is True and v != 1, 'actual label is not certified regular')
    return {'prime_certificate_nodes': len(done), 'actual_order_certificates': len(orders)}

def factors(row: dict[str, Any]) -> dict[int, int]:
    return {int(p): e for p, e in row['w_factorization'].items()}

def guard(row: dict[str, Any]) -> dict[int, tuple[int, int]]:
    a = row.get('a', row.get('A1_rigid_log', 0))
    return {p: (e, a % (p**e)) for p, e in factors(row).items()}

def intersect(a: dict[int, tuple[int, int]], b: dict[int, tuple[int, int]]) -> dict[int, tuple[int, int]]:
    out = dict(a)
    for p, (e, r) in b.items():
        if p in out:
            f, s = out[p]
            require((r-s) % (p**min(e, f)) == 0, 'incompatible fixed guards')
            if e > f:
                out[p] = (e, r)
        else:
            out[p] = (e, r)
    return out

def json_guard(g: dict[int, tuple[int, int]]) -> dict[str, list[int]]:
    return {str(p): [e, r] for p, (e, r) in sorted(g.items())}

def structural(model: dict[str, Any], arithmetic: dict[str, Any]) -> dict[str, Any]:
    rows, basins = model['rows'], model['basins']
    ar = arithmetic['order_certificates']
    roots = model['roots']
    require(len(roots) == len(set(roots)) == len(basins) == 7, 'not seven distinct origins')
    require(set(roots) == {b['root'] for b in basins}, 'root/basin mismatch')
    require(model['cost'] == 'number of proper regular admitted descendants', 'cost changed')
    require(model['stopping_threshold'] == 2, 'stopping threshold changed')
    require(model['global_state']['frozen'] is True and model['global_state']['same_state_for_all_d_and_both_anchors'] is True, 'global state not frozen')
    require(model['global_state']['separator_modulus'] == 54, 'separator changed')
    require(model['global_state']['selected_parity'] == 0 and model['global_state']['c_star'] == 1, 'boundary changed')
    require(model['special_rows']['2'] == {'K':2,'r_mod_4':1,'A0_rejected':True,'A1_rejected':False}, 'two-adic BOTH guard changed')
    require(model['special_rows']['3'] == {'K':2,'E':[1],'r_mod_9':2}, 'row3 state changed')
    all_regular: set[int] = set()
    all_row_ids: set[str] = set()
    provenance, shadows, capacities = [], {}, {}
    endpoint_paths: dict[str, list[str]] = {}
    for b in basins:
        name, root, R = b['id'], b['root'], b['regular_primes']
        require(R == sorted(set(R)) and R and not (set(R) & all_regular), 'basins overlap or repeat a regular label')
        all_regular.update(R)
        rids = {'p'+str(p) for p in R} | {root}
        require(not (rids & all_row_ids), 'row reused across basins')
        all_row_ids |= rids
        require(b['state_cost'] == len(R) and b['full_basin_vertex_count'] == len(R)+1, 'incorrect union cost')
        require(b['head'] in R and b['depth'] in (1,2,3), 'bad head/depth')
        a = b['a']
        require(a % 2 == 0 and a % (3**b['depth']) == b['leaf'], 'basin state outside its fixed leaf')
        require(b['a_modulus'] == 2*3**b['depth']*math.prod(R) and 0 <= a < b['a_modulus'], 'bad CRT construction constant')
        H = {}
        gateway = []
        for p in R:
            row = rows['p'+str(p)]
            require(row['kind'] == 'ACTUAL_REGULAR_ORIGINAL_ROW' and row['p'] == p and p % 4 == 3, 'actual original helper type failed')
            require(str(p) in ar and row['w'] == ar[str(p)]['w'] and row['w_factorization'] == ar[str(p)]['w_factorization'], 'actual arithmetic data changed')
            require(row['a'] == a and row['K'] == 2 and row['E'] == [1] and row['center_own_digit'] == 0, 'fresh local state or accepted local zero')
            require(a % p == 0 and row['r_mod_p2'] == (3+pow(5,a,p*p)) % (p*p), 'residue/center identity failed')
            fs = factors(row)
            require(all(t < p for t in fs), 'order DAG not strictly descending')
            H[p] = {t for t in fs if t > 3}
            require(H[p] <= set(R), 'missing actual order-support vertex')
            if {t for t in fs if t % 2} == {3}:
                gateway.append(p)
        maxima = sorted(set(R)-set().union(*H.values()))
        require(b['maximal_generators'] == maxima, 'wrong maximal-generator antichain')
        require(gateway == [b['head']], 'wrong basal gateway')
        q = rows[root]
        require(q['kind'] == 'FORMAL_ORIGINAL_NONREGULAR_ORIGIN' and q['actual_prime_instantiated'] is False and q['integer_order_label_only'] is True, 'formal endpoint promoted to actual prime/macro')
        require(q['w'] == math.prod(maxima) and q['w_factorization'] == {str(p):1 for p in maxima}, 'formal root order does not generate the exact state')
        require(q['K'] == 2 and q['E'] == [1] and q['declared_s_lower_bound'] == 2 and q['A1_rigid_log'] == 0, 'invalid formal rigid state')
        require(q['fixed_state_term'] == 'r_Q = Q + 4 (mod Q^2)', 'formal root received a fresh local residue')
        require(q['required_if_instantiated']['Q_mod_4'] == 3 and q['required_if_instantiated']['Q_greater_than'] >= max(2000000000,q['w'],max(R)), 'missing endpoint admission/size obligation')
        require(a % q['w'] == 0, 'formal root log not aligned with common construction')
        closure = set(maxima)
        old = None
        while old != closure:
            old = set(closure)
            closure |= set().union(*(H[p] for p in list(closure)))
        require(closure == set(R), 'root closure not exactly R')
        all_odd = True
        for rid in rids:
            row = rows[rid]
            require(row['basin'] == name and product_factors(row['w_factorization']) == row['w'], 'row identity/order mismatch')
            fs = factors(row)
            require(fs.get(2,0) <= 1 and fs.get(3,0) <= b['depth'] and all(e==1 for p,e in fs.items() if p>3), 'normal-form order depth violation')
            all_odd &= row['w'] % 2 == 1
        require(all_odd == b['O31_all_odd'], 'incorrect all-odd annotation')
        if name == 'O31':
            require(b['head'] == 31 and all_odd, 'O31 violated')
        # Exact descending linear witness; one rigid parent at every private coordinate.
        current = guard(q)
        support = {root}
        chosen = {}
        steps = []
        for p in sorted(R, reverse=True):
            require(current.get(p) == (1,0), 'missing centered depth-one incoming cylinder')
            eligible = [rid for rid in support if guard(rows[rid]).get(p) == (1,0)]
            require(bool(eligible), 'no original exact provider for omitted center')
            provider = min(eligible, key=lambda rid: rows[rid].get('p', 10**100))
            chosen['p'+str(p)] = provider
            before = json_guard(current)
            del current[p]
            current = intersect(current, guard(rows['p'+str(p)]))
            steps.append({'coordinate':p,'original_exact_provider':provider,'dynamic_original_row':'p'+str(p),'support_before':sorted(support),'incoming_guard':before,'outgoing_guard':json_guard(current),'omitted_center_digit':0,'accepted_shell_valuation':1,'charged_origin':root})
            support.add('p'+str(p))
        expected = {3:(b['depth'],b['leaf'])}
        if not all_odd:
            expected[2] = (1,0)
        require(current == expected and support == rids, 'linear contraction did not yield the exact leaf/support')
        for rid in chosen:
            path, at = [rid], rid
            while at != root:
                require(at in chosen, 'ancestry did not reach original rigid origin')
                nxt = chosen[at]
                require(rows[at]['p'] in factors(rows[nxt]), 'ancestry edge not certified by an original order')
                require(nxt == root or rows[nxt]['p'] > rows[at]['p'], 'ancestry is not increasing')
                path.append(nxt); at = nxt
                require(len(path) <= len(R)+1, 'ancestry cycle')
            endpoint_paths[rid] = path
        sh = set()
        for rid in rids:
            g = guard(rows[rid])
            if 3 in g:
                e,r = g[3]
                require(b['leaf'] % (3**e) == r, 'shadow does not contain final leaf')
                sh.add((e,r))
        require(sh and max(e for e,r in sh) == b['depth'], 'missing exact head shadow')
        require(all((r-s) % (3**min(e,f)) == 0 for e,r in sh for f,s in sh), 'shadows not nested')
        capacities[root] = 1
        shadows[root] = [[e,r] for e,r in sorted(sh)]
        provenance.append({'basin':name,'origin':root,'steps':steps,'final_original_support':sorted(support),'final_guard':json_guard(current),'final_private_provider':'p'+str(b['head'])})
    require(set(rows) == all_row_ids, 'unused/external rows silently inserted into the core')
    require(sorted(b['depth'] for b in basins) == [1,1,2,2,3,3,3], 'not pure-3 (2,2,3)')
    require({b['head'] for b in basins if b['depth']==1} == {7,31} and {b['head'] for b in basins if b['depth']==2} == {19,5167}, 'mandatory heads changed')
    require(len({b['head'] for b in basins if b['depth']==3}) == 3 and all(b['head'] in {163,271,487,4159,31051,16018507} for b in basins if b['depth']==3), 'depth-three heads invalid')
    require(all(sum(z % 3**b['depth'] == b['leaf'] for b in basins)==1 for z in range(27)), 'ternary leaves do not partition')
    L = 54*math.prod(all_regular)
    induced = math.lcm(2, *(r['w']*(r['p'] if r['kind']=='ACTUAL_REGULAR_ORIGINAL_ROW' else 1) for r in rows.values()))
    require(induced == L == model['global_state']['original_abstract_period_L'] == model['global_state']['original_abstract_U'], 'original abstract ambient mismatch')
    require(model['global_state']['retained_under_deletion'] is True, 'ambient not retained')
    eqs = [(1,4),(2,9)]+[(rows['p'+str(p)]['r_mod_p2'],p*p) for p in sorted(all_regular)]
    c,m = crt(eqs)
    require(c == model['global_state']['actual_regular_subledger_CRT_residue'] and m == model['global_state']['actual_regular_subledger_CRT_modulus'], 'actual subledger is not one CRT state')
    # Reconciled exact B7 state registry, not a numerical factorization of Z_R.
    universe = model['B7_registry']['certified_regular_vertex_universe']
    require(universe == sorted(set(universe)) and set(universe) == {7,43,127,379,7603,19531,519499,6717031}, 'registry universe changed')
    H7 = {p:{int(l) for l in ar[str(p)]['w_factorization'] if int(l)>3} for p in universe}
    states, used_indices = [], set()
    for mask in range(1,1<<len(universe)):
        S = {p for i,p in enumerate(universe) if mask>>i&1}
        if 7 not in S or any(not H7[p] <= S for p in S):
            continue
        A = S-set().union(*(H7[p] for p in S))
        optional = sorted(S-A)
        J = []
        for bits in range(1<<len(optional)):
            n = math.prod(A)*math.prod(p for i,p in enumerate(optional) if bits>>i&1)
            J += [delta*n for delta in (1,2,3,6)]
        J.sort()
        require(len(J) == len(set(J)) == 4*2**(len(S)-len(A)), 'incorrect J(R) count')
        require(not (set(J)&used_indices), 'different exact states share an index')
        used_indices |= set(J)
        states.append({'R':sorted(S),'A':sorted(A),'cost':len(S),'J':J})
    states.sort(key=lambda s:(s['cost'],s['R']))
    b7 = [b for b in basins if b['head']==7]
    require(len(b7)==1, 'more than one B7 origin')
    b = b7[0]
    require(model['B7_registry']['actual_ledger_B7_state'] == b['regular_primes'], 'B7 state identity altered')
    marks = model['B7_registry']['formal_hit_relation']
    require(len(marks)==1, 'additional square-hit source invented')
    mark = marks[0]
    require(mark == {'origin':b['root'],'exact_state':b['regular_primes'],'exact_order':rows[b['root']]['w'],'multiplicity':2}, 'mark migrated away from its exact state')
    matching = [s for s in states if s['R']==mark['exact_state']]
    require(len(matching)==1 and mark['exact_order'] in matching[0]['J'], 'marked root is not in its exact J stratum')
    cheap = [s for s in states if s['cost'] < b['state_cost']]
    require(b['state_cost']>2 and cheap, 'antecedent not above the stopping class')
    require(all(7 not in x['regular_primes'] for x in basins if x['id']!=b['id']), 'another original root could be B7')
    z7_factors = [29,43,127,379,449,7603,19531,519499]
    z7 = (5**42-1)//((5**6-1)*7)
    require(z7 == math.prod(z7_factors) and len(z7_factors)==len(set(z7_factors)), 'Z_{7} complete product mismatch')
    require(all(str(p) in arithmetic['prime_certificates'] for p in z7_factors), 'Z7 prime certificate missing')
    # Finite primitive-divisibility reduct: every represented prime atom is
    # assigned to at most one exact stratum, including valuation-one atoms.
    # This does NOT evaluate the full integer Z_R or assert completeness of
    # its prime-factor inventory.
    incidence = []
    for label, certificate in sorted(ar.items(), key=lambda item:int(item[0])):
        matched = [st for st in states if certificate['w'] in st['J']]
        require(len(matched) <= 1, 'primitive atom occurs in two exact strata')
        if matched:
            incidence.append({'atom':'actual_prime_'+label,'p':int(label),
                              'exact_order':certificate['w'],
                              'exact_state':matched[0]['R'],'valuation':1,
                              'scope':'actual regular factor, not full factorization'})
    incidence.append({'atom':b['root'],'exact_order':mark['exact_order'],
                      'exact_state':mark['exact_state'],'valuation':2,
                      'scope':'FORMAL mark only; arithmetic realization unverified'})
    require(len({x['atom'] for x in incidence})==len(incidence),
            'distinct-state coprimality guard violated by a represented atom')
    return {'represented_primitive_incidence':incidence,'provenance':provenance,'center_ancestry_paths':endpoint_paths,'fixed_3_shadows':shadows,'capacities':capacities,'B7_state_registry':states,'B7_registry_index_count':len(used_indices),'cheaper_registry_states':len(cheap),'B7_exact_order':rows[b['root']]['w'],'B7_exact_state':b['regular_primes'],'B7_J_count':len(matching[0]['J']),'original_L':L,'regular_primes':sorted(all_regular)}

def row_fatal(row: dict[str, Any], z: int, digits: dict[int,int]) -> bool:
    for p,(e,a) in guard(row).items():
        x = z % (p**e) if p in (2,3) else digits[p]
        if x != a:
            return False
    if row['kind']=='FORMAL_ORIGINAL_NONREGULAR_ORIGIN':
        return True  # Abstract rigid-atom axiom, NOT a base-5 endpoint check.
    return digits[row['p']] != 0

def row3(z: int) -> bool:
    v = (2-3-pow(5,z,9)) % 9
    return v != 0 and v % 3 == 0

def basin_values(model: dict[str, Any], b: dict[str, Any], z: int, disabled: str|None=None):
    rows=model['rows']; R=b['regular_primes']
    for mask in range(1<<len(R)):
        digits={p:(mask>>i)&1 for i,p in enumerate(R)}
        ids=['p'+str(p) for p in R]+[b['root']]
        value=any(rid != disabled and row_fatal(rows[rid],z,digits) for rid in ids)
        yield mask,digits,value

def finite_checks(model: dict[str, Any], structural_data: dict[str, Any]) -> dict[str, Any]:
    profiles={b['id']:[] for b in model['basins']}
    kernel_comparisons=0; actual_comparisons=0; abstract_cells=0
    # Check the exact 0/nonzero quotient against actual modular rows at one
    # representative of each class. The proof of class invariance is in MODEL.md.
    for b in model['basins']:
        R=b['regular_primes']
        for z in range(54):
            vals=[]
            for _,digits,value in basin_values(model,b,z):
                abstract_cells += 1; vals.append(value)
                d,_=crt([(z,54)]+[(digits[p],p) for p in R])
                for p in R:
                    r=model['rows']['p'+str(p)]
                    local=(r['r_mod_p2']-3-pow(5,d,p*p)) % (p*p)
                    actual=(local != 0 and local % p == 0)
                    require(actual == row_fatal(r,z,digits), 'actual modular row and compressed kernel disagree')
                    actual_comparisons += 1
                # For the formal root this verifies the declared congruence
                # guard only; no Q or Q^2 modular arithmetic is performed.
                r=model['rows'][b['root']]
                require(row_fatal(r,z,digits)==(d % r['w']==0), 'formal exact-log kernel mismatch')
                kernel_comparisons += 1
            whole=all(vals)
            expected=(z % 3**b['depth']==b['leaf'] and (b['O31_all_odd'] or z%2==0))
            require(whole==expected, 'whole-profile/parity-persistence mismatch')
            if whole: profiles[b['id']].append(z)
    possible_masks={}
    for z in range(54):
        possible={int(row3(z))}
        require(row3(z)==(z%2==1 and z%3!=0), 'row3 actual state mismatch')
        for b in model['basins']:
            v={int(x[2]) for x in basin_values(model,b,z)}
            possible={a|c for a in possible for c in v}
        require(possible=={1}, 'not complete at anchor 1 on one global state')
        # Two-adic row gives A0 independently of the unknown formal A0 root masks.
        masks={1|(2*x) for x in possible}
        require(masks=={3}, 'BOTH was weakened to EITHER')
        possible_masks[str(z)]=sorted(masks)
    # Exact row-deletion witnesses with the ORIGINAL induced ambient retained.
    deletion=[]
    for deleted in sorted(model['rows']):
        witness=None
        for z in range(0,54,2):
            digits={}; block_masks={}; possible=True
            for b in model['basins']:
                found=next((v for v in basin_values(model,b,z,deleted) if not v[2]),None)
                if found is None:
                    possible=False;break
                mask,ds,_=found;digits.update(ds);block_masks[b['id']]=mask
            if possible and not row3(z):
                require(not any(rid!=deleted and row_fatal(r,z,digits) for rid,r in model['rows'].items()), 'deletion witness not simultaneous')
                d,L=crt([(z,54)]+[(digits[p],p) for p in structural_data['regular_primes']])
                require(L==structural_data['original_L'], 'ambient recomputed after deletion')
                for rid,r in model['rows'].items():
                    if rid==deleted or r['kind']!='ACTUAL_REGULAR_ORIGINAL_ROW':continue
                    p=r['p'];v=(r['r_mod_p2']-3-pow(5,d,p*p))%(p*p)
                    require(not(v!=0 and v%p==0), 'actual helper blocks alleged deletion escape')
                witness={'deleted_original_row':deleted,'separator':z,'private_class_masks':block_masks,'d_mod_original_L':d,'original_L':L,'anchor_1_escape_in_abstract_model':True}
                break
        require(witness is not None, 'a core row was redundant')
        deletion.append(witness)
    cumulative=[]; covered=set()
    for b in model['basins']:
        covered|={z for z in profiles[b['id']] if z%2==0}
        cumulative.append(len(covered))
    require(cumulative==[9,18,21,24,25,26,27], 'selected-parity frontier mismatch')
    return {'basin_whole_profiles_mod54':profiles,'possible_full_typed_masks_mod54':possible_masks,'deletion_witnesses':deletion,'actual_regular_row_comparisons':actual_comparisons,'formal_root_guard_comparisons':kernel_comparisons,'abstract_private_class_cases':abstract_cells,'selected_parity_cumulative_counts':cumulative}

def mutation_tests(model: dict[str, Any], arithmetic: dict[str, Any]) -> list[str]:
    tests=[]
    def reject(name: str, edit, edit_arithmetic=False):
        m,a=copy.deepcopy(model),copy.deepcopy(arithmetic)
        edit(a if edit_arithmetic else m)
        try:
            verify_arithmetic(a);structural(m,a)
        except (CheckError,KeyError,ValueError):
            tests.append(name);return
        raise CheckError('negative control was incorrectly accepted: '+name)
    reject('same-q mark duplicated into cheaper exact state', lambda m:m['B7_registry']['formal_hit_relation'].append({'origin':'Q_B7','exact_state':[7,43],'exact_order':43,'multiplicity':2}))
    reject('same-q exact-state migration', lambda m:m['B7_registry']['formal_hit_relation'][0].update(exact_state=[7,43]))
    reject('root support silently shortened', lambda m:m['rows']['Q_B7'].update(w=43,w_factorization={'43':1}))
    reject('O31 changed to an even order', lambda m:m['rows']['Q_O31'].update(w=2*m['rows']['Q_O31']['w'],w_factorization={'2':1,**m['rows']['Q_O31']['w_factorization']}))
    reject('cross-basin helper reuse', lambda m:m['basins'][2]['regular_primes'].append(7))
    reject('local-zero sentinel accepted', lambda m:m['rows']['p43'].update(E=[1,2]))
    reject('fresh row state inside B7 basin', lambda m:m['rows']['p43'].update(a=m['rows']['p43']['a']+1))
    reject('derived macro substituted for original origin', lambda m:m['rows']['Q_B7'].update(kind='DERIVED_MACRO'))
    reject('duplicate original origin', lambda m:m['roots'].__setitem__(1,m['roots'][0]))
    reject('uncertified lifting exponent', lambda a:a['order_certificates']['127'].update(lift_mod_p2=1),True)
    reject('BOTH weakened by dropping A0 obstruction', lambda m:m['special_rows']['2'].update(A0_rejected=False))
    reject('a formal root promoted to an actual prime', lambda m:m['rows']['Q_B7'].update(actual_prime_instantiated=True))
    return tests

def manifest_check() -> int:
    manifest=HERE/'SHA256SUMS.txt'
    require(manifest.is_file(),'missing checksum manifest')
    seen=set()
    for line in manifest.read_text().splitlines():
        h,name=line.split('  ',1)
        require(name not in seen and not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe or duplicate manifest path')
        seen.add(name)
        p=HERE/name
        require(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==h,'checksum mismatch: '+name)
    actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*')
            if p.is_file() and p.name!='SHA256SUMS.txt'}
    require(seen==actual,'manifest does not cover exactly the payload files')
    return len(seen)

def run() -> tuple[dict[str, Any],dict[str, Any]]:
    model=json.loads((HERE/'model.json').read_text())
    arithmetic=json.loads((HERE/'arithmetic_certificates.json').read_text())
    ac=verify_arithmetic(arithmetic)
    st=structural(model,arithmetic)
    finite=finite_checks(model,st)
    neg=mutation_tests(model,arithmetic)
    data={**st,**finite,'negative_controls_rejected':neg}
    results={'schema':'a303656.phase-g.results.v1','verification':'PASS','main_sha':model['source_commit'],'main_tree':'57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06','THEOREM':'NOT PROVED','THEOREM_scope':'requested strict different-prime SQD; auxiliary proofs are in PROOFS.md','auxiliary_theorems':['unique in-certificate B7 original origin','no different original root can hit any other B7 exact state','conditional external-root transplantation with a newly constructed ONE global state'], 'ABSTRACT_COUNTERMODEL':'FOUND','abstract_scope':'explicit finite structural/order/provenance/typed-mask reduct; symbolic original endpoints; not full base-5 arithmetic','ACTUAL_ARITHMETIC_COUNTEREXAMPLE':'NOT FOUND','ROUTE_STATUS':'DEAD AT CURRENT AUTHORITY','route_scope':'deducing a different-prime replacement solely from current structural constraints; not an arithmetic nonexistence theorem','GITHUB_WRITES_PERFORMED':'NONE','original_formal_nonregular_roots':7,'actual_regular_core_rows':14,'actual_special_odd_row_3':1,'core_rows_deletion_indispensable':len(finite['deletion_witnesses']),'B7_cost':4,'B7_basin_vertices':5,'B7_maximal_generators':[6717031],'B7_exact_index':st['B7_exact_order'],'B7_exact_J_count':st['B7_J_count'],'B7_registry_states':len(st['B7_state_registry']),'B7_registry_indices':st['B7_registry_index_count'],'cheaper_registry_states':st['cheaper_registry_states'],'other_original_B7_roots':0,'same_origin_state_migration':False,'formal_cheaper_B7_root_witnesses':0,'O31_compatible':True,'all_seven_capacity_values':list(st['capacities'].values()),'simultaneous_obligations':7,'simultaneous_capacity':7,'capacity_deficit':0,'one_fixed_state_all_separator_cells':True,'BOTH_not_merely_EITHER':True,'actual_endpoint_prime_checks':0,'arithmetic_certificate_checks':ac,'actual_regular_row_comparisons':finite['actual_regular_row_comparisons'],'formal_root_guard_comparisons':finite['formal_root_guard_comparisons'],'abstract_private_class_cases':finite['abstract_private_class_cases'],'separator_cells':54,'negative_controls_rejected':len(neg),'arithmetic_SQD':'UNRESOLVED','B7_EMPTY':'NO','EXACTLY_SEVEN':'NOT KILLED','N_GE_8':'NOT PROVED','A303656':'UNRESOLVED','repository_native_tests_replayed':False,'all_files_in_required_directories_read':False}
    return results,data

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,help='optional replay results destination outside the bundle')
    parser.add_argument('--write',action='store_true',help='producer-only: write fresh frozen data/results')
    parser.add_argument('--check-hashes',action='store_true')
    args=parser.parse_args()
    try:
        if args.check_hashes:
            count=manifest_check()
            print('SHA256 entries verified:',count)
        results,data=run()
        def text(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
        if args.write:
            (HERE/'results.json').write_text(text(results))
            (HERE/'finite_model_data.json').write_text(text(data))
        else:
            require(json.loads((HERE/'results.json').read_text())==results,'frozen results mismatch')
            require(json.loads((HERE/'finite_model_data.json').read_text())==data,'frozen finite-model data mismatch')
        if args.out:
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(text(results))
        print(text(results))
        return 0
    except (CheckError,OSError,ValueError,KeyError) as e:
        print('FAIL:',e)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
