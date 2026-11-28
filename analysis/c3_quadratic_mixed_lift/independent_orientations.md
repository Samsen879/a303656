# Independent orientations at the same mixed-edge target

This supplements [the quadratic lift](README.md) without changing the integer or the three power labels. It gives a uniform obstruction for *complete* base-6 axes at the original first endpoint, and a separate exact finite statement for the four factors in the certified example.

## An axis on which both conjugate directions fail

Use the notation \(F_1(I)=h^2+20E-100+20(h+10)I\) from the lift. For \(\pi_j=6^{2j+1}+(-1)^ji\), the two conjugate divisor directions give \(I=\pm(-1)^j6^{2j+1}\) modulo an odd prime \(p\) dividing \(N(\pi_j)\). A nonsquare \(F_1(I)\) rules out the entire oriented divisor, regardless of the parameter \(y\).

For an obstructing row \((p,j)\), put \(s=2j+1\). At every index \(j+sk\) the value of \(I\) is unchanged for the given sign: both the alternating sign and the power of 6 contribute \((-1)^k\). So at any fixed \(L\), one positive-direction obstruction of period \(s_+\) and one negative-direction obstruction of period \(s_-\) meet at \((m-1)/2\) modulo \(m=\operatorname{lcm}(s_+,s_-)\). The exact enumeration below of all \(L\bmod2160\) gives the smallest paired periods 3, 9, 15, 27 with multiplicities 1230, 570, 300, 60, respectively. Therefore the first 14 axes (indices 0 through 13) always contain a completely unavailable axis, and so does every block of 27 consecutive axes. A unit does not change divisibility; conjugating the whole original endpoint swaps the two signs. Deleting axes, or using a proper factor of an unavailable full axis, is not excluded.

## Exact finite rotation family at one certified target

Use the first certified \(L=12,K=1080\) target in the progression. The four given Gaussian divisors have distinct prime norms; each divides only its original endpoint, with valuation one and in only one orientation. At this fixed target, keep the anchor and two endpoint norms and allow independent unit multiplication or conjugation of their coordinates, and switching any subset of the two listed factors of each endpoint. Modulo an isometry common to the anchor and the relevant endpoint, this leaves at most 32 variants per edge: four subsets and eight relative isometries. Conjugating an input before switching factors exchanges their directions and is covered by conjugating the output of the corresponding subset.

For a candidate endpoint \(UQ_j\), where \(U\) is the combined isometry, let \(q=|UQ_j-P|^2/2\), \(S=|P|^2\), and \(V=(-3,1)\). The identity \(q=S+D_j-\langle P,UQ_j\rangle\), with \(D_j=(D,E)_j\), gives
\[
  \left|\frac qS-\left(1-\frac{\langle V,UV\rangle}{10}\right)\right|
  \le \frac{D_j}{S}+\frac{4h+|Q_j-P|}{\sqrt S}<2^{-260}.
\]
Indeed \(P=tV+(h,0)\) with \(t>0\), so the norm distance between its unit direction and that of \(V\) is at most \(2h/\sqrt S\). Replacing both unit vectors in the inner product costs at most \(4h/\sqrt S\). Replacing \(UQ_j\) by \(UP\) costs at most \(|Q_j-P|/\sqrt S\). The replay bounds the right-hand side by exact rational numbers. Only the two single-factor switches with identity relative isometry enter the critical band; exact coordinates verify primitivity and even determinant there. There are precisely two distinct certified \(q\) values per edge, four in total, and four ordered pairs obtainable with the anchor fixed. This is not a bound for other Gaussian factors, other initial endpoints, or arbitrary targets.

## Exact replay

Run this standalone Python 3.9+ block. Expected output: the paired-period counts and “two per edge, four distinct q”.

