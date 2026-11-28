# Positive and negative certificates in the 570-point native phase

Use exactly the fixed target and odd-\(c\) phase from [#100](https://github.com/Samsen879/a303656/pull/100):
\[
N=3^{540}+5^{270}+7986363,\qquad
c=5+18u,\quad d=200+9v,\qquad 0\le u\le29,\quad0\le v\le18.
\]
The phase contains exactly 570 positive residuals \(R_{c,d}=N-3^c-5^d\). Sort them by increasing actual shift \(3^c+5^d\); ranks below are one-based.

**There are ten certified actual two-square residuals.** In particular, rank 19 has \((c,d)=(23,209)\), with square coordinates
\[
\begin{aligned}
a&=\text{599897200366067856329526934199224695322220806134214082693321720455211399614784968069852428907134472952975626257745763245963297714},\\
b&=\text{286669866991340395471136606258910668277187414441475385063186268622794227145581448166532975043313964296564389381268813176748259071}.
\end{aligned}
\]
The least actual shift giving a two-square residual is therefore at rank 7, 14 or 19. Ranks 7 and 14 remain undecided. Rank 18, the earlier minimum for the all-unit three-row panel, is rigorously excluded by valuation one at 67. For ranks below 19 other than 7, 14 and 18, valuation one at 7 is enough.

## Complete bounded obstruction panel

For each residual, the replay processes every prime \(p\equiv3\bmod4\) up to \(10^8\) in increasing order. At each hit it verifies the exact valuation; odd valuation is a genuine obstruction, since \(-1\) is nonsquare at \(p\). Products of consecutive prime blocks are used only to skip blocks coprime to the product of all currently unclassified residuals. Within a nontrivial block the exact valuations are computed individually. Every negative classification gives an explicit least such prime and odd valuation, not merely a failed search for coordinates.

| Prime panel | Exact exclusions |
| --- | ---: |
| \(\{7,11,23\}\) | 304 |
| primes \(\le10^2\) | 338 |
| primes \(\le10^5\) | 412 |
| primes \(\le10^7\) | 431 |
| primes \(\le62,262,922\) | 439 |
| primes \(\le62,262,923\) | 440 |
| primes \(\le10^8\) | 440 |

Here 100 distinct least obstruction primes cover these 440 points. The last new exclusion is rank 343 with valuation one at 62,262,923. Of the 130 not excluded by the panel, ten direct positive certificates verify exact integer identities; **120 points remain unclassified**. There is no claim about any other phase or target.

The Python replay uses roughly 100 MB for its sieve. The construction of positive coordinates uses known partial factors and the Euclidean square-root procedure but accepts a positive claim only after rechecking the full integer square identity. No large-index primality assumption is needed.

```python
from hashlib import sha256
from math import gcd, isqrt, prod

N = 3**540 + 5**270 + 7986363
rows = sorted((3**c + 5**d, c, d)
              for c in range(5, 528, 18) for d in range(200, 363, 9))
assert len(rows) == 570 and rows[-1][0] < N < min(3**545, 5**371)
assert all(x[0] < y[0] for x, y in zip(rows, rows[1:]))
R = [N-s for s, _, _ in rows]

def val(r, p):
    e = 0
    while r % p == 0:
        r //= p
        e += 1
    return e

def product(xs):
    if len(xs) < 32:
        return prod(xs)
    k = len(xs)//2
    return product(xs[:k])*product(xs[k:])

B = 10**8
prime = bytearray(b"\1")*(B+1)
prime[:2] = b"\0\0"
for p in range(2, isqrt(B)+1):
    if prime[p]:
        prime[p*p::p] = b"\0"*len(prime[p*p::p])

first = [None]*len(R)
left = set(range(len(R)))
union = product(R)
for lo in range(3, B+1, 32768):
    ps = [p for p in range(lo, min(lo+32768, B+1), 4) if prime[p]]
    common = gcd(union, product(ps))
    if common == 1:
        continue
    before = len(left)
    for p in ps:
        if common % p:
            continue
        for i in list(left):
            e = val(R[i], p)
            if e % 2:
                first[i] = (p, e)
                left.remove(i)
    if len(left) != before:
        union = product([R[i] for i in left])

panel = sorted({hit[0] for hit in first if hit})
assert len(left) == 130 and len(panel) == 100
assert sum(any(val(r, p) % 2 for p in (7, 11, 23)) for r in R) == 304
assert first[342] == (62262923, 1)
assert [i+1 for i in range(19) if first[i] is None] == [7, 14, 19]
assert first[17] == (67, 1)
assert all(first[i-1]==(7,1) for i in range(1,18) if i not in (7,14))
assert rows[18][1:] == (23,209)
a0 = 599897200366067856329526934199224695322220806134214082693321720455211399614784968069852428907134472952975626257745763245963297714
b0 = 286669866991340395471136606258910668277187414441475385063186268622794227145581448166532975043313964296564389381268813176748259071
assert a0*a0+b0*b0+rows[18][0] == N
encoded = " ".join(f"{p[0]}:{p[1]}" if p else "-" for p in first)
assert sha256(encoded.encode()).hexdigest() == (
    "4aff20bb4260d790a5551a3ea463fdac13264f4c5a1a2aca786e4b318a770318")
# 每个元素对应一个按实际移位排序的位点。None 表示截至 B 未排除。
for lim, expected in [(10**2,338),(10**5,412),(10**7,431),(62262922,439),(62262923,440),(10**8,440)]:
    assert sum(p is not None and p[0]<=lim for p in first)==expected

def squares(m):
    k = isqrt(m)
    if k*k == m:
        return 0, k
    assert m % 4 == 1
    for g in range(2, 100):
        t = pow(g, (m-1)//4, m)
        if t*t % m == m-1:
            break
    else:
        raise AssertionError(m)
    u, v = m, t
    while v*v > m:
        u, v = v, u % v
    w = isqrt(m-v*v)
    assert v*v + w*w == m
    return v, w

factors = {19: [], 76: [17, 353], 209: [], 296: [],
           312: [9, 49, 17], 349: [81761, 1089133],
           374: [53, 617, 1481], 410: [1542217], 509: [], 534: [1091561]}
for i, fs in factors.items():
    assert first[i-1] is None
    cofactor, remainder = divmod(R[i-1], prod(fs))
    assert remainder == 0
    a, b = 1, 0
    for m in fs + [cofactor]:
        v, w = squares(m)
        a, b = a*v-b*w, a*w+b*v
    s, c, d = rows[i-1]
    assert a*a + b*b + s == N
    print(i, c, d, abs(a), abs(b))

```
