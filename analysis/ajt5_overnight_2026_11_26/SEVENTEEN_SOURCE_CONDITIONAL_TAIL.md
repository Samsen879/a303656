# Conditional tail for unrestricted first blockers after sixteen common sources

**The 17-seed theorem gives a conditional cutoff for the unrestricted growing box.** If at most 16 inert primes Wieferich to both bases lie through \(X\), every first blocker of the full box lies above \(X\). An explicit bound for that remaining mass is \(O(1/\log X)\). The pinned unconditional bound stays **\(0.0000909120846076457\ldots\%\)**, with its cutoff and all three tails intact. [Seventeen-source theorem](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/RANK_SEVEN_SIXTEEN_SOURCE_ESCAPE.md) · [Pinned density ledger](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/DISTINCT_FACTORIAL_ALLOWANCE_REPLACEMENT.md)

### Where the seed threshold applies

The transfer uses the theorem’s **positive-\(c\), fixed-\(d\)-parity muted slice**. On a finite prefix, use its reservations to mute the indicated rows and its ordinary base-3 corrections at singly exceptional base-5 primes. Choose the \(d\)-parity giving a unit at \(3\). That unit condition survives as \(c\) grows. After the odd-row work, higher binary digits of \(d\) can satisfy the \(2\)-adic norm condition because odd inert row periods read at most the parity of \(d\). All these tests are finite, so the final exponent classes admit arbitrarily large representatives on both axes. On the resulting slice each common exceptional prime can supply at most one rigid seed, and the rank theorem leaves a survivor with at most 16 seeds. [Exact modulus bridge](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md) · [Simultaneous muting](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/LOW_ORDER_HELPER_MUTING.md)

