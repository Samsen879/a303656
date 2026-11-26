# A divisor bound coupling directions in an ordinary middle-area slice

Use the same displacement notation as [dual-axis reconstruction](SYMMETRIC_RECONSTRUCTION_PRIME_POWER.md). A marked triple consists of a base point \((a,b)\), then \((a-h,b+k)\) and \((a-j/q,b+\ell/q)\), with \(q\in\{1,5\}\) and \(D=kj-h\ell\). Their norms plus the respective shifts \(s_0,s_1,s_2\) must equal the same integer. Write \(\delta=s_0-s_1,\gamma=s_0-s_2\), and
\[
 S=4j-qh,\quad v=4\ell-qk,\quad M=hj(j-qh)+q\delta j-q^2\gamma h.
\]

In the fixed positive corridor \(35/160\le j/(qh)\le37/160\) and \(39/160\le\ell/(qk)\le41/160\), the determinant is nonzero, of size comparable to \(hk\). The norm-difference linear equations give \(2qDb=M-qjk^2+h\ell^2\), and identically
\(Sk=4D+hv,\ S\ell=qD+jv\). Multiplying the first equation by \(S^2\) and reducing mod \(D\) yields
\[
 D\mid N_*:=S^2M+hv^2j(j-qh).
\]
For fixed \(h,j,v\) and shifts the right side is independent of \(k\). Each of its signed divisors determines at most one \(k=(4D+hv)/S\), then \(\ell\), and then the unique rational coordinates. Full integrality remains a separate check.

For example, take shifts from the ordinary power box \(X^{1/4}\le3^c\le X^{1/3},\,5^e\le X^{1/8}\), with \(h\asymp\sqrt X\,w^2,\ k\asymp\sqrt X\,w,\ w=C/(\log X)^2\) for fixed \(C>0\). Require \(0<|40j-9qh|\le J,\ 0<|v|\le V\), with \(1\le J,V\le\sqrt X\). In this corridor \(j(j-qh)\) is negative of order \(h^2\), and \(M\) is negative for sufficiently large \(X\) since \(X^{1/3}=o(h^2)\). Thus \(N_*\ne0\); the same bounds give \(|N_*|=O_C(X^{5/2})\). There are \(O_C(\sqrt X JV(\log X)^6)\) choices of \(h,j,v\) and the shift triple. The divisor bound then gives \(O_{C,\varepsilon}(X^{1/2+\varepsilon}JV)\) actual marked triples, a power saving when \(JV\le X^{1/2-\eta}\) for fixed \(\eta>0\), choosing \(\varepsilon<\eta\). This is a thin slice and not a bound on the full third moment.

## Positive and half-integral controls

```python
from fractions import Fraction as Q
s0,s1,s2=3**10+1,3**10+5,3**10+25
de,ga=s0-s1,s0-s2
def calc(h,k,j,l):
    D=k*j-h*l
    P,T=h*h+k*k,j*j+l*l
    S,v=4*j-h,4*l-k
    M=h*j*(j-h)+de*j-ga*h
    N=S*S*M+h*v*v*j*(j-h)
    a,b=Q(l*(de-P)-k*(ga-T),2*D),Q(j*(de-P)-h*(ga-T),2*D)
    assert S*k==4*D+h*v and S*l==D+j*v
    assert N%D==0
    return D,N,a,b
D,N,a,b=calc(13,46819,3,11927)
assert D==-14594 and N//D==21120
n=445604744718323439
assert a*a+b*b+s0==(a-13)**2+(b+46819)**2+s1==n
assert (a-3)**2+(b+11927)**2+s2==n
D,N,a,b=calc(13,42123,3,10533)
assert (D,N,a,b)==(-10560,-31680,Q(1327263341,2),Q(367497,2))
```
