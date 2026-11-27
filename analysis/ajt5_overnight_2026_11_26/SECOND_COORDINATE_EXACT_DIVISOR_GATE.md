# The second coordinate gives an exact divisor test beyond the reduced cubic

Use the [noncollinear reconstruction](NONCOLLINEAR_TRIPLE_INTEGER_INTERFACE.md): points \(z=(a,b)\), \(z+(-h,k)\), and \(z+(-j,\ell)/q\), with \(q=1\) or \(5\). Set \(P=h^2+k^2,\ D=kj-h\ell\ne0\), and let \(\delta,\gamma\) be the actual two norm gaps. Besides the first-coordinate identity involving \(F(\ell)\), there is the exact second-coordinate identity
\[
 (2qbh+2kj-D)D = J(j),\qquad
 J(j)=Pj(j-qh)+q\delta hj-q^2\gamma h^2.
\]
Indeed multiply the numerator \(qj(\delta-P)-h(q^2\gamma-j^2-\ell^2)\) of \(2qDb\) by \(h\), then substitute \(h\ell=kj-D\). Thus integer coordinates require \(D\mid J(j)\) (in particular \(D/g\mid J(j)\) for \(g=\gcd(k,\ell)\mid D\)). Modulo \(g\), the older equation is \(g\mid hj(j-qh)+q\delta j-q^2\gamma h\), since \(h\) is a unit there for a primitive edge. This weaker test does not imply the full integer coordinate conditions.

## Exact countercontrol at \(D/g=41^2\)

At \(n=378887772889668927\), shifts \(59050,531442,531466\) give squared-norm witnesses at \((615538586,148441),(615538573,195034),(615538519,323290)\). For \(q=1\), the data have \(h=13,k=46593,j=67,g=501\), \(\ell/g=349\) and \(D=848694\). Change only \(\ell/g\) to 350, keeping the direction and the same two gaps. The reduced cubic still passes, but now \(D/g=1681=41^2\) and \(J(j)=35\bmod41\). Both reconstructed coordinates are nonintegral. The three original coordinates are verified below; this note does not assert a large-area summed bound.

```python
from math import gcd
n,a,b=378887772889668927,615538586,148441
s,t,u=59050,531442,531466
assert (s,t,u)==(3**10+1,3**12+1,3**12+25)
h,k,j=13,46593,67
de,ga=s-t,s-u
P=h*h+k*k
J=P*j*(j-h)+de*h*j-ga*h*h
assert gcd(h,k)==1 and n==a*a+b*b+s
assert n==(a-h)**2+(b+k)**2+t
assert n==(a-j)**2+(b+501*349)**2+u
for lam,actual in ((349,True),(350,False)):
    l=501*lam; D=k*j-h*l; Q=j*j+l*l
    g=gcd(k,l)
    aa=l*(de-P)-k*(ga-Q); bb=j*(de-P)-h*(ga-Q)
    assert g==501 and (h*j*(j-h)+de*j-ga*h)%g==0
    if actual:
        assert D==848694 and (aa,bb)==(2*D*a,2*D*b)
        assert J==(2*b*h+2*k*j-D)*D
    else:
        assert D//g==41**2 and J%41==35
        assert aa%(2*D) and bb%(2*D)
```
