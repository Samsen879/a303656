# A common free gap need not be the prescribed gap

The pairwise screen in [COMMON_QUOTIENT_STRATUM_COMPATIBILITY.md](COMMON_QUOTIENT_STRATUM_COMPATIBILITY.md) has a concrete failure even after the strict product, individual norm, and rough-part gcd tests. An interval argument specifies precisely how much extra congruence would remove this type of false compatibility.

## Setup and anchoring lemma

Use the actual labels \((0,13),(18,0)\). Write \(X=3^{18}\), \(Z=5^{13}\), so the shifts are \(X+1,Z+1\), with prescribed gap \(\Delta=Z-X=833282636\). In a row with scales \(S,D\) and rough parts \(u,w\in[L,U-1]\), the two independently proposed targets are \(Z+1+Su\) and \(X+1+Dw\). They coincide exactly when the free gap \(\xi=Dw-Su\) equals \(\Delta\).

The one-sided marginal windows require \((Dw-\Delta)/S\) and \((\Delta+Su)/D\) to be in the closed interval \([L,U-1]\), without requiring these reconstructions to be integral. Subtracting \(u,w\) respectively gives
\[
 |\xi-\Delta|\ \le\ (U-L-1)\min(S,D).
\]
If an anchor row's admissible gaps are required to be congruent to \(\Delta\bmod M\), with \(M>(U-L-1)\min(S,D)\), each remaining gap of that row is the prescribed one. Compatibility of each other row with that anchor then certifies that all rows admit the prescribed gap. This need not give one shared target across different rows, and the congruence is a hypothesis, not a consequence of local norm tests.

## Verified controls

For \(Y=127,\ [L,U)=[18209,24613),\ D=9\cdot71^2\), take rows \(S=109\) and \(S=109^2\). Their admissible free-gap sets intersect at exactly \(833253788=\Delta-28848\), with respective rough pairs \((19501,18413)\) and \((18493,23209)\). The pairs obey the common positive-target interval and strict product window, have coprime rough parts, and each of the four residuals is a true norm. Neither row admits the prescribed gap.

For \(Y=109,\ [L,U)=[16637,20989)\), use \(S=81\cdot109,\ D=25\cdot47^2\). The window width \(U-L-1=4351\) is less than \(109^2\), so taking \(M=S\cdot109^2\) suffices for this row. One extra factor of 109 does not: modulo \(S\cdot109\) both the true correction \((19141,18149)\) and the false correction \((18269,18149)\) are compatible. The pair at the true gap shares target \(1389699015\).

```python
from math import gcd, isqrt
X,Z=3**18,5**13
de=Z-X

def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

def norm(r):
    return any(isqrt(r-a*a)**2==r-a*a for a in range(isqrt(r)+1))

def row(Y,L,U,S,D):
    ps=[p for p in range(2,Y+1) if prime(p)]
    rr=[r for r in range(L,U)
        if r%4==1 and all(r%p for p in ps) and norm(r)]
    ok=lambda n:max(X,Z)+1<n<X+Z
    aa=[u for u in rr if ok(Z+1+S*u) and D*L<=de+S*u<=D*(U-1)]
    bb=[w for w in rr if ok(X+1+D*w) and S*L<=D*w-de<=S*(U-1)]
    out={}
    for u in aa:
        for w in bb:
            if gcd(u,w)==1 and u*w<L*U:
                out.setdefault(D*w-S*u, []).append((u,w))
    return out

D=9*71**2
assert all(norm(z) for z in (109,109**2,D))
a=row(127,18209,24613,109,D)
b=row(127,18209,24613,109**2,D)
assert a.keys() & b.keys()=={833253788}
assert de not in a and de not in b
assert a[833253788]==[(19501,18413)] and b[833253788]==[(18493,23209)]

S,D=81*109,25*47**2
assert norm(S) and norm(D)
z=row(109,16637,20989,S,D)
assert {h for h in z if (h-de)%(109*S)==0}=={de,840981524}
assert {h for h in z if (h-de)%(109**2*S)==0}=={de}
assert z[de]==[(19141,18149)] and z[840981524]==[(18269,18149)]
assert Z+1+S*19141==X+1+D*18149==1389699015
```
