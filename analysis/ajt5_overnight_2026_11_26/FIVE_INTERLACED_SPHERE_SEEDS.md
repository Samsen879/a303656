# Five interlaced free-sphere seeds in both odd target classes

**Five exact norm seeds reduce the moving-exponent height gaps and give \(\gg_\epsilon X^{13/34-\epsilon}\) distinct targets up to \(X\) in each odd class modulo \(4\).** Both positive exponents grow. At a fixed height, the construction gives \(B^{1/2-o(1)}\) targets, and allowing a second free coordinate within the same norm factorization cannot increase that power of \(B\).

### Interlacing the heights

Use the following seeds, each satisfying \(5^m-3^e=a^2+3b^2\).

| \(m\) | \(e\) | \(a\) | \(b\) |
|---:|---:|---:|---:|
| 2 | 2 | 4 | 0 |
| 22 | 6 | 7139528 | 27887948 |
| 26 | 10 | 1220699108 | 1808048 |
| 34 | 34 | 758993440348 | 44742038272 |
| 14 | 10 | 5128 | 45008 |

For \(k\ge2\), put \(Q=5^{m3^k}\), \(W=3^{e3^k}\), and \(B=5Q\). Iterating \(U^3-V^3=(U-V)(U^2+UV+V^2)\) gives an integral norm factorization, since for odd \(U,V\),
\[
U^2+UV+V^2=\left(\frac{U-V}{2}\right)^2+3\left(\frac{U+V}{2}\right)^2.
\]
Multiplying the seed and the cubing factors in \(\mathbb Z[\sqrt{-3}]\), and multiplying the result by \(2\), gives \(v^2+3t^2=4(Q-W)\).

We can enforce \(3\nmid t\) and \(t^2\asymp B\) simultaneously. Each cubing factor has imaginary-to-real ratio \(1\bmod3\), and conjugation reverses it. Keep all factors after the first two fixed. If the remaining product has ratio zero, use the first two with equal signs. Otherwise use opposite signs. Both conjugate choices in the selected pair give \(3\nmid t\). The product of the first two factors has nonzero real and imaginary parts for either sign pattern. For such a fixed factor \(a_0+b_0\sqrt{-3}\), the two possible imaginary parts after multiplication are \(a_0C\pm b_0A\). Their larger absolute value is a fixed positive fraction of the norm’s square root.

For \(\lambda=1\) or \(3\), set \(P=\lambda W\) and \(A=(4-\lambda)W\). This exchanges the signed and positive \(3\)-powers between the two odd classes. Take a three-square representation
\[
x^2+y^2+r^2=N=3t^2+2P,\qquad r\text{ odd},\qquad S=x^2+y^2>P.
\]
The same target then satisfies
\[
n=B+P-S=Q+A+v^2+r^2,\qquad 2P-S=r^2-3t^2.
\]
Here \(Q<n<B\). Since \(N\equiv2\pmod4\) and \(N\equiv3\pmod9\), the triple has exactly two odd coordinates and all three are units modulo \(3\). Hence \(n\equiv\lambda\pmod4\), and the signed ternary residual \(n-B=P-S\) is a unit.

### Count and ceiling

The Gauss–Siegel bound gives \(\gg_\epsilon B^{1/2-\epsilon}\) three-square triples at this \(N\asymp B\). Two thirds have \(r\) odd, and each \(|r|\) has only \(B^{o(1)}\) Gaussian representations of \(N-r^2\). The cutoff \(S>P\) discards \(O(1+P/\sqrt B)\) possible values of \(|r|\), negligible since \(P\ll B^{\log3/\log5}\). Distinct \(|r|\) give distinct targets. [Gauss’s formula](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_30) · [Siegel’s bound](https://bibliotekanauki.pl/articles/1395111)

After normalizing by powers of \(3\), the exponents have phases
\[
2,\quad 22/9,\quad 26/9,\quad 34/9,\quad 14/3,\quad 6.
\]
The last entry is the first phase of the next cycle. The largest consecutive ratio is \(17/13\), so the highest available \(B\le X\) exceeds \(X^{13/17}\). This gives the stated uniform count.

For the ceiling, at fixed signed and positive powers any transfer retaining \(r\) must satisfy \(v^2+3t^2=B-Q-P-A\). There are \(O(\tau(B-Q-P-A))=B^{o(1)}\) choices of \((v,t)\) when the right side is positive: count elements of the given norm in the full Eisenstein integer ring by unique factorization, up to its six units. The integral pairs in the subring are a subset. Each allows only \(O(\sqrt B)\) distinct \(|r|\), and varying \(x,y\) at fixed \(r,t\) changes no target. The exponent \(13/34\) is also sharp in the liminf for **this interlacing**: at \(X=5^{34\cdot3^k}\), the next height supplies no target yet, and the preceding height is \(5^{26\cdot3^k+1}\).

**Generation** chooses an admissible \(r\) on the sphere. **Recognition** starts from \(n\), takes the least \(5^D>n\), and strips powers of \(3\) from \(D-1\) to identify the seed. A fixed conjugation convention reconstructs \(v,t\). Testing \(n-Q-A-v^2\) for an odd square recovers a true positive witness. Signed-family membership additionally requires \(N-r^2\) to be a Gaussian norm. This is a test for the constructed family, with no coverage claim for arbitrary targets.

```python
from itertools import product
from math import isqrt

seeds = [(2,2,4,0), (22,6,7139528,27887948), (26,10,1220699108,1808048),
         (34,34,758993440348,44742038272), (14,10,5128,45008)]

def mul(z,w):
    a,b = z
    c,d = w
    return a*c-3*b*d, a*d+b*c

for m,e,a,b in seeds:
    X,Y = 5**m,3**e
    assert a*a+3*b*b == X-Y
    f = ((X-Y)//2,(X+Y)//2)
    X,Y = X**3,Y**3
    g = ((X-Y)//2,(X+Y)//2)
    Q,W = X**3,Y**3
    lifts = [mul((2*a,2*b),mul((f[0],i*f[1]),(g[0],j*g[1])))
             for i,j in product((1,-1),repeat=2)]
    t,v = max((abs(t),abs(v)) for v,t in lifts if t%3)
    assert v*v+3*t*t == 4*(Q-W)
    u = isqrt(W)
    assert u*u == W
    for lam,x,y in ((1,t-u,t),(3,t+u,t-2*u)):
        r,S,P,A = t+u,x*x+y*y,lam*W,(4-lam)*W
        n = 5*Q+P-S
        assert Q<n<5*Q and n%4 == lam and (n-5*Q)%3
        assert 2*P-S == r*r-3*t*t
        assert n == Q+A+v*v+r*r
```

Independent BigInt checks covered all five seed norms, exact reconstructed positive and signed identities for both odd classes at every seed, and the maximum consecutive phase ratio. This gives a lower count for generated targets only, not a test that covers arbitrary preassigned integers.
