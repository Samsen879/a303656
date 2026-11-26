# Coprime large-prime cofactor pairs carry positive second-moment mass

Use the fixed class \(n\equiv527\bmod672\) and the separated two-axis grid of [the mixed-digit note](MIXED_INERT_DIGIT_OBSTRUCTION.md). It has \(K_X\asymp(\log X)^2\) distinct shifts \(s\). Fix a sufficiently large cutoff \(y\) and then let \(X\) grow. There are
\[
\gg \frac{XK_X^2}{\log X\,\log(3y)}
\]
ordered pairs of distinct labels on the same \(n\in[X,2X)\) with coprime true residuals \(n-s=ab,\ n-t=a'b'\). Both \(1<a,a'\le X^{1/8}\) are products of distinct split primes above \(y\); the different \(b,b'\ge X^{7/8}\) are split primes. Normalizing by the square of the true count's mean (and by the number of progression points) gives a contribution bounded below independently of \(X\) for each such fixed \(y\). This rules out a truncation keeping only pairs with a nontrivial gcd or a bounded cofactor on one side. It does not identify the complete second-moment constant.

First count witnesses on one shift. Let \(a\) be a squarefree product of split primes in \((y,X^\delta]\), truncated at \(X^{1/8}\), with \(a>1\). The reciprocal weight is \(\gg\sqrt{\log X/\log(3y)}\): use [Mertens in progressions](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf), and discard at most half via the bound \(O(\delta\log X)\) on the reciprocal-weighted average of \(\log a\). Choose fixed \(\delta\) small. The prime number theorem in the fixed class \(493a^{-1}\bmod672\) gives \(\gg X/(a\log X)\) primes in \([X/a,3X/(2a))\), uniformly over the allowed \(a\). They are split and strictly larger than the other factors, so each residual is counted once. Adding the shift keeps \(n\) in \([X,2X)\). Summing over shifts then applying Cauchy–Schwarz on \(n\) gives the claimed order for all pairs before dropping the negligible diagonal.

For a common prime \(p\), we have \(p\mid h=s-t\ne0\). Because \(|h|\le2\sqrt X\), it must come from the small cofactors, with \(y<p\le X^{1/8}\). Divide both norms by \(p\), which is split, and use [Rieger's pair upper bound](https://arxiv.org/pdf/1311.1396#page=8) to count at most \(O(XC(h)/(p\log X))\) pairs for this choice, where \(C(h)=\prod_{q\mid h,\ q\equiv3(4)}(1+1/q)\); replacing \(h/p\) by \(h\) in the bound is harmless. The average over shifts of \(C(h)\sum_{p\mid h,\ p>y,\ p\equiv1(4)}1/p\) is \(O(\log(3y)/\sqrt y+(\log\log X)/\sqrt{\log X})\). Indeed expand \(C(h)\), absorb the factor for 3, and put \(m=pd\) with \(d\) squarefree and inert-supported. Fixing three exponents allows at most one class of the remaining base-3 index modulo \(\operatorname{ord}_m(3^{24})\). The uniform endpoint error for all \(m\le2\sqrt X\) is at most \((\log X)^{-1}\) times the inert reciprocal divisor sum \(O(\sqrt{\log X})\) and the split-prime reciprocal sum \(O(\log\log X)\). The reciprocal mass of moduli of order at most \(J\) divides the Euler product of \(\prod_{j\le J}(3^{24j}-1)\); it is \(O(\log(3J))\) by Mertens and splitting at the log of that product. With the additional requirement \(p>y\), this is multiplied by \(O(\min(1,J^2/y))\), since the sum of reciprocals of such eligible primes dividing the product is \(O(J^2/y)\). Dyadic summation in the order gives the asserted bound. Choosing \(y\) large and fixed makes the subtraction smaller than the lower bound above. No uniformity in a growing \(y\) is proposed.

## Exact same-integer control

For \(n=96834161246447\equiv527\bmod672\) and \(w=9710422\), the labels \((26,2)\) and \((2,2)\) in the ordinary active box produce \(w^2+3^2=17\cdot5546605612829\) and \(w^2+(3^{13})^2=29\cdot3339109008497\), respectively. The two residuals are coprime and squarefree. This finite example is in the ordinary box, not in the narrower asymptotic rectangular grid.

```python
from math import gcd,isqrt
n,w=96834161246447,9710422
u,v=5546605612829,3339109008497
r,s=n-3**26-25,n-3**2-25
assert n%672==527 and 4*max(3**26,25)<n
assert r==w*w+9==17*u and s==w*w+3**26==29*v and gcd(r,s)==1
for p in (17,29,u,v):
    assert p%4==1 and all(p%d for d in range(2,isqrt(p)+1))
```
