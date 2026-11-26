# Whole affine repair lines give representation density above 99.93346%

**The exception-density upper bound drops below \(0.06654\%\)**, using the same search cutoff. The largest charge in the previous certificate was the finite depth-one term, \(0.00053076061\) in density units. Using the whole repaired affine line lowers it to \(0.00032230937\).

| Charge | Previous | Revised |
|---|---:|---:|
| Finite depth-one term | 0.00053076061 | 0.00032230937 |
| All other finite and infinite charges, including inherited rounding slack | 0.00034308939 | 0.00034308939 |
| **Total upper bound** | **0.00087385000** | **0.00066539876** |

The calculation carries forward the published rational threshold \(0.00087385\) and replaces just one summand. In particular, it retains the improved \(D=81\) term, both tails, and the other compensation charges. [Previous density certificate](https://github.com/Samsen879/a303656/blob/a7232f58d5beb92a71da1df5f1c831ecdf2f2660/analysis/ajt5_overnight_2026_11_26/DISTINCT_SHALLOW_READER_DENSITY_BOUND.md)

### Charge losses on the whole repair line

Use the published depth-one setup. At source \(r\), both bases are ordinary, the terminal \(q\) reads at most one \(r\)-digit on either axis, and at least one axis is read. Choose the starting phase without reading \(n_r\) or the observations of the dropped older readers. A collision at \(r\) occurs with probability \(1/r\). It gives \(r\) repaired phases on the first-digit line \(j=s_0+\lambda i\). The next digit makes the valuation exactly two and is invisible at \(q\). At most one intercept \(s_0\) gives constant terminal shifts. [Published depth-one compensation](https://github.com/Samsen879/a303656/blob/a7232f58d5beb92a71da1df5f1c831ecdf2f2660/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md)

On a nonconstant line, a terminal shift has at most
\[
K_r=\left\lfloor\frac{1+\sqrt{4r-3}}2\right\rfloor
\]
preimages. The one-axis and equal-character nonconstant cases are injective. In the distinct-character case, write the shift as \(Az+Bz^m\) on the order-\(r\) subgroup. In a fiber, any specified nonidentity ordered ratio \(z'/z=\rho\) occurs at most once. The two equations determine \(z,z^m\), since their determinant has the nonzero factor \(\rho^m-\rho\). A fiber of size \(k\) therefore satisfies \(k(k-1)\le r-1\). [Affine-line fiber bound](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/LOCKED_HEAD_MAX_PRIME_POWER_PEELING.md)

A first blocker at \(q\) requires the older rows to kill at least \(r-K_r\) of the repaired phases. Otherwise two old survivors have different shifts modulo \(q\), and at least one gives a unit at \(q\). Conditional on the retained observations and \(n_r\), each phase is killed by the dropped rows with probability at most their reciprocal weight sum \(S\). Thus the expected number of killed phases is at most \(rS\), with no independence assumption between phases. Markov gives the new source-depth charge
\[
E_r(S)=\frac1{r^2}
 +\left(\frac1r-\frac1{r^2}\right)
   \min\!\left(1,\frac{rS}{r-K_r}\right).
\]
The two coefficients account for disjoint intercept cases. If there is no constant intercept, this expression is still an upper bound. The terminal probability factor is applied afterward by conditioning on all older observations. The two other compensation branches and sources where either axis is nonordinary use their previous charges.

### Standalone replay

The replay uses the same finite interval \(r\le10^5\), the same outward-rounded \(S,R\) envelopes, and the previous strict rational threshold. The ordinary control at the end has one genuine double fiber, so the replay also checks that injectivity cannot simply be assumed.

```python
from collections import Counter
from fractions import Fraction as Q
from math import ceil, floor, isqrt

W, P = 10**11, 10**5

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2,u2 = series(Q(2))
def logs(x):
    y,k = Q(x),0
    while y>=2:
        y /= 2
        k += 1
    a,b = series(y)
    return Q(floor(W*(a+k*l2)),W), Q(ceil(W*(b+k*u2)),W)

def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)

flags = bytearray(b"\x01")*(P+1)
flags[:2] = b"\x00\x00"
for r in range(2,isqrt(P)+1):
    if flags[r]:
        flags[r*r::r] = b"\x00"*((P-r*r)//r+1)

old = new = Q(0)
for r in range(31,P+1,4):
    if not flags[r]:
        continue
    l,u = logs(4*r)
    S = (hi(r)+Q(1,2))/(r-1)
    R = min(S,(1/(Q(4*r,3)-u)
               +hi((Q(4*r,3)-l)/(34-u)))/(r-1))
    E0 = E1 = Q(1,r)
    if all(pow(b,r-1,r*r)!=1 for b in (3,5)):
        K = (1+isqrt(4*r-3))//2
        assert K*(K-1)<=r-1<K*(K+1)
        E0 = min(E0,Q(1,r*r)+min(1,2*S)/r)
        E1 = Q(1,r*r)+(Q(1,r)-Q(1,r*r))*min(1,Q(r,r-K)*S)
    assert E1<=E0
    old += up(R*E0)
    new += up(R*E1)

assert (old,new)==(Q(53076061,W),Q(32230937,W))
answer = Q(87385,10**8)-old+new
assert answer==Q(66539876,W)<Q(6654,10**7)

n,c,d,r,q,C = 89577491769,3,275,31,2791,3960
def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p

assert (n-S(c,d,32))%32==1 and (n-pow(5,d,3))%3==1
assert all((n-S(c,d,p))%p==1 for p in (7,11,19,23))
assert all(pow(b,r-1,r*r)!=1 and pow(b,q-1,q*q)!=1 for b in (3,5))
assert all(pow(b,C*r,q)==1 and pow(b,C,q)!=1 for b in (3,5))
assert pow(5,24*C,q)==pow(3,2*C,q)

fibers = Counter()
for i in range(r):
    x,y = c+C*i,d+C*(24*i%r)
    assert (n-S(x,y,r*r))%(r*r)==0
    before = S(x,y,q)
    if (n-S(x,y,r**3))%r**3==0:
        y += C*r
    assert (n-S(x,y,r**3))%r**3 in range(r*r,r**3,r*r)
    assert S(x,y,q)==before
    fibers[before] += 1
assert sorted(fibers.values())==[1]*29+[2]
print("OK:", float(100*answer), "%")
```

The bound applies to the growth-box miss density and hence to the all-exponent exception density. The control terminal \(2791\) is ordinary. The proof uses no assumed genuine exceptional examples and gives no density-one or pointwise conclusion.

The finite replacement is only for the rooted, depth-one, doubly ordinary source branch from the linked compensation result. The phases on the repaired line are chosen from observations outside the dropped readers and from \(n_r\); even if a dropped reader reads the second repair digit, its retained probability bound holds for each of these predetermined phases. The other cases are bounded separately as in the old certificate, rather than conditioning the line argument on their failure. Once all older observations are fixed, any terminal blocker must kill a chosen survivor, so applying the original terminal weight after this step preserves the product bound. No independence between the killed-phase indicators is needed.
