# A true anchor with no integer-oriented fixed-gap polynomial lift

Set $A=5^{34}+3^{12}-131779$, $V=5^{35}+3^{13}-658897$, and $B=V/5$. At $w_0=762939453206$ the two shifted norms are genuine:
$$
w_0^2-A=10051950^2+4749157^2,\qquad
5w_0^2-V=23989945^2+6516402^2.
$$
Nevertheless, this anchor has no nonconstant rational polynomial lift $w(t)$ with parent square coordinates $(w(t)-a,Y(t))$ and polynomial child norm $5w(t)^2-V$, if the parent carries an integer orientation at the anchor. Here $a$ is constant and the anchor is at a rational parameter.

To see this, the prime parent norm makes its integer representations unique up to signs and exchange. The first parent coordinate at the anchor is thus one of $10051950,-10051950,4749157,-4749157$. In every case $a=w_0-P$ is nonzero and has valuation exactly one at one of the primes $11,34603,631,7$, respectively. Each of these is inert for sums of two squares over the corresponding rational local field, and $B$ is a nonzero square modulo that prime.

Let $F=\mathbb Q(\sqrt B)$. The parent equation reads $2aw=Y^2+a^2+A$. Divide the child representation by the Gaussian factor $1+2i$ to express $w^2-B$ as a polynomial norm. Over $F$, the two polynomials $2a(w\pm\sqrt B)$ are coprime and their product is a norm from $F(i)$. In the unique factorization domain $F(i)[t]$, factors fixed by conjugation occur to even exponent and paired factors are paired within each of the two coprime polynomials. Both have square leading coefficient, namely that of $Y^2$. Hence $2a(w-\sqrt B)$ is itself a polynomial norm. Substitution at the anchor would make $2a(w_0-\sqrt B)$ a sum of two squares in $F$.

Choose the embedding into $\mathbb Q_q$ for which $w_0-\sqrt B$ is a unit. This is possible since $B$ is a nonzero square modulo $q$ and the two local roots have distinct nonzero reductions. The proposed norm then has valuation exactly one. A nonzero sum of two squares in $\mathbb Q_q$, $q\equiv3\bmod4$, has even valuation, as seen by extracting the smaller coordinate valuation and reducing modulo $q$. This is a contradiction.

This excludes fixed-gap polynomial lifts for this anchor in its integer parent orientations. It does not exclude lifts with moving parent gap, nonintegral rational rotations of the anchor, or other anchors at the same label. It is not a claim about the original conjecture.

Replay (Python standard library):

```python
from math import isqrt

def prime(v):
    return v > 1 and all(v % d for d in range(2, isqrt(v)+1))

w = 762939453206
A = 5**34 + 3**12 - 131779
V = 5**35 + 3**13 - 658897
x,y = 10051950,4749157
assert w % 30 == 26
assert w*w-A == x*x+y*y == 123596191013149
assert prime(w*w-A)
assert 5*w*w-V == 23989945**2+6516402**2
for u,q in zip((x,-x,y,-y),(11,34603,631,7)):
    assert prime(q) and q % 4 == 3
    assert (w-u) % q == 0 and (w-u) % (q*q) != 0
    Bmod = V*pow(5,-1,q) % q
    assert Bmod and pow(Bmod,(q-1)//2,q) == 1
```
