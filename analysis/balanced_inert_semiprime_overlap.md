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

## Sharper conditional reduction: joint unit-gap projections

I obtained a conditional reduction for the balanced \(pq\) layer at \(a=1\). On all but \(o(1)\) of the balanced prime pairs, elementary order estimates give the joint order needed to control **nonunit differences**, provided the orders lift at both primes. The remaining estimate is a simultaneous discrete-log test on two exponent gaps. I did not prove the required bound for that test or a density statement about order lifting.

### A joint order bound for almost all pairs

Put \(H=\log X\), \(P=\sqrt H\), and take distinct inert primes \(p,q\in[2P,3P]\). For either \(b=9\) or \(b=5\), write \(r_p=\operatorname{ord}_p(b)\). Then, for all but \(o(1)\) of these pairs,
\[
r_p,r_q\ge \frac{P^{1/2}}{(\log P)^2},
\qquad
\operatorname{lcm}(r_p,r_q)>P^{7/10}.
\]
This assertion concerns orders modulo primes and uses no lifting hypothesis.

For the first inequality, all primes with order at most \(T\) divide \(\prod_{j\le T}(b^j-1)\), whose logarithm is \(O(T^2)\). For the second, fix a prime \(p\) satisfying the first inequality. If the least common multiple is at most \(P^{7/10}\), then \(q\) divides one of \(b^{r_pj}-1\) with \(j\le P^{7/10}/r_p\). The logarithm of their product is \(O(P^{7/5}/r_p)=O(P^{9/10}(\log P)^2)\). It has \(o(P/\log P)\) prime divisors in \([2P,3P]\), uniformly in \(p\). The prime number theorem in the inert progression gives the claimed pair count. [Davenport, *Multiplicative Number Theory*](https://link.springer.com/book/9780387950976)

### Reduce the energy to two unit gaps

Let \(M=(pq)^2\), and use consecutive exponent ranges of length \(\asymp H\) for the actual labels \(9^e+5^d\). For base \(b\), its one-axis difference energy counts
\[
b^i(b^k-1)\equiv b^j(b^\ell-1)\pmod M,
\]
with the starting exponents and signed gaps in the permitted ranges.

Suppose the order of \(b\) lifts at both primes and the joint order bound above holds. The terms with a nonunit difference cost \(O(H^{59/20})\), as follows.

- If the differences are divisible by just one of \(p,q\), both gaps are multiples of the order at that prime. There are \(O((H/r_p)^2)\) choices for the gaps when that prime is \(p\). For each choice, the order modulo \(q^2\) leaves \(O(H(1+H/(qr_q)))\) starting pairs. This costs \(O(H^{11/4}(\log H)^6)\), with the same estimate after interchanging the primes.
- If both primes divide the differences exactly once, put \(r=\operatorname{lcm}(r_p,r_q)\). Both gaps are multiples of \(r\), and after division the starting-exponent congruence is modulo \(pq\), with order \(r\). The cost is \(O(H^4/r^3)=O(H^{59/20})\).
- If either prime square divides the differences, both gaps are multiples of the lifted order at that prime. Counting all starting pairs costs \(O(H^{5/2}(\log H)^4)\). The zero-gap diagonal costs \(O(H^2)\).

For unit differences, define \(A_b(p,q)\) to count ordered signed gap pairs \((k,\ell)\) such that
\[
\frac{b^k-1}{b^\ell-1}\equiv b^t\pmod{p^2q^2}
\]
for some \(t\) in the actual range of starting-exponent differences. This is a simultaneous projection test. The ratio must lie in the cyclic subgroup at both prime squares, and its two local discrete logs must agree modulo the gcd of the two orders. The resulting CRT class must meet the allowed interval for \(t\).

The lifted order modulo \(M\) exceeds the exponent range, so a qualifying gap pair costs \(O(H)\) starting pairs. Thus the one-axis energy is \(O(H A_b(p,q)+H^{59/20})\).

**Explicit sufficient condition.** Retain \(\asymp H/(\log H)^2\) balanced pairs satisfying the joint order bounds and with **both bases lifting at both primes**. If this retained family satisfies
\[
\operatorname{mean}_{p,q} A_9(p,q)\ll H^2/(\log H)^5,
\]
then the same-factor contribution meets the second-moment budget. Indeed, Cauchy–Schwarz on the two difference histograms bounds the mixed label energy by the geometric mean of their one-axis energies. The \(5\)-axis has the elementary \(O(H^3)\) bound from injectivity, so the mean mixed energy is \(O(H^3/(\log H)^{5/2})\). Multiplying by the uniform inert sieve correction \(O(\sqrt{\log H})\) gives \(O(H^3/(\log H)^2)\) per factor on average. The sieve bound for two genuine norm cofactors then gives the required aggregate \(O(XH/(\log H)^4)\). The lifted orders also give the shared-prime saving on this retained family. Together with the coprime contribution and the first moment, these hypotheses would give positive-fraction **distinct-target** coverage. They would leave pointwise coverage open. [Tao and Teräväinen, sieve upper bound, Lemma 3.2](https://doi.org/10.1112/jlms.12663) · [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### Independent exact replay

Both marginal discrete logs exist at the two prime squares but disagree modulo the shared order. The same semiprime separately gives a true positive target.

~~~python
from decimal import Decimal, localcontext
from math import gcd
p,q=7,19
a=9
M=p*p*q*q
x=(a-1)*pow(a**7-1,-1,M)%M
assert x==617 and gcd((a-1)*(a**7-1),M)==1
def cycle(mod):
    C=[1]
    while C[-1]*a%mod != 1:C.append(C[-1]*a%mod)
    return C
u,v=cycle(49),cycle(361)
assert (len(u),len(v))==(21,171)
i,j=u.index(x%49),v.index(x%361)
assert (i,j)==(9,64) and (i-j)%gcd(len(u),len(v))!=0
n=937531
with localcontext() as ctx:
    ctx.prec=60
    y=Decimal(n)
    assert 70<y.sqrt()/y.ln()<71
assert n-(3**2+5)==133**2*53==266**2+931**2
assert 53<71*79 and 53%4==1
~~~

## Joint four-term base-nine catalogue and short-span savings

The base-\(9\) unit-gap test reduces exactly to counting **pairs of prime squares dividing the same four-term integer**. This removes the need to estimate marginal discrete logs separately. It also gives an unconditional saving for every configuration with normalized exponent span at most \(H^{3/5}/(\log H)^{1+\eta}\), where \(H=\log X\) and \(\eta>0\) is fixed. I did not obtain the required bound for the longer configurations or positive-fraction coverage at \(a=1\) without the lifting hypotheses.

### Exact prime-square reduction

For the base-\(9\) axis, count collisions of positive differences \(9^{i+k}-9^i\) and \(9^{j+\ell}-9^j\) in an exponent interval of length \(N\asymp H\). Interchange the two differences if needed so that \(t=j-i\ge0\). Define
\[
D(k,\ell,t)=9^k-1-9^t(9^\ell-1),
\qquad w=\max(k,t+\ell).
\]
For inert primes \(p,q\asymp\sqrt H\), the exact simultaneous unit test is
\[
p^2q^2\mid D(k,\ell,t),\qquad
\gcd\!\big((9^k-1)(9^\ell-1),pq\big)=1.
\]
For a given triple, there are exactly \(N-w\) starting positions when \(w<N\). The starting-exponent shift disappears because \(9\) is invertible modulo \(p^2q^2\). Negative differences have the reflected histogram, so Cauchy–Schwarz controls opposite-sign collisions from the same positive-difference energy. The zero differences contribute their own diagonal.

For any chosen set of layer primes, let \(r(D)\) count primes in the set whose squares divide \(D\) and which pass the unit test. A nonidentity triple contributes to exactly \(\binom{r(D)}2\) unordered prime pairs. Thus the aggregate positive unit energy is a sum of
\[
(N-w)\binom{r(D)}2
\]
over this catalogue, with the orientation factor for \(t>0\) and the elementary identity diagonal handled separately. Here \(D=0\) only for \(t=0,\ k=\ell\), by uniqueness of the base-\(9\) digits in \(9^k+9^t=1+9^{t+\ell}\). The reduction uses no order lifting. It counts solutions with the same exponent displacement at both prime squares.

### Short spans fit the second-moment budget

For nonzero \(D\) of span \(w\), \(\log|D|\ll w\). Each counted prime square uses \(\asymp\log H\) of this logarithm, so \(r(D)\ll w/\log H\). There are \(O(W^3)\) triples of span at most \(W\). Their total unweighted contribution across prime pairs is therefore
\[
O\!\left(\frac{W^5}{(\log H)^2}\right).
\]
At \(W=H^{3/5}/(\log H)^{1+\eta}\), this is \(O(H^3/(\log H)^{7+5\eta})\). Multiplication by at most \(N\) starting positions gives \(O(H^4/(\log H)^{7+5\eta})\) in aggregate one-axis energy, below the \(O(H^4/(\log H)^7)\) budget from the previous reduction.

Three elementary parts of the catalogue also reduce to one order test. For \(t=0\), the congruence tests \(k-\ell\). For \(k=t+\ell\), it tests \(t\). For \(k=\ell\), the factorization \(D=(1-9^t)(9^k-1)\) and the unit condition again reduce it to \(t\). If \(\operatorname{ord}_{p^2q^2}(9)>N\), these parts give only the identity diagonal.

A sufficient remaining estimate is
\[
\sum_{\substack{W<w<N\\D\ne0}}
\binom{r(D)}2\ll \frac{H^3}{(\log H)^7}
\]
on a retained family of \(\asymp H/(\log H)^2\) factors. With the previous lifted-order bounds for nonunit differences and shared primes, this would supply the same-factor estimate needed for positive-fraction **distinct-target** coverage. The size argument alone gives only \(O(H^5/(\log H)^2)\) at full span. The missing input is control of *co-occurring square divisors* in the long catalogue. The exact reduction does not settle that estimate or remove the separate shared-prime and nonunit costs for an unlifted family. [Tao and Teräväinen, sieve upper bound, Lemma 3.2](https://doi.org/10.1112/jlms.12663) · [Repository status](https://github.com/Samsen879/a303656/blob/main/STATUS.md)

### New exact control

For \(p=7,\ q=19\), the modulus is \(17689\). The triple \((40,4,9)\) gives a genuine simultaneous **unit** collision
\[
9^{40}-1\equiv 9^{13}-9^9\pmod{17689}.
\]
In contrast, \((1,10,0)\) passes both tests modulo the primes, with both differences units, but \(D\equiv532=4\cdot7\cdot19\bmod17689\). Both prime valuations are exactly one. This directly checks why ordinary prime divisors cannot substitute for prime squares in the catalogue.

The same factor gives a separate positive certificate at \(n=1079043\), with actual label \((c,d)=(2,1)\):
\[
1079043-(3^2+5)=133^2\cdot61=665^2+798^2.
\]
The \(a=1\) screen is \(74\), and the stripped cofactor \(61\) is below \(79\cdot83\). The following arithmetic checks replay the exact controls.

```python
from math import gcd, log, isqrt

def D(k, ell, t):
    return 9**k - 1 - 9**t * (9**ell - 1)

M = 133**2
for k, ell in [(40, 4), (1, 10)]:
    assert gcd((9**k - 1) * (9**ell - 1), M) == 1

assert D(40, 4, 9) % M == 0
assert D(1, 10, 0) % M == 532
assert all(D(1, 10, 0) % p == 0 and D(1, 10, 0) % p**2 != 0
           for p in (7, 19))

n = 1079043
assert n - 3**2 - 5 == M*61 == 665**2 + 798**2
B = int(n**0.5 / log(n))
inert = [p for p in range(3, 100, 4)
         if all(p % j for j in range(2, isqrt(p) + 1))]
assert B == 74 and [p for p in inert if p > B][:2] == [79, 83]
assert all(61 % p for p in inert if p <= B) and 61 < 79*83
```