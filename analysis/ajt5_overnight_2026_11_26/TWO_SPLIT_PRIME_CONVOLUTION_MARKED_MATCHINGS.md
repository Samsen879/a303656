# Unconditional two-prime convolution markings and growing true anchor matchings

An unconditional two-prime marking reaches **every fixed open subinterval of the original \(2/3<\log p/\log B<3/4\) band** and gives growing distinct-axis matchings at the same integer target. For every sufficiently large even \(a,b\) in the original balance strip, it gives \(\gg B/(\log B)^{3/2}\) distinct targets, each with the true anchor and \(\gg\sqrt{\log B}\) alternative true norms with no repeated exponent on either axis. The signed comparison covers the **42 blocked phases**. The whole-grid sign remains open.

The cubic cyclotomic proposal puts the second exponent at \((b+2)/3>b/3\). The result below keeps the exact cap. Its only common divisor is \(45=6^2+3^2\). The change that recovers the sieve level is to distribute the product of two split primes.

## Exact grid and marked targets

Write \(A=3^a,\ B=5^b,\ S_0=A+25B\) and use
\[
\frac{39}{40}<\frac BA<\frac{122}{125},
\qquad
1457A-123B<n\le729A+625B.
\]
For a compatible label \(S=3^c+5^e\), take
\[
a/10\le c\le a/3,\quad b/5\le e\le b/3,\quad
c\equiv a\pmod4,\quad e\equiv b+2\pmod6.
\]
Then \(\kappa=(S_0-S)/45\) is a positive integer, \(\kappa\asymp B\), and \(8\mid\kappa\). Divisibility follows separately modulo \(5,9,8\). At \(n\equiv0\pmod{49}\), both remainders are units at 7, since each offset is a sum of two nonzero squares modulo 7.

Mark targets by \(n=S_0+45hp\), with primes \(h,p\equiv1\pmod4\). Fix a power interval \(B^{\eta_-}\le h\le B^{\eta_+}\) with \(1/4<\eta_-<\eta_+<1/3\). Its endpoints can be chosen so that all marked \(p\) lie in any given open subinterval of the requested band, since \(hp\asymp B\) throughout the ordinary window. The anchor is a true norm. The alternative is a true norm exactly when \(hp+\kappa\) is, since \(45\) has even valuation at every inert prime.

For the signed comparison take
\[
r_-=3^{a+4}+5^{b+2}+7\pmod{49}.
\]
Among the \(21\) compatible \(c\)-phases modulo 84 and the \(7\) compatible \(e\)-phases modulo 42, each \(e\)-phase has seven \(c\)-phases with \(S\equiv r_-\pmod7\). Across those seven, \(3^c\bmod49\) traverses the seven lifts of its residue because \(3^{12}\) has order 7 modulo 49. Exactly one gives \(S\equiv r_-\pmod{49}\). The other six give exact 7-adic depth one at every target in the \(r_-\) class. These are the 42 blocked phases.

## Forward sieve and reverse count

**Forward.** The unsieved number \(W\) of pairs \((h,p)\) in the window is \(\asymp B/\log B\), by the prime number theorem in the fixed class \(1\bmod4\) and the prime harmonic sum over the chosen power interval for \(h\). For a given label, discard \(h\mid\kappa\). There are \(O(1)\) such \(h\), with negligible total cost.

