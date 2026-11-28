# Fixed-anchor even quartic Gram rigidity through degree seven

**Verified the P3 claim for the even quartic top target.** With the four #88 offsets and \(M(0)=\left(\begin{smallmatrix}450&609\\609&7578\end{smallmatrix}\right)\), every \(M\in\operatorname{Sym}_2\mathbb Q[t]\) of degree at most seven whose four even quartic residuals are sums of two squares in \(\mathbb Q(S,R,t)\) is constant. The proof allows arbitrary denominators in the original coordinates. It is separate from #110’s fixed-denominator exclusion. [Pinned #88 input](https://github.com/Samsen879/a303656/blob/5277b098af15dbef95cf5a90c91a58c418598439/analysis/four_distinct_noncollinear_labels.md)

The finite replay is reconstructed from the pinned public coefficients and treats degrees two and four directly.

### Descent and degree reduction

In \(\mathbb Q(i)[S,R,t]\), factor the rational norm \(f\bar f\), choosing monic irreducibles. Conjugation-fixed factors have even exponents. Conjugate pairs have equal exponents. Since the residual is polynomial, all these exponents are nonnegative. Keep half the exponent on fixed factors and put each conjugate pair entirely on one side. The scalar unit is the original scalar norm, so this gives polynomial two-square coordinates. Their highest and lowest \(S,R\)-homogeneous terms cannot cancel in a sum of real squares. Thus the coordinates are homogeneous of degree two in \(S,R\), with \(t\)-degree at most half the target degree.

If the \(SR\) coefficient vector is nonzero, the vanishing odd cross-terms force the \(S^2\) and \(R^2\) vectors to lie in its one-dimensional orthogonal complement. Hence \((A-a_i)(B-b_i)\) is a square in \(\mathbb Q(t)\), where \(M=\left(\begin{smallmatrix}A&C\\ C&B\end{smallmatrix}\right)\). At \(t=0\) the four products are nonzero nonsquares. Specializing a rational square that is regular and nonzero there gives a rational square, so the \(SR\) vectors must vanish.

It follows that \(M-D_i\) is a polynomial Gram matrix, with signed polynomial determinant roots \(y_i\). Put \(K=AB-C^2\) and \(r=(705,-571,-189,55)\). Then
\[
y_i^2=K-b_iA-a_iB+a_ib_i,\qquad
r\cdot(y^2-y(0)^2)=0.
\]
Positivity at both real ends excludes odd degrees. A rank-two highest coefficient makes all determinant roots have the same leading term after sign choice. Their differences are constant because \(y_i^2-y_j^2\) has degree at most \(\deg M\). The cofactor identity would then require \(r\cdot y(0)=0\), which fails for every sign choice.

### Finite certificate for the rank-one cases

For degrees two and four the determinant roots have degree at most two. The first three Gram matrices are strictly positive definite for real \(t\), since each exceeds the fourth by a positive diagonal matrix. Their roots therefore have even degree. The fourth root obeys the same upper bound by the determinant-difference formula. Choose positive constants \(k=(1740,1722,1688,1362)\) and write \(y=k+ut+vt^2\). The cofactor conditions are exactly
\[
r\cdot(ku)=0,\quad r\cdot u^2+2r\cdot(kv)=0,\quad
r\cdot(uv)=0,\quad r\cdot v^2=0
\]
with componentwise products. **All 1,473 normalized nonzero mod-11 candidates fail the square test \(AB-K=C^2\).**

For degree six, at least one of the first three roots must have degree four. Otherwise their differences force \(\deg A,\deg B\le4\), and the determinant equation then forces \(\deg C\le4\). All four roots therefore have degree four with common leading and cubic coefficients after sign choice. The first three constant signs are positive, and the fourth can have either sign. Writing these constants as \(d\), coefficient comparison gives exactly
\[
y=d+h-\frac{r\cdot h^2}{2(r\cdot d)}\mathbf1,\qquad
h=ut+vt^2,\qquad r\cdot h=r\cdot(dh)=0.
\]
For example, if \(\alpha\) is the vector of quadratic root coefficients, the quadratic coefficient of \(h\) is \(\alpha-\mathbf1(r\cdot(d\alpha))/(r\cdot d)\). The \(t^2,t^3,t^4\) cofactor equations then give the displayed common correction.

I reproduced the report’s 1,320 independent pairs and 12 ray directions per sign, including the ray odd-part degree histogram \(\{4:1,5:2,6:9\}\). The replay below instead tests **all 1,476 normalized paths per sign**, including all 156 dependent or one-term reductions directly. None passes.

