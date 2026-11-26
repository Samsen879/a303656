# Dual-axis reconstruction and a true-shift prime-power obstruction

Consider the three points \((a,b)\), \((a-h,b+k)\), and \((a-j/q,b+\ell/q)\). Their squared norms are to differ from the first by \(\delta=s_0-s_1\) and \(\gamma=s_0-s_2\), respectively. Use positive \(q\), nonzero \(h,k\), and \(D=kj-h\ell\ne0\). Set \(P=h^2+k^2\) and
\[
 F(r,w)=Pw(w-qr)+qr\delta w-q^2r^2\gamma.
\]
The formulas below determine the base coordinates over the rationals; if \(q>1\), the third point also needs integral offsets \(j/q,\ell/q\) to be an integer point.

Put \(g=\gcd(k,\ell)\), \((K,\lambda,d)=(k/g,\ell/g,D/g)\) and \(f=\gcd(h,j)\), \((U,V,e)=(h/f,j/f,D/f)\). The two reconstruction directions are
\[
 \begin{aligned}
 2qKa&=F(K,\lambda)/d+2h\lambda+d, &2kb&=2ha+\delta-P,\\
 2qUb&=F(U,V)/e-2kV+e, &2ha&=2kb+P-\delta.
 \end{aligned}
\]
In fact the norm difference linear system gives
\(2qDa=q\ell(\delta-P)-k(q^2\gamma-j^2-\ell^2)\) and
\(2qDb=qj(\delta-P)-h(q^2\gamma-j^2-\ell^2)\).
Multiply these numerators by \(k,h\) respectively and use \(kj-h\ell=D\); the resulting quadratic forms are \(F(k,\ell)=g^2F(K,\lambda)\) and \(F(h,j)=f^2F(U,V)\). This recovers the horizontal identity in [the earlier exact divisor gate](SECOND_COORDINATE_EXACT_DIVISOR_GATE.md) and gives its vertical analogue. In addition to the form divisibilities, the reconstructed coordinates still have to pass the remaining integer tests.

## Failure of a one-digit test on actual powers

Take \(q=1\), actual shifts \(59050,59054,531442\), and directions \((13,45549,59,157815)\). Then \(g=189\), \(K=241\), \(\lambda=835\), and \(d=3364=4\cdot29^2\). The primitive first-edge reduced congruence
\[
 g\mid hj(j-h)+\delta j-\gamma h
\]
holds, and \(4\cdot29\) divides both \(F(K,\lambda)\) and \(F(h,j)\). Nevertheless their residues modulo \(29^2\) are 87 and 493. Neither base coordinate is integral; both have reduced denominator exactly 29. This rules out sufficiency of retaining only the first 29-adic digit in these tests, even on these actual power shifts. It makes no claim about the frequency of such obstructions or any summed moment bound.

As a positive control, the different actual shifts \(59050,59054,59074\) at \(n=378458683301107119\) have base point \((615189937,157210)\), direction \((13,44557,39,112419)\), and \(D=276276\). Here the horizontal reduced coordinate is \(U=1\), but the vertical reduced coordinate is \(K=44557\).

```python
from fractions import Fraction as Q
from math import gcd

def test(h,k,j,l,shifts):
    s,t,u=shifts
    a0,b0=s-t,s-u
    P,D=h*h+k*k,k*j-h*l
    F=lambda r,w:P*w*(w-r)+r*a0*w-r*r*b0
    N=l*(a0-P)-k*(b0-j*j-l*l)
    M=j*(a0-P)-h*(b0-j*j-l*l)
    a,b=Q(N,2*D),Q(M,2*D)
    g,f=gcd(k,l),gcd(h,j)
    K,A,d=k//g,l//g,D//g
    U,V,e=h//f,j//f,D//f
    assert 2*K*a==Q(F(K,A),d)+2*h*A+d
    assert 2*U*b==Q(F(U,V),e)-2*k*V+e
    assert (a-h)**2+(b+k)**2-a*a-b*b==a0
    assert (a-j)**2+(b+l)**2-a*a-b*b==b0
    return a,b,D,d,F(K,A),F(h,j),K,U

s,t,u=3**10+1,3**10+5,3**12+1
h,k,j,l=13,45549,59,157815
g=gcd(k,l)
assert gcd(h,k)==1 and g==189
assert (h*j*(j-h)+(s-t)*j-(s-u)*h)%g==0
a,b,D,d,F1,F2,K,U=test(h,k,j,l,(s,t,u))
assert d==4*29**2 and K==241
assert F1%(4*29)==F2%(4*29)==0
assert (F1%29**2,F2%29**2)==(87,493)
assert a.denominator==b.denominator==29
s,t,u=3**10+1,3**10+5,3**10+25
a,b,D,_,_,_,K,U=test(13,44557,39,112419,(s,t,u))
assert (a,b,D,K,U)==(615189937,157210,276276,44557,1)
assert a*a+b*b+s==378458683301107119
```
