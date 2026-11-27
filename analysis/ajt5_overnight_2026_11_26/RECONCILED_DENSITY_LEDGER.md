# Reconciled density ledger gives representation density above 99.999846608%

The audited exception-density bound is **below \(0.000153392\%\)**, with the exact rational certificate evaluating to \(0.00015339189744333908\ldots\%\). I recovered the entire \(6.329033294780848\ldots\times10^{-7}\) discrepancy as two historical round-ups, in density units. The cutoff \(B=9\cdot10^{14}\), both high-order infinite tails, and the low-order analytic tail are carried in full. The bound applies to growth-box misses and hence to all-exponent exceptions. [Pinned exact-order certificate](https://github.com/Samsen879/a303656/blob/9826d9cfa8038c80f460fafe27f24dc2ce99acd6/analysis/ajt5_overnight_2026_11_26/EXACT_ORDER_LOW_DENSITY_BOUND.md)

### Where the slack entered

| Historical carryover | Recomputed bound before round-up | Excess, in density units |
|---|---:|---:|
| Nine-phase calculation started from \(0.00175\) | \(0.0017493681392091957\ldots\) | \(6.318607908044394\ldots\times10^{-7}\) |
| Whole-repair-line calculation started from \(0.00087385\) | \(0.0008738489574613264\ldots\) | \(1.042538673645422\ldots\times10^{-9}\) |

The replay proves that **the sum of these two excesses equals the pinned total minus the rebuilt total as an exact fraction**. The finite factorial allowance \(14/2^{27}\) is an analytic charge and remains in the ledger. The per-class outward rounding is also preserved. [Foundational compensated sum](https://github.com/Samsen879/a303656/blob/9826d9cfa8038c80f460fafe27f24dc2ce99acd6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md) · [Distinct-shallow calculation](https://github.com/Samsen879/a303656/blob/a7232f58d5beb92a71da1df5f1c831ecdf2f2660/analysis/ajt5_overnight_2026_11_26/DISTINCT_SHALLOW_READER_DENSITY_BOUND.md) · [Whole-repair-line carryover](https://github.com/Samsen879/a303656/blob/a476e9ca22a16358c763229700f7bf07a9f5212b/analysis/ajt5_overnight_2026_11_26/WHOLE_REPAIR_LINE_DENSITY_BOUND.md)

| Rebuilt charge | Exact value or density units |
|---|---:|
| Finite prime \(D\) | \(40008/10^{11}\) |
| Finite higher-power \(D\) | \(85039/10^{11}\) |
| Finite factorial allowance | \(14/2^{27}\) |
| Prime-source tail | \(1633/10^{11}\) |
| Higher-power tail | \(7320/10^{11}\) |
| **Retained subtotal before low order** | **\(134000/10^{11}+14/2^{27}\)** |
| Low order, finite part and tail | \(8.961084607645708\ldots\times10^{-8}\) |
| **Total** | **\(1.533918974433391\ldots\times10^{-6}\)** |

**The largest individual charge is \(D=31^3=29791\)** at \(27014/10^{11}\), about 17.6% of the rebuilt total. The two base residues \(3^{30},5^{30}\bmod31^2\) are \(528,280\), so both lifting depths are one. The depth-three branch charges \(R_{31^3}/31^2\) before outward rounding. The next two classes are \(D=243\) and \(D=81\). Finite higher powers are the largest aggregate, with the inert cubes from \(r\ge31\) alone contributing \(40141/10^{11}\). [Higher-power depth formula](https://github.com/Samsen879/a303656/blob/9826d9cfa8038c80f460fafe27f24dc2ce99acd6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md) · [Ranked finite envelope](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/MAX_ORDER_RANKED_TERMINAL_DENSITY_BOUND.md)

### Standalone rational replay

The inline version carries the certified single-class \(D=81\) entries and the exact low-order finite numerator as inputs. It rebuilds the remaining finite charges, both source tails, the old and new low-order tails, and both historical round-ups. The predecessor denominator below is the exact published integer in factored form.

```python
from fractions import Fraction as Q
from functools import cache
from math import ceil, factorial, floor, isqrt, prod

B, P, H, W, Z = 9*10**14, 10**5, 10**6, 10**11, 10**25

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, u2 = series(Q(2))

@cache
def logs(x):
    y, k = Q(x), 0
    assert y >= 1
    while y >= 2:
        y /= 2
        k += 1
    a, b = series(y)
    return Q(floor(W*(a+k*l2)),W), Q(ceil(W*(b+k*u2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)

def exp_lo(x,n):
    s = t = Q(1)
    for j in range(1,n):
        t *= Q(x,j)
        s += t
    return s

prime = bytearray(b'\x01')*(P+1)
prime[:2] = b'\x00\x00'
for p in range(2,isqrt(P)+1):
    if prime[p]:
        prime[p*p::p] = b'\x00'*((P-p*p)//p+1)

def powers(p,N):
    m = 1
    while m <= N:
        yield m
        m *= p

def low_tail(j,m,C,inert):
    u = lo(B)+j*l2
    pmin = 3 if inert else 2
    assert 8**m < pmin*7**m
    c2 = Q(2**(m-1)) if inert else Q(1)
    assert c2*prod(max(Q((a+1)**m,p**a) for a in range(7))
                   for p in range(pmin,2**m) if prime[p]) < C**m

    def geom(z):
        return 1/(exp_lo(z*u,100)*(1-1/exp_lo(z*l2,12)))

    a = Q(104,125*m)
    v = hi(3)*Z*Z/((4 if inert else 2)*u)
    root = Q(isqrt(floor(v))+1,Z)
    return C*(root*geom(Q(1,2)-a)+geom(1-a))

def legacy_low():
    n = 0
    for j in range(24):
        Y = B*2**j
        T = floor(Q(4,5)*(hi(B)+j*u2))
        ds = [1]
        for p in range(2,T+1):
            if prime[p]:
                ds = [d*m for d in ds for m in powers(p,T)]
        v = hi(3)/(2*(lo(B)+j*l2)*Y)
        n += sum(ceil(Z*min(v*d,Q(1,d)+Q(1,Y))) for d in ds)
    assert n == 48533122419939870652
    return Q(n,Z)+low_tail(24,4,9,False)

def phi(D,r): return D-D//r
def readers(D,r): return (hi(D)+Q(1,2))/phi(D,r)

def progression(D,r,m=4,extra=1):
    l,h = logs(m*D)
    u,v = Q(4*D,3),34-h
    assert u-h > v > 0
    return (1/(u-h)+hi((u-l)/v))/(extra*phi(D,r))

def reciprocal(D,r):
    return min(readers(D,r),progression(D,r))

def exceptional(r):
    return any(pow(b,r-1,r*r)==1 for b in (3,5))

def depth(r,a):
    if r <= 23 or r%4 == 1:
        return Q(0)
    costs = []
    for b in (3,5):
        e = a
        while pow(b,r-1,r**(e-a+2)) == 1:
            e += 1
        costs.append(Q(1,r**((e+1)//2)*(2**(r-2) if e%2==0 else 1)))
    return max(costs)

def cover(r,s,nine):
    if r >= 29:
        return Q(0)  # Allocated to the finite factorial allowance.
    g = min(1,Q(r,r-1)*s,(r*s)**(r-1)/factorial(r-1))
    if nine:
        g = min(g,r*s**(r-1))
        if r == 3:
            g = min(g,27*s**3)
    return g

@cache
def parity_caps(x,y):
    weights = ((0,0,40),(0,1,19),(1,0,19),(1,1,18))
    return tuple(Q(max(sum(w for a,b,w in weights
                           if (s*a+t*b)%2 and (x*a+y*b)%2==j)
                       for j in (0,1)),96)
                 for s,t in ((0,0),(0,1),(1,0),(1,1)))

def charge1(r,R,plain):
    s = readers(r,r)
    if exceptional(r):
        return up(R/r)
    K = (1+isqrt(4*r-3))//2
    h = r-K
    whole = Q(1,r*r)+(Q(1,r)-Q(1,r*r))*min(1,r*s/h)
    psi = moment = Q(1)
    for j in range(6):
        if h-j*K <= 0:
            break
        moment *= r*s/(h-j*K)
        psi = min(psi,moment)
    p = parity_caps(*(pow(b,(r-1)//2,r)==r-1 for b in (3,5)))
    align = R*max(p)
    if plain:
        align = min(align,2*progression(r,r,60,8)*sum(p))
    sh = (1+Q(1,2*r+1))*s
    return up(min(R*whole,R*psi/r+(1-psi)*(align+Q(19,48)*sh*R)/r**2))

def charge_power(D,r,a,R,nine):
    return up(R*(depth(r,a)+cover(r,readers(D,r),nine)))

def sym(xs):
    a = [1]+[0]*len(xs)
    for x in xs:
        for k in range(len(xs),0,-1):
            a[k] += x*a[k-1]
    return a

@cache
def inverse_exp(u):
    z = 1 << (2*u+64)
    return Q(ceil(z*Q(10**7,27182818)**u),z)

def maximal(D,r):
    ps = [p for p in range(3,D+1,2) if p!=r and prime[p]]
    ms = [max(powers(p,D)) for p in ps]
    E = sym([Q(1,phi(m,p)) for m,p in zip(ms,ps)])
    C = [Q(0)]
    scale = 2*D*prod(m//p for p,m in zip(ps,ms))*hi(3)/68
    for a in sym(ps):
        C.append(C[-1]+scale*a)
    logsM = [hi(4*D)]
    for m in sorted(ms,reverse=True):
        logsM.append(logsM[-1]+hi(m))
    V, G = ceil(Q(5*D,4)+u2), 10**30

    def kernel(u,interval):
        x = (Q(2,3) if interval else 1)*inverse_exp(u)
        vals = [ceil(G*C[-1]*x)]
        for k,h in enumerate(logsM):
            if h >= u:
                break
            a,b = C[k]*x,E[k]/(phi(D,r)*(u-h))
            vals.append(ceil(G*a)+ceil(G*b))
        return Q(min(vals),G)

    def F(u):
        return ((hi(u)+Q(1,5))/phi(D//3,3))**3 if r==3 else 1

    return F(V)*kernel(V,False)+sum(
        F(u+1)*kernel(u,True) for u in range(34,V))

# Both source tails. Catalogue exhaustiveness uses the published search.
catalog = {3:(11,1006003),5:(20771,40487,53471161,1645333507,
                              6692367337,188748146801)}
assert all(pow(b,p-1,p*p)==1 for b,ps in catalog.items() for p in ps)
assert all(pow(5,p-1,p*p)!=1 for p in catalog[3])
assert 150000*prod((2,3,5,7,11,13,17,19,23,29))==970453984500000>B
h,A = hi(P)+Q(1,2),Q(P,P-1)
rare = [p for ps in catalog.values() for p in ps if P<p<=B and p%4==3]
assert sorted(rare) == [1006003,1645333507]
p_tail = up((A*(h/2+Q(1,4))+2*A*A*(h*h/2+h/2+Q(1,4)))/P**2
            +sum((hi(p)+Q(1,2))/(p*(p-1)) for p in rare)
            +(hi(B)+Q(3,2))/(B-1)+Q(3,2**P))
old_p_tail = Q(10001,10000)*(hi(P)+Q(3,2))/P

def integ(X,k,A,B):
    return ((A*hi(X)+B)/(k-1)+Q(A,(k-1)**2))/X**(k-1)

assert not any(exceptional(r) for r in range(31,20001,4) if prime[r])
h = hi(H)+Q(1,2)
kill_tail = Q(81,8)/H**2*(h**3/2+3*h*h/4+3*h/4+Q(3,8))
old_h_tail = Q(27,10)/H*(2*(hi(2*H)+Q(1,2))+2*u2)
tree_tail = old_h_tail/2+kill_tail
z,w = Q(1,31**3),Q(1,20000**3)
h_tail = up(kill_tail+Q(3,2)*(
    integ(100,5,3,Q(1,2))+
    integ(30,8,5/(1-z)+2*z/(1-z)**2,Q(1,2)/(1-z))+
    Q(1,2**28)*(2*hi(31)*z/(1-z)**2+Q(1,2)*z/(1-z))+
    integ(20000,4,2/(1-w)**2,Q(1,2)/(1-w))))
assert (p_tail,h_tail) == (Q(1633,W),Q(7320,W))

legacy, before, current = {}, {}, {}
for r in range(31,P+1,4):
    if not prime[r]:
        continue
    s,R = readers(r,r),reciprocal(r,r)
    eta = Q(1,r)
    if not exceptional(r):
        eta = min(eta,Q(1,r*r)+min(1,2*s)/r)
    legacy[r] = up(R*eta)
    before[r] = charge1(r,R,True)
    current[r] = (min(before[r],charge1(r,maximal(r,r),False))
                  if r<=500 else before[r])

# Published D=81 leaf certificates at three successive stages.
at81, distinct81, ranked81 = [Q(n,W) for n in (33452894,14055070,19019)]
for r in range(3,isqrt(H)+1,2):
    if not prime[r]:
        continue
    for a,D in enumerate(powers(r,H)):
        if D<28 or a<2:
            continue
        R = reciprocal(D,r)
        legacy[D] = charge_power(D,r,a,R,False)
        before[D] = ranked81 if D==81 else charge_power(D,r,a,R,True)
        current[D] = before[D]
        if D!=81 and before[D] and (D<=500 or D in (729,2187)):
            q = maximal(D,r)
            v = up(q) if r==3 else charge_power(D,r,a,q,True)
            current[D] = min(before[D],v)

small = [D for r in (3,5,7,11,13,17,19,23) for D in powers(r,H)
         if D>=28]
nine = at81+sum(before[D] for D in small if D!=81)
old_small = sum(legacy[D] for D in small)
old_low = legacy_low()
lump = Q(14,2**27)
foundation = old_low+sum(legacy.values())+lump+old_p_tail+old_h_tail
slack1 = Q(175,10**5)-foundation
stage9 = Q(175,10**5)-old_small+nine
assert stage9 == Q(111020555,W)
slack2 = Q(87385,10**8)-(stage9-at81+distinct81-old_h_tail+tree_tail)

retained = sum(current.values())+lump+p_tail+h_tail
assert retained == Q(134000,W)+lump
low = Q(891331308302981248,Z)+low_tail(48,6,70,True)
answer = retained+low

pre81 = Q(8401430807510648551056610750957092065253478722474169318289,
          59266799168786352*10**45)
pinned = pre81-Q(9636386-19019+3695048,W)-old_low+low
assert slack1>0 and slack2>0 and pinned-answer==slack1+slack2
assert Q(216682,W) < pinned < Q(216683,W)
assert answer < Q(153392,W)
assert max(current,key=current.get) == 31**3
assert current[31**3] == Q(27014,W) and depth(31,3)==Q(1,31**2)

print("historical slack",float(slack1),float(slack2))
print("retained subtotal",retained)
print("exception density percent",float(100*answer))
```

The two deletions are exactly identified upward rounding gaps in earlier additive accounting, not changes to the mathematical terminal model, input bound, or prime search. The standard-library program was independently rerun; both source tails, the exact-order low tail, and the finite factorial term remain present. Density one and the pointwise conjecture remain open.
