# Preselected trace ratios separate two blocks and certify phase 514/27

For fixed odd traces t,s use u=(1+kr/t)/2 and v=(1+kr/s)/2 where r²=−3. Choose rational τ and t:s=(2τ²−1):(2τ³−1), and keep all displayed denominators units in the supported prime component. A hit u²=v³ forces v≠0 away from t−s; with x=u/v we get u=x³,v=x². The eliminated equation factors as (x−τ)((2τ²−1)x²+(1−τ)x+τ(1−τ))=0. The other branch has discriminant (τ−1)(8τ³−3τ−1). A nonsquare leaves only τ. Its conjugate mismatch is τ²(τ−1)²(2τ²+4τ+3); when this is a unit the hit is one-sided. Then the exact weight is governed by C²+3k²=0, C=t(2τ³−1)=s(2τ²−1). Any chosen signs on verified coprime supported prime powers combine by CRT, with simple-root lifting allowed. If the quadratic discriminant splits, the other roots must separately pass the conjugate mismatch test.

Actual τ=−1/3 gives (t,s)=(21,29) inside the old 2,…,21 base panel. For the complete (29,17) plus half the replay isolates 19 and 25741 by modular probes, and their four weight classes have least positive representative 86890, simultaneously one-sided on both blocks. The earlier 4/8 traces cannot separate p=19 for any weight, and the old unweighted normalized panel misses 25741. On that same 25741 block τ=+1/3 gives three verified one-sided classes. The true plus norm does not cure the minus half, whose v11 is one. Discovery chose constants after diagnostics; the whole-half replay does not input the decomposition.

All low-scale U=29 labels are excluded, while the complete true higher seed (257,19) yields both signed norms and phase 514/27. Scale 9 is not exhausted. The new 40-ray catalogue's largest ratio is 45/43 at (86/3,30), giving effective lower exponent 43/90 in each class 3 and 21 mod 24, with ε loss; this gains 1/4005 from 85/178. Both exponent axes grow. The integer rotations verify actual same-height controls and opposite characters mod 5 at each parity depth; actual angles have a uniform sine bound under cubing. For the two classes the Gauss sphere count avoids the single possible exceptional discriminant by the two distinct squarefree kernels, and divisor multiplicity is O_ε(Q^ε). This is effective for the constructed family only, not natural density one or an arbitrary prescribed target. Initial label search used finite sieving and ECM; verification uses exact integer norms.

~~~python
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt, lcm

def N(x, y):
    return x*x + 3*y*y

def crt(a, b, p, q):
    return a + p*((b-a)*pow(p, -1, q) % q)

def err(t, s, k, r, p):
    uv = [((t+k*x)*pow(2*t,-1,p)%p, (s+k*x)*pow(2*s,-1,p)%p)
          for x in (r,-r)]
    return [(u*u-v**3)%p for u,v in uv]

H = (5**29+3**17)//8
C, B = -609, 27
def G(k):
    return C*C + 3*B*B*k*k

p = gcd(H,G(3))
h = H//p
z = pow(7,lcm(*(i for i in range(1,14) if i%3)),h)
q = gcd(h,z*z+z+1)
assert (p,q) == (19,25741)
r1, r2 = C*pow(3*B,-1,p)%p, (2*z+1)%q
weights = sorted(crt(C*pow(B*x,-1,p)%p,C*pow(B*y,-1,q)%q,p,q)
                 for x,y in product((r1,-r1),(r2,-r2)))
