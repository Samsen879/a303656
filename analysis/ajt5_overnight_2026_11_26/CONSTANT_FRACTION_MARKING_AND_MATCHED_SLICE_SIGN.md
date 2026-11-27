# Positive-fraction split-cofactor marking and a signed matched slice

The original two-prime marking captures \(\asymp_J(\log B)^{-1/2}\) of the distinct true-pair mass in **each nonblocked cell**, uniformly over the actual exponent grid. Allowing the smaller cofactor to be any integer supported on split primes raises that share to a positive constant. Here \(J\) is any fixed open subinterval of the original \(2/3<\log p/\log B<3/4\) band.

There is also a signed comparison on a larger matched family. Keep all 42 blocked phases across the original window and add **all 105 nonblocked phases** in a fixed positive-width slice of the \(5\)-exponent interval. For a sufficiently narrow slice, the class \(n\equiv0\pmod{49}\) has strictly more true pairs than the \(r_-\) class, even in the unmarked count. The whole-width grid sign remains open.

## Counts and scope

Let \(A=3^a,\ B=5^b\), with \(a,b\) even and \(39/40<B/A<122/125\). Use the original window and labels
\[
1457A-123B<n\le729A+625B,\qquad
S_0=A+25B,\qquad S=3^c+5^e,
\]
\[
a/10\le c\le a/3,\quad b/5\le e\le b/3,\quad
c\equiv a\pmod4,\quad e\equiv b+2\pmod6.
\]
Write \(\kappa=(S_0-S)/45\), so \(\kappa\asymp B\) and \(8\mid\kappa\). Put
\[
F_I(\kappa)=\prod_{\substack{q\mid\kappa\\q\equiv3\pmod4}}\frac{q-1}{q-2},
\qquad r_-=3^{a+4}+5^{b+2}+7\pmod{49}.
\]

A true pair counts one integer \(n\) for one label \((c,e)\) when both remainders are sums of two squares. There is no weight for the number of square representations. Choose fixed \(1/4<\eta_-<\eta_+<1/3\) so that \([1-\eta_+,1-\eta_-]\) lies in the interior of \(J\). Both markings require
\[
n=S_0+45hp,\qquad B^{\eta_-}\le h\le B^{\eta_+},\qquad p\equiv1\pmod4\ \text{prime}.
\]
The original marking takes \(h\equiv1\pmod4\) prime. The enlarged marking allows every \(h\) whose prime factors are all \(1\bmod4\). Since \(hp\asymp B\) in the ordinary window, the actual \(p\) lies in \(J\) for large \(B\). Also \(h<p\), so the factorization marks each \(n\) at most once.

For \(r=0\) and \(r=r_-\), the counts for each nonblocked label satisfy

| Count in \(n\equiv r\pmod{49}\) | Uniform order |
|---|---:|
| All true pairs, with no condition modulo 45 | \(F_I(\kappa)B/\log B\) |
| Enlarged marking | \(F_I(\kappa)B/\log B\) |
| Original two-prime marking | \(F_I(\kappa)B/(\log B)^{3/2}\) |

The constants are uniform in the exponents for sufficiently large \(B\), with marked constants allowed to depend on \(J\). All three counts are zero in the 42 blocked phases in \(r_-\). The other phases in \(r_-\) comprise 98 unit phases and seven with \(S\equiv r_-\pmod{49}\). For the lower bound in those seven, use the single lift \(n\equiv S+49\pmod{343}\), which gives exact depth two. The anchor remains a unit at 7 because \(r_--S_0\equiv3\cdot3^a\pmod7\).

## Why the enlarged marking gives the full order

