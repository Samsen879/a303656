# A new true common-target K671 double chord, and reconstruction without a direction search

For actual first-label norms S=n−H,R=S+2D, a signed integer Gaussian coordinate pair Z with N(Z)=SR supplies a direct interface. If both norms are positive even, D is odd, and gcd(S,D)=1, take
```
g = gcd_Z[i](Z,S)/(1+i),  P = conjugate(g),  Q = Z/g.
```
The gcd has norm 2S: at odd p the two rational endpoint norms are coprime, so the full p-adic contribution to S is precisely extracted from Z. At the ramified prime 1+i one endpoint is 2 modulo 4 and the other 0, hence this gcd extracts v_2(S)+1 powers of 1+i. Thus the quotient is integral, N(P)=S, N(Q)=R. Their actual difference has both coordinates odd; its half squared norm is q=S+D−Re Z. It is primitive iff gcd(q,D)=1: for an odd p dividing q and D, the norm identity forces Z≡S modulo p and g is a unit there, so the displacement vanishes modulo p. Conversely a common displacement divisor divides q and D. Check the original strict window on q.

A direction-specific alternative uses Δ=d+i a and e=N(Δ)/2. One requires an actual signed integer Y with Y²=SR−(e−S−D)² and Δ|D−e+iY in Z[i]. Then P=(D−e+iY)/Δ and Q=conjugate(P)+Δ have the desired endpoint norms. In this alternative Δ is the conjugate-cross difference; the actual displacement Q−P still must be checked. This is equivalent to the coordinates, not an assertion that a local square suffices.

The exact new 672-bit example has three genuine second chords at the actual (8,7),(7,8) label pair and one genuine primitive first chord whose smaller displacement coordinate is 323 bits. Both reconstructions are replayed. Another target in the same progression and height has the same three genuine second constructions but v_7(n−H)=1, preventing **all** first-label directions as the lower norm cannot be a sum of two squares. This is an exact new same-target positive and a full-direction negative control. It does not establish growing simultaneous success, arbitrary n, or anything about the full-direction status of the previous K5684 target.

```python
from math import gcd, lcm

L,K = 7,671
A,B = 9**L,25**L
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
ms = (7592,7594,7596)
t = 79186934766042045095929803573073104476777060604159795000641641588139114268924441178860030070538531575
P = (44431203582073559282494574809832918293984662102542474582518318621124282161821021916287391661118156350,
    -102795960151803292317648126601409819709413677981069550595950114807445277622604722731580554168269201516)
Q = (44404131936308723490377453276856351802501036674815895158077617651899081800748832297785227943339691253,
    -102807657021574440378638433005380974661597798592021324296397639839177576805982968758041358322577020383)

def N(z): return z[0]**2+z[1]**2
def bar(z): return z[0],-z[1]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]

def div(z,w):
    a,b = mul(z,bar(w))
    m = N(w)
    assert a%m==b%m==0
    return a//m,b//m

def ggcd(z,w):
    while w != (0,0):
        m = N(w)
        a,b = mul(z,bar(w))
        u = mul(w,((a+m//2)//m,(b+m//2)//m))
        z,w = w,(z[0]-u[0],z[1]-u[1])
    return z

def check(n,P,Q,H,D):
    S = n-H
    assert 25**128 <= n <= 9**224 and 2**K <= S < 2**(K+1)
    assert N(P)==S and N(Q)==S+2*D
    d,w = Q[0]-P[0],Q[1]-P[1]
    h = d*P[1]-w*P[0]
    q = (d*d+w*w)//2
    assert d%2 and w%2 and gcd(d,w)==1 and h%2==0
    assert 2*q*S==(D-q)**2+h*h and 64*K*K*q<S<64*K*(K+1)*q
    return q

def second(t):
    n = 2*(t*t+c*c)+J
    qs = set()
    for m in ms:
        v,r = divmod(t+m*(c+1),m*m+1)
        assert r==0
        f,g = (m*m-1)*v-m*(c+1),2*m*v-c-1
        qs.add(check(n,(t-c,t+c),(f-g,f+g),J,E))
    assert len(qs)==3
    return n

n = second(t)
S = n-H
q = check(n,P,Q,H,D)
assert n.bit_length()==672 and gcd(S,D)==gcd(q,D)==1
assert min(abs(Q[j]-P[j]) for j in (0,1)).bit_length()==323
Z = mul(bar(P),Q)
assert N(Z)==S*(S+2*D) and q==S+D-Z[0]
g = div(ggcd(Z,(S,0)),(1,1))
assert check(n,bar(g),div(Z,g),H,D)==q
d,a = Q[0]-P[0],Q[1]+P[1]
e = (d*d+a*a)//2
Y = mul(P,Q)[1]
assert Y*Y==S*(S+2*D)-(e-S-D)**2
assert div((D-e,Y),(d,a))==P

n_bad = second(t+4*lcm(*(m*m+1 for m in ms)))
assert n_bad.bit_length()==672 and (n_bad-H)%49==21
print("verified", K, (n_bad-H)%49)
```
