# An exceptional-prime obstruction affecting a whole quartic circle

Let p be inert odd, A,B,r be local units, Delta=r−B/r, k=v_p(Delta)>0, and H=(r+B/r)²−4A. For each local point X²+Y²=H, the usual angle construction has m=(X−r−B/r)/2, s=Y/Delta. Assume the formula is defined (m,s nonzero). The inert norm criterion implies X,Y and hence m are integral. If v_p(Y)<k, then sigma=v_p(s)<0. In the identity
```
2mQ(sv) = m²/s² + 2mrv² + s²(1+v²)(B+r² v²)
```
the last summand has valuation 2*sigma+4*min(0,v_p(v)) because B≡r² mod p and −1 is nonsquare. It strictly dominates both other terms, so Q cannot be integral. An integer anchor must therefore have v_p(Y)≥k. If v_p(H)<2k, this forces H to be a square in Q_p (remove the smaller even valuation of X² and use the odd-prime unit square criterion). Consequently a nonsquare H at that depth excludes the **entire circle**, not just a chosen slope or an anchor parameter.

The previously proposed u=23 genuine label, with h lifted from six local requirements, trips this condition at p=251: Delta is divisible by 251 and H is a nonsquare unit. The direct replay below verifies the six-condition integer choice and the four forbidden h classes. It does not exclude other h outside those classes. Rechoosing h can resolve this fixed obstruction but may introduce other exceptional primes, so no full growth statement follows.

```python
p, u = 251, 23
h, M = 0, 1
for q, a in ((2, 1), (3, 2), (5, 1), (7, 1), (11, 1), (13, 4)):
    mod = q**20
    h += M * ((a - h) * pow(M, -1, mod) % mod)
    M *= mod
d, c = 24*u + 10, 8*u + 4
A = (pow(5, d, p) + pow(3, c, p) - 131779) % p
B = (pow(5, d+1, p) + pow(3, c+1, p) - 658897) * pow(5, -1, p) % p
L = (4*A - 2*B) % p
r = (h + L*pow(h, -1, p)) * pow(2, -1, p) % p
H = ((r + B*pow(r, -1, p))**2 - 4*A) % p
assert (h % p, A, B, r, H) == (28, 124, 154, 107, 120)
assert r*r % p == B and pow(H, (p-1)//2, p) == p-1
assert [x for x in range(1, p)
        if (x**4 + (2*L-4*B)*x*x + L*L) % p == 0] == [28, 65, 186, 223]
```