Let \(H=\sum_h1/h\) over the chosen cofactor set. It is \(\asymp_J1\) for prime \(h\) and \(\asymp_J\sqrt{\log B}\) for split-supported \(h\). The latter follows from the square of the split-only Dirichlet series,
\[
\left(\prod_{q\equiv1(4)}(1-q^{-s})^{-1}\right)^2
=\zeta(s)L(s,\chi_4)(1-2^{-s})\prod_{q\equiv3(4)}(1-q^{-2s}),
\]
and Karamata applied at \(s=1\) to the harmonic sum. The unsieved product interval contains \(\asymp BH/\log B\) pairs by the prime number theorem for \(p\equiv1\pmod4\). [Karamata’s Laplace–Stieltjes theorem](https://geodesic.mathdoc.fr/item/JRAM_1931__164_149745/)

The convolution Bombieri–Vinogradov estimate permits an arbitrary divisor-bounded coefficient on \(h\), so the enlarged support preserves the level \(D=B^{1/2}/(\log B)^C\). Its other coefficient is the split-prime indicator on \(p\), which satisfies Siegel–Walfisz at odd moduli. Both factors are smaller than \(B^{1-\epsilon}\) for fixed \(\epsilon>0\). For the target class modulo 49 or 343 and any squarefree inert sieve modulus \(j\) coprime to \(7\kappa\), the conditions specify one reduced class for \(hp\) modulo \(49j\) or \(343j\). Every supported product is coprime to that modulus. Thus the sieve density at \(q\mid j\) is \(1/(q-1)\), with the convolution error summed at the product scale. [Kurlberg–Lester–Rosenzweig, Lemma A.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

Sift at \(z=B^{1/2-\delta}\), omitting 7 and the inert divisors of \(\kappa\). The half-dimensional lower sieve gives at least
\[
c_1\sqrt{\delta}\,F_I(\kappa)\frac{BH}{(\log B)^{3/2}}
\]
rough survivors. Here \(f_{1/2}(s)\gg\sqrt{s-1}\) near the sifting limit, and \(s=\log D/\log z\ge1+c\delta\). [Half-dimensional sieve and explicit lower function](https://arxiv.org/html/2501.16723v1#S5)

The new reverse step allows shared split factors of \(h\) and \(\kappa\). A false rough survivor has
\[
hp+\kappa=w m q_1q_2,\qquad w\in\{1,49\},\quad z<q_1<q_2,
\]
where \(q_1,q_2\) are distinct inert primes and \(m\) is split-supported with \(m\le Y=C_0 B^{2\delta}\). This follows from \((hp+\kappa)/w\equiv1\pmod4\) and \(z^3\gg B\). Set
\[
g=(h,\kappa)=(h,m),\qquad h_1=h/g,\quad m_1=m/g,\quad \kappa_1=\kappa/g.
\]
Then \(m_1q_1\) is coprime to \(h_1\kappa_1\). For coprimality with \(\kappa_1\), a common prime would divide \(h_1p\), and \(p>\max(m_1,q_1)\). If \(w=49\), then \(7\nmid\kappa_1\) since \(hp\) is a unit at 7. The switch
\[
q_2=\alpha+h_1t,\qquad
p=w m_1q_1t+\frac{wm_1q_1\alpha-\kappa_1}{h_1}
\]
uses \(wm_1q_1\alpha\equiv\kappa_1\pmod{h_1}\). It gives primitive linear forms on an interval of length \(T\ll B/(hwm_1q_1)\), which can be enlarged to that length and has \(T\gg z/h\). The odd-prime root count is two except at divisors of the slopes or determinant, where it is one. An elementary two-form upper sieve therefore bounds the count for fixed \(h,m_1,q_1\) by
\[
\ll \frac{B}{hm_1q_1(\log B)^2}F(h_1)F(m_1)F(q_1)F(\kappa_1),
\qquad F(v)=\prod_{\substack{q>2\\q\mid v}}\frac{q-1}{q-2}.
\]
The fixed factor \(F(w)\) is absorbed in the constant. The interval is a fixed positive power of \(B\), so this step needs only elementary CRT residue counts.

Now \(1+\sum_{j\ge1}F(q^j)q^{-j}=F(q)\). In the \(m_1\)-sum, the condition \((m_1,h_1\kappa_1)=1\) omits precisely the split factors restored by \(F(h_1)F_+(\kappa_1)\) up to \(Y\). They are restored once because \((h_1,\kappa_1)=1\). Factors above \(Y\) are \(1+o(1)\) uniformly, and \(F_I(\kappa_1)=F_I(\kappa)\). The restored split product is \(O(\sqrt{\delta\log B})\), while \(\sum_{z<q_1\ll\sqrt B}q_1^{-1}=O(\delta)\). The total false count is consequently
\[
\ll \delta^{3/2}F_I(\kappa)\frac{BH}{(\log B)^{3/2}}.
\]
Fixing \(\delta\) sufficiently small gives the true-pair lower bounds for both markings.

## Upper bounds for distinct pairs

For the unmarked upper bound write \(x=n-S_0\) and \(\Delta=S_0-S=45\kappa\). Extract the complete inert square parts \(d_1^2\mid x\) and \(d_2^2\mid x+\Delta\). Either \(d_i>B^\epsilon\) costs \(O(B^{1-\epsilon}+\sqrt B)\) by the union bound over square divisors. Otherwise CRT gives at most one progression modulo \([d_1,d_2]^2\). Outside the primes dividing \(d_1d_2\), sieve out the two inert roots, which coincide precisely at divisors of \(\Delta\). The interval upper sieve on each progression gives
\[
\ll \frac{B F_I(\Delta)}{[d_1,d_2]^2\log B}
\prod_{q\mid d_1d_2}(1-2/q)^{-1}.
\]
The sum of the last product times \([d_1,d_2]^{-2}\) converges by Euler products, with local terms \(1+O(q^{-2})\). Also \(F_I(\Delta)\le2F_I(\kappa)\). This bound even discards the restriction on \(n\bmod49\).

For a marked upper bound, fix \(h\) and extract only the inert square part \(d^2\) of \(hp+\kappa\). For \(d\le B^\epsilon\), the progression for \(p\) has length \(O(B/(hd^2))\). Sieve one prime root at split primes, and the prime and norm roots at inert primes outside \(d\). The inert roots coincide at divisors of \(\kappa\), yielding \(F_I(\kappa)\). The sieve product has order at most \((\log B)^{-3/2}\) times these corrections. Summing over \(d\) costs a convergent Euler product and summing over \(h\) gives \(H\). The large \(d\) tail can again be counted over all integers because the marking is unique. This proves the upper bound of the same order as the marked lower bound.

## Signed comparison with nonblocked phases included

The singular factors have a bounded row average on the actual grid. For each fixed compatible \(e\),
\[
\sum_{c}F_I(\kappa_{c,e})\ll\log B.
\]
To see this, remove the bounded factor at 3 and truncate the Euler product at \(Y_0=(\log B)^2\), with uniform factor \(1+o(1)\) above \(Y_0\). Expand with coefficients \(a_d=\prod_{q\mid d}(q-2)^{-1}\) over squarefree inert \(d\) coprime to 3. The condition \(d\mid\kappa_{c,e}\) implies \(3^c\equiv S_0-5^e\pmod d\). Along the step-four row it occurs at most \(1+O(\log B/\log d)\) times for \(d>1\), since \(\operatorname{ord}_d(81)\ge\log(d+1)/\log81\). The truncated sum of \(a_d\) is \(O(\sqrt{\log Y_0})\). Moreover \(\sum_{d>1}a_d/\log d\) converges. Its integral representation uses \(\prod_q(1+q^{-s}/(q-2))-1=O(s^{-1/2})\) near \(s=0^+\), from the inert-prime Euler product, and exponential decay at infinity.

Retain every blocked label, and add every nonblocked label in \(b/5\le e\le b/5+\varepsilon b\), using the same labels in both target classes. The blocked labels contribute \(\gg B\log B\) positive excess in the unmarked or enlarged-mark count. The total possible opposing contribution of the added rows is \(O(\varepsilon B\log B)+O(B)\) by the row bound. Choose a sufficiently small **fixed** \(\varepsilon>0\). The resulting signed excess is \(\gg B\log B\). The identical argument for the original marking has excess \(\gg_J B\sqrt{\log B}\). The slice contains \(\asymp_\varepsilon(\log B)^2\) nonblocked labels and includes every nonblocked phase.

These fractions and signs count \((n,c,e)\) once. They give neither a constant fraction after projecting onto \(n\) alone nor a sign after restoring the remaining nonblocked rows.



## Independent composite-cofactor check

This small instance is outside the narrow balance strip; it checks actual arithmetic in the same window and marked band, not the asymptotic. The first label is nonblocked and gives an actual distinct pair in both classes. The second label is blocked in class \(r_-\) even at the same \(r_-\) target at which the first label succeeds.

~~~python
from math import isqrt

a,b,e = 28,20,4
A,B = 3**a,5**b
S0 = A+25*B
h = 109*137
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
assert r == 39 and all(q%4==1 and all(q%j for j in range(2,isqrt(q)+1)) for q in (109,137))
for c,p,R,x,y in [
    (4,28563481421,0,18115876,12322491),
    (4,28563485449,r,20803559,6873190),
    (8,28563494161,0,21574462,3817267),
]:
    assert p%4==1 and all(p%j for j in range(2,isqrt(p)+1))
    assert p**3>B**2 and p**4<B**3
    S = 3**c+5**e
    n = S0+45*h*p
    assert 1457*A-123*B < n <= 729*A+625*B and n%49==R
    assert n-S == 45*(x*x+y*y) and (S0-S)%360==0
    if R==r:
        assert (n-3**8-5**e)%49==7
~~~

