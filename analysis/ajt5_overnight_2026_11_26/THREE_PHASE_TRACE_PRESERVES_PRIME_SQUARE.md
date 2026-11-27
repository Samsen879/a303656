# Three-phase trace selection preserves an actual prime square

In the quadratic norm-one algebra with θ²=−3 and ξ=(−1+θ)/2, the product of the three trace terms (Tr(W ξ^j)+1) for j=0,1,2 is Tr(W³)−2. One can check the identity by writing the terms as Wξ^j+W^(-1)ξ^(-j)+1 and multiplying. Thus the full product detects its ordinary support, while testing the individual factors can separate supported blocks; the blocks need not be disjoint.

On the true (231,13) negative half the three individual trace gcds are exactly (13729·121,86083·13729,86083·121), computed from the fixed LCM exponent and modular seed in the replay. The actual coordinate gcd recovers the full square 121, not just its radical. On the separately vetoed true (231,295) positive half, the three phase gcds are pq,q,p for the two known inert blocks. This latter exponent is chosen from already discovered factors and is not a generic factor-discovery algorithm. None of these data classifies the remaining unresolved (231,13) or (231,31) halves.

```python
from math import gcd, lcm

A = 5**231
M = lcm(*range(1, 50001))

def check(v, sign, N, E, expected):
    c = pow(v, -1, 231)
    g = pow(5, c, N)*pow(-3*sign, (1-v*c)//231, N)%N
    u = pow(g*g+3, -1, N)
    z = ((g*g-3)*u%N, 2*g*u%N)
    def mul(x, y):
        a,b = x
        c,d = y
        return (a*c-3*b*d)%N, (a*d+b*c)%N
    w = (1,0)
    for bit in bin(E)[2:]:
        w = mul(w,w)
        if bit == "1":
            w = mul(w,z)
    a,b = w
    assert tuple(gcd(N,t) for t in (2*a+1,1-a-3*b,1-a+3*b)) == expected
    return gcd(N,2*a+1,2*b+1)

H = (A-3**13)//2
assert check(13,-1,H,M//3**9,(13729*121,86083*13729,86083*121)) == 121
p,q = 72197823963870893,778603984326529553
J = (A+3**295)//8
assert check(295,1,J,lcm((p+1)//3,(q+1)//3),(p*q,q,p)) == p
```
