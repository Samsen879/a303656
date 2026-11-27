# A divisibility test for repeated short CRT representatives

Suppose gcd(Q,15)=1 and 3^c+5^d=n modulo Q at four corners z,z+w1,z+w2,z+w1+w2, with both coordinates of each increment nonzero. This includes a three-term progression if the increments coincide. Write A=3^c,B=5^d, and X_i=3^u_i−1, Y_i=5^v_i−1 in the unit ring, using inverses for negative exponents. Fixed-value edge equations give A X_i+B Y_i=0. The mixed difference gives A X1 X2+B Y1 Y2=0; substitution and cancellation of units give n X1 X2=0 modulo Q. At each prime power dividing Q, X_i and Y_i have equal truncated valuations, by the edge equations. Thus Q/gcd(Q,n) divides G1 G2, where G_i=gcd(3^|u_i|−1,5^|v_i|−1).

If all exponents are O(log X), [Corvaja–Zannier](https://arxiv.org/pdf/math/0311030) gives each G_i=X^o(1), so no such parallelogram is possible when Q/gcd(Q,n)>=X^delta for a fixed delta>0 and X sufficiently large. On a fixed mixed affine row of length L in that situation, positive gaps between hits are distinct, so h hits imply binomial(h,2)<=L−1. The global periods need not be small for this repeated-hit obstruction.

A single short pair for a supplied Q can be tested without traversing its periods. When both powers are at most n/4, the quotient k=(n−3^c−5^d)/Q lies between ceil(n/(2Q)) and floor((n−2)/Q). For each such k, the larger summand is the largest power of its own base not exceeding n−kQ. Trying each choice of larger base and checking the remaining exact power gives O(1+n/Q) quotient candidates. This does not select a suitable Q for arbitrary n.

The replay checks real positive and negative controls for Q=8177, short repeated hits with n divisible by Q, and a unit-target prime-power control where Q divides G² but not G. No new global density or prescribed-target result follows.

```python
from math import gcd

def power(t,b):
    k,v = 0,1
    while b*v <= t:
        k,v = k+1,b*v
    return k,v

def small_hits(n,Q):
    out = set()
    for h in range((n+2*Q-1)//(2*Q),(n-2)//Q+1):
        f = n-h*Q
        for a,b in ((3,5),(5,3)):
            j,x = power(f,a)
            if x >= f:
                continue
            k,y = power(f-x,b)
            if x+y == f and 4*max(x,y) <= n:
                out.add((j,k) if a==3 else (k,j))
    return out

Q = 13*17*37
assert [next(k for k in range(1,145) if pow(g,k,Q)==1)
        for g in (3,5)] == [144,144]
assert small_hits(499449,Q) == {(3,4)}
assert 499449-3**3-5**4 == 61*Q == 19**2+706**2
assert small_hits(504753,Q) == set()
assert (504753-3**3-pow(5,68,Q))%Q == 0

lo = Q**6
assert 4*5**30 <= lo and 2*lo < 4*3**144
assert all((pow(3,j,Q)+pow(5,j,Q))%Q==0 for j in (6,18,30))

n,q = 976564617,169
G = gcd(3**6-1,5**4-1)
assert gcd(n,q)==1 and G==104 and G%q and G**2%q==0
for j in range(3):
    x,y = 3**(3+6*j),5**(4+4*j)
    assert 4*max(x,y)<=n and (n-x-y)%q==0
print("Quotient recovery and parallelogram boundary controls verified")

assert gcd(3**6-1,q)==gcd(5**4-1,q)==13
x,y=pow(3,6,q),pow(5,4,q)
assert (x-1)%q and (y-1)%q
assert gcd((x-1)*(y-1),q)==q
print("Prime-power boundary independently checked")
```
