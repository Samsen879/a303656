# Occupancy and catalogue bounds give representation density above 99.980329%

**The exception-density bound improves to below \(0.019671\%\)** without extending the prime search. The largest remaining term was the finite \(D=81\) cover charge. An occupancy bound reduces that term, and the published single-base Wieferich catalogue allows a larger saving in the prime-source tail. [Previous rational certificate](https://github.com/Samsen879/a303656/blob/debfafbeee90f7b79045a21085a60d5e327e3103/analysis/ajt5_overnight_2026_11_26/PARITY_FILTERED_INTERCEPT_DENSITY_BOUND.md)

| Charge, in density units | Previous | Revised |
|---|---:|---:|
| Finite \(D=81\) | \(0.00014055070\) | \(0.00010897636\) |
| Prime-source tail | \(0.00013014226757526498\ldots\) | \(0.00000001633\) |
| All other charges and inherited slack | \(0.00008771411242473502\ldots\) | same |
| **Total** | **\(0.00035840708\)** | **\(0.00019670680242473502\ldots\)** |

### Count occupied prefixes in the \(D=81\) tree

Each shallow reader can kill one of three prefixes or none. Conditional on the retained phase, these categorical observations are independent across primes. The probability that \(k\) specified prefixes are all hit is at most the product of their individual hit probabilities. To prove this, condition on one prefix being absent. Replace every draw of that prefix by a fresh draw conditioned to avoid it. This gives the conditional law and can only add hits to the other prefixes. Repeating the resulting inequality gives the product bound.

For shallow weights \(w_p=1/(p+1)\) with sum \(s\), the hit probability of a specified prefix is \(1-\prod_p(1-w_p)\). Every such reader has \(p\ge163\), since the first candidate in the progression is the composite \(55\). Therefore, with \(a=327/326\),
\[
-\log(1-w_p)\le a w_p,\qquad
1-\prod_p(1-w_p)\le U(s):=as-\frac{(as)^2}{2}+\frac{(as)^3}{6}.
\]
The cover polynomial is consequently bounded by \(P(U(s),t)\), where \(P(x,t)=x^3+9x^2t^2+18xt^5+9t^8\) and \(t\) is the deep-reader weight. The shallow and deep groups use disjoint prime observations. [Published cover polynomial and integration range](https://github.com/Samsen879/a303656/blob/c09792c9285da96523960fc20bfe4a939f31151a/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COVER_TREE_DENSITY_BOUND.md)

For \(L=s+t\le53/250\), the replay checks \(U(L)\ge0.89L\) and \(U'(L)\ge0.78\). Hence \(U(L)^3-U(s)^3\ge0.78(0.89)^2tL^2\). The three mixed terms, divided by \(tL^2\), sum to at most \((4/3)a^2L+18aL^3+9L^5\). The resulting bound is
\[
P(U(s),t)\le U(L)^3-\tfrac18 tL^2
           \le U(L)^3-\tfrac18\tau_bL^2,
\]
where \(\tau_b\) is the verified deep weight in the existing reader window. This numerator is increasing in \(L\), and after substituting the published \(L_b(\log q)\), its weight divided by \(q\) is decreasing. Thus the same outward-rounded partial summation applies. **This replacement alone** gives \(0.032683274\%\).

### Reprice the prime-source tail

The existing cutoff \(B=9\cdot10^{14}\) is within Dorais–Klyve’s search for **each** base. For the inert sources \(10^5<r\le B\), the only exceptions to both axes being ordinary are \(1006003\) and \(1645333507\). Keep their \(1/r\) depth charge. For every other source in the interval, the already proved ordinary-source charge is at most \(1/r^2+2S_r/r\). No modular search is added. [Dorais–Klyve, §4.1 and Tables 5–6](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf) · [Ordinary-source compensation bound](https://github.com/Samsen879/a303656/blob/a7232f58d5beb92a71da1df5f1c831ecdf2f2660/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md)

Use \(R_r\le S_r=(\log r+1/2)/(r-1)\). For the ordinary range, integrate \(S_r/r^2+2S_r^2/r\) over all integers above \(P=10^5\), majorizing \(1/(r-1)\) by \(P/((P-1)r)\). For \(r>B\), keep the unconditional \(1/r\) depth charge and integrate from \(B\). The two robust-reader branches cost at most \(2^{1-r}+2^{-r}\) per source by the existing factorial bounds, so \(3\cdot2^{-P}\) covers both throughout the tail. This accounts for the entire old prime-source tail.

### Standalone rational replay

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt, prod

W,P,B = 10**11,10**5,9*10**14

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

# Completeness through B comes from the published catalogue.
assert 150000*prod((2,3,5,7,11,13,17,19,23,29)) > B
catalog = {3:(11,1006003),
           5:(20771,40487,53471161,1645333507,6692367337,188748146801)}
assert all(pow(b,p-1,p*p)==1 for b,ps in catalog.items() for p in ps)
named = [p for ps in catalog.values() for p in ps if P<p<=B and p%4==3]
assert sorted(named)==[1006003,1645333507]

oldtail = Q(10001,10000)*(hi(P)+Q(3,2))/P
h,A = hi(P)+Q(1,2),Q(P,P-1)
assert 3*P*h/(P-1)**2<Q(1,2)
ordinary = (A*(h/2+Q(1,4))+2*A*A*(h*h/2+h/2+Q(1,4)))/P**2
named_charge = sum((hi(r)+Q(1,2))/(r*(r-1)) for r in named)
newtail = up(ordinary+named_charge+(hi(B)+Q(3,2))/(B-1)+Q(3,2**P))
assert newtail==Q(1633,W)

def depth(b,p):
    m = p-1
    while m%3==0 and pow(b,m//3,p)==1:
        m //= 3
    j = 0
    while m%3==0:
        j += 1
        m //= 3
    return j

stats = []
for b,c in ((3,Q(47,50)),(5,Q(221,250))):
    rows = [(p,depth(b,p)) for p in range(55,3457,108)
            if all(p%i for i in range(2,isqrt(p)+1))]
    ws = [Q(1,p+1) for p,k in rows if k==3]
    tau = sum(Q(1,p+1) for p,k in rows if k>=4)
    M,A,K = sum(ws),sum(w*w for w in ws),sum(w**3 for w in ws)
    assert lo(lo(32))-Q(1,34)-18*(M+tau)>c
    assert tau<Q(1,8)<(lo(34)-c)/18
    stats.append((c,M,A,K,tau))

a,J,b,d,g = Q(327,326),Q(53,250),Q(89,100),Q(39,50),Q(1,8)
assert (hi(108)-Q(221,250))/18<J and lo(B)>34
assert 1-a*J/2>=b and a*(1-a*J)>=d and a*J<1
assert d*b*b-(Q(4,3)*a*a*J+18*a*J**3+9*J**5)>g
assert 3*b*b*d>2*g and b**3-g>Q(1,2)
assert 3*a**3<18*34*Q(1,8)*Q(1,2)

def numerator(u,new):
    v = []
    for c,M,A,K,tau in stats:
        L = (hi(u)-c)/18
        y = a*L
        U = y-y*y/2+y**3/6
        v.append(U**3-g*tau*L*L if new else
                 L**3-3*A*L+2*K-tau*(L-M)**2/2)
    return max(v)

l,u = logs(324)
def charge(new):
    return up((numerator(108,new)/(108-u)+sum(
        numerator(t+1,new)*hi((t+1-l)/(t-u))
        for t in range(34,108)))/54)

old81,new81 = charge(False),charge(True)
assert (old81,new81)==(Q(14055070,W),Q(10897636,W))
answer = Q(35840708,W)-oldtail+newtail-old81+new81
assert answer==Q(9835340121236751,50000000000000000000)
assert answer<Q(19671,10**8)
print(float(100*answer), "%")
```

This is an upper bound for the growth-box miss density and hence for the all-exponent exception density. It uses no assumed genuine common Wieferich examples.

The catalogue dependency is specifically the separate base-3 and base-5 search ranges reported in §5/Table 2 and the zero entries in Tables 5–6 of Dorais–Klyve, together with their preexisting small list. The huge published search has not been rerun; the replay reruns only the stated exact residues and rational estimates. The factorial tails follow from \(m!\ge(m/e)^m\) and the verified decreasing endpoint bound \(3P(\log P+1/2)/(P-1)^2<1/2\); the main tail integrands are decreasing beyond \(P\), so integrating from \(P\) is upward-safe.

For the occupancy inequality, if \(A\) means a designated prefix is hit and \(B\) means a chosen collection of other prefixes are hit, conditioning on \(A^c\) is implemented by replacing just the draws of that prefix by independent draws conditioned to avoid it. This only helps \(B\); consequently \(\Pr(B\mid A)\le\Pr(B)\), and induction gives the stated product bound.
