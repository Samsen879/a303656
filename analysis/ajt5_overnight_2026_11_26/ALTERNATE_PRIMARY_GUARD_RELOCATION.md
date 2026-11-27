# Relocating exceptional guards to alternate primary digits

**A guard can be moved to another digit in its actual order without consuming the ordinary lifting coordinate.** On the same target as the two-guard result, moving \(40487\) from \(d_{31}\) to \(d_{653}\) lets us use \(d_{31}=6\), its old forbidden digit, while keeping \(c_{31}\) available. An exact polynomial gcd leaves **651 of the 653** choices at the new coordinate. The construction also extends to three genuine base-\(5\) hard rows on one integer. [Two-guard baseline](https://github.com/Samsen879/a303656/blob/55a42657f5f156ebacf2b173df48d1044352ad12/analysis/ajt5_overnight_2026_11_26/TWO_REAL_SHALLOW_GUARDS.md)

### A relocation criterion for a variable number of guards

For a protected row \(p\), suppose the allowed \(c\)-digits make \(3^c\bmod p\) range over \(AH_u\), a coset of a subgroup of size \(u\). Assign this row to a \(d\)-coordinate \(s\mid o_5(p)\), and fix the other digits read by its actual order. If \(a=v_s(o_5(p))\) and \(h<a\) low digits at \(s\) are already locked, the remaining choices for \(5^d\bmod p\) are a coset of size \(s^{a-h}\). A value \(X=5^d\bmod p\) is unsafe exactly when
\[
(N-X)^u-A^u=0.
\]
This polynomial has degree \(u\). Thus the row forbids at most \(u\) of the remaining choices, including when \(N\equiv0\bmod p\). A gcd with the polynomial defining the \(5\)-coset gives the exact count.

Several rows can share a relocated coordinate \(s\) if
\[
\sum_{p\text{ assigned to }s}\frac{u_p}{s^{a_p-h}}<1.
\]
This works for any finite number of groups if they can be ordered so that each group reads only its own coordinate and earlier or already fixed \(d\)-coordinates. Choose their digits in that order. Stationary guards must either ignore the moved digits or already be protected uniformly over them. Afterwards an ordinary prime can lift on either axis if its own coordinate is still free and every guard that reads it was protected uniformly over that variation. This gives an order-graph test with explicit capacities and prelocks. A cycle or a failed capacity inequality leaves further cases to check.

### Real relocation at \(40487\)

Retain the baseline target \(N_0\), \(c\equiv0\bmod653\), and odd \(d\), but take \(d\equiv6\bmod31\). Keeping the old \(d\equiv5\bmod653\) allows the genuine hard row at \(40487\) with \(c=0,d\equiv10453\bmod40486\). Release the \(653\)-digit instead. The actual orders are
\[
o_3(40487)=31\cdot653,\qquad o_5(40487)=2\cdot31\cdot653.
\]
The possible \(c\)-powers are the order-\(31\) subgroup. The \(d\)-exponent is \(37\bmod62\), and varying \(d_{653}\) takes it through a coset of size 653. Modulo \(40487\), the exact check is
\[
\gcd\!\left(X^{653}-30604,\ (N_0-X)^{31}-1\right)
=(X-14676)(X-9902).
\]
The roots correspond to \(d_{653}=5,101\). Taking \(d_{653}=0\) protects \(40487\) for every \(c_{31}\). The other guard, \(20771\), ignores \(d_{653}\); it remains protected because its forbidden \(d_{31}\) digit is \(5\). This is a failure of the *old uniform guard at the frozen digit*, followed by an actual relocation. It does not require the old finite panel to have been unsatisfiable.

### Three genuine hard rows and an ordinary lift

Extend the baseline square coordinates \(X_0,Y_0\) to \(X,Y\) by retaining them modulo \(972\cdot11^3\cdot31^3\cdot67^3\cdot20771^2\cdot40487^2\) and adding these CRT conditions:

| Modulus | \(X\) | \(Y\) |
|---|---:|---:|
| \(30469139^3\) | \(0\) | \(23419822301212619237474\) |
| \(1645333507^2\) | \(0\) | \(148695610142201686\) |

Set \(N=10+X^2+Y^2\), so \(N\) has a true representation with \(c=2,d=0\). At \(c=0\), the hard exponents at \(20771,40487,1645333507\) are respectively \(5,10453,5\). Each row has \(5^{p-1}\equiv1\bmod p^2\) and \(N-1-5^e\equiv p\bmod p^2\). All three are ordinary to base \(3\).

Write \(u=30469139\). The third guard uses the actual orders \(o_3(1645333507)=o_5(1645333507)=54u\). Choose \(d_u=1\) to avoid its root digit \(5\). The intermediate row \(u\) is protected via \(d_{1429}=1\), since \(o_5(u)=1429\cdot1523\) and its collision root reads \(5\bmod1429\).

The complete locks for this control are
\[
\begin{aligned}
c&\equiv0\pmod{\operatorname{lcm}(10640680710,\ 54u,\ u-1)},\\
d&\equiv5\pmod{439966890},\\
(d\bmod31^2,\ d\bmod653,\ d\bmod u,\ d\bmod1429)&=(6,0,1,1).
\end{aligned}
\]
The \(c\)-modulus includes the locks preserving the old \(11,67\) shells, and has no factor \(31\). Both shared guards cover the entire \(c_{31}\) orbit. At the chosen \(d\), keeping \(c=0\) gives \(8\cdot31\bmod31^2\); the available ordinary \(c_{31}\) lift changes it to exact valuation \(2\). The replay verifies the three units and all preceding norm conditions with integer modular powers.

```python
from math import gcd,isqrt,lcm
X0=7469418541821370391905589976840289
Y0=8187539692710415393868954311484136
N0=10+X0*X0+Y0*Y0
def crt(*pairs):
    x,M=0,1
    for a,m in pairs:
        g=gcd(M,m)
        assert (a-x)%g==0
        x+=M*((a-x)//g*pow(M//g,-1,m//g)%(m//g))
        M=lcm(M,m)
    return x
def order(b,p,expected):
    assert pow(b,expected,p)==1
    u=expected
    for k in range(2,isqrt(u)+1):
        if u%k==0:
            assert pow(b,expected//k,p)!=1
            while u%k==0: u//=k
    if u>1: assert pow(b,expected//u,p)!=1
r,q,P,u=31,40487,1645333507,30469139
for p in (r,q,P,u,20771,653,1429):
    assert all(p%j for j in range(2,isqrt(p)+1))
for b,expected in ((3,31*653),(5,62*653)):
    order(b,q,expected)
H={pow(3,653*j,q) for j in range(r)}
roots=[]
for j in range(653):
    d=37+62*j
    x=pow(5,d,q)
    assert pow(x,653,q)==30604
    if (N0-x)%q in H: roots.append((d%653,x))
assert sorted(roots)==[(5,14676),(101,9902)]
moduli=(972*11**3*31**3*67**3*20771**2*q**2,u**3,P**2)
N=10+crt((X0,moduli[0]),(0,moduli[1]),(0,moduli[2]))**2+crt((Y0,moduli[0]),(23419822301212619237474,moduli[1]),(148695610142201686,moduli[2]))**2
for p,e in ((20771,5),(q,10453),(P,5)):
    assert p%4==3 and pow(5,p-1,p*p)==1 and pow(3,p-1,p*p)!=1
    assert (N-1-pow(5,e,p*p))%(p*p)==p
for base in (3,5): order(base,P,54*u)
order(5,u,1429*1523)
def R(c,d,m):return (N-pow(3,c,m)-pow(5,d,m))%m
B=lcm(10640680710,54*u,u-1)
d=crt((5,439966890),(6,31**2),(0,653),(1,u),(1,1429))
assert B%31 and R(0,d,31**2)==8*31
c=B*next(i for i in range(31**2) if R(B*i,d,31**3)==31**2)
assert all(R(c,d,p) for p in (20771,q,P,u))
assert (R(c,d,4),R(c,d,27),R(c,d,11**3),R(c,d,67**3))==(1,18,121,4489)
print('OK')
```

This verifies a real three-row panel and a sufficient order criterion. Arbitrary exceptional panels can still have insufficient alternate capacity or coupled order dependencies.
