# Pairing an ordinary prime's repair digits can peel a saturated core

The [one-axis peeling test](SINGLE_WITNESS_DIGIT_PEELING.md) can get stuck on a finite reader panel even when the panel is feasible for the same integer. A joint valuation-two repair of an ordinary prime with both axes ordinary gives a strictly stronger, though still sufficient, test.

Fix the other coordinates and let each \(p\)-primary exponent coordinate run modulo \(p^L\), \(L\ge2\) sufficient for the readers. The two powers \(U,V\) biject onto their respective unit cosets of depth one, taken modulo \(p^{L+1}\). If the residual is a unit, the whole grid passes. Otherwise the exact valuation-two slice is
\[
 V=n_p-U-p^2 w,\qquad w\in(\mathbb Z/p^{L-1}\mathbb Z)^\times.
\]
Both marginal coordinates are uniform on this slice. A reader of just one axis of depth \(e\) therefore costs a fraction at most \(p^{-e}\), not the larger load relative to one-axis repair capacity. For a reader of both axes with maximum depth \(E\ge2\), freeze its other axis: the deeper axis has \((p-1)p^{L-2}\) permitted values and at most \(p^{L-E}\) bad values. Its loss is at most \(p^{2-E}/(p-1)\).

A reader of the first digit on each axis sees the first-digit affine line \(\alpha i+\beta j=\gamma\bmod p\), with equal numbers of deep points on every first-digit pair. Its root equation on the line is \(a z+b z^k=n_t\bmod t\), \(z\) in an order-\(p\) group. Take the exact union of these shallow bad points and add the bounds on the other readers. If the total is below one, the two coordinates can be assigned after all unrelated tests. This can be used recursively when the needed bound holds for all returned lower assignments, or tested directly on the returned assignment. When \(n_t=0\) and \(k\ne1\bmod p\), at most one point is bad. When the characters agree and the coefficients cancel, a single shallow reader can instead veto the entire specified line.

In the same-\(n\) five-condition example below, the first-axis load at 3 is exactly one, the second-axis load there is \(11/9\), and both 7-axes have load \(3/7>6/49\). No one-axis deletion applies; dropping any one condition lets the first 3-axis peel the rest. Yet for the joint repair at 7, the chosen integer is zero modulo 7 and the first digit coefficients of the two powers are opposites when their sum collides (the normalized multiplicative coefficients are both 4). Thus the allowed line has slope 1. Its three shallow targets have character ratios \(4,3,4\). Two have target zero and cost at most one point each. In the nonzero-target case the corresponding three-character function is not identically zero; all its translations lie in a space of dimension at most three. Three basis translations of its support cover the group (otherwise some coordinate would be zero for every translate), so at least three points are nonzero, i.e. that reader costs at most four. Total loss is at most \(6/7\) on the line, uniformly after choosing a lower part passing 19. The concrete lower choice below has 252 survivors among 294 repair points.

The final check shows the opposite behavior: at 23 a line of good local repairs can completely cancel at the reader 139. This is a restricted line, not a common Wieferich or all-exponent obstruction. Both examples concern actual 3,5 orders and same-integer phases; they do not settle density one.

~~~python
from fractions import Fraction as F
from itertools import product

n = 342457643633
P = (7,19,43,127,883)
O = ((6,6),(18,9),(42,42),(126,42),(126,126))
for p,pair in zip(P,O):
    for a,o in zip((3,5),pair):
        assert pow(a,o,p)==1
        assert all(pow(a,o//r,p)!=1 for r in (2,3,7) if o%r==0)
        assert pow(a,p-1,p*p)!=1

def weight(o,r):
    d = 1
    while o%r==0:
        o //= r
        d *= r
    return F(1,d) if d>1 else 0

assert [sum(weight(o[j],3) for o in O) for j in (0,1)] == [1,F(11,9)]
assert [sum(weight(o[j],7) for o in O[1:]) for j in (0,1)] == [F(3,7)]*2
assert (n%4,n%3,n%343) == (1,2,35)
assert [n%p for p in P[1:]] == [0,12,0,0]
assert [(pow(a,18,49)-1)//7 for a in (3,5)] == [4,4]
assert [next(k for k in range(1,7) if pow(3,18*k,t)==pow(5,18,t))
        for t in P[2:]] == [4,3,4]

def s(x,y,m):
    return (pow(3,1+18*x,m)+pow(5,2+18*y,m))%m

A = [(x,y) for x,y in product(range(49),repeat=2)
     if (n-s(x,y,343))%343 in range(49,343,49)]
B = [(x,y) for x,y in A if all((n-s(x,y,t))%t for t in P[1:])]
assert len(A)==294 and len(B)==252 and B[0]==(1,12)
assert (n-s(1,12,343))%343==245
assert (n-s(1,12,4))%4==1 and (n-s(1,12,3))%3

n,r,q=705981,23,139
def s2(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m
A={(x,y) for x,y in product(range(r),repeat=2)
   if (n-s2(1+66*x,250+66*y,r*r))%(r*r)==0}
assert A=={(15*y%r,y) for y in range(r)}
assert all(s2(1+66*x,250+66*y,q)==0 for x,y in A)
for x,y in A:
    assert any((n-s2(1+66*x,250+66*(y+r*j),r**3))%r**3
               in range(r*r,r**3,r*r) for j in (0,1))

~~~
