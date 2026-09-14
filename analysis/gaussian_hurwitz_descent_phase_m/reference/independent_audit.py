"""Independent standard-library replay: pair enumeration and 36 associate moves.
Does not import reference.py/lab.py, NumPy, or the first producer's operators.
"""
from __future__ import annotations
from collections import defaultdict, deque
from functools import lru_cache
from itertools import product, combinations
from math import isqrt, gcd
import json,sys,time
from pathlib import Path

def qmul(a,b):
    # Scalar/vector definition, deliberately distinct from the matrix producer.
    s=a[0]*b[0]-sum(a[k]*b[k] for k in (1,2,3))
    cross=(a[2]*b[3]-a[3]*b[2],a[3]*b[1]-a[1]*b[3],a[1]*b[2]-a[2]*b[1])
    return (s,)+tuple(a[0]*b[k]+b[0]*a[k]+cross[k-1] for k in (1,2,3))

U=[]
for k in range(4):
    for s in [-1,1]:
        x=[0]*4;x[k]=2*s;U.append(tuple(x))
U+=list(product([-1,1],repeat=4))
A=[]
for k in (1,2,3):
    for s in [-1,1]:
        x=[2,0,0,0];x[k]=4*s;A.append(tuple(x))

@lru_cache(None)
def unit_orbit(x):
    seen={x};queue=[x]
    while queue:
        y=queue.pop()
        for u in U:
            for z in (qmul(u,y),qmul(y,u)):
                assert all(t%2==0 for t in z)
                z=tuple(sorted(abs(t//2) for t in z))
                if z not in seen:seen.add(z);queue.append(z)
    return tuple(sorted(seen))

def canon(x):
    return unit_orbit(tuple(sorted(abs(t) for t in x)))[0]

def point_enumeration(M):
    b=isqrt(4*M); pairs=defaultdict(list)
    for a in range(-b,b+1):
        for c in range(-b,b+1):
            v=a*a+c*c
            if v<=4*M and a%2==c%2:pairs[(v,a%2)].append((a,c))
    ns=defaultdict(int);Lcount=Hcount=target=0
    for (v,par),left in pairs.items():
        for a,b in left:
            for c,d in pairs.get((4*M-v,par),[]):
                x=(a,b,c,d);Hcount+=1;ns[tuple(sorted(abs(t) for t in x))]+=1
                if par==0:
                    Lcount+=1
                    val=(c*c+d*d)//4
                    if val>0:
                        while val%5==0:val//=5
                        target+=int(val==1)
    return ns,Lcount,Hcount,target

def height(orbit):
    vals=[]
    for x in orbit:
        if x[0]%2:continue
        for i,j in combinations(range(4),2):
            v=(x[i]*x[i]+x[j]*x[j])//4
            if v:
                while v%5==0:v//=5
                vals.append(v)
    assert vals
    return min(vals)

def component(A,s,keep):
    seen={s};queue=[s]
    while queue:
        u=queue.pop()
        for v in A[u]:
            if v not in seen and keep(v):seen.add(v);queue.append(v)
    return seen

def main(root):
    t=time.time();data=json.loads((root/'results.json').read_text());receipts=[]
    # Independently enumerate ALL 144 norm-5 elements by their two coordinate patterns.
    from itertools import permutations
    allA=set()
    for pattern in [(4,2,0,0),(3,3,1,1)]:
        for p in set(permutations(pattern)):
            for signs in product([-1,1],repeat=4):allA.add(tuple(x*s for x,s in zip(p,signs)))
    assert len(allA)==144
    for side in [0,1]:
        actual=[]
        for a in A:
            coset={tuple(t//2 for t in (qmul(u,a) if side==0 else qmul(a,u))) for u in U}
            assert len(coset)==24;actual.extend(coset)
        assert len(actual)==len(set(actual))==144 and set(actual)==allA
    for p in data['panels']:
        M=p['M'];ns,lc,hc,tc=point_enumeration(M)
        assert (lc,hc,tc)==(p['L_points'],p['H_points'],p['fixed_pair_target_points'])
        assert dict(ns)=={tuple(x):w for x,w in zip(p['B4_shapes'],p['B4_weights'])}
        orbits=sorted({unit_orbit(x) for x in ns})
        assert len(orbits)==len(p['unit_symmetry_orbits'])
        pos={o[0]:i for i,o in enumerate(orbits)};adj=[]
        for i,o in enumerate(orbits):
            expected=tuple(tuple(p['B4_shapes'][k]) for k in p['unit_symmetry_orbits'][i])
            assert o==expected
            x=o[0];neighbors={i}
            for a in A:
                for b in A:
                    y=qmul(qmul(a,x),b)
                    if any(t%20 for t in y):continue
                    y=tuple(t//20 for t in y)
                    assert len({t%2 for t in y})==1
                    assert sum(t*t for t in y)==4*M
                    neighbors.add(pos[canon(y)])
            adj.append(neighbors)
            assert neighbors==set(p['symmetry_quotient_adjacency'][i]),(M,i,neighbors,p['symmetry_quotient_adjacency'][i])
        H=[height(o) for o in orbits]
        assert H==p['heights']['bad']
        receipts.append({'M':M,'status':'PASS','L_points':lc,'H_points':hc,'fixed_pair_targets':tc,'quotient_vertices':len(orbits)})
        if M==1175:
            assert H[8]==H[9]==2
            assert component(adj,8,lambda i:H[i]<13)=={8,9}
            assert all(H[i]!=1 for i in [8,9])
            assert 34 in adj[8] and 6 in adj[34] and H[34]==13 and H[6]==1
    # Direct integer expansion of the two exhibited norm-1175 moves.
    q=(1,3,3,34);a=(-2,0,0,-1);b=(-2,0,1,0)
    out=qmul(qmul(a,q),b);assert out==tuple(5*t for t in (-11,15,10,27))
    q=(10,11,15,27);a=(-2,0,1,0);b=(-2,0,0,-1)
    out=qmul(qmul(a,q),b);assert out==tuple(5*t for t in (1,2,9,33))
    receipt={'status':'PASS','method':'Independent stdlib pair enumeration + 36 associate-class moves; no producer imports or NumPy',
             'panels':receipts,'1175_barrier':{'start':8,'initial_height':2,'strict_sublevel_13_component':[8,9],'exact_bottleneck':13,'path':[8,34,6]},
             'limitations':'Independent implementation replay by the same assistant, not an external mathematical referee or independent human review.',
             'seconds':round(time.time()-t,3)}
    (root/'INDEPENDENT_REPLAY.json').write_text(json.dumps(receipt,indent=2))
    print(json.dumps({'status':'PASS','panels':len(receipts),'seconds':receipt['seconds']}))

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Do not use -O: verification assertions must remain enabled.')
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent)
