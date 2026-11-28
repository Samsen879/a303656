# Four distinct true minima behind 17,100 exact valuation readings

**The four outcomes now share 17,100 exact valuation entries.** On the same 570-row #109 phase, there are four distinct targets with identical valuations to the original \(N\) at every inert prime through **263**. Their true minimum ranks are **7, 14, 19, and \(\infty\)**. All four targets lie in \((N,5N/4)\). A second negative target has the same table and a primitive representation at \((3,199)\), outside the phase. This extends the [earlier 7,410-entry quartet](https://github.com/Samsen879/a303656/pull/116) and exceeds the 16,530-entry negative-only comparison. [Public #109 phase and ordering](https://github.com/Samsen879/a303656/pull/109/files)

### Joint exclusion and its limit

The common panel leaves 212 rows. Among the first 19 ranks it leaves exactly \(7,14,19\). For the rank-14 control, prime \(271\) excludes rank 7. For the rank-19 control, **one prime, \(547\), excludes both** ranks 7 and 14. The two earlier shifts are \(142\bmod547\), while the rank-19 shift is \(61\bmod547\). The earlier residuals are \(186\cdot547\) and \(402\cdot547\bmod547^2\), so both valuations are exactly one.

The complete list of inert primes that can jointly obstruct the two earlier ranks is \(7,19,43,127,547,883\). Both shifts use \(d=200\), so any common obstruction prime other than 3 must divide \(3^{126}-1\). The replay verifies the factorization after removing those inert factors and verifies a square root of \(-1\) modulo the remaining odd cofactor. This certifies that the cofactor has no inert prime divisor. **At cutoff 883**, both early ranks still pass the original table, and any target with that same table through 883 and rank-19 minimum needs at least two distinct new obstruction primes. Their product is at least \(887\cdot907=804509\). This is a lower bound on the extra CRT modulus contributed by those primes. The largest cutoff certified here for all four outcomes is 263.

For the negative control I fixed the old table only through each prime’s maximum valuation, then avoided the next digit at rows attaining that maximum. The same parameter also retained the odd-valuation hits from 65 coarse CRT rows. Nine remaining rows were excluded after choosing the parameter. The first negative certificate needs only primes through \(293659\). The two earlier ranks of the **original** \(N\) remain unresolved.

### Exact replay

The script uses only the Python standard library. It checks all 17,100 entries for each target, verifies every required exclusion, and checks the outside-phase primitive identity.

```python
from math import gcd, isqrt, prod

N = 3**540 + 5**270 + 7986363
S = sorted(3**(5+18*u) + 5**(200+9*v)
           for u in range(30) for v in range(19))
top = min(3**545 + 5**200, 3**5 + 5**371)
assert len(S) == len(set(S)) == 570 and S[-1] < N < 17*N < top

def inert(B):
    a = bytearray(b"\1")*(B+1)
    a[:2] = b"\0\0"
    for p in range(2, isqrt(B)+1):
        if a[p]:
            a[p*p::p] = b"\0"*len(a[p*p::p])
    return [p for p in range(3, B+1, 4) if a[p]]

def v(r, p):
    e = 0
    while r % p == 0:
        r //= p
        e += 1
    return e

def one(r, p):
    return r % p == 0 and r % (p*p) != 0

P = inert(263)
def table(n):
    return [tuple(v(n-s, p) for p in P) for s in S]

T = table(N)
live = [i for i, row in enumerate(T) if all(e % 2 == 0 for e in row)]
assert len(P) == 30 and len(live) == 212
assert [i+1 for i in live if i < 19] == [7, 14, 19]

positives = [
    (7,
     664873118457859565327991287081559533294912222632819802610646386668871944469188529801364194536465377719584694148454857215224948256,
     3569578162035926717027009500285023408275459223739166956122872837458947),
    (14,
     664873118457859565327991287081559533294912222632819805955786731505603082452133733163225664750033803307658036607065990398968964560,
     107794536558026433249531186357907367666546662333951182292803366753549333843),
    (19,
     664873118457859565327991287081559533294912222632819810102978917226609709234756142705379023917134976394073809596193657871490133313,
     7179783549946059529599535691577825469288801457116883036759243076124401955418),
]
seen = {N}
for rank, a, b in positives:
    n = S[rank-1] + a*a + b*b
    assert N < n and 4*n < 5*N and table(n) == T and n not in seen
    seen.add(n)
    q = 271 if rank == 14 else 547
    assert all(one(n-S[i], q) for i in live if i < rank-1)

neg = 543388467635283658255883246041453066990683435993718638164104042564801951630237816054305538573817828337784723559720622535825542108445729973116776096189997356832330938654078569450249720628325005836816679779823825629226738662411570195755031002716132583541117437
assert N < neg and 4*neg < 5*N and neg not in seen and table(neg) == T

a = 1427315607818552094354906413176084670792621715045161268393785615120117076970301265377716439300897464047240566650344460822063712401
b = 2270276708193891662071853484388137652648444531659714963647612190112244165150134319959893734789545128483626042838790578230314220318
outside = 3**3 + 5**199 + a*a + b*b
assert gcd(a, b) == 1 and N < outside < 17*N and table(outside) == T

Q = [p for p in inert(778223) if p > 263]
for n, bound in ((neg, 293659), (outside, 778223)):
    witnesses = [next(p for p in Q if one(n-S[i], p)) for i in live]
    assert max(witnesses) == bound

I = (7, 19, 43, 127, 547, 883)
K = 66683474480736247602981080295133144348562709601
t = 53380471264114540189148926390202641915028824791
assert set(I) <= set(inert(883))
assert 3**126 - 1 == 8*7*prod(I)*K and (t*t+1) % K == 0
assert all(v(N-S[i], p) % 2 == 0 for i in (6, 13) for p in inert(883))
assert [p for p in inert(907) if p > 883] == [887, 907]
print('PASS 17100 entries per target and all exact exclusions')
```
