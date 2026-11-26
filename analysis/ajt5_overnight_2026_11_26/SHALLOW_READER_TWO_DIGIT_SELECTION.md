# Two-digit selection against shallow readers

This local criterion concerns an ordinary repair chart with accessible lower digits, not the unconditional density ledger. It is based on the equal-depth collapse law in EQUAL_DEPTH_REPAIR_LINE_COLLAPSE.md.

Fix the old head and non-p coordinates. Set G to the first source digits admitting at least one noncollapsed top line. The collapse law gives |G| >= p-2 outside whole-chart collapse. An old reader r is shallow when the p-parts of both orders modulo r are at most p. On the two-axis source repair equation the compensated first digit is affine in the free first digit x, with nonzero slope. Its reader shift is then f_r(x)=A xi^x+B eta^x modulo r, with both characters of order dividing p. A single nontrivial term gives injectivity. Coincident nontrivial characters do likewise unless the combined coefficient vanishes. With two distinct nontrivial characters, for each j!=0, the equation f_r(x+j)=f_r(x) determines (xi/eta)^x uniquely if it is solvable. Thus there are at most (p-1)/2 unordered equal-value pairs, and no fiber can contain k points with k(k-1)>p-1. Constant readers may reject the whole chart and must be reserved or handled separately.

Reserve at most one unresolved reader. If the sum of equal-value pairs in G at all other readers is strictly below |G|(|G|-1)/2, then a pair of first digits separates every other reader. For p=71 and |G|>=69, this sufficient bound allows 67 distinct-character readers, any number of injective readers, and one reserved reader. A designated nonconstant reader can instead be bypassed deterministically by deleting its rooted fiber before running the pair test.

For a uniform r-adic observation and fixed shifts differing to exact depth e, put a_r=1/(r+1) and J_r=(1-r^(-e))/(r+1); J_r=a_r for equal shifts. The joint odd-valuation probability equals J_r: precisely one direction of odd/even mismatch can occur past the common-depth ball, with mass r^(-e)/(r+1) per direction by the geometric sum. Distinct residues give J_r=0. A shallow reader has a fixed r-adic shift within a selected chart provided the higher p-digit changes are also made in steps divisible by all fixed non-p order periods (at every required r-adic precision). When the other retained rows pass the chosen probes, independence across unresolved reader primes gives exact probability that both charts are rejected by one or more readers:
1 - 2 product(1-a_r) + product(1-2a_r+J_r).
A union bound is J_reserved + sum_(r!=s) a_r a_s. If each selected chart has two distinct terminal shifts, any joint terminal failure is independently limited by the corresponding two-shift terminal bound. This conditional estimate does not establish chart access for the full charged terminal families or handle deeper unresolved readers.

At the actual 71-to-715823 target, the only collapsed lower coordinate at first digit zero can be replaced by coordinate 71; all first digits therefore admit a noncollapsed line. Reader 1279 has just four equal-value pairs, and on this target its only rooted digit is 50. The separate 59-to-2243 control gives two fixed probes at legal heads with the same reader residue modulo 827 and different lifts modulo 827². A single CRT target rejects both probes at that reader. It does not show that higher-depth repair options are unavailable in general.

