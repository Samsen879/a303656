# Terminal-blind legal head menu improves the D=81 bound

**The \(D=81\) row falls from 13,603 to 13,199 units of \(10^{-11}\) density.** Every small-head reading admits a second legal class that changes the required ternary digit. Using a single terminal-blind menu for the whole first-blocker sum, the 404-unit saving gives a finite subtotal of **53,200** and an exception-density bound **strictly below \(0.000062192085\%\)**. The \(D=243\) row, cutoff, and all three tails carry forward. [Verified predecessor](https://github.com/Samsen879/a303656/commit/47e9971cf4cdb8f0aac9e6e53a0b3d614c7aacb6) · [Active \(D=81\) envelope](https://github.com/Samsen879/a303656/commit/8becd5b26695ec9511819ec6d050845e938fdc66)

### The second legal head has probability one

Use the published parity policy. Preselect **all** classes modulo \(3960\) satisfying its small-head tests and \(c\not\equiv0\bmod3,\ d\equiv0\bmod3\). This menu depends only on the small observations and is nonempty by the existing construction. Starting from any class in it, change only the exponent on the terminal axis by \(0,1320,2640\bmod3960\). This preserves its residue modulo \(440\) and modulo \(3\), and traverses the three possible residues modulo \(9\).

The moves preserve the tests at \(2,3,7,11,23\). At \(19\) the orders of \(3,5\) are \(18,9\), and either move gives three distinct shifts. At most one choice fails the unit test there. Thus every legal class has a legal alternative along **either** axis, for every small-head reading. [Published head and three-chart construction](https://github.com/Samsen879/a303656/blob/64e66c0720e2fbde33c2ee1ceb2ae34ba0458191/analysis/ajt5_overnight_2026_11_26/THREE_CHART_SHALLOW_DENSITY_BOUND.md)

The event being bounded is **first blocking of this menu**, throughout the ledger. An unrestricted finite blocker also blocks the menu. Every older per-terminal bound still applies. Its initial retained phase can be selected from the menu, and each of its prescribed repairs then stays in that phase’s class. The existential robust-branch choices are made over the menu, and their specific probes are fixed before reading the charged observations. All classes have the published parity pair, so the parity averages keep their original weights. An ordinary terminal remains repairable using its own primary digit, and the order catalogues are independent of the chosen phase domain. This is why the other rows and tails can carry forward. A \(D=81\) escape on a different head would not justify a subtraction from a first-blocker sum defined for just one fixed class. [First-blocker construction and small-head lock](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

### Matched restore and subtraction

Use the original depth-three dropped union, including auxiliary-only readers, and temporarily omit the common-Wieferich primes \(J\) among the retained rows. Select the reference phase from the reduced retained observations. Prepare its alternate by changing only the second 3-primary digit on the terminal axis to a legal alternative. All unheaded inert readers of that change exceed \(81\). Indeed, the candidates at or below \(81\) are \(19,55\), and \(19\) has already been checked. Repair the affected ordinary retained rows in increasing order. Their primary coordinates preserve the terminal orders and the **full** orders of the 15 named readers, whose largest prime factor is \(59\).

Prepare both charts before reading \(J\) or either dropped group. Every \(p\in J\) has depth at most two on **both** axes. Within each chart all moves are pure 3-primary increments divisible by \(9\), so even the auxiliary changes preserve the full orders at \(p\). Thus the joint unit screen excludes at most two residues per \(p\). Its uniform probability lower bound for \(\log q\le u\) is
\[
h(u)=\exp\!\left[-\left(2+\frac4{B-1}\right)
 \left(\frac1{u-\log4}+\log\frac{u-\log4}{\log B-\log4}\right)\right].
\]
On screen success use the prepared reference. On failure select a reference deterministically from the fully retained menu. As in the pinned proof, keep that reference if it satisfies the auxiliary-only rows at its reference digit, and otherwise select an auxiliary-compatible extension before reading the main readers. If there is no extension, the first-blocker event is empty. The reference prefix hits therefore have their original law \(w_p=1/(p+1)\) on both branches. [Audited restoration argument](https://github.com/Samsen879/a303656/blob/47e9971cf4cdb8f0aac9e6e53a0b3d614c7aacb6/analysis/ajt5_overnight_2026_11_26/D243_MATCHED_ALTERNATE_CHART_REPRICE.md)

The old subtraction uses exactly three reference shallow hits that include a named **dual** reader. The new subtraction uses exactly three reference shallow hits with at least one named **pure** reader and with every named hit pure. These events are disjoint. On screen success, each designated named pure reader misses the entire alternate chart because the lower-digit change changes its main-axis coset. The other designated readers can kill at most one prefix each at the fixed alternate auxiliary digit. Hence one prefix offers two terminal-distinct points to reserve. Requiring both to survive, together with the exact reference shallow hits, uses the original five-event avoidance budget per unused reader. The reference is required to pass its auxiliary-only tests on these events, so the selection rule keeps it.

Let \(x\) be the unnamed shallow weight and \(e_j\) the elementary symmetric sum of degree \(j\) over the named pure weights. The additional subtraction is
\[
\frac{h(u)}3\left[3e_1(x^2-x/164)_+ +6e_2 x+6e_3\right].
\]
It counts six assignments per triple and uses the distinct-pair bound for the two-unnamed case. The terminal factor is applied after all older observations. The resulting bound applies to growing-box misses and hence to all-exponent exceptions.

### Standalone replay

The code rebuilds the original and active \(D=81\) rows, keeps the 128 rational subintervals in each of the first nine log bins, and checks the new numerator’s padding and deep-mass endpoint inequalities separately at every bin endpoint. The ordinary \(379\to3727\) fixture checks both legal heads, a stripe across all auxiliary variants, and nine distinct alternate shifts.

```python
from fractions import Fraction as Q
from functools import cache
from itertools import combinations
from math import ceil, floor, isqrt, lcm, prod

B, W, V = 9*10**14, 10**11, 102

def prime(p):
    return p > 1 and all(p%i for i in range(2, isqrt(p)+1))

def order(b, p):
    return next(i for i in range(1, p) if pow(b, i, p) == 1)

def v3(m):
    return 0 if m % 3 else 1 + v3(m//3)

def series(y):
    z = (y-1)/(y+1)
    a = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return a, a+2*z**25/(25*(1-z*z))

L2, H2 = series(Q(2))

@cache
def logs(x):
    y, k = Q(x), 0
    while y >= 2:
        y /= 2
        k += 1
    a, b = series(y)
    return Q(floor(W*(a+k*L2)), W), Q(ceil(W*(b+k*H2)), W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]

@cache
def exp_bounds(x, k):
    assert 0 <= x < k+2
    s = t = Q(1)
    for j in range(1, k+1):
        t *= Q(x, j)
        s += t
    return s, s+t*Q(x, k+1)/(1-Q(x, k+2))

small = (7,11,19,23)
assert [tuple(order(b,p) for b in (3,5)) for p in small] == [
    (6,6),(5,5),(18,9),(11,22)]
assert [p for p in range(19,82,36) if prime(p)] == [19]

readers = (163,271,379,487,811,919,1459,1567,1783,1999,
           2539,2647,2971,3079,3187)
assert [p for p in range(55,3457,108) if prime(p)] == list(readers)
orders = [tuple(order(b,p) for b in (3,5)) for p in readers]
assert lcm(*(o for pair in orders for o in pair)) == (
    2*3**6*5*7**2*11*17*19*29*37*47*59)
rows = [(Q(1,p+1),tuple(map(v3,o))) for p,o in zip(readers,orders)]
union = sum(w for w,d in rows if max(d)>=3)
offset = lo(lo(32))-Q(1,34)
assert Q(820,159)*((hi(V)-offset)/18+union) < lo(3)
assert lo(B)>34 and ceil(Q(405,4)+H2)==V

@cache
def keep(u):
    reciprocal = 1/(u-hi(4))+hi((u-lo(4))/(lo(B)-hi(4)))
    z = Q(ceil(10**20*(2+Q(4,B-1))*reciprocal),10**20)
    return Q(floor(10**15/exp_bounds(z,40)[1]),10**15)

a0 = Q(327,326)
stats = []
for i, off in enumerate((Q(47,50),Q(221,250))):
    t = sum(w for w,d in rows if d[i]>3)
    named = [(w,d[1-i]>=3) for w,d in rows if d[i]==3]
    m = sum(w for w,_ in named)
    dual = [6*sum(prod(w for w,_ in group)
                  for group in combinations(named,j)
                  if any(flag for _,flag in group))
            for j in (1,2,3)]
    pure = [w for w,flag in named if not flag]
    extra = [6*sum(prod(group) for group in combinations(pure,j))
             for j in (1,2,3)]
    dual[0] /= 2
    extra[0] /= 2
    stats.append((off,t,m,dual,extra))

    for u in range(35,V+1):
        e, jmax = (lo(u)-off)/18, (hi(u)-off)/18
        low, deriv = 1-a0*jmax/2, a0*(1-a0*jmax)
        a,h,c = [x+keep(u)*y for x,y in zip(dual,extra)]
        assert m+t<e and t<e/2 and a0*jmax<1
        assert (a/(2*m)+h/m**2)/3 < 3*low**2*deriv
        j = jmax/2
        slope = (3*deriv-18*a0**2*j-90*a0**5*j**3/low
                 -72*a0**8*j**5/low**2)
        assert slope*low**2 > (2*a/(e/2)+h/(e/2)**2)/3
        cap = a0**3/8+9*a0**4*jmax/16+18*a0**6*jmax**3+9*a0**8*jmax**5
        assert (low*(1-t/e))**3-(a/e+h/e**2+c/e**3)/3 > cap

def occupancy(x):
    z = a0*x
    return z-z*z/2+z**3/6

def numerator(u, new):
    values = []
    for off,t,m,dual,extra in stats:
        s = (hi(u)-off)/18-t
        x,y,z = s-m,occupancy(s),occupancy(t)
        a,h,c = [v+(keep(u)*w if new else 0)
                 for v,w in zip(dual,extra)]
        values.append(y**3+9*y*y*z*z+18*y*z**5+9*z**8
                      -(a*max(0,x*x-x/164)+h*x+c)/3)
    return max(values)

def symmetric(xs):
    e = [Q(1)]+[Q(0)]*len(xs)
    for x in xs:
        for j in range(len(xs),0,-1):
            e[j] += x*e[j-1]
    return e

ps = [p for p in range(5,81,2) if prime(p)]
ms = [p*p if p*p<=81 else p for p in ps]
scale = 162*prod(m//p for p,m in zip(ps,ms))
assert scale==5670
C = [Q(0)]
for x in symmetric(ps):
    C.append(C[-1]+scale*hi(3)*x/68)
E = [x/54 for x in symmetric([Q(1,m-m//p) for p,m in zip(ps,ms)])]
moduli = [324]
for m in sorted(ms,reverse=True):
    moduli.append(moduli[-1]*m)
L = list(map(logs,moduli))

@cache
def kernel(u, band):
    x = (Q(2,3) if band else 1)/exp_bounds(u,160)[0]
    return min(C[j]*x+E[j]*(hi((u+1-l)/(u-h)) if band else 1/(u-h))
               for j,(l,h) in enumerate(L) if h<u)

def segment(a,b):
    d = 1/a-1/b
    choices = []
    for j,(l,h) in enumerate(L):
        if lo(a)>h:
            choices.append(C[j]*d+E[j]*hi((hi(b)-l)/(lo(a)-h)))
        if lo(b-B)>h:
            choices.append(d*(C[j]+E[j]*(b-B)/(lo(b-B)-h)))
        if a>B and lo(a-B)>h:
            choices.append(C[j]*d+E[j]*(hi(b/a)-B*d)/(lo(a-B)-h))
    return min(choices)

@cache
def band_weight(u, shifted):
    k = kernel(u,True)
    if shifted and u<43:
        a = max(B,floor(exp_bounds(u,160)[0]))
        b = ceil(exp_bounds(u+1,160)[1])
        cuts = [a+Q((b-a)*i,128) for i in range(129)]
        k = min(k,sum(segment(x,y) for x,y in zip(cuts,cuts[1:])))
    return k

def charge(new=False, shifted=True):
    x = numerator(V,new)*kernel(V,False)
    x += sum(numerator(u+1,new)*band_weight(u,shifted) for u in range(34,V))
    return ceil(W*x)

assert (charge(shifted=False),charge(),charge(True))==(17949,13603,13199)
assert 13603+8760+28266+2975==53604
assert 13199+8760+28266+2975==53200
upper = Q(625960846076458,10**19)-Q(404,10**9)
assert upper==Q(621920846076458,10**19)<Q(62192085,10**12)

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p

for c in range(18):
    for d in range(18):
        assert len({S(c+1320*i,d,19) for i in range(3)})==3
        assert len({S(c,d+1320*i,19) for i in range(3)})==3

n,T,p,q,c,d = 364575509889,300191513160,379,3727,1,3
assert all(prime(r) and r%4==3 for r in (p,q))
assert [order(b,q) for b in (3,5)]==[3726,414]
assert all(pow(b,q-1,q*q)!=1 for b in (3,5))
assert (T%9,T%440)==(3,0)
assert (c%3960,(c+T)%3960,d%3960)==(1,2641,3)
assert (n%3,n%32)==(0,1)
for a in (c,c+T):
    assert (n-S(a,d,32))%4==1 and (n-pow(5,d,3))%3
    assert all((n-S(a,d,r))%r for r in small)
assert all((n-S(c+9*T*i,d+3*T*j,p*p))%(p*p)==p
           for i in range(3) for j in range(3))
assert all((n-S(c+T+3*T*i,d+3*T*j,p))%p
           for i in range(9) for j in range(3))
assert len({S(c+T+3*T*i,d,q) for i in range(9)})==9
print(13603,13199,404,53200)
```

The unaffected first-blocker charges retain the same law because their reference selection depends on retained observations and on the terminal-blind menu only; a per-terminal projection step stays within its selected legal class. The cumulative loss is still calculated on one fixed menu, not as a sum over unrelated starting phases. The verified strict natural representation-density lower bound is **99.999937807915%**; the exact sublogarithmic matching theorem transfers this same numerical bound to \(o(\log X)\) distinct-label representations. Neither statement establishes density one or pointwise representability.
