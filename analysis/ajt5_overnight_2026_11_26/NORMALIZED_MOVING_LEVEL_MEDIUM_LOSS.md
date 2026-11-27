# Normalized switched losses under a moving sieve level

The normalized mismatch from the least additional inert primes near \(B^{4\rho}\) is **exponentially small in \(1/\rho\)**, even though there are order \(M_\ell/\sqrt{\rho}\) such losses in each class. A moving sieve level also bounds the normalized mismatch by \(O(M_\ell)\) through \(t=B^{6/25}\). The sign of the remaining contrast is open.

### Moving-level comparison

Keep the original strip \(A=3^a,\ B=5^b\), with even \(a,b\) and \(39/40<B/A<122/125\). Write \(S_0=A+25B,\ S=3^c+5^e,\ \kappa=(S_0-S)/45\). The labels still satisfy
\[
a/10\le c\le a/3,\qquad b/5\le e\le b/3,\qquad
c\equiv a\pmod4,\quad e\equiv b+2\pmod6,
\]
and lie in the seven phases \(S\equiv r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). Count prime anchors \(n=S_0+45p\), \(p\equiv1\pmod4\), in the sharp window \(1457A-123B<n\le729A+625B\). The two classes are \(w=1\) with \(n\equiv0\pmod{49}\), and \(w=49\) with \(v_7(p+\kappa)=2\), which gives \(n\equiv r_-\pmod{49}\). Their progression densities are \(\alpha_1=1/84\) and \(\alpha_{49}=1/98\).

Mark \(q\in(B^\rho,B^{2\rho}]\) and \(r\in(B^{2\rho},B^{3\rho}]\), both prime and \(3\bmod4\). Let \(K_{\ell,w}(b_0,b_1)\) count the switched losses whose least additional inert prime \(t\) lies in \((B^{b_0},B^{b_1}]\), where \(b_0\ge4\rho\). Thus \((p+\kappa)/w=qrtv\), and \(v\) has no inert prime below \(t\). For \(w\)-indexed counts put \(\Delta_\ell X=X_{\ell,1}/\alpha_1-X_{\ell,49}/\alpha_{49}\), and set
\[
M_\ell=\frac{B}{(\log B)^{3/2}}
       \prod_{\substack{j\mid\kappa\\j\ {\rm prime},\ j\equiv3\ (4)}}\frac{j-1}{j-2}.
\]

