# Same endpoint gcd matrix, opposite second-label outcomes

For actual labels A=9^(T+3), B=25^(T+3), let S1=n−(27A+5B), R1=n−(9A+B), S2=n−(3A+125B), R2=n−(A+25B). The four differences first endpoint minus second endpoint, in that order of rows and columns, are
```
[ 24(5B−A),   20B−26A ]
[ 124B−6A,     8(3B−A) ]
```
An original integer gcd is expressible via that difference. In particular the gcd of the two diagonal differences is 48: after extracting 8, any common odd prime must divide 3, since A and B are coprime, and the first difference has exact 3-adic valuation 1; the 2-adic valuations are 5 and 4. Thus any common odd split factors used on the two diagonal transfers must come from distinct primes.

If g_S divides the first Gaussian endpoint P1 and g_R divides Q1, a second chord keeping those allocations must have endpoints g_S z, g_R w with N(z)=S2/N(g_S), N(w)=R2/N(g_R), and the original parity, primitivity, and critical-window conditions. Removing a split factor does not change an inert-prime valuation.

The replay checks two actual K=692 targets with **identical** full matrix [[802,2],[2,2704]]. One has a true second primitive critical chord assembled from g_S=(19,21), g_R=(20,48) and exact cofactors. For the other, g_R still transfers and reconstructs a true norm R2, but S2 is 276 modulo 23², so v_23(S2)=1 and it cannot be a two-square norm. The failure occurs before the angular test. In the positive fixture both Gaussian factors have norms equal to the corresponding gcd; the same is true of the transferred R factor in the negative fixture. The K396 and K500 controls also give a genuine second chord despite no shared odd prime. These examples do not classify all angles, construct an unbounded successful double-label family, or establish any arbitrary-target guarantee.

```python
from math import gcd

def N(z): return z[0]**2+z[1]**2
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def bar(z): return z[0],-z[1]
def div(z,w):
    k=N(w); a=mul(z,bar(w))
    assert all(v%k==0 for v in a)
    return tuple(v//k for v in a)
def data(T):
    A,B=9**(T+3),25**(T+3)
    return 27*A+5*B,9*A+B,3*A+125*B,A+25*B
def seed(P,Q,S,R,K):
    d,e=Q[0]-P[0],Q[1]-P[1]
    q=(d*d+e*e)//2
    h=P[0]*Q[1]-P[1]*Q[0]
    assert d%2 and e%2 and gcd(d,e)==1 and h%2==0
    assert N(P)==S and N(Q)==R and 2*q*S==((R-S)//2-q)**2+h*h
    assert 2**K<=S<2**(K+1) and 64*K*K*q<S<64*K*(K+1)*q

def anchor(T,K,a,u,g):
    H,J,H2,J2=data(T)
    D=(H-J)//2; x=a*u+D-(a*a+1)//2
    P=mul(div((x,u),g),bar(g)); Q=(x+1,a-u)
    n=x*x+u*u+H
    assert 25**(16*(T+4))<=n<=9**(32*(T+3))
    assert 64*K*K*(1+(a-2*u)**2)>2*(n-H)
    r,s=g
    assert 400*K*K*r*s>9*N(g) and 400*K*K*s<11*r
    seed(P,Q,n-H,n-J,K)
    S,R=n-H2,n-J2
    return P,Q,S,R,[[gcd(N(p),v) for v in (S,R)] for p in (P,Q)]

for T,K,a,m,u,V,W in [
    (1,396,4479,6272660,
     107631485777229402067141184459932727503114031274994405730,
     (-402027876083264712643034407366633865588710892230259818918608,
       266037776584567469843013189860709784275576321292507200145802),
     (-402146554373700147282217986704201478331699512354938718599599,
       265858346725171887405552333993217862639834692105443252076883)),
    (2,500,5655,10000044,
     383926026185211066579832133483647870363756550889720823037289401350858274,
     (-555665752269218079463250868810112072466437126704976976051563694667035033416,
      -2098789702591625386933144891775165171678475697642987232074809988870967114790),
     (-554924397528368768078439618419470379730429580287588640477205764547695341095,
      -2098985840108821775405675712994120271255707649544548238849623031313911542723))
]:
    P,Q,S,R,G=anchor(T,K,a,u,(m,1))
    seed(V,W,S,R,K)
    assert G==[[4,2],[2,2]] and gcd(N(P)*N(Q),S*R)==8

gs,gr=(19,21),(20,48)
for bad,u,r in [
    (False,21971192886866971970018735123723528582244322574908256486687716817273768616531491076289938385186208385,
     (2854186525561869658626979365433357281388535358342838614713375126251636208255746967547984862778133530992,
      1672134630569446518371818448424744811960147784067280159655062908073992262506249946321344576078243929351)),
    (True,21971183573796827611548290605141974780909742520077136890650374911111698562588004360319244846440972801,
     (2956823170088325220297632770641365661112721465514272881971348986053325228376294586014124448172290326617,
      1483105663739587070895034147313146608759851347547473413495962774528389443652352747698557794313702155960))
]:
    P,Q,S,R,G=anchor(5,692,7829,u,(10464643495,548))
    assert G==[[802,2],[2,2704]] and N(gs)==802 and N(gr)==2704
    div(P,gs); div(Q,gr)
    W=mul(gr,r)
    assert N(W)==R
    if bad:
        assert S%529==276 and R%23==4
    else:
        s=(3912679469294950753411730218583498993597338909061349550737332549031640099920579113695453098199297633425,
           4645865803264816085481595569551027930441066410501978924539923428513836955285867786591042592917116594922)
        seed(mul(gs,s),W,S,R,692)

H,J,H2,J2=data(5)
D=(H-J)//2; L=151800
assert gcd(H2-H,J2-J)==48
for p,F,k in [(401,H2-H,218),(13,J2-J,12)]:
    assert F%p==0 and pow(25*pow(9,-1,p*p),L,p*p)==1+k*p
assert all(pow(x,L,m)==1 for x in (9,25) for m in (64,529))
def S(a,u): return (a*u+D-(a*a+1)//2)**2+u*u
assert (S(1,19)-(H2-H))%529==437
assert S(21,1)%4==2 and (S(21,1)+2*D)%64==32
assert D%401==343 and D%13==3
print("PASS")
```
