# Seventh-power reciprocity rejects the two factors in an actual neutral row

This treats the previously open \((13,67)\) row of [the known high-order barrier](https://github.com/Samsen879/a303656/commit/24da2e41c8d228736218edb4f798e007bb158411) by its **known** complete split \(R=Dq\). The earlier certificate regenerates the unique root and all seven native lifts of the tag \((25,171)\) and certifies the large prime \(q\). The companion \(D\) is independently trial-certified here. Its mismatch and \(q\)'s mismatch close this individual row; no cohort total or factor-free complete-row claim follows.

For modulus \(M\in\{R,D,q\}\), write \(y=x^{49}\bmod M\) and form \(I=(M,\zeta_7-y)\) in \(\mathbb Z[\zeta_7]\). Evaluation at \(y\) onto \(\mathbb Z/M\mathbb Z\) is a ring map, and \(I\) is its kernel of index \(M\). The displayed coefficient vector \(\alpha\) is in \(I\), and its multiplication determinant has absolute value \(M\). Thus \(I=(\alpha)\). Its value at 1 is nonzero modulo 7, and its derivative vanishes modulo 7, so it is primary: the Taylor expansion at \(\zeta_7=1\) gives a rational integer mod \((1-\zeta_7)^2\).

For a rational numerator \(b\), [Eisenstein reciprocity in the rational-numerator form](https://www.degruyterbrill.com/document/doi/10.1515/jmc-2020-0013/html) equates \((b/I)_7\) with the symbol of \(\alpha\) modulo \((b)\) here. Both 3 and 5 have order 6 modulo 7, so \((3)\) and \((5)\) are inert in the degree-six field. The small exponents \((3^6-1)/7=104\) and \((5^6-1)/7=2232\) give the two logarithms relative to \(\zeta_7\). The argument depends on neither the large prime-to-7 order nor a search for a short full-modulus mask.

At a prime \(p\mid R\), set \(s=(p-1)/343\). A valid joint lift has phase exponents \(E\) and \(kE\) relative to \(x\) for its 7-primary components. Taking \((p-1)/7\)-th powers gives \((se,sek)\bmod7\) as logarithms relative to \(y\), with \(e=E\bmod49\). The prime-to-7 part drops out. Here the native tag requires \((1,3)\) at \(q\) and \((0,0)\) at \(D\); the measured pairs are \((3,1)\) and \((2,5)\), respectively. Direct prime symbol powers agree with the two independently recomputed reciprocity calculations.

On the full composite, the computed pair is \((5,6)\). A mismatch there establishes that at least one component fails, not that they all do; addition of symbol exponents expressly allows cancellation. The calculations on the two known prime parts are why this particular row closes. Nothing is asserted about all other rows, discovery of a split, or higher digits when the first digit agrees.

The exact raw resultant of \(1+X^{13}-X-X^{67}\) and \(\Phi_{343}(X)\) is \(363899834996301124452459405391759665346211411650784701\), equal to \(7\cdot1373\cdot18523\cdot341629\cdot R\). It was independently verified by 26 modular resultants whose combined modulus exceeds \(2\cdot4^{294}\), the symmetric bound from the 294 primitive roots of unity. The extra factors are below the frozen chart's cutoff. Replaying the symbol calculations alone requires only a \(6\times6\) integer determinant and two small residue exponentiations per vector, as below.


```python
from itertools import permutations
from math import isqrt, prod

D=605519181779
q=9881419104602277971980597987
R=D*q
x=55710389148389160288578247553687525224
assert all(D%p for p in range(2,isqrt(D)+1))
assert pow(x,343,R)==1
assert (1+pow(x,13,R)-x-pow(x,67,R))%R==0

def mul(a,b):
    z=[0]*11
    for i,e in enumerate(a):
        for j,f in enumerate(b):
            z[i+j]+=e*f
    for i in range(10,5,-1):
        for j in range(6): z[i-6+j]-=z[i]
    return tuple(z[:6])
def power(a,h,m):
    z=(1,0,0,0,0,0)
    while h:
        if h%2: z=tuple(t%m for t in mul(z,a))
        a=tuple(t%m for t in mul(a,a))
        h//=2
    return z
def det(A):
    return sum((-1)**sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))*
               prod(A[i][p[i]] for i in range(6)) for p in permutations(range(6)))
basis=[tuple(int(i==j) for j in range(6)) for i in range(6)]
for m,a,l in [
 (q,(-27344,-10116,-16331,20627,-27169,-31210),(3,1)),
 (D,(-14,39,-64,-52,-30,3),(2,5)),
 (R,(-3216637,-1666475,-2530315,-1141391,-3667751,780723),(5,6)),
]:
    y=pow(x,49,m)
    assert sum(pow(y,j,m) for j in range(7))%m==0
    assert sum(t*pow(y,j,m) for j,t in enumerate(a))%m==0
    assert sum(a)%7 and sum(j*t for j,t in enumerate(a))%7==0
    assert det([mul(a,b) for b in basis])==m
    assert all(power(a,h,b)==power(basis[1],v,b)
               for (b,h),v in zip(((3,104),(5,2232)),l))
    if m!=R:
        assert all(pow(b,(m-1)//7,m)==pow(y,v,m) for b,v in zip((3,5),l))
        assert tuple((m-1)//343*e%7 for e in (25,25*171))!=l
assert 7*1373*18523*341629*R==363899834996301124452459405391759665346211411650784701
```
