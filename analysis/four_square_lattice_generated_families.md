# A four-square lattice with actual two-power labels

There is an explicit sparse but almost linearly growing family of genuine A303656 targets in each of the four classes \(69,117,27,99\bmod120\). This is a lower bound on the size of generated families, not density one, a pointwise construction, or a proof of the conjecture.

Fix odd integers \(1\le V\le U\), and put \(Q=5^{2U}\), \(Z=3^{2V}\). For \(L=1,3\), write \(N_L=4Q+(2L-4)Z\), and take lattice solutions
\[
 u^2+16b^2+x^2+4e^2=N_L,\qquad 3\nmid ubxe.
\]
They give both exact identities
\[
 n=Q+(4-L)Z+u^2+(4b)^2=5Q+LZ-x^2-(2e)^2.
\]
The first is a genuine positive representation with labels \((2V+1,2U)\) for \(L=1\), or \((2V,2U)\) for \(L=3\). The upper expression is a **signed** identity, not a second positive A303656 representation. The height window \(Q<n<5Q\) holds when \(x^2+4e^2>LZ\). Parity in the form forces \(u,x\) odd and \(e\) even for \(L=1\), odd for \(L=3\). The unit condition at 3 gives \(n\equiv0\bmod3\). Thus \(n\equiv21\bmod24\) for \(L=1\), and \(n\equiv3\bmod24\) for \(L=3\).

## Counting in four separate residue classes

Impose \(5\mid u,b\) or \(5\mid x,e\) separately. After rescaling, the fixed diagonal forms have coefficients \((25,400,1,4)\) or \((1,16,25,100)\), respectively, with square-root determinant 200. Since \(Z\equiv-1\bmod5\), the two choices yield classes \(117,69\bmod120\) for \(L=1\), and \(99,27\bmod120\) for \(L=3\).

