# P2 signed divisor interval and an excluded highest-block branch

### A two-sided divisor certificate

Write \(W=\sqrt A\), \(d=uv=24LT\), with \(T=D_r\) the highest block and \(L=D_0\cdots D_{r-1}\). For the ordinary window \(S_3<K\le K_{\max}=729A+625B\), the **exact** short-factor interval is
\[
V_-\le v<V_+,\qquad
V_-=V(K_{\max}),\quad V_+=V(S_3),\quad
V(K)=\frac{\sqrt{K-S_0}-\sqrt{K-S_1}}2.
\]
For definiteness, use the balanced strip \(0.9\le B/A\le1.1\). On it the interval lies inside \(4W<v<21W/2\) and \(u<33W\). This follows from \(v=(8A+600B)/(2(\sqrt{K-S_0}+\sqrt{K-S_1}))\) at the endpoints: the sum of roots at \(K_{\max}\) is below \(65W\), and at \(S_3\) it exceeds \(32W\); the numerator lies between \(548A\) and \(668A\). In the preceding formula \(S_i=9^iA+5^{P_i}B\) with \(P=(2,4,3,0)\).

Let \(m_{k,\epsilon}\) be a certified lower bound on the true low divisors \(kw\), where \(w\mid L\), \(k\in\{2,4,6,12\}\), \((w/11)=\epsilon\), and the residue \(kw\bmod1331\) passes the square conditions. This uses \(T\equiv1\bmod1331\) on **every divisor** of \(T\). A short side of type \((k,\epsilon)\) has a long side of type \((24/k,-\epsilon)\).

Now certify a highest-block divisor \(P\mid T\). In a branch assigning \(g\mid P\) to the short side and \(P/g\) to the long side, exact multiplication forces
\[
m_{k,\epsilon}g\ \le v\ \le\
\frac{d}{m_{24/k,-\epsilon}(P/g)}.
\]
If this interval misses \([V_-,V_+)\) in every branch, the whole ordinary window is empty. The endpoint comparisons use monotonicity of \((v+d/v)^2\) below \(\sqrt d\), so they can be replayed with rational arithmetic. A full prime power \(p^m\parallel T\) has only two placements if either \(-4e\) or \(-4f\) is a nonsquare modulo \(p\), since splitting that power would make both \(u\) and \(v\) divisible by \(p\).

### Cofinal control and the remaining size gap

On the \(r=3\) progression
\[
(s,t)=\bigl((a-1)/1331,(b+2)/1331\bigr)
\equiv(1273865740071,681186)\pmod{11128367376720},
\]
take \(v=4\cdot727\cdot15973\) and the exact quotient \(u=d/v\). The power \(727^1\) belongs to \(D_2\), and \(15973^1\) belongs to \(D_3\). The two remaining square tests give \((121,289)\bmod1331\), \((272,418)\bmod727\), and \((15738,6122)\bmod15973\), all with stable square lifts. Irrationality of \(\log3/\log5\) gives arbitrarily large balanced pairs in this progression.

Nevertheless, **every allocation whose entire short-side highest-block share is \(15973\) misses the ordinary window**, even with all lower factors available. Indeed,
\[
24L=6\bigl((A/3)^{1/11}+(25B)^{1/11}\bigr)<18A^{1/11}.
\]
For all sufficiently large pairs this gives \(v\le18\cdot15973\,A^{1/11}<4W\). A surviving allocation with \(15973\) on the short side must therefore supply an additional true highest-block divisor \(z\mid T/15973\) with
\[
z>\frac{2}{9\cdot15973}A^{9/22}.
\]
It must also hit the exact interval after multiplication by the selected low divisor. Passing the local square tests does not establish either that divisor or the remaining integer squares.

The replay uses the displayed exponent progressions to check exact divisibility and all three local square tests, including their invariance under the steps. Cofinality in the stated strip follows from irrational rotation of the integer exponent steps. Neither the unchecked size hypothesis in other allocations nor integer squarehood has been inferred.

```python
from math import isqrt
M=11128367376720
s,t=1273865740071,681186
a,b=1331*s+1,1331*t-2
assert (a%720,b%720)==(22,4) and 1331*M%720==0
p,q=727,15973
v=4*p*q
for mod,wanted in ((1331,(121,289)),(p,(272,418)),(q,(15738,6122))):
    m=v*mod
    assert all(pow(base,1331*M,m)==1 for base in (3,5))
    A,B=pow(3,a,m),pow(5,b,m)
    z=2*(A+75*B)%m
    assert z%v==0
    u=z//v
    G,J=((u+v)**2-4*(20*A+25*B))%mod,((u+v)**2-4*(182*A-6*B))%mod
    assert (G,J)==wanted
    if mod==1331:
        assert G%121==0 and G%1331!=0 and pow(G//121,5,11)==pow(J,5,11)==1
    else:
        assert pow(G,(mod-1)//2,mod)==pow(J,(mod-1)//2,mod)==1
for prime,j in ((p,2),(q,3)):
    assert all(prime%i for i in range(2,isqrt(prime)+1))
    m=prime**2
    assert all(pow(base,M*11**(j-1),m)==1 for base in (3,5))
    lo=(pow(3,s*11**(j-1),m)+pow(5,t*11**(j-1),m))%m
    hi=(pow(3,s*11**j,m)+pow(5,t*11**j,m))%m
    assert lo%prime and hi%prime==0 and hi
print("OK")
```
