# Semiprime, bounded-factor squarefree, and prime-square denominator sectors

This continues [the prime-denominator large-gap bound](https://github.com/Samsen879/a303656/commit/50dea4525bdd73b510f5926048cfea6dadb34a63). The additional sectors preserve the true Gaussian critical band and are still strictly within-label. Larger denominators remain unresolved. The embedded native rotations, matched failed band rotation, and both factored primality certificates were independently replayed.

In the angular sieve with \(J\) fixed, the marked product of primes at most \(z=L^{1/(10J)}\) contains at most \(J-1\) primes, with at most \(2^{J-1}\) root classes per product. The progression has length \(\gg L/z^{J-1}\); the combined remainder over marked products is \(O_J(z^{J+1}\log^5 L)\) for each transverse coordinate, negligible compared with the required \(L/\log L\) scale. In the prime-square case the shared-depth branch with \(p\mid D\) must be kept: its per-rotation Fourier error has weight \(O(p^3)\), but there are only \(O(K)\) such primes per label. The \(p\nmid D\) branch has weight \(O(p^2)\) summed over all \(p\le X^{1/32}\). Both error sums are \(X^{3/32+o(1)}\) times the common \(X^{25/32+\epsilon}\) factor from completion, yielding the stated \(X^{7/8+\epsilon}\).

The large-gap saving extends to **squarefree semiprime denominator norms** and to prime-square norms. For \(X=2^K\), count unordered pairs of distinct certificates at the same \(n\in[X,2X)\) whose reduced Gaussian quotient has denominator norm \(m\le X^{1/16}\). The bounds are
\[
\begin{array}{c|c}
m&\text{number of pairs}\\ \hline
p_1p_2,\quad p_1\ne p_2&
 O_\epsilon\!\left(X(\log K)^3/K^2+X^{29/32+\epsilon}\right)\\
p^2&
 O_\epsilon\!\left(X/K+X^{7/8+\epsilon}\right).
\end{array}
\]
These are genuine large gaps: every pair in the counted sectors has \(|q'-q|\gg X^{31/32}/K\). Both sectors are within-label. The squarefree argument also works for any fixed bound \(J\) on the number of prime factors, with \((\log K)^{J+1}\) in the main bound.

### Squarefree CRT and the angular saving

Write \(Z=S+D-q+2iw\), with \(N(Z)=SR\). At one label, \(Z'/Z=\nu/\gamma\) has norm one. In lowest terms, \(\nu\) is a unit times \(\bar\gamma\), so \(\gamma\mid Z\). The band confines \(\arg Z\asymp K^{-1}\) to an interval of width \(O(K^{-2})\). Thus \(\gamma\) lies within angular distance \(O(K^{-2})\) of an axis or diagonal. A reduced odd denominator of norm greater than one lies off those lines. Its nonzero transverse lattice coordinate gives angular displacement \(\gg m^{-1/2}\), hence the stated \(q\)-gap.

As in the prime case, factor \(D+2iw=\alpha\beta\) with \(N(\alpha)=q\). This uses the numerical norm condition on \(q\) and \(q\mid D^2+4w^2\). Write
\[
\alpha=f(a+ib),\quad \beta=c+id,\quad
f\mid D,\quad (a,b)=1,\quad ac-bd=D/f.
\]
Choose an associate with \(a\ge |b|\). For \(Y=\sqrt X/K\), we have \(a\asymp Y/f\). The exact critical band gives \(2w/q=8\sqrt2K+O(1)\), so \(d\) ranges over an interval of length \(O(fa)\). The extra condition is
\[
\gamma\mid 2Z=(\beta-\bar\alpha)(\bar\beta+\alpha).
\tag{1}
\]

The essential CRT step is to **partition by \(\delta=(a,m)\)**. At each \(p\mid m/\delta\), substitute \(c=(D/f+bd)/a\) modulo the chosen Gaussian prime. Each factor in (1) is linear in \(d\) for fixed \(b\). Its coefficient vanishes at at most one \(b\bmod p\), so the union gives at most \(4p\) residue pairs. CRT gives at most \(4^Jm/\delta\) pairs modulo \(m/\delta\). At the primes dividing \(\delta\), drop the test in (1) and charge the spacing of the \(a\)'s, which are multiples of \(\delta\). This recovers the full factor \(1/m\) in the principal bound, even if a denominator prime divides \(D\).

For completeness, when the progression step \(m/\delta\) is coprime to \(a\), complete \(bd\equiv-D/f\bmod a\) on each residue pair. The principal term is \(O(fa/(m/\delta)^2)\). The error is \(O_\epsilon(fa^{1/2+\epsilon}\sqrt{D/f})\). In the complete-sum bound, factor
\[
(r,sD/f,a)^{1/2}
\le (D/f,a)^{1/2}(r,s,a)^{1/2}.
\]
For frequencies constrained to multiples of \(v\mid a\), the nonzero Fourier \(L^1\) norm of either interval progression is \(O((a/v)\log a)\). Separating the two-zero principal term gives the stated error by summing over \(v\mid a\). Summing over \(a\) and \(f\mid D\), the count for a fixed label and denominator is therefore
\[
\ll_{J,\epsilon}\frac{Y^2\log K}{m}+mX^{25/32+\epsilon}.
\tag{2}
\]
Each fixed rotation determines at most one partner for each certificate. [Estermann, *On Kloosterman’s sum*](https://www.cambridge.org/core/journals/mathematika/article/abs/on-kloostermans-sum/DED1120FD0994F590EA6E980D07D0F43).

The angular sum for squarefree \(m\) with \(\omega(m)\le J\) is
\[
\sum_\gamma \frac1{N(\gamma)}\ll_J\frac{(\log K)^J}{K^2}.
\]
In a dyadic annulus of radius \(L\), the nonzero transverse coordinate \(h\) has \(O(L/K^2)\) choices. For fixed \(h\), the norm polynomial along the strip is \(u^2+h^2\) or \(u^2+(u-h)^2\). Mark the product \(d_0\) of its prime factors up to \(z=L^{1/(10J)}\). There are at most \(J-1\) marked factors because the norm is \(\asymp L^2\). In each root class modulo \(d_0\), sieve the remaining split primes up to \(z\). The Selberg upper bound is
\[
\ll_J \frac{L}{d_0\log L}
 \prod_{\ell\mid h,\ \ell\equiv1(4)}\frac{\ell-1}{\ell-2}
 +O_J(z^2\log^5 L).
\]
The local root counts are two when \(\ell\nmid h\) and one otherwise. The error follows by expanding the square weights and summing \(6^{\omega(d)}\) for \(d\le z^2\). Summing \(1/d_0\) costs \(O_J((1+\log\log L)^{J-1})\), and the product over \(\ell\mid h\) has bounded mean. Summing the annuli starting at \(L\gg K^2\) gives the displayed angular sum. Applying it to (2) over \(O(K^2)\) labels proves the squarefree bound. [Williams, *Mertens’ theorem for arithmetic progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf).

### Prime squares and cross-label pairs

For \(m=p^2\), the squarefree partition alone loses a factor \(p\) when \(p\mid a\). Use the shear \(a_1=a+\ell b,\ d_1=d+\ell c\), taking \(\ell=0\) when \(p\nmid a\) and \(\ell=\operatorname{sgn}(b)\) otherwise. Then \(p\nmid a_1\), \(a_1c-bd_1=D/f\), and the interval for \(d_1\) still has length \(O(fa_1)\).

Modulo the Gaussian prime square, the two linear factors in (1) have coefficients \(b+\iota a\) and \(b-\iota a\) after multiplication by \(a_1\). If \(p\nmid D\), the factors cannot both vanish modulo \(p\), since that would force \(2D=\alpha\beta+\bar\alpha\bar\beta\equiv0\). A zero slope modulo \(p\) makes that factor incompatible with the determinant equation. Thus there are \(O(p^2)\) residue pairs modulo \(p^2\). If \(p\mid D\), both factors can vanish modulo \(p\) and share the required depth. There are \(O(p^3)\) pairs: outside at most two exceptional \(b\)-classes modulo \(p\), the two slopes are units and the common-root case contributes at most \(p\) lifts per \(b\bmod p^2\).

The angular condition forces \(p\gg K^2\). For \(p\nmid D\), sum the principal weights \(1/p^2\). For \(p\mid D\), sum \(1/p\) over at most \(O(K/\log K)\) eligible prime divisors of \(D\). The latter gives \(O(X/K)\) after summing labels. The completion errors are \(O_\epsilon(X^{7/8+\epsilon})\).

Cross-label pairs stay outside both sectors. Their two circle norms have gcd \(O(X^{1/4})\), by the product of the four nonzero differences between the shifts \(3A+5B,A+B\) at the two labels. Their reduced denominator norms are therefore \(\gg X^{7/4}\). Larger denominators, unbounded numbers of squarefree factors, and nonsquarefree norms beyond prime squares remain outside these estimates.

### Standalone exact replay

This verifies a legal squarefree pair with denominator norm \(2073600725760063505\) and a 1159-bit \(q\)-gap. Its dominant Gaussian coordinate has gcd **5** with the denominator norm, so the exceptional CRT branch occurs in a genuine collision. At the same target, the norm-65 rotation solves the certificate equation and fails the band. The final check gives a legal prime-square pair.

```python
from math import gcd, isqrt, prod

def prime(n, factors, w):
    assert prod(factors) == n-1
    assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in factors)
    assert pow(w,n-1,n)==1
    assert all(gcd(pow(w,(n-1)//p,n)-1,n)==1 for p in set(factors))

def crt(x,m,y,n):
    g=gcd(m,n)
    assert (y-x)%g==0
    q=n//g
    return (x+m*((y-x)//g*pow(m//g,-1,q)%q))%(m*q),m*q

def case(k,r,a,rots,inside):
    A,B=9**r,25**r
    D=A+2*B
    C=D-(a*a+1)//2
    u,m=0,2
    for G,H in rots:
        z=G*G+H*H
        i=-G*pow(H,-1,z)%z
        assert (i*i+1)%z==0
        u,m=crt(u,m,-C*pow(a+i,-1,z)%z,z)
    lo=(9*(1<<(k//2)))//(8*a)
    u=lo+(u-lo)%m
    x,y=a*u+C,u
    v,t=x+1,a-u
    S=x*x+y*y
    n=S+3*A+5*B
    assert S.bit_length()-1==n.bit_length()-1==k
    assert A<=B and B**16<=n<=A**32 and v*v+t*t==S+2*D

    def cert(x,y):
        f,g=x-v,y-t
        assert f%2 and g%2
        q=((f+g)//2)**2+((f-g)//2)**2
        Y=y*v-x*t
        assert q%2 and Y>0 and Y%2==0
        assert 2*q*S==(D-q)**2+Y*Y
        return q,S+D-q,Y

    def band(q): return 64*k*k*q<=S<=64*k*(k+1)*q
    q,X,Y=cert(x,y)
    assert band(q)
    for (G,H),good in zip(rots,inside):
        z=G*G+H*H
        assert gcd(G,H)==1 and z%2 and z**16<=1<<k
        c,e=(G*x+H*y)//z,(G*y-H*x)//z
        assert (G*c-H*e,H*c+G*e)==(x,y)
        Q,U,V=cert(G*c+H*e,G*e-H*c)
        assert (G*U-H*V,H*U+G*V)==(G*X+H*Y,G*Y-H*X)
        assert band(Q)==good
        if good: assert abs(Q-q)**100>1<<(49*k)

    aa,bb=(2*u-a+1)//2,(2*u-a-1)//2
    assert aa>=abs(bb) and gcd(aa,bb)==1 and aa*aa+bb*bb==q
    c,j=divmod(aa*D+bb*Y,q)
    d,l=divmod(aa*Y-bb*D,q)
    assert j==l==0 and aa*c-bb*d==D
    return aa,D

N=1440000252
m=N*N+1
prime(m//5,(2,2,5,5,7,11,13,43,217457,443077),2)
aa,D=case(1200,12,13581,[(N,1),(-8,1)],[True,False])
assert gcd(aa,m)==5

N=1440000070
p=N*N+1
prime(p,(2,5,149,373,2591)*2,3)
_,D=case(2400,24,27155,[(N*N-1,2*N)],[True])
assert D%p
```
