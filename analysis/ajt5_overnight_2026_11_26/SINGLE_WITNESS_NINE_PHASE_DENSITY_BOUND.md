# Nine phase variants give representation density above 99.8889%

The natural density of exceptions in [the original all-exponent problem](EXACT_DENSITY_ALL_EXPONENTS.md) is less than \(0.001111\). This is an upper bound on the larger miss density of the two-growth-axis box as well. The exact rational endpoint below is \(0.00111020555\), still not density one. The input is the [preceding explicit bound](SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md), including its full tails, published base-3 search, and small-head phase modulo \(3960\). This note replaces only certain finite terms; it does not discard the tails.

## A finer count of early losses

With a one-digit reset of \(r\) distinct phases modulo the terminal, the earlier rows must kill at least \(r-1\) to permit first blocking. Take the union over the \(r\) possible subsets of size \(r-1\). For each specified phase to be killed by a different row, the probability for a particular allocation is a product of \(1/(p+1)\), since the phase choices were made before reading the dependent rows. Summing over allocations, then relaxing to all choices, gives \(\min(G_r(S),rS^{r-1})\) as a replacement for the old \(G_r(S)\).

For \(D=3^a\ge81\), move the chosen axis by \(3^{a-2}\) times each digit \(0,\dots,8\). This keeps the previously fixed phase modulo \(3960\), including a unit at 3. There are nine distinct terminal shifts. A dependent old prime reading exactly \(a-1\) digits can kill a group of three variants with the same new lowest digit. A prime reading \(a\) digits or more can kill one specific variant. Let their respective reciprocal weight sums be \(S_L,S_H\). With \(\ell\) groups killed completely by lower-read rows, the high-read rows need to kill at least \(8-3\ell\) remaining variants (zero if \(\ell=3\)). By specifying groups and variants and summing independent row assignments, the total bound is
\[
 S_L^3+9S_L^2 S_H^2+18S_L S_H^5+9S_H^8.
\]
The coefficients count \(3\binom32,\ 3\binom65,\ \binom98\) for \(\ell=2,1,0\), respectively. The two groups of old rows are disjoint; no independence of variants is used. The old explicit Brun–Titchmarsh reciprocal envelopes imply \(S_H\le S_D,\ S_L+S_H\le3S_D\), using \(\varphi(D/3)=\varphi(D)/3\) for the envelope of the combined rows. For \(S_D\le1/10\) the display is at most \(27S_D^3\): divide by \(S_D^3\), put \(x=S_H/S_D\), and bound the first term by \((3-x)^3\); its deficit from 27 is at least \(19x\), greater than the other three terms combined. Multiply by the same \(1/q\) bound for the terminal reading.

For the finite term \(D=81\), keep \(S(q)\le(\log\log q+1/5)/54\) inside the sum. The terminal interval is \(B<q\le e^{108}\), in the unique class \(1\bmod81,3\bmod4\). Apply the [Montgomery–Vaughan bound](https://doi.org/10.1112/S0025579300004708) and partial summation with decreasing weight \((\log\log q+1/5)^3/q\). Its negative derivative is at most \((\log\log q+1/5)^3/q^2\). Discard the nonpositive lower boundary, use \(\log B>34\), and substitute \(t=\log q\) to get the finite upper bound
\[
 \frac{27}{54^4}\left[
  \frac{(\log108+1/5)^3}{108-\log324}
  +\int_{34}^{108}\frac{(\log t+1/5)^3}{t-\log324}\,dt
 \right].
\]
The replay uses an upper numerator on each unit interval and integrates the denominator exactly with upper-rounded logarithms. In the finite range for primes \(r\le23\) the preloaded \(r\)-condition never incurs a depth charge, so the old finite terms can be replaced directly. The rational subtraction compares the old and new terms on the same upward grid while retaining the strict full-tail baseline \(0.00175\).

## A separate deeper repair control

For a chosen \(r\)-primary reset on axis \(b\) with terminal order depth \(A\), its local shift depth at \(r\) is \(d=v_r(b^{r-1}-1)+A-1\). To cancel at that depth a second unit axis needs digit \(j=d-v_r(c^{r-1}-1)\), which must be nonnegative and free in the preloaded phase. With odd \(d\) and a match through depth \(d\), choose it to cancel at depth \(d+1\), then use the next digit to make valuation exactly \(d+1\). If the terminal depth on \(c\) is \(C\le j\), both changes are invisible; if \(C=j+1\), the last is invisible but a cancelling character intercept can occur; if \(C>j+1\), the last digit can itself supply distinct terminal values. These cases require accounting for all old readers of the moved digits. The replay shows the invisible case at \(9923\) and the impossibility of an invisible repair at \(2663\) for a particular source state. They are ordinary targets for the local controls, and no deeper compensation bound is needed in the numerical subtraction above.

~~~python
from fractions import Fraction as Q
from math import ceil, factorial, floor, isqrt

W = 10**11

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

L2, U2 = series(Q(2))

def logs(x):
    y, k = Q(x), 0
    assert y >= 1
    while y >= 2:
        y /= 2
        k += 1
    l, u = series(y)
    return Q(floor(W*(l+k*L2)),W), Q(ceil(W*(u+k*U2)),W)

def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)

