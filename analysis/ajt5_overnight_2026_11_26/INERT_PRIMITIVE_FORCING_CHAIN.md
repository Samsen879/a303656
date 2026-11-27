# Inert forcing prohibits finite repair of an inadmissible odd power

Keep coprime positive odd \(A>B\) with \(3\mid AB\), and an odd inert prime \(p\nmid AB\). As in the [fixed-seed closure definition](https://github.com/Samsen879/a303656/commit/7cca2cf8c1d43b6a6c085bbb9b708eaf47845204), put \(t_p=\operatorname{ord}_p(A/B)\), \(D_p=t_p/\gcd(2,t_p)\), \(w_p=v_p(A^{2D_p}-B^{2D_p})\). If \(D_p\) is odd, there exists a larger inert prime \(q\) with \(D_q=pD_p\) and odd \(w_q\).

Indeed \(p\) divides \(\Phi_{t_p p}(A,B)\) exactly once by the cyclotomic LTE rule. That factor is odd, since its index is odd or twice odd and greater than two; modulo 3 it is 1, because one of \(A,B\) is zero, the other is a unit, and its homogeneous degree is even. After dividing out \(p\equiv2\bmod3\), a second inert prime has odd valuation. Any nonprimitive prime divisor of a cyclotomic factor is the largest prime dividing its index, since its index then has the form \(t_q q^j\) with \(t_q\mid q-1\). Here that largest prime is \(p\). Thus the second prime is primitive with \(t_q=t_pp\), so \(D_q=pD_p\) and \(q\ge2pD_p+1\). Its odd valuation persists in the first activated even exponent.

For a proposed admissible odd multiplier \(r\), first suppose an active inert prime divides \(r\), where active means \(D_p\mid r\). Take the largest such \(p\). The forcing step gives an active \(q>p\) with odd \(w_q\). LTE then requires \(q\mid r\) to repair its parity, contradicting maximality. It follows that no admissible odd multiplier contains an active inert prime. More precisely, with the initial 2-adic parity held fixed, admissibility is equivalent to even \(w_p\) at every active \(p\). Necessity follows by the maximality argument and LTE; sufficiency follows because any active inert divisor of \(r\) would force an active odd \(w_q\). In particular, the admissible odd indices are divisor-closed.

An attempted finite closed support containing an initial odd-valuation witness must keep adding larger primes, since \(D_{i+1}=p_iD_i\) remains supported and \(2D_{i+1}>(2D_i)^2\). For the seed \((5,3)\), \(\Phi_5\) and \(\Phi_{49}\) give the first odd witnesses in the two branches. **Every odd multiplier divisible by 5 or by 49 therefore fails, regardless of finite repairs.** The first seventh lift still works. The replay shows the \(\Phi_{55}\) factorization and actual two-prime repairs that are defeated by the next layer. This proves closure growth through mixed indices; it does not require any assertion about further pure \(5^j\) or \(7^j\) shells, and it does not enlarge the generated catalogue.

~~~python
from math import gcd, isqrt, prod

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

def order(p,t,qs):
    z = 5*pow(3,-1,p)%p
    assert pow(z,t,p) == 1 and all(pow(z,t//q,p) != 1 for q in qs)

def v_at(r,p):
    j = 1
    while pow(5,2*r,p**j) == pow(3,2*r,p**j):
        j += 1
    return j-1

assert 5**2-3**2 == 2**2+3*2**2
assert (5**7-3**7)//2 == 137**2+3*80**2
assert (5**7+3**7)//8 == 74**2+3*39**2

assert (5**5-3**5)//2 == 11*131
for p in (11,131):
    assert prime(p) and p%3 == 2 and v_at(5,p) == 1
    order(p,5,(5,))

H = (5**55-3**55)*2//((5**5-3**5)*(5**11-3**11))
q = 2677154441795220311
fac = (2,5,7,11,1289,2697303297427)
# Lucas primality certificate for q.
assert prod(fac) == q-1 and all(prime(p) for p in fac)
assert pow(7,q-1,q) == 1
assert all(gcd(pow(7,(q-1)//p,q)-1,q) == 1 for p in fac)
assert H == 11*3191*42131*q and H%6 == 1
assert prime(3191) and prime(42131)
for p in (3191,42131,q):
    assert p%3 == 2 and H%(p*p) != 0
    order(p,55,(5,11))
assert [v_at(5*11*131,p) for p in (11,131,3191)] == [2,2,1]
assert 55*3191 == 175505

for p in (197,6236819):
    assert prime(p) and p%3 == 2 and v_at(49,p) == 1
    order(p,49,(7,))
    assert v_at(49*197*6236819,p) == 2
assert 49*197 == 9653
print("PASS")
~~~