```python
from collections import Counter
from fractions import Fraction as F
from math import gcd, isqrt, lcm, prod

plus = [(13,1),(97,1),(73,4),(109,13)]
minus = [(13,1),(37,0),(73,4),(61,7),(181,7),(241,2)]
def prime(p): return p > 1 and all(p%d for d in range(2,isqrt(p)+1))
def bad(L,p,j,sign):
    a,b = pow(9,L,p),pow(25,L,p)
    h = 12*b-3*a-5
    I = sign*(-1)**j*pow(6,2*j+1,p)
    return pow(h*h+20*(a+10*b)-100+20*(h+10)*I,(p-1)//2,p)==p-1

for p,j in plus+minus:
    assert prime(p) and pow(9,2160,p)==pow(25,2160,p)==1
    assert pow(6,4*j+2,p)==p-1
cnt = Counter(min(lcm(2*j+1,2*k+1)
                  for p,j in plus for r,k in minus
                  if bad(L,p,j,1) and bad(L,r,k,-1))
              for L in range(2160))
assert cnt == {3:1230,9:570,15:300,27:60}
print(dict(sorted(cnt.items())))

def N(z): return sum(x*x for x in z)
def mul(z,w):
    x,y=z
    a,b=w
    return x*a-y*b,x*b+y*a
def iso(z,c,k):
    return mul((z[0],(-1)**c*z[1]),((1,0),(0,1),(-1,0),(0,-1))[k])

A,B,Y,K=9**12,25**12,2**270,1080
H,D,E=3*A+25*B,12*B-3*A,A+10*B
h=D-5
packs=[[(12224,1,69449792),(73339,6,2702964291)],
       [(48889,4,1366406856),(61122,5,2021034347)]]
cs=[(0,2),((3*h-E)*pow(h,-1,5),5)]
cs += [(r,m*m+b*b) for pack in packs for m,b,r in pack]
M=prod(p for _,p in cs)
r=sum(a*(M//p)*pow(M//p,-1,p) for a,p in cs)%M
lo=13*Y//16
y=lo+(r-lo)%M
t,rem=divmod(5*y*y-h*y+5+3*h-E,10)
assert rem==0 and lo<=y<7*Y//8
P=(h-3*t,t)
S=N(P)
n=H+S
Qs=[(P[0]+1,P[1]+3),(P[0]+3-y,P[1]-1-3*y)]
assert [N(z) for z in Qs]==[n-9*A-B,n-A-5*B]
assert 2**K<=S<2**(K+1) and (25*B)**16<=n<=A**32

eps=F(1,2**260)
low,high=F(1,64*K*(K+1)),F(1,64*K*K)
assert F(max(D,E),2**K)+F(4*h+4*Y,2**540)<eps
v=(-3,1)
tot=set()
for j,(Q,pack) in enumerate(zip(Qs,packs)):
    axes=[]
    for m,b,_ in pack:
        p=m*m+b*b
        assert prime(p) and N(Q)%p==0 and N(Q)%(p*p)!=0
        assert N(P)%p and N(Qs[1-j])%p
        assert all(x%p==0 for x in mul(Q,(m,b)))
        assert any(x%p for x in mul(Q,(m,-b)))
        axes.append((F(m*m-b*b,p),F(2*m*b,p)))
    got=set()
    for mask,G in enumerate([(1,0),*axes,mul(*axes)]):
        for c in range(2):
            for k in range(4):
                a,b=iso(mul(G,v),c,k)
                ideal=1-(v[0]*a+v[1]*b)/10
                if (mask,c,k) in ((1,0,0),(2,0,0)):
                    assert low+eps<ideal<high-eps
                else:
                    assert ideal<low-eps or ideal>high+eps
                R=iso(mul(G,Q),c,k)
                assert all(x.denominator==1 for x in R)
                x,z=int(R[0])-P[0],int(R[1])-P[1]
                q=F(x*x+z*z,2)
                w=x*P[1]-z*P[0]
                if low<q/S<high:
                    assert x%2==z%2==1 and gcd(x,z)==1 and w%2==0
                    assert 2*q*S==((D,E)[j]-q)**2+w*w
                    got.add(q)
    assert len(got)==2
    tot.update(got)
assert len(tot)==4
print("two per edge, four distinct q")

```
