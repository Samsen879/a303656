# A complete-axis obstruction for the original dual mixed edge

This uses the signed anchor in [#93](https://github.com/Samsen879/a303656/pull/93), not the different anchor of [#101](https://github.com/Samsen879/a303656/pull/101). Write \(A=9^L,\ B=25^L\). The two endpoint labels are \(9A+B\) and \(A+5B\). For any common target \(n\) the endpoint norm difference is therefore \(4(B-2A)\), independently of the choice of Gaussian representatives.

For every \(L\ge1\), both endpoints cannot each load any complete factor \(6^{2j+1}+(-1)^j i\) with \(j\ge0\), even with independent conjugation. Indeed \(6^2=-1\pmod{37}\) implies that the norm of every full factor is divisible by 37; conjugation does not change it. If both endpoints were divisible by full factors, \(37\mid B-2A\) would be necessary. But \(25/9\equiv11\pmod{37}\) generates exactly \(\{1,11,10,36,26,27\}\), which omits 2. Thus deleting all but one complete axis on each side still fails.

This does not extend to split factors. In the actual #93 parametrization at \(L=2,y=11000\), the equality \(216-i=(6+i)(35-6i)\) gives one divisor on each side. Rotating preserves the norms and both resulting chords are primitive on the single target \(27585780689211246\). At \(L=28,y=410\), the factor \(3+8i\) of norm 73 can be loaded on both sides; the endpoint norm difference prevents a common lift to norm \(73^2\) because \(B-2A\equiv62\cdot73\pmod{73^2}\).

These are exact divisibility and same-target controls for real powers of 3 and 5. Neither small control is claimed to be a critical-angle mesh, and the obstruction does not apply to every possible choice of factors.

```python
from math import gcd
def gaussian_mul(z,w):
 a,b=z;c,d=w
 return a*c-b*d,a*d+b*c
def rotate(z,g):
 a,b=g
 m=a*a+b*b
 a,b=gaussian_mul(z,(a,-b))
 assert a%m==b%m==0
 return gaussian_mul((a//m,b//m),(g[0],-g[1]))
N=lambda x:x[0]**2+x[1]**2
def points(L,y):
 A,B=9**L,25**L
 D,E=12*B-3*A,A+10*B
 h=D-5
 t,r=divmod(5*y*y-h*y+5+3*h-E,10)
 assert r==0
 P=(h-3*t,t);Q=(P[0]+1,P[1]+3);R=(P[0]+3-y,P[1]-1-3*y)
 n=N(P)+3*A+25*B
 assert N(Q)+9*A+B==N(R)+A+5*B==n
 return A,B,P,Q,R,n
assert set(pow(25*pow(9,-1,37),j,37) for j in range(36))=={1,11,10,36,26,27}
assert gaussian_mul((6,1),(35,-6))==(216,-1)
A,B,P,Q,R,n=points(2,11000)
z,w=rotate(Q,(6,1)),rotate(R,(35,-6))
dx=lambda z: tuple(a-b for a,b in zip(z,P))
assert n==27585780689211246 and dx(z)==(25551993,48263263) and dx(w)==(-8496989,-55514065)
assert gcd(*dx(z))==gcd(*dx(w))==1
assert N(z)+9*A+B==N(w)+A+5*B==n
A,B,P,Q,R,n=points(28,410)
assert (B-2*A)%73**2==62*73
for z in (Q,R): assert N(rotate(z,(3,8)))==N(z)
print("PASS")
```
