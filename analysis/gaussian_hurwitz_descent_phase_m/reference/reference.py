"""Frozen 43-norm Hurwitz representation lab; no original-n search.
Python 3.10+ and NumPy required. Uses exact bounded int64 arithmetic.
Run: python reference.py --out /path/to/disposable-output
Assertions are proof checks: optimized Python is deliberately rejected.
"""
from __future__ import annotations
import itertools, math, collections, json, time
from pathlib import Path
try:
    import numpy as np
except ImportError as exc:
    raise SystemExit("NumPy is required for the producer. The separate independent_audit.py uses only the standard library.") from exc

OUT=Path(__file__).resolve().parent

def mul(a,b):
    w,x,y,z=map(int,a); v,s,t,u=map(int,b)
    return (w*v-x*s-y*t-z*u,w*s+x*v+y*u-z*t,w*t-x*u+y*v+z*s,w*u+x*t-y*s+z*v)

def L(a):
    w,x,y,z=map(int,a)
    return np.array([[w,-x,-y,-z],[x,w,-z,y],[y,z,w,-x],[z,-y,x,w]],dtype=np.int64)

def R(a):
    w,x,y,z=map(int,a)
    return np.array([[w,-x,-y,-z],[x,w,z,-y],[y,-z,w,x],[z,y,-x,w]],dtype=np.int64)

def elements(N):
    # Doubled coordinates of all Hurwitz integers of norm N.
    b=math.isqrt(4*N); ans=[]
    for x in itertools.product(range(-b,b+1),repeat=3):
        t=4*N-sum(v*v for v in x)
        if t<0: continue
        d=math.isqrt(t)
        if d*d!=t: continue
        for y in ([0] if d==0 else [-d,d]):
            q=x+(y,)
            if all(v%2==q[0]%2 for v in q): ans.append(q)
    return sorted(ans)

