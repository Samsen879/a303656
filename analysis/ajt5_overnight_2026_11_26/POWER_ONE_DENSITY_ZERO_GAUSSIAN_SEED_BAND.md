# A power-one, density-zero sufficient language for genuine growing 3,5 labels

This independently verifies the qualitative power-one/density-zero conclusion of the logarithmic seed band, using a simpler lower bound than the sharper logarithmic exponent. If \(F_{\rm win}\) counts distinct targets with \(n^{1/32}\le A\le B\le n^{1/16}\), and \(F_{\rm all}\) also allows all actual power labels, then
\[
 X/(\log X)^{14}\ll F_{\rm win}(X)\le F_{\rm all}(X)\ll X/\sqrt{\log X}.
\]
The positive density or arbitrary-target problem is not solved. In particular, these are bounds for this sufficient language, not for all integers representable in Sun's conjecture. Neither the sharper logarithmic lower exponent nor a priority claim is part of this audit.

Set \(A=9^r,B=25^s,D=A+2B,S=n-3A-5B>0,R=S+2D\). A seed is an odd numerical sum of two squares \(q>0\), a nonnegative integer \(w\) with \(2qS=(D-q)^2+4w^2\), and the band \(k^3q\le S\le(k^3+k^2)q\), where \(k=\lfloor\log_2 S\rfloor\ge 2\) is the actual remainder panel. The same identity gives \(2qR=(D+q)^2+4w^2\) and \(RS=(S+D-q)^2+4w^2\). Since \(2q,S,R\) are positive and the primes \(3\bmod4\) have even valuation in \(2q,2qS,2qR\), both rows are genuine Gaussian norms.

## Lower bound and collision accounting

