# Exact Gaussian Gram factors for two numerical seeds

For any two actual seed pairs of the critical t=8 band, choose Gaussian integers P_i,Q_i with |P_i|²=S_i, |Q_i|²=S_i+2D_i. Their dot product is n−U_i−q_i, so z_i=conjugate(P_i)Q_i, after conjugating P_i and Q_i together if needed to select the orientation of the actual imaginary part. Let e=U₂−U₁ and put d=|z₁−z₂|²−e², b=D₁+D₂, g=D₂−D₁. Two separate Gaussian norms are then furnished by the original seed coordinates:

~~~text
d+b² = N(conjugate(P₁) P₂ − conjugate(Q₁) Q₂)
d+g² = N(conjugate(P₁) conjugate(Q₂) − conjugate(Q₁) conjugate(P₂)).
~~~

In each expansion the cross term is 2 Re(z₁ conjugate(z₂)); the pure terms are respectively 2((n−U₁)(n−U₂)+D₁D₂) and 2((n−U₁)(n−U₂)−D₁D₂). This proves both identities exactly, with no nondegeneracy or local-density assumptions. Therefore each positive Gram factor separately satisfies the even-valuation rule for every Gaussian inert prime. In addition, at an odd prime p outside bg that divides one of these factors, d is −b² or −g² modulo p. If p is Gaussian inert, d is a nonsquare there, so that prime cannot introduce real quadratic split-prime allocation choices. This explains why the small prime norm indicators used in the proposed sieve are arithmetically valid, without asserting the whole joint-shell bound.

## Exact integer replay

The earlier native high-shell example gives both certificates directly. Use pairs from the numerical seeds, conjugating both Gaussian inputs for a label whenever their imaginary cross term is negative.

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


def conj(t):
    return (t[0],-t[1])

def mul(t,s):
    return (t[0]*s[0]-t[1]*s[1],t[0]*s[1]+t[1]*s[0])

def diff(t,s):
    return t[0]-s[0],t[1]-s[1]

def norm(t):
    return t[0]**2+t[1]**2

def orient(P,Q):
    v=mul(conj(P),Q)
    return (P,Q) if v[1]>=0 else (conj(P),conj(Q))

P1,Q1=orient(P,Q)
P2,Q2=orient((x,u),(x+1,3411-u))
assert mul(conj(P1),Q1)==(a,b)
assert mul(conj(P2),Q2)==(c,f)
assert norm(diff(mul(conj(P1),P2),mul(conj(Q1),Q2)))==d+B*B
assert norm(diff(mul(conj(P1),conj(Q2)),mul(conj(Q1),conj(P2))))==d+G*G
~~~
