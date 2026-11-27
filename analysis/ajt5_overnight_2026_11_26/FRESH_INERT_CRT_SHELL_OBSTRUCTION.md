# Fresh inert primes defeat finite CRT promises for signed shells

For odd \(u,v>0\) with \(A=5^u>B=3^v\), the signed layer \(\Phi_d(A,B)\), \(d>1\) odd, is a norm for every such pair if \(3\mid d\). The plus layer \(\Phi_{2d}(A,B)\) is universally a norm if \(3\mid d\) or \(5\mid d\). These positive statements use the [exact order support and fifth plus certificate](https://github.com/Samsen879/a303656/commit/f0762caad9ef46371c4e0cee565d9fb35ae7ad4b). In every other case, **each compatible exponent congruence class contains a failure with arbitrarily large inert witness prime**. One can impose any finite list of such failures simultaneously. This is a statement about varying exponents in a congruence class, not about a fixed seed or preserving globally admissible earlier layers.

Start from a compatible class for \(u,v\bmod M\). For each prime \(\ell\mid d\), refine the class to fix the two exponent valuations and write \(s_\ell\) for their minimum. Choose an inert prime \(p\equiv11\bmod12\) with \(v_\ell(p-1)=v_\ell(d)+s_\ell\). At other odd primes dividing the refined modulus require \(p-1\) coprime to them. For minus, take \(p\equiv1\bmod5\) if \(5\mid d\), otherwise \(p\equiv4\bmod5\); for plus take \(p\equiv2\bmod5\) (so \(5\nmid d\)). At each \(\ell\mid d\), require the base belonging to an exponent of valuation \(s_\ell\) to be a non-\(\ell\)-th-power residue and the other base to be an \(\ell\)-th-power residue.

These simultaneous prime conditions follow from Chebotarev in the Kummer extension of the cyclotomic field defining the progression. Over that abelian cyclotomic field the classes of 3 and 5 are independent modulo \(\ell\)-th powers. Otherwise an \(\ell\)-th root of \(3^a5^b\) in a nontrivial class would lie there; using the \(\ell\)-th roots of unity one could take its real root, whose degree is \(\ell\) by the valuation at 3 or 5, and whose real field is not normal. That is impossible in an abelian extension. Each Kummer kernel is therefore \(C_\ell^2\) and the extensions for distinct \(\ell\) have coprime degrees. Since the chosen cyclotomic automorphism fixes the \(\ell\)-th roots of unity, the residue and nonresidue restrictions pick a nonempty set of lifts. The resulting Frobenius conditions are conjugacy-invariant.

Take both exponents divisible by the prime-to-\(2d\) part of \(p-1\), which is coprime to their refined modulus. By the exponent valuations and Kummer choices, the ratio has exact \(\ell\)-primary order \(\ell^{v_\ell(d)}\) for each \(\ell\mid d\). Quadratic characters give total order \(d\) on the minus side, \(2d\) on the plus side. On a further CRT extension at this new \(p\), choose \(v_p(5^{p-1}-1)+v_p(u)\) odd and strictly below \(v_p(3^{p-1}-1)+v_p(v)\). LTE forces that odd valuation in precisely the desired primitive cyclotomic factor. Repetition preserves all earlier imposed witness congruences.

Conversely any fixed finite inert-prime panel can be made harmless simultaneously at every index \(3^a5^b7^c\): use the same unequal-valuation construction with the smaller valuation even at its odd primes other than 5. None of those primes divides the index, and 5 is absent. Choose \(u,v\equiv1\bmod4\) to get valuation four at 2 in the combined numerator. The finite-panel construction and fresh-prime theorem are therefore compatible. The replay shows a single panel passing alongside three new inert witnesses and also gives positive and failed lifts with genuine parent norms.

~~~python
from math import gcd, isqrt

def crt(a,m,b,n):
    assert gcd(m,n) == 1
    return (a + m*((b-a)*pow(m,-1,n)%n)) % (m*n)

def join(u,v,m,a,b,q):
    return crt(u,m,a,q), crt(v,m,b,q), m*q

panel = (11,17,23,71,113,197)
u,v,M = 1,1,140
for p in panel:
    assert pow(5,p-1,p*p) != 1
    u,v,M = join(u,v,M,p,0,p*p)

# d, numerator sign, prime, ratio order, prime divisors of order, residue
rows = [(25,-1,5351,25,(5,),149828),
        (35,-1,108011,35,(5,7),7384928092),
        (49,+1,66347,98,(2,7),3449446877)]
for d,sg,p,o,qs,r in rows:
    assert p not in panel and p%3 == 2
    assert all(p%i for i in range(2,isqrt(p)+1))
    assert (p-1)%(2*d) == 0
    u,v,M = join(u,v,M,0,0,(p-1)//(2*d))
    u,v,M = join(u,v,M,1,0,p)

u += M
assert u >= v > 0 and u%4 == v%4 == 1
assert (pow(5,2*u,32)-pow(3,2*v,32))%32 == 16
for p in panel:
    w = (pow(5,u*(p-1),p**3)-pow(3,v*(p-1),p**3))%(p**3)
    assert w and w%(p*p) == 0
for d,sg,p,o,qs,r in rows:
    z = pow(5,u,p)*pow(pow(3,v,p),-1,p)%p
    assert pow(z,o,p) == 1 and all(pow(z,o//q,p) != 1 for q in qs)
    w = (pow(5,u*d,p*p)+sg*pow(3,v*d,p*p))%(p*p)
    assert w == r and 0 < r < p*p and r%p == 0

def N(x,y): return x*x+3*y*y

A,B = 5**11,3**3
assert A*A-B*B == N(45401686,10374210)
assert (A**5-B**5)//(A-B) == N(594392000783087,1333047033266432)
assert (A**5+B**5)//(A+B) == N(A*A-3*A*B+B*B,5**6*3*(A-B))
assert (A**25-B**25)%(7451**2) == 52097392
z = A*pow(B,-1,7451)%7451
assert pow(z,25,7451) == 1 and pow(z,5,7451) != 1

assert 5**2-3**2 == N(2,2)
assert (5**7-3**7)//2 == N(137,80) and (5**7+3**7)//8 == N(74,39)
A,B = 5**13,3**5
assert A*A-B*B == N(1220699108,1808048)
assert (A**7-B**7)%(197**2) == 18715 == 95*197
assert pow(A*pow(B,-1,197),7,197) == 1 and A%197 != B%197

def vp(n,p):
    e = 0
    while n%p == 0: n,e = n//p,e+1
    return e

for U,V,r in [(11,3,5),(55,15,5),(1,1,7),(13,5,7)]:
    assert all(vp(5**(2*r*U)-3**(2*r*V),p)%2 == 0
               for p in (2,11,17,23,29,71,113))
print("PASS")
~~~
