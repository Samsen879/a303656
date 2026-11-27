# A counted second Gaussian certificate and a fixed-menu limit

The fixed cell **\((c,d)=(3,1)\)** has a primitive two-square remainder for \(\gg X/(\log X)^{3/2}\) distinct primes \(p\le X\) in the family \(n=5p+52\), \(p\equiv1\pmod{12}\). The remainders in this construction are composite. A separate CRT argument shows that every fixed finite menu of cells away from \((3,2)\) fails on infinitely many primes in the same family.

### A counted class with full Gaussian certificates

Take primes of the form
\[
p=5(u^2+v^2)-4,\qquad \gcd(u,v)=1,\qquad p\equiv1\pmod3.
\]
Fuchs–Hsu–Rickards–Schindler–Stange give the lower bound for **distinct prime values** with \(f=u^2+v^2\), discriminant \(-4\), shift \(A=-4\), multiplier \(B=5\), and progression \(1\bmod3\). The leading coefficient is \(1\), \((A,B)=1\), \(AB\) is even, and the progression checks are \((1,3)=(3,40)=(1-A,3)=1\). Apply Theorem 1.1(2) directly, since the remaining form and progression hypotheses are satisfied. Its part (1) gives the matching upper bound for this class. [Shifted quadratic forms, Theorem 1.1 and Proposition 3.8](https://arxiv.org/html/2504.20289v1)

For odd \(p\), the odd norm \(u^2+v^2\) is \(1\bmod4\). Thus the counted primes satisfy \(p\equiv1\pmod{60}\). After discarding \(p\le80\), both \((3,1)\) and \((3,2)\) are active since \(4\max(27,25)=108<n\). At the new cell,
\[
R=n-3^3-5=5(p+4)=25(u^2+v^2)
  =(3u\mp4v)^2+(\pm4u+3v)^2.
\]
At least one sign gives coprime coordinates \(x,y\). Away from \(5\) each matrix is invertible modulo every prime, since its determinant is \(25\). Modulo \(5\) the two kernels are the distinct lines \(v=2u\) and \(v=3u\), and the primitive input lies on at most one. Then \(y\) is invertible modulo \(R\), and \(xy^{-1}\bmod R\) is a root of \(-1\) modulo the **whole** remainder.

For example, \(p=421\) gives \(n=2157\) and \(u^2+v^2=2^2+9^2=85\). One sign gives the primitive certificate \(2125=42^2+19^2\) with root \(1568\bmod2125\). At the earlier fixed-base obstruction \(p=109,\ n=597\), the new cell also succeeds, with \(565=6^2+23^2\). [Verified fixed-base obstruction](https://github.com/Samsen879/a303656/commit/2f72f3b6a98423627c7f27b99e794ee7bb311705)

### Fixed-menu limit and the original cell

For each offset \(F_i=3^{c_i}+5^{d_i}\ne52\) in a fixed finite menu, choose a distinct prime \(q_i\equiv3\pmod4\) with \(q_i\nmid60(52-F_i)\). Impose
\[
5p+52-F_i\equiv q_i\pmod{q_i^2},\qquad p\equiv1\pmod{60}.
\]
These conditions combine into a reduced residue class. Dirichlet’s theorem supplies infinitely many primes in it. For all sufficiently large such primes the menu is active, and each remainder has an inert prime of valuation exactly one. An explicit control is \(p=661,\ n=3357\), where the new cell has remainder \(3325=25\cdot7\cdot19\), while the original cell has \(3305=13^2+56^2\).

There is also a scalable certificate at the original cell for **every** prescribed prime in the family. Recover \(p=(n-52)/5\), sample a quadratic nonresidue modulo \(p\) by Euler’s criterion, and raise it to \((p-1)/4\). A uniform nonzero base takes two trials in expectation. Combine the resulting root modulo \(p\) with \(2\bmod5\) by CRT to obtain a verified root modulo \(R=5p\). The new-cell theorem is a counting guarantee. Selection from a growing menu for every prescribed target remains open.

### Standalone replay

```python
from math import gcd, isqrt

def remainder(p, c, d):
    n = 5*p + 52
    assert p > 80 and p % 12 == 1
    assert all(p % q for q in range(2, isqrt(p)+1))
    assert 4*max(3**c, 5**d) <= n
    return n - 3**c - 5**d

for p,u,v,expected in [(181,1,6,(925,-21,22,882)),
                       (421,2,9,(2125,42,19,1568))]:
    assert gcd(u,v) == 1 and p == 5*(u*u+v*v)-4 and p % 60 == 1
    R = remainder(p,3,1)
    for e in (1,-1):
        x,y = 3*u-4*e*v, 4*e*u+3*v
        assert x*x+y*y == R
        if gcd(x,y) == 1:
            break
    t = x*pow(y,-1,R) % R
    assert (R,x,y,t) == expected and (t*t+1) % R == 0

assert remainder(661,3,1) == 25*7*19 == 3325
assert 3325 % 49 and (661+4) % 49 == 28 and gcd(661,2940) == 1
assert remainder(661,3,2) == 13**2+56**2
assert remainder(109,3,1) == 6**2+23**2
R = remainder(109,3,2)
assert R == 545 and gcd(R,pow(3,(R-1)//2,R)+1) == 1
assert (142**2+1) % R == 0
print("all exact controls passed")
```

No level-of-distribution assumption or two simultaneous primes is needed for this counted family. It has a second fixed-offset witness on the counted subfamily; it does not establish pointwise coverage outside the original prescribed family.
