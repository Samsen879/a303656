# A prime-denominator large-gap sector of the Gaussian critical band

This extends [the close-gap analysis](https://github.com/Samsen879/a303656/commit/6cd48df876a075c1c66da7f785abe5070dbf694a) for the fixed \(t=8\) band. The result bounds one genuinely large-gap same-label sector; it is not an estimate for the entire collision second moment. For distinct labels, the denominator separation follows just from the two genuine powers and the resulting shifts, with no prime-denominator assumption.

In the completion step below, the residues modulo \(p\) specify two arithmetic progressions of step \(p\). For \(p\nmid a\), the step is coprime to the completion modulus \(a\). For the interval Fourier transform along that progression, the total absolute mass on nonzero frequencies divisible by \(v\mid a\) is \(O((a/v)\log(2a))\), by the geometric-sum bound on the reduced frequency circle. Its zero coefficient is instead the progression length. In the Weil bound, isolate the two-zero term and majorize the gcd factor on the rest by \(\sqrt{(D/f,a)}\sum_{v\mid(r,s,a)}\sqrt v\). At least one frequency is nonzero; using the preceding Fourier bound for it and the (O(fa)) zero-coefficient bound for the other gives \(O(f a^{1/2+o(1)}\sqrt{D/f})\) after summing over \(v\). This works even if the longer interval exceeds a full copy of modulus \(a\); full copies contribute only at zero frequency. The cited sources supply standard sieve product and complete-sum bounds, not the present certificate-specific conclusion.

For \(X=2^K\), count unordered pairs of distinct certificates at the same \(n\in[X,2X)\) whose reduced Gaussian quotient has denominator of **odd prime norm \(p\le X^{1/16}\)**. Their total number is
\[
\boxed{\displaystyle
\ll_\epsilon \frac{X(\log K)^2}{K^2}+X^{29/32+\epsilon}.}
\]
Every pair in this sector has \(|q'-q|\gg X^{31/32}/K\). Cross-label pairs cannot occur in it. The estimate leaves composite denominator norms and larger prime denominator norms untreated.

### Angle restriction and counting

Write \(Z=S+D-q+2iw\), so \(N(Z)=SR\). For a same-label pair, \(Z'/Z\) has norm one. If its reduced denominator is \(\gamma\) of odd prime norm \(p\), its numerator is a unit times \(\bar\gamma\).

The critical band puts \(\arg Z\asymp K^{-1}\) in an interval of width \(O(K^{-2})\). Indeed, the \(q\)-interval has width \(O(X/K^3)\), and \(d(\arg Z)/dq=1/(2w)\asymp K/X\). Consequently \(\gamma\) lies in a strip of angular width \(O(K^{-2})\) about an axis or diagonal. It cannot lie on the line itself, since its norm is an odd prime. The nonzero transverse lattice coordinate also gives \(|\arg Z'-\arg Z|\gg p^{-1/2}\), which proves the large-gap assertion.

The prime norms in those strips satisfy
\[
\sum_{\gamma}\frac1{N(\gamma)}\ll\frac{\log K}{K^2}.
\tag{1}
\]
To see this, work in a dyadic annulus of radius \(L\). The transverse integer \(b\) has \(0<|b|\ll L/K^2\). For fixed \(b\), the longitudinal coordinate runs through \(O(L)\) integers, with norm polynomial \(u^2+b^2\) or \(u^2+(u-b)^2\). A split sieving prime has two roots if it does not divide \(b\), and one if it does. The Selberg upper sieve with weights supported on divisors up to \(L^{1/10}\) gives
\[
\ll \frac{L}{\log L}
       \prod_{\ell\mid b,\ \ell\equiv1(4)}
       \frac{\ell-1}{\ell-2}.
\]
Here the remainder is \(O(L^{1/5}\log^5 L)\), from at most \(2^{\omega(d)}\) roots and \(3^{\omega(d)}\) coefficient multiplicity at an expanded divisor \(d\). The displayed product has bounded mean over \(b\), by expanding it and summing the convergent product with factors \(1+1/(\ell(\ell-2))\). Thus each annulus contributes \(O(1/(K^2\log L))\) to (1). Summing from \(L\gg K^2\) proves (1). [Williams, *Mertens’ theorem for arithmetic progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf).

For the count at one label and one \(\gamma\), use the numerical norm condition on \(q\) and \(q\mid D^2+4w^2\). Gaussian factorization gives \(D+2iw=\alpha\beta\) with \(N(\alpha)=q\). At a split prime, allocate the factors between its two Gaussian primes. At an inert prime, the exponent in \(q\) is even, and the corresponding rational prime power divides \(D+2iw\).

Put \(\alpha=f(a+ib)\), with \(\gcd(a,b)=1\) and \(a\ge|b|\), and write \(\beta=c+id\). Then \(f\mid D\), and, with \(Y=\sqrt X/K\),
\[
a\asymp Y/f,\qquad ac-bd=D/f,\qquad
d=fa\bigl(8\sqrt2\,K+O(1)\bigr)+O(1).
\tag{2}
\]
The \(O(1)\) width in \(2w/q=8\sqrt2 K+O(1)\) comes from the actual critical band. Thus (2) confines \(d\) to an interval of length \(O(fa)\).

The identity
\[
2Z=(\beta-\bar\alpha)(\bar\beta+\alpha)
\]
supplies the extra congruence for \(\gamma\mid Z\). Modulo \(\gamma\), identify \(i\) with a root \(\iota\) of \(-1\) in \(\mathbb F_p\). When \(p\nmid a\), substitute \(c=(D/f+bd)/a\). Each of the two factors gives a linear equation in \(d\) for each \(b\bmod p\). Its coefficient vanishes at at most one \(b\bmod p\), so there are at most \(4p\) eligible residue pairs \((b,d)\bmod p\).

For each such residue pair, complete \(bd\equiv-D/f\pmod a\), with \((a,b)=1\), over the two interval progressions. The principal term is \(O(fa/p^2)\), and the error is
\[
O\!\left(fa^{1/2+o(1)}\sqrt{D/f}\right).
\]
For the error, the complete sum contributes the factor \(\sqrt{(r,sD/f,a)}\) at frequencies \(r,s\). Bound it by \(\sqrt{(D/f,a)}\sqrt{(r,s,a)}\), and expand the last factor over common divisors \(v\mid a\). On frequencies divisible by \(v\), the interval Fourier \(L^1\) sum excluding zero is \(O((a/v)\log a)\). The two-zero term is the principal term. This gives the stated uniform error, including composite \(a\). When \(p\mid a\), the crude \(O(fa)\) count per \(a\) suffices because only one in \(p\) values of \(a\) occurs. [Estermann, *On Kloosterman’s sum*](https://www.cambridge.org/core/journals/mathematika/article/abs/on-kloostermans-sum/DED1120FD0994F590EA6E980D07D0F43).

Summing over \(a\) and \(f\mid D\) gives
\[
\ll \frac{Y^2\log K}{p}+pX^{25/32+o(1)}.
\]
A fixed rotation gives at most one partner per certificate. Summing this bound over rotations by (1), using \(\sum_\gamma p\ll X^{1/8}\), and over \(O(K^2)\) labels proves the result. Any Gaussian-coordinate aliases in the upper bound only enlarge it.

### Cross-label separation

For a label let \(H=3A+5B\), \(J=A+B\), and \(M=(n-H)(n-J)=N(Z)\). At distinct labels all four differences between \(\{H,J\}\) and \(\{H',J'\}\) are nonzero. At fixed \(B\), this follows from \(A\le B\) and strict monotonicity in \(A\). If \(B\) changes, its factor of at least 25 separates the ranges of the shifts. Hence
\[
\gcd(M,M')\mid
\prod_{u\in\{H,J\}}\prod_{v\in\{H',J'\}}|u-v|
\ll X^{1/4}.
\]
If \(Z'/Z=\nu/\gamma\) is reduced, \(N(\gamma)\) is a multiple of \(M/\gcd(M,M')\). Thus **every cross-label denominator has norm \(\gg X^{7/4}\)**. This separates the two types of collisions. It gives no bound for the total cross-label second moment.

### Standalone exact replay

The following verifies a genuine \(r=s=12\) pair with \(K=1200\), prime denominator norm \(2073600201600004901\), and a 1159-bit \(q\)-gap. A second rotation at the same target still satisfies the exact Gaussian equation but fails the critical band. The primality check uses the fully factored \(p-1=N^2\).

```python
from math import gcd, isqrt, prod

k = 1200
A, B = 9**12, 25**12
D = A+2*B
a, N = 13579, 1440000070
p = N*N+1
ps = (2,5,149,373,2591)
assert prod(ps)==N
assert all(all(l%d for d in range(2,isqrt(l)+1)) for l in ps)
assert pow(3,p-1,p)==1
assert all(gcd(pow(3,(p-1)//l,p)-1,p)==1 for l in ps)

C = D-(a*a+1)//2
u1, u2 = -C*pow(a-N,-1,p)%p, -C*pow(a-2,-1,5)%5
b = u1+p*((u2-u1)*pow(p,-1,5)%5)
b += 5*p*(b%2)
lo = (9*(1<<(k//2)))//(8*a)
u = lo+(b-lo)%(10*p)
z, v = (a*u+C,u), (a*u+C+1,a-u)
S = sum(x*x for x in z)
n = S+3*A+5*B
assert S.bit_length()-1==n.bit_length()-1==k
assert A<=B and B**16<=n<=A**32
assert sum(x*x for x in v)==S+2*D

def rotate(z, N):
    x,y = z
    m = N*N+1
    assert (N*x+y)%m==(N*y-x)%m==0
    c,d = (N*x+y)//m,(N*y-x)//m
    return N*c+d,N*d-c

def cert(z):
    x,y = z
    c,d = x-v[0],y-v[1]
    assert c%2 and d%2
    q = ((c+d)//2)**2+((c-d)//2)**2
    Y = y*v[0]-x*v[1]
    assert not Y%2 and q%2 and 2*q*S==(D-q)**2+Y*Y
    return q,S+D-q,Y

q,x,y = cert(z)
qq,xx,yy = cert(rotate(z,N))
bad,_,_ = cert(rotate(z,2))
assert y>0 and yy>0
assert (N*xx-yy,xx+N*yy)==(N*x+y,N*y-x)
assert p**16<=1<<k and abs(q-qq)**100>1<<(49*k)
assert abs(q-qq).bit_length()==1159
assert all(64*k*k*t<=S<=64*k*(k+1)*t for t in (q,qq))
assert not 64*k*k*bad<=S<=64*k*(k+1)*bad

# A different eligible label at the same target.
AA = 9**13
assert AA<=B and n<=AA**32
L1,L2 = (3*A+5*B,A+B),(3*AA+5*B,AA+B)
M1,M2 = (prod(n-h for h in L) for L in (L1,L2))
g = gcd(M1,M2)
assert prod(abs(h-j) for h in L1 for j in L2)%g==0
assert M1//g>p
```