```python
from collections import Counter
from math import isqrt, lcm, prod

H = 3960

def S(c, d, m):
    return (pow(3, c, m) + pow(5, d, m)) % m

def head(n, c, d, extra=()):
    w = (n-S(c, d, 32)) % 32
    a = w & -w
    return (a in (1, 2, 4, 8) and w//a % 4 == 1
            and (n-pow(5, d, 3)) % 3
            and all((n-S(c, d, r)) % r for r in (7, 11, 19, 23)+extra))

def ordinary(r):
    assert r % 4 == 3 and all(r % i for i in range(2, isqrt(r)+1))
    assert all(pow(b, r-1, r*r) != 1 for b in (3, 5))

def lift(n, c, d, x, p, h, L):
    # The controls use odd h, so the target valuation is h+1.
    P = p**h
    a, b = c+L*((x-c)*pow(L, -1, P) % P), d
    for i in range(h):
        u, m = L*p**i, p**(i+2)
        b += u*next(j for j in range(p) if n % m == S(a, b+u*j, m))
    m = p**(h+2)
    if n % m == S(a, b, m):
        b += L*P
    assert (n-S(a, b, m)) % m in range(p**(h+1), m, p**(h+1))
    assert (a-c) % H == (b-d) % H == 0 and a % P == x
    return a, b

p, q, r, n, c, d = 71, 715823, 1279, 2420068764704544, 10082, 45369
for a in (p, q, r):
    ordinary(a)
assert head(n, c, d) and r == 18*p+1 < 2*p*p+1
g, t = [pow(b, 18*pow(18, -1, p), r) for b in (3, 5)]
assert t != 1 and pow(t, 60, r) == g
f, g = [(pow(b, p-1, p*p)-1)//p for b in (3, 5)]
assert -pow(3, c, p)*f*pow(pow(5, d, p)*g, -1, p) % p == 41
L = lcm(H, p-1, 18, r)
R = [S(*lift(n, c, d, x, p, 1, L), r) for x in range(p)]
cnt = Counter(R)
assert [x for x in range(p) if R[x] == n % r] == [50]
assert max(cnt.values()) == 2
assert sum(v*(v-1)//2 for v in cnt.values()) == 4
assert (R[1], R[2]) == (195, 374)

P, M = p**3, p**4
assert pow(3, P, q) == 1 != pow(3, P//p, q)
t = pow(5, 2*pow(2, -1, P), q)
assert pow(t, P, q) == 1 != pow(t, P//p, q)
assert pow(t, 321174, q) == 3
U, V = [pow(b, (p-1)*pow(p-1, -1, P), M) for b in (3, 5)]
W = pow(V, 321174, M)
A, B = [pow(b, e*P*pow(P, -1, p-1), M) for b, e in ((3, c), (5, d))]
def F(x):
    return (A*pow(U, x, M) + B*pow(W, x, M)) % M
assert all(F(x) != n % M for x in range(1, p+1))
for x in (0, p, 1, 2, 50):
    pts = [lift(n, c, d, x+p*p*j, p, 3, L) for j in range(p)]
    assert all(head(n, a, b) and S(a, b, r) == R[x % p] for a, b in pts)
    assert len({S(a, b, q) for a, b in pts}) == (1 if x == 0 else p)

p, q, r, n = 59, 2243, 827, 1772213347634616708129
for a in (p, q, r):
    ordinary(a)
assert r == 14*p+1 and all(pow(b, 14, r) != 1 for b in (3, 5))
assert n % (p*p) == 1407 and n % (q*q) == q
L = lcm(H, 58, 38, 30, 42, 46, 14, r)
heads = (23, 8839)
for c in heads:
    assert head(n, c, 8817, (31, 43, 47))
    assert {S(*lift(n, c, 8817, x, p, 1, L), q) for x in range(p)} == {0}

pts = [lift(n, c, 8817, x, p, 1, L) for c, x in zip(heads, (43, 54))]
assert [S(*pt, r*r) for pt in pts] == [371227, 441522]
assert 441522-371227 == 85*r
M = 32*3*prod((7, 11, 19, 23, 31, 43, 47))*p**3*q**2
N = n+M*((731-n)*pow(M, -1, r*r) % (r*r))
for pt in pts:
    assert (N-S(*pt, r*r)) % (r*r) in range(r, r*r, r)
    assert (N-S(*pt, q*q)) % (q*q) in range(q, q*q, q)
    assert head(N, *pt, (31, 43, 47))
print("71 repeated-chart bypass and 59 shared-reader control verified")

# Independent finite distribution check: replace infinite parity by
# parity of the truncated valuation and compare with exact finite formula.
from fractions import Fraction
for r0 in (3,7):
    k=5
    M0=r0**k
    def odd_truncated(x):
        x%=M0
        v=0
        while v<k and x%r0==0:
            x//=r0
            v+=1
        return v%2
    for e in range(k):
        both=sum(odd_truncated(x)*odd_truncated(x-r0**e) for x in range(M0))
        exact=Fraction(1-Fraction(1,r0**e),r0+1)
        assert abs(Fraction(both,M0)-exact)<=Fraction(2,M0)
print("Joint valuation formula checked against finite residue counts")
```
