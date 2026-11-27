# Thirteen sphere rays and a phase-dependent kernel smoothness obstruction

**The seed \((m,e)=(290,54)\) closes the \(30\)–\(34\) gap at phase \(290/9\).** The thirteen rays now have maximum consecutive ratio \(71/63\). In each odd class modulo \(4\), they give an effective count of distinct generated targets
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{63/142}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda=1,3.
\]
The exponent \(63/142\) is sharp in the liminf for these rays.

The two halves also impose a stronger common restriction than the previous per-sign bound. **For every fixed \(c>0\)**, only \(o(U)\) half-exponents \(u\le U\) have an admissible partner for which *either* half’s squarefree kernel is supported on primes at most \(c\log U\log\log U\). This holds even when the \(3\)-exponent is chosen freely.

### The shared restriction on the two kernels

Let \(H_\pm=(5^u\pm3^v)/2\) for odd \(u,v\), and let \(C_\pm\) be their squarefree kernels. For an admissible pair the kernels are coprime and supported on primes \(p\equiv1\bmod3\). Fix a finite set \(\mathcal L\) of primes \(\ell\ge7\). For any \(\ell\nmid u\) and \(p\equiv1\bmod\ell\), write \(a_\ell,b_\ell\) for the logarithms of the \(\ell\)-th power residue symbols of \(5,3\) at \(p\), using the same generator. **Either** divisibility \(p\mid H_-\) or \(p\mid H_+\) forces
\[
a_\ell u=b_\ell v\pmod\ell,
\]
because \(-1\) is an \(\ell\)-th power. Thus at a fixed exponent phase the two kernels use a common prime set.

