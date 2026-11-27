# Optimal norm composition can lose one allocation bit

This belongs to the shared-label P2 norm composition track. If an unramified rational prime splits on its own quadratic edge and is inert in the other, the corresponding relative ideal norm has even depth at its specified orientation. Thus demands 2r−1 and 2r are identical for the composing element. The allocations (2r−1,2s) and (2r,2s−1) between the short and long sides give the same admissible sets, even at optimal norm. Weighted traces depending only on the whole edge products, small-prime allocations, and selected composing elements cannot distinguish such a matched and unmatched pair.

In the integer control q=23, one edge is (433,42439). The other is either (q,81q²) or (q²,81q). Products and small-prime allocations agree, but only the first pair shares sum 42872. Let r=sqrt(−3), s=sqrt(−5), omega=(1+r)/2, and beta=(−8−s)+(1+3s)omega. The same composing elements (1+12r)beta and (28−11r)beta work for both demands; the replay checks their norms and orientations. This is not an ordinary-height actual 3,5 collision. A separate real 3,5 control gives three square labels at K=2150, and an alternative allocation with the same prime-to-30 oriented inputs fails the edge match.

The rounded norms recover exact depths except when a cross-inert prime has odd total depth and positive rounded depth on both sides. Then one binary choice remains. If at most one prime per edge is ambiguous, a positive ordinary short-factor interval of endpoint ratio less than the ambiguous prime selects at most one alternative. The intervals (4 sqrt(A), (21/2)sqrt(A)) and ((5/4)sqrt(A), (9/5)sqrt(A)) meet that condition. This is an exact test once the required factor/valuation data are supplied, not a claim of a polynomial-time factorization. Multiple ambiguous primes can have competing product ratios close to one. The edge sums must still agree and n−K must still be a square for a prescribed target. No general pointwise or density result follows.

```python
from math import gcd

# Actual P2 shifts and a true three-label height.
A, B = 3**2, 5**0
S0, S1, S2 = A+25*B, 9*A+625*B, 81*A+125*B
d, e = (S1-S0)//4, (S2-S0)//4
assert (d,e) == (4*42,5*41)
assert 4+42 == 5+41 == 46
K = S0+46**2
assert K == 2150 and (K-S0,K-S1,K-S2) == (46**2,38**2,36**2)
assert 1*205 == e
assert 204**2 < S0+206**2-S1 < 205**2

# Unramified collision with unchanged small-prime allocations.
q, v, u = 23, 433, 42439
d, e = v*u, 81*q**3
assert gcd(d,e) == 1
assert pow(-3,11,q) == q-1 and pow(-5,11,q) == 1
assert q*(81*q*q) == q*q*(81*q) == e
assert v+u == q+81*q*q == 42872
assert (q*q+81*q)**2 < 4*d
assert 1+42872**2-(1+4*d) == (u-v)**2
assert 1+42872**2-(1+4*e) == (81*q*q-q)**2

# Same optimal norms in both allocations.
round_even = lambda j: j+j%2
assert tuple(map(round_even,(1,2))) == tuple(map(round_even,(2,1))) == (2,2)
assert 22**2+5*3**2 == q*q       # Relative norm of beta.
assert (22-3*15)%q == 0          # The chosen root of sqrt(-5) modulo q.
assert 1+3*12**2 == v
assert 206**2+3 == u == 31*37**2
assert 28**2+3*11**2 == 31*37

# Independent norm and orientation checks for the composing elements.
# beta=A+B*r, with A=(-15+s)/2 and B=(1+3*s)/2, s^2=-5.
def mul5(U,V):
    a,b=U; c,d=V
    return a*c-5*b*d,a*d+b*c
AA=mul5((-15,1),(-15,1))
BB=mul5((1,3),(1,3))
assert tuple((a+3*b)//4 for a,b in zip(AA,BB))==(22,-3)
for p in (31,37):
    root=-206%p
    assert (root*root+3)%p==0 and (28-11*root)%p==0
    assert (28+11*root)%p!=0
def xnorm(a,b): return a*a+3*b*b
assert xnorm(1,12)**2*(22**2+5*3**2)==(433*23)**2
assert xnorm(28,-11)**2*(22**2+5*3**2)==(31*37*23)**2
print("Independent orientation checks passed")
```