assert weights == [86890,119038,370041,402189]
k = weights[0]
d = gcd(H,G(k))
r = C*pow(B*k,-1,d)%d
assert (d,r) == (489079,286212)
for j in (p,q):
    assert all(j%i for i in range(2,isqrt(j)+1))
    assert pow(32,(j-1)//2,j)==j-1 and (r*r+3)%j==0
    e0,e1 = err(21,29,k,r,j)
    assert e0==0 and e1!=0 and all(err(21,29,1,r,j))
assert [k for k in range(19) if 0 in err(7,15,k,4,19)] == [7,12]
assert all(err(7,15,k,4,19)==[0,0] for k in (7,12))
assert all(err(21,25,k,3061,q)[0]==0!=err(21,25,k,3061,q)[1]
           for k in (7446,2901,6172))

def power(a,i):
    if i==2:
        return a*a-1,2*a-1
    return a**3-3*a+1,3*a*a-3*a

for a,b,i,j in product(range(2,22),range(2,22),(2,3),(2,3)):
    if i>j or (i==j and a==b):
        continue
    x,y = power(a,i)
    v,w = power(b,j)
    T,S = (2*b-1)**j,(2*a-1)**i
    x,y = T*x-S*v,T*y-S*w
    assert (x*x-x*y+y*y)%q

h = H//d
e = h-1
while e%3==0:
    e//=3
z = pow(2,e,h)
R = crt(r,(2*z+1)%h,d,h)
assert (z*z+z+1)%h==0 and (R*R+3)%H==0
a,b = H,min(R,H-R)
while b*b>H:
    a,b = b,a%b
assert b==3326620156 and N(b,2017974455)==H
assert ((5**29-3**17)//2)%121==55

# A zero entry invokes the exact 2-adic veto.
D = [17,0,3748739,11,4920473,0,479,0,11,0,47,13650977,
     140171,0,59,95876687,17,0,11,1217,17]
assert 3**41<5**29<3**43
for v in range(43):
    f = 25**29-9**v
    g = D[v//2] if v%2 else 0
    if g:
        assert g%3==2 and f%g==0 and gcd(g,f//g)==1
    else:
        assert ((f&-f).bit_length()-1)%2==1

A,S = 5**257,3**19
m = (218852462724906178320250943330341008682828208243467242265867982572901631042639248078572211,
     236648694225994457468640173418245778582682515012695924073579307231880582956479963701327706)
p = (218921862442703528239951205350526560626836798942335569130887632991870769011004456101301468,
     44904608575506194102754983577350841041352111393562015359671515459617416180138851230328410)
assert 2*N(*m)==A-S and 8*N(*p)==A+S

def mul(z,w):
    x,y=z
    a,b=w
    return x*a-3*y*b,x*b+y*a

def rot(z):
    x,y=z
    return z,((x-3*y)//2,(x+y)//2),((-x-3*y)//2,(x-y)//2)

Q,Z = A*A,S*S
z = tuple(8*t for t in mul(m,p))
assert N(*z)==4*(Q-Z) and Q>1000*Z
assert all(23*w*w>=4*(Q-Z) for _,w in rot(z))
assert (Q%30,Z%30)==(25,9)
v = z
for depth,sign in enumerate((1,-1,1)):
    q,s = Q**(3**depth),Z**(3**depth)
    assert N(*v)==4*(q-s)
    ww = sorted(w%15 for _,w in rot(v) if w%3)
    assert ww==[5,14]
    for L in (1,3):
        assert {pow(3*w*w+8*L,2,5) for w in ww}=={1,4}
    v = mul(v,((q-s)//2,sign*((q+s)//2)))

W,V = max((abs(w),abs(v)) for v,w in rot(z) if w%3)
for L in (1,3):
    for t in (W,S+17):
        x,y = (t-S,t) if L==1 else (t+S,t-2*S)
        n = 5*Q+L*Z-x*x-y*y
        R = n-Q-(4-L)*Z
        assert Q<n<5*Q and R>0 and n%24==(21 if L==1 else 3)
        if t==W:
            assert R==V*V+(W+S)**2
        else:
            assert R%121==99   # Exact odd 11-valuation at this label.

P = sorted(map(F, """18 166/9 170/9 178/9 182/9 62/3 190/9 22 202/9
206/9 70/3 218/9 74/3 674/27 26 710/27 82/3 742/27 86/3 30 278/9
290/9 298/9 314/9 34 106/3 110/3 38 118/3 122/3 42 130/3 134/3
46 142/3 146/3 50 470/9 158/3 54""".split()))
def gaps(P):
    return sorted(((b/a,a,b) for a,b in zip(P,P[1:])),reverse=True)
assert len(P)==40 and gaps(P)[0]==(F(89,85),F(170,9),F(178,9))
g = gaps(sorted(P+[F(514,27)]))
assert g[0]==(F(45,43),F(86,3),F(30)) and g[1][0]<g[0][0]
assert F(43,90)-F(85,178)==F(1,4005)
print("PASS")
~~~
