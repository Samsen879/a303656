# Distinct-reader charging gives representation density above 99.999909087%

The finite factorial allowance can be replaced by a class-wise bound **below \(1.564\times10^{-25}\)** in density units. The resulting exception-density upper bound is **below \(0.000090913\%\)**, with the exact rational replay evaluating to \(0.0000909120846076457\ldots\%\). This removes almost the entire \(14/2^{27}\) allowance and preserves the cutoff and all three infinite tails. The bound applies to growth-box misses and hence to all-exponent exceptions. [Pinned three-chart predecessor](https://github.com/Samsen879/a303656/blob/64e66c0720e2fbde33c2ee1ceb2ae34ba0458191/analysis/ajt5_overnight_2026_11_26/THREE_CHART_SHALLOW_DENSITY_BOUND.md)

### Remaining charges

The disjoint predecessor charges, in units of \(10^{-11}\) of density, were:

| Component | Charge |
|---|---:|
| Finite prime-\(D\) subtotal | 40,008 |
| \(D=81\) | 17,949 |
| \(D=243\) | 12,063 |
| Finite factorial allowance | 10,430.813 |
| Finite low order | 8,913.313 |
| Higher-power tail | 7,320 |
| Other finite higher powers | 2,978 |
| Prime-source tail | 1,633 |
| Low-order tail | 47.772 |

The next individual finite classes after \(81\) and \(243\) are \(20771\) at 1,648, \(729\) at 1,516, and \(127\) at 1,059. The factorial allowance gives the largest saving certified here. After its replacement, \(D=81\) remains the largest individual charge.

### Distinct readers give a smaller sum

For fixed retained observations, each dropped reader \(p\) can kill at most one of the \(r\) variants. The chance of killing a specified variant is \(w_p=1/(p+1)\). The variants are fixed before the dropped observations are read, so for any specified \(k\) variants the probability of killing them all is at most
\[
k!\,e_k((w_p)_p)\ \le\ \left(\sum_p w_p\right)^k .
\]
Here the factorial counts bijections from a set of \(k\) distinct reader primes to the \(k\) variants. For a robust chart that loses \(r-1\) variants, there are \(r\) choices of the lost set. The auxiliary branch must lose all \(r\) and has just one such set. This gives the class-wise bounds
\[
R_D\,r S_D^{r-1},
\qquad
R_D\, S_D^r
\]
for the two parts of the old allowance. The second applies only at \(D=r\) for a doubly ordinary inert source. The later cube-specific auxiliary charges are already in their own rows and stay there. [Original allowance and auxiliary branch](https://github.com/Samsen879/a303656/blob/64e66c0720e2fbde33c2ee1ceb2ae34ba0458191/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md) · [Distinct-reader bound](https://github.com/Samsen879/a303656/blob/64e66c0720e2fbde33c2ee1ceb2ae34ba0458191/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_NINE_PHASE_DENSITY_BOUND.md)

The replay sums the six source primes below \(53\) directly over the existing finite cutoffs. For \(r\ge53\), monotonicity gives \(R_D\le S_D<1/10\), and \(53^4>10^6\) leaves at most three charged powers per source, including \(D=r\). Summing \(3r10^{-r}+10^{-r-1}\) over all integers \(r\ge53\) bounds the rest of this **finite allowance** by \(1.772\times10^{-51}\). The \(D=29\) class supplies over 99% of the replacement bound.

**Real control.** At the ordinary terminal \(q=2791\) with \(D=31\), the actual older readers \(311\) and \(683\) each kill one variant. For \(n=1695726231599621889\) their kill sets are \(\{4\},\{7\}\). For \(n=2161263885617279649\) they are \(\{4\},\{4\}\). Thus two reader hits can remove two terminal shifts or just one. The replay checks the exact valuations, the legal head, and the distinct surviving terminal shifts. Both terminal Wieferich tests fail. [Earlier \(2791\) control](https://github.com/Samsen879/a303656/blob/a476e9ca22a16358c763229700f7bf07a9f5212b/analysis/ajt5_overnight_2026_11_26/WHOLE_REPAIR_LINE_DENSITY_BOUND.md)

### Standalone replay

The script reconstructs the exact pinned sum, replaces only \(14/2^{27}\), and checks the two controls. It uses the existing finite cutoffs and the geometric bound above, with no extended prime scan.

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt, lcm

B, P, H, W, Z = 9*10**14, 10**5, 10**6, 10**11, 10**25

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, u2 = series(Q(2))

def logs(n):
    y, j = Q(n), 0
    while y >= 2:
        y /= 2
        j += 1
    l, h = series(y)
    return Q(floor(W*(l+j*l2)),W), Q(ceil(W*(h+j*u2)),W)

def hi(n):
    return logs(n)[1]

def prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))

def envelopes(r,D):
    phi = D-D//r
    S = (hi(D)+Q(1,2))/phi
    l,h = logs(4*D)
    U,V = Q(4*D,3)-h,34-h
    assert U > V > 0
    R = min(S,(1/U+hi((Q(4*D,3)-l)/V))/phi)
    return S,R

roots = (29,31,37,41,43,47)
assert roots == tuple(r for r in range(29,53) if prime(r))
rows = []
for r in roots:
    total, D = Q(0), r
    ordinary = all(pow(b,r-1,r*r)!=1 for b in (3,5))
    while D <= (P if D==r else H):
        S,R = envelopes(r,D)
        cost = r*S**(r-1)
        if D==r and r%4==3 and ordinary:
            cost += S**r
        total += R*cost
        D *= r
    rows.append(total)

# Geometric upper bound for the remaining finite classes.
x = Q(1,10)
assert (hi(53)+Q(1,2))/52 < x and 53**4 > H
rest = x**53*(3*(53/(1-x)+x/(1-x)**2)+x/(1-x))
replacement = sum(rows)+rest
assert Q(0) < replacement < Q(1564,10**28)
assert rows[0] > Q(99,100)*replacement

def exp_lo(x,n):
    s = t = Q(1)
    for j in range(1,n):
        t *= x/j
        s += t
    return s

t = logs(B)[0]+48*l2

def geom(v):
    return 1/(exp_lo(v*t,100)*(1-1/exp_lo(v*l2,12)))

root = Q(isqrt(floor(hi(3)*Z*Z/(4*t)))+1,Z)
low_tail = 70*(root*geom(Q(271,750))+geom(Q(323,375)))
prime_tail, power_tail = Q(1633,W), Q(7320,W)
finite = Q(125047-39893-12156,W)
assert finite == Q(40008+17949+12063+2978,W)
low_finite = Q(891331308302981248,Z)
allowance = Q(14,2**27)
predecessor = finite+allowance+low_finite+low_tail+prime_tail+power_tail
answer = finite+replacement+low_finite+low_tail+prime_tail+power_tail
assert Q(101342,W) < predecessor < Q(101343,W)
assert answer == predecessor-allowance+replacement
assert answer < Q(90913,W)

r,q,c,d = 31,2791,1,3
ps = (311,683)
L = lcm(3960,r-1,(q-1)//r,*(p*(p-1)//r for p in ps))
assert q-1==2*3**2*5*r and L%r
assert all(prime(p) and p%4==3 for p in (r,q)+ps)
assert all(p<q for p in (r,)+ps)
assert all(pow(b,p-1,p*p)!=1 for p in (r,q)+ps for b in (3,5))
assert pow(3,r*L,q)==1 and pow(3,L,q)!=1
assert all(pow(3,r*L,p*p)==1 and pow(3,L,p)!=1 for p in ps)
assert c%3 and d%3==0

def shift(i,m):
    return (pow(3,c+L*i,m)+pow(5,d,m))%m

def crt(pairs):
    n,m = 0,1
    for a,p in pairs:
        n += m*((a-n)*pow(m,-1,p)%p)
        m *= p
    return n

for wanted,expected in (((4,7),1695726231599621889),
                        ((4,4),2161263885617279649)):
    small = (7,11,19,23,r)
    n = crt([(0,3),(1,32)]+[((shift(0,p)+1)%p,p) for p in small]
            +[((shift(i,p*p)+p)%(p*p),p*p) for i,p in zip(wanted,ps)])
    assert n==expected
    assert (n-shift(0,32))%32==1 and (n-pow(5,d,3))%3
    assert all((n-shift(i,p))%p==1 for p in small for i in range(r))
    masks = [{i for i in range(r) if
              (n-shift(i,p*p))%(p*p) in range(p,p*p,p)} for p in ps]
    assert masks == [{i} for i in wanted]
    survivors = [i for i in range(r) if all(i not in m for m in masks)]
    assert len({shift(i,q) for i in survivors}) == r-len(set(wanted))

print("replacement in density units",float(replacement))
print("exception density percent",float(100*answer))
```

This replacement concerns only the finite allowance. The high-order source tails already account for charges beyond the finite cutoffs, and are preserved. The injection estimate can also be proved by summing directly over ordered distinct tuples, bounded above by all ordered tuples; it does not treat reader outcomes within one row as independent. The independently rerun control distinguishes exact valuation-one kills on two different labels from overlapping kills on one label. The pointwise conjecture and density one remain open.
