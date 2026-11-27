# First rank seven is excluded through seventeen sources

This extends the fixed-target muted-slice rank-seven argument only. It does not exclude other first nonlinear ranks at budget 17, and it does not yet establish an 18-source theorem for all-exponent obstructions. Use the 72-unit window, two 36-unit ternary halves, and lower-only bound A(l)=12+4(l−1) for positive l, with A(0)=0, from RANK_SEVEN_SIXTEEN_SOURCE_ESCAPE.md. All units have size 1/135.

## Tight flat branches

With 11 top and 6 lower sources, remove one lower guard of cost at most four (copies of the only potentially larger row-19 guard coincide). The 11+5 result guarantees 16 uncovered units; restoring that guard leaves at least 12.

With 12 top and 5 lower sources, no nested witness fits. A nonshallow singleton caps the top union at 18; otherwise a shallow singleton confines it to one half B. If row 19's lower guard misses the opposite half, that half alone leaves 16 units. If a deficient 7-branch has at most two sources, its top union costs at most 24 on B. In the remaining cases the deficient branch sizes are (3,3) or (3,4). The five other branches use the five shallow mixed heads, and only four order-63,126 heads are available across the deficient branches. A three-source branch with at most two full ternary ninths caps the top union at 28 by RANK7_ELEVEN_TOP_SPLIT.md.

The sole new case has three such ninths on the three-source side and at most one on the four-source side. A full quinary strip on B on the latter side can use only the actual order-35 heads 211 and 631. The least-helper list consists of divisors of the permitted lower (at most one first ternary and one first quinary digit) times the first 7 digit. The older mutes and row-11 cut exclude the smaller quinary possibilities; order 70,105,210 have no inert factor by the primitive norm certificates below. At most two full quinary strips remain. Such a strip costs nine units in B, or six after one ternary ninth is removed. Every other proper guard costs at most four. The four-source cap is thus 28, with uncovered mass at least 72−28−28=16.

## Other source counts

With flat-only support a deficient singleton caps the top union at 18. For 9 or 10 top sources without a deficient singleton, a deficient pair costs at most 24 in the half selected by a shallow singleton (a nonshallow singleton gives the stronger 18 cap). With 13 or more top sources, a singleton costs at most 36. Without one, each branch needs at least two and the smaller of the two deficient branches has at most floor((t−10)/2) sources, each costing at most 18. These caps give the table in the replay.

A nested witness needs 13 top sources. Two candidate expanded branches would require at least fourteen second prefixes and five other first prefixes, beyond budget 17. Of the six branches outside the unique possible expansion, at least two must be singleton; any flat or nested witness needs those singleton sources. Their proper guard is bounded by 36, and at most four lower-only sources can cost 24. The gap is at least 12. Thus all first-rank-seven cases escape on this slice, with at least six units in the coarsest split.

The replay verifies exact order inventory and conditional geometry. It supplies no genuine rigid source.

```python
from math import gcd, isqrt

def cyclo(x,a,b,s):
    N,r = divmod((x**(a*b)+s)*(x+s),(x**a+s)*(x**b+s))
    assert r == 0
    return N

def primitive(N,a,b):
    assert N == a*a+b*b and gcd(a,b) == 1

N35 = cyclo(5,5,7,-1)
assert N35 == 211*631*(249459**2+544090**2)
primitive(N35//(211*631),249459,544090)
for q in (211,631):
    assert q%4==3 and all(q%j for j in range(2,isqrt(q)+1))
    assert pow(5,35,q)==1 and pow(5,35,q*q)!=1
    assert pow(5,7,q)!=1 and pow(5,5,q)!=1

primitive(cyclo(5,5,7,1),233260120,130734441)
for s,a,b in ((-1,31829902611893280,58230199846466641),
              (1,32804091353358780,43693984265720489)):
    N,r = divmod(cyclo(5**7,3,5,s),cyclo(5,3,5,s))
    assert r==0
    primitive(N,a,b)

# Four sources, at most one full ternary ninth and two full quinary strips.
assert max(12*s+q*(9-3*s)+4*(4-s-q)
           for s in range(2) for q in range(3)) == 28

A = lambda ell: 12+4*(ell-1) if ell else 0
caps = (18,18,24,24,28,28,36,36,36,54,54)
assert [72-cap-A(17-t) for t,cap in enumerate(caps,7)] == [
    6,10,8,12,12,16,12,16,20,6,18]
assert 72-36-A(4)==12
print("PASS")

from itertools import combinations_with_replacement
B={(x,y) for x in range(1,27,3) for y in range(4)}
N=[{p for p in B if p[0]%9==a} for a in (1,4,7)]
Q=[{p for p in B if p[1]==a} for a in range(4)]
# For each stripe/ninth choice, independently recompute residual size and
# add the proven at-most-four units per remaining proper rectangle.
assert max(len(set().union(*X,*Y))+4*(4-k-j)
           for k in range(2) for j in range(3)
           for X in combinations_with_replacement(N,k)
           for Y in combinations_with_replacement(Q,j))==28
print("Independent deficient-branch union bound verified")
```
