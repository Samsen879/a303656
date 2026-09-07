from arithmetic import factor,order
from itertools import combinations
from pathlib import Path
import json

def run():
    bs={7:0,31:1,43:2,103:2}; rows={}
    for q,b in bs.items():
        w=order(q);e=factor(w).get(3,0)
        assert factor(q)=={q:1} and q%4==3 and e==1
        assert pow(5,w,q*q)!=1 # all regular; not fabricated rigid rows.
        r=(1+pow(5,b,q*q))%(q*q)
        assert (r-1)%q==pow(5,b,q)
        rows[q]=dict(q=q,w=w,s=1,K=2,E=[1],r=r,b=b,c=0,projection3=b%3)
    def union(ids):return {bs[q]%3 for q in ids}
    I={7,31};J={7,43,103}
    assert len(I)<len(J) and union(I)!={0,1,2} and union(J)!={0,1,2}
    assert all(union(I|{q})=={0,1,2} for q in J-I)
    ids=list(bs)
    subsets=[set(c) for n in range(5) for c in combinations(ids,n)]
    checks=0
    # exact submodularity of union cardinality on all ordered pairs.
    for A in subsets:
        for B in subsets:
            assert len(union(A))+len(union(B))>=len(union(A|B))+len(union(A&B));checks+=1
    return dict(scope='Actual regular-row positive-divisibility guards, single anchor, free coordinate3. NOT nonregular-root completeness.',
      rows=list(rows.values()),I=sorted(I),J=sorted(J),unionI=sorted(union(I)),unionJ=sorted(union(J)),
      augmentations=[dict(q=q,union=sorted(union(I|{q}))) for q in sorted(J-I)],
      matroid_exchange='FAIL',submodularity_checks=checks,submodularity='PASS')

if __name__=='__main__':
    r=run();(Path(__file__).parent/'resource_results.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2))
