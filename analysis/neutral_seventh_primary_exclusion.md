# Exact seventh-primary exclusion at the neutral source (17,188)

This is an exact negative for a family of target traces in a fixed finite left window. It does not factor the source, rule out other common odd components, or test the pointwise A303656 conjecture.

Let \(C_j\) be the trace recurrence \(C_0=2,C_1=t,C_{j+1}=tC_j-C_{j-1}\). At an odd prime, roots \(U,V\) with traces \(2z,2/z\) respectively have orders dividing \(p-1\) or \(p+1\); this follows from the two roots of each reciprocal quadratic lying in \(\mathbb F_p\) or being interchanged by Frobenius. If \(m=\operatorname{ord}U,\ n=\operatorname{ord}V,\ g=\gcd(m,n)\), the trace \(C_b(2/z)\) has a nondegenerate match at some unrestricted positive left exponent exactly when
\[
 \frac n g\mid b,\qquad \frac n{\gcd(n,2)}\nmid b.
\]
Equality of reciprocal quadratic traces means equality or inversion of roots. Thus \(V^b\) must belong to the common subgroup of size \(g\) and must not be \(1\) or \(-1\). This tests a fixed \(b\) without claiming a finite list of \(b\)'s suffices across primes.

For the actual \((17,188)\) modulus \(R\) below, put \(H=2^{19}\) and \(E=7^{49}\operatorname{lcm}\{a\le H:7\nmid a\}\). Since \(R+1<7^{50}\), the 7-primary component of each local order divides \(7^{49}\). If \(U^a\) had 7-power order for some \(1\le a\le H\) at a prime \(p\mid R\), the prime-to-7 part of its original order would divide \(a\). Thus the full order would divide \(E\), and \(p\) would divide \(C_E(2z)-2\). The exact gcd is 1, so no such left power, and therefore no 7-primary target trace, can hit in the stated window. The same elimination holds for left powers of \(V\). The exponent in the independent computation is constructed by 43,389 prime-power factors in addition to \(7^{49}\), and has 756,778 bits.

A positive comparator is the actual source \((10,176)\): \(b=196\) gives a nontrivial order-seven trace at the prime factor 1373, and its first left hit is exactly 56. Moving the cap down to 55, or the target index to 1 at cap 56, removes every hit.

~~~python
from math import gcd, isqrt, prod

def trace(t,e,mod):
    a,b=2,t%mod
    for bit in bin(e)[2:]:
        c=(a*b-t)%mod
        a,b=((a*a-2)%mod,c) if bit=='0' else (c,(b*b-2)%mod)
    return a

R=626751537547263614426465772417729978972491
z=pow(252568635021313874012910903862214825457075,172,R)
assert pow(z,33,R)==(z+1)%R and R+1<7**50 and R%2
H=2**19
sieve=bytearray(b'\1')*(H+1)
sieve[:2]=b'\0\0'
for p in range(2,1+isqrt(H)):
    if sieve[p]:
        sieve[p*p::p]=b'\0'*((H-p*p)//p+1)
def pp(p):
    q=p
    while q*p<=H:
        q*=p
    return q
es=[pp(p) for p in range(2,H+1) if sieve[p] and p!=7]
E=7**49*prod(es)
assert len(es)==43389 and E.bit_length()==756778
assert [gcd(R,trace(t,E,R)-2) for t in [2*z,2*pow(z,-1,R)]]==[1,1]

M=60673898377
z=pow(56617887735,172,M)
t=trace(2*pow(z,-1,M),196,M)
assert gcd(M,t**3+t*t-2*t-1)==1373
assert gcd(1373,t*t-4)==1
hits=[(a,gcd(M,trace(2*z,a,M)-t)) for a in range(1,57)]
assert [(a,g) for a,g in hits if g!=1]==[(56,1373)]
t=trace(2*pow(z,-1,M),1,M)
assert all(gcd(M,trace(2*z,a,M)-t)==1 for a in range(1,57))
~~~
