# A certified logarithmic matching coefficient on a majority of a composite progression

**More than half of the composite targets \(n\equiv0\pmod{15}\) have an ordinary-height matching of size at least \((\log X)/64\) in the limit inferior over \(X<n\le2X\).** The certified lower relative proportion is
\[
\frac{8143011}{16239811}> \frac12.
\]
The proof bounds conditional local moments using prime orders only up to \(2^{14}\) and an analytic tail. This progression lies outside the prime-indexed family \(n=5p+52\). [Verified capped endpoint profile](https://github.com/Samsen879/a303656/commit/c92bb115bf6404a70b1344d2337835f108e4db7e)

### A conditional lower-tail bound

Write \(C=\{n\equiv0\pmod{15}\}\), let \(\Psi=F^2/G\) on \(\{F>0\}\), and set \(\Psi=0\) on \(\{F=0\}\). In the notation of the endpoint profile,
\[
G=8\log3\,P_3(F_5^2)+6\log5\,P_5(F_3^2).
\]
Jensen gives \(\Psi\le(8\log3+6\log5)^{-1}<h=25/458\).

For this class, both local arguments at \(3\) and \(5\) are units in every eventual exponent phase. At \(3\) the shift is \(5^d\), and at \(5\) it is \(3^c\). Their norm densities are respectively \(4/3\) and \(4/5\). Thus \(\mathbb E_C F=(16/15)\pi\). In the conditional endpoint moments these same two factors occur squared. All other primes integrate by the verified local pair kernels. For the one-axis difference at base \(b\), write \(k\) for the Haar difference of the two exponents. This gives
\[
\frac{\mathbb E_C G}{(\mathbb E_C F)^2}
=8\log3\,H_5+6\log5\,H_3,
\]
where
\[
H_b=\mathbb E_k\!\left[
\kappa_2(b^k-1)\prod_{q\ge7}
(1-q^{-2})\sum_{j=0}^{v_q(b^k-1)}q^{-j}
\right].
\]
The formula follows first for finite prime panels and then by the verified \(L^2\) convergence of the one-axis profiles.

The bounds below give \(H_3<27/20\) and \(H_5<7/4\). Conditional Cauchy–Schwarz applied to \(F=\sqrt{\Psi G}\) therefore gives
\[
\mathbb E_C\Psi \ \ge\ \frac{(\mathbb E_C F)^2}{\mathbb E_C G}
\ >\ m=\frac{1000}{28441}.
\]
Let \(\beta=\mu_C(F=0)\), exactly the conditional measure of the eventual modular obstruction union. For \(0\le t<h\), splitting the mean according to \(\Psi=0,\ 0<\Psi\le t,\ \Psi>t\) gives
\[
\mu_C(\Psi>t)\ \ge\ \frac{m-t(1-\beta)}{h-t}.
\]
At \(t=1/64\), even using \(\beta\ge0\) gives the stated proportion. The capped profile convergence holds under the fixed restriction \(n\equiv0\bmod15\): the finite-modulus approximations can use moduli divisible by \(15\), and their mean errors increase by at most a fixed factor. Applying the open event \(F^2>tG\) transfers the bound to \(\nu_X\ge t\log X\) in the verified ordinary-height rectangle. [Exact obstruction-union comparison](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e)

### Certifying the moments without a large modulus

Put \(o_q=\operatorname{ord}_q(b)\). Bound each geometric factor by \(1+\mathbf1_{o_q\mid k}/(q-1)\). For \(7\le q\le61\), expand exactly and group products by the lcm \(l\) of their orders. A term has mean \(\mathbb E(\kappa_2\mid l\mid k)/l\). Writing \(r=v_2(l)\), the conditional mean is \(2-2^{-r-1}\), except for \(b=3,\ r=0\), where it is \(9/8\). This follows from the actual \(2\)-adic valuations of \(3^k-1\) and \(5^k-1\), with \(\mathbb E(2^{-v_2(u)})=2/3\) for Haar \(u\).

For larger primes, expand by the largest chosen prime \(q\), bounding its contribution by
\[
\frac{2}{(q-1)o_q}\prod_{7\le p<q}\frac p{p-1}.
\]
Sum this explicitly up to \(Y=2^{14}\). Above \(Y\), the Rosser–Schoenfeld bound gives \(\prod_{p<q}p/(p-1)\le2\log q\). In a dyadic block \(U<q\le2U\), the orders at most \(\sqrt U\) contribute at most \((\log b)/\sqrt U\) to \(\sum \log q/((q-1)o_q)\): the primes of each order \(j\) divide \(b^j-1\). The larger orders contribute at most \(2\log2/\sqrt U\), since the product of primes in that block divides \(\binom{2U}{U}\). The geometric dyadic tail, including the factor \(2\) and the removal of \(2,3,5\) from the Mertens product, is bounded by
\[
\frac{16}{15}\frac{7}{2}\frac{31}{10}\frac1{\sqrt Y}.
\]
[Rosser–Schoenfeld, Theorem 7](https://doi.org/10.1215/ijm/1255631807)

The bound certifies a fixed packing coefficient on a majority of one progression. An inverse-moment estimate such as \(\mathbb E_C[(G/F^2)^s;\,F>0]<\infty\) for some \(s>0\) would give power decay of the positive lower tail. That estimate and pointwise coverage remain open.

```python
from fractions import Fraction as F
from math import isqrt, lcm

N = 2**14
s = [True]*(N+1)
s[0] = s[1] = False
for p in range(2,isqrt(N)+1):
    if s[p]:
        s[p*p::p] = [False]*((N-p*p)//p+1)
P = [p for p in range(2,N+1) if s[p]]

def order(b,p):
    rem = o = p-1
    for q in P:
        if q*q > rem:
            break
        if rem % q == 0:
            while rem % q == 0:
                rem //= q
            while o % q == 0 and pow(b,o//q,p) == 1:
                o //= q
    if rem > 1:
        while o % rem == 0 and pow(b,o//rem,p) == 1:
            o //= rem
    return o

def k2mean(b,l):
    return F(9,8) if b == 3 and l % 2 else 2-F(1,2*(l & -l))

def bound(b):
    D, bg = {1:F(1)}, F(1)
    S = 10**12
    W, mid = S, 0
    for p in P[3:]:
        o = order(b,p)
        if p <= 61:
            for l,a in list(D.items()):
                k = lcm(l,o)
                D[k] = D.get(k,0) + a/(p-1)
            bg *= 1-F(1,p*p)
        else:
            d = (p-1)*o
            mid += (2*W+d-1)//d
        W = (W*p+p-2)//(p-1)  # round the scaled product upward
    tail = F(16,15)*F(7,2)*F(31,10)/128
    return bg*(sum(a*k2mean(b,l)/l for l,a in D.items())+F(mid,S)+tail)

assert bound(3) < F(27,20) and bound(5) < F(7,4)
m,h,t = F(1000,28441),F(25,458),F(1,64)
assert (m-t)/(h-t) == F(8143011,16239811) > F(1,2)

X,n = 10**6,1000080
for c,d,x,y in [(2,3,585,811),(3,4,272,962)]:
    a,b = 3**c,5**d
    assert X<n<=2*X and n%15==0 and 4*max(a,b)<=n
    assert X<=a**8 and a**4<=X and X<=b**3 and b*b<=X
    assert n-a-b == x*x+y*y
```

For the tail constants, the full Mertens product is bounded by \(2\log q\) above \(2^{14}\) by the cited explicit theorem. Removing primes 2, 3 and 5 multiplies it by \(4/15\); the other factor 2 bounds the binary correlation. The dyadic geometric sum is less than \(7/2\), and \(\log b+2\log2<31/10\) for \(b=3,5\). The coarse rational choices of \(m,h\) follow, for example, from \(1.098<\log3<1.099\) and \(1.609<\log5<1.610\). The complement of this majority claim is not certified as exceptional.
