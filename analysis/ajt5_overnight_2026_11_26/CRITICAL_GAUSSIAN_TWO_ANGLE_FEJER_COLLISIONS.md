# Two-angle critical-band collision bound

This follows [the actual-shift cross-label sieve](https://github.com/Samsen879/a303656/commit/b4057ab280c6877e8df3261efb60a576bd2249b5). Retaining both angular windows yields a stronger logarithmic saving, but still leaves \(K^2\) after summing the actual label pairs. The bound here cannot imply an \(O(X)\) second moment or positive density. The native one-by-two collision and matched failed conjugate were independently replayed.

For the Fejér step, apply a nonnegative kernel to the angle multiplied by four, with kernel degree a sufficiently small fixed multiple of \(K^2\). It is bounded below by a fixed multiple of its degree throughout the true angular window. Its Fourier coefficients have squared sum \(O(T)\), so Cauchy gives the stated normalized harmonic bound. For the frequency-dependent Euler product, partial summation using the disk-lattice bound controls the tail beyond \((2+|\nu|)^2\) by \(O(1)\). In replacing \(p^{-\sigma}\) by \(1/p\) up to \(X\), the total loss is \(O((\log X)^{-1}\sum_{p\le X}\log p/p)\); the absolutely bounded prime tail above \(X\) follows from Chebyshev and \(\sigma-1=1/\log X\). All uses of the corrected discriminant-uniform result are upper bounds.

Keeping **both** critical-band angles gives a stronger cross-label bound. For \(X=2^K\), let \(\mu_i(n)\) count distinct numerical seeds \(q\) at the actual label \(i=(r_i,s_i)\). Uniformly for distinct labels,
\[
\sum_{X\le n<2X}\mu_i(n)\mu_j(n)
 \ll \frac{X}{K^2}(1+\log K)^C.
\]
Summing over all label pairs gives \(O(XK^2(1+\log K)^C)\), improving the preceding \(K^{4-\eta}\) bound. There is no restriction on the cross-label denominator norm. The same order bounds the full second moment after including the within-label terms. It remains above \(O(X)\).

### Keep the second angle in the multiplicity bound

For one label write \(M=SR\) and \(Z=S+D-q+2iw\). The fixed \(t=8\) band gives
\[
N(Z)=M,\qquad
\arg Z=\frac{\sqrt2}{8K}+O(K^{-2}).
\]
This follows from \(q/S=1/(64k^2)+O(k^{-3})\) and \(k=K+O(1)\). A Fejér kernel of degree \(T-1\), with \(T\asymp K^2\) and a sufficiently small absolute proportionality constant, majorizes the actual angular window after division by \(T\).

Define the normalized Gaussian harmonics
\[
F_m(N)=\frac14\sum_{N(z)=N}(z/|z|)^{4m}.
\]
The kernel bound and Cauchy–Schwarz give
\[
\mu_i(n)^2\ll \frac1T\sum_{|m|<T}|F_m(S_iR_i)|^2.
\tag{1}
\]
Each numerical seed determines one point \(Z\). Counting additional circle points in the majorant only enlarges the upper bound.

The useful feature of the **squared** harmonics is their first-order prime weight. For a split prime \(p\) of Gaussian angle \(\theta_p\), the weight for \(m\ne0\) is
\[
|F_m(p)|^2=2+2\cos(8m\theta_p).
\]
Uniformly for \(0<|m|<T\), its harmonic sum over primes up to \(X\) is at most \(\log\log X+O(1+\log\log K)\). For \(m=0\) the corresponding bound is \(2\log\log X+O(1)\).

The uniform cosine bound here follows from an elementary lattice estimate. For \(\nu\ne0\), comparison of the angular character with its integral over a disk gives
\[
\left|\sum_{0<N(z)\le u}(z/|z|)^{4\nu}\right|
 \ll (1+|\nu|)\sqrt u .
\]
The disk integral is zero. The boundary cells contribute \(O(\sqrt u)\), and summing the gradient bound \(O(|\nu|/|z|)\) over interior cells gives the remaining error. Splitting the Gaussian Dirichlet series at \((2+|\nu|)^2\) and using partial summation bounds its absolute value by \(O(1+\log(2+|\nu|))\) for real \(1<\sigma\le2\). Its Euler product at \(\nu=2m\) therefore bounds the cosine prime sum from above. Taking \(\sigma=1+1/\log X\) and replacing \(p^{-\sigma}\) by \(1/p\) up to \(X\), with the tail discarded, costs \(O(1)\) by Chebyshev’s bound. [Williams, *Mertens’ theorem for arithmetic progressions*](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf).

### From harmonics to collision counts

At primes outside \(2D_i\), at most one of \(S_i,R_i\) is divisible by that prime. Multiplicativity therefore separates their squared harmonic weights. At primes dividing \(2D_i\), the envelope \((e+1)^2\) on each prime power \(p^e\) bounds their combined weight.

Apply Henriot’s corrected upper bound to the four distinct monic shifts. The weights are nonnegative multiplicative functions bounded by the squared divisor function, uniformly in the frequencies. The shifts have height \(O(X^{1/16})\). The Euler factors at primes dividing the shift differences cost only \((1+\log K)^C\). The good-prime factors, including the four-shift sieve factor, give
\[
\sum_n |F_m(S_iR_i)|^2\,|F_l(S_jR_j)|^2
 \ll X(1+\log K)^C K^{2\mathbf 1_{m=0}+2\mathbf 1_{l=0}}.
\]
In (1), each zero frequency costs \(1/T\asymp K^{-2}\), cancelling its extra \(K^2\). Hence for \(W(n)=\mu_i(n)\mu_j(n)\),
\[
\sum_n W(n)^2\ll X(1+\log K)^C .
\tag{2}
\]
The same calculation with two shifts gives \(\sum_n\mu_i(n)^2\ll X(1+\log K)^C\) for one label. [Henriot, discriminant-uniform bound](https://doi.org/10.1017/S0305004111000752) · [Erratum](https://doi.org/10.1017/S0305004114000280).

For the lower moment, the cross-shift sieve from the preceding result gives \(\sum_n W^{1/2}\ll XK^{-3}(1+\log K)^C\). Its input is the first label’s critical-band determinant chart and the two inert valuation-one exclusions at the other label. The discriminants of those exclusions are the products of the four cross-shift differences, and the combined local density is \(2/p+O(p^{-3/2})\) at good inert primes. Sieve completion at cutoff \(X^{1/100}\) has power-smaller error. Interpolating this bound with (2) proves the result:
\[
\sum_n W(n)\le
 \left(\sum_n W(n)^{1/2}\right)^{2/3}
 \left(\sum_n W(n)^2\right)^{1/3}.
\]

These two moment bounds alone cannot give \(O(X)\) after summing labels. For example, the synthetic distribution \(W=K^2\) on \(\lfloor X/K^4\rfloor\) targets saturates both bounds and has mass of order \(X/K^2\). This is a barrier to the interpolation argument. The next concrete input would be cancellation in the signed two-frequency Fejér sum over the actual four shifts. Its zero–zero term already carries the required \(T^{-2}\) scale, up to the shift factors.

### New native control

This replay verifies one seed at \((3,4)\) and **two distinct seeds** at \((5,4)\) for a single target. The cross gaps have 267 and 269 bits. The circle norms have gcd 40. Conjugating one coordinate pair preserves the norm equation and fails the exact band.

```python
from math import gcd, prod

K = 300
A, B = 9**3, 25**4
a, u = 3395, 473908545666970293546287554900113349394416
D = A+2*B
x = a*u+D-(a*a+1)//2
n = x*x+u*u+3*A+5*B
assert 1<<K <= n < 1<<(K+1)

def cert(r, Z, R):
    A = 9**r
    S, D = n-3*A-5*B, A+2*B
    k = S.bit_length()-1
    assert k==K and A<=B and B**16<=n<=A**32
    x,y = Z
    a,b = R
    assert x*x+y*y==S and a*a+b*b==S+2*D
    d,e = x-a,y-b
    assert d%2 and e%2 and (x*b-y*a)%2==0
    q = ((d+e)//2)**2+((d-e)//2)**2
    w = abs(x*b-y*a)//2
    assert q%2 and 2*q*S==(D-q)**2+4*w*w
    return q,64*k*k*q<=S<=64*k*(k+1)*q

q,ok = cert(3,(x,u),(x+1,a-u))
assert ok
P = ((370364302106323949618686923647947300990535546,
      -1565711501568699087370650397834208298305903076),
     (371286745392217617117272419857876274653556789,
      -1565493013435470228569674359748079227673377687))
Q = ((-1597955578264978799405325545778388930894084774,
       187510512534769672105752777958105055482476396),
     (-1597844914361732718846382659807004607991060757,
       188451192799519932657551043355716796288702729))
seeds = []
for Z,R in (P,Q):
    qq,ok = cert(5,Z,R)
    assert ok
    seeds.append(qq)
assert len(set(seeds))==2
assert [abs(q-qq).bit_length() for qq in seeds]==[267,269]
assert not cert(5,P[0],(P[1][0],-P[1][1]))[1]

L  = (3*9**3+5*B,9**3+B)
LL = (3*9**5+5*B,9**5+B)
M,N = (prod(n-s for s in shifts) for shifts in (L,LL))
assert gcd(M,N)==40 and (M//40)**4>(1<<K)**7
```
