# The least native square multiplier for (5,3)

For the native seed \((5,3)\), \(17^2=289\) is the least \(r=q^2\) for prime \(q>3\) such that \(5^{2r}-3^{2r}\) is a norm \(x^2+3y^2\). All four signed shells at \(q=17\), levels one and two, have explicit coordinates. Their product multiplied by \(16=4^2\) is the full difference. The replay uses only integer arithmetic, not an assertion about any large-prime factor.

At the smaller primes \(q=5,7,11,13\), the full difference has valuation one at the actual inert prime \(11,197,23,53\), respectively. The middle control \(q=7\) passes both first-layer norm equalities and fails specifically at its second layer.

An admissible \(r\) extends to \(3r\): factor \(A^3-B^3\) for \(A=5^{2r},B=3^{2r}\) and use \(A^2+AB+B^2=((A-B)/2)^2+3((A+B)/2)^2\). Thus \(289\cdot3^j\) is admissible for each \(j\ge0\), not a new non-cubing multiplier. The exact question at \(17^3\) and the pointwise target problem stay open.

## Generated positive targets

For these indices put \(Q=5^{2r},Z=3^{2r}\). Multiplying a norm representation by scale 2 gives \(V^2+3W^2=4(Q-Z)\) with \(V,W\) divisible by 8, since the unscaled representation can retain the scalar seed factor 4. Rotating the direction of \((V,\sqrt3 W)\) by \(0,60,120\) degrees gives integral coordinates divisible by 4. Since \(3\nmid V\), exactly two choices have \(3\nmid W\). Their lines are separated by \(60\) degrees, so at least one has \(3W^2\ge Q-Z\).

For \(L=1,3\), let \(D_L=3W^2+2LZ\equiv2\bmod4\). Legendre's theorem gives a sum of three squares. Take \(t\) to be the smaller of the two odd coordinates in absolute value, and call the others \(x,y\). Since \(v_3(D_L)=1\), none of the coordinates vanishes modulo 3. Now \(x^2+y^2\ge D_L/2>LZ\), so
\[
 n=5Q+LZ-x^2-y^2=Q+(4-L)Z+V^2+t^2\in(Q,5Q).
\]
As \(V^2=16,t^2=1,Z=9,Q=1\bmod24\), \(L=1,3\) give \(n=21,3\bmod24\), respectively. Both actual exponent axes grow. This constructs targets, not a selector for prescribed \(n\).

```python
witnesses = {
    (1, -1): (512959, 198560),
    (1,  1): (225833, 121632),
    (2, -1): (
        114792319219011872638986807213188904428103962881996076399055656581752532318254975178592131870177,
        949000774563177791679267766261510284095096949312078684882906281270969451930408387143300308152,
    ),
    (2,  1): (
        114746667825705859742939384182460424698468167451742156138753413107539473812088533428645444702263,
        1704843785569940513994802227007735596776032265007690562713118199648764056324264413790273367768,
    ),
}
for (j, sign), (x, y) in witnesses.items():
    r, s = 17**j, 17**(j-1)
    assert (5**s + sign*3**s)*(x*x + 3*y*y) == 5**r + sign*3**r

from math import isqrt
assert 137**2+3*80**2==(5**7-3**7)//2
assert 74**2+3*39**2==(5**7+3**7)//8
for q,j,sign,p,m in [(5,1,-1,11,110),(7,2,-1,197,1773),
                    (11,1,1,23,368),(13,1,1,53,53)]:
    assert all(p%i for i in range(2,isqrt(p)+1)) and p%3==2
    r,s=q**j,q**(j-1)
    h=(5**r+sign*3**r)//(5**s+sign*3**s)
    assert h%(p*p)==m and m%p==0 and m%(p*p)!=0
    assert (pow(5,2*q*q,p*p)-pow(3,2*q*q,p*p))%(p*p) in range(p,p*p,p)
```