For both certificates, rescale \(t\) by a power of a uniformizer with \(\pi^2=11\), using weights one and two for the two coefficient vectors. This gives integral coefficients and a nonzero reduction, even when the rational coefficients initially have 11-adic denominators. Recovery of \(A,B,K\) uses a matrix invertible modulo 11. Thus \(C^2\) is integral, and the Gauss valuation implies \(C\) is integral as well. This handles degenerate **polynomial path** reductions. It does not audit smooth conics, their bad reductions, or the report’s separate nonhomogeneous rigidity theorem.

### Public-only replay

```python
from itertools import product
from math import isqrt

a,b = (1,5,25,125),(9,81,1,729)
r,k = (705,-571,-189,55),(1740,1722,1688,1362)
L = ((20,7),(21,2),(19,8),(17,6))
V = ((0,87),(21,84),(59,-64),(57,-60))

def dot(x,y):
    return sum(u*v for u,v in zip(x,y))

for x,y,u,v,z in zip(a,b,L,V,k):
    assert (dot(u,u)+x,dot(u,v),dot(v,v)+y) == (450,609,7578)
    assert abs(u[0]*v[1]-u[1]*v[0]) == z
    g = (450-x)*(7578-y)
    assert isqrt(g)**2 != g
assert sum(r) == dot(r,a) == dot(r,b) == 0
assert all(dot(r,[x*s for x,s in zip(k,e)])
           for e in product((-1,1),repeat=4))

p = 11
I = ((1,1,9),(9,10,3),(6,10,7))
rows = [(-b[i],-a[i],1) for i in (1,2,3)]
assert [[dot(w,v)%p for v in zip(*rows)] for w in I] == [
    [1,0,0],[0,1,0],[0,0,1]]

def trim(f):
    f = [x%p for x in f]
    while f and not f[-1]:
        f.pop()
    return f

def add(f,g):
    c = [0]*max(len(f),len(g))
    for i,x in enumerate(f): c[i] += x
    for i,x in enumerate(g): c[i] += x
    return trim(c)

def mul(f,g):
    if not f or not g:
        return []
    c = [0]*(len(f)+len(g)-1)
    for i,x in enumerate(f):
        for j,y in enumerate(g): c[i+j] += x*y
    return trim(c)

def scale(z,f):
    return trim([z*x for x in f])

def lin(weights,polys):
    f = []
    for z,g in zip(weights,polys):
        f = add(f,scale(z,g))
    return f

def rad(y):
    q = [add(mul(y[i],y[i]),[-a[i]*b[i]]) for i in (1,2,3)]
    A,B,K = [lin(w,q) for w in I]
    return add(mul(A,B),scale(-1,K))

def square(f):
    assert f[0] == 609**2%p
    if len(f)%2 == 0:
        return False
    c = [609%p]
    for j in range(1,(len(f)+1)//2):
        middle = sum(c[i]*c[j-i] for i in range(1,j))
        c.append((f[j]-middle)*pow(1218,-1,p)%p)
    return mul(c,c) == f

F = list(product(range(p),repeat=4))
def rd(d,v):
    return dot(r,[x*y for x,y in zip(d,v)])%p
def first(v):
    return next((x for x in v if x),0)

groups = {}
for v in F:
    if rd(v,v)==0:
        groups.setdefault(rd(k,v),[]).append(v)
n = 0
for u in F:
    if rd(k,u) or first(u)>1:
        continue
    for v in groups.get(-6*rd(u,u)%p,[]):
        if not any(u+v) or rd(u,v):
            continue
        n += 1
        assert not square(rad([[d,x,z] for d,x,z in zip(k,u,v)]))
assert n==1473 and square(rad([[d] for d in k]))

for sign in (1,-1):
    d = k[:3]+(sign*k[3],)
    H = [v for v in F if dot(r,v)%p==rd(d,v)==0]
    c = dot(r,d)%p
    assert len(H)==121 and c
    counts = [0,0]
    for u,v in product(H,repeat=2):
        if (first(u)!=1 if any(u) else first(v) not in (1,2)):
            continue
        dep = any(all((y-s*x)%p==0 for x,y in zip(u,v))
                  for s in range(p))
        counts[int(any(u) and not dep)] += 1
        h = [[0,x,z] for x,z in zip(u,v)]
        j = scale(-pow(2*c,-1,p),lin(r,[mul(x,x) for x in h]))
        assert not square(rad([add([e],add(x,j)) for e,x in zip(d,h)]))
    assert counts == [156,1320]
print("PASS")
```
