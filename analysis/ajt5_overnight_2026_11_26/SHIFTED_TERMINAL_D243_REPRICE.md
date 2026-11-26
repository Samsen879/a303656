# Shifted progression repricing for D=243

The D=243 row decreases from 12,063 to 9,670 units of 10^(-11) density. The D=81 row remains at 13,603, and all other rows, the cutoff, and all three infinite tails are unchanged. The finite subtotal falls from 68,649 to 66,256 units. Against SHIFTED_TERMINAL_D81_REPRICE.md this proves natural exception density **below 0.000084170085%**.

The calculation uses the original cutoff B=9*10^14 and the original endpoint exp(305), from log q<5D/4+log 2. The six-reader phase numerator, its 59/100 factor, and the maximum over axis choices are unchanged; all 271 endpoint values were checked exactly against THREE_CHART_SHALLOW_DENSITY_BOUND.md. Only the first nine log bins are repriced, through [42,43]. The endpoint term and all later bins retain the old kernel.

The D=243 weighted catalogue is different from D=81: it uses L_0=12,162,150 and the original set of optional powers, including 125,49,121,169. For threshold k the exact-set count C_k bounds terminals with fewer than k factors; the rest are covered by all k-factor progressions with coefficient E_k/162 and modulus at most M_k. With t−B>M_k use [Montgomery–Vaughan's interval bound](https://doi.org/10.1112/S0025579300004708), bounding the count by C_k plus E_k/162 times (t−B)/log((t−B)/M_k). Integrate using a fixed left-end denominator when available, or the right-end count by monotonicity, also allowing the old absolute bound and pure catalogue. Every option bounds the entire count. Multiple progressions may cover the same terminal without invalidating an upper bound. No prime count below B is assumed.

The exact rational replay gives 12,063 for the old row, 11,071 after cutoff clipping and refinement using the absolute bound, and 9,670 with the shifted bound. The ledger improves by exactly 2,393/10^11 in density units. This is neither a density-one result nor a pointwise resolution.

```python
from fractions import Fraction as Q
from functools import cache
from itertools import combinations
from math import ceil, floor, prod

B, W, D, V = 9*10**14, 10**11, 243, 305

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, h2 = series(Q(2))

@cache
def logs(x):
    y, k = Q(x), 0
    while y >= 2:
        y /= 2
        k += 1
    l, h = series(y)
    return Q(floor(W*(l+k*l2)),W), Q(ceil(W*(h+k*h2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]

assert ceil(Q(5*D,4)+h2)==V and lo(B)>34

@cache
def exps(n):
    a = t = Q(1)
    for j in range(1,161):
        t *= Q(n,j)
        a += t
    return a, a+t*Q(n,161)/(1-Q(n,162))

def depth(p,b):
    m,d = p-1,0
    while m%3 == 0:
        m //= 3
        d += 1
    while d and pow(b,3**(d-1)*m,p)==1:
        d -= 1
    return d

readers = (163,487,811,1459,1783,3079)
rows = [(Q(1,p+1),depth(p,3),depth(p,5)) for p in readers]
offset, lam = lo(lo(Q(3456,324)))-Q(1,34), Q(59,100)
union = sum(w for w,d,e in rows if max(d,e)>=4)
assert Q(820,159)*((hi(V)-offset)/54+union)<lo(1/lam)
stats = []
for i in (1,2):
    t = sum(z[0] for z in rows if z[i]>4)
    named = [(z[0],z[3-i]>=4) for z in rows if z[i]==4]
    m = sum(w for w,_ in named)
    a,h,c = [6*sum(prod(w for w,_ in s) for s in combinations(named,j)
                   if any(flag for _,flag in s)) for j in (1,2,3)]
    stats.append((offset-54*(m+t),t,m,a/2,h,c))

def U(s):
    z = Q(327,326)*s
    return z-z*z/2+z**3/6

@cache
def F(u):
    out = []
    for c,t,m,a,h,b in stats:
        s = (hi(u)-c)/54-t
        x,y,z = s-m,U(s),U(t)
        out.append(y**3+9*y*y*z*z+18*y*z**5+9*z**8
                   -lam*(a*max(0,x*x-x/164)+h*x+b))
    return max(out)

def sym(xs):
    e = [Q(1)]+[Q(0)]*len(xs)
    for x in xs:
        for j in range(len(xs),0,-1):
            e[j] += x*e[j-1]
    return e

ps = (5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,
      83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,
      167,173,179,181,191,193,197,199,211,223,227,229,233,239,241)
ms = [next(p**j for j in (3,2,1) if p**j<=D) for p in ps]
L0 = 2*D*prod(m//p for p,m in zip(ps,ms))
assert L0==12162150
C = [Q(0)]
for z in sym(ps):
    C.append(C[-1]+L0*hi(3)*z/68)
E = [e/162 for e in sym([Q(1,m-m//p) for p,m in zip(ps,ms)])]
LM = [logs(4*D)]
for m in sorted(ms,reverse=True):
    l,h = LM[-1]
    LM.append((l+lo(m),h+hi(m)))

def up30(x): return Q(ceil(10**30*x),10**30)

@cache
def old(u,interval):
    z = 1<<(2*u+64)
    x = Q(ceil(z*Q(10**7,27182818)**u),z)
    if interval:
        x *= Q(2,3)
    return min([up30(C[-1]*x)]+[up30(C[j]*x)+up30(E[j]/(u-h))
               for j,(_,h) in enumerate(LM) if h<u])

def segment(a,b,shift):
    d = 1/a-1/b
    opts = [C[-1]*d]
    for j,(l,h) in enumerate(LM):
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
            a,b = max(B,floor(exps(u)[0])),ceil(exps(u+1)[1])
            cut = [a+Q((b-a)*i,128) for i in range(129)]
            k = min(k,sum(segment(x,y,mode==2)
                          for x,y in zip(cut,cut[1:])))
        z += F(u+1)*k
    return ceil(W*z)

result = tuple(charge(i) for i in range(3))
assert result == (12063,11071,9670)
delta = Q(result[0]-result[2],W)
assert delta == Q(2393,W)
finite = 40008+13603+12063+2978-3
assert (finite,finite-2393) == (68649,66256)

# Enclosure of the exact verified D=81 ledger, in percent.
lower = Q(865630846076456,10**19)
upper = Q(865630846076458,10**19)
assert lower-100*delta < upper-100*delta < Q(84170085,10**12)
print(result, "revised exception bound < 0.000084170085%")
```
