# Shared terminal hits force a safe progression on a reserved line

**Two shared hits exclude a cover by arbitrarily many active terminals on one reserved repair line**, provided their veto sets have distinct nonzero differences. The two hits force three common safe phases. Those phases form an arithmetic progression, so one additional terminal with the same distinct-difference property can veto at most two of them.

### The exclusion criterion

On a legal first-digit repair line \(x\in\mathbb F_r\), write a terminal shift as \(A X^x+B Y^x\), with the line intercept absorbed into \(B\). If \(X\ne Y\), two hits separated by a fixed nonzero difference determine the two summands uniquely. Thus a terminal’s hit set cannot contain two ordered pairs with that difference. [Predecessor difference bound](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

Suppose a family of such terminals all hit a set \(H\). Every point of \((H+H-H)\setminus H\) is safe for the entire family. If \(x=a+b-c\) were another hit, the distinct pairs \((x,a)\) and \((b,c)\) would have the same nonzero difference. Every midpoint of two distinct elements of \(H\) is safe by the same argument.

In particular, two shared hits \(a,b\) give the three safe phases
\[
2a-b,\qquad (a+b)/2,\qquad 2b-a
\]
for \(r\ge5\). They form a three-term progression. One additional terminal with distinct differences can veto at most two, leaving a phase that passes the whole panel. Verifying the two shared hits takes two readings per anchored terminal. The size of that family does not enter the test.

**The zero exception is exact.** For an active terminal with \(X=Y\ne1\), a whole-line veto occurs precisely when \(A+B=0\bmod q\) and \(n=0\bmod q\). If \(X\ne Y\), the difference proof works even at zero observation. A terminal blind to the reserve digit is constant and needs its own check. Subsequent ordinary repairs must preserve the selected terminal readings. [Protected continuation](https://github.com/Samsen879/a303656/commit/2e2c5d54904e266ee271fb9ea237dcd12cc86780)

### Actual \(3,5\) controls

On one legal \(31\)-repair line and one integer target, **16 ordinary terminals** each veto exactly \(\{0,1\}\). Even the sum of their exact veto counts is 32, so a cardinality-only union bound gives no exclusion on the 31-point line. The safe progression is \(\{30,16,2\}\). A seventeenth ordinary terminal vetoes \(\{30,2\}\), leaving 16 safe. Adding the zero-aligned comparator \(174407\) vetoes all 31 phases at exact valuation one.

The replay also changes the 16 terminal observations while keeping the head, source reading, and phase line fixed. Their nonzero observations then veto all 16 orbits of \(x\mapsto1-x\), covering the entire line. Thus the shared-hit hypothesis provides a genuine restriction. The numerical readers are ordinary comparators with their output readings fixed. The exclusion applies to hypothetical common-Wieferich terminals only when the same repair-line and hit hypotheses hold.

```python
from math import isqrt, lcm, prod

r = 31
G = (216071,242731,303491,329779,429971,476719,716659,737119,
     885919,958459,1099199,1203359,1558619,1616899,1715851,1723291)
extra, zero = 1899371,174407
qs = (*G,extra,zero)
step = lcm(3960,*(q*(q-1)//r for q in qs))
odd = step//(step & -step)
c,d = 15*step,13*step+r*odd

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

def phase(x):
    return c+step*x,d+step*(5*x%r)

assert step%r and all(pow(b,r-1,r*r)!=1 for b in (3,5))
for q in qs:
    assert q%4==3 and all(q%a for a in range(2,isqrt(q)+1))
    assert (q-1)%r==0 and (q-1)%(r*r)
    assert all(pow(b,q-1,q*q)!=1 for b in (3,5))
    X,Y = (pow(b,step,q*q) for b in (3,5))
    assert X!=1 and Y!=1 and pow(X,r,q*q)==pow(Y,r,q*q)==1
    if q==zero:
        assert X==pow(Y,5,q*q) and S(c,d,q*q)==0
    else:
        assert X*pow(Y,5,q*q)%(q*q)==1

def target(select):
    rows = [(32,3),(3,0),(r**3,(S(c,d,r**3)+r*r)%r**3)]
    rows += [(u,(S(c,d,u)+1)%u) for u in (7,11,19,23)]
    rows += [(q*q,(S(*phase(i),q*q)+q)%(q*q))
             for q,i in select.items()]
    M = prod(m for m,_ in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for m,a in rows)%M

def vetoes(n, readers):
    assert (n-S(c,d,32))%4==1
    assert all((n-S(c,d,u))%u for u in (3,7,11,19,23))
    out = {q:set() for q in readers}
    for x in range(r):
        C,E = phase(x)
        assert (n-S(C,E,r*r))%(r*r)==0
        k, = [k for k in range(r)
              if (n-S(C+step*r*k,E,r**3))%r**3==r*r]
        C += step*r*k
        for q in readers:
            v = (n-S(C,E,q*q))%(q*q)
            if v%q==0:
                assert v==q
                out[q].add(x)
    return out

n = target({**dict.fromkeys(G,0),extra:2,zero:0})
A = vetoes(n,qs)
assert all(n%q and A[q]=={0,1} for q in G)
assert n%extra and A[extra]=={2,30}
assert n%zero==0 and A[zero]==set(range(r))
assert {30,16,2}-set.union(*(A[q] for q in (*G,extra)))=={16}

reps = [x for x in range(r) if x<=(1-x)%r]
N = target({**dict(zip(G,reps)),extra:2,zero:0})
B = vetoes(N,G)
assert all(N%q and B[q]=={x,(1-x)%r} for q,x in zip(G,reps))
assert set.union(*B.values())==set(range(r))
assert all((n-N)%u==0 for u in (32,3,7,11,19,23,r**3,extra**2,zero**2))
```

Independent BigInt checked the full line on both CRT targets, all sixteen shared hit sets, the extra terminal's two hits, and the exact zero-aligned whole-line veto. The arbitrarily many-reader exclusion follows under the shared-hit and distinct-difference hypotheses only, not from physical prime constraints by themselves.
