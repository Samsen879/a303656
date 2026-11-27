# Exact repair slices and failure after planar flatness

**The shortest dual width can pass the sharp general planar flatness threshold while the full local panel still fails.** In an actual \(3,5\) quarter-box, the \(7,59\) repair lattice has width \(910/413>1+2/\sqrt3\) and contains exactly four candidate cells. Each cell has a different, unique odd-valuation blocker. Removing any one of the four blocking rows restores an ordinary-height local survivor.

### Slice the lattice before charging deletions

For a first-level repair coset \(z+\Lambda\), choose a primitive dual functional \(w\), so \(w(\Lambda)=\mathbb Z\). Let \(\delta\) generate \(\Lambda\cap\ker w\), and choose \(b\in\Lambda\) with \(w(b)=1\). The box support function gives the possible levels \(w(z)+j\). At each level, intersecting
\[
z+jb+i\delta
\]
with the index box gives an exact integer interval of allowable \(i\). A level can meet the real box and have an empty integer interval.

For a higher reader with other reads fixed and only a first native \(p\)-digit exposed, its deleted labels pull back to explicit classes of \(i\bmod p\). If \(\delta_u\equiv0\bmod p\), that reader can erase the whole slice. On the first-level repair coset, the remainder divided by \(p^2\), reduced modulo \(p\), is a polynomial of degree at most two in \(i\). This follows by expanding the two unit powers modulo \(p^3\). Its roots give the additional deletions for **exact valuation two**. Union the two residue lists at each \(p\), then count the remaining integers in the interval by CRT and inclusion–exclusion, or directly on a short interval. A zero at this precision requires a deeper check when proving odd valuation.

This test uses actual slice lengths and phases. On the preceding positive \(3,5\) control, the active box \([0,29]\times[0,19]\) has a single occupied slice with cells \((14,2),(29,10)\). The \(43\) unit test deletes the first, and the second passes the stated panel. The earlier sufficient basis box was \([0,106]\times[0,67]\). This is a finite improvement on that certificate. A growing-family bound that guarantees enough surviving slices is still open in this setup.

### Flatness passes and all four candidates fail

Use
\[
c=99+522u,\qquad d=522v,\qquad
B=[0,50]\times[0,34].
\]
At the CRT target constructed below, both native rows always collide modulo their primes. Even valuation at both \(7,59\) therefore requires the first repair congruence \(v\equiv-27u\bmod413\).

The dual vectors are \((h,k)/413\) with \(h\equiv27k\bmod413\). Their shortest box width is \(910/413\), attained at \((-8,15)/413\). The general planar flatness theorem guarantees an interior lattice point before deletions at this width (which also exceeds the threshold 2 for centrally symmetric sets). Its hypothesis concerns the underlying lattice and convex box. [Averkov–Wagner, Theorem 2.2](https://arxiv.org/html/1003.4365v2)

Here the shortest functional ranges over \([-400,510]/413\), admitting levels \(0,1\). Level \(1\) would require \(u\equiv14\bmod15\) and \(v\ge35\). Level \(0\) contains all four candidates.

| Index pair | \(v_7\) | \(v_{59}\) | \(v_{43}\) | \(v_{1063}\) |
|---|---:|---:|---:|---:|
| \((0,0)\) | 2 | 2 | 0 | **1** |
| \((15,8)\) | 2 | 2 | **1** | 0 |
| \((30,16)\) | **3** | 2 | 0 | 0 |
| \((45,24)\) | 2 | **3** | 0 | 0 |

Every other inert prime through \(1063\) is a unit at these four cells, and the \(2,3\) tests pass. The two higher readers use just the first source digits on both axes, \(43\) at \(7\) and \(1063\) at \(59\). The target is lifted into the interval that makes \(B\) exactly the anchored quarter-box \(3^c,5^d\le n/4\).

```python
from math import isqrt, prod

A,c0,P = 522,99,413
def off(m,u,v):
    return (pow(3,c0+A*u,m)+pow(5,A*v,m)) % m
def cells(U,V,tau):
    return [(u,v) for u in range(U+1) if (v:=(tau-27*u)%P)<=V]

for p,q in [(7,43),(59,1063)]:
    assert pow(3,A,p)==pow(5,A,p)==1
    a=(pow(3,A,p*p)-1)//p*pow(3,c0,p)%p
    b=(pow(5,A,p*p)-1)//p%p
    assert b and a==27*b%p
    assert all(pow(g,A,q)!=1 and pow(g,A*p,q)==1 for g in (3,5))

U,V = 50,34
w = min([P*U]+[U*abs((27*k+P//2)%P-P//2)+V*k
               for k in range(1,910//V+1)])
assert w==910 and 3*(w-P)**2>4*P*P
S = cells(U,V,0)
assert S==[(0,0),(15,8),(30,16),(45,24)]

kill = [(1063,1),(43,1),(7,3),(59,3)]
Q = [p for p in range(7,1064,4) if all(p%d for d in range(2,isqrt(p)+1))]
H = {p:e+1 for p,e in kill}
t = {3:0,4:1}
for (u,v),(p,e) in zip(S,kill):
    m=p**(e+1)
    t[m]=(off(m,u,v)+p**e)%m
for p in Q:
    if p not in H:
        t[p]=next(r for r in range(p) if all(off(p,u,v)!=r for u,v in S))
M=prod(t)
r=sum(a*(M//m)*pow(M//m,-1,m) for m,a in t.items())%M
lo=4*max(3**(c0+A*U),5**(A*V))
n=lo+(r-lo)%M
assert lo<=n<4*min(3**(c0+A*(U+1)),5**(A*(V+1)))
assert all(n%p**2==off(p**2,0,0) for p in (7,59))
for (u,v), expected in zip(S,kill):
    odds=[]
    assert (n-off(4,u,v))%4==1 and (n-off(3,u,v))%3
    for p in Q:
        m=p**H.get(p,1)
        z=(n-off(m,u,v))%m
        assert z
        e=0
        while z%p==0:
            z//=p
            e+=1
        if e%2:
            odds.append((p,e))
    assert odds==[expected]

# Earlier positive chart, with a different target on the same lattice shape.
n=33665234458065+4*38639644414476*3**(c0+A*29)
assert 4*max(3**(c0+A*29),5**(A*19))<=n
assert n<4*min(3**(c0+A*30),5**(A*20))
assert all(n%p**2==off(p**2,0,380) for p in (7,59))
assert cells(29,19,380)==[(14,2),(29,10)]
assert (n-off(43,14,2))%43==0
assert all((n-off(q,29,10))%q for q in (43,1063))
assert all((n-off(p**3,29,10))%p**3 in range(p*p,p**3,p*p)
           for p in (7,59))
```

The countercontrol rules out a certificate based solely on passing the shortest-width threshold and checking the rows separately. The slice test instead certifies joint survival in the actual box. The positive replay checks a specified local panel, and the negative replay blocks one anchored chart through \(1063\). Neither settles two-square representation at the target.
