# Intersecting the forced-safe triples of terminal clusters

**Different anchored clusters can be combined by intersecting their forced-safe triples.** On a reserve line of prime length \(r>3\), at most **three distinct anchor pairs** can share two forced-safe phases. The \(3,5\) control below attains that limit. A separate retargeting of the same arithmetic line gives a full cover by 16 nonzero double-hit readers, so favorable clustering requires evidence about the hits.

### Intersecting the safe sets

Write a terminal shift along the reserve line as \(AX^x+BY^x\). When \(X\ne Y\), its hit set has distinct nonzero ordered differences. For a fixed difference \(d\ne0\), the two hit equations determine \(AX^x\) and \(BY^x\) uniquely, and hence determine \(x\). [Predecessor difference bound](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

For every cluster sharing a hit pair \(\{a,b\}\), remove its vetoes from consideration at
\[
W(a,b)=\{2a-b,\ (a+b)/2,\ 2b-a\}.
\]
A hit at any of these points would repeat an ordered difference. Intersect the \(W\)'s across clusters, then check the remaining readers only on that intersection. If more common hit pairs are known for a cluster, union their safe triples before taking the intersection.

There are exactly three three-term progressions containing any two distinct candidate phases \(u,v\). Their third points are \(2u-v,(u+v)/2,2v-u\). Each progression determines a unique anchor pair by contracting its endpoints by a factor of three about its midpoint. Thus three distinct anchor pairs can share two safe phases, and four can share at most one.

**What the physical orders force.** For inverse characters \(Y=X^{-1}\), any double hit satisfies \(B/A=X^{a+b}\). On common exponent steps \(U,V\) prime to \(r\), with lower line \(y=\lambda x+\mu\), the \(r\)-primary projections force
\[
a+b\equiv
-c_0/U-(d_0/V+\mu)/\lambda\pmod r.
\]
So double-hit pairs in this class share a midpoint even when they are different pairs. Other character slopes can break that restriction.

**Zero observations.** When \(n\equiv0\bmod q\) and \(X\ne Y\), the equation \((X/Y)^x=-B/A\) has at most one solution. An active reader with \(X=Y\ne1\) vetoes the entire line exactly when \(A+B=0\) and \(n\equiv0\bmod q\). A reader blind to the reserve is constant and must be checked separately.

### Actual \(3,5\) control

On one legal \(31\)-repair line, 16 ordinary terminals share the pair \(\{0,1\}\). Two further ordinary readers have different midpoints, giving the following exact data.

| Anchors | Forced-safe triple |
|---|---|
| \(\{0,1\}\) | \(\{2,16,30\}\) |
| \(\{0,15\}\) at \(1056047\) | \(\{16,23,30\}\) |
| \(\{14,15\}\) at \(1620743\) | \(\{13,16,30\}\) |

The intersection is \(\{16,30\}\). An outside reader vetoes \(\{2,30\}\), leaving 16 safe. On that same integer, the zero-aligned reader \(174407\) vetoes all 31 phases.

For the countercontrol, change the terminal observations while retaining the head, source reading, and phase line. Fifteen inverse-character readers cover all phases except 16 with nonzero double hits. The noninverse reader \(36767\) vetoes \(\{16,17\}\), completing the cover. All numerical readers are ordinary comparators with frozen terminal readings. The geometric criterion applies conditionally to genuine common-Wieferich terminals with the stated hit data.

```python
from math import isqrt, lcm, prod

r = 31
G = (216071,242731,303491,329779,429971,476719,716659,737119,
     885919,958459,1099199,1203359,1558619,1616899,1715851,1723291)
bq,cq,dq,extra,zq = 1056047,1620743,36767,1899371,174407
qs = (*G,bq,cq,dq,extra,zq)
H = lcm(3960,*(q*(q-1)//r for q in qs))
H *= pow(H,-1,r)
L = lcm(3960,30*r*r,*(q*(q-1) for q in qs))
c,d = 15*H,13*H+r*(H//(H&-H))
for q,s,k in ((bq,17033,859),(cq,26141,9483),(dq,593,516)):
    assert q-1==2*r*s
    assert all((L//s)%(v*(v-1))==0 for v in qs if v!=q)
    d += k*(L//s)

def S(a,b,m):
    return (pow(3,a,m)+pow(5,b,m))%m

def phase(x):
    return c+H*x,d+H*(5*x%r)

assert H%r==1 and all(pow(b,r-1,r*r)!=1 for b in (3,5))
for q in qs:
    assert q%4==3 and all(q%i for i in range(2,isqrt(q)+1))
    assert (q-1)%r==0 and (q-1)%(r*r)
    assert all(pow(b,q-1,q*q)!=1 for b in (3,5))
    X,Y=pow(3,H,q),pow(5,5*H,q)
    assert X!=1 and Y!=1 and pow(X,r,q)==pow(Y,r,q)==1
    if q==zq:
        assert X==Y and S(c,d,q*q)==0
    elif q in (bq,cq,dq):
        assert X!=Y and X*Y%q!=1
    else:
        assert X*Y%q==1

def target(reads):
    rows=[(32,3),(3,0),(r**3,(S(c,d,r**3)+r*r)%r**3)]
    rows += [(u,(S(c,d,u)+1)%u) for u in (7,11,19,23)]
    for q,x in reads.items():
        values={S(*phase(i),q*q) for i in range(r)}
        T=S(*phase(x),q)
        rows.append((q*q,next(T+q*k for k in range(r+1)
                              if T+q*k not in values)))
    M=prod(m for m,_ in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for m,a in rows)%M

def vetoes(n,readers):
    out={q:set() for q in readers}
    assert (n-S(c,d,32))%4==1
    assert all((n-S(c,d,u))%u for u in (3,7,11,19,23))
    for x in range(r):
        C,E=phase(x)
        assert (n-S(C,E,r*r))%(r*r)==0
        k,=[k for k in range(r) if (n-S(C+H*r*k,E,r**3))%r**3==r*r]
        C+=H*r*k
        for q in readers:
            z=(n-S(C,E,q*q))%(q*q)
            if z%q==0:
                assert z
                out[q].add(x)
    return out

reads={**dict.fromkeys(G,0),bq:0,cq:14,dq:16,extra:2,zq:0}
n=target(reads)
A=vetoes(n,qs)
assert all(A[q]=={0,1} for q in G)
assert [A[q] for q in (bq,cq,dq,extra)]==[
    {0,15},{14,15},{16,17},{2,30}]
assert all(n%q for q in qs if q!=zq)
assert n%zq==0 and A[zq]==set(range(r))
assert all(S(*phase(x),extra)%extra for x in range(r))

def safe(a,b):
    return {(2*a-b)%r,(2*b-a)%r,(a+b)*pow(2,-1,r)%r}

P=safe(0,1)&safe(0,15)&safe(14,15)
assert P=={16,30} and P-A[extra]=={16}

reps=[x for x in range(r) if x<(1-x)%r]
N=target({**reads,**dict(zip(G,reps))})
B=vetoes(N,(*G[:15],dq))
assert all(N%q and len(xs)==2 for q,xs in B.items())
assert set.union(*B.values())==set(range(r))
assert all((N-n)%u==0 for u in (32,3,7,11,19,23,r**3))
```

Independent BigInt checked all exact clustered and retargeted hit sets, the nonzero observation checks and the zero-aligned veto. The test requires actual common hit pairs within each cluster and makes no general full-panel assertion.
