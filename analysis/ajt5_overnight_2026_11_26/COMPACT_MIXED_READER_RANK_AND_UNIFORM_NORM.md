# Compact mixed-reader rank test and a uniform cyclotomic norm bound

The \(31\)-sink certificate reduces from 70 columns to **at most 11**. The replacement is a rank test on the clean coefficient space. A separate norm argument gives a reusable theorem for every odd prime order \(r\). At \(r=7\), it gives a two-strip bound above the existing cutoff, and a small exact certificate gives the sharp bound of three over all physical primes.

### Replace the coefficient chain by a rank test

As before, \(r-h\) strips would give a nonzero polynomial \(Q=\sum_{t=0}^h q_t x^t\), padded to degree \(h\), with
\[
((1+x)^r-\alpha x^j)Q(x)\equiv0\pmod{x^r-\gamma}.
\]
Use degrees \(h+1,\ldots,r-1\), which receive no wrapped terms. Put the rows with \(i-j\notin[0,h]\) in a clean set \(I\). The other rows have the form \(Dq=\alpha Eq\), with \(E\) selecting coefficients \(q_{i-j}\).

There is a useful uniform reduction for \(h\le(r-3)/2\) and \(p>r+h\). The clean equations are equivalent to requiring that the degree-\(h\) polynomial
\[
U_q(s)=\sum_{t=0}^h q_t(s)_{\underline t}(r+h-s)_{\underline{h-t}}
\]
vanish on \(I\). The displayed polynomials form a basis by triangular evaluation at \(0,\ldots,h\). If \(d=h+1-|I|>0\), the clean space has dimension \(d\).

The available coordinates selected by \(E\) form an interval touching at least one end of \(0,\ldots,h\). The first \(d\) coefficients determine \(U_q\) by evaluation at \(0,\ldots,d-1\) and at \(I\). The last \(d\) do the same using \(r+h,r+h-1,\ldots,r+h-d+1\). Thus the corresponding block \(E_0\) is invertible on the clean space. In clean-space coordinates, set
\[
M=E_0^{-1}D_0,\qquad R=D_1-E_1M.
\]
A nonzero solution must satisfy \(Mv=\alpha v\) and \(Rv=0\). It is excluded if the stack \(R,RM,\ldots,RM^{d-1}\) has rank \(d\). Conversely, a deficient stack has an \(M\)-invariant kernel by Cayley–Hamilton, so the reduced pencil has an eigenvector over an algebraic closure. This equivalence concerns the coefficient equations. The original coset and root conditions impose further restrictions.

For \(r=31,h=13\), the compact check gives full rank at every physical prime \(p\equiv1\pmod{961}\). The only factors above 99 left in the selected minor gcds are \(2243\) and \(28436731\), at \(j=6,25\). Neither is \(1\bmod961\). This recovers the 17-strip cap with no prime search.

### A uniform norm bound and a matched use at \(r=7\)

Write a mixed reader as \(T=AX^x+BX^{rkx}\), where \(X\) has order \(r^2\), \(k\not\equiv0\bmod r\), and \(A,B,T\ne0\). Three hits have distinct lower digits. Translate the first hit to zero and let the other deep exponents be \(a,b\), with \(c=ka,\ d=kb\bmod r\). Then \(p\) divides the cyclotomic norm of
\[
F(\zeta)=(\zeta^a-1)(\zeta^{rd}-1)-(\zeta^b-1)(\zeta^{rc}-1),
\qquad \zeta=\zeta_{r^2}.
\]
The terms occupy three distinct classes \(0,a,b\bmod r\), so \(F(\zeta)\ne0\) by the degree-\(r\) extension over \(\mathbb Q(\zeta_r)\). In each class there are two monomials of opposite signs. The coefficient-square sum is 6, and the evaluations at nonprimitive roots vanish. Parseval and AM–GM bound the absolute norm by \((6r/(r-1))^{r(r-1)/2}\). Removing the norm of \((1-\zeta)(1-\zeta^r)\) gives the uniform necessary condition
\[
p\ \le\ \frac{(6r/(r-1))^{r(r-1)/2}}{r^{r+1}} .
\]

At \(r=7\), this threshold is \(7^{13}=96{,}889{,}010{,}407\), below the existing common-Wieferich cutoff \(B=9\cdot10^{14}\). Thus a **full frozen \(7\)-chart supplied only by earlier mixed common-Wieferich readers** requires at least 25 distinct readers. They must occupy \(99\bmod196\) above \(B\). The 25th possible position is \(900000000004827\), so a terminal at or below that value cannot have this earlier-reader cover. This matches the stated full-chart branch and gives no density subtraction. [Repair-chart hypotheses](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e) · [Published cutoff input](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)

The two-strip theorem is a large-prime theorem. For \(r=7\), the separate finite check below normalizes \(a=1\) and leaves 18 possible physical primes for a triple. At each it excludes four hits by fixing two hits and solving for \(B/A\). The ordinary \(3,5\) reader \(9311\) realizes three strips, so the all-prime bound of three is sharp. The replay also checks three actual strips at the ordinary \(31\)-reader \(21143\).

### Exact replay

