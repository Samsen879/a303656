# An exact arithmetic parametrization of a noncollinear third witness

Extend the [primitive edge interface](PRIMITIVE_EDGE_THIRD_WITNESS.md). At the same actual integer \(n\), write the base point as \(z=(a,b)\), the second as \(z_1=z+(-h,k)\) with \(\gcd(h,k)=1\), and the third after pulling back its sector as \(z_2=z+(-j,\ell)/q\), where \(q=1\) or \(5\). Put \(\delta=N(z_1)-N(z)\), \(\gamma=N(z_2)-N(z)\); these are actual shift differences \(s_0-s_1,s_0-s_2\). Write \(P=h^2+k^2,\ Q=j^2+\ell^2,\ D=kj-h\ell\). For the noncollinear branch \(D\ne0\), expanding the two exact norm equations and solving the two-by-two linear system gives
\[
 (a,b)=\frac1{2qD}
 \bigl(q\ell(\delta-P)-k(q^2\gamma-Q),\
       qj(\delta-P)-h(q^2\gamma-Q)\bigr).
\]
This permits enumeration in \((D,\ell)\): first require \(j=(D+h\ell)/k\) integral (for \(k\ne0\)), then both displayed coordinates integral. Finally check actual sectors, shifts, positivity and squarefreeness where those are required. None may be inferred from the divisibility condition alone.

Eliminating \(j\) from the first coordinate gives the cheaper necessary condition
\[
 (2qak-2h\ell-D)D
 =F(\ell),\qquad
 F(\ell)=P\ell(\ell-qk)+qk\delta\ell-q^2k^2\gamma.
\]
The discriminant divided by \(q^2k^2\) is
\[
 (P+2\gamma-\delta)^2+4\gamma(\delta-\gamma).
\]
If \(\gamma=0\) or \(\gamma=\delta\), \(F\) splits into linear factors (over the rationals). For three distinct shifts with \(|\delta|,|\gamma|\le R\) and \(R^2=o(P)\), the second term is nonzero of size \(o(P)\), strictly between the relevant neighboring square differences for large \(P\). Thus the discriminant is nonsquare in the nondegenerate small-gap branch. This elementary separation does not by itself give an average bound on the number of divisors that pass both coordinate divisibilities.

## Exact divisor false candidate on actual offsets

At \(n=366278248984909119\) use offsets \((59074,59054,59174)=(3^{10}+25,3^{10}+5,3^{10}+125)\). The points are \((605209237,168626), (605209224,210167), (605209189,294168)\); the middle one rotates integrally by \((4+3i)/5\). Keeping the same direction and shift triple, the candidate \((j,\ell)=(27,83082)\) satisfies \(D\mid F(\ell)\), but reconstruction forces \(a\) to be a half-integer. Thus divisibility is not equivalent to real integer reconstruction even on genuine \(3,5\) data.

```python
from math import gcd
a,b,h,k=605209237,168626,13,41541
n=366278248984909119
s,t,u=59074,59054,59174
assert (s,t,u)==(3**10+25,3**10+5,3**10+125)
assert gcd(h,k)==1 and n==a*a+b*b+s
assert n==(a-h)**2+(b+k)**2+t
assert n==(a-48)**2+(b+125542)**2+u
assert (4*(a-h)-3*(b+k))%5==(3*(a-h)+4*(b+k))%5==0
de,ga=s-t,s-u
P=h*h+k*k
for j,l,valid in ((48,125542,True),(27,83082,False)):
    D=k*j-h*l; Q=j*j+l*l
    F=P*l*(l-k)+k*de*l-k*k*ga
    aa=l*(de-P)-k*(ga-Q)
    bb=j*(de-P)-h*(ga-Q)
    assert D and F%D==0
    if valid:
        assert aa==2*D*a and bb==2*D*b and F==(2*a*k-2*h*l-D)*D
    else:
        assert aa%(2*D)==D
```