For a fixed subset \(J=\{\ell\in\mathcal L:\ell\nmid u\}\) and fixed residues \(v/u\bmod\ell\), that prime set has density
\[
\delta_J=\frac12\prod_{\ell\in J}(1-1/\ell).
\]
To verify this, take \(F=\mathbb Q(\zeta_{3\prod_{\ell\in\mathcal L}\ell})\). Over \(F\), adjoining the \(\ell\)-th roots of \(5\) and \(3\) gives degree \(\ell^2\). The first root has degree \(\ell\) by the valuation at \(5\), and its extension is unramified at \(3\). The valuation of \(3\) is still \(2\), giving degree \(\ell\) for the second root. These Galois extensions have coprime degrees for distinct \(\ell\), so their Frobenius coordinates are independent over a fixed cyclotomic Frobenius. When \(p\equiv1\bmod\ell\), the required linear relation takes exactly \(1/\ell\) of the \(\ell^2\) choices. Averaging over the base residues gives the factor \(1-1/\ell\). [Chebotarev density theorem, Lagarias–Odlyzko](https://aareyanmanzoor.github.io/assets/articles/lagarias-odlyzko.pdf)

At a fixed phase there are at most \(3^{(\delta_J+o(1))y/\log y}\) jointly \(y\)-smooth kernel pairs. Each available prime can occur in the minus kernel, the plus kernel, or neither. For a single smooth sign the corresponding base is \(2\). Each fixed kernel \(C\) yields only \(O(1)\) exponent pairs, uniformly in \(C\). In fact, writing \(H_\pm=Cz^2\) and \(x=5^{(u-1)/2}\), the two elements \(5x\pm z\sqrt{10C}\) have sum \(10x\) and product \(\mp5\cdot3^v\). Dividing by the sum gives a unit equation over a field of degree at most two with support above \(2,3,5\). Its normalized product fixes \(3^v/5^u\). [Evertse–Schlickewei–Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04)

To remove the fixed-phase restriction, choose \(\mathcal L\) far enough out that \(\sum_{\ell\in\mathcal L}\ell^{-2}<\epsilon\), and large enough that \(T=\sum_{\ell\in\mathcal L}1/\ell\) is arbitrarily large. At most \(\epsilon U\) integers \(u\le U\) lose more than one unit of reciprocal mass to primes \(\ell\mid u\), by averaging. On all other phases, \(\delta_J\le \tfrac12 e^{1-T}\). For \(y=c\log U\log\log U\), choose \(T\) so that \(c\delta_J\log3<1/2\). Summing over the finitely many phases leaves at most \(\epsilon U+U^{1/2+o(1)}\) half-exponents. This proves the claim for either sign. It also survives cubing: depths at least \(K\) contribute only multiples of \(3^K\), and the finitely many smaller depths preserve \(o(U)\). Bounded spacing therefore requires a source of seeds whose kernels escape **every** fixed multiple of this smoothness scale.

There is a small exact sign conflict as well. The \(2\)-primary projections of \(5,3\) at both \(2089\) and \(2281\) have order four and are negatives of one another. Each prime is individually eligible in either half. Assigning \(2089\) to the minus half requires \(u\equiv3v\bmod4\), while assigning \(2281\) to the plus half requires \(u\equiv v\bmod4\). These assignments cannot coexist at one odd exponent pair.

### Seed, spacing, and replay

The two half-norm identities in the replay certify \(5^{290}-3^{54}\) directly. At depth \(k\), set \(Q=5^{290\cdot3^k}\) and \(Z=3^{54\cdot3^k}\). The usual sphere identity gives
\[
n=5Q+\lambda Z-S=Q+(4-\lambda)Z+v^2+r^2,\qquad Q<n<5Q,
\]
with \(\lambda=1,3\), giving the classes \(21\bmod24\) and \(3\bmod24\). Both positive exponents grow. The fixed-height count applies since the new seed has \(Z\le Q^{54\log3/(290\log5)}\) and the same ternary and discriminant conditions as the preceding rays. The next bottleneck is \(42\)–\(142/3\). At \(X=5^{(142/3)3^j}\) the preceding lower power is \(5^{42\cdot3^j}\), and the all-orientation ceiling \(Q^{1/2+o(1)}\) gives the matching liminf bound. [Effective fixed-height count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The replay checks both classes at depths zero and one. At each height the failed control has a valid signed witness and an exact odd valuation at a Gaussian inert prime for its prescribed positive pair.

```python
from fractions import Fraction as F

def N(a,b):
    return a*a + 3*b*b

def orient(a,b,c,d):
    pairs = [(a*c-3*b*j*d, abs(b*c+a*j*d)) for j in (1,-1)]
    return max((z for z in pairs if z[1]%3), key=lambda z:z[1])

a,b = 94086251848665204528919377240060042405884834671909,185518781043011841167325615469382081368333244973686
c,d = 26029961511497997281578194494451396377790138030632,192722873793516700429591052412211515424450128646112
q,s = 5**145,3**27
assert 2*N(a,b) == q-s and 2*N(c,d) == q+s
Q,Z = q*q,s*s
v,w = (4*z for z in orient(a,b,c,d))
for k,(j,p,h) in enumerate(((5,19,133),(37,79,3713))):
    assert Q == 5**(290*3**k) and Z == 3**(54*3**k) == s*s
    assert N(v,w) == 4*(Q-Z) and w > s and w%3
    for good,t in ((True,w),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            r,S = t+s,x*x+y*y
            n = 5*Q+lam*Z-S
            assert Q < n < 5*Q and S > lam*Z
            assert n%24 == (21 if lam == 1 else 3)
            assert 2*lam*Z-S == r*r-3*t*t
            R = n-Q-(4-lam)*Z
            assert R == v*v+r*r if good else R%(p*p) == h
    v,w = orient(v,w,(Q-Z)//2,(Q+Z)//2)
    Q,Z,s = Q**3,Z**3,s**3

for p,o in ((2089,261),(2281,285)):
    A,B = pow(5,o,p),pow(3,o,p)
    assert A*A%p == p-1 and (A+B)%p == 0
ph = [F(18),F(178,9),F(22),F(70,3),F(26),F(82,3),F(30),F(290,9),
      F(34),F(38),F(42),F(142,3),F(158,3),F(54)]
assert max(b/a for a,b in zip(ph,ph[1:])) == F(71,63)
```

The count concerns the constructed targets. The failure tests concern their specified positive exponent pairs.
