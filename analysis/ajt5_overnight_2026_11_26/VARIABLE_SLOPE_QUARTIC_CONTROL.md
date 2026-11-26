# An explicit variable-slope lift at d=8 and an obstruction to the same fixed slope

The normalized slope-one construction in NORMALIZED_QUARTIC_STEP_AND_OBSTRUCTION.md fails at $d=8$. Allowing slope $r=39$ does give an unbounded integer orbit at the same real label $(8,2;9,3)$.

For the general square-difference label, write $A=5^d-131770$, $B=A-4$, $H=r+A/r+4$, $m=H/2$ and put
$$
z=rt^2-2,\quad w=(z^2+m^2+B)/H,\quad D=(r^2t^2+A)/m .
$$
Parent coordinates are $(w-D,t(D-r))$, with norm $w^2-A$. Child coordinates are obtained by multiplying $(w-m)+iz$ by $1+2i$, giving norm $5(w^2-B)$. At the stated label, apply the additional fixed child rotation $(5-12i)/13$, and take $t=11950641/13+868440n$. All five quantities are integer polynomials in $n$ and $w$ is always $26\bmod30$. The replay verifies the polynomial coefficients by exact interpolation, verifies both norm identities (degree at most eight, nine exact parameter values), and checks the residue for all parameter classes modulo 30. The leading term of $w$ makes the family unbounded.

The same slope fails on the infinite progression $d=236+306j$. For $r=39$, $39H=5^d-130093$, which vanishes modulo the inert prime $307$. Any rational $t$ giving integer $w$ must then be integral at $307$, since a pole of $rt^2$ would make its square dominate the numerator. Modulo 307 the numerator equals $(rt^2+r)(rt^2-r-4)$, so a solution needs $t^2=-1$ or $t^2=43/39$. Neither is a square there. This excludes the specific slope and does not address other slopes in this progression.

```python
from fractions import Fraction as F
from math import isqrt

r,t0,step=39,F(11950641,13),868440
A=5**8-131770
B,H=A-4,r+F(A,r)+4
m=H/2
def values(t):
    z=r*t*t-2
    w=(z*z+m*m+B)/H
    D=(r*r*t*t+A)/m
    P,Q=w-D,t*(D-r)
    U,V=w-m-2*z,2*(w-m)+z
    return w,P,Q,(5*U+12*V)/13,(-12*U+5*V)/13

# Interpolate degree at most four using differences in the binomial basis.
def coeff(v):
    out=[F(0)]*5
    basis=[F(1)]
    for j in range(5):
        for i,x in enumerate(basis): out[i]+=v[0]*x
        v=[y-x for x,y in zip(v,v[1:])]
        nxt=[F(0)]*(len(basis)+1)
        for i,x in enumerate(basis):
            nxt[i]-=x*j/(j+1)
            nxt[i+1]+=x/(j+1)
        basis=nxt
    return out
assert 5**2+12**2==13**2
assert values(t0)==(162601347230168296362836,162601347229783475650300,
    353758014185835429,362726082287753577807072,-25015591808042753481071)
grid=[values(t0+step*n) for n in range(9)]
assert all(c.denominator==1 for row in zip(*grid[:5]) for c in coeff(list(row)))
for w,P,Q,U,V in grid:
    assert P*P+Q*Q==w*w-A and U*U+V*V==5*(w*w-B)
assert all(values(t0+step*n)[0]%30==26 for n in range(30))
p=307
assert all(p%d for d in range(2,isqrt(p)+1))
assert pow(5,236,p)==130093%p and pow(5,306,p)==1
assert pow(43*pow(39,-1,p)%p,(p-1)//2,p)==p-1
```
