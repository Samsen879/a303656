# A shared half-root test for partial factor allocations in P2

Take the four shifts of [the P2 local cover](FOURTH_SQUARE_COMPLETE_LOCAL_COVER.md), with \(d=(S_1-S_0)/4,\ e=(S_2-S_0)/4,\ f=(S_3-S_0)/4\). In the integer half-root branch put \(R,Y,H,J\) for the positive half-roots, \(u=R+Y,\ v=R-Y\); thus \(uv=d\) and \(u+v=2R\).

For a block prime \(p^m\Vert d\) with at least one nonsplit character \((59/p),(3414/p)\), the [whole-power rule](P2_WHOLE_POWER_ALLOCATION.md) assigns \(p^m\) entirely to one side. The two single-root characters must use the same side: they form either \(((59/p),(3414/p))\) when it goes into \(u\) or \((1,1)\) when it goes into \(v\). Picking an allowed character independently from each projection may give a pair that cannot occur for any single \(R,Y,H,J\).

A bound \(K\in(K_{\min},K_{\max}]\), above all shifts, puts \(v\) in a specific interval \(I\), via
\[
 v=\big(\sqrt{K-S_0}-\sqrt{K-S_1}\big)/2 .
\]
Given authenticated, disjoint whole powers assigned to \(u\) and \(v\), with products \(P\) and \(Q\), put \(N=d/(PQ)\). Any solution has \(v=Qz\in I,\ u=P(N/z)\) for some \(z\mid N\). At each prime power \(p^m\mid P\), test **both** \(w^2-4e\) and \(w^2-4f\) for being squares modulo \(p^m\) with the same \(w=Qz\); at \(p^m\mid Q\) do the same with \(w=P(N/z)\). This follows by reducing \(2R=u+v\) and using \(4H^2=(2R)^2-4e,\ 4J^2=(2R)^2-4f\). In the second test \(z\) is a unit modulo \(p^m\). If the compatible CRT classes for every assignment are disjoint from the possible \(z\)-interval, that is an exclusion certificate for the window, even without factoring \(N\). This is only a necessary filter on survivors.

The explicit example below uses a balanced, locally admissible exponent class and finds depth one at the double-split prime 67 and depth two at the double-nonsplit prime 727 in the same first cyclotomic block. At 727 the two isolated-root local tests accept 364 nonzero values of \(R\) each, but only 178 are common. At \(R=1\) one cannot splice \((+,-)\) from the two branches \(Y=1\) and \(Y=-1\). The ordinary integer \(K=S_3+\mathrm{offset}\) in the replay passes all four square tests at the ten listed primes and lies below \(729A+625B\) (the offset is smaller than \(624B\)), yet its fourth residual is not a square. This does not certify that any other \(K\) fails.

~~~python
from fractions import Fraction as F
from math import isqrt
a,b=182986688501791627983199859542,124907847079800385175916116884
assert (a%720,b%720)==(22,4)
assert (a-1)%(29*11)==(b+2)%(29*11)==0
def logint(k,N=260):
 t=F(k-1,k+1); lo=2*sum(t**(2*i+1)/(2*i+1) for i in range(N))
 return lo,lo+2*t**(2*N+1)/((2*N+1)*(1-t*t))
l3,u3=logint(3);l5,u5=logint(5)
assert -F(1,25)<b*l5-a*u3<=b*u5-a*l3<F(1,25)
def val(n,p):
 assert n
 d=0
 while n%p==0:d+=1;n//=p
 return d
for p,d,u,v in [(67,1,1,1),(727,2,726,726)]:
 m=p**4
 U,V=pow(3,(a-1)//11,m),pow(5,(b+2)//11,m)
 T=sum((-1)**k*U**(10-k)*V**k for k in range(11))%m
 assert val(T,p)==d
 assert (pow(59,(p-1)//2,p),pow(3414,(p-1)//2,p))==(u,v)
p=727
A,B=pow(3,a,p),pow(5,b,p)
e,f=(20*A+25*B)%p,(182*A-6*B)%p
qr={i*i%p for i in range(p)}
U={r for r in range(1,p) if (r*r-e)%p in qr}
V={r for r in range(1,p) if (r*r-f)%p in qr}
assert tuple(map(len,(U,V,U&V)))==(364,364,178)
assert 125**2%p==(1-e)%p and 73**2%p==(1-f)%p
for y,want in [(1,1),(-1,726)]:
 assert all(pow((1+h)*(y+h)%p,(p-1)//2,p)==want for h in (125,73))
offset=622735459764237203580003844
assert isqrt(offset)==24954668095653 and 24954668095653**2<offset
for p in (2,3,5,7,11,13,17,19,61,727):
 m=p**8
 A,B=pow(3,a,m),pow(5,b,m)
 shifts=[(9**i*A+5**e*B)%m for i,e in enumerate((2,4,3,0))]
 K=shifts[-1]+offset
 for s in shifts:
  w=(K-s)%m; d=val(w,p); assert d%2==0
  u=w//p**d
  assert (u%8==1 if p==2 else pow(u,(p-1)//2,p)==1),(p,d,u)
print('balanced, two factor depths, shared-root characters and all 40 local square checks verified')

~~~