Thus the first 16 common primes are excluded as first blockers of the **unrestricted** box. The muted slice can choose a different head from the one preselected in the numerical ledger, so this rank exclusion does not justify deleting those terms from that ledger. Rigid seeds also need no factor \(1/q\) apiece. That factor comes from bounding the final test at a first blocker after the earlier observations. The conditional estimate below averages over \(n\) under an arithmetic hypothesis about primes through \(X\). It is not a uniform estimate after fixing an arbitrary observed prefix. [Full-box first-blocker criterion](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

### An explicit conditional tail

Take \(X\ge B=9\cdot10^{14}\), \(m=\lfloor(4/5)\log X\rfloor\ge10^6\), and \(L=\log(4m)+1/2\). Under the at-most-16 hypothesis, the box miss density is at most
\[
\frac{\log3}{2\log X}\,
 \frac{X^{-21/125}}{1-2^{-21/125}}
 +\frac7m+\frac9{m^2}
 +\frac{9L}{m^{3/2}}+\frac{72L}{m^{7/6}} .
\]
The same bound holds for the all-exponent exception density.

- **Low order.** In a dyadic interval \([Y,2Y)\) starting at \(X\), let \(T=\lfloor(4/5)\log Y\rfloor\). If both orders divide \(\operatorname{lcm}(1,\ldots,T)\), a common Wieferich terminal has its square dividing \(3^{\operatorname{lcm}(1,\ldots,T)}-1\). Counting squared prime divisors and using \(\operatorname{lcm}(1,\ldots,T)\le Y^{104/125}\) gives the first term.
- **Higher order.** A selected order prime power \(D=r^a\) satisfies \(D>m\). The one-axis reset works on the unrestricted panel. Freeze the retained observations, drop the readers of the released digit, and use the source-depth gate \(r^{-\lceil a/2\rceil}\) at an inert source. For \(r=3\) the grown base-3 contribution at the source is zero. If base \(5\) is moved, its ordinary lift at \(3\) supplies the source test. Split sources have no depth charge. The reader charge is bounded by \(rS_D^{r-1}\), with \(R_D\le S_D\le\frac32(\log D+1/2)/D\). [One-axis reset and reciprocal envelopes](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_EXPLICIT_DENSITY_BOUND.md)
- **Prime, square, and higher-power sums.** At prime \(D\), the depth cost is at most \(1/D\) on inert sources and the reader cost is at most \(D^{-2}\). Dyadic Brun–Titchmarsh with moduli \(4\) and \(1\), respectively, gives \(7/m+9/m^2\). At \(D=r^2\), an ordinary moved base has even depth and costs at most \(2S_D/\sqrt D\le1/D\). A nonordinary moved base has depth at least three and also costs at most \(1/D\). On all powers, the reader cost is at most \(3S_D^2\le1/D\). Counting squares by \(\sqrt{2Y}\) gives \(9L/m^{3/2}\). Counting powers of exponent at least three by \(9(2Y)^{1/3}\) gives \(72L/m^{7/6}\). The latter count follows by separating cubes and using \(\log_2 x<8x^{1/12}\) for the remaining exponents. [Even-depth repair](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md) · [Brun–Titchmarsh bound](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED)

For example, **if** the count is at most 16 through \(X=B2^{2^{30}}\), the replay gives a conditional bound below \(0.0000104\%\). The computation evaluates the envelope and supplies no prime-count certification through that \(X\).

### The \(20771\) source and a real control

The lifting depths at \(r=20771\) are \((1,2)\). In its \(D=r\) class, any genuine terminal whose base-5 order reads \(r\) can use the even-depth axis at the source. Its depth charge then falls from \(1/r\) to at most \(G_{r-1}(S_D)/r\), where \(G_{r-1}\) is the inherited reader-cover bound. The residual \(1/r\) charge is needed in this argument only for terminals whose base-3 order reads \(r\) and whose base-5 order does not. I have no certified reciprocal-mass split between those two terminal types, so the unconditional \(20771\) charge stays in the ledger. [Even-depth source formula](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

For the represented integer \(n=840955481\), freeze \(c=1\) and take \(d=62310y\). Every \(y\) gives valuation one at \(20771\). After the ordinary base-3 lift \(c=14781263025780811\), exactly \(20770\) of the \(20771\) first digits \(y\) give valuation two. This is a real frozen-slice obstruction and an escape through the ordinary axis at the same source. The source is exceptional to base \(5\) alone. [Same-target lift](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md)

### Inline replay

The script uses exact fractions for the conditional envelope, reconstructs the unchanged unconditional ledger including all three tails, and checks the source control.

```python
from fractions import Fraction as Q
from math import floor, ceil, isqrt, lcm

B, W = 9*10**14, 10**11

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, u2 = series(Q(2))

def logs(x):
    y, k = Q(x), 0
    assert y >= 1
    while y >= 2:
        y /= 2
        k += 1
    l, h = series(y)
    return Q(floor(W*(l+k*l2)),W), Q(ceil(W*(h+k*u2)),W)

def hi(x):
    return logs(x)[1]

def exp_lo(x,n):
    s = t = Q(1)
    for j in range(1,n):
        t *= x/j
        s += t
    return s

def iroot(n,a):
    l, h = 0, 1 << ((n.bit_length()+a-1)//a)
    while h-l > 1:
        m = (l+h)//2
        if m**a <= n:
            l = m
        else:
            h = m
    return l

def conditional(j):
    # X = B*2**j, with the prime-count hypothesis supplied externally.
    u = logs(B)[0]+j*l2
    m = floor(Q(4,5)*u)
    assert m >= 10**6
    h = hi(m)+Q(1,2)
    assert Q(27,4)*h*h < m and 3*h < isqrt(m)
    assert 29**3 < 2**28
    assert logs(Q(m,2))[0] > 6*(hi(4)+Q(1,2))
    assert logs(2*m)[0] > 4

    delta = Q(21,125)
    low = hi(3)/(2*u*exp_lo(delta*u,100)*(1-1/exp_lo(delta*l2,12)))
    L = hi(4*m)+Q(1,2)
    prime = Q(7,m)+Q(9,m*m)
    square = 9*L/(m*isqrt(m))
    higher = 72*L/(m*iroot(m,6))
    return m, low+prime+square+higher

def pinned():
    x = Q(1,10)
    cover = x**53*(3*(53/(1-x)+x/(1-x)**2)+x/(1-x))
    for r in (29,31,37,41,43,47):
        D = r
        ordinary = all(pow(b,r-1,r*r)!=1 for b in (3,5))
        while D <= 10**6:
            phi = D-D//r
            s = (hi(D)+Q(1,2))/phi
            l,h = logs(4*D)
            U = Q(4*D,3)-h
            R = min(s,(1/U+hi((Q(4*D,3)-l)/(34-h)))/phi)
            extra = s**r if D==r and r%4==3 and ordinary else 0
            cover += R*(r*s**(r-1)+extra)
            D *= r
    assert cover < Q(1564,10**28)

    Z = 10**25
    u = logs(B)[0]+48*l2

    def geom(d):
        return 1/(exp_lo(d*u,100)*(1-1/exp_lo(d*l2,12)))

    root = Q(isqrt(floor(hi(3)*Z*Z/(4*u)))+1,Z)
    low_tail = 70*(root*geom(Q(271,750))+geom(Q(323,375)))
    prime_tail, power_tail = Q(1633,W), Q(7320,W)
    return (Q(72998,W)+cover+Q(891331308302981248,Z)
            +low_tail+prime_tail+power_tail)

predecessor = pinned()
assert Q(90912,W) < predecessor < Q(90913,W)
m, bound = conditional(2**30)
assert m==595408921 and bound<Q(104,10**9)<predecessor
print("unchanged unconditional percent",float(100*predecessor))
print("conditional percent",float(100*bound))

r,p,n = 20771,40487,840955481
assert n==3+5**4+13038**2+25903**2
assert all(q%4==3 and all(q%d for d in range(2,isqrt(q)+1))
           for q in (r,p))
assert [pow(b,r-1,r*r) for b in (3,5)] == [347394976,1]
assert pow(5,r-1,r**3) == 207519966122
assert (n-3-1)%r**3 == (n-3-1)%p**3 == r*p

C1,C2 = 14781263025780811,17620428032262670841383591
for c,u,v in ((C1,r*r,6138091353325),(C2,r*r,p*p)):
    assert c%30==1 and (n-pow(3,c,31))%31==2
    assert ((n-pow(3,c,r**3)-1)%r**3,
            (n-pow(3,c,p**3)-1)%p**3) == (u,v)

L = lcm(30,r-1)
assert L%r and pow(5,L,r*r)==1
step = (pow(5,L,r**3)-1)//r**2
assert step%r
bad = pow(step,-1,r)
assert bad==12667
for y in (0,1,bad,(bad+1)%r):
    assert (n-3-pow(5,L*y,r*r))%(r*r) == r*(p%r)
    assert (n-pow(3,C1,r**3)-pow(5,L*y,r**3))%r**3 == r**2*((1-step*y)%r)
# The last identity for arbitrary y follows by expanding (1+r^2*step)^y.
```

The finite pass can be made at the precise modulus needed by the first-blocker theorem, with zero balls interpreted by that theorem's positive local sub-ball. This supplies a cutoff only conditionally on the count through X and only for the unrestricted growing box. The vast illustrative X is not a proved or computed catalogue extension. The unconditional density ledger and all its listed charges remain unchanged.
