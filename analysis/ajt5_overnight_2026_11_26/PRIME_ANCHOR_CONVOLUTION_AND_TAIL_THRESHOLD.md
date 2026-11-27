# Prime-anchor convolution and a residual threshold for the distinct sign

There is an unconditional convolution asymptotic for the stratum \(u=p\equiv1\pmod4\) prime. It counts each anchor once, so the large split prime on the anchor side has been fully inverted. In the seven deep phases, the remaining **alternate representation mass** in \(r_-\) is \(7/8\) of that in \(r=0\), with a uniform error in the sharp window. The alternate reciprocal still needs a signed comparison. Below is the explicit comparison that would suffice for the full distinct-pair sign.

## Prime anchors counted once

Use \(A=3^a,\ B=5^b,\ S_0=A+25B,\ S=3^c+5^e\), with the original even \(a,b\), balance strip \(39/40<B/A<122/125\), and compatible labels in the original exponent ranges. Write \(n=S_0+45u\), \(\kappa=(S_0-S)/45\), and let \((L,U]\) be the interval for \(u\) induced by
\[
1457A-123B<n\le729A+625B.
\]
The classes remain \(r=0\) and \(r=r_-=3^{a+4}+5^{b+2}+7\bmod49\). Set
\[
T_r=\sum_{\substack{L<p\le U,\ p\ {\rm prime}\\
                  p\equiv1\ (4),\ S_0+45p\equiv r\ (49)}}
                 \frac{r_2(p+\kappa)}4 .
\]
Each \(p\asymp B\) is a genuine norm anchor, with \(r_2(p)/4=2\). Counting it once removes the reciprocal factor \(1/2\) at this split prime above \(B^\delta\).

Let \(\chi=\chi_4\), and define the convergent constant
\[
C_\kappa=L(1,\chi)
\prod_{q\nmid 7\kappa}\left(1+\frac{\chi(q)}{q(q-1)}\right)
\prod_{q\mid 7\kappa}\left(1-\frac{\chi(q)}q\right).
\]
Uniformly over the original grid, for every fixed \(N>0\),
\[
T_r=b_r\frac{2C_\kappa}{84}\int_L^U\frac{dt}{\log t}
       +O_N\!\left(\frac{B}{(\log B)^N}\right).
\]
Here \(b_0=1\). For \(r_-\), \(b_-=1\) on the 98 unit phases, \(0\) on the 42 blocked phases, and \(7/8\) on the seven deep phases.

For the proof, first restrict to an exact even depth \(t=v_7(p+\kappa)\), and put \(w=7^t\). The norm multiplicity is unchanged by division by \(w\), and \((p+\kappa)/w\equiv1\pmod4\). The divisor hyperbola identity therefore gives twice the sum of \(\chi(d)\) over \(d<\sqrt{(p+\kappa)/w}\) dividing \((p+\kappa)/w\), plus the square term. Such \(d\) are coprime to \(7\kappa\). A prime common to \(d\) and \(\kappa\) would have to equal \(p>d\).

