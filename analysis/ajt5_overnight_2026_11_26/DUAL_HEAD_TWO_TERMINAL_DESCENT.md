# Two terminals with preselected small-head classes

### Two-terminal descent with the original menu

Keep the two classes \((c_0,d_0),(c_1,d_0)\bmod3960\) selected from the small-head readings. In particular, \(c_0,c_1\) differ modulo each of \(3,5,11\). Assume every other required inert row above \(23\) is ordinary. The aim is a phase giving **units at both terminals** and passing the ordinary rows. [Preselected dual-head theorem](https://github.com/Samsen879/a303656/blob/4a33a5d51aa0e617fb108629f84b782beebd7977/analysis/ajt5_overnight_2026_11_26/DUAL_LOCKED_HEAD_UNIT_EXTENSION.md)

Among the active targets, take the largest prime \(s\) for which at least one order reads an \(s\)-primary digit beyond the mod \(3960\) lock. Temporarily remove every target that reads such a digit. If \(s>23\) is inert, add \(s\) as an auxiliary unit target, counting it only once. The largest free source strictly decreases. On restoring a step, vary one free \(s\)-digit on each axis. An affected target excludes at most \(s\) cells of this \(s\times s\) grid because its reading is injective along at least one axis. Since \(s\) is odd, two targets cannot cover the grid. The source itself stays a unit, or has no test if split. Ordinary rows above the released source can be repaired in increasing order using their own digits, which the active targets do not read.

Thus a shared maximal source, a split or small-head source, or a merger with a target already active reduces the problem to at most one target. The same shared-source argument works if “maximal” means the **numerically largest free prime power** \(s^a\). Vary its top digit. Other ordinary rows at primes \(p\le s^a\), \(p\ne s\), cannot read that digit since their orders divide \(p-1<s^a\). Rows above \(s^a\) can be repaired afterward.

If two targets remain when no free source is left, their orders divide \(3960\), hence divide \(990\) by inertness. The exact gcd
\[
\gcd(3^{990}-1,5^{990}-1)
=2^3\,11^2\cdot7\cdot19\cdot23\cdot31\cdot61\cdot67\cdot181
 \cdot199\cdot331\cdot661\cdot991
\]
leaves just **\(31,67,199,331,991\)** as possible pinned targets above \(23\). Both bases are ordinary at each. At any such target the two heads give distinct shifts, since the order of \(3\) has an odd factor in \(\{3,5,11\}\) and \(d_0\) is fixed. Each row therefore vetoes at most one head. **The exact additional relation at the pinned pair is that their allowed-head sets intersect.** Equivalently, the two rows must avoid vetoing opposite heads. This is a sufficient test for the original pair and an exact test at the pinned pair. [Earlier prime-power peeling](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/LOCKED_HEAD_MAX_PRIME_POWER_PEELING.md)

### True-base countercontrol

At \(n=1352683603486061699285433\), the two heads \((339,275)\) and \((11,275)\) meet the original head rules. They are held fixed throughout the replay.

| Head | Ordinary source | Source’s passing projection | Reader forced to zero |
|---|---:|---|---:|
| \((339,275)\) | \(31\) | \(j=12i+18\bmod31\) | \(2791\) |
| \((11,275)\) | \(67\) | \(j=16i+5\bmod67\) | \(19163\) |

The other reader is individually avoidable on each head. The failed unit at either reader can also be repaired to exact valuation two using that reader’s own coordinate. Thus the example defeats simultaneous **unit** avoidance in the fixed menu for ordinary readers. It gives no finite norm blocker or common Wieferich example.

```python
from itertools import product
from math import gcd, isqrt, lcm, prod

C, d, n = 3960, 275, 1352683603486061699285433
heads = (339, 11)
E = ((31,2791,339,12,18), (67,19163,11,16,5))

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

def prime(p):
    return p > 1 and all(p%j for j in range(2,isqrt(p)+1))

def order(b,p):
    return next(j for j in range(1,p) if pow(b,j,p)==1)

P = (2,7,11,19,23,31,61,67,181,199,331,661,991)
assert all(map(prime,P))
assert gcd(3**990-1,5**990-1) == 44*prod(P)
assert all(pow(b,p-1,p*p)!=1 for p in (31,67,199,331,991)
           for b in (3,5))
assert all(prime(p) and p%4==3 for p in (31,67,2791,19163))
assert [(order(3,p),order(5,p)) for p in (31,67,2791,19163)] == [
    (30,3),(22,22),(558,465),(737,1474)]
assert heads[0]%8 == heads[1]%8
assert all((heads[0]-heads[1])%p for p in (3,5,11))
for c in heads:
    assert (n-S(c,d,32))%32 == 1 and (n-pow(5,d,3))%3
    assert all((n-S(c,d,p))%p for p in (7,11,19,23))

for r,q,c,lam,j0 in E:
    assert n%q==0 and all(pow(b,q-1,q*q)!=1 for b in (3,5))
    for i,j in product(range(r),repeat=2):
        cc,dd = c+C*i,d+C*j
        line = (j-lam*i-j0)%r==0
        assert (n-S(cc,dd,r))%r==0
        assert ((n-S(cc,dd,r*r))%(r*r)==0)==line
        assert (S(cc,dd,q)==0)==line
    t,Q,*_ = next(e for e in E if e[0]!=r)
    dd = d+C*j0
    assert (n-S(c,dd,r**3))%r**3==r*r
    assert (n-S(c,dd,t))%t and (n-S(c,dd,Q))%Q

    B = lcm(C,30*31**2,66*67**2,558,465,737,1474,q-1)
    assert B%q
    c += B*next(i for i in range(q) if (n-S(c+B*i,dd,q*q))%(q*q)==0)
    if (n-S(c,dd,q**3))%q**3==0:
        c += B*q
    assert (n-S(c,dd,q**3))%q**3 in range(q*q,q**3,q*q)
    assert (n-S(c,dd,r**3))%r**3==r*r
    assert (n-S(c,dd,t))%t and (n-S(c,dd,Q))%Q
print("OK")
```

The result concerns finite local phases with the prescribed menu. It gives no new all-tail bound, density-one theorem, or pointwise conclusion.

The structural test here is sufficient for the initial terminals. If the two pinned rows veto opposite heads, it does not establish failure at the initial terminals. The replay shows why opposite vetoes cannot simply be dismissed for ordinary readers. The corresponding genuine common Wieferich case remains open.
