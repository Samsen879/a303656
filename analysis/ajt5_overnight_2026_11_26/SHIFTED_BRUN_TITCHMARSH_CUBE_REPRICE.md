# Shifted Brun–Titchmarsh repricing of the finite cube rows

The finite cube subtotal decreases from 248 to 245 units of 10^(-11) in density units. Combined with DISTINCT_FACTORIAL_ALLOWANCE_REPLACEMENT.md, this gives natural exception density below **0.000090909085%**. The source cutoff and all three infinite tails are unchanged. This is a density bound, not pointwise representation or density one.

The verified case-three gate is at most the original gate times w(q)=min(1,p²(q-B+4)/(4B)) for source p and cutoff B. Put X=B+4B/p²−4. Then w(q)/q<=min(1/X,1/q): below X the left side increases to 1/X, and above X both sides equal 1/q. For a reduced progression modulo M let N(t) count eligible progression primes between B and t. With the unchanged upper endpoint Y=exp(4p³/3), partial summation gives the reciprocal envelope N(Y)/Y+integral_X^Y N(t)/t² dt for the capped weight.

On each subinterval [u,v] up to 128B bound N(t) by 2(t−B)/(phi(M) log((u−B)/M)), by [Montgomery–Vaughan, Theorem 2](https://doi.org/10.1112/S0025579300004708). The integral numerator is log(v/u)+B/v−B/u. Before B+delta, when needed, use the monotone upper count at B+delta. Above 128B use the old envelope based on 2t/(phi(M) log(t/M)), retaining the positive endpoint term N(Y)/Y. This does not subtract an unknown or presumed prime count below B. In the two progressions M=4p³ and 60p³, phi(M)/2 equals phi(p³) and 8phi(p³), respectively.

Only the case-three envelope is replaced; the original factorial branch, parity weights, fallback bound, and upward rounding are retained. The interval estimate by itself changes 31³ from 186 to 184 and 47³ from 18 to 17. The other six rows total 44, unchanged. Using the capped gate with the interval estimate further lowers the unrounded envelopes but does not save an extra rounded unit. Using the capped gate with the old interval-unshifted envelope alone changes no rounded row.

```python
from fractions import Fraction as Q
from math import ceil, floor, factorial, isqrt

B, W, Z = 9*10**14, 10**11, 10**25

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
    a, b = series(y)
    return Q(floor(W*(a+k*l2)), W), Q(ceil(W*(b+k*u2)), W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]

def env(p, D, m, scale, lower_log):
    l, h = logs(m*D)
    u = Q(4*D, 3)
    assert u-h > lower_log-h > 0
    return (1/(u-h)+hi((u-l)/(lower_log-h)))/(scale*(D-D//p))

def shifted(p, m, scale, X):
    D, end = p**3, 128*B
    delta = Q(B, 2**11)
    a = max(Q(X), B+delta)
    assert B <= X < end and delta > m*D and hi(end) < Q(4*D, 3)
    h = hi(m*D)
    # For the uncapped comparison, use monotonicity through B+delta.
    head = delta*max(0, 1/Q(X)-1/(B+delta))/(lo(delta)-h)
    points = {a, Q(end)}
    for j in range(-11, 7):
        y = B*Q(2)**j
        points.update(B+y*(1+Q(i,4)) for i in range(5)
                      if a < B+y*(1+Q(i,4)) < end)
    pts = sorted(points)
    head += sum((hi(v/u)+B/v-B/u)/(lo(u-B)-h)
                for u,v in zip(pts, pts[1:]))
    return env(p,D,m,scale,lo(end))+head/(scale*(D-D//p))

parities = ((0,0),(0,1),(1,0),(1,1))
counts = (40,19,19,18)

def masses(p):
    f,g = [pow(b,(p-1)//2,p)==p-1 for b in (3,5)]
    return [Q(max(sum(w for (a,b),w in zip(parities,counts)
                      if (a*s+b*t)%2 and (a*f+b*g)%2==j)
                  for j in (0,1)),96) for s,t in parities]

rows = []
for p in (31,43,47,59,67,71,79,83):
    D = p**3
    S = (hi(D)+Q(1,2))/(D-D//p)
    gamma = min(Q(1),p*S/(p-(1+isqrt(4*p-3))//2))
    R = min(S,env(p,D,4,1,Q(34)))
    w = masses(p)
    def units(E4,E60):
        r = min(R,E4)
        a = min(r*max(w),2*E60*sum(w))
        return W*min(R/p**2, R*(p*S)**p/factorial(p)
                     +gamma*r/p**2+(1-gamma)*a/p**3)

    X = B+Q(4*B,p*p)-4
    old = units(R,env(p,D,60,8,Q(34)))
    cap = units(env(p,D,4,1,lo(X)),env(p,D,60,8,lo(X)))
    plain = units(shifted(p,4,1,B),shifted(p,60,8,B))
    new = units(shifted(p,4,1,X),shifted(p,60,8,X))
    assert new < plain and ceil(cap)==ceil(old) and ceil(plain)==ceil(new)
    rows.append((ceil(old),ceil(new)))

assert rows == [(186,184),(29,29),(18,17),(7,7),(3,3),(3,3),(1,1),(1,1)]
old_cubes,new_cubes = map(sum,zip(*rows))
assert (old_cubes,new_cubes) == (248,245)

# Reconstruct the exact current ledger, including the factorial replacement.
factorial_charge = Q(0)
for p in (29,31,37,41,43,47):
    D = p
    while D <= (10**5 if D==p else 10**6):
        S = (hi(D)+Q(1,2))/(D-D//p)
        R = min(S,env(p,D,4,1,Q(34)))
        ordinary = all(pow(b,p-1,p*p)!=1 for b in (3,5))
        factorial_charge += R*(p*S**(p-1)
            +(S**p if D==p and p%4==3 and ordinary else 0))
        D *= p
x = Q(1,10)
factorial_charge += x**53*(3*(53/(1-x)+x/(1-x)**2)+x/(1-x))

def exp_lo(x,n):
    s = t = Q(1)
    for j in range(1,n):
        t *= x/j
        s += t
    return s

t = lo(B)+48*l2
def geom(v):
    return 1/(exp_lo(v*t,100)*(1-1/exp_lo(v*l2,12)))

root = Q(isqrt(floor(hi(3)*Z*Z/(4*t)))+1,Z)
low_tail = 70*(root*geom(Q(271,750))+geom(Q(323,375)))
tails = Q(1633,W)+Q(7320,W)+low_tail
other = (Q(40008+17949+12063+2978-old_cubes,W)
         +Q(891331308302981248,Z)+factorial_charge+tails)
current = other+Q(old_cubes,W)
revised = other+Q(new_cubes,W)

assert current-revised == Q(3,W)
assert Q(909120846076456,10**19) < 100*current < Q(909120846076458,10**19)
assert 100*revised < Q(90909085,10**12)
print(rows, "revised bound < 0.000090909085%")
```
