# Primitive seven-adic coefficients and an exact medium-loss cancellation

Averaging over the seven deep phases **does cancel the bare primitive mod-343 coefficients**. It does not cancel their joint contribution with the medium loss. There is an identifiable component of the loss for which the primitive contribution has distinct-count order and cancels a mod-49 term of exactly the opposite sign. Dropping the primitive terms after averaging would therefore give a spurious signed contribution. The sign of the full normalized loss remains unresolved.

## Exact decomposition on the seven phases

Keep \(A=3^a,\ B=5^b,\ S_0=A+25B\), even \(a,b\), and \(39/40<B/A<122/125\). Use the original compatible label \(S=3^c+5^e\), with \(S\equiv r_-\pmod{49}\) on the seven deep phases. Put \(\kappa=(S_0-S)/45\) and \(v=p+\kappa\). All prime sums below count \(p\equiv1\pmod4\) once in the sharp window
\[
1457A-123B<S_0+45p\le729A+625B.
\]

Write \(u_0=-S_0/45\bmod49\) and \(u_-=-\kappa\bmod49\). Let \(A_-(p)\) indicate \(p\equiv u_-\pmod{49}\), and \(E_\kappa(p)\) indicate \(p\equiv-\kappa\pmod{343}\), the omitted lift. The comparison remains class zero against **exact** depth two. For the medium-loss indicator \(\Psi(v)\), require that all non-7 inert valuations through \(Y\) are even and that some non-7 inert valuation in \((Y,Z]\) is odd. This same function applies before and after stripping 49.

The normalized signed loss is exactly
\[
84\sum_p\bigl(1_{p\equiv u_0\ (49)}-A_-(p)\bigr)\Psi(v)
+\sum_p\bigl(98E_\kappa(p)-14A_-(p)\bigr)\Psi(v).
\]
The second term is purely primitive mod 343, since
\[
98E_\kappa(p)-14A_-(p)
=\frac13\sum_{\operatorname{cond}(\chi)=343}
       \overline{\chi}(-\kappa)\chi(p).
\]
In each deep phase, for fixed \(e\), increasing \(c\) by 84 cycles \(-\kappa\bmod343\) through its seven lifts above \(u_-\). This follows from the order seven of \(3^{84}\bmod343\). Each complete block cancels for a primitive character. The mean bare coefficient over the \(\asymp(\log B)^2\) actual labels is therefore \(O(1/\log B)\). This argument does not control the correlation with \(\Psi(p+\kappa)\).

## A middle-loss component with no averaging gain

Take \(Y=B^\eta,\ Z=B^{1/2-\delta}\). Choose small fixed \(0<\eta<\rho\) with \(2\rho<1/2-\delta\). Define \(Q(v)\) to mean that the **only** non-7 inert prime factor of \(v\) is one prime \(q\in(B^\rho,B^{2\rho}]\), to exact exponent one. Then \(Q\) implies \(\Psi\). Since \(v\equiv1\pmod4\), \(Q\) forces \(v_7(v)\) to be odd. Thus \(Q\) vanishes in class zero and exact depth two. Within the coarse \(r_-\) class, it lies entirely in the omitted lift.

For sufficiently small fixed \(\rho\), uniformly over every actual deep label,
\[
\#\{p:A_-(p)=1,\ Q(p+\kappa)=1\}
\asymp_\rho \frac{F_I(\kappa)B}{(\log B)^{3/2}},
\qquad
F_I(\kappa)=\prod_{\substack{\ell\mid\kappa\\\ell\equiv3\ (4)}}
          \frac{\ell-1}{\ell-2}.
\]
Consequently the primitive term on this component is **positive** and equals \(84\) times that count. The mod-49 term is its negative. Both survive the average over all seven phases, and their cancellation is exact. This identifies an error in replacing the exact six lifts by the coarse class using bare character cancellation. It leaves open whether other components compensate in the full primitive sum.

For the lower bound, fix the lift \(v\equiv343\pmod{2401}\), so the 7-adic depth is three. Mark an inert \(q\in(B^\rho,B^{2\rho}]\) coprime to \(\kappa\), and sieve \(m=v/(343q)\) up to \(z_*=B^{1/2-\omega}\), where \(2\rho<\omega/2\) and \(\omega\) is sufficiently small. The prime base modulus is \(M=4\cdot7^4\). A squarefree divisor test \(d\) on \(m\) uses prime modulus \(Mqd\), including the extra power \(q^2\) when \(q\mid d\). Bombieri–Vinogradov applies at \(d\le B^{1/2-2\rho}/(\log B)^C\). In the summed remainder, a modulus is repeated at most \(O(\log B)\) times, since each possible marked \(q\) divides it.

