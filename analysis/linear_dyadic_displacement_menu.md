# Linear displacement menus and shorter integral lines

For fixed adjacent power labels \(L=3^c+5^d\), \(U=3^{c+1}+5^{d+1}\) with even \(c\ge2\), put \(D=U-L\) and \(Q=27\cdot2^k\), \(k\ge5\). There is a menu of \(O(k)\) primitive displacements, of maximum length \(O(\sqrt Q)\), covering exactly the locally admissible common target classes. The menu size matches the lower bound in [#91](https://github.com/Samsen879/a303656/pull/91). On each class the construction gives an integral line with consecutive selected points at Euclidean distance \(O(Q)\). In the label-height regime below this yields true common targets at forward gaps \(o(X)\) for \(Q=o(\sqrt X)\). It does not show that the prescribed integer itself is a common target.

## Classifying the dyadic part

Write \(B=N-L\). For a displacement \(s=(u,v)\) set \(A=u^2+v^2=2a\), \(H=(D+A)/2\), with both \(u,v\) odd. We need \(z\cdot s=H\) and \(|z|^2=B\) locally, since then \(|z-s|^2=B-D\). Here \(D\equiv6\bmod8\) and \(3\nmid D\). The classes admissible modulo \(2^k\) have \(B=0,2\bmod8\). For nonzero \(B=2^e\rho\) with \(e<k\), an admissible representative can be chosen with odd part \(\rho=1\bmod4\); if \(e=1\), it must also have \(\rho\equiv D/2+2\equiv-D/2\bmod8\) because \(B-D\) must have its odd part \(1\bmod4\) at valuation two. These necessary conditions follow by dividing the coordinates by their largest common power of two. At the highest nonzero valuation the missing bits of \(\rho\) can be chosen in the representative. The construction below proves sufficiency, including liftability to modulo \(2^{k+1}\).

| Dyadic case | Scale \(z=2^j z'\) | Prescribe \(H\) |
| --- | --- | --- |
| \(e=2j\ge4\) | \(j=e/2\) | \(2^j\bmod2^{j+1}\) |
| \(e=2j+1\ge3\) | \(j=(e-1)/2\) | \(0\) or \(2^{j+2}\bmod2^{j+3}\) |
| \(e=1\) | \(j=0\) | \(0\bmod8\) |
| \(B=0\bmod2^k\) | \(j=\lfloor k/2\rfloor\) | \(0\bmod2^{\lceil k/2\rceil}\) |

For the nonzero rows set \(t=H/2^j\) and \(B'=B/2^{2j}\). The determinant identity reduces existence over \(\mathbb Z_2\) to the square \(w^2=AB'-t^2\). Indeed \(z'=((ut-vw)/A,(vt+uw)/A)\) is integral because \(w\equiv t\bmod2\) and \(A\) has valuation one. It has the required norm and dot product. In the first row the discriminant is \(1\bmod8\) because \(a\equiv1\bmod4\) and \(t\) is odd. In the second row divide by 4 to get \(a\rho-(t/2)^2\). Here \(a\rho\equiv1\bmod4\) with \(a\equiv-D/2\bmod8\); the choices subtract 0 or 4 modulo 8, allowing the result to be 1. In the third row, after division by 4 the residue is \((-D/2)\rho\equiv1\bmod8\). An odd unit \(1\bmod8\) has a square root in \(\mathbb Z_2\), by elementary bit lifting. For the zero row, every integral point on the scaled dot-product line has norm \(0\bmod2^k\): for odd \(k\), \(t\) is even, so both coordinates of \(z'\) have the same parity. To see a common lift modulo \(2^{k+1}\) of this zero class independently of the prescribed displacement, choose \(B=2^{2\lceil(k+1)/2\rceil}\), so \(B-D\equiv2\bmod8\), which is a dyadic norm by the local square argument or by writing it as the sum of two odd squares.

## Bounded first coordinate and primitive menu

For each of the 15 modulo-27 admissible norm pairs, take any two coordinates with norms \(B,B-D\bmod27\), then subtract. At least one difference is a unit modulo 3. Simultaneously swap the coordinate axes if needed so the first difference is such a unit, and fix its smallest positive odd representative \(u\le53\). A prescription \(H_0\bmod2^h\) is realized by solving \(v^2\equiv2H_0-D-u^2\bmod2^{h+1}\). The right side is \(1\bmod8\) for all prescriptions, since \(D\equiv6\bmod8\) and \(u\) is odd. Take a root, require the original second difference modulo 27 and \(v\equiv1\bmod u\), and apply CRT with pairwise coprime moduli. We can take \(0\le v<27u\,2^{h+1}\), giving primitivity without any logarithmic loss.

There are \(O(k)\) prescriptions and \(h+1\le\lceil k/2\rceil+3\). More precisely, \(\sqrt A=O(2^j)\) in each nonzero row, and \(O(2^{\lceil k/2\rceil})\) in the zero row. Conversely, for a nonzero low norm of valuation \(2j\), \(z/2^j\) has exactly one odd coordinate and \(s\) has two odd coordinates (the low and high norms are \(0,2\bmod4\)). Therefore \(v_2(D+A)=j+1\). Taking one admissible class for each \(2\le j\le\lfloor(k-1)/2\rfloor\) gives \(\Omega(k)\) displacements. This does not match the best length lower bound \(\Omega(Q^{1/4})\).

## The integral line keeps the scale

Take an integral solution to \(u z'_1+v z'_2=t\) and move along the primitive direction \((-v,u)\). Any dot-product solution modulo a modulus at which \(u\) is a unit is represented by exactly one parameter class. For the nonzero rows the dyadic norm condition on \(z'\) uses only modulus \(2^{k-2j}\), and the modulo-27 condition uses modulus 27 since \(2^j\) is invertible there. Combine them by CRT. In the zero row no dyadic restriction on the parameter is necessary. Thus consecutive selected original points have Euclidean distance
\[
P=27\cdot2^{k-j}\sqrt A=O(Q)\quad(e<k),
\qquad
P=27\cdot2^{\lfloor k/2\rfloor}\sqrt A=O(Q)\quad(B=0).
\]
The minimum real target along the line is \(\mu=L+H^2/A\). Taking the first selected point strictly above \(T>\mu\) on the increasing ray gives \(0<N-T\le2P\sqrt{T-\mu}+P^2\). For the smallest even \(c\) and integer \(d\) with \(3^c\ge X^{1/8}\), \(5^d\ge X^{1/3}\), both labels belong to the original exponent window for large \(X\). In this regime \(D=O(X^{1/3})\) and \(\mu=O(X^{2/3}+Q)\). Hence if \(T\asymp X\) and \(Q=o(\sqrt X)\), the gap is \(o(X)\) and both residuals are positive.

## Exact replay

The block checks integer witnesses in every modulo-27 admissible class for seven dyadic cases, including both endpoint parities and the highest nonzero valuation. It checks the false lift \(B=2\bmod16\) versus \(B=10\bmod16\) for the actual label pair.

```python
from math import gcd, isqrt

X = 10**12
L, U = 3**4+5**6, 3**5+5**7
D = U-L
for c,d in [(4,6),(5,7)]:
    assert 3**(4*c)<=X<=3**(8*c) and 5**(2*d)<=X<=5**(3*d)

def norm(p): return sum(x*x for x in p)
def crt(a,m,b,n): return a+m*((b-a)*pow(m,-1,n)%n)

p27 = {}
for x in range(27):
    for y in range(27):
        p27.setdefault((x*x+y*y)%27, (x,y))
classes = sorted(r for r in p27 if (r-D)%27 in p27)
assert len(classes)==15
assert (2-D)%16==12 and (10-D)%16==4

def witness(k,B,R,j,h,H0):
    u,v0 = ((a-b)%27 for a,b in zip(p27[R],p27[(R-D)%27]))
    if u%3==0:
        u,v0 = v0,u
    assert u%3
    u += 27 if u%2==0 else 0
    m = 1<<(h+1)
    v2 = next(v for v in range(m) if (v*v-2*H0+D+u*u)%m==0)
    v = next(v for v in range(crt(v2,m,v0,27),27*m*u,27*m)
             if gcd(u,v)==1)
    A, H, s = u*u+v*v,(D+u*u+v*v)//2,1<<j
    assert H%s==0
    y0 = (H//s)*pow(v,-1,u)%u
    x0 = (H//s-v*y0)//u

    def xy(t): return s*(x0-v*t),s*(y0+u*t)

    M = 1 if B==0 else 1<<(k-2*j)
    t2 = next(t for t in range(M) if (norm(xy(t))-B)%(1<<k)==0)
    t3 = next(t for t in range(27) if norm(xy(t))%27==R)
    t0 = crt(t2,M,t3,27)
    lo = isqrt(A*(X-L)-H*H)+1
    w = s*(u*y0-v*x0)
    t = (lo-w+s*A-1)//(s*A)
    t += (t0-t)%(27*M)
    x,y = xy(t)
    N = L+x*x+y*y
    assert N>X and N==U+(x-u)**2+(y-v)**2
    assert (N-L)%(1<<k)==B and (N-L)%27==R
    return N,u,v

# k, B, scale exponent j, exponent h, prescribed H0
for k,B,j,h,H0 in [(5,10,0,3,0),(5,16,2,3,4),(5,8,1,4,8),
                   (6,40,1,4,0),(6,32,2,5,16),
                   (6,0,3,3,0),(7,0,3,4,0)]:
    got = [witness(k,B,R,j,h,H0) for R in classes]
    assert X < got[classes.index(0)][0] < 2*X
    if k==7:
        assert got[classes.index(0)]==(1107829825498,53,673)
print("OK")

```
