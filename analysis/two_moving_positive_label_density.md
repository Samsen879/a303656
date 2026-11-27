# Positive lower density of targets with two positive labels on both moving axes

Fix \(0<\eta<1/2\). For all sufficiently large odd \(U\), put \(Q=5^{2U}\) and choose any set of at least \(\eta U\) odd labels \(V\in[1,U]\). There are \(\gg_\eta Q\) distinct \(n\equiv36\pmod{120}\) in \(Q<n<5Q\) with true positive representations at both
\[
(c,d)=(2V,2U),\qquad (2V+1,2U-1)
\]
for some chosen \(V\). The new determinant can share primes with the pivot. Restricting to coprime pivots restores the box count, and the resulting loss has bounded mean over the actual labels.

### Congruence-box audit

Write \(T=5^U,\ Z=9^V,\ h=2Z-4Q/5\). Use
\[
ab+cd=h,\qquad a,c,d\in I=[T,11T/10),\qquad
(a,b,c,d)\equiv(79,43,81,41)\pmod{120},\qquad (a,h)=1.
\]
With \((u,v,x,y)=(a+b,c+d,b-a,d-c)/2\), put \(P=u^2+v^2\) and \(S=x^2+y^2\). Then \(P-S=h\) and
\[
n=Q+Z+P=Q/5+3Z+S.
\]
The base congruence gives \(n\equiv36\bmod120\) and both norms are units at 5. Since \(b=(h-cd)/a\) and \(Z/Q=o(1)\) uniformly for \(V\le U\), the box gives \(P,S\asymp Q\) and \(Q<n<5Q\).

For a compatible residue class \(\rho=(a_0,b_0,c_0,d_0)\bmod m\) extending the base class, assume \(m\le T\) and \((a_0,h,m)=1\). With the same pivot restriction, its box count is
\[
\frac{|I|^2\log(11/10)}{m^3}
\prod_{p\nmid mh}(1-p^{-2})
\prod_{\substack{p\mid h\\p\nmid m}}(1-p^{-1})
+O_\epsilon(T^{3/2+\epsilon}). \tag{1}
\]
The constants are uniform for the determinants here. A class with \((a_0,h,m)>1\) contributes zero.

For the shared-prime case, fix an admissible \(a\), let \(m_1\) be the full part of \(m\) supported on primes dividing \(a\), and put \(m_2=m/m_1,\ q=am_1,\ K=h-ab_0\). Then \(K\) is a unit modulo \(q\). Given the prescribed \(c,d\bmod m\), the \(b\)-condition is equivalent to \(cd\equiv K\bmod q\). Compatibility handles \(b\bmod m_2\), since \(a\) is a unit there.

