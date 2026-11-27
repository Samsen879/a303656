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
