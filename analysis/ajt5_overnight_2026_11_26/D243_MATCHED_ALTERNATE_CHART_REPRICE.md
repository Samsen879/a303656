# Matched alternate-chart repricing for D=243

**The \(D=243\) subtraction survives the audit.** The corrected proof fixes both charts before reading any omitted exceptional or dropped-reader observations. The rational replay recovers the active **9,670-unit** row and certifies **8,760 units** after the subtraction. From the verified predecessor, the finite subtotal becomes **53,604 units of \(10^{-11}\) density**, and the exception-density bound is **strictly below \(0.000062596085\%\)**. The \(D=81\) row, finite-prime subtotal, cutoff, and all three tails carry forward. [Verified predecessor](https://github.com/Samsen879/a303656/commit/eff2c50d124b77652ce9d14532f889da18448f7e) · [Active \(D=243\) envelope](https://github.com/Samsen879/a303656/commit/a3e1b5858a16b4b361d86726614c47ecbbf63463)

### Matched selection and restoration

Fix an eligible terminal \(q\) and an axis that reads depth five. Let \(\mathcal B\) be the earlier readers of depth at least four on that axis, and \(\mathcal A\) the auxiliary-only readers of depth at least four. Let \(J\) be the common-Wieferich primes among the **retained** rows. Thus \(J\) is disjoint from \(\mathcal A\cup\mathcal B\), and every \(p\in J\) is above \(B=9\cdot10^{14}\).

1. **Prepare both charts using only reduced retained observations.** Omit \(J\) temporarily. Choose a reference anchor by a fixed selection rule. If the reduced prefix is empty, \(q\) cannot be the first blocker. Change the terminal axis’s third ternary digit to obtain the alternate anchor. Below 243, an inert row that can read this change must be \(55\bmod108\). The only prime candidate is 163, whose exact orders are \(162,54\), so it is already in the dropped union in either orientation. Repair affected ordinary retained rows in increasing order, on an ordinary axis. Every repair prime exceeds 243. Those primary changes preserve both terminal orders and all six named readers’ full orders. The largest prime factor in those six order pairs is 19.
2. **Screen \(J\) jointly.** Within either chart, the main nine moves and all three auxiliary variations change only the 3-primary coordinates above depth three. At a retained \(p\), each full base order modulo \(p\) is \(3^j m\), with \(j\le3\) and \(3\nmid m\). Each chart move fixes the residue modulo \(m\) and is zero modulo \(27\). At precision \(p^k\) the order can acquire only a factor of \(p\), and the chart also fixes that coordinate. Thus each chart has **one shift per omitted row**, including all auxiliary variations. Conditioned on the reduced observations, the joint unit screen has exact probability \(\prod_{p\in J}(1-m_p/p)\), with \(m_p\in\{1,2\}\) the number of different shifts across the two charts. The replay uses the lower bound \(\prod_{p\in J}(1-2/p)\).
3. **Select the reference deterministically.** On screen success, use the prepared reference anchor. On failure, use the original deterministic anchor from the fully retained observations. In either branch, keep the selected reference if it passes \(\mathcal A\) at the reference auxiliary digit. Otherwise use the original deterministic \(\mathcal A\)-compatible extension, if one exists, before reading \(\mathcal B\). If none exists, the first-block event is empty. [Original reference-selection rule](https://github.com/Samsen879/a303656/blob/64e66c0720e2fbde33c2ee1ceb2ae34ba0458191/analysis/ajt5_overnight_2026_11_26/THREE_CHART_SHALLOW_DENSITY_BOUND.md)

The **full-order** provision matters. At the ordinary retained-order analogue 3079 the orders are \(114,513\). The fixture’s raw ternary step fails to preserve the base-5 power there. Adding its prime-to-3 factor makes each chart constant, while the lower-digit release can still give two different shifts across charts.

### Hit law and disjoint subtraction

Conditional on the retained readings and the \(\mathcal A\)-selection, the reference phase is fixed before \(\mathcal B\) is read. Each main reader has probability \(w_p=1/(p+1)\) of an odd valuation at a specified point. Its readable prefixes have distinct shifts modulo \(p\), and distinct prime observations are independent. This proves the same reference-cover bound in both screen branches.

For each subtraction, freeze the retained readings **before** reading \(\mathcal A\) or \(\mathcal B\). Require the prepared reference to pass the auxiliary-only tests used in the event, so the selection rule keeps it. Require exactly the three assigned shallow hits on that reference. The old dual-reader construction then works on either screen branch, using the selected reference’s auxiliary charts. Its retained rows pass throughout those charts by the full-order argument.

The new event requires screen success and exactly **one named pure reader and two unnamed shallow readers** among the three reference hits. The pure reader misses the entire alternate chart after the lower-digit change. At the fixed alternate auxiliary digit, the other two designated readers can kill at most one prefix each. Reserve two terminal-distinct points in an uncovered prefix. The unused shallow readers avoid at most five specified odd-valuation events each, and the deep readers avoid at most two. The auxiliary-only tests fit the same five-event allowance. The old \(59/100\) factor therefore applies. The new event is disjoint from the old subtraction because the latter has a named dual reader among its exact three reference hits.

Writing \(x\) for the unnamed shallow weight and \(w_*\) for the named pure weight, the reduction in the original numerator is at least
\[
\frac{59}{100}\,h(u)\,3w_*(x^2-x/164)_+ .
\]
Here \(h(u)\) is a lower bound for the joint screen for \(\log q\le u\). Partial summation of Brun–Titchmarsh in the class \(3\bmod4\) gives the reciprocal bound \(1/U+\log(U/V)\), with \(U=u-\log4\) and \(V=\log B-\log4\). Hence one may take
\[
h(u)=\exp\!\left[-\left(2+\frac4{B-1}\right)
                       \left(\frac1U+\log\frac UV\right)\right].
\]
The screen is measured before either dropped group is read. The hit law is uniform in each legal selected chart, so this lower bound multiplies the disjoint subtraction on the original probability space. The terminal factor is applied after all earlier observations. [Montgomery–Vaughan interval bound](https://doi.org/10.1112/S0025579300004708)

### Standalone rational replay

The code rebuilds the active weighted terminal envelope, including the 128 subdivisions of each of its first nine log bins. For a subinterval \([a,b]\), it uses \(d=1/a-1/b\) and the original minimum over catalogue, absolute, and shifted progression bounds. The shifted left-end expression is \(C_kd+E_k(\log(b/a)-Bd)/\log((a-B)/M_k)\). The alternative right-end count is \([C_k+E_k(b-B)/\log((b-B)/M_k)]d\). All bounds are rounded outward. The named arithmetic fixture checks a pure stripe at 163 and its escape at the ordinary terminal 8263. [Pinned interval and catalogue formulas](https://github.com/Samsen879/a303656/commit/a3e1b5858a16b4b361d86726614c47ecbbf63463)

```python
from fractions import Fraction as Q
from functools import cache
from itertools import combinations
from math import ceil, floor, isqrt, lcm, prod

B, W, V = 9*10**14, 10**11, 305

def prime(p):
    return p > 1 and all(p%i for i in range(2,isqrt(p)+1))

def order(b,p):
    return next(i for i in range(1,p) if pow(b,i,p)==1)

def v3(m):
    return 0 if m%3 else 1+v3(m//3)

def series(y):
    z = (y-1)/(y+1)
    a = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return a,a+2*z**25/(25*(1-z*z))

L2,H2 = series(Q(2))

@cache
def logs(x):
    y,k = Q(x),0
    while y >= 2:
        y /= 2
        k += 1
    a,b = series(y)
    return Q(floor(W*(a+k*L2)),W),Q(ceil(W*(b+k*H2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(10**30*x),10**30)

def exp_interval(x,k):
    assert x < k+2
    s=t=Q(1)
    for j in range(1,k+1):
        t *= Q(x,j)
        s += t
    return s,s+t*Q(x,k+1)/(1-Q(x,k+2))

readers = (163,487,811,1459,1783,3079)
assert [p for p in range(55,244,108) if prime(p)] == [163]
assert [p for p in range(163,3457,324) if prime(p)] == list(readers)
orders = [tuple(order(b,p) for b in (3,5)) for p in readers]
assert orders == [(162,54),(486,54),(810,405),(1458,243),(594,162),(114,513)]
assert lcm(*(o for pair in orders for o in pair)) == 2*3**6*5*11*19
rows = [(Q(1,p+1),tuple(map(v3,o))) for p,o in zip(readers,orders)]
offset = lo(lo(Q(3456,324)))-Q(1,34)
lam,a0 = Q(59,100),Q(327,326)
assert lo(B)>34 and ceil(Q(5*243,4)+H2)==V
assert Q(820,159)*((hi(V)-offset)/54
                  +sum(w for w,d in rows if max(d)>=4)) < lo(1/lam)

stats = []
for i in (0,1):
    t = sum(w for w,d in rows if d[i]>4)
    named = [(w,d[1-i]>=4) for w,d in rows if d[i]==4]
    m = sum(w for w,_ in named)
    a,h,c = (6*sum(prod(w for w,_ in g) for g in combinations(named,k)
                    if any(dual for _,dual in g)) for k in (1,2,3))
    pure = sum(w for w,dual in named if not dual)
    off = offset-54*(m+t)
    stats.append((off,t,m,a/2,h,c,pure))

    # Check padding in shallow mass and maximization at minimum deep mass.
    E,J = (lo(35)-off)/54,(hi(V)-off)/54
    a = a/2+3*pure
    b,d = 1-a0*J/2,a0*(1-a0*J)
    assert m+t<E and t<E/2 and a0*J<1
    assert lam*(a/(2*m)+h/m**2) < 3*b*b*d
    j = J/2
    z = 3*d-18*a0*a0*j-90*a0**5*j**3/b-72*a0**8*j**5/b**2
    assert z*b*b > lam*(2*a/(E/2)+h/(E/2)**2)
    coarse = a0**3/8+9*a0**4*J/16+18*a0**6*J**3+9*a0**8*J**5
    assert (b*(1-t/E))**3-lam*(a/E+h/E**2+c/E**3) > coarse

def occupancy(x):
    z = a0*x
    return z-z*z/2+z**3/6

@cache
def keep(u):
    ub = 1/(u-hi(4))+hi((u-lo(4))/(lo(B)-hi(4)))
    z = Q(ceil(10**20*(2+Q(4,B-1))*ub),10**20)
    return Q(floor(10**15/exp_interval(z,40)[1]),10**15)

@cache
def numerator(u,new):
    out = []
    for off,t,m,a,h,c,pure in stats:
        s = (hi(u)-off)/54-t
        x = s-m
        y,z = occupancy(s),occupancy(t)
        A = a+3*pure*keep(u) if new else a
        out.append(y**3+9*y*y*z*z+18*y*z**5+9*z**8
                   -lam*(A*max(0,x*x-x/164)+h*x+c))
    return max(out)

def symmetric(xs):
    e = [Q(1)]+[Q(0)]*len(xs)
    for x in xs:
        for j in range(len(xs),0,-1):
            e[j] += x*e[j-1]
    return e

ps = [p for p in range(5,243,2) if prime(p)]
ms = [max(p**k for k in (1,2,3) if p**k<=243) for p in ps]
L0 = 486*prod(m//p for p,m in zip(ps,ms))
assert L0 == 12162150
C = [Q(0)]
for z in symmetric(ps):
    C.append(C[-1]+L0*hi(3)*z/68)
E = [z/162 for z in symmetric([Q(1,m-m//p) for p,m in zip(ps,ms)])]
LM = [logs(972)]
for m in sorted(ms,reverse=True):
    l,h = LM[-1]
    LM.append((l+lo(m),h+hi(m)))

assert Q(27182818,10**7) < exp_interval(1,11)[0]

@cache
def kernel(u,bin_):
    z = 1<<(2*u+64)
    x = Q(ceil(z*Q(10**7,27182818)**u),z)
    x *= Q(2,3) if bin_ else 1
    return min([up(C[-1]*x)]+[up(C[j]*x)+up(E[j]/(u-h))
                for j,(_,h) in enumerate(LM) if h<u])

def segment(a,b):
    d = 1/a-1/b
    out = [C[-1]*d]
    for j,(l,h) in enumerate(LM):
        if lo(a)>h:
            out.append(C[j]*d+E[j]*hi((hi(b)-l)/(lo(a)-h)))
        if lo(b-B)>h:
            out.append(d*(C[j]+E[j]*(b-B)/(lo(b-B)-h)))
        if a>B and lo(a-B)>h:
            out.append(C[j]*d+E[j]*(hi(b/a)-B*d)/(lo(a-B)-h))
    return min(out)

@cache
def band(u,shifted):
    k = kernel(u,True)
    if shifted and u<43:
        a = max(B,floor(exp_interval(u,160)[0]))
        b = ceil(exp_interval(u+1,160)[1])
        cuts = [a+Q((b-a)*i,128) for i in range(129)]
        k = min(k,sum(segment(x,y) for x,y in zip(cuts,cuts[1:])))
    return k

def charge(new=False,shifted=True):
    z = numerator(V,new)*kernel(V,False)
    z += sum(numerator(u+1,new)*band(u,shifted) for u in range(34,V))
    return ceil(W*z)

assert (charge(shifted=False),charge(),charge(True)) == (12063,9670,8760)
saved = 9670-8760
assert 54514-saved == 53604
assert Q(635060846076458,10**19)-Q(saved,10**9) == Q(625960846076458,10**19)
assert Q(625960846076458,10**19) < Q(62596085,10**12)

n,c,d,T,q = 14085077719262572575297,1,3,131111764407554040,8263
P = (163,811,1783)

def S(a,b,p):
    return (pow(3,a,p)+pow(5,b,p))%p

assert all(prime(p) and p%4==3 for p in P+(q,))
assert tuple(order(b,q) for b in (3,5)) == (8262,486)
assert all(pow(b,q-1,q*q)!=1 for b in (3,5))
assert T%3960==0 and v3(T)==2 and (n%3,n%32)==(0,1)
assert (n-S(c,d,32))%4==1 and all((n-S(c,d,p))%p for p in (7,11,19,23))
for j in range(3):
    assert all((n-S(c+9*T*j,d+3*T*k,163**2))%163**2==163
               for k in range(3))
assert all((n-S(c+T+3*T*j,d,p))%p for j in range(9) for p in P)
assert len({S(c+T+3*T*j,d,q) for j in range(9)})==9

# Retained-order control, including the auxiliary digit.
assert pow(5,3*T,3079)!=1
T1 = lcm(T,38)
assert v3(T1)==2 and all(pow(b,3*T1,3079)==1 for b in (3,5))
for h in (0,1):
    shifts = {S(c+3*T1*i,d+h*T1+3*T1*j,3079)
              for i in range(9) for j in range(3)}
    assert len(shifts)==1
assert S(c,d,3079)!=S(c,d+T1,3079)
print(9670,8760,saved,53604)
```

The joint screen uses the two full chart shifts, one per chart at each omitted row; choosing two alternate terminal points later, from the independent dropped observations, cannot introduce extra omitted-row readings. On a failed screen the old reference selection and old dual-reader subtraction remain available. Thus no selection based on omitted exceptional primes is used in certifying the new pure-reader branch. The updated strict natural representation-density lower bound is **99.999937403915%**. This is not a pointwise theorem.
