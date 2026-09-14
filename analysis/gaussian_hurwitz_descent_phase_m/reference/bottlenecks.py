"""Exact minimax paths on the frozen representation graphs; standard library only.
Run after reference.py: python bottlenecks.py /path/to/disposable-output
"""
from __future__ import annotations
import heapq,json,sys
from pathlib import Path

def main(root:Path)->None:
    data=json.loads((root/'results.json').read_text())
    barriers=[]; all_costs=[]
    for p in data['panels']:
        h=p['heights']['bad']; adj=p['symmetry_quotient_adjacency']
        costs=[None]*len(h); heap=[]
        for t in p['target_symmetry_orbits']:
            costs[t]=1;heapq.heappush(heap,(1,t))
        while heap:
            cost,u=heapq.heappop(heap)
            if costs[u]!=cost:continue
            for v in adj[u]:
                cand=max(cost,h[v])
                if costs[v] is None or cand<costs[v]:
                    costs[v]=cand;heapq.heappush(heap,(cand,v))
        all_costs.append({'M':p['M'],'minimax_bad_heights':costs})
        for i,cost in enumerate(costs):
            if cost is not None and cost>h[i]:
                integer_shapes=[[v//2 for v in p['B4_shapes'][j]] for j in p['unit_symmetry_orbits'][i] if p['B4_shapes'][j][0]%2==0]
                barriers.append({'M':p['M'],'height':'bad','orbit':i,'initial':h[i],'barrier':cost,'integer_shapes':integer_shapes})
        if p['M']==1175:
            assert costs[8]==costs[9]==13
    (root/'barriers.json').write_text(json.dumps(barriers,indent=2))
    (root/'minimax_paths.json').write_text(json.dumps(all_costs,indent=2))
    print(json.dumps({'panels':len(all_costs),'compulsory_uphill_bad_height_cases':len(barriers)}))

if __name__=='__main__':
    if not __debug__:raise SystemExit('Do not use -O.')
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent)
