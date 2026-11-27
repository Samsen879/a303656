# Actual short-square incidence and an almost-every-target diagonal bound

Consider the still-open (rs,rs) diagonal with r,s distinct primes comparable to H^(3/4) and actual stride-720 chart side J=floor(H/12000). Let D=rs and P_D consist of the actual inert primes with D dividing both original orders and both dividing 720D. Every such prime is 1 mod 2D. Their product divides the crossing gcd of 27^(720D)−1 and 5^(720D)−1, so ∑log p=O(D), count O(D/log D), and ∑1/p=O(log D/D) by the harmonic bound in the progression. These are primes in one precise sector, not all possible markers.

On the short chart write a label's shift as αx^u+βy^v with x=3^720,y=5^720. For nonzero n mod p, let m_p be the number of actual hits. Multiply the two coordinates of every hit by x^i,y^j, with i,j in an initial interval of length comparable to J. The new points lie in a Cartesian product of side O(J). The J² lines x^(−i)X+y^(−j)Y=n are distinct up to constants because their common right side is nonzero. The [Stevens–de Zeeuw point-line incidence theorem, v4 Theorem 4](https://arxiv.org/pdf/1609.06284v4) bounds incidences by O(J^(11/4)); its characteristic condition is met since p≥2D+1 and D is comparable to H^(3/2). The translated length can be a sufficiently small fixed multiple of J if needed to fit the theorem's constant. Since each line contains all original m_p translated points, m_p≪J^(3/4). This never completes a full period.

For fixed n the zero reads contribute O(1/log H) chart fraction: every p divides n and marks at most J cells. Nonzero primes p≤2D H^(5/4)/log H have O(H^(5/4)/log H) possible values in the progression; so do p≥exp(H^(1/4)log H) by the total log budget. Each tail contributes O(1/log H) using incidence. The intermediate nonzero segment remains open pointwise.

For averaging over H-bit n, fix a chart anchor first. For fixed integer k split primes at 2^(H/(4k)); the larger primes remove at most O_k(H^(−3/4)) of the chart including zero reads. For smaller primes put w_p=m_p/J∈[0,1]; its mod-p average is J/p. Products of up to k distinct moduli are ≤2^(H/4), so the H-bit average of products is at most twice its CRT average. With W=∑w_p, the falling factorial bound k!e_k≥W(W−1)…(W−k+1) gives P(W≥H^(1/4))≪_k(log H/H^(3/4))^k. A union over O(H^(5/2)) possible parameter choices and original 12 anchors proves that apart from O_A(H^(−A)) of H-bit targets, this entire diagonal marks only O_A(H^(−3/4)) uniformly. This is an average-target theorem, not pointwise.

For two nonzero hits differing by (h,k), put a=x^h,b=y^k. Distinct short-grid hits imply a≠b and the first point's coordinates must be n(1−b)/(a−b), n(a−1)/(a−b) mod p. Actual exponents of both hits must still lie in the short box. Partition into blocks of side about H^(3/4). For E actual ordered same-block double hits and S=∑m_p, Cauchy gives S²≪(H²/log H)(E+S). A future pointwise bound E=O(H²) would close the middle segment; growth of E from a first-moment average is not enough.

## Exact same-target witness

The independent replay verifies the actual 2,400,000-bit n, a true witnessed origin, a genuine inert p=7446148379 with both step orders containing rs, and exact valuation-one hits at two specific other chart cells. Both belong to the same n; the two-point formulas and all height conditions are checked.

~~~python
from itertools import product
from math import isqrt

H,J,t,r,s,p = 2400000,200,100801,61007,61027,7446148379
D = r*s
def prime(q):
    return q > 2 and q%2 == 1 and all(q%d for d in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p == 2*D+1 and p%4 == 3
assert t%720 == 1 and 16*t <= H <= 24*t and J == H//12000 < D
assert H**3 < 2*r**4 and s**4 < 2*H**3
for q in (3,5):
    assert pow(q,720*D,p) == 1
    assert all(pow(q,720*(D//a),p) != 1 for a in (r,s))

def base(i,k,m=None):
    return pow(3,3*t+80*i,m) + pow(5,t+144*k,m)
def S(u,v,m=None):
    return base(1+9*u,1+5*v,m)

M = 5129789681521523843464636920
z = 1 << (H//2-4)
x,y = (z+(a-z)%M for a in (3590994819971548504415513537,
                           4240949814279166587960897760))
n = S(0,0) + 85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert (n%8,n%3,n%25,n%17) == (5,1,17,15)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert next(i for i in range(6)
            if all((n-base(i,0,q))%q for q in (7,19,31))) == 1
assert next(k for k in range(2) if (n-base(0,k,11))%11) == 1
assert (n-S(0,0,289))%289 == 85

hits = {uv for uv in product(range(J),repeat=2) if (n-S(*uv,p))%p == 0}
assert hits == {(31,188),(138,56)} and n%p == 1913223921
assert all((n-S(*uv,p*p))%(p*p) != 0 for uv in hits)
a,b = pow(3,720*107,p),pow(5,-720*132,p)
assert a != b
X,Y = pow(3,3*t+80+720*31,p),pow(5,t+144+720*188,p)
assert ((a-b)*X-n*(1-b))%p == ((a-b)*Y-n*(a-1))%p == 0
assert pow(15,D,p) == 1  # 两轴同二次特征，零读数无命中
print(sorted(hits), n%p)
~~~
