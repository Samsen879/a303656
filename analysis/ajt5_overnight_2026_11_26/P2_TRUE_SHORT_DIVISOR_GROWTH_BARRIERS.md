# Moving prime support and growth barriers for the independent P2 edge

No fixed set of primes can supply a true short divisor of \(e\) at ordinary height. The stronger obstruction is that **both complementary divisors must obtain essentially all their logarithmic size from outside any fixed prime set**. I also found two restrictions on how those divisors can be constructed: a sharp coefficient threshold for homogeneous forms and a fixed-support obstruction for the coordinates of the exact quadratic norm factorization.

### The short interval and its prime support

Keep \(N=623894271,\ a=Nh+1,\ b=Nk-2,\ A=3^a,\ B=5^b\), and \(39/40<B/A<122/125\). Write \(W=\sqrt A\) and \(e=20A+25B=60\cdot3^{Nh}+5^{Nk}\). The independent edge joins the shifts \(A+25B\) and \(81A+125B\). For a true short divisor \(z\mid e\), set \(L=z+e/z\). The ordinary window gives, with \(t=B/A\),
\[
728-24t<(L/W)^2\le728+600t.
\]
On the short branch \(z\le\sqrt e\), the function \(z+e/z\) decreases. Substitution at the two endpoints gives
\[
\boxed{\quad \tfrac54 W<z<\tfrac95 W.\quad}
\]

