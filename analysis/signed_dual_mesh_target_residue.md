# A permanent target residue for the signed two-mesh construction

**The two full endpoint norms in the signed #101/#106 family cannot be coprime, even after removing their common factor of \(2\).** Every main layer forces both endpoint norms to be divisible by the fixed split primes \(97\) and \(198593\). This also forces every target produced by the construction into one fixed residue class:
\[
\boxed{n\equiv106843006\pmod{154108168}.}
\]
The restriction survives #106’s additional CRT avoidance. [PR #101](https://github.com/Samsen879/a303656/pull/101/files) · [PR #106](https://github.com/Samsen879/a303656/pull/106/files)

### What the construction forces

Write \(T_1=S+2D\) and \(T_2=S+2E\) for the full endpoint norms. Every rotation on an edge preserves its \(T_i\). Since the endpoint coordinates are odd, both norms are \(2\bmod8\) and neither endpoint lies on a coordinate axis. The common \(2\)-part is therefore exactly \(2\). For comparison, #106 gives \(\gcd(S,T_i)=\gcd(S,2D_i)=2\) on each **source-to-endpoint** pair. The obstruction concerns the **endpoint-to-endpoint** pair.

The odd obstruction comes from the forcing moduli. In #101, \(M_i\mid T_i\). If \(R_i\) is the lcm of the initial factor norms on edge \(i\), then \(R_i\mid M_i\), \(R_i\mid A-B\), and \(R_1,R_2\) are coprime. Since
\[
T_1-T_2=24(A-B),
\]
each \(R_i\) divides both endpoint norms. In particular \(2R_1R_2\mid\gcd(T_1,T_2)\). Rotation choices, signs, coordinate swaps, and the #106 adjustment to \(t\) cannot remove these factors.

The primes \(198593=(5^8+3^8)/2\) and \(97\) divide the initial \(e=1\) and \(e=2\) factor norms, respectively. At either prime the two labels coincide with \(28B\). For the main exponent \(s=80\,\operatorname{lcm}(1,3,\ldots,2J+1)\) with \(J\ge128\),
\[
25^s\equiv1\pmod{97},\qquad
25^s\equiv-1\pmod{198593}.
\]
The first follows from \(25^{48}\equiv1\bmod97\) and \(48\mid s\). For the second, \(25^{16\cdot29\cdot107}\equiv-1\bmod198593\), and \(s/(16\cdot29\cdot107)\) is an odd integer. Together with \(n\equiv6\bmod8\), these give the boxed class.

There is no corresponding inert-prime obstruction. If an odd \(p\equiv3\bmod4\) divided both norms, both **unrotated** endpoints would have both coordinates zero modulo \(p\). Their difference is \(\rho(t,3t-2)\), which cannot vanish modulo such a \(p\). This excludes \(3\) as well. The prime \(5\) is excluded directly by \(T_1-T_2=24(A-B)\). The forced split factors concern the *integer norms* and do not imply a common divisor of an endpoint’s two coordinates.

In fact on each layer \(n\equiv28B\pmod{R_1R_2}\); the two displayed primes isolate a fixed modulus valid across all layers. These conditions concern the particular signed forcing schedule, not all possible 3/5 representations at the target.

### Exact replay

The first part checks the roots and both labels at the two fixed primes using the first main layer \(J=128\). The second reconstructs all eight endpoints of the public #101 finite native control; its odd endpoint norms are coprime after removing the two-power.

