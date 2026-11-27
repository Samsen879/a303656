# Allocation-conditioned Gram counts for two relative-angle sectors

This follows [the signed Fejér and Gram factorization](https://github.com/Samsen879/a303656/commit/74d4fe6a0e3128794d33c8899b8df7c88857292e). The allocation calculation is at the level of two actual circle points, so it also upper bounds the original numerical seed collisions. It extends control of very small angles and controls a deep divisible-deficit sector. The remaining intermediate sector, not satisfying the deep divisibility, is expressly left open.

The bounded unit count uses the positive embedding \(x+\sqrt d\,|y|\), which for fixed \(d\) is comparable to \(dX\) throughout the full dyadic target interval. Its allowed multiplicative width is bounded independently of \(X\), so no logarithmic factor from unit powers is needed. When \(d\) is a square, use ordinary difference-of-squares factorization instead; an inert good prime then cannot divide a Gram factor because \(d\equiv-\lambda_\nu^2\bmod p\) would be impossible. At a bad prime the allocation factor follows from the actual shared valuation \(t\), not just from the gcd of the norms. The \(p=5\) true, reflected and \(p=211\) false-deficit controls were independently replayed.

The Gram factor gives an unconditional aggregate bound for a larger part of the relative-angle diagonal. For \(X=2^K\), the diagonal contributes \(O(X)\) from relative angles \(\ll 1/(K\sqrt X)\). There is also a separate estimate inside the intermediate range. If the dot-product deficit is divisible by the least power of \(3\) at least \(X\), the signed contribution from angles up to \(1/K\) is \(O(X(1+\log K)/K^2)\). Both bounds include the extra Gaussian points in the Fejér majorant, so they apply to the original distinct numerical seeds.

### The allocation congruence

For the two actual labels let
\[
 A_i=9^{r_i},\quad B_i=25^{s_i},\quad
 U_i=2A_i+3B_i,\quad D_i=A_i+2B_i,\quad M_i=(n-U_i)^2-D_i^2 .
\]
Keep \(X\le n<2X\) and \(A_i\le B_i,\ B_i^{16}\le n\le A_i^{32}\). Order the labels by \(U_1<U_2\), which also orders \(D_1<D_2\). Put
\[
 e=U_2-U_1,\quad G=D_2^2-D_1^2,\quad H=2n-U_1-U_2,\quad
 L=(n-U_1)(n-U_2)-(D_1^2+D_2^2)/2 .
\]
For Gaussian points of norms \(M_1,M_2\), rotate by a unit to compare the closest directions and write \(\bar z_1z_2=L-j+ih\). The integer \(j\) is positive for large \(X\). In fact,
\[
 M_1M_2-L^2=-eGH/2-e^2(D_1^2+D_2^2)/2-G^2/4<0
\]
and \(L-1<\sqrt{M_1M_2}<L\). With \(d=2j\) and \(\lambda=(e,D_1+D_2,D_2-D_1)\), the exact equation is
\[
 (dH-eG)^2-d(2h)^2=R(d),\qquad R(d)=\prod_{\nu=1}^3(d+\lambda_\nu^2).
\]

The new restriction concerns how many Gaussian pairs yield the **same** product \(L-j+ih\). At a split prime \(p\) the number of allocations is at most \(1+t\), where
\[
 t=\min\{v_p(M_1),v_p(M_2),v_p(L-j),v_p(h)\}.
\]
Indeed, if the two conjugate prime exponents of the product are \(a,b\), the allowed allocations form an integer interval of length at most \(1+\min(a,b,v_p(M_1),v_p(M_2))\). At a prime that does not split, the allocation is unique.

If \(t>0\), choose signs \(s_1,s_2\) such that \(n\equiv U_i+s_iD_i\bmod p^{\lceil t/2\rceil}\) for both labels. The two actual shifts then agree modulo this power. Substitution gives
\[
 2L\equiv -(D_1-s_1s_2D_2)^2\pmod {p^{\lceil t/2\rceil}},
 \qquad
 p^{\lceil t/2\rceil}\mid d+(D_1-s_1s_2D_2)^2 .
\]
Thus the allocation multiplicity costs only primes in the shift discriminant, and its depth is charged to **the same three Gram factors**. A common prime of \(M_1,M_2\) alone does not force this congruence. The replay below exhibits the difference at \(5\).

### Aggregate count and diagonal bound

Let \(\mathcal B=2\prod_\nu\lambda_\nu\prod_{\nu<\rho}(\lambda_\nu^2-\lambda_\rho^2)\). This is nonzero because the four actual shifts are distinct. At \(p\nmid\mathcal B\) dividing \(R(d)\), exactly one Gram factor vanishes and \(d\equiv-\lambda_\nu^2\bmod p\). In the Pell ideal count for \(x^2-dy^2=R(d)\), the local count is therefore \(v+1\) at \(p\equiv1\bmod4\) and the even-valuation indicator at \(p\equiv3\bmod4\). These are exactly the local weights of \(r_2/4\). When \(d\) is square, ordinary integer factorization gives the same upper bound. At the bad primes, the Pell ideal count and the allocation congruence together cost at most a fixed polynomial in each Gram factor’s valuation.

There is no \(\log X\) loss from Pell units. For each \(d\), \(x=dH-eG\asymp dX\), and \(x+\sqrt d\,|y|\) lies between \(x\) and \(2x\). Generators of one ideal in this fixed-ratio interval have bounded multiplicity, since the absolute value of a real quadratic unit greater than 1 is at least the golden ratio.

Apply Henriot’s bound to the three linear forms \(j+\lambda_\nu^2/2\). The constants are integral since all \(\lambda_\nu\) are even. The good-prime Euler product is bounded, since its logarithm is \(3\sum_{p\le Y}\chi_4(p)/p+O(1)\). The bad-prime factor is \(\Gamma(\mathcal B)=\prod_{p\mid\mathcal B}(1+C/p)\). Its mean over the actual label pairs is bounded. To see this, split \(\mathcal B\) into its finitely many linear factors in the four actual powers and freeze all but one suitable 3-exponent in each factor. Primes with \(\operatorname{ord}_p(9)<p^{1/4}\) have summable reciprocals, by counting primes in \([Y,2Y]\) that divide \(\prod_{h\le(2Y)^{1/4}}(9^h-1)\). For the others with \(p\le K^2\), the divisibility proportion is \(O(p^{-1/4}+K^{-1})\). Hölder with reciprocal exponents \(8C/(p\log p)\) beyond a fixed cutoff gives a bounded mean. Primes above \(K^2\) have bounded reciprocal contribution by the size of the factors. [Henriot, Corollary 2](https://arxiv.org/pdf/1102.1643) and [erratum](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf/nair-tenenbaum-uniform-with-respect-to-the-discriminant-erratum.pdf).

It follows that the total number of pairs with \(1\le j\le J\), over all distinct eligible labels and targets, is
\[
 N_X(J)\ll K^4J\qquad (X^{1/3}\le J\ll X^2).
\]
For the initial \(j\le X^{1/4}\) use the elementary \(X^\epsilon\) divisor bound per deficit and label pair. Above it, use dyadic intervals in Henriot’s bound. Since the normalized relative-diagonal kernel is \(O(1/T)\) with \(T\asymp K^2\), \(j\le X/K^2\) costs \(O(X)\). Here \(j\asymp X^2\delta^2\) for the closest relative angle \(\delta\), by the displayed formula for \(M_1M_2-L^2\).

For the deeper \(3\)-adic sector, let \(m\) be the least power of \(3\) at least \(X\) and write \(j=mu\). Then \(v_3(d)>2v_3(eG)\). At every prime above \(3\), both Pell conjugates have valuation exactly \(v_3(eG)\) in the normalization \(v_3(3)=1\). The reason is that \(dH-eG\) has that valuation, whereas \(2h\sqrt d\) has strictly larger valuation. Hence the ideal allocation at \(3\) is fixed. Gaussian allocation at \(3\) is already unique. After removing the fixed 3-parts the three primitive linear forms in \(u\) have coefficient height \(O(X^3)\) for their product, and the same bad-prime bound away from \(3\). Henriot applies on dyadic \(u\)-intervals above \(X^{1/3}\), using its coefficient-height exponent \(1/12\). The smaller \(u\)'s again cost only \(O_\epsilon(K^4 X^{1/3+\epsilon})\) pairs. This gives \(O(K^4Y)\) pairs on each remaining shell \(Y<u\le2Y\). The normalized kernel is
\[
 O\!\left(\frac{1}{T(1+T^2mu/X^2)}\right).
\]
Summing the shells up to \(\delta\le1/K\) gives the claimed \(O(X(1+\log K)/K^2)\). Subtracting the zero harmonic on this sector costs \(O(X/K^2)\). The intermediate sector with \(m\nmid j\) remains open. In particular, these estimates give neither an \(O(X)\) bound on the whole diagonal nor a complete second moment.

### Native replay

The control uses the same ordinary target and distinct numerical seeds at \((3,4),(5,4)\). The genuine pair shares a prime \(5\) in both norms without sharing it in the Gaussian product. Reflecting the Gaussian point produces an allocation with rational \(5\)-content. A separate perturbation of the deficit stays inside the angular window and preserves its low \(2,5\) digits, yet the good inert prime \(211\) rejects it.

```python
from math import isqrt, prod

K, B, A = 300, 25**4, 9**3
X = 1 << K
a, u = 3395, 473908545666970293546287554900113349394416
x = a*u + A + 2*B - (a*a+1)//2
n = x*x + u*u + 3*A + 5*B

def cert(r, p, t):
    A = 9**r
    U, D = 2*A+3*B, A+2*B
    S = n-U-D
    k = S.bit_length()-1
    assert X <= n < 2*X and A <= B and B**16 <= n <= A**32
    x,y = p
    a,b = t
    assert x*x+y*y == S and a*a+b*b == S+2*D
    f,g,h = x-a,y-b,x*b-y*a
    assert f%2 and g%2 and h%2 == 0
    q = ((f+g)//2)**2 + ((f-g)//2)**2
    assert q%2 and 2*q*S == (D-q)**2+h*h
    return q,(n-U-q,abs(h)),U,D,64*k*k*q <= S <= 64*k*(k+1)*q

p = (370364302106323949618686923647947300990535546,
     -1565711501568699087370650397834208298305903076)
t = (371286745392217617117272419857876274653556789,
     -1565493013435470228569674359748079227673377687)
q,(a,b),U,D,ok = cert(3,(x,u),(x+1,3395-u))
qq,(c,d),V,E,ok2 = cert(5,p,t)
assert ok and ok2 and q != qq and not cert(5,p,(t[0],-t[1]))[-1]
M,N = (n-U)**2-D*D,(n-V)**2-E*E
P,L = M*N,(n-U)*(n-V)-(D*D+E*E)//2
lam = (V-U,D+E,E-D)
G,H = E*E-D*D,2*n-U-V

def gram(c,d):
    dot,h = a*c+b*d,a*d-b*c
    j = L-dot
    assert dot*dot+h*h == P and isqrt(P) == L-1
    assert (2*j*H-lam[0]*G)**2-2*j*(2*h)**2 == prod(2*j+v*v for v in lam)
    return j,dot,h

j,dot,h = gram(c,d)
assert j > X and 0 < h*h*K**4 < P
assert M%5 == N%5 == 0 and (dot%5,h%5) == (2,4)
assert (2*j+lam[2]**2)%5 == 1
jc,bc,hc = gram(c,-d)
assert bc%5 == hc%5 == (2*jc+lam[2]**2)%5 == 0

p = 211
assert p%4 == 3 and all(p%f for f in range(2,isqrt(p)+1))
bad = 2*prod(lam)*prod(v*v-w*w for i,v in enumerate(lam) for w in lam[:i])
change = 183500800
assert bad%p and change%(25*2**16) == 0
h_bad_sq = P-(L-j-change)**2
assert 0 < h_bad_sq*K**4 < P
assert (2*(j+change)+lam[0]**2) % p**2 == 197*p
assert pow(h_bad_sq%p,(p-1)//2,p) == p-1
print("True seeds, shared-prime control, and false defect verified")
```
