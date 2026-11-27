# An integral-target separation for Pell prime allocations in the critical band

For distinct integral targets with the same oriented Gaussian difference and the same sign of the imaginary cross product, let d=2j>0 and set e=U2−U1, b=D1+D2, g=D2−D1, W=ebg. The actual label parameters are U_i=2A_i+3B_i and D_i=A_i+2B_i with A_i=9^r_i, B_i=25^s_i; the critical band restricts A_i≤B_i, B_i^16≤n≤A_i^32 and X≤n<2X.

The oriented difference fixes d, and the Gram identity gives
[
 x=d(2n-U_1-U_2)-W,qquad y=2h,qquad x^2-dy^2=R=(d+e^2)(d+b^2)(d+g^2).
]
Between two solutions x,y and x',y' compare their positive larger Pell conjugates. Write eta for their ratio and V=(eta+eta^(-1))/2. If the allocations at split prime p differ by u_p in one component (and by −u_p in its conjugate), put m=prod p^|u_p|. Unique factorization of ideals in the maximal order gives m|R and m eta integral: any negative valuation of eta occurs in one split component and is canceled by the corresponding power of p. Inert and ramified valuations agree, since the norms are fixed. If d is square the two rational factors give the same statement without the field. The rational trace shows 2m(V−1) is an integer.

The exact integral-target congruence contributes new divisibility:
[
 R(V-1)=x'x-dy'y-Requiv0pmod d
]
because both x and x' reduce to −W and R≡W² modulo d. In particular d/gcd(d,R/m) divides 2m(V−1). Distinct targets give V>1 in a fixed sign sector. For d≈J with X≤J≪X²/(log X)^4, the larger conjugate is 4dn(1+o(1)) uniformly: x=2dn(1+o(1)) and R/x²=O(d/X²)=o(1). Hence V−1=O(1). As e,b,g=O(X^1/16), W=O(X^3/16) and gcd(d,R)≤W²; consequently m≫J^5/8. For large J, changing only a set of split prime allocations whose combined available prime power budget is at most J^1/2 cannot take one integral target to a distinct one with the same oriented difference and sign sector.

This rules out close allocation changes; it does not give a uniform bound on all allocations or imply the claimed whole- or partial-moment upper bound by itself. Those estimates additionally require a mixed-weight polynomial sieve and averaged bad-prime control, not asserted here.

## Independently replayed native control

The following integral seeds have the same actual target, different labels and a 553-bit deficit; the positive Pell constraint and threshold are exact.

~~~python
from math import gcd, isqrt, prod

K, X, B = 300, 1 << 300, 25**4
a, u = 3395, 473908545666970293546287554900113349394416
x = a*u + 9**3 + 2*B - (a*a+1)//2
n = x*x + u*u + 3*9**3 + 5*B

def cert(r, P, Q):
    A = 9**r
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    x,y = P
    c,d = Q
    f,g,h = x-c,y-d,x*d-y*c
    assert X<=n<2*X and A<=B and B**16<=n<=A**32
    assert x*x+y*y==S and c*c+d*d==S+2*D
    assert f%2 and g%2 and h%2==0
    q = ((f+g)//2)**2 + ((f-g)//2)**2
    assert q%2 and 2*q*S==(D-q)**2+h*h
    assert X<=S<2*X and 64*K*K*q<S<64*K*(K+1)*q
    return q,(n-U-q,abs(h)),U,D

p1 = (370364302106323949618686923647947300990535546,
      -1565711501568699087370650397834208298305903076)
p2 = (371286745392217617117272419857876274653556789,
      -1565493013435470228569674359748079227673377687)
q,(a,b),U,D = cert(3,(x,u),(x+1,3395-u))
qq,(c,f),V,E = cert(5,p1,p2)
assert q!=qq
e,bs,g = V-U,D+E,E-D
H,L = 2*n-U-V,(n-U)*(n-V)-(D*D+E*E)//2
j,h = L-a*c-b*f,a*f-b*c
d,du,dv = 2*j,a-c,b-f
C,W = du*du+dv*dv,e*bs*g
xx,yy = d*H-W,2*h
R = prod(d+l*l for l in (e,bs,g))
assert j**5>X**9 and 0<h*h*K**4<(a*a+b*b)*(c*c+f*f)
assert C==d+e*e and xx*xx-d*yy*yy==R
assert d//gcd(d,R)>isqrt(j)

assert j.bit_length()==553
~~~