```python
from math import gcd, isqrt, lcm

s = 80*lcm(*range(1,258,2))  # main layer J=128
for p,e,expected in [(97,2,28),(198593,1,-28)]:
    assert all(p%d for d in range(2,isqrt(p)+1))
    f,g = 5**(20*e),3**(20*e)
    x,y = (f+g)//2,(g-f)//2
    assert (x*x+y*y)%p==0
    I = -x*pow(y,-1,p)%p
    t = (3+I)*pow(5,-1,p)%p
    A,B = pow(9,s,p),pow(25,s,p)
    u = A*(3*t-38)+B*(-15*t*t-147*t+138)
    v = A*(-t+12)+B*(5*t*t+49*t-16)
    for a,b in [(1,3),(t+1,3*t+1)]:
        assert (u+2*B*a+I*(v+2*B*b))%p==0
    n = (A+125*B+(u*u+v*v)*pow(4*B,-1,p))%p
    assert n==expected%p
    assert all(n==(pow(3,c,p)+pow(5,d,p))%p
               for c,d in [(2*s+1,2*s+2),(2*s+3,2*s)])

assert pow(25,48,97)==1
assert pow(25,16*29*107,198593)==198592
assert [106843006%p for p in (8,97,198593)]==[6,28,198565]


# Native small-layer control from the public #101 replay.
from math import comb,gcd,isqrt,prod
s,K=42,4029
A,B=9**s,25**s
H=(A+125*B,3*A+25*B,27*A+B)
D,E=(H[0]-H[1])//2,(H[0]-H[2])//2
# edge, bin, a,b for divisor a-i*b, verified modular root
pack=(
    (1, 0, 4786648, 105, 4166402983095),
    (1, 1, 2233760, 49, 4203548683733),
    (1, 2, 3191071, 70, 268576829947),
    (1, 3, 5424800, 119, 15962826517306),
    (2, 0, 2871850, 63, 2913516008210),
    (2, 1, 2233654, 49, 1937840990991),
    (2, 2, 4786382, 105, 21199354421098),
    (2, 3, 4467275, 98, 12010672491224),
)
r=sum(comb(2*s,j)*2**(2*s-j)*(-1)**(j//2) for j in range(0,2*s+1,2))
v=sum(comb(2*s,j)*2**(2*s-j)*(-1)**((j-1)//2) for j in range(1,2*s,2))
assert r*r+v*v==B
I=r*pow(v,-1,B)%B
mods=[(0,2),(0,abs(D*E)),((38-12*I)*pow(3-I,-1,B)%B,B)]
mods += [(root,a*a+b*b) for _,_,a,b,root in pack]
M=prod(d for _,d in mods)
R=0
for a,d in mods:
    h=M//d
    assert gcd(h,d)==1
    R+=a*h*pow(h,-1,d)
T=isqrt(isqrt((1<<K)//B));lo=(3*T+7)//8;hi=2*T//5
t=lo+(R-lo)%M
assert lo<=t<hi
fx=A*(3*t-38)+B*(-15*t*t-147*t+138)
fy=A*(-t+12)+B*(5*t*t+49*t-16)
assert (r*fx-v*fy)%(2*B)==(v*fx+r*fy)%(2*B)==0
x,y=(r*fx-v*fy)//(2*B),(v*fx+r*fy)//(2*B)
S=x*x+y*y;n=S+H[0]
assert 1<<K<S<1<<(K+1) and B**16<n<A**32 and n%8==6
qs=[]
for edge,j,a,b,root in pack:
    p,q=(1,3) if edge==1 else (t+1,3*t+1)
    ux,uy=r*p-v*q,v*p+r*q
    X,Y=x+ux,y+uy;N=a*a+b*b;c,h=a*a-b*b,2*a*b
    assert gcd(a,b)==1 and (c*X-h*Y)%N==(h*X+c*Y)%N==0
    xx,yy=(c*X-h*Y)//N,(h*X+c*Y)//N
    assert X*X+Y*Y==xx*xx+yy*yy==n-H[edge]>0
    dx,dy=xx-x,yy-y;seed=(dx*dx+dy*dy)//2
    gap=(D,E)[edge-1];det=x*dy-y*dx
    assert dx%2==dy%2==1 and gcd(dx,dy)==1 and det%2==0
    origin=S if gap>0 else S+2*gap
    assert 1<<K<origin<1<<(K+1)
    assert 2*seed*origin==(abs(gap)-seed)**2+det*det
    k=(8 if edge==1 else 20)+j
    assert k*origin<32*(64*K*K*(K+1)*seed-K*origin)<(k+1)*origin
    assert 64*K*(K+1)*((ux*ux+uy*uy)//2)<S # same-n negative control
    qs.append(seed)
assert qs==sorted(set(qs))
print('PASS',n.bit_length(),M.bit_length(),len(qs),[n%1000000007,*[q%1000000007 for q in qs]])
assert gcd(n-H[1],n-H[2])==2
print('PASS signed congruence and exact smaller-layer odd coprimality')
```
