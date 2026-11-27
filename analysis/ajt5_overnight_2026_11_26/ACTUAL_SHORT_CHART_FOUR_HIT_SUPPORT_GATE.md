# Same-target double hits and a four-hit support gate

Use the actual selected chart with D=rs, r,s comparable to H^(3/4), and J=floor(H/12000), writing its two coordinate powers X_u=αx^u,Y_v=βy^v with x=3^720,y=5^720. For a nonzero read n mod p and displacement (h,k), set a=x^h,b=y^k. Actual distinct double hits within the short chart imply a≠b mod p. The support of a fixed displacement in a fixed block is exactly the simultaneous prime support of the products over admissible axial start positions of (a−b)X_u−n(1−b) and (a−b)Y_v−n(a−1). The axes can recover different start positions for different p; a true two-prime control below proves no single common start should be assumed.

For actual three hits including the origin and two displacements d,e, elimination gives a nonzero prime multiple of the numerator Δ(d,e)=(x^(d₁)−1)(y^(e₂)−1)−(x^(e₁)−1)(y^(d₂)−1), unless that rational determinant is zero in characteristic zero. A fixed p,n and nontrivial shape determine at most one actual start. In an exponent-collinear triple with primitive direction (h,k) both components must be nonzero; taking the origin at an end, use the strict increase of (z^j−1)/(z^i−1) for positive z and integers 0<i<j, plus multiplicative independence of x,y. The determinant is nonzero and at length L costs logarithmic size O(L). Counting O(ℓ(L/ℓ)^2) triples for direction max size ℓ gives O(L³ log(2L)/log H) real prime–shape hits. Thus the double-hit subfamily extendible to such triples of diameter H^(2/3) contributes O(H²).

For arbitrary four points in blocks of diameter R=floor(H^(3/4)), require a prime dividing both Δ(d,e) and Δ(d,f). The [Evertse–Schlickewei–Schmidt rank-two unit equation bound](https://annals.math.princeton.edu/2002/155-3/p04) bounds the number of characteristic-zero points on each non-axis line not through the origin; origin lines have at most one here by multiplicative independence, and actual axis lines cannot contain multiple hits. Thus the degenerate triples/quads cost O(m²)/O(m³) inside an m-hit block. Over O(H²/log H) prime/block pairs, a positive deleted chart fraction would force Ω(H²(log H)^3) actual prime/quadruple pairs with both determinants nonzero by the fourth moment, and then Ω(H^(5/4)(log H)^4) distinct four-point shapes since each short determinant supports O(R/log H) primes. This is a necessary condition, not a contradiction. The full pointwise double-hit bound remains open.

The short recurrence also gives a precise exclusion: on a non-axis arithmetic progression of exponents, actual nonzero hits at positions 0,1,3 force 1+λ+μ=0 for λ=x^h,μ=y^k. The read differences F_j obey F₇=−2e₂e₃F₂ and F₉=3e₂²e₃F₂. A further hit at either 7 or 9 forces λ³=μ³=1, impossible for the stated actual inert double-order sector, since gcd(3,D)=1 and each exponent shift is nonzero and <D. The two exact target controls below independently check the shared displacement and actual 0,1,3 progression with both outer positions failing. These are true exact-one controls. Merely having unique offsets and bounded row capacities cannot prove the pointwise result: sparse parabola rows over a prime field have both properties and enough combinatorial double hits, without being actual power-chart rows.

~~~python
from math import isqrt

def fixture(H,t,r,s,M,a,b,rows):
    J,D = H//12000,r*s
    def prime(q):
        return q > 2 and q%2 and all(q%d for d in range(3,isqrt(q)+1,2))
    assert all(map(prime,[t,r,s,*rows])) and t%720 == 1 and 16*t <= H <= 24*t
    for p in rows:
        assert p%4 == 3 and (p-1)%(2*D) == 0 and J < D
        for q in (3,5):
            assert pow(q,720*D,p) == 1
            assert all(pow(q,720*(D//ell),p) != 1 for ell in (r,s))
    def raw(i,k,m=None):
        return pow(3,3*t+80*i,m)+pow(5,t+144*k,m)
    def S(u,v,m=None):
        return raw(1+9*u,1+5*v,m)
    w = 1 << (H//2-4)
    x,y = w+(a-w)%M,w+(b-w)%M
    n = S(0,0)+85*(x*x+y*y)
    assert n.bit_length() == H and n > S(J-1,J-1)
    assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
    assert (n%8,n%3,n%25,n%17) == (5,1,17,15)
    assert next(i for i in range(6)
                if all((n-raw(i,0,q))%q for q in (7,19,31))) == 1
    assert next(k for k in range(2) if (n-raw(0,k,11))%11) == 1
    assert (n-S(0,0,289))%289 == 85
    for p,pts in rows.items():
        assert n%p
        for u,v in pts:
            assert 0 <= u < J and 0 <= v < J
            z = (n-S(u,v,p*p))%(p*p)
            assert z and z%p == 0
    return n,S,J

p,q = 4705423,7842371
n,S,J = fixture(3000000,126001,811,967,
    125987743237311920348139418484578680,
    95062447867707982709617912725519137,
    27887742690454097753998950083285680,
    {p:[(1,172),(77,188)],q:[(162,174),(238,190)]})
for l,(u,v) in [(p,(162,174)),(q,(1,172))]:
    assert (S(u+76,v+16,l)-S(u,v,l))%l
assert (n%p,n%q) == (3511323,3210959)

p = 148859
def P(j):
    return 33+104*j,78+102*j
n,S,J = fixture(12000000,570961,263,283,2050153513110345720,
    1861276262607540857,356791373907911320,
    {p:[P(j) for j in (0,1,3)]})
assert n%p == 11880 and all(0 <= a < J for j in (7,9) for a in P(j))
assert [(n-S(*P(j),p))%p for j in (0,1,3,7,9)] == [0,0,0,145377,119623]
~~~
