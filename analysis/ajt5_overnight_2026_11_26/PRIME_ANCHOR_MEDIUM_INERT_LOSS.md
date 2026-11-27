# Matching early inert valuations and isolating the medium-prime loss

The two classes can be matched unconditionally after sieving for **even inert valuations up to a fixed power of \(B\)**. At the other end, the correction from inert primes above a near-square-root cutoff is arbitrarily small on the distinct-count scale. This leaves one specific comparison for \(h_1/h_0\): the normalized losses from odd inert valuations **between** those cutoffs. A sufficiently sharp bound on that signed difference remains open.

## The part that can be matched

Fix a deep label on the original grid. Thus \(A=3^a,\ B=5^b\), \(a,b\) are even, \(39/40<B/A<122/125\), and
\[
S=3^c+5^e\equiv r_-\pmod{49},\quad
S_0=A+25B,\quad \kappa=(S_0-S)/45.
\]
The label has the original exponent bounds and phases \(c\equiv a\pmod4,\ e\equiv b+2\pmod6\). Count prime anchors \(p\equiv1\pmod4\) once, in the sharp window \(1457A-123B<S_0+45p\le729A+625B\).

Write \(w=1\) for class zero and \(w=49\) for **exact depth two** in \(r_-\). The normalized alternate is \(x=(p+\kappa)/w\), which is odd, \(1\bmod4\), and a unit at 7 in both cases. The prime progression densities are \(\alpha_1=1/84\) and \(\alpha_{49}=1/98\), the latter summing all six depth-two lifts. Write \(D^{(w)}\) for the distinct true count in each case.

Let \(C_w(Y)\) count the anchors for which every inert valuation of \(x\) at primes \(q\le Y\) is even. For \(Y=B^\eta\) with sufficiently small fixed \(\eta>0\),
\[
C_w(Y)=\alpha_w\mathcal L
 \prod_{\substack{q\le Y,\ q\equiv3\ (4)\\q\nmid7\kappa}}
 \left(1-\frac{q}{q^2-1}\right)
 \left(1+O(s^{-s/2})+o(1)\right),
\qquad
s=\frac1{2\eta}+o(1).
\]
Here \(\mathcal L=\int_L^U dt/\log t\) in the original sharp prime window. The main term is common after division by \(\alpha_w\). This count includes the even positive valuations at small inert primes.

