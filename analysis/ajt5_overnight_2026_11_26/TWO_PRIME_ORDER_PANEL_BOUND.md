# Two growing prime factors in the order panel: the genuinely joint diagonal remains

Stay with the same target n and the two-dimensional anchor square from the [one-factor repair](https://github.com/Samsen879/a303656/commit/e6ae0098912f9a932542bbcbfae1e24e27d420eb). The initial 6×2 search avoids all four fixed inert periods dividing 720. The expanded steps are 720 on both axes, and J=floor(H/12000) fits the ordinary exponent box at bit height H. If an old factor 17 is peeled, at most one class v mod 17 per row is lost.

For distinct primes r,s>5 consider only primes with lcm(ord_p 27,ord_p 5)|720rs. Put a=gcd(ord_p 27,rs), b=gcd(ord_p 5,rs). The expanded 720-step orders are divisible by a and b respectively; the 3-axis can retain an extra factor 3, which only strengthens the counting upper bound. For (a,b)≠(1,1), group by (a,b). If L=lcm(a,b) and M=max(a,b), all actual primes of the group divide gcd(27^(720a)−1,5^(720b)−1) and have p≥2L+1. For K primes in the group, the chart fraction they can mark is at most K(1/M+1/J), using the longer of the two order axes at fixed other coordinate. This bounds every congruence hit and a fortiori every exact-one hit, regardless of whether p|n.

In each group except (rs,rs), the crossing gcd log is at most O(min(a,b)), at most O(max(r,s)). Their total marked fraction is O((1+max(r,s)/H)/log(min(r,s))). In particular comparable r,s≈H^(3/4) give o(1) for all off-diagonal sectors, even though rs greatly exceeds H. The remaining (rs,rs) sector is not controlled by this conclusion. Any selected low-cost panel of these order types still has total fraction o(1) if its CRT log cost is o(H log(min(r,s))): the main K/M terms sum to O(1/log(min(r,s))), and the 1/J terms are charged to the distinct-prime cost.

For the complete actual panel, the elementary gcd size resolves the diagonal when rs=o(H log H). At rs=O(H log H) the [Bugeaud–Corvaja–Zannier theorem](https://doi.org/10.1007/s00209-002-0449-z) gives log gcd(27^(720rs)−1,5^(720rs)−1)=o(rs), since 27 and 5 are fixed and multiplicatively independent. The old 17 gate plus the complete such panel in that range thus leave at least 16/17−o(1) of the square. This is not a claim about broad unbounded order diversity or about all labels.

Exact r=23,s=37 control, on two matched 320,000-bit targets: the newly present inert primes 5107 and 15319 correspond to (23,37) and (851,37). On one actual n both hit precisely at valuation one on (49763,16705), but (49763,17425) has a true norm, and the matched other target has a true norm already at the original label. The 23×23 previous survivors count 484 in both; the new panel reduces one target to 483 rather than charging the same removed cell twice.

~~~python
from itertools import product
from math import gcd, isqrt, prod

def panel(m):
    g = gcd(27**(720*m)-1, 5**(720*m)-1)
    out, p = set(), 2
    while p*p <= g:
        if g % p == 0:
            if p > 5 and p % 4 == 3:
                out.add(p)
            while g % p == 0:
                g //= p
        p += 1
    if g > 5 and g % 4 == 3:
        out.add(g)
    return out

def order(a, p):
    return next(e for e in range(1, p) if pow(a, e, p) == 1)

P = panel(23) | panel(37)
Q = panel(23*37) - P
assert panel(1) == {7,11,19,31}
assert P == {7,11,19,31,47,139,223,691,3331,6211}
assert Q == {5107,15319}
assert [(order(3**80,p), order(5**144,p))
        for p in (7,11,19,31)] == [(3,1),(1,5),(9,1),(3,1)]
assert pow(5,720,289) == 1+13*17

H,t,J = 320000,16561,23
assert t % 720 == 1 and all(t % d for d in range(2,isqrt(t)+1))
assert 16*t <= H <= 24*t and 720*J+400 <= H//16

def S(i,k,m=None):
    return pow(3,3*t+80*i,m) + pow(5,t+144*k,m)

def target(k,M,x0,y0):
    z = 1 << (H//2-4)
    x,y = z+(x0-z)%M, z+(y0-z)%M
    s = S(1,k)
    n = s + 85*(x*x+y*y)
    assert n.bit_length() == H
    assert n-s == (7*x-6*y)**2 + (6*x+7*y)**2 > 0
    return n

a = target(1,9388084832334607023240,4381315991659259056097,
           6501706549976544723040)
b = target(6,
    757649713650405461537536065948325432665227896039952315487463013691482294534132736960,
    223218134195205809912026156790579905206856110098441348411308257817375244489054788697,
    720149665922715543630524749133335072257777932333533269670183034263944727438995332440)
assert (b-a) % (25*1728*289*prod(p**3 for p in P)) == 0
assert (a%8,a%3,a%25,a%17) == (5,1,17,15)
for n in (a,b):
    assert next(i for i in range(6)
                if all((n-S(i,0,p))%p for p in (7,19,31))) == 1
    assert next(k for k in range(2) if (n-S(0,k,11))%11) == 1
    for k in (1,6):
        R = n-S(1,k)
        assert R > 0 and (R%8,R%3,R%25) == (5,2,15)
        assert R%17 == 0 and R%289 != 0

for p,A,B,U,V in [(5107,46,222,23,37),(15319,5106,333,851,37)]:
    assert (order(27,p),order(5,p),order(3**720,p),order(5**720,p)) == (A,B,U,V)
    assert (b-S(1,1,p*p)) % (p*p) == p and b%p != 0
    ys = {pow(5,t+144+720*v,p) for v in range(V)}
    assert sum((b-pow(3,3*t+80+720*u,p))%p in ys for u in range(U)) == 1

def clean(n,F):
    return {(u,v) for u,v in product(range(J),repeat=2)
            if all((n-S(1+9*u,1+5*v,p))%p for p in F)
            and (n-S(1+9*u,1+5*v,289))%289}

A,B = clean(a,P|Q),clean(b,P|Q)
assert clean(a,P) == clean(b,P) == A
assert (len(A),len(B)) == (484,483) and min(A) == (0,0) and min(B) == (0,1)
assert B == A-{(0,0)}
print(sorted(Q),len(A),len(B))
~~~
