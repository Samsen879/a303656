# Large prime-source tail: sparse support and aligned lines

The large prime-source tail falls from 1,633 to 3 units of 10^(-11) density. The natural exception density is therefore **below 0.000065454085%**. The finite rows, cutoff, higher-power tail, and low-order tail are unchanged.

Keep the largest assigned order prime power D. Only the prime case D=r>10^5 is treated here. For doubly ordinary inert r<=B, use the exact-two repair grid of DISTINCT_READER_MOMENT_DENSITY_BOUND.md. A nonconstant shallow reader kills at most K=floor((1+sqrt(4r−3))/2) normalized positions, and a deep reader at most r/(r−1)<=K. A nonconstant terminal needs r−K fully killed positions. The distinct second moment costs at most (r S_r)^2/((r−K)(r−2K))<=4S_r²; the source gate contributes 1/r and the terminal reciprocal factor is at most S_r. Older shallow constant alignments each need an intercept and a zero observation, costing at most 2S_r/r² before the terminal factor.

A constant terminal alignment needs a nonsquare parity choice at the terminal. For 10^5<r<=10^6, the parity masses 37,37,38 out of 96 occur on two reduced progressions each modulo 60r. The per-class [Brun–Titchmarsh](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED) reciprocal envelope is less than (log r−2)/(8(r−1)): with U=4r/3−log(60r), V=34−log(60r), use U>5/2, V>16, and log 12>12/5. The summed parity-weighted envelope is 7/24 times (log r−2)/(r−1). Above 10^6 retain the universal 19S_r/48. Each pays the source/intercept factor r^(-2).

Eligible inert sources avoid 3,5,7,11,13,17,19,23. Inclusion–exclusion in the class 3 modulo 4 bounds the candidate count over an interval of length L by rho L+256, with rho=55296/676039. Partial summation bounds a decreasing nonnegative weight by rho times its integral plus 256 times its left-end value. The disjoint parity ranges can each be enlarged to infinity for an upper bound. This needs no source scan. The two named singly exceptional sources, the unconditional above-cutoff reservoir, and the robust-reader allowance retain their inherited charges. The replay gives 143 units from sparsity alone and 3 after the distinct-reader and parity charges. The exact 31-to-683 arithmetic fixture explains why the alignment term cannot just be discarded. No pointwise or density-one proof follows.

```python
from fractions import Fraction as Q
from math import ceil, factorial, floor, isqrt, prod

W,P,C,B,Z = 10**11,10**5,10**6,9*10**14,10**25

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2,u2 = series(Q(2))

def logs(x):
    y,k = Q(x),0
    while y >= 2:
        y /= 2
        k += 1
    l,u = series(y)
    return Q(floor(W*(l+k*l2)),W), Q(ceil(W*(u+k*u2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]

def I(x,k,m,b=Q(1,2)):
    L = hi(x)+b
    return sum(Q(factorial(m),factorial(m-j))*L**(m-j)/(k-1)**(j+1)
               for j in range(m+1))/x**(k-1)

rho = prod(1-Q(1,p) for p in (3,5,7,11,13,17,19,23))/4
assert rho == Q(55296,676039)

def J(x,k,m,b=Q(1,2)):
    return rho*I(x,k,m,b)+256*(hi(x)+b)**m/x**k

assert lo(B)>34 and 34-hi(60*C)>16
assert Q(4*P,3)-hi(60*C)>Q(5,2) and lo(12)>Q(12,5)
assert 4*(isqrt(P)+1)<=P and lo(P)-2>1
A = Q(P,P-1)
ordinary = (Q(7,24)*A*J(P,3,1,Q(-2))+Q(19,48)*A*J(C,3,1)
            +4*A**3*J(P,4,3)+2*A*A*J(P,4,2))

rare = (1006003,1645333507)
for r,b in zip(rare,(3,5)):
    assert r%4==3 and P<r<B
    assert pow(b,r-1,r*r)==1!=pow(8-b,r-1,r*r)
keep = (sum((hi(r)+Q(1,2))/(r*(r-1)) for r in rare)
        +(hi(B)+Q(3,2))/(B-1)+Q(3,2**P))

old = ceil(W*(A*I(P,3,1)+2*A*A*I(P,3,2)+keep))
sparse = ceil(W*(A*J(P,3,1)+2*A*A*J(P,3,2)+keep))
new = ceil(W*(ordinary+keep))
assert (old,sparse,new)==(1633,143,3)
assert W*ordinary<Q(1314,1000) and W*keep<Q(1420,1000)

def exp_lo(x,n):
    s=t=Q(1)
    for j in range(1,n):
        t *= x/j
        s += t
    return s

fact = Q(0)
for p in (29,31,37,41,43,47):
    D = p
    while D <= (P if D==p else C):
        phi = D-D//p
        S = (hi(D)+Q(1,2))/phi
        l,u = logs(4*D)
        R = min(S,(1/(Q(4*D,3)-u)+hi((Q(4*D,3)-l)/(34-u)))/phi)
        extra = D==p and p%4==3 and all(pow(b,p-1,p*p)!=1 for b in (3,5))
        fact += R*(p*S**(p-1)+(S**p if extra else 0))
        D *= p
x = Q(1,10)
fact += x**53*(3*(53/(1-x)+x/(1-x)**2)+x/(1-x))

t = lo(B)+48*l2
def geom(v):
    return 1/(exp_lo(v*t,100)*(1-1/exp_lo(v*l2,12)))

root = Q(isqrt(floor(hi(3)*Z*Z/(4*t)))+1,Z)
low_tail = 70*(root*geom(Q(271,750))+geom(Q(323,375)))
low_finite = Q(891331308302981248,Z)
finite = 30214+13603+9670+2975
assert finite==56462
before = Q(finite+28+old,W)+fact+low_finite+low_tail
after = before-Q(old-new,W)
assert Q(670840846076456,10**19)<100*before<Q(670840846076458,10**19)
assert Q(654540846076456,10**19)<100*after<Q(654540846076458,10**19)

# Actual aligned line with r-valuation two and q-valuation one.
n,c,d,r,q = 6028380249757748835,59811986528,55,31,683
L = 3960*q
def residual(a,b,m): return (n-pow(3,a,m)-pow(5,b,m))%m

assert residual(c,d,4)==1 and residual(c,d,3)!=0
assert all(residual(c,d,p) for p in (7,11,19,23))
assert all(pow(b,p-1,p*p)!=1 for p in (r,q) for b in (3,5))
for i in range(r):
    a,b = c+L*i,d+L*((14+20*i)%r)
    assert residual(a,b,r*r)==0
    ys = [b+L*r*j for j in range(r) if residual(a,b+L*r*j,r**3)]
    assert len(ys)==r-1 and all(residual(a,y,q*q)==q for y in ys)

print(old,sparse,new)
```
