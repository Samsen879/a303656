# A true four-column seed and the exact limit of the old Pell identity

At \(m=2000001865414,\ x=5m+4=10000009327074\), all four adjacent columns \(d=4,8,12,16\) are strictly active at the same point and the least true shift is \(248=5+3^5\). For the first-root residual \(x-248\) the square coordinates are \((958715,3013449)\), and for the four parent residuals \(m-5^d-1\) they are \((871948,1113422),(991318,1008608),(418052,1350922),(73672,1357198)\). The corresponding child residuals \(x-5^{d+1}-9\) are five times the parent residuals, so the map \((a,b)\mapsto(2a-b,a+2b)\) proves genuine child representations. The verification below covers all twenty earlier shifts with exact valuation one at inert primes, none of them 3.

## The previous infinite family's curve cannot carry a fourth identity

The [first-248 three-column Pell construction](FIRST_248_THREE_ACTUAL_COLUMNS_PELL.md) uses \(Y^2=a(s-s_*)^2+b(s-s_*)\) and certifies \(d=4,8,12\). At any other d the additional parent, after multiplication by the inverse of the rational norm constant \(4/g\), would be \(s^2+h_d\), where \(h_d=q^2+g(5^{12}-5^d)/4\). For every remaining \(d\le12\), the original seed \(s=s_*,Y=0\) has an inert prime of odd valuation in that parent residual, as verified below. A two-square rational-function identity with finite value specializes at this point: on the smooth curve any poles in the two coordinates cannot cancel their leading squares in its real residue field. Hence none of these parent residuals is a rational-function sum of two squares on the old curve.

For \(d\ge13\), take the same real point for all d: \(s=-77000000\) has \(a(s-s_*)^2+b(s-s_*)>0\), while \(s^2+h_{13}=-28143656675900<0\) and \(h_d\) decreases strictly. Nonnegative squares at that real smooth point cannot realize the negative target (poles cannot cancel there either). Thus there is no fourth-column identity anywhere in the old curve's function field. This does not rule out additional columns at individual integer points, and the new four-column seed is not yet known to belong to an infinite four-column family.

~~~python
from fractions import Fraction as F
from math import isqrt
def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
m=2000001865414; x=5*m+4
blocks={2:312500291471,4:7,6:19,8:11,10:1831,14:23,26:117751,
        28:14326660927,32:7,34:941351,52:10998763,82:19,86:147058960691,
        106:23,126:71,128:19079,134:9413191,152:23,206:11,244:23}
assert set(blocks)=={5**e+3**f for e in range(4) for f in range(6) if 5**e+3**f<248}
assert len(set(blocks.values()))==14
assert x-248==958715**2+3013449**2
for r,p in blocks.items():
    assert p>3 and p%4==3 and prime(p)
    assert (x-r)%p==0 and (x-r)%(p*p)!=0
for d,a,b in [(4,871948,1113422),(8,991318,1008608),
              (12,418052,1350922),(16,73672,1357198)]:
    assert m-5**d-1==a*a+b*b
    assert x-5**(d+1)-9==(2*a-b)**2+(a+2*b)**2
m0=10000899126
for d,p in {0:103,1:151,2:23,3:1111211,5:383,6:59,7:19,
            9:67,10:19982267,11:3}.items():
    assert p%4==3 and prime(p)
    r=m0-5**d-1
    v=0
    while r%p==0:
        r//=p
        v+=1
    assert v%2==1
s0,g,q=245623470,24771085,-9512335
h0,h3=F(3204782529189581,2),1599972509339725
l0,l3=1/(s0*s0+h0),F(1,s0*s0+h3)
b=s0*(l0+l3)-F(1,s0)
a=l0-(s0*l0-b/2)**2
s=-77000000
v=s-s0
assert a*v*v+b*v>0
assert s*s+q*q+F(g*(5**12-5**13),4)==-28143656675900
~~~
