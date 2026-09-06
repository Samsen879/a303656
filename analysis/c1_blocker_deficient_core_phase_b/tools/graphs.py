#!/usr/bin/env python3
"""Exact finite matching, Hall cores, and descending guard-route certificates."""
from collections import Counter, deque
from itertools import combinations

def subsets(items):
    v=tuple(items)
    for mask in range(1 << len(v)):
        yield frozenset(v[i] for i in range(len(v)) if mask >> i & 1)

def neighborhood(S, adj):
    return set().union(*(adj[q] for q in S)) if S else set()

def capacity(R, caps):
    return sum(caps[r] for r in R)

def maximum_matching(adj, caps):
    """Deterministic slot expansion and augmenting paths; all integers."""
    owners={}
    choices={q:tuple((r,k) for r in sorted(adj[q]) for k in range(caps[r]))
             for q in sorted(adj)}
    def augment(q, seen):
        for slot in choices[q]:
            if slot in seen: continue
            seen.add(slot)
            if slot not in owners or augment(owners[slot], seen):
                owners[slot]=q
                return True
        return False
    for q in sorted(adj):
        augment(q,set())
    return {q:slot for slot,q in owners.items()}

def hall_data(adj,caps):
    data=[]
    for S in subsets(sorted(adj)):
        N=neighborhood(S,adj)
        data.append((S,len(S)-capacity(N,caps)))
    delta=max(d for S,d in data)
    maximizers=[S for S,d in data if d==delta]
    return dict(max_deficiency=delta,
        rank=len(adj)-delta,
        canonical_smallest=set.intersection(*(set(S) for S in maximizers)),
        canonical_largest=set.union(*(set(S) for S in maximizers)))

def minimal_deficient(adj,caps):
    S=frozenset(adj)
    if len(S)<=capacity(neighborhood(S,adj),caps): return False
    return all(len(T)<=capacity(neighborhood(T,adj),caps) for T in subsets(S) if T!=S)

def assert_minimal_structure(adj,caps):
    S=frozenset(adj); N=neighborhood(S,adj)
    assert minimal_deficient(adj,caps)
    assert capacity(N,caps)==len(S)-1
    for q in S:
        T=S-{q}
        assert neighborhood(T,adj)==N
        mat=maximum_matching({v:adj[v] for v in T},caps)
        assert len(mat)==len(T)==capacity(N,caps)
    for lam in N:
        assert sum(lam in adj[q] for q in S)>=caps[lam]+1
    for R in subsets(S):
        if R and R!=S:
            lost=N-neighborhood(S-R,adj)
            assert capacity(lost,caps)<=len(R)-1
    if len(S)>1:
        assert all(adj[q] for q in S)
        seenL={min(S)}; seenR=set()
        while True:
            a=neighborhood(seenL,adj)
            b={q for q in S if adj[q]&a}
            if a==seenR and b==seenL: break
            seenR=a; seenL=b
        assert seenL==set(S) and seenR==N

def terminal_frontiers(P, supports):
    """P row labels; an odd order factor not in P is a free terminal."""
    P=set(P); ans={}
    for p in sorted(P):
        vals=set()
        for lam in supports[p]:
            assert lam<p
            vals.update(ans[lam] if lam in P else {lam})
        ans[p]=vals
    return ans

def route_forest(P,targets,supports,caps,matching):
    """Extract a guard forest from a terminal matching, merging row identities."""
    P=set(P); targets=set(targets)
    assert set(matching)==targets
    front=terminal_frontiers(P,supports)
    edge_options={}; paths={}
    for root in sorted(targets):
        terminal=matching[root][0]
        p=root; path=[root]
        while p in P:
            choices=[lam for lam in sorted(supports[p])
                     if lam==terminal or (lam in P and terminal in front[lam])]
            assert choices
            lam=choices[0]
            edge_options.setdefault(p,set()).add(lam)
            path.append(lam);p=lam
        assert p==terminal
        paths[root]=path
    forest={p:min(v) for p,v in sorted(edge_options.items())}
    loads=Counter(forest.values())
    assert targets <= forest.keys()
    for p,lam in forest.items():
        assert lam in supports[p] and lam<p
        assert lam not in P or lam in forest
    for lam,load in loads.items():
        assert load<=caps[lam]
    return dict(forest=forest,loads=dict(loads),paths=paths)

def dag_min_cut(P,targets,supports,caps):
    P=set(P); targets=set(targets)
    best=None; optimizers=[]
    for A in subsets(sorted(P)):
        boundary=neighborhood(A,supports)-A
        val=len(targets-A)+capacity(boundary,caps)
        if best is None or val<best: best=val;optimizers=[A]
        elif val==best: optimizers.append(A)
    return best,optimizers
