# The same-target 0,v,w,2v+w four-hit sector admits a one-axis certificate

On the actual short chart, keep one target n and only nonzero reads at inert p in the double-order rs sector. Consider a noncollinear shape 0,v,w,2v+w of diameter ≤R where v=(ah,bk),w=(ch,dk), positive integral a,b,c,d≤M with ad≠bc and hk≠0. Assume 2R<rs. Thus the two moves within each axis share a sign, although h and k may be negative.

If all four hit, write their step factors (λ,μ) for v and (ξ,η) for w. With ρ=−X/Y, the first two hits give ρ=(μ−1)/(λ−1), with ρ≠0,1. The other two imply (λ+μ)ξ=1+μ and (λ+μ)η=1+λ after dividing by the nonzero factors forced by the short orders. If η=μ², then ξ=−(1+μ)², impossible because ξ is a nonzero square of an even step power at inert p; μ=−1 is already impossible. Exchanging axes gives the same obstruction when the other coordinate doubles. This subcase does not need a coefficient bound.

Put U=x^h,V=y^k. Then V^b=(1−U^(a+c))/(U^c−1) and V^d=(1+U^a)(U^c−1)/(1−U^a). Taking cross powers leaves a prime divisor of the numerator of
P(U)=(1−U^(a+c))^d (1−U^a)^b−(1+U^a)^b(U^c−1)^(b+d).
This rational value is never zero in the eligible sector. Indeed a=c would give two hits with the same first coordinate in the short chart. For W=x^|h|, a [Zsigmondy primitive prime](https://zenodo.org/records/2131326) of W^(a+c)−1 has order a+c, which divides neither c nor 2a. It kills the first term but not the second at U=W or W^−1; W is large and a+c≥3, outside the exceptions.

Given p and h, V^b has at most one permitted k in the short range, since its exponent varies by ≤2R. Given the shape p,n fixes at most one start. By exchanging axes assume B=max(b,d)≤A=max(a,c). The rational numerator log-height is O(AB|h|+B), and ∑ over 1≤|h|≤R/A is O(R² B/A)≤O(R²). A prime supporting this sector is ≥2rs+1. Thus the total true prime–shape count is O(R²M^4/log(rs)). At R≈H^(3/4), M=O(H^(1/8)), this is O(H²/log H), smaller than the earlier necessary Ω(H²(log H)^3) for globally positive reduction. It settles this one shape sector, not general fourth points.

On the same actual n, the finite p=1259 control below has four exact valuation-one hits for v=(48,35),w=(112,140), but replacing w by (39,70) still hits the first three and misses the fourth (residual 152 mod p). Origin has a literal two-square witness and all actual height inequalities are checked.

~~~python
from math import isqrt

H,J,t,r,s,p = 2880000,240,122401,17,37,1259
D = r*s
def prime(q):
    return q > 2 and q%2 and all(q%d for d in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p == 2*D+1 and p%4 == 3
assert t%720 == 1 and 16*t <= H <= 24*t and J == H//12000 and 2*J < D
for q in (3,5):
    assert pow(q,720*D,p) == 1
    assert all(pow(q,720*(D//ell),p) != 1 for ell in (r,s))

def raw(i,k,m=None):
    return pow(3,3*t+80*i,m) + pow(5,t+144*k,m)
def S(u,v,m=None):
    return raw(1+9*u,1+5*v,m)

M,z = 146651884329720, 1 << (H//2-4)
x,y = (z+(a-z)%M for a in (106736496414857,117376362362560))
n = S(0,0) + 85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert (n%8,n%3,n%25,n%17,n%p) == (5,1,17,15,248)
assert next(i for i in range(6)
            if all((n-raw(i,0,q))%q for q in (7,19,31))) == 1
assert next(k for k in range(2) if (n-raw(0,k,11))%11) == 1
assert (n-S(0,0,289))%289 == 85

for u,v in ((5,16),(53,51),(117,156),(213,226),(44,86)):
    assert 0 <= u < J and 0 <= v < J
    z = (n-S(u,v,p*p))%(p*p)
    assert z and z%p == 0
assert (n-S(140,156,p))%p == 152

def det(h,k):
    return (3**(720*48)-1)*(5**(720*k)-1) - (3**(720*h)-1)*(5**(720*35)-1)
assert all(z and z%p == 0 for z in (det(112,140),det(208,210)))
U = 3**(720*16)
P = (1-U**10)**4*(1-U**3) - (1+U**3)*(U**7-1)**5
assert P and P%p == 0
mu = pow(5,720*35,p)
assert pow(-(1+mu)**2,(p-1)//2,p) == p-1
print(n%p, (n-S(140,156,p))%p)  # 248 152
~~~
