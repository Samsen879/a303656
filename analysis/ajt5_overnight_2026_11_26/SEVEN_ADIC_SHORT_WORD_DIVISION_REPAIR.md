# Short division repair for rank-deficient 7-primary word reads

At common prime support, assume x has order 343 and each captured word value Z_i lies in <x>. Logarithms relative to x^L give a linear system W(F,G)^T=d modulo 343. For two integral rows and nonzero determinant, let s_1≤s_2 be the valuation exponents in 7-local Smith form (s_1 is the minimum entry valuation, and s_1+s_2=v_7(det W)). With c_i=min(3,s_i), the system, when consistent, has a kernel and any solution fiber of size 7^(c_1+c_2). If a third row in those coordinates is (a,b), its restriction to that kernel has image of size 7^max(0,c_1−v_7(a),c_2−v_7(b)). Hence, when already rank one modulo 7, full repair occurs exactly when the new row is transverse modulo 7. If rank zero, a single extra row cannot give full repair. These statements do not convert an order above 343 into an order-343 read.

A transverse word can sometimes be constructed rather than searched. When w_1 is nonzero modulo 7 and t=v_7(det(w_1,w_2))>0 is finite, choose centered c modulo 7^t with w_2≡cw_1, then let w_3=(w_2−cw_1)/7^t. Its determinant with w_1 is a 7-unit. On the original common capture support, let Q=Z(w_3)^H where H is a 7-power. Q^(7^t)=1 by the original capture, so Q has 7-power order and Z(w_3) does as well. With H=7^(bitlength(R)), it kills all 7-primary orders modulo each prime factor p of R. Recompute the actual word rather than take an arbitrary modular root. If both input words have physical sup norm at most h, the output norm is at most h(1+7^(−t))/2. This is in physical integer coordinates, not in a native lattice basis.

For the true source (14,152), the replay certifies p=4564509729907, two actual word pairs with kernel sizes 7 and 49, and the same repaired word (647,278) from both. The recovered original axes are (300,308) modulo 343. The tested old rows all lie on u+2v=0 mod 7, while the new row is transverse. An exact meet-in-the-middle search finds only the zero word and this signed pair in the physical half-width 647 capture box. This result is precision recovery, not a full source veto or an arbitrary-target representation. The other factor of R is composite and is not closed here.

## Exact replay

```python
from math import gcd, isqrt, prod

R = 7794092988996359616004983264299816596361951171
x = 13637500586108896670367803493377664812606052
assert pow(x,343,R)==1 and gcd(pow(x,49,R)-1,R)==1
assert (1-x+pow(x,14,R)-pow(x,152,R))%R==0

B = 2**19
s = bytearray(b'\1')*(B+1)
s[:2] = b'\0\0'
for a in range(2,isqrt(B)+1):
    if s[a]:
        s[a*a::a] = b'\0'*((B-a*a)//a+1)
def power(a):
    b = a
    while b*a <= B:
        b *= a
    return b
L = prod(power(a) for a in range(2,B+1) if s[a] and a!=7)
U,V = (pow(a,L,R) for a in (3,5))
H = 7**R.bit_length()
def word(w):
    return pow(U,w[0],R)*pow(V,w[1],R)%R
def det(a,b):
    return a[0]*b[1]-a[1]*b[0]

A,B,C = (4317,547),(212,1399),(10118,10887)
assert A==tuple(-175*a-474*b for a,b in zip((-3,5),(-8,-3)))
assert B==tuple(109*a-430*b for a,b in zip((-2,1),(-1,-3)))
assert C==tuple(739*a-320*b for a,b in zip((2,13),(-27,-4)))
D = (647,278)
assert tuple(a+b for a,b in zip(A,B))==tuple(7*d for d in D)
assert tuple(5*a+c for a,c in zip(A,C))==tuple(49*d for d in D)
assert det(A,B)==7*846217 and det(A,C)==49*846217
assert det(A,D)==846217 and det(A,D)%7!=0

p = gcd(R,pow(word(A),H,R)-1,pow(word(B),H,R)-1)
assert p==4564509729907 and p%1372==687
assert all(gcd(R,pow(word(w),H,R)-1)==p for w in (A,B,C,D))
for n,fs in ((846217,[73,23]),(p,[846217,2621])):
    assert all(all(f%d for d in range(2,isqrt(f)+1)) for f in fs if f!=846217)
    F = prod(fs)
    assert (n-1)%F==0 and F*F>n and pow(2,n-1,n)==1
    assert all(gcd(pow(2,(n-1)//f,n)-1,n)==1 for f in fs)
q = R//p
assert p*q==R and gcd(2,q)==1 and pow(2,q-1,q)!=1

logs = {pow(x,(L%343)*i,p):i for i in range(343)}
assert [logs[word(w)%p] for w in (A,B,C,D)]==[338,229,221,179]
assert [(300*u+308*v)%343 for u,v in (A,B,C,D)]==[338,229,221,179]
assert [gcd(det(A,w),343) for w in (B,C,D)]==[7,49,1]
assert all((u+2*v)%7==0 for u,v in (A,B,C)) and sum((D[0],2*D[1]))%7==6

P,Q = (pow(u,H,p) for u in (U,V))
I = {pow(P,i,p):i for i in range(-647,648)}
assert len(I)==1295
assert {(I[z],j) for j in range(-647,648)
        if (z:=pow(Q,-j,p)) in I}=={(0,0),D,(-647,-278)}
print("PASS")
```

The source integer R can additionally be regenerated with SymPy:
```python
from sympy import symbols, resultant
z=symbols('z')
assert resultant(sum(z**i for i in range(0,343,49)),1-z+z**14-z**152,z)==7*R
```
