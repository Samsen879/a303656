# A single-axis certificate for four hits of shape 0,v,w,mv+w

Fix a target n, a short exponent chart with head (c0,d0), and hits where 3^(c0+720u)+5^(d0+720j)=n modulo p. Here the orders of 3^720 and 5^720 are both D=rs, p is odd, p does not divide n, and each chart axis has width <D. For fixed m≥2, restrict four-point shapes to 0,v,w,mv+w with coordinate diameter ≤R, 2R<D, v=(ah,bk), w=(ch,dk), a,b,c,d∈[1,M], hk≠0, ad≠bc. Then the number of realized (p, four-point shape with start) pairs is O_m(R² M⁴/log D). This concerns divisible chart rows, not actual sums of two squares or an arbitrary-target selector.

## Elimination

Let x=3^720, y=5^720, U=x^h, V=y^k, and (λ,μ,ξ,η)=(U^a,V^b,U^c,V^d). Write S_m(z)=1+⋯+z^(m−1) and T_m(λ,μ)=∑_{i=0}^{m−1} λ^i μ^(m−1−i). The first two hits with residues X,Y give ρ=−X/Y=(μ−1)/(λ−1); λ,μ are not 1 because the two nonzero displacements have absolute value <D. Also λ≠μ because n is nonzero modulo p. The third hit yields η=1+ρ(ξ−1). Substitute into Xλ^mξ+Yμ^mη=n, then divide out λ−μ and the nonzero factors, giving F=ξT_m−S_m(μ)=0; by symmetry G=ηT_m−S_m(λ)=0.

Let ℛ(U)=Res_V(F,G). Its specialization at every negative h is nonzero: use the valuation above x's base prime, with ν(U)<0. At a common root, V=0 is impossible because G would equal −S_m(λ)≠0. If ν(μ)>ν(λ), T_m and S_m(λ) have the same uniquely minimal term λ^(m−1); G forces ν(V)=0, then F compares a negative valuation to 0. If ν(μ)<ν(λ), T_m and S_m(μ) share the unique lowest term μ^(m−1), so F would force ν(U^c)=0. If ν(μ)=ν(λ), the valuations of the two S_m are equal and finite; F,G imply cν(U)=dν(V), forcing ad=bc. The leading V coefficients U^c−1 and 1 do not drop for these specializations. Thus ℛ is a nonzero integer polynomial. At genuine four hits the specialized cleared numerator is divisible by p.

## Count, including zero specializations

By symmetry assume A=max(a,c)≥B=max(b,d). The Sylvester matrix has O_m(B) rows and coefficient ℓ1 sum O_m(1) in each row. Its determinant has degree O_m(AB) and log coefficient ℓ1 norm O_m(B). Summing the log of the nonzero cleared numerator over 0<|h|≤R/A therefore costs O_m(R²B/A); this also works for negative h by multiplying by the appropriate power of x. Every p≥2D+1, so divide by log D to count distinct divisors for each h. For a fixed p,h, F is nonzero of degree m−1 in μ, with leading coefficient U^c−1 because 0<|ch|≤R<D. The map k↦y^(bk) is injective in the interval for k because the span of bk is ≤2R<D. For fixed p,h,k the first two hits fix the residues X,Y uniquely since λ≠μ, and exact order makes the start unique in the short chart.

Any zero specialization has h>0. The ordinary polynomial root bound gives h=O_m(B), while |k|≤R/B. Thus there are O_m(R) such parameter pairs. For each one, at least one of the original two rational cross determinants for w and mv+w is nonzero: otherwise exact positive reads would also have ξT_m=S_m(μ), impossible when U>1 since ξ>1 and termwise T_m>S_m(μ). The logarithmic numerator height for that short determinant is O_m(R), including clearing negative exponents. Charge its prime divisors as before. Both branches together cost O_m(R²/log D) for each coefficient tuple.

## Same-target exact replay

In the chart below a single actual target admits both m=3 and m=4 four hits at the same inert p; all tested hits have valuation exactly one. Changing only the fourth point in the m=3 fixture to the m=5 choice gives a non-hit with residue 1033. The chart head has a separate true two-square witness.

```python
from math import isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
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

L,z = 146651884329720, 1 << (H//2-4)
x,y = (z+(a-z)%L for a in (61827877807697,135417323161960))
n = S(0,0)+85*(x*x+y*y)
assert n.bit_length() == H and n > S(J-1,J-1)
assert n-S(0,0) == (7*x-6*y)**2+(6*x+7*y)**2 > 0
assert (n%8,n%3,n%25,n%17,n%p) == (5,1,17,15,1018)
assert next(i for i in range(6)
            if all((n-raw(i,0,q))%q for q in (7,19,31))) == 1
assert next(k for k in range(2) if (n-raw(0,k,11))%11) == 1
assert (n-S(0,0,289))%289 == 85

for m,(u,k),(h,j),(g,l) in [(3,(160,1),(12,37),(88,28)),
                             (4,(7,224),(66,2),(10,25))]:
    assert h*l != j*g
    for i,d in ((0,0),(h,j),(g,l),(m*h+g,m*j+l)):
        assert 0 <= u+i < J and 0 <= k+d < J
        z = (n-S(u+i,k+d,p*p))%(p*p)
        assert z and z%p == 0
    lam,mu = pow(3,720*h,p),pow(5,720*j,p)
    T = sum(lam**i*mu**(m-1-i) for i in range(m))
    assert (pow(3,720*g,p)*T-sum(mu**i for i in range(m)))%p == 0
    assert (pow(5,720*l,p)*T-sum(lam**i for i in range(m)))%p == 0
    for i,d in ((g,l),(m*h+g,m*j+l)):
        f = (3**(720*h)-1)*(5**(720*d)-1) - (3**(720*i)-1)*(5**(720*j)-1)
        assert f and f%p == 0

assert 308 < J and 214 < J
assert (n-S(308,214,p))%p == 1033
print(n%p,(n-S(308,214,p))%p)  # 1018 1033
```
