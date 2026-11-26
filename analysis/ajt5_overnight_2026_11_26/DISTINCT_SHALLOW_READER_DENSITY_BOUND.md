# Distinct shallow readers give representation density above 99.912615%

**The published exception-density bound improves to below \(0.087385\%\)**, with the same prime-search cutoff and all tail terms retained. The rational replay gives \(0.08738489574613263\ldots\%\). The saving is in the finite \(D=81\) term: a shallow reader can kill only one of the three prefixes, so that reader cannot be used twice in a cover. Keeping the already verified shallow and deep reader weights separate gives a further saving. [Published cover-tree bound](https://github.com/Samsen879/a303656/blob/c09792c9285da96523960fc20bfe4a939f31151a/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COVER_TREE_DENSITY_BOUND.md)

### A disjoint saving in the \(D=81\) term

On the selected base \(b\), the nine variants have three prefixes. A shallow prime \(p\), whose \(3\)-order depth is exactly three, sees three distinct shifts modulo \(p\), one per prefix. Conditional on the retained observations, its four outcomes are disjoint: it kills no prefix with probability \(1-3w_p\), or kills one specified prefix with probability \(w_p=1/(p+1)\). The starting phase was selected before reading \(n_p\). A prefix-free cover therefore uses \(p\) at most once. The replay checks these three distinct prefixes on the actual bases at \(379\) and \(163\).

Write \(s,t\) for the full shallow and deep weight sums. The published cover polynomial is
\[
P(s,t)=s^3+9s^2t^2+18st^5+9t^8.
\]
For the shallow readers in the **existing** window \(p\le3456\), set \(M=\sum w_p\), \(A=\sum w_p^2\), and \(K=\sum w_p^3\). Let \(\tau\) be the weight of the verified deep readers in that same window. Put \(L=s+t\). Keeping only terms in which each named shallow reader occurs at most once gives the bound
\[
F_b(L)=L^3-3AL+2K-\tfrac12\tau(L-M)^2.
\]

To see this, write \(s=s_0+M\). In the Taylor expansion in \(M\), replace \(M^j\) by \(j!\) times the \(j\)-th elementary symmetric sum of the named weights. For \(j=1,2,3\), the Taylor coefficients of \(P\) are bounded by the corresponding coefficients of \((s_0+t+M)^3\) on the verified range \(L\le53/250\). The constant coefficient satisfies
\[
P(s_0,t)\le (s_0+t)^3-\tfrac12t(s_0+t)^2.
\]
Indeed, the loss from replacing \(s_0^3\) by \((s_0+t)^3\) is at least \(t(s_0+t)^2\), and the other terms consume less than half of that loss. Expanding the distinct-reader cubic and using \(t\ge\tau\) gives the displayed \(F_b\).

Using the same reader window separately on each axis gives \(L_b(u)\le(\log u-c_b)/18\), where \(u=\log q\), \(c_3=47/50\), and \(c_5=221/250\). The reader progression has modulus \(108\). For the terminal progression modulo \(324\), use the same partial summation as the published proof, with numerator \(\max_b F_b(L_b(u))\). Each numerator is increasing over the relevant interval, and dividing by \(q\) gives a decreasing weight. For example, on this range \(F_b(L)\ge0.9L^3\), \(F'_b(L)\le3L^2\), and \(dL_b/d\log q=1/(18u)\). [Montgomery–Vaughan Brun–Titchmarsh bound](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED)

| \(D=81\) finite term | Upward-rounded bound |
|---|---:|
| Published | \(0.00014259727\) |
| Distinct shallow readers, with the published envelope | \(0.00014249240\) |
| Distinct readers, separate axis envelopes, and verified deep weights | \(0.00014055070\) |

The first saving is entirely from the disjoint prefix outcomes. The full replacement saves \(0.00000204657\) in density units.

### What the six-head theorem contributes

It excludes an all-menu first blocker at any of the first seven **actual** common Wieferich terminals. The numerical envelope sums over eligible prime classes without tracking that rank. It also charges covers for a selected phase, which can occur while another head survives. Neither fact identifies a positive numerical summand to delete. The saving above instead applies at every eligible \(D=81\) terminal and uses no assumption about the existence or location of genuine exceptional primes. [Seven-terminal fixed-menu theorem](https://github.com/Samsen879/a303656/blob/a0e12a2f3f7efb859a549c4f47bda86913ecc2a0/analysis/ajt5_overnight_2026_11_26/SIX_HEADS_SEVEN_TERMINALS_LOW_ORDER_CORE.md)

### Standalone rational replay

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt

W, H = 10**11, 10**6

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
    return Q(floor(W*(a+k*l2)),W),Q(ceil(W*(b+k*u2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)

def depth(b,p):
    m = p-1
    while m%3==0 and pow(b,m//3,p)==1:
        m //= 3
    j = 0
    while m%3==0:
        m //= 3
        j += 1
    return j

c0 = Q(22,25)
cs = {3:Q(47,50),5:Q(221,250)}
stats = {}
for b in (3,5):
    rows = [(p,depth(b,p)) for p in range(55,3457,108)
            if all(p%i for i in range(2,isqrt(p)+1))]
    w = [Q(1,p+1) for p,a in rows if a==3]
    M,A,K = sum(w),sum(x*x for x in w),sum(x**3 for x in w)
    tau = sum(Q(1,p+1) for p,a in rows if a>=4)
    assert lo(lo(32))-Q(1,34)-18*(M+tau)>cs[b]>=c0
    assert M+tau<Q(1,8)<(lo(34)-cs[b])/18
    assert A<Q(1,10000) and tau<Q(1,80)
    stats[b] = M,A,K,tau

J = Q(53,250)
assert (hi(108)-min(cs.values()))/18<J
assert Q(4,3)*J+18*J**3+9*J**5<Q(1,2)
assert lo(9*10**14)>34

l,u = logs(324)
def envelope(num):
    return (num(108)/(108-u)+sum(
        num(t+1)*hi((t+1-l)/(t-u)) for t in range(34,108)))/54

def cubic(t,c):
    return ((hi(t)-c)/18)**3

def num(t,constants,deep):
    terms = []
    for b,(M,A,K,tau) in stats.items():
        L = (hi(t)-constants[b])/18
        terms.append(L**3-3*A*L+2*K-deep*tau*(L-M)**2)
    return max(terms)

S = (hi(81)+Q(1,2))/54
R = min(S,(1/(108-u)+hi((108-l)/(34-u)))/54)
old81 = up(min(R*Q(9,2)*S*S,R*3*S*S,R*27*S**3,
               envelope(lambda t:cubic(t,-Q(1,5)))))
base81 = up(envelope(lambda t:cubic(t,c0)))
repeat = up(envelope(lambda t:num(t,{3:c0,5:c0},0)))
new81 = up(envelope(lambda t:num(t,cs,Q(1,2))))
assert (old81,base81,repeat,new81) == tuple(
    Q(i,W) for i in (33452894,14259727,14249240,14055070))

oldtail = Q(27,10)/H*(2*(hi(2*H)+Q(1,2))+2*u2)
L = hi(H)+Q(1,2)
newtail = oldtail/2+Q(81,8)/H**2*(L**3/2+3*L*L/4+3*L/4+Q(3,8))
answer = Q(111020555,W)-(old81-new81)-(oldtail-newtail)
assert answer<Q(87385,10**8)

for b,p in ((3,379),(5,163)):
    step,m = 3960*7*p,p*p
    z = [(pow(3,3960+(step*j if b==3 else 0),m)
          +pow(5,3960+(step*j if b==5 else 0),m))%m for j in range(9)]
    assert depth(b,p)==3 and len({x%p for x in z})==3
    assert z==z[:3]*3
    for i in range(3):
        n = z[i]+p
        assert [j for j,x in enumerate(z) if (n-x)%p==0]==list(range(i,9,3))

print(float(100*answer), "%")
```

This refines the published growth-box miss bound, which also bounds the original all-exponent exception density. The phase checks use ordinary readers. The numerical saving requires no assumed common Wieferich examples and gives no density-one or pointwise conclusion.

For the coefficient comparison, the linear and quadratic coefficients in \(M\) are bounded using \(t<1/3\) and \(18t^5\le3t^2\). For the constant term, divide the three extra terms by \(t(s_0+t)^2\): their sum is bounded by \(\tfrac43 J+18J^3+9J^5<1/2\), where \(J=53/250\) bounds \(s_0+t+M\). Distinct named readers' weights multiply because each assignment then uses different prime observations; no independence is imposed between the three alternatives of a single named reader.

For the monotonicity check, \(L\ge1/8,\ A<1/10000,\ \tau<1/80,\ L\le J\) imply \(F'_b(L)=3L^2-3A-\tau(L-M)>0\), \(F'_b(L)\le3L^2\), and \(F_b(L)\ge0.9L^3\). These bounds also give \(d(F_b(L_b(\log q))/q)/dq<0\) on the published integration range. The final strict threshold is a density of exceptions below \(0.00087385\), hence natural representation density above \(0.99912615\).
