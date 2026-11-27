# Largest-order restriction gives representation density above 99.995441%

**The exception-density upper bound drops below \(0.004559\%\)** without extending the prime search. Choosing the largest order prime power lets us replace the \(D=81\) terminal envelope using actual order divisibility and the modulo-\(q^2\) lifting condition. The phase and cover calculation stays the same. [Predecessor certificate](https://github.com/Samsen879/a303656/blob/0ad4a565789dd446058134081d187b8408991337/analysis/ajt5_overnight_2026_11_26/EXPONENT_PARITY_HIGH_POWER_DENSITY_BOUND.md)

| Charge, in density units | Previous | Revised |
|---|---:|---:|
| Finite \(D=81\) | \(0.00009636386\) | \(0.00000019019\) |
| All other finite and infinite charges | \(0.0000453922484003\ldots\) | same |
| **Total** | **\(0.0001417561084003\ldots\)** | **\(0.0000455824384003\ldots\)** |

### A smaller terminal envelope

In the high-order branch, choose the **largest** prime power occurring in either order. This is an allowed choice in the existing proof. It restricts which terminals each charge needs to cover, so all the other charges can be retained. For \(D=81\), both orders divide
\[
L=2\,\operatorname{lcm}(1,3,5,\ldots,81).
\]
The factor of \(2\) uses inertness. This holds even if only the base \(5\) supplies the order factor \(81\). [Original branch rule](https://github.com/Samsen879/a303656/blob/0ad4a565789dd446058134081d187b8408991337/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_EXPLICIT_DENSITY_BOUND.md)

For every prime \(p\in[5,81]\), let \(m_p\) be the largest power of \(p\) at most \(81\). Call \(p\) present if \(q\equiv1\bmod m_p\). For an **exact** present set \(I\), both orders divide
\[
L_I=L_0\prod_{p\in I}p,\qquad
L_0=\frac{L}{\prod_{5\le p\le81}p}=5670,
\]
where the products are over primes. An absent \(p\) removes one factor of \(p\) from the order bound. In particular, absence of \(25\) or \(49\) removes only one factor of \(5\) or \(7\).

At a genuine common Wieferich terminal, \(q^2\mid 3^{L_I}-1\). Indeed, if \(d=\operatorname{ord}_q(3)\), raising \(3^d\) to \((q-1)/d\) cannot erase a nonzero first \(q\)-adic digit, since that multiplier is a unit modulo \(q\). As \(\log q>34\), terminals with fewer than \(k\) present powers therefore number at most
\[
C_k=\frac{L_0\log3}{68}\sum_{j<k}e_j((p)_p).
\]
Here \(e_j\) is the elementary symmetric sum. The sum charges every exact subset, with its own exponent budget.

A terminal with at least \(k\) present powers belongs to a progression modulo \(324\prod_{p\in I}m_p\) for some \(k\)-element subset \(I\). Let \(M_k\) be \(324\) times the product of the \(k\) largest optional moduli and \(E_k=e_k((1/\varphi(m_p))_p)\). Summing the progression bounds gives, for \(u>\log M_k\),
\[
\frac{\Pi(e^u)}{e^u}
\le C_k e^{-u}+\frac{E_k}{54(u-\log M_k)}.
\]
Here \(\Pi\) counts the candidate \(D=81\) terminals above the existing cutoff. The \(k=0\) case recovers the original envelope. The replay takes the best integrated bound on each log interval. [Montgomery–Vaughan progression bound](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED)

### Standalone rational replay

The script rebuilds the previous \(D=81\) charge and uses its unchanged phase numerator and endpoint \(102\). Every new count or integral is rounded outward. It evaluates neither the enormous integers \(3^{L_I}-1\) nor any new terminal primes. [Inherited phase numerator](https://github.com/Samsen879/a303656/blob/904d8df47b00e3eacb3f000e5332628cfcfe4a54/analysis/ajt5_overnight_2026_11_26/JOINT_CHART_OCCUPANCY_DENSITY_BOUND.md)

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt, lcm, prod

W = 10**11

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s,s+2*z**25/(25*(1-z*z))

l2,u2 = series(Q(2))
def logs(x):
    y,k = Q(x),0
    while y>=2:
        y /= 2
        k += 1
    a,b = series(y)
    return Q(floor(W*(a+k*l2)),W),Q(ceil(W*(b+k*u2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)

def prime(p):
    return p>1 and all(p%j for j in range(2,isqrt(p)+1))

def depth(b,p):
    m = p-1
    while m%3==0 and pow(b,m//3,p)==1:
        m //= 3
    j = 0
    while m%3==0:
        m //= 3
        j += 1
    return j

# Unchanged phase numerator.
a,J = Q(327,326),Q(53,250)
stats = []
for b,t,c in ((3,5,Q(47,50)),(5,3,Q(221,250))):
    rows = [(p,depth(b,p),depth(t,p))
            for p in range(55,3457,108) if prime(p)]
    rho = sum(Q(1,p+1) for p,d,_ in rows if d>=3)
    tau = sum(Q(1,p+1) for p,d,_ in rows if d>=4)
    M = sum(Q(1,p+1) for p,d,e in rows if d==3 and e>=3)
    assert lo(lo(32))-Q(1,34)-18*rho>c
    stats.append((c,tau,M,Q(2,3)*(1-3*J)*M))

def U(s):
    x = a*s
    return x-x*x/2+x**3/6

def F(u):
    vals = []
    for c,t,M,delta in stats:
        s = (hi(u)-c)/18-t
        x,y = U(s),U(t)
        vals.append(x**3+9*x*x*y*y+18*x*y**5+9*y**8
                    -delta*max(0,(s-M)**2-(s-M)/164))
    return max(vals)

assert lo(9*10**14)>34 and Q(405,4)+hi(2)<102
l,h = logs(324)
old = up((F(102)/(102-h)+sum(
    F(u+1)*hi((u+1-l)/(u-h)) for u in range(34,102)))/54)
assert old==Q(9636386,W)

# Each optional prime contributes one order factor if absent.
P = [p for p in range(5,82,2) if prime(p)]
M = [p*p if p*p<=81 else p for p in P]
assert len(P)==20 and all(p**3>81 for p in P)
L = 2*lcm(*range(1,82,2))
assert L==5670*prod(P)

def esym(xs):
    e = [Q(1)]+[Q(0)]*len(xs)
    for x in xs:
        for k in range(len(xs),0,-1):
            e[k] += x*e[k-1]
    return e

A = esym(P)
E = esym([Q(1,m-m//p) for m,p in zip(M,P)])
mods = [324]
for m in sorted(M,reverse=True):
    mods.append(mods[-1]*m)
C = [5670*hi(3)*sum(A[:k])/68 for k in range(len(mods))]
bounds = [logs(m) for m in mods]

def inv_exp(u):
    s=t=Q(1)
    for j in range(1,161):
        t *= Q(u,j)
        s += t
    return 1/s  # upper bound for exp(-u)

def kernel(u,interval):
    x = inv_exp(u)
    vals = []
    for k,(l,h) in enumerate(bounds):
        if u<=h:
            continue
        if interval:
            # Integral of exp(-t) on this interval is < (2/3) exp(-u).
            vals.append(Q(2,3)*C[k]*x+E[k]*hi((u+1-l)/(u-h))/54)
        else:
            vals.append(C[k]*x+E[k]/(54*(u-h)))
    return min(vals)

new = up(F(102)*kernel(102,False)+sum(
    F(u+1)*kernel(u,True) for u in range(34,102)))
assert new==Q(19019,W)

base = Q(8401430807510648551056610750957092065253478722474169318289,
         59266799168786352000000000000000000000000000000000000000000000)
answer = base-old+new
assert answer<Q(4559,10**8)
print("OK:",float(100*answer),"%")
```

The reduction applies to the genuine terminal branch for either selected axis. It gives the stated upper bound on growth-box misses and hence on all-exponent exceptions. The pointwise conjecture remains open.

The new cumulative count is used by partial summation with respect to \(u=\log q\). For \(w(q)=F(\log q)/q\), the inherited phase numerator is nonnegative and increasing, while \(w\) is decreasing. Thus the derivative term is safely bounded using \(F(\log q)/q^2\), with the logarithmic interval supremum \(F(u+1)\). Each interval is bounded by every eligible subset threshold \(k\) separately, so taking their minimum does not assume a single optimal \(k\) across the integration. The predecessor's rational total was independently reconstructed before replacing this one charge.
