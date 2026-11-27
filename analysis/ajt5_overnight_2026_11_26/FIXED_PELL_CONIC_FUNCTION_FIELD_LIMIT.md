# No third rational-function norm on the fixed joint Pell conic

On the original conic \(U^2-5p^2=C=10924\) over \(\mathbb Q\), the expression \(5p^2+K\) is a rational-function sum of two squares for the two actual labels \(K=10940,10928\) from [the joint-label orbit](JOINT_LABEL_PELL_ORBIT.md). **There is no third such identity for any label \(K=10942-5^e-3^f\) with \(e,f\ge0\)**, even allowing arbitrary rational functions in U and p. It does not follow that a third label cannot work at individual points. A [different projection and conic](JOINT_TRIPLE_AND_CROSS_BASE_PELL_ORBITS.md) already give a true infinite triple.

## Exact criterion after extending constants

For any nonzero rational C let \(E=\mathbb Q(\sqrt5)\) and \(z=U+\sqrt5p\). Multiplying \(5p^2+K\) by \(4z^2\) gives the monic quartic
\[
R(z)=z^4+(4K-2C)z^2+C^2.
\]
It is a norm from \(E(i)(z)\) precisely if it is already the norm of a monic quadratic polynomial in \(E(i)[z]\). Indeed, in the UFD \(E(i)[z]\), a rational-function norm has even order at every conjugation-fixed monic irreducible; pair the other factors by conjugation to construct a monic polynomial of the required norm. Writing this quadratic as \(z^2+iaz+s+ir\), with real-algebraic coefficients in E (the vanishing cubic coefficient forces the linear coefficient to be purely imaginary), its linear term in the norm forces \(ar=0\). If \(a=0\), comparison gives \(s=2K-C,\ r^2=4K(C-K)\). If \(r=0\), one has \(s=\pm C\) and \(a^2=4K\) or \(4(K-C)\). Thus the exact criterion over \(E(z)\) is that at least one of \(K,\ K-C,\ K(C-K)\) is a square in E, with zero allowed. A rational number is a square there iff it is a rational square or five times one, by expanding \((a+b\sqrt5)^2\).

For the actual C, every negative K fails all three tests by sign. Nonnegative actual labels lie in \(0\le e\le5,\ 0\le f\le8\). Exact enumeration leaves only \(K=10940,10928,4356,10816\) over E. The last two pass only as candidates over this larger field; they are not norms over the original rational conic.

## Descending the last two obstructions

For \(K=4356=66^2\) or \(K=10816=104^2\), choose a zero of \(5p^2+K\): \(p_0=\sqrt{-K/5}\), \(U_0=\sqrt{C-K}\). This defines a closed point on the rational conic whose residue field is \(\mathbb Q(\sqrt{-5},\sqrt{C-K})\). It does not contain i. In fact \(C-K>0\), and none of the possible nontrivial quadratic square classes \(-5,C-K,-5(C-K)\) equals \(-1\); for the last, \(5(C-K)\) equals 32840 or 540, neither a square. The zero is simple because \(U_0\ne0\) makes \(p-p_0\) a parameter at the geometric point and \(10p_0\ne0\). At that valuation adjoining i gives an unramified quadratic residue-field extension (the constant polynomial \(T^2+1\) has unit discriminant and is irreducible in the residue field). Norms from that extension have even valuation, since the extended valuation is fixed by conjugation. Thus \(5p^2+K\) is not a norm over the original conic. The first two offsets are identities over the original conic by \(K-C=16,4\). This completes the classification for the actual menu. For background on this setting see [Grimm, *Sums of squares in function fields of conics*](https://www.math.uni-konstanz.de/~grimm/Grimm.pdf).

A nonnorm here also stays a nonnorm under any odd-degree finite field extension: i is still absent, and taking the field norm of a putative representation would make an odd power of the original element a Gaussian norm, by transitivity. Every square is already a Gaussian norm. Even-degree covers remain outside the claim.

## Pointwise countercontrol and replay

At the original seed \(p=1599\) both designated labels work, and \(K=10936,10856,10208\) work as well. Thus one integer on this conic realizes at least five true labels, despite the absence of a third rational-function identity. This proof does not settle infinitude of third-label values on the same Pell orbit.

~~~python
from math import isqrt
C=10924
def square(n):
    return n>=0 and isqrt(n)**2==n
def squareE(n):
    return square(n) or (n%5==0 and square(n//5))
got=[]
for e in range(6):
    for f in range(9):
        K=10942-5**e-3**f
        if any(squareE(v) for v in (K,K-C,K*(C-K))):
            got.append((e,f,K))
assert got==[(0,0,10940),(1,2,10928),(2,8,4356),(3,0,10816)]
assert all(square(K) and C>K and not square(5*(C-K)) for K in (4356,10816))
assert 3577**2-5*1599**2==C
for K,a,b in [(10940,3577,4),(10928,3577,2),(10936,405,3554),
              (10856,806,3485),(10208,2098,2897)]:
    assert a*a+b*b==5*1599**2+K
~~~
