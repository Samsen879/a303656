# Gaussian sieve audit and a bounded-depth reduction of the mod-49 comparison

The audit recovers the uniform \(\gg B/\log B\) lower bound for each admissible label. The shared factor \(h=(m,\ell)\) is essential. In the exact replay, omitting it overcounts complete quotient boxes by a factor of \(h\).

The whole-grid sign remains open. I obtained a finite-depth reduction for it: the true-pair contribution at \(7\)-depth at least \(2J\) is \(O(7^{-2J}BK/\log B)\), with a constant independent of \(J\). Thus compensation for the 42 blocked phases would already have to appear in a bounded set of depth classes.

### Distribution audit

Use the preceding parametrization with \(X=\sqrt B\), \(H=k/4\), \(N=H/g\), and
\[
mw+de=N,\qquad (m,d)=1.
\]
The two Gaussian vectors are \((w\pm gm,e\pm gd)\). The boxes have \(m\asymp X/g\), widths \(\asymp X/g\) for \(m,d\), and width \(\asymp X\) for \(e\). Fix a compatible tuple modulo \(q=49\ell\), where \(\ell\) is squarefree and supported on split primes. The fixed \(49\)-tuple makes \(m\) a unit at \(7\).

For a fixed \(m\) put \(h=(m,\ell)\). Given the prescribed \(d,e\) classes, the exact lift is
\[
de\equiv N-mw_0\pmod{mh}.
\]
It enforces integrality of \(w\) and its residue modulo \(h\). The equation modulo \(q/h\), where \(m\) is invertible, enforces the rest of \(w\bmod q\). In a complete quotient box, choosing \(d\bmod mh\) a unit with \(d\equiv d_0\bmod h\) determines \(e\bmod mh\). The zero-frequency count is therefore
\[
\frac{\varphi(mh)}{\varphi(h)}
=m\prod_{\substack{p\mid m\\p\nmid q}}(1-1/p).
\]
This also checks the normalization after summing \(m\). Expand the product by divisors coprime to \(q\). For each such divisor \(j\), the \(m\)-sum is in one class modulo \(qj\). Summing \(1/m\) over that class gives \((qj)^{-1}\int dm/m+O(g/X)\). The resulting density is \(q^{-1}\prod_{p\nmid q}(1-p^{-2})\), with error \(O(g\log X/X)\). Each primitive local fibre has \(p(p^2-1)\) tuples, so summing the fibres restores precisely the omitted factors \(1-p^{-2}\) at the primes of \(\ell\).

For the nonzero frequencies, the restriction \(d\equiv d_0\bmod h\) shifts the first Kloosterman frequency from \(j\) to \(j+tm\). With \(c=N-mw_0\),
\[
(mh,j+tm,lc)\le h(m,N)(m,j,l).
\]
The progression step \(q/h\) is invertible modulo \(m\). Grouping nonzero frequencies by divisors of \(m\) bounds their gcd-weighted interval sums by \(m^{1+o(1)}\). This bound still holds when the \(e\)-interval wraps around the quotient. Its zero frequency can be \(O(gm)\), and retaining that factor gives error \(O(hg\sqrt{m(m,N)}\,X^{o(1)})\) for fixed \(m\). Summation uses \(\sum_{m\le L}\sqrt{(m,N)}\le L\tau(N)\). After rounding the box lengths and summing at most \(\ell^3\) tuples, the error is \(O(\ell^4X^{3/2+o(1)})\), uniform in \(g,\ell\le X^{1/20}\). The sieve-level sum over \(\ell\) and the \(g\mid H\) sum give \(X^{7/4+o(1)}=o(B/\log B)\). I found no missing local factor or loss of uniformity in this step. [Kloosterman bound, equation (1.4)](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70291)

### The remaining comparison has a finite-depth form

Keep the original balanced \(A=3^a,B=5^b\) window and \(n=S_0+45u\). After requiring \(y\equiv b+2\bmod6\), the 147 compatible phase cells split into three sets at \(r_-=3^{a+4}+5^{b+2}+7\bmod49\):

- \(\mathcal H\) has 42 cells of exact \(7\)-depth one.
- \(\mathcal U\) has 98 cells with unit alternative remainder.
- \(\mathcal Z\) has seven cells with alternative remainder divisible by \(49\).

Let \(T_r(\mathcal C)\) count genuine target–label pairs in class \(r\) on cells \(\mathcal C\). For \(J\ge1\), write \(R_J\) for the contribution of \(\mathcal Z\) in \(r_-\) at depth at least \(2J\). Then, uniformly for \(7^{2J}\le B^{1/4}\),
\[
0\le R_J\ll 7^{-2J}\frac{BK}{\log B}.
\tag{1}
\]