For \(0<\rho<1/250\), use \(h_\rho=49/100-5\rho/2\) and the divisor level \(D(t)=\lfloor B^{h_\rho}/t\rfloor\). The full prime modulus is \(196qrtd\) or \(1372qrtd\), with \(d\le D(t)\). It is \(O(B^{h_\rho+5\rho})\), below the Bombieri–Vinogradov level by a fixed power. A modulus admits \(O(\rho^{-3})\) choices for the three marked primes and then determines \(d\). The progression errors therefore sum to \(O_A(B(\log B)^{-A})\) for arbitrary \(A\), uniformly in the actual label and both window endpoints. This also works when \((\log B)^{-1/2}\le\rho\le1/300\). [Bombieri, *On the large sieve*](https://doi.org/10.1112/S0025579300005313).

The two sieve main terms agree after normalization. At \(q,r\) a further sieve hit imposes a second power, giving local densities \(1/q,1/r\). Elsewhere the density is \(1/(j-1)\) at inert \(j\nmid 7\kappa\). Writing \(u=\log t/\log B\), the moving sieve parameter is \(s(u)=h_\rho/u-1+o(1)\). For fixed endpoints \(4\rho\le b_0<b_1\le6/25\), the resulting bound is
\[
|\Delta_\ell K(b_0,b_1)|
 \le H_\ell\int_{b_0}^{b_1}u^{-3/2}
      \bigl(F_{1/2}-f_{1/2}\bigr)(h_\rho/u-1)\,du
      +o_\rho(M_\ell).
\]
Here \(H_\ell\asymp M_\ell\) is the common coefficient obtained from the sharp interval’s logarithmic-integral length, the inert Euler product, and the marked harmonic masses \(\frac12\log2,\frac12\log(3/2)\). The density \(u^{-3/2}\) follows by summing \(1/((t-1)\sqrt{\log t})\) over inert primes \(t\). This integral bounds the difference by the width of the two sieve envelopes at each \(t\), before summation. [Nath and Xie, Lemma 3.6 and §5](https://arxiv.org/html/2501.16723v1#S5).

There are two useful bounds on that width. First, if \(G=F_{1/2}-f_{1/2}\), the sieve differential equations give
\[
(\sqrt{s}\,G(s))'=-\frac{G(s-1)}{2\sqrt{s}}\qquad(s>2).
\]
Since \(\sqrt{s}G(s)\) is decreasing also on \([1,2]\), integration gives \(G(s)\le2G(2)/s\) for \(s\ge2\): for \(H(s)=\sqrt{s}G(s)\), monotonicity gives \(H'(s)\le-H(s)/(2\sqrt{s(s-1)})\le-H(s)/(2s)\). The integral is thus bounded at \(u=0\), even as \(\rho\downarrow0\). Second, the fundamental lemma gives the stronger relative error \(O(s^{-s/2})\). For \(u\le1/16\) one has \(s\ge 2/(5u)\) for large \(B\). On each dyadic exponent band \(u\in(\lambda/2,\lambda]\), the common main term is \(O(M_\ell/\sqrt{\lambda})\). Summing the fundamental-lemma errors on those bands gives
\[
\boxed{\displaystyle
|\Delta_\ell K(4\rho,\eta)|
 \ll M_\ell\exp\!\left[-\frac{\log(1/\eta)}{20\eta}\right]
      +O_A\!\left(M_\ell(\log B)^{-A}\right),
\qquad 4\rho<\eta\le1/16 .}
\]
In particular \(K_{\ell,w}(4\rho,8\rho)/\alpha_w\asymp M_\ell/\sqrt\rho\), while the normalized difference on that band satisfies the boxed bound with \(\eta=8\rho\). No averaging assumption on the exponent labels enters the proof. [Kurlberg, Lester and Rosenzweig, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136).

### A sufficient rate on the residual range

Let \(T_{\ell,w}\) count the exact two-inert failures: the cofactor after removing \(q,r\) has only split primes. Write \(\mathcal M=\sum_\ell M_\ell\) and \(\Delta=\sum_\ell\Delta_\ell\). For sufficiently small \(\rho\), take
\[
\eta_\rho=\frac{\log\log(1/\rho)}{100\log(1/\rho)},\qquad
K_{\rm res}=K(\eta_\rho,\,1/2-12\rho).
\]
Then
\[
\boxed{\displaystyle
\Delta T=-\Delta K_{\rm res}
       +O(\rho^{3/2}\mathcal M)
       +O_A\!\left(\mathcal M(\log B)^{-A}\right).}
\]

Indeed, the initial sieve through \(B^{4\rho}\) has the same normalized main term, and the boxed lower-range estimate with \(\eta_\rho\) costs \(O(\rho^{5/2}\mathcal M)\). Beyond \(z_*=B^{1/2-12\rho}\), a surviving cofactor with an inert factor has exactly two, counting multiplicity, by parity and \(z_*^3\gg B\). Repeated factors contribute \(O(B/z_*+\sqrt B)\) per label. For distinct factors, the two-linear-form upper sieve in the larger factor gives the terminal \(O(\rho^{3/2}M_\ell)\) bound. The smaller inert factor contributes a harmonic \(O(\rho)\), and the split cofactor, at most \(O(B^{24\rho})\), contributes \(O(\sqrt{\rho\log B})\). Excluding split primes dividing \(\kappa\) from that cofactor cancels their split singular factors.

A signed contrast on the explicit residual band that dominates \(\rho^{3/2}\mathcal M\) therefore decides the **opposite** sign for the marked loss. For example, at \(\rho=(\log B)^{-1/2}\), a fixed-sign lower bound of order \(\mathcal M(\log B)^{-3/4+\varepsilon}\) suffices for any fixed \(\varepsilon>0\). Such an estimate has yet to be proved. The raw \(48/49\) inequality does not supply it.

### Exact replay

For \((a,b,c,e)=(712,486,80,122)\) and \(\rho=1/375\), the replay certifies both classes at the same label. Group 0 is a true alternate, group 1 has exactly the two marked odd valuations, group 2 has two more at least prime \(4211<B^{8\rho}\), and group 3 has two more at least prime \(2^{61}-1\), above \(B^{\sqrt\rho}\) and below \(B^{6/25}\). All depth-two controls have the same lift \(p+\kappa\equiv49\pmod{343}\).

```python
from math import gcd, isqrt, prod

def small_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n)+1))

def mersenne(h):
    assert small_prime(h)
    n, x = (1 << h)-1, 4
    for _ in range(h-2):
        x = (x*x-2) % n
    assert x == 0                         # Lucas–Lehmer
    return n

A, B = 3**712, 5**486
S0, S = A+25*B, 3**80+5**122
k, rem = divmod(S0-S, 45)
L = (1457*A-123*B-S0)//45+1
U = (729*A+625*B-S0)//45
r = (pow(3,716,49)+pow(5,488,49)+7)%49
Q = 1 << 378
t, u = mersenne(61), mersenne(89)
assert 39*A < 40*B and 125*B < 122*A and S%49 == r == 27
assert rem == k%8 == 0 and B < 59**375 < B**2 < 67**375 < B**3
assert B**4 < 4211**375 < B**8 and 8**2 < 375
assert B**53 < t**1000 and 53**2*375 > 1000**2 and t**25 < B**6
assert all(small_prime(p) and p%4 == 3 for p in (59,67,4211,4219))
groups = [(), (59,67), (59,67,4211,4219), (59,67,t,u)]

for w,g,j,s in [(1,0,1088,5), (49,0,88,5), (1,1,429,5), (49,1,952,13),
                (1,2,209,13), (49,2,173,5), (1,3,1469,13), (49,3,743,17)]:
    F = prod(groups[g])
    f = 4*((isqrt((L+k)//(w*F))+4)//4+j)
    h, rem = divmod(((k+1+Q)*pow(w*F,-1,2*Q)-f*f-1)%(2*Q),8)
    assert rem == 0
    v = h%2
    for i in range(2,377):
        v += (h-2*v*v-v)%(1<<i)
    x = 1+4*v
    M = 49 if w == 1 else 7
    a = -S*pow(45*F,-1,49) if w == 1 else pow(F,-1,7)
    z = next(z for z in range(M) if (z*z+f*f-a)%M == 0)
    x += Q*((z-x)*pow(Q,-1,M)%M)
    m = x*x+f*f
    p = w*F*m-k
    hi, lo = divmod((p-1)//Q,Q)
    D = lo*lo-4*hi
    assert L <= p <= U < Q**3 and p%Q == 1 and ((p-1)//Q)%2
    assert pow(s,(p-1)//2,p) == p-1 and (D < 0 or isqrt(D)**2 != D)
    assert gcd(x,f) == 1 and m%2 == 1
    assert (S0+45*p)%49 == (0 if w == 1 else r)
    assert (p+k)%7 != 0 if w == 1 else (p+k)%343 == 49
    print(w,g,p.bit_length(),(p+k)%343)
```

The modular witness forces every prime divisor of \(p\) to be \(1\bmod Q\). A composite \(p<Q^3\) would have two factors \(1+Qx,1+Qy\), with \(xy<Q\) and \(x+y<Q\). The two digits of \((p-1)/Q\) would then be \(xy,x+y\), giving a square discriminant. The cofactor \(m\) is an odd primitive sum of two squares, so the marked primes give the complete inert support of the alternate outside the even \(7\)-power.