Here \(m\equiv1\pmod4\). The half-dimensional lower sieve gives \(\gg\sqrt\omega\,F_I(\kappa)B/(\log B)^{3/2}\) rough survivors summed over \(q\), using \(\sum_q1/q\to\frac12\log2\) on the marked band. A survivor with any inert factor has exactly two above \(z_*\), counted with multiplicity. Repeated squares cost \(O(B/z_*+B^{1/2+\rho})\). For distinct factors \(q_1<q_2\), switch to \(q_2\) and \(p=343q m_0q_1q_2-\kappa\), with \(m_0\) split-supported. The two-form upper sieve has interval length \(O(B/(343q m_0q_1))\). The \(m_0\)-sum restores the split singular factors of \(\kappa\) and costs \(O(\sqrt{\omega\log B})\); the \(q_1\) harmonic sum costs \(O(\omega)\). The resulting \(O(\omega^{3/2})\) correction on the same scale is smaller than the lower bound. Thus \(m\) can genuinely be required to be split-only, making the marked \(q\) unique. [Nath–Xie, semi-linear sieve functions and reverse-sieve setting](https://arxiv.org/html/2501.16723v1#S5)

For the upper bound, at each odd depth \(t\ge3\) and marked \(q\), sieve \(p=7^tqm-\kappa\) for primality and \(m\) for split support. If \(7^tq\le B^{1/2}\), the dimension-\(3/2\) upper bound is \(O(F_I(\kappa)B/(7^tq(\log B)^{3/2}))\). Summing \(t\) geometrically and \(q\) harmonically preserves the order. If \(7^tq>B^{1/2}\), the trivial count is \(O(B^{1/2+2\rho}\log B)\). This is a count of distinct prime anchors in a false-alternate stratum. It neither estimates the full normalized loss nor gives the sign for ordinary norm counts.

## Exact replay

The replay keeps \((a,b,c,e)=(712,486,80,122)\). It checks the primitive coefficient cycle, a class-zero true pair, and a true and failed pair on the **same exact depth-two lift**. The latter two both clear the small inert panel. The failure has two certified odd inert valuations in the middle range of the finite control.

```python
from math import gcd, isqrt, prod

A,B = 3**712,5**486
S0,S = A+25*B,3**80+5**122
k,rem = divmod(S0-S,45)
L,U = (1457*A-123*B-S0)//45+1,(729*A+625*B-S0)//45
Q = 1<<567
r = (pow(3,716,49)+pow(5,488,49)+7)%49
assert 39*A<40*B and 125*B<122*A and S%49==r and rem==k%8==0
a = (-k)%49
g = lambda x: 98*(x%343==(-k)%343)-14*(x%49==a)
assert sorted(g(a+49*j) for j in range(7)) == [-14]*6+[84]
assert len({pow(3,80+84*j,343) for j in range(7)}) == 7

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

p0,p2 = positive(1,62267),positive(49,4081)
panel = prod((3,11,19,23,31,43,47))
m = 343*panel
R = p2%m
large = []
for t in (89,127):
    q,s = (1<<t)-1,4
    assert all(t%d for d in range(2,isqrt(t)+1))
    for _ in range(t-2):
        s = (s*s-2)%q
    assert s==0 and q%4==3                 # Lucas–Lehmer
    large.append(q)
    R += m*((q-k-R)*pow(m,-1,q*q)%(q*q))
    m *= q*q
h = (L+Q-2)//Q
h += ((R-1)*pow(Q,-1,m)-h)%m
h += m*(1-h%2)
bad = 1+Q*(h+38*m)

for p,witness,phase in [(p0,5,0),(p2,17,r),(bad,23,r)]:
    assert L<=p<=U and 0<p<Q*Q and p%Q==1 and (p-1)//Q%2==1
    assert pow(witness,(p-1)//2,p)==p-1    # Proth certificate
    assert (S0+45*p)%49==phase
assert (p2+k)%343==(bad+k)%343==49
assert gcd((p2+k)*(bad+k),panel)==1 and 53**200>B
assert all((bad+k)%(q*q)==q and q**13>B>q**3 for q in large)
```
