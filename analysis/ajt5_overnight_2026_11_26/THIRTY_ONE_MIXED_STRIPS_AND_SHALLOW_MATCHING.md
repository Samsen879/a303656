# Mixed-reader strip limits and colored shallow matching at the 31-sink

**A mixed \(31\)-reader can strike at most 21 of the 31 lower-digit pairs at one nonzero target.** Its exact relative order slope can reduce that bound to 16. A full chart covered only by mixed readers therefore needs at least **46 distinct primes**, or **61** if all their slopes are in the 16-strip class. The previous strip count required 31. A separate shallow-reader test gives a matching obstruction, with real ordinary controls that attain four covered lower pairs on one chart and at most three on another. [Predecessor repair chart and capacities](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

### Mixed readers share one target across all strips

Freeze the chart and orient a \((2,1)\) reader with its deep axis first. Write its expression as \(A X^x+B Z^i\), where \(X\) has order \(r^2\), \(Z\) has order \(r=31\), and \(i=x\bmod r\). The lower-line slope and intercept are absorbed into \(Z,B\). Define \(j\in\{1,\ldots,30\}\) by \(Z^j=X^r\).

For fixed \(T\ne0\), a strip exists above \(i\) exactly when \(z=Z^i\) satisfies
\[
(T-Bz)^r=A^r z^j .
\]
The converse holds because a candidate \((T-Bz)/A\) whose \(r\)th power is \(z^j\) belongs to the order-\(r^2\) subgroup and has the required lower digit.

Let \(h\) be the number of lower pairs missed. Reduce the polynomial in this equation modulo \(z^r-1\), and multiply by the monic polynomial \(Q\) whose roots are the \(h\) missed points. The product vanishes modulo \(z^r-1\). At coefficient indices \(h+1\le i\le30\) outside \([j,j+h]\), the convolution involves only unmodified binomial coefficients. After removing nonzero row and column factors, its columns are evaluations of
\[
(i)_{\underline t}(r+h-i)_{\underline{h-t}},\qquad 0\le t\le h.
\]
Cyclic terms wrapping around land at indices at most \(h-1\), so no wraparound enters these clean equations. This matrix follows by scaling \(\binom r{i-t}\) by \(\binom{r+h}{i}^{-1}\). These degree-\(h\) polynomials are independent by triangular evaluation at \(0,\ldots,h\). The characteristic exceeds \(r+h\), since \(r^2\mid p-1\). Thus there can be at most \(h\) clean indices. Counting them gives the exact bound from this test
\[
L(j)=\min\!\left(21,\ 16+\left\lfloor\frac{\min(j,31-j)}2\right\rfloor\right).
\]
The replay checks all 30 values. A \((2,0)\) reader still has \(L=1\).

### Shallow readers and the joint cover test

For a shallow reader with both axes active, write the lower-line expression as \(A\omega^i+B\omega^{ki}\). If \(k\ne\pm1\bmod31\), there is **at most one nonzero double-hit pair in its entire menu of target residues** at \(p>9\cdot10^{14}\). The [previous three-hit lemma](THIRTY_ONE_CYCLOTOMIC_DETERMINANT_CAPACITIES.md) handles intersecting pairs. For disjoint pairs, normalize the first pair to \((0,1)\) and the second to \((u,v)\). Two collisions would force
\[
(1-z)(z^{ku}-z^{kv})-(z^u-z^v)(1-z^k)=0
\quad\text{at }z=\omega.
\]
The finite certificate below checks all 11,368 normalized determinants. Each reduced coefficient-square sum is positive and at most 14. As in the degree-30 norm argument, the determinant vanishes at 1 and contains two factors \(1-\zeta\). Hence its normalized norm is bounded by \((14\cdot31/30)^{15}/31^2\), below the cutoff. This certificate is separate from the short-cofactor computation. For \(k=1\) there is no nonzero double pair. For \(k=-1\) the possible double pairs satisfy \(\omega^{i+i'}=B/A\).

Form the graph of possible nonzero shallow double pairs, with each edge carrying its physical reader as its color. If there are \(s\) shallow readers and the largest matching with distinct colors has size \(\nu\), they cover at most \(s+\nu\) lower pairs. Assign each covered pair to one reader that hits it. Every reader assigned two pairs contributes a disjoint edge of a distinct color.

If \(a\) lower pairs survive the shallow readers, a full cover therefore requires
\[
930a\ \le\
30\sum_{\rm mixed}\min(a,L_p)
+\sum_{\rm doubly\ deep}\min(2a,C_p),
\qquad a\ge31-s-\nu ,
\]
where \(C_p=62\), or \(31\) for an aligned reader. Each mixed strip covers at most 30 legal cells. The inequality uses one observation per physical prime.

### Controls and replay

The ordinary readers \(311,683\) have unique nonzero double pairs \(\{20,24\},\{9,19\}\) on the offset-zero chart. One integer target realizes both, together with two strips of the ordinary mixed reader \(21143\). On the offset-two chart their unique double pairs are \(\{26,30\},\{9,30\}\). The shared vertex forces the two shallow readers’ maximum down to three. A third integer preserves the entire offset-zero chart and both shallow observations while changing the mixed strips. This distinguishes the within-reader constraint from CRT freedom across distinct reader primes on a frozen chart.

All controls below have nonzero observations and exact valuation-one hits. They are ordinary finite controls. The structural bounds apply under the stated full-chart hypotheses, and the density ledger has no new subtraction.

```python
from collections import Counter, defaultdict
from itertools import combinations
from math import isqrt

r, W = 31, 307654935875658360
weights = Counter()
for k in range(2,r-1):
    for u,v in combinations(range(2,r),2):
        f = [0]*r
        exps = (k*u,k*v,k*u+1,k*v+1,u,v,u+k,v+k)
        for e,s in zip(exps,(1,-1,-1,1,-1,1,1,-1)):
            f[e%r] += s
        weights[sum(t*t for t in f)] += 1
assert weights == {6:1220,8:6336,10:3372,12:336,14:104}
assert (14*r)**15 < 9*10**14 * (r-1)**15 * r*r

for j in range(1,r):
    h = next(h for h in range(r+1)
             if sum(not(j<=i<=j+h) for i in range(h+1,r)) <= h)
    assert r-h == min(21,16+min(j,r-j)//2)

def S(x,y,m):
    return (pow(3,2+W*x,m)+pow(5,3+W*y,m)) % m

def fibres(p,off,deep=False):
    g = defaultdict(set)
    for i in range(r):
        for a in range(r if deep else 1):
            g[S(i+r*a,(14*i+off)%r,p)].add((i,a))
    return g

assert W%3960==0 and W%r
assert all(pow(b,30,r*r)!=1 for b in (3,5))
for p,depths in ((311,(1,1)),(683,(1,1)),(21143,(2,1))):
    assert p%4==3 and all(p%a for a in range(2,isqrt(p)+1))
    for b,d in zip((3,5),depths):
        assert pow(b,p-1,p*p)!=1
        assert pow(b,W*r**d,p*p)==1 and pow(b,W*r**(d-1),p)!=1

cases = [(0,1117038962129450725338467466723,178,57,18768),
         (2,1196212477410504713343011957187,64,143,18768),
         (0,1680732312524596587163463209635,178,57,9527)]
for (off,n,t,u,v),edges,strips in zip(
    cases, [({20,24},{9,19}),({26,30},{9,30}),({20,24},{9,19})],
    [{(20,13),(30,0)},set(),{(1,3),(20,20)}]):
    for p,T,E in zip((311,683),(t,u),edges):
        assert {z:{i for i,a in F} for z,F in fibres(p,off).items()
                if z and len(F)>1} == {T:E}
    assert fibres(21143,off,True)[v] == strips
    assert [n%p for p in (311,683,21143)] == [t,u,v]
    assert n%32==3 and n%3==0
    assert all((n-S(0,0,p))%p for p in (7,11,19,23))
    counts, total = Counter(), 0
    for i in range(r):
        j, = [j for j in range(r) if S(i,j,r*r)==n%(r*r)]
        assert j==(14*i+off)%r
        for a in range(r):
            for b in range(r):
                x,y = i+r*a,j+r*b
                if S(x,y,r**3)==n%r**3:
                    continue
                total += 1
                for p in (311,683,21143):
                    if S(x,y,p)==n%p:
                        assert S(x,y,p*p)!=n%(p*p)
                        counts[p]+=1
    assert total==28830
    assert [counts[p] for p in (311,683,21143)] == [1860,1860,30*len(strips)]

p,Z = 21143,pow(5,14*W,21143)
assert pow(Z,30,p)==pow(3,r*W,p)
for T,rows in ((18768,{20,30}),(9527,{1,20})):
    assert {i for i in range(r) if pow(T-125*pow(Z,i,p),r,p)
            == pow(9,r,p)*pow(Z,30*i,p)%p} == rows
assert (cases[2][1]-cases[0][1]) % (32*3*7*11*19*23*r**3*311**2*683**2)==0
```

Independent BigInt replay checked all 11,368 determinant coefficient vectors, all 30 slope counts, and the three ordinary full 28,830-cell repair charts with exact valuation-one reader hits. The slope-dependent limits are upper bounds, not assertions of attainability.
