# Maximal-order envelopes give representation density above 99.9991368%

The exception-density upper bound improves from **0.004558244% to below 0.0008632%**, an **81.1% reduction**. The calculation uses the same published cutoff \(B=9\cdot10^{14}\) and retains the low-order charge, both infinite tails, and all other inherited charges. It bounds the limiting miss density in the two-growth-axis box, and therefore the all-exponent exception density. The pointwise conjecture remains open. [Pinned predecessor](https://github.com/Samsen879/a303656/blob/f91c8ad63d23c02f1a88239f74fa44d8417e9ac7/analysis/ajt5_overnight_2026_11_26/MAX_ORDER_81_TERMINAL_DENSITY_BOUND.md) · [All-exponent density theorem](https://github.com/Samsen879/a303656/blob/f91c8ad63d23c02f1a88239f74fa44d8417e9ac7/analysis/ajt5_overnight_2026_11_26/EXACT_DENSITY_ALL_EXPONENTS.md)

### Reconstructed ledger

The following are the nine largest finite charges in the predecessor, in units of \(10^{-11}\) of density.

| \(D\) | Previous | Revised |
|---:|---:|---:|
| 243 | 2,077,604 | 23,149 |
| 31 | 401,161 | 121 |
| 43 | 219,031 | 325 |
| 47 | 178,957 | 462 |
| 59 | 162,667 | 502 |
| 71 | 110,220 | 699 |
| 67 | 88,149 | 618 |
| 125 | 70,921 | 879 |
| 729 | 62,368 | 1,516 |

The replay tests nonzero finite charges with \(D\le500\), retaining the existing \(D=81\) certificate, and also tests \(D=729,2187\). It replaces a charge only when the rounded replacement is smaller.

| Charge | Previous density | Revised density |
|---|---:|---:|
| Replaced prime \(D\) charges | \(0.00001513409\) | \(0.00000021648\) |
| Replaced higher-power \(D\) charges | \(0.00002228890\) | \(0.00000025603\) |
| All retained charges and inherited rounding slack | \(0.000008159448400322956\ldots\) | same |
| **Total** | **\(0.000045582438400322956\ldots\)** | **\(0.000008631958400322956\ldots\)** |

The retained subtotal includes \(77796/10^{11}\) of untouched finite charges, \(14/2^{27}\) for the finite large-source reader allowance, and the prime and high-power tails \(1633/10^{11}\) and \(7320/10^{11}\). The remaining \(0.000007187650271966\ldots\) is the original low-order charge plus inherited rounding slack. The low-order charge alone is approximately \(0.000006554747\), about **76% of the revised total**. [Original low-order calculation](https://github.com/Samsen879/a303656/blob/f91c8ad63d23c02f1a88239f74fa44d8417e9ac7/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md) · [Inherited high-power tail](https://github.com/Samsen879/a303656/blob/0ad4a565789dd446058134081d187b8408991337/analysis/ajt5_overnight_2026_11_26/EXPONENT_PARITY_HIGH_POWER_DENSITY_BOUND.md)

### General maximal-order bound

Assign each high-order terminal its largest order prime power \(D=r^a\) across both bases. In its original dyadic interval \([Y,2Y)\), \(D>\lfloor(4/5)\log Y\rfloor\), so \(\log q<5D/4+\log 2\). Inertness gives \(v_2(q-1)=1\). For each odd prime \(p\le D\) other than \(r\), put \(m_p=\max\{p^j:p^j\le D\}\). For a given terminal, let \(I=\{p:m_p\mid q-1\}\). Both orders divide
\[
L_I=L_0\prod_{p\in I}p,\qquad
L_0=2D\prod_{p\ne r}\frac{m_p}{p}.
\]
An absent top power removes one copy of \(p\) from the bound. The argument allows either base to supply \(D\). For example, the ordinary prime \(2843\) has orders \(203,2842\), so \(D=49\) comes from base \(5\) alone. The modulo-\(q^2\) test excludes it as a common Wieferich terminal.

For each exact \(I\), a genuine terminal satisfies \(q^2\mid 3^{L_I}-1\). This follows by first lifting the order of \(3\) to \(q^2\), since the ratio of \(q-1\) to that order is a unit modulo \(q\). The product of the squared primes in this class is therefore smaller than \(3^{L_I}\). As \(\log q>34\), summing over exact sets of cardinality below \(k\) gives the count bound
\[
C_k=\frac{L_0\log3}{68}\sum_{j<k}e_j((p)_p),
\]
where \(e_j\) is the elementary symmetric sum. A terminal with at least \(k\) present powers lies in a reduced CRT class modulo \(4D\prod_{p\in J}m_p\) for some \(k\)-element \(J\subseteq I\). Let \(M_k\) use the \(k\) largest optional moduli and set \(E_k=e_k((1/\varphi(m_p))_p)\). Brun–Titchmarsh gives, for \(u>\log M_k\),
\[
e^{-u}\Pi_D(e^u)\le C_ke^{-u}
+\frac{E_k}{\varphi(D)(u-\log M_k)}.
\]
The replay also uses the pure count bound \(C_{N+1}e^{-u}\) for \(N\) optional primes. The two coefficient arrays come from \(\prod_p(1+px)\) and \(\prod_p(\varphi(m_p)+x)\). This computes the **exact subset sums in \(O(N^2)\) integer operations**, without enumerating subsets or evaluating \(3^{L_I}\). [Montgomery–Vaughan, *The large sieve*](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED)

Partial summation keeps the upper endpoint and uses the best integrated bound on each unit log interval. For prime \(D\), the replacement applies the inherited reader-moment bound with the largest allowable parity mass over terminal signs. For \(D=3^a\), \(a\ge5\), the nine-phase argument bounds the phase numerator by
\[
F_D(u)=\left(\frac{\log u+1/5}{\varphi(D/3)}\right)^3.
\]
Indeed, all affected readers have order depth at least \(a-1\), so their combined weight is at most the quantity inside the cube. The cover polynomial is at most that cube below combined weight \(0.3\), which the replay checks throughout each interval. The weight \(F_D(\log q)/q\) is decreasing, and its negative derivative is at most \(F_D(\log q)/q^2\). [Parity-filtered phase bound](https://github.com/Samsen879/a303656/blob/debfafbeee90f7b79045a21085a60d5e327e3103/analysis/ajt5_overnight_2026_11_26/PARITY_FILTERED_INTERCEPT_DENSITY_BOUND.md) · [Cover polynomial and reciprocal bounds](https://github.com/Samsen879/a303656/blob/c09792c9285da96523960fc20bfe4a939f31151a/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COVER_TREE_DENSITY_BOUND.md)

### Standalone replay

Python 3.9 or later, standard library only. This rebuilds the finite ranking and the exact subtraction from the pinned rational total. All comparisons and rounding are rational.

```python
from fractions import Fraction as Q
from functools import cache
from math import ceil, factorial, floor, isqrt, prod

W, P, H = 10**11, 10**5, 10**6

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
    return Q(floor(W*(a+k*l2)), W), Q(ceil(W*(b+k*u2)), W)

def hi(x):
    return logs(x)[1]

def up(x):
    return Q(ceil(W*x), W)

sieve = bytearray(b'\x01')*(P+1)
sieve[:2] = b'\x00\x00'
for p in range(2, isqrt(P)+1):
    if sieve[p]:
        sieve[p*p::p] = b'\x00'*((P-p*p)//p+1)

def prog(D, r, m, scale=1):
    l, h = logs(m*D)
    U, V = Q(4*D, 3)-h, 34-h
    assert U > V > 0
    return (1/U + hi((Q(4*D, 3)-l)/V))/(scale*(D-D//r))

def reader(D, r):
    return (hi(D)+Q(1,2))/(D-D//r)

def one(r, recip=None):
    s = reader(r,r)
    R = min(s,prog(r,r,4)) if recip is None else recip
    if any(pow(b,r-1,r*r)==1 for b in (3,5)):
        return up(R/r)
    K = (1+isqrt(4*r-3))//2
    T = r-K
    whole = Q(1,r*r)+(Q(1,r)-Q(1,r*r))*min(1,r*s/T)
    psi = moment = Q(1)
    for j in range(6):
        if T-j*K <= 0:
            break
        moment *= r*s/(T-j*K)
        psi = min(psi,moment)
    x,y = [pow(b,(r-1)//2,r)==r-1 for b in (3,5)]
    v = (0,Q(19 if x else 37,96),Q(19 if y else 37,96),
         Q(19 if x!=y else 38,96))
    A = R*max(v)
    if recip is None:
        A = min(A,2*prog(r,r,60,8)*sum(v))
    sh = (1+Q(1,2*r+1))*s
    return up(min(R*whole,R*psi/r+(1-psi)*(A+Q(19,48)*sh*R)/r**2))

def higher(D, r, a, recip=None):
    s = reader(D,r)
    R = min(s,prog(D,r,4)) if recip is None else recip
    if r < 29:
        z = min(1,Q(r,r-1)*s,(r*s)**(r-1)/factorial(r-1),r*s**(r-1))
        return up(R*min(z,27*s**3) if r==3 else R*z)
    if r%4 == 1:
        return Q(0)
    depths = []
    for b in (3,5):
        d = a
        while pow(b,r-1,r**(d-a+2)) == 1:
            d += 1
        depths.append(Q(1,r**((d+1)//2)*(2**(r-2) if d%2==0 else 1)))
    return up(R*max(depths))

@cache
def inv_exp(u):
    z = 1 << (2*u+64)
    return Q(ceil(z*Q(10**7,27182818)**u),z)

def envelope(D,r,F,V):
    pairs = []
    for p in range(3,D+1,2):
        if not sieve[p] or p==r:
            continue
        m = p
        while m*p <= D:
            m *= p
        pairs.append((p,m))
    L0 = 2*D*prod(m//p for p,m in pairs)
    A, E = [1], [1]
    for p,m in pairs:
        f = m-m//p
        A = [a+p*b for a,b in zip(A+[0],[0]+A)]
        E = [f*a+b for a,b in zip(E+[0],[0]+E)]
    counts = [0]
    for a in A:
        counts.append(counts[-1]+a)
    h = [int(W*hi(4*D))]
    for m in sorted((m for p,m in pairs),reverse=True):
        h.append(h[-1]+int(W*hi(m)))
    C = L0*hi(3)/68
    den, grid = E[0]*(D-D//r), 10**30

    def kernel(u, interval):
        # e < 3 gives integral_u^(u+1) exp(-t) dt < (2/3) exp(-u).
        x = C*inv_exp(u)*(Q(2,3) if interval else 1)*grid
        best = ceil(counts[-1]*x)
        for k,logM in enumerate(h):
            d = u*W-logM
            if d <= 0:
                break
            # A left rectangle bounds the decreasing progression kernel.
            best = min(best,ceil(counts[k]*x)+ceil(Q(E[k]*grid*W,den*d)))
        return Q(best,grid)

    return F(V)*kernel(V,False)+sum(F(u+1)*kernel(u,True) for u in range(34,V))

def new(D,r,a):
    V = ceil(Q(5*D,4)+u2)
    if r==3 and a>=5:
        phi = D//3-D//9
        assert (hi(V)+Q(1,5))/phi < Q(3,10)
        return up(envelope(D,r,lambda u: ((hi(u)+Q(1,5))/phi)**3,V))
    R = envelope(D,r,lambda u: 1,V)
    return one(r,R) if a==1 else higher(D,r,a,R)

assert logs(9*10**14)[0] > 34 and logs(34)[0] > Q(3,34)
assert sum(Q(1,factorial(j)) for j in range(13)) > Q(27182818,10**7)
assert Q(4,3)*Q(3,10)+18*Q(3,10)**3+9*Q(3,10)**5 < 1

terms = {r:(r,1,one(r)) for r in range(31,P+1,4) if sieve[r]}
assert sum(v for r,a,v in terms.values()) == Q(1531769,W)
for r in range(3,isqrt(H)+1,2):
    if sieve[r]:
        D,a = r*r,2
        while D <= H:
            if D >= 28:
                terms[D] = (r,a,higher(D,r,a))
            D,a = D*r,a+1
terms[81] = (3,4,Q(19019,W))
assert sum(v for r,a,v in terms.values() if a>1) == Q(2288326,W)
rank = sorted(terms,key=lambda D: -terms[D][2])
assert rank[:11] == [243,31,43,47,59,71,67,125,729,79,83]

before, after = [Q(0),Q(0)], [Q(0),Q(0)]
for D,(r,a,v) in sorted(terms.items()):
    if not v or D==81 or (D>500 and D not in (729,2187)):
        continue
    t = min(v,new(D,r,a))
    if t < v:
        j = int(a>1)
        before[j] += v
        after[j] += t
        print(D,int(v*W),int(t*W))

pre81 = Q(8401430807510648551056610750957092065253478722474169318289,
          59266799168786352000000000000000000000000000000000000000000000)
baseline = pre81-Q(9636386-19019,W)
carry = baseline-sum(before)
retained_finite = Q(1531769+2288326,W)-sum(before)
tails_and_allowance = Q(1633+7320,W)+Q(14,2**27)
assert retained_finite == Q(77796,W)
assert Q(718765,W) < carry-retained_finite-tails_and_allowance < Q(718766,W)
assert before == [Q(1513409,W),Q(2228890,W)]
assert after == [Q(21648,W),Q(25603,W)]
answer = carry+sum(after)
assert answer < Q(8632,10**9)
print("percent:",float(100*answer))

def order(b,q):
    return next(d for d in range(1,q) if (q-1)%d==0 and pow(b,d,q)==1)

assert [order(b,311) for b in (3,5)] == [155,155] and 310%25
assert [order(b,2843) for b in (3,5)] == [203,2842]
assert [pow(b,2842,2843**2) for b in (3,5)] == [7769920,2754868]
```

The sum of squared-prime logarithms in each exact presence class is bounded by the logarithm of one integer, so no independence of presence subsets is assumed. For the progression union, inertness fixes the single reduced class modulo 4 and φ(4D)=2φ(D), cancelling the factor two in Brun–Titchmarsh. The D-group assignment is deterministic; terminal groups not replaced keep their fully charged predecessor bounds. The rational ledger was independently checked by recovering the exact predecessor fraction and rerunning the finite replacement table. The published vast lower-cutoff search is inherited, not recomputed here.
