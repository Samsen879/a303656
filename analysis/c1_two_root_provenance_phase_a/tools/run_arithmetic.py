#!/usr/bin/env python3
"""Independent actual-row replay and exact paired-mask quotient audit.

This is NOT a prime scan and imports no repository implementation.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
from math import prod, lcm
import json, hashlib, os, sys
from residue_states import power_cycle, direct_mask, trie_quotient
from contraction import contract_provenance

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('A303656_OUTPUT_DIR', ROOT / 'results'))
CATALOG_OUT = Path(os.environ.get('A303656_CATALOG_DIR', ROOT / 'catalogs'))
OUT.mkdir(parents=True, exist_ok=True)
CATALOG_OUT.mkdir(parents=True, exist_ok=True)


def write(name, value):
    (OUT / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def literal_signature(p, powers, r):
    """K=2 full pair signature, with precomputed independent dictionaries."""
    w = next((j for j in range(1, len(powers)) if powers[j] % p == 1), len(powers))
    base_logs = {v % p: j for j, v in enumerate(powers[:w])}
    full_logs = {v: j for j, v in enumerate(powers)}
    sig = []
    for shift in (1, 3):
        b = base_logs.get((r - shift) % p)
        if b is None:
            sig.append(None)
        elif len(powers) == w:
            sig.append(None if (r - shift) % (p*p) in full_logs else ('R', b))
        else:
            sig.append(('D', b, full_logs[(r-shift) % (p*p)]))
    return tuple(sig)


def run_quotients():
    tests = []
    for p, k in [(3,2),(3,3),(7,2),(7,3),(11,2),(19,2)]:
        pw = power_cycle(p, k)
        acc = frozenset([1])
        states, stats = trie_quotient(p,k,acc,pw)
        brute = Counter(direct_mask(p,k,acc,pw,r) for r in range(p**k))
        assert brute == {s.mask:s.residue_count for s in states}
        for s in states:
            assert direct_mask(p,k,acc,pw,s.representative) == s.mask
        stats.update(prime=p, precision=k, mismatches=0, brute_force_residues=p**k)
        tests.append(stats)
    records = []
    catalog_records = {}
    for p in (67,20771):
        pw = power_cycle(p,2)
        period = len(pw)
        w = next((j for j in range(1,period) if pw[j] % p == 1),period)
        base_logs = {v % p:j for j,v in enumerate(pw[:w])}
        full_logs = {v:j for j,v in enumerate(pw)}
        def signature(r):
            sig = []
            for shift in (1,3):
                b=base_logs.get((r-shift)%p)
                if b is None:
                    sig.append(None)
                elif period==w:
                    sig.append(None if (r-shift)%(p*p) in full_logs else ('R',b))
                else:
                    sig.append(('D',b,full_logs[(r-shift)%(p*p)]))
            return tuple(sig)
        states, stats = trie_quotient(p,2,frozenset([1]),pw)
        # Method B, independent of the trie: literal p^2 residues for 67;
        # for 20771 classify each low digit by its at most two zero lifts.
        independently = Counter()
        if p==67:
            for r in range(p*p):
                independently[signature(r)] += 1
            independent_method='all 4489 residues by order/log signature'
        else:
            for low in range(p):
                exceptional=set()
                for shift in (1,3):
                    b=base_logs.get((low-shift)%p)
                    if b is not None:
                        zero=(shift+pw[b])%(p*p)
                        assert zero%p==low
                        exceptional.add((zero-low)//p)
                for high in exceptional:
                    independently[signature(low+p*high)] += 1
                normal=next(h for h in range(p) if h not in exceptional)
                independently[signature(low+p*normal)] += p-len(exceptional)
            independent_method='20771 low digits, exact exceptional-zero-lift partition'
        trie_signatures=Counter()
        independent_masks={}
        catalog=[]
        for state in states:
            sig=signature(state.representative)
            trie_signatures[sig]+=state.residue_count
            # Independently reconstruct every state mask from the signature.
            mask=0
            for c,s in enumerate(sig):
                if s is None:
                    continue
                if s[0]=='R':
                    mask |= 1 << (c*period+s[1])
                else:
                    for d in range(s[1],period,w):
                        if d!=s[2]:
                            mask |= 1 << (c*period+d)
            assert mask==state.mask
            assert sig not in independent_masks  # no hidden duplicate quotient
            independent_masks[sig]=mask
            catalog.append({'signature':sig,'representative':state.representative,
                            'residue_count':state.residue_count,
                            'anchor_sizes':[]})
            catalog[-1]['anchor_sizes']=[(mask&((1<<period)-1)).bit_count(),(mask>>period).bit_count()]
        assert independently==trie_signatures
        assert len(independently)==len(states)
        both=[s for s in independently if all(v is not None for v in s)]
        singles=[s for s in independently if sum(v is not None for v in s)==1]
        assert independently[(None,None)]>0
        # Inclusion dominance has a particularly simple exact form here:
        # rigid singleton states may be included in a genuine two-sided state;
        # distinct nonempty regular dynamic masks cannot contain each other.
        if period==w:
            covered_singles=set()
            for s in both:
                covered_singles.add((s[0],None)); covered_singles.add((None,s[1]))
            dominated_single_count=len(set(singles)&covered_singles)
        else:
            dominated_single_count=0
        maximal_states=len(states)-1-dominated_single_count
        stats.update(prime=p,precision=2,base_order=w,independent_method=independent_method,
                     independently_verified_states=len(states),mismatches=0,
                     empty_state_weight=independently[(None,None)],
                     both_active_states=len(both),single_active_states=len(singles),
                     dominated_single_states=dominated_single_count,
                     maximal_states=maximal_states)
        records.append(stats)
        catalog_records[p]=catalog
        path=CATALOG_OUT/f'paired_states_p{p}_K2.json'
        path.write_text(json.dumps(catalog,sort_keys=True,separators=(',',':'))+'\n')
        stats['catalog_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        print('quotient',p,stats,flush=True)
    write('residue_quotient.json',{'small_literal_tests':tests,'actual_rows':records,
         'raw_pair_residue_assignments':prod(r['raw_residues'] for r in records),
         'exact_state_product':prod(r['exact_states'] for r in records),
         'maximal_state_product':prod(r['maximal_states'] for r in records),
         'state_products_are_counts_not_enumerated_searches':True})
    return catalog_records


def arithmetic_replay():
    p,q=67,20771
    pw_p=power_cycle(p,2); pw_q=power_cycle(q,2)
    assert len(pw_p)==1474 and len(pw_q)==10385
    assert pow(5,22,p*p)!=1 and pow(5,10385,q*q)==1
    assert pow(5,10385,q**3)!=1
    U=lcm(len(pw_p),len(pw_q)); M=U//67
    assert U==228470 and M==3410
    logs_p={v:d for d,v in enumerate(pw_p)}
    logs_q={v%q:d for d,v in enumerate(pw_q)}
    outputs=[]
    for rp,rq in [(2,13471),(0,4494)]:
        both_row_truth=[]; anchors=[]; traces=[]; shapes=[]
        centers=[logs_p[(rp-shift)%(p*p)] for shift in (1,3)]
        rigidlogs=[logs_q[(rq-shift)%q] for shift in (1,3)]
        for c,shift in enumerate((1,3)):
            h,b=centers[c],rigidlogs[c]
            fatal=[]; rowcounts=[0,0]; safelist=[]; zero_p=zero_q=0
            fiber_counts=[0]*M
            hashes=hashlib.sha256()
            for d in range(U):
                vp=(rp-shift-pw_p[d%len(pw_p)])%(p*p)
                vq=(rq-shift-pw_q[d%len(pw_q)])%(q*q)
                fp=vp%p==0 and vp!=0
                fq=vq%q==0 and vq!=0
                assert fp == (d%22==h%22 and d%67!=h%67)
                assert fq == (d%10385==b)
                zero_p += vp==0; zero_q += vq==0
                rowcounts[0]+=fp; rowcounts[1]+=fq
                fatal.append((fp,fq))
                if fp or fq:
                    fiber_counts[d%M]+=1
                else:
                    safelist.append(d)
                hashes.update(bytes([int(fp)+2*int(fq)]))
            saturated=[y for y,count in enumerate(fiber_counts) if count==67]
            dims=(2,5,11,31,67)
            sh_p=(1<<(h%2),(1<<5)-1,1<<(h%11),(1<<31)-1,((1<<67)-1)^(1<<(h%67)))
            sh_q=((1<<2)-1,1<<(b%5),(1<<11)-1,1<<(b%31),1<<(b%67))
            result=contract_provenance(dims,[sh_p,sh_q],True)
            assert not result['covered']
            assert len(saturated)==1
            # Check all 67 digits on the selected fiber, especially the local zero.
            y=saturated[0]
            selected=[d for d in range(y,U,M)]
            assert sum(fatal[d][0] for d in selected)==66
            assert sum(fatal[d][1] for d in selected)==1
            zero_d=next(d for d in selected if not fatal[d][0])
            assert (rp-shift-pw_p[zero_d%1474])%(p*p)==0 and fatal[zero_d][1]
            anchors.append({'anchor':c,'dynamic_center_log':h,'rigid_log':b,
                            'row_fatal_counts':rowcounts,'covered_count':U-len(safelist),
                            'safe_count':len(safelist),'first_safe_exponent':safelist[0],
                            'local_zero_counts':[zero_p,zero_q],
                            'saturation_lower_residues':saturated,'root_covered':False,
                            'full_row_mask_sha256':hashes.hexdigest()})
            traces.append(result['stages'])
            both_row_truth.append(fatal)
            shapes.append([sh_p,sh_q])
        for d in range(U):
            assert not(both_row_truth[0][d][0] and both_row_truth[1][d][0])
            assert not(both_row_truth[0][d][1] and both_row_truth[1][d][1])
        holes=[]
        for y in range(M):
            holes.append(sum(not any(both_row_truth[c][d]) for c in (0,1) for d in range(y,U,M)))
        outputs.append({'residues':[rp,rq],'period':U,'lower_period':M,'anchors':anchors,
                        'minimum_joint_fiber_holes':min(holes),
                        'minimizing_lower_count':holes.count(min(holes)),
                        'same_lower_saturation_intersection':[],
                        'contraction_traces':traces,
                        'mismatches':0,'pointwise_row_exclusion_checks':2*U})
    assert outputs[0]['anchors'][0]['saturation_lower_residues']==[2728]
    assert outputs[0]['anchors'][1]['saturation_lower_residues']==[1639]
    assert outputs[1]['anchors'][0]['saturation_lower_residues']==[2431]
    assert outputs[1]['anchors'][1]['saturation_lower_residues']==[106]
    assert [o['minimum_joint_fiber_holes'] for o in outputs]==[67,66]
    write('actual_arithmetic_replay.json',outputs)
    print('replay',[(o['residues'],[a['safe_count'] for a in o['anchors']],o['minimum_joint_fiber_holes']) for o in outputs],flush=True)


def compatibility_join():
    pp=power_cycle(67,2); pq=power_cycle(20771,2)
    dp={v:i for i,v in enumerate(pp)}
    dq={v%20771:i for i,v in enumerate(pq)}
    dynamic=[]; rigid=[]
    for r in range(4489):
        a=dp.get((r-1)%4489); b=dp.get((r-3)%4489)
        if a is not None and b is not None:
            dynamic.append((r,a,b))
    for r in range(20771):
        a=dq.get((r-1)%20771); b=dq.get((r-3)%20771)
        if a is not None and b is not None:
            rigid.append((r,a,b))
    buckets=defaultdict(list)
    for rr,b0,b1 in rigid:
        buckets[(b0%67,b1%67)].append((rr,b0,b1))
    matches=[]
    for rp,a0,a1 in dynamic:
        for rr,b0,b1 in buckets[(a0%67,a1%67)]:
            y0=(a0%22 + 22*((b0-a0)*pow(22,-1,155)%155))%3410
            y1=(a1%22 + 22*((b1-a1)*pow(22,-1,155)%155))%3410
            matches.append((rp,rr,a0,a1,b0,b1,y0,y1))
    # Independent nested-loop join, not using hash buckets.
    nested=[]
    for rp,a0,a1 in dynamic:
        for rr,b0,b1 in rigid:
            if (a0-b0)%67==0 and (a1-b1)%67==0:
                nested.append((rp,rr))
    assert sorted(nested)==sorted((r[0],r[1]) for r in matches)
    assert len(dynamic)==603 and len(rigid)==5192 and len(matches)==693
    assert len(set((r[-2],r[-1]) for r in matches))==692
    assert not any(r[-2]==r[-1] for r in matches)
    assert sum((a-b)%155==0 for _,a,b in rigid)==33
    write('actual_pair_compatibility.json',{
        'dynamic_shared_center_states':len(dynamic),'rigid_shared_class_states':len(rigid),
        'both_anchor_aligned_combinations':len(matches),
        'distinct_ordered_lower_pairs':len(set((r[-2],r[-1]) for r in matches)),
        'same_lower_pairs':0,'rigid_pairs_with_equal_lower_mod155':33,
        'valid_full_residue_systems_with_two_pointwise_fibers':len(matches)*(20771-2),
        'independent_nested_pairs_checked':len(dynamic)*len(rigid),
        'join_mismatches':0,
        'all_matches':matches})
    print('compatibility',len(dynamic),len(rigid),len(matches),flush=True)


if __name__=='__main__':
    run_quotients()
    arithmetic_replay()
    compatibility_join()
