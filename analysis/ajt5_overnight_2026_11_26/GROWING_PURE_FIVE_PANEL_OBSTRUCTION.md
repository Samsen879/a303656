# Growing pure-five shells can defeat a growing inert panel

A growing pure-\(5\) shell does **not** guarantee transfer. On the actual balanced P2 phase, both higher pure-\(5\) labels can fail at one prescribed target even when the common split cofactor is maximal, the first witness is ordinary, and both quotients pass a growing list of inert-prime checks.

### Obstruction at a prescribed target

Write \(A=3^a,\ B=5^b\), with \(39/40<B/A<122/125\), and use
\[
S_0=A+25B,\quad P=A+125B,\quad Q=A+625B,\quad
S_3=729A+B,\quad U=729A+625B.
\]
For an even \(j<b\), put \(c=5^{b-j}\) and \(R=5^{j/2}\), so \(B=cR^2\). At a prescribed target with \(c\mid n-S_0\), the two quotients are
\[
k-100R^2,\qquad k-600R^2,\qquad k=(n-S_0)/c.
\]
For distinct inert primes \(p,q>5\), the conditions
\[
k\equiv100R^2+p\pmod{p^2},\qquad
k\equiv600R^2+q\pmod{q^2}
\]
force exact odd depth one in the respective quotients. Neither second label represents \(n\), regardless of the supplied first representation or Gaussian orientation. If \(5\nmid k\), then \(c\) is already maximal: the common offset gcd is \(100B\), and \(v_5(n-S_0)=b-j\). [Verified finite-shell setup](https://github.com/Samsen879/a303656/commit/1ac4d7adccb4392542741dd3b3afd98049bb3e03)

### Genuine growing controls

These congruences are compatible with many actual ordinary first witnesses. Choose \(k=X^2+Y^2\) with \(X\equiv1,\ Y\equiv0\bmod20\) and \(11\mid X,Y\). At \(p\) and \(q\), the required residues of \(k\) are units. Each is a sum of two squares modulo the prime, and a nonzero coordinate lifts that sum to the specified residue modulo its square. At any other checked inert prime, choose \(k\) outside the two offset residues. CRT gives progressions for \(X,Y\).

Take points of that grid with
\[
\frac{917}{25}<\frac XR<\frac{7337}{200},\qquad
\frac1{200}<\frac YR<\frac1{100}.
\]
Then \(n=S_0+ck\equiv36\bmod121\) on the pinned phase. The first representation is \((\sqrt c\,X,\sqrt c\,Y)\), and the exact bounds give
\[
S_3<S_0+cX^2\le n\le U,\qquad n>2S_3-P.
\]
The last inequality means that **either** second quotient, if it were a norm, could be placed at ordinary height by putting its larger coordinate first. The failure is arithmetic. Also \(A+3125B>U\), so \(P,Q\) exhaust the higher pure-\(5\) labels available at these targets.

The checked budget can grow. For a cutoff \(Y_0\ge11\), let \(G\) be the product of inert primes up to \(Y_0\). Take an inert prime \(p\mid4G-1\) and an inert prime \(q\mid4Gp-1\). They are distinct and exceed \(Y_0\). The CRT modulus is \(O(G^7)\), hence \(R^{o(1)}\) whenever \(Y_0\log Y_0=o(\log R)\). The grid then gives \(R^{2-o(1)}\) distinct targets, using the divisor bound on representations of \(k\). Both quotients are \(1\bmod4\) and units at every checked inert prime. Choosing even \(j\to\infty\) with \(j=o(b)\) lets the maximal cofactor remain as large as \(A^{1-o(1)}\) while the shell grows.

### Standalone replay

This actual \(3,5\) control checks all inert primes through \(31\), with the two failures at \(43\) and \(47\).

```python
from math import gcd

a,b = 574422,392104
A,B = 3**a,5**b
assert a%10 == 2 and b%110 == 64 and 39*A < 40*B and 125*B < 122*A
j = 2*(b//4)
R,V = 5**(j//2),5**((b-j)//2)
c = V*V

def pair(z,m):
    sq = {x*x%m:x for x in range(m)}
    return next((x,sq[(z-x*x)%m]) for x in range(m)
                if (z-x*x)%m in sq)

rows = [(20,1,0),(11,0,0)]
for p,d in ((43,100),(47,600)):
    rows.append((p*p,*pair(d*R*R+p,p*p)))
for p in (3,7,19,23,31):
    z = next(z for z in range(p) if (z-100*R*R)%p and (z-600*R*R)%p)
    rows.append((p,*pair(z,p)))
x=y=0
M=1
for m,u,v in rows:
    z=pow(M,-1,m)
    x+=M*((u-x)*z%m)
    y+=M*((v-y)*z%m)
    M*=m
X=x+M*((917*R//25-x)//M+1)
Y=y+M*((R//200-y)//M+1)
assert 917*R<25*X and 200*X<7337*R and R<200*Y and 100*Y<R

S0,S3,U=A+25*B,729*A+B,729*A+625*B
P,Q=A+125*B,A+625*B
n=S0+(V*X)**2+(V*Y)**2
assert n%121==36 and 2*S3-P<n<=U and S3<S0+c*X*X
assert gcd(n-S0,gcd(P-S0,Q-S0))==c
F,G=(n-P)//c,(n-Q)//c
assert all(d%4==1 and all(d%p for p in (3,7,11,19,23,31)) for d in (F,G))
assert F%43**2==43 and G%47**2==47

from fractions import Fraction as Fr
lo,hi=Fr(917,25),Fr(7337,200)
assert Fr(39,40)*(lo*lo+148)>1456
assert Fr(122,125)*(hi*hi+Fr(1,100)**2-600)<728
assert Fr(39,40)*(lo*lo+24)>728
assert Fr(39,40)*(3125-625)>728
print("controls and uniform height constants passed")
```

The congruences decide failure for a target once it is prescribed. The grid construction proves that many eligible targets satisfy them. These targets already have an \(S_0\) witness. The result leaves lower pure-\(5\) labels, changes in the \(3\)-exponent, and unrestricted target transfer open.

At the reserved primes two distinct bad valuations are used; at 11 the forced vanishing of the first quotient seed still leaves both shifted quotients units because neither offset is zero modulo 11. Squaring and scaling the CRT coordinates is a construction of many bad-transfer targets, not a counterexample to representability: the first representation is already present.
