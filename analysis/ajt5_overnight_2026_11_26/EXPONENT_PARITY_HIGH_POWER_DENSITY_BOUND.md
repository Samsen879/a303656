# Exponent parity in the high-power tail gives representation density above 99.985824%

**The exception-density bound drops below \(0.014176\%\)** without broadening the search. The high-power tail is the larger certified saving. Its charge falls from \(0.0000424113940244\ldots\) to \(0.00000007320\) in density units. The \(D=81\) charge carries forward. [Predecessor certificate](https://github.com/Samsen879/a303656/blob/904d8df47b00e3eacb3f000e5332628cfcfe4a54/analysis/ajt5_overnight_2026_11_26/JOINT_CHART_OCCUPANCY_DENSITY_BOUND.md)

| Charge, in density units | Previous | Revised |
|---|---:|---:|
| \(D=81\) | \(0.00009636386\) | same |
| High-power tail \(D>10^6\) | \(0.0000424113940244\ldots\) | \(0.00000007320\) |
| All other charges and inherited slack | \(0.0000453190484003\ldots\) | same |
| **Total** | **\(0.0001840943024247\ldots\)** | **\(0.0001417561084003\ldots\)** |

### Why two heads do not automatically clear a shallow reader

There is an exact ordinary control with \(p=3187\), \(q=4051\), and two legal heads \((8,55),(480,55)\bmod3960\). The \(c\)-values differ modulo each of \(3,5,11\), and both terminal axes read the released digits. Nevertheless, at the same integer \(n=2819999481783\), reader \(3187\) kills the prefix \(\{0,3,6\}\) on **both** heads. This persists across all three auxiliary choices in the replay.

The two reference shifts agree modulo \(p\) and differ modulo \(p^2\). Their joint odd-valuation probability under a Haar observation is exactly \((p-1)/(p(p+1))\), close to the single-head probability \(1/(p+1)\). For the common root modulo \(p\), \(p-2\) lifts give valuation one at both shifts. Each of the other two lifts gives valuation one at one shift and a further odd-valuation test at the other. This rules out a blanket two-head discount based only on the small-head distinctions. A conditional discount would need to check the actual reader shifts in the retained extensions. The control uses ordinary primes and establishes no genuine blocker.

### Reprice the high-power tail by exponent parity

For \(D=r^a>10^6\), the repair depth on base \(b\) is \(d=a-1+v_r(b^{r-1}-1)\). The existing argument charges at most \(r^{-\lceil d/2\rceil}\) for odd \(d\). For even \(d\), all but one of the repaired phases have even valuation, so the charge gains a factor at most \(2^{2-r}\). Indeed, at least \(r-2\) distinct reader kills are needed, and the existing reciprocal envelope gives \(3rS_D/(r-2)<1/2\) in this range. [Published even-depth repair bound](https://github.com/Samsen879/a303656/blob/904d8df47b00e3eacb3f000e5332628cfcfe4a54/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

The source-depth charge vanishes for the pinned small sources and the split sources. For the other sources:

- **Odd \(a\):** use \(r^{-(a+1)/2}\). Integrate cubes from \(r=100\), and sum the odd exponents \(a\ge5\) geometrically before integrating over \(r\ge31\).
- **Even \(a\), both axes ordinary:** use \(r^{-a/2}2^{2-r}\).
- **Even \(a\), either axis nonordinary:** use \(r^{-a/2-1}\). A nonordinary axis has \(d\ge a+1\), and an ordinary axis gains \(2^{2-r}\le1/r\). The replay verifies that such inert sources above \(23\) must exceed \(20000\), using a subinterval of the existing \(r\le10^5\) scan. Above \(20000\), the estimate allows every source to be nonordinary.

Multiplying by \(R_D\le \tfrac32(\log D+1/2)/D\) gives the integrals below. The reader-cover part of the high-power tail remains charged in full. [Previous high-power tail](https://github.com/Samsen879/a303656/blob/904d8df47b00e3eacb3f000e5332628cfcfe4a54/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COVER_TREE_DENSITY_BOUND.md)

### Standalone rational replay

```python
from fractions import Fraction as Q
from math import ceil, isqrt

W,H = 10**11,10**6

def log_series_upper(y):
    z = (y-1)/(y+1)
    return (2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
            + 2*z**25/(25*(1-z*z)))

u2 = log_series_upper(Q(2))
def hi(x):
    y,k = Q(x),0
    while y>=2:
        y /= 2
        k += 1
    return Q(ceil(W*(log_series_upper(y)+k*u2)),W)

def prime(p):
    return p>1 and all(p%j for j in range(2,isqrt(p)+1))

assert all(pow(b,r-1,r*r)!=1
           for r in range(31,20001,4) if prime(r) for b in (3,5))

L = hi(H)+Q(1,2)
assert Q(3*31,29)*Q(3,2)*L/H < Q(1,2)
readers = Q(81,8)/H**2*(L**3/2+3*L*L/4+3*L/4+Q(3,8))
old = Q(27,20)/H*(2*(hi(2*H)+Q(1,2))+2*u2)+readers

# Upper integral of (A log(x)+B)/x**k from X to infinity.
def I(X,k,A,B):
    return ((A*hi(X)+B)/(k-1)+A/Q((k-1)**2))/X**(k-1)

cubes = Q(3,2)*I(100,5,3,Q(1,2))
z = Q(1,31**3)
odd = Q(3,2)*I(30,8,5/(1-z)+2*z/(1-z)**2,Q(1,2)/(1-z))
even = Q(3,2)*Q(1,2**28)*(2*hi(31)*z/(1-z)**2+Q(1,2)*z/(1-z))
z = Q(1,20000**3)
rare = Q(3,2)*I(20000,4,2/(1-z)**2,Q(1,2)/(1-z))
new = Q(ceil(W*(readers+cubes+odd+even+rare)),W)
assert new==Q(7320,W)
answer = Q(9204715121236751,50000000000000000000)-old+new
assert answer<Q(14176,10**8)

# Ordinary two-head control.
p,q,n,C,L,d = 3187,4051,2819999481783,3960,3723053400,55
heads = (8,480)
def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

assert prime(p) and prime(q)
assert all(pow(b,r-1,r*r)!=1 for r in (p,q) for b in (3,5))
assert all((heads[1]-heads[0])%r for r in (3,5,11))
assert L%C==0 and heads[0]%8==heads[1]%8
assert all(pow(b,9*L,q)==1 and pow(b,3*L,q)!=1 for b in (3,5))
assert pow(3,L,p*p)==1 and pow(5,3*L,p*p)==1!=pow(5,L,p)
x,y = [S(c,d,p*p) for c in heads]
assert (x-y)%p==0 and (x-y)%(p*p)!=0
for c in heads:
    assert (n-S(c,d,4))%4==1 and (n-pow(5,d,3))%3
    assert all((n-S(c,d,r))%r for r in (7,11,19,23))
    for j in range(3):
        killed = [i for i in range(9)
                  if (n-S(c+L*j,d+L*i,p*p))%(p*p) in range(p,p*p,p)]
        assert killed==[0,3,6]

print("OK:",float(100*answer),"%")
```

The replay gives \(0.014175610840032295\ldots\%\). It replaces only the high-power tail and retains the full \(D=81\) charge. The result bounds growth-box misses and hence all-exponent exceptions.

The odd \(a\ge5\) terms begin at power \(r^{-8}\) in the summand after multiplying the source charge by \(R_D\), and are bounded by a geometric series in \(r^{-3}\). The even nonordinary terms begin at \(r^{-4}\) by the same calculation. In the ordinary even case the sum of \(2^{2-r}\) over all integers \(r\ge31\) is \(2^{-28}\); all remaining factors can be bounded at \(r=31\) by monotonicity. This deliberately overcounts the actual prime powers and keeps the reader-cover tail in full.
