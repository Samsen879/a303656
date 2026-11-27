# Three-chart shallow-reader escape gives representation density above 99.999898657%

The exception-density bound improves to **below \(0.000101343\%\)**, from \(0.00011349889744333906\ldots\%\). A change to the small-head selection prevents a dual shallow reader from covering all three auxiliary charts. It applies to both \(D=81\) and \(D=243\), including terminals where only one axis reads the top digit. The cutoff and all three infinite tails stay in the exact ledger. [Pinned cube-repair predecessor](https://github.com/Samsen879/a303656/blob/64768956ad32075ae297d35e6a76ec08003d7385/analysis/ajt5_overnight_2026_11_26/ORDINARY_INERT_CUBE_DENSITY_BOUND.md)

| Charge, in \(10^{-11}\) of density | Pinned | Reference-chart occupancy | With the new three-chart saving |
|---|---:|---:|---:|
| \(D=81\) | 19,019 | 19,343 | **17,949** |
| \(D=243\) | 23,149 | 12,485 | **12,063** |
| **Total** | **42,168** | **31,828** | **30,012** |

For \(D=81\), I kept the previous reader envelopes and recovered the pinned joint-chart numerator in the replay. For \(D=243\), the reference-chart column applies separate shallow and deep occupancy using the same verified reader window through \(3456\). The final column isolates the additional saving from the new chart argument. [Previous joint-chart numerator](https://github.com/Samsen879/a303656/blob/904d8df47b00e3eacb3f000e5332628cfcfe4a54/analysis/ajt5_overnight_2026_11_26/JOINT_CHART_OCCUPANCY_DENSITY_BOUND.md)

### The small-head change

The head can require **\(c\not\equiv0\bmod3\) and \(d\equiv0\bmod3\)** while preserving the published parity choice. Start from the legal exponents modulo eight. Adjust \(d\) by a multiple of eight before reading the small inert rows. At \(7\), the three choices of \(c\) in steps of eight give three distinct shifts and three distinct classes modulo three. At most one choice fails the unit test, so a nonzero class remains. The subsequent steps \(24,72,360\) at \(19,11,23\) preserve it. Use this head globally. The inherited charges use its legality, its lock modulo \(3960\), and the published parity masses. [Small-head construction](https://github.com/Samsen879/a303656/blob/64768956ad32075ae297d35e6a76ec08003d7385/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

For \(D=3^{k+1}\), choose an axis \(b\) that actually reads depth \(k+1\) at the terminal. Vary its two released digits through nine choices and the auxiliary axis’s first released digit through three choices. Each auxiliary chart contains nine distinct terminal shifts on \(b\). If both terminal axes read depth \(k+1\), either orientation is valid and the smaller bound is available. Taking the maximum over orientations for the unconditional sum covers either terminal configuration.

A shallow reader on \(b\) has depth \(k\), so it can kill one whole prefix in each chart. A reader blind to the auxiliary digit can kill the same prefix across three charts. A reader that sees the auxiliary digit has a smaller footprint:

- If both reader depths equal \(k\), the nine prefix shifts have the form \(A\xi^i+B\zeta^j\), with both characters generating the order-three subgroup \(H\). A collision would give \(A/B\in \pm H\), by taking the ratio of two nonzero differences in \(H\). The head makes the \(3\)-part of \(A/B\) have order \(3^k\), so all nine shifts are distinct.
- If the auxiliary reader depth exceeds \(k\), three matches would use all three \(b\)-prefixes. The ratio of consecutive differences along that permutation is a primitive cube root. On the auxiliary side the ratio is \(\zeta\), whose order is at least nine. Thus there are at most two matches.

Consequently, **three shallow readers that hit different prefixes on the reference chart leave an entire prefix uncovered on another chart whenever at least one sees the auxiliary digit**. This holds for all six assignments of the three readers to the reference prefixes.

### Charging the escape

Drop the \(b\)-readers and the auxiliary-only readers, then choose the initial phase from the retained observations. If the initial phase passes the auxiliary-only rows on the reference chart, keep it as the reference. Otherwise choose an auxiliary-pass extension before reading the \(b\)-rows, if one exists. The reference-chart occupancy bound therefore still applies.

For the subtraction, require the auxiliary-only rows to pass on all three charts. Require exactly the designated three shallow hits on the reference chart, then reserve two shifts in an uncovered alternate prefix. Each other shallow row must avoid at most five specified odd-valuation events. Each deep row must avoid at most two. At \(w_p=1/(p+1)\le1/164\), the resulting product is at least
\[
\exp\!\left(-\frac{820}{159}L_\cup\right),
\]
where \(L_\cup\) bounds the weight of the **union** of reader sets. Both sets lie in the same progression \(p\equiv1\bmod3^k,\ p\equiv3\bmod4\). The replay certifies lower factors \(\lambda=1/3\) and \(59/100\), respectively. Events for different triples and assignments are disjoint because the three reference hits are exact.

Let \(M\) be the named shallow weight and \(x=s-M\) the unnamed shallow weight. For \(j=1,2,3\), let \(a_j\) be six times the sum of products over \(j\)-element named sets containing a dual reader. The amount subtracted from the reference bound is at least
\[
\lambda\left[
\frac{a_1}{2}(x^2-x/164)_+ + a_2x+a_3
\right].
\]
The first term uses the distinct-pair bound for the unnamed readers. The replay checks that the full numerator increases when padding \(s+t\) to its envelope and is maximized at the verified deep lower bound. It then uses the pinned maximal-order terminal kernels. [Maximal-order terminal envelopes](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/MAX_ORDER_RANKED_TERMINAL_DENSITY_BOUND.md)

**Real control.** At the ordinary terminal \(q=3727\), the actual depths are \((4,2)\). The same three older primes \(1999,2539,379\) kill all three reference prefixes in both fixtures. In an unrestricted legal head, the first two readers have opposite full matching masks. In a legal head with the new congruences, each hits only a single cell. The pure reader \(379\) keeps its full stripe. The replay checks exact valuation one at every displayed kill, and three distinct terminal shifts in the recovered prefix. The ordinary control lies below the cutoff.

### Standalone replay

The exact new total is the pinned total minus \(12156/10^{11}\), giving \(0.00010134289744333906\ldots\%\). The replay uses the existing reader window and preserves the prime-source, higher-power, and low-order tails explicitly.

```python
from fractions import Fraction as Q
from functools import cache
from itertools import combinations
from math import ceil, floor, isqrt, prod

W, Z, B = 10**11, 10**25, 9*10**14

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, u2 = series(Q(2))

@cache
def logs(n):
    y, j = Q(n), 0
    assert y >= 1
    while y >= 2:
        y /= 2
        j += 1
    l, h = series(y)
    return Q(floor(W*(l+j*l2)),W), Q(ceil(W*(h+j*u2)),W)

def lo(n): return logs(n)[0]
def hi(n): return logs(n)[1]
def up(x): return Q(ceil(W*x),W)
def prime(p): return p>1 and all(p%d for d in range(2,isqrt(p)+1))

def exp_lo(x,n):
    s = t = Q(1)
    for j in range(1,n):
        t *= Q(x,j)
        s += t
    return s

def v3(m):
    j = 0
    while m%3 == 0:
        m //= 3
        j += 1
    return j

def depth(p,b):
    m = p-1
    while m%3==0 and pow(b,m//3,p)==1:
        m //= 3
    return v3(m)

def coeff(k,named):
    terms = [
        6*sum(prod(w for p,w,d in group)
              for group in combinations(named,n)
              if any(d>=k for p,w,d in group))
        for n in (1,2,3)]
    return terms[0]/2,terms[1],terms[2]

a, w0 = Q(327,326), Q(1,164)

def U(s):
    z = a*s
    return z-z*z/2+z**3/6

def P(s,t):
    return s**3+9*s*s*t*t+18*s*t**5+9*t**8

@cache
def chart(D):
    k = v3(D)-1
    m = 3**k
    phi = 2*m//3
    V = ceil(Q(5*D,4)+u2)
    lam = Q(1,3) if D==81 else Q(59,100)
    rows = [(p,Q(1,p+1),depth(p,3),depth(p,5))
            for p in range(2*m+1,3457,4*m) if prime(p)]
    assert min(p for p,*_ in rows)>=163
    offset = lo(lo(Q(3456,4*m)))-Q(1,34)
    union = sum(w for p,w,d,e in rows if max(d,e)>=k)
    L_union = (hi(V)-offset)/phi+union
    assert Q(820,159)*L_union<lo(1/lam)
    stats = []
    for b in (3,5):
        data = rows if b==3 else [(p,w,e,d) for p,w,d,e in rows]
        named = [(p,w,e) for p,w,d,e in data if d==k]
        M = sum(w for p,w,e in named)
        t = sum(w for p,w,d,e in data if d>k)
        c = offset-phi*(M+t)
        if D==81:
            old_c = Q(47,50) if b==3 else Q(221,250)
            assert c>old_c
            c = old_c
        A,H,C = coeff(k,named)
        E,J = (lo(34)-c)/phi,(hi(V)-c)/phi
        lower,d = 1-a*J/2,a*(1-a*J)
        assert M+t<E and t<E/2 and a*J<1 and lam<lower**2*d
        # Along s=L-t, compare derivatives on t <= L/2.
        j = J/2
        c0 = 3*d-18*a*a*j-90*a**5*j**3/lower-72*a**8*j**5/lower**2
        rhs = lam*(2*A/(E/2)+max(0,H-2*A*M)/(E/2)**2)
        assert c0*lower**2>rhs
        # The endpoint t=tau dominates t >= L/2.
        coarse = a**3/8+9*a**4*J/16+18*a**6*J**3+9*a**8*J**5
        assert (lower*(1-t/E))**3-lam*(A/E+H/E**2+C/E**3)>coarse
        dual = sum(w for p,w,e in named if e>=k)
        stats.append((c,t,M,A,H,C,dual))
    return phi,V,lam,stats

def numerator(D,u,mode):
    phi,V,lam,stats = chart(D)
    if mode==0 and D==243:
        return ((hi(u)+Q(1,5))/phi)**3
    values = []
    for c,t,M,A,H,C,dual in stats:
        s = (hi(u)-c)/phi-t
        z = P(U(s),U(t))
        if mode==0:
            x = s-dual
            z -= Q(2,3)*(1-3*Q(53,250))*dual*max(0,x*x-w0*x)
        elif mode==2:
            x = s-M
            z -= lam*(A*max(0,x*x-w0*x)+H*x+C)
        values.append(z)
    return max(values)

def sym(xs):
    a = [1]+[0]*len(xs)
    for x in xs:
        for j in range(len(xs),0,-1):
            a[j] += x*a[j-1]
    return a

def max_power(p,D):
    x = p
    while x*p <= D:
        x *= p
    return x

def charge(D,mode):
    V = chart(D)[1]
    ps = [p for p in range(5,D+1,2) if prime(p)]
    ms = [max_power(p,D) for p in ps]
    C = [Q(0)]
    k = 2*D*prod(m//p for p,m in zip(ps,ms))*hi(3)/68
    for a in sym(ps):
        C.append(C[-1]+k*a)
    E = sym([Q(1,m-m//p) for m,p in zip(ms,ps)])
    M = 4*D
    lm = [logs(M)]
    for m in sorted(ms,reverse=True):
        M *= m
        lm.append(logs(M) if D==81 else (0,lm[-1][1]+hi(m)))
    phi = D-D//3

    def kernel(u,interval):
        if D==81:
            x = 1/exp_lo(u,161)
        else:
            z = 1 << (2*u+64)
            x = Q(ceil(z*Q(10**7,27182818)**u),z)
        if interval:
            x *= Q(2,3)
        v = [] if D==81 else [Q(ceil(10**30*C[-1]*x),10**30)]
        for j,(l,h) in enumerate(lm):
            if h>=u:
                break
            g = hi((u+1-l)/(u-h)) if D==81 and interval else 1/(u-h)
            A,F = C[j]*x,E[j]*g/phi
            v.append(A+F if D==81 else Q(ceil(10**30*A)+ceil(10**30*F),10**30))
        return min(v)

    return up(numerator(D,V,mode)*kernel(V,False)+sum(
        numerator(D,u+1,mode)*kernel(u,True) for u in range(34,V)))

rows = {D:[int(W*charge(D,j)) for j in range(3)] for D in (81,243)}
assert rows == {81:[19019,19343,17949],243:[23149,12485,12063]}
old = Q(sum(v[0] for v in rows.values()),W)
new = Q(sum(v[2] for v in rows.values()),W)

x = lo(B)+48*l2
def geom(v):
    return 1/(exp_lo(v*x,100)*(1-1/exp_lo(v*l2,12)))

root = Q(isqrt(floor(hi(3)*Z*Z/(4*x)))+1,Z)
low_tail = 70*(root*geom(Q(271,750))+geom(Q(323,375)))
prime_tail,power_tail = Q(1633,W),Q(7320,W)
predecessor = (Q(125047-39893,W)+Q(14,2**27)+prime_tail+power_tail
               +Q(891331308302981248,Z)+low_tail)
assert Q(113498,W)<predecessor<Q(113499,W)
answer = predecessor-old+new
assert answer==predecessor-Q(12156,W) and answer<Q(101343,W)

def good2(x):
    t = x&-x
    return t and t<=8 and (x//t)%4==1

head = ((7,8,3),(19,24,3),(11,72,5),(23,360,11))
for j,(p,L,k) in enumerate(head):
    assert len({pow(3,L*x,p) for x in range(k)})==k
    assert all(pow(3,L,q)==1 for q,_,_ in head[:j])
    assert all(pow(b,3960,p)==1 for b in (3,5))
    assert L%8==0 and (L%3==0 if j else L%3!=0)

q,L,d = 3727,2132727401874567960,15651
ps = (1999,2539,379)
assert L%3960==0 and v3(L)==2 and d%3==0
assert (depth(q,3),depth(q,5))==(4,2) and q-1==46*81
assert pow(3,9*L,q)==1!=pow(3,3*L,q) and pow(5,L,q)==1
assert all(prime(p) and p%4==3 for p in ps+(q,))
assert all(pow(b,p-1,p*p)!=1 for p in ps+(q,) for b in (3,5))
assert [(depth(p,3),depth(p,5)) for p in ps]==[(3,3),(3,3),(3,1)]

for c,n,want in (
    (15651,9963001358781466157276673,
     [{(0,0),(1,1),(2,2)},{(0,1),(1,0),(2,2)},{(2,0),(2,1),(2,2)}]),
    (15652,60487452760423778227296,
     [{(0,0)},{(1,0)},{(2,0),(2,1),(2,2)}])):
    def shift(i,j,m):
        return (pow(3,c+L*i,m)+pow(5,d+L*j,m))%m
    assert (n-pow(5,d,3))%3 and good2((n-shift(0,0,32))%32)
    assert all((n-shift(0,0,p))%p==1 for p,_,_ in head)
    for p,cells in zip(ps,want):
        kills = {(i,j) for i in range(9) for j in range(3)
                 if (n-shift(i,j,p*p))%(p*p) in range(p,p*p,p)}
        assert kills=={(i,j) for i in range(9) for j in range(3)
                       if (i%3,j) in cells}
    assert {i for cells in want for i,j in cells if j==0}=={0,1,2}
    assert len({shift(i,2,q) for i in (0,3,6)})==3

print(rows)
print("exception-density percent",float(100*answer))
```

The head choices are fixed using only the small-row observations. The unused-reader factor follows from the bound on five excluded readings per row: log(1−5w) ≥ −5w/(1−5w) ≥ −(820/159)w when w≤1/164. The comparison is between whole reference-hit events; reserving an alternate prefix uses the already determined three designated observations, not observations of the additional readers. The numerical replay preserves all previous charges outside the two revised classes. Neither density one nor pointwise representation is claimed.
