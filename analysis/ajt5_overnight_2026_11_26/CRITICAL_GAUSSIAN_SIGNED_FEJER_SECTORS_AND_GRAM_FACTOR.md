# Signed Fejér sectors, averaged actual discriminants, and the cross-label Gram identity

This follows [the two-angle collision bound](https://github.com/Samsen879/a303656/commit/6900b362cf2af280d088b415dbadd048843a2cfb). Three partial advances are certified: bounded mean of the true four-shift bad-prime weights on the actual exponent box, a vanishing low-mode sector, and exact control of the extreme angular tails on the relative-angle diagonal. The intermediate angular range and the general nonzero signed correlation remain open. The native intermediate-angle control was independently replayed, including its nonparallelism and exact Gram factorization.

The varying-weight Hölder argument uses reciprocal exponents \(8C/(p\log p)\); for all sufficiently large primes their sum is at most one, and a unit function absorbs the unused exponent. The individual power turns \(\exp(C/p)\) into \(p^{1/8}\), and the true order bound controls the occurrence of the divisibility event. Zero differences are excluded, not counted as universal bad-prime supports. For the real-axis Hecke lower bound, the elementary positive Euler factor \(3+4\cos\theta+\cos2\theta=2(1+\cos\theta)^2\) is used at distance \(c\Lambda^{-12}\) from 1; the derivative estimate extends it to 1 with a smaller constant. This is only the real-axis estimate needed for the weighted prime sums, not a claimed zero-free region.

### Averaging the actual shifts

Put \(X=2^K\). For a label \(i=(r,s)\), write
\[
A_i=9^r,\quad B_i=25^s,\quad U_i=2A_i+3B_i,\quad D_i=A_i+2B_i,
\qquad M_i=(n-U_i)^2-D_i^2.
\]
I retain the exact gates \(X\le n<2X\) and \(B_i^{16}\le n\le A_i^{32}\), with \(A_i\le B_i\). A certificate with numerical seed \(q\) gives the point
\[
Z_i=n-U_i-q+2iw,\qquad N(Z_i)=M_i.
\]
For each \(q\), the certificate determines at most one \(w\ge0\). In the fixed \(t=8\) band the angles lie within \(O(K^{-2})\) of a common center \(\theta_K\). Thus the previous Fejér majorant applies with \(T\asymp K^2\). Let \(F_m(M)\) be the sum of \(e^{4im\arg z}\) over Gaussian representations of norm \(M\) modulo units. Set
\[
C_{m,\ell}=\sum_{i\ne j}\ \sum_{\substack{X\le n<2X\\ i,j\ {\rm eligible}}}
 F_m(M_i)F_\ell(M_j).
\]
The normalized cross-label majorant is, up to its fixed scale factor,
\[
T^{-2}\sum_{|m|,|\ell|<T} b_m b_\ell C_{m,\ell},
\qquad b_m=(1-|m|/T)e^{-4im\theta_K}.
\]

The four shifts \(U_i\pm D_i,U_j\pm D_j\) are distinct. At equal \(B\) this follows from \(A\le B\) and the different \(A\)'s. At unequal \(B\), consecutive possible \(B\)'s differ by a factor of 25, whereas all shifts at a given \(B\) lie between \(B\) and \(8B\). Henriot’s upper bound gives a factor \(\prod_{p\mid\Delta}(1+C/p)\), with \(\Delta\) the product of the six differences of these shifts. The four forms are monic and have product of coefficient height \(O(X^{1/4})\). At primes dividing \(\Delta\) one can bound each individual prime-power contribution by \(v+1\), using \(u+v+1\le(u+1)(v+1)\) when a prime divides both factors of \(M_i\). [Henriot, Corollary 2](https://arxiv.org/pdf/1102.1643) and [erratum](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf/nair-tenenbaum-uniform-with-respect-to-the-discriminant-erratum.pdf).

**That bad-prime factor has bounded mean on the actual exponent box, for every fixed \(C\).** For each difference, freeze all but one suitable 3-exponent. Outside \(2,3\), divisibility requires \(9^r\) to equal one residue. Write \(d_p=\operatorname{ord}_p(9)\). The only primes discarded by the test \(d_p\ge p^{1/4}\) have summable reciprocals. In \([Y,2Y]\) they divide \(\prod_{h\le(2Y)^{1/4}}(9^h-1)\), giving \(O(Y^{1/2}/\log Y)\) such primes. For the other primes \(p\le K^2\) the divisibility proportion is \(O(p^{-1/4}+K^{-1})\). Apply generalized Hölder to the factors \(\exp(C\mathbf1_{p\mid\Delta_1}/p)\) for a single nonzero difference \(\Delta_1\), with reciprocal exponents \(8C/(p\log p)\) after discarding a fixed initial segment. These reciprocals sum to at most one. The individual moments are bounded by
\[
1+O\!\left(p^{1/8}(p^{-1/4}+K^{-1})\right)=O(1).
\]
The \(p>K^2\) contribution is uniformly bounded since \(|\Delta_1|\le \exp(O(K))\). A final Hölder inequality combines the six differences. The averaging can use a containing box of side \(O(K)\), assigning zero weight at a zero difference. No prime independence is needed.

This proves \(C_{0,0}\ll XK^4\). For nonzero modes the same argument gives
\[
\sum_{i\ne j}\sum_{n\ {\rm eligible}} |F_m(M_i)F_\ell(M_j)|
\ll XK^{4-a(\mathbf1_{m\ne0}+\mathbf1_{\ell\ne0})}(1+\log K)^C,
\qquad a=2-\frac4\pi .
\]
Here the constant \(2/\pi\) per nonzero linear factor comes from the split-prime mean of \(|2\cos(4m\theta_p)|\). One can get the needed uniformity without a zero-free-region input. For \(\nu\ne0\), summation over Gaussian lattice cells gives \(\sum_{v\le y}F_\nu(v)\ll(1+|\nu|)\sqrt y\). Partial summation gives \(|L_\nu(\sigma)|\ll \Lambda\) and \(|L_\nu'(\sigma)|\ll\Lambda^2\) for \(1\le\sigma\le2\), where \(\Lambda=1+\log(2+|\nu|)\). The Euler-product inequality \(\zeta_{\mathbb Q(i)}^3|L_\nu|^4|L_{2\nu}|\ge1\) at \(1+c\Lambda^{-12}\), followed by the derivative bound, gives a lower bound \(|L_\nu|\gg\Lambda^{-37/4}\) throughout that real interval. The Fourier series of \(|2\cos x|\), whose nonconstant coefficients are \(O(h^{-2})\), now gives the prime sum \((2/\pi)\log\log X+O(1+\log\log(3+|m|))\). The zero mode uses the ordinary Mertens sum over split primes. [Williams, *Mertens’ theorem for arithmetic progressions*](https://www.sciencedirect.com/science/article/pii/0022314X74900328).

Consequently, for any fixed \(0<\epsilon<a\), the nonzero modes in \(\max(|m|,|\ell|)\le K^{a-\epsilon}\) contribute \(o(X)\) in absolute value after normalization. **For \(O(X)\) on the cross-label majorant, the remaining estimate is the one-sided bound**
\[
\Re\!\sum_{\substack{|m|,|\ell|<T\\ \max(|m|,|\ell|)>K^{a-\epsilon}}}
 b_m b_\ell C_{m,\ell}\ \ll XK^4 .
\]
The label average above handles the local discriminants. It gives no independence or signed cancellation in this remaining four-shift correlation.

### The relative-angle diagonal

On \(\ell=-m\), the weights \(b_m b_{-m}\) are the Fourier coefficients of the convolution of the Fejér kernel with itself. This convolution is nonnegative and bounded by \(O(T/(1+T^2\|u\|^2))\), where \(\|u\|\) is angular distance on the circle in the kernel’s normalization. It follows that the normalized **nonzero** relative-angle diagonal is bounded below by \(-O(X)\), by subtracting its zero mode. Its unconditional upper bound from the mode estimate is \(O(XK^{8/\pi-2}(1+\log K)^C)\). Pairs with relative angle at least \(1/K\) modulo units contribute \(O(X)\) to the nonnegative convolution, since their normalized kernel is \(O(K^{-4})\).

There is also a power saving at the other end of the angular range. For Gaussian points \(z,z'\) of norms \(M_i,M_j\), rotate by a unit to compare their closest angles. Order the labels so \(e=U_j-U_i>0\). Then \(G=D_j^2-D_i^2>0\) by the same ordering of the actual powers. Define
\[
H=2n-U_i-U_j,\quad
L=(n-U_i)(n-U_j)-\frac{D_i^2+D_j^2}{2},\quad
j_0=L-\Re(\bar z z'),\quad h=\Im(\bar z z').
\]
The \(D\)'s are odd, so \(L\) is integral. Direct subtraction gives
\[
M_iM_j-L^2=-eGH/2-e^2(D_i^2+D_j^2)/2-G^2/4<0.
\]
For large \(X\) the square root lies strictly between \(L-1\) and \(L\). Exact parallelism is therefore impossible. The Gram identity gives the further exact factorization
\[
(2j_0H-eG)^2-2j_0(2h)^2
=(2j_0+e^2)(2j_0+(D_i+D_j)^2)(2j_0+(D_i-D_j)^2).
\]
For \(1\le j_0\le J\le X\), this gives \(O_\epsilon(JX^\epsilon)\) possible targets per label pair. If \(2j_0\) is square, factor the difference of squares. Otherwise, count ideals of the indicated norm in the real quadratic field and then count their generators in the polynomial height range. The ideal count is at most the divisor count of the right side and the unit orbits contribute \(O(\log X)\), uniformly. The Gaussian multiplicity and number of labels can also be absorbed in \(X^\epsilon\). In particular, relative angles \(\le X^{-1/2-\eta}\) contribute only \(O_{\eta,\epsilon}(X^{1-2\eta+\epsilon})\) pairs for \(0<\eta<1/2\), since then \(j_0=O(X^{1-2\eta})\). This holds even for the extra Gaussian points in the majorant. The **intermediate angular range** remains in the diagonal estimate, and the complete second moment is still unresolved.

### Exact replay

The same target below has two distinct numerical seeds at labels \((3,4),(5,4)\). It lies in the intermediate range. Conjugating the last norm coordinate preserves the norm identities and fails the exact critical band.

```python
from math import isqrt

K, B = 300, 25**4
X, A = 1 << K, 9**3
a, u = 3395, 473908545666970293546287554900113349394416
x = a*u + A + 2*B - (a*a+1)//2
n = x*x + u*u + 3*A + 5*B

def cert(r, p, t):
    A = 9**r
    U, D = 2*A+3*B, A+2*B
    S = n-U-D
    k = S.bit_length()-1
    assert X <= n < 2*X and A <= B and B**16 <= n <= A**32
    x,y = p
    a,b = t
    assert x*x+y*y == S and a*a+b*b == S+2*D
    f,g,h = x-a,y-b,x*b-y*a
    assert f%2 and g%2 and h%2 == 0
    q = ((f+g)//2)**2 + ((f-g)//2)**2
    assert q%2 and 2*q*S == (D-q)**2+h*h
    return q,(n-U-q,abs(h)),U,D,64*k*k*q <= S <= 64*k*(k+1)*q

p = (370364302106323949618686923647947300990535546,
     -1565711501568699087370650397834208298305903076)
t = (371286745392217617117272419857876274653556789,
     -1565493013435470228569674359748079227673377687)
q,(a,b),U,D,ok = cert(3,(x,u),(x+1,3395-u))
qq,(c,d),V,E,ok2 = cert(5,p,t)
assert ok and ok2 and q != qq and not cert(5,p,(t[0],-t[1]))[-1]
P = ((n-U)**2-D*D)*((n-V)**2-E*E)
L = (n-U)*(n-V)-(D*D+E*E)//2
dot,h = a*c+b*d,a*d-b*c
j,e,G,H = L-dot,V-U,E*E-D*D,2*n-U-V
assert dot*dot+h*h == P and isqrt(P) == L-1
assert j > X and 0 < h*h*K**4 < P
assert (2*j*H-e*G)**2-2*j*(2*h)**2 == (
    (2*j+e*e)*(2*j+(D+E)**2)*(2*j+(D-E)**2))
print(q.bit_length(), qq.bit_length(), j.bit_length(), abs(h).bit_length())
# 278 278 553 578
```
