# Three genuine child labels and a separate cross-base Pell orbit

Continue the [joint-label Pell construction](JOINT_LABEL_PELL_ORBIT.md) at \(m=p^2+2188\). For the child \(5m+2\), the offsets \(K=10942-5^e-3^f\) at \((e,f)=(0,0),(1,2),(2,2)\) are \(10940,10928,10908\). There are unconditionally infinitely many positive p for which all three residuals \(5p^2+K\) are genuine integer norms at the same m and \(v_{41}(p)=1\).

## Common projection and an actual anchor

For a direction \(v=(s,t)\), let \(A=s^2+t^2\). The projection \(H=v\cdot z\) and determinant \(w=\det(v,z)\) reconstruct the coordinates as \((sH-tw,tH+sw)/A\) and the norm as \((H^2+w^2)/A\). For the first two labels \(w_0^2-w_1^2=12A\). If \(w_1=w_0-dA\) for integer \(d\ne0\), then \(d(2w_0-dA)=12\). The determinant choice \(w_j=w_0-jA\) permits precisely the candidate offset \(10940-12j/d+Aj(j-d)\). This test must be supplemented by the Pell equation and integrality of the reconstructed coordinates. For example \(A=2,\ w=(5,1,3)\) passes the offset test but needs \(H^2-10p^2=21855\), impossible modulo 25.

Take \(v=(5,1)\), so \(A=26\), and use \(w=29,-23,3\) in the order of the three labels. The common equation and a genuine anchor are
\[
 H^2-130p^2=283599,\quad (H,p)=(266927,23411),\quad p=41\cdot571.
\]
This gives \((51331,10272),(51333,10262),(51332,10267)\). The unit \(\eta=6499+570\sqrt{130}\) has norm one and \(\eta^{3198}\) is the identity modulo \(\operatorname{lcm}(4,26,41^2)\) in both coefficients. Use its positive powers to obtain strictly increasing p, preserving all three integral coordinates and \(p\equiv3\bmod4,\ v_{41}(p)=1\).

On the further orbit with exponents \(36+3457038n\) from the anchor, \(q=p/41\equiv871\bmod47^2\). Thus removing 41 from p makes the second target fail at exact valuation one of 47, since \(5q^2+10928\equiv235\bmod47^2\), while the unstripped second label succeeds.

## Independent cross-base orbit

Let \(X^2-5p^2=8756\) with the positive seed \((X,p)=(1684231,753211)\), \(p=41\cdot18371\). At the same \(m=p^2+2188\), the shift \(5^0+3^7\) works at both children \(5m+4\) and \(3m+2\):
\[
 5m+4-1-3^7=X^2,\quad
 3m+2-1-3^7=((X-p)/2)^2+((X+p)/2)^2 .
\]
Multiplication by \((9+4\sqrt5)^{820}\) preserves the Pell equation and the odd parities and \(v_{41}(p)=1\). This is a different orbit from the triple. No infinitude of prime cofactors or universal representation is asserted.

### Offline replay

~~~python
from math import lcm
def power(a,b,e,D,M):
    def mul(u,v):
        x,y=u
        s,t=v
        return ((x*s+D*y*t)%M,(x*t+y*s)%M)
    r,u=(1,0),(a,b)
    while e:
        if e&1:
            r=mul(r,u)
        u=mul(u,u)
        e//=2
    return r
H,p=266927,23411
assert H*H-130*p*p==283599 and p==41*571
for w,(e,f) in zip((29,-23,3),((0,0),(1,2),(2,2))):
    a,b=5*H-w,H+5*w
    assert a%26==b%26==0
    assert (a//26)**2+(b//26)**2 == 5*(p*p+2188)+2-5**e-3**f
assert 6499**2-130*570**2==1
assert power(6499,570,3198,130,lcm(4,26,41**2))==(1,0)
M=lcm(4,26,41**2,41*47**2)
u,v=power(6499,570,36,130,M)
assert (H*v+p*u)%(41*47**2)==41*871
assert power(6499,570,3457038,130,M)==(1,0)
assert (5*871**2+10928)%47**2==235
assert all((h*h-10*v*v-21855)%25 for h in range(25) for v in range(25))
X,p=1684231,753211
assert X*X-5*p*p==8756 and p==41*18371 and X%2==p%2==1
assert power(9,4,820,5,lcm(4,41**2))==(1,0)
m=p*p+2188
assert X*X==5*m+4-1-3**7
assert ((X-p)//2)**2+((X+p)//2)**2==3*m+2-1-3**7
~~~
