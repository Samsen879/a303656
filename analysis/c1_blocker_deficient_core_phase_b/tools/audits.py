#!/usr/bin/env python3
import json
from pathlib import Path
from itertools import product
from graphs import (subsets,neighborhood,capacity,maximum_matching,hall_data,
    minimal_deficient,assert_minimal_structure,terminal_frontiers,route_forest,dag_min_cut)
from arithmetic import row,isprime

def hall_audit():
    right=(3,5,7)
    modes={'paired':{p:(p-1)//2 for p in right},'single':{p:p-1 for p in right}}
    report={}
    for name,caps in modes.items():
        casecount=0; minimal={str(n):0 for n in range(1,6)}
        for n in range(1,6):
            for masks in product(range(8),repeat=n):
                adj={q:{p for i,p in enumerate(right) if masks[q]>>i&1} for q in range(n)}
                d=hall_data(adj,caps)
                match=maximum_matching(adj,caps)
                assert len(match)==d['rank']
                for S in (d['canonical_smallest'],d['canonical_largest']):
                    assert len(S)-capacity(neighborhood(S,adj),caps)==d['max_deficiency']
                if minimal_deficient(adj,caps):
                    minimal[str(n)]+=1
                    assert_minimal_structure(adj,caps)
                casecount+=1
        report[name]=dict(graphs=casecount,minimal_whole_left_cores_by_size=minimal,
                          mismatches=0)
    report['total_graph_capacity_cases']=sum(v['graphs'] for v in report.values())
    return report

def route_audit():
    vertices=(3,7,11,23,31,67)
    supports={3:set(),7:{3},11:{5},23:{11},31:{3},67:{11}}
    for p in vertices:
        assert set(row(p)['odd_order_factors'])==supports[p]
    all_labels=set(vertices)|set().union(*supports.values())
    out={}
    for name,div in [('paired',2),('single',1)]:
        caps={p:(p-1)//div for p in all_labels}
        cases=0;passed=0
        for P in subsets(vertices):
            front=terminal_frontiers(P,supports)
            for p in P:
                assert capacity(front[p],caps)<=capacity(supports[p],caps)<caps[p]
            for T in subsets(sorted(P)):
                adj={q:front[q] for q in T}
                match=maximum_matching(adj,caps)
                cut,_=dag_min_cut(P,T,supports,caps)
                assert len(match)==cut
                if len(match)==len(T):
                    route_forest(P,T,supports,caps,match)
                    passed+=1
                cases+=1
        out[name]=dict(cases=cases,passing=passed,mismatches=0)
    # Coalescing is strictly stronger than conserved unit-demand flow.
    P={11,23,67};T=P
    caps={p:(p-1)//2 for p in all_labels}
    front=terminal_frontiers(P,supports)
    match=maximum_matching({q:front[q] for q in T},caps)
    forest={11:5,23:11,67:11}
    assert len(match)==2 and all(forest[q] in supports[q] for q in T)
    assert sum(v==5 for v in forest.values())<=caps[5]
    assert sum(v==11 for v in forest.values())<=caps[11]
    out['coalescing_counterexample']=dict(P=sorted(P),mandatory_targets=sorted(T),
        target_type='actual regular rows treated as mandatory guard targets, not nonregular Q',
        maximum_terminal_matching_size=len(match),valid_forest=forest,
        disproves='necessity of terminal Hall for all guard-forest strategies only')
    return out

def signatures():
    out={}
    for m in range(1,101):
        ps=[p for p in range(5,m+1) if p%4==1 and isprime(p)]
        sig=[]
        def rec(i,total,chosen):
            if total==m-1:
                sig.append(chosen);return
            if total>m-1:return
            for j in range(i,len(ps)):
                p=ps[j]
                if total+p-1<=m-1:
                    rec(j+1,total+p-1,chosen+[p])
        rec(0,0,[])
        if sig:out[str(m)]=sig
    return dict(max_core_size=100,interpretation='possible frontier capacity signatures only',
                signatures=out)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,fn in [('hall_audit',hall_audit),('route_audit',route_audit),('terminal_signatures',signatures)]:
        data=fn()
        (args.output_dir/(name+'.json')).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        print(name, 'PASS',data if name!='terminal_signatures' else data['signatures'])
