# Higher-power tail on prime-power support

The higher-power source tail falls from 7,320 to 28 units of 10^(-11) density. Against FINITE_PRIME_SOURCE_REPRICE.md the new natural exception density is **below 0.000067084085%**. The finite subtotal remains 56,462, and the cutoffs and other two tails are unchanged.

For inert ordinary sources r in the previously certified range 100<r<=20,000, the cube case division from ORDINARY_INERT_CUBE_DENSITY_BOUND.md applies to D=r³>10^6. Preserve its robust branch inside the reader-cover bound. The remaining charge per cube is at most R_D times ((r S_D)^r/r! + gamma/r² + (19/48)/r³), where gamma=min(1,r S_D/(r−K_r)) and K_r=floor((1+sqrt(4r−3))/2). The parity bound 19/48 is universal: the largest nonsquare parity-head mass in the original head table is 38 of 96. For larger sources retain the old coarse bound. The rational replay uses K_r<r/9, monotone integral estimates on the inert spacing-four progression, and bounds the auxiliary factorial branch by a geometric tail. The older ordinary-source check through 20,000 is inherited; no scan of larger sources or terminals is needed.

The same reader-cover bound per D can retain its actual support D=r^a, a>=2. Square powers are bounded on all integer squares above 10^6. In a dyadic bin (Y,2Y], a nonsquare prime power needs an odd exponent at least three; there are at most (21+j)/2 possible exponents for Y=10^6*2^j, and at most (2Y)^(1/3) bases per exponent. The replay bounds the resulting geometric moments using ratio 1/6. This reduces the reader-cover portion below 6.634 units. All other high-power lifting charges are retained, including the large-source exceptional bound.

The two changes apply only above 10^6, leaving the eight finite cube rows untouched. The terminal's largest assigned order prime power distinguishes this tail from the finite prime-source rows. No pointwise or density-one conclusion follows.

```python
from fractions import Fraction as Q
from math import ceil, comb, factorial

W,H = 10**11,10**6

def series(y):
    z = (y-1)/(y+1)
    t = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return t+2*z**25/(25*(1-z*z))

ln2 = series(Q(2))

def hi(x):
    y,k = Q(x),0
    while y>=2:
        y/=2
        k+=1
    return Q(ceil(W*(series(y)+k*ln2)),W)

# Upper bound for the integral of (a log x+b)^n / x^k from X.
def I(X,k,a,b,n=1):
    L = a*hi(X)+b
    return sum(Q(factorial(n),factorial(n-j))*a**j*L**(n-j)
               /(k-1)**(j+1) for j in range(n+1))/X**(k-1)

L = hi(H)+Q(1,2)
old_read = Q(81,8)/H**2*(L**3/2+3*L*L/4+3*L/4+Q(3,8))
old_cube = Q(3,2)*I(100,5,3,Q(1,2))
z,w = Q(1,31**3),Q(1,20000**3)
odd = Q(3,2)*I(30,8,5/(1-z)+2*z/(1-z)**2,Q(1,2)/(1-z))
even = Q(3,2)/2**28*(2*hi(31)*z/(1-z)**2+Q(1,2)*z/(1-z))
rare = Q(3,2)*I(20000,4,2/(1-w)**2,Q(1,2)/(1-w))
keep = odd+even+rare
old = ceil(W*(old_read+old_cube+keep))
assert old == 7320

# Reindex the reader-cover sum on squares and nonsquares.
x = Q(1,6)
a,b = L+ln2,ln2
mom = (1/(1-x), x/(1-x)**2, x*(1+x)/(1-x)**3,
       x*(1+4*x+x*x)/(1-x)**4,
       x*(1+11*x+11*x*x+x**3)/(1-x)**5)
assert 2*H<2**21 and Q(4,3)**3>2
nonsq = Q(81,8)*Q(200,3)/H**3*sum(
    comb(3,j)*a**(3-j)*b**j*(21*mom[j]+mom[j+1]) for j in range(4))
read = Q(81,8)*I(1000,6,2,Q(1,2),3)+nonsq
assert W*read < Q(6634,1000)

# Ordinary cubes, using the inherited source check through 20,000.
# K_r <= sqrt(r)+1/2 <= 21*r/200 < r/9 for r >= 100.
# Inert integers start at 103. The integral from 99 pays for spacing four.
c = Q(100,99)
assert c*(3*hi(100)+Q(1,2))/100**2 < Q(1,2)
markov = Q(9,8)*c*c*I(99,8,3,Q(1,2),2)/4
intercept = Q(19,48)*c*I(99,6,3,Q(1,2))/4
aux = c*(3*hi(100)+Q(1,2))/100**3/2**100
far = c*I(20000,5,3,Q(1,2))
cube = markov+intercept+aux+far
assert ceil(W*(old_read+cube+keep)) == 1674

new = ceil(W*(read+cube+keep))
assert new == 28

# Exact replacement within the verified 30214-unit finite-prime ledger.
delta = Q(old-new,W)
assert delta == Q(7292,W)
old_pct_hi = Q(743760846076458,10**19)
assert old_pct_hi - 100*delta < Q(67084085,10**12)
print(old, new, "revised exception bound < 0.000067084085%")
```
