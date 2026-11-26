# Why the thin-box estimate cannot simply be summed over rational centers

Generalize the divisor identity in [CROSS_DIRECTION_DIVISOR_SLICE.md](CROSS_DIRECTION_DIVISOR_SLICE.md). For a reduced vertical center \(s/r\), put \(S=rj-sqh,\ v=r\ell-sqk\). Then \(Sk=rD+hv,\ S\ell=sqD+jv\), and the same calculation gives the \(k\)-independent numerator
\[
 N_{r,s}=S^2M+hv^2j(j-qh),\qquad
 N_{r,s}\equiv S^2(2qDb)\pmod D.
\]
If \(S\ne0\), every signed divisor \(D\) determines at most one \(k\) at fixed \(h,j,r,s,v\) and shifts. In the previous middle corridor the terms have the same sign for sufficiently large \(X\), as \(hj(j-qh)\) dominates the \(O(X^{1/3}h)\) part of \(M\).

Now suppose one covers a fixed positive area in the two ratio variables \(\alpha=j/(qh),\,\beta=\ell/(qk)\) solely by rectangles at centers \(a/p,s/r\) with bounds \(|pj-aqh|\le J,\ |r\ell-sqk|\le V\). Here \(h\asymp H,\ k\asymp B\). Each rectangle has area \(O(JV/(prHB))\), hence \(\sum JV/(pr)\gg HB\). The box estimate's horizontal allowance can account for the residue \(aqh\equiv-u\bmod p\) at each \(u=pj-aqh\): since \((a,p)=1\) and \(q\) is bounded, its per-box enumeration envelope is \(O((1+H/p)(1+J))\). In the vertical direction it enumerates \(O(1+V)\) possible biases. Even replacing each divisor allowance by 1, the corresponding sum of budget terms
\[
 \sum_{\rm boxes}(1+H/p)(1+J)(1+V)
 \ \ge H\sum_{\rm boxes}JV/(pr)\ \gg H^2B
\]
cannot supply a useful \(O(X)\) upper bound when \(H=\sqrt X\,w^2,\ B=\sqrt X\,w,\ w=C/(\log X)^2\). This is an obstruction to that envelope-based proof, not a lower bound for the actual integer witnesses or for more selective enumeration after the exact coordinate constraints.

Nor are two rational centers automatically independent. For centers \((r_i,s_i)\),
\[
 S_1v_2-S_2v_1=-qD(r_1s_2-r_2s_1).
\]
If both \(S_i\) are units modulo \(D\), their divisor tests are equivalent by the congruence above, including the full prime powers of \(D\).

```python
from math import gcd
h,k,j,l=13,46819,3,11927
a,b,n=667536305,161942,445604744718323439
s0,s1,s2=59050,59054,59074
D=k*j-h*l
M=h*j*(j-h)+(s0-s1)*j-(s0-s2)*h
assert D==-14594 and M==-90
assert a*a+b*b+s0==(a-h)**2+(b+k)**2+s1==(a-j)**2+(b+l)**2+s2==n
rows=[]
for r,s in ((4,1),(15,4)):
    S,v=r*j-s*h,r*l-s*k
    N=S*S*M+h*v*v*j*(j-h)
    assert gcd(S,D)==1 and N%D==0
    assert (N-S*S*(2*D*b))%D==0
    rows.append((S,v,N//D))
assert rows==[(-1,889,21120),(-7,-8371,1872600)]
assert rows[0][0]*rows[1][1]-rows[1][0]*rows[0][1]==-D
```
