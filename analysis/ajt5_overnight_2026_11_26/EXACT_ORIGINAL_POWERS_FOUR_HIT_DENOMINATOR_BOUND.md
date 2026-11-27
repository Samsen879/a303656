# Keep the original fourth powers and remove the explicit per-denominator square cost

In the same fixed target two-order chart, write a sublinear interior shape e f=m v+l w, with gcd(e,m,l)=1, m,l>0, m+l<e, v=(ah,bk), w=(ch,dk), both axes reduced, a,b,c,d≤M, nonzero signed h,k, ad≠bc. Count only p not dividing n, diameter ≤R, 2R<D=rs, short chart widths <D. Let P=ma+lc,Q=mb+ld, s_x=e/gcd(e,P), s_y=e/gcd(e,Q). Integrality requires s_x|h,s_y|k. Set U=3^(720h/s_x), V=5^(720k/s_y), A=U^(s_x a)−1, C=U^(s_x c)−1, L=U^(P/gcd(e,P))−1. The exact hit equations are
```
F=A(V^(s_y d)−1)−C(V^(s_y b)−1)
G=A(V^(Q/gcd(e,Q))−1)−L(V^(s_y b)−1).
```

Over Q(U) their gcd is exactly V−1. This root is simple in F, and any root with V^(s_y b)=1 must be it by gcd(b,d)=1 and gcd(s_y,Q/gcd(e,Q))=1. V=0 is excluded since a≠c for an actual hit. For any other root, use ν(U)=−1 with residue characteristic zero. Writing the scaled exponents as a',b',c',d',P',Q', positive ν(V) forces a'=c'. Negative ν(V) gives (d'−b')ν(V)=a'−c' and (Q'−b')ν(V)=a'−P'; combining the relations eP'=m a'+l c' and eQ'=m b'+l d' yields b'ν(V)=−a', d'ν(V)=−c', contradicting noncollinearity. At zero ν(V), exactly one of V^b'−1 and V^d'−1 has positive valuation (otherwise their valuation difference could not be a'−c'). Since P'<max(a',c'), V^Q'−1 also has positive valuation. All positive deviations from 1 of powers of a given unit have matching valuation in residue characteristic zero, which would force P'=a' or c', a repeated axis. Thus the Sylvester map loses one rank generically, and every genuine finite-field hit loses another because V≠1 is a second common root. A nonzero maximal minor in characteristic zero supplies the certificate, even if a finite-field leading coefficient vanishes.

Let A0=max(a,c), B0=max(b,d). Sparse rows give degree O(s_x A0 s_y B0) and log coefficient norm O(s_y B0). Nonzero specialized certificate height sums to O(R² s_y B0/(s_x A0)); each p,h supports at most B0 choices of k by the third-hit polynomial in Z=5^(720bk), using reduced b,d and the short-order injection. Zero specializations, by forward and reciprocal Cauchy bounds, leave O(s_y B0) h/s_x choices and hence O(R) pairs with k/s_y. Use the original short determinants, at least one nonzero by the strict weighted-log concavity at the interior point, to charge O(R) height each. Exchanging axes and taking the better bound gives O(R²(1+sqrt(A0 B0))/log D) per coefficient and fraction tuple, uniformly in e. Summing e≤E gives O(M^5 R² E³/log D).

There is also a direct aggregate for r|e≤Cr with r≈R and r not dividing ad−bc. At least one of h,k is divisible by r by the two integer axis constraints and primitive (e,m,l). If r|h, then a,c,h/r have O(1) choices. The original three-hit determinant is nonzero by 3-adic valuation; if h<0 its vanishing would make 720h(a−c)=v_3(b)−v_3(d), and if h>0 it would make 720h min(a,c)=v_3(d−b)−v_3(b). These are impossible since b,d≤R and |h|≥r. The other direction uses 5-adic valuation. For r not dividing k, we have r|Q and each e/r≤C, so across the full denominator menu only O_C(B0) fourth vertical offsets are possible at fixed k; each permits at most one horizontal read. This cancels the R/B0 choices of k after charging each three-hit determinant O(R/log D) primes. If r also divides k, there are only O(1) axis steps and each prime permits O(R) fourth points. Summing both coarse-axis directions gives O_C(M²R²/log D) in the stated subcase.

