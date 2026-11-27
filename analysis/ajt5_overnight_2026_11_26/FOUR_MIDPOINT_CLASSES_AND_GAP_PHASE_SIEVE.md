# Four midpoint classes and a prescribed-gap-phase sieve

**The midpoint equation gives a four-candidate test at an exponential gap scale.** At the first nonsquare kernel \(d=6\ell+1\) for \(\ell=23\), a single mod‑17 check rejects all four candidates in the first period. The same equation also gives a conditional sieve for prescribed gap phases, including phases in which no panel prime divides the gap.

### A pointwise bound from four midpoint candidates

Let \(\ell>5\) be prime, \(H=(5^\ell-3^\ell)/2\) or \((5^\ell+3^\ell)/8\), and
\[
H=d s^2q_1q_2,\qquad \Delta=q_2-q_1=6\ell j
\]
for distinct inert primes \(q_1<q_2\) and squarefree \(d\). Put
\[
C=H/d,\qquad N=s(q_1+q_2)/2,\qquad T=s\Delta/2.
\]
Then \(N^2-T^2=C\) and \(d s^2\Delta^2=4d(N^2-C)\).

The exact prime orders give \(N\equiv1\bmod\ell\). Since \(3\ell\mid T\), we have \(N^2\equiv C\bmod9\ell^2\). This fixes one root modulo \(\ell^2\) and allows two roots modulo \(9\). At \(2\), \(N,T\) have opposite parity. If \(C\equiv1\bmod4\), then \(T^2\bmod16\) is fixed by \(C\bmod8\), leaving two possible \(N\bmod8\). If \(C\equiv3\bmod4\), then \(N^2\equiv C+1\bmod8\) fixes \(N\bmod4\), again leaving two classes modulo \(8\). Thus **exactly four midpoint classes survive these tests modulo \(M=72\ell^2\)**.

Take the first representative of each class strictly above \(\sqrt C\), and let \(N_0\) be the smallest. If all four values \(N^2-C\) are nonsquares, every genuine pair satisfies
\[
d s^2\Delta^2\ \ge\ 4d\big((N_0+M)^2-C\big)\ >\ 8M\sqrt{dH}.
\]
This test requires no bound on \(s\). For an exact square survivor with \(T>0\), recover \(s=\gcd(N,T)\) and test \((N-T)/s,(N+T)/s\) for the required prime and inertness conditions. The gcd formula follows because the two reconstructed primes are distinct.

### A sieve for prescribed gap phases

Write \(b=sj\). On a dyadic block \(X<\ell\le2X\), let \(z=\lfloor\log\log X/10\rfloor\), let \(P\) be the product of the \(r\) primes \(7\le p\le z\), and let \(M_0=\operatorname{lcm}(P,\{p-1:7\le p\le z,\ p\text{ prime}\})\). For each reduced phase \(a\bmod M_0\), prescribe at most \(K\) possible classes of \(b\bmod P\), shared across that phase.

In the range \(1<d\le6\ell U+1<(2\ell+1)^2\), the kernel must be a prime \(d=6k\ell+1\). For a fixed phase and a fixed \(b\bmod P\), the condition at every panel prime is
\[
H/d+9\ell^2 b^2\ \text{is a square modulo }p,
\]
including zero. The phase fixes \(H\bmod p\), which is nonzero for genuine exponents since \(p<2\ell+1\). As \(k\) varies with \(d\ne0\bmod p\), the expression runs over every residue except \(9\ell^2b^2\), itself a square. Exactly \((p-1)/2\) classes of \(k\bmod p\) pass.

CRT and a union bound give a fraction at most \(K2^{-r}\). For \(U\ge P\), the two-form Selberg sieve on \(\ell,6k\ell+1\), followed by Cauchy–Schwarz on the local factors in \(k\), bounds the number of prime exponents by
\[
\ll \frac{XU}{\log^2 X}\,z^{O(1)}\min(1,\sqrt K\,2^{-r/2}).
\]
Here \(M_0=X^{o(1)}\), and the local factors \(\prod_{p>2,\ p\mid 6k}(1-2/p)^{-1}\) have bounded second mean by divisor expansion. Taking \(K\le2^{r/2}\) and \(U=\lfloor\log X\,2^{r/8}\rfloor\) makes the exceptional prime exponents reciprocal-summable. In particular, one may prescribe \(b\equiv1\bmod P\), a phase with no small-prime divisibility of the gap. [Selberg’s upper sieve](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1950.1/ICM1950.1.ocr.pdf)

The phase restriction matters. If \(j\) is a unit modulo \(p\ge7\) and \(s\) can vary locally, every unit \(C\bmod p\) survives. Choose \(xy=C\) with \(x\ne\pm y\), possible because at most four of the \(p-1\) unit choices for \(x\) are excluded. Then \(N=(x+y)/2\) and \(s=(y-x)/(6\ell j)\) are units and solve the local equation. This explains why projecting away unrestricted \(s\) gives no sieve saving at such primes. It gives no uniform separation for arbitrary kernels and gaps.

### Exact \(25,9\) replay

The two genuine plus-half factorizations below have \(s=1\). At \((\ell,d)=(23,139)\), the four-candidate test gives \(d s^2\Delta^2\ge164565282768624\). Even the previously admissible phase \(j=2\bmod20\) does not suffice: \(j=2\) with \(s=1\) fails the new midpoint test modulo \(7\).

```python
from math import gcd, isqrt

for ell,d,p,q,r,cut in [
    (23,139,47,228092436443,17,164565282768624),
    (31,102859,353897,15990462533,13,5036834127725154864),
]:
    H = (5**ell+3**ell)//8
    C = p*q
    assert H == d*C and d % (6*ell) == 1 and p % 3 == q % 3 == 2
    assert 25**ell-9**ell == 8*(5**ell-3**ell)*H
    for a in (ell,d,p,q,r):
        assert all(a % i for i in range(2,isqrt(a)+1))
    for a in (d,p,q):
        g = -5*pow(3,-1,a) % a
        assert g != 1 and pow(g,ell,a) == 1
    M = 72*ell**2
    a = 1+ell*((C-1)//ell*pow(2,-1,ell) % ell)
    m8 = {u for u in range(8) if any(
        (u-v)%2 and (u*u-v*v-C)%16 == 0 for v in range(8))}
    L = isqrt(C)+1
    first = [L+(n-L)%M for n in range(a,M,ell**2)
             if (n*n-C)%9 == 0 and n%8 in m8]
    assert len(first) == 4
    assert all(pow(n*n-C,(r-1)//2,r) == r-1 for n in first)
    assert cut == 4*d*((min(first)+M)**2-C)
    N,T = (p+q)//2,(q-p)//2
    assert N*N-T*T == C and gcd(N,T) == 1 and 4*d*T*T >= cut
    if ell == 23:
        assert pow(C+(6*ell)**2,3,7) == 6
```

Independent BigInt verified both complete four-candidate lists, exact modular rejections, and the real factorizations at exponents 23 and 31. The exponential-scale bound concerns the weighted square gap, and only applies when the initial four candidates are ruled out; it is not a uniform unweighted separation.
