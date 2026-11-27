# Integral Gaussian refactor counts, bad-prime moments, and unbounded native content

This follows [the second-marker pin and rational flexibility](https://github.com/Samsen879/a303656/commit/1cd7964887a409cf1935801e54644892daca7646). The pointwise integral count is exact, and the additional weight is charged to bad primes of the already proved angular boxes. This is not a saving in the global number of different integral targets. To distinguish pointwise from average, two independently constructed depths of the cofinal 113 family are replayed below.

For a common rotation \(\rho=\eta/\gamma\) in lowest Gaussian terms, the Gaussian norm \(N(\gamma)\), i.e. its squared complex absolute value, divides the gcd of the two endpoint norms. In fact \(\gamma\) must divide both endpoints. Each local interval of allowed split exponents can be realized independently by a product of \(\pi/\bar\pi\) powers, and norm-one Gaussian units contribute no extra choice modulo units. The moving-prime charge holds because \(N(G)\) divides \(\bar ac\) as a rational Gaussian divisor. Substituting \(n-U_i\equiv D_i\equiv z_i\equiv0\bmod p^m\) into \(N(z_1-z_2)\) puts that same valuation depth in both other Gram factors. It therefore changes only the fixed bad-prime polynomial weight.

For a fixed native seed, the number of integral endpoint factorizations modulo common Gaussian units is **exactly**
\[
\boxed{\mathcal A(z)=\prod_{p=\pi\bar\pi\ {\rm split}}
       \bigl(1+v_\pi(G)+v_{\bar\pi}(G)\bigr),\qquad G=\gcd_{\mathbb Z[i]}(a,c).}
\]
Every integral refactorization preserves the second and third Pell allocations at good primes. The count has bounded moments in the existing angular-shell estimate, but it is unbounded pointwise. A cofinal one-label construction below gives \(\mathcal A(z)\gg\log\log X\).

### Integral rotation restriction

Fix \(z=\bar a c\), with \(N(a)=S\) and \(N(c)=S+2D\). Every other endpoint factorization has the form \((\rho a,\rho c)\) with \(\rho\in\mathbb Q(i)\) and \(N(\rho)=1\). At a split prime its rotation exponent \(t=v_\pi(\rho)=-v_{\bar\pi}(\rho)\) can be any integer in
\[
[-v_\pi(G),\,v_{\bar\pi}(G)].
\]
The choices are independent across primes. Inert and ramified primes have rotation exponent zero. This gives the exact count, and the Gaussian norm of the reduced denominator of \(\rho\) divides \(\gcd(S,S+2D)\). In particular, \(\mathcal A(z)\) is at most the divisor count of the split part of \(D\).

For two fixed seeds, write \(m_{i,p}=v_\pi(G_i)+v_{\bar\pi}(G_i)\). The second marker \(W_b=a_1\bar a_2-c_1\bar c_2\) transforms by \(\rho_1\bar\rho_2\). Its number of integral values modulo units is exactly \(\prod_p(1+m_{1,p}+m_{2,p})\), by subtracting the two exponent intervals. Every prime in this product divides \(D_1D_2\). Hence the marker can rotate while its allocation at each good prime stays fixed.

There is also a restriction at the moving bad primes. If \(m=m_{i,p}>0\), then \(p^m\mid D_i,n-U_i\), and \(p^m\mid z_i\) as a rational Gaussian divisor. Set \(d=2j\), \(e=U_2-U_1\), \(b=D_1+D_2\), and \(g=D_2-D_1\). Since \(N(z_1-z_2)=d+e^2\), reduction modulo \(p^m\) gives
\[
p^m\mid d+b^2,\qquad p^m\mid d+g^2 .
\]
Thus all the endpoint multiplicities can be charged to the bad-prime powers of the existing Gram factors. In the earlier angular-box proof this changes only the fixed polynomial bounds at primes dividing \(4D_1D_2=b^2-g^2\). The good-prime Euler factors and the bounded mean of the bad-prime factors are unchanged in order. Consequently, for each fixed \(t>0\),
\[
\sum_{\substack{\text{native seed pairs}\\J<j\le2J}}
(\mathcal A(z_1)\mathcal A(z_2))^t\ll_t K^2J,
\qquad X^{1/3}\le J\ll X^2/K^4,\quad X=2^K .
\]
This controls integral refactoring multiplicity in the large-\(j\) range. It does not select the good-prime allocation across different seeds or improve the full diagonal bound. [De la Bretèche and Tenenbaum, Theorem 3.1](https://tenenb.perso.math.cnrs.fr/PPP/NTpols.pdf).

### Unbounded native multiplicity

Take \(p=113\). The exact starting data are \(113\mid 9^3+2\cdot25^3\) and \(9^{56}\equiv1+4p\bmod p^2\). For each depth \(\ell\), lift \(r=3+56u\) one digit at a time to obtain \(9^r+2\cdot25^3\equiv0\bmod p^\ell\). The derivative in the next digit is \(4\cdot9^r\bmod p\), a unit. Now put \(P=112p^{\ell-1}\), choose that \(r\) in \([2P,5P/2)\), and choose \(s\equiv3\bmod P\) nearest \(r\). This preserves \(p^\ell\mid D=9^r+2\cdot25^s\). With \(K=96r\), the ordinary gates hold throughout \([2^K,2^{K+1})\).

Choose an odd slope \(a_0\) with
\[
K^2+K/8\le(a_0^2+1)/128\le K^2+7K/8,\qquad a_0\not\equiv\pm15\bmod113.
\]
For an integer \(u_0\asymp 2^{K/2}/a_0\), use the endpoints
\[
(x,u_0),\quad (x+1,a_0-u_0),\qquad x=a_0u_0+D-(a_0^2+1)/2.
\]
Their squared norms differ by \(2D\). The numerical seed is \(q=((2u_0-a_0)^2+1)/2\), an odd Gaussian norm, and \(S/(64q)=(a_0^2+1)/128+o(1)\). Taking \(a_0u_0/2^{K/2}\) between \(9/8\) and \(5/4\) puts both \(S\) and the target in the required dyadic bin.

Lift \(i_0=15\bmod113\) to a root of \(-1\) modulo \(113^{\ell+1}\), and impose \(2u_0\equiv a_0-i_0\bmod113^\ell\). Both endpoints then vanish in that split component to depth \(\ell\). Their next-digit slopes are \(a_0+i_0\) and \(a_0-i_0\), both units. Avoiding at most two next digits makes both depths exactly \(\ell\), with the conjugate component a unit. Thus the \(113\)-part of the count is exactly \(\ell+1\). Since \(K\asymp113^{\ell-1}\), this gives the claimed lower bound. I replayed depths one and two at \(K=21{,}792\) and \(2{,}527{,}008\). This family supplies one true label per target. The two-label control follows.


## Independent native replay

The integral rotation keeps the allocation at 353 unchanged. An exact opposite-allocation rational example has already been independently constructed and linked above; this replay does not count it as an integral refactorization.

```python
from fractions import Fraction as F
from math import gcd, prod

K, X = 300, 1 << 300
a, u = 3395, 473185169285762983115008677420232836904800
x = a*u + 9**3 + 2*25**3 - (a*a+1)//2
n = x*x + u*u + 3*9**3 + 5*25**3

def N(z): return z[0]**2 + z[1]**2
def bar(z): return z[0], -z[1]
def sub(z,w): return z[0]-w[0], z[1]-w[1]
def mul(z,w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]

def cert(r,s,A0,C0):
    A,B = 9**r,25**s
    U,D = 2*A+3*B,A+2*B
    S = n-U-D
    f,g = sub(A0,C0)
    assert X<=n<2*X and A<=B and B**16<=n<=A**32
    assert N(A0)==S and N(C0)==S+2*D and f%2 and g%2
    q = ((f+g)//2)**2+((f-g)//2)**2
    z = mul(bar(A0),C0)
    if z[1]<0: A0,C0,z = bar(A0),bar(C0),bar(z)
    assert q%2 and z[1]%2==0 and z[0]==n-U-q
    assert 2*q*S==(D-q)**2+z[1]**2 and X<=S<2*X
    assert 64*K*K*q<S<64*K*(K+1)*q
    return A0,C0,z,U,D,q

p1 = (1178057198258375364927876802975536556234008052,
      1092202783105834238850010565585469156261930366)
p2 = (1177413431472334130986096524428684574884890859,
      1092896744061874424278275940778049409811653201)
a1,c1,z,U,D,q = cert(3,3,(x,u),(x+1,a-u))
a2,c2,w,V,E,qq = cert(4,4,p1,p2)
assert q!=qq and gcd(N(a1),N(c1))==226 and gcd(N(a2),N(c2))==2

e,b,g = V-U,D+E,E-D
H,L = 2*n-U-V,(n-U)*(n-V)-(D*D+E*E)//2
dot,h = mul(bar(z),w)
j,delta = L-dot,sub(z,w)
d,C,W = 2*j,N(delta),e*b*g
xx,yy = d*H-W,2*h
R = prod(d+l*l for l in (e,b,g))
assert j**5>X**9 and 0<h*h*K**4<N(z)*N(w)
assert C==d+e*e and xx*xx-d*yy*yy==R

def rotate(v):
    t = mul((-15,-112),v)
    assert all(a%113==0 for a in t)
    return tuple(a//113 for a in t)

aa,cc = rotate(a1),rotate(c1)
assert (N(aa),N(cc),mul(bar(aa),cc))==(N(a1),N(c1),z)
p,i = 353,42
bad = 2*W*(e*e-b*b)*(e*e-g*g)*(b*b-g*g)
assert (i*i+1)%p==0 and bad%p and C%p and R%p==0 and R%p**2
for A0,C0 in ((a1,c1),(aa,cc)):
    P = mul(A0,bar(a2))
    B0 = sub(P,mul(C0,bar(c2)))
    assert N(B0)==d+b*b
    vals = [(xx-yy*b*t)%p for t in (i,-i)]
    assert vals == [2*b*(B0[0]-t*B0[1])*(P[0]+t*P[1])%p
                    for t in (i,-i)] == [0,258]


# Independent cofinal construction, at two depths.
from math import isqrt
def at_depth(k):
    p=113
    r=3
    for j in range(1,k):
        m=p**(j+1)
        r+=56*p**(j-1)*next(t for t in range(p)
                           if (pow(9,r+56*p**(j-1)*t,m)+2*25**3)%m==0)
    P=112*p**(k-1)
    T=P//2
    r=2*P+(r-2*P)%T
    s=3+P*((r-3+P//2)//P)
    K=96*r
    L=128*K*K+16*K-1
    a=isqrt(L)
    if a*a<L: a+=1
    if a%2==0: a+=1
    while a%p in (15,p-15): a+=2
    assert a*a+1<=128*K*K+112*K
    i=15
    for j in range(1,k+1):
        i+=p**j*next(t for t in range(p) if ((i+p**j*t)**2+1)%p**(j+1)==0)
    P1,P2=p**k,p**(k+1)
    r0=(a-i)*pow(2,-1,P1)%P1
    D0=(pow(9,r,P2)+2*pow(25,s,P2))%P2
    res=next(z for z in range(r0,r0+P2,P1)
             if ((a+i)*z+D0-(a*a+1)//2)%P2
             and ((a-i)*z+D0-(a*a+1)//2+1+i*a)%P2)
    lo=(9*2**(K//2)+8*a-1)//(8*a)
    u=lo+(res-lo)%P2
    A,B=9**r,25**s
    D=A+2*B
    x=a*u+D-(a*a+1)//2
    S=x*x+u*u
    n=S+3*A+5*B
    q=((2*u-a)**2+1)//2
    assert A<=B and B**16<=n<=A**32 and n.bit_length()==S.bit_length()==K+1
    assert 64*K*K*q<S<64*K*(K+1)*q and q%2
    assert (x+1)**2+(a-u)**2==S+2*D and D%P1==0
    z,w=(x+i*u)%P2,(x+1+i*(a-u))%P2
    assert z and w and z%P1==w%P1==0
    assert (x-i*u)%p and (x+1-i*(a-u))%p
    return K
assert [at_depth(k) for k in (1,2)]==[21792,2527008]
```