To prove it, extract the complete square part \(d^2\) contributed by inert primes up to \(Y\). The part with \(d>(\log B)^K\) costs \(O(B/(\log B)^K+\sqrt B)\) by counting square divisors. For smaller \(d\), fix \(d^2\mid x\) and sieve \(x/d^2\). At \(q\nmid d\) the density is \(1/(q-1)\), and at \(q\mid d\) the conditional density is \(1/q\). The latter adds one power of \(q\) to an already imposed prime progression. The combined prime moduli are \(Md^2j\), where \(M=196\) or \(1372\) and \(j\) is the squarefree sieve modulus. Bombieri–Vinogradov applies at \(j\le B^{1/2}/(\log B)^{C_K}\), even after summing the polylogarithmically many \(d\). The fundamental lemma gives the displayed error. Summing the square parts restores at each permitted \(q\) the exact local factor
\[
1-\frac1{q-1}+\sum_{i\ge1}\frac{1-1/q}{\varphi(q^{2i})}
=1-\frac{q}{q^2-1}.
\]
The main-term square-part truncation is harmless by a convergent \(d^{-2}\)-weighted Euler product. [Kurlberg–Lester–Rosenzweig, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

## The contribution still needing distribution

Put \(Z=B^{1/2-\delta}\). Uniformly in the two classes, for fixed sufficiently small \(\delta>0\),
\[
0\le C_w(Z)-D^{(w)}
\ll \delta^{3/2}\frac{F_I(\kappa)B}{w(\log B)^{3/2}},
\qquad
F_I(\kappa)=\prod_{\substack{q\mid\kappa\\q\equiv3\ (4)}}\frac{q-1}{q-2}.
\]
In fact a false survivor has \(x=d^2m q_1q_2\), with \(d\) inert-supported, \(m\) split-supported, and distinct inert \(Z<q_1<q_2\). Parity forces an even number of odd inert valuations, and \(Z^3\gg B\) leaves exactly two. For fixed \(d,m,q_1\), upper-sieve \(q_2\) and the prime form \(wd^2m q_1q_2-\kappa\) on an interval of length \(O(B/(wd^2m q_1))\). The \(d^{-2}\)-weighted singular factors sum absolutely. The \(m\)-sum restores the split factors of \(\kappa\) and costs \(O(\sqrt{\delta\log B})\); the \(q_1\) harmonic sum costs \(O(\delta)\). This gives the stated bound with the full small inert square part included.

There is also a genuine favorable norm stratum in both classes: **\(x\) has only split prime factors**. Its distinct count is \(\asymp F_I(\kappa)B/(w(\log B)^{3/2})\). Sieve out all inert primes below \(Z\). The half-dimensional lower bound at the valid Bombieri–Vinogradov level gives a \(\gg\sqrt\delta\) contribution on this scale. Subtract the distinct-prime false term just bounded and the repeated large inert prime squares, whose total is \(O(B/Z+\sqrt B)\). This proves the order for genuine split-only alternates, while leaving their normalized ratio open. [Nath–Xie, explicit semi-linear lower function](https://arxiv.org/html/2501.16723v1#S5)

Now set \(L_w=C_w(Y)-C_w(Z)\). It counts anchors that pass the even-valuation test through \(Y\) and have at least one odd inert valuation in \((Y,Z]\). For every fixed \(\xi>0\), one can choose fixed \(\eta,\delta>0\) so that, for sufficiently large \(B\),
\[
\left|
\frac{h_1}{h_0}-1-
\frac{L_1/\alpha_1-L_{49}/\alpha_{49}}{D^{(1)}/\alpha_1}
\right|\le\xi .
\]
Indeed, the early comparison error on the distinct-count scale is \(O(s^{-s/2}/\sqrt\eta)\), and the late error is \(O(\delta^{3/2})\). Thus a sufficient comparison is
\[
\frac{L_1}{\alpha_1}-\frac{L_{49}}{\alpha_{49}}
< (1/6-\xi)\frac{D^{(1)}}{\alpha_1}.
\]
This identifies the missing distribution estimate. Keeping the same normalized reverse tuple does not couple the classes: the intervals for \(x\) and \(x/49\) obtained from the same physical remainder window are disjoint. Scaling a norm by 49 preserves normhood but takes the associated anchor outside the window. The switched prime forms therefore still differ. The divisor-convolution asymptotic of Assing–Blomer–Li supplies representation averages in the two classes, while this loss involves an odd-valuation condition and primality of a remaining inert factor. [Assing–Blomer–Li, Theorems 2.1–2.2](https://arxiv.org/pdf/2005.13915)

## Exact same-lift replay

At \((a,b,c,e)=(712,486,80,122)\), the replay gives a class-zero positive, a depth-two positive, and a failed alternate on that **same** depth-two lift. Both deep anchors clear every inert prime up to \(B^{1/200}\) after stripping 49. The failure has two certified odd inert valuations at \(2^{89}-1\) and \(2^{127}-1\), both between \(B^{1/13}\) and \(B^{1/3}\). Thus it is a real loss between cutoffs, in the narrow balanced strip.

```python
from math import gcd, isqrt, prod

a,b,c,e = 712,486,80,122
A,B = 3**a,5**b
S0,S = A+25*B,3**c+5**e
k,rem = divmod(S0-S,45)
L,U = (1457*A-123*B-S0)//45+1, (729*A+625*B-S0)//45
Q = 1<<567
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
assert 39*A<40*B and 125*B<122*A and S%49==r
assert a<=10*c and 3*c<=a and b<=5*e and 3*e<=b
assert rem==k%8==(a-c)%4==(b+2-e)%6==0

def positive(w,i):
    f = 4*((isqrt((L+k)//w)+4)//4+i)
    h = (((k+1+Q)*pow(w,-1,2*Q)-f*f-1)%(2*Q))//8
    v,j = h%2,1
    while j<565:
        j = min(2*j,565)
        m = 1<<j
        v = (v-(2*v*v+v-h)*pow(4*v+1,-1,m))%m
    x = 1+4*v
    if x>Q//2:
        x -= Q
    return w*(x*x+f*f)-k

def mersenne(t):
    assert all(t%d for d in range(2,isqrt(t)+1))
    q,s = (1<<t)-1,4
    for _ in range(t-2):
        s = (s*s-2)%q
    assert s==0  # Lucas–Lehmer
    return q

p0,p2 = positive(1,62267),positive(49,4081)
panel = prod((3,11,19,23,31,43,47))
m = 343*panel
R = p2%m
large = [mersenne(89),mersenne(127)]
for q in large:
    R += m*((q-k-R)*pow(m,-1,q*q)%(q*q))
    m *= q*q
h = (L+Q-2)//Q
h += ((R-1)*pow(Q,-1,m)-h)%m
h += m*(1-h%2)
bad = 1+Q*(h+2*m*19)

for p,witness,phase in [(p0,5,0),(p2,17,r),(bad,23,r)]:
    assert L<=p<=U and 0<p<Q*Q and p%Q==1 and ((p-1)//Q)%2
    assert pow(witness,(p-1)//2,p)==p-1  # Proth certificate
    assert (S0+45*p)%49==phase
assert (p2+k)%343==(bad+k)%343==49
assert gcd((p2+k)*(bad+k),panel)==1 and 53**200>B
assert all((bad+k)%(q*q)==q and q**13>B>q**3 for q in large)
```
