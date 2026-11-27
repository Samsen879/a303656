# Controlling Delta and h poles does not give a global circle anchor

Let p be inert odd, A,B units, and −A a nonsquare mod p. In the quartic construction, if v_p(S) is negative and odd then the entire circle fails. Indeed an integral Q would imply by the parent norm identity that m,Z are integral. If m is divisible by p, that identity implies Z²=−A mod p, impossible. If m is a unit, Y²=−4(A+m²+mS) has the negative odd valuation of S, again impossible.

At the actual u=23 label the revised h organized to remove earlier obstruction types is a unit at 10979. But h²+L has exact valuation one, so r=(h²+L)/(2h) has valuation one and S=r+B/r has valuation −1. The independent replay gives the h choice, its pinned local preliminaries, and the exact residues at 10979. No angle or parameter can repair this one h. This does not exclude other h or establish any result over all labels.

```python
from fractions import Fraction as F
from math import gcd, isqrt

def red(x, n):
    x = F(x)
    return x.numerator * pow(x.denominator, -1, n) % n

A = 5**562 + 3**188 - 131779
B = F(5**563 + 3**189 - 658897, 5)
D, L, C = B-A, 4*A-2*B, 3*B-4*A
lam = D * F(7, 2*13**4)**2
K, R = (B+C-lam-B*C/lam)/4, B*C-lam*lam
d, den = F(1463616, 9282325), 924
core = (2, 3, 5, 7, 11, 13)
T = abs(F(A*B).numerator * R.numerator)
for p in core:
    while T % p == 0:
        T //= p
T //= gcd(T, pow(abs(D.numerator), T.bit_length(), T))

rows, left = [], T
for j in range(14):
    z = d*(1+j*j)
    U = z*z+K
    f = z*U*(z*z-K)*(U*U+L*z*z)*(U*U-L*z*z)
    bad = gcd(left, pow(red(f, left), left.bit_length(), left))
    if left > bad:
        rows.append((left//bad, j*den))
    left = bad
    if left == 1:
        break
assert left == 1
a = (68392437145, 131465068579781339, 2226873210018264275445618,
     2007861763576786793646412398879, 24492265661614694552837064519542231103,
     577181895713950532360869733660058064699)
rows += [(p**(35+e), b) for p,e,b in zip(core,(2,1,0,1,1,0),a)]
n, M = 0, 1
for mod, b in rows:
    n += M*((b-n)*pow(M,-1,mod) % mod)
    M *= mod
n += M*max(0, ((int(abs(K)/d)+2)*den-n)//M+1)
z = d*(1+F(n,den)**2)
h = z+K/z
assert all(red(h-a,p**20)==0 for p,a in zip(core,(1,2,1,1,1,4)))

p = 10979
assert p % 4 == 3 and all(p % j for j in range(2,isqrt(p)+1))
assert T % p and red(h,p*p)==28060157
assert red(h*h+L,p*p)==10144*p
assert (A % p, red(B,p))==(10163,2296)
assert pow(-A % p,(p-1)//2,p)==p-1
```
