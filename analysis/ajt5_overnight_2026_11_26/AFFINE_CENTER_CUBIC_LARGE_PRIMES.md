# Large determinant primes and the affine center cubic

Use the notation of [common-center redundancy](AFFINE_COMMON_CENTER_AND_ANGLE.md). Assume the four shifts are distinct with \(S_i\ll \sqrt X\), the positive weights are fixed, \(K\ne0\), and \(|h|\asymp X,\ X\le n\le2X\). Define \(m=Az_1+Bz_2=Cz_3+Dz_*\), \(p=B-A,\ q=C-D,\ H_1=W(S_2-S_1),H_2=W(S_3-S_*)\). The exact dot identities are \(2m\cdot u=H_1-pM,\ 2m\cdot v=H_2-qN\).

Let \(\ell\mid h\) be prime with \(\ell\ge X^\tau,\ \tau>1/2\). For sufficiently large \(X\) both \(u,v\) are nonzero modulo \(\ell\) since they are nonzero vectors of ordinary length \(O(\sqrt X)\). They are scalar multiples; if \(M\) or \(N\) vanished, both would, contradicting \(0<|K|\ll\sqrt X\). Thus \(v=ru\bmod\ell\) for \(r=F/M\) a unit, and \(M(\alpha-\delta r^2)=K\bmod\ell\). The center congruence is equivalent to
\[
 {\cal P}(r)=0\bmod\ell,\qquad
 {\cal P}(x)=(H_2-xH_1)(\alpha-\delta x^2)+K(px-qx^2).
\]
This is the same condition for the two cross pairs; it is not two modular tests. In the complete modular population there are \(\ell-\chi_\ell(-1)\) choices of \(u\) for each allowed \(r\) (the split norm is a product; the inert norm is onto with fibers of size \(\ell+1\)). The conditional fraction that passes is at most \(3/(\ell-3)\), using the at most two excluded roots of \(\alpha-\delta r^2\). This does not give an averaging statement for actual lattice chords.

## Reducible cubics

If \({\cal P}\) is reducible over \(\mathbb Q\), and \(3/4<\tau<1\), the number of distinct targets satisfying the above assumptions is
\[
 O_\epsilon(X^{\max(5/2-2\tau,\ 3/4)+\epsilon}).
\]
The coefficients of the primitive factors are \(O(\sqrt X)\) by the [bounded-degree factor height bound](https://link.springer.com/article/10.1007/s10817-019-09526-y#Sec7); the content of \({\cal P}\) cannot be divisible by the larger prime. As \(H_1\ne0\), it is a cubic. Its root \(r\) is then a root of a linear or quadratic factor; multiplying a linear factor by \(x\) if necessary gives \(a x^2+b x+c\), \(a\ne0\), of height at most \(H=O(\sqrt X)\). Since \(r^2M=N,\ rM=F\bmod\ell\), this implies \(\ell\mid aN+bF+cM\). Count the two integer quotients \(k=h/\ell,\ j=(aN+bF+cM)/\ell\): there are \(O(HX^{2-2\tau})\) pairs. Set \(\lambda=j/k\), \(T=a\alpha/\delta+c\). Combining \(bF-\lambda h=-TM+aK/\delta\) with the Gram identity gives
\[
 (\lambda F+bh)^2=(b^2+\lambda^2)M(\alpha M-K)/\delta-(TM-aK/\delta)^2 .
\]
If \(b=\lambda=0\), the linear identity fixes \(M\) or is impossible. Otherwise for a genuine quadratic with nonzero discriminant, clearing denominators and counting divisors and quadratic-field unit orbits gives \(X^{o(1)}\) solutions in the polynomial-height box, as in [cross-pair collisions](AFFINE_CROSS_PAIR_COLLISIONS.md). The constant term is strictly negative, so a genuine quadratic with zero discriminant has negative leading coefficient and yields at most one solution.

The zero-quadratic-coefficient case has at most two rational values of \(\lambda\), satisfying \(\lambda^2=(a\alpha+c\delta)^2/(\alpha\delta)-b^2\); their denominators are bounded in terms of the fixed weights. Count these cases once per factor rather than once per pair of quotients. Clearing fixed denominators gives \(Y^2=B_0M-C_0^2\) with \(0<B_0=O(H^2\sqrt X)\) necessary. By prime-power valuation and CRT, \(Y^2=-C_0^2\bmod B_0\) has at most \(B_0^{1/2+o(1)}\) residue classes. Counting \(Y=O(\sqrt{B_0 X})\) gives \(O_\epsilon(X^\epsilon(\sqrt X+HX^{1/4}))\) options. Each allowed \(M,\lambda\) yields at most two Gram tuples. The Gram data determine the squared length of the common center from its two dot products, hence determine \(n\). Finally sum over \(O((\log X)^8)\) labels. In particular, when the relevant factor heights are uniformly bounded, the proof gives exponent \(\max(2-2\tau,1/2)\) for \(\tau>1/2\).

## Finite controls

The first certificate has primitive cubic \((3x-2)(8x^2+50x+25)\); reversing only its first chord keeps the unsigned Gram data but fails the modular center constraint. The second has a primitive cubic irreducible already modulo 11 and a large determinant prime at which its realized center passes. Irreducible cubics are outside the count above. None of the bounds asserts anything about all representations in the original conjecture.

~~~python
from math import gcd, isqrt

def check(n, w, labels, z, ell):
    A,B,C,D = w
    S = [3**c+5**d for c,d in labels]
    a,b,c,e = S
    assert len(set(S)) == 4 and max(S)**2 <= n
    assert [x*x+y*y+s for (x,y),s in zip(z,S)] == [n]*4
    assert all(A*x+B*y == C*v+D*t for x,y,v,t in zip(*z))
    assert len({0,(A*A-D*D)*(a-e),(C*C-B*B)*(c-b)}) == 3
    assert len({0,(B*B-D*D)*(b-e),(C*C-A*A)*(c-a)}) == 3
    x,y = (z[0][i]-z[1][i] for i in range(2))
    v,t = (z[3][i]-z[2][i] for i in range(2))
    M,N,F,h = x*x+y*y,v*v+t*t,x*v+y*t,x*t-y*v
    assert gcd(M,N)==2 and 4*min(abs(F),abs(h))>=n
    assert h%ell==0 and ell**4>n**3
    assert all(ell%j for j in range(2,isqrt(ell)+1))
    W=A+B
    K=W*(D*e+C*c-A*a-B*b)
    H1,H2=W*(b-a),W*(c-e)
    assert A*B*M-C*D*N==K and M*N==F*F+h*h
    G=M*(H2-(C-D)*N)
    L=F*(H1-(B-A)*M)
    assert (G-L)%ell==0
    return F*pow(M,-1,ell)%ell, (G+L)%ell

r,bad = check(22543,(5,5,4,6),[(2,1),(2,2),(4,1),(0,3)],
              [(127,80),(-147,30),(-139,-56),(76,129)],1997)
assert (r,bad)==(1801,956) and (8*r*r+50*r+25)%1997==0
r,_ = check(61339,(1,6,5,2),[(0,1),(2,3),(0,3),(4,1)],
            [(247,-18),(-206,137),(-117,218),(-202,-143)],6311)
P = lambda x: 160*x**3-47*x*x-101*x+30
assert r==2201 and P(r)%6311==0 and all(P(j)%11 for j in range(11))

~~~
