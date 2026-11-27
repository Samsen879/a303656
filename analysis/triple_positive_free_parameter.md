# Triple-positive power-law population with a free parameter

**A different three-label scheme gives \(\Theta(\sqrt X\log X)\) distinct generated targets up to \(X\), with both exponent axes growing.** For the original offsets, I did not obtain a power-law bound. I proved that every integral triple has difference determinant \(2\bmod4\), ruled out affine-line deformations through integral triples, and isolated the cancellation needed in a direct two-frequency count.

## Original offsets: the exact rank-two obstruction

Set \(T=5^U,\ W=3^V,\ Q=625T^2\), with \(\lceil U/2\rceil\le V\le U\). The original shifts, in order, are
\[
s=(T^2+81W^2,\ 125T^2+3W^2,\ 625T^2+243W^2).
\]
Write \(h=s_2-s_1\) and \(k=s_3-s_1\). Then
\[
h=124T^2-78W^2,\qquad k=624T^2+162W^2,\qquad
(h,k)\equiv(14,2)\pmod{16}.
\]
Also \(\gcd(h,k)=2\). Eliminating \(T^2,W^2\) puts the gcd among the divisors of \(68760=2^3 3^2 5\cdot191\). The primes \(3,5\) do not divide \(h\), and \(191\mid h\) would require the square \(T^2/W^2\equiv53\bmod191\), whereas \(53^{95}\equiv-1\bmod191\).

For an integral triple \(N(z_i)=n-s_i\), where \(N(x,y)=x^2+y^2\), put \(u=z_2-z_1,\ v=z_3-z_1,\ D=\det(u,v)\). Each difference vector has two odd coordinates. Indeed, its coordinate sum is even by the norm differences modulo \(2\), and two even coordinates would give a norm difference divisible by \(4\). Therefore
\[
z_1\cdot u\equiv0\pmod4,\qquad z_1\cdot v\equiv2\pmod4,
\]
by expanding the two norms modulo \(8\). If \(4\mid D\), then \(v\) is an odd multiple of \(u\) modulo \(4\), contradicting those dot products. Thus **\(D\equiv2\bmod4\) for every integral triple and every choice of its square coordinates.**

There is a stronger free-parameter obstruction. Suppose \(z_i=A_i+tB_i\) gives a rational affine line through an integral triple and preserves both norm differences identically. Rescale the directions so the \(B_i\) are integral and at least one coordinate is odd. Comparing coefficients gives a common \(G=N(B_i)>0\) and common \(A_i\cdot B_i\). For \(X_i=\det(B_i,A_i)\) this forces
\[
X_1^2-X_2^2=Gh,\qquad X_1^2-X_3^2=Gk.
\]
If \(G\) is odd, the first equation is impossible modulo \(4\). Otherwise the primitive direction at \(2\) gives \(G\equiv2\bmod8\). The three squares must then be \(X_1^2,X_1^2+4,X_1^2-4\bmod16\), which is impossible. This rules out affine lines even with a different direction in each row.

**The remaining counting problem is explicit.** For candidate \(u,v\), put \(H=h+N(u)\), \(K=k+N(v)\), and \(w=Hv-Ku\). The two norm equations reconstruct
\[
z_1=\frac{(-w_y,w_x)}{2D}.
\]
Both coordinates of \(w\) must vanish modulo \(2D\), and the reconstructed point must satisfy \(Q<n<5Q\). At each odd \(p^a\parallel D\), at least one component of \(u\) or \(v\) must be a unit since \(\gcd(h,k)=2\). The two divisibilities there reduce to one scalar test using that unit component and the determinant identities. The choice of component can change with \(p\). This leaves a joint congruence with a moving modulus, often of order \(Q\). A lower bound \(Q^\eta\) for the number of integral triples in the ordinary window on a growing sequence of layers would give \(Q^{\eta-o(1)}\) distinct targets, since each target contributes at most \(Q^{o(1)}\) triples.

There is a quantitative obstacle to bounding the direct minor arcs absolutely. For \(S(\alpha)=\sum_{|j|\le L}e(\alpha j^2)\), set \(f=|S|^2\). The absolute integral of the two-frequency kernel equals
\[
\iint f(\alpha+\beta)f(\alpha)f(\beta)\,d\alpha\,d\beta
 =\sum_m\widehat f(m)^3\ge(2L+1)^3.
\]
Here \(\widehat f(m)\) counts differences of squares and is nonnegative. Simultaneous major arcs with \(q\le R\) and coordinate radii \(R/L^2\) have absolute contribution \(O(L^2R^5)\) by their area and the trivial bound on \(S\). For \(R=L^\varepsilon\), \(0<\varepsilon<1/5\), the complement therefore still has absolute mass \(\gg L^3\), above the \(L^2\) counting scale. This calculation applies to a box at ordinary height: \(L=37T\) contains the explicit seed for \(U\ge3\), and any solution in the box has \(Q<n<5Q\). A zero third residual contributes only \(Q^{o(1)}\) triples.