Complete the progressions \((c-c_0)/m_1,(d-d_0)/m_1\bmod a\), whose step \(m_2\) is a unit. The complete sum at frequencies \(r,s\bmod a\) is, up to a unit phase,
\[
\frac1{m_1}\sum_{j\bmod m_1}e_{m_1}(-jc_0)S_q(r+ja,sK).
\]
Here \(\gcd(r+ja,sK,q)\mid m_1\gcd(r,s,a)\). The Weil bound gives \(O(\tau(q)m_1\sqrt a\,\gcd(r,s,a)^{1/2})\). The normalized interval completion costs \(O_\epsilon(a^\epsilon)\) away from the zero pair: on nonzero frequencies divisible by \(k\mid a\), the sum of absolute Fourier coefficients is \(O((a/k)\log a)\). Summing against the gcd weight costs \(O(\log^2a\sum_{k\mid a}k^{-1/2})\). Thus the total nonzero-frequency error is \(O_\epsilon(T^{3/2+\epsilon})\), using \(m_1\le m\) and \(O(T/m+1)\) choices of \(a\). [Weil’s bound](https://pmc.ncbi.nlm.nih.gov/articles/PMC1079093/)

The zero pair has \(\varphi(q)/\varphi(m_1)\) choices, so after normalization its factor is \(a^{-1}\prod_{p\mid a,\ p\nmid m}(1-1/p)\). Expanding this product and using Möbius inversion for \((a,h)=1\) gives (1). Each harmonic progression contributes its integral divided by its modulus, with error \(O(1/T)\); the summed error before the two interval lengths are inserted is \(O(\tau(|h|)\log T/T)\). This also verifies the previous box formula: for \(h=2\cdot9^V\), every prime dividing \(h\) is already fixed by the base class. Sharing a prime with \(m\) is covered by the completion. Sharing a prime with \(h\) can make \(K\) a nonunit, as the actual boxed control below shows.

### What the new determinant costs

At \(p>5\), the ambient density in the coprime-pivot chart is
\[
\beta_p^*=
\begin{cases}
1-p^{-2},&p\nmid h,\\
1-p^{-1},&p\mid h.
\end{cases}
\]
For \(p\mid h\), the unpruned density is \((1-p^{-2})\sum_{j=0}^{v_p(h)}p^{-j}\), obtained by grouping first rows \((a,c)\) by their common valuation. Thus the exact fraction retained by requiring \(a\) a unit is \(\beta_p^*\) divided by that density.

At an **inert divisor of \(h\)**, the surviving chart forces both residuals to be units. Indeed,
\[
4a^2P\equiv(a^2+c^2)(a^2+d^2)\pmod p,
\]
and neither factor can vanish. Relative to the unit-determinant ambient factor, the cost is \(p/(p+1)\).

At a **sieved split divisor of \(h\)**, give each norm weight \(1,1/2,0\) at valuations \(0,1,\ge2\). Conditional on the unit pivot, the exact product-weight means are
\[
w_p=
\begin{cases}
1-3/p+4/p^3,&v_p(h)=1,\\
1-3/p+1/p^2+2/p^3,&v_p(h)\ge2.
\end{cases}
\]
To see this, the two coordinates \(c,d\bmod p\) each have two roots of \(t^2=-a^2\). With neither root hit, both norms are units. With exactly one hit, the next digit of \(P\) is uniform, and one or two digits are forbidden according as \(p^2\mid h\) or \(p^2\nmid h\). At a double hit, \(P\equiv0\) or \(h\bmod p^2\), so the weight is zero. At a split \(p\nmid h\), the combined ambient and sieve factor is \((1-1/p)^2(1-2/p^2)\). Consequently the combined factor at a split divisor of \(h\) costs \(1-2/p+O(p^{-2})\) relative to that factor.

### First moment and collision mean

For squarefree sieve \(d\), sum (1) over compatible classes modulo \(m=120d^2\), using the split marking weights. There are at most \(m^4\) classes and the weights lie in \([0,1]\). Through \(D=Q^{1/200}\) the total remainder is \(O(Q^{41/50})\), taking \(\epsilon=1/20\) in (1). The lower fundamental lemma applies to a sufficiently small fixed power of \(Q\): the local survival probabilities are at least \(1-4/p\) at the sieved primes. Its main term is
\[
\gg \frac{Q}{\log Q}\,F_C(|h|)^{-1},
\qquad F_C(m)=\prod_{p\mid m}(1+C/p).
\]
The bound is uniform, including the sieve remainder, since \(F_C(|h|)\ll(\log\log Q)^C\). The unsieved split factors have bounded multiplicity in \(PS=O(Q^2)\) above the fixed-power sieve range. Thus the same lower bound holds for the full witness weight \(2^{-\Omega_+(P)-\Omega_+(S)}\). The weight at one target and label is at most \(16\), by \(r_2/4\) and \(e+1\le2^e\). [Weighted lower sieve, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

Both \(F_C(|h|)\) and the collision factor have bounded means. The four roots for \(V\ne W\) are \(Q+9^i,\ Q/5+3\cdot9^i\) for \(i=V,W\), and are distinct for large \(U\). An inert-prime upper sieve bounds their common weight by \(O(QF_C(\Delta)/\log^2Q)\), where \(\Delta\) is the product of the six differences. At a good inert prime the four roots forbid exactly \(4(p-1)\) classes modulo \(p^2\).

For the averaging, each determinant or root difference has logarithmic size \(O(U)\). In the expansion of \(F_C(m)\), primes above \(U^\delta\) cost a bounded factor, and the remaining divisor weights can be truncated at \(d\le U\) by bounding their mean \(\log d\) by \(O_C(\delta\log U)\). Away from 2 and 3, each divisibility condition reduces to \(81^j\equiv r\bmod d\) after fixing the other label if present. Its mean is \(O(1/\operatorname{ord}_d(81)+1/U)\). The order-weighted divisor sum converges by dyadic summation, since divisors of order at most \(t\) divide \(\prod_{j\le t}(81^j-1)\). Hölder combines the six differences. Cauchy–Schwarz on the reciprocal determinant factors now gives total first moment \(\gg_\eta Q\), and the summed cross weight is \(O(Q)\). The diagonal is at most 16 times the first moment, so a final Cauchy–Schwarz gives \(\gg_\eta Q\) distinct targets.

This is a positive lower density statement for the generated family in class \(36\bmod120\). Taking the largest odd \(U\) with \(5Q\le X\) preserves that lower density up to \(X\). No conclusion about prescribed targets follows.

### Independent exact replay

The first target verifies two true labels with both powers changing, including a shared-modulus unit pivot; the second tests a genuinely nonunit pivot. The nearby target tests odd valuation at 7. The last block directly enumerates the weighted split local law at both determinant depths.

~~~python
from math import gcd

def check(U,V,box,n):
    a,b,c,d = box
    T,Z = 5**U,9**V
    Q,h = T*T,2*Z-4*T*T//5
    assert tuple(t%120 for t in box) == (79,43,81,41)
    assert all(T <= t and 10*t < 11*T for t in (a,c,d))
    assert a*b+c*d == h
    u,v,x,y = (a+b)//2,(c+d)//2,(b-a)//2,(d-c)//2
    assert n == Q+Z+u*u+v*v == Q//5+3*Z+x*x+y*y
    assert Q < n < 5*Q and n%120 == 36
    return Q,Z,h,u,v

a,b,c,d = box = (1953199,-3737117,2005881,2117561)
Q,Z,h,u,v = check(9,3,box,8860981605876)
m1 = 41**2
K = h-a*(b%(120*m1))
assert a%41 == 0 and gcd(a,h) == gcd(K,a*m1) == 1
assert (c*d-K)%(a*m1) == 0
bad = Q+Z+(u+120)**2+v*v
assert Q < bad < 5*Q and bad%120 == 36
assert (bad-Q//5-3*Z)%49 == 7

a,b,c,d = box = (83359,-138437,83001,80321)
_,_,h,_,_ = check(7,7,box,13535214036)
assert gcd(a,h) == 31
assert (h-a*(b%(120*31**2)))%31 == 0


from fractions import Fraction
def wt(n,p):
    return 0 if n%p**2==0 else (1 if n%p==0 else 2)
p=13
r=p*p
J=pow(2,-1,r)
for h in [p,p*p]:
    w=0
    for c in range(r):
        for d in range(r):
            b=(h-c*d)%r
            P=((1+b)*J)**2+((c+d)*J)**2
            S=((b-1)*J)**2+((d-c)*J)**2
            w += wt(P,p)*wt(S,p)
    bound=Fraction(1)-Fraction(3,p)+(Fraction(4,p**3) if h==p else Fraction(1,p*p)+Fraction(2,p**3))
    assert Fraction(w,4*r*r)==bound
print("pivot controls and both local split divisor densities passed")
~~~
