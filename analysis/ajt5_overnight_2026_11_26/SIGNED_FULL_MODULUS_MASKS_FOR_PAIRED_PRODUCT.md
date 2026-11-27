# Signed full-modulus masks for paired-product phase comparisons

This follows [the paired-product lift comparison](https://github.com/Samsen879/a303656/commit/26575f9c2ca06e032a2947555db77561d5840438). For a prime \(q\mid R\), put \(A=W^{LH}\), where \(L\) is prime to 7 and \(H\) kills the 7-part. If \(d=\operatorname{ord}_q(A)\), then \(d\mid q-1\), and the full \(R\) is congruent to its companion \(R/q\) modulo \(d\), even if \(q\) divides the companion. For a signed mask \(M=(R^h\pm1)_{7'}\), the local order is
\[
 \operatorname{ord}_q(A^M)=d/\gcd(d,R^h\pm1).
\]
Removing powers of 7 does not change the gcd with \(d\). The same mask is a unit on the 7-primary phase tag, so it can shorten the residual order without changing whether the corresponding lift is valid.

The original sharp boundary prime \(C=83464673905159\) has projected base-3 order \(42193\cdot73939\), out of range for the unmasked cutoff 44,100. The orders of \(R\) modulo those factors are 14,064 and 12,323, respectively. The minus mask with index 12,323 removes the second order factor; it yields an exact paired-product capture of \(C\) at 44,100, and every candidate tag lift fails the phase twist. The plus mask with index 7,032 removes the first order factor. Neither direct power gcd is nontrivial, but their composition gives exactly \(C\). The replay also regenerates every tag lift and certifies the known row via checked common annihilators. This is recertification, not an additional closed row. The choice of indices used the known local return periods; no discovery algorithm for unknown components is asserted.

One unconditional limitation of these masks: if a prime \(\ell\) divides the projected order and \(R\bmod\ell\) has odd multiplicative order \(h\), no plus mask touches that factor. A minus mask removes it only at multiples of \(h\). A finite product or lcm of masks at indices below \(h\) does not help. This general argument does not independently verify a claimed large native countercontrol lacking its full modulus/root inputs.

```python
from functools import cache
from math import gcd, lcm

R = 7320452716949759354345164426511787518233
F = [int(i % 49 == 0) for i in range(295)]
G = [0]*52
G[0] = G[12] = 1
G[1] = G[51] = -1
while G:
    while G and G[-1]%R == 0:
        G.pop()
    if not G:
        break
    v = pow(G[-1],-1,R)
    G = [g*v%R for g in G]
    d = len(G)-1
    for j in range(len(F)-1,d-1,-1):
        for i in range(d):
            F[j-d+i] = (F[j-d+i]-F[j]*G[i])%R
    F,G = G,F[:d]
assert len(F) == 2 and F[1] == 1
x = -F[0] % R
assert pow(x,343,R) == 1 and gcd(R,pow(x,49,R)-1) == 1

@cache
def canonical(a,b):
    P,Q = (0,a),(1,b)
    return min(((p[1-i]-p[i])*s%343,(q[1-j]-p[i])*s%343,d)
               for p,q in ((P,Q),(Q,P)) for i in (0,1) for j in (0,1)
               if (d := (q[j]-p[i])%343)%7 for s in (pow(d,-1,343),))

menu = set()
bands = [(17,{33,12,47},{39,11,46}), (24,{40,5,26},{46,4,25}),
         (38,{5,40,33},{11,39,32})]
for a in range(36,343,49):
    h = a+343*((-a)%6)
    g,f = pow(3,h,2401),pow(5,h,2401)
    inv = {pow(f,v,2401):v for v in range(343)}
    for start,left,right in bands:
        for u in range(start,343,49):
            delta = pow(g,u,2401)-pow(g,u+1,2401)
            for v in range((1-u)%7,343,7):
                w = inv[(pow(f,v,2401)+delta)%2401]
                if v%49 in left or w%49 in right:
                    continue
                for k in range(1,343):
                    if k%7:
                        b,c,d = canonical((k*v-u)%343,(k*w-u)%343)
                        if (b,c) == (12,51):
                            menu.add((pow(a*d,-1,343),k))
assert menu == {(E,66) for E in range(15,343,49)}

def free7(m):
    while m%7 == 0:
        m //= 7
    return m

L,H = free7(lcm(*range(1,20001))),7**R.bit_length()
m,n = free7(R**12323-1),free7(R**7032+1)
A = pow(3,L*H,R)
assert gcd(R,pow(A,m,R)-1) == gcd(R,pow(A,n,R)-1) == 1
C = gcd(R,pow(pow(A,m,R),n,R)-1)
assert C == 83464673905159
D = R//C
assert C*D == R and gcd(C,D) == 1
for d,M in ((C,L*m*n),(D,L*35882695707051169)):
    U,V = (pow(w,M,d) for w in (3,5))
    assert M%7 and pow(U,H,d) == pow(V,H,d) == 1
    for E,k in menu:
        assert gcd(d,U-pow(x,M*E%343,d),V-pow(x,M*E*k%343,d)) == 1

def support(a,T=44100):
    z,v=1,1
    for j in range(1,T+1):
        z=z*a%R
        if j%7:
            v=v*(z-1)%R
    d=gcd(R,v)
    while gcd(R,d*d)!=d:
        d=gcd(R,d*d)
    return d
assert support(A)==1
assert support(pow(A,m,R))==C
for E,k in menu:
    assert support(pow(3,L*m,R)*pow(x,(-L*m*E)%343,R)%R)==1
for p,t,fs in [(42193,14064,(2,3,293)),(73939,12323,(12323,))]:
    assert pow(R,t,p)==1
    assert all(t%f==0 and pow(R,t//f,p)!=1 for f in fs)
```