```python
from fractions import Fraction as F
from math import comb, gcd, isqrt, lcm, prod
from random import Random

def core(n):
    for t in range(2,100):
        while n and n % t == 0:
            n //= t
    return n

def mul(A,B):
    return [[sum(x*y for x,y in zip(a,b)) for b in zip(*B)] for a in A]

def solve(E,D):
    d = len(E)
    A = [[F(x) for x in a+b] for a,b in zip(E,D)]
    for k in range(d):
        i = next(i for i in range(k,d) if A[i][k])
        A[k],A[i] = A[i],A[k]
        A[k] = [x/A[k][k] for x in A[k]]
        for i in range(d):
            if i != k:
                A[i] = [x-A[i][k]*y for x,y in zip(A[i],A[k])]
    return [a[d:] for a in A]

def minor(rows):
    A, prev = [a[:] for a in rows], 1
    d = len(A[0])
    for k in range(d):
        i = next((i for i in range(k,len(A)) if A[i][k]), None)
        if i is None:
            return 0
        A[k],A[i] = A[i],A[k]
        p = A[k][k]
        for i in range(k+1,len(A)):
            for j in range(k+1,d):
                A[i][j], rem = divmod(p*A[i][j]-A[i][k]*A[k][j],prev)
                assert not rem
        prev = p
    return abs(prev)

def compact(r,h,j):
    I = [i for i in range(h+1,r) if not 0<=i-j<=h]
    J = [i for i in range(h+1,r) if 0<=i-j<=h]
    d = h+1-len(I)
    if d <= 0:
        return 1
    if J[0] != j:
        J.reverse()
    def fall(x,t):
        return prod(range(x-t+1,x+1))
    Q = []
    for k in range(d):
        a = []
        for i in range(h+1):
            def G(t):
                return fall(i,t)*fall(r+h-i,h-t)
            a.append((prod(i-z for z in I)*i**k
                      -sum(a[t]*G(t) for t in range(i)))/F(G(i)))
        s = lcm(*(x.denominator for x in a))
        assert core(s)==1
        Q.append([int(x*s) for x in a])
    E = [[a[i-j] for a in Q] for i in J]
    D = [[sum(comb(r,i-t)*a[t] for t in range(h+1)) for a in Q] for i in J]
    M = solve(E[:d],D[:d])
    s = lcm(*(x.denominator for a in M for x in a))
    assert core(s)==1
    M = [[int(x*s) for x in a] for a in M]
    R = [[s*x-y for x,y in zip(a,b)] for a,b in zip(D[d:],mul(E[d:],M))]
    rows = []
    for _ in range(d):
        for a in R:
            f = gcd(*a)
            if f:
                a[:] = [x//(f//core(f)) for x in a]
        rows += R
        R = mul(R,M)
    g, rng = 0, Random(r+j)
    expected = 2243*28436731 if r==31 and j in (6,25) else 1
    for _ in range(12):
        g = gcd(g,minor(rows))
        if core(g)==expected:
            return core(g)
        rng.shuffle(rows)
    return core(g)

for p in (2243,28436731):
    assert all(p%t for t in range(2,isqrt(p)+1)) and p%961!=1
assert {j:g for j in range(1,31) if (g:=compact(31,13,j))!=1} == {
    6:2243*28436731, 25:2243*28436731}

def primes(n):
    k = 2
    while k*k <= n:
        if n%k == 0:
            yield k
            while n%k == 0:
                n //= k
        k += 1
    if n>1:
        yield n

# The exact small-order check, separate from the uniform bound.
exceptional = set()
for k in range(1,7):
    for b in range(1,49):
        if b%7 in (0,1):
            continue
        c,d = 7*k,7*(k*b%7)
        terms = ((1+d,1),(b+c,-1),(1,-1),(d,-1),(b,1),(c,1))
        v = [1]+[0]*48
        for u in range(1,49):
            if u%7:
                w = [0]*49
                for i,s in enumerate(v):
                    for e,t in terms:
                        w[(i+u*e)%49] += s*t
                v = w
        assert len({v[i] for i in range(1,49) if i%7})==1
        assert len({v[i] for i in range(7,49,7)})==1
        N, rem = divmod(abs(v[0]-v[7]),7**8)
        assert N and not rem
        exceptional.update(p for p in primes(N) if p%49==1)
assert len(exceptional)==18
for p in exceptional:
    e = (p-1)//49
    X = next(pow(g,e,p) for g in range(2,p) if pow(g,7*e,p)!=1)
    a = [pow(X,i,p) for i in range(49)]
    for k in range(1,7):
        b = [a[7*k*i%49] for i in range(49)]
        for j in range(1,49):
            if j%7:
                c = (1-a[j])*pow(b[j]-1,-1,p)%p
                T = (1+c)%p
                if T:
                    assert sum((x+c*y)%p==T for x,y in zip(a,b))<=3

for r,p,c,d,lam,W,n,want in (
    (7,9311,2,67,1,700559640,8284208475706275,{(2,0),(3,3),(6,6)}),
    (31,21143,4,2,10,26609383058821567214760,
     218690032476506695564926720515,{(10,18),(14,14),(22,28)}),
):
    def S(x,y,m):
        return (pow(3,c+W*x,m)+pow(5,d+W*y,m))%m
    assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
    assert W%3960==0 and W%r and n%p
    assert all(pow(b,r-1,r*r)!=1 for b in (3,5))
    for b,k in ((3,2),(5,1)):
        assert pow(b,p-1,p*p)!=1
        assert pow(b,W*r**k,p*p)==1 and pow(b,W*r**(k-1),p)!=1
    hits = set()
    for i in range(r):
        j, = [j for j in range(r) if S(i,j,r*r)==n%(r*r)]
        assert j==lam*i%r
        for a in range(r):
            if S(i+r*a,j,p)==n%p:
                assert S(i+r*a,j,p*p)!=n%(p*p)
                assert sum(S(i+r*a,j+r*b,r**3)==n%r**3
                           for b in range(r))==1
                hits.add((i,a))
    assert hits==want
```

Independent BigInt replay reproduced all 30 compact minor gcds using different row permutations, the 18 order-seven exceptional physical candidates, the exhaustive no-four-hit test on those candidates, the three-strip 9311 control, and the congruence-based earliest position. All cover limits refer only to the stated frozen-chart hypotheses.