Apply Assing–Blomer–Li’s prime progression theorem with divisor modulus \(d\), residue \(-\kappa\), divisor classes modulo 28, and outer prime modulus \(196\) or \(4\cdot7^{t+1}\). In Theorem 2.1 take \(a_1=-\kappa,a_2=1\). The outer modulus is supported on the primes dividing 28, and all divisor classes modulo 28 are reduced because the divisors are odd and coprime to 7. The unconditional range allows the outer modulus to be a fixed power of \(\log B\) and the divisor moduli to reach the hyperbola cutoff. To handle the moving cutoff, partition \((L,U]\) into a sufficiently fine polylogarithmic mesh. The two endpoint cutoffs on each bin differ relatively by \(O(1/\text{mesh size})\), and the progression theorem bounds the intervening divisor band using unweighted positive counts instead of \(\chi(d)\). Indeed the sum of \(1/\varphi(d)\) over a relative-width \(\eta\) band at \(R\asymp B^{1/2}/(\log B)^{O(1)}\) is \(O(\eta+R^{-1+o(1)})\), by expanding \(d/\varphi(d)\). Square terms and prime powers cost \(O(B^{1/2+o(1)})\). The remaining divisor sum is
\(\sum_{(d,7\kappa)=1}\chi(d)/\varphi(d)=C_\kappa\). Convolving \(\chi(d)/d\) with its Euler correction gives truncation error \(O_\epsilon(B^\epsilon R^{-1/2})\) at cutoff \(R\). The correction has absolute \(1/2\)-moment \(O_\epsilon(B^\epsilon)\), and partial sums of \(\chi\) are bounded. [Assing–Blomer–Li, Theorems 2.1 and 2.2](https://arxiv.org/pdf/2005.13915)

In a deep phase, exact depth \(t\ge2\) contributes six reduced classes modulo \(7^{t+1}\), together with \(p\equiv1\pmod4\). Odd \(t\) contributes zero. The sum of the even-depth densities is
\[
\sum_{j\ge1}\frac{6}{\varphi(4\cdot7^{2j+1})}=\frac1{96},
\]
against \(1/\varphi(196)=1/84\) in class zero. This gives \(7/8\). The tail above a multiple of \(\log\log B\) in depth is negligible to any prescribed logarithmic order. For represented remainders, an inert factor \(7^t\) can be stripped at even depth, and \(\sum_{m\le X}r_2(m)\ll X\).

This calculation removes the anchor multiplicity completely. It still weights the alternate by \(r_2(p+\kappa)/4\). Even on the subcase \(p+\kappa=49q\) with \(q\) split prime, a separate asymptotic would require a two-prime count for \(49q-p=\kappa\). Also, the unconditional outer-modulus range of Theorem 2.1 is polylogarithmic. Applying it directly with a fixed-power reciprocal sieve in that outer modulus exceeds the stated range.

## The residual comparison needed for distinct pairs

For each nonblocked label \(\ell\), write the fixed-power inverted masses as
\[
V_{\ell,0}=M_\ell(1+e_{\ell,0}),\qquad
V_{\ell,-}=b_\ell M_\ell(1+e_{\ell,-}),\qquad |e_{\ell,r}|\le\epsilon,
\]
where \(b_\ell=1\) on unit phases and \(7/8\) on deep phases. Let \(m_{\ell,r}\) be the mean of the remaining reciprocal over split primes \(q>B^\delta\), under the measure defining \(V_{\ell,r}\). The exact distinct count is \(V_{\ell,r}m_{\ell,r}\).

Let \(\lambda\) be the deep-phase share of \(\sum_\ell M_\ell m_{\ell,0}\), and define \(R_U,R_D\) as the ratios \(\sum M_\ell m_{\ell,-}/\sum M_\ell m_{\ell,0}\) separately over unit and deep phases. Then the ratio of the full nonblocked distinct counts satisfies
\[
\frac{1-\epsilon}{1+\epsilon}\,G
\ \le\ \frac{D_-}{D_0}\ \le\
\frac{1+\epsilon}{1-\epsilon}\,G,\qquad
G=(1-\lambda)R_U+\frac78\lambda R_D .
\]
In particular, a sufficient bound for the desired sign is
\[
(1-\lambda)(R_U-1)+\frac78\lambda(R_D-1)
 <\frac{\lambda}{8}-\frac{2\epsilon}{1+\epsilon}.
\]
A necessary bound is the same left side \(<\lambda/8+2\epsilon/(1-\epsilon)\). The existing distinct upper and lower bounds and the row bound on \(F_I(\kappa)\) keep \(\lambda\) bounded away from zero. Its value is a mass share. As a benchmark, if \(\lambda=1/15\) and \(\epsilon=0\), a common upper bound on both residual ratios would need to be below \(1+1/119\). The \(7/8\) factor leaves a much smaller margin on the full grid than on the seven deep phases alone.

## Exact balanced controls

This replay uses the **same narrow-strip label** \((a,b,c,e)=(712,486,80,122)\). It certifies three 1134-bit prime anchors in the sharp window. The first two have true alternates at depths zero and two. The final anchor is also a true norm, but its alternate fails at exact depth three in the same \(r_-\) class.

```python
from math import isqrt

a,b,c,e = 712,486,80,122
A,B = 3**a,5**b
S0,S = A+25*B,3**c+5**e
k,rem = divmod(S0-S,45)
L = (1457*A-123*B-S0)//45+1
U = (729*A+625*B-S0)//45
Q = 1<<567
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
assert 39*A < 40*B and 125*B < 122*A and S%49 == r
assert a <= 10*c and 3*c <= a and b <= 5*e and 3*e <= b
assert rem == k%8 == (a-c)%4 == (b+2-e)%6 == 0

def positive(w,i):
    f = 4*((isqrt((L+k)//w)+4)//4+i)
    rhs = (((k+1+Q)*pow(w,-1,2*Q)-f*f-1)%(2*Q))//8
    v,j = rhs%2,1
    while j < 565:
        j = min(2*j,565)
        m = 1<<j
        v = (v-(2*v*v+v-rhs)*pow(4*v+1,-1,m))%m
    c = 1+4*v
    if c > Q//2:
        c -= Q
    return w*(c*c+f*f)-k

m = 2401
h = (L+Q-2)//Q
R = (S+343-S0)*pow(45,-1,m)%m
h += ((R-1)*pow(Q,-1,m)-h)%m
h += m*(1-h%2)
p3 = 1+Q*(h+2*m*165)

for p,witness,phase,depth in [
    (positive(1,62267),5,0,0),
    (positive(49,4081),17,r,2),
    (p3,11,r,3),
]:
    assert L <= p <= U and 0 < p < Q*Q
    assert p%Q == 1 and ((p-1)//Q)%2 == 1
    assert pow(witness,(p-1)//2,p) == p-1  # Proth certificate
    n = S0+45*p
    assert 1457*A-123*B < n <= 729*A+625*B and n%49 == phase
    assert (p+k)%7**depth == 0 and (p+k)%7**(depth+1) != 0
    x,y = p,pow(witness,(p-1)//4,p)
    while y*y > p:
        x,y = y,x%y
    assert p-y*y == isqrt(p-y*y)**2  # Explicit anchor norm check
```
