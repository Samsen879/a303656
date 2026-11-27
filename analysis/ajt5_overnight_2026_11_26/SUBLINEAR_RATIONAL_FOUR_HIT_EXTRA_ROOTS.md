# Sublinear rational four-hit sectors and genuine extra roots

For an interior combination e f=m v+l w with e>m+l, m,l>0, the primitive affine relation has coefficients (e−m−l,m,l,−e) divided by their gcd. Changing the distinguished fourth point changes its minimum denominator to the magnitude of that primitive coefficient. Thus 5 f=2 v+2 w can be relabeled with integer denominator (though chart step signs still matter), whereas 17 f=5 v+5 w has smallest possible denominator 5 under any relabeling.

In a fixed actual n, count four hits modulo p in the short chart with both step orders D=rs, length <D each axis, p not dividing n, coordinate diameter ≤R and 2R<D. Assume v=(ah,bk), w=(ch,dk), 1≤a,b,c,d≤M, ad≠bc, hk≠0. The number of (p, realized shape with start) pairs in this fixed e,m,l sector is O(e² R² M⁴/log D).

Perform period and divisibility changes in the actual integers: on the first axis t=e/gcd(e,ma+lc) divides h. Use U=3^(720h/t), a'=ta, c'=tc and P=(ma'+lc')/e, and do the analogous change for V,b',d',Q. In particular no modular division of the exponent is used. Put A=U^a'−1, C=U^c'−1, L=U^P−1, Z=V^b', B=A+C(Z−1), K=A+L(Z−1). The real modular reads are eta=B/A and Omega=K/A; the fourth hit needs Omega=V^Q. The necessary elimination equations are
```
F = A^b' Z^d' − B^b'
G = (A^e Z^m B^l − A^l K^e)/(Z−1).
```
The quotient is a polynomial, and the G leading Z coefficient is −A^l L^e, a unit at an actual hit. Consequently at most e−1 k candidates remain at fixed p,h by exact order in the short chart. The start is unique via the two-equation Cramer system.

The resultant is nonzero. Take a formal valuation with ν(U)=−1 and residue characteristic zero. Repeated one-axis coordinates cannot occur, so a',c',P are distinct and positive; Z=0 contradicts a'≠c', and Z=1 contradicts G(U,1)=A^(e+l−1)(mA+lC−eL). A hypothetical root otherwise has eta^b'=Z^d', Omega^e=Z^m eta^l. If ν(Z)>0 then ν(eta)>0 and the third-hit identity forces a'=c'. If ν(Z)<0, the two hit identities yield ν(eta)−ν(Z)=a'−c' and ν(Omega)−ν(Z)=a'−P. With the power equation this forces ν(Z)=−a', ν(eta)=−c', incompatible with ad≠bc. If ν(Z)=0 and a'>c', then eta tends to 1 and ν(eta−1)=a'−c'. Since P<max(a',c'), Omega tends to 1 as well. The two positive powers of Z in eta^b' and Omega^(e b') both tend to 1; in residue characteristic zero their deviations have the same order (each is a simple root at the residue of Z). Thus ν(Omega−1)=a'−c'; the fourth identity forces P=c'. For c'>a' the roles imply Z and Omega tend to 1 with ν(Omega−1)=ν(Z−1)=c'−a', forcing P=a'. All branches are excluded.

After swapping axes to arrange A0=max(a',c')≥B0=max(b',d'), the Sylvester determinant has degree O(e A0 B0), log coefficient norm O(e B0), and total nonzero log height O(eR²) over |h/t|≤R/A0. Multiply by the at most e−1 k for each prime and h. Direct/reciprocal Cauchy bounds put zero specializations at |h/t|=O(eB0), leaving O(eR) shapes. The two original rational determinants cannot both vanish: rebasing at the interior point f would give two actual positive axis triples related by Y_i=1+σ(X_i−1), with both weighted products for weights (e−m−l,m,l) equal to 1. The strictly concave weighted log sum would have three distinct zeros at 0,1,σ. Each short original determinant that is nonzero therefore costs only O(R) log height. Count primes by their minimum size 2D+1 and sum the at most M⁴ tuples. This fixed-sector estimate does not sum growing denominator choices or resolve arbitrary n.

## A real false positive for power filtering

Even within the original order-D cyclic step subgroup, the e-th power read can admit gcd(e,D) roots. For p=1259 and e=17, the same n and same first three actual hits give a true 17 f=5 v+5 w and a false 17 f=2 v+2 w; the latter has nonzero fourth remainder 1210 but its reconstructed-to-actual ratio 1008 has exact order 17. The fifth line is another such false positive. Exact original residue comparison is necessary.

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

T1 = (71,138),(77,-122),(203,-28)
T2 = (26,83),(193,161),(266,179)
for e,m,l,(o,v,w),res,rho in [
    (5,2,2,T1,17626,1),
    (17,4,2,T1,1020161,946),
    (17,5,5,T2,950545,1),
    (17,2,2,T2,1471722,1008),
    (8279,616,1296,T2,426461,51),
]:
    assert gcd(e,gcd(m,l)) == 1 and m+l < e
    assert v[0]*w[1] != v[1]*w[0]
    f = tuple(m*a+l*b for a,b in zip(v,w))
    assert all(a%e == 0 for a in f)
    f = tuple(a//e for a in f)
    def read(z):
        u,k = (a+b for a,b in zip(o,z))
        assert 0 <= u < J and 0 <= k < J
        return (n-S(u,k,p*p))%(p*p)
    assert all(read(z) in range(p,p*p,p) for z in ((0,0),v,w))
    assert read(f) == res != 0 and (res%p == 0) == (rho == 1)
    i,j = (a+b for a,b in zip(o,f))
    X,Y = pow(3,3*t+80+720*i,p),pow(5,t+144+720*j,p)
    assert (n-X)*pow(Y,-1,p)%p == rho
    if rho in (1008,51):
        assert gcd(e,D) == 17 and rho != 1 and pow(rho,17,p) == 1
    print(e,m,l,(i,j),res%p,rho)
```
