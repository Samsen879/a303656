# Two-sided size margins force multiple primitive penultimate blocks

**Yes. Both sides can be forced to use at least two distinct penultimate primitive blocks, with the earlier shares unrestricted.** This holds for a specified true highest-block share on a cofinal refinement of the pinned balanced family. The argument scales to any fixed number of blocks on each side. It also leaves a precise obstacle to closing the ordinary window. [Pinned refined-primitive result](https://github.com/Samsen879/a303656/commit/f79fcf8fc5a843fa61ab55f9af8b26be2526dd74)

### A two-sided exponent margin

Suppose the highest block has size \(T\asymp A^t\), and the prescribed true short-side share has size \(w\asymp A^\sigma\). Let the entire earlier product be \(O(A^\lambda)\). For a fixed refinement, write \(\beta_1\ge\beta_2\ge\cdots\) for the size exponents of the coprime penultimate blocks.

If a side uses at most \(k\) blocks, give it the **entire** earlier product and the \(k\) largest blocks. That side is still too small for ordinary height, for all sufficiently large \(A\), whenever
\[
\sigma+\lambda+\sum_{i=1}^k\beta_i<\tfrac12
\quad\text{on the short side},\qquad
t-\sigma+\lambda+\sum_{i=1}^k\beta_i<\tfrac12
\quad\text{on the long side}.
\]
The proof uses the exact complementary top share \(T/w\) and the fact that both ordinary factors exceed \(4\sqrt A\). A block used only in part still receives its full size allowance in this test.

### An explicit cofinal exclusion

Keep \(g=468741\), \(n=1331g\), and the pinned \((h,k)\) progression. Impose \(19\cdot23\mid h,k\), which is compatible with its period. For \(x=3^h,\ y=5^k\), choose the true short-side top share
\[
w_*=\prod_{j\in\{468741,3939,1717\}}\Phi_{2662j}(x,y).
\]
Its exponent is \(\sigma=2344000/5156151\). Refining \(D_2\) by the additional common exponent \(19\cdot23\) makes its largest block exponent
\[
\beta_1=\frac{27648000}{751079329}.
\]
With **all** of \(E=24D_0D_1\) available, \(\lambda=1/121\) and \(t=10/11\). The short and long margins at \(k=1\) are respectively
\[
\frac{15954223}{49571235714},\qquad
\frac{21626483}{49571235714}.
\]
For all sufficiently large balanced members, **either side touching only one refined \(D_2\) block excludes the entire ordinary window** for \(w_*\). The original pinned share \(w\) also forces at least two refined \(D_2\) blocks on the short side for sufficiently large \(a\), with all of \(E\) available.

### How far it scales

For every fixed \(m\), a further cofinal refinement forces **at least \(m\) blocks of \(F_2\) on each side**, even allowing the full product \(24D_0D_1C_2\), of exponent \(13/363\), on either side in the upper bound. Choose additional common-exponent primes \(q\equiv2\pmod3\), avoiding the fixed period and existing indices. They cannot collide with primes of \(F_2\), whose orders force \(p\equiv1\pmod3\). The largest refined block exponent decreases by \(\prod_q(1-1/q)\), which can be made arbitrarily small. This follows from the Euler product for \(\zeta(s)/L(s,\chi_3)\) as \(s\downarrow1\). Each fixed \(m\) has its own refinement and height cutoff.

The remaining gap in the method is concrete. Assign the old block \(R\) wholly short and every other \(D_2\) block wholly long. For \(w_*\), the short earlier share must then have exponent
\[
\frac12-\sigma-\frac{\tau}{11}
=\frac{541661}{113435322}\in(0,1/121).
\]
The complementary earlier exponent is positive too. This allocation remains compatible with both size budgets after any further refinement, by keeping the descendants of \(R\) together. Closing it requires an **actual** divisor of \(E\) in the short interval after division by \(w_*R\), or a further test on the two remaining integer squares.


The verification below concerns the exact cyclotomic size exponents, CRT compatibility and the strict margins. It does not assert that an exact pair passes any additional local square test. On a fixed refinement, any homogeneous cyclotomic factor of index \(j\) has size comparable to \(A^{\varphi(j)/N}\), since the input-base ratio is bounded on the balanced strip and the finitely many factors in the Möbius product preserve both bounds. This is enough for the asymptotic exclusions above.

```python
from fractions import Fraction as F
from math import gcd
def phi(n):
    y=n
    j=2
    while j*j<=n:
        if n%j==0:
            y=y//j*(j-1)
            while n%j==0:n//=j
        j+=1
    return y if n==1 else y//n*(n-1)
g=468741
N=1331*g
aux=19*23
period=21112080
assert gcd(aux,period)==1
assert all(g%j==0 for j in (468741,3939,1717))
sigma=sum((F(phi(2662*j),N) for j in (468741,3939,1717)),F(0))
tau=F(phi(2*N),N)
beta=F(phi(242*g*aux),N*aux)
assert (sigma,tau,beta)==(F(2344000,5156151),F(768000,1718717),F(27648000,751079329))
opt=F(10,11); lam=F(1,121)
assert (F(1,2)-sigma-lam-beta,F(1,2)-opt+sigma-lam-beta)==(
 F(15954223,49571235714),F(21626483,49571235714))
gap=F(1,2)-sigma-tau/11
assert gap==F(541661,113435322) and 0<gap<lam
assert max(sigma,opt-sigma)+F(13,363)<F(1,2)
print("OK")
```
