# Normalized Gaussian divisor strata and the remaining true-pair moment gap

Adding the inert common divisors restores positive support to a family of formerly zero-weight true pairs at order \(BK/\log B\). In fact, the normalized sieve can include **every \(g\mid H\) coprime to \(7\)** up to its cutoff. The resulting weighted inequality across the 147 compatible phases is
\[
\boxed{W_0\ge \frac{13}{10}W_-}
\]
for all sufficiently large balanced \((a,b)\). The sign for distinct true pairs remains open.

### Summing the common-divisor strata

Keep \(A=3^a\), \(B=5^b\), even \(a,b\), \(39/40<B/A<122/125\), and \(S_0=A+25B\). Use \(n=S_0+45u\) in the original ordinary window. For a compatible label \(S_i=3^x+5^y\), set \(k_i=(S_0-S_i)/45\) and \(H_i=k_i/4\).

In the shared boxes, count ordered vectors \((w\pm gm,e\pm gd)\) with \(mw+de=H_i/g\), \((m,d)=1\), and \(7\nmid m\). Let \(X=\sqrt B\), \(D=X^{1/20}\), and \(z=D^{1/s}\) for a sufficiently large fixed \(s\). At every split \(p<z\), forbid the same one of the two Gaussian primes above \(p\) in both vectors. The audited distribution estimate applies to each \(g\le D\) coprime to \(7\), with main volume \(Y_1/g\). The total error per label is \(X^{7/4+o(1)}\). [Shared upper and lower sieve weights, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

Adding just \(3^j g_{\rm split}\) multiplies the label main term by \(\sum_{j\le v_3(H_i)}3^{-j}\). The full divisor sum has a stronger cancellation. At a sifted split prime with \(t=v_p(H_i)\ge1\), its sum over depths in \(g\) is exactly
\[
\frac{p-2}{p+1}
+\frac{p-1}{p+1}\sum_{j=1}^{t-1}p^{-j}
+\frac{p}{p+1}p^{-t}
=\frac{p-1}{p+1}.
\]
That is also the factor at \(t=0\). The remaining label factor is
\[
F_z(H_i)=
\sum_{\substack{d\mid H_i\\
p\mid d\ \Rightarrow\ p\ne7,\ p\text{ outside the sifted set}}}\frac1d.
\]
Give each retained representation pair weight \(1/F_z(H_i)\). This normalization preserves its support. The omitted divisor mass above \(D\) is at most \(\tau(H_i)/D=o(1/\log B)\) uniformly.

The normalized main terms now use only the common box factor and the modulo-\(49\) counts. In units of \(K/441\), the \(r_0=0\) main term is at least \(49\cdot156=7644\). For \(r_-=3^{a+4}+5^{b+2}+7\bmod49\), it is \(49(50+60)+7\cdot42=5684\). The 42 blocked cells contribute zero. The main-term ratio is at least \(39/29\), and \((99/101)(39/29)>13/10\) leaves room for the shared sieve errors.

### Restored support and a remaining hole

In each compatible phase, \(y\equiv b+2\bmod54\) retains \(1/9+o(1)\) of its labels and forces \(9\mid k_i\). Apply the original true-pair lower bound in the boxes scaled by \(1/3\), with divisor cutoff \(D/3\) and the same prime cutoff \(z\) (the fixed cutoff factor does not affect the sieve bounds), to \(v,v+k_i/9\). Multiplying both vectors by \(3\) gives \(u=9v\) and common divisor \(g=3g_{\rm split}\). The split-prime orientations survive multiplication by \(3\). This restores \(\gg B/\log B\) **distinct supported pairs per refined label** in every admissible class. The statement concerns positive support. The normalized weight of each pair still depends on its representation multiplicity and on \(F_z(H_i)\).

The shared boxes still restrict height. For example, choose them so their target images lie in the central third of the ordinary interval. The replay below gives a true \(r_-\) pair in the upper third whose common divisor \(g=3\) is now eligible. Its box weight is zero. The true-pair lower bound in that upper third gives \(\gg B/\log B\) pairs per admissible label there, so this remaining omission is already of natural order for those boxes.

### A sufficient moment comparison

There is a full-support proxy independent of the boxes. Count **all** ordered Gaussian representation pairs satisfying the split-prime orientation tests, and divide by \(16\). Unique factorization gives the pointwise weight
\[
P_z(u,k)=\beta(u)\beta(u+k)
\prod_{\substack{p\ge z\\p\equiv1\ (4)}}
(v_p(u)+1)(v_p(u+k)+1).
\]
It is zero off true pairs and lies in \([1,C_s]\) on true pairs. Thus its support is exact, while its multiplicity remains variable.

Let \(w_r\) be the normalized box weight per target–label pair, \(M_{2,0}=\sum w_0^2\), and \(\Pi_-=\sum P_z\) in class \(r_-\). For the distinct counts,
\[
T_0-T_-\ \ge\ \frac{W_0^2}{M_{2,0}}-\Pi_-.
\]
Consequently a sufficient condition for a positive true gap of order \(BK/\log B\) is
\[
\limsup_{B\to\infty}
\frac{M_{2,0}}{W_0}\frac{\Pi_-}{W_-}<\frac{13}{10}.
\]
Both factors are weighted moments. The first-moment sieve comparison leaves their product uncontrolled.

### Exact replay

This constructs a genuine anchor and a genuine alternative in \(r_-\), with an eligible \(g=3\) and target height outside the central-third boxes. At the same target, \(T\) has exact \(7\)-depth one. The split prime \(17\) also certifies proxy multiplicity at least two for \(z=13\).

```python
from math import gcd, isqrt

a,b = 7864,5368
A,B = 3**a,5**b
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
S,T = 3**1144+5**1212,3**1064+5**1086
k,rem = divmod(S0-S,405)
assert rem == k%8 == 0 and (1212-b-2)%54 == 0

mid = ((lo-S0)//405+(hi-S0)//405)//2
m = (isqrt(mid+k)-isqrt(mid))//2+4
w,e = divmod(k//4,m)
w,e = w+4,e-4*m
v0,v1 = (3*(w-m),3*(e-1)), (3*(w+m),3*(e+1))
u,v = (sum(t*t for t in pair) for pair in (v0,v1))
n = S0+45*u
assert lo < n <= hi and n%49 == r == 45
assert n-S == 45*v and (n-T)%49 == 7
assert gcd((v1[0]-v0[0])//2,(v1[1]-v0[1])//2) == 3
assert m%7 and 3*(n-lo)>2*(hi-lo) and (u*v)%17 == 0

for label,(x,y) in [(S0,v0),(S,v1)]:
    x,y = sorted((3*abs(x),3*abs(y)),reverse=True)
    assert n == label+(2*x+y)**2+(x-2*y)**2
    assert S3 < label+(2*x+y)**2 <= hi
```

Independent BigInt verified the local divisor-depth cancellation, the exact ratio margin, and the genuine out-of-box target with eligible common divisor 3 and variable full-support weight. The moment condition is sufficient but is not established here.
