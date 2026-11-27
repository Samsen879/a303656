# Seventeen-strip cap from a coefficient-rank invariant

**A mixed reader at the \(31\)-sink hits at most 17 lower pairs, for every physical relative slope.** This excludes 21-strip saturation and the 46-reader same-orientation design. The certificate applies to every prime with \(31^2\mid p-1\). It uses neither the prime search cutoff nor the short-cofactor certificate.

On the full chart, a mixed-only cover now needs at least \(\lceil31^2/17\rceil=57\) readers. At 57, all must have the same orientation. With fewer than 60 readers, a block can only be covered by striking all 31 coordinates on one axis. At 57 readers, even one reader on the other axis would leave at most \(56\cdot17=952<961\) useful strip incidences. The 57-reader case has eight incidences to spare, so at least 49 readers must hit 17 lower pairs. Whether 17 is attainable remains open. [Predecessor repair chart](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

### The coefficient invariant

Orient a \((2,1)\) reader with its deep axis first. Let \(X\) have order \(31^2\), \(Z\) have order 31, and \(Z^j=X^{31}\), with \(1\le j\le30\). At a nonzero target \(T\), a strip exists above lower digit \(i\) exactly when
\[
(T-Bz)^{31}=A^{31}z^j,\qquad z=Z^i .
\]
Scale \(x=-Bz/T\). The equation becomes \((1+x)^{31}=\alpha x^j\) on the coset \(x^{31}=\gamma\).

If at least 18 strips existed, at most 13 coset points would be missed. Let \(Q\) be the monic product of their linear factors, padded with powers of \(x\) to degree 13. Then
\[
\big((1+x)^{31}-\alpha x^j\big)Q(x)\equiv0\pmod{x^{31}-\gamma}.
\]
Degrees \(14,\ldots,30\) receive no wrapped coefficients. For \(Q=\sum_t q_t x^t\), their equations are
\[
\sum_{t=0}^{13}\binom{31}{i-t}q_t=\alpha q_{i-j},
\]
with out-of-range coefficients set to zero. The earlier strip bound used the rows where the right side vanished. Here the other rows are retained by introducing five scaled copies \(Q_k=\alpha^k Q\). Each equation then links the coefficients of \(Q_k\) and \(Q_{k+1}\) by a **constant integer matrix**, independent of the target and coset.

For each \(j\), the replay certifies full column rank at every physical prime. After removing factors below 100, the gcd of the selected maximal minors is 1 except at \(j=6,25\), where it is \(2243\cdot28436731\). Neither factor is \(1\bmod961\). Thus the matrix forces \(Q=0\), contradicting monicity.

At zero target the scaling by \(T\) is unavailable, but the mixed reader has a simpler bound. Write \(Z=X^{31k}\). A hit requires \(X^{(1-31k)x}=-B/A\), which determines at most one full deep exponent because \(1-31k\) is a unit modulo \(31^2\). Depth \((2,0)\) also has at most one strip.

### Ordinary controls and exact replay

One integer target gives three strips for ordinary \(21143\) at the previously 21-capable slope \(j=11\), and two for ordinary \(86491\) in the opposite orientation at \(j=4\). Both observations are nonzero, and both sets consist of exact valuation-one strips. The code checks the rank certificate and the actual \(3,5\) chart independently.

```python
from math import comb, gcd, isqrt
from random import Random

r = 31
factors = (2243, 28436731)
for p in factors:
    assert all(p%d for d in range(2,isqrt(p)+1)) and p%961 != 1

def strip_small(n):
    for t in range(2,100):
        while n and n%t == 0:
            n //= t
    return n

def minor(rows):
    # Fraction-free elimination with row pivots selects a maximal minor.
    a = [row[:] for row in rows]
    n, prev = len(a[0]), 1
    for k in range(n):
        b = next((i for i in range(k,len(a)) if a[i][k]), None)
        if b is None:
            return 0
        a[k],a[b] = a[b],a[k]
        p = a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,n):
                a[i][j], rem = divmod(p*a[i][j]-a[i][k]*a[k][j], prev)
                assert rem == 0
        prev = p
    return abs(prev)

for j in range(1,r):
    rows = []
    for k in range(5):
        for i in range(14,31):
            linked = 0 <= i-j <= 13
            if k == 4 and linked:
                continue
            row = [0]*70
            row[14*k:14*k+14] = [comb(31,i-t) for t in range(14)]
            if linked:
                row[14*(k+1)+i-j] = -1
            rows.append(row)
    g, rng = 0, Random(31+j)
    expected = 2243*28436731 if j in (6,25) else 1
    for _ in range(8):
        g = gcd(g,minor(rows))
        if strip_small(g) == expected:
            break
        rng.shuffle(rows)
    assert strip_small(g) == expected

W, n = 26609383058821567214760, 218690032476506695564926720515
def S(x,y,m):
    return (pow(3,4+W*x,m) + pow(5,2+W*y,m)) % m

assert W%3960 == 0 and W%31
assert (n%32,n%3,n%31**3) == (3,2,1067)
assert all((n-S(0,0,p))%p for p in (3,7,11,19,23))
for i in range(r):
    assert [y for y in range(r) if S(i,y,r*r)==n%(r*r)] == [10*i%r]
    excluded = [[b for b in range(r)
                 if S(i+r*a,10*i%r+r*b,r**3)==n%r**3]
                for a in range(r)]
    assert all(len(v)==1 for v in excluded)
    assert len({v[0] for v in excluded}) == r

for p, deep, slope, j, T, expected in (
    (21143,3,10,11,14597,{(10,18),(14,14),(22,28)}),
    (86491,5,28,4,86391,{(9,27),(16,23)}),
):
    assert p%4==3 and all(p%d for d in range(2,isqrt(p)+1))
    shallow = 8-deep
    for b,e in ((deep,2),(shallow,1)):
        assert pow(b,p-1,p*p)!=1
        assert pow(b,W*r**e,p*p)==1 and pow(b,W*r**(e-1),p)!=1
    assert pow(shallow,W*slope*j,p)==pow(deep,W*r,p)
    assert n%(p*p)==T and T!=0
    hits = set()
    for i in range(r):
        for a in range(r):
            x,y = (i+r*a,10*i%r) if deep==3 else (i,10*i%r+r*a)
            if S(x,y,p)==T:
                assert S(x,y,p*p)!=T
                hits.add((i,a))
    assert hits==expected
```

This sharpens the conditional cover test. A density subtraction would still require a matched bound on the remaining stalled charts.

Independent BigInt verification used different deterministic row permutations and checked all 30 slopes and exact minor gcd residues. The two real ordinary strip sets and every excluded upper-cell permutation were also replayed independently.
