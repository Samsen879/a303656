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

## Stronger result: a positive lower density via a weighted lattice sieve

**A weighted sieve removes the leading logarithmic loss.** Fix \(0<\eta<1/2\). For every sufficiently large odd \(U\), put \(Q=5^{2U}\) and choose any set of at least \(\eta U\) odd labels \(V\in[1,U]\). The four-square construction gives **\(\gg_\eta Q\) distinct targets on that one layer in each of \(69,117,27,99\bmod120\)**. The proof uses a split-prime sieve on the actual lattice and a bounded weight per label. The key local identity holds even at split primes dividing the lattice target.

### A label weight with a bounded diagonal

Put \(Z=9^V\). For \(L=1,3\), keep the original equations and constraints
\[
P=n-Q-(4-L)Z=u^2+v^2,\qquad
S=5Q+LZ-n=x^2+y^2,\qquad
4\mid v,\quad 2\mid y,\quad 3\nmid uvxy .
\]
Write \(N=P+S=4Q+(2L-4)Z\). Requiring \(5\mid u,v\) gives classes \(117,99\bmod120\) for \(L=1,3\), respectively. Requiring \(5\mid x,y\) gives \(69,27\bmod120\). In each branch also require that the norm on the scaled side has \(5\)-adic valuation exactly two. The true positive label remains \((2V+1,2U)\) for \(L=1\) and \((2V,2U)\) for \(L=3\).

Give each witness weight \(2^{-\Omega_+(P)-\Omega_+(S)}\), where \(\Omega_+\) counts primes \(1\bmod4\) with multiplicity. If \(W_V(n)\) is the resulting weight at one target and label, then
\[
0\le W_V(n)\le16.
\]
Indeed, the unrestricted representation count is \(r_2(P)r_2(S)\), and each split-prime factor satisfies \(e+1\le2^e\). The main step is to prove \(\sum_n W_V(n)\gg Q/\log Q\) uniformly in \(V\) and the branch.

### Exact local cancellation and the first moment

At a split prime \(p>5\), a binary norm becomes a product of two variables by an invertible local change of coordinates. Its density at \(t\ne0\) is
\[
d_p(t)=(1-p^{-1})(v_p(t)+1).
\]
Give \(t\) local weight \(\sigma_p(t)\) equal to \(1,1/2,0\) according as \(v_p(t)=0,1,\ge2\). Then \(d_p(t)\sigma_p(t)=(1-p^{-1})\mathbf1_{p^2\nmid t}\). On the fiber \(P+S=N\), the unnormalized weighted density is exactly
\[
\int_{\mathbb Z_p}d_p(t)d_p(N-t)\sigma_p(t)\sigma_p(N-t)\,dt
=(1-p^{-1})^2\left(1-\frac2{p^2}+\frac{\mathbf1_{p^2\mid N}}{p^2}\right). \tag{1}
\]
Thus even when the two residues coincide modulo \(p\), the first-order term stays \(1-2/p\).

Here are the sieve precision and error. For a lattice witness, mark each split \(p\le z,\ p>5\) independently with probability \(1-\sigma_p(P)\sigma_p(S)\). This is a finite weighted sieve sequence: avoidance has weight \(\prod_{p\le z}\sigma_p(P)\sigma_p(S)\), and the count attached to a squarefree \(d\) uses the product of marking probabilities for \(p\mid d\).

Each condition \(p^j\mid ab\), for \(j=1,2\), is a union of the \(j+1\) homogeneous sublattices \(p^i\mid a,\ p^{j-i}\mid b\). At a point the admissible \(i\)'s are consecutive, so the union indicator equals the sum of the indicators minus the sum of adjacent intersections. The largest index is \(p^{j+1}\). Since \(\sigma_p(t)=1-\tfrac12\mathbf1_{p\mid t}-\tfrac12\mathbf1_{p^2\mid t}\), the marking probability uses at most \(82\) signed terms of index at most \(p^6\). For \(d\) the index is \(O(d^6)\), and the number of terms is at most \(82^{\omega(d)}\le d^2\).

