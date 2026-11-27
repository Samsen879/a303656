# Sixth Eisenstein seed and a smaller sphere-phase gap

The seed \((m,e)=(82,2)\) closes the \(26\)–\(34\) gap. Its normalized phase is \(82/3\), and adding it reduces the largest consecutive phase ratio from \(17/13\) to \(9/7\). In **each** odd class modulo \(4\), the six rays now give the effective bound
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{7/18}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}}
\qquad(\lambda=1,3)
\]
for every fixed \(\varepsilon>0\) and all sufficiently large \(X\). Here \(A_\lambda\) counts distinct generated targets with true positive representations. The exponent \(7/18\) is sharp in the liminf for these six rays.

### The seed and both classes

Put \(A=5^{41}\). The two coprime halves have exact Eisenstein norm representations
\[
\begin{aligned}
(A-3)/2&=68339394802783^2+3\cdot77603897372732^2,\\
(A+3)/2&=145414787396114^2+3\cdot23035531618684^2.
\end{aligned}
\]
Multiply their norm elements in \(\mathbb Z[\sqrt{-3}]\) and multiply the product by \(2\). This gives \(a^2+3b^2=5^{82}-9\) with \(4\mid a,b\). The displayed equalities certify the composition directly. The same gap has \(v_7=1\), which rules out a Gaussian norm. The nearby seed \(5^{82}-3^6\) has \(v_{11}=1\), which rules out an Eisenstein norm and persists under every cubing: the quotient \(U^2+UV+V^2\) for cubing is \(3V^2\not\equiv0\pmod{11}\) whenever \(U\equiv V\not\equiv0\pmod{11}\).

At depth \(k\), set \(Q=5^{82\cdot3^k}\) and \(Z=3^{2\cdot3^k}\). Cubing gives norm pairs \(v^2+3w^2=4(Q-Z)\). For \(\lambda=1,3\), take \(r>0\) odd and
\[
S=x^2+y^2=3w^2+2\lambda Z-r^2>\lambda Z.
\]
Then
\[
n=5Q+\lambda Z-S=Q+(4-\lambda)Z+v^2+r^2,\qquad
2\lambda Z-S=r^2-3w^2 .
\]
Both positive exponents grow, and \(Q<n<5Q\). With \(v,w\in4\mathbb Z\) and \(3\nmid w\), the targets are \(21\bmod24\) for \(\lambda=1\) and \(3\bmod24\) for \(\lambda=3\).

The effective orientation argument applies on the new ray. The cubing shell norms are pairwise coprime, and the last two signs give \(\gg2^k\) distinct \(v^2\) with \(3\nmid w\) and \(|w|\gg\sqrt Q\). For either class write \(N_\lambda=3w^2+2\lambda Z=3df^2\) with \(d\) squarefree. The real norm
\[
\operatorname{Norm}(|w|+f\sqrt d)=-2\lambda Z/3
\]
still has prime support only at \(2,3\). For fixed \(d\), at most two ideals occur and the generators lie in a fixed multiplicative interval. Thus one possible exceptional character removes only \(O(1)\) orientations. The Gauss and polynomial-moment estimates then give \(\gg_\varepsilon 2^k\sqrt Q/(\log Q)^{1+\log 2+\varepsilon}\) distinct targets per completed window in each class. The cutoff loses \(O(1+Z/\sqrt Q)\) marked coordinates per sphere, and cross-orientation collisions are bounded by factoring \(r_2^2-r_1^2=v_1^2-v_2^2\). [Effective orientation argument](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md) · [Polynomial-moment theorem](https://arxiv.org/pdf/2403.19320#page=4)

### Spacing and exact controls

The phases in the requested scaling are
\[
18,\ 22,\ 26,\ 82/3,\ 34,\ 42,\ 54,
\]
where \(54\) starts the next cycle. The two new ratios are \(41/39\) and \(51/41\). The maximum is now \(54/42=9/7\), so the largest completed window below \(X\) has upper endpoint \(>X^{7/9}\). Using \(2^k\asymp(\log Q)^{\log_3 2}\) gives the population bound. At \(X=5^{54\cdot3^j}\), all targets lie in preceding windows with lower power at most \(5^{42\cdot3^j}\). Even all norm pairs at such a height give only \(Q^{1/2+o(1)}\) targets by the quadratic ideal divisor bound. This gives the matching liminf ceiling. [Original five-ray spacing](https://raw.githubusercontent.com/Samsen879/a303656/945ab5dbf0455c900e60a455d0f1c6a698c9da8d/analysis/ajt5_overnight_2026_11_26/FIVE_INTERLACED_SPHERE_SEEDS.md)

The replay constructs true positive and signed witnesses in both classes at depths zero and one. It also gives two signed controls \(5\cdot5^{82}-8\) and \(5\cdot5^{82}-26\). For the prescribed positive powers their common residual is \(4\cdot5^{82}-35\), of exact \(23\)-valuation one, so those pairs fail.

```python
from fractions import Fraction as F

def norm(a, b):
    return a*a + 3*b*b

a,b,c,d = 68339394802783,77603897372732,145414787396114,23035531618684
assert 2*norm(a,b) == 5**41-3 and 2*norm(c,d) == 5**41+3
v,w = 4*(a*c-3*b*d),4*(a*d+b*c)
Q0 = 5**82
Q,Z,s = Q0,9,3
for k in range(2):
    assert Q == 5**(82*3**k) and Z == s*s == 3**(2*3**k)
    assert norm(v,w) == 4*(Q-Z) and w > s and w%3
    r = w+s
    for lam,x,y in ((1,w-s,w),(3,w+s,w-2*s)):
        S = x*x+y*y
        n = Q+(4-lam)*Z+v*v+r*r
        assert n == 5*Q+lam*Z-S and Q < n < 5*Q and S > lam*Z
        assert 2*lam*Z-S == r*r-3*w*w and n%24 == (21 if lam == 1 else 3)
    a,b = (Q-Z)//2,(Q+Z)//2
    v,w = a*v-3*b*w,a*w+b*v
    Q,Z,s = Q**3,Z**3,s**3

for lam,x,y in ((1,1,4),(3,7,-2)):
    S = x*x+y*y
    n = 5*Q0+9*lam-S
    assert 18*lam-S == 7**2-3*4**2 and Q0 < n < 5*Q0
    assert n%24 == (21 if lam == 1 else 3)
    assert (n-Q0-9*(4-lam)) % 23**2 == 20*23
assert (Q0-9)%49 == 42 and (Q0-3**6)%121 == 55
p = [F(18),F(22),F(26),F(82,3),F(34),F(42),F(54)]
assert max(y/x for x,y in zip(p,p[1:])) == F(9,7)
```

The population bound concerns the generated sets. The signed controls test failure at their prescribed positive pairs, and arbitrary targets remain outside the theorem’s guarantee.
