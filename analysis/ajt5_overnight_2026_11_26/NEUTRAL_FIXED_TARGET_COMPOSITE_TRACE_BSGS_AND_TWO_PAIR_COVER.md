# Exact fixed-target trace search over a composite, and a two-pair control

Write \(C_0(t)=2,\ C_1(t)=t,\ C_{n+1}(t)=tC_n(t)-C_{n-1}(t)\). In the neutral source with \(z=x^{172}\), fix a target \(c=C_b(2/z)\). We want the full prime-power support in \(M\) of primes \(p\mid M\) such that \(c^2\ne4\bmod p\) and \(C_a(2z)=c\bmod p\) for at least one \(1\le a\le H\). This is a **fixed target** method; it does not select \(b\) on the unresolved chart.

For \(x=C_j(t),y=C_i(t)\), the identity
\[
x^2-cyx+c^2+y^2-4=(c-C_{j+i}(t))(c-C_{j-i}(t))
\]
holds as a polynomial identity, by expanding \(t=u+u^{-1}\) and \(C_n(t)=u^n+u^{-n}\). Put \(s=\lfloor\sqrt H\rfloor+1\). Build the monic product in \(X\) of the displayed quadratics with \(y=C_i(t)\) for \(0\le i\le s\); evaluate at \(X=C_{(2k+1)s}(t)\) for \(0\le k<\lfloor H/(2s)\rfloor\). The exponents in these blocks cover the range up to \(2s\lfloor H/(2s)\rfloor\), including 0 (which only hits the discarded \(c=2\bmod p\) support). Check the tail directly. For \(F\) the product of all values and \(e=\operatorname{bitlength}(M)\), compute \(d=\gcd(M,F^e)\) and return \(d/\gcd(d,(c^2-4)^e)\). This saturates the full prime-power support even when a match is not valid modulo the full prime power.

Product and multipoint remainder trees give \(\widetilde O(\sqrt H)\) ring operations using quasi-linear polynomial multiplication. The remainder tree only divides by monic polynomials, with reversed divisor unit constant 1, so no inversion of a nonunit in the composite ring is necessary. The direct replay below deliberately uses the transparent block product and recurrence instead.

For the two-pair statement, at each residue field choose roots \(U,V\) of the norm-one trace polynomials with traces \(2z,2/z\). For instance in an algebraic closure put \(h^2=z^2-1,\ U=z+h,\ V=(1+ih)/z\), with \(i^2=-1\). Then the two product-pair traces are \(2\pm2i(z-z^{-1})\). For each odd prime \(\ell\) with at least one nonzero primary depth, if the depths of \(U,V\) are equal and positive, the original pair shares a nonzero \(\ell\) component. If they are unequal, the product and quotient both retain the larger depth. For the actual unresolved \((17,188)\), removing the entire 2-primary part of the four units by the exponent \(2^{\operatorname{bitlength}(M+1)}\) leaves each nontrivial on every prime support, as verified by the four trace norm gcds below. This power of 2 dominates the 2-primary part since each \(U\) and \(V\) has order dividing \(p-1\) or \(p+1\) over the field of definition of its base-field trace; the same bound on the 2-primary part carries over to products. Coverage by the two pairs does **not** distinguish the sign side: the exact mixed-chart inert control below has a genuine, nondegenerate composite-pair collision. A specific odd primary component of both original units being nontrivial would be stronger than the mere two-pair coverage.

~~~python
from math import gcd,isqrt

def trace(t,n,M):
    def mul(u,v):
        return ((u[0]*v[0]-u[1]*v[1])%M,(u[0]*v[1]+u[1]*v[0])%M)
    def sub(u,v):
        return ((u[0]-v[0])%M,(u[1]-v[1])%M)
    a,b=(2,0),t
    for bit in bin(n)[2:]:
        c=sub(mul(a,b),t)
        a,b=(sub(mul(a,a),(2,0)),c) if bit=='0' else (c,sub(mul(b,b),(2,0)))
    return a

def block(M,t,c,H):
    s=isqrt(H)+1
    k=H//(2*s)
    ys=[trace((t,0),i,M)[0] for i in range(s+1)]
    D=1
    for j in range(k):
        x=trace((t,0),(2*j+1)*s,M)[0]
        for y in ys:
            D=D*(x*x-c*y*x+c*c+y*y-4)%M
    for a in range(2*s*k+1,H+1):
        D=D*(trace((t,0),a,M)[0]-c)%M
    e=M.bit_length()
    d=gcd(M,pow(D,e,M))
    return d//gcd(d,pow(c*c-4,e,d))

M,x=169969064866856199529458159287,68693850624006015651041237082
z=pow(x,172,M); iz=pow(z,-1,M)
c=trace((2*iz,0),379680,M)[0]
p=block(M,2*z,c,2**19)
assert p==421761845597 and M%p==0
q=M//p
assert q==402997726421332771
c=trace((2*iz,0),(q+1)//2,M)[0]
assert c%q==q-2 and block(M,2*z,c,2**19)==1
B=2*(z-iz)%M
a,b=trace((2,B),q,M)
assert gcd(M,(a-2)**2+(b+B)**2)==q and gcd(q,B*(16+B*B))==1
assert block(45,6,12,1)==9

R=626751537547263614426465772417729978972491
z=pow(252568635021313874012910903862214825457075,172,R)
iz=pow(z,-1,R)
assert pow(z,33,R)==(z+1)%R
J=1<<(R+1).bit_length()
for t in [(2*z,0),(2*iz,0),(2,2*(z-iz)),(2,-2*(z-iz))]:
    a,b=trace(t,J,R)
    assert gcd(R,(a-2)**2+b*b)==1
~~~

The fixed target \(b=379680\) came from the already known mixed positive control, not a new selector. The obstruction in \((17,188)\) remains to find a bounded nondegenerate original-pair match or a common odd-primary certificate strong enough to distinguish the sign side.
