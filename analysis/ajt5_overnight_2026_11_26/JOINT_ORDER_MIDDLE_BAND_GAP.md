# Why the elementary rank-two order bound leaves a middle-band gap

For primes $p\in(Y,2Y]$, let $R=\operatorname{ord}_p(9)$, $S=\operatorname{ord}_p(25)$, and $D=\operatorname{lcm}(R,S)$, the size of the generated subgroup. For fixed real bounds $r,s,d\ge1$, the number with $R\le r,S\le s,D\le d$ is
$$
 O\big(\min(Y,r^2,s^2,d^{3/2})/\log Y\big).
$$
For the joint bound take $m=\lfloor\sqrt d\rfloor$. The $(m+1)^2>d$ monomials $9^i25^j$ for $0\le i,j\le m$ force a collision. Cancel common powers and identify signed duplicate differences. There are $O(m^2)$ nonzero integer differences to test (nonzero by multiplicative independence), each of absolute value at most $225^m$. All the primes in question divide their product, whose logarithm is $O(d^{3/2})$. The same argument with one base gives the one-axis exponents $r^2,s^2$. This is the rank-two argument also used in [Pappalardi's subgroup-order estimates](https://papparnta.github.io/pappa/papers/J_Num_Theory_57_1996.pdf).

For a layer $RS\asymp T$ and $g=\gcd(R,S)\asymp G$, one can combine the count with the singleton-coset estimate of [Mit'kin, quoted as Lemma 10 here](https://arxiv.org/pdf/1302.3839#page=10). It bounds the roots of $u+v=n\bmod p$ in the two subgroups by $O(T^{1/3})$ when $T<p^{3/2}$ and $T$ is large: with one coset pair the two hypotheses are exactly the product bound and a fixed lower bound on $T$. For $n=0$ and inert $p$, there are no roots, since both variables are nonzero squares. Thus the sum of root-occupancy fractions from a layer is bounded by
$$
 O\!\left(\frac{\min(Y,(T/G)^{3/2})}{T^{2/3}\log Y}\right).
$$
In the balanced case $G\asymp\sqrt T$ this still leaves $T^{1/12}/\log Y$ on the rank-two side. For $T\asymp Y^\theta$, $1\le\theta<3/2$ fixed, neither term of the displayed minimum tends to zero. This is a gap in the upper-bound method, not a claim that large occupation or many such primes actually exist.

A concrete contrast: at $p=541447$, both mixed words $9^2\cdot25$ and $9\cdot25^2$ generate the full square subgroup, while the original two axis orders remain $93,8733$. Large order of a mixed word is therefore not enough to replace the product of the two original orders in the occupancy estimate.

```python
from math import gcd,isqrt
p=541447
assert all(p%j for j in range(2,isqrt(p)+1))
def order(a):
    a%=p
    n,b=1,a
    while b!=1:
        b=b*a%p
        n+=1
    return n
R,S,C,D=map(order,(9,25,9**2*25,9*25**2))
assert (R,S,C,D)==(93,8733,270723,270723)
assert R*S==812169 and R*S//gcd(R,S)==(p-1)//2
```