def shapes(N):
    ans=[]; T=4*N
    for a in range(math.isqrt(T//4)+1):
        for b in range(a,math.isqrt((T-a*a)//3)+1):
            if b%2!=a%2: continue
            for c in range(b,math.isqrt((T-a*a-b*b)//2)+1):
                if c%2!=a%2: continue
                t=T-a*a-b*b-c*c; d=math.isqrt(t)
                if d>=c and d*d==t and d%2==a%2: ans.append((a,b,c,d))
    return ans

def weight(x):
    v=math.factorial(4)
    for n in collections.Counter(x).values(): v//=math.factorial(n)
    return v*2**sum(t!=0 for t in x)

def hcontent(x):
    return math.gcd((x[0]-x[3])//2,(x[1]-x[3])//2,(x[2]-x[3])//2,x[3])

def remove5(x):
    assert x>0
    while x%5==0: x//=5
    return x

def omega(x):
    assert x>=1
    out=0; p=2
    while p*p<=x:
        while x%p==0: x//=p; out+=1
        p+=1
    return out+int(x>1)

def is5(x):
    return x>0 and remove5(x)==1

def target_pairs(x):
    if x[0]%2: return 0
    return sum(is5((x[i]*x[i]+x[j]*x[j])//4) for i,j in itertools.combinations(range(4),2))

def height(x,kind):
    if x[0]%2: return None
    vals=[remove5((x[i]*x[i]+x[j]*x[j])//4) for i,j in itertools.combinations(range(4),2) if x[i] or x[j]]
    return min(vals if kind=='bad' else [omega(v) for v in vals])

def components(adj,allowed=None):
    unseen=set(range(len(adj))) if allowed is None else set(allowed)
    res=[]
    while unseen:
        s=min(unseen); unseen.remove(s); comp=[s]; stack=[s]
        while stack:
            v=stack.pop()
            for w in adj[v]:
                if w in unseen: unseen.remove(w); stack.append(w); comp.append(w)
        res.append(sorted(comp))
    return res

def divisors(n): return [d for d in range(1,n+1) if n%d==0]


def main():
    start=time.time()
    U=elements(1); A=elements(5)
    assert len(U)==24 and len(A)==144
    C=np.unique(np.stack([L(a)@R(b) for a in A for b in A]),axis=0)
    assert len(C)==10368
    assert np.all(np.transpose(C,(0,2,1))@C==400*np.eye(4,dtype=np.int64))
    # Every inverse is present (transpose since C^t C=400 I).
    Cset={tuple(map(int,c.ravel())) for c in C}
    assert all(tuple(map(int,c.T.ravel())) in Cset for c in C)
    # Exact conjugation closure under generators of signed coordinate permutations.
    gens=[]
    for k in range(4):
        g=np.eye(4,dtype=np.int64);g[k,k]=-1;gens.append(g)
    for k in range(3):
        g=np.eye(4,dtype=np.int64);g[[k,k+1]]=g[[k+1,k]];gens.append(g)
    for g in gens:
        assert all(tuple(map(int,c.ravel())) in Cset for c in g[None,:,:]@C@g.T[None,:,:])
    D=np.unique(np.stack([L(u) for u in U]+[R(u) for u in U]),axis=0)
    # The 6 x 6 associate-class representatives are complete on either side.
    reps=[]
    for k in range(1,4):
        for s in [-1,1]:
            a=[2,0,0,0];a[k]=4*s;reps.append(tuple(a))
    lefts=[{tuple(v//2 for v in mul(u,a)) for u in U} for a in reps]
    rights=[{tuple(v//2 for v in mul(a,u)) for u in U} for a in reps]
    assert len(set.union(*lefts))==144 and all(len(s)==24 for s in lefts)
    assert len(set.union(*rights))==144 and all(len(s)==24 for s in rights)
    # Mod-5 matrix model in the H basis 1,i,j,(1+i+j+k)/2.
    def F(x):
        a,b,c,d=[int(t)*3%5 for t in x]
        return np.array([[a+2*b,-c-2*d],[c-2*d,a-2*b]],dtype=np.int64)%5
    Ar=[F(a) for a in reps]
    ranks=collections.Counter(); move_counts=collections.Counter()
    for h in itertools.product(range(5),repeat=4):
        a,b,c,d=h; x=(2*a+d,2*b+d,2*c+d,d)
        Q=F(x); det=int(round(int(Q[0,0])*int(Q[1,1])-int(Q[0,1])*int(Q[1,0])))%5
        rank=2 if det else int(np.any(Q))
        good=sum(not np.any((a@Q@b)%5) for a in Ar for b in Ar)
        assert good=={0:36,1:11,2:6}[rank]
        ranks[rank]+=1;move_counts[(rank,good)]+=1
    assert dict(ranks)=={0:1,1:144,2:480}
    Ns=[1,2,3,4,5,7,8,9,10,11,12,15,16,17,25,27,31,32,45,47,49,63,64,65,67,75,81,100,121,125,169,225,243,256,343,625,729,961,1024,1175,1875,2000,3919]
    result={
      'scope':'Fixed-norm representation graphs only. No original-n counterexample scan.',
      'coordinates':'x=2q in Hamilton coordinates; all even or all odd.',
      'graph':'All norm-5 two-sided operators plus left/right Hurwitz units, quotiented by all signed coordinate permutations. Further quotient by unit edges for heights.',
      'operator_count_pairs':144**2,'distinct_operators':len(C),
      'norm5_elements':A,'associate_representatives_doubled':reps,
      'residue_ranks':dict(ranks),'legal_class_pairs_by_rank':{0:36,1:11,2:6},
      'signed_permutation_normalization_verified':True,'inverse_closure_verified':True,
      'panels':[],'height_counterexamples':[]
    }
    np.savez_compressed(OUT/'operators.npz',operators=C,units=D)
    for M in Ns:
        xs=shapes(M); index={x:i for i,x in enumerate(xs)}
        adj=[set() for _ in xs]; uadj=[set() for _ in xs]
        for i,x in enumerate(xs):
            xx=np.array(x,dtype=np.int64)
            ys=C@xx; ys=ys[np.all(ys%20==0,axis=1)]//20
            assert np.all(np.sum(ys*ys,axis=1)==4*M)
            assert all(all(int(t)%2==int(y[0])%2 for t in y) for y in ys)
            for y in np.unique(np.sort(np.abs(ys),axis=1),axis=0):
                j=index[tuple(map(int,y))]; adj[i].add(j)
            zs=D@xx
            assert np.all(zs%2==0)
            zs=zs//2
            for y in np.unique(np.sort(np.abs(zs),axis=1),axis=0):
                j=index[tuple(map(int,y))]; adj[i].add(j);uadj[i].add(j)
        for i,ns in enumerate(adj):
            assert all(i in adj[j] for j in ns)
            assert all(remove5(hcontent(xs[i]))==remove5(hcontent(xs[j])) for j in ns)
        ws=[weight(x) for x in xs]; tp=[target_pairs(x) for x in xs]
        assert sum(ws)==24*sum(d for d in divisors(M) if d%2)
        assert sum(w for w,x in zip(ws,xs) if x[0]%2==0)==8*sum(d for d in divisors(M) if d%4)
        comps=components(adj); symcomps=components(uadj)
        sid={i:j for j,g in enumerate(symcomps) for i in g}
        sadj=[set() for _ in symcomps]
        for i,ns in enumerate(adj):
            for j in ns: sadj[sid[i]].add(sid[j])
        hs={kind:[min(height(xs[i],kind) for i in g if xs[i][0]%2==0) for g in symcomps] for kind in ['bad','omega']}
        st=[any(tp[i] for i in g) for g in symcomps]
        primitiveH={i for i,x in enumerate(xs) if hcontent(x)==1}
        primitiveL={i for i,x in enumerate(xs) if x[0]%2==0 and math.gcd(*(t//2 for t in x))==1}
        compdata=[]
        for comp in comps:
            compdata.append({'shape_indices':comp,'kappa5':sorted({remove5(hcontent(xs[i])) for i in comp}),
                             'H_points':sum(ws[i] for i in comp),
                             'L_points':sum(ws[i] for i in comp if xs[i][0]%2==0),
                             'primitive_H_points':sum(ws[i] for i in comp if i in primitiveH),
                             'primitive_L_points':sum(ws[i] for i in comp if i in primitiveL),
                             'fixed_pair_target_points':sum(ws[i]*tp[i] for i in comp)//6,
                             'any_pair_target_points':sum(ws[i] for i in comp if tp[i])})
        # Multi-source BFS on symmetry-quotient graph.
        dist={i:0 for i,v in enumerate(st) if v}; queue=collections.deque(dist)
        while queue:
            i=queue.popleft()
            for j in sadj[i]:
                if j not in dist:dist[j]=dist[i]+1;queue.append(j)
        for kind in ['bad','omega']:
            for i in range(len(symcomps)):
                if st[i] or i not in dist:continue
                if all(hs[kind][j]>=hs[kind][i] for j in sadj[i]):
                    # Record a full auditable local-minimum witness and one shortest target path.
                    path=[i]; k=i
                    while dist[k]>0:
                        k=min(j for j in sadj[k] if dist.get(j,10**9)==dist[k]-1);path.append(k)
                    result['height_counterexamples'].append({'M':M,'height':kind,'symmetry_orbit':i,
                      'H':hs[kind][i],'neighbor_heights':[[j,hs[kind][j]] for j in sorted(sadj[i])],
                      'distance_to_target':dist[i],'shortest_symmetry_path':path,
                      'path_heights':[hs[kind][j] for j in path]})
        result['panels'].append({'M':M,'L_points':sum(w for w,x in zip(ws,xs) if x[0]%2==0),'H_points':sum(ws),
          'B4_shapes':xs,'B4_weights':ws,'B4_adjacency':[sorted(ns) for ns in adj],
          'unit_symmetry_orbits':symcomps,'symmetry_quotient_adjacency':[sorted(ns) for ns in sadj],
          'heights':hs,'target_symmetry_orbits':[i for i,v in enumerate(st) if v],
          'distances_to_target':[dist.get(i) for i in range(len(symcomps))],
          'components':compdata,'component_count':len(comps),
          'target_free_component_count':sum(c['fixed_pair_target_points']==0 for c in compdata),
          'primitive_H_induced_component_count':len(components(adj,primitiveH)),
          'primitive_L_induced_component_count':len(components(adj,primitiveL)),
          'fixed_pair_target_points':sum(w*t for w,t in zip(ws,tp))//6,
          'max_target_distance':max(dist.values()) if dist else None})
        print(M,len(xs),len(symcomps),len(comps),result['panels'][-1]['target_free_component_count'],result['panels'][-1]['fixed_pair_target_points'],flush=True)
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    print('height_counterexamples',len(result['height_counterexamples']))
    print(json.dumps(result['height_counterexamples'][:6],indent=2))
    print('runtime_seconds',round(time.time()-start,3))

if __name__=='__main__':
    import argparse
    if not __debug__:
        raise SystemExit("Do not use -O: exact verification assertions must remain enabled.")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=OUT,help='Output directory; use a disposable directory to preserve packaged hashes.')
    args=parser.parse_args()
    OUT=args.out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
    main()
