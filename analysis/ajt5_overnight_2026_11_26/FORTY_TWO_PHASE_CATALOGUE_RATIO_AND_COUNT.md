# The ray (229,21) improves the certified constructive catalogue gap

The earlier [41-phase catalogue](https://github.com/Samsen879/a303656/commit/61aaca7206f7d06c15a5d4001348a9252beb7e0e) uses a closed interval with a duplicate right endpoint 54=3·18. After inserting the exactly certified new phase 458/9, the closed list has 43 entries but the actual number of distinct cubing phases is **42**. The exact ratio audit below takes the largest gap from 47/45 on (50,470/9) to **145/139 on (278/9,290/9)**. Previously certified old ray coordinates are not recopied here.

## Per-layer count on the new ray

Use the exact two half norms of (229,21) and conjugate the positive one before multiplying their coordinates. Scale by 8 to get x²+3W²=4(Q−Z), where Q=(5^229)² and Z=(3^21)² at the base. Among the three unit rotations modulo overall sign, the replay shows all |W|>sqrt(Q)/2. Exactly two W are units mod 3, while mod 5 the base W² residues of the three rotations are 0,1,1, with zero initially in the first rotation. Cubing multiplies by Q+Zω or Q+Z conjugate(ω), where ω=(1+sqrt(−3))/2; its norm is Q²+QZ+Z². Each factor is 1 modulo 3 as an Eisenstein integer and is a unit of rotation ±60 degrees up to sign modulo 5 (Q≡0,Z≡−1). At every positive cubing depth choose the signs so their total is nonzero modulo 3; then the zero mod-5 W² sits on one of the two mod-3 unit rotations, and the other has W²=1. This choice does not affect uniform angular control: each multiplier's arg has magnitude ≤Z/Q, with summable total <2 Z_base/Q_base, so all rotated |W| remain comparable to sqrt(Q). At each depth both choices satisfy W divisible by 4 and W²≡0 or 1 mod 5, respectively. The exact first-layer replay yields four distinct n in two classes, and strict height Q<n<5Q.

Let s=sqrt(Z) at a layer. For L=1,3 form M=3W²+2L Z, comparable to Q. These M are 2 mod 4 and have exactly v_3(M)=1. The two choices of W² have opposite nonzero quadratic characters modulo 5 for either L, so the squarefree parts of their M are distinct. In the [Gauss three-square formula](https://pure.mpg.de/rest/items/item_3118169/component/file_3118171/content), r_3(M)=12H(4M) in these residue classes. Writing M=d f², the class number of the order of discriminant −4M has the usual conductor factor f ∏_(p|f)(1−χ_(−4d)(p)/p), up to the bounded units factor. [Tatuzawa's bound](https://www.jstage.jst.go.jp/article/jjm1924/21/0/21_0_163/_article) has at most one exceptional fundamental discriminant; at least one of our two distinct −4d avoids it. The conductor factor is ≫_ε f^(1−ε) and the good fundamental class number is ≫_ε d^(1/2−ε). Thus at least one orientation gives r_3(M)≫_ε Q^(1/2−ε).

Each representation of M has exactly two odd coordinates and all three are units modulo 3. Let t be the absolute smaller odd coordinate, so t²≤M/2. Then
```
n = 5Q − 3W² − LZ + t²
  = Q + (4−L)Z + x² + t²
```
is a true ordinary target in (Q,5Q), in class 21 mod 24 for L=1 and class 3 for L=3. The height follows from the second form and the t² bound in the first. Each chosen t can occur with at most O_ε(Q^ε) residual two-square coordinate choices, by the divisor bound, so at least ≫_ε Q^(1/2−ε) distinct targets remain on that layer in each class after renaming ε.

Combine this new layer estimate with the previously certified layer estimates on the old catalogue. The new maximum logarithmic-height ratio is 145/139. The last completed height scale 5Q≤X consequently has Q≫ X^(139/145). For each of the two classes this gives a constructive counting lower bound ≫_ε X^(139/290−ε), improving 45/94. This is a lower bound on the growth of these explicit represented families; it is **not** a natural-density increase or a percentage of the conjecture solved. The replay adds a separate exact inert veto at the true label (427,305), which does not enter the catalogue.

```python
from math import gcd, isqrt, lcm

A, S = 5**229, 3**21
H, J = (A-S)//2, (A+S)//8
p = 3692254399036927
assert 2*H == A-S > 0 and 8*J == A+S
assert H%p == J%199 == 0 and gcd(p,H//p) == 1

coords=[]
for N, b, E in [(H,13,lcm(p-1,H//p-1)), (J,12,lcm(198,J//199-1))]:
    while E%3 == 0:
        E //= 3
    z = pow(b,E,N)
    assert (z*z+z+1)%N == 0
    r = (2*z+1)%N
    a,x = N,min(r,N-r)
    while x*x > N:
        a,x = x,a%x
    y = isqrt((N-x*x)//3)
    assert x*x+3*y*y == N
    coords.append((x,y))

def mul(z,w):
    a,b=z
    c,d=w
    return a*c-3*b*d,a*d+b*c
def half(z):
    assert not any(v%2 for v in z)
    return tuple(v//2 for v in z)


def rotations(z):
    for _ in range(3):
        yield z
        z=half(mul(z,(1,1)))
u,v=coords
z=tuple(8*i for i in mul(u,(v[0],-v[1])))
assert all(2*abs(w)>A for _,w in rotations(z))
assert [(w%3==0,w*w%5) for _,w in rotations(z)]==[(True,0),(False,1),(False,1)]
z=half(mul(z,(2*A*A+S*S,S*S)))
Q,s=A**6,S**3
ns,wtypes=set(),set()
for x,W in rotations(z):
    if W%3:
        W=abs(W)
        assert W>3*s and 64*W*W>=4*(Q-s*s)
        wtypes.add(W*W%5)
        for L,cl in [(1,21),(3,3)]:
            n=Q+(4-L)*s*s+x*x+(W+s)**2
            assert n==5**1374+3**(126+(L==1))+x*x+(W+s)**2
            assert Q<n<5*Q and n%24==cl
            ns.add(n)
assert len(ns)==4 and wtypes=={0,1}
from fractions import Fraction as F
old=list(map(F,"18 166/9 170/9 514/27 178/9 182/9 62/3 190/9 22 202/9 206/9 70/3 218/9 74/3 674/27 26 710/27 82/3 742/27 86/3 266/9 30 278/9 290/9 298/9 34 314/9 106/3 110/3 38 118/3 122/3 42 130/3 134/3 46 142/3 146/3 50 470/9 158/3 54".split()))
new=sorted(old+[F(458,9)])
def gap(a): return max((v/u,u,v) for u,v in zip(a,a[1:]))
assert len(old)-1==41 and len(new)-1==42 and old[-1]==3*old[0]
assert gap(old)==(F(47,45),F(50),F(470,9))
assert gap(new)==(F(145,139),F(278,9),F(290,9))
assert 1/(2*gap(new)[0])==F(139,290)
p=321593
assert p%3==2 and all(p%i for i in range(2,isqrt(p)+1))
assert gcd(5**427+3**305,p*p)==p
```
