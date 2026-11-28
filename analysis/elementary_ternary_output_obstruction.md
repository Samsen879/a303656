# An elementary infinite obstruction for bounded-support ternary outputs

This is an obstruction to a specified output bridge, not a counterexample to Sun's two-square conjecture. Let \(M=10626=2\cdot3\cdot7\cdot11\cdot23\). For arbitrarily large \(k\), every solution \(0\le A<M^{2k}\) of \(A^2\equiv-4847\bmod M^{2k}\) gives
\[
n=A^2+4847=A^2+69^2+3^4+5.
\]
Every actual label \(S=3^c+5^d\le n\) with \(n-S\) a sum of two squares then has odd valuation at some prime \(p\equiv3\bmod4\) outside \(\{3,7,11,23\}\).

In particular, consider a family of rational positive definite ternary spaces whose anisotropic primes \(p\equiv3\bmod4\) are confined to this set. A rational equivalence up to nonzero scale to \(\langle1,1,P\rangle\) cannot output any valid label as \(S=Pz^2\) with \(z\in\mathbb Q\) at these targets. At an excluded prime, \(v_p(S)\equiv v_p(P)\bmod2\), and \(X^2+Y^2=-PZ^2\) has no nonzero solution over \(\mathbb Q_p\), as a nonzero sum of two squares has even valuation. Rational basis change and common nonzero scaling preserve isotropy.

## An elementary five-point valuation lemma

Among \(K,128K,\ldots,128^4K\) for every \(K\ge64\), at least one \(k\) has
\[
v_p(3^c+5^d)<2k-1 \qquad (p\mid M,\quad c+d<60k).
\]
For \(p=3\) the only possible positive valuations are \(1+v_3(d)\), at \(c=0\) and \(d\) odd. Those do not hit the threshold. Fix another \(p\mid M\) and write \(g=2\) for \(p=2\) and \(g=p-1\) otherwise. A hit implies \(3^{gc}=5^{gd}\bmod p^{2K-1}\). Two hits eliminate one variable and imply \(p^{2K-1-v_p(3^g-1)}\mid cd'-c'd\) by LTE. At \(p=2\), \(3^g\equiv1\bmod8\), so the same LTE formula applies. The determinant is strictly smaller in absolute value than \((60\cdot128^4K)^2<2^{2K-4}\), and \(v_p(3^g-1)\le3\). Thus every hit for this prime is on the same integer ray.

If the ray hits at two candidates \(k_0<k_1\), write the labels as \(X^{r_0}+Y^{r_0}\) and \(X^{r_1}+Y^{r_1}\), where \(X,Y\) are the powers corresponding to the ray's primitive vector. Applying LTE to \(X^{2r_0r_1}-Y^{2r_0r_1}\) in two ways shows that their valuation difference is \(v_p(r_1)-v_p(r_0)\): at odd \(p\), the difference factors \(X^{r_i}-Y^{r_i}\) are units, while at 2 each has valuation one. The earlier label is below \(2^{180k_0+1}\) and \(r_1<60\cdot128^4K\). Consequently the later valuation is less than \(180k_0+35+K/4<2k_1-1\), a contradiction. These numerical inequalities at \(K=64\) persist for larger \(K\) by monotonicity (use \(\log_2 K\le K/4\) there). At most four candidates can be excluded by the four primes, proving the lemma.

For each such \(k\), square roots exist by simple lifting at the odd primes and \(-4847=1\bmod8\) at 2. The exact bound \(M^4+4847<\min(3^{36},5^{24})\) puts all labels in \(c+d<60k\). Valuation transfer from \(S\) to the positive residual \(n-S\) forces even valuation at \(3,7,11,23\). Dividing by \(2^{v_2(S)}\) and taking residues modulo 4 shows the odd part of \(S\) is \(3\bmod4\). That supplies the excluded prime.

The same reasoning applies to any fixed finite set \(\mathcal P\) of inert primes. Include 2 and 3 in the modulus along with \(\mathcal P\), choose an even positive \(c\) divisible by the orders of 3 at the remaining primes, and use the base label \(3^c+5\). This is \(6\bmod8\) and a unit at every odd modulus prime. The norm over each inert finite field is onto; for this nonzero value choose a representation of the negative label and swap coordinates so its first coordinate is nonzero. By CRT choose an odd fixed second coordinate matching those representations. Its square plus the base label plays the role of 4847. The ray argument only requires a finite number of primes, a linear bound on the exponent box, and fixed LTE constants: choose a sufficiently large fixed multiplicative separation between samples, one more sample than there are non-3 primes, and then \(K\) large enough that the exponential lower bound overwhelms the polynomial determinant bound. This gives an unbounded sequence without any two-logarithm estimate.

## Exact controls and scope

The replay certifies the valuation guard at \(k=11,64\), reconstructs a native 586-bit example, and confirms the six true labels at 2016. Adding an explicit fourth-variable label correction yields a different output at the native example: \(n=A^2+61^2+626+500\) with both 626 and 500 square-sums. The correction is not absorbable into one true label, since 1126 is not a 3/5 power sum; this does not give an ordinary ternary output mechanism.


```python
from math import isqrt

M, ps = 10626, (2, 3, 7, 11, 23)
assert M**4 + 4847 < min(3**36, 5**24)
for p in (2, 7, 11, 23):
    g = 2 if p == 2 else p-1
    assert all((a**g-1) % p**4 for a in (3, 5))

def conflict(k, p):
    m = p**(2*k-1)
    left = {}
    x = y = 1
    for c in range(60*k):
        left.setdefault(x, c)
        x = 3*x % m
    for d in range(60*k):
        c = left.get(-y % m, 60*k)
        if c+d < 60*k:
            return c, d
        y = 5*y % m

assert conflict(10, 2) == (381, 151)  # 三角窗反控
assert all(conflict(k,p) is None for k in (11,64) for p in ps)

A, B = 0, 1
for p,r,e in ((2,1,3),(3,1,1),(7,2,1),(11,2,1),(23,11,1)):
    m = p**e
    assert (r*r+4847) % m == 0
    while e < 22:
        if p == 2:
            if (r*r+4847) % (2*m):
                r += m//2
        else:
            r += m*(-((r*r+4847)//m)*pow(2*r,-1,p) % p)
        m *= p
        e += 1
    assert (r*r+4847) % m == 0
    A += B*((r-A)*pow(B,-1,m) % m)
    B *= m
n = A*A+4847
assert B == M**22 and 0 < A < B and n % B == 0
assert n == A*A+69**2+3**4+5

def labels(n):
    return [(c,d,3**c+5**d) for c in range(n.bit_length())
            for d in range(n.bit_length()) if 3**c+5**d <= n]

rows = []
for c,d,S in labels(2016):
    R = 2016-S
    pairs = [(a,isqrt(R-a*a)) for a in range(isqrt(R//2)+1)
             if a*a+isqrt(R-a*a)**2 == R]
    if pairs:
        rows.append((c,d,S,len(pairs)))
assert rows == [(2,3,134,1),(3,3,152,1),(4,1,86,2),
                (4,3,206,2),(5,1,248,2),(6,1,734,1)]

assert n == A*A+61**2+626+500
assert 626 == 1+5**4 == 1+25**2
assert 500 == 5**4-5**3 == 10**2+20**2
assert all(S != 1126 for _,_,S in labels(1126))
assert ((n-626)//2)%4 == 3 and 1126 == 2*563
assert all(563%p for p in range(2,isqrt(563)+1))
print("k=11,64 clear;", n.bit_length(), "bits;", rows)
```
