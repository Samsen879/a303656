# Distinct prime-anchor alternates by exact 7-adic depth

The prime-anchor **distinct** count has matching upper and lower order bounds at every even 7-adic depth of polylogarithmic size. Deeper contributions admit a geometric upper bound. This reduces the comparison in the seven deep phases to finitely many normalized distinct counts, with an explicit margin. The sieve bounds still leave the sign of those normalized counts unresolved.

## Distinct counts by exact depth

Keep the original even \(a,b\), \(A=3^a,\ B=5^b\), \(39/40<B/A<122/125\), and sharp window
\[
1457A-123B<n\le729A+625B.
\]
Write \(S_0=A+25B\), \(S=3^c+5^e\) for an original compatible label, \(n=S_0+45p\), and \(v=p+\kappa\), where \(\kappa=(S_0-S)/45\). Restrict to prime anchors \(p\equiv1\pmod4\), counted once. Let \(D_0\) be the number of true alternates in \(n\equiv0\pmod{49}\). For a deep label \(S\equiv r_-\pmod{49}\), let \(D_j\) count true alternates at **exact** depth \(v_7(v)=2j\), for \(j\ge1\). These all lie in the original \(r_-\) class.

With \(w=49^j\) and \(F_I(\kappa)=\prod_{q\mid\kappa,\ q\equiv3(4)}(q-1)/(q-2)\), the unconditional bounds are
\[
D_0\asymp \frac{F_I(\kappa)B}{(\log B)^{3/2}},\qquad
D_j\asymp_K \frac{F_I(\kappa)B}{w(\log B)^{3/2}}
\quad\bigl(w\le(\log B)^K\bigr).
\]
The second bound also holds on each of the six individual exact-depth lifts modulo \(7w\). For the **whole tail**, uniformly for \(49^j\le B^{1/2}\),
\[
\sum_{i\ge j}D_i\ll
\frac{F_I(\kappa)B}{49^j(\log B)^{3/2}}.
\]

### Valid divisor level and reverse subtraction

