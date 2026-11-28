# One exact finite phase table, four different true minima

**The four-outcome comparison holds on the exact #109 phase.** I independently constructed four distinct targets with the same 570 positive rows and the same **7,410 exact inert-prime valuations** as the original \(N\). Their true minimum ranks are **7, 14, 19, and \(\infty\)**. The last target has a primitive representation at \((c,d)=(3,199)\), outside the phase. The four controls here are distinct explicit targets; the replay is standalone. [Public phase and rank ordering in #109](https://github.com/Samsen879/a303656/pull/109/files)

### Original \(N\)

The **primitive minimum is exactly rank 19**, at \((23,209)\). For \(d=200+9v\), the residual modulo \(27\) is \(7-25(-1)^v\), so its \(3\)-valuation is exactly \(2\) when \(v\) is even and zero otherwise. The first 17 ranks all have \(v=0\). Rank 18 has \(67\)-valuation exactly \(1\). Thus the unit tests at \(3\) and \(67\) eliminate every earlier rank.

At rank 19 let \(m=N-3^{23}-5^{209}\). Exact modular exponentiation gives \(t=2^{(m-1)/4}\bmod m\) with \(t^2\equiv-1\pmod m\). The lattice \(x\equiv ty\pmod m\) has determinant \(m\), is invariant under quarter-turns, and every squared length is a multiple of \(m\). In a Gauss-reduced basis, if \(A\le B\) are the squared lengths and \(D\) is the dot product, then \(m^2=AB-D^2\ge3A^2/4\). Hence \(A=m\). A vector of that length and its quarter-turn span the lattice, so its coordinates are coprime because the lattice contains \((t,1)\). The replay obtains the exact square identity without a primality assumption.

A primitive two-square residual is a unit at every inert prime. Therefore **every finite inert-prime unit panel containing \(3,67\) has minimum rank 19** at the original \(N\). Two rows are necessary to attain that minimum because the rank-7 and rank-18 residuals are coprime. The unrestricted two-square minimum of the original \(N\) remains among ranks \(7,14,19\).

### Standalone replay

The constructed positive targets are within \(N(1+10^{-71})\), and the negative target is within \(N(1+10^{-28})\). The old panel leaves 232 points. On the negative target each of those has exact valuation one at an inert prime between 103 and 1699. The script checks the ordinary window, every table entry, each earlier-rank exclusion, and the primitive outside-phase identity.

```python
from math import gcd, isqrt

N = 3**540 + 5**270 + 7986363
S = sorted(3**(5+18*u) + 5**(200+9*v)
           for u in range(30) for v in range(19))
assert len(S) == len(set(S)) == 570
assert S[-1] < N < 2*N < min(3**545, 5**371)
assert [S[i-1] for i in (7, 14, 18, 19)] == [
    3**113+5**200, 3**239+5**200, 3**5+5**209, 3**23+5**209]

def val(r, p):
    e = 0
    while r % p == 0:
        r //= p
        e += 1
    return e

def inert(lo, hi):
    return [p for p in range(lo, hi+1, 4)
            if all(p % q for q in range(2, isqrt(p)+1))]

P, Q = inert(3, 100), inert(103, 1699)
def table(n):
    return [tuple(val(n-s, p) for p in P) for s in S]

profile = table(N)
alive = [i for i, row in enumerate(profile) if not any(e % 2 for e in row)]
assert len(P) == 13 and len(alive) == 232

def norm(v):
    return v[0]**2 + v[1]**2

m = N-S[18]
assert m % 4 == 1
t = pow(2, (m-1)//4, m)
assert (t*t+1) % m == 0
u, v = (m, 0), (t, 1)
while True:
    if norm(u) > norm(v):
        u, v = v, u
    a = norm(u)
    d = u[0]*v[0] + u[1]*v[1]
    if abs(2*d) <= a:
        break
    q = (2*d+a)//(2*a)
    v = (v[0]-q*u[0], v[1]-q*u[1])
assert norm(u) == m and gcd(*u) == 1
assert all((N-s) % 3 == 0 for s in S[:17])
assert val(N-S[17], 67) == 1
assert gcd(N-S[6], N-S[17]) == 1

# Rank 0 encodes the outside-phase witness for the negative control.
controls = [
    (7,
     664873118457859565327991287081559533294912222632819802610568135499305600668784919365319313221911244639111016975024324268533927672,
     249917388931110500203509217547148492045651732597),
    (14,
     664873118457859565327991287081559533294912222632819802610568135499305600668787325395184659356157397847834893530262809500725269680,
     2776591473796693852763044201612646874425721214728525),
    (19,
     664873118457859565327991287081559533294912222632819802610568135499305601050439378277861567422247641941698514328112638430483088585,
     750474001842591705906603384214402054911180501619351892234),
    (0,
     659317497025380820110242342462906291166424009015447026116022365605554059517281332335130595305896001852682859147752060721817703998,
     85771217573647112396855782177859859068156934762045783121476260256463953283508381857132748353371096060270972142292083897947832063),
]
seen = {N}
for rank, a, b in controls:
    shift = S[rank-1] if rank else 3**3 + 5**199
    n = shift + a*a + b*b
    assert N < n < 2*N and n not in seen
    assert (n-N)*(10**71 if rank else 10**28) < N
    seen.add(n)
    assert table(n) == profile
    stop = rank-1 if rank else len(S)
    for i in alive:
        if i < stop:
            r = n-S[i]
            assert any(r % p == 0 and r % (p*p) != 0 for p in Q)
    if rank in (0, 19):
        assert gcd(a, b) == 1
    print(rank or "infinity")
```

The common table determines the finite-panel minimum, which is rank 7 for all four targets. The exact square identities and the additional odd valuations certify the four different true minima.