For \(T=2^k\), keep labels \((2T)^{1/32}\le A\le B\le T^{1/16}\). There are \(\asymp k^2\) of them: choose any two separated nonempty exponent subintervals for \(\log A/\log T\) and \(\log B/\log T\) strictly between \(1/32\) and \(1/16\). Keep primes \(q\equiv1\bmod4\) between \(6T/(5k^3)\) and \(7T/(5k^3)\). There are \(\gg T/k^4\) by the [prime number theorem in fixed progressions](https://doi.org/10.1112/S0010437X12000802). Here \(0<D<q\) for large \(T\), so \(4w^2\equiv-D^2\bmod q\) specifies two distinct residue classes. The real root interval has length in units of \(q\)
\[
 \sqrt{(k^3+k^2)/2-((D-q)/(2q))^2}
 -\sqrt{k^3/2-((D-q)/(2q))^2}\asymp\sqrt k.
\]
For sufficiently large \(k\), it contributes \(\gg\sqrt k\) integral \(w\) in the two classes, with \(S\) even integral and \(n\in[T,2T]\) inside the label window. Hence the number of incidences \((n,r,s,q)\) is \(M\gg T/k^{3/2}\).

Put \(f(m)=r_2(m)/4\) for \(m>0\). At fixed \(n,r,s\) different valid numerical \(q\) give different first coordinates in the representation of \(RS\); for simultaneously represented \(R,S\) one has \(f(RS)\le f(R)f(S)\) prime-by-prime. Thus the multiplicity satisfies \(\mu(n)\le4\sum_{r,s}f(R)f(S)\). Cauchy first in labels, and then in \(n\) for each shifted pair, gives \(\sum_n\mu(n)^2\ll T k^{11}\): the label factor is \(O(k^4)\) and the fourth moment of \(f\) is \(O(T k^7)\).

For the latter, \(f(m)^4\le f^{*8}(m)\), where \(*\) is Dirichlet convolution. At split \(p^a\), \((a+1)^4\le\binom{a+15}{15}\): encode four cut positions in \(\{0,\ldots,a\}\) by counting each of the 16 membership patterns of the \(a\) ordered positions with respect to the cuts. The pattern counts recover all four cut positions. At ramified or inert primes use \(f(p^a)\in\{0,1\}\). The elementary disk lattice bound \(\sum_{m\le T} f(m)\ll T\), partial summation and seven iterations of the convolution bound prove the fourth moment. A final Cauchy step gives at least \(M^2/(Tk^{11})\gg T/k^{14}\) distinct targets. For arbitrary sufficiently large \(X\), use a dyadic \(T\asymp X\) with \(2T\le X\).

## Upper bound, including all actual labels

On \(T\le S<2T\) every admissible \(q\asymp Q=T/k^3\), while the equation bounds \(D\le q+\sqrt{2qS}=O(T/k^{3/2})\). Thus \(n\asymp T\), and all labels lie in an origin box with both sides \(O(k)\). For odd \(q\), put \(\rho_q(D)=\#\{x\bmod q:x^2\equiv-D^2\bmod q\}\). For an odd norm \(q\), prime-power root counting and CRT give
\[
 \rho_q(D)\le\sum_{h\mid D,\ h^2\mid q}h f(q/h^2);
 \qquad \sum_{q\le C Q,\ q\ {\rm odd\ norm}}\rho_q(D)\ll Q\sigma_{-1}(D).
\]
Indeed if \(a=v_p(q)\le 2v_p(D)\), use \(h=p^{\lfloor a/2\rfloor}\); when \(a>2v_p(D)\), the root count is zero for inert \(p\) and at most \(2p^{v_p(D)}\) for split \(p\), supplied by \(h=p^{v_p(D)}\). Sum the majorant using \(\sum_{m\le Y}f(m)\ll Y\).

The origin-box average of \(\sigma_{-1}(9^r+2\cdot25^s)\) is \(O(1)\). Remove the bounded Euler factors at \(2,3,5\); for \(d\) coprime to 30 count along the longer exponent axis \(a\in\{9,25\}\). For each fixed other coordinate, \(d\mid D\) contributes at most \((L+1)/\operatorname{ord}_d(a)+1\) choices. The endpoint sum over \(d\le\exp(O(L+1))\) is \(O(L+1)\). For the main term, \(\sum 1/(d\operatorname{ord}_d(a))<\infty\) because all moduli of order \(\le y\) divide the product of \(a^j-1\), \(1\le j\le y\). Its logarithm is \(O(y^2)\), so its reciprocal divisor sum is \(O(\log(2y))\) by the [Mertens product bound](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf) (split its Euler product at the logarithm of the integer). A dyadic sum of \(O(\log(2y)/y)\) converges. The same reciprocal divisor bound gives \(\sigma_{-1}(D)=O(\log(2k))\) pointwise on the panel.

For \(D\le T/k^4\) the root interval has length \(O(\sqrt k)\) in units of \(q\). Its endpoint contribution is included in \(O(1+\sqrt k)\); the average bound just proved gives \(O(\sqrt k\,Q k^2)=O(T/\sqrt k)\) incidences. For \(D>T/k^4\), one exponent is within \(O(\log k)\) of its largest possible value given \(A,B\ll T\). There are only \(O(k\log k)\) such labels. Even across the square-root turning point the length in units of \(q\) is \(O(k)\) (use \(\sqrt{x+k^2/2}-\sqrt{x}\le k\) after taking the nonnegative interval). The pointwise divisor bound therefore gives \(O(k Q\cdot k(\log k)^2)=O(T(\log k)^2/k)\). This is smaller than \(T/\sqrt k\) asymptotically. Summation over the dyadic panels yields the claimed upper bound. Both ends of the proof count distinct targets correctly: incidence counting is only used directly for the upper bound; the second moment is required for the lower bound.

## Independent exact controls

The following checks compare the new band against the entire old band in the original height window, and retain an input that fails the new language despite a genuine original representation.

```python
from math import isqrt
n=2361517588799380546639730
S,D=n-152,59
q,w=4611686018427387905,2333513125387609047546
assert 25**16<=n<=9**32 and n<625**16
assert q==2147483648**2+1 and q==1288490188**2+1717986919**2
assert q*S//2-((D-q)//2)**2==w*w
assert S==1087700468247**2+1085552983587**2
assert S+118==1085552984600**2+1087700467236**2
k=S.bit_length()-1
assert k==80 and k**3*q<=S<=(k**3+k*k)*q
# Only (A,B)=(9,25) lies in the original window. Enlarge the old q band:
Q=isqrt(isqrt(S))
assert Q==1239646 and S>=32**16
lo=((32*Q+32)//33)|1
assert len(range(lo,Q+1,2))==18783
for u in range(lo,Q+1,2):
    z=u*S//2-((D-u)//2)**2
    assert z<0 or isqrt(z)**2!=z
n0=25**16+13
assert 25**16<=n0<=9**32 and n0<625**16 and (n0-152)%9==3
assert n0==102087582334**2+113407186274**2+3**0+5**1
```
