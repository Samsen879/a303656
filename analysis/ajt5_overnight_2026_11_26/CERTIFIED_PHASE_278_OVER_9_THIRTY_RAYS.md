# A certified phase 278/9 and the 30-ray generated-population bound

The coprime seed (139,123) gives two verified integral half-norms in the norm x²+3y². This certifies the ray (278·3^k,246·3^k) in the exponents of 5 and 3 respectively. Both axes grow. The arithmetic also produces genuine targets having positive two-square residual in both odd classes 3 and 21 modulo 24, and nearby targets at the same height bin for which the same prescribed label fails. Those failed labels are not counterexamples to Sun's conjecture.

The previous catalogue already includes phase 314/9. Inserting 278/9 splits (30,290/9) into ratios 139/135 and 145/139. The unique largest remaining ratio is 35/33, attained on (22,70/3). Here 54 is the cyclic copy of 18.

For this ray the two coprime cube-factor orientations have residue (8,±2) modulo 15, which are inverse under x²+3y² multiplication. Across k factors the net signed count can be 1 for odd k and 2 for even k≥2. In the two choices of rotation the second coordinate is 1 or 10 modulo 15 (checked below), implying opposite characters modulo 5 for 3w²+2LZ for each L=1,3, since Z=3^(246·3^k)≡4 modulo 5. Both are 5-adic units; hence their squarefree kernels differ. These give distinct discriminants, at most one of which is exceptional in Tatuzawa's effective lower bound. The rotation angles at the base have sine bounded away from zero; the actual cube factors differ in argument from ±π/3 by O(Z/Q), whose total over all iterations is less than 1/32 here. Thus the relevant w remain of order √Q. Applying the same effective three-square sphere and divisor multiplicity argument as in the [preceding 29-ray construction](https://github.com/Samsen879/a303656/commit/0822ed65934d962a216f7d22758b2e8621a399f4) yields at least ≫ε X^(33/70−ε) distinct generated targets up to X in each odd class. This improves 27/58 for this family; it says nothing about an arbitrary prescribed target or a stronger natural-density lower bound.

## Exact replay (Python 3)

~~~python
from math import gcd

def N(x, y):
    return x*x + 3*y*y

A, S = 5**139, 3**123
a, b = 2648973724981955407420796392407109640082187290121, \
       229191580486927341643728670776859748017557327344
c, d = 1080196964727802103900857836970951902434933203088, \
       -457105586536491336065248725767446734199894619025
assert gcd(139, 123) == 1
assert A - S == 2*N(a, b) and A + S == 8*N(c, d)

Q, Z = A*A, S*S
x, y = 8*(a*c - 3*b*d), 8*(a*d + b*c)
O = [(x, y), ((x-3*y)//2, (x+y)//2), ((-x-3*y)//2, (x-y)//2)]
W, V = max((abs(w), abs(v)) for v, w in O if w % 3)
assert N(V, W) == 4*(Q-Z) and W > 3*S

for L in (1, 3):
    for t in (W, S+169):
        x, y = (t-S, t) if L == 1 else (t+S, t-2*S)
        n = 5*Q + L*Z - x*x - y*y
        R = n - Q - (4-L)*Z
        assert Q < n < 5*Q and n % 24 == (21 if L == 1 else 3)
        assert R > 0
        if t == W:
            assert R == V*V + (W+S)**2
        else:
            assert R % 131**2 == 118*131

from fractions import Fraction as F

def mul(P, T):
    x,y=P; u,v=T
    return x*u-3*y*v,x*v+y*u

def rots(x,y):
    return [(x,y),((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)]

base=(8*(a*c-3*b*d),8*(a*d+b*c))
cube=((Q-Z)//2,(Q+Z)//2)
assert tuple(z%15 for z in cube)==(8,2)
assert tuple(z%15 for z in mul(cube,(cube[0],-cube[1])))==(1,0)
for fac in (cube,mul(cube,cube)):
    usable=[w for _,w in rots(*mul(base,fac)) if w%15 in (1,10)]
    assert sorted(w%15 for w in usable)==[1,10]
for k in (1,3):
    assert {pow((3*w*w+8*k)%5,2,5) for w in (1,10)}=={1,4}

P=list(map(F,"18 166/9 170/9 178/9 182/9 62/3 190/9 22 70/3 74/3 26 82/3 86/3 30 278/9 290/9 314/9 34 110/3 38 118/3 122/3 42 130/3 134/3 46 142/3 50 470/9 158/3 54".split()))
items=sorted((v/u,u,v) for u,v in zip(P,P[1:]))
assert items[-1]==(F(35,33),F(22),F(70,3)) and items[-2][0]<F(35,33)
assert F(1,2)/items[-1][0]==F(33,70)
~~~

Four other proposed interior lifts are excluded by primitive inert divisors. For (u,v,q) and divisor D in the following list, the exact test uses H=(5^(uq)−3^(vq))/(5^u−3^v). The conditions D≡2 mod 3 and gcd(D,(H/D)(5^u−3^v)q)=1 imply an inert prime of odd valuation in H with exact order q; no claim about factoring D is needed.

~~~python
for u,v,q,D in [
    (7,5,59,416219452820013820493),
    (7,5,61,27484331267744790059),
    (9,1,47,44699351),
    (9,11,47,170132895498527777),
]:
    B=5**u-3**v
    H=(5**(u*q)-3**(v*q))//B
    assert H%D==0 and D%3==2 and gcd(D,H//D*B*q)==1
~~~

The other two lift candidates (59,35,7), (61,37,7) remain unresolved.