On one exact-depth lift put \(X=B/w\) and sieve \(v/w\) against inert primes below \(z=X^{1/2-\delta}\). The prime base modulus is \(M=28w\), or \(196\) in class zero with \(w=1\). For a squarefree inert divisor modulus \(d\) coprime to \(7\kappa\), the combined condition is one reduced prime class modulo \(Md\). Bombieri–Vinogradov thus supplies the absolute remainder sum at divisor level
\[
D=\frac{B^{1/2}}{M(\log B)^C}.
\]
When \(w\le(\log B)^K\), the logarithmic saving can absorb \(w\), and \(s=\log D/\log z=1+2\delta+O(\delta^2)+o(1)\). The density is \(1/(q-1)\) at the sieving primes. The half-dimensional lower function satisfies \(f_{1/2}(s)\asymp\sqrt{s-1}\), giving \(\gg\sqrt\delta\,F_I(\kappa)X/(\log B)^{3/2}\) rough survivors. [Nath–Xie, semi-linear sieve functions](https://arxiv.org/html/2501.16723v1#S5)

A false rough survivor has \(v/w=mq_1q_2\), with distinct inert primes \(z<q_1<q_2\) and split-supported \(m\ll X^{2\delta}\). There are at most two inert factors with multiplicity by size, and their number is even because \(v/w\equiv1\pmod4\). For fixed \(m,q_1\), the reverse forms are \(q_2\) and \(p=wmq_1q_2-\kappa\). Their interval has length \(O(X/(mq_1))\), and their odd-prime root count is two except at divisors of \(wmq_1\kappa\), where it is one. Since \(q_2>q_1\) and \(m q_1q_2\ll X\), the available length scale \(X/(m q_1)\) is at least a constant times \(X^{1/2-\delta}\). Here \((wmq_1,\kappa)=1\) because the deep label has \(7\nmid\kappa\), and a prime dividing both \(mq_1\) and \(\kappa\) would have to equal \(p\).

The two-form upper sieve gives a bound with factor \(F(wm q_1\kappa)\), where \(F(t)=\prod_{q>2,\ q\mid t}(q-1)/(q-2)\). In the harmonic \(m\)-sum, \(1+\sum_{k\ge1}F(q^k)q^{-k}=F(q)\) restores the omitted split factors of \(\kappa\). The factor at 7 is bounded independently of its depth. The \(m\)-sum costs \(O(\sqrt{\delta\log B})\), and the \(q_1\)-sum costs \(O(\delta)\). Thus the false count is \(O(\delta^{3/2}F_I(\kappa)X/(\log B)^{3/2})\). Fixing \(\delta\) sufficiently small leaves the distinct lower bound.

For the tail upper bound, impose only \(w\mid v\), write \(x=v/w\), and extract the full inert square part \(d^2\mid x\). The portion with \(d>X^{1/10}\) costs \(O(X^{9/10}+\sqrt X)\) by counting square divisors. For smaller \(d\), sieve the prime form \(wd^2t-\kappa\) and the inert divisors of \(t=x/d^2\) outside \(7d\). There is one root at split primes and two at inert primes except at collisions from \(\kappa\). This gives
\[
\ll \frac{F_I(\kappa)X}{d^2(\log X)^{3/2}}
\prod_{q\mid d}(1-2/q)^{-1}.
\]
The sum over \(d\) converges. For \(w\le B^{1/2}\), \(\log X\asymp\log B\), giving the asserted uniform tail. The same upper argument with \(w=1\) handles class zero.

## The comparison margin and multiplicity loss

Let \(\mathcal L=\int_L^U dt/\log t\), where \((L,U]\) is the sharp interval for \(p\). Define normalized **distinct** densities \(h_j\) by
\[
D_0=h_0\frac{F_I(\kappa)\mathcal L}{84\sqrt{\log B}},
\qquad
D_j=h_j\frac{F_I(\kappa)\mathcal L}{2\cdot49^j\sqrt{\log B}}.
\]
The denominator \(2\cdot49^j\) incorporates the six reduced lifts at exact depth \(2j\). The actual ratio on a deep label is
\[
\frac{D_-}{D_0}
=\sum_{j=1}^J\frac{42}{49^j}\frac{h_j}{h_0}+R_J,
\qquad 0\le R_J\le C\,49^{-J-1}.
\]
Thus depth two has coefficient \(6/7\), and **all** higher even depths have total coefficient \(1/56\) before the normalized distinct densities are applied. For example, \(h_j/h_0\le9/8\) for the first \(J\) depths, with \(C49^{-J-1}\le1/128\), suffices for \(D_-/D_0\le127/128\). Conversely, a positive sign requires \(h_1/h_0<7/6\). The order bounds do not establish either comparison of normalized densities.

The earlier prime-input representation asymptotic, applied separately at these polylogarithmic depths, gives a sharp loss. If \(T_j\) weights the alternate by \(r_2(v)/4\) while counting each prime anchor once, then
\[
\frac{D_j}{T_j}\asymp_K
\frac{\displaystyle\prod_{q\mid\kappa,\ q\equiv1(4)}(1-1/q)^{-1}}
     {\sqrt{\log B}},
\]
also with the class-zero convention. The split product is at most \(O(\sqrt{\log\log B})\). Hence the representation-to-indicator loss is at least of order \(\sqrt{\log B/\log\log B}\) in both classes. Assing–Blomer–Li’s progression result supplies the divisor hyperbola asymptotic for \(T_j\). Its signed divisor sum does not supply the absolute or sieve-weighted remainder estimate needed to extend the distinct lower sieve beyond the level above. [Assing–Blomer–Li, Theorems 2.1–2.2](https://arxiv.org/pdf/2005.13915)

## Exact same-label, same-lift replay

On \((a,b,c,e)=(712,486,80,122)\), the replay certifies a class-zero positive, a depth-two positive, and a failed alternate on the **same depth-two lift** as that positive. The failed alternate has odd valuation at 3. All three anchors are certified 1134-bit primes \(1\bmod4\).

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
assert a<=10*c and 3*c<=a and b<=5*e and 3*e<=b
assert rem == k%8 == (a-c)%4 == (b+2-e)%6 == 0

def positive(w,i):
    f = 4*((isqrt((L+k)//w)+4)//4+i)
    rhs = (((k+1+Q)*pow(w,-1,2*Q)-f*f-1)%(2*Q))//8
    v,j = rhs%2,1
    while j<565:
        j = min(2*j,565)
        m = 1<<j
        v = (v-(2*v*v+v-rhs)*pow(4*v+1,-1,m))%m
    x = 1+4*v
    if x>Q//2:
        x -= Q
    return w*(x*x+f*f)-k

m = 3087
h = (L+Q-2)//Q
h += ((2216-1)*pow(Q,-1,m)-h)%m
h += m*(1-h%2)
bad = 1+Q*(h+2*m*55)
p0,p2 = positive(1,62267),positive(49,4081)
for p,witness,phase in [(p0,5,0),(p2,17,r),(bad,3,r)]:
    assert L<=p<=U and 0<p<Q*Q and p%Q==1 and (p-1)//Q%2==1
    assert pow(witness,(p-1)//2,p)==p-1  # Proth certificate
    assert (S0+45*p)%49==phase
assert (p0+k)%7 and (p0+k)%25==5
assert (p2+k)%343 == (bad+k)%343 == 49
assert (bad+k)%9==3
```
