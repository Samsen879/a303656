# Balanced inert semiprime layers: exact overlaps and two open energies

Consider the stripped-cofactor selector at screen \(B(n)=\lfloor\sqrt n/\log n\rfloor\), only on odd targets. Write \(H=\log X\), take actual distinct labels \(\lambda=9^e+5^d\le X/8\), and balanced squarefree factors \(s=pq\asymp H\) with distinct inert primes \(p,q\asymp\sqrt H\), choosing the constants so \(s\ge2H\). Require \(n=\lambda+s^2u\in[X,2X]\), with all prime factors of \(u\) congruent to \(1\bmod4\). Such cofactors give genuine positive odd certificates and \(u\) is below the screen cutoff for large \(X\). The argument is for this chosen layer, not for every representation and not for individual \(n\).

There are \(\asymp H^2\) eligible distinct labels after imposing \(2e\ge2\log_3 H\) and keeping a bulk rectangle of exponent choices. A collision at different \(3\)-exponents would force the smaller one to equal \(v_3(5^{|d-d'|}-1)\le1+\log_3|d-d'|\), impossible for large \(X\). There are \(\asymp H/(\log H)^2\) balanced factors. The count of integers supported on split primes, from [Wirsing's theorem](https://doi.org/10.1007/BF01351892), gives first moment \(\asymp X\sqrt H/(\log H)^2\). Thus a second moment \(O(XH/(\log H)^4)\) would suffice for a positive fraction.

## The coprime contribution is controlled

For two witness types \((s,\lambda),(t,\mu)\), let \(g=\gcd(s,t)\), \(h=\mu-\lambda\). CRT requires \(g^2\mid h\), and any inert prime dividing exactly one factor and also dividing \(h\) forbids overlap: its divisibility survives in the other cofactor. If \(h=0\) but \(s\ne t\), exact inert square support also forbids overlap.

For compatible \(h\ne0\), parametrizing the common progression modulo \(s^2t^2/g^2\) gives two affine cofactor forms. At each inert prime away from \(st\) the slopes are units, and the two forbidden classes coincide exactly when the prime divides \(h\). The [upper-bound sieve](https://doi.org/10.1112/jlms.12663) along an interval of length \(X\) divided by a polylogarithmic modulus gives the bound
\[
\ll \frac{Xg^2}{s^2t^2H}\,\mathfrak S(h),\qquad
\mathfrak S(h)=\prod_{\substack{p\mid h\\p\equiv3\bmod4}}\frac{p-1}{p-2}.
\]
The primes dividing \(st\) can be omitted at bounded cost. Uniformly \(\mathfrak S(h)\ll\sqrt{\log H}\) by Mertens in the inert progression and a split at \(H\); the large-prime reciprocal sum is bounded by the log-height of \(h\).

The mean of \(\mathfrak S(h)\) over all unequal actual labels is bounded. For the elementary expansion, dominate each factor by \(1+2/p\) when \(p\ge3\). Discard primes above \(H^2\) at bounded cost as \(\log|h|=O(H)\), and expand the product. Fixing three exponent indices leaves a congruence \(9^e\equiv a\bmod b\) for each squarefree modulus \(b\), excluding 3 at bounded cost. It has at most \(O(H/\operatorname{ord}_b(9)+1)\) solutions. The order-weighted series \(\sum_b 2^{\omega(b)}/(b\,\operatorname{ord}_b(9))\) converges: the support of moduli of order at most \(T\) is contained in the primes of \(\prod_{j\le T}(9^j-1)\); its logarithm is \(O(T^2)\), giving weighted divisor mass \(O((1+\log T)^2)\) by Mertens and a split at \(T^2\). Dyadic division by \(T\) is summable. The endpoint \(+1\) multiplies an Euler product \(O((\log H)^2)\), still \(o(H)\). Thus summing the overlap bound for coprime factors gives the required \(O(XH/(\log H)^4)\).

## Precisely what remains

Let \(E(q)=\sum_{\lambda\ne\mu,\ q^2\mid h}\mathfrak S(h)\) over ordered labels. Counting the partners for each shared prime gives an upper bound
\[
\ll\frac{X}{H^3(\log H)^2}\sum_p E(p)
\]
for distinct factors with one shared prime. The same-factor contribution is at most \(O(XH^{-3}\sum_s E(s))\). Hence sufficient bounds are \(O(H^4/(\log H)^2)\) and \(O(H^4/(\log H)^4)\) on the respective energy sums.

For \(q\) coprime to 15, fixing three exponents and varying the axis of larger order gives
\[
E(q)\ll H^3\sqrt{\log H}\left(1+
\frac H{\max(\operatorname{ord}_{q^2}(9),\operatorname{ord}_{q^2}(5))}\right).
\]
For a shared \(p\asymp\sqrt H\) the desired saving follows for the subfamily with either lifted order \(\ge p^{1+\delta}\), fixed \(\delta>0\). Primes \(p\asymp P\) of order at most \(P^{1/2}/(\log P)^2\) for one specified base number \(O(P/(\log P)^5)\), by the log-height of the product of \(b^j-1\) over those indices. After removing these for both bases, the unresolved shared-prime part is the simultaneous failure to lift. The same-factor estimate is short by a factor \((\log H)^{5/2}\) even if the order exceeds \(H\); a genuinely two-axis collision saving is needed. No positive-fraction or pointwise result is asserted.

## Exact controls

~~~python
from math import gcd, isqrt

def two_squares(m):
    return any(a*a+isqrt(m-a*a)**2==m for a in range(isqrt(m//2)+1))

n=118715
assert n-(3**4+5)==21**2*269==210**2+273**2
assert n-(3**2+5)==33**2*109==99**2+330**2
assert gcd(21,33)**2==9 and n%53361==11993
assert 11993%441==86 and 11993%1089==14

n=101075
h=(3**4+5**7)-(3**4+5)
assert h%9==h%7==0
assert n-(3**4+5)==21**2*229==42**2+315**2
assert n-(3**4+5**7)==33**2*21 and not two_squares(33**2*21)

n=85127
assert n-(3**2+5)==441*193==147**2+252**2
assert n-(3**8+5**7)==441==21**2
assert (3**8+5**7)-(3**2+5)==441*192
assert len({pow(9,e,49) for e in range(21)})==21 and pow(9,21,49)==1
assert len({pow(5,e,441) for e in range(42)})==42 and pow(5,42,441)==1
assert pow(3,42,49)==1 and all(pow(3,2+42*i,441)==9 for i in range(10))
~~~

The last order identities, with the 3-power transient modulo 9 handled separately, show exact fixed-modulus rank deficiency: all actual labels \(3^{2+42i}+5^{1+42j}\) occupy the same class modulo 441, including exponent boxes with a quadratic number of distinct labels. This fixed example does not prove failure for growing semiprime factors.
