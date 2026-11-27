# Independent shifts at three labels with Gaussian gcd norms 2 and 10

There are \(X^{1/3-o(1)}\) different integers \(n\le X\) in the following construction, with one fixed triple of labels for each height batch. Each has the stated adjacent Gaussian gcd norms. None can be obtained at these same labels from the earlier common-vertical-shift model. This is a construction for a sparse set, not a pointwise representation result.

Let \(f=3^j\) with \(j\equiv1\bmod8,\ j\ge9\), and \(D\) even. In the lattice \(\mathbb Z^2\) take a primitive \(p=(a,b)\equiv(1,1)\bmod19680\), and complete it to \(q=(c,d)\equiv(614,615)\bmod19680\) with \(\det(p,q)=1\). Start with any Bezout completion. Modulo \(19680\) the target completion has determinant one and differs from the initial one by a multiple of \(p\), since \(a\equiv1\). Adding that multiple, then optimizing by multiples of \(19680p\), gives \(\|q\|=O(\|p\|)\).

Solve the integral linear system
\[
 Z\cdot p=131220f^2-\|p\|^2/2,\qquad Z\cdot q=66430f^2-\|q\|^2.
\]
Take \(z_0,z_1,z_2\) to be \(1+i\) times the Gaussian integers corresponding to \(Z,Z+p,Z+2q\). Expanding norms gives successive increases \(524880f^2\) and \(6560f^2\). Thus the same \(n\) is obtained with labels \((2j+12,D),(2j+8,D),(2j,D)\), respectively.

The three norms are \(2\bmod8,\ 1\bmod3\) by the fixed residues. The two increase factors are \(2^4 3^8 5\) and \(2^5 5\cdot41\). At \(5\), the vectors before multiplying by \(1+i\) are \((1,3),(2,4),(-1,3)\); the first hits only the root \(i=-2\), and the other two only \(i=2\). At \(41\), the middle vector is \((-6,23)\), of nonzero norm modulo \(41\). Hence the adjacent integer gcds are \(10,10\), with Gaussian gcd norms \(2,10\).

## Separate from the common vertical shift

In the [common vertical shift](NONAFFINE_TWO_PARAMETER_TRANSFER.md) model let the unscaled vertical coordinates be \(639f+w,819f+w,821f+w\) and write \(u=X_0^2\) for the first horizontal square. Then \(u-360fw\) and \(u-364fw\) must both be squares. If the first residual divided by two is \(1\bmod4\), exhaustive reduction modulo \(64\) forces it to be \(9\) or \(13\bmod16\). The present model gives \(Z\equiv(12,7)\bmod16\), making it \(1\bmod16\). The short exhaustive check below covers both possible \(f\bmod64\).

## Count and independent replay

Among \(1\le a,b\le L\), a fixed class \((1,1)\bmod19680\) contains \(\gg L^2\) primitive pairs (Möbius inversion on the common divisor). Choose the same admissible \(f\asymp L\) and the same \(5^D\asymp L^6\) for the whole batch. Inverting the determinant-one system gives \(\|Z\|=O(L^3)\) and \(n\asymp L^6\). For a fixed \(n\), the ordered pair \(Z,Z+p\) determines \(p\), and each of those two vectors has at most \(n^{o(1)}\) possibilities by the two-square representation bound. Taking \(L\) a small constant times \(X^{1/6}\) proves the count with the claimed quantifiers. In particular both exponent sizes are logarithmic in these batches.

~~~python
from math import gcd
P = {x*x % 64 for x in range(64)}
for f0 in {pow(3,9,64), pow(3,17,64)}:
    V = {(u+(639*f0+w)**2)%16 for u in P for w in range(64)
         if (u-360*f0*w)%64 in P and (u-364*f0*w)%64 in P
         and (u+(639*f0+w)**2)%4 == 1}
    assert V == {9,13}
f, D = 3**9, 20
a,b,c,d = 1,1,614,615
assert a*d-b*c == 1
A = 131220*f*f - (a*a+b*b)//2
B = 66430*f*f - c*c-d*d
x,y = d*A-b*B,a*B-c*A
Z = [(x,y),(x+a,y+b),(x+2*c,y+2*d)]
R = [2*(u*u+v*v) for u,v in Z]
n = 3**30 + 5**D + R[0]
assert n == 3897206499689708539323722800403564
assert all(r == n-3**e-5**D > 0 and r%8 == 2 and r%3 == 1
           for e,r in zip((30,26,18),R))
assert R[0]//2%16 == 1 and gcd(R[0],R[1]) == gcd(R[1],R[2]) == 10
assert [((u+2*v)%5==0,(u-2*v)%5==0) for u,v in Z] == [
    (False,True),(True,False),(True,False)]
~~~