gain = Q(0)
for r in (3,5,7,11,13,17,19,23):
    D = r*r
    while D <= 10**6:
        if D >= 28:
            phi = D-D//r
            l,u = logs(4*D)
            Um,Up,Vm = Q(4*D,3)-u,Q(4*D,3)-l,34-u
            assert 0 < Vm < Um
            S = (hi(D)+Q(1,2))/phi
            R = min(S,(1/Um+hi(Up/Vm))/phi)
            G = min(Q(1),Q(r,r-1)*S,(r*S)**(r-1)/factorial(r-1))
            new = R*min(G,r*S**(r-1))
            if r == 3:
                assert S <= Q(1,10)
                new = min(new,R*27*S**3)
            if D == 81:
                integral = sum((hi(t+1)+Q(1,5))**3
                               * hi((t+1-l)/(t-u))
                               for t in range(34,108))
                weighted = Q(27,54**4)*(
                    (hi(108)+Q(1,5))**3/Um + integral)
                new = min(new,weighted)
            gain += up(R*G)-up(new)
        D *= r

upper = Q(175,10**5)-gain
assert upper < Q(1111,10**6)
print("saved",float(gain),"full-tail upper",float(upper))

r,H = 11,3960

def v(n):
    j = 0
    while n%r == 0:
        j += 1
        n //= r
    return j

def order(b,q):
    t,k = b%q,1
    while t != 1:
        t = t*b%q
        k += 1
    return k

for q,b,c,A,C,L,n in ((9923,3,5,2,1,14760,2927233575),
                        (2663,5,3,3,3,360,826324611)):
    assert all(q%i for i in range(2,isqrt(q)+1))
    assert (v(order(b,q)),v(order(c,q))) == (A,C)
    e,f = v(b**10-1),v(c**10-1)
    d,j = e+A-1,e+A-1-f
    assert d == 3 and L*r**j%H == L*r**(A-1)%H == 0
    S = lambda u,w,m: (pow(b,H+L*u,m)+pow(c,H+L*w,m))%m
    assert n%4 == 3
    assert all(n%p==0 and S(0,0,p)!=0 for p in (3,7,19,23))
    residues = set()
    for t in range(r):
        x = r**(A-1)*t
        s, = [s for s in range(r) if (n-S(x,r**j*s,r**4))%r**4==0]
        z = next(z for z in (0,1)
                 if (n-S(x,r**j*(s+r*z),r**5))%r**5)
        assert (n-S(x,r**j*(s+r*z),r**5))%r**5 in range(r**4,r**5,r**4)
        residues.add(S(x,r**j*(s+r*z),q))
    if q == 9923:
        assert (e,f,j)==(2,1,2) and pow(c,L*r**j,q)==1
        assert len(residues)==r
    else:
        assert (e,f,j)==(1,2,1) and pow(c,L*r**(j+1),q)!=1
        assert (n-S(0,0,r**5))%r**5==r**3
        assert pow(c,L*r**C,r**5)==1

~~~
