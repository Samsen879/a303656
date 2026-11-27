# Portable lattice and orientation-sieve inputs for simultaneous quadratic norms

For the integral norm form $Q(a,b)=a^2+tab+ub^2$ of an imaginary quadratic maximal order, put $G=\left(\begin{smallmatrix}2&t\\t&2u\end{smallmatrix}\right)$. The difference of two norms has the identity
$$
 2(Q(S)-Q(V))=(S-V)^tG(S+V).
$$
Consequently a finite simultaneous-norm seed gives congruence conditions on an ordinary dot-product equation, regardless of the class number.

More explicitly, for a nonzero seed difference $\Delta_0=S_0-V_0$ set $c=\gcd((G\Delta_0)_1,(G\Delta_0)_2)$, $A_0=G\Delta_0/c$ and $w_0=S_0+V_0$. Let $L=2F\det G$, with $F$ a fixed integer modulus for the coordinates. If $H\equiv Q(S_0)-Q(V_0)\bmod cF\det G$, any integer solution to
$$
 A\cdot w=2H/c,\qquad (A,w)\equiv(A_0,w_0)\pmod L
$$
gives $\Delta=cG^{-1}A$, $V=(w-\Delta)/2$, $S=(w+\Delta)/2$. All recovered coordinates are integral and keep their seed classes modulo $F$, since $\Delta-\Delta_0$ and $w-w_0$ are multiples of $2F$. The resulting difference of norms is exactly $H$. If $Q(\beta)=B$, $B\mid F$, and $V_0=\beta U_0$, this also gives integral $U=V/\beta$ by $1/\beta=\bar\beta/B$. This is a congruence-preserving reduction, not a lower bound on the number of solutions in a given region.

At a split odd prime away from the fixed moduli and discriminant, the single-orientation deletion density on primitive solutions modulo $p$ is $(1+1_{p\mid H})/(p+1)$, as in the Gaussian case. To see this, write the split norm in linear coordinates as a nonzero constant times the product of the two coordinates; either factor line is orthogonal to itself. The primitive parameter means $\Delta\ne0$ modulo $p$, giving $p(p^2-1)$ total solutions. Deletion on one line counts $p(p-1)$ if $H\ne0\bmod p$, doubled if $H=0\bmod p$. If both lines are deleted, subtract their intersection $V=0$; there are respectively $p-1,2(p-1)$ choices of $\Delta$ at that intersection. This gives the two-orientation density $(2p-1)(1+1_{p\mid H})/[p(p+1)]$. The finite calculation is independent of the class number.

The replay verifies three seeds: $(3,5)$ Gaussian with first numerical root 4, and $(7,37)$ in both Eisenstein and discriminant $-7$ norms with first numerical root 8. In all three, the only earlier distinct numerical root is 2 and its exact odd inert valuation verifies its failure. The two non-Gaussian seeds occur at different integers. The replay also verifies the frozen period condition and the two orientation counts. These are portable algebraic/sieve inputs; no joint distribution estimate or all-integer coverage follows from the controls alone.

```python
from math import gcd

rows = [
    (0,1,5,3,4,4,7,4900,168,(1,-2),(-1,-1),(-3,1),(-6,2)),
    (-1,1,37,7,12,8,5,205350,20,(-3,-7),(-7,2),(35,57),(-72,-35)),
    (1,2,37,7,12,8,5,958300,420,(-1,-4),(-1,1),(9,-1),(-38,20)),
]
for t,u,B,C,r,T,p,F,P,beta,U,V,S in rows:
    def Q(z):
        a,b = z
        return a*a+t*a*b+u*b*b
    a,b = beta
    k,l = U
    assert Q(beta)==B and V==(a*k-u*b*l,a*l+b*k+t*b*l)
    m = B+1+Q(U)
    x = B*m+r
    assert C*C==B+r and x==T+Q(S)==B*B+C*C+Q(V)
    assert (x-2)%p==0 and (x-2)%(p*p)!=0
    assert all((j*j-t*j+u)%p for j in range(p))
    a,b = S[0]-V[0],S[1]-V[1]
    c = gcd(2*a+t*b,t*a+2*u*b)
    L = c*F*(4*u-t*t)
    R = L
    while gcd(B,R)>1:
        R //= gcd(B,R)
    assert B*B%(L//R)==0 and pow(B,P,R)==1
    assert all(pow(B,j,R)!=1 for j in range(1,P))
    print(m,x,Q(U),Q(V),Q(S),P)

for t,u,p,lam in [(0,1,13,5),(-1,1,7,2),(1,2,11,5)]:
    def Q(a,b):
        return a*a+t*a*b+u*b*b
    for H in (0,1):
        total = one = both = 0
        for a in range(p):
            for b in range(p):
                if (a,b)==(0,0):
                    continue
                for x in range(p):
                    for y in range(p):
                        if (Q(x+a,y+b)-Q(x,y)-H)%p:
                            continue
                        L = (x+lam*y)%p==0
                        R = (x+(t-lam)*y)%p==0
                        total += 1
                        one += L
                        both += L or R
        k = 1+int(H==0)
        assert (total,one,both)==(p*(p*p-1),k*p*(p-1),k*(p-1)*(2*p-1))
```
