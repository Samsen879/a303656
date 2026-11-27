# Fixed-seed support closure and the exact-order distribution gap

For coprime positive odd \(A>B\) with \(A^2-B^2\) a norm \(x^2+3y^2\), define at odd inert primes \(p\nmid AB\)
\[
D_p=\operatorname{ord}_p((A/B)^2),\qquad w_p=v_p(A^{2D_p}-B^{2D_p}).
\]
Let \(g\) be an odd integer with finite prime support \(S\). If \(D_p\mid g^k\), LTE gives \(v_p(A^{2g^k}-B^{2g^k})=w_p+k v_p(g)\). If the support of \(D_p\) is not contained in \(S\), \(p\) is never activated; otherwise it is activated for all sufficiently large \(k\). At 2 the valuation stays that of the admissible seed.

Consequently a parity \(\epsilon\bmod2\) gives infinitely many admissible \(k\) if and only if every activated prime satisfies \(w_p+\epsilon v_p(g)=0\bmod2\). If it satisfies the test, every \(k\) of that parity works; otherwise a single inert witness eventually rules it out. There exists a generator with support \(S\) and infinitely many admissible powers precisely when \(S\) contains every activated inert prime having odd \(w_p\). For sufficiency take each necessary exponent to have parity \(w_p\) and use odd powers of the generator. If such a finite support includes a prime different from 3, the normalized phases of those powers are dense because \(\log_3g\) is irrational.

For the actual seed \((5,3)\), including 5 first forces 11, 131; including 11 then forces 23, 266333. Thus a generator on that branch is a multiple of \(44135373095\). Including 7 forces 197, 6236819 (exact order 49), so a generator on that branch is a multiple of \(8600573401\). The first seventh lift works; the displayed inert factors in its next layer have valuation one. For either branch even powers eventually fail, regardless of the repair primes. There is no assertion that either initial support has finite closure.

The exact-order set is thin. For fixed \(A,B,\ell\), the number of primes through \(X\) at which \(A/B\) has order \(\ell^j\) or \(2\ell^j\) for some \(j\ge1\) is \(O(\sqrt X/\log X)\). For \(\ell^j\le\sqrt X\), at most \(O(\ell^j/j)\) such primes can divide \(A^{2\ell^j}-B^{2\ell^j}\) because each exceeds \(\ell^j\); sum the geometric scales. Above that threshold all those primes lie in a single progression modulo the first power of \(\ell\) above \(\sqrt X\), and Brun–Titchmarsh gives the same order.

A fixed-base control highlights why a condition on the primary part of order is not enough. The admissible seed \(5^{11}/3^3\) has inert primes 7451 and 1451 in the same progression modulo 1500, with nontrivial fifth-power residue symbol and exact first Fermat-power valuation one. Their total orders are respectively 25 and \(25\cdot29\); only the first belongs to the primitive layer \(\Phi_{25}\). In the degree-five Kummer extension of \(\mathbb Q(\zeta_{1500})\) adjoining its fifth root, those primes even have the same conjugacy class: the common cyclotomic action fixes \(\zeta_5\), its lift fixing the real fifth root is central, and the four nonzero Kummer shifts form a single conjugacy class. The degree claim follows from the 5-adic valuation 11 and the fact that a real, nonnormal degree-five field is not contained in an abelian field.

Primitive divisors alone or a density result for the primary part thus do not show there are infinitely many valuation-one inert primes in exact signed layers. Such an infinite sequence would preclude finite repair support. The replay checks the exact finite controls; the [28-ray exponent](https://github.com/Samsen879/a303656/commit/31be464193ce17f59e13a9fd8964b3e3ce17d257) stays \(51/110\) on generated targets only.

~~~python
from math import gcd, isqrt, prod

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

def order(A,B,p,t,qs):
    R = A*pow(B,-1,p)%p
    assert pow(R,t,p) == 1 and all(pow(R,t//q,p) != 1 for q in qs)

def N(x,y):
    return x*x+3*y*y

A,B = 5**11,3**3
assert A*A-B*B == N(45401686,10374210)
assert (A**5-B**5)//(A-B) == N(594392000783087,1333047033266432)
assert (A**5+B**5)//(A+B) == N(A*A-3*A*B+B*B,5**6*3*(A-B))
for p,t,qs,r in [(7451,25,(5,),38678141),(1451,725,(5,29),1591747)]:
    assert prime(p) and p%1500 == 1451 and p%3 == 2
    order(A,B,p,t,qs)
    assert pow(A*pow(B,-1,p),(p-1)//5,p) != 1
    assert (pow(A,p-1,p*p)-pow(B,p-1,p*p))%(p*p) == r
    assert 0 < r < p*p and r%p == 0
assert (A**25-B**25)%(7451**2) == 52097392

A,B = 5,3
assert A*A-B*B == N(2,2)
assert (A**7-B**7)//2 == N(137,80) and (A**7+B**7)//8 == N(74,39)
assert (A**5-B**5)//(A-B) == 11*131
assert (A**11+B**11)//(A+B) == 23*266333
for p,t,qs in [(11,5,(5,)),(131,5,(5,)),(23,22,(2,11)),(266333,22,(2,11))]:
    assert prime(p) and p%3 == 2
    order(A,B,p,t,qs)

H = (A**49-B**49)//(A**7-B**7)
p = 190388929073498585263
fac = [2,3,3,7,7,251,2393,2617,13723,10007]
# Lucas primality certificate for the large split factor.
assert prod(fac) == p-1 and all(prime(q) for q in set(fac))
assert pow(3,p-1,p) == 1
assert all(gcd(pow(3,(p-1)//q,p)-1,p) == 1 for q in set(fac))
I = 197*6236819
assert H == I*p and I**10 > H**3
assert prime(197) and prime(6236819)
assert (197%3,6236819%3,p%3) == (2,2,1)
for q in (197,6236819,p):
    order(A,B,q,49,(7,))
print("PASS")
~~~
