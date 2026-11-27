# A prime-parameter ray forces linear cost for zero-read covers

In the selected chart c≡3 mod 16,d≡1 mod 144, with both exponents in [ceil(H/32),floor(H/4)], use (c,d)=(3t,t) for primes t≡1 mod 720 in [H/32,H/12]. The chosen congruence also keeps c≡3 mod 80. Write S_t=27^t+5^t. If an inert p≥7 with p|n can mark this label, it must divide S_t. The ratio −27/5 then has order exactly t modulo p: order one would force p|32. It follows that the same p cannot mark two different chosen prime parameters and that p≥2t+1. Moreover its order t divides lcm(ord_p(3^16),ord_p(5^144)), because raising the ratio to the 144th power puts it in the joint subgroup, and t is prime to 144. Thus at least one axis has effective order at least t. This applies even when the two axis orders have a large gcd.

In fact S_t/32 is odd, and those integers have pairwise disjoint prime supports as t varies. All such used primes also divide n. A full zero-read cover therefore costs at least the sum of log(2t+1), which is (5/(96 φ(720))+o(1))H by the prime number theorem for fixed arithmetic progressions (natural logs). A zero-read panel with cost o(H) leaves ≫H/log H genuine in-box labels on this ray. This is a necessary condition regardless of how many candidates lift to exact valuation one.

A variant can accommodate any fixed panel of ordinary inert primes and their specified mod-p³ readings. First find a repaired chart anchor (a,b) with valuations zero or two at the fixed panel. Since its individual index periods are fixed, choose positive representatives with larger-to-smaller ratio less than eight. Every t in a suitable fixed nonempty proportional interval then keeps (at,bt) in the original box. Impose t≡1 modulo the relevant fixed group orders and chart periods. Outside the original panel, any exception to order exactly t at a zero-read prime divides the fixed 3^a+5^b; exclude it by extending the target subgroup with n≡3^a+5^b+p² mod p³ and including its orders in the same progression modulus. These new readings are extra conditions on the target, not assertions for every given n. On that nonempty CRT subclass, fixed repaired primes plus o(H) zero-read cost leave a positive asymptotic count of prime parameters. The proof does not control unbounded nonzero-read panels or labels outside the selected chart.

## True matched controls

The first example has two true outputs with the same head and selected phase, and gives 11 versus 5 congruence cells at p=23 for the zero and nonzero reads. On the zero-read target, a change in actual c alters p=23 valuation from exactly one to exactly two. The long-order example uses t=8641 and p=7448543; both effective orders equal 431t, and p hits the prime-parameter label at valuation one on the matched zero-read target. The other actual target has an explicit norm on the same ray label.

~~~python
from math import isqrt

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

def crt(a,m,b,k):
    return a+m*((b-a)*pow(m,-1,k)%k)

def norm_mod_cube(R,p):
    x,y = next((x,y) for x in range(1,p) for y in range(p)
               if (x*x+y*y-R)%p==0)
    for m in (p,p*p):
        x += m*((R-x*x-y*y)//m*pow(2*x,-1,p)%p)
    return x,y

def inside(H,c,d):
    return (H+31)//32 <= min(c,d) <= max(c,d) <= H//4

def head(n,S):
    return n%8==5 and n%3==1 and n%17==S%17 and (n-S)%25==10

p,t = 23,2161
H,c,d = 16*t,3*t,t
S = 3**c+5**d
assert prime(t) and t%720==1 and S%p==9
m,L = p**3,8640
a = next(c+80*i for i in range(11)
         if (pow(3,c+80*i,p)+pow(5,d,p))%p==0)
s0,s1 = 3**a+5**d,3**(a+880)+5**d
r0 = (s1+p*p)%m
targets = []
for r in (r0,r0+1):
    x,y = norm_mod_cube((r-S)*pow(85,-1,m)%m,p)
    x,y = crt(1,L,x,m),crt(40,L,y,m)
    z = 2**(H//2-4)
    x,y = z+(x-z)%(L*m),z+(y-z)%(L*m)
    n = S+85*(x*x+y*y)
    assert n.bit_length()==H and head(n,S)
    assert n-S==(7*x-6*y)**2+(6*x+7*y)**2
    targets.append(n)

n0,n1 = targets
assert (n0%p,n1%p)==(0,1) and (n1-n0)%(25*1728*17)==0
assert 0<abs(n1-n0)<1000*L*m*2**(H//2)
assert inside(H,c,d) and inside(H,c+800,d+1440)
assert inside(H,a,d) and inside(H,a+880,d)
assert (n0-s0)%p==0 and (n0-s0)%p**2!=0
assert (n0-s1)%p**3==p**2
assert [sum((n-pow(3,c+80*i,p)-pow(5,d+144*k,p))%p==0
            for i in range(11) for k in range(11))
        for n in targets]==[11,5]

p,t = 7448543,8641
ell = 431*t
assert all(map(prime,(p,t,431))) and p==2*ell+1 and p%4==3
assert t%720==1
for x in (pow(3,16,p),pow(5,144,p)):
    assert pow(x,ell,p)==1 and all(pow(x,ell//q,p)!=1 for q in (431,t))
u = -27*pow(5,-1,p)%p
assert u!=1 and pow(u,t,p)==1
H,c,d = 16*t,3*t,t
S = 3**c+5**d
z = 3*2**(H//2-5)
z += (25-z)%30
good = S+85*(z*z+16)
Q = 25*1728*17
bad = good+Q*((S+p-good)*pow(Q,-1,p*p)%(p*p))
assert inside(H,c,d) and good.bit_length()==bad.bit_length()==H
assert head(good,S) and head(bad,S) and good%p!=0 and bad%p==0
assert (bad-S)%p**2==p
assert good-S==(7*z-24)**2+(6*z+28)**2
~~~