Apply the unconditional convolution Bombieri–Vinogradov estimate to \(\alpha_h=1\) on the retained split primes in the chosen interval and \(\beta_p=1\) on primes \(1\bmod4\). The lemma permits arbitrary divisor-bounded \(\alpha\) and requires Siegel–Walfisz for \(\beta\) at odd moduli. This holds by imposing \(1\bmod4\) through CRT. At both endpoints of the product window, the supported factors are bounded by \(B^{1-\epsilon}\) for fixed \(\epsilon>0\), so the lemma’s logarithmic factor cutoffs hold. Its error is uniform in the moving restriction \(h\nmid\kappa\). [Kurlberg–Lester–Rosenzweig, Lemma A.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

For a squarefree product \(j\) of inert primes outside \(7\kappa\), \(n\equiv0\pmod{49}\) and \(j\mid hp+\kappa\) specify one reduced class for \(hp\bmod49j\). Every supported product is coprime to \(49j\). The main term is therefore \(W/\varphi(49j)\), with total error \(O(B/(\log B)^L)\) up to sieve level \(D=B^{1/2}/(\log B)^C\), for arbitrarily large fixed \(L\) and suitable \(C\). This is a level at the **product** scale.

Set \(z=B^{1/2-\delta}\), with fixed small \(\delta>0\). Write \(F(w)=\prod_{q>2,\ q\mid w}(q-1)/(q-2)\), with \(F_I,F_+\) its inert and split parts. The half-dimensional lower sieve has \(s=\log D/\log z\ge1+c\delta\) and \(f_{1/2}(s)\gg\sqrt\delta\). Its rough count is
\[
\gg \sqrt\delta\,F_I(\kappa)\frac{B}{(\log B)^{3/2}}.
\]
The local density is \(1/(q-1)\) for inert \(q\nmid7\kappa\). Omitting the inert divisors of \(\kappa\) produces \(F_I(\kappa)\), up to a bounded factor from 7 and \(1+o(1)\) from divisors above \(z\). [Half-dimensional sieve, Theorem 2.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136) · [Explicit \(f_{1/2}\) near \(s=1\)](https://arxiv.org/html/2501.16723v1#S5)

**Reverse.** A rough survivor that fails the norm test has
\[
hp+\kappa=mq_1q_2,\qquad z<q_1<q_2,
\]
with distinct inert primes and split-supported \(m\le C_0B^{2\delta}\). Indeed, \(hp+\kappa\equiv1\pmod4\), \(z^3\gg B\), and a repeated inert prime would have even depth. Also \((mq_1,h\kappa)=1\). A common prime with \(h\) would divide \(\kappa\), and a common prime with \(\kappa\) would have to equal \(h\) or \(p\). The former was discarded and \(p>\max(m,q_1)\).

For fixed \(h,m,q_1\), choose \(mq_1\alpha\equiv\kappa\pmod h\). The exact switch is
\[
q_2=\alpha+ht,\qquad
p=mq_1t+\frac{mq_1\alpha-\kappa}{h}.
\]
The interval for \(t\) is contained in one of length \(T\asymp B/(hmq_1)\gg z/h\), a fixed positive power of \(B\). The forms are primitive, have coprime slopes, and have determinant \(-\kappa\). For odd sieve primes there are two roots except at divisors of \(hmq_1\kappa\), where there is one. The elementary Selberg upper sieve thus bounds the count by
\[
\ll \frac{B}{hmq_1(\log B)^2}\,F(h)F(m)F(q_1)F(\kappa).
\]
For uniformity, one can take weight level \(R=T^{1/20}\) and sieve primes up to \(R^c\) for small absolute \(c\). The truncated Selberg denominator retains at least half its Euler product by the logarithmic mean bound \(\sum_{q\le R^c}\rho(q)\log q/q\le\tfrac12\log R\). The elementary residue-count error is \(O(R^6)\). This upper bound requires no prime distribution in the reverse modulus.

The singular factors cancel in the sum over \(m\). With \(Y=C_0 B^{2\delta}\),
\[
1+\sum_{j\ge1}\frac{F(q^j)}{q^j}=F(q).
\]
Hence the \(m\)-sum is bounded by the split Euler product up to \(Y\) with the primes dividing \(h\kappa\) omitted. Multiplying back \(F(h)F_+(\kappa)\) restores those factors exactly once, since \((h,\kappa)=1\). The factors above \(Y\) are \(1+o(1)\) uniformly. The restored product is \(O(\sqrt{\delta\log B})\). Also \(\sum_{z<q_1\ll\sqrt B}q_1^{-1}=O(\delta)\) and \(\sum_h h^{-1}=O(1)\). Thus the false survivors are
\[
\ll \delta^{3/2}F_I(\kappa)\frac{B}{(\log B)^{3/2}}.
\]
Fix the \(h\)-interval first and then choose \(\delta\) sufficiently small. Subtraction gives the asserted order of true pairs for **each** label, uniformly. Since \(h<p\), each product \(hp\) gives one distinct target.

## Growing matchings at one target

The blocked rectangle \(c\equiv a+4\pmod{84},\ e\equiv b+2\pmod{42}\) contains \(\asymp\log B\) choices on each axis. Pair them in advance to obtain \(K\asymp\log B\) labels with no repeated coordinate. Summing the true-pair lower bound gives \(\gg KB/(\log B)^{3/2}\) incidences across the common pool of \(O(B/\log B)\) marked targets. Targets with fewer than \(c\sqrt{\log B}\) successes account for less than half those incidences when \(c\) is small enough. Each remaining target accounts for at most \(K\), which gives the claimed distinct-target count. This argument uses no independence between labels. In the \(r_-\) class the same labels give zero true alternatives. The other 105 phases could still compensate in the whole-grid count.

## Standalone replay

The first checks use two distinct-axis labels in the exact narrow strip. The smaller fixture lies outside that strip and tests the full marked arithmetic in the stated ordinary window, including primality, the intermediate band, a true alternative, and an exact odd-depth failure.

```python
from math import gcd, isqrt, prod

def shifts(a, b, c, e):
    A, B = 3**a, 5**b
    s0, s = A + 25*B, 3**c + 5**e
    r = (pow(3, a+4, 49) + pow(5, b+2, 49) + 7) % 49
    assert a <= 10*c and 3*c <= a and b <= 5*e and 3*e <= b
    assert (a-c)%4 == (b+2-e)%6 == (s0-s)%360 == 0
    assert (r-s)%49 == 7 and s0%7 and s%7
    return A, B, s0, s, r

for c, e in ((128, 110), (212, 152)):
    A, B, *_ = shifts(712, 486, c, e)
    assert 39*A < 40*B and 125*B < 122*A

def trial(q):
    return all(q % i for i in range(2, isqrt(q)+1))

A, B, s0, s, r = shifts(28, 20, 8, 4)
h, k = 13997, (s0-s)//45
assert h%4 == 1 and trial(h) and k%h
for p, factors, phase in [
    (30473585089, (1319, 120331), 0),
    (30473563709, (1088341561,), r),
]:
    F = prod(factors)
    assert p%4 == 1 and (p-1)%F == 0 and F*F > p
    assert pow(2, p-1, p) == 1
    assert all(trial(q) and gcd(pow(2, (p-1)//q, p)-1, p) == 1
               for q in factors)  # Pocklington
    assert p**3 > B**2 and p**4 < B**3
    n = s0 + 45*h*p
    assert 1457*A-123*B < n <= 729*A+625*B and n%49 == phase
    if phase == 0:
        assert h*p+k == 21681742**2 + 3151367**2
    else:
        assert (n-s)%49 == 7
```

The quoted convolution lemma was checked at the two product-window endpoints: alpha is divisor-bounded and beta satisfies odd-modulus Siegel–Walfisz, so the base 49 modulus and moving h exclusion are permitted. Independent BigInt checked both tight grid labels and both marked Pocklington controls. The theorem compares a matched portion of the originally blocked phases; it does not establish the sign of the distinct true-pair count across all compatible phases.
