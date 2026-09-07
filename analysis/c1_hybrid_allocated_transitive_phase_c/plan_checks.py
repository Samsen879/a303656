"""Read-only finite plan validation for the frozen arithmetic regression."""
from pathlib import Path
from copy import deepcopy
import json
from arithmetic import factor
from actual_checks import run as actual_run

def validate(rows,targets):
    seen=set()
    for t in targets:
        q,c,p=t['q'],t['c'],t['p']
        if not isinstance(q,int) or str(q) not in rows:raise ValueError('source is not an original row')
        if c not in (0,1) or (q,c) in seen:raise ValueError('invalid or duplicated anchor tag')
        seen.add((q,c));row=rows[str(q)];b=row['logs'][c]
        if b is None:raise ValueError('guard is absent')
        if not isinstance(p,int) or p%2==0 or factor(p)!={p:1} or p>=q:raise ValueError('invalid receiver')
        e=factor(row['w']).get(p,0)
        if e==0 or t['e']!=e or t['a']!=b%p**e:raise ValueError('invalid full-depth projection')
    return True

def receipt(row,c,prefix):
    b=row['logs'][c]
    if b is None:return {'kind':'ABSENT_GUARD'}
    for p,z in sorted(prefix.items()):
        e=factor(row['w']).get(p,0)
        if e and z%p**e!=b%p**e:
            return dict(kind='PERMANENT_CONGRUENCE_FAILURE',p=p,e=e,chosen=z%p**e,required=b%p**e)
    return None

def run():
    data=actual_run();rows=data['rows'];targets=data['targets'];validate(rows,targets)
    # Explicit adversarial mutations: none is treated as a valid actual source edge.
    mutations=[]
    t=deepcopy(targets);t[0]['q']=1429;mutations.append(('phantom relay source',t))
    t=deepcopy(targets);t[0]['q']='macro_1645333507';mutations.append(('macro as original row',t))
    t=deepcopy(targets);t[0]['p']=761;mutations.append(('non-order edge',t))
    t=deepcopy(targets);t[0]['e']=1;mutations.append(('wrong full projection depth',t))
    t=deepcopy(targets);t[0]['a']=2;mutations.append(('changed frozen logarithm',t))
    t=deepcopy(targets);t.append(t[0]);mutations.append(('duplicated tag as new resource',t))
    rejected=[]
    for name,t in mutations:
        try:validate(rows,t)
        except ValueError:rejected.append(name)
        else:raise AssertionError('invalid plan accepted')
    prefix={2:1};trace=[]
    assignments={}
    for modulus,value in data['coarse_CRT'].items():
        pf=factor(int(modulus));assert len(pf)==1
        p=next(iter(pf));assignments[p]=value
    for p,z in sorted(assignments.items()):
        if p==2:continue
        own={}
        for t in targets:
            if t['q']==p:
                r=receipt(rows[str(p)],t['c'],prefix)
                assert r is not None
                own[str(t['c'])]=r
        incoming=[t for t in targets if t['p']==p]
        before=[receipt(rows[str(t['q'])],t['c'],prefix) for t in incoming]
        prefix[p]=z
        after=[receipt(rows[str(t['q'])],t['c'],prefix) for t in incoming]
        assert all(r is not None for r in after)
        trace.append(dict(p=p,chosen=z,own_targeted_release_receipts=own,
                          incoming_tags=[[t['q'],t['c']] for t in incoming],
                          before_receipts=before,after_receipts=after))
    # Intended allocation is not a receipt: q anchor1 remains live at lower3.
    q=rows['1645333507']
    assert receipt(q,1,{2:1,3:14}) is None
    assert receipt(q,0,{2:1,3:14}) is not None
    assert receipt(q,1,{2:1,3:14,30469139:0}) is not None
    return dict(valid_plan='PASS',targets=len(targets),rejected_mutations=rejected,
                trace=trace,intention_is_not_release='PASS',anchor_specific_release='PASS')
if __name__=='__main__':
    r=run();(Path(__file__).parent/'plan_results.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='trace'},indent=2))