For (1), write \(Q=7^{2J}\) and \(u=Qv+c\), where \(0\le c<Q\) and \(c\equiv-k\bmod Q\). The two true norm tests are on the primitive linear forms \(Qv+c\) and \(v+(c+k)/Q\). The first is a unit at \(7\), and removing \(Q\) from the second remainder preserves normhood. Their coefficient height is \(O(B)\), and the interval for \(v\) has location and length \(\asymp B/Q\). The uniform multiplicative-function upper bound applies with fixed interval and coefficient exponents \(1/2\). [De la Bretèche–Tenenbaum, Theorem 3.1](https://arxiv.org/pdf/2403.19320#page=4)

At a split prime with \(\nu\) distinct roots, the exact-valuation factor \(1+\nu/p\) pairs with the sieve factor \(1-\nu/p\). At an inert prime the exact-valuation factor is \(1+O(p^{-2})\), since a positive allowed depth starts at two. Away from \(7\), the two roots coincide exactly at primes dividing \(k\). Thus the per-label upper bound is
\[
\ll \frac{B}{Q\log B}
\prod_{\substack{p\mid k,\ p\equiv3\ (4)\\p\ne3,7}}
\left(1+\frac1{p-2}\right).
\]
This product has bounded mean on each phase cell. Expand it over squarefree divisors \(d\) with weights \(a(d)=\prod_{p\mid d}1/(p-2)\). For fixed \(y\), a hit \(d\mid k\) occupies at most one class modulo \(\operatorname{ord}_d(3^{84})\), giving frequency \(O(1/\log d+1/a)\) for \(d>1\). Mertens in the inert progression gives \(\sum_{d\le t}a(d)\ll\sqrt{\log(2t)}\). Hence \(\sum_{d>1}a(d)/\log d<\infty\), and the \(1/a\) error is bounded as well. Summing over \(\mathcal Z\) proves (1).

An exact sufficient comparison is now available. Put
\[
D_J=T_0(\mathcal H)+T_0(\mathcal U\cup\mathcal Z)
-T_-(\mathcal U)-T_-(\mathcal Z;\ v_7<2J).
\]
The full signed count is \(D_J-R_J\). If \(C\) is the constant in (1), a positive natural-scale lower bound for the full signed count is equivalent to finding a fixed \(J\) with
\[
\liminf_{B\to\infty}\frac{\log B}{BK}D_J>C7^{-2J}.
\]
The forward implication follows by taking \(J\) large and using \(R_J\ge0\). The reverse follows from (1). The two true-anchor denominators agree to leading order, so this is also the comparison needed for a positive mean gap of order \(K/\sqrt{\log B}\). The blocked-cell lower bound supplies \(T_0(\mathcal H)\gg BK/\log B\). The bounded-depth comparison against it remains unresolved.

### Exact replay

The final control has a genuine anchor and a genuine alternative at exact \(7\)-depth two. A second label on the **same target** is blocked at depth one.

```python
from fractions import Fraction as F
from math import gcd, isqrt, prod

q = 49*65
for m in (11, 25, 39, 65, 325):
    h, N = gcd(m, 65), 4*m+6
    pairs = [(1+q*i, 6+q*j) for i in range(m) for j in range(m)
             if gcd(1+q*i, m) == 1]
    direct = sum((N-d*e)%m == 0 and ((N-d*e)//m-4)%q == 0 for d,e in pairs)
    lifted = sum((N-d*e-4*m)%(m*h) == 0 for d,e in pairs)
    zero = sum(gcd(d,m) == 1 and (d-1)%h == 0 for d in range(m*h))
    assert direct == lifted == zero
    assert sum((N-d*e)%m == 0 for d,e in pairs) == h*zero
    free = (2,3,17)
    assert sum(prod(1-F(1,p) for p in free if (m+q*j)%p == 0)
               for j in range(prod(free)))/prod(free) == prod(1-F(1,p*p) for p in free)

a,b = 7864,5368
A,B = 3**a,5**b
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
T,S = 3**1064+5**1086,3**1064+5**1122
k,rem = divmod(S0-S,45)
assert rem == k%8 == 0
mid = ((lo-S0)//45+(hi-S0)//45)//2
m = (isqrt(mid+k)-isqrt(mid))//2+7
e = (k//4)*pow(2,-1,m)%m-4*m
w = (k//4-2*e)//m
n = S0+45*((w-m)**2+(e-2)**2)
assert lo < n <= hi and n%49 == r == 45
assert n-S == 45*((w+m)**2+(e+2)**2)
assert (n-S)%343 == 147 and (n-T)%49 == 7
```

Independent replay checked direct versus lifted quotient counts at five integer moduli, including the exact factor h when the lift is omitted, and verified the same-target depth-two true pair versus depth-one blocked label. The bounded-depth reduction does not settle the sign of the full-grid comparison.