Use the [Siegel genus formula](https://doi.org/10.2307/1968644) with normalized local densities \(p^{-3k}\) times the number of solutions modulo \(p^k\). For each fixed form the theta series minus its genus average is a weight-two cusp form; its \(N\)-th coefficient is \(O_\epsilon(N^{1/2+\epsilon})\) by Deligne's bound, including the finitely many oldforms (see [Rouse's quaternary theta-series treatment](https://arxiv.org/pdf/1111.0979)). Including or excluding each divisibility by 3 replaces any selected coefficients by nine times themselves, a finite list of fixed forms. At primes other than 3 the changes of variables are by units. The real factor \(3^{-j}\) for \(j\) substitutions cancels the factor \(3^j\) relating the local unrestricted density of the substituted form to the density with those \(j\) coordinates restricted to multiples of 3. This gives the restricted local factor at 3 and the same order of error.

- At 2, the changes from multiplication by 5 are invertible. Here \(N_L\equiv2L\bmod8\). Choose \(u\) odd and the required parity of \(e\), with \(b\) free; the integer for the remaining square is \(1\bmod8\), with four roots modulo each \(2^k\), \(k\ge3\). Both \(u,x\) even is impossible modulo 8. The normalized factor is 1.
- At 3, the 16 unit tuples solve the equation modulo 3 and have a nonzero derivative. The restricted factor is \(16/27\).
- At 5, the unscaled pair is a split binary form representing the nonzero residue \(N_L\bmod5\). There are four such pairs modulo 5 with a nonzero derivative; with the other two variables free, the factor is \(4/5\).
- At each \(p\ge7\), square unit scalings reduce the equation to four squares. The count modulo \(p\) is \(p^3-p\) when \(p\nmid N_L\) and \(p^3+p^2-p\) when \(p\mid N_L\) (the even-dimensional quadratic Gauss sum count). Removing the origin in the latter case still gives a factor at least \(1-p^{-2}\).

The real factor is \(\pi^2 N_L/200\), and multiplying the preceding bounds using \(\prod_p(1-p^{-2})=6/\pi^2\) gives a main term at least \(N_L/45\) for each branch. Uniformity in \(U,V,L\) follows from using the same fixed forms and their 16 restricted variants.

To pass from tuples to distinct targets, group by \(P=u^2+(4b)^2\). The multiplicity \(m(P)\) is at most \(r_2(P)r_2(N_L-P)\). Unit restrictions exclude \(P=0,N_L\). A Cauchy–Schwarz bound and \(r_2(j)\le4\tau(j)\) give
\[
 \sum_P m(P)^2\ll N_L(1+\log N_L)^{15},
\]
using \(\tau(j)^4\le\tau_{16}(j)\) and the standard divisor-sum upper bound (iterated harmonic sums). By another Cauchy–Schwarz bound the interval \(N_L-P\le LZ\) removes only \(O\bigl((ZQ)^{1/2}(1+\log Q)^{15/2}\bigr)=o(Q)\) tuples, uniformly since \(Z\le Q^{\log_5 3}\). A final application to the surviving multiplicities gives \(\gg Q/(1+\log Q)^{15}\) distinct \(n\) in each class. With \(V=U\), successive \(Q\) for odd \(U\) differ by a factor \(625\). Taking the largest with \(5Q\le X\) gives the announced \(\gg X/(1+\log X)^{15}\) bound in each class, with both true exponent labels growing.

## Finite controls

At \((U,V)=(47,19)\) the replay gives one witness in each class. Two other targets meet the signed height identity but have an odd inert valuation in the would-be positive residual. The last check concerns only the separate Eisenstein seed criterion and is not used in the counting proof.

~~~python
from math import isqrt

Q, Z = 5**94, 3**38
for L, r, u, v, x, y in (
    (1,117,988048763976100642871944640241815,20,1021392949540523305053101497576801,436),
    (1,69,993572046962721769137531891352259,4,1016020917530784515268018486740515,1100),
    (3,99,147854353557642485909552296651115,20,1413372918765547125772103070879907,3602),
    (3,27,1419949710346964981345627024638283,8,56804378804459013728916433760395,550),
):
    n = Q + (4-L)*Z + u*u + v*v
    assert n == 5*Q + L*Z - x*x - y*y
    assert v % 4 == y % 2 == 0 and all(w % 3 for w in (u,v,x,y))
    assert ((u % 5 == v % 5 == 0) if r in (117,99) else (x % 5 == y % 5 == 0))
    assert Q < n < 5*Q and n % 120 == r

for L, r, x, y in ((1,117,2324523239,4), (3,27,2324522941,2)):
    n = 5*Q + L*Z - x*x - y*y
    R = n - Q - (4-L)*Z
    assert Q < n < 5*Q and n % 120 == r and R > 0 and R % 49 == 7

p = 815939
assert p % 3 == 2 and all(p % d for d in range(2, isqrt(p)+1))
assert ((5**47 - 3**19)//2) % (p*p) == 83212*p
~~~

## Refinement: aggregate many labels on one layer

Fix \(A>0\) and \(0<\eta<1/2\). For all sufficiently large odd \(U\), put \(Q=5^{2U}\) and take any set of at least \(\eta U\) odd labels \(V\in[1,U]\). In **each** of the four classes \(69,117,27,99\bmod120\), the construction gives
\[
\boxed{\displaystyle
\gg_{A,\eta}\frac{Q}{(\log Q)^{2\log 2-1}}\,
             \exp\!\bigl(A\sqrt{\log\log Q}\bigr)}
\]
distinct targets on the same ordinary layer. The constant and threshold can depend on the fixed \(A\). The new input is a Gaussian lower tail for the split-prime count under the actual lattice witness measure. The argument retains a positive fraction of witness weight at a smaller multiplicity cutoff.

### The multiplicity cutoff

Fix \(L\in\{1,3\}\), put \(Z=9^V\), \((\alpha,\beta)=(4-L,L)\), and write
\[
P=n-Q-\alpha Z=u^2+v^2,\qquad
S=5Q+\beta Z-n=x^2+y^2,\qquad
P+S=N=4Q+(\beta-\alpha)Z .
\]
Keep \(4\mid v,\ 2\mid y,\ 3\nmid uvxy\). The restriction \(5\mid u,v\) gives classes \(117,99\bmod120\) for \(L=1,3\), respectively. The restriction \(5\mid x,y\) gives classes \(69,27\bmod120\). The positive labels remain \((c,d)=(2V+1,2U)\) for \(L=1\) and \((2V,2U)\) for \(L=3\).

In each branch the lattice has \(\gg Q\) witnesses before the height cut. The real density is \(\pi^2N/200\), and the local densities at \(2,3,5\) are \(1,16/27,4/5\). At \(p\ge7\) the density is \((1-p^{-2})\sum_{i=0}^{v_p(N)}p^{-i}\), giving a main term at least \(N/45\). Restricting to \(Q+3\cdot9^U<n<5Q\) removes \(o(Q)\) witnesses uniformly. Each removed endpoint forces \(P\) or \(S\) to be at most \(3\cdot9^U\), so Cauchy–Schwarz with \(\sum_{m\le N}r_2(m)^4\ll N(1+\log N)^{15}\) gives the error \(O(\sqrt{9^UQ}(1+\log Q)^{15/2})\). Both residuals are nonzero on the lattice. [Siegel’s density formula](https://doi.org/10.2307/1968644) · [Rouse, §§2–3](https://arxiv.org/pdf/1111.0979#page=11)

Set \(\ell=\log\log Q\), \(y=Q^{1/\ell^{1/4}}\), and count
\[
X=\sum_{\substack{5<p\le y\\p\equiv1\bmod4}}
       \bigl(\mathbf1_{p\mid P}+\mathbf1_{p\mid S}\bigr).
\]
The congruence counts needed for its moments admit a uniform power saving. At a split prime each binary norm becomes \(ab\) in invertible local coordinates. The event \(p^j\mid ab\) is a union of the homogeneous linear conditions \(p^i\mid a,\ p^{j-i}\mid b\), \(0\le i\le j\). Inclusion–exclusion uses full-rank sublattices. A sublattice of index \(h\) has Gram determinant \(O(h^2)\) and level \(O(h^2)\). Rouse’s general cusp-coefficient bound gives, for example, \(O_\epsilon(Q^{1/2+\epsilon}h^8)\). If a restricted form acquires content \(c\), divide both the form and \(N\) by \(c\) when \(c\mid N\). Otherwise the count is zero. The main term is the original density times the product of the conditional local probabilities, since the real index factor cancels the local change of variables. For any fixed moment order \(k\), all indices are \(y^{O(k)}\), and there are \(y^{O(k)}\) terms. Their total error after normalization is \(Q^{-1/2+\epsilon+o(1)}\). This uses the general cusp bound, which applies even when \(N\) and the level share primes. [Rouse, Theorem 3 and the general coefficient bound in §5](https://arxiv.org/pdf/1802.03437#page=10)

Here is the local calculation behind the limit law. For a split prime \(p>5\), the product of two Haar variables has density \(d_p(t)=(1-1/p)(v_p(t)+1)\) off zero. On the fiber \(P+S=N\), the density in \(P=t\) is proportional to \(d_p(t)d_p(N-t)\). This gives
\[
\Pr(p^j\mid P),\ \Pr(p^j\mid S)\ll(j+1)^2p^{-j}
\]
uniformly in \(N\), by Cauchy–Schwarz on the ball \(p^j\mathbb Z_p\). When \(p\nmid N\), the summand in \(X\) is Bernoulli with probability \(2(2p-1)/(p(p+1))=4/p+O(p^{-2})\). When \(p\mid N\), the two indicators agree and their total mean and variance are \(O(1/p)\). The latter primes change the summed mean and variance by \(O(\log\ell)\), since \(N=O(Q)\).

Consequently the independent local model has mean and variance \(2\ell+O(\log\ell)\). Its cumulants of each fixed order \(k\ge3\) are \(O_k(\ell)\), so its normalized moments converge to the normal moments. The congruence estimate transfers every fixed moment to the integer lattice, uniformly over the labels and branches. In particular, for any fixed \(B>0\), a positive fraction of the lattice witnesses have \(X\le2\ell-B\sqrt\ell\).

The higher prime powers can be removed without losing that fraction. Choose a large fixed \(p_0\) so that the sum of the \(p^2\)-divisibility bounds over \(p>p_0\) is smaller than a quarter of the chosen Gaussian tail. The same sublattice estimate applies simultaneously to the sum over \(p\le y\). At the finitely many smaller split primes, discard sufficiently high fixed exponents. At 5 the scaled side is \(25ab\) and the other side is a unit, so the two free variables on the scaled side are Haar under the local fiber measure. This gives the required fixed cutoff there as well. Finally, primes above \(y\), counted with multiplicity in \(PS\), contribute at most \(\log(PS)/\log y=O(\ell^{1/4})\).

Writing \(f=r_2/4\), the retained witnesses therefore satisfy
\[
\log\!\bigl(16f(P)f(S)\bigr)
   \le (\log2)X+O_B(1+\ell^{1/4}).
\]
Choose \(B>A/\log2\). A positive fraction of each branch’s weight then lies at targets whose entire single-label multiplicity is at most
\[
T=(\log Q)^{2\log2}\exp(-A\sqrt\ell).
\]
The endpoint exclusion still costs \(o(Q)\).

### Corrected Henriot audit and aggregation

For distinct \(V,W\), the actual monic roots are \(a_i=Q+\alpha9^i,\ b_i=5Q+\beta9^i\) for \(i=V,W\). The same-side differences are \(\alpha(9^W-9^V)\) and \(\beta(9^W-9^V)\). The four mixed differences are \(4Q+\beta9^j-\alpha9^i\), all positive. The polynomial height is \(O(Q^4)\) and its discriminant is nonzero with absolute value \(O(Q^{12})\).

Henriot’s corrected **New Theorem 5** applies on the dyadic intervals with interval parameter \(1/2\), height parameter \(1/8\), and growth exponent \(10^{-5}\). For the powers \(f^t\), \(0\le t\le2\), keep \(f^0=\mathbf1_{f>0}\). The bounds \(f(p^j)^t\le(j+1)^2\) and the fixed divisor-function bound give the same growth constants down to \(t=0\). In the corrected congruence count, at a good prime a single positive valuation \(j\) has density \((1-1/p)p^{-j}\). At a bad prime any vector of maximum \(j\) has density at most \(p^{-j}\), including when the correction imposes additional nondivisibility on a zero slot. This gives \(1+O(1/p)\) uniformly in the powers and in the collision depth. The good-prime logarithmic exponent is \(\tfrac12\sum_i2^{t_i}-s\) for \(s\) slots. In particular, four powers equal to one give exponent zero, and the bad factor is at most \((\log\log Q)^C\) from the discriminant size. This uses the upper-bound theorem only. The cutoff itself comes from the lattice distribution, so no moment constant is raised to a power tending to infinity. [Henriot](https://arxiv.org/pdf/1102.1643) · [Corrected theorem](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf/nair-tenenbaum-uniform-with-respect-to-the-discriminant-erratum.pdf)

Let \(R(n)\) sum the retained label weights in one branch, \(M\) be the number of labels, and \(H=\sum_nR(n)\gg_A MQ\). The diagonal contributes at most \(TH\). Removing the cutoff for the cross-label upper bound gives
\[
\sum_nR(n)^2\le TH+O\!\left(M^2Q(\log\log Q)^C\right).
\]
Since \(M\asymp_\eta\log Q\) and \(T\gg_A M(\log\log Q)^C\), Cauchy–Schwarz gives \(\gg H/T\) distinct targets, as claimed.

### Independent exact replay for cross-label collisions and the split-prime law

This verifies the common positive target for `V=1,11`, both non-inclusions with an odd inert valuation, and the finite depth-one local law at `p=41`. The population bound is proved above; it is neither density one nor prescribed-target coverage.

~~~python
Q = 5**22
for n, V, u, v, x, y in (
    (2384279934231477, 1, 290465, 98860, 75434239, 62018744),
    (2384279934231477, 11, 175, 80, 92153879, 32316296),
    (2384279934639477, 1, 272065, 141860, 29965249, 92944784),
    (2384279934229677, 11, 125, 140, 32194339, 92196556),
):
    Z = 9**V
    assert n == Q + 3*Z + u*u + v*v == 5*Q + Z - x*x - y*y
    assert Q + 3*9**11 < n < 5*Q and n % 120 == 117
    assert v % 4 == y % 2 == u % 5 == v % 5 == 0
    assert all(t % 3 for t in (u,v,x,y))

for n, W in ((2384279934639477, 11), (2384279934229677, 1)):
    P = n-Q-3*9**W
    assert P > 0 and P % 49 == 7
assert [j for j in range(1,11) if pow(9,j,25) == 1] == [10]

from collections import Counter
from fractions import Fraction
p=41; Q=5**22
assert [(4*Q+2*9**V)%(p**3) for V in (1,7,3)]==[18732,4633,20172]
M=p*p
f=[0]*M
for x in range(M):
    g=__import__("math").gcd(x,M)
    for t in range(0,M,g):f[t]+=g
N=(4*Q+2*9**7)%M
assert Fraction(sum(f[t]*f[(N-t)%M] for t in range(0,M,p)),sum(f[t]*f[(N-t)%M] for t in range(M)))==Fraction(4*p,(p+1)**2)
print("same-layer controls and conditional split-prime law passed")

~~~