For each fixed prime \(p\ge7\), apply Yu’s \(p\)-adic logarithm bound to \(-60\cdot3^{Nh}5^{-Nk}-1\). The bases are fixed \(p\)-adic units, the expression is nonzero, and its valuation is \(v_p(e)\). This gives \(v_p(e)=O_p(\log(h+k))\). At \(2,3,5\) the valuations on the pinned progression are \(0,0,1\). Thus the part of \(e\) supported on any fixed finite set \(S\) is at most a power of \(\log A\). If a short divisor exists, then
\[
\log z_{\overline S}=\tfrac12\log A+O_S(\log\log A),\qquad
\log (e/z)_{\overline S}=\tfrac12\log A+O_S(\log\log A).
\]
Here \(u_{\overline S}\) removes all prime powers supported on \(S\). This leaves open how the moving primes can be partitioned. [Yu, *P-adic logarithmic forms and group varieties III*](https://www.degruyterbrill.com/document/doi/10.1515/FORUM.2007.009/html)

### Two restrictions on constructive factors

**Homogeneous forms.** For any \(r\mid\gcd(h,k)\), set \(M=Nr,\ X=3^{h/r},\ Y=5^{k/r}\), so \(e=60X^M+Y^M\). Suppose a short \(z\mid e\) is supplied by \(z\mid F(X,Y)\), where \(F\) is a nonzero integral homogeneous form of degree \(d<M\). Then
\[
\|F\|_\infty>\frac{\sqrt X}{60\sqrt M}.
\]
Indeed, \(X\) is invertible modulo \(z\), so \(z\) divides the resultant of \(T^M+60\) and \(F(1,T)\). The resultant is nonzero by Eisenstein at 3. Averaging \(|F(1,T)|^2\) over the \(M\) roots and applying AM–GM bounds its absolute value by \(60^d(\sqrt M\|F\|_\infty)^M\). Conversely, a collision of coefficient vectors modulo \(z\) gives a nonzero form of degree \(M-1\) and coefficient height at most \(\lfloor z^{1/M}\rfloor=O(\sqrt X)\). The exponent \(1/2\) is therefore sharp up to the \(\sqrt M\) loss. Since \(M\log(Y/X)=\log(75t)\), Matveev’s bound for the nonzero form \((k/r)\log5-(h/r)\log3\) gives \(M\ll(\log X)^C\). This excludes coefficients polynomially bounded in \(M\), even when the refinement changes with height. [Matveev, *An explicit lower bound for a homogeneous rational linear form in logarithms II*](https://www.mathnet.ru/eng/im314)

**Exact norm coordinates.** Put \(U=2\sqrt A,\ V=\sqrt B,\ Q=e/5=U^2+5V^2\), and \(w=\sqrt{-5}\). Every \(z=5^\epsilon D\mid e\) yields an integer factorization
\[
(r+sw)(R+Tw)=m(U+Vw),\qquad
r^2+5s^2=mD,\quad R^2+5T^2=mQ/D,\qquad m\in\{1,2\}.
\]
To see this, take a shortest nonzero vector in the lattice \(rV-sU\equiv0\bmod D\), with norm \(r^2+5s^2\). That norm is a multiple of \(D\). The weighted covolume is \(\sqrt5D\), so planar lattice reduction bounds the shortest norm by \(2\sqrt{5/3}\,D<3D\). The second factor is \((U+Vw)(r-sw)/D\), which has integer coordinates by the same congruence. Both factors are primitive. For a short \(z\) at sufficiently large height, both norms grow, so all four coordinates are nonzero.

For any fixed \(S\), **at least two of those coordinates must have a prime factor outside \(S\)** at sufficiently large height. If three coordinates are \(S\)-units, swap factors so that \(r,s\) are two of them. Eliminating the unknown fourth coordinate gives one of
\[
Rr^2+5Rs^2-mUr-5mVs=0,\qquad
Tr^2+5Ts^2-mVr+mUs=0.
\]
The first two terms have the same sign. Of the two possible pairwise cancellations, the direct pairing forces the omitted coordinate to be zero. The crossed pairing gives \(Ur^3=25Vs^3\) or \(Vr^3=-5Us^3\), each impossible by \(v_2\) modulo 3. Thus the four-term \(S\)-unit equation is nondegenerate, after adjoining \(2,3,5\) to \(S\). Its finitely many projective solutions give finitely many ratios \(r/s\) and \(U/V\), hence finitely many exponent pairs. This restriction applies even if the norms of the proposed \(S\)-unit coordinates themselves have moving prime factors. [Evertse, *On sums of \(S\)-units and linear recurrences*, Theorem 1](https://www.numdam.org/item/CM_1984__53_2_225_0/)

### Genuine arithmetic control

The old prime \(q=126736826507\) supplies **true growing divisors \(q^j\)**. For the phase below, \(3^{NT}\equiv1+81014673431q\bmod q^2\). Each additional base-\(q\) digit of the \(h\)-shift therefore has exactly one choice that lifts the zero and \(q-1\) choices that stop at the current exact depth. For every \(j\ge1\) this gives a phase modulo \(Tq^j\) with \(v_q(e)=j\), cofinal in the balanced strip. These are powers of one fixed prime, and they stay below the short-divisor scale by the fixed-support bound.

```python
from fractions import Fraction as F
from math import isqrt, lcm

N, P = 623894271, 23894400218362914240
p, q = 562190443, 126736826507
h0, k0 = 645806464976090519188845783659560241603756891, 19848674835359031706
T = lcm(P, p*(p-1), q-1)
assert all(q % i for i in range(2, isqrt(q)+1))
assert (h0 % P, k0 % P) == (6540501655095556571, 19848674835359031706)
assert pow(3, N*T, q*q) == 1 + 81014673431*q

a = 19880680576670272546883607970869685064352468642948577935537419802909072611505110310983019155741302427330629212424738141334621937399818478456321738909062895142901568960847800070822
b = 13570675712232338353700049524444292324285783989700651261742655268818691802762808549773788410750853005175916495719290207697843094856108105835357455645515612726803043857129899002084
assert (a, b) == (N*((a-1)//N)+1, N*((b+2)//N)-2)
assert (((a-1)//N-h0) % T, ((b+2)//N-k0) % T) == (0, 0)
assert (60*pow(3,a-1,q**4)+pow(5,b+2,q**4)) % q**4 == 40579912650*q**3

def log_bounds(x):
    u = (F(x)-1)/(F(x)+1)
    s = 2*sum(u**(2*j+1)/ (2*j+1) for j in range(570))
    err = 2*abs(u)**1141/(1141*(1-u*u))
    return s-err, s+err

l3, u3 = log_bounds(3)
l5, u5 = log_bounds(5)
assert log_bounds(F(39,40))[1] < b*l5-a*u3 < b*u5-a*l3 < log_bounds(F(122,125))[0]
for t in (F(39,40),F(122,125)):
    E=20+25*t
    assert (F(5,4)+E/F(5,4))**2>728+600*t
    assert (F(9,5)+E/F(9,5))**2<728-24*t
aa,bb=3**6,5**4
zz,vv=35,863
assert zz*vv==20*aa+25*bb
assert aa+25*bb+(zz+vv)**2==81*aa+125*bb+(vv-zz)**2==822758
print("OK")
```

The replay also verifies the endpoint inequalities and an actual small two-label identity outside the pinned balance strip.

For the original conjecture, the transferable tool is the exact shared-coordinate identity
\[
K=A+25B+(z+e/z)^2=81A+125B+(e/z-z)^2.
\]
A true factor pair gives two representations of every \(K+t^2\) with the same free coordinate \(t\). The all-exponent problem asks for a representation of each prescribed integer. The results here restrict one way to construct simultaneous witnesses and leave the existence of unrestricted ordinary short divisors unresolved.

The normalized endpoint differences used for the short-divisor interval are increasing in the stated range, so their signs are controlled by the appropriate endpoints. For the weighted norm lattice, \(U\) is invertible modulo \(D\); substituting the lattice congruence shows that both the first norm and the real coordinate of the second factor's numerator are divisible by \(D\). Primitivity also follows from the product identity: a common divisor of the coordinates of either factor divides the two product coordinates and hence divides \(m\). If \(m=2\) both factor norms have 2-adic valuation 1, so neither can have both coordinates even. The fixed-support statements concern restricted constructions, not existence of short divisors with moving support.