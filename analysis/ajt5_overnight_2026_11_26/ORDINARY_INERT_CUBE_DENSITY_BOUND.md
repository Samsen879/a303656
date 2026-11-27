# Two-axis cube repairs give representation density above 99.999886501%

The ordinary inert cube repair lowers the exception-density bound to **below \(0.000113499\%\)**, from \(0.00015339189744333908\ldots\%\). The eight finite cube charges fall from \(40141/10^{11}\) to \(248/10^{11}\) in density units. In particular, \(D=31^3\) falls from \(27014/10^{11}\) to \(186/10^{11}\). The cutoff and all three infinite tails are carried forward. The bound applies to growth-box misses and hence to all-exponent exceptions. [Reconciled predecessor](https://github.com/Samsen879/a303656/blob/b0d4e8dbac4e9dd86893925667a61ec69b530f75/analysis/ajt5_overnight_2026_11_26/RECONCILED_DENSITY_LEDGER.md)

### Cube repair

Let \(D=r^3\) be the largest order prime power across both axes at a genuine terminal \(q\). Assume \(r\ge31\) is inert and both bases are ordinary at \(r\). Select a base \(b\) whose order at \(q\) contains \(D\), and use base \(3\) when both do. Write \(S=S_D\) for the inherited upper bound on the total reciprocal weight of older readers on either axis at depth at least three. Their union lies in the same progression \(p\equiv1\bmod D,\ p\equiv3\bmod4\).

A phase is robust if its residual at \(r\) has even valuation below three. There are three cases.

1. If a robust phase exists after dropping the \(b\)-readers and the source test, its \(r\) variants give the usual \(G_r(S)\) charge. This is already in the finite factorial allowance.
2. If a robust phase exists after dropping both axes’ readers but the first case fails, vary the other axis through its \(r\) third-digit choices. The readers on that axis alone must kill all \(r\) variants. Each such reader kills at most one, so this costs at most \((rS)^r/r!\).
3. Otherwise, fix the retained observations and let \(V\) be the set of surviving shifts modulo \(r^3\) with the source test omitted. An exceptional source reading must lie in \(V\). Two different exceptional readings must differ at valuation one, since a difference of valuation zero or two would give a robust phase. There are at most \(r\) such readings, giving the inherited gate of probability \(r^{-2}\).

In the third case, choose a matching phase using the retained observations and \(n_r\bmod r^3\). Ordinary lifting makes the next source equation linear in the two third digits. Its solutions are \(y=s+mx\bmod r\), with \(m\ne0\) and \(s\) uniform over the next source digit. A fourth-digit change on the auxiliary axis makes the residual have **exact valuation four**. This change is invisible at \(q\) because \(D\) is maximal. An older dropped reader can see the fourth digit, but each repaired phase is fixed before its observation is read.

At \(q\) the repair line has shifts \(A\xi^x+B\zeta^{s+mx}\). A nonconstant line has fibers of size at most \(K=\lfloor(1+\sqrt{4r-3})/2\rfloor\). When the two characters are distinct and nontrivial, each nonzero difference \(t\) allows at most one \(x\) with equal shifts at \(x,x+t\), giving \(K(K-1)\le r-1\). The single-character cases are injective. A first blocker must therefore lose at least \(r-K\) repaired phases. Their expected number of losses is at most \(rS\), so the conditional charge is \(\gamma=\min(1,rS/(r-K))\). This uses no independence between phase losses. [Whole-line fiber argument](https://github.com/Samsen879/a303656/blob/a476e9ca22a16358c763229700f7bf07a9f5212b/analysis/ajt5_overnight_2026_11_26/WHOLE_REPAIR_LINE_DENSITY_BOUND.md)

Cancellation takes at most one intercept \(s\). It requires both terminal axes to read the digit and \(\xi=\zeta^\mu\), with \(m=\mu\). With \(f_b=(b^{r-1}-1)/r\bmod r\), the source equation forces \(3^c/5^d=-\mu f_5/f_3\bmod r\). At \(q\), cancellation requires \(3^c/5^d\) to be a nonsquare, since the moving characters have odd order and \(-1\) is a nonsquare. Thus the same two parity gates as in the depth-one calculation apply. For terminal Legendre bits \(u\), let \(\eta_r(u)\) be the maximum head mass satisfying both gates over the two possible source ratio signs. The two reduced classes modulo \(60\) for each \(u\) give the reciprocal charge
\[
A_D=\min\!\left(R_D\max_u\eta_r(u),\
                2R_{60D}\sum_u\eta_r(u)\right).
\]
Here \(R_{60D}\) bounds a single reduced progression. The replacement outside the already charged \(G_r(S)\) is the upward-rounded minimum of \(R_D/r^2\) and
\[
R_D\left(\frac{(rS)^r}{r!}+\frac{\gamma}{r^2}\right)
 +(1-\gamma)\frac{A_D}{r^3}.
\]
The last denominator counts the exceptional source reading and the single cancelling lift. [Parity gates and progression envelopes](https://github.com/Samsen879/a303656/blob/debfafbeee90f7b79045a21085a60d5e327e3103/analysis/ajt5_overnight_2026_11_26/PARITY_FILTERED_INTERCEPT_DENSITY_BOUND.md)

**Real control.** At \(r=71,\ q=715823=2r^3+1\), the actual orders are \(r^3\) and \(2r^3\). The replay checks two integers with the same lower source reading and legal small-head readings. All 71 repaired points have exact source valuation four. One intercept gives terminal shift set \(\{0\}\), and the next gives 71 distinct terminal shifts. This is an ordinary-terminal control below \(B\). Both modulo-\(q^2\) Wieferich tests fail.

### Inline rational replay

The replay replaces only the eight existing finite cube rows. It reconstructs the exact reconciled predecessor, including the three tails, and checks the ordinary control by modular arithmetic.

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt, factorial, lcm

B, W, Z = 9*10**14, 10**11, 10**25

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, u2 = series(Q(2))

def logs(x):
    y, k = Q(x), 0
    while y >= 2:
        y /= 2
        k += 1
    a, b = series(y)
    return Q(floor(W*(a+k*l2)),W), Q(ceil(W*(b+k*u2)),W)

def hi(x):
    return logs(x)[1]

def up(x):
    return Q(ceil(W*x),W)

def prime(q):
    return q>1 and all(q%p for p in range(2,isqrt(q)+1))

def prog(D,r,m=4,scale=1):
    l,h = logs(m*D)
    u,v = Q(4*D,3),34-h
    assert u-h > v > 0
    return (1/(u-h)+hi((u-l)/v))/(scale*(D-D//r))

parities = ((0,0),(0,1),(1,0),(1,1))

def head_parity(n3,n32):
    table = ("XY000Y00","XZZXZZXX","YY000Y00")
    key = "Z" if (n3,n32) in ((1,0),(0,1)) else table[n3][n32%8]
    return parities["0XYZ".index(key)]

counts = tuple(sum(head_parity(t,u)==v for t in range(3) for u in range(32))
               for v in parities)
assert counts == (40,19,19,18)

def masses(r):
    x,y = [pow(b,(r-1)//2,r)==r-1 for b in (3,5)]
    return [Q(max(sum(w for (a,b),w in zip(parities,counts)
                      if (a*s+b*t)%2 and (a*x+b*y)%2==i)
                  for i in (0,1)),96)
            for s,t in parities]

roots = (31,43,47,59,67,71,79,83)
assert roots == tuple(r for r in range(31,101,4) if prime(r))
old = new = Q(0)
rows = []
for r in roots:
    assert all(pow(b,r-1,r*r)!=1 for b in (3,5))
    D = r**3
    S = (hi(D)+Q(1,2))/(D-D//r)
    R = min(S,prog(D,r))
    K = (1+isqrt(4*r-3))//2
    gamma = min(Q(1),r*S/(r-K))
    weights = masses(r)
    A = min(R*max(weights),2*prog(D,r,60,8)*sum(weights))
    extra = (r*S)**r/factorial(r)
    a = up(R/r**2)
    b = up(min(R/r**2,R*(extra+gamma/r**2)+(1-gamma)*A/r**3))
    old += a
    new += b
    rows.append((r,int(a*W),int(b*W)))
assert rows[0] == (31,27014,186)
assert (old,new) == (Q(40141,W),Q(248,W))

def exp_lo(x,n):
    v = t = Q(1)
    for j in range(1,n):
        t *= x/j
        v += t
    return v

u = logs(B)[0]+48*l2

def geom(z):
    return 1/(exp_lo(z*u,100)*(1-1/exp_lo(z*l2,12)))

root = Q(isqrt(floor(hi(3)*Z*Z/(4*u)))+1,Z)
low_tail = 70*(root*geom(Q(271,750))+geom(Q(323,375)))
prime_tail, power_tail = Q(1633,W), Q(7320,W)
predecessor = (Q(125047,W)+Q(14,2**27)+prime_tail+power_tail
               +Q(891331308302981248,Z)+low_tail)
assert Q(153391,W) < predecessor < Q(153392,W)
answer = predecessor-old+new
assert answer == predecessor-Q(39893,W)
assert answer < Q(113499,W)

r,q,c,d = 71,715823,10082,45369
L = lcm(3960,r-1)*r*r
assert prime(q) and q==2*r**3+1
assert pow(3,r**3,q)==1 and pow(3,r*r,q)!=1
assert pow(5,r**3,q)==q-1 and pow(5,2*r*r,q)!=1
assert all(pow(b,q-1,q*q)!=1 for b in (3,5))
assert [pow(b,r-1,r*r) for b in (3,5)] == [1+32*r,1+48*r]
assert pow(5,41*L,q)==pow(3,L,q)!=1

def shift(x,y,m):
    return (pow(3,c+L*x,m)+pow(5,d+L*y,m))%m

n1,n2 = 2420068764704544,5408745815534784
assert (n2-n1)%(32*3*7*11*19*23*r**3)==0
for n,s,k in ((n1,19,1),(n2,20,r)):
    assert (c%2,d%2)==head_parity(n%3,n%32)==(0,1)
    assert (n-pow(5,d,3))%3
    assert (n-shift(0,0,32))%32==18
    assert all((n-shift(0,0,p))%p==1 for p in (7,11,19,23))
    assert (n-shift(0,0,r**3))%r**3==0
    vals = set()
    for x in range(r):
        y = (s+41*x)%r
        assert (n-shift(x,y,r**4))%r**4==0
        if (n-shift(x,y,r**5))%r**5==0:
            y += r
        assert (n-shift(x,y,r**5))%r**5 in range(r**4,r**5,r**4)
        vals.add(shift(x,y,q))
    assert len(vals)==k
    if k==1:
        assert vals=={0}

print("r, old and new charges in units of 1/W",rows)
print("percent before and after",float(100*predecessor),float(100*answer))
```

For the exceptional-reading charge, an empty surviving menu before the source test cannot give a first terminal blocker. On a nonempty menu any reading outside the menu has a robust survivor by definition of case 3. Each repaired phase in the line is chosen without reading any dropped reader or the terminal observation. Conditional on the source reading and fixed retained phase, the expected-loss upper bound is therefore valid even when a dropped reader sees the new fourth digit. The replay evaluates the small ordinary control and the eight exact replacement charges, not the inherited large prime search. The pointwise conjecture and density one remain open.
