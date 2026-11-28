# Two exact cross-phase controls for finite inert-prime panels

The fixed target from [#90](https://github.com/Samsen879/a303656/pull/90) is
\[
N=3^{540}+5^{270}+7986363.
\]
Its original even-\(c\) phase cannot yield a true norm: \(N\equiv1\bmod4\), so the positive residual is \(3\bmod4\) for every even \(c\). The finite-panel conclusion is unaffected.

## Fixed target, different global minima within one actual phase

Consider \(c=5+18u,d=200+9v\) with \(u,v\ge0\), and the finite panel \(\{7,11,23\}\). The exact ordinary-height window is \(0\le u\le29,0\le v\le18\) because \(3^{527}+5^{362}<N<\min(3^{545},5^{371})\). The entire infinite phase retains residue 17 modulo 19, residue 1 modulo 4, and valuation 2 or 0 at 3 (by residues 9 and 5 modulo 27). Sorting the 570 positive candidates by the actual shift shows that the first all-unit point is rank 18, \((c,d)=(5,209)\), but the first even-valuation point is rank 7, \((113,200)\), with valuations \((2,0,0)\). The unit-minimal candidate fails at 67 to valuation one. The even-minimal residual is \(3^2 7^2\cdot39929\cdot C\), with \(39929=100^2+173^2\). The remaining 251-digit \(C\) is composite by an exact Fermat witness. Full trial division found no factor of \(C\) up to \(10^7\). Neither compositeness nor the search bounds determine whether it is a genuine sum of two squares.

## A different native phase with permanent obstruction

Take \(L=1514205\), \(c=Lu,d=3+Lv\), and \(N_+=3^L+5^{L+3}+R\) for \(R=2598605506848708=19349568^2+47161422^2\). Let \(N_-=N_++33649\). Each target has exactly the four ordinary-height candidates \((u,v)\in\{0,1\}^2\), since \(N_-<127\cdot5^L<\min(3^{2L},5^{2L+3})\). At \(N_+\) the point \((1,1)\) is a genuine norm. At \(N_-\) all four parity classes, hence every point of the entire infinite phase, have exact valuation one at at least one of \(7,19,23\). This follows from the residue table in the replay, because both step powers are signs modulo the corresponding squares. The \((0,1)\) parity class has 19 as its only obstruction from this panel, \((1,0)\) only 23, and \((1,1)\) only 7; each prime is essential. Throughout this phase 11 is a unit, not an obstruction. The claim does not extend to unrelated phases or rule out a Sun representation of \(N_-\).

## Exact replay


```python
from math import isqrt

P = (7, 11, 23)
N = 3**540 + 5**270 + 7986363

def val(n, p):
    assert n > 0
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e

def shift(c, d):
    return 3**c + 5**d

assert shift(527, 362) < N < min(3**545, 5**371)
rows = sorted((shift(c, d), c, d)
              for c in range(5, 545, 18) for d in range(200, 371, 9))
assert len(rows) == 570
assert (N % 27, pow(5,200,27), pow(5,209,27), pow(5,18,27)) == (7,25,2,1)
assert pow(3,18,19) == pow(5,9,19) == 1
for s, c, d in rows:
    r = N-s
    assert val(r,3) in (0,2) and r % 19 == 17 and r % 4 == 1

u = next(i for i,(s,c,d) in enumerate(rows) if all((N-s) % p for p in P))
e = next(i for i,(s,c,d) in enumerate(rows)
         if all(val(N-s,p) % 2 == 0 for p in P))
assert (u+1, rows[u][1:]) == (18, (5,209))
assert (e+1, rows[e][1:]) == (7, (113,200))
R = N-rows[e][0]
assert tuple(val(R,p) for p in (3,7,11,19,23,39929)) == (2,2,0,0,0,1)
assert 39929 == 100**2+173**2

B = 10**7
sieve = bytearray(b"\1")*(B+1)
sieve[:2] = b"\0\0"
for p in range(2,isqrt(B)+1):
    if sieve[p]:
        sieve[p*p::p] = b"\0"*len(sieve[p*p::p])
assert sum(sieve) == 664579
assert [(p,val(R,p)) for p in range(2,B+1) if sieve[p] and R%p==0] == [
    (3,2), (7,2), (39929,1)]
C = R//(3**2*7**2*39929)
assert C%4 == 1 and len(str(C)) == 251 and pow(2,C-1,C) != 1

L, T = 1514205, 2598605506848708+33649
pairs = ((0,0),(1,0),(0,1),(1,1))
expected = {7:(48,48,[28,30,33,35]), 11:(1,1,[82]*4),
            19:(360,1,[95,97,95,97]), 23:(1,528,[345,345,66,66])}
for p,(a,b,row) in expected.items():
    m = p*p
    assert (pow(3,L,m),pow(5,L,m)) == (a,b)
    n = (a+125*b+T) % m
    assert [(n-pow(a,u,m)-125*pow(b,w,m))%m for u,w in pairs] == row

def hit(p, i):
    r = expected[p][2][i]
    return r%p == 0 and r != 0

assert [any(hit(p,i) for p in P) for i in range(4)] == [True,True,False,True]
assert all(any(hit(p,i) for p in (7,19,23)) for i in range(4))
Rplus=2598605506848708
assert 19349568**2+47161422**2==Rplus
assert (N-shift(5,209))%(67*67)==58*67
assert L >= 9 and 3**33 > T and 9**9 > 127*5**9
```