The displayed absolute-mass estimate does not rule out cancellation in the original two-frequency count. It only rules out this unrestricted absolute-value treatment of its minor arcs.

## Different offsets: a free integer parameter

For the same range of \(U,V\), take \(T\le t\le2T\) and set
\[
n=25T^2+81W^2+5t^2.
\]
Use the three actual exponent pairs
\[
(2V+4,2U+2),\qquad (2V+4,2U+1),\qquad (2V,2U+2).
\]
Their residuals are \(5(t^2+b^2)\) for \(b=0,2T,4W\), respectively, and
\[
5(t^2+b^2)=(t-2b)^2+(2t+b)^2.
\]
The mechanism is the shared square class in \(25-5=5\cdot2^2\) and \(81-1=5\cdot4^2\). All three residuals are positive, \(30T^2<n<75T^2\), and every label grows on both axes. The menu repeats one exponent on each axis.

At fixed \(U\), equal targets from \(V<V'\) require
\[
(t-t')(t+t')=\frac{81}{5}(9^{V'}-9^V).
\]
Since \(t+t'\ge2T\), there are \(O(1+9^U/T)\) possible positive differences per pair \(V,V'\), each determining at most one pair \(t,t'\). Thus the \(O(U^2(1+(9/5)^U))\) collision pairs are \(o(U5^U)\), leaving \(\Theta(U5^U)\) distinct targets per layer. Taking the largest complete layer below \(X\) gives the stated lower bound, and summing the layer sizes gives the matching upper bound.

The fourth corner can genuinely fail at the same \(n\). For \(U=V=1,t=6\), the three labels hold at \(n=1534\), while the fourth residual is \(1400\), with \(v_7=1\). This failure persists for \(U,V\equiv1\bmod21\) and \(t\equiv6\bmod49\), which retain the same population order. The count concerns generated targets and gives no coverage bound for a prescribed integer.

### Offline replay

```python
from itertools import product
from math import gcd, isqrt

def N(z): return sum(x*x for x in z)
def diff(a,b): return tuple(x-y for x,y in zip(a,b))
def det(a,b): return a[0]*b[1]-a[1]*b[0]

def witness(n, labels, rows):
    assert all(n == 3**c + 5**d + N(z)
               for (c,d),z in zip(labels,rows))

def old(U,V):
    T,W = 5**U,3**V
    labels = [(2*V+c,2*U+d) for c,d in [(4,0),(1,3),(5,4)]]
    s = [3**c+5**d for c,d in labels]
    h,k = s[1]-s[0],s[2]-s[0]
    n = 1025*T*T+960*T*W+835*W*W
    rows = [(32*T+15*W,23*W),(-24*W,30*T+16*W),(-20*T-24*W,-4*W)]
    witness(n,labels,rows)
    z,y,x = rows
    u,v = diff(y,z),diff(x,z)
    D = det(u,v)
    w = tuple((h+N(u))*b-(k+N(v))*a for a,b in zip(u,v))
    assert (-w[1],w[0]) == tuple(2*D*a for a in z)
    assert D == 1560*T*T+1670*T*W+780*W*W and D%4 == 2
    assert (h%16,k%16,gcd(h,k)) == (14,2,2)
    return labels,s,n

labels,s,n = old(1,1)
assert (s,n) == ([754,3152,17812],47540)
witness(18740,labels,[(115,69),(102,72),(28,12)])
witness(26660,labels[:2],[(159,25),(132,78)])
assert (26660-s[2])%49 == 28
old(15,8)
assert all(191%j for j in range(2,isqrt(191)+1))
assert 124*53%191 == 78 and pow(53,95,191) == 190

Z = list(product(range(8),repeat=2))
for a,b,c in product(Z,repeat=3):
    if ((N(a)-N(b))%8,(N(a)-N(c))%8) == (6,2):
        assert det(diff(b,a),diff(c,a))%4 == 2
sq = {x*x%16 for x in range(16)}
assert all((x-14*g)%16 not in sq or (x-2*g)%16 not in sq
           for x,g in product(sq,{N((a,b)) for a,b in Z if (a|b)%2}))

def new(U,V,t):
    T,W = 5**U,3**V
    assert (U+1)//2 <= V <= U and T <= t <= 2*T
    labels = [(2*V+4,2*U+2),(2*V+4,2*U+1),(2*V,2*U+2)]
    n = 25*T*T+81*W*W+5*t*t
    witness(n,labels,[(t-2*b,2*t+b) for b in (0,2*T,4*W)])
    assert 30*T*T < n < 75*T*T
    return n,5*(t*t+4*T*T+16*W*W)

assert new(1,1,6) == (1534,1400)
assert pow(25,21,49) == pow(9,21,49) == 1 and 1400%49 == 28
assert new(4,2,999)[0] == new(4,4,945)[0] == 14762191
print("PASS")
```

## New offsets: power-law count with both axes pairwise distinct

For every fixed integer \(m\ge1\), an explicit affine construction gives
\[
\Theta_m\!\left(X^{m/(2m+2)}\right)
\]
distinct targets up to \(X\), each with three positive two-square residuals at the same \(n\). The three \(3\)-exponents are pairwise distinct, the three \(5\)-exponents are pairwise distinct, and all six exponents are \(\asymp_m\log n\). Taking \(m=1\) gives \(X^{1/4}\), and the count exponent approaches \(1/2\) as \(m\) increases.

### Affine construction

Take \(T=5^U,\ W=3^V\) with \(1\le V\le U\). Use the three shifts
\[
(s_1,s_2,s_3)
=(25T^2+27W^2,\;15625T^2+2187W^2,\;T^2+3W^2).
\]
Their exponent pairs \((c,d)\) are
\[
(2V+3,2U+2),\qquad (2V+7,2U+6),\qquad (2V+1,2U).
\]
In particular, these shifts all agree modulo \(16\).

Write \(N(x,y)=x^2+y^2\), \(w=(51T-19W,51T+19W)\), and \(G=N(w)\). The identity behind the construction is
\[
4x^3-3x-1=(x-1)(2x+1)^2.
\]
Applying it at \(25\) and \(9\), with \(25-1=3(9-1)=24\), gives
\[
4(s_2-s_1)-(s_3-s_1)=12G,\qquad s_3-s_1=-24(T^2+W^2).
\]
Consequently any integral \(z\) with \(z\cdot w=3(T^2+W^2)\) gives the same target in all three rows:
\[
\boxed{n=s_1+N(z-2w)=s_2+N(z-w)=s_3+N(z+2w).}
\]
The residual norms are strictly positive because \(z\cdot w+\lambda G\ne0\) for \(\lambda=-2,-1,2\).

The integer line is explicit. Since \(\gcd(51T,19W)=3\) and both quotients by \(3\) are odd, the coordinates of \(w\) have gcd \(6\). Write \(w=6(p,q)\) and \(R=(T^2+W^2)/2\). Choose
\[
x_0=Rp^{-1}\pmod q,\quad 0\le x_0<q,\qquad y_0=(R-px_0)/q.
\]
Then \(z=(x_0+tq,y_0-tp)\) works for every integer \(t\).

### Height and distinct targets

Take \(U=V=j\) and \(T^m\le t\le2T^m\). From \(W\le3T/5\) we get \(6T<p<9T\), \(8T<q<11T\), and \(-9T<y_0<T/8\). Hence \(n(t)\) is strictly increasing for \(t\ge0\): its forward difference is
\[
(2t+1)(p^2+q^2)+2(qx_0-py_0)>0.
\]
For \(t\ge T\), the same bounds give \(25T^2t^2<n(t)<3000T^2t^2\). Thus each layer contributes \(T^m+1\) distinct targets at height \(\asymp T^{2(m+1)}\). Taking the largest complete layer below \(X\) gives the lower bound, and summing the geometrically growing layer sizes gives the matching upper bound.

The height tradeoff is explicit. The largest \(5\)-power is \(\asymp n^{1/(m+1)}\), and the largest \(3\)-power is \(\asymp n^{(\log_5 3)/(m+1)}\). The free line has step \(\asymp T\), so it supplies only \(O(1)\) points per layer in a window \(n=O(T^2)\). The power-law count uses the larger height window and concerns generated targets.

For \(U=V=1,\ t=5\), the target is \(657297\). The labels \((5,4),(9,8),(3,2)\) have square coordinates \((-115,-802),(83,-490),(677,446)\), respectively. At that same target the crossed label \((3,4)\) fails: its residual is \(656645\equiv99\pmod{121}\), so \(v_{11}=1\).

### Exact replay

```python
from math import gcd

def N(x, y):
    return x*x + y*y

def family(U, V, t):
    assert 1 <= V <= U
    T, W = 5**U, 3**V
    a, b = 51*T - 19*W, 51*T + 19*W
    assert gcd(a, b) == 6
    p, q = a//6, b//6
    R = (T*T + W*W)//2
    x = R*pow(p, -1, q) % q
    y = (R-p*x)//q
    assert p*x + q*y == R
    x, y = x+t*q, y-t*p
    G = N(a, b)
    labels = [(2*V+3, 2*U+2), (2*V+7, 2*U+6), (2*V+1, 2*U)]
    s = [3**c + 5**d for c,d in labels]
    assert 4*(s[1]-s[0])-(s[2]-s[0]) == 12*G
    rows = [(x+l*a, y+l*b) for l in (-2,-1,2)]
    n = N(x,y) + 4*G + 13*T*T + 15*W*W
    assert all(n-S == N(*z) > 0 for S,z in zip(s,rows))
    if t >= T:
        assert 25*T*T*t*t < n < 3000*T*T*t*t
    return n, labels, rows

n, labels, rows = family(1, 1, 5)
assert (n, labels, rows) == (
    657297, [(5,4),(9,8),(3,2)], [(-115,-802),(83,-490),(677,446)]
)
assert (n-3**3-5**4) % 121 == 99
for j in range(1, 16):
    T = 5**j
    assert family(j,j,T)[0] < family(j,j,T+1)[0] < family(j,j,2*T)[0]
print("PASS")
```
