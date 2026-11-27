# A fixed oriented Gaussian difference gives stronger integral target spacing

This is an algebraic refinement of the [integral-target allocation trace](https://github.com/Samsen879/a303656/commit/038dec98c40a2fcbcb268af5eb0b8a9cd7a49035). In the actual critical t=8 seed band, fix two labels with U₁<U₂, the same oriented difference Δ=z₁−z₂, and one sign sector of the imaginary cross term h. Retain e=U₂−U₁, b=D₁+D₂, g=D₂−D₁, C=N(Δ)=d+e², Q=(d+b²)(d+g²), R=CQ, and d=2j>0. Assume g≠0 for power and distance conclusions below.

For two true integral targets set s=n′−n, c=z₁′−z₁ (the same increment also takes z₂ to z₂′), and let V be the half-trace of the ratio of the larger positive Pell conjugates. Subtract the projections of z₁ and z₁′ onto Δ. This gives conjugate(Δ)c=e s+i(h′−h), hence C N(c)=e²s²+(h′−h)². Expanding the difference of the two Pell points gives R(V−1)=2d((h′−h)²−ds²). Thus

~~~text
Q(V−1) = 2d ℓ,  ℓ = N(c)−s².
~~~

In ordinary-height shells with X≤j≪X²/(log X)^4, x=2dn(1+o(1)), R/x²=o(1), and the logarithmic derivative of the larger conjugate α=x+sqrt(x²−R) is 2d/sqrt(x²−R)≈1/X. For distinct targets this gives V−1≈(s/X)² and ℓ≈d(s/X)². The actual integral Gaussian coordinates impose ℓ∈Z and ℓ>0.

Let m be the product over split primes of p to the absolute change in allocation on either side. As in the preceding note, d/gcd(d,R/m) divides 2m(V−1), so

~~~text
Q/gcd(Q,4m gcd(d,R/m)) divides ℓ.
~~~

Since gcd(Q,d) divides b²g², this yields |s|≫X sqrt(d/(m b²g²)), in particular m≫j^(3/4) even over the whole height interval. If only allocations supported on d+b² change, m divides that factor and the same divisibility retains the lower bound (d+g²)/gcd(d+g²,4d) for ℓ, giving |s|≫X/|g|. If only allocations supported on d+g² change, |s|≫X/b. Consequently fixing the first factor and bad-prime allocations rules out single-factor changes within target blocks of width o(X^(15/16)). This does not rule out mixed changes between the two factors.

The following independent control has actual labels (4,3),(3,4), true integer seeds, and a 563-bit deficit j exceeding seven eighths of the geometric angular cap scale. The same oriented difference admits a rational conic point that still passes the angle and ordinary-height tests with 1<s<2, but has 0<ℓ<1. It is not a second integer point. No global shell-count estimate is asserted in this note; use of a polynomial sieve would still require checking its arithmetic weight hypotheses and degeneracies.

~~~python
from fractions import Fraction as F
from math import isqrt, prod

K, X = 301, 1 << 301
u, a = 828928256542149812983540043167074401999330, 3411
x = a*u + 9**3+2*25**4-(a*a+1)//2
n = x*x+u*u+3*9**3+5*25**4

def cert(r,s,P,Q):
    A,B = 9**r,25**s
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    a,b = P
    c,f = Q
    h = a*f-b*c
    assert (a-c)%2 and (b-f)%2 and h%2==0
    q = ((a-c+b-f)//2)**2+((a-c-b+f)//2)**2
    assert 196*X<=100*n<200*X and A<=B and B**16<=n<=A**32
    assert a*a+b*b==S and c*c+f*f==S+2*D
    assert q%2 and 2*q*S==(D-q)**2+h*h and X<=S<2*X
    assert 64*K*K*q<S<64*K*(K+1)*q
    return U,D,(n-U-q,abs(h)),q

P = (2698115859994096559547095681235316801185026742,
     845447996369883676206443633193679268818732588)
Q = (2698611898993095184751390925053140197778235579,
     843863334391543961275303183778626961636017633)
U,D,(a,b),q = cert(4,3,P,Q)
V,E,(c,f),qq = cert(3,4,(x,u),(x+1,3411-u))
assert q!=qq
e,B,G = V-U,D+E,E-D
L = (n-U)*(n-V)-(D*D+E*E)//2
j,h = L-a*c-b*f,a*f-b*c
d,du,dv = 2*j,a-c,b-f
C = du*du+dv*dv
xx,yy = d*(2*n-U-V)-e*B*G,2*h
R = prod(d+t*t for t in (e,B,G))
assert C==d+e*e and xx*xx-d*yy*yy==R

l,r = F(1,64*K*(K+1)),F(1,64*K*K)
v,T = l*(2-l)*r*(2-r),1<<128
root = isqrt(v.numerator*T*T//v.denominator)
upper = 4*X*X*(1-(1-l)*(1-r)-F(root,T))
assert 7*upper<8*j<8*(upper-F(4*X*X,T))

t = 1+F(3*R,2*xx*yy**2)
Y = yy+2*yy*(1-t)*xx**2/(t*t*d*yy**2-xx**2)
Z = xx+t*F(d*yy,xx)*(Y-yy)
H = (Z+e*B*G)/d
nn = (H+U+V)/2
s = nn-n
assert Z*Z-d*Y*Y==R and 1<s<2 and nn.denominator>1 and nn<2*X
v,h1 = (e*H+B*G+C)/2,Y/2
x1,y1 = (v*du-h1*dv)/C,(v*dv+h1*du)/C
for r,k,A0,D0,a0,b0 in ((4,3,U,D,x1,y1),(3,4,V,E,x1-du,y1-dv)):
    S,Q = nn-A0-D0,nn-A0-a0
    assert 25**(16*k)<=nn<=9**(32*r) and X<=S<2*X
    assert b0>0 and a0*a0+b0*b0==S*(S+2*D0)
    assert 2*Q*S==(D0-Q)**2+b0*b0 and 64*K*K*Q<S<64*K*(K+1)*Q
ell = (x1-a)**2+(y1-b)**2-s*s
assert du*(x1-a)+dv*(y1-b)==e*s
assert 0<ell<1 and (d+B*B)*(d+G*G)*((Z*xx-d*Y*yy)/R-1)==2*d*ell
print("Native high shell and rational projection control verified")
~~~
