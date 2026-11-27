# Repricing the largest eligible non-cube row: D=81

The existing D=81 charge decreases from 17,949 to 13,603 units of 10^(-11) density. The finite subtotal decreases from 72,995 to 68,649 units. Replacing only this row in SHIFTED_BRUN_TITCHMARSH_CUBE_REPRICE.md gives natural exception density **below 0.000086563085%**. No cutoff, other row, or infinite-tail term is changed.

Keep the earlier common-Wieferich cutoff B=9*10^14, the terminal endpoint exp(102), and the original three-chart numerator including the maximum across axis choices. Only the first nine log bins are repriced. Clip their integration at B, since no eligible terminals are below that cutoff. On each subinterval the absolute or shifted envelope can be used, whichever is smaller. The endpoint term and every later log interval retain the old formula.

For an optional-factor threshold k, keep the old exact-set catalogue bound C_k for terminals with fewer than k present factors. For the rest, cover by the union of the progressions for all k-factor subsets. The moduli are at most M_k, with the sum of reciprocal totients inherited from MAX_ORDER_81_TERMINAL_DENSITY_BOUND.md. No overlap subtraction is made. If t−B>M_k, applying [Montgomery–Vaughan's interval bound, Theorem 2](https://doi.org/10.1112/S0025579300004708) to each progression bounds the eligible count by C_k plus (t−B)/log((t−B)/M_k) times the same reciprocal-totient factor. On a subinterval [a,b] with a−B>M_k the denominator can be fixed at a; the integral numerator is log(b/a)+B/b−B/a. If only the upper endpoint allows an interval estimate, use its counting bound throughout by monotonicity. Each candidate bounds the entire count, so minimization introduces no overlap assumption.

The exact rational replay reconstructs the old row, obtains 15,777 by cutoff clipping alone, and obtains 13,603 using the shifted inequality and 128 rational subintervals per early log bin (an initial 16-subinterval check gave 13,645). The exact ledger change is 4,346/10^11 in density units. This does not settle the conjecture or establish density one.

```python
from fractions import Fraction as Q
from functools import cache
from itertools import combinations
from math import ceil, floor, prod

B, W, V = 9*10**14, 10**11, 102

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, h2 = series(Q(2))

@cache
def logs(x):
    y, k = Q(x), 0
    assert y >= 1
    while y >= 2:
        y /= 2
        k += 1
    l, h = series(y)
    return Q(floor(W*(l+k*l2)),W), Q(ceil(W*(h+k*h2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]

@cache
def exps(n):
    a = t = Q(1)
    for j in range(1,161):
        t *= Q(n,j)
        a += t
    return a, a+t*Q(n,161)/(1-Q(n,162))

# Fixed reader list from the published window.
readers = (163,271,379,487,811,919,1459,1567,1783,1999,2539,
           2647,2971,3079,3187)

def depth(p,b):
    d,m = 0,p-1
    while m%3 == 0:
        m //= 3
        d += 1
    while d and pow(b,3**(d-1)*m,p) == 1:
        d -= 1
    return d

weights = [(Q(1,p+1),depth(p,3),depth(p,5)) for p in readers]
stats = []
for i,c in ((1,Q(47,50)),(2,Q(221,250))):
    t = sum(z[0] for z in weights if z[i]>3)
    named = [(z[0],z[3-i]>=3) for z in weights if z[i]==3]
    m = sum(w for w,_ in named)
    f,g,h = [6*sum(prod(w for w,_ in s) for s in combinations(named,k)
                   if any(dual for _,dual in s)) for k in (1,2,3)]
    stats.append((c,t,m,f/2,g,h))

def U(s):
    z = Q(327,326)*s
    return z-z*z/2+z**3/6

@cache
def F(u):
    vals = []
    for c,t,m,a,b,d in stats:
        s = (hi(u)-c)/18-t
        x,y,z = s-m,U(s),U(t)
        vals.append(y**3+9*y*y*z*z+18*y*z**5+9*z**8
                    -(a*max(0,x*x-x/164)+b*x+d)/3)
    return max(vals)

def sym(xs):
    e = [1]+[0]*len(xs)
    for x in xs:
        for j in range(len(xs),0,-1):
            e[j] += x*e[j-1]
    return e

ps = (5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79)
ms = [p*p if p*p<=81 else p for p in ps]
C = [Q(0)]
for z in sym(ps):
    C.append(C[-1]+5670*hi(3)*z/68)
E = [Q(z)/54 for z in sym([Q(1,m-m//p) for p,m in zip(ps,ms)])]
M = [324]
for m in sorted(ms,reverse=True):
    M.append(M[-1]*m)
L = list(map(logs,M))

def old(u,is_bin):
    return min((Q(2,3) if is_bin else 1)*C[j]/exps(u)[0]
               +E[j]*(hi((u+1-l)/(u-h)) if is_bin else 1/(u-h))
               for j,(l,h) in enumerate(L) if h<u)

def segment(a,b,shift):
    d = 1/a-1/b
    opts = []
    for j,(l,h) in enumerate(L):
        if lo(a)>h:
            opts.append(C[j]*d+E[j]*hi((hi(b)-l)/(lo(a)-h)))
        if shift and lo(b-B)>h:
            opts.append((C[j]+E[j]*(b-B)/(lo(b-B)-h))*d)
        if shift and a>B and lo(a-B)>h:
            opts.append(C[j]*d+E[j]*(hi(b/a)-B*d)/(lo(a-B)-h))
    return min(opts)

def charge(mode):
    z = F(V)*old(V,False)
    for u in range(34,V):
        k = old(u,True)
        if mode and u<43:
            a = max(B,floor(exps(u)[0]))
            b = ceil(exps(u+1)[1])
            cut = [a+Q((b-a)*i,128) for i in range(129)]
            k = min(k,sum(segment(x,y,mode==2)
                          for x,y in zip(cut,cut[1:])))
        z += F(u+1)*k
    return ceil(W*z)

rows = tuple(charge(i) for i in (0,1,2))
assert rows == (17949,15777,13603)
delta = Q(rows[0]-rows[2],W)
assert delta == Q(4346,W)
finite = 40008+17949+12063+2978-3
assert (finite,finite-4346) == (72995,68649)

# Verified enclosure of the exact 4f5bf29 ledger, in percent.
lo_pct = Q(909090846076456,10**19)
hi_pct = Q(909090846076458,10**19)
assert lo_pct-100*delta < hi_pct-100*delta < Q(86563085,10**12)
print(rows, "revised exception bound < 0.000086563085%")
```