The exact same-target controls below verify the original-root gcd degree 2 at true rational fourth points and degree 1 at the false ones, including the e=17 powered false positive and a genuine coarse-axis e=34 fixture. Neither estimate covers the general pointwise middle.

```python
from math import gcd, isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
D = r*s
def prime(q):
    return q > 2 and q%2 and all(q%d for d in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p == 2*D+1 and p%4 == 3
assert t%720 == 1 and 16*t <= H <= 24*t and J == H//12000 and 2*J < D
for q in (3,5):
    assert pow(q,720*D,p) == 1
    assert all(pow(q,720*(D//a),p) != 1 for a in (r,s))

def S(u,v,m=None):
    return pow(3,3*t+80+720*u,m) + pow(5,t+144+720*v,m)

M,z = 146651884329720, 1 << (H//2-4)
x,y = (z+(a-z)%M for a in (61827877807697,135417323161960))
n = S(0,0)+85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert n%(p*p) == 1223507

def poly(*terms):
    a = [0]*(1+max(k for k,v in terms))
    for k,v in terms:
        a[k] = (a[k]+v)%p
    while a and not a[-1]:
        a.pop()
    return a

def degree_gcd(a,b):
    while b:
        z = pow(b[-1],-1,p)
        while len(a) >= len(b):
            d,c = len(a)-len(b),a[-1]*z%p
            for j,v in enumerate(b):
                a[d+j] = (a[d+j]-c*v)%p
            while a and not a[-1]:
                a.pop()
        a,b = b,a
    return len(a)-1

T2 = (26,83),(193,161),(266,179)
Tc = (219,244),(-187,-51),(-68,-162)
for e,m,l,(o,v,w),expected,rho0,deg in [
    (17,5,5,T2,950545,1,2),
    (17,2,2,T2,1471722,1008,1),
    (34,12,17,Tc,153598,1,2),
    (34,10,17,Tc,1258386,701,1),
]:
    assert gcd(e,gcd(m,l)) == 1 and m+l < e
    h,k = (gcd(a,b)*(1 if a>0 else -1) for a,b in zip(v,w))
    a,b,c,d = v[0]//h,v[1]//k,w[0]//h,w[1]//k
    P,Q = m*a+l*c,m*b+l*d
    gx,gy = gcd(e,P),gcd(e,Q)
    sx,sy = e//gx,e//gy
    assert h%sx == k%sy == 0
    U,V = pow(3,720*(h//sx),p),pow(5,720*(k//sy),p)
    A,C,L = pow(U,a*sx,p)-1,pow(U,c*sx,p)-1,pow(U,P//gx,p)-1
    F = poly((sy*d,A),(sy*b,-C),(0,C-A))
    G = poly((Q//gy,A),(sy*b,-L),(0,L-A))
    def ev(T):
        return sum(v*pow(V,i,p) for i,v in enumerate(T))%p
    def read(z):
        u,j = (a+b for a,b in zip(o,z))
        assert 0 <= u < J and 0 <= j < J
        return (n-S(u,j,p*p))%(p*p)
    assert all(read(z) in range(p,p*p,p) for z in ((0,0),v,w))
    f = (h*P//e,k*Q//e)
    i,j = (a+b for a,b in zip(o,f))
    X,Y = pow(3,3*t+80+720*i,p),pow(5,t+144+720*j,p)
    rho = (n-X)*pow(Y,-1,p)%p
    res = read(f)
    assert res == expected and rho == rho0
    assert ev(F) == 0 and (ev(G)==0) == (rho==1)
    assert degree_gcd(F,G) == deg
    if e == 17:
        assert (a*d-b*c)%r == 0 and h%r and k%r and pow(rho,17,p)==1
    else:
        assert (a*d-b*c)%r and h%r==0 and k%r and Q%r==0
    print(e,m,l,(i,j),res%p,deg)
```