For a sublattice of index \(h\), the Gram determinant and level are \(O(h^2)\). The general quaternary cusp-coefficient bound gives \(O(Q^{9/16}h^4)\) here. A form with content \(c\) is divided by \(c\) together with \(N\), or contributes zero when \(c\nmid N\). The real index factor cancels the local change of variables in the density main term. The fixed conditions at 3 and 5 use finite inclusion–exclusion. Thus the total error through sieve level \(D=Q^{1/100}\) is
\[
O\!\left(Q^{9/16}\sum_{d\le D}d^{26}\right)=O(Q^{0.8325}).
\]
[Rouse, Theorem 3 and the general (not coprime-level) coefficient bound in §5](https://arxiv.org/pdf/1802.03437#page=10)

The ambient densities at \(2,3,5\) are \(1,16/27,64/125\). At 5 the unscaled side has unit norm, and the two split coordinates on the scaled side must be units, giving \((4/5)^3\). At \(p>5\), the ambient density is \(\beta_p(N)=(1-p^{-2})\sum_{j=0}^{v_p(N)}p^{-j}\), between \(1-p^{-2}\) and \(1+p^{-1}\). Dividing (1) by \(\beta_p(N)\) gives the conditional survival probability, at least \(1-5/p\). The sieve dimension condition holds uniformly, for example with dimension \(10\). The lower-bound fundamental lemma therefore applies with \(z=D^{1/s_0}\) for a sufficiently large **fixed** \(s_0\). Its main term is \(\gg Q/\log z\). Indeed, (1) replaces the ambient factor at each sieved split prime, giving \(\prod_{p\le z,\ p\equiv1(4)}(1-1/p)^2\asymp1/\log z\) up to bounded factors. The unsieved ambient factors have a uniformly positive lower product. [Friedlander–Iwaniec, *Opera de Cribro*, Lemma 6.11](https://bookstore.ams.org/coll-57) · [Weighted formulation, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

On the surviving witnesses, the factor at 5 is \(2^{-2}\), and the number of split prime factors above \(z\), with multiplicity, is at most \(\log(PS)/\log z=O_{s_0}(1)\). Hence the full weight is bounded below by a fixed multiple of the sieve weight. Restricting to \(Q+3\cdot 9^U<n<5Q\) discards at most \(O(\sqrt{9^UQ}(1+\log Q)^{15/2})=o(Q/\log Q)\) even in unweighted witnesses. To see this, one endpoint forces \(P\le3\cdot9^U\), the other forces \(S\le3\cdot9^U\), and Cauchy–Schwarz uses \(\sum_{j\le N}r_2(j)^4\ll N(1+\log N)^{15}\). This proves the first moment at the original ordinary height.

### Cross-label collisions and distinct targets

For \(V\ne W\), the four integer roots are \(Q+(4-L)9^i,\ 5Q+L9^i\) for \(i=V,W\). Let \(\Delta\) be the product of their six differences. An elementary upper sieve detects a necessary condition for all four residuals to be norms. At an inert prime \(p>7\) with \(p\nmid\Delta\), the forbidden exact-valuation-one classes number \(4(p-1)\) modulo \(p^2\). At the remaining primes the product loses at most \(F_C(\Delta)=\prod_{p\mid\Delta}(1+C/p)\). CRT gives remainder \(O(4^{\omega(d)}d)\) at squarefree \(d\), so the upper sieve at the same fixed-power level gives
\[
\sum_n W_V(n)W_W(n)\ll \frac{Q}{(\log Q)^2}F_C(\Delta).
\]
The upper sieve uses only nonnegative mass and a necessary inert-prime condition; its remainder through a fixed small power of Q is negligible. See also [Tao–Teräväinen, Lemma 3.2](https://doi.org/10.1112/jlms.12663) for the elementary sieve framework.

The mean of \(F_C(\Delta)\) over the actual label pairs is bounded. For each nonzero difference \(m\), \(\log|m|=O(U)\). Discard its prime factors above \(U^\delta\) at bounded cost. In the remaining divisor expansion with weights \(C^{\omega(d)}/d\), the mean of \(\log d\) is \(O_C(\delta\log U)\). For small fixed \(\delta\), at least half the weight has \(d\le U\). Away from 2 and 3, each divisor condition is \(81^i\equiv a\bmod d\) after fixing the other label when present. This uses \(V=2i+1\) and applies to the mixed differences \(4Q+L9^W-(4-L)9^V\) as well. The average fraction is \(O(1/\operatorname{ord}_d(81)+1/U)\). The order-weighted divisor sum converges by dyadic summation, since all squarefree \(d\) of order at most \(t\) divide \(\prod_{j\le t}(81^j-1)\), whose logarithm is \(O(t^2)\). Hölder then combines the six differences. The sum of the cross-label contributions is \(O(Q)\).

In one branch let \(R(n)=\sum_VW_V(n)\) and \(H=\sum_nR(n)\). The first moment gives \(H\gg_\eta Q\), and the diagonal and cross bounds give \(\sum_nR(n)^2\le16H+O(Q)\). Therefore \(|\{n:R(n)>0\}|\gg_\eta Q\). On one layer this is a positive proportion of **distinct generated targets**. Taking the largest odd \(U\) with \(5Q\le X\) also gives positive lower density up to \(X\) in each branch, since successive \(Q\)'s have ratio \(625\). Density one and the prescribed-\(n\) conjecture remain open.

### Independent exact replay

This checks the weighted identity at an actual split prime at depths 0, 1, and 2, and the four parity branches with the exact extra valuation restriction at 5.

~~~python
Q, p = 5**22, 41
m, phi = p*p, p*p-p
def fiber(t):
    return m+2*phi if t == 0 else phi*(1+(t%p == 0))
def twice_weight(t):
    return 0 if t == 0 else 2-(t%p == 0)
for V, e in ((1,0), (7,1), (3,2)):
    N = 4*Q+2*9**V
    assert N%p**e == 0 and N%p**(e+1)
    a = [fiber(t)*twice_weight(t) for t in range(m)]
    assert sum(a[t]*a[(N-t)%m] for t in range(m)) == 4*phi**2*(m-2+(e==2))

for L,r,n,u,v,x,y in (
    (1,117,2384279934231477,290465,98860,75434239,62018744),
    (1,69,2384279934201909,120311,282256,93905785,26802100),
    (3,99,2384279934211059,220055,213820,72333623,65608658),
    (3,27,2384279934289827,210463,223268,45114335,86610310),
):
    P,S = u*u+v*v,x*x+y*y
    assert n == Q+(4-L)*9+P == 5*Q+L*9-S
    assert Q+3*9**11 < n < 5*Q and n%120 == r
    assert v%4 == y%2 == 0 and all(t%3 for t in (u,v,x,y))
    a,b = (u,v) if r in (117,99) else (x,y)
    assert a%5 == b%5 == 0 and (a*a+b*b)%125
~~~
