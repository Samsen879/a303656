# Cyclotomic determinant limits at the 31-sink

A cyclotomic norm bounds **every doubly deep reader at the \(31\)-sink by 62 rejected repairs**, down from 173, independently of either order cofactor. An aligned reader rejects at most 31. Under the [verified short-cofactor exclusion](THIRTY_ONE_SINK_SHORT_COFACTOR_EXCLUSION.md) and the \(961\) prime-power cap, these bounds therefore apply to all remaining long-cofactor readers. A full cover by doubly deep readers alone requires at least **465 distinct primes**, or **930** if all are aligned. [Predecessor capacities](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

### The order-31 invariant

Let \(\omega\) have order \(r=31\) in \(\mathbf F_p^\times\), and fix nonzero \(A,B,T\). Three distinct hits of
\[
A\omega^x+B\omega^y=T
\]
would have distinct coordinates on each axis. Translate the first pair to \((0,0)\) and write the other two as \((a,c),(b,d)\). Eliminating the coefficients gives \(F(\omega)=0\), where
\[
F(z)=(z^a-1)(z^d-1)-(z^b-1)(z^c-1).
\]

For a primitive complex \(31\)st root \(\zeta\), \(F(\zeta)\ne0\). Otherwise a complex affine map would send the three distinct unit-circle points \(1,\zeta^a,\zeta^b\) to \(1,\zeta^c,\zeta^d\). The image circle would be the same circle, and the map fixes 1, so the map would be the identity. Then \(a=c,\ b=d\bmod31\), and the first two finite-field hits would differ by multiplication by \(\omega^a\ne1\), forcing \(T=0\).

Consequently \(p\) divides the nonzero norm \(N(F(\zeta))\). Each difference is divisible by \(1-\zeta\), so \(31^2\) also divides the norm. Reduce the six signed monomials modulo \(z^{31}-1\). Their coefficient squares sum to at most 14. One sign can have a triple collision and the other at most a double, since simultaneous triples force \(b=c=2a,\ a=d=2b\), hence \(3a=0\bmod31\). Parseval, \(F(1)=0\), and AM–GM now give
\[
p\le\frac{|N(F(\zeta))|}{31^2}
  \le\frac{(14\cdot31/30)^{15}}{31^2}
  <264730350241189.
\]
This is below the existing \(9\cdot10^{14}\) catalogue cutoff. The published finite input is used only to put every genuine common-Wieferich reader above the three-hit threshold. [Dorais–Klyve, §4.1 and Tables 2, 5–6](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)

### What this forces on a full repair chart

Assume the other coordinates are frozen, both \(31\)-digits are available on both axes, and the reader observations are nonzero modulo their respective physical primes. The full chart has 31 lower-digit pairs, each with 930 legal upper-digit pairs.

| Reader depths | Maximum rejected repairs |
|---|---:|
| Shallow, with at least one active axis | 1,860 |
| \((2,0)\) or \((0,2)\) | 30 |
| \((2,1)\) or \((1,2)\) | 930 |
| \((2,2)\) | 62 |
| Aligned \((2,2)\) | 31 |

A shallow reader hits at most two lower pairs by the norm bound. A doubly deep reader hits at most two upper pairs above each lower pair by the same bound. A mixed reader strikes one row or column per lower pair. With depths \((2,0)\), the constant axis makes a hit determine the whole deep exponent, so only one lower pair can be struck.

The mixed-reader strips give a stronger joint test. In a lower pair missed by all shallow readers, if \(u\) rows and \(v\) columns survive the mixed readers, at least \(uv-\min(u,v)\) legal cells remain. Each doubly deep reader can remove at most two of them. For example, at most 15 shallow readers leave some lower pair untouched. Even 15 mixed readers on each axis leave at least 240 cells there, requiring at least **120 doubly deep readers**.

For the alignment test, write the frozen multipliers as \(X=3^U,Y=5^V\bmod p\), both of order \(31^2\), and the lower repair line as \(y\equiv\lambda x+\mu\bmod31\). If \(X^{31}=Y^{31\lambda}\), the ratio \(Y^y/X^x\) takes at most 31 values on the chart. Each ratio gives at most one hit at nonzero \(T\). For a common-Wieferich prime the alignment equality lifts to \(p^2\), since two \(31\)st roots of unity that agree modulo \(p\) also agree modulo \(p^2\). Thus an aligned exact order pair \((d_3,d_5)\) must satisfy
\[
p^2\mid\gcd\!\left(\Phi_{d_3}(3),\Phi_{d_5}(5),3^{31U}-5^{31V\lambda}\right).
\]

These are deterministic restrictions on a full-chart cover. Zero observations and unavailable digits remain outside the argument. The counts give no matched density subtraction on their own.

### Independent replay

The ordinary \(683\) control realizes three nonzero shallow hits and has normalized norm \(683\cdot9641\). The ordinary \(640027\) control has actual cofactors \((666,222)\), aligns on the real slope-28 chart modulo \(p\), and fails the lift modulo \(p^2\). Both checks use actual powers of 3 and 5. Sufficiently large translates preserving the checked congruences give positive remainders on the finite charts.

```python
from math import isqrt

r, B = 31, 9 * 10**14
num, den = (14*r)**15, (r-1)**15*r*r
assert num // den == 264730350241188 and num < B*den

def terms(a,b,c,d):
    return ((a+d,1),(b+c,-1),(a,-1),(d,-1),(b,1),(c,1))

# Scale the first nonzero difference to 1.
energy = 0
for b in range(2,r):
    for c in range(1,r):
        for d in range(1,r):
            if c != d:
                f = [0]*r
                for e,s in terms(1,b,c,d):
                    f[e%r] += s
                energy = max(energy, sum(z*z for z in f))
assert energy == 14

def S(c,d,W,x,y,m):
    return (pow(3,c+W*x,m) + pow(5,d+W*y,m)) % m

for p in (31,683,640027):
    assert p%4 == 3 and all(p%k for k in range(2,isqrt(p)+1))
    assert all(pow(b,p-1,p*p) != 1 for b in (3,5))
assert [pow(5,p-1,p*p) for p in (11,1006003)] == [78,31695130519]

p,W,n = 683,3960,22241446170263907
pts = [(4,1),(19,28),(24,6)]
assert n%32 == 3 and n%p == 436
for x,y in pts:
    assert y == 8*x%r
    for q,h in ((3,0),(7,0),(11,0),(19,0),(23,0),(r,2),(p,1)):
        m = q**(h+1)
        R = (n-S(2,11,W,x,y,m)) % m
        assert R and R%q**h == 0
Y = pow(5,W,p)
assert Y == 67 and pow(Y,r,p) == 1 and pow(Y,20,p) == pow(3,W,p)
F = terms(21,28,27,5)
assert sum(s*pow(Y,e,p) for e,s in F)%p == 0
v = [1]+[0]*(r-1)
for k in range(1,r):
    w = [0]*r
    for i,z in enumerate(v):
        for e,s in F:
            w[(i+k*e)%r] += s*z
    v = w
assert len(set(v[1:])) == 1 and v[0]-v[1] == r*r*p*9641

p,W,n = 640027,146520,26447836475
assert p-1 == 2*9*r*r*37 and W%3960 == 0 and W%r
for b,d in ((3,640026),(5,213342)):
    assert (p-1)%d == 0 and pow(b,d,p) == 1
    assert all(pow(b,d//t,p) != 1 for t in (2,3,31,37) if d%t == 0)
    assert d//(r*r) > 81 and W%(d//(r*r)) == 0 and pow(b,W*r,p) != 1
assert (pow(3,W*r,p*p)-pow(5,28*W*r,p*p))%(p*p) == 114538*p
R = n-3**6-5**2
assert R%(r**3) and R%r**2 == 0 and R%p**2 and R%p == 0
assert R%4 == 1 and all(R%t for t in (3,7,11,19,23))
hits = []
for i in range(r):
    good = [j for j in range(r) if (n-S(6,2,W,i,j,r*r))%(r*r) == 0]
    assert good == [28*i%r]
    for a in range(r):
        for b in range(r):
            x,y = i+r*a,good[0]+r*b
            if (n-S(6,2,W,x,y,r**3))%(r**3) and S(6,2,W,x,y,p) == n%p:
                hits.append((x,y))
assert hits == [(0,0)]
assert 465*62 == 930*31 == r*r*(r-1)
```

Independent BigInt replay confirmed the coefficient-energy maximum, norm threshold, exact ordinary 683 determinant norm, and the unique legal hit on the ordinary 640027 aligned chart.
